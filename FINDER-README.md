# KnowNet X Finder Demo

A fully interactive, self-contained HTML demo of the KnowNet X Scholarship & University Finder.

## What It Does

- **Profile Form** — Fill your field, country, education level, bio
- **AI Matching** — See scholarships ranked by 60% semantic + 25% rules + 15% urgency
- **University Finder** — Filter by country, ranking, tuition budget
- **Knowledge Search** — Semantic AI search demo

## How to Use

1. Open `finder-demo.html` in any browser (Chrome, Safari, Firefox)
2. Fill your profile
3. Click **"Save Profile & Find Matches"**
4. Browse AI-matched scholarships with score breakdowns

## Deploy Anywhere

This is a single HTML file. No build step. No server needed.

**Vercel:**
1. Go to [vercel.com](https://vercel.com)
2. Upload `finder-demo.html` as `index.html`
3. Done — live URL in 10 seconds

**GitHub Pages:**
1. Create repo → Upload `finder-demo.html` as `index.html`
2. Settings → Pages → Select main branch
3. Live in 1 minute

**Netlify:**
1. Drag and drop `finder-demo.html` onto [netlify.com](https://netlify.com)
2. Instant deploy

## Demo Data

- **20 scholarships** — Google, Rhodes, Fulbright, Microsoft, ETH, Commonwealth, Chevening, DAAD, Gates Cambridge, Erasmus, Turing AI, UNSW, Knight-Hennessy, ADB-Japan, Swiss Government, Meta Fellowship, MEXT Japan, McCall MacBain, Australia Awards, EPFL
- **16 universities** — MIT, Stanford, Oxford, ETH Zurich, Toronto, Imperial, CMU, NUS, Tokyo, EPFL, UBC, Tsinghua, Edinburgh, KAIST, Melbourne, TU Munich

## Connect to Real Backend

To use live data instead of demo data, replace the hardcoded arrays with API calls:

```javascript
// Replace this:
const scholarships = [...]; // hardcoded

// With this:
const res = await fetch('https://your-backend.vercel.app/api/v1/scholarships/match', {
  headers: { 'Authorization': 'Bearer ' + token }
});
const scholarships = await res.json();
```

See the full backend in the `backend/` folder.
