# Deployment Configuration for HTTPS

## Overview
This document outlines the HTTPS configuration and deployment setup for the LibraryProject Django application.

## Django HTTPS Settings

The following security settings have been configured in `settings.py`:

### 1. HTTPS Enforcement
- **SECURE_SSL_REDIRECT = True**: Redirects all HTTP traffic to HTTPS automatically
- **SECURE_HSTS_SECONDS = 31536000**: Enforces HTTPS for one year (browsers remember this)
- **SECURE_HSTS_INCLUDE_SUBDOMAINS = True**: Applies HTTPS requirement to all subdomains
- **SECURE_HSTS_PRELOAD = True**: Allows the site to be included in browser HSTS preload lists

### 2. Secure Cookie Configuration
- **SESSION_COOKIE_SECURE = True**: Session cookies only transmitted over HTTPS
- **CSRF_COOKIE_SECURE = True**: CSRF tokens only transmitted over HTTPS

### 3. Additional Security Headers
- **SECURE_CONTENT_TYPE_NOSNIFF = True**: Prevents MIME-sniffing attacks
- **SECURE_BROWSER_XSS_FILTER = True**: Enables browser XSS protection
- **X_FRAME_OPTIONS = 'DENY'**: Prevents clickjacking attacks

## Web Server Configuration

### Nginx Configuration Example
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # SSL Certificate Configuration
    ssl_certificate /etc/ssl/certs/your_certificate.crt;
    ssl_certificate_key /etc/ssl/private/your_private_key.key;
    
    # SSL Protocol and Cipher Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS Header (handled by Django, but can be set here too)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /path/to/your/static/files/;
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/media/files/;
    }
}
```

### Apache Configuration Example
```apache
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    
    # Redirect HTTP to HTTPS
    Redirect permanent / https://example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName example.com
    ServerAlias www.example.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/your_certificate.crt
    SSLCertificateKeyFile /etc/ssl/private/your_private_key.key
    SSLCertificateChainFile /etc/ssl/certs/your_chain.crt
    
    # SSL Protocol Configuration
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite HIGH:!aNULL:!MD5
    
    # HSTS Header
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    
    # Django Application
    WSGIDaemonProcess libraryproject python-home=/path/to/venv python-path=/path/to/project
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/project/LibraryProject/wsgi.py
    
    <Directory /path/to/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    # Static files
    Alias /static /path/to/static
    <Directory /path/to/static>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media /path/to/media
    <Directory /path/to/media>
        Require all granted
    </Directory>
</VirtualHost>
```

## SSL Certificate Setup

### Using Let's Encrypt (Recommended for Production)
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate for Nginx
sudo certbot --nginx -d example.com -d www.example.com

# Or for Apache
sudo certbot --apache -d example.com -d www.example.com

# Auto-renewal is set up automatically
# Test renewal with:
sudo certbot renew --dry-run
```

### Development/Testing SSL Certificate

For development, you can create a self-signed certificate:
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

**Note**: Self-signed certificates will show browser warnings and should NOT be used in production.

## Testing HTTPS Configuration

### 1. Test SSL/TLS Configuration
- Use [SSL Labs](https://www.ssllabs.com/ssltest/) to test your SSL configuration
- Target: A+ rating

### 2. Verify HSTS Headers
```bash
curl -I https://example.com
# Should see: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### 3. Test HTTP to HTTPS Redirect
```bash
curl -I http://example.com
# Should see: 301 Moved Permanently, Location: https://example.com/
```

## Environment-Specific Settings

### Development
For local development without HTTPS, you can temporarily disable these settings:
```python
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
```

### Production
Ensure all security settings are enabled (as configured in settings.py).

## Security Checklist

- [ ] SSL/TLS certificate installed and valid
- [ ] HTTPS redirect configured
- [ ] HSTS headers properly set
- [ ] Cookie security flags enabled
- [ ] Security headers configured
- [ ] SSL Labs test shows A+ rating
- [ ] All resources loaded over HTTPS (no mixed content)

## Maintenance

- Certificates must be renewed before expiration (Let's Encrypt: every 90 days)
- Monitor certificate expiration dates
- Regularly update SSL/TLS protocols and ciphers
- Keep Django and dependencies updated for security patches