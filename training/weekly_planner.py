"""Weekly training planner with rest-day management and load-balance guardrails."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from database.database import SessionLocal, get_db_session
from database.models import ScheduledWorkout, WorkoutRoutine
from recommendation.routine_generator import generate_workout_routine, save_workout_routine


def get_week_start(reference: date | None = None) -> date:
    """Return the Monday of the week containing `reference`."""
    ref = reference or date.today()
    return ref - timedelta(days=ref.weekday())


def assign_day_schedule(
    user_id: int,
    scheduled_date: date,
    routine_id: int | None = None,
    is_rest_day: bool = False,
    status: str = "planned",
    notes: str | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> int:
    """Create or replace a user's schedule entry for a specific date."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        existing = (
            session.query(ScheduledWorkout)
            .filter_by(user_id=user_id, scheduled_date=scheduled_date)
            .first()
        )
        if existing is not None:
            existing.routine_id = None if is_rest_day else routine_id
            existing.is_rest_day = is_rest_day
            existing.status = status
            existing.notes = notes
            session.flush()
            return existing.id

        record = ScheduledWorkout(
            user_id=user_id,
            routine_id=None if is_rest_day else routine_id,
            scheduled_date=scheduled_date,
            is_rest_day=is_rest_day,
            status=status,
            notes=notes,
        )
        session.add(record)
        session.flush()
        return record.id


def get_week_schedule(
    user_id: int,
    week_start: date | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> list[dict[str, Any]]:
    """Return all 7 days of the requested week with routine metadata attached."""
    start = get_week_start(week_start)
    end = start + timedelta(days=6)
    factory = session_factory or SessionLocal

    with get_db_session(factory) as session:
        entries = (
            session.query(ScheduledWorkout)
            .filter(
                ScheduledWorkout.user_id == user_id,
                ScheduledWorkout.scheduled_date >= start,
                ScheduledWorkout.scheduled_date <= end,
            )
            .all()
        )
        by_date = {e.scheduled_date: e for e in entries}

        routine_ids = {e.routine_id for e in entries if e.routine_id is not None}
        routine_map: dict[int, WorkoutRoutine] = {}
        if routine_ids:
            routines = session.query(WorkoutRoutine).filter(WorkoutRoutine.id.in_(routine_ids)).all()
            routine_map = {r.id: r for r in routines}

        week_days: list[dict[str, Any]] = []
        for offset in range(7):
            day = start + timedelta(days=offset)
            entry = by_date.get(day)
            routine = routine_map.get(entry.routine_id) if (entry and entry.routine_id) else None
            week_days.append(
                {
                    "date": day,
                    "day_name": day.strftime("%A"),
                    "schedule_id": entry.id if entry else None,
                    "is_rest_day": entry.is_rest_day if entry else False,
                    "status": entry.status if entry else "unscheduled",
                    "notes": (entry.notes or "") if entry else "",
                    "routine_id": routine.id if routine else None,
                    "routine_title": routine.title if routine else ("Rest & Recovery Day" if (entry and entry.is_rest_day) else "Not Scheduled"),
                    "routine_type": routine.routine_type if routine else "",
                    "intensity": routine.intensity if routine else ("Rest" if (entry and entry.is_rest_day) else ""),
                    "estimated_duration_min": routine.estimated_duration_min if routine else 0,
                    "exercises": list(routine.exercises_payload or []) if routine else [],
                }
            )
        return week_days


def evaluate_weekly_load(week_days: list[dict[str, Any]]) -> dict[str, Any]:
    """Check weekly training balance and warn against excessive training loads."""
    active_days = [d for d in week_days if not d["is_rest_day"] and d["routine_id"] is not None]
    rest_days = [d for d in week_days if d["is_rest_day"]]
    high_days = [d for d in active_days if d["intensity"] == "High"]

    warnings: list[str] = []
    if len(active_days) == 7 and not rest_days:
        warnings.append(
            "You have workouts scheduled all 7 days without a rest day. Consider scheduling at least 1–2 rest or gentle recovery days."
        )

    consecutive_high = 0
    max_consecutive_high = 0
    for d in week_days:
        if not d["is_rest_day"] and d["intensity"] == "High":
            consecutive_high += 1
            max_consecutive_high = max(max_consecutive_high, consecutive_high)
        else:
            consecutive_high = 0

    if max_consecutive_high >= 2:
        warnings.append(
            "Back-to-back High-intensity sessions are scheduled. Separating intense days with moderate, mobility, or rest days supports better recovery."
        )

    if len(high_days) > 3:
        warnings.append(
            f"{len(high_days)} High-intensity workouts are scheduled this week. Keeping intense sessions to 2–3 per week helps avoid excessive fatigue."
        )

    return {
        "planned_workouts": len(active_days),
        "rest_days": len(rest_days),
        "high_intensity_days": len(high_days),
        "total_planned_minutes": sum(d["estimated_duration_min"] for d in active_days),
        "is_balanced": len(warnings) == 0,
        "warnings": warnings,
    }


def generate_balanced_weekly_plan(
    user_id: int,
    profile: dict[str, Any],
    week_start: date | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> list[dict[str, Any]]:
    """Auto-build and persist a balanced 7-day plan respecting frequency and recovery.

    Never schedules intense workouts every day—always caps high-effort sessions
    and builds in explicit rest or low-strain recovery days.
    """
    start = get_week_start(week_start)
    # Cap active training sessions at 6 so at least 1 explicit rest day is always protected
    freq = max(1, min(6, int(profile.get("weekly_frequency", 3))))
    duration = int(profile.get("available_duration_min", 25))
    sport = profile.get("primary_sport", "General Fitness")
    pref_intensity = profile.get("preferred_intensity", "Moderate")

    # Evenly spaced training day offsets (0=Mon .. 6=Sun)
    day_patterns: dict[int, list[int]] = {
        1: [2],
        2: [1, 4],
        3: [0, 2, 4],
        4: [0, 1, 3, 5],
        5: [0, 1, 2, 4, 5],
        6: [0, 1, 2, 3, 4, 5],
    }
    active_offsets = set(day_patterns[freq])

    # Rotate routine types cleanly so intense days are never back-to-back
    session_rotation: list[tuple[str, str]] = [
        ("Sport-specific conditioning routine" if sport != "General Fitness" else "20-minute full-body workout", "High" if pref_intensity == "High" else "Moderate"),
        ("10-minute mobility routine", "Low"),
        ("30-minute strength routine", "Moderate"),
        ("Recovery-focused routine", "Low"),
        ("20-minute full-body workout", "Moderate"),
        ("15-minute flexibility routine", "Low"),
    ]

    rot_idx = 0
    for offset in range(7):
        day = start + timedelta(days=offset)
        if offset not in active_offsets:
            assign_day_schedule(
                user_id=user_id,
                scheduled_date=day,
                is_rest_day=True,
                status="planned",
                notes="Scheduled rest & hydration day to support recovery.",
                session_factory=session_factory,
            )
        else:
            r_type, r_intensity = session_rotation[rot_idx % len(session_rotation)]
            rot_idx += 1
            routine = generate_workout_routine(
                profile=profile,
                routine_type=r_type,
                duration_min=min(duration, 20) if r_intensity == "Low" else duration,
                intensity=r_intensity,
                session_factory=session_factory,
            )
            routine_id = save_workout_routine(
                user_id=user_id,
                routine=routine,
                is_favorite=False,
                session_factory=session_factory,
            )
            assign_day_schedule(
                user_id=user_id,
                scheduled_date=day,
                routine_id=routine_id,
                is_rest_day=False,
                status="planned",
                notes=f"Auto-balanced {r_intensity.lower()}-intensity session for {sport}.",
                session_factory=session_factory,
            )

    return get_week_schedule(user_id, start, session_factory)


def update_schedule_status(
    user_id: int,
    schedule_id: int,
    status: str,
    session_factory: sessionmaker[Session] | None = None,
) -> bool:
    """Update a scheduled workout status ('planned', 'completed', 'skipped')."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        row = session.query(ScheduledWorkout).filter_by(id=schedule_id, user_id=user_id).first()
        if row is None:
            return False
        row.status = status
        return True


def get_upcoming_workouts(
    user_id: int,
    days_ahead: int = 7,
    session_factory: sessionmaker[Session] | None = None,
) -> list[dict[str, Any]]:
    """Return upcoming planned sessions starting from today."""
    today = date.today()
    end = today + timedelta(days=days_ahead)
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        rows = (
            session.query(ScheduledWorkout)
            .filter(
                ScheduledWorkout.user_id == user_id,
                ScheduledWorkout.scheduled_date >= today,
                ScheduledWorkout.scheduled_date <= end,
            )
            .order_by(ScheduledWorkout.scheduled_date.asc())
            .all()
        )
        routine_ids = {r.routine_id for r in rows if r.routine_id is not None}
        routine_map = {}
        if routine_ids:
            routine_map = {
                r.id: r
                for r in session.query(WorkoutRoutine).filter(WorkoutRoutine.id.in_(routine_ids)).all()
            }
        results: list[dict[str, Any]] = []
        for row in rows:
            routine = routine_map.get(row.routine_id) if row.routine_id else None
            results.append(
                {
                    "schedule_id": row.id,
                    "date": row.scheduled_date,
                    "day_name": row.scheduled_date.strftime("%a, %b %d"),
                    "is_rest_day": row.is_rest_day,
                    "status": row.status,
                    "routine_id": row.routine_id,
                    "title": "Rest & Recovery Day" if row.is_rest_day else (routine.title if routine else "Scheduled Session"),
                    "duration_min": routine.estimated_duration_min if routine else 0,
                    "intensity": "Rest" if row.is_rest_day else (routine.intensity if routine else "Moderate"),
                }
            )
        return results
