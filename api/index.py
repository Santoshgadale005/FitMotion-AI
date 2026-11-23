"""Vercel-native FastAPI serverless backend for FitMotion AI.

Reuses 100% of the modular Python core (`exercises`, `authentication`, `athlete`,
`recommendation`, `training`, `assistant`, `database`) and powers the WHOOP ×
Strava × Nike × GOWOD × Darebee web application deployed on Vercel.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

import config
from assistant import answer_training_question
from athlete import (
    RESTRICTION_OPTIONS,
    get_athlete_profile,
    get_user_feedback_map,
    save_athlete_profile,
    save_exercise_feedback,
)
from authentication import authenticate_user, register_user
from database import init_db
from exercises import (
    ALL_EQUIPMENT_OPTIONS,
    get_all_exercises,
    get_exercise_by_id,
    load_sport_profiles,
    search_exercises,
    sync_exercises_to_db,
)
from recommendation import (
    ROUTINE_BLUEPRINTS,
    generate_workout_routine,
    get_user_routines,
    recommend_exercises,
    save_workout_routine,
    toggle_favorite_routine,
)
from training import (
    WORKOUT_PLANS,
    apply_workout_plan_to_week,
    evaluate_weekly_load,
    generate_balanced_weekly_plan,
    get_week_schedule,
    get_workout_history,
    log_completed_workout,
)
from training.progress_tracker import compute_progress_json

DEMO_EMAIL = "demo@fitmotion.ai"
DEMO_PASSWORD = "FitMotion2026!"

app = FastAPI(
    title="FitMotion AI API",
    version=config.APP_VERSION,
    description="AI-Powered Exercise Recommendation & Athlete Wellness Platform API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_BOOTSTRAPPED = False


def _ensure_bootstrapped() -> None:
    """Initialize SQLite schema and seed all 90 exercises once per container."""
    global _BOOTSTRAPPED
    if not _BOOTSTRAPPED:
        init_db()
        sync_exercises_to_db()
        _BOOTSTRAPPED = True


def _ensure_demo_athlete() -> dict[str, Any]:
    """Ensure the Portfolio Demo Athlete exists in the active DB and return user + profile."""
    _ensure_bootstrapped()
    ok, _, user = authenticate_user(DEMO_EMAIL, DEMO_PASSWORD)
    if not (ok and user):
        ok, _, user = register_user("Aarav Sharma (Demo)", DEMO_EMAIL, DEMO_PASSWORD)
        assert ok and user is not None
        uid = user["id"]
        profile = save_athlete_profile(
            user_id=uid,
            age=23,
            height_cm=177.0,
            weight_kg=71.0,
            gender="Male",
            primary_sport="Football",
            experience_level="Intermediate",
            primary_goal="Improve mobility",
            secondary_goals=["Improve flexibility", "Improve athletic performance"],
            weekly_frequency=4,
            available_duration_min=25,
            available_equipment=["Yoga Mat", "Resistance Band"],
            preferred_intensity="Moderate",
            physical_restrictions="",
        )
        for ex_id, rating in [
            ("mob-hip-drills", 5),
            ("str-hamstring", 5),
            ("wu-leg-swings", 5),
            ("sp-football-cod-shuttle", 4),
            ("bal-single-leg", 4),
            ("st-glute-bridges", 4),
        ]:
            save_exercise_feedback(uid, ex_id, rating=rating, is_excluded=False)

        r1 = generate_workout_routine(profile, routine_type="Pre-sports warm-up", duration_min=12)
        r1_id = save_workout_routine(uid, r1, is_favorite=True)
        r2 = generate_workout_routine(profile, routine_type="10-minute mobility routine", duration_min=15)
        r2_id = save_workout_routine(uid, r2, is_favorite=True)
        generate_balanced_weekly_plan(uid, profile)

        now = datetime.now(timezone.utc)
        sample_logs = [
            (r1_id, r1["title"], 14, r1["exercises"], 5, 100.0, now - timedelta(days=9), "Smooth pre-match activation."),
            (r2_id, r2["title"], 16, r2["exercises"], 4, 100.0, now - timedelta(days=7), "Hips felt noticeably looser after 90/90 drills."),
            (r1_id, "Football Conditioning & Agility (25 min)", 26, r1["exercises"], 7, 92.0, now - timedelta(days=5), "Strong deceleration mechanics on turns."),
            (r2_id, r2["title"], 15, r2["exercises"], 4, 100.0, now - timedelta(days=3), "Great active recovery session."),
            (r1_id, r1["title"], 12, r1["exercises"], 5, 100.0, now - timedelta(days=1), "Ready for weekend match."),
        ]
        for rid, title, mins, exs, rpe, pct, ts, note in sample_logs:
            compact = [
                {"exercise_id": e["id"], "name": e["name"], "category": e["category"], "completed": True}
                for e in exs
            ]
            log_completed_workout(
                user_id=uid,
                routine_id=rid,
                routine_title=title,
                actual_duration_min=mins,
                exercises_completed=compact,
                perceived_effort_rpe=rpe,
                completion_percentage=pct,
                notes=note,
                completed_at=ts,
            )

    profile = get_athlete_profile(user["id"])
    return {"user": user, "profile": profile}


def _default_guest_profile() -> dict[str, Any]:
    return {
        "user_id": None,
        "full_name": "Guest Athlete",
        "email": "",
        "age": 24,
        "height_cm": None,
        "weight_kg": None,
        "gender": None,
        "primary_sport": "Football",
        "experience_level": "Intermediate",
        "primary_goal": "Improve mobility",
        "secondary_goals": ["Improve flexibility"],
        "weekly_frequency": 4,
        "available_duration_min": 25,
        "available_equipment": [],
        "preferred_intensity": "Moderate",
        "excluded_exercises": [],
        "physical_restrictions": "",
    }


def _resolve_profile(user_id: int | None, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    base = get_athlete_profile(user_id) if user_id else None
    profile = dict(base) if base else _default_guest_profile()
    if overrides:
        for k, v in overrides.items():
            if v is not None:
                profile[k] = v
    return profile


# --- Pydantic Request Schemas ---


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None
    age: int = Field(ge=10, le=110, default=24)
    height_cm: float | None = None
    weight_kg: float | None = None
    gender: str | None = None
    primary_sport: str = "General Fitness"
    experience_level: str = "Beginner"
    primary_goal: str = "General fitness and wellness"
    secondary_goals: list[str] = Field(default_factory=list)
    weekly_frequency: int = Field(ge=1, le=7, default=3)
    available_duration_min: int = Field(ge=5, le=180, default=25)
    available_equipment: list[str] = Field(default_factory=list)
    preferred_intensity: str = "Moderate"
    physical_restrictions: str = ""


class FeedbackRequest(BaseModel):
    user_id: int
    exercise_id: str
    rating: int | None = None
    is_excluded: bool | None = None


class RecommendRequest(BaseModel):
    user_id: int | None = None
    top_n: int = 12
    primary_sport: str | None = None
    primary_goal: str | None = None
    experience_level: str | None = None
    preferred_intensity: str | None = None
    available_equipment: list[str] | None = None
    categories_filter: list[str] | None = None


class GenerateRoutineRequest(BaseModel):
    user_id: int | None = None
    routine_type: str = "20-minute full-body workout"
    duration_min: int = 20
    difficulty: str | None = None
    intensity: str | None = None
    primary_sport: str | None = None
    selected_categories: list[str] | None = None
    available_equipment: list[str] | None = None
    title: str | None = None


class SaveRoutineRequest(BaseModel):
    routine: dict[str, Any]
    is_favorite: bool = False


class ApplyPlanRequest(BaseModel):
    user_id: int
    plan_id: str


class AssistantRequest(BaseModel):
    question: str
    user_id: int | None = None
    primary_sport: str | None = None
    experience_level: str | None = None


class LogWorkoutRequest(BaseModel):
    routine_title: str
    actual_duration_min: int = 20
    exercises_completed: list[dict[str, Any]] = Field(default_factory=list)
    routine_id: int | None = None
    schedule_id: int | None = None
    perceived_effort_rpe: int | None = 6
    completion_percentage: float = 100.0
    notes: str = ""


# --- API Endpoints ---


@app.get("/api/health")
def api_health() -> dict[str, Any]:
    _ensure_bootstrapped()
    return {
        "status": "ok",
        "app": config.APP_NAME,
        "version": config.APP_VERSION,
        "serverless": config.IS_SERVERLESS,
        "exercise_count": len(get_all_exercises()),
    }


@app.get("/api/meta")
def api_meta() -> dict[str, Any]:
    _ensure_bootstrapped()
    all_ex = get_all_exercises()
    return {
        "app_name": config.APP_NAME,
        "version": config.APP_VERSION,
        "sports": config.SUPPORTED_SPORTS,
        "categories": config.EXERCISE_CATEGORIES,
        "goals": config.FITNESS_GOALS,
        "levels": config.EXPERIENCE_LEVELS,
        "intensities": config.INTENSITY_LEVELS,
        "equipment": ALL_EQUIPMENT_OPTIONS,
        "restrictions": RESTRICTION_OPTIONS,
        "sport_profiles": load_sport_profiles(),
        "routine_types": list(ROUTINE_BLUEPRINTS.keys()),
        "routine_blueprints": {
            k: {"default_duration": v["default_duration"], "default_intensity": v["default_intensity"], "description": v["description"]}
            for k, v in ROUTINE_BLUEPRINTS.items()
        },
        "safety_disclaimer": config.SAFETY_DISCLAIMER,
        "counts": {
            "total_exercises": len(all_ex),
            "Beginner": sum(1 for e in all_ex if e["difficulty_level"] == "Beginner"),
            "Intermediate": sum(1 for e in all_ex if e["difficulty_level"] == "Intermediate"),
            "Advanced": sum(1 for e in all_ex if e["difficulty_level"] == "Advanced"),
        },
    }


@app.post("/api/auth/demo")
def api_auth_demo() -> dict[str, Any]:
    return _ensure_demo_athlete()


@app.post("/api/auth/register")
def api_auth_register(req: RegisterRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    ok, msg, user = register_user(req.full_name, req.email, req.password)
    if not ok or user is None:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "user": user, "profile": None}


@app.post("/api/auth/login")
def api_auth_login(req: LoginRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    ok, msg, user = authenticate_user(req.email, req.password)
    if not ok or user is None:
        raise HTTPException(status_code=401, detail=msg)
    return {"message": msg, "user": user, "profile": get_athlete_profile(user["id"])}


@app.get("/api/profile/{user_id}")
def api_get_profile(user_id: int) -> dict[str, Any]:
    _ensure_bootstrapped()
    profile = get_athlete_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {"profile": profile, "feedback": get_user_feedback_map(user_id)}


@app.post("/api/profile/{user_id}")
def api_save_profile(user_id: int, req: ProfileUpdateRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    try:
        profile = save_athlete_profile(
            user_id=user_id,
            full_name=req.full_name,
            age=req.age,
            height_cm=req.height_cm,
            weight_kg=req.weight_kg,
            gender=req.gender,
            primary_sport=req.primary_sport,
            experience_level=req.experience_level,
            primary_goal=req.primary_goal,
            secondary_goals=req.secondary_goals,
            weekly_frequency=req.weekly_frequency,
            available_duration_min=req.available_duration_min,
            available_equipment=req.available_equipment,
            preferred_intensity=req.preferred_intensity,
            physical_restrictions=req.physical_restrictions,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"profile": profile}


@app.get("/api/exercises")
def api_exercises(
    query: str = "",
    category: str = "All",
    sport: str = "All",
    difficulty: str = "All",
    bodyweight_only: bool = False,
    user_id: int | None = Query(default=None),
) -> dict[str, Any]:
    _ensure_bootstrapped()
    items = search_exercises(
        query=query,
        category=category,
        sport=sport,
        difficulty=difficulty,
        bodyweight_only=bodyweight_only,
    )
    fb_map = get_user_feedback_map(user_id) if user_id else {}
    for item in items:
        fb = fb_map.get(item["id"], {})
        item["user_rating"] = fb.get("rating")
        item["is_excluded"] = bool(fb.get("is_excluded", False))
    return {"total": len(items), "exercises": items}


@app.post("/api/feedback")
def api_feedback(req: FeedbackRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    try:
        saved = save_exercise_feedback(
            user_id=req.user_id,
            exercise_id=req.exercise_id,
            rating=req.rating,
            is_excluded=req.is_excluded,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"feedback": saved}


@app.post("/api/recommendations")
def api_recommendations(req: RecommendRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    profile = _resolve_profile(
        req.user_id,
        {
            "primary_sport": req.primary_sport,
            "primary_goal": req.primary_goal,
            "experience_level": req.experience_level,
            "preferred_intensity": req.preferred_intensity,
            "available_equipment": req.available_equipment,
        },
    )
    res = recommend_exercises(
        profile=profile,
        top_n=req.top_n,
        categories_filter=req.categories_filter,
    )
    return {
        "recommendations": res["recommendations"],
        "ml_active": res["ml_active"],
        "ml_training_samples": res["ml_training_samples"],
        "filtered_out_count": res["filtered_out_count"],
        "sport_profile": res["sport_profile"],
    }


@app.post("/api/routines/generate")
def api_generate_routine(req: GenerateRoutineRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    profile = _resolve_profile(req.user_id, {"primary_sport": req.primary_sport})
    routine = generate_workout_routine(
        profile=profile,
        routine_type=req.routine_type,
        duration_min=req.duration_min,
        difficulty=req.difficulty,
        intensity=req.intensity,
        selected_categories=req.selected_categories,
        available_equipment=req.available_equipment,
        title=req.title,
    )
    return {"routine": routine}


@app.get("/api/routines/{user_id}")
def api_user_routines(user_id: int) -> dict[str, Any]:
    _ensure_bootstrapped()
    rows = get_user_routines(user_id)
    for r in rows:
        if isinstance(r.get("created_at"), datetime):
            r["created_at"] = r["created_at"].isoformat()
    return {"routines": rows}


@app.post("/api/routines/{user_id}/save")
def api_save_routine(user_id: int, req: SaveRoutineRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    rid = save_workout_routine(user_id, req.routine, is_favorite=req.is_favorite)
    return {"routine_id": rid}


@app.post("/api/routines/{user_id}/{routine_id}/favorite")
def api_toggle_favorite(user_id: int, routine_id: int) -> dict[str, Any]:
    _ensure_bootstrapped()
    is_fav = toggle_favorite_routine(user_id, routine_id)
    return {"is_favorite": is_fav}


@app.get("/api/plans")
def api_plans(sport: str = "All", difficulty: str = "All") -> dict[str, Any]:
    _ensure_bootstrapped()
    enriched_plans: list[dict[str, Any]] = []
    for plan in WORKOUT_PLANS:
        if sport != "All" and plan["sport"] != sport:
            continue
        if difficulty != "All" and plan["difficulty"] != difficulty:
            continue
        copy_plan = dict(plan)
        days_out = []
        for d in plan["weekly_schedule"]:
            d_copy = dict(d)
            d_copy["exercise_details"] = [
                ex for eid in d["exercise_ids"] if (ex := get_exercise_by_id(eid)) is not None
            ]
            days_out.append(d_copy)
        copy_plan["weekly_schedule"] = days_out
        enriched_plans.append(copy_plan)
    return {"plans": enriched_plans}


@app.post("/api/plans/apply")
def api_apply_plan(req: ApplyPlanRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    ok, msg = apply_workout_plan_to_week(req.user_id, req.plan_id)
    if not ok:
        raise HTTPException(status_code=404, detail=msg)
    return {"message": msg}


@app.post("/api/assistant/ask")
def api_assistant_ask(req: AssistantRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    profile = _resolve_profile(
        req.user_id,
        {"primary_sport": req.primary_sport, "experience_level": req.experience_level},
    )
    return answer_training_question(req.question, profile)


@app.get("/api/planner/{user_id}")
def api_get_planner(user_id: int) -> dict[str, Any]:
    _ensure_bootstrapped()
    week = get_week_schedule(user_id)
    load = evaluate_weekly_load(week)
    serialized = []
    for d in week:
        item = dict(d)
        item["date"] = d["date"].isoformat()
        serialized.append(item)
    return {"week": serialized, "load": load}


@app.post("/api/planner/{user_id}/auto")
def api_auto_planner(user_id: int) -> dict[str, Any]:
    _ensure_bootstrapped()
    profile = _resolve_profile(user_id)
    generate_balanced_weekly_plan(user_id, profile)
    return api_get_planner(user_id)


@app.get("/api/history/{user_id}")
def api_get_history(user_id: int) -> dict[str, Any]:
    _ensure_bootstrapped()
    logs = get_workout_history(user_id)
    for l in logs:
        if isinstance(l.get("completed_at"), datetime):
            l["completed_at"] = l["completed_at"].isoformat()
    return {"logs": logs}


@app.post("/api/history/{user_id}/log")
def api_log_workout(user_id: int, req: LogWorkoutRequest) -> dict[str, Any]:
    _ensure_bootstrapped()
    log_id = log_completed_workout(
        user_id=user_id,
        routine_title=req.routine_title,
        actual_duration_min=req.actual_duration_min,
        exercises_completed=req.exercises_completed,
        routine_id=req.routine_id,
        schedule_id=req.schedule_id,
        perceived_effort_rpe=req.perceived_effort_rpe,
        completion_percentage=req.completion_percentage,
        notes=req.notes,
    )
    return {"log_id": log_id}


@app.get("/api/analytics/{user_id}")
def api_analytics(user_id: int) -> dict[str, Any]:
    _ensure_bootstrapped()
    profile = _resolve_profile(user_id)
    return compute_progress_json(
        user_id=user_id,
        weekly_target_frequency=int(profile.get("weekly_frequency", 3)),
    )


@app.get("/assets/images/{filename}")
def serve_svg_asset(filename: str) -> Response:
    """Serve verified local animated exercise SVGs with long-lived caching."""
    safe_name = Path(filename).name
    if not safe_name.endswith(".svg"):
        raise HTTPException(status_code=404, detail="Asset not found.")
    target = config.ASSETS_DIR / "images" / safe_name
    if not target.exists():
        raise HTTPException(status_code=404, detail="SVG not found.")
    return Response(
        content=target.read_bytes(),
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@app.get("/")
def serve_index() -> FileResponse:
    """Serve the web application shell when running FastAPI locally."""
    index_path = config.BASE_DIR / "public" / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(index_path)


@app.get("/{asset_name:path}")
def serve_public_files(asset_name: str) -> FileResponse:
    """Serve static frontend assets (CSS/JS) when running locally with uvicorn."""
    safe = (config.BASE_DIR / "public" / asset_name).resolve()
    public_root = (config.BASE_DIR / "public").resolve()
    if public_root in safe.parents and safe.is_file():
        return FileResponse(safe)
    return FileResponse(public_root / "index.html")
