# AI Social Media Agent 🤖📱

Automated AI-powered content creation and posting agent for fashion & fabric marketplace. Generates original, platform-specific content and automatically posts to Instagram and TikTok.

## Features

✨ **AI Content Generation** - Anthropic Claude generates original fashion content  
📅 **Automated Scheduling** - Posts at 12:00 PM & 6:00 PM Cameroon Time (WAT/GMT+1)  
📊 **Analytics Dashboard** - Real-time performance tracking and engagement metrics  
🔄 **Smart Feedback Loop** - AI learns from engagement to improve future content  
🔐 **Secure Credentials** - Encrypted storage for all platform tokens  
💰 **Token Optimized** - Prompt caching & batch processing to minimize API costs  
📱 **Multi-Account Support** - Manage multiple Instagram & TikTok accounts  
🎨 **Platform-Specific Content** - Tailored captions for Instagram, TikTok, Facebook, LinkedIn  

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React + TypeScript
- **Database:** PostgreSQL
- **Job Scheduler:** APScheduler (lightweight, no Redis needed)
- **AI:** Anthropic Claude API
- **Encryption:** python-cryptography
- **Deployment:** DigitalOcean / Heroku / Self-hosted

## Project Structure

```
ai-social-media-agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Configuration & env vars
│   │   ├── database.py             # PostgreSQL connection
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── agents/                 # AI agents
│   │   ├── services/               # Business logic
│   │   ├── api/                    # API routes
│   │   └── scheduler/              # Job scheduling
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Anthropic API Key

### Installation

1. Clone the repository
```bash
git clone https://github.com/westside200-oss/ai-social-media-agent.git
cd ai-social-media-agent
```

2. Set up backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Initialize database
```bash
python -m alembic upgrade head
```

5. Start backend
```bash
python app/main.py
```

6. Set up frontend
```bash
cd ../frontend
npm install
npm start
```

Visit `http://localhost:3000` for the dashboard.

## Configuration

### Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/ai_social_media

# Anthropic
ANTHROPIC_API_KEY=your_key_here

# Encryption
ENCRYPTION_KEY=your-32-character-hex-key

# Platforms
INSTAGRAM_API_VERSION=v18.0
TIKTOK_API_VERSION=v1

# Posting Schedule (Cameroon Time WAT/GMT+1)
FIRST_POST_TIME=12:00
SECOND_POST_TIME=18:00

# Server
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

## Usage

### Add Instagram Account

```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "instagram",
    "username": "your_username",
    "access_token": "your_token",
    "account_type": "business"
  }'
```

### Trigger Content Generation

```bash
curl -X POST http://localhost:8000/api/posts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 1,
    "template": "new_arrivals",
    "theme": "summer_collection"
  }'
```

## Performance Tracking

The dashboard displays:
- **Impressions** - Reach per post
- **Engagement Rate** - Likes + Comments / Impressions
- **Best Content** - Top performing posts & themes
- **Feedback Loop** - Engagement trends for AI optimization

## API Cost Optimization

- **Prompt Caching:** Reuses fashion/fabric templates (saves 90% on repeated prompts)
- **Batch Generation:** Creates multiple captions in single API call
- **Selective Analytics:** Fetches engagement data daily, not per-request

## Roadmap

- [x] MVP: Instagram & TikTok
- [ ] Facebook & LinkedIn integration
- [ ] Video script generation
- [ ] Advanced analytics dashboard
- [ ] Content calendar UI
- [ ] Multi-language support
- [ ] API rate limiting & quotas

## Contributing

Contributions welcome! Please open an issue or PR.

## License

MIT License - See LICENSE file

## Support

For issues or questions, open a GitHub issue or contact the maintainers.

---

**Built with ❤️ for fashion & fabric entrepreneurs**
