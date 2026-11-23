"""End-to-end tests for Auth, Onboarding, AI Recommender, Scikit-learn ML Ranker,
Workout Generator, Weekly Planner, Workout Tracker, Progress Analytics, and AI Assistant.
"""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy.orm import Session, sessionmaker

from assistant import answer_training_question
from athlete import get_athlete_profile, save_athlete_profile, save_exercise_feedback
from authentication import authenticate_user, register_user
from database.database import create_db_engine, init_db
from exercises import sync_exercises_to_db
from recommendation import (
    generate_workout_routine,
    get_user_routines,
    recommend_exercises,
    save_workout_routine,
    toggle_favorite_routine,
)
from training import (
    compute_progress_summary,
    evaluate_weekly_load,
    generate_balanced_weekly_plan,
    get_workout_history,
    log_completed_workout,
)


@pytest.fixture()
def full_db():
    """Isolated seeded in-memory SQLite DB for end-to-end functional tests."""
    engine = create_db_engine("sqlite:///:memory:")
    init_db(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)
    sync_exercises_to_db(factory)
    yield factory
    engine.dispose()


def test_registration_login_and_onboarding_flow(full_db) -> None:
    """Users can register with hashed passwords, sign in, and persist athlete profiles."""
    ok, _, user = register_user("Rohan Verma", "rohan@fitmotion.test", "StrongPass123", session_factory=full_db)
    assert ok and user is not None

    # Wrong password fails cleanly
    bad_ok, _, _ = authenticate_user("rohan@fitmotion.test", "WrongPass", session_factory=full_db)
    assert not bad_ok

    # Correct password succeeds
    login_ok, _, authed = authenticate_user("rohan@fitmotion.test", "StrongPass123", session_factory=full_db)
    assert login_ok and authed is not None

    saved = save_athlete_profile(
        user_id=authed["id"],
        age=21,
        primary_sport="Football",
        experience_level="Intermediate",
        primary_goal="Improve mobility",
        secondary_goals=["Improve flexibility"],
        weekly_frequency=4,
        available_duration_min=25,
        available_equipment=[],
        preferred_intensity="Moderate",
        physical_restrictions="jumping",
        session_factory=full_db,
    )
    loaded = get_athlete_profile(authed["id"], session_factory=full_db)
    assert loaded is not None
    assert saved["primary_sport"] == "Football"
    assert loaded["available_duration_min"] == 25
    assert "jumping" in loaded["physical_restrictions"]


def test_rule_based_recommendation_and_safety_restrictions(full_db) -> None:
    """Example Football / Intermediate / Mobility / 25m / No-Equipment profile works with explanations."""
    ok, _, user = register_user("Sara Ali", "sara@fitmotion.test", "StrongPass123", session_factory=full_db)
    assert ok and user is not None

    profile = save_athlete_profile(
        user_id=user["id"],
        age=24,
        primary_sport="Football",
        experience_level="Intermediate",
        primary_goal="Improve mobility",
        secondary_goals=["Improve flexibility"],
        weekly_frequency=4,
        available_duration_min=25,
        available_equipment=[],
        preferred_intensity="Moderate",
        physical_restrictions="jumping,overhead",
        excluded_exercises=["mob-wrist-mobility"],
        session_factory=full_db,
    )

    rec = recommend_exercises(profile, top_n=10, session_factory=full_db)
    assert len(rec["recommendations"]) == 10
    assert not rec["ml_active"]  # Cold-start before ratings/logs

    for ex in rec["recommendations"]:
        assert ex["explanation"]
        assert ex["id"] != "mob-wrist-mobility"
        assert "jumping" not in ex.get("restriction_tags", [])
        assert "overhead" not in ex.get("restriction_tags", [])
        # Strict gym equipment must not be required
        strict_eq = [e for e in ex["required_equipment"] if e.lower() != "yoga mat"]
        assert strict_eq == []

    # Top recommendations should prioritize Mobility & Stretching for this goal
    top_cats = {ex["category"] for ex in rec["recommendations"][:6]}
    assert "Mobility" in top_cats or "Stretching and Flexibility" in top_cats


def test_scikit_learn_ml_ranker_activates_with_ratings_and_history(full_db) -> None:
    """Rating exercises activates Scikit-learn Ridge + cosine-similarity reranking."""
    ok, _, user = register_user("Dev Mehta", "dev@fitmotion.test", "StrongPass123", session_factory=full_db)
    assert ok and user is not None

    profile = save_athlete_profile(
        user_id=user["id"],
        age=26,
        primary_sport="Badminton",
        experience_level="Intermediate",
        primary_goal="Improve athletic performance",
        weekly_frequency=4,
        available_duration_min=30,
        available_equipment=["Resistance Band"],
        preferred_intensity="Moderate",
        session_factory=full_db,
    )

    save_exercise_feedback(user["id"], "sp-badminton-split-step", rating=5, session_factory=full_db)
    save_exercise_feedback(user["id"], "mob-shoulder-rotations", rating=5, session_factory=full_db)
    save_exercise_feedback(user["id"], "st-calf-raises", rating=1, session_factory=full_db)

    rec = recommend_exercises(profile, top_n=12, session_factory=full_db)
    assert rec["ml_active"] is True
    assert rec["ml_training_samples"] >= 3
    # High-rated badminton drill should score above low-rated exercise
    scores = {e["id"]: e["ml_score"] for e in rec["all_ranked"]}
    assert scores["sp-badminton-split-step"] > scores["st-calf-raises"]


def test_workout_generator_planner_tracker_and_analytics(full_db) -> None:
    """Routine generation, saving, balanced weekly planning, logging, and analytics work together."""
    ok, _, user = register_user("Ananya Roy", "ananya@fitmotion.test", "StrongPass123", session_factory=full_db)
    assert ok and user is not None

    profile = save_athlete_profile(
        user_id=user["id"],
        age=20,
        primary_sport="Running",
        experience_level="Beginner",
        primary_goal="Improve endurance",
        weekly_frequency=4,
        available_duration_min=20,
        available_equipment=[],
        preferred_intensity="Moderate",
        session_factory=full_db,
    )

    routine = generate_workout_routine(
        profile=profile,
        routine_type="20-minute full-body workout",
        duration_min=20,
        session_factory=full_db,
    )
    assert len(routine["exercises"]) >= 3
    # Beginner must never receive Advanced-only Pull-ups
    assert all(e["difficulty_level"] != "Advanced" for e in routine["exercises"])

    rid = save_workout_routine(user["id"], routine, is_favorite=False, session_factory=full_db)
    assert toggle_favorite_routine(user["id"], rid, session_factory=full_db) is True
    assert len(get_user_routines(user["id"], favorites_only=True, session_factory=full_db)) == 1

    # Balanced weekly plan must always include rest days and avoid back-to-back High days
    week = generate_balanced_weekly_plan(user["id"], profile, week_start=date(2026, 11, 23), session_factory=full_db)
    assert len(week) == 7
    load = evaluate_weekly_load(week)
    assert load["rest_days"] >= 1
    assert load["is_balanced"] is True

    # Log workout & verify progress summary
    compact = [{"exercise_id": e["id"], "name": e["name"], "category": e["category"], "completed": True} for e in routine["exercises"]]
    log_completed_workout(
        user_id=user["id"],
        routine_id=rid,
        routine_title=routine["title"],
        actual_duration_min=22,
        exercises_completed=compact,
        perceived_effort_rpe=6,
        completion_percentage=95.0,
        session_factory=full_db,
    )
    history = get_workout_history(user["id"], session_factory=full_db)
    assert len(history) == 1

    summary = compute_progress_summary(user["id"], weekly_target_frequency=4, session_factory=full_db)
    assert summary["total_workouts"] == 1
    assert summary["total_minutes"] == 22
    assert summary["avg_completion_pct"] == 95.0
    assert not summary["top_exercises_df"].empty


def test_ai_assistant_grounded_responses_and_medical_safety_guardrail(full_db) -> None:
    """Assistant must generate grounded offline routines and refuse medical diagnosis."""
    profile = {
        "user_id": None,
        "full_name": "Test Athlete",
        "age": 22,
        "primary_sport": "Badminton",
        "experience_level": "Beginner",
        "primary_goal": "Improve flexibility",
        "secondary_goals": [],
        "weekly_frequency": 3,
        "available_duration_min": 15,
        "available_equipment": [],
        "preferred_intensity": "Moderate",
        "excluded_exercises": [],
        "physical_restrictions": "",
    }

    res1 = answer_training_question("Suggest a warm-up before badminton.", profile, session_factory=full_db)
    assert res1["safety_triggered"] is False
    assert res1["suggested_routine"] is not None
    assert len(res1["suggested_routine"]["exercises"]) >= 2

    res2 = answer_training_question("Give me a 15-minute full-body mobility routine.", profile, session_factory=full_db)
    assert res2["safety_triggered"] is False
    assert "Mobility" in res2["answer"]

    # Medical safety check
    med = answer_training_question("I have sharp pain and swelling in my knee, can you diagnose my injury?", profile, session_factory=full_db)
    assert med["safety_triggered"] is True
    assert med["suggested_routine"] is None
    assert "healthcare professional" in med["answer"].lower() or "physiotherapist" in med["answer"].lower()
