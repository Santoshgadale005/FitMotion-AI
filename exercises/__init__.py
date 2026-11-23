"""Exercise database package exports for FitMotion AI."""

from exercises.exercise_database import (
    ALL_EQUIPMENT_OPTIONS,
    EXERCISES_JSON_PATH,
    SPORTS_JSON_PATH,
    export_exercises_json,
    get_all_exercises,
    get_exercise_by_id,
    load_exercises_from_json,
    load_sport_profiles,
    search_exercises,
    sync_exercises_to_db,
)

__all__ = [
    "ALL_EQUIPMENT_OPTIONS",
    "EXERCISES_JSON_PATH",
    "SPORTS_JSON_PATH",
    "export_exercises_json",
    "load_exercises_from_json",
    "load_sport_profiles",
    "sync_exercises_to_db",
    "get_all_exercises",
    "get_exercise_by_id",
    "search_exercises",
]
