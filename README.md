# KnowNet X

> AI Knowledge Intelligence Platform + Scholarship & University Finder
> 
> Live: [knownet-ai-x.vercel.app](https://knownet-ai-x.vercel.app)

---

## What Is This?

KnowNet X is two things in one:

1. **Knowledge Intelligence** — Organize research, notes, and papers with AI-powered semantic search (like Notion + Perplexity)
2. **Opportunity Finder** — AI-matched scholarships and universities based on your academic profile

Built for students who want to discover funding and organize knowledge without switching between 10 different apps.

---

## What Changed (v2.0)

| Before (Old Backend) | After (This) |
|---------------------|--------------|
| Single 426-line file | 15+ modular files |
| Token in query string | `Authorization: Bearer` header |
| Any user could access any data | Owner-only access on every endpoint |
| Hardcoded secrets | App refuses to boot if env vars missing |
| Single long-lived token | 30-min access + 7-day revocable refresh |
| No rate limits | 5/min login, 3/min register |
| SQL `ILIKE` search | Claude embeddings + cosine similarity |
| No scholarship system | Full AI matching engine + auto-collection |

---

## Live Demo

**[Open Finder Demo](https://knownet-ai-x.vercel.app)** — No download, no signup, works on mobile.

Fill your profile → See AI-matched scholarships with score breakdown → Browse universities → Search knowledge with semantic AI.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL + pgvector (Supabase) |
| AI | Claude API (Anthropic) |
| Auth | JWT + OAuth2PasswordBearer |
| Scheduler | APScheduler (30-min intervals) |
| Rate Limit | slowapi |
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
│   │   ├── models/        # SQLAlchemy models (User, Project, Knowledge, Scholarship, RefreshToken)
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── services/      # Business logic + AI integration
│   │   ├── routers/       # API endpoints
│   │   ├── scheduler/     # Background RSS collection job
│   │   └── main.py        # FastAPI app entry
│   ├── requirements.txt   # Pinned dependencies
│   ├── .env.example       # Required environment variables
│   └── vercel.json        # Vercel deployment config
├── frontend/
│   ├── src/
│   │   ├── components/    # Layout, shared UI
│   │   ├── pages/         # Dashboard, Scholarships, Knowledge, Profile
│   │   ├── hooks/         # useAuth (Zustand), useScholarships (TanStack Query)
│   │   ├── lib/           # API client, utilities
│   │   └── types/         # TypeScript interfaces
│   ├── public/
│   │   └── finder.html    # Standalone deployable demo
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── finder-demo.html       # Single-file demo (no build needed)
├── vercel.json            # Root monorepo config
└── wiki/                  # Documentation
    ├── Home.md
    ├── API-Reference.md
    ├── Deployment-Guide.md
    └── Security-Audit.md
```

---

## Quick Start

### 1. Try the Demo (No Setup)

Open `finder-demo.html` in any browser or deploy it to Vercel/Netlify in 10 seconds.

### 2. Deploy the Full Stack

**Prerequisites:** GitHub account, Vercel account, Supabase account, Claude API key

**Backend:**
```bash
# 1. Push backend/ folder to GitHub
# 2. Create Vercel project → Import repo → Set root: backend/
# 3. Add environment variables (see below)
# 4. Deploy
```

**Frontend:**
```bash
# 1. Create second Vercel project → Import same repo → Set root: frontend/
# 2. Framework: Vite
# 3. Add VITE_API_URL=https://your-backend.vercel.app/api/v1
# 4. Deploy
```

**Detailed phone-only deployment:** See [wiki/Deployment-Guide.md](wiki/Deployment-Guide.md)

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string (Supabase/Neon) | ✅ Yes |
| `JWT_SECRET` | 50+ random characters for token signing | ✅ Yes |
| `CLAUDE_API_KEY` | From [console.anthropic.com](https://console.anthropic.com) | ✅ Yes |
| `SCHOLARSHIP_SOURCES` | Comma-separated RSS feed URLs | ❌ Optional |
| `ENVIRONMENT` | `production` or `development` | ❌ Optional |
| `DEBUG` | `true` or `false` | ❌ Optional |

**Frontend only:**
| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Your deployed backend URL |

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | — | Create account (3/min) |
| `POST` | `/auth/login` | — | Login, get tokens (5/min) |
| `POST` | `/auth/refresh` | — | Rotate refresh token |
| `POST` | `/auth/logout` | — | Revoke refresh token |
| `GET` | `/users/me` | Bearer | Get profile |
| `PATCH` | `/users/me` | Bearer | Update profile |
| `GET` | `/projects` | Bearer | List projects |
| `POST` | `/projects` | Bearer | Create project |
| `GET` | `/knowledge` | Bearer | List knowledge |
| `POST` | `/knowledge/search` | Bearer | **Semantic AI search** |
| `GET` | `/scholarships` | Bearer | List + filter |
| `GET` | `/scholarships/match` | Bearer | **AI-matched for you** |
| `POST` | `/scholarships/demo-seed` | Bearer | Load demo data |
| `POST` | `/admin/scholarships/trigger-collection` | Bearer + Admin | Manual collection |

**Full docs:** [wiki/API-Reference.md](wiki/API-Reference.md)

---

## AI Matching Algorithm

Scholarships are ranked for each user using:

- **60%** Semantic similarity — Claude embeds your bio and the scholarship text, ranks by cosine similarity
- **25%** Rule-based — Field of study + country + education level match
- **15%** Deadline urgency — Closer deadlines score higher

Every score is returned transparently so you see *why* each scholarship matched.

---

## Security

**Fixed:**
- ✅ OAuth2PasswordBearer with real Bearer header
- ✅ IDOR vulnerability fixed (owner verification on every endpoint)
- ✅ Environment-only secrets (app hard-fails if missing)
- ✅ Short-lived access tokens + revocable refresh tokens
- ✅ Rate limiting on auth endpoints
- ✅ Semantic search (no SQL injection)

**Remaining gaps:** See [wiki/Security-Audit.md](wiki/Security-Audit.md)

---

## Demo Data

- **20 scholarships** — Google, Rhodes, Fulbright, Microsoft, ETH, Commonwealth, Chevening, DAAD, Gates Cambridge, Erasmus, Turing AI, UNSW, Knight-Hennessy, ADB-Japan, Swiss Government, Meta Fellowship, MEXT Japan, McCall MacBain, Australia Awards, EPFL
- **16 universities** — MIT, Stanford, Oxford, ETH Zurich, Toronto, Imperial, CMU, NUS, Tokyo, EPFL, UBC, Tsinghua, Edinburgh, KAIST, Melbourne, TU Munich

---

## What's Implemented

- [x] Modular FastAPI backend
- [x] OAuth2PasswordBearer auth
- [x] Resource ownership verification
- [x] Environment-only secrets with hard fail
- [x] 30-min access + 7-day refresh tokens
- [x] Rate limiting (login 5/min, register 3/min)
- [x] Semantic knowledge search via embeddings
- [x] Scholarship model with structured metadata
- [x] APScheduler auto-collection every 30 min
- [x] AI matching (60/25/15 weights)
- [x] Admin-only manual trigger
- [x] React frontend with Zustand + TanStack Query
- [x] Standalone HTML demo (no build)
- [x] 20 demo scholarships + 16 demo universities
- [x] Wiki documentation (4 pages)

## What Needs Your Input

- [ ] Real RSS feed URLs in `SCHOLARSHIP_SOURCES`
- [ ] Switch embedding from deterministic fallback to Voyage AI
- [ ] Update CORS `allow_origins` to your exact domain
- [ ] Email verification (optional)
- [ ] Password reset (optional)

---

## License

MIT — Free to use, modify, and deploy.

---

Built for mobile-first deployment. No local CLI required.
