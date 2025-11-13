"""Tests for enhanced APT operations module."""

import unittest
from datetime import datetime
from unittest.mock import patch

from apt_toolkit.apt_operations_enhanced import (
    APTOperationsDirector,
    analyze_dual_targets_enhanced,
    generate_operational_plan_enhanced
)


class TestAPTOperationsDirector(unittest.TestCase):
    """Test the APTOperationsDirector class."""
    
    def setUp(self):
        self.director = APTOperationsDirector(seed=42)
    
    def test_initialization(self):
        """Test director initialization."""
        self.assertIsNotNone(self.director.american_analyzer)
        self.assertIsNotNone(self.director.uk_analyzer)
        self.assertIsNotNone(self.director.social_engineering)
        self.assertIsNotNone(self.director.payload_engine)
        self.assertIsNotNone(self.director.supply_chain)
        self.assertIsNotNone(self.director.edr_evasion)
        self.assertIsNotNone(self.director.persistence)
        self.assertIsNotNone(self.director.adcs_exploit)
        self.assertIsNotNone(self.director.logger)
    
    def test_analyze_dual_targets(self):
        """Test dual target analysis."""
        with patch("apt_toolkit.apt_operations_enhanced.datetime") as mock_datetime, patch(
            "apt_toolkit.american_targets_enhanced.datetime"
        ) as mock_american_datetime, patch(
            "apt_toolkit.uk_targets_enhanced.datetime"
        ) as mock_uk_datetime, patch(
            "apt_toolkit.initial_access_enhanced.datetime"
        ) as mock_initial_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_american_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_uk_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_initial_datetime.now.return_value = datetime(2024, 1, 1, 20, 0, 0)
            
            analysis = self.director.analyze_dual_targets()
        
        self.assertIn("american_targets", analysis)
        self.assertIn("uk_targets", analysis)
        self.assertIn("comparative_analysis", analysis)
        self.assertIn("recommended_prioritization", analysis)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_analyze_dual_targets_enhanced(self):
        """Test enhanced dual target analysis function."""
        with patch("apt_toolkit.apt_operations_enhanced.datetime") as mock_datetime, patch(
            "apt_toolkit.american_targets_enhanced.datetime"
        ) as mock_american_datetime, patch(
            "apt_toolkit.uk_targets_enhanced.datetime"
        ) as mock_uk_datetime, patch(
            "apt_toolkit.initial_access_enhanced.datetime"
        ) as mock_initial_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_american_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_uk_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_initial_datetime.now.return_value = datetime(2024, 1, 1, 20, 0, 0)
            
            analysis = analyze_dual_targets_enhanced(seed=42)
        
        self.assertIn("american_targets", analysis)
        self.assertIn("uk_targets", analysis)
        self.assertIn("comparative_analysis", analysis)
    
    def test_generate_operational_plan_enhanced(self):
        """Test enhanced operational plan generation function."""
        with patch("apt_toolkit.apt_operations_enhanced.datetime") as mock_datetime, patch(
            "apt_toolkit.american_targets_enhanced.datetime"
        ) as mock_american_datetime, patch(
            "apt_toolkit.uk_targets_enhanced.datetime"
        ) as mock_uk_datetime, patch(
            "apt_toolkit.initial_access_enhanced.datetime"
        ) as mock_initial_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_american_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_uk_datetime.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_initial_datetime.now.return_value = datetime(2024, 1, 1, 20, 0, 0)
            
            plan = generate_operational_plan_enhanced("american", seed=42)
        
        self.assertIn("target_type", plan)
        self.assertIn("analysis", plan)
        self.assertIn("phasing_strategy", plan)


if __name__ == "__main__":
    unittest.main()
