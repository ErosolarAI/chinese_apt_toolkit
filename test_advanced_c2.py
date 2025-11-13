#!/usr/bin/env python3
"""
Test script for Advanced C2 functionality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apt_toolkit.advanced_c2 import AdvancedC2Server, AdvancedC2Client
import time
import threading

def test_c2_server():
    """Test the C2 server functionality."""
    print("[*] Testing C2 Server...")
    
    # Create and start server
    server = AdvancedC2Server(host="127.0.0.1", port=8888)
    result = server.start()
    
    if result["status"] == "success":
        print(f"[+] Server started: {result['message']}")
        
        # Wait for connections
        time.sleep(2)
        
        # Get beacons
        beacons = server.get_beacons()
        print(f"[+] Active beacons: {len(beacons)}")
        
        # Stop server
        server.stop()
        print("[+] Server stopped")
        
        return True
    else:
        print(f"[-] Failed to start server: {result['message']}")
        return False

def test_c2_client():
    """Test the C2 client functionality."""
    print("[*] Testing C2 Client...")
    
    # Create client
    client = AdvancedC2Client(
        server_host="127.0.0.1",
        server_port=8888
    )
    
    # Send beacon
    result = client.send_beacon()
    
    if result["status"] == "success":
        print(f"[+] Beacon sent: {result['message']}")
        print(f"[+] Beacon ID: {result['beacon_id']}")
        print(f"[+] Command received: {result['command_received']}")
        return True
    else:
        print(f"[-] Beacon failed: {result['message']}")
        return False

def main():
    """Main test function."""
    print("[*] Starting Advanced C2 Tests...")
    
    # Test server
    if not test_c2_server():
        print("[-] Server test failed")
        return
    
    # Test client (server won't be running, so this should fail gracefully)
    test_c2_client()
    
    print("[*] Tests completed")

if __name__ == "__main__":
    main()