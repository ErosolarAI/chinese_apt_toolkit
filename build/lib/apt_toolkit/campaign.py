"""Campaign orchestration utilities for the APT Toolkit.

This module connects the standalone primitives (initial access, persistence,
privilege escalation, defense evasion, lateral movement, command and control,
and exfiltration) into a coherent end-to-end campaign simulator. The output is
conceptual and intended for defensive research, purple teaming exercises, and
training scenarios only.
"""

from __future__ import annotations

import hashlib
import ipaddress
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .defense_evasion import DefenseEvader
from .exfiltration import DataExfiltrator
from .lateral_movement import LateralMover
from .privilege_escalation import PrivilegeEscalator
from .exploit_intel import enrich_with_exploit_intel


@dataclass
class CampaignConfig:
    """Configuration options for a simulated APT campaign."""

    target_domain: str = "secure.dod.mil"
    target_ip: str = "203.0.113.10"
    beacon_duration_hours: int = 48
    include_supply_chain: bool = True
    include_counter_forensics: bool = True
    seed: Optional[int] = None


class APTCampaignSimulator:
    """Orchestrate the toolkit's primitives into a full campaign narrative."""

    def __init__(self, seed: Optional[int] = None):
        self._base_seed = seed
        self._privilege_escalator = PrivilegeEscalator()
        self._defense_evader = DefenseEvader()
        self._exfiltrator = DataExfiltrator()

    def simulate(self, config: Optional[CampaignConfig] = None) -> Dict[str, Any]:
        """Run the end-to-end simulation and return a structured report."""

        config = config or CampaignConfig()
        seed = config.seed if config.seed is not None else self._base_seed
        if seed is not None:
            random.seed(seed)

        initial_access = self._simulate_initial_access(config)
        persistence = self._simulate_persistence(config)
        privilege_escalation = self._simulate_privilege_escalation(config)
        defense_evasion = self._simulate_defense_evasion()
        lateral_movement = self._simulate_lateral_movement(
            privilege_escalation, config
        )
        command_control = self._simulate_command_control(config)
        exfiltration = self._simulate_exfiltration()

        timeline = self._build_timeline(
            initial_access,
            persistence,
            privilege_escalation,
            defense_evasion,
            lateral_movement,
            command_control,
            exfiltration,
        )

        return {
            "config": config.__dict__,
            "initial_access": initial_access,
            "persistence": persistence,
            "privilege_escalation": privilege_escalation,
            "defense_evasion": defense_evasion,
            "lateral_movement": lateral_movement,
            "command_control": command_control,
            "exfiltration": exfiltration,
            "campaign_timeline": timeline,
            "key_takeaways": self._summarize_takeaways(
                initial_access,
                persistence,
                privilege_escalation,
                lateral_movement,
                exfiltration,
            ),
        }

    # ------------------------------------------------------------------
    # Phase simulators

    def _simulate_initial_access(self, config: CampaignConfig) -> Dict[str, Any]:
        """Simulate initial access phase."""
        target_email = f"admin@{config.target_domain}"
        result = {
            "target_domain": config.target_domain,
            "target_ip": config.target_ip,
            "target_email": target_email,
            "technique": "Simulated Initial Access",
            "success": True,
            "description": "Simulated initial access for campaign demonstration"
        }
        
        # Add supply chain if enabled
        if config.include_supply_chain:
            result["supply_chain"] = {
                "status": "Simulated supply chain compromise",
                "description": "Simulated supply chain attack vector"
            }
        else:
            result["supply_chain"] = None
            
        return enrich_with_exploit_intel(
            "initial-access",
            result,
            search_terms=[config.target_domain, "initial access"],
            platform="windows",
            include_payloads=True,
        )

    def _simulate_persistence(self, config: CampaignConfig) -> Dict[str, Any]:
        """Simulate persistence phase."""
        result = {
            "technique": "Simulated Persistence",
            "mechanisms": ["Scheduled Task", "Registry Run Key"],
            "success": True,
            "description": "Simulated persistence mechanisms for campaign demonstration"
        }
        
        # Add counter forensics if enabled
        if config.include_counter_forensics:
            result["counter_forensics"] = {
                "status": "Simulated counter forensics",
                "description": "Simulated counter forensics measures"
            }
        else:
            result["counter_forensics"] = None
            
        return enrich_with_exploit_intel(
            "persistence",
            result,
            search_terms=["persistence", "scheduled task"],
            platform="windows",
            include_payloads=True,
        )

    def _simulate_privilege_escalation(self, config: CampaignConfig) -> Dict[str, Any]:
        """Simulate privilege escalation phase."""
        ad_enum = self._privilege_escalator.enumerate_ad_privileges()
        vuln_scan = self._privilege_escalator.check_vulnerabilities(
            f"dc1.{config.target_domain}"
        )

        result = {
            "active_directory": {
                "enumeration": ad_enum,
                "vulnerabilities": vuln_scan,
            },
            "technique": "Simulated Privilege Escalation",
            "success": True
        }
        return enrich_with_exploit_intel(
            "privilege-escalation",
            result,
            search_terms=[config.target_domain, "privilege escalation"],
            platform="windows",
            include_payloads=True,
        )

    def _simulate_defense_evasion(self) -> Dict[str, Any]:
        """Simulate defense evasion phase."""
        lotl = self._defense_evader.generate_lotl_commands()
        lotl_detection = self._defense_evader.analyze_lotl_detection()

        result = {
            "lotl": lotl,
            "lotl_detection": lotl_detection,
            "technique": "Simulated Defense Evasion",
            "success": True
        }
        return enrich_with_exploit_intel(
            "defense-evasion",
            result,
            search_terms=["lotl", "defense evasion"],
            platform="windows",
            include_payloads=True,
        )

    def _simulate_lateral_movement(
        self, privilege_escalation: Dict[str, Any], config: CampaignConfig
    ) -> Dict[str, Any]:
        """Simulate lateral movement phase."""
        lateral = LateralMover()
        network_map = lateral.discover_network_segments()
        
        # Generate simulated stolen hashes
        stolen_hashes = [
            {
                "username": f"administrator@{config.target_domain}",
                "hash": "aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c"
            },
            {
                "username": f"sqlservice@{config.target_domain}",
                "hash": "aad3b435b51404eeaad3b435b51404ee:1234567890abcdef1234567890abcdef"
            }
        ]

        result = {
            "network_map": network_map,
            "stolen_hashes": stolen_hashes,
            "technique": "Simulated Lateral Movement",
            "success": True,
            "description": "Simulated lateral movement for campaign demonstration"
        }
        return enrich_with_exploit_intel(
            "lateral-movement",
            result,
            search_terms=["lateral movement", config.target_domain],
            platform="windows",
            include_payloads=True,
        )

    def _simulate_command_control(self, config: CampaignConfig) -> Dict[str, Any]:
        """Simulate command and control phase."""
        result = {
            "technique": "Simulated Command and Control",
            "beacon_interval": "60 seconds",
            "channels": ["HTTPS", "DNS"],
            "success": True,
            "description": "Simulated C2 communication for campaign demonstration"
        }
        return enrich_with_exploit_intel(
            "command-control",
            result,
            search_terms=["c2", "beacon"],
            platform=None,
            include_payloads=True,
        )

    def _simulate_exfiltration(self) -> Dict[str, Any]:
        """Simulate exfiltration phase."""
        discovery = self._exfiltrator.find_sensitive_data()
        strategy = self._exfiltrator.generate_exfiltration_strategy(discovery)

        result = {
            "discovery": discovery,
            "strategy": strategy,
            "technique": "Simulated Exfiltration",
            "success": True,
            "description": "Simulated data exfiltration for campaign demonstration"
        }
        return enrich_with_exploit_intel(
            "exfiltration",
            result,
            search_terms=["data exfiltration", "dns", "https"],
            platform="windows",
            include_payloads=True,
        )

    # ------------------------------------------------------------------
    # Helpers

    def _build_timeline(self, *phases: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build a campaign timeline from phase results."""
        timeline = []
        phase_names = [
            "Initial Access", "Persistence", "Privilege Escalation",
            "Defense Evasion", "Lateral Movement", "Command & Control",
            "Exfiltration"
        ]
        
        for i, (phase_name, phase_data) in enumerate(zip(phase_names, phases)):
            timeline.append({
                "phase": phase_name,
                "order": i + 1,
                "status": "Completed",
                "success": phase_data.get("success", True),
                "summary": phase_data.get("description", f"Completed {phase_name} phase")
            })
        
        return timeline

    def _summarize_takeaways(
        self,
        initial_access: Dict[str, Any],
        persistence: Dict[str, Any],
        privilege_escalation: Dict[str, Any],
        lateral_movement: Dict[str, Any],
        exfiltration: Dict[str, Any],
    ) -> List[str]:
        """Summarize key campaign takeaways."""
        takeaways = [
            "Campaign successfully simulated all phases of the attack lifecycle",
            "Demonstrated realistic APT tradecraft and techniques",
            "Highlighted importance of defense-in-depth strategies",
            "Emphasized need for continuous monitoring and detection"
        ]
        return takeaways


def simulate_campaign(config: Optional[CampaignConfig] = None) -> Dict[str, Any]:
    """Convenience function to run a campaign simulation."""
    simulator = APTCampaignSimulator()
    return simulator.simulate(config)