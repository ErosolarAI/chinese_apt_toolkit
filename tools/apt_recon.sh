#!/bin/bash

# APT Reconnaissance Toolkit
# Advanced reconnaissance and intelligence gathering tools
# For educational and authorized penetration testing only

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
  ___  _____ _____   _____                      _           
 / _ \|  _  |  __ \ /  __ \                    (_)          
/ /_\ \ | | | |  \/ | /  \/ ___  _ __  ___  ___ _  ___  _ __ 
|  _  | | | | | __  | |    / _ \| '_ \/ __|/ __| |/ _ \| '_ \
| | | \ \_/ / |_\ \ | \__/\ (_) | | | \__ \ (__| | (_) | | | |
\_| |_/\___/ \____/  \____/\___/|_| |_|___/\___|_|\___/|_| |_|

Advanced Persistent Threat Reconnaissance Toolkit
For Educational and Authorized Testing Only
EOF
echo -e "${NC}"

# Configuration
OUTPUT_DIR="recon_output_$(date +%Y%m%d_%H%M%S)"
TARGET_DOMAIN=""
TARGET_IP=""

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "OPTIONS:"
    echo "  -d, --domain DOMAIN    Target domain for reconnaissance"
    echo "  -i, --ip IP            Target IP address for scanning"
    echo "  -o, --output DIR       Output directory (default: recon_output_YYYYMMDD_HHMMSS)"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "EXAMPLES:" 
    echo "  $0 -d example.com"
    echo "  $0 -i 192.168.1.1 -o my_recon"
    echo ""
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--domain)
            TARGET_DOMAIN="$2"
            shift 2
            ;;
        -i|--ip)
            TARGET_IP="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate inputs
if [[ -z "$TARGET_DOMAIN" && -z "$TARGET_IP" ]]; then
    echo -e "${RED}Error: Either domain or IP must be specified${NC}"
    usage
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}[+] Output directory created: $OUTPUT_DIR${NC}"

# Function to check dependencies
check_dependencies() {
    local deps=("nmap" "whois" "dig" "curl" "host" "python3")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}[-] Missing dependencies: ${missing[*]}${NC}"
        echo "Please install missing tools before running this script."
        exit 1
    fi
    
    echo -e "${GREEN}[+] All dependencies found${NC}"
}

# Function for domain reconnaissance
domain_recon() {
    local domain="$1"
    echo -e "${BLUE}[*] Starting domain reconnaissance for: $domain${NC}"
    
    # WHOIS lookup
    echo -e "${YELLOW}[*] Performing WHOIS lookup...${NC}"
    whois "$domain" > "$OUTPUT_DIR/whois_$domain.txt" 2>/dev/null || echo "WHOIS lookup failed"
    
    # DNS enumeration
    echo -e "${YELLOW}[*] Enumerating DNS records...${NC}"
    {
        echo "=== A Records ==="
        dig "$domain" A +short
        echo ""
        echo "=== AAAA Records ==="
        dig "$domain" AAAA +short
        echo ""
        echo "=== MX Records ==="
        dig "$domain" MX +short
        echo ""
        echo "=== TXT Records ==="
        dig "$domain" TXT +short
        echo ""
        echo "=== NS Records ==="
        dig "$domain" NS +short
        echo ""
        echo "=== CNAME Records ==="
        dig "$domain" CNAME +short
    } > "$OUTPUT_DIR/dns_$domain.txt"
    
    # Subdomain enumeration
    echo -e "${YELLOW}[*] Enumerating subdomains...${NC}"
    {
        echo "Common subdomains:"
        for sub in www ftp mail smtp pop imap admin test dev staging api; do
            host "$sub.$domain" 2>/dev/null | grep -v "not found"
        done
    } > "$OUTPUT_DIR/subdomains_$domain.txt"
    
    # HTTP headers
    echo -e "${YELLOW}[*] Gathering HTTP headers...${NC}"
    curl -I "http://$domain" 2>/dev/null > "$OUTPUT_DIR/http_headers_$domain.txt" || echo "HTTP header collection failed"
    
    echo -e "${GREEN}[+] Domain reconnaissance completed${NC}"
}

