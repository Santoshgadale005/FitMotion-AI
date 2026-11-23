"""Database layer for FitMotion AI."""

from database.database import (
    Base,
    SessionLocal,
    check_database_health,
    create_db_engine,
    get_db_session,
    get_table_counts,
    init_db,
)
from database.models import (
    AthleteProfile,
    Exercise,
    ExerciseFeedback,
    ScheduledWorkout,
    User,
    WorkoutLog,
    WorkoutRoutine,
)

__all__ = [
    "Base",
    "SessionLocal",
    "create_db_engine",
    "init_db",
    "get_db_session",
    "check_database_health",
    "get_table_counts",
    "User",
    "AthleteProfile",
    "Exercise",
    "WorkoutRoutine",
    "ScheduledWorkout",
    "WorkoutLog",
    "ExerciseFeedback",
]
