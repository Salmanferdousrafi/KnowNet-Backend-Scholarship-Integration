# KnowNet X — AI Knowledge Intelligence + Scholarship Finder

## What's Implemented

### Backend (FastAPI)
- [x] Modular FastAPI structure (no monolithic files)
- [x] OAuth2PasswordBearer + JWT auth with real `Authorization: Bearer &lt;token&gt;` header
- [x] Access control on all projects/knowledge endpoints (owner-only or public)
- [x] IDOR vulnerability fixed — resources verified against `current_user.id`
- [x] Secrets from environment variables only — hard fail on missing `JWT_SECRET` or `DATABASE_URL`
- [x] Short-lived access tokens (30 min) + revocable refresh tokens stored hashed in DB
- [x] Rate limiting: `/auth/login` 5/min, `/auth/register` 3/min per IP
- [x] Semantic knowledge search via Claude embeddings + cosine similarity
- [x] Scholarship model with embeddings, metadata, and admin controls
- [x] APScheduler job runs every 30 min to collect from RSS feeds
- [x] AI-powered matching: 60% semantic + 25% rules + 15% urgency
- [x] Admin-only manual collection trigger

### Frontend
- [x] `ScholarshipFinderModule` plugs into existing dashboard
- [x] Reuses existing auth session (Zustand store)
- [x] "For You" tab with AI match scores + "Browse All" with filters
- [x] Demo seed button for testing

## Deployment (Mobile-friendly)

### Backend
1. Push to GitHub
2. Deploy to **Vercel** or **Railway** or **Render**
3. Set environment variables in dashboard:
   - `DATABASE_URL`
   - `JWT_SECRET` (32+ chars)
   - `CLAUDE_API_KEY`

### Frontend
1. Update `VITE_API_URL` in Vercel dashboard
2. Deploy to Vercel (no local build needed)

## Database Setup (Supabase/Postgres)
Run this SQL in your Supabase SQL editor:

