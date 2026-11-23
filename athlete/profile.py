"""Athlete profile retrieval, exclusion preferences, and exercise ratings."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from database.database import SessionLocal, get_db_session
from database.models import AthleteProfile, ExerciseFeedback, User


def get_athlete_profile(
    user_id: int,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any] | None:
    """Return a clean dictionary representation of the user's athlete profile."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        user = session.get(User, user_id)
        if user is None:
            return None
        profile = session.query(AthleteProfile).filter_by(user_id=user_id).first()
        if profile is None:
            return None
        return {
            "user_id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "age": profile.age,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "gender": profile.gender,
            "primary_sport": profile.primary_sport,
            "experience_level": profile.experience_level,
            "primary_goal": profile.primary_goal,
            "secondary_goals": list(profile.secondary_goals or []),
            "weekly_frequency": profile.weekly_frequency,
            "available_duration_min": profile.available_duration_min,
            "available_equipment": list(profile.available_equipment or []),
            "preferred_intensity": profile.preferred_intensity,
            "excluded_exercises": list(profile.excluded_exercises or []),
            "physical_restrictions": profile.physical_restrictions or "",
        }


def save_exercise_feedback(
    user_id: int,
    exercise_id: str,
    rating: int | None = None,
    is_excluded: bool | None = None,
    notes: str | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Create or update per-user rating and exclusion flags for an exercise."""
    if rating is not None and not (1 <= int(rating) <= 5):
        raise ValueError("Rating must be between 1 and 5.")

    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        entry = (
            session.query(ExerciseFeedback)
            .filter_by(user_id=user_id, exercise_id=exercise_id)
            .first()
        )
        if entry is None:
            entry = ExerciseFeedback(
                user_id=user_id,
                exercise_id=exercise_id,
                rating=rating,
                is_excluded=bool(is_excluded) if is_excluded is not None else False,
                notes=notes,
            )
            session.add(entry)
        else:
            if rating is not None:
                entry.rating = int(rating)
            if is_excluded is not None:
                entry.is_excluded = bool(is_excluded)
            if notes is not None:
                entry.notes = notes

        # Keep profile.excluded_exercises synchronized
        profile = session.query(AthleteProfile).filter_by(user_id=user_id).first()
        if profile is not None and is_excluded is not None:
            current = set(profile.excluded_exercises or [])
            if is_excluded:
                current.add(exercise_id)
            else:
                current.discard(exercise_id)
            profile.excluded_exercises = sorted(current)

        session.flush()
        return {
            "user_id": entry.user_id,
            "exercise_id": entry.exercise_id,
            "rating": entry.rating,
            "is_excluded": entry.is_excluded,
            "notes": entry.notes or "",
        }


def get_user_feedback_map(
    user_id: int,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, dict[str, Any]]:
    """Return mapping of exercise_id -> {rating, is_excluded, notes} for a user."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        entries = session.query(ExerciseFeedback).filter_by(user_id=user_id).all()
        return {
            e.exercise_id: {
                "rating": e.rating,
                "is_excluded": e.is_excluded,
                "notes": e.notes or "",
            }
            for e in entries
        }
