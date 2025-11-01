"""
APT1 (Comment Crew) Campaign Simulation

Simulates campaigns by APT1, one of the most prolific Chinese APT groups known for:
- Long-term cyber espionage campaigns
- Government and defense industry targeting
- Extensive use of custom malware
- Sophisticated command and control infrastructure
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from apt_toolkit.campaign import CampaignConfig, APTCampaignSimulator
from apt_toolkit.initial_access_enhanced import AdvancedSocialEngineering
from apt_toolkit.persistence_enhanced import AdvancedPersistenceFramework


@dataclass
class APT1CampaignConfig(CampaignConfig):
    """Extended configuration for APT1-specific campaigns."""
    
    government_targeting: bool = True
    defense_industry: bool = True
    long_term_espionage: bool = True
    custom_malware_families: List[str] = None
    c2_infrastructure_type: str = "bulletproof_hosting"
    
    def __post_init__(self):
        if self.custom_malware_families is None:
            self.custom_malware_families = ["Gh0stRAT", "PoisonIvy", "HydraQ", "BUBBLEWRAP"]


class APT1CampaignSimulator:
    """Specialized simulator for APT1 (Comment Crew) campaigns."""
    
    def __init__(self, seed: Optional[int] = None):
        self._base_seed = seed
        self._base_simulator = APTCampaignSimulator(seed=seed)
        self._social_engineering = AdvancedSocialEngineering()
        self._persistence_framework = AdvancedPersistenceFramework()
    
    def simulate_government_espionage_campaign(self, config: Optional[APT1CampaignConfig] = None) -> Dict[str, Any]:
        """Simulate APT1's signature government espionage campaigns."""
        
        config = config or APT1CampaignConfig()
        seed = config.seed if config.seed is not None else self._base_seed
        if seed is not None:
            random.seed(seed)
        
        # APT1-specific initial access
        initial_access = self._simulate_apt1_initial_access(config)
        
        # APT1-specific persistence
        persistence = self._simulate_apt1_persistence(config)
        
        # APT1-specific C2 infrastructure
        command_control = self._simulate_apt1_command_control(config)
        
        # Standard campaign phases
        base_campaign = self._base_simulator.simulate(config)
        
        # Merge APT1-specific results
        result = {
            "apt_group": "APT1 (Comment Crew)",
            "campaign_type": "Government and Defense Espionage",
            "apt1_specific": {
                "initial_access": initial_access,
                "persistence": persistence,
                "command_control": command_control,
                "malware_families": config.custom_malware_families,
                "espionage_focus": self._get_espionage_focus(config)
            },
            **base_campaign
        }
        
        return result
    
    def _simulate_apt1_initial_access(self, config: APT1CampaignConfig) -> Dict[str, Any]:
        """Simulate APT1's unique initial access techniques."""
        
        # Government and defense targeting
        if config.government_targeting:
            target_emails = [
                f"policy.analyst@{config.target_domain}",
                f"defense.contractor@{config.target_domain}",
                f"intelligence.officer@{config.target_domain}",
                f"research.scientist@{config.target_domain}"
            ]
        else:
            target_emails = [f"admin@{config.target_domain}"]
        
        # APT1's social engineering themes
        social_engineering_themes = [
            "Policy briefing documents",
            "Defense contract opportunities",
            "Intelligence community alerts",
            "Research collaboration invitations",
            "Government procurement notices"
        ]
        
        # Spear-phishing payload types
        payload_types = [
            "Malicious PDF documents with embedded exploits",
            "Office documents with macro malware",
            "Compressed archives with executable payloads",
            "Link to compromised government websites"
        ]
        
        return {
            "target_emails": target_emails,
            "social_engineering_themes": social_engineering_themes,
            "payload_types": payload_types,
            "attack_vectors": [
                "Spear-phishing emails with malicious attachments",
                "Watering hole attacks on government portals",
                "Compromised third-party vendor software",
                "Strategic web compromises"
            ]
        }
    
    def _simulate_apt1_persistence(self, config: APT1CampaignConfig) -> Dict[str, Any]:
        """Simulate APT1's persistence mechanisms."""
        
        # Long-term persistence mechanisms
        persistence_techniques = []
        
        # Windows service persistence
        service_persistence = {"technique": "Windows Service", "description": "Malware runs as system service"}
        persistence_techniques.append(service_persistence)
        
        # Registry persistence
        registry_persistence = {"technique": "Registry Run Keys", "description": "Persistence via registry autorun"}
        persistence_techniques.append(registry_persistence)
        
        # Scheduled task persistence
        task_persistence = {"technique": "Scheduled Task", "description": "Regular execution via task scheduler"}
        persistence_techniques.append(task_persistence)
        
        # WMI persistence
        wmi_persistence = {"technique": "WMI Event Subscription", "description": "Permanent WMI event consumers"}
        persistence_techniques.append(wmi_persistence)
        
        return {
            "persistence_techniques": persistence_techniques,
            "long_term_focus": config.long_term_espionage,
            "malware_rotation": {
                "multiple_backdoors": True,
                "regular_updates": True,
                "fallback_mechanisms": True
            }
        }
    
    def _simulate_apt1_command_control(self, config: APT1CampaignConfig) -> Dict[str, Any]:
        """Simulate APT1's sophisticated C2 infrastructure."""
        
        # C2 infrastructure types
        c2_infrastructure = {
            "primary_c2": {
                "type": config.c2_infrastructure_type,
                "characteristics": [
                    "Bulletproof hosting providers",
                    "Compromised legitimate websites",
                    "Dynamic DNS services",
                    "Cloud infrastructure"
                ]
            },
            "communication_protocols": [
                "HTTP/HTTPS with custom encryption",
                "DNS tunneling for stealth",
                "ICMP for network evasion",
                "Custom TCP protocols"
            ],
            "infrastructure_management": {
                "fast_flux_dns": True,
                "domain_generation_algorithms": True,
                "regular_infrastructure_rotation": True,
                "redundant_c2_channels": True
            }
        }
        
        # Beacon communication patterns
        beacon_patterns = {
            "beacon_intervals": "Variable (30 minutes to 8 hours)",
            "data_exfiltration": "Encrypted chunks during off-peak hours",
            "command_execution": "Delayed to avoid detection",
            "infrastructure_failover": "Automatic switching to backup C2"
        }
        
        return {
            "c2_infrastructure": c2_infrastructure,
            "beacon_patterns": beacon_patterns,
            "operational_security": {
                "geographic_diversity": True,
                "provider_diversity": True,
                "protocol_diversity": True,
                "regular_infrastructure_refresh": True
            }
        }
    
    def _get_espionage_focus(self, config: APT1CampaignConfig) -> Dict[str, Any]:
        """Define APT1's espionage focus areas."""
        
        espionage_targets = []
        
        if config.government_targeting:
            espionage_targets.extend([
                "Government policy documents",
                "Diplomatic communications",
                "Legislative research",
                "Administrative records"
            ])
        
        if config.defense_industry:
            espionage_targets.extend([
                "Defense contract specifications",
                "Weapons system designs",
                "Military technology research",
                "Defense procurement plans"
            ])
        
        return {
            "intelligence_priorities": espionage_targets,
            "collection_methods": [
                "Document exfiltration",
                "Email harvesting",
                "Database access",
                "Network reconnaissance"
            ],
            "data_processing": {
                "on_target_filtering": True,
                "encrypted_storage": True,
                "compression_before_exfiltration": True,
                "staged_exfiltration": True
            }
        }
    
    def simulate_long_term_campaign(self, duration_days: int = 365, config: Optional[APT1CampaignConfig] = None) -> Dict[str, Any]:
        """Simulate APT1's long-term espionage campaign."""
        
        config = config or APT1CampaignConfig()
        
        # Run the main simulation
        base_report = self.simulate_government_espionage_campaign(config)
        
        # Add long-term campaign details
        campaign_phases = {
            "phase_1_reconnaissance": {
                "duration": "1-2 weeks",
                "activities": [
                    "Target identification and profiling",
                    "Network reconnaissance",
                    "Social media intelligence gathering",
                    "Technical vulnerability assessment"
                ]
            },
            "phase_2_initial_compromise": {
                "duration": "1-4 weeks", 
                "activities": [
                    "Spear-phishing campaign execution",
                    "Watering hole establishment",
                    "Initial payload delivery",
                    "First-stage backdoor deployment"
                ]
            },
            "phase_3_consolidation": {
                "duration": "2-8 weeks",
                "activities": [
                    "Lateral movement within network",
                    "Privilege escalation",
                    "Additional persistence mechanisms",
                    "Secondary backdoor deployment"
                ]
            },
            "phase_4_espionage_operations": {
                "duration": f"{duration_days - 12} weeks",
                "activities": [
                    "Continuous data collection",
                    "Regular exfiltration operations",
                    "Infrastructure maintenance",
                    "Malware updates and evolution"
                ]
            },
            "phase_5_cleanup": {
                "duration": "1-2 weeks",
                "activities": [
                    "Evidence removal",
                    "Log cleaning",
                    "Infrastructure takedown",
                    "Operational security review"
                ]
            }
        }
        
        # Merge with base report
        result = {
            **base_report,
            "campaign_type": "Long-Term Espionage Operation",
            "total_duration_days": duration_days,
            "campaign_phases": campaign_phases,
            "operational_characteristics": {
                "low_and_slow": True,
                "persistent_presence": True,
                "multiple_compromise_vectors": True,
                "continuous_intelligence_collection": True
            }
        }
        
        return result