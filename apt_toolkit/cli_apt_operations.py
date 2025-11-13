"""
CLI interface for enhanced APT operations targeting American and British organizations.
"""

import argparse
import json
import sys
from typing import Any, Dict

from .apt_operations_enhanced import (
    APTOperationsDirector,
    analyze_dual_targets_enhanced,
    generate_operational_plan_enhanced,
    execute_targeted_campaign_enhanced
)


def main():
    """Main CLI entry point for enhanced APT operations."""
    parser = argparse.ArgumentParser(
        description="Enhanced APT Operations - Advanced targeting of American and British organizations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  apt-operations analyze-dual-targets
  apt-operations operational-plan --target-type american
  apt-operations execute-campaign --email admin@army.mil --domain army.mil
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="APT operations commands")

    # Analyze dual targets
    analyze_parser = subparsers.add_parser(
        "analyze-dual-targets", 
        help="Analyze both American and British targets for comparative analysis"
    )
    analyze_parser.add_argument("--seed", type=int, help="Seed for deterministic output")

    # Generate operational plan
    plan_parser = subparsers.add_parser(
        "operational-plan", 
        help="Generate comprehensive operational plan for specified targets"
    )
    plan_parser.add_argument(
        "--target-type", 
        choices=["american", "british", "both"], 
        default="both",
        help="Target type for operational planning"
    )
    plan_parser.add_argument("--seed", type=int, help="Seed for deterministic output")

    # Execute targeted campaign
    campaign_parser = subparsers.add_parser(
        "execute-campaign", 
        help="Execute targeted campaign against specific email/domain"
    )
    campaign_parser.add_argument("--email", required=True, help="Target email address")
    campaign_parser.add_argument("--domain", required=True, help="Target domain")
    campaign_parser.add_argument(
        "--campaign-type", 
        choices=["standard", "advanced", "stealth"], 
        default="standard",
        help="Campaign type"
    )
    campaign_parser.add_argument("--seed", type=int, help="Seed for deterministic output")

    # Common arguments
    for subparser in [analyze_parser, plan_parser, campaign_parser]:
        subparser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        result = handle_command(args)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_pretty_result(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def handle_command(args) -> Dict[str, Any]:
    """Handle CLI commands and return results."""

    if args.command == "analyze-dual-targets":
        analysis = analyze_dual_targets_enhanced(seed=args.seed)
        return {
            "command": "analyze_dual_targets",
            "analysis": analysis
        }

    elif args.command == "operational-plan":
        plan = generate_operational_plan_enhanced(
            target_type=args.target_type, 
            seed=args.seed
        )
        return {
            "command": "operational_plan",
            "target_type": args.target_type,
            "plan": plan
        }

    elif args.command == "execute-campaign":
        campaign = execute_targeted_campaign_enhanced(
            target_email=args.email,
            target_domain=args.domain,
            campaign_type=args.campaign_type,
            seed=args.seed
        )
        return {
            "command": "execute_campaign",
            "target_email": args.email,
            "target_domain": args.domain,
            "campaign": campaign
        }

    else:
        raise ValueError(f"Unknown command: {args.command}")


def print_pretty_result(result):
    """Print results in a human-readable format."""
    command = result.get("command", "")
    
    if command == "analyze_dual_targets":
        analysis = result["analysis"]
        print("\n" + "="*60)
        print("ENHANCED APT OPERATIONS - DUAL TARGET ANALYSIS")
        print("="*60)
        
        comparative = analysis["comparative_analysis"]
        risk_comp = comparative["risk_comparison"]
        target_comp = comparative["target_count_comparison"]
        
        print(f"\nRISK COMPARISON:")
        print(f"  American Risk Score: {risk_comp['american_risk_score']}")
        print(f"  British Risk Score: {risk_comp['uk_risk_score']}")
        print(f"  Higher Risk: {risk_comp['higher_risk'].upper()}")
        
        print(f"\nTARGET COUNT:")
        print(f"  American Targets: {target_comp['american_targets']}")
        print(f"  British Targets: {target_comp['uk_targets']}")
        print(f"  Total Targets: {target_comp['total_targets']}")
        
        print(f"\nTOP PRIORITY TARGETS:")
        prioritized = analysis["recommended_prioritization"]
        for i, target in enumerate(prioritized[:5], 1):
            print(f"  {i}. {target['target']} ({target['country']} - {target['priority_level']})")

    elif command == "operational_plan":
        plan = result["plan"]
        print("\n" + "="*60)
        print(f"ENHANCED APT OPERATIONS - {result['target_type'].upper()} OPERATIONAL PLAN")
        print("="*60)
        
        phases = plan["phasing_strategy"]
        print(f"\nPHASING STRATEGY:")
        for phase_key, phase_data in phases.items():
            print(f"\n  {phase_data['name']} ({phase_data['duration']})")
            for activity in phase_data['activities'][:3]:  # Show first 3 activities
                print(f"    • {activity}")
        
        techniques = plan["technique_selection"]
        print(f"\nPRIMARY TECHNIQUES:")
        for category, tech in techniques.items():
            print(f"  {category.replace('_', ' ').title()}: {tech['primary']}")

    elif command == "execute_campaign":
        campaign = result["campaign"]
        print("\n" + "="*60)
        print("ENHANCED APT OPERATIONS - TARGETED CAMPAIGN EXECUTION")
        print("="*60)
        
        print(f"\nTARGET: {result['target_email']} ({result['target_domain']})")
        print(f"CAMPAIGN ID: {campaign['campaign_id']}")
        print(f"OVERALL SUCCESS: {'YES' if campaign['overall_success'] else 'NO'}")
        print(f"DETECTION PROBABILITY: {campaign['estimated_detection_probability']:.1%}")
        
        print(f"\nEXECUTION STEPS:")
        for step in campaign["execution_steps"]:
            print(f"  • {step['phase']}: {step['action']}")
        
        print(f"\nRECOMMENDED NEXT STEPS:")
        for step in campaign["recommended_next_steps"]:
            print(f"  • {step}")

    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
