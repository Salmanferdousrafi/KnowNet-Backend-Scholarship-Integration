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
