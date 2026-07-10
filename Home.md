# KnowNet X Wiki

Welcome to the KnowNet X documentation. This wiki covers everything you need to build, deploy, and use the platform.

---

## What is KnowNet X?

KnowNet X is an **AI-powered knowledge intelligence platform** combined with a **Scholarship & University Finder**. It helps students:

1. **Organize knowledge** with semantic AI search (like Notion + Perplexity)
2. **Find scholarships** matched to their profile using Claude AI embeddings
3. **Discover universities** that fit their academic background and budget

---

## Quick Links

| Page | Description |
|------|-------------|
| [API Reference](API-Reference) | Complete REST API documentation |
| [Deployment Guide](Deployment-Guide) | Deploy from your phone, no laptop needed |
| [Security Audit](Security-Audit) | Fixed vulnerabilities & remaining gaps |

---

## Live Demo

Try the interactive finder without downloading anything:

🔗 **[Open Live Demo](finder-demo.html)**

Or visit the deployed app:
- **Frontend:** [knownet-ai-x.vercel.app](https://knownet-ai-x.vercel.app)
- **Backend API:** `https://your-backend.vercel.app/api/v1`

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL + pgvector (Supabase) |
| AI | Claude API (Anthropic) |
| Auth | JWT + OAuth2PasswordBearer |
| Scheduler | APScheduler (30-min intervals) |
| Rate Limiting | slowapi |
| Frontend | React + Vite + Tailwind CSS |
| Hosting | Vercel |

---

## Project Structure

```
knownet-x/
├── backend/
│   ├── app/
│   │   ├── core/          # Config, security, dependencies
│   │   ├── db/            # Database session & init
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── routers/       # API endpoints
│   │   ├── scheduler/     # Background jobs
│   │   └── main.py        # FastAPI app entry
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks (auth, scholarships)
│   │   ├── types/         # TypeScript types
│   │   └── lib/           # Utilities
│   └── public/
│       └── finder.html    # Standalone demo
├── wiki/                  # This documentation
└── finder-demo.html       # Single-file deployable demo
```

---

## Getting Started in 5 Minutes

### 1. Try the Demo
Open `finder-demo.html` in any browser. Fill your profile and see AI-matched scholarships instantly.

### 2. Deploy the Backend
Follow the [Deployment Guide](Deployment-Guide) to deploy to Vercel + Supabase in 10 minutes from your phone.

### 3. Connect Frontend
Update `VITE_API_URL` in your frontend environment variables to point to your deployed backend.

---

## What's Implemented

- [x] Modular FastAPI backend (no monolithic files)
- [x] OAuth2PasswordBearer with real Bearer header
- [x] Resource ownership verification on all endpoints
- [x] Environment-only secrets with hard fail on missing
- [x] 30-min access tokens + 7-day revocable refresh tokens
- [x] Rate limiting: login 5/min, register 3/min per IP
- [x] Semantic knowledge search via embeddings
- [x] Scholarship model with structured metadata
- [x] APScheduler auto-collection every 30 min
- [x] AI matching: 60% semantic + 25% rules + 15% urgency
- [x] Admin-only manual trigger endpoint
- [x] Frontend ScholarshipFinderModule
- [x] Demo seed endpoint
- [x] 20 demo scholarships + 16 demo universities
- [x] Standalone HTML demo (no build step)

---

## What Needs Your Input

1. **Real RSS feeds** — Add actual scholarship source URLs to `SCHOLARSHIP_SOURCES`
2. **Embedding provider** — Switch from deterministic fallback to Voyage AI
3. **CORS domain** — Update `allow_origins` in `main.py` to your exact URL
4. **Email/Password reset** — Not implemented (optional)

---

## Support

- **Issues:** [github.com/Salmanferdousrafi/knownet-ai-X/issues](https://github.com/Salmanferdousrafi/knownet-ai-X/issues)
- **Email:** (add your contact)
- **Discord:** (add your server)

---

Built for mobile-first deployment. No local CLI required.
