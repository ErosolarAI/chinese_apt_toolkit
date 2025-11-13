"""
Additional interactive shell commands for non-blocked initial access techniques.
This file should be merged into the main interactive_shell.py
"""

import json
import textwrap

# Add these imports to the main interactive_shell.py imports section:
# from .initial_access_non_blocked import NonBlockedInitialAccess

# Add these command help entries to COMMAND_HELP:
NON_BLOCKED_COMMAND_HELP = {
    "non_blocked_techniques": {
        "category": "Initial Access",
        "summary": "List non-blocked initial access techniques that bypass Microsoft Defender.",
        "usage": ["non_blocked_techniques"],
        "details": textwrap.dedent(
            """
            Displays all available initial access techniques that are not blocked
            by Microsoft Defender as of 2022 (macros are blocked). Includes:
            • LNK file attacks
            • HTML smuggling
            • ISO container attacks
            • Living-off-the-land techniques
            • Browser exploit delivery
            """
        ).strip(),
    },
    "generate_attack_plan": {
        "category": "Initial Access",
        "summary": "Generate comprehensive attack plan using non-blocked techniques.",
        "usage": ["generate_attack_plan example.com"],
        "details": textwrap.dedent(
            """
            Creates a multi-vector attack plan using techniques that bypass
            Microsoft Defender's macro blocking. The plan includes multiple
            attack vectors for increased success probability.
            """
        ).strip(),
    },
}

# Add these methods to the APTToolkitShell class:
NON_BLOCKED_SHELL_METHODS = """
    def do_non_blocked_techniques(self, arg: str) -> None:
        \"\"\"List non-blocked initial access techniques.\"\"\"
        try:
            techniques = self.non_blocked_access.get_available_techniques()
            print("\\nNon-Blocked Initial Access Techniques (Bypass Microsoft Defender):\\n")
            for i, technique in enumerate(techniques, 1):
                print(f"{i}. {technique['name']}")
                print(f"   Description: {technique['description']}")
                print(f"   Evasion Level: {technique['evasion_level']}")
                print(f"   Success Rate: {technique['success_rate']}")
                print(f"   User Interaction: {technique['user_interaction']}\\n")
        except Exception as e:
            print(f"Error retrieving techniques: {e}")

    def do_generate_attack_plan(self, arg: str) -> None:
        \"\"\"Generate attack plan using non-blocked techniques.\"\"\"
        target_domain = arg.strip() if arg.strip() else "example.com"
        try:
            attack_plan = self.non_blocked_access.generate_attack_plan(target_domain)
            print(f"\\nAttack Plan for {target_domain} (Non-Blocked Techniques):\\n")
            print(json.dumps(attack_plan, indent=2))
        except Exception as e:
            print(f"Error generating attack plan: {e}")
"""