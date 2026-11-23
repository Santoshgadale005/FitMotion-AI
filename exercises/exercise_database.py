"""Exercise database manager, JSON exporter, SQLite seeder, and sport-accurate filtering."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

import config
from database.database import SessionLocal, get_db_session
from database.models import Exercise
from exercises.advanced_and_sport_catalog import EXPANDED_EXERCISES
from exercises.balance import BALANCE_EXERCISES
from exercises.cardio import CARDIO_EXERCISES
from exercises.mobility import MOBILITY_EXERCISES
from exercises.recovery import RECOVERY_EXERCISES
from exercises.sport_conditioning import SPORT_CONDITIONING_EXERCISES
from exercises.strength import STRENGTH_EXERCISES
from exercises.stretching import STRETCHING_EXERCISES
from exercises.visuals import ensure_exercise_visual
from exercises.warmup import WARMUP_EXERCISES

EXERCISES_JSON_PATH = config.DATA_DIR / "exercises.json"
SPORTS_JSON_PATH = config.DATA_DIR / "sports.json"

ALL_EQUIPMENT_OPTIONS: list[str] = [
    "Yoga Mat",
    "Dumbbells",
    "Resistance Band",
    "Pull-up Bar",
    "Jump Rope",
    "Stationary Bike",
    "Swimming Pool",
]

# Authentic sport-specificity mapping so filtering by Relevant Sport surfaces
# genuinely tailored exercises per discipline instead of showing identical lists.
CURATED_RELEVANT_SPORTS: dict[str, list[str]] = {
    "wu-light-jogging": ["Running", "Football", "Cricket", "General Fitness"],
    "wu-high-knees": ["Running", "Football", "Basketball"],
    "wu-butt-kicks": ["Running", "Football", "Cricket"],
    "wu-jumping-jacks": ["General Fitness", "Basketball", "Badminton"],
    "wu-arm-circles": ["Swimming", "Badminton", "Tennis", "Cricket"],
    "wu-dynamic-lunges": ["Football", "Badminton", "Tennis", "Cricket", "General Fitness"],
    "wu-leg-swings": ["Running", "Football", "Cricket"],
    "wu-side-shuffles": ["Badminton", "Basketball", "Tennis", "Football"],
    "mob-hip-drills": ["Football", "Running", "Badminton", "General Fitness"],
    "mob-ankle-mobility": ["Basketball", "Running", "Football", "Badminton"],
    "mob-shoulder-rotations": ["Swimming", "Badminton", "Tennis", "Cricket"],
    "mob-thoracic-rotations": ["Swimming", "Cricket", "Tennis", "General Fitness"],
    "mob-wrist-mobility": ["Badminton", "Tennis", "Cricket", "Basketball"],
    "mob-deep-squat": ["Basketball", "Football", "General Fitness"],
    "str-hamstring": ["Running", "Football", "Cricket", "General Fitness"],
    "str-quadriceps": ["Running", "Basketball", "Football", "General Fitness"],
    "str-calf": ["Running", "Basketball", "Badminton", "Tennis"],
    "str-hip-flexor": ["Running", "Football", "Swimming", "General Fitness"],
    "str-groin": ["Football", "Badminton", "Tennis", "Basketball"],
    "str-shoulder": ["Badminton", "Tennis", "Swimming", "Cricket"],
    "str-chest": ["Swimming", "Cricket", "General Fitness"],
    "str-triceps": ["Swimming", "Badminton", "Tennis", "Basketball"],
    "st-squats": ["General Fitness", "Football", "Basketball", "Running"],
    "st-lunges": ["Badminton", "Tennis", "Football", "General Fitness"],
    "st-pushups": ["General Fitness", "Swimming", "Basketball", "Cricket"],
    "st-pullups": ["Swimming", "Basketball", "General Fitness"],
    "st-planks": ["General Fitness", "Swimming", "Running", "Football"],
    "st-glute-bridges": ["Running", "Football", "General Fitness", "Cricket"],
    "st-calf-raises": ["Running", "Basketball", "Badminton", "Tennis"],
    "st-deadlifts": ["Football", "Cricket", "General Fitness", "Basketball"],
    "cardio-running": ["Running", "Football", "Cricket", "General Fitness"],
    "cardio-cycling": ["General Fitness", "Running", "Football"],
    "cardio-jump-rope": ["Badminton", "Tennis", "Basketball", "General Fitness"],
    "cardio-swimming": ["Swimming", "General Fitness"],
    "cardio-interval-training": ["Football", "Basketball", "Badminton", "Tennis"],
    "cardio-low-intensity": ["General Fitness", "Running", "Cricket"],
    "bal-single-leg": ["Running", "Football", "Basketball", "General Fitness"],
    "bal-bird-dog": ["Swimming", "Cricket", "General Fitness", "Running"],
    "bal-dead-bug": ["Swimming", "Running", "General Fitness", "Football"],
    "bal-single-leg-squats": ["Basketball", "Running", "Football", "Badminton"],
    "bal-side-plank": ["Football", "Cricket", "Tennis", "Swimming"],
    "rec-light-walking": ["Running", "Football", "Cricket", "General Fitness"],
    "rec-gentle-stretching": ["General Fitness", "Swimming", "Basketball", "Badminton"],
    "rec-breathing": ["General Fitness", "Swimming", "Running", "Cricket"],
    "rec-gentle-mobility": ["General Fitness", "Swimming", "Cricket", "Tennis"],
    "rec-low-cycling": ["Football", "Running", "Basketball", "General Fitness"],
    "sp-badminton-split-step": ["Badminton", "Tennis"],
    "sp-badminton-lateral-lunge": ["Badminton", "Tennis"],
    "sp-football-acceleration": ["Football", "Cricket"],
    "sp-football-cod-shuttle": ["Football", "Basketball", "Cricket"],
    "sp-basketball-landing": ["Basketball", "Badminton"],
    "sp-basketball-defensive-slides": ["Basketball", "Tennis", "Badminton"],
    "sp-cricket-rotational-core": ["Cricket", "Tennis", "Badminton"],
    "sp-cricket-scapular-slides": ["Cricket", "Swimming", "Tennis"],
    "sp-tennis-external-rotation": ["Tennis", "Badminton", "Cricket", "Swimming"],
    "sp-swimming-ytw-activation": ["Swimming", "Cricket", "Tennis"],
    "sp-running-a-skips": ["Running", "Football"],
    "sp-gym-goblet-squat": ["General Fitness", "Basketball", "Football"],
    "sp-gym-dumbbell-row": ["General Fitness", "Swimming", "Cricket"],
}


def build_raw_exercise_catalog(overwrite_visuals: bool = False) -> list[dict[str, Any]]:
    """Aggregate all 8 modular exercise lists + expanded catalog with curated sports & SVGs."""
    combined = (
        WARMUP_EXERCISES
        + MOBILITY_EXERCISES
        + STRETCHING_EXERCISES
        + STRENGTH_EXERCISES
        + CARDIO_EXERCISES
        + BALANCE_EXERCISES
        + RECOVERY_EXERCISES
        + SPORT_CONDITIONING_EXERCISES
        + EXPANDED_EXERCISES
    )
    enriched: list[dict[str, Any]] = []
    for item in combined:
        entry = dict(item)
        if entry["id"] in CURATED_RELEVANT_SPORTS:
            entry["relevant_sports"] = list(CURATED_RELEVANT_SPORTS[entry["id"]])
        entry["media_type"] = "svg"
        entry["media_reference"] = ensure_exercise_visual(entry, overwrite=overwrite_visuals)
        enriched.append(entry)
    return enriched


def export_exercises_json(overwrite_visuals: bool = False) -> list[dict[str, Any]]:
    """Write the complete structured exercise catalog to `data/exercises.json`."""
    catalog = build_raw_exercise_catalog(overwrite_visuals=overwrite_visuals)
    EXERCISES_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXERCISES_JSON_PATH.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return catalog


def load_exercises_from_json() -> list[dict[str, Any]]:
    """Load exercises from `data/exercises.json`, generating it if absent."""
    if not EXERCISES_JSON_PATH.exists():
        return export_exercises_json()
    return json.loads(EXERCISES_JSON_PATH.read_text(encoding="utf-8"))


def load_sport_profiles() -> dict[str, dict[str, Any]]:
    """Load sports-science demand profiles from `data/sports.json`."""
    return json.loads(SPORTS_JSON_PATH.read_text(encoding="utf-8"))


def sync_exercises_to_db(
    session_factory: sessionmaker[Session] | None = None,
    force_export_json: bool = False,
) -> int:
    """Idempotently seed or update all exercises into SQLite from the structured catalog."""
    catalog = (
        export_exercises_json(overwrite_visuals=force_export_json)
        if (force_export_json or not EXERCISES_JSON_PATH.exists())
        else load_exercises_from_json()
    )
    for entry in catalog:
        ensure_exercise_visual(entry, overwrite=force_export_json)

    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        existing_ids = {row[0] for row in session.query(Exercise.id).all()}
        for item in catalog:
            if item["id"] in existing_ids:
                ex = session.get(Exercise, item["id"])
                if ex is not None:
                    ex.name = item["name"]
                    ex.category = item["category"]
                    ex.description = item["description"]
                    ex.instructions = item["instructions"]
                    ex.target_muscles = item["target_muscles"]
                    ex.difficulty_level = item["difficulty_level"]
                    ex.default_duration_sec = item["default_duration_sec"]
                    ex.recommended_sets = item["recommended_sets"]
                    ex.recommended_reps = item["recommended_reps"]
                    ex.rest_seconds = item["rest_seconds"]
                    ex.required_equipment = item["required_equipment"]
                    ex.safety_instructions = item["safety_instructions"]
                    ex.common_mistakes = item["common_mistakes"]
                    ex.beginner_modification = item.get("beginner_modification")
                    ex.media_type = item.get("media_type", "svg")
                    ex.media_reference = item.get("media_reference")
                    ex.suitable_levels = item["suitable_levels"]
                    ex.relevant_sports = item["relevant_sports"]
            else:
                session.add(
                    Exercise(
                        id=item["id"],
                        name=item["name"],
                        category=item["category"],
                        description=item["description"],
                        instructions=item["instructions"],
                        target_muscles=item["target_muscles"],
                        difficulty_level=item["difficulty_level"],
                        default_duration_sec=item["default_duration_sec"],
                        recommended_sets=item["recommended_sets"],
                        recommended_reps=item["recommended_reps"],
                        rest_seconds=item["rest_seconds"],
                        required_equipment=item["required_equipment"],
                        safety_instructions=item["safety_instructions"],
                        common_mistakes=item["common_mistakes"],
                        beginner_modification=item.get("beginner_modification"),
                        media_type=item.get("media_type", "svg"),
                        media_reference=item.get("media_reference"),
                        suitable_levels=item["suitable_levels"],
                        relevant_sports=item["relevant_sports"],
                    )
                )
    return len(catalog)


def _exercise_model_to_dict(ex: Exercise, restriction_map: dict[str, list[str]]) -> dict[str, Any]:
    """Convert ORM Exercise into a clean dictionary including safety restriction tags."""
    return {
        "id": ex.id,
        "name": ex.name,
        "category": ex.category,
        "description": ex.description,
        "instructions": list(ex.instructions or []),
        "target_muscles": list(ex.target_muscles or []),
        "difficulty_level": ex.difficulty_level,
        "default_duration_sec": ex.default_duration_sec,
        "recommended_sets": ex.recommended_sets,
        "recommended_reps": ex.recommended_reps,
        "rest_seconds": ex.rest_seconds,
        "required_equipment": list(ex.required_equipment or []),
        "safety_instructions": list(ex.safety_instructions or []),
        "common_mistakes": list(ex.common_mistakes or []),
        "beginner_modification": ex.beginner_modification or "",
        "media_type": ex.media_type or "svg",
        "media_reference": ex.media_reference or "",
        "suitable_levels": list(ex.suitable_levels or []),
        "relevant_sports": list(ex.relevant_sports or []),
        "restriction_tags": restriction_map.get(ex.id, []),
    }


def _build_restriction_tag_map() -> dict[str, list[str]]:
    """Map exercise ID -> safety restriction tags from the structured catalog."""
    raw = load_exercises_from_json()
    return {item["id"]: list(item.get("restriction_tags", [])) for item in raw}


def get_all_exercises(
    session_factory: sessionmaker[Session] | None = None,
) -> list[dict[str, Any]]:
    """Fetch all exercises stored in SQLite (auto-seeding if empty)."""
    factory = session_factory or SessionLocal
    restriction_map = _build_restriction_tag_map()
    with get_db_session(factory) as session:
        rows = session.query(Exercise).order_by(Exercise.category, Exercise.name).all()
        if rows:
            return [_exercise_model_to_dict(row, restriction_map) for row in rows]

    sync_exercises_to_db(factory)
    with get_db_session(factory) as session:
        rows = session.query(Exercise).order_by(Exercise.category, Exercise.name).all()
        return [_exercise_model_to_dict(row, restriction_map) for row in rows]


def get_exercise_by_id(
    exercise_id: str,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any] | None:
    """Retrieve a single exercise by its unique ID."""
    factory = session_factory or SessionLocal
    restriction_map = _build_restriction_tag_map()
    with get_db_session(factory) as session:
        row = session.get(Exercise, exercise_id)
        return _exercise_model_to_dict(row, restriction_map) if row else None


def search_exercises(
    query: str = "",
    category: str | None = None,
    difficulty: str | None = None,
    sport: str | None = None,
    available_equipment: list[str] | None = None,
    bodyweight_only: bool = False,
    excluded_ids: set[str] | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> list[dict[str, Any]]:
    """Filter exercises by keyword, category, difficulty, sport, equipment, and exclusions.

    When a specific sport is selected, prioritizes sport-exclusive and
    Sport-Specific Conditioning exercises at the top of the list so each sport
    view is distinct and immediately relevant.
    """
    exercises = get_all_exercises(session_factory)
    q = query.strip().lower()
    equip_set = {e.lower() for e in available_equipment} if available_equipment is not None else None
    excluded = excluded_ids or set()

    results: list[dict[str, Any]] = []
    for ex in exercises:
        if ex["id"] in excluded:
            continue
        if category and category != "All" and ex["category"] != category:
            continue
        if difficulty and difficulty != "All" and ex["difficulty_level"] != difficulty:
            continue
        if sport and sport != "All" and sport not in ex["relevant_sports"]:
            continue
        if bodyweight_only and len(ex["required_equipment"]) > 0:
            continue
        if equip_set is not None:
            req = {e.lower() for e in ex["required_equipment"]}
            strict_req = {e for e in req if e != "yoga mat"}
            if not strict_req.issubset(equip_set):
                continue
        if q:
            haystack = " ".join(
                [
                    ex["name"],
                    ex["category"],
                    ex["description"],
                    " ".join(ex["target_muscles"]),
                    " ".join(ex["relevant_sports"]),
                ]
            ).lower()
            if q not in haystack:
                continue
        results.append(ex)

    if sport and sport != "All":
        results.sort(
            key=lambda e: (
                0 if e["category"] == "Sport-Specific Conditioning" else 1,
                0 if (e["relevant_sports"] and e["relevant_sports"][0] == sport) else 1,
                len(e["relevant_sports"]),
                e["name"],
            )
        )

    return results
