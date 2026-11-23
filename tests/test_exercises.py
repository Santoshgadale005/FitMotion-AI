"""Unit tests for the structured exercise catalog, JSON export, SVGs, and filtering."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session, sessionmaker

import config
from database.database import create_db_engine, init_db
from exercises import (
    EXERCISES_JSON_PATH,
    SPORTS_JSON_PATH,
    get_all_exercises,
    get_exercise_by_id,
    load_sport_profiles,
    search_exercises,
    sync_exercises_to_db,
)


@pytest.fixture()
def seeded_db():
    """Isolated in-memory SQLite DB seeded with the full exercise catalog."""
    engine = create_db_engine("sqlite:///:memory:")
    init_db(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)
    sync_exercises_to_db(factory, force_export_json=True)
    yield factory
    engine.dispose()


def test_all_eight_categories_and_sports_are_populated(seeded_db) -> None:
    """Every required exercise category, sport, and difficulty tier must be richly populated."""
    all_ex = get_all_exercises(seeded_db)
    assert len(all_ex) >= 85
    assert EXERCISES_JSON_PATH.exists()
    assert SPORTS_JSON_PATH.exists()

    present_categories = {e["category"] for e in all_ex}
    assert set(config.EXERCISE_CATEGORIES) == present_categories

    # Ensure Advanced, Intermediate, and Beginner each have substantial coverage
    by_level = {lvl: [e for e in all_ex if e["difficulty_level"] == lvl] for lvl in config.EXPERIENCE_LEVELS}
    assert len(by_level["Beginner"]) >= 25
    assert len(by_level["Intermediate"]) >= 18
    assert len(by_level["Advanced"]) >= 20

    sport_profiles = load_sport_profiles()
    assert set(config.SUPPORTED_SPORTS) == set(sport_profiles.keys())


def test_relevant_sport_filter_produces_distinct_sport_specific_results(seeded_db) -> None:
    """Switching Relevant Sport must return genuinely distinct, sport-prioritized exercises."""
    swim_ex = search_exercises(sport="Swimming", session_factory=seeded_db)
    foot_ex = search_exercises(sport="Football", session_factory=seeded_db)
    badm_ex = search_exercises(sport="Badminton", session_factory=seeded_db)

    swim_top5 = {e["id"] for e in swim_ex[:5]}
    foot_top5 = {e["id"] for e in foot_ex[:5]}
    badm_top5 = {e["id"] for e in badm_ex[:5]}

    assert swim_top5 != foot_top5
    assert foot_top5 != badm_top5
    assert swim_top5 != badm_top5
    assert any("sp-swimming" in e["id"] for e in swim_ex[:5])
    assert any("sp-football" in e["id"] for e in foot_ex[:5])
    assert any("sp-badminton" in e["id"] for e in badm_ex[:5])

    # Advanced filter across library must return many results
    adv_ex = search_exercises(difficulty="Advanced", session_factory=seeded_db)
    assert len(adv_ex) >= 20


def test_every_exercise_has_required_fields_and_verified_local_visual(seeded_db) -> None:
    """No exercise may have missing metadata or a broken/missing demonstration file."""
    all_ex = get_all_exercises(seeded_db)
    seen_ids: set[str] = set()

    for ex in all_ex:
        assert ex["id"] not in seen_ids
        seen_ids.add(ex["id"])
        assert ex["name"]
        assert ex["description"]
        assert len(ex["instructions"]) >= 3
        assert len(ex["target_muscles"]) >= 1
        assert len(ex["safety_instructions"]) >= 1
        assert len(ex["common_mistakes"]) >= 1
        assert ex["beginner_modification"]
        assert len(ex["suitable_levels"]) >= 1
        assert len(ex["relevant_sports"]) >= 1

        # Verify local animated SVG demonstration asset exists and is valid XML
        import xml.etree.ElementTree as ET

        visual_path = config.BASE_DIR / ex["media_reference"]
        assert visual_path.exists(), f"Missing visual asset: {visual_path}"
        svg_text = visual_path.read_text(encoding="utf-8")
        assert svg_text.startswith("<svg")
        assert "<animate " in svg_text, f"SVG is not animated: {visual_path}"
        ET.fromstring(svg_text)


def test_search_and_filter_exercises(seeded_db) -> None:
    """Keyword, category, sport, bodyweight, and exclusion filters must work accurately."""
    warmup_only = search_exercises(category="Warm-up", session_factory=seeded_db)
    assert len(warmup_only) >= 10
    assert all(e["category"] == "Warm-up" for e in warmup_only)

    badminton_ex = search_exercises(sport="Badminton", session_factory=seeded_db)
    assert any("Badminton" in e["name"] for e in badminton_ex)

    bw_only = search_exercises(bodyweight_only=True, session_factory=seeded_db)
    assert len(bw_only) >= 20
    assert all(len(e["required_equipment"]) == 0 for e in bw_only)

    hamstring = search_exercises(query="hamstring", session_factory=seeded_db)
    assert any(e["id"] == "str-hamstring" for e in hamstring)

    excluded = search_exercises(excluded_ids={"str-hamstring"}, session_factory=seeded_db)
    assert all(e["id"] != "str-hamstring" for e in excluded)

    single = get_exercise_by_id("wu-high-knees", seeded_db)
    assert single is not None
    assert single["name"] == "High Knees"