# Function for network scanning
network_scan() {
    local ip="$1"
    echo -e "${BLUE}[*] Starting network scan for: $ip${NC}"
    
    # Quick TCP port scan
    echo -e "${YELLOW}[*] Performing TCP port scan...${NC}"
    nmap -sS -T4 "$ip" > "$OUTPUT_DIR/nmap_tcp_$ip.txt"
    
    # Service version detection
    echo -e "${YELLOW}[*] Detecting service versions...${NC}"
    nmap -sV -T4 "$ip" > "$OUTPUT_DIR/nmap_services_$ip.txt"
    
    # OS detection
    echo -e "${YELLOW}[*] Attempting OS detection...${NC}"
    nmap -O "$ip" > "$OUTPUT_DIR/nmap_os_$ip.txt" 2>/dev/null
    
    # Vulnerability scan (basic)
    echo -e "${YELLOW}[*] Running basic vulnerability scan...${NC}"
    nmap --script vuln "$ip" > "$OUTPUT_DIR/nmap_vuln_$ip.txt" 2>/dev/null
    
    echo -e "${GREEN}[+] Network scanning completed${NC}"
}

# Function to generate reconnaissance report
generate_report() {
    echo -e "${BLUE}[*] Generating reconnaissance report...${NC}"
    
    cat > "$OUTPUT_DIR/recon_report.md" << EOF
# APT Reconnaissance Report

**Date:** $(date)
**Target Domain:** $TARGET_DOMAIN
**Target IP:** $TARGET_IP

## Executive Summary

This report contains reconnaissance data gathered using the APT Reconnaissance Toolkit.

## Domain Information

### WHOIS Data
\`\`\`
$(cat "$OUTPUT_DIR/whois_$TARGET_DOMAIN.txt" 2>/dev/null || echo "No WHOIS data available")
\`\`\`

### DNS Records
\`\`\`
$(cat "$OUTPUT_DIR/dns_$TARGET_DOMAIN.txt" 2>/dev/null || echo "No DNS data available")
\`\`\`

### Subdomains
\`\`\`
$(cat "$OUTPUT_DIR/subdomains_$TARGET_DOMAIN.txt" 2>/dev/null || echo "No subdomain data available")
\`\`\`

## Network Information

### TCP Port Scan Results
\`\`\`
$(cat "$OUTPUT_DIR/nmap_tcp_$TARGET_IP.txt" 2>/dev/null || echo "No TCP scan data available")
\`\`\`

### Service Detection
\`\`\`
$(cat "$OUTPUT_DIR/nmap_services_$TARGET_IP.txt" 2>/dev/null || echo "No service detection data available")
\`\`\`

## Indicators for Further Investigation

- Open ports and services
- Software versions and potential vulnerabilities
- DNS configuration and subdomains
- Network infrastructure details

## Recommendations

1. Review open ports and services for unnecessary exposure
2. Check for outdated software versions
3. Monitor for suspicious DNS activity
4. Implement proper network segmentation

---
*This report was generated for educational and authorized testing purposes only.*
EOF
    
    echo -e "${GREEN}[+] Report generated: $OUTPUT_DIR/recon_report.md${NC}"
}

# Main execution
main() {
    echo -e "${GREEN}[+] APT Reconnaissance Toolkit Started${NC}"
    
    # Check dependencies
    check_dependencies
    
    # Perform domain reconnaissance if specified
    if [[ -n "$TARGET_DOMAIN" ]]; then
        domain_recon "$TARGET_DOMAIN"
    fi
    
    # Perform network scanning if specified
    if [[ -n "$TARGET_IP" ]]; then
        network_scan "$TARGET_IP"
    fi
    
    # Generate final report
    generate_report
    
    echo -e "${GREEN}[+] Reconnaissance completed successfully${NC}"
    echo -e "${GREEN}[+] Results saved to: $OUTPUT_DIR${NC}"
    echo ""
    echo -e "${BLUE}Summary of files created:${NC}"
    find "$OUTPUT_DIR" -type f -name "*.txt" -o -name "*.md" | sort
}

# Execute main function
main "$@"