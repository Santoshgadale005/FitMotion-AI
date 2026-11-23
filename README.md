# FitMotion AI

**AI-Powered Exercise Recommendation & Athlete Wellness Platform**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-fit--motion--ai.vercel.app-FC4C02?style=for-the-badge&logo=vercel&logoColor=white)](https://fit-motion-ai.vercel.app)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FSantoshgadale005%2FFitMotion-AI)

### 🌐 Live Demo: [https://fit-motion-ai.vercel.app](https://fit-motion-ai.vercel.app)

> Explore the live interactive demo immediately (preloaded with a Demo Athlete profile, hybrid ML recommendations, 90 animated exercise motion demos, 9 complete 4-week sport plans, AI training coach, and Plotly progress charts).

FitMotion AI is a standalone, modular Python sports-technology platform featuring **90 animated biomechanical exercise demos**, a **hybrid rule-based + Ridge ML recommendation engine**, **9 evidence-based 4-week sport plans** (NSCA, ACSM, FIFA 11+, BWF, USTA, USA Swimming), a **grounded AI training assistant**, a **load-balanced weekly training planner**, and **interactive Plotly progress analytics**.

It ships with **two full frontends sharing the exact same Python AI/database core**:
1. **Vercel-Native Web App (`api/index.py` + `public/`)** — FastAPI serverless backend + WHOOP × Strava × Nike × GOWOD × Darebee web UI (deploys cleanly to Vercel with zero cold-sleep screens).
2. **Streamlit Studio App (`app.py`)** — Full 16-page local Python/Streamlit dashboard.

> **Wellness & Safety Notice:** FitMotion AI provides general fitness, exercise organization, and athletic conditioning guidance. It is not a medical application and does not diagnose injuries or medical conditions.

---

## Live Demo Deployment (Vercel — 30 Seconds)

1. Go to **https://vercel.com/new** and import **`Santoshgadale005/FitMotion-AI`**.
2. Leave the default settings as-is (`vercel.json` + lightweight `requirements.txt` are already preconfigured).
3. Click **Deploy** — your live portfolio demo is hosted at **[https://fit-motion-ai.vercel.app](https://fit-motion-ai.vercel.app)** with the Portfolio Demo Athlete preloaded!
4. *(Optional)* Add a free PostgreSQL `DATABASE_URL` (Neon or Supabase) in **Vercel → Project Settings → Environment Variables** for permanent cloud user persistence across cold starts.

---

## Core Capabilities

- **90 Verified Animated Exercises** across 8 categories (*Warm-up, Mobility, Stretching & Flexibility, Strength Training, Cardiovascular Training, Balance & Stability, Recovery & Cooldown, Sport-Specific Conditioning*) and all 3 levels (**44 Beginner · 20 Intermediate · 26 Advanced**), each with a local looping animated SVG movement demo (`assets/images/`).
- **8 Dedicated Sports** (*Badminton, Football, Basketball, Cricket, Tennis, Swimming, Running, General Fitness*) with sport-first filtering and conditioning demand profiles (`data/sports.json`).
- **Hybrid Explainable AI Engine** combining sports-science rules + Ridge regression & cosine-similarity personalization (`Scikit-learn` locally, exact closed-form `NumPy` Ridge on lightweight Vercel serverless) with clear explanations for every exercise.
- **9 Complete 4-Week Sport & Fitness Programs** displayed as Darebee-style 7-day visual posters with 1-click assignment to the Weekly Training Planner.
- **Grounded AI Training Assistant** with natural-language intent extraction, strict non-diagnostic medical safety guardrails, optional `.env` LLM polish, and full offline fallback.
- **Weekly Planner, Workout History & Plotly Analytics** tracking session consistency, training duration, completion rates, and top exercises with built-in rest-day and load-balance guardrails.

---

## Architecture

```text
FitMotion AI/
├── api/index.py               # Vercel FastAPI serverless API
├── public/                    # WHOOP × Strava × GOWOD × Darebee web frontend (HTML/CSS/JS + Plotly.js)
├── vercel.json                # Vercel rewrites & asset bundling config
├── app.py                     # 16-page Streamlit application entrypoint
├── config.py                  # Settings, serverless /tmp DB auto-detection, safety notice
├── requirements.txt           # Lightweight Vercel runtime dependencies
├── requirements-local.txt     # Full local dev dependencies (Streamlit, Scikit-learn, Pandas, Plotly, Pytest)
├── authentication/            # bcrypt registration & login
├── athlete/                   # Onboarding, profile, goals, exclusions & restriction safety filters
├── exercises/                 # 90 exercises across 8 categories + animated SVG generator
├── recommendation/            # Hybrid rule-based + Ridge ML ranker & workout generator
├── training/                  # Weekly planner, 9 structured 4-week plans, workout tracker & analytics
├── assistant/                 # Grounded AI training coach + medical guardrail + offline fallback
├── database/                  # SQLAlchemy 2.0 ORM (7 normalized tables with FK & check constraints)
├── dashboard/                 # Streamlit 16-page UI modules
├── data/                      # exercises.json, sports.json
├── assets/images/             # 90 verified looping animated biomechanical SVGs
└── tests/                     # Database, exercise catalog, AI engine, Streamlit & Vercel API tests
```

---

## Local Setup & Testing

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-local.txt

# Run the complete automated test suite
pytest

# Option A: Run the Vercel Web App locally (FastAPI + HTML/JS UI)
uvicorn api.index:app --reload --port 8000

# Option B: Run the 16-page Streamlit App locally (port 8502)
streamlit run app.py
```
