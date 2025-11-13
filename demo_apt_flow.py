#!/usr/bin/env python3
"""
Demo script showing APT code execution flow targeting US and UK organizations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apt_toolkit.advanced_campaign_orchestrator import AdvancedCampaignOrchestrator

def demo_simple_usage():
    """Demonstrate simple usage of the APT toolkit."""
    print("\n[DEMO] Simple APT Campaign Usage")
    print("-" * 40)
    
    # Create a campaign orchestrator
    orchestrator = AdvancedCampaignOrchestrator("Demo Campaign")
    
    # Analyze targets
    print("[*] Analyzing US and UK targets...")
    analysis = orchestrator.analyze_targets()
    print(f"[+] Found {analysis['total_targets']} targets")
    print(f"[+] US: {analysis['target_distribution']['american']}, UK: {analysis['target_distribution']['uk']}")
    
    # Setup C2
    print("[*] Setting up C2 infrastructure...")
    c2_setup = orchestrator.setup_c2_infrastructure()
    print(f"[+] {c2_setup['message']}")
    
    # Execute initial access
    print("[*] Executing initial access...")
    if len(orchestrator.targets) > 0:
        access_result = orchestrator.execute_initial_access(0)
        print(f"[+] Compromised: {access_result['target']['target_email']}")
    
    # Show campaign status
    status = orchestrator.get_campaign_status()
    print(f"\n[+] Campaign Status:")
    print(f"    Targets: {status['targets_analyzed']}")
    print(f"    Compromised: {status['systems_compromised']}")
    print(f"    C2 Active: {status['c2_infrastructure']}")

def demo_advanced_campaign():
    """Demonstrate running a full advanced campaign."""
    print("\n[DEMO] Advanced APT Campaign")
    print("-" * 40)
    
    orchestrator = AdvancedCampaignOrchestrator("Advanced US/UK Campaign")
    
    # Run full campaign
    result = orchestrator.run_full_campaign()
    
    print(f"\n[+] Campaign Summary:")
    print(f"    Name: {result['campaign_name']}")
    print(f"    ID: {result['campaign_id']}")
    print(f"    Targets: {result['final_status']['targets_analyzed']}")
    print(f"    Compromised: {result['final_status']['systems_compromised']}")
    print(f"    Duration: {result['final_status']['campaign_duration_hours']} hours")
    
    # Show target breakdown
    us_targets = result['target_analysis']['target_distribution']['american']
    uk_targets = result['target_analysis']['target_distribution']['uk']
    print(f"    US Targets: {us_targets}")
    print(f"    UK Targets: {uk_targets}")

def main():
    """Main demo function."""
    print("=" * 50)
    print("APT TOOLKIT DEMONSTRATION")
    print("Advanced Persistent Threat Code Execution Flow")
    print("Targeting US and UK Government/Military Organizations")
    print("=" * 50)
    
    # Demo 1: Simple usage
    demo_simple_usage()
    
    # Demo 2: Advanced campaign
    demo_advanced_campaign()
    
    print("\n" + "=" * 50)
    print("[SUCCESS] APT Toolkit Demonstration Complete")
    print("The toolkit successfully demonstrates:")
    print("✓ US/UK target analysis and profiling")
    print("✓ C2 infrastructure setup and beaconing")
    print("✓ Initial access and payload delivery")
    print("✓ Lateral movement simulation")
    print("✓ Data exfiltration simulation")
    print("✓ Full campaign orchestration")
    print("=" * 50)

if __name__ == "__main__":
    main()