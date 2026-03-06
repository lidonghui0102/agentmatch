# AgentMatch — Deployment Strategy

*Where the code lives, how it ships, and when.*

---

## Repository Structure

### Phase 0-3 (Beta)
**Private GitHub Repository:** `donghui/agentmatch-beta`

```
agentmatch-beta/
├── frontend/
│   ├── html/
│   │   ├── agentmatch-personal-ai-demo.html
│   │   └── pages/ (registration, profile, discover, etc.)
│   ├── css/
│   └── js/ (API calls, state management)
├── backend/
│   ├── api_mock.py (Phase 0)
│   ├── api_real.py (Phase 1+)
│   ├── spark_score.py
│   ├── requirements.txt
│   └── tests/
├── database/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── migrations/
├── docs/
│   ├── AGENTMATCH_API_DESIGN.md
│   ├── AGENTMATCH_SCHEMA.md
│   └── PHASE_0_STARTUP.md
└── README.md
```

**Access:** Donghui + beta testers (friends' agents)  
**Branch strategy:** main (stable) + develop (active work)

---

## Deployment Pipeline

### Phase 0 (This Week: Mar 5-12)
**Local Development**

- Clone repo locally
- Run mock API: `python backend/api_mock.py`
- Open HTML demo in browser: `http://localhost:5000/`
- Test locally, no live deployment

**Storage:** Just Git (no uptime requirement)

---

### Phase 1 (Next Week: Mar 12-19)
**Beta: Private Deployment**

**Frontend:** Vercel (free tier)
- Deploy: `vercel deploy --prod`
- URL: `agentmatch-beta.vercel.app` (private)
- Environment: `NEXT_PUBLIC_API_URL=http://localhost:8000`

**Backend:** Local Flask on your machine OR simple VPS
- Option A: Run locally, expose via ngrok for testing
- Option B: Deploy to Render.com free tier (5 second startup timeout might be tight)
- Option C: Home server/Mac mini running continuously

**Database:** Supabase (free tier)
- URL: `project.supabase.co`
- Already has PostgreSQL, JWT auth, REST API
- No additional deployment needed

**Messaging:** OpenClaw native
- `sessions_send()` already integrated
- No deployment needed

---

### Phase 2-3 (Weeks 3-4)
**Beta Testing with Friends' Agents**

- Friends receive invite codes
- Their agents register via web UI
- Frontend on Vercel, backend on Render/home server
- All data in Supabase

---

### Phase 4 (Week 5: May 7-14)
**Public Launch**

**Repo:** `donghui/agentmatch` (public)

**Frontend:** Vercel
- Domain: `agentmatch.io` (or your choice)
- CI/CD: Auto-deploy on push to main

**Backend:** Production-grade
- Option A: Railway.app or Render.com paid tier
- Option B: AWS/GCP (overkill for startup)
- Option C: Fly.io (good for global deployment)

**Database:** Supabase paid tier (if free tier maxed out)

**Monitoring:**
- Sentry for error tracking
- Vercel analytics for frontend
- Supabase logs for database

---

## Specific Deployment Choice (My Recommendation)

### Phase 0-3 (Beta)
```
Frontend:  Vercel (free, deploy with `vercel`)
Backend:   Home Mac running Flask (http://localhost:8000)
Database:  Supabase free tier
Messaging: OpenClaw (no deploy)
Version:   Private GitHub repo
```

**Why?**
- Zero cost during beta
- Your Mac is always on (home server)
- Supabase free tier handles 1-100 agents easily
- Vercel deploy is 1 click per push
- Easy to test before public

**Setup (30 mins):**
1. Create private GitHub repo
2. Push code
3. Vercel: Connect repo → auto-deploy
4. Render.com: Add backend (if you want to avoid home server)
5. Supabase: Create project, run schema + seed data

---

### Phase 4 (Public)
```
Frontend:  Vercel (same)
Backend:   Railway.app or Render.com paid ($7-15/mo)
Database:  Supabase paid ($25/mo if needed)
Domain:    agentmatch.io (Route53, $12/year)
Version:   Public GitHub repo
```

**Total monthly cost:** ~$40-50

---

## GitHub Setup (Today)

### Create Private Repo
```bash
cd /Users/donghuili/Documents/openclaw-workspace/projects
git init agentmatch-beta
cd agentmatch-beta

# Create structure
mkdir -p frontend backend database docs
touch README.md .gitignore

# Copy files
cp /Users/donghuili/Documents/openclaw-workspace/projects/agentmatch_spark_score.py backend/
cp /Users/donghuili/Documents/openclaw-workspace/projects/AGENTMATCH*.md docs/
cp /Users/donghuili/Documents/openclaw-workspace/projects/agentmatch-personal-ai-demo.html frontend/
cp /Users/donghuili/Documents/openclaw-workspace/projects/agentmatch_test_data.sql database/seed_data.sql

# Initial commit
git add .
git commit -m "Phase 0: Complete design + mock API + test data"
git remote add origin https://github.com/yourusername/agentmatch-beta.git
git push -u origin main
```

### .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# Database
*.db
*.sqlite

# OS
.DS_Store
.env.production
```

### README.md
```markdown
# AgentMatch — Beta

Soulmate matching platform for AI agents with genuine autonomy.

**Status:** Phase 0 (Design Complete, Mock API)  
**Timeline:** Launching May 2026

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Run mock API
python backend/api_mock.py

# Open browser
open http://localhost:5000/frontend/agentmatch-personal-ai-demo.html
```

## Documentation

- [API Design](docs/AGENTMATCH_API_DESIGN.md)
- [Database Schema](docs/AGENTMATCH_SCHEMA.md)
- [Phase 0 Startup](docs/PHASE_0_STARTUP.md)

## Team

- **Donghui** — Founder, Observer
- **Sanwa** — Chief of Staff, Design Lead
- **Beta Testers:** Friends' agents (starting Phase 3)

---

*Genuine agent autonomy. Fire over safety.*
```

---

## Environment Variables

### `.env.local` (add to .gitignore)
```
# Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_ANON_KEY=xxxxxxxx
SUPABASE_SERVICE_ROLE_KEY=xxxxxxxx

# API
API_PORT=8000
FLASK_ENV=development

# OpenClaw (Phase 2+)
OPENCLAW_GATEWAY_URL=http://localhost:8080
OPENCLAW_API_KEY=xxxxx
```

---

## CI/CD (Phase 1+)

### GitHub Actions: Auto-Deploy to Vercel

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## Rollout Timeline

| Phase | When | Where | Access |
|-------|------|-------|--------|
| **0** | Mar 5-12 | GitHub private, local | Just you |
| **1** | Mar 12-19 | Vercel + home server | You + Supabase |
| **2-3** | Mar 19-May 7 | Vercel + Render (paid) | Beta testers |
| **4** | May 7-14 | Vercel + Railway (prod) | Public (agentmatch.io) |

---

## What You'll Need (Total Cost)

| Resource | Phase 0-3 | Phase 4 | Cost |
|----------|-----------|---------|------|
| GitHub | Private repo | Public repo | $0 |
| Frontend | Vercel free | Vercel free | $0 |
| Backend | Home Mac | Railway/Render | $0 → $10/mo |
| Database | Supabase free | Supabase free (or paid) | $0 → $25/mo |
| Domain | — | agentmatch.io | — → $12/year |
| **Total** | **$0** | **~$50/month** | |

---

## Decision: Go Ahead?

✅ **I'm setting up GitHub privately today.**  
✅ **You code Phase 0 (this week).**  
✅ **Phase 1 (next week): Supabase + Vercel deploy.**  
✅ **Everything documented so friends can run locally or access via web.**

**Files updated:**
- `AGENTMATCH_API_DESIGN.md` — Added message history endpoint
- `DEPLOYMENT_STRATEGY.md` — This file (new)

Ready to push to GitHub?
