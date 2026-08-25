# Comprehensive Quick Start Guide

## 🏃 Quick Start (5 minutes)

### Using Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/westside200-oss/ai-social-media-agent.git
cd ai-social-media-agent

# 2. Setup environment
cp .env.example .env
# Edit .env with your credentials:
# - ANTHROPIC_API_KEY
# - Social media API credentials
# - Database password

# 3. Start everything
docker-compose up -d

# 4. Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

### Local Development Setup

```bash
# 1. Run setup script
bash scripts/setup-dev.sh

# 2. Activate backend environment
cd backend
source venv/bin/activate

# 3. Create database
python -c "from app.database import init_db; init_db()"

# 4. Start backend (new terminal)
python app/main.py

# 5. Start frontend (another terminal)
cd frontend
npm start
```

## 📋 First Steps After Setup

### 1. Add Your First Account

```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "instagram",
    "username": "your_username",
    "account_name": "My Fashion Brand",
    "account_id": "your_account_id",
    "account_type": "business",
    "access_token": "your_access_token"
  }'
```

### 2. Generate AI Content

```bash
curl -X POST http://localhost:8000/api/posts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 1,
    "platform": "instagram",
    "theme": "new_arrivals",
    "additional_context": "Summer collection launch"
  }'
```

### 3. View Dashboard

Open http://localhost:3000 in your browser

## 🔑 Required API Keys

1. **Anthropic Claude API Key**
   - Get from: https://console.anthropic.com
   - Save to: `ANTHROPIC_API_KEY`

2. **Instagram Business Account**
   - Access Token from: Meta Developer Portal
   - Account ID: Your Instagram Business Account ID

3. **TikTok API**
   - Client Key and Secret from: https://developer.tiktok.com

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change ports in docker-compose.yml
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs postgres
```

### API Key Invalid
```bash
# Verify key in .env
cat .env | grep ANTHROPIC_API_KEY

# Test connection
curl http://localhost:8000/health
```

## 📚 Next Steps

- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Check [README.md](README.md) for full documentation
- Review backend code in `backend/app/agents/` for content generation logic

## 🆘 Support

- GitHub Issues: https://github.com/westside200-oss/ai-social-media-agent/issues
- Docker Compose logs: `docker-compose logs -f`
- API documentation: http://localhost:8000/docs

---

**Happy content creation! 🚀**
