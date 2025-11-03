# APT Toolkit - Multi-Language Tools

This directory contains a comprehensive collection of Advanced Persistent Threat (APT) simulation and analysis tools written in multiple programming languages. These tools are designed for educational purposes, authorized penetration testing, and defensive security research.

## ⚠️ Legal and Ethical Notice

**IMPORTANT**: These tools are designed for:
- **Educational purposes** in cybersecurity training and research
- **Defensive security** to understand and protect against APT threats
- **Authorized penetration testing** with proper permissions
- **Academic research** in cybersecurity and threat intelligence

**PROHIBITED USES**:
- Unauthorized penetration testing or hacking
- Malicious activities against any systems
- Criminal or illegal purposes
- Attacks against critical infrastructure

Users are solely responsible for ensuring they have proper authorization before using these techniques.

## 🛠️ Available Tools

### Shell Scripts

#### `apt_recon.sh` - APT Reconnaissance Toolkit
- **Purpose**: Advanced reconnaissance and intelligence gathering
- **Features**:
  - Domain reconnaissance (WHOIS, DNS enumeration)
  - Network scanning with Nmap
  - Subdomain enumeration
  - HTTP header analysis
  - Automated report generation
- **Usage**:
  ```bash
  chmod +x apt_recon.sh
  ./apt_recon.sh -d example.com
  ./apt_recon.sh -i 192.168.1.1 -o my_recon
  ```

### PowerShell

#### `APT-PowerShell-Toolkit.ps1` - APT PowerShell Toolkit
- **Purpose**: Windows-based APT simulation and analysis
- **Features**:
  - System reconnaissance and information gathering
  - Persistence mechanisms (Registry, Scheduled Tasks, Services)
  - Privilege escalation analysis
  - Defense evasion techniques (AMSI/ETW bypass)
  - Living Off The Land (LOL) binaries documentation
- **Usage**:
  ```powershell
  .\APT-PowerShell-Toolkit.ps1 --Recon --Persistence
  .\APT-PowerShell-Toolkit.ps1 --All
  ```

### C Programming

#### `apt_memory_injector.c` - APT Memory Injection Toolkit
- **Purpose**: Advanced process injection techniques
- **Features**:
  - Process listing and analysis
  - Memory region analysis
  - Process injection framework
  - Educational demonstration of injection techniques
- **Compilation**:
  ```bash
  gcc -o apt_memory_injector apt_memory_injector.c -lpsapi
  ```
- **Usage**:
  ```bash
  ./apt_memory_injector --list
  ./apt_memory_injector --pid 1234
  ```

### Python

#### `apt_persistence.py` - APT Persistence Toolkit
- **Purpose**: Cross-platform persistence mechanism simulation
- **Features**:
  - Windows Registry persistence
  - Windows Scheduled Tasks
  - Linux cron jobs
  - Linux systemd services
  - macOS launchd persistence
  - File-based persistence
  - Automated reporting
- **Usage**:
  ```bash
  python3 apt_persistence.py --install
  python3 apt_persistence.py --help
  ```

#### `sliver_client.py` - LightC2 Agent Generator
- **Purpose**: Generate configurable agent source artifacts without external Sliver dependencies
- **Features**:
  - Uses the bundled LightC2 Nim template for Windows agents
  - Emits bash tasking loops for Linux targets
  - Configurable C2 URL, secret key, and sleep interval (`config/lightc2_agent_config.json`)
- **Usage**:
  ```bash
  python3 sliver_client.py  # writes payload metadata and artefacts to payloads/
  ```

### Go

#### `apt_network_scanner.go` - APT Network Scanner
- **Purpose**: Advanced network reconnaissance and scanning
- **Features**:
  - CIDR notation support
  - Port range scanning
  - Service detection
  - Concurrent scanning
  - JSON output
  - Customizable timeouts
- **Compilation**:
  ```bash
  go build apt_network_scanner.go
  ```
- **Usage**:
  ```bash
  ./apt_network_scanner -t 192.168.1.0/24 -p 1-1000
  ./apt_network_scanner -t example.com -p common -o results.json
  ```

### JavaScript/Node.js

#### `apt_web_recon.js` - APT Web Reconnaissance Toolkit
- **Purpose**: Web application and infrastructure reconnaissance
- **Features**:
  - DNS record enumeration
  - HTTP/HTTPS analysis
  - Security header analysis
  - Technology stack detection
  - Subdomain enumeration
  - Automated reporting
- **Usage**:
  ```bash
  node apt_web_recon.js example.com
  node apt_web_recon.js --subdomains --output results.json example.com
  ```

### Ruby

#### `apt_social_engineering.rb` - APT Social Engineering Toolkit
- **Purpose**: Social engineering analysis and simulation
- **Features**:
  - Email pattern analysis
  - Psychological profiling
  - Social media presence analysis
  - Spear phishing template generation
  - Communication style recommendations
- **Usage**:
  ```bash
  ruby apt_social_engineering.rb --name "John Doe" --email john.doe@example.com
  ruby apt_social_engineering.rb --email admin@company.com --company "ACME Corp"
  ```

## 🔧 Tool Categories

### Reconnaissance & Intelligence Gathering
- **apt_recon.sh**: Comprehensive network and domain reconnaissance
- **apt_network_scanner.go**: Advanced network scanning
- **apt_web_recon.js**: Web infrastructure analysis

### Persistence & Evasion
- **APT-PowerShell-Toolkit.ps1**: Windows persistence mechanisms
- **apt_persistence.py**: Cross-platform persistence
- **apt_memory_injector.c**: Process injection techniques

### Social Engineering
- **apt_social_engineering.rb**: Target analysis and profiling

## 🎯 Use Cases

### Educational Scenarios
1. **Red Team Training**: Simulate APT tactics, techniques, and procedures
2. **Blue Team Defense**: Understand attack vectors for better detection
3. **Academic Research**: Study advanced cyber attack methodologies
4. **Security Testing**: Authorized penetration testing exercises

### Defensive Applications
1. **Threat Hunting**: Identify indicators of compromise
2. **Incident Response**: Understand attack patterns
3. **Security Controls**: Test defensive measures
4. **Training**: Security awareness and technical training

## 📋 Prerequisites

### General Requirements
- Proper authorization for testing
- Understanding of cybersecurity concepts
- Legal compliance with local regulations

### Language-Specific Requirements
- **Shell**: bash, core utilities (nmap, whois, dig, curl)
- **PowerShell**: Windows PowerShell 5.1+ or PowerShell Core
- **C**: GCC compiler, Windows SDK (for Windows features)
- **Python**: Python 3.6+
- **Go**: Go 1.16+
- **Node.js**: Node.js 14+
- **Ruby**: Ruby 2.7+

## 🔒 Security Considerations

### Operational Security
- Use in isolated testing environments
- Ensure proper network segmentation
- Follow responsible disclosure practices
- Maintain testing documentation

### Legal Compliance
- Obtain written authorization for testing
- Follow organizational security policies
- Comply with local and international laws
- Maintain testing scope boundaries

## 📚 Learning Resources

### Recommended Reading
- MITRE ATT&CK Framework
- NIST Cybersecurity Framework
- OWASP Testing Guide
- SANS Security Training

### Related Tools
- Metasploit Framework
- Cobalt Strike
- Empire Project
- BloodHound

## 🤝 Contributing

We welcome contributions from security researchers, red teamers, and defensive security professionals. Please ensure:

1. Code follows security best practices
2. Tools include proper documentation
3. Ethical use guidelines are maintained
4. Legal compliance is prioritized

## 📄 License

This project is licensed under the MIT License - see the main LICENSE file for details.

## 🆘 Support

For questions, issues, or contributions:
1. Review tool documentation
2. Check existing issues
3. Follow responsible disclosure
4. Maintain professional conduct

---

**Remember**: These tools are for educational and authorized testing purposes only. Always ensure you have proper authorization before using them in any environment.
