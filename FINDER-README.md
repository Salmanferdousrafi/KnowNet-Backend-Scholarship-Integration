# KnowNet X — Finder Demo

## What This Is
A fully interactive, self-contained HTML demo of the KnowNet X Scholarship & University Finder. 
It works entirely in the browser — no backend, no download, no installation.

## How to Use
1. Open `finder-demo.html` in any browser
2. Fill out your profile (field of study, country, education level, bio)
3. Click **"Save Profile & Find Matches"**
4. Browse AI-matched scholarships with breakdown scores:
   - **60%** Semantic similarity (Claude AI embedding match)
   - **25%** Rule-based (field + country + education level)
   - **15%** Deadline urgency (closer = higher score)
5. Switch to **Universities** tab to find matching universities
6. Try **Knowledge** tab for semantic AI search demo

## Deploy Anywhere
This is a single HTML file. You can:
- Upload to Vercel, Netlify, GitHub Pages, or any static host
- Open directly from your phone's file manager
- Email it to someone — it just works

## Connect to Real Backend
To connect this to your actual FastAPI backend:
1. Replace the demo `scholarships` and `universities` arrays with API calls
2. Use the `useAuthStore` and `useScholarships` hooks from the React frontend
3. Point `API_BASE` to your deployed backend URL

## Demo Data Included
- 6 real scholarships (Google, Rhodes, Fulbright, Microsoft, ETH, Commonwealth)
- 8 top universities (MIT, Stanford, Oxford, ETH Zurich, etc.)
- 3 knowledge entries (Transformer Architecture, Fulbright Guide, GRE Strategies)
