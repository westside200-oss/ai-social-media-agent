# AI Social Media Agent - Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Git
- Anthropic API Key
- Social media platform API credentials (Instagram, TikTok)

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/westside200-oss/ai-social-media-agent.git
cd ai-social-media-agent
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Start with Docker Compose
```bash
docker-compose up -d
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Initialize Database
```bash
docker-compose exec backend python -m alembic upgrade head
```

## Production Deployment

### Option 1: DigitalOcean (Recommended for Budget)

#### Prerequisites
- DigitalOcean Account
- Droplet (2GB RAM, 50GB SSD minimum)
- Ubuntu 22.04 LTS

#### Deployment Steps

1. **SSH into your droplet**
```bash
ssh root@your_droplet_ip
```

2. **Install Docker & Docker Compose**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone Repository**
```bash
cd /opt
sudo git clone https://github.com/westside200-oss/ai-social-media-agent.git
cd ai-social-media-agent
```

4. **Setup Environment**
```bash
sudo cp .env.example .env
sudo nano .env  # Edit with your credentials
```

5. **Start Services**
```bash
sudo docker-compose up -d
```

6. **Setup Nginx Reverse Proxy**
```bash
sudo apt-get update
sudo apt-get install nginx -y
```

Create `/etc/nginx/sites-available/ai-social-media`:
```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name your_domain.com;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/ai-social-media /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Enable HTTPS (Let's Encrypt)**
```bash
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your_domain.com
```

### Option 2: Heroku

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create your-app-name
```

4. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:standard-0
```

5. **Set Environment Variables**
```bash
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set ENCRYPTION_KEY=your_key
heroku config:set SECRET_KEY=your_secret
```

6. **Deploy**
```bash
git push heroku main
```

## Monitoring & Logs

### Docker Logs
```bash
# Backend
docker-compose logs -f backend

# Frontend
docker-compose logs -f frontend

# Database
docker-compose logs -f postgres
```

### Database Backup
```bash
docker-compose exec postgres pg_dump -U social_media ai_social_media > backup.sql
```

## Scaling Considerations

- Use Redis for caching (optional upgrade)
- Implement database indexing on frequently queried fields
- Use CDN for static frontend assets
- Implement rate limiting on API endpoints
- Consider separate worker instances for background jobs

## Security Checklist

- [ ] Change default database credentials
- [ ] Generate strong encryption keys
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Regular database backups
- [ ] Monitor API rate limits
- [ ] Rotate API tokens regularly
- [ ] Use environment-specific secrets

## Troubleshooting

### Database Connection Issues
```bash
docker-compose exec backend python -c "from app.database import engine; engine.connect()"
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# Or kill existing process:
lsof -ti:8000 | xargs kill -9
```

### Frontend API Connection
Ensure `REACT_APP_API_URL` is correctly set in `.env`

## Support

For issues, check:
1. GitHub Issues: https://github.com/westside200-oss/ai-social-media-agent/issues
2. Docker logs
3. Database connectivity
4. API key validity
