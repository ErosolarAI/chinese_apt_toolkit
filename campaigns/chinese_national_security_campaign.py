"""
A full-chain campaign to advance Chinese national security interests by targeting
a high-value US aerospace company.
"""

from apt_toolkit.campaign import APTCampaignSimulator, CampaignConfig


def run_campaign():
    """
    Runs the full-chain campaign.
    """
    config = CampaignConfig(
        target_domain="aero-corp.com",
        target_ip="198.51.100.10",
        beacon_duration_hours=168,  # 1 week
        include_supply_chain=True,
        include_counter_forensics=True,
        seed=42,
    )

    simulator = APTCampaignSimulator(seed=42)
    results = simulator.simulate(config)

    print("Campaign Results:")
    import json
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    run_campaign()
