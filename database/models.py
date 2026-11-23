"""Relational ORM models for FitMotion AI.

Designed in Phase 1 to support all planned modules without breaking schema
changes in later phases:
- Users & Athlete Profiles (Phase 3)
- Structured Exercise Library (Phase 2)
- Personalized Routines & ML Feedback Ranking (Phases 4 & 5)
- Weekly Planner & Workout Tracking Analytics (Phases 6 & 8)
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


def _utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class User(Base):
    """Registered user account."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utc_now,
        onupdate=_utc_now,
        nullable=False,
    )

    profile: Mapped[AthleteProfile | None] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    routines: Mapped[list[WorkoutRoutine]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    scheduled_workouts: Mapped[list[ScheduledWorkout]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    workout_logs: Mapped[list[WorkoutLog]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    exercise_feedback: Mapped[list[ExerciseFeedback]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class AthleteProfile(Base):
    """Athlete and general-fitness onboarding profile."""

    __tablename__ = "athlete_profiles"
    __table_args__ = (
        CheckConstraint("age >= 10 AND age <= 110", name="ck_profile_age_range"),
        CheckConstraint("weekly_frequency >= 1 AND weekly_frequency <= 7", name="ck_profile_weekly_freq"),
        CheckConstraint("available_duration_min >= 5 AND available_duration_min <= 180", name="ck_profile_duration"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(40), nullable=True)

    primary_sport: Mapped[str] = mapped_column(String(80), nullable=False, default="General Fitness")
    experience_level: Mapped[str] = mapped_column(String(30), nullable=False, default="Beginner")
    primary_goal: Mapped[str] = mapped_column(String(100), nullable=False, default="General fitness and wellness")
    secondary_goals: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    weekly_frequency: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    available_duration_min: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    available_equipment: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    preferred_intensity: Mapped[str] = mapped_column(String(20), nullable=False, default="Moderate")

    excluded_exercises: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    physical_restrictions: Mapped[str | None] = mapped_column(Text, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utc_now,
        onupdate=_utc_now,
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="profile")


class Exercise(Base):
    """Structured exercise entry populated in Phase 2."""

    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    instructions: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    target_muscles: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    difficulty_level: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    default_duration_sec: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    recommended_sets: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    recommended_reps: Mapped[str] = mapped_column(String(40), nullable=False, default="10-12")
    rest_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=45)

    required_equipment: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    safety_instructions: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    common_mistakes: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    beginner_modification: Mapped[str | None] = mapped_column(Text, nullable=True)

    media_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    media_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)

    suitable_levels: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    relevant_sports: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    feedback_entries: Mapped[list[ExerciseFeedback]] = relationship(
        back_populates="exercise",
        cascade="all, delete-orphan",
    )


class WorkoutRoutine(Base):
    """Saved or generated personalized workout routine."""

    __tablename__ = "workout_routines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(140), nullable=False)
    routine_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    target_sport: Mapped[str | None] = mapped_column(String(80), nullable=True)
    difficulty_level: Mapped[str] = mapped_column(String(30), nullable=False, default="Beginner")
    intensity: Mapped[str] = mapped_column(String(20), nullable=False, default="Moderate")
    estimated_duration_min: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    exercises_payload: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now, nullable=False)

    user: Mapped[User | None] = relationship(back_populates="routines")


class ScheduledWorkout(Base):
    """Weekly training planner entry, supporting both workout days and rest days."""

    __tablename__ = "scheduled_workouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    routine_id: Mapped[int | None] = mapped_column(
        ForeignKey("workout_routines.id", ondelete="SET NULL"),
        nullable=True,
    )
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    is_rest_day: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="planned")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now, nullable=False)

    user: Mapped[User] = relationship(back_populates="scheduled_workouts")


class WorkoutLog(Base):
    """Completed workout record used for history and progress charts."""

    __tablename__ = "workout_logs"
    __table_args__ = (
        CheckConstraint("actual_duration_min >= 1", name="ck_log_duration_positive"),
        CheckConstraint(
            "completion_percentage >= 0.0 AND completion_percentage <= 100.0",
            name="ck_log_completion_pct",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    routine_id: Mapped[int | None] = mapped_column(
        ForeignKey("workout_routines.id", ondelete="SET NULL"),
        nullable=True,
    )
    routine_title: Mapped[str] = mapped_column(String(140), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now, nullable=False, index=True)
    actual_duration_min: Mapped[int] = mapped_column(Integer, nullable=False)
    exercises_completed: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    perceived_effort_rpe: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completion_percentage: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship(back_populates="workout_logs")


class ExerciseFeedback(Base):
    """Per-user exercise rating and exclusion preference for ML ranking (Phase 4)."""

    __tablename__ = "exercise_feedback"
    __table_args__ = (
        UniqueConstraint("user_id", "exercise_id", name="uq_user_exercise_feedback"),
        CheckConstraint("rating IS NULL OR (rating >= 1 AND rating <= 5)", name="ck_feedback_rating_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exercise_id: Mapped[str] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_excluded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utc_now,
        onupdate=_utc_now,
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="exercise_feedback")
    exercise: Mapped[Exercise] = relationship(back_populates="feedback_entries")
