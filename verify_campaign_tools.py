#!/usr/bin/env python3
"""
Campaign Tools Verification Script
Verifies that all campaigns have access to all available tools
"""

import os
import sys
import subprocess
from pathlib import Path

def get_all_campaigns():
    """Get all campaign directories."""
    campaigns_dir = Path("campaigns")
    campaigns = []
    
    for item in campaigns_dir.iterdir():
        if item.is_dir() and not item.name.startswith('__') and not item.name.startswith('.'):
            campaigns.append(item)
    
    return campaigns

def get_available_tools():
    """Get all available tools from the main tools directory."""
    tools_dir = Path("tools")
    tools = []
    
    for item in tools_dir.iterdir():
        if item.is_file() and not item.name.startswith('.') and item.name != "README.md":
            tools.append(item.name)
    
    return tools

def verify_tool_accessibility(campaign_path, tool_name):
    """Verify that a tool is accessible in a campaign."""
    tool_path = campaign_path / "tools" / tool_name
    
    if not tool_path.exists():
        return False, f"Tool {tool_name} not found"
    
    if tool_path.is_symlink():
        try:
            target = tool_path.resolve()
            if target.exists():
                return True, f"Symlink to {target}"
            else:
                return False, f"Broken symlink to {target}"
        except Exception as e:
            return False, f"Symlink error: {e}"
    else:
        return True, "Local file"

def main():
    """Main function to verify campaign tools."""
    print("[*] Verifying campaign tools accessibility...")
    
    campaigns = get_all_campaigns()
    available_tools = get_available_tools()
    
    print(f"[*] Found {len(campaigns)} campaigns")
    print(f"[*] Available tools: {', '.join(available_tools)}")
    
    # Test a sample of campaigns
    sample_campaigns = campaigns[:10]
    
    overall_results = {}
    
    for campaign in sample_campaigns:
        print(f"\n[*] Verifying tools in campaign: {campaign.name}")
        
        campaign_results = {}
        accessible_tools = 0
        
        for tool_name in available_tools:
            accessible, message = verify_tool_accessibility(campaign, tool_name)
            campaign_results[tool_name] = {
                "accessible": accessible,
                "message": message
            }
            if accessible:
                accessible_tools += 1
        
        overall_results[campaign.name] = campaign_results
        
        print(f"    Accessible tools: {accessible_tools}/{len(available_tools)}")
        
        # Print inaccessible tools
        for tool_name, result in campaign_results.items():
            if not result["accessible"]:
                print(f"    [-] {tool_name}: {result['message']}")
    
    # Generate summary report
    print(f"\n[*] Campaign Tools Accessibility Summary")
    print("=" * 50)
    
    total_campaigns_tested = len(sample_campaigns)
    total_tools_tested = total_campaigns_tested * len(available_tools)
    total_accessible = 0
    
    for campaign_name, results in overall_results.items():
        campaign_accessible = sum(1 for result in results.values() if result["accessible"])
        total_accessible += campaign_accessible
        accessibility_rate = (campaign_accessible / len(results)) * 100
        print(f"{campaign_name}: {campaign_accessible}/{len(results)} ({accessibility_rate:.1f}%)")
    
    overall_accessibility_rate = (total_accessible / total_tools_tested) * 100
    print(f"\nOverall accessibility rate: {total_accessible}/{total_tools_tested} ({overall_accessibility_rate:.1f}%)")
    
    if overall_accessibility_rate >= 95:
        print(f"\n[+] Campaign tools are properly accessible!")
    else:
        print(f"\n[!] Some campaign tools need attention")
    
    print(f"\n[*] Verification completed!")

if __name__ == "__main__":
    main()