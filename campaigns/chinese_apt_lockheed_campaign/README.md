# Chinese APT Campaign: Operation Dragon's Fire

This campaign simulates an Advanced Persistent Threat (APT) operation attributed to a Chinese state-sponsored actor, targeting high-value United States defense contractors and government agencies.

## Campaign Objectives

1.  **Initial Access**: Gain a foothold in the target network through sophisticated phishing campaigns and exploitation of public-facing applications.
2.  **Persistence**: Establish long-term persistence using multi-layered techniques, including WMI event subscriptions, COM hijacking, and scheduled tasks.
3.  **Defense Evasion**: Bypass security controls using hidden backdoors, covert communication channels, and anti-detection measures.
4.  **Command and Control**: Maintain covert communication with compromised systems using DNS and ICMP tunneling.
5.  **Data Exfiltration**: Exfiltrate sensitive data, including intellectual property, defense secrets, and classified information.

## Primary Targets

*   Lockheed Martin
*   Northrop Grumman
*   Raytheon Technologies
*   General Dynamics
*   Boeing

## Secondary Targets

*   Department of Defense (DoD) networks
*   Department of Energy (DoE) national laboratories
*   Key government infrastructure networks

## Toolkit

This campaign utilizes the APT Toolkit, with customized modules for this specific operation. The toolkit provides capabilities for all phases of the attack lifecycle, from initial access to data exfiltration.

## Running a Real Campaign

This campaign can be configured to run against real targets for authorized penetration testing.

To run a real campaign, you will need to create a `config.json` file in this directory. You can use the `config.json.example` file as a template.

Populate the `config.json` file with the actual information for your authorized target.

Once you have configured your target, you can run the campaign using the following command:

```
python run_campaign.py
```
