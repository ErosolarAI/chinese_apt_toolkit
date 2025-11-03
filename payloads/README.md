# Payloads Repository

This directory contains comprehensive payloads organized by:
- **Campaign Types** - Payloads tailored for specific campaign scenarios
- **Tools** - Payloads designed for specific APT toolkit tools
- **Organizations** - Targeted payloads based on email database organizations
- **Payload Categories** - General payload types for various attack vectors

## Structure

```
payloads/
├── campaigns/              # Campaign-specific payloads
│   ├── financial_institution/
│   ├── government_agency/
│   ├── healthcare/
│   └── ...
├── tools/                  # Tool-specific payloads
│   ├── lightc2/
│   ├── powershell/
│   ├── memory_injector/
│   └── ...
├── organizations/          # Organization-targeted payloads
│   ├── google/
│   ├── ibm/
│   ├── stanford_university/
│   └── ...
├── categories/             # General payload categories
│   ├── phishing/
│   ├── persistence/
│   ├── data_exfiltration/
│   ├── reconnaissance/
│   └── ...
└── templates/              # Payload templates
    ├── email_templates/
    ├── document_templates/
    └── script_templates/
```

## Usage

Each payload includes:
- Description and use case
- Target environment
- Required dependencies
- Configuration options
- Detection avoidance features

## Generation

Payloads are generated using data from the emails database and can be customized for specific targets using the organization-specific email patterns and domains.