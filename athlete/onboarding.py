"""Athlete onboarding persistence logic."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from database.database import SessionLocal, get_db_session
from database.models import AthleteProfile, User


def save_athlete_profile(
    user_id: int,
    age: int,
    primary_sport: str,
    experience_level: str,
    primary_goal: str,
    weekly_frequency: int,
    available_duration_min: int,
    available_equipment: list[str],
    preferred_intensity: str,
    height_cm: float | None = None,
    weight_kg: float | None = None,
    gender: str | None = None,
    secondary_goals: list[str] | None = None,
    excluded_exercises: list[str] | None = None,
    physical_restrictions: str | None = None,
    full_name: str | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Create or update a user's AthleteProfile and mark onboarding complete."""
    if not (10 <= int(age) <= 110):
        raise ValueError("Age must be between 10 and 110.")
    if not (1 <= int(weekly_frequency) <= 7):
        raise ValueError("Weekly training frequency must be between 1 and 7 days.")
    if not (5 <= int(available_duration_min) <= 180):
        raise ValueError("Available workout duration must be between 5 and 180 minutes.")

    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        user = session.get(User, user_id)
        if user is None:
            raise ValueError(f"User {user_id} does not exist.")

        if full_name and full_name.strip():
            user.full_name = full_name.strip()

        profile = session.query(AthleteProfile).filter_by(user_id=user_id).first()
        if profile is None:
            profile = AthleteProfile(user_id=user_id, age=int(age))
            session.add(profile)

        profile.age = int(age)
        profile.height_cm = float(height_cm) if height_cm and height_cm > 0 else None
        profile.weight_kg = float(weight_kg) if weight_kg and weight_kg > 0 else None
        profile.gender = gender if gender and gender != "Prefer not to say" else None
        profile.primary_sport = primary_sport
        profile.experience_level = experience_level
        profile.primary_goal = primary_goal
        profile.secondary_goals = list(secondary_goals or [])
        profile.weekly_frequency = int(weekly_frequency)
        profile.available_duration_min = int(available_duration_min)
        profile.available_equipment = list(available_equipment)
        profile.preferred_intensity = preferred_intensity
        if excluded_exercises is not None:
            profile.excluded_exercises = list(dict.fromkeys(excluded_exercises))
        profile.physical_restrictions = physical_restrictions.strip() if physical_restrictions else None

        user.onboarding_completed = True
        session.flush()

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
