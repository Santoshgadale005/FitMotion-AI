# FitMotion AI

**AI-Powered Exercise Recommendation & Athlete Wellness Platform**

FitMotion AI is a standalone, modular Python sports-technology platform built with **Streamlit**, **SQLAlchemy (SQLite)**, **Pandas**, **NumPy**, **Scikit-learn**, and **Plotly**. It provides explainable, sport-aware exercise recommendations, customizable workout routines, balanced weekly training schedules, a grounded AI training assistant, and interactive activity analytics for athletes across 8 sports and general-fitness users.

> **Wellness & Safety Notice:** FitMotion AI provides general fitness, exercise organization, and athletic conditioning guidance. It is not a medical application and does not diagnose injuries or medical conditions.

---

## Key Features (All 16 Pages Active)

1. **Login & Registration** — Secure `bcrypt`-hashed accounts + optional 1-click **Portfolio Demo Athlete** account preloaded with ratings, schedules, and workout logs.
2. **Onboarding & Athlete Profile** — Collects age, optional height/weight/gender, sport, experience level, primary & secondary goals, weekly frequency, session duration, equipment inventory, movement restrictions, and excluded exercises.
3. **Main Dashboard** — Live athlete overview, AI ranker status, top 3 personalized picks, upcoming schedule, and sport conditioning demands.
4. **Structured Exercise Library (59 Verified Exercises)** — Covers all 8 categories (*Warm-up, Mobility, Stretching & Flexibility, Strength Training, Cardiovascular Training, Balance & Stability, Recovery & Cooldown, Sport-Specific Conditioning*) with step-by-step instructions, safety precautions, common mistakes, beginner modifications, and verified local SVG demonstration diagrams (`assets/images/`).
5. **Hybrid AI Exercise Recommendation Engine** — Transparent rule-based scoring combined with a **Scikit-learn** (`StandardScaler + Ridge` + cosine similarity) ranker that adapts to user ratings and workout history, explaining *why* every exercise was selected.
6. **Personalized Workout Generator & 4 Specialized Modules** — 9 preset routines (*5-min quick warm-up, 10-min mobility, 15-min flexibility, 20-min full-body, 30-min strength, pre-sports warm-up, post-workout cooldown, recovery-focused, sport-specific conditioning*) plus custom duration, difficulty, intensity, category, and equipment overrides, alongside dedicated **Warm-up**, **Mobility & Flexibility**, **Strength & Conditioning**, and **Recovery** assistants.
7. **Sport-Specific Training** — Dedicated physical-demand matrices and conditioning routines for *Badminton, Football, Basketball, Cricket, Tennis, Swimming, Running,* and *General Fitness*.
8. **AI Training Assistant** — Conversational coaching grounded directly in the exercise catalog and recommender, featuring a strict non-diagnostic medical safety guardrail, optional `.env` LLM polish, and a complete offline fallback.
9. **Weekly Training Planner & Workout History** — Auto-generates recovery-balanced 7-day schedules, enforces rest-day and consecutive high-intensity load warnings, and tracks completed workouts.
10. **Interactive Plotly Progress Dashboard** — Visualizes completed sessions, weekly consistency, total training duration, completion rates, most frequently performed exercises, and category balance.

---

## Project Architecture

```text
FitMotion AI/
├── app.py                     # Streamlit entrypoint & 16-page router
├── config.py                  # Centralized settings, env vars, domain constants & safety notice
├── requirements.txt           # Pinned/bounded Python dependencies
├── pytest.ini                 # Pytest configuration
├── .env.example               # Template for local DB URL & optional LLM keys
├── .streamlit/config.toml     # Sports-tech dark theme & port 8502 server config
├── authentication/            # bcrypt registration & login
├── athlete/                   # Onboarding, profile management, fitness goals & restrictions
├── exercises/                 # 8 category modules, SVG diagram generator, JSON/SQLite catalog
├── recommendation/            # Rule-based engine, Scikit-learn ML ranker, routine generator
├── assistant/                 # Grounded AI training assistant + medical guardrail + offline fallback
├── training/                  # Weekly planner, load balancer, workout logger, progress stats
├── database/                  # SQLAlchemy 2.0 engine, foreign-key pragma, 7 ORM models
├── dashboard/                 # 16-page sports-tech Streamlit UI & Plotly visualizations
├── data/                      # exercises.json, sports.json, local SQLite DB
├── assets/images/             # 59 verified local SVG movement diagrams
└── tests/                     # Database, exercise catalog, AI engine & 16-page UI smoke tests
```

---

## Quick Start (Local Setup)

### 1. Activate the virtual environment

```bash
source .venv/bin/activate
```

*(If setting up on a new machine: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`)*

### 2. Optional environment configuration

```bash
cp .env.example .env
```

### 3. Run the automated test suite

```bash
pytest
```

### 4. Launch the application

```bash
streamlit run app.py
```

Open **`http://localhost:8502`** in your browser (configured in `.streamlit/config.toml` to avoid conflicting with apps on port `8501`). You can override the port anytime with `streamlit run app.py --server.port 8510`.
