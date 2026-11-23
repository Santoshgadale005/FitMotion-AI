"""Machine learning exercise ranker for FitMotion AI.

Uses Scikit-learn (`StandardScaler` + `Ridge` + `cosine_similarity`) when
installed locally, and falls back to an exact closed-form NumPy Ridge +
cosine-similarity implementation in lightweight serverless runtimes (Vercel).
"""

from __future__ import annotations

from typing import Any

import numpy as np

import config

try:
    from sklearn.linear_model import Ridge
    from sklearn.metrics.pairwise import cosine_similarity as _sk_cosine
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    _HAS_SKLEARN = True
except ImportError:
    _HAS_SKLEARN = False

DIFFICULTY_NUMERIC: dict[str, float] = {
    "Beginner": 1.0,
    "Intermediate": 2.0,
    "Advanced": 3.0,
}


def _numpy_ridge_predict(X_train: np.ndarray, y_train: np.ndarray, X_all: np.ndarray, alpha: float = 2.0) -> np.ndarray:
    """Exact closed-form standardized Ridge regression using NumPy only."""
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    std = np.where(std < 1e-8, 1.0, std)

    Xs = (X_train - mean) / std
    X_all_s = (X_all - mean) / std

    y_mean = float(y_train.mean())
    yc = y_train - y_mean

    n_features = Xs.shape[1]
    weights = np.linalg.solve(Xs.T @ Xs + alpha * np.eye(n_features), Xs.T @ yc)
    return X_all_s @ weights + y_mean


def _numpy_cosine_sim(matrix: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between every row in `matrix` and `centroid`."""
    mat_norm = np.linalg.norm(matrix, axis=1, keepdims=True)
    cen_norm = np.linalg.norm(centroid, axis=1, keepdims=True)
    mat_norm = np.where(mat_norm < 1e-8, 1.0, mat_norm)
    cen_norm = np.where(cen_norm < 1e-8, 1.0, cen_norm)
    return ((matrix / mat_norm) @ (centroid / cen_norm).T).ravel()


class MLExerciseRanker:
    """Personalized ML ranker that learns from exercise ratings and workout history."""

    def __init__(self) -> None:
        self._categories = list(config.EXERCISE_CATEGORIES)
        self._sports = list(config.SUPPORTED_SPORTS)
        self._model: Any = None
        self.is_trained: bool = False
        self.training_samples: int = 0
        self.backend_name: str = "Scikit-learn Ridge" if _HAS_SKLEARN else "NumPy Ridge ML"

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
        """Fit a per-user preference model and return ML boost scores + reasons."""
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
                target = (float(rating) - 3.0) / 2.0
                train_X.append(feature_matrix[idx])
                train_y.append(target)
                if rating >= 4:
                    positive_indices.append(idx)
            elif completions > 0:
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

        X_arr = np.vstack(train_X)
        y_arr = np.array(train_y, dtype=np.float64)

        if _HAS_SKLEARN:
            pipeline = Pipeline(
                [
                    ("scaler", StandardScaler()),
                    ("regressor", Ridge(alpha=2.0)),
                ]
            )
            pipeline.fit(X_arr, y_arr)
            self._model = pipeline
            reg_preds = np.clip(pipeline.predict(feature_matrix), -1.0, 1.0)
        else:
            reg_preds = np.clip(_numpy_ridge_predict(X_arr, y_arr, feature_matrix, alpha=2.0), -1.0, 1.0)

        self.is_trained = True

        sim_scores = np.zeros(len(exercises), dtype=np.float64)
        if positive_indices:
            pos_centroid = np.mean(feature_matrix[positive_indices], axis=0, keepdims=True)
            sim_scores = (
                _sk_cosine(feature_matrix, pos_centroid).ravel()
                if _HAS_SKLEARN
                else _numpy_cosine_sim(feature_matrix, pos_centroid)
            )

        for idx, ex in enumerate(exercises):
            ex_id = ex["id"]
            blended = float(reg_preds[idx]) * 12.0 + float(sim_scores[idx]) * 6.0
            fb_rating = feedback.get(ex_id, {}).get("rating")
            completions = history.get(ex_id, 0)

            reason = ""
            if fb_rating is not None and fb_rating >= 4:
                reason = f"Boosted by ML ranker because you rated this exercise {fb_rating}/5."
            elif fb_rating is not None and fb_rating <= 2:
                reason = f"Deprioritized by ML ranker based on your {fb_rating}/5 rating."
            elif blended >= 6.0:
                reason = "Boosted by ML ranker because its profile closely matches exercises you favor and complete."
            elif completions > 0:
                reason = f"Informed by your workout history ({completions} prior completion{'s' if completions > 1 else ''})."

            scores[ex_id] = {
                "ml_score": round(blended, 2),
                "ml_reason": reason,
            }

        return scores
