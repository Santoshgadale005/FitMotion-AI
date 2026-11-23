"""Workout completion logging and workout history queries (Phase 6)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from database.database import SessionLocal, get_db_session
from database.models import ScheduledWorkout, WorkoutLog


def log_completed_workout(
    user_id: int,
    routine_title: str,
    actual_duration_min: int,
    exercises_completed: list[dict[str, Any]],
    routine_id: int | None = None,
    schedule_id: int | None = None,
    perceived_effort_rpe: int | None = None,
    completion_percentage: float = 100.0,
    notes: str | None = None,
    completed_at: datetime | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> int:
    """Persist a completed workout log and mark linked scheduled workout done."""
    duration = max(1, int(actual_duration_min))
    pct = max(0.0, min(100.0, float(completion_percentage)))

    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        entry = WorkoutLog(
            user_id=user_id,
            routine_id=routine_id,
            routine_title=routine_title.strip() or "Completed Workout",
            completed_at=completed_at or datetime.now(timezone.utc),
            actual_duration_min=duration,
            exercises_completed=list(exercises_completed),
            perceived_effort_rpe=int(perceived_effort_rpe) if perceived_effort_rpe is not None else None,
            completion_percentage=pct,
            notes=notes.strip() if notes else None,
        )
        session.add(entry)

        if schedule_id is not None:
            scheduled = session.query(ScheduledWorkout).filter_by(id=schedule_id, user_id=user_id).first()
            if scheduled is not None:
                scheduled.status = "completed"

        session.flush()
        return entry.id


def get_workout_history(
    user_id: int,
    limit: int = 100,
    session_factory: sessionmaker[Session] | None = None,
) -> list[dict[str, Any]]:
    """Return chronological list of logged workouts (newest first)."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        rows = (
            session.query(WorkoutLog)
            .filter_by(user_id=user_id)
            .order_by(WorkoutLog.completed_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "routine_id": r.routine_id,
                "routine_title": r.routine_title,
                "completed_at": r.completed_at,
                "actual_duration_min": r.actual_duration_min,
                "exercises_completed": list(r.exercises_completed or []),
                "perceived_effort_rpe": r.perceived_effort_rpe,
                "completion_percentage": round(float(r.completion_percentage), 1),
                "notes": r.notes or "",
            }
            for r in rows
        ]