```sql
-- Tables are auto-created by SQLAlchemy on first boot, but you can also run:
CREATE EXTENSION IF NOT EXISTS vector;

-- Add admin user manually if needed:
-- UPDATE users SET is_admin = true WHERE email = 'your@email.com';


# KnowNet X Backend + Scholarship Integration

&gt; A modular FastAPI backend with AI-powered semantic search, revocable JWT sessions, and an integrated Scholarship & Internship Finder that matches opportunities to user profiles using Claude embeddings.

---

##  Architecture

knownet-x-backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Env-only secrets, hard fail on missing
│   │   ├── security.py        # JWT, bcrypt, refresh token hashing
│   │   └── deps.py            # OAuth2Bearer, DB session, rate limiter
│   ├── db/
│   │   ├── session.py         # SQLAlchemy engine + pgvector
│   │   └── init.py        # init_db()
│   ├── models/
│   │   ├── user.py            # +field_of_study, country, education_level, bio_embedding
│   │   ├── project.py         # owner_id FK, is_public
│   │   ├── knowledge.py       # embedding[], owner_id FK
│   │   ├── scholarship.py     # embedding[], field_tags[], country_scope[]
│   │   └── refresh_token.py   # token_hash, is_revoked, expires_at
│   ├── schemas/
│   │   ├── user.py, auth.py, project.py, knowledge.py, scholarship.py
│   ├── services/
│   │   ├── user_service.py    # CRUD + bio embedding generation
│   │   ├── auth_service.py    # login, rotate refresh, revoke
│   │   ├── project_service.py # +verify_owner checks
│   │   ├── knowledge_service.py # semantic_search via cosine_similarity
│   │   ├── scholarship_service.py # match_scholarships_for_user (60/25/15 weights)
│   │   └── ai_service.py      # Claude chat, extract_structured, get_embedding
│   ├── routers/
│   │   ├── auth.py            # /login (5/min), /register (3/min), /refresh, /logout
│   │   ├── users.py           # GET/PATCH /me
│   │   ├── projects.py        # All endpoints verify owner_id
│   │   ├── knowledge.py       # +POST /search (semantic)
│   │   ├── scholarships.py    # GET /, GET /match, POST /demo-seed
│   │   └── admin.py           # POST /trigger-collection (admin-only)
│   ├── scheduler/
│   │   └── collector.py       # APScheduler 30-min RSS → Claude → upsert
│   └── main.py                # FastAPI app, CORS, scheduler startup
├── requirements.txt           # Pinned versions
└── .env.example


---

##  Security Fixes Applied

| Issue | Before | After |
|-------|--------|-------|
| Token handling | Plain function param / query string | `OAuth2PasswordBearer` + `Authorization: Bearer <token>` |
| Access control | None — any auth'd user could access any resource | Every endpoint verifies `resource.owner_id == current_user.id` |
| Secrets | Hardcoded fallback in code | Env-only; app **refuses to boot** if missing |
| Session tokens | Single long-lived token | 30-min access + 7-day refresh, server-side revocable |
| Rate limiting | None | `/login` 5/min, `/register` 3/min per IP |
| Search | SQL `ILIKE` scan | Claude embeddings + cosine similarity |

---

##  AI Features

- **Knowledge Semantic Search**: Embed query and stored knowledge via Claude API, rank by cosine similarity
- **Scholarship Matching**: `60%` semantic similarity + `25%` rule-based eligibility (field/country/education) + `15%` deadline urgency
- **Auto-Collection**: APScheduler runs every 30 min, fetches RSS feeds, sends raw text to Claude for structured JSON extraction
- **Profile Embeddings**: User bio auto-embedded on profile update for personalized matching

>  **Note**: Claude doesn't expose a native embedding API. The current implementation uses a deterministic fallback. For production, switch to **Voyage AI** (Anthropic's partner) by replacing `get_embedding()` in `ai_service.py`.

---

##  API Reference

| Method | Endpoint | Auth | Rate Limit | Description |
|--------|----------|------|------------|-------------|
| `POST` | `/api/v1/auth/register` | — | 3/min | Create account |
| `POST` | `/api/v1/auth/login` | — | 5/min | OAuth2 login → tokens |
| `POST` | `/api/v1/auth/refresh` | — | — | Rotate refresh token |
| `POST` | `/api/v1/auth/logout` | — | — | Revoke refresh token |
| `GET` | `/api/v1/users/me` | Bearer | — | Current user profile |
| `PATCH` | `/api/v1/users/me` | Bearer | — | Update profile |
| `GET` | `/api/v1/projects` | Bearer | — | List my projects |
| `POST` | `/api/v1/projects` | Bearer | — | Create project |
| `GET` | `/api/v1/knowledge` | Bearer | — | List my knowledge |
| `POST` | `/api/v1/knowledge/search` | Bearer | — | Semantic AI search |
| `GET` | `/api/v1/scholarships` | Bearer | — | List + filter scholarships |
| `GET` | `/api/v1/scholarships/match` | Bearer | — | AI-matched for you |
| `POST` | `/api/v1/scholarships/demo-seed` | Bearer | — | Load 6 demo scholarships |
| `POST` | `/api/v1/admin/scholarships/trigger-collection` | Bearer + Admin | — | Manual collection |

---

##  Deploy from Your Phone (No Laptop Needed)

### 1. Push to GitHub
Use GitHub mobile app or web to upload files. No CLI required.

### 2. Connect to Vercel / Railway / Render
- Import your GitHub repo
- Set **Build Command**: `pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 3. Add Environment Variables
In your hosting dashboard → Environment Variables:

```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
JWT_SECRET=your-32-char-minimum-random-secret-key-here
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
SCHOLARSHIP_SOURCES=https://example.com/rss-feed,https://example2.com/feed


Live Demo
App: knownet-ai-x.vercel.app
Source: github.com/Salmanferdousrafi/knownet-ai-X
The live demo includes 6 pre-seeded scholarships. Hit POST /api/v1/scholarships/demo-seed to populate them.
