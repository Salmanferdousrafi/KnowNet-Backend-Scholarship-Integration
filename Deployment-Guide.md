# Deployment Guide

Deploy KnowNet X from your phone — no laptop required.

---

## Prerequisites

You need:
1. A **GitHub account** (free)
2. A **Vercel account** (free, sign in with GitHub)
3. A **Supabase** or **Neon** account for PostgreSQL (free tier)
4. A **Claude API key** from [console.anthropic.com](https://console.anthropic.com)

---

## Step 1: Prepare Your Code

### Option A: GitHub Mobile App
1. Open GitHub app → Create new repository → Name it `knownet-x`
2. Upload all files from the `backend/` folder
3. Add `requirements.txt` and `.env.example`

### Option B: GitHub Web (on phone browser)
1. Go to github.com → New Repository
2. Drag-and-drop or use "Upload files" button
3. Upload the entire project folder

---

## Step 2: Set Up PostgreSQL Database

### Using Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com) on your phone
2. Create new project → Name it `knownet-x-db`
3. Wait for database to provision (~2 minutes)
4. Go to **Settings → Database**
5. Copy the **Connection String** (URI format):
   ```
   postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
   ```
6. Save this — you'll need it in Step 4

### Using Neon
1. Go to [neon.tech](https://neon.tech)
2. Create project → Copy connection string
3. Same process as Supabase

---

## Step 3: Deploy Backend to Vercel

1. Go to [vercel.com](https://vercel.com) on your phone browser
2. Sign in with GitHub
3. Click **Add New Project**
4. Import your `knownet-x` repository
5. Configure:
   - **Framework Preset:** Other
   - **Build Command:** `pip install -r requirements.txt`
   - **Output Directory:** (leave empty)
   - **Install Command:** (leave empty)
6. Click **Deploy** — it will fail initially (no env vars yet). That's OK.

---

## Step 4: Add Environment Variables

In Vercel dashboard:
1. Go to your project → **Settings → Environment Variables**
2. Add these variables:

| Variable | Value | Required |
|----------|-------|----------|
| `DATABASE_URL` | Your Supabase connection string | ✅ Yes |
| `JWT_SECRET` | Generate at [jwtsecret.com](https://jwtsecret.com) or type 50+ random characters | ✅ Yes |
| `CLAUDE_API_KEY` | `sk-ant-api03-...` from Anthropic console | ✅ Yes |
| `SCHOLARSHIP_SOURCES` | Comma-separated RSS feed URLs (optional) | ❌ No |
| `ENVIRONMENT` | `production` | ❌ No |
| `DEBUG` | `false` | ❌ No |

3. Click **Save**
4. Go to **Deployments** → Click the three dots on latest deploy → **Redeploy**

---

## Step 5: Initialize Database

The app auto-creates tables on first boot. But to be safe:

1. Go to Supabase dashboard → **SQL Editor**
2. Run this:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Your tables will be created automatically when the backend starts

---

## Step 6: Deploy Frontend

### Option A: Same Vercel Project (Monorepo)
1. In your GitHub repo, add a `vercel.json` at root:
   ```json
   {
     "version": 2,
     "builds": [
       { "src": "backend/app/main.py", "use": "@vercel/python" },
       { "src": "frontend/package.json", "use": "@vercel/static-build" }
     ],
     "routes": [
       { "src": "/api/v1/(.*)", "dest": "backend/app/main.py" },
       { "src": "/(.*)", "dest": "frontend/dist/$1" }
     ]
   }
   ```

### Option B: Separate Vercel Project (Easier)
1. Create a new Vercel project for just the frontend
2. Import the same repo but set **Root Directory** to `frontend/`
3. Framework preset: **Vite**
4. Add environment variable:
   - `VITE_API_URL` = `https://your-backend.vercel.app/api/v1`
5. Deploy

### Option C: Static HTML Demo (Fastest)
1. Upload `finder-demo.html` to any static host
2. Or rename it to `index.html` and deploy to Vercel/Netlify
3. Zero build step — works instantly

---

## Step 7: Verify Deployment

Test these endpoints in your phone browser:

```
https://your-backend.vercel.app/health
```
→ Should return: `{"status": "ok", "version": "2.0.0"}`

```
https://your-backend.vercel.app/api/v1/scholarships
```
→ Should return 401 (no auth token) — this means auth is working!

---

## Mobile-First Tips

### Managing Secrets
- Use a password manager app (Bitwarden, 1Password) to store `JWT_SECRET`
- Never commit `.env` files to GitHub
- Vercel's mobile dashboard works great for adding env vars

### Debugging from Phone
- Use **Safari DevTools** (iOS) or **Chrome Remote Debugging** (Android)
- Or add `console.log` and check Vercel's **Function Logs** in dashboard

### Updating Code
1. Edit files in GitHub mobile app
2. Vercel auto-deploys on every push
3. No CLI needed ever

---

## Troubleshooting

### "App refuses to boot" error
→ Check that `DATABASE_URL`, `JWT_SECRET`, and `CLAUDE_API_KEY` are all set

### "500 Internal Server Error"
→ Check Vercel Function Logs for the actual error
→ Common cause: Database connection string is wrong

### "CORS error" in browser
→ Update `allow_origins` in `app/main.py` to include your frontend URL

### "Rate limit exceeded"
→ Wait 1 minute, or check if you're hitting the endpoint too fast

### Scholarships not appearing
→ Hit `POST /api/v1/scholarships/demo-seed` once to populate data
→ Or wait 30 minutes for the scheduler to run

---

## Architecture Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Your Phone    │────▶│  Vercel Frontend │────▶│  Vercel Backend │
│  (Browser/App)  │     │  (React/Vite)    │     │  (FastAPI)      │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                    ┌─────────────────────┘
                                    │
                          ┌─────────▼──────────┐
                          │   Supabase/Neon    │
                          │   (PostgreSQL)     │
                          └────────────────────┘
                                    │
                          ┌─────────▼──────────┐
                          │   Claude API       │
                          │   (Anthropic)      │
                          └────────────────────┘
```

---

## Cost Estimate (Free Tier)

| Service | Free Tier | Limit |
|---------|-----------|-------|
| Vercel | ✅ Hobby | 100GB bandwidth, 10s serverless functions |
| Supabase | ✅ Free | 500MB database, 2GB bandwidth |
| Claude API | ✅ $5 credits | ~500 API calls |
| GitHub | ✅ Free | Unlimited public repos |

**Total monthly cost: $0** (for personal use)
