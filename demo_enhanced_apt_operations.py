#!/usr/bin/env python3
"""
Demonstration script for Enhanced APT Operations targeting American and British organizations.

This script showcases the advanced capabilities of the enhanced APT operations module,
including comparative analysis, operational planning, and targeted campaign execution.
"""

import json
from apt_toolkit.apt_operations_enhanced import (
    analyze_dual_targets_enhanced,
    generate_operational_plan_enhanced,
    execute_targeted_campaign_enhanced,
    generate_intelligence_report_enhanced
)


def demo_enhanced_apt_operations():
    """Demonstrate enhanced APT operations capabilities."""
    
    print("=" * 80)
    print("ENHANCED APT OPERATIONS DEMONSTRATION")
    print("Advanced targeting of American and British government/military organizations")
    print("=" * 80)
    
    # Demo 1: Dual Target Analysis
    print("\n1. DUAL TARGET ANALYSIS")
    print("-" * 40)
    analysis = analyze_dual_targets_enhanced(seed=42)
    
    comparative = analysis["comparative_analysis"]
    risk_comp = comparative["risk_comparison"]
    target_comp = comparative["target_count_comparison"]
    
    print(f"American Targets: {target_comp['american_targets']}")
    print(f"British Targets: {target_comp['uk_targets']}")
    print(f"Total Targets: {target_comp['total_targets']}")
    print(f"Higher Risk: {risk_comp['higher_risk'].upper()}")
    print(f"Risk Difference: {risk_comp['risk_difference']}")
    
    # Show top 3 prioritized targets
    prioritized = analysis["recommended_prioritization"]
    print("\nTop Priority Targets:")
    for i, target in enumerate(prioritized[:3], 1):
        print(f"  {i}. {target['target']} ({target['country']} - {target['priority_level']})")
    
    # Demo 2: Operational Planning
    print("\n2. OPERATIONAL PLANNING")
    print("-" * 40)
    plan = generate_operational_plan_enhanced("american", seed=42)
    
    phases = plan["phasing_strategy"]
    techniques = plan["technique_selection"]
    timeline = plan["timeline_estimation"]
    
    print(f"Target Type: {plan['target_type'].upper()}")
    print(f"Total Estimated Duration: {timeline['total_estimated']}")
    
    print("\nKey Techniques:")
    for category, tech in techniques.items():
        if category in ["initial_access", "defense_evasion", "exfiltration"]:
            print(f"  • {category.replace('_', ' ').title()}: {tech['primary']}")
    
    # Demo 3: Targeted Campaign Execution
    print("\n3. TARGETED CAMPAIGN EXECUTION")
    print("-" * 40)
    campaign = execute_targeted_campaign_enhanced(
        target_email="security.director@secure.dod.mil",
        target_domain="dod.mil",
        campaign_type="advanced",
        seed=42
    )
    
    print(f"Target: {campaign['target_email']}")
    print(f"Campaign ID: {campaign['campaign_id']}")
    print(f"Overall Success: {'YES' if campaign['overall_success'] else 'NO'}")
    print(f"Detection Probability: {campaign['estimated_detection_probability']:.1%}")
    
    print("\nExecution Steps:")
    for step in campaign["execution_steps"]:
        print(f"  • {step['phase']}")
    
    # Demo 4: Intelligence Report
    print("\n4. INTELLIGENCE REPORT")
    print("-" * 40)
    report = generate_intelligence_report_enhanced(seed=42)
    
    print(f"Report ID: {report['report_id']}")
    print(f"\nExecutive Summary:")
    print(f"  {report['executive_summary']}")
    
    threat_landscape = report["threat_landscape"]
    print(f"\nDefensive Capabilities:")
    for country, capabilities in threat_landscape["defensive_capabilities"].items():
        print(f"  • {country.title()}: {capabilities}")
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("Enhanced APT Operations provides comprehensive targeting and operational")
    print("planning capabilities for American and British government/military targets.")
    print("=" * 80)


if __name__ == "__main__":
    demo_enhanced_apt_operations()