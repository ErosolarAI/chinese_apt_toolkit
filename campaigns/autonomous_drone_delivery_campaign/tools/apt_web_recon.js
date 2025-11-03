#!/usr/bin/env node
/*
APT Web Reconnaissance Toolkit
Advanced web reconnaissance and information gathering
For educational and authorized penetration testing only
*/

const https = require('https');
const http = require('http');
const dns = require('dns');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

class APTWebRecon {
    constructor() {
        this.results = {
            domain: '',
            timestamp: new Date().toISOString(),
            dns: {},
            http: {},
            security: {},
            technologies: [],
            subdomains: []
        };
    }

    printBanner() {
        const banner = `APT Web Reconnaissance Toolkit`;
        console.log(banner);
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async dnsLookup(domain) {
        return new Promise((resolve, reject) => {
            dns.resolve4(domain, (err, addresses) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(addresses);
                }
            });
        });
    }

    async getDNSRecords(domain) {
        const recordTypes = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME'];
        const results = {};

        for (const type of recordTypes) {
            try {
                results[type] = await this.resolveDNS(domain, type);
            } catch (error) {
                results[type] = [`Error: ${error.message}`];
            }
            await this.sleep(100); // Rate limiting
        }

        return results;
    }

    resolveDNS(domain, type) {
        return new Promise((resolve, reject) => {
            dns.resolve(domain, type, (err, records) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(records);
                }
            });
        });
    }

    async httpRequest(url, options = {}) {
        return new Promise((resolve, reject) => {
            const parsedUrl = new URL(url);
            const protocol = parsedUrl.protocol === 'https:' ? https : http;
            
            const reqOptions = {
                hostname: parsedUrl.hostname,
                port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
                path: parsedUrl.pathname + parsedUrl.search,
                method: 'GET',
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    ...options.headers
                },
                timeout: 10000,
                ...options
            };

            const req = protocol.request(reqOptions, (res) => {
                let data = '';
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
                res.on('end', () => {
                    resolve({
                        statusCode: res.statusCode,
                        headers: res.headers,
                        body: data,
                        url: url
                    });
                });
            });

            req.on('error', (err) => {
                reject(err);
            });

            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Request timeout'));
            });

            req.end();
        });
    }

    async analyzeHeaders(headers) {
        const securityHeaders = [
            'strict-transport-security',
            'content-security-policy',
            'x-frame-options',
            'x-content-type-options',
            'x-xss-protection',
            'referrer-policy'
        ];

        const analysis = {};
        
        securityHeaders.forEach(header => {
            analysis[header] = headers[header] || 'Not Present';
        });

        return analysis;
    }

    detectTechnologies(headers, body) {
        const technologies = [];
        const techPatterns = {
            'WordPress': /wp-content|wp-includes|wordpress/i,
            'Joomla': /joomla/i,
            'Drupal': /drupal/i,
            'Apache': /apache/i,
            'Nginx': /nginx/i,
            'IIS': /microsoft-iis/i,
            'PHP': /php/i,
            'ASP.NET': /asp\.net|aspx/i,
            'jQuery': /jquery/i,
            'React': /react/i,
            'Angular': /angular/i,
            'Vue.js': /vue/i,
            'Bootstrap': /bootstrap/i,
            'Google Analytics': /google-analytics|ga\.js/i,
            'Cloudflare': /cloudflare/i
        };

        // Check headers
        const serverHeader = headers['server'] || '';
        const poweredBy = headers['x-powered-by'] || '';
        
        Object.entries(techPatterns).forEach(([tech, pattern]) => {
            if (pattern.test(serverHeader) || pattern.test(poweredBy) || pattern.test(body)) {
                technologies.push(tech);
            }
        });

        return [...new Set(technologies)]; // Remove duplicates
    }

    async findSubdomains(domain, wordlist = null) {
        const commonSubdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'staging',
            'dev', 'blog', 'shop', 'api', 'admin', 'forum', 'support', 'help', 'docs', 'news',
            'app', 'apps', 'secure', 'vpn', 'portal', 'download', 'uploads', 'cdn', 'media',
            'static', 'assets', 'img', 'images', 'js', 'css', 'files', 'backup', 'db', 'database'
        ];

        const subdomainsToCheck = wordlist || commonSubdomains;
        const foundSubdomains = [];

        for (const subdomain of subdomainsToCheck) {
            const fullDomain = `${subdomain}.${domain}`;
            
            try {
                const addresses = await this.dnsLookup(fullDomain);
                if (addresses && addresses.length > 0) {
                    foundSubdomains.push({
                        subdomain: fullDomain,
                        ip: addresses[0]
                    });
                    console.log(`[+] Found subdomain: ${fullDomain} -> ${addresses[0]}`);
                }
            } catch (error) {
                // Subdomain doesn't exist or can't be resolved
            }
            
            await this.sleep(50); // Rate limiting
        }

        return foundSubdomains;
    }

    async scanDomain(domain, options = {}) {
        this.results.domain = domain;
        
        console.log(`[*] Starting reconnaissance for: ${domain}`);
        
        // DNS Analysis
        console.log('[*] Performing DNS analysis...');
        try {
            this.results.dns = await this.getDNSRecords(domain);
            console.log('[+] DNS analysis completed');
        } catch (error) {
            console.log('[-] DNS analysis failed:', error.message);
        }

        // HTTP Analysis
        console.log('[*] Performing HTTP analysis...');
        try {
            const httpResponse = await this.httpRequest(`http://${domain}`);
            const httpsResponse = await this.httpRequest(`https://${domain}`);
            
            this.results.http = {
                http: {
                    status: httpResponse.statusCode,
                    headers: httpResponse.headers
                },
                https: {
                    status: httpsResponse.statusCode,
                    headers: httpsResponse.headers
                }
            };

            // Security headers analysis
            this.results.security = await this.analyzeHeaders(httpsResponse.headers || httpResponse.headers);
            
            // Technology detection
            this.results.technologies = this.detectTechnologies(
                httpsResponse.headers || httpResponse.headers,
                httpsResponse.body || httpResponse.body
            );
            
            console.log('[+] HTTP analysis completed');
        } catch (error) {
            console.log('[-] HTTP analysis failed:', error.message);
        }

        // Subdomain enumeration
        if (options.subdomains) {
            console.log('[*] Enumerating subdomains...');
            try {
                this.results.subdomains = await this.findSubdomains(domain, options.wordlist);
                console.log(`[+] Found ${this.results.subdomains.length} subdomains`);
            } catch (error) {
                console.log('[-] Subdomain enumeration failed:', error.message);
            }
        }

        return this.results;
    }

    generateReport(results, outputFile = null) {
        const report = {
            metadata: {
                tool: 'APT Web Reconnaissance Toolkit',
                version: '1.0.0',
                timestamp: results.timestamp,
                domain: results.domain
            },
            results: results
        };

        if (outputFile) {
            fs.writeFileSync(outputFile, JSON.stringify(report, null, 2));
            console.log(`[+] Report saved to: ${outputFile}`);
        }

        return report;
    }

    printResults(results) {
        console.log('\n[*] Reconnaissance Results:');
        console.log('=' .repeat(50));
        
        console.log('\nDNS Records:');
        Object.entries(results.dns).forEach(([type, records]) => {
            console.log(`  ${type}: ${records.join(', ')}`);
        });

        console.log('\nHTTP Information:');
        if (results.http.http) {
            console.log(`  HTTP Status: ${results.http.http.status}`);
        }
        if (results.http.https) {
            console.log(`  HTTPS Status: ${results.http.https.status}`);
        }

        console.log('\nSecurity Headers:');
        Object.entries(results.security).forEach(([header, value]) => {
            console.log(`  ${header}: ${value}`);
        });

        console.log('\nDetected Technologies:');
        if (results.technologies.length > 0) {
            results.technologies.forEach(tech => console.log(`  - ${tech}`));
        } else {
            console.log('  None detected');
        }

        console.log('\nSubdomains:');
        if (results.subdomains.length > 0) {
            results.subdomains.forEach(sub => console.log(`  - ${sub.subdomain} -> ${sub.ip}`));
        } else {
            console.log('  None found');
        }
    }
}

// CLI Interface
async function main() {
    const recon = new APTWebRecon();
    recon.printBanner();

    const args = process.argv.slice(2);
    
    if (args.length === 0 || args.includes('--help')) {
        console.log('\nUsage: node apt_web_recon.js [OPTIONS] <domain>');
        console.log('\nOPTIONS:');
        console.log('  --subdomains     Enumerate subdomains');
        console.log('  --wordlist FILE  Use custom subdomain wordlist');
        console.log('  --output FILE    Save results to JSON file');
        console.log('  --help           Show this help message');
        console.log('\nEXAMPLES:');
        console.log('  node apt_web_recon.js example.com');
        console.log('  node apt_web_recon.js --subdomains --output results.json example.com');
        return;
    }

    const domain = args[args.length - 1];
    const options = {
        subdomains: args.includes('--subdomains'),
        wordlist: null,
        output: null
    };

    const wordlistIndex = args.indexOf('--wordlist');
    if (wordlistIndex !== -1 && args[wordlistIndex + 1]) {
        try {
            options.wordlist = fs.readFileSync(args[wordlistIndex + 1], 'utf8')
                .split('\n')
                .map(line => line.trim())
                .filter(line => line && !line.startsWith('#'));
        } catch (error) {
            console.log('[-] Error reading wordlist file:', error.message);
        }
    }

    const outputIndex = args.indexOf('--output');
    if (outputIndex !== -1 && args[outputIndex + 1]) {
        options.output = args[outputIndex + 1];
    }

    try {
        const results = await recon.scanDomain(domain, options);
        recon.printResults(results);
        
        if (options.output) {
            recon.generateReport(results, options.output);
        }
        
        console.log('\n[+] Reconnaissance completed successfully');
    } catch (error) {
        console.log('[-] Error during reconnaissance:', error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = APTWebRecon;