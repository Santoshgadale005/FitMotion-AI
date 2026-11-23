"""Phase 1 unit tests for FitMotion AI database schema, constraints, and health checks."""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

import config
from database.database import (
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


@pytest.fixture()
def test_db():
    """Provide an isolated in-memory SQLite engine and session factory per test."""
    engine = create_db_engine("sqlite:///:memory:")
    init_db(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)
    yield engine, factory
    engine.dispose()


def test_database_initializes_all_expected_tables(test_db) -> None:
    """All 7 core relational tables should exist after init_db()."""
    engine, _ = test_db
    health = check_database_health(engine)

    assert health["status"] == "connected"
    assert health["dialect"] == "sqlite"
    expected_tables = {
        "users",
        "athlete_profiles",
        "exercises",
        "workout_routines",
        "scheduled_workouts",
        "workout_logs",
        "exercise_feedback",
    }
    assert expected_tables.issubset(set(health["tables"]))


def test_get_table_counts_starts_empty(test_db) -> None:
    """A freshly initialized database should report zero rows across all tables."""
    engine, _ = test_db
    counts = get_table_counts(engine)

    assert len(counts) == 7
    assert all(count == 0 for count in counts.values())


def test_user_and_athlete_profile_crud_and_cascade(test_db) -> None:
    """Users and their 1-to-1 athlete profiles should persist and cascade-delete cleanly."""
    engine, factory = test_db

    with get_db_session(factory) as session:
        user = User(
            email="athlete@fitmotion.local",
            password_hash="hashed_secret_placeholder",
            full_name="Aarav Sharma",
            onboarding_completed=True,
        )
        session.add(user)
        session.flush()

        profile = AthleteProfile(
            user_id=user.id,
            age=22,
            height_cm=178.0,
            weight_kg=72.5,
            primary_sport="Football",
            experience_level="Intermediate",
            primary_goal="Improve mobility",
            secondary_goals=["Improve flexibility"],
            weekly_frequency=4,
            available_duration_min=25,
            available_equipment=[],
            preferred_intensity="Moderate",
        )
        session.add(profile)

    counts = get_table_counts(engine)
    assert counts["users"] == 1
    assert counts["athlete_profiles"] == 1

    # Verify cascade delete removes dependent athlete profile
    with get_db_session(factory) as session:
        stored_user = session.query(User).filter_by(email="athlete@fitmotion.local").one()
        assert stored_user.profile is not None
        assert stored_user.profile.primary_sport == "Football"
        session.delete(stored_user)

    counts_after = get_table_counts(engine)
    assert counts_after["users"] == 0
    assert counts_after["athlete_profiles"] == 0


def test_unique_email_and_check_constraints(test_db) -> None:
    """Duplicate emails and out-of-range profile values must be rejected by SQLite."""
    _, factory = test_db

    with get_db_session(factory) as session:
        session.add(User(email="dup@fitmotion.local", password_hash="hash1", full_name="User One"))

    with pytest.raises(IntegrityError):
        with get_db_session(factory) as session:
            session.add(User(email="dup@fitmotion.local", password_hash="hash2", full_name="User Two"))

    # Invalid weekly frequency (> 7) should violate CheckConstraint
    with pytest.raises(IntegrityError):
        with get_db_session(factory) as session:
            u = session.query(User).filter_by(email="dup@fitmotion.local").one()
            session.add(AthleteProfile(user_id=u.id, age=24, weekly_frequency=9, available_duration_min=30))


def test_exercise_routine_schedule_log_and_feedback_relationships(test_db) -> None:
    """Core training entities should link cleanly across foreign keys."""
    engine, factory = test_db

    with get_db_session(factory) as session:
        user = User(email="runner@fitmotion.local", password_hash="hash", full_name="Maya Patel")
        exercise = Exercise(
            id="wu-high-knees",
            name="High Knees",
            category="Warm-up",
            description="Dynamic running-in-place drill to elevate heart rate and warm up hip flexors.",
            instructions=["Stand tall with feet hip-width apart.", "Drive knees alternately to hip height."],
            target_muscles=["Hip Flexors", "Quadriceps", "Calves"],
            difficulty_level="Beginner",
            default_duration_sec=45,
            recommended_sets=2,
            recommended_reps="30-45 sec",
            rest_seconds=30,
            required_equipment=[],
            safety_instructions=["Land softly on the balls of your feet."],
            common_mistakes=["Leaning backward while lifting knees."],
            suitable_levels=["Beginner", "Intermediate", "Advanced"],
            relevant_sports=["Running", "Football", "Badminton"],
        )
        session.add_all([user, exercise])
        session.flush()

        routine = WorkoutRoutine(
            user_id=user.id,
            title="Pre-Run Dynamic Warm-up",
            routine_type="5-minute quick warm-up",
            target_sport="Running",
            difficulty_level="Beginner",
            intensity="Moderate",
            estimated_duration_min=5,
            exercises_payload=[{"exercise_id": exercise.id, "reason": "Prepares hip flexors for running"}],
        )
        session.add(routine)
        session.flush()

        schedule = ScheduledWorkout(
            user_id=user.id,
            routine_id=routine.id,
            scheduled_date=date(2026, 11, 24),
            is_rest_day=False,
            status="planned",
        )
        log = WorkoutLog(
            user_id=user.id,
            routine_id=routine.id,
            routine_title=routine.title,
            actual_duration_min=6,
            exercises_completed=[{"exercise_id": exercise.id, "completed": True}],
            perceived_effort_rpe=5,
            completion_percentage=100.0,
        )
        feedback = ExerciseFeedback(
            user_id=user.id,
            exercise_id=exercise.id,
            rating=5,
            is_excluded=False,
        )
        session.add_all([schedule, log, feedback])

    counts = get_table_counts(engine)
    assert counts["exercises"] == 1
    assert counts["workout_routines"] == 1
    assert counts["scheduled_workouts"] == 1
    assert counts["workout_logs"] == 1
    assert counts["exercise_feedback"] == 1


def test_config_domain_constants_present() -> None:
    """Core sports, categories, and safety notice must be configured."""
    assert "Badminton" in config.SUPPORTED_SPORTS
    assert "Football" in config.SUPPORTED_SPORTS
    assert len(config.EXERCISE_CATEGORIES) == 8
    assert "not a medical service" in config.SAFETY_DISCLAIMER.lower()
