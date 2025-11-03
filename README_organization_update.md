# Organization Management System - New Feature

## Overview

The APT Toolkit now includes an advanced Organization Management System that provides sophisticated organization discovery, profiling, and targeting capabilities with deepseek-reasoner integration.

## Key Features

### Organization Discovery
- **List Organizations**: Discover all organizations from the email database
- **Search Organizations**: Find organizations by name using substring matching
- **Organization Statistics**: Get detailed statistics about email counts, domains, and sample data

### Enhanced Profiling with Deepseek
- **Basic Profiles**: Generate profiles using database information only
- **Enhanced Profiles**: Use deepseek-reasoner to create detailed organization profiles including:
  - Industry classification
  - Company size estimation
  - Security posture assessment
  - Key employee roles
  - Potential attack vectors

### Attack Planning
- **Custom Attack Plans**: Generate tailored attack plans for specific organizations
- **Multiple Attack Types**: Support for spear_phishing, supply_chain, lateral_movement, and persistence attacks
- **Deepseek Integration**: Use deepseek-reasoner to create unique, organization-specific attack strategies

### Landscape Analysis
- **Industry Distribution**: Analyze the distribution of organizations by industry
- **Size Distribution**: Understand the size distribution of target organizations
- **Security Posture Summary**: Get an overview of security postures across organizations

## Usage

### Command Line Interface

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

## Documentation

See `docs/organization_system.md` for detailed documentation and examples.

## Integration with Existing Toolkit

The Organization Management System integrates seamlessly with existing APT Toolkit modules:

- **Email Repository**: Leverages the existing email database for organization discovery
- **Initial Access**: Generates targeted spear-phishing campaigns
- **Campaign Orchestration**: Provides organization-specific targeting for campaigns
- **Logging**: All operations are logged through the standard campaign logging system