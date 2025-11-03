#!/usr/bin/env python3
"""
Demonstration script for the Organization Management System
"""

import sys
import os

# Add the parent directory to the path so we can import apt_toolkit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from apt_toolkit.organization_manager import OrganizationManager


def main():
    """Demonstrate the organization management system."""
    print("=== APT Toolkit Organization Management Demo ===\n")
    
    try:
        with OrganizationManager() as manager:
            
            # List organizations
            print("1. Listing available organizations:")
            print("-" * 40)
            organizations = manager.list_organizations(limit=10)
            for i, org in enumerate(organizations, 1):
                print(f"{i}. {org}")
            print()
            
            if organizations:
                # Get stats for first organization
                first_org = organizations[0]
                print(f"2. Statistics for '{first_org}':")
                print("-" * 40)
                stats = manager.get_organization_stats(first_org)
                print(f"Email Count: {stats.get('email_count', 0)}")
                print(f"Domains: {', '.join(stats.get('domains', []))}")
                print()
                
                # Generate profile
                print(f"3. Generating profile for '{first_org}' (without deepseek):")
                print("-" * 40)
                profile = manager.generate_organization_profile(first_org, use_deepseek=False)
                print(f"Industry: {profile.get('industry', 'Unknown')}")
                print(f"Size: {profile.get('size', 'Unknown')}")
                print(f"Security Posture: {profile.get('security_posture', 'Unknown')}")
                print()
                
                # Generate attack plan
                print(f"4. Generating attack plan for '{first_org}' (without deepseek):")
                print("-" * 40)
                attack_plan = manager.generate_attack_plan(first_org, use_deepseek=False)
                print(f"Attack Type: {attack_plan.get('attack_type', 'Unknown')}")
                print(f"Strategy: {attack_plan.get('strategy', 'No strategy available')}")
                print()
                
                # Get sample emails
                print(f"5. Sample emails for '{first_org}':")
                print("-" * 40)
                emails = manager.get_organization_emails(first_org, limit=3)
                for email in emails:
                    print(f"• {email.get('email', 'Unknown')}")
                    if email.get('first_name') or email.get('last_name'):
                        print(f"  Name: {email.get('first_name', '')} {email.get('last_name', '')}".strip())
                    print()
                
                # Landscape analysis
                print("6. Organization landscape analysis:")
                print("-" * 40)
                landscape = manager.analyze_organization_landscape(limit=3)
                print(f"Total Organizations Analyzed: {landscape.get('total_organizations_analyzed', 0)}")
                
                industry_dist = landscape.get('industry_distribution', {})
                if industry_dist:
                    print("\nIndustry Distribution:")
                    for industry, count in industry_dist.items():
                        print(f"  • {industry}: {count}")
                
            else:
                print("No organizations found in the database.")
                print("Please ensure the email database is properly set up.")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nThis demo requires the email database to be set up.")
        print("Make sure you have run the email extraction scripts first.")


if __name__ == "__main__":
    main()