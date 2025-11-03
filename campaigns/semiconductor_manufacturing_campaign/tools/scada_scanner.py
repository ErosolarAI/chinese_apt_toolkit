#!/usr/bin/env python3
"""
SCADA/OT Network Scanner - Identify industrial control systems
Targets: Modbus, DNP3, OPC, Profinet, EtherNet/IP
"""

import socket
import struct
import json
from datetime import datetime

class SCADAScanner:
    """
    Scanner for industrial protocols used in semiconductor fabs:
    - Modbus TCP (502)
    - OPC UA (4840)
    - EtherNet/IP (44818)
    - Profinet (34964)
    - S7comm (102)
    """

    SCADA_PORTS = {
        20000: 'DNP3',
        102: 'S7comm (Siemens)',
        502: 'Modbus TCP',
        4840: 'OPC UA',
        44818: 'EtherNet/IP',
        34962: 'Profinet DCP',
        34964: 'Profinet',
        47808: 'BACnet',
        1911: 'Niagara Fox',
        789: 'Redlion Crimson',
        2222: 'EtherNet/IP Explicit',
    }

    def __init__(self, target_network='192.168.1.0/24'):
        self.target_network = target_network
        self.findings = []

    def parse_cidr(self, cidr):
        """Parse CIDR notation to IP list"""
        # Simplified implementation
        base = cidr.split('/')[0]
        octets = base.split('.')
        return [f"{octets[0]}.{octets[1]}.{octets[2]}.{i}"
                for i in range(1, 255)]

    def scan_port(self, ip, port, timeout=1):
        """Scan single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def identify_modbus(self, ip, port=502):
        """Attempt Modbus identification"""
        try:
            # Modbus TCP query (read holding registers)
            transaction_id = 0x0001
            protocol_id = 0x0000
            length = 0x0006
            unit_id = 0x01
            function_code = 0x03
            start_addr = 0x0000
            quantity = 0x000A

            query = struct.pack('>HHHBBHH',
                transaction_id, protocol_id, length,
                unit_id, function_code, start_addr, quantity)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            sock.send(query)
            response = sock.recv(1024)
            sock.close()

            if len(response) > 0:
                return {
                    'protocol': 'Modbus TCP',
                    'response_length': len(response),
                    'details': 'Device responded to Modbus query'
                }
        except:
            pass
        return None

    def scan_network(self):
        """Scan target network for SCADA devices"""
        print(f"[*] Scanning network: {self.target_network}")
        print(f"[*] Looking for {len(self.SCADA_PORTS)} industrial protocols")

        ip_list = self.parse_cidr(self.target_network)

        for ip in ip_list:
            print(f"[*] Scanning {ip}...", end='\r')

            device_info = {
                'ip': ip,
                'open_ports': [],
                'protocols': [],
                'timestamp': datetime.now().isoformat()
            }

            for port, protocol in self.SCADA_PORTS.items():
                if self.scan_port(ip, port):
                    device_info['open_ports'].append(port)
                    device_info['protocols'].append(protocol)

                    print(f"\n[!] FOUND: {ip}:{port} - {protocol}")

                    # Attempt protocol-specific identification
                    if port == 502:
                        modbus_info = self.identify_modbus(ip, port)
                        if modbus_info:
                            device_info['modbus_details'] = modbus_info

            if device_info['open_ports']:
                self.findings.append(device_info)

        return self.generate_report()

    def generate_report(self):
        """Generate scan report"""
        report = {
            'scan_timestamp': datetime.now().isoformat(),
            'target_network': self.target_network,
            'devices_found': len(self.findings),
            'devices': self.findings,
            'protocols_summary': {},
        }

        # Count protocol occurrences
        for device in self.findings:
            for protocol in device['protocols']:
                if protocol not in report['protocols_summary']:
                    report['protocols_summary'][protocol] = 0
                report['protocols_summary'][protocol] += 1

        return report

    def export_report(self, output_file='scada_scan_results.json'):
        """Export findings"""
        report = self.generate_report()

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n\n[*] Scan complete")
        print(f"[*] Devices found: {len(self.findings)}")
        print(f"[*] Protocols detected: {', '.join(report['protocols_summary'].keys())}")
        print(f"[*] Report saved to: {output_file}")

        return report


def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   SCADA/OT Network Scanner                    ║
    ║   Industrial Control System Reconnaissance    ║
    ╚═══════════════════════════════════════════════╝
    """)

    import sys
    network = sys.argv[1] if len(sys.argv) > 1 else '192.168.1.0/24'

    scanner = SCADAScanner(network)
    scanner.scan_network()
    scanner.export_report()


if __name__ == "__main__":
    main()
