"""Centralized 1-click navigation registry with athletic icons for all 16 pages."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PageDefinition:
    """Metadata for a single FitMotion AI page."""

    key: str
    title: str
    icon: str
    section: str
    phase: int
    status: str  # "Active"
    summary: str


PAGES: list[PageDefinition] = [
    # Command Center
    PageDefinition(
        key="main_dashboard",
        title="Main Dashboard",
        icon="⚡",
        section="Command Center",
        phase=1,
        status="Active",
        summary="WHOOP-style readiness overview, quick-start workout actions, top AI picks, and upcoming schedule.",
    ),
    # Training & Exercises
    PageDefinition(
        key="exercise_library",
        title="Exercise Library",
        icon="🏃",
        section="Exercises & AI",
        phase=2,
        status="Active",
        summary="GOWOD-inspired visual exercise library across 90 animated movements, 8 categories, and 8 sports.",
    ),
    PageDefinition(
        key="ai_recommendations",
        title="AI Exercise Recommendations",
        icon="🎯",
        section="Exercises & AI",
        phase=4,
        status="Active",
        summary="Explainable rule-based + Scikit-learn ranked exercise recommendations tailored to your athlete profile.",
    ),
    PageDefinition(
        key="workout_generator",
        title="Workout Generator",
        icon="🔥",
        section="Exercises & AI",
        phase=5,
        status="Active",
        summary="Custom workout builder, Darebee-inspired 4-week sport plans, and guided session runner.",
    ),
    PageDefinition(
        key="sport_specific",
        title="Sport-Specific Training",
        icon="🏆",
        section="Exercises & AI",
        phase=4,
        status="Active",
        summary="Dedicated conditioning matrices and 4-week programs for 8 sports.",
    ),
    # Specialized Modules
    PageDefinition(
        key="warmup_assistant",
        title="Warm-up Assistant",
        icon="☀️",
        section="Training Modules",
        phase=5,
        status="Active",
        summary="Quick 5-minute and pre-sport dynamic warm-up generator.",
    ),
    PageDefinition(
        key="mobility_flexibility",
        title="Mobility & Flexibility",
        icon="🧘",
        section="Training Modules",
        phase=5,
        status="Active",
        summary="GOWOD-inspired joint mobility drills and targeted stretching sequences.",
    ),
    PageDefinition(
        key="strength_conditioning",
        title="Strength & Conditioning",
        icon="💪",
        section="Training Modules",
        phase=5,
        status="Active",
        summary="Equipment-aware strength, balance, and cardiovascular routines scaled to experience.",
    ),
    PageDefinition(
        key="recovery_assistant",
        title="Recovery Assistant",
        icon="🔋",
        section="Training Modules",
        phase=5,
        status="Active",
        summary="Post-workout cooldown, breathing exercises, and active recovery sessions.",
    ),
    # Coaching, Planning & Analytics
    PageDefinition(
        key="ai_training_assistant",
        title="AI Training Assistant",
        icon="🤖",
        section="Coaching & Analytics",
        phase=7,
        status="Active",
        summary="Conversational fitness Q&A backed by the structured exercise database and offline fallback.",
    ),
    PageDefinition(
        key="weekly_planner",
        title="Weekly Training Planner",
        icon="📅",
        section="Coaching & Analytics",
        phase=6,
        status="Active",
        summary="7-day visual calendar strip with rest-day management and load-balance guardrails.",
    ),
    PageDefinition(
        key="workout_history",
        title="Workout History",
        icon="📋",
        section="Coaching & Analytics",
        phase=6,
        status="Active",
        summary="Chronological log of completed sessions, duration, RPE, and completion rate.",
    ),
    PageDefinition(
        key="progress_dashboard",
        title="Progress Dashboard",
        icon="📊",
        section="Coaching & Analytics",
        phase=8,
        status="Active",
        summary="Strava/WHOOP-styled Plotly charts tracking workout consistency, duration, and frequency.",
    ),
    # Account & Profile
    PageDefinition(
        key="login_registration",
        title="Login & Registration",
        icon="🔐",
        section="Account & Profile",
        phase=3,
        status="Active",
        summary="Secure registration, login (bcrypt), and 1-click Portfolio Demo Athlete access.",
    ),
    PageDefinition(
        key="onboarding",
        title="Onboarding",
        icon="🧭",
        section="Account & Profile",
        phase=3,
        status="Active",
        summary="Guided onboarding collecting sport, experience, goals, equipment, and restrictions.",
    ),
    PageDefinition(
        key="athlete_profile",
        title="Athlete Profile",
        icon="👤",
        section="Account & Profile",
        phase=3,
        status="Active",
        summary="Editable athlete profile, equipment inventory, movement restrictions, and excluded exercises.",
    ),
]

PAGE_BY_KEY: dict[str, PageDefinition] = {page.key: page for page in PAGES}
SECTIONS: list[str] = list(dict.fromkeys(page.section for page in PAGES))
