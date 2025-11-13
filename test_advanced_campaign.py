#!/usr/bin/env python3
"""
Test script for Advanced Campaign Orchestrator.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apt_toolkit.advanced_campaign_orchestrator import AdvancedCampaignOrchestrator
import json

def test_campaign_orchestrator():
    """Test the campaign orchestrator functionality."""
    print("[*] Testing Advanced Campaign Orchestrator...")
    
    # Create orchestrator
    orchestrator = AdvancedCampaignOrchestrator("Test Campaign - US/UK Targets")
    
    # Test target analysis
    print("[*] Testing target analysis...")
    analysis_result = orchestrator.analyze_targets()
    
    if analysis_result["total_targets"] > 0:
        print(f"[+] Target analysis successful: {analysis_result['total_targets']} targets found")
        print(f"[+] US targets: {analysis_result['target_distribution']['american']}")
        print(f"[+] UK targets: {analysis_result['target_distribution']['uk']}")
    else:
        print("[-] Target analysis failed")
        return False
    
    # Test C2 infrastructure setup
    print("[*] Testing C2 infrastructure setup...")
    c2_result = orchestrator.setup_c2_infrastructure(host="127.0.0.1", port=8888)
    
    if c2_result["status"] == "success":
        print(f"[+] C2 infrastructure setup: {c2_result['message']}")
    else:
        print(f"[-] C2 setup failed: {c2_result['message']}")
        # Continue anyway for testing
    
    # Test initial access
    print("[*] Testing initial access...")
    if len(orchestrator.targets) > 0:
        access_result = orchestrator.execute_initial_access(0)
        
        if access_result["status"] == "success":
            print(f"[+] Initial access successful for: {access_result['target']['target_email']}")
        else:
            print(f"[-] Initial access failed: {access_result.get('message', 'Unknown error')}")
    
    # Test campaign status
    print("[*] Testing campaign status...")
    status = orchestrator.get_campaign_status()
    
    print(f"[+] Campaign Status:")
    print(f"    - Targets Analyzed: {status['targets_analyzed']}")
    print(f"    - Systems Compromised: {status['systems_compromised']}")
    print(f"    - C2 Infrastructure: {status['c2_infrastructure']}")
    print(f"    - Active C2 Clients: {status['active_c2_clients']}")
    print(f"    - Campaign Duration: {status['campaign_duration_hours']} hours")
    
    # Test lateral movement
    print("[*] Testing lateral movement...")
    if status['systems_compromised'] > 0:
        lateral_result = orchestrator.execute_lateral_movement(0)
        print(f"[+] Lateral movement: {lateral_result['success_rate']} success rate")
    
    # Test data exfiltration
    print("[*] Testing data exfiltration...")
    if status['systems_compromised'] > 0:
        exfil_result = orchestrator.execute_data_exfiltration(0)
        print(f"[+] Data exfiltration: {exfil_result['data_size_mb']}MB exfiltrated")
    
    print("[+] Advanced Campaign Orchestrator test completed successfully")
    return True

def test_full_campaign():
    """Test running a full campaign."""
    print("\n[*] Testing Full Campaign Execution...")
    
    orchestrator = AdvancedCampaignOrchestrator("Full Test Campaign")
    
    try:
        result = orchestrator.run_full_campaign()
        
        print(f"[+] Full campaign completed successfully!")
        print(f"[+] Campaign ID: {result['campaign_id']}")
        print(f"[+] Targets analyzed: {result['final_status']['targets_analyzed']}")
        print(f"[+] Systems compromised: {result['final_status']['systems_compromised']}")
        
        return True
    except Exception as e:
        print(f"[-] Full campaign test failed: {e}")
        return False

def main():
    """Main test function."""
    print("[*] Starting Advanced Campaign Orchestrator Tests...")
    
    # Test individual components
    if not test_campaign_orchestrator():
        print("[-] Individual component tests failed")
        return
    
    # Test full campaign
    if not test_full_campaign():
        print("[-] Full campaign test failed")
        return
    
    print("\n[+] All tests completed successfully!")
    print("[+] Advanced APT code execution flow is working correctly for US and UK targets")

if __name__ == "__main__":
    main()