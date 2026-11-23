"""Personalized workout routine generator and persistence service (Phase 5)."""

from __future__ import annotations

from math import ceil
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from database.database import SessionLocal, get_db_session
from database.models import WorkoutRoutine
from recommendation.recommendation_engine import recommend_exercises

ROUTINE_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "5-minute quick warm-up": {
        "default_duration": 5,
        "default_intensity": "Low",
        "phases": [("Warm-up", 0.70), ("Mobility", 0.30)],
        "description": "Fast, joint-friendly dynamic activation before training or desk breaks.",
    },
    "10-minute mobility routine": {
        "default_duration": 10,
        "default_intensity": "Low",
        "phases": [("Mobility", 0.70), ("Stretching and Flexibility", 0.30)],
        "description": "Focused joint range-of-motion sequence targeting hips, ankles, thoracic spine, and shoulders.",
    },
    "15-minute flexibility routine": {
        "default_duration": 15,
        "default_intensity": "Low",
        "phases": [("Mobility", 0.25), ("Stretching and Flexibility", 0.60), ("Recovery and Cooldown", 0.15)],
        "description": "Relaxed stretching session designed to release tight muscles and calm breathing.",
    },
    "20-minute full-body workout": {
        "default_duration": 20,
        "default_intensity": "Moderate",
        "phases": [
            ("Warm-up", 0.20),
            ("Strength Training", 0.40),
            ("Balance and Stability", 0.20),
            ("Recovery and Cooldown", 0.20),
        ],
        "description": "Balanced total-body conditioning combining warm-up, strength, stability, and cooldown.",
    },
    "30-minute strength routine": {
        "default_duration": 30,
        "default_intensity": "Moderate",
        "phases": [
            ("Warm-up", 0.15),
            ("Mobility", 0.15),
            ("Strength Training", 0.50),
            ("Balance and Stability", 0.10),
            ("Recovery and Cooldown", 0.10),
        ],
        "description": "Progressive strength session scaled to your experience and available equipment.",
    },
    "Pre-sports warm-up": {
        "default_duration": 12,
        "default_intensity": "Moderate",
        "phases": [("Warm-up", 0.45), ("Mobility", 0.30), ("Sport-Specific Conditioning", 0.25)],
        "description": "Sport-tailored dynamic prep to elevate heart rate and rehearse key athletic patterns.",
    },
    "Post-workout cooldown": {
        "default_duration": 10,
        "default_intensity": "Low",
        "phases": [("Recovery and Cooldown", 0.45), ("Stretching and Flexibility", 0.55)],
        "description": "Gradual heart-rate taper paired with restorative stretching and paced breathing.",
    },
    "Recovery-focused routine": {
        "default_duration": 20,
        "default_intensity": "Low",
        "phases": [("Recovery and Cooldown", 0.40), ("Mobility", 0.30), ("Stretching and Flexibility", 0.30)],
        "description": "Low-strain active recovery session ideal for rest days or heavy training weeks.",
    },
    "Sport-specific conditioning routine": {
        "default_duration": 30,
        "default_intensity": "High",
        "phases": [
            ("Warm-up", 0.15),
            ("Mobility", 0.15),
            ("Sport-Specific Conditioning", 0.35),
            ("Strength Training", 0.20),
            ("Recovery and Cooldown", 0.15),
        ],
        "description": "High-relevance athletic conditioning aligned with your sport's physical demands.",
    },
    "Custom personalized routine": {
        "default_duration": 25,
        "default_intensity": "Moderate",
        "phases": [],
        "description": "Fully tailored routine driven by your profile goals, selected categories, and time budget.",
    },
}


def _estimate_block_seconds(exercise: dict[str, Any], intensity: str) -> tuple[int, int, int]:
    """Return (sets, rest_seconds, total_block_seconds) calibrated to intensity."""
    sets = int(exercise.get("recommended_sets", 2))
    rest = int(exercise.get("rest_seconds", 30))
    work_sec = int(exercise.get("default_duration_sec", 60))

    if intensity == "Low":
        sets = max(1, sets - 1) if sets >= 3 else sets
        rest = max(15, int(rest * 0.85))
    elif intensity == "High":
        sets = min(4, sets + 1) if exercise["category"] in {"Strength Training", "Sport-Specific Conditioning", "Balance and Stability"} else sets
        rest = max(20, int(rest * 0.9))

    # Cap single long cardio blocks inside short multi-exercise routines
    if work_sec > 300:
        work_sec = 300

    total_sec = sets * work_sec + max(0, sets - 1) * rest + 20  # +20s transition buffer
    return sets, rest, total_sec


def generate_workout_routine(
    profile: dict[str, Any],
    routine_type: str = "Custom personalized routine",
    duration_min: int | None = None,
    difficulty: str | None = None,
    intensity: str | None = None,
    selected_categories: list[str] | None = None,
    available_equipment: list[str] | None = None,
    title: str | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Generate a structured, time-budgeted, explainable workout routine."""
    blueprint = ROUTINE_BLUEPRINTS.get(routine_type, ROUTINE_BLUEPRINTS["Custom personalized routine"])
    target_duration = int(duration_min or profile.get("available_duration_min") or blueprint["default_duration"])
    target_duration = max(5, min(90, target_duration))
    target_seconds = target_duration * 60

    eff_difficulty = difficulty or profile.get("experience_level", "Beginner")
    eff_intensity = intensity or (
        blueprint["default_intensity"] if routine_type != "Custom personalized routine" else profile.get("preferred_intensity", "Moderate")
    )
    eff_equipment = (
        list(available_equipment)
        if available_equipment is not None
        else list(profile.get("available_equipment", []))
    )

    rec_result = recommend_exercises(
        profile=profile,
        top_n=80,
        categories_filter=selected_categories if selected_categories else None,
        intensity_override=eff_intensity,
        equipment_override=eff_equipment,
        difficulty_override=eff_difficulty,
        session_factory=session_factory,
    )
    ranked_pool = rec_result["all_ranked"]

    chosen: list[dict[str, Any]] = []
    chosen_ids: set[str] = set()
    accumulated_sec = 0

    def _add_exercise(ex: dict[str, Any], phase_label: str) -> bool:
        nonlocal accumulated_sec
        if ex["id"] in chosen_ids:
            return False
        sets, rest, block_sec = _estimate_block_seconds(ex, eff_intensity)
        # Allow a single short cardio/warm-up exercise to scale down to fit remaining time
        remaining = target_seconds - accumulated_sec
        if block_sec > remaining + 90 and len(chosen) >= 2:
            if sets > 1:
                sets = 1
                block_sec = min(int(ex.get("default_duration_sec", 60)), max(45, remaining)) + 15
            else:
                return False

        entry = dict(ex)
        entry["phase"] = phase_label
        entry["prescribed_sets"] = sets
        entry["prescribed_reps"] = ex["recommended_reps"]
        entry["prescribed_rest_sec"] = rest
        entry["estimated_block_sec"] = block_sec
        chosen.append(entry)
        chosen_ids.add(ex["id"])
        accumulated_sec += block_sec
        return True

    # Structured phased assembly when blueprint defines phases and no narrow custom override conflicts
    phases = blueprint["phases"]
    if phases and not selected_categories:
        for phase_cat, ratio in phases:
            phase_budget = max(60, int(target_seconds * ratio))
            phase_sec = 0
            phase_candidates = [e for e in ranked_pool if e["category"] == phase_cat and e["id"] not in chosen_ids]
            for ex in phase_candidates:
                if phase_sec >= phase_budget and len(chosen) >= 2:
                    break
                before = accumulated_sec
                if _add_exercise(ex, phase_cat):
                    phase_sec += accumulated_sec - before
                if accumulated_sec >= target_seconds - 30:
                    break

    # Fill any remaining time budget using top-ranked goal/sport matches
    for ex in ranked_pool:
        if accumulated_sec >= target_seconds - 45 and len(chosen) >= 3:
            break
        if len(chosen) >= 12:
            break
        _add_exercise(ex, ex["category"])

    # Guarantee sensible ordering: Warm-up -> Mobility -> Main Work -> Stretching -> Recovery
    phase_order = {
        "Warm-up": 1,
        "Mobility": 2,
        "Sport-Specific Conditioning": 3,
        "Strength Training": 4,
        "Cardiovascular Training": 5,
        "Balance and Stability": 6,
        "Stretching and Flexibility": 7,
        "Recovery and Cooldown": 8,
    }
    chosen.sort(key=lambda item: phase_order.get(item["category"], 5))

    estimated_min = max(1, ceil(accumulated_sec / 60)) if chosen else 0
    sport = profile.get("primary_sport", "General Fitness")
    routine_title = title or f"{sport} — {routine_type} ({target_duration} min)"

    return {
        "title": routine_title,
        "routine_type": routine_type,
        "target_sport": sport,
        "difficulty_level": eff_difficulty,
        "intensity": eff_intensity,
        "target_duration_min": target_duration,
        "estimated_duration_min": estimated_min,
        "ml_active": rec_result["ml_active"],
        "exercises": chosen,
    }


def save_workout_routine(
    user_id: int,
    routine: dict[str, Any],
    is_favorite: bool = False,
    session_factory: sessionmaker[Session] | None = None,
) -> int:
    """Persist a generated or customized routine to SQLite and return its ID."""
    factory = session_factory or SessionLocal
    compact_payload = [
        {
            "exercise_id": ex["id"],
            "name": ex["name"],
            "category": ex["category"],
            "prescribed_sets": ex.get("prescribed_sets", ex.get("recommended_sets", 2)),
            "prescribed_reps": ex.get("prescribed_reps", ex.get("recommended_reps", "10")),
            "prescribed_rest_sec": ex.get("prescribed_rest_sec", ex.get("rest_seconds", 30)),
            "estimated_block_sec": ex.get("estimated_block_sec", ex.get("default_duration_sec", 60)),
            "explanation": ex.get("explanation", ""),
            "media_reference": ex.get("media_reference", ""),
        }
        for ex in routine.get("exercises", [])
    ]

    with get_db_session(factory) as session:
        record = WorkoutRoutine(
            user_id=user_id,
            title=routine["title"],
            routine_type=routine["routine_type"],
            target_sport=routine.get("target_sport"),
            difficulty_level=routine.get("difficulty_level", "Beginner"),
            intensity=routine.get("intensity", "Moderate"),
            estimated_duration_min=int(routine.get("estimated_duration_min") or routine.get("target_duration_min", 20)),
            is_favorite=is_favorite,
            exercises_payload=compact_payload,
        )
        session.add(record)
        session.flush()
        return record.id


def get_user_routines(
    user_id: int,
    favorites_only: bool = False,
    session_factory: sessionmaker[Session] | None = None,
) -> list[dict[str, Any]]:
    """List saved routines belonging to a user."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        query = session.query(WorkoutRoutine).filter_by(user_id=user_id)
        if favorites_only:
            query = query.filter_by(is_favorite=True)
        rows = query.order_by(WorkoutRoutine.is_favorite.desc(), WorkoutRoutine.created_at.desc()).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "routine_type": r.routine_type,
                "target_sport": r.target_sport,
                "difficulty_level": r.difficulty_level,
                "intensity": r.intensity,
                "estimated_duration_min": r.estimated_duration_min,
                "is_favorite": r.is_favorite,
                "exercises": list(r.exercises_payload or []),
                "created_at": r.created_at,
            }
            for r in rows
        ]


def toggle_favorite_routine(
    user_id: int,
    routine_id: int,
    session_factory: sessionmaker[Session] | None = None,
) -> bool:
    """Toggle a saved routine's favorite flag and return the new boolean value."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        row = session.query(WorkoutRoutine).filter_by(id=routine_id, user_id=user_id).first()
        if row is None:
            return False
        row.is_favorite = not row.is_favorite
        return row.is_favorite


def delete_workout_routine(
    user_id: int,
    routine_id: int,
    session_factory: sessionmaker[Session] | None = None,
) -> bool:
    """Delete a saved routine belonging to the user."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        row = session.query(WorkoutRoutine).filter_by(id=routine_id, user_id=user_id).first()
        if row is None:
            return False
        session.delete(row)
        return True
