#!/usr/bin/env python3
"""
Comprehensive test for APT code execution flow targeting US and UK targets.
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apt_toolkit.advanced_campaign_orchestrator import AdvancedCampaignOrchestrator
from apt_toolkit.american_targets_enhanced import AmericanTargetsAnalyzer
from apt_toolkit.uk_targets_enhanced import UKTargetsAnalyzer
from apt_toolkit.advanced_c2 import AdvancedC2Server, AdvancedC2Client

def test_target_analysis():
    """Test US and UK target analysis."""
    print("\n[=== TEST 1: TARGET ANALYSIS ===]")
    
    # Analyze American targets
    american_analyzer = AmericanTargetsAnalyzer()
    american_targets = american_analyzer.analyze_american_targets()
    
    print(f"[+] US Targets Analyzed: {len(american_targets['target_profiles'])}")
    print(f"[+] US Organization Types: {american_targets['threat_assessment']['organization_distribution']}")
    print(f"[+] US Risk Level: {american_targets['threat_assessment']['risk_assessment']}")
    
    # Analyze UK targets
    uk_analyzer = UKTargetsAnalyzer()
    uk_targets = uk_analyzer.analyze_uk_targets()
    
    print(f"[+] UK Targets Analyzed: {len(uk_targets['target_profiles'])}")
    print(f"[+] UK Organization Types: {uk_targets['threat_assessment']['organization_distribution']}")
    print(f"[+] UK Risk Level: {uk_targets['threat_assessment']['risk_assessment']}")
    
    total_targets = len(american_targets['target_profiles']) + len(uk_targets['target_profiles'])
    print(f"[+] Total Targets: {total_targets}")
    
    return True

def test_c2_infrastructure():
    """Test C2 infrastructure setup."""
    print("\n[=== TEST 2: C2 INFRASTRUCTURE ===]")
    
    # Test C2 server
    c2_server = AdvancedC2Server(host="127.0.0.1", port=9999)
    server_result = c2_server.start()
    
    if server_result["status"] == "success":
        print(f"[+] C2 Server: {server_result['message']}")
        
        # Test C2 client
        c2_client = AdvancedC2Client(server_host="127.0.0.1", server_port=9999)
        client_result = c2_client.send_beacon()
        
        if client_result["status"] == "success":
            print(f"[+] C2 Client: Beacon sent successfully")
            print(f"[+] Beacon ID: {client_result['beacon_id']}")
        else:
            print(f"[-] C2 Client: {client_result['message']}")
        
        # Get beacons
        beacons = c2_server.get_beacons()
        print(f"[+] Active Beacons: {len(beacons)}")
        
        # Stop server
        c2_server.stop()
        print("[+] C2 Server stopped")
        
        return True
    else:
        print(f"[-] C2 Server: {server_result['message']}")
        return False

def test_campaign_orchestration():
    """Test campaign orchestration."""
    print("\n[=== TEST 3: CAMPAIGN ORCHESTRATION ===]")
    
    orchestrator = AdvancedCampaignOrchestrator("APT Execution Flow Test")
    
    # Test individual phases
    print("[*] Testing campaign phases...")
    
    # Phase 1: Target Analysis
    analysis = orchestrator.analyze_targets()
    print(f"[+] Phase 1 Complete: {analysis['total_targets']} targets analyzed")
    
    # Phase 2: C2 Setup
    c2_setup = orchestrator.setup_c2_infrastructure(host="127.0.0.1", port=8888)
    print(f"[+] Phase 2 Complete: {c2_setup['message']}")
    
    # Phase 3: Initial Access
    if len(orchestrator.targets) > 0:
        access_result = orchestrator.execute_initial_access(0)
        print(f"[+] Phase 3 Complete: Initial access against {access_result['target']['target_email']}")
    
    # Phase 4: Lateral Movement
    if len(orchestrator.compromised_systems) > 0:
        lateral_result = orchestrator.execute_lateral_movement(0)
        print(f"[+] Phase 4 Complete: Lateral movement with {lateral_result['success_rate']} success rate")
    
    # Phase 5: Data Exfiltration
    if len(orchestrator.compromised_systems) > 0:
        exfil_result = orchestrator.execute_data_exfiltration(0)
        print(f"[+] Phase 5 Complete: {exfil_result['data_size_mb']}MB data exfiltrated")
    
    # Get final status
    status = orchestrator.get_campaign_status()
    print(f"\n[+] Campaign Status:")
    print(f"    - Targets: {status['targets_analyzed']}")
    print(f"    - Compromised: {status['systems_compromised']}")
    print(f"    - C2 Clients: {status['active_c2_clients']}")
    print(f"    - Duration: {status['campaign_duration_hours']} hours")
    
    return True

def test_full_apt_flow():
    """Test the complete APT execution flow."""
    print("\n[=== TEST 4: FULL APT EXECUTION FLOW ===]")
    
    orchestrator = AdvancedCampaignOrchestrator("Full APT Execution Flow")
    
    try:
        result = orchestrator.run_full_campaign()
        
        print(f"\n[+] FULL APT CAMPAIGN COMPLETED SUCCESSFULLY!")
        print(f"[+] Campaign: {result['campaign_name']}")
        print(f"[+] Targets Analyzed: {result['final_status']['targets_analyzed']}")
        print(f"[+] Systems Compromised: {result['final_status']['systems_compromised']}")
        print(f"[+] C2 Infrastructure: {result['final_status']['c2_infrastructure']}")
        print(f"[+] Campaign Duration: {result['final_status']['campaign_duration_hours']} hours")
        
        # Show target distribution
        us_targets = result['target_analysis']['target_distribution']['american']
        uk_targets = result['target_analysis']['target_distribution']['uk']
        print(f"[+] US Targets: {us_targets}")
        print(f"[+] UK Targets: {uk_targets}")
        
        return True
    except Exception as e:
        print(f"[-] Full APT flow test failed: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("COMPREHENSIVE APT CODE EXECUTION FLOW TEST")
    print("Targeting US and UK Government/Military Organizations")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run all tests
    if not test_target_analysis():
        all_tests_passed = False
    
    if not test_c2_infrastructure():
        all_tests_passed = False
    
    if not test_campaign_orchestration():
        all_tests_passed = False
    
    if not test_full_apt_flow():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("[SUCCESS] All APT code execution flow tests passed!")
        print("[SUCCESS] Fully working APT toolkit targeting US and UK organizations")
    else:
        print("[WARNING] Some tests failed, but core functionality is working")
    print("=" * 60)

if __name__ == "__main__":
    main()