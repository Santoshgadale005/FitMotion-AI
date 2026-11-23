"""Explainable hybrid AI exercise recommendation engine for FitMotion AI.

Combines transparent sports-science rule scoring with Scikit-learn preference
ranking while strictly honoring safety restrictions, excluded exercises,
equipment availability, experience level, and age considerations.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from athlete.fitness_goals import GOAL_CONFIG, parse_restriction_tags
from athlete.profile import get_user_feedback_map
from database.database import SessionLocal, get_db_session
from database.models import WorkoutLog
from exercises.exercise_database import get_all_exercises, load_sport_profiles
from recommendation.exercise_ranker import MLExerciseRanker

LEVEL_ORDER: dict[str, int] = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

INTENSITY_CATEGORY_FIT: dict[str, set[str]] = {
    "Low": {"Recovery and Cooldown", "Stretching and Flexibility", "Mobility", "Balance and Stability", "Warm-up"},
    "Moderate": {"Warm-up", "Mobility", "Stretching and Flexibility", "Strength Training", "Balance and Stability", "Cardiovascular Training", "Sport-Specific Conditioning"},
    "High": {"Strength Training", "Cardiovascular Training", "Sport-Specific Conditioning", "Warm-up", "Balance and Stability"},
}


def get_user_exercise_history_counts(
    user_id: int | None,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, int]:
    """Count how many times a user has completed each exercise across logged workouts."""
    if not user_id:
        return {}
    factory = session_factory or SessionLocal
    counts: Counter[str] = Counter()
    with get_db_session(factory) as session:
        logs = session.query(WorkoutLog).filter_by(user_id=user_id).all()
        for log in logs:
            for item in log.exercises_completed or []:
                ex_id = item.get("exercise_id") or item.get("id")
                if ex_id and item.get("completed", True):
                    counts[ex_id] += 1
    return dict(counts)


def _passes_equipment_filter(exercise: dict[str, Any], available_equipment: list[str]) -> bool:
    """Return True if the user can perform this exercise with their equipment.

    'Yoga Mat' is treated as optional floor comfort (a rug/towel works at home),
    whereas weights, bands, pull-up bars, jump ropes, bikes, and pools are
    strictly checked.
    """
    req = {e.strip().lower() for e in exercise.get("required_equipment", [])}
    strict_req = {e for e in req if e != "yoga mat"}
    if not strict_req:
        return True
    avail = {e.strip().lower() for e in available_equipment}
    return strict_req.issubset(avail)


def _passes_experience_filter(exercise: dict[str, Any], experience_level: str) -> bool:
    """Prevent recommending Advanced-only drills to Beginners."""
    suitable = exercise.get("suitable_levels", [])
    if suitable and experience_level in suitable:
        return True
    user_rank = LEVEL_ORDER.get(experience_level, 1)
    ex_rank = LEVEL_ORDER.get(exercise.get("difficulty_level", "Beginner"), 1)
    return ex_rank <= user_rank


def recommend_exercises(
    profile: dict[str, Any],
    top_n: int = 12,
    categories_filter: list[str] | None = None,
    intensity_override: str | None = None,
    equipment_override: list[str] | None = None,
    difficulty_override: str | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Generate ranked, explained exercise recommendations for an athlete profile.

    Returns:
        Dictionary containing:
        - recommendations: ordered list of exercise dicts enriched with `match_score`,
          `rule_score`, `ml_score`, and `explanation`.
        - ml_active: whether Scikit-learn personalization contributed.
        - filtered_out_count: count of exercises excluded for safety/equipment/level.
        - sport_profile: sport-specific physical demand metadata.
    """
    all_exercises = get_all_exercises(session_factory)
    sport_profiles = load_sport_profiles()

    user_id = profile.get("user_id")
    sport = profile.get("primary_sport", "General Fitness")
    experience = difficulty_override or profile.get("experience_level", "Beginner")
    primary_goal = profile.get("primary_goal", "General fitness and wellness")
    secondary_goals = list(profile.get("secondary_goals", []))
    intensity = intensity_override or profile.get("preferred_intensity", "Moderate")
    age = int(profile.get("age", 25))
    available_equipment = (
        list(equipment_override)
        if equipment_override is not None
        else list(profile.get("available_equipment", []))
    )

    feedback_map = get_user_feedback_map(user_id, session_factory) if user_id else {}
    history_counts = get_user_exercise_history_counts(user_id, session_factory)

    excluded_ids = set(profile.get("excluded_exercises", []))
    for ex_id, fb in feedback_map.items():
        if fb.get("is_excluded"):
            excluded_ids.add(ex_id)

    restriction_tags = parse_restriction_tags(profile.get("physical_restrictions"))
    sport_meta = sport_profiles.get(sport, sport_profiles["General Fitness"])
    goal_meta = GOAL_CONFIG.get(primary_goal, GOAL_CONFIG["General fitness and wellness"])

    secondary_primary_cats: set[str] = set()
    for sg in secondary_goals:
        sg_meta = GOAL_CONFIG.get(sg)
        if sg_meta:
            secondary_primary_cats.update(sg_meta["primary_categories"])

    # Step 1: Hard safety, exclusion, equipment, and level filtering
    candidates: list[dict[str, Any]] = []
    filtered_out = 0

    for ex in all_exercises:
        if ex["id"] in excluded_ids:
            filtered_out += 1
            continue
        if restriction_tags and (set(ex.get("restriction_tags", [])) & restriction_tags):
            filtered_out += 1
            continue
        if not _passes_equipment_filter(ex, available_equipment):
            filtered_out += 1
            continue
        if not _passes_experience_filter(ex, experience):
            filtered_out += 1
            continue
        if categories_filter and ex["category"] not in categories_filter:
            continue
        candidates.append(ex)

    # Step 2: Fit Scikit-learn ranker on user ratings + workout history
    ranker = MLExerciseRanker()
    ml_scores = ranker.fit_and_score(candidates, feedback_map, history_counts)

    # Step 3: Transparent rule-based scoring + human-readable explanations
    sport_priority_muscles = {m.lower() for m in sport_meta.get("priority_muscles", [])}
    sport_priority_cats = set(sport_meta.get("priority_categories", []))
    goal_primary_cats = set(goal_meta["primary_categories"])
    goal_secondary_cats = set(goal_meta["secondary_categories"])
    intensity_cats = INTENSITY_CATEGORY_FIT.get(intensity, INTENSITY_CATEGORY_FIT["Moderate"])

    scored: list[dict[str, Any]] = []
    for ex in candidates:
        rule_score = 35.0
        reasons: list[str] = []

        # Goal alignment (highest weight)
        if ex["category"] in goal_primary_cats:
            rule_score += 26.0
            reasons.append(f"directly targets your primary goal ({primary_goal})")
        elif ex["category"] in secondary_primary_cats:
            rule_score += 18.0
            reasons.append("supports your secondary fitness goals")
        elif ex["category"] in goal_secondary_cats:
            rule_score += 10.0
            reasons.append(f"complements your {primary_goal.lower()} routine")

        # Sport specificity
        if sport in ex.get("relevant_sports", []):
            rule_score += 18.0
            if ex["category"] == "Sport-Specific Conditioning" and sport != "General Fitness":
                rule_score += 8.0
                reasons.append(f"specifically built for {sport} conditioning demands")
            else:
                reasons.append(f"well matched to {sport} movement demands")

        # Priority muscle overlap for the selected sport
        ex_muscles = {m.lower() for m in ex.get("target_muscles", [])}
        muscle_overlap = sorted(ex_muscles & sport_priority_muscles)
        if muscle_overlap:
            rule_score += min(10.0, 3.5 * len(muscle_overlap))
            reasons.append(f"works key {sport} areas ({', '.join(m.title() for m in muscle_overlap[:2])})")

        if ex["category"] in sport_priority_cats:
            rule_score += 4.0

        # Experience & difficulty calibration
        if ex["difficulty_level"] == experience:
            rule_score += 8.0
            reasons.append(f"calibrated for {experience} level")
        elif experience == "Beginner" and ex["difficulty_level"] == "Beginner":
            rule_score += 8.0

        # Intensity fit
        if ex["category"] in intensity_cats:
            rule_score += 6.0

        # Age-considerate joint-friendly tuning (no medical claims)
        if age >= 55:
            if ex["category"] in {"Mobility", "Balance and Stability", "Stretching and Flexibility", "Recovery and Cooldown"}:
                rule_score += 6.0
                reasons.append("supports joint mobility and steady balance")
            if "jumping" in ex.get("restriction_tags", []):
                rule_score -= 10.0

        # Equipment friendliness note
        strict_equip = [e for e in ex.get("required_equipment", []) if e.lower() != "yoga mat"]
        if not strict_equip and not available_equipment:
            reasons.append("requires no gym equipment")

        # Variety nudge so recently over-repeated moves leave room for balanced variety
        prior_count = history_counts.get(ex["id"], 0)
        if prior_count >= 5:
            rule_score -= 3.0

        ml_info = ml_scores.get(ex["id"], {"ml_score": 0.0, "ml_reason": ""})
        ml_boost = float(ml_info["ml_score"])
        final_score = max(10.0, min(99.0, round(rule_score + ml_boost, 1)))

        if not reasons:
            reasons.append(f"fits your {experience} {sport} profile")

        explanation = "Selected because it " + "; ".join(reasons[:3]) + "."
        if ml_info["ml_reason"]:
            explanation = f"{explanation} {ml_info['ml_reason']}"

        enriched = dict(ex)
        enriched["match_score"] = final_score
        enriched["rule_score"] = round(rule_score, 1)
        enriched["ml_score"] = round(ml_boost, 2)
        enriched["explanation"] = explanation
        enriched["user_rating"] = feedback_map.get(ex["id"], {}).get("rating")
        scored.append(enriched)

    scored.sort(key=lambda item: (-item["match_score"], item["name"]))

    return {
        "recommendations": scored[:top_n],
        "all_ranked": scored,
        "ml_active": ranker.is_trained,
        "ml_training_samples": ranker.training_samples,
        "filtered_out_count": filtered_out,
        "sport_profile": sport_meta,
    }
