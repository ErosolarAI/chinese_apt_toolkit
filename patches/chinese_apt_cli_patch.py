"""
Script to properly add Chinese APT support to CLI
"""

import re

# Read the original CLI file
with open('apt_toolkit/cli.py', 'r') as f:
    content = f.read()

# Add Chinese APT imports after the campaign import
import_pattern = r'(from \.campaign import APTCampaignSimulator, CampaignConfig)'
chinese_imports = '''from .campaign import APTCampaignSimulator, CampaignConfig

# Chinese APT campaign imports
try:
    from campaigns.chinese_apts.chinese_apt_orchestrator import (
        ChineseAPTCampaignOrchestrator, ChineseAPTCampaignConfig
    )
    CHINESE_APT_SUPPORT = True
except ImportError:
    CHINESE_APT_SUPPORT = False'''

content = re.sub(import_pattern, chinese_imports, content)

# Add Chinese APT subparser after American parser
american_parser_pattern = r'(american_parser = subparsers\.add_parser\(\s*"american",\s*help="U\.S\. government and military targeting simulations",\s*\)\s*american_parser\.add_argument\(\s*"action",\s*choices=\["targets"\],\s*help="Run american targets reconnaissance",\s*\))'
chinese_parser = '''american_parser = subparsers.add_parser(
        "american",
        help="U.S. government and military targeting simulations",
    )
    american_parser.add_argument(
        "action",
        choices=["targets"],
        help="Run american targets reconnaissance",
    )

    # Chinese APT campaigns subparser
    if CHINESE_APT_SUPPORT:
        chinese_parser = subparsers.add_parser(
            "chinese-apt",
            help="Chinese APT campaign simulations (APT41, APT1, APT10, APT12)",
        )
        chinese_parser.add_argument(
            "--campaign",
            choices=[
                "apt41_gaming", "apt41_supply_chain",
                "apt1_government", "apt1_long_term",
                "apt10_msp", "apt10_cloud",
                "apt12_diplomatic", "apt12_strategic",
                "comparative"
            ],
            help="Specific Chinese APT campaign type to simulate",
        )
        chinese_parser.add_argument(
            "--domain",
            default="secure.dod.mil",
            help="Target domain for campaign simulation",
        )
        chinese_parser.add_argument(
            "--seed",
            type=int,
            help="Seed random number generation for deterministic output",
        )'''

content = re.sub(american_parser_pattern, chinese_parser, content, flags=re.DOTALL)

# Update the common arguments section
subparser_list_pattern = r'(for subparser in \[\s*ia_parser,\s*per_parser,\s*pe_parser,\s*de_parser,\s*lm_parser,\s*cc_parser,\s*ex_parser,\s*campaign_parser,\s*exploit_parser,\s*american_parser,\s*\]:)'
updated_subparser_list = '''subparser_list = [
        ia_parser,
        per_parser,
        pe_parser,
        de_parser,
        lm_parser,
        cc_parser,
        ex_parser,
        campaign_parser,
        exploit_parser,
        american_parser,
    ]
    
    if CHINESE_APT_SUPPORT:
        subparser_list.append(chinese_parser)
    
    for subparser in subparser_list:'''

content = re.sub(subparser_list_pattern, updated_subparser_list, content, flags=re.DOTALL)

# Add Chinese APT command handler after campaign handler
campaign_handler_pattern = r'(elif args\.module == "campaign":\s*config = CampaignConfig\(\s*target_domain=args\.domain,\s*target_ip=args\.ip,\s*beacon_duration_hours=args\.hours,\s*include_supply_chain=not args\.skip_supply_chain,\s*include_counter_forensics=not args\.skip_counter_forensics,\s*seed=args\.seed,\s*\)\s*simulator = APTCampaignSimulator\(seed=args\.seed\)\s*return \{"campaign_report": simulator\.simulate\(config\)\})'
chinese_handler = '''elif args.module == "campaign":
        config = CampaignConfig(
            target_domain=args.domain,
            target_ip=args.ip,
            beacon_duration_hours=args.hours,
            include_supply_chain=not args.skip_supply_chain,
            include_counter_forensics=not args.skip_counter_forensics,
            seed=args.seed,
        )
        simulator = APTCampaignSimulator(seed=args.seed)
        return {"campaign_report": simulator.simulate(config)}

    elif args.module == "chinese-apt" and CHINESE_APT_SUPPORT:
        if not args.campaign:
            orchestrator = ChineseAPTCampaignOrchestrator(seed=args.seed)
            return {
                "available_campaigns": orchestrator.get_available_campaign_types(),
                "chinese_apt_overview": orchestrator._get_chinese_apt_overview()
            }
        
        config = ChineseAPTCampaignConfig(
            target_domain=args.domain,
            seed=args.seed
        )
        orchestrator = ChineseAPTCampaignOrchestrator(seed=args.seed)
        
        if args.campaign == "comparative":
            return orchestrator.run_comparative_analysis(config)
        else:
            return orchestrator.simulate_specific_campaign_type(args.campaign, config)

    elif args.module == "chinese-apt" and not CHINESE_APT_SUPPORT:
        return {"error": "Chinese APT campaign support not available"}'''

content = re.sub(campaign_handler_pattern, chinese_handler, content, flags=re.DOTALL)

# Write the updated content
with open('apt_toolkit/cli.py', 'w') as f:
    f.write(content)

print("Successfully updated CLI with Chinese APT support")