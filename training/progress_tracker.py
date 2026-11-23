"""Workout tracking metrics and Pandas aggregations for Plotly dashboards (Phase 8).

Strictly measures logged activity consistency, duration, completion rates, and
exercise frequency—never making unsupported physiological or medical claims.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any

import pandas as pd
from sqlalchemy.orm import Session, sessionmaker

from training.workout_tracker import get_workout_history


def compute_progress_summary(
    user_id: int,
    weekly_target_frequency: int = 3,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Compute activity metrics and chart-ready DataFrames from logged workouts."""
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
    daily_rows: list[dict[str, Any]] = []

    for log in logs:
        ts: datetime = log["completed_at"]
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts >= seven_days_ago:
            last_7_days_count += 1

        daily_rows.append(
            {
                "date": ts.date(),
                "week": ts.strftime("%Y-W%W"),
                "duration_min": int(log["actual_duration_min"]),
                "completion_pct": float(log["completion_percentage"]),
                "rpe": log["perceived_effort_rpe"] or 0,
                "title": log["routine_title"],
            }
        )

        for ex in log["exercises_completed"]:
            if ex.get("completed", True):
                ex_name = ex.get("name") or ex.get("exercise_id", "Exercise")
                exercise_counter[ex_name] += 1
                cat = ex.get("category")
                if cat:
                    category_counter[cat] += 1

    if daily_rows:
        df_logs = pd.DataFrame(daily_rows)
        weekly_df = (
            df_logs.groupby("week", as_index=False)
            .agg(workouts=("duration_min", "count"), total_minutes=("duration_min", "sum"), avg_completion=("completion_pct", "mean"))
            .sort_values("week")
        )
        daily_df = (
            df_logs.groupby("date", as_index=False)
            .agg(workouts=("duration_min", "count"), total_minutes=("duration_min", "sum"))
            .sort_values("date")
        )
    else:
        weekly_df = pd.DataFrame(columns=["week", "workouts", "total_minutes", "avg_completion"])
        daily_df = pd.DataFrame(columns=["date", "workouts", "total_minutes"])

    top_exercises_df = pd.DataFrame(
        [{"Exercise": name, "Times Completed": count} for name, count in exercise_counter.most_common(10)]
    )
    category_df = pd.DataFrame(
        [{"Category": cat, "Exercises Completed": count} for cat, count in category_counter.most_common()]
    )

    weekly_target = max(1, int(weekly_target_frequency))
    weekly_goal_adherence_pct = min(100.0, round((last_7_days_count / weekly_target) * 100.0, 1))

    return {
        "total_workouts": total_workouts,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60.0, 1),
        "workouts_last_7_days": last_7_days_count,
        "weekly_target_frequency": weekly_target,
        "weekly_goal_adherence_pct": weekly_goal_adherence_pct,
        "avg_completion_pct": avg_completion,
        "weekly_df": weekly_df,
        "daily_df": daily_df,
        "top_exercises_df": top_exercises_df,
        "category_df": category_df,
        "recent_logs": logs[:10],
    }
