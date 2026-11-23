"""Scikit-learn machine learning exercise ranker for FitMotion AI.

Uses a scikit-learn Pipeline (StandardScaler + Ridge regression) combined with
cosine similarity over engineered exercise feature vectors to personalize
rankings from each user's exercise ratings and workout completion history.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import config

DIFFICULTY_NUMERIC: dict[str, float] = {
    "Beginner": 1.0,
    "Intermediate": 2.0,
    "Advanced": 3.0,
}


class MLExerciseRanker:
    """Personalized Scikit-learn ranker that learns from ratings and workout history."""

    def __init__(self) -> None:
        self._categories = list(config.EXERCISE_CATEGORIES)
        self._sports = list(config.SUPPORTED_SPORTS)
        self._model: Pipeline | None = None
        self.is_trained: bool = False
        self.training_samples: int = 0

    def _featurize(self, exercise: dict[str, Any]) -> np.ndarray:
        """Encode an exercise dictionary into a fixed-length numeric feature vector."""
        cat_vec = [1.0 if exercise["category"] == c else 0.0 for c in self._categories]
        sport_vec = [1.0 if s in exercise.get("relevant_sports", []) else 0.0 for s in self._sports]
        diff_val = DIFFICULTY_NUMERIC.get(exercise.get("difficulty_level", "Beginner"), 1.0)
        equip_count = float(len([e for e in exercise.get("required_equipment", []) if e.lower() != "yoga mat"]))
        duration_min = float(exercise.get("default_duration_sec", 60)) / 60.0
        sets_val = float(exercise.get("recommended_sets", 2))
        rest_val = float(exercise.get("rest_seconds", 30)) / 60.0

        return np.array(
            cat_vec + sport_vec + [diff_val, equip_count, duration_min, sets_val, rest_val],
            dtype=np.float64,
        )

    def fit_and_score(
        self,
        exercises: list[dict[str, Any]],
        feedback_map: dict[str, dict[str, Any]] | None = None,
        exercise_completion_counts: dict[str, int] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """Fit a per-user preference model and return ML boost scores + reasons.

        Gracefully returns neutral scores (0.0) when there is insufficient
        user interaction history (cold-start safe).
        """
        if not exercises:
            return {}

        feedback = feedback_map or {}
        history = exercise_completion_counts or {}

        feature_matrix = np.vstack([self._featurize(ex) for ex in exercises])
        id_to_idx = {ex["id"]: idx for idx, ex in enumerate(exercises)}

        train_X: list[np.ndarray] = []
        train_y: list[float] = []
        positive_indices: list[int] = []

        for ex_id, idx in id_to_idx.items():
            fb = feedback.get(ex_id, {})
            rating = fb.get("rating")
            completions = history.get(ex_id, 0)

            if rating is not None:
                # Map 1..5 rating onto -1.0..+1.0 preference target
                target = (float(rating) - 3.0) / 2.0
                train_X.append(feature_matrix[idx])
                train_y.append(target)
                if rating >= 4:
                    positive_indices.append(idx)
            elif completions > 0:
                # Implicit positive signal from repeated completion (capped gently)
                implicit_target = min(0.65, 0.25 + 0.12 * completions)
                train_X.append(feature_matrix[idx])
                train_y.append(implicit_target)
                positive_indices.append(idx)

        self.training_samples = len(train_X)
        scores: dict[str, dict[str, Any]] = {}

        if len(train_X) < 2:
            self.is_trained = False
            for ex in exercises:
                scores[ex["id"]] = {"ml_score": 0.0, "ml_reason": ""}
            return scores

        # 1. Fit regularized Ridge regression on explicit & implicit preferences
        X_arr = np.vstack(train_X)
        y_arr = np.array(train_y, dtype=np.float64)

        pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("regressor", Ridge(alpha=2.0)),
            ]
        )
        pipeline.fit(X_arr, y_arr)
        self._model = pipeline
        self.is_trained = True

        reg_preds = np.clip(pipeline.predict(feature_matrix), -1.0, 1.0)

        # 2. Content-based cosine similarity to user's positively rated/completed moves
        sim_scores = np.zeros(len(exercises), dtype=np.float64)
        if positive_indices:
            pos_centroid = np.mean(feature_matrix[positive_indices], axis=0, keepdims=True)
            sim_scores = cosine_similarity(feature_matrix, pos_centroid).ravel()

        for idx, ex in enumerate(exercises):
            ex_id = ex["id"]
            # Blend predicted preference and content similarity into a -12..+18 score adjustment
            blended = float(reg_preds[idx]) * 12.0 + float(sim_scores[idx]) * 6.0
            fb_rating = feedback.get(ex_id, {}).get("rating")
            completions = history.get(ex_id, 0)

            reason = ""
            if fb_rating is not None and fb_rating >= 4:
                reason = f"Boosted by ML ranker because you rated this exercise {fb_rating}/5."
            elif fb_rating is not None and fb_rating <= 2:
                reason = f"Deprioritized by ML ranker based on your {fb_rating}/5 rating."
            elif blended >= 6.0:
                reason = "Boosted by Scikit-learn ranker because its profile closely matches exercises you favor and complete."
            elif completions > 0:
                reason = f"Informed by your workout history ({completions} prior completion{'s' if completions > 1 else ''})."

            scores[ex_id] = {
                "ml_score": round(blended, 2),
                "ml_reason": reason,
            }

        return scores
