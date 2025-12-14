# Deployment Guide - Social Media API

## Prerequisites
- Python 3.13.7
- PostgreSQL database (for production)
- Git
- Hosting account (Heroku, Railway, or similar)

## Environment Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file based on `.env.example`:
```bash
SECRET_KEY=your-actual-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,.herokuapp.com
DATABASE_URL=postgres://user:password@host:port/database
```

### 3. Database Migration
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Collect Static Files
```bash
python manage.py collectstatic --no-input
```

## Deployment Steps

### Option 1: Heroku Deployment

#### 1. Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

#### 2. Login to Heroku
```bash
heroku login
```

#### 3. Create Heroku App
```bash
heroku create your-app-name
```

#### 4. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

#### 5. Set Environment Variables
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='.herokuapp.com'
```

#### 6. Deploy
```bash
git push heroku main
```

#### 7. Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Option 2: Railway Deployment

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login to Railway
```bash
railway login
```

#### 3. Initialize Project
```bash
railway init
```

#### 4. Add PostgreSQL
```bash
railway add postgresql
```

#### 5. Deploy
```bash
railway up
```

### Option 3: Manual Server Deployment

#### 1. Update System
```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. Install Dependencies
```bash
sudo apt install python3-pip python3-venv postgresql nginx -y
```

#### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Configure Gunicorn
Create `/etc/systemd/system/gunicorn.service`:
```
[Unit]
Description=Gunicorn daemon for Social Media API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/social_media_api
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/path/to/social_media_api.sock \
    social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 5. Configure Nginx
Create `/etc/nginx/sites-available/social_media_api`:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/social_media_api;
    }

    location /media/ {
        root /path/to/social_media_api;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/social_media_api.sock;
    }
}
```

#### 6. Enable Nginx Site
```bash
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. Start Gunicorn
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## Security Checklist

- [x] `DEBUG = False` in production
- [x] `SECRET_KEY` stored in environment variables
- [x] `ALLOWED_HOSTS` configured
- [x] HTTPS enabled (SSL certificate)
- [x] Security headers configured
- [x] Database credentials secured
- [x] Static files served via WhiteNoise or CDN
- [x] CORS configured if needed
- [x] Rate limiting implemented

## Post-Deployment

### 1. Test All Endpoints
```bash
curl https://your-api.com/api/posts/
curl https://your-api.com/register/
curl https://your-api.com/login/
```

### 2. Monitor Application
- Set up error logging (Sentry, Rollbar)
- Monitor performance (New Relic, DataDog)
- Track uptime (UptimeRobot, Pingdom)

### 3. Regular Maintenance
- Update dependencies monthly
- Review security advisories
- Backup database regularly
- Monitor disk space and memory

## Troubleshooting

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --no-input
```

**Database connection errors:**
- Check `DATABASE_URL` environment variable
- Verify database credentials
- Ensure database service is running

**502 Bad Gateway:**
- Check Gunicorn is running
- Verify Nginx configuration
- Check application logs

**CSRF token errors:**
- Verify `CSRF_TRUSTED_ORIGINS` includes your domain
- Check HTTPS configuration

## Monitoring Commands
```bash
# Check application status
heroku ps  # For Heroku
railway status  # For Railway

# View logs
heroku logs --tail
railway logs

# Run management commands
heroku run python manage.py migrate
railway run python manage.py migrate
```

## Rollback Procedure

### Heroku
```bash
heroku releases
heroku rollback v123
```

### Railway
```bash
railway rollback
```

## Support

For issues or questions:
- Check logs first
- Review documentation
- Contact support team

---

**Last Updated:** December 2025
**Version:** 1.0.0