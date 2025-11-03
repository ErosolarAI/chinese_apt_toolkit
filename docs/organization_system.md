# Organization Management System

## Overview

The Organization Management System provides advanced capabilities for discovering, profiling, and targeting organizations using the APT Toolkit's email intelligence corpus and deepseek-reasoner integration.

## Features

### 1. Organization Discovery
- **List Organizations**: Discover all organizations in the email database
- **Search Organizations**: Find organizations by name using substring matching
- **Organization Statistics**: Get detailed statistics about email counts, domains, and sample data

### 2. Organization Profiling
- **Basic Profiles**: Generate profiles using database information only
- **Enhanced Profiles**: Use deepseek-reasoner to create detailed organization profiles including:
  - Industry classification
  - Company size estimation
  - Security posture assessment
  - Key employee roles
  - Potential attack vectors

### 3. Attack Planning
- **Custom Attack Plans**: Generate tailored attack plans for specific organizations
- **Multiple Attack Types**: Support for spear_phishing, supply_chain, lateral_movement, and persistence attacks
- **Deepseek Integration**: Use deepseek-reasoner to create unique, organization-specific attack strategies

### 4. Landscape Analysis
- **Industry Distribution**: Analyze the distribution of organizations by industry
- **Size Distribution**: Understand the size distribution of target organizations
- **Security Posture Summary**: Get an overview of security postures across organizations

## Usage

### Command Line Interface

The organization management system can be accessed through the enhanced CLI:

```bash
# List organizations
python3 -m apt_toolkit.cli_enhanced list --limit 20

# Search for organizations
python3 -m apt_toolkit.cli_enhanced search "Technology" --limit 10

# Generate organization profile
python3 -m apt_toolkit.cli_enhanced profile "Acme Corporation"

# Generate attack plan
python3 -m apt_toolkit.cli_enhanced attack-plan "Acme Corporation" --type spear_phishing

# Get organization emails
python3 -m apt_toolkit.cli_enhanced emails "Acme Corporation" --limit 10

# Analyze organization landscape
python3 -m apt_toolkit.cli_enhanced landscape --limit 15
```

### Python API

```python
from apt_toolkit.organization_manager import OrganizationManager

with OrganizationManager() as manager:
    # List organizations
    organizations = manager.list_organizations(limit=50)
    
    # Generate profile with deepseek
    profile = manager.generate_organization_profile("Target Corp", use_deepseek=True)
    
    # Generate attack plan
    attack_plan = manager.generate_attack_plan(
        "Target Corp", 
        attack_type="spear_phishing", 
        use_deepseek=True
    )
    
    # Analyze landscape
    landscape = manager.analyze_organization_landscape(limit=10)
```

## Deepseek Integration

The system integrates with deepseek-reasoner to generate unique content:

### Configuration

1. Add your Deepseek API key to `config/secrets.json`:
```json
{
  "DEEPSEEK_API_KEY": "your_api_key_here"
}
```

2. The system will automatically use deepseek-reasoner when available
3. Fallback to basic profiles when API is unavailable

### Enhanced Features with Deepseek

- **Realistic Organization Profiles**: Generate detailed descriptions, industry classifications, and security assessments
- **Unique Attack Plans**: Create tailored attack strategies specific to each organization
- **Context-Aware Content**: Generate realistic phishing emails and attack scenarios

## Example Output

### Organization Profile
```json
{
  "organization": "Acme Corporation",
  "email_count": 245,
  "domains": ["acme.com", "acme-corp.com"],
  "description": "A leading technology company specializing in enterprise software solutions...",
  "industry": "Technology",
  "size": "large",
  "key_employees": ["CEO", "CTO", "Head of Security", "IT Director"],
  "security_posture": "medium",
  "attack_vectors": ["spear_phishing", "supply_chain", "credential_stuffing"]
}
```

### Attack Plan
```json
{
  "organization": "Acme Corporation",
  "attack_type": "spear_phishing",
  "strategy": "Target IT department with fake security update notifications",
  "steps": [
    {
      "phase": "reconnaissance",
      "action": "Identify key IT personnel and their email patterns",
      "tools": ["theharvester", "linkedin"]
    },
    {
      "phase": "initial_access", 
      "action": "Send targeted phishing emails with malicious attachments",
      "tools": ["gophish", "setoolkit"]
    }
  ],
  "techniques": ["spear_phishing", "attachment_based_execution"],
  "challenges": ["MFA enabled", "Security awareness training"],
  "mitigations": ["Use trusted domains", "Social engineering techniques"]
}
```

## Testing

Run the organization management tests:

```bash
cd tests
python3 -m pytest test_organization_manager.py -v
python3 -m pytest test_organization_cli.py -v
```

## Demo

Run the demonstration script to see the system in action:

```bash
python3 examples/organization_demo.py
```

## Integration with Existing Toolkit

The Organization Management System integrates seamlessly with existing APT Toolkit modules:

- **Email Repository**: Leverages the existing email database for organization discovery
- **Initial Access**: Generates targeted spear-phishing campaigns
- **Campaign Orchestration**: Provides organization-specific targeting for campaigns
- **Logging**: All operations are logged through the standard campaign logging system

## Security Considerations

- All organization data is sourced from the existing email intelligence corpus
- Deepseek integration requires proper API key management
- Generated content should be used only for authorized security testing
- Always comply with local laws and customer scoping agreements