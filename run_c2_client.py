
from apt_toolkit.command_control_real import C2Client
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_client():
    logging.info("Starting C2 client...")
    client = C2Client()
    while True:
        try:
            client.beacon("Client is beaconing")
        except Exception as e:
            logging.error(f"An error occurred during beaconing: {e}")
        time.sleep(5)

if __name__ == "__main__":
    run_client()
