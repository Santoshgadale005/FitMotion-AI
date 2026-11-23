"""Workout tracking metrics and chart aggregations for Streamlit (Pandas) & Vercel API (JSON).

Strictly measures logged activity consistency, duration, completion rates, and
exercise frequency—never making unsupported physiological or medical claims.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from training.workout_tracker import get_workout_history

try:
    import pandas as pd

    _HAS_PANDAS = True
except ImportError:
    pd = None  # type: ignore[assignment]
    _HAS_PANDAS = False


def compute_progress_json(
    user_id: int,
    weekly_target_frequency: int = 3,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Compute pure-Python JSON-serializable progress summary and chart series."""
    logs = get_workout_history(user_id, limit=500, session_factory=session_factory)

    total_workouts = len(logs)
    total_minutes = sum(int(l["actual_duration_min"]) for l in logs)
    avg_completion = (
        round(sum(float(l["completion_percentage"]) for l in logs) / total_workouts, 1)
        if total_workouts > 0
        else 0.0
    )

    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)

    last_7_days_count = 0
    exercise_counter: Counter[str] = Counter()
    category_counter: Counter[str] = Counter()
    weekly_agg: dict[str, dict[str, float]] = defaultdict(lambda: {"workouts": 0, "total_minutes": 0, "pct_sum": 0.0})
    daily_agg: dict[str, dict[str, int]] = defaultdict(lambda: {"workouts": 0, "total_minutes": 0})

    for log in logs:
        ts: datetime = log["completed_at"]
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts >= seven_days_ago:
            last_7_days_count += 1

        week_key = ts.strftime("%Y-W%W")
        day_key = ts.date().isoformat()
        dur = int(log["actual_duration_min"])
        pct = float(log["completion_percentage"])

        weekly_agg[week_key]["workouts"] += 1
        weekly_agg[week_key]["total_minutes"] += dur
        weekly_agg[week_key]["pct_sum"] += pct

        daily_agg[day_key]["workouts"] += 1
        daily_agg[day_key]["total_minutes"] += dur

        for ex in log["exercises_completed"]:
            if ex.get("completed", True):
                ex_name = ex.get("name") or ex.get("exercise_id", "Exercise")
                exercise_counter[ex_name] += 1
                cat = ex.get("category")
                if cat:
                    category_counter[cat] += 1

    weekly_series = [
        {
            "week": wk,
            "workouts": int(v["workouts"]),
            "total_minutes": int(v["total_minutes"]),
            "avg_completion": round(v["pct_sum"] / max(1, v["workouts"]), 1),
        }
        for wk, v in sorted(weekly_agg.items())
    ]
    daily_series = [
        {
            "date": dk,
            "workouts": int(v["workouts"]),
            "total_minutes": int(v["total_minutes"]),
        }
        for dk, v in sorted(daily_agg.items())
    ]
    top_exercises = [{"Exercise": name, "Times Completed": count} for name, count in exercise_counter.most_common(10)]
    categories = [{"Category": cat, "Exercises Completed": count} for cat, count in category_counter.most_common()]

    weekly_target = max(1, int(weekly_target_frequency))
    weekly_goal_adherence_pct = min(100.0, round((last_7_days_count / weekly_target) * 100.0, 1))

    recent_serialized = [
        {
            "id": l["id"],
            "routine_title": l["routine_title"],
            "completed_at": l["completed_at"].isoformat() if isinstance(l["completed_at"], datetime) else str(l["completed_at"]),
            "actual_duration_min": l["actual_duration_min"],
            "perceived_effort_rpe": l["perceived_effort_rpe"],
            "completion_percentage": l["completion_percentage"],
            "notes": l["notes"],
            "exercises_completed": l["exercises_completed"],
        }
        for l in logs[:15]
    ]

    return {
        "total_workouts": total_workouts,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60.0, 1),
        "workouts_last_7_days": last_7_days_count,
        "weekly_target_frequency": weekly_target,
        "weekly_goal_adherence_pct": weekly_goal_adherence_pct,
        "avg_completion_pct": avg_completion,
        "weekly_series": weekly_series,
        "daily_series": daily_series,
        "top_exercises": top_exercises,
        "categories": categories,
        "recent_logs": recent_serialized,
    }


def compute_progress_summary(
    user_id: int,
    weekly_target_frequency: int = 3,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Compute activity metrics plus Pandas DataFrames for the Streamlit dashboard."""
    base = compute_progress_json(user_id, weekly_target_frequency, session_factory)
    if _HAS_PANDAS and pd is not None:
        base["weekly_df"] = (
            pd.DataFrame(base["weekly_series"])
            if base["weekly_series"]
            else pd.DataFrame(columns=["week", "workouts", "total_minutes", "avg_completion"])
        )
        base["daily_df"] = (
            pd.DataFrame(base["daily_series"])
            if base["daily_series"]
            else pd.DataFrame(columns=["date", "workouts", "total_minutes"])
        )
        base["top_exercises_df"] = pd.DataFrame(base["top_exercises"])
        base["category_df"] = pd.DataFrame(base["categories"])
    return base
