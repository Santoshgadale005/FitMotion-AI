"""Recommendation and routine generation package exports."""

from recommendation.exercise_ranker import MLExerciseRanker
from recommendation.recommendation_engine import (
    get_user_exercise_history_counts,
    recommend_exercises,
)
from recommendation.routine_generator import (
    ROUTINE_BLUEPRINTS,
    delete_workout_routine,
    generate_workout_routine,
    get_user_routines,
    save_workout_routine,
    toggle_favorite_routine,
)

__all__ = [
    "MLExerciseRanker",
    "get_user_exercise_history_counts",
    "recommend_exercises",
    "ROUTINE_BLUEPRINTS",
    "generate_workout_routine",
    "save_workout_routine",
    "get_user_routines",
    "toggle_favorite_routine",
    "delete_workout_routine",
]
