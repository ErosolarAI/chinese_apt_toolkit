#!/usr/bin/env python3
"""
Campaign Tools Test Script
Tests that all tools work correctly in campaign environments
"""

import os
import sys
import subprocess
import json
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

def test_tool_in_campaign(campaign_path, tool_name):
    """Test if a tool works in a campaign environment."""
    tool_path = campaign_path / "tools" / tool_name
    
    if not tool_path.exists():
        return False, f"Tool {tool_name} not found in {campaign_path.name}"
    
    # Test based on file extension
    try:
        if tool_name.endswith('.sh'):
            # Test shell script
            result = subprocess.run(
                ["bash", str(tool_path), "--help"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, f"Shell script test: {result.returncode}"
            
        elif tool_name.endswith('.py'):
            # Test Python script
            result = subprocess.run(
                ["python3", str(tool_path), "--help"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, f"Python script test: {result.returncode}"
            
        elif tool_name.endswith('.js'):
            # Test JavaScript script
            result = subprocess.run(
                ["node", str(tool_path), "--help"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, f"JavaScript test: {result.returncode}"
            
        elif tool_name.endswith('.rb'):
            # Test Ruby script
            result = subprocess.run(
                ["ruby", str(tool_path), "--help"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, f"Ruby script test: {result.returncode}"
            
        elif tool_name.endswith('.ps1'):
            # Test PowerShell script
            result = subprocess.run(
                ["pwsh", "-Command", f"& {{. {str(tool_path)} -Help}}"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, f"PowerShell test: {result.returncode}"
            
        elif tool_name.endswith('.c'):
            # C source file - check if compiled version exists
            compiled_name = tool_name.replace('.c', '')
            compiled_path = campaign_path / "tools" / compiled_name
            if compiled_path.exists():
                result = subprocess.run(
                    [str(compiled_path), "--help"],
                    capture_output=True, text=True, timeout=10
                )
                return result.returncode == 0, f"C binary test: {result.returncode}"
            else:
                return True, "C source file present (needs compilation)"
                
        else:
            # Binary files
            if os.access(tool_path, os.X_OK):
                result = subprocess.run(
                    [str(tool_path), "-h"],
                    capture_output=True, text=True, timeout=10
                )
                return result.returncode == 0, f"Binary test: {result.returncode}"
            else:
                return True, "Non-executable file present"
                
    except subprocess.TimeoutExpired:
        return False, "Test timeout"
    except Exception as e:
        return False, f"Test error: {str(e)}"

def test_campaign_tools(campaign_path):
    """Test all tools in a campaign."""
    available_tools = get_available_tools()
    results = {}
    
    for tool_name in available_tools:
        success, message = test_tool_in_campaign(campaign_path, tool_name)
        results[tool_name] = {
            "success": success,
            "message": message
        }
    
    return results

def main():
    """Main function to test campaign tools."""
    print("[*] Starting campaign tools testing...")
    
    campaigns = get_all_campaigns()
    available_tools = get_available_tools()
    
    print(f"[*] Found {len(campaigns)} campaigns")
    print(f"[*] Available tools: {', '.join(available_tools)}")
    
    # Test a sample of campaigns (first 5 to avoid too much output)
    sample_campaigns = campaigns[:5]
    
    overall_results = {}
    
    for campaign in sample_campaigns:
        print(f"\n[*] Testing tools in campaign: {campaign.name}")
        
        campaign_results = test_campaign_tools(campaign)
        overall_results[campaign.name] = campaign_results
        
        # Print summary for this campaign
        successful_tools = sum(1 for result in campaign_results.values() if result["success"])
        total_tools = len(campaign_results)
        
        print(f"    Success rate: {successful_tools}/{total_tools} tools")
        
        # Print failed tests
        for tool_name, result in campaign_results.items():
            if not result["success"]:
                print(f"    [-] {tool_name}: {result['message']}")
    
    # Generate summary report
    print(f"\n[*] Campaign Tools Test Summary")
    print("=" * 50)
    
    total_campaigns_tested = len(sample_campaigns)
    total_tools_tested = total_campaigns_tested * len(available_tools)
    total_successful = 0
    
    for campaign_name, results in overall_results.items():
        campaign_success = sum(1 for result in results.values() if result["success"])
        total_successful += campaign_success
        success_rate = (campaign_success / len(results)) * 100
        print(f"{campaign_name}: {campaign_success}/{len(results)} ({success_rate:.1f}%)")
    
    overall_success_rate = (total_successful / total_tools_tested) * 100
    print(f"\nOverall success rate: {total_successful}/{total_tools_tested} ({overall_success_rate:.1f}%)")
    
    if overall_success_rate >= 80:
        print(f"\n[+] Campaign tools are working well!")
    else:
        print(f"\n[!] Some campaign tools need attention")
    
    print(f"\n[*] Test completed!")

if __name__ == "__main__":
    main()