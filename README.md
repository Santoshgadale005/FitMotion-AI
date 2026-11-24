# FitMotion AI

**AI-Powered Exercise Recommendation & Athlete Wellness Platform**

FitMotion AI is a standalone, modular Python sports-technology platform built with **Streamlit**, **SQLAlchemy (SQLite)**, **Pandas**, **NumPy**, **Scikit-learn**, and **Plotly**. Designed with a **WHOOP × Strava × Nike Training Club × GOWOD × Darebee** aesthetic, it delivers **90 animated biomechanical exercise demos**, an **explainable hybrid Rule + Scikit-learn ML recommendation engine**, **9 complete evidence-based 4-week sport plans** (NSCA, ACSM, FIFA 11+, BWF, USTA, USA Swimming), a **grounded AI training assistant**, a **load-balanced weekly training planner**, and **interactive Plotly progress analytics**.

> **Wellness & Safety Notice:** FitMotion AI provides general fitness, exercise organization, and athletic conditioning guidance. It is not a medical application and does not diagnose injuries or medical conditions.

---

## Core Capabilities (All 16 Pages Live)

- **90 Verified Animated Exercise Demos** across all 8 categories (*Warm-up, Mobility, Stretching & Flexibility, Strength Training, Cardiovascular Training, Balance & Stability, Recovery & Cooldown, Sport-Specific Conditioning*) and all 3 levels (**44 Beginner · 20 Intermediate · 26 Advanced**), each powered by a local looping animated SVG movement studio card (`assets/images/`).
- **8 Sports With Sport-First Filtering** (*Badminton, Football, Basketball, Cricket, Tennis, Swimming, Running, General Fitness*) backed by structured sports-science physical demand profiles (`data/sports.json`).
- **Hybrid Explainable AI Recommendation Engine** combining transparent sports-science rule scoring with a per-user **Scikit-learn** (`StandardScaler + Ridge` + cosine similarity) preference ranker that adapts to ratings and workout history—explaining *why* every exercise was selected.
- **Personalized Workout Generator & 9 Complete 4-Week Sport Plans** featuring Darebee-inspired 7-day visual program posters, guided session completion checklists, and 1-click assignment to the Weekly Training Planner.
- **Grounded AI Training Assistant** with natural-language intent extraction, strict non-diagnostic medical safety guardrails, optional `.env` LLM refinement, and a full offline fallback.
- **Weekly Training Planner, Workout History & Plotly Progress Dashboard** with rest-day protection, consecutive high-intensity load warnings, and interactive Strava/WHOOP-styled Plotly charts.

---

## Project Architecture

```text
FitMotion AI/
├── app.py                     # 16-page Streamlit entrypoint & 1-click sidebar router
├── config.py                  # Centralized settings, domain constants & safety notice
├── requirements.txt           # Python dependencies (Local & Streamlit Community Cloud)
├── pytest.ini                 # Pytest configuration
├── .env.example               # Template for local DB URL & optional LLM keys
├── .streamlit/config.toml     # WHOOP/Strava/Nike dark theme configuration
├── authentication/            # bcrypt registration & login
├── athlete/                   # Onboarding, profile, goals, exclusions & restriction safety filters
├── exercises/                 # 90 exercises across 8 categories + animated SVG generator
├── recommendation/            # Hybrid rule-based + Scikit-learn ML ranker & workout generator
├── training/                  # Weekly planner, 9 structured 4-week plans, tracker & analytics
├── assistant/                 # Grounded AI training coach + medical guardrail + offline fallback
├── database/                  # SQLAlchemy 2.0 ORM (7 normalized tables with FK & check constraints)
├── dashboard/                 # 16-page Streamlit UI modules & design system
├── data/                      # exercises.json, sports.json
├── assets/images/             # 90 verified looping animated biomechanical SVGs
└── tests/                     # Database, exercise catalog, AI engine & 16-page UI smoke tests
```

---

## Local Setup & Testing

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the complete automated test suite
pytest

# Launch FitMotion AI locally (use --server.port 8502 if port 8501 is in use)
streamlit run app.py --server.port 8502
```

---

## Deploy Free on Streamlit Community Cloud

1. Visit **https://share.streamlit.io** and sign in with GitHub.
2. Click **Create app → Deploy a public app from GitHub**.
3. Select:
   - **Repository:** `Santoshgadale005/FitMotion-AI`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy** — all 16 pages, 90 animated exercises, Scikit-learn ML ranker, 4-week plans, and Plotly analytics will launch live automatically!
