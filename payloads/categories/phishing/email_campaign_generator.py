#!/usr/bin/env python3
"""
Email Campaign Generator for Phishing Attacks
Generates targeted phishing emails based on organization and campaign type
"""

import os
import json
import random
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime, timedelta
from pathlib import Path

class EmailCampaignGenerator:
    def __init__(self, emails_db_path="emails/unique_emails.db"):
        self.db_path = emails_db_path
        self.templates = self.load_templates()
    
    def load_templates(self):
        """Load email templates for different campaign types"""
        return {
            "password_reset": {
                "subject": "Security Alert: Password Reset Required",
                "body": """Dear {recipient_name},

Our security system has detected unusual login activity on your {organization} account. 
To protect your information, we require you to reset your password immediately.

Click here to reset your password: {malicious_link}

If you did not request this password reset, please contact our support team immediately.

Best regards,
{organization} Security Team"""
            },
            "invoice": {
                "subject": "Invoice #{invoice_number} - Payment Required",
                "body": """Dear {recipient_name},

Please find attached invoice #{invoice_number} for services rendered.
Total Amount Due: ${amount}
Due Date: {due_date}

You can view and pay your invoice here: {malicious_link}

If you have any questions about this invoice, please contact our billing department.

Thank you for your business.

Sincerely,
{organization} Billing Department"""
            },
            "hr_policy": {
                "subject": "Important HR Policy Update - Action Required",
                "body": """Dear {recipient_name},

Please review the attached HR policy update that requires your immediate attention. 
All employees must acknowledge receipt of these policy changes by {due_date}.

Access the policy document here: {malicious_link}

Failure to acknowledge these changes may result in disciplinary action.

Thank you for your cooperation.

Best regards,
Human Resources Department
{organization}"""
            },
            "system_update": {
                "subject": "System Maintenance Notification",
                "body": """Dear {recipient_name},

We will be performing critical system maintenance on {maintenance_date} from {start_time} to {end_time}.
During this time, you may experience temporary service interruptions.

To ensure uninterrupted service, please install the latest update:
{malicious_link}

If you have any questions, please contact the IT Help Desk.

Thank you for your understanding.

Sincerely,
IT Department
{organization}"""
            },
            "ceo_fraud": {
                "subject": "URGENT: Wire Transfer Request",
                "body": """Team,

I need you to process an urgent wire transfer for a confidential business acquisition.
This is time-sensitive and requires immediate attention.

Amount: ${amount}
Recipient: {recipient_name}
Account: {account_number}
Routing: {routing_number}

Process the transfer here: {malicious_link}

Do not discuss this with anyone else in the organization.

Regards,
{ceo_name}
CEO, {organization}"""
            }
        }
    
    def generate_phishing_email(self, template_name, recipient_data, organization, malicious_link):
        """Generate a phishing email using the specified template"""
        
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name]
        
        # Generate dynamic content based on template
        dynamic_data = {
            "recipient_name": recipient_data.get("name", "Valued Employee"),
            "organization": organization,
            "malicious_link": malicious_link,
            "invoice_number": str(random.randint(10000, 99999)),
            "amount": f"{random.randint(1, 50)},{random.randint(100, 999)}",
            "due_date": (datetime.now() + timedelta(days=7)).strftime("%B %d, %Y"),
            "maintenance_date": (datetime.now() + timedelta(days=2)).strftime("%A, %B %d"),
            "start_time": "10:00 PM",
            "end_time": "2:00 AM",
            "ceo_name": "John Smith",  # Would be dynamic in real scenario
            "account_number": "".join([str(random.randint(0, 9)) for _ in range(10)]),
            "routing_number": "".join([str(random.randint(0, 9)) for _ in range(9)])
        }
        
        subject = template["subject"].format(**dynamic_data)
        body = template["body"].format(**dynamic_data)
        
        return {
            "subject": subject,
            "body": body,
            "template": template_name,
            "organization": organization,
            "recipient": recipient_data,
            "malicious_link": malicious_link,
            "generated_at": datetime.now().isoformat()
        }
    
    def create_email_campaign(self, campaign_name, template_name, organization, 
                            recipient_list, malicious_link, sender_email=None):
        """Create a complete email campaign"""
        
        campaign = {
            "campaign_name": campaign_name,
            "template": template_name,
            "organization": organization,
            "malicious_link": malicious_link,
            "sender_email": sender_email,
            "created_at": datetime.now().isoformat(),
            "emails": []
        }
        
        for recipient in recipient_list:
            email = self.generate_phishing_email(
                template_name, 
                recipient, 
                organization, 
                malicious_link
            )
            campaign["emails"].append(email)
        
        return campaign
    
    def save_campaign(self, campaign, output_dir="payloads/categories/phishing"):
        """Save campaign to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save campaign configuration
        campaign_file = os.path.join(output_dir, f"{campaign['campaign_name']}_campaign.json")
        with open(campaign_file, 'w') as f:
            json.dump(campaign, f, indent=2)
        
        # Save individual emails
        emails_dir = os.path.join(output_dir, campaign['campaign_name'])
        os.makedirs(emails_dir, exist_ok=True)
        
        for i, email in enumerate(campaign['emails']):
            email_file = os.path.join(emails_dir, f"email_{i+1}.txt")
            with open(email_file, 'w') as f:
                f.write(f"Subject: {email['subject']}\n\n")
                f.write(email['body'])
        
        return campaign_file
    
    def generate_smtp_config(self, smtp_server, smtp_port, username, password):
        """Generate SMTP configuration for sending emails"""
        
        config = {
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "username": username,
            "password": password,
            "use_tls": True,
            "batch_size": 50,  # Emails per batch
            "delay_between_batches": 60  # seconds
        }
        
        return config

def main():
    """Generate sample phishing campaigns"""
    generator = EmailCampaignGenerator()
    
    print("Generating phishing email campaigns...")
    
    # Sample recipient data (in real scenario, this would come from emails database)
    sample_recipients = [
        {"name": "John Doe", "email": "john.doe@example.com"},
        {"name": "Jane Smith", "email": "jane.smith@example.com"},
        {"name": "Bob Johnson", "email": "bob.johnson@example.com"}
    ]
    
    # Generate password reset campaign
    password_campaign = generator.create_email_campaign(
        campaign_name="password_reset_campaign",
        template_name="password_reset",
        organization="Example Corporation",
        recipient_list=sample_recipients,
        malicious_link="https://malicious-site.com/reset-password"
    )
    
    campaign_file = generator.save_campaign(password_campaign)
    print(f"Created password reset campaign: {campaign_file}")
    
    # Generate CEO fraud campaign
    ceo_campaign = generator.create_email_campaign(
        campaign_name="ceo_fraud_campaign", 
        template_name="ceo_fraud",
        organization="Acme Inc.",
        recipient_list=sample_recipients,
        malicious_link="https://fake-bank.com/wire-transfer"
    )
    
    ceo_file = generator.save_campaign(ceo_campaign)
    print(f"Created CEO fraud campaign: {ceo_file}")
    
    print("\nPhishing email campaigns generated successfully!")
    print("Use responsibly and only for authorized security testing.")

if __name__ == "__main__":
    main()