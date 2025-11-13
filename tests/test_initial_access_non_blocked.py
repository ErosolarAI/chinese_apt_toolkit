"""
Tests for non-blocked initial access techniques.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from apt_toolkit.initial_access_non_blocked import (
    LNKFileAttack,
    HTMLSmuggling,
    ISOFileAttack,
    LivingOffTheLand,
    BrowserExploitDelivery,
    NonBlockedInitialAccess
)


class TestLNKFileAttack(unittest.TestCase):
    """Test LNK file attack techniques."""
    
    def setUp(self):
        self.lnk_attack = LNKFileAttack()
    
    def test_create_malicious_lnk_basic(self):
        """Test basic LNK file creation."""
        result = self.lnk_attack.create_malicious_lnk("http://example.com/payload.ps1")
        
        self.assertIn("file_name", result)
        self.assertIn("file_path", result)
        self.assertIn("target_path", result)
        self.assertIn("arguments", result)
        self.assertEqual(result["payload_type"], "LNK with PowerShell")
        self.assertEqual(result["detection_evasion"], "High (uses legitimate PowerShell)")
    
    def test_create_malicious_lnk_different_disguises(self):
        """Test LNK file creation with different disguises."""
        disguises = ["document", "invoice", "resume", "presentation"]
        
        for disguise in disguises:
            result = self.lnk_attack.create_malicious_lnk("http://example.com/payload.ps1", disguise)
            self.assertIn("file_name", result)
            self.assertIn("description", result)
    
    def test_get_disguise_config(self):
        """Test disguise configuration retrieval."""
        config = self.lnk_attack._get_disguise_config("document")
        self.assertIn("filename", config)
        self.assertIn("description", config)
        
        # Test fallback for unknown disguise
        config = self.lnk_attack._get_disguise_config("unknown")
        self.assertIn("filename", config)
        self.assertIn("description", config)


class TestHTMLSmuggling(unittest.TestCase):
    """Test HTML smuggling techniques."""
    
    def setUp(self):
        self.html_smuggling = HTMLSmuggling()
    
    def test_create_smuggling_html_basic(self):
        """Test basic HTML smuggling creation."""
        result = self.html_smuggling.create_smuggling_html("http://example.com/payload.exe")
        
        self.assertIn("html_file", result)
        self.assertIn("template_type", result)
        self.assertIn("payload_url", result)
        self.assertEqual(result["delivery_method"], "HTML Smuggling")
        self.assertEqual(result["technique"], "JavaScript-based payload delivery")
        
        # Verify file was created
        self.assertTrue(os.path.exists(result["html_file"]))
        
        # Clean up
        if os.path.exists(result["html_file"]):
            os.remove(result["html_file"])
    
    def test_create_smuggling_html_different_templates(self):
        """Test HTML smuggling with different templates."""
        templates = ["invoice", "security"]
        
        for template in templates:
            result = self.html_smuggling.create_smuggling_html("http://example.com/payload.exe", template)
            self.assertEqual(result["template_type"], template)
            
            # Clean up
            if os.path.exists(result["html_file"]):
                os.remove(result["html_file"])
    
    def test_generate_html_content(self):
        """Test HTML content generation."""
        encoded_url = "aHR0cDovL2V4YW1wbGUuY29tL3BheWxvYWQuZXhl"
        content = self.html_smuggling._generate_html_content("invoice", encoded_url)
        
        self.assertIn("<!DOCTYPE html>", content)
        self.assertIn("<html>", content)
        self.assertIn("<script>", content)
        self.assertIn(encoded_url, content)


class TestISOFileAttack(unittest.TestCase):
    """Test ISO file attack techniques."""
    
    def setUp(self):
        self.iso_attack = ISOFileAttack()
    
    def test_create_malicious_iso_basic(self):
        """Test basic ISO file creation."""
        result = self.iso_attack.create_malicious_iso("/path/to/payload.exe")
        
        self.assertIn("iso_structure", result)
        self.assertIn("autorun_content", result)
        self.assertEqual(result["delivery_method"], "ISO Container")
        self.assertEqual(result["target_platform"], "Windows")
    
    def test_create_malicious_iso_with_disguise_files(self):
        """Test ISO file creation with custom disguise files."""
        disguise_files = ["report.pdf", "data.xlsx", "notes.txt"]
        result = self.iso_attack.create_malicious_iso("/path/to/payload.exe", disguise_files)
        
        self.assertEqual(result["iso_structure"]["disguise_files"], disguise_files)


class TestLivingOffTheLand(unittest.TestCase):
    """Test Living-off-the-land techniques."""
    
    def setUp(self):
        self.lotl = LivingOffTheLand()
    
    def test_generate_lotl_command_basic(self):
        """Test basic LOTL command generation."""
        result = self.lotl.generate_lotl_command("http://example.com/payload.exe")
        
        self.assertIn("tool", result)
        self.assertIn("description", result)
        self.assertIn("command", result)
        self.assertEqual(result["evasion_level"], "Very High (uses legitimate Windows tools)")
    
    def test_generate_lotl_command_different_tools(self):
        """Test LOTL command generation with different tools."""
        tools = ["bitsadmin", "certutil", "mshta", "rundll32", "regsvr32"]
        
        for tool in tools:
            result = self.lotl.generate_lotl_command("http://example.com/payload.exe", tool)
            self.assertEqual(result["tool"], tool)
            self.assertIn(tool, result["command"])


class TestBrowserExploitDelivery(unittest.TestCase):
    """Test browser exploit delivery techniques."""
    
    def setUp(self):
        self.browser_exploit = BrowserExploitDelivery()
    
    def test_generate_browser_exploit_basic(self):
        """Test basic browser exploit generation."""
        result = self.browser_exploit.generate_browser_exploit("Chrome", "http://example.com/exploit.html")
        
        self.assertIn("target_browser", result)
        self.assertIn("exploit_technique", result)
        self.assertIn("cve_reference", result)
        self.assertIn("payload_url", result)
        self.assertEqual(result["target_browser"], "Chrome")
    
    def test_generate_browser_exploit_different_browsers(self):
        """Test browser exploit generation for different browsers."""
        browsers = ["Chrome", "Edge", "Firefox", "Internet Explorer"]
        
        for browser in browsers:
            result = self.browser_exploit.generate_browser_exploit(browser, "http://example.com/exploit.html")
            self.assertEqual(result["target_browser"], browser)


class TestNonBlockedInitialAccess(unittest.TestCase):
    """Test main non-blocked initial access class."""
    
    def setUp(self):
        self.non_blocked = NonBlockedInitialAccess()
    
    def test_get_available_techniques(self):
        """Test retrieval of available techniques."""
        techniques = self.non_blocked.get_available_techniques()
        
        self.assertIsInstance(techniques, list)
        self.assertGreater(len(techniques), 0)
        
        for technique in techniques:
            self.assertIn("name", technique)
            self.assertIn("description", technique)
            self.assertIn("evasion_level", technique)
            self.assertIn("success_rate", technique)
    
    def test_generate_attack_plan(self):
        """Test attack plan generation."""
        attack_plan = self.non_blocked.generate_attack_plan("example.com")
        
        self.assertIn("target_domain", attack_plan)
        self.assertIn("attack_techniques", attack_plan)
        self.assertIn("rationale", attack_plan)
        self.assertEqual(attack_plan["target_domain"], "example.com")
        self.assertEqual(len(attack_plan["attack_techniques"]), 3)


if __name__ == "__main__":
    unittest.main()