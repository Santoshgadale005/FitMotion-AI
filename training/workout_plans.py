"""Complete structured multi-day/multi-week evidence-based workout plans (One-Stop Hub)."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from exercises.exercise_database import get_exercise_by_id
from recommendation.routine_generator import save_workout_routine
from training.weekly_planner import assign_day_schedule, get_week_start

WORKOUT_PLANS: list[dict[str, Any]] = [
    {
        "id": "plan-football-fifa11-pro",
        "title": "Football — FIFA 11+ Speed, Agility & Hamstring Resilience Plan",
        "sport": "Football",
        "difficulty": "Advanced",
        "duration_weeks": 4,
        "days_per_week": 5,
        "goal": "Improve athletic performance",
        "framework": "Inspired by FIFA 11+ & NSCA Field Conditioning",
        "summary": "Balances repeated sprint ability, change-of-direction mechanics, Nordic hamstring eccentrics, Copenhagen adductor planks, and hip mobility with protected recovery days.",
        "weekly_schedule": [
            {"day": "Monday", "title": "FIFA Dynamic Prep + Acceleration & Lower Power", "intensity": "High", "duration_min": 35, "exercise_ids": ["wu-light-jogging", "wu-leg-swings", "wu-carioca-footwork", "sp-football-acceleration", "st-bulgarian-split-squat", "st-nordic-hamstring", "str-hamstring"]},
            {"day": "Tuesday", "title": "Hip Mobility, Adductor Stability & Recovery", "intensity": "Low", "duration_min": 20, "exercise_ids": ["mob-hip-drills", "mob-cossack-squat", "bal-copenhagen-plank", "str-groin", "str-hip-flexor", "rec-breathing"]},
            {"day": "Wednesday", "title": "Rest & Active Walking Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Thursday", "title": "Change-of-Direction Agility & Repeated Sprints", "intensity": "High", "duration_min": 35, "exercise_ids": ["wu-high-knees", "wu-dynamic-lunges", "sp-football-cod-shuttle", "sp-football-rsa-sprints", "st-single-leg-rdl", "str-pnf-hamstring"]},
            {"day": "Friday", "title": "Core Stability, Balance & Posterior Strength", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["wu-butt-kicks", "st-glute-bridges", "bal-single-leg", "bal-side-plank", "st-planks", "str-quadriceps", "rec-contrast-breathing-decompression"]},
            {"day": "Saturday", "title": "Pre-Match Activation & Post-Match Cooldown", "intensity": "Moderate", "duration_min": 20, "exercise_ids": ["wu-light-jogging", "wu-leg-swings", "wu-side-shuffles", "rec-light-walking", "str-calf", "str-groin"]},
            {"day": "Sunday", "title": "Full Rest & Hydration Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-badminton-bwf-court",
        "title": "Badminton — BWF 6-Corner Footwork, Lunge & Overhead Power Plan",
        "sport": "Badminton",
        "difficulty": "Intermediate",
        "duration_weeks": 4,
        "days_per_week": 5,
        "goal": "Improve athletic performance",
        "framework": "BWF Footwork & Court Conditioning Principles",
        "summary": "Develops split-step timing, explosive lateral skater bounds, deep lunge strength, wrist resilience, and overhead shoulder stability.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Court Footwork, Split-Step & Skater Bounds", "intensity": "High", "duration_min": 30, "exercise_ids": ["wu-side-shuffles", "wu-carioca-footwork", "sp-badminton-split-step", "sp-badminton-skater-bounds", "sp-badminton-lateral-lunge", "str-groin"]},
            {"day": "Tuesday", "title": "Overhead Shoulder, Wrist & Core Mobility", "intensity": "Low", "duration_min": 20, "exercise_ids": ["mob-shoulder-rotations", "mob-wrist-mobility", "mob-thoracic-rotations", "sp-swimming-band-pull-aparts", "bal-pallof-press", "str-shoulder"]},
            {"day": "Wednesday", "title": "Rest & Recovery Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Thursday", "title": "6-Corner Ghosting & Lower-Body Strength", "intensity": "High", "duration_min": 35, "exercise_ids": ["wu-high-knees", "cardio-jump-rope", "sp-badminton-six-corner-ghosting", "st-bulgarian-split-squat", "st-heavy-calf-eccentric", "str-calf"]},
            {"day": "Friday", "title": "Rotational Smash Power & Forearm Care", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["wu-arm-circles", "sp-tennis-serve-power-slams", "sp-tennis-external-rotation", "sp-tennis-forearm-eccentrics", "bal-copenhagen-plank", "str-triceps"]},
            {"day": "Saturday", "title": "Active Mobility & Flexibility Flush", "intensity": "Low", "duration_min": 15, "exercise_ids": ["mob-cossack-squat", "str-hamstring", "str-quadriceps", "rec-gentle-stretching", "rec-breathing"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-basketball-vertical-court",
        "title": "Basketball — Vertical Jump, Soft-Landing & Court Stamina Plan",
        "sport": "Basketball",
        "difficulty": "Advanced",
        "duration_weeks": 4,
        "days_per_week": 4,
        "goal": "Improve athletic performance",
        "framework": "NSCA Plyometrics & Lower-Body Force Development",
        "summary": "Combines reactive depth jumps, soft-landing mechanics, ankle dorsiflexion, defensive lateral slides, and full-body explosive strength.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Explosive Vertical Jump & Lower Strength", "intensity": "High", "duration_min": 35, "exercise_ids": ["mob-ankle-mobility", "wu-high-knees", "sp-basketball-landing", "sp-basketball-depth-jump", "st-bulgarian-split-squat", "st-heavy-calf-eccentric", "str-quadriceps"]},
            {"day": "Tuesday", "title": "Ankle, Hip & Thoracic Mobility Recovery", "intensity": "Low", "duration_min": 20, "exercise_ids": ["mob-ankle-mobility", "mob-hip-drills", "mob-overhead-squat-drill", "str-couch-stretch", "rec-contrast-breathing-decompression"]},
            {"day": "Wednesday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Thursday", "title": "Defensive Slides, Core & Full-Body Power", "intensity": "High", "duration_min": 30, "exercise_ids": ["wu-side-shuffles", "sp-basketball-defensive-slides", "sp-gym-dumbbell-thrusters", "bal-hollow-body-hold", "bal-single-leg-squats", "str-calf"]},
            {"day": "Friday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Saturday", "title": "Court Conditioning & Stability", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["cardio-double-under-rope", "st-pushups", "st-pullups", "bal-copenhagen-plank", "rec-gentle-stretching"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-cricket-rotational-endurance",
        "title": "Cricket — Rotational Power, Bowling Shoulder & Pitch-Sprint Plan",
        "sport": "Cricket",
        "difficulty": "Intermediate",
        "duration_weeks": 4,
        "days_per_week": 5,
        "goal": "Improve athletic performance",
        "framework": "NSCA Asymmetric Sport & Rotational Conditioning",
        "summary": "Balances bowling/throwing scapular health, anti-rotation Pallof core work, unilateral leg balance, and 20m between-wickets sprint conditioning.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Unilateral Leg Strength & Wicket Sprints", "intensity": "High", "duration_min": 35, "exercise_ids": ["wu-light-jogging", "wu-dynamic-lunges", "sp-cricket-between-wickets-shuttle", "st-bulgarian-split-squat", "st-single-leg-rdl", "str-hamstring"]},
            {"day": "Tuesday", "title": "Bowling Shoulder Health & Thoracic Mobility", "intensity": "Low", "duration_min": 20, "exercise_ids": ["mob-thoracic-rotations", "sp-cricket-scapular-slides", "sp-tennis-external-rotation", "sp-swimming-band-pull-aparts", "str-chest", "str-shoulder"]},
            {"day": "Wednesday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Thursday", "title": "Rotational Core Power & Anti-Rotation", "intensity": "Moderate", "duration_min": 30, "exercise_ids": ["wu-inchworm-spiderman", "sp-cricket-rotational-core", "bal-pallof-press", "sp-tennis-serve-power-slams", "bal-bird-dog", "rec-gentle-mobility"]},
            {"day": "Friday", "title": "Aerobic Stamina & Lower Endurance", "intensity": "Moderate", "duration_min": 30, "exercise_ids": ["wu-leg-swings", "cardio-tempo-threshold", "st-glute-bridges", "st-calf-raises", "rec-light-walking", "str-calf"]},
            {"day": "Saturday", "title": "Match-Ready Prehab & Stretching", "intensity": "Low", "duration_min": 15, "exercise_ids": ["wu-arm-circles", "mob-hip-drills", "str-hip-flexor", "str-groin", "rec-breathing"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-tennis-usta-complete",
        "title": "Tennis — USTA Baseline Agility, Serve Power & Shoulder Health Plan",
        "sport": "Tennis",
        "difficulty": "Intermediate",
        "duration_weeks": 4,
        "days_per_week": 4,
        "goal": "Improve athletic performance",
        "framework": "USTA Kinetic-Chain & Shoulder Prehab Guidelines",
        "summary": "Targets baseline lateral bounds, serve rotational power, rotator cuff external rotation, and forearm eccentric conditioning.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Baseline Agility & Lateral Power", "intensity": "High", "duration_min": 30, "exercise_ids": ["wu-carioca-footwork", "wu-side-shuffles", "sp-badminton-skater-bounds", "sp-badminton-lateral-lunge", "st-bulgarian-split-squat", "str-groin"]},
            {"day": "Tuesday", "title": "Serve Prehab, Forearms & Thoracic Mobility", "intensity": "Low", "duration_min": 20, "exercise_ids": ["mob-wrist-mobility", "mob-thoracic-rotations", "sp-tennis-external-rotation", "sp-tennis-forearm-eccentrics", "sp-swimming-band-pull-aparts", "str-shoulder"]},
            {"day": "Wednesday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Thursday", "title": "Rotational Serve Power & Court Cardio", "intensity": "High", "duration_min": 30, "exercise_ids": ["cardio-jump-rope", "sp-tennis-serve-power-slams", "bal-pallof-press", "st-single-leg-rdl", "bal-copenhagen-plank", "str-triceps"]},
            {"day": "Friday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Saturday", "title": "Active Mobility & Match Cooldown", "intensity": "Low", "duration_min": 20, "exercise_ids": ["mob-cossack-squat", "str-pnf-hamstring", "str-calf", "rec-contrast-breathing-decompression"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-swimming-dryland-pro",
        "title": "Swimming — Dryland Streamline Core, Catch Power & Shoulder Plan",
        "sport": "Swimming",
        "difficulty": "Intermediate",
        "duration_weeks": 4,
        "days_per_week": 5,
        "goal": "Improve endurance",
        "framework": "USA Swimming Dryland Conditioning",
        "summary": "Builds high-elbow dryland lat pull power, streamline hollow-body core tension, overhead thoracic mobility, and balanced scapular strength.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Dryland Pull Power & Streamline Core", "intensity": "Moderate", "duration_min": 30, "exercise_ids": ["wu-arm-circles", "mob-shoulder-rotations", "sp-swimming-band-pull", "st-pullups", "bal-hollow-body-hold", "bal-dead-bug", "str-chest"]},
            {"day": "Tuesday", "title": "Aerobic Lap Swimming & Thoracic Mobility", "intensity": "Moderate", "duration_min": 30, "exercise_ids": ["mob-thoracic-rotations", "sp-swimming-ytw-activation", "cardio-swimming", "str-triceps", "rec-breathing"]},
            {"day": "Wednesday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Thursday", "title": "Overhead Strength, Scapular Stability & Core", "intensity": "High", "duration_min": 30, "exercise_ids": ["wu-inchworm-spiderman", "st-pike-pushups", "sp-gym-dumbbell-row", "sp-swimming-band-pull-aparts", "st-planks", "str-shoulder"]},
            {"day": "Friday", "title": "Lower-Body Kick Power & Mobility", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["mob-ankle-mobility", "st-squats", "st-glute-bridges", "bal-bird-dog", "str-hip-flexor", "rec-gentle-mobility"]},
            {"day": "Saturday", "title": "Easy Swim Flush & Decompression", "intensity": "Low", "duration_min": 20, "exercise_ids": ["cardio-swimming", "rec-gentle-stretching", "rec-contrast-breathing-decompression"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-running-economy-endurance",
        "title": "Running — Economy, Tendon Stiffness & Endurance Strength Plan",
        "sport": "Running",
        "difficulty": "Intermediate",
        "duration_weeks": 4,
        "days_per_week": 5,
        "goal": "Improve endurance",
        "framework": "ACSM & NSCA Endurance Running Strength Standards",
        "summary": "Combines aerobic base & threshold runs with heavy-slow calf raises, pogo-hop ankle stiffness, single-leg hip stability, and targeted lower-body flexibility.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Running Mechanics + Steady Aerobic Run", "intensity": "Moderate", "duration_min": 30, "exercise_ids": ["wu-light-jogging", "wu-leg-swings", "sp-running-a-skips", "cardio-running", "rec-light-walking", "str-calf"]},
            {"day": "Tuesday", "title": "Runner's Strength & Tendon Stiffness", "intensity": "Moderate", "duration_min": 30, "exercise_ids": ["mob-ankle-mobility", "st-heavy-calf-eccentric", "sp-running-pogo-hops", "st-single-leg-rdl", "bal-single-leg-squats", "st-glute-bridges"]},
            {"day": "Wednesday", "title": "Active Mobility & Recovery Day", "intensity": "Low", "duration_min": 15, "exercise_ids": ["mob-hip-drills", "str-couch-stretch", "str-hamstring", "rec-contrast-breathing-decompression"]},
            {"day": "Thursday", "title": "Lactate-Threshold Tempo Run + Cooldown", "intensity": "High", "duration_min": 30, "exercise_ids": ["wu-high-knees", "wu-butt-kicks", "cardio-tempo-threshold", "rec-light-walking", "str-pnf-hamstring", "str-quadriceps"]},
            {"day": "Friday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Saturday", "title": "Core Stability & Unilateral Control", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["st-bulgarian-split-squat", "bal-dead-bug", "bal-side-plank", "bal-single-leg", "str-hip-flexor"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-general-beginner-home",
        "title": "General Fitness — Beginner Zero-Equipment Wellness Plan",
        "sport": "General Fitness",
        "difficulty": "Beginner",
        "duration_weeks": 4,
        "days_per_week": 4,
        "goal": "General fitness and wellness",
        "framework": "ACSM General Health & Beginner Progression",
        "summary": "Accessible, equipment-free 4-day routine blending joint mobility, foundational bodyweight strength, gentle cardio, and restorative stretching.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Full-Body Beginner Strength", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["wu-light-jogging", "wu-arm-circles", "st-squats", "st-pushups", "st-glute-bridges", "st-planks", "rec-gentle-stretching"]},
            {"day": "Tuesday", "title": "Mobility & Flexibility Flow", "intensity": "Low", "duration_min": 15, "exercise_ids": ["mob-hip-drills", "mob-thoracic-rotations", "str-hamstring", "str-hip-flexor", "str-chest", "rec-breathing"]},
            {"day": "Wednesday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Thursday", "title": "Low-Impact Cardio & Core Stability", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["wu-jumping-jacks", "cardio-low-intensity", "bal-bird-dog", "bal-dead-bug", "bal-single-leg", "str-calf"]},
            {"day": "Friday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Saturday", "title": "Lower Body & Active Recovery", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["wu-leg-swings", "st-lunges", "st-calf-raises", "st-glute-bridges", "rec-gentle-mobility", "str-quadriceps"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
    {
        "id": "plan-general-advanced-athlete",
        "title": "General Fitness — Advanced Athletic Strength & Conditioning Plan",
        "sport": "General Fitness",
        "difficulty": "Advanced",
        "duration_weeks": 4,
        "days_per_week": 5,
        "goal": "Build strength",
        "framework": "NSCA Total-Body Athletic Periodization",
        "summary": "High-output strength, unilateral power, metabolic conditioning, and elite core stability paired with dedicated mobility and decompression days.",
        "weekly_schedule": [
            {"day": "Monday", "title": "Lower-Body Strength & Posterior Chain", "intensity": "High", "duration_min": 35, "exercise_ids": ["wu-inchworm-spiderman", "st-bulgarian-split-squat", "st-nordic-hamstring", "st-single-leg-rdl", "bal-pistol-squat-progression", "str-couch-stretch"]},
            {"day": "Tuesday", "title": "Upper-Body Push/Pull & Hollow Core", "intensity": "Moderate", "duration_min": 35, "exercise_ids": ["mob-shoulder-rotations", "st-pullups", "st-pike-pushups", "sp-gym-dumbbell-row", "bal-hollow-body-hold", "str-chest"]},
            {"day": "Wednesday", "title": "Deep Mobility & Parasympathetic Reset", "intensity": "Low", "duration_min": 20, "exercise_ids": ["mob-cossack-squat", "mob-overhead-squat-drill", "str-pnf-hamstring", "rec-contrast-breathing-decompression"]},
            {"day": "Thursday", "title": "Metabolic Power & Tabata Conditioning", "intensity": "High", "duration_min": 30, "exercise_ids": ["wu-carioca-footwork", "sp-gym-dumbbell-thrusters", "sp-gym-burpee-broad-jump", "cardio-tabata-sprints", "rec-light-walking"]},
            {"day": "Friday", "title": "Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
            {"day": "Saturday", "title": "Anti-Rotation Stability & Aerobic Flush", "intensity": "Moderate", "duration_min": 25, "exercise_ids": ["cardio-double-under-rope", "bal-copenhagen-plank", "bal-pallof-press", "st-heavy-calf-eccentric", "rec-gentle-stretching"]},
            {"day": "Sunday", "title": "Full Rest Day", "intensity": "Rest", "duration_min": 0, "exercise_ids": []},
        ],
    },
]


def get_workout_plans(
    sport: str | None = None,
    difficulty: str | None = None,
) -> list[dict[str, Any]]:
    """Return structured workout plans optionally filtered by sport or difficulty."""
    results: list[dict[str, Any]] = []
    for plan in WORKOUT_PLANS:
        if sport and sport != "All" and plan["sport"] != sport:
            continue
        if difficulty and difficulty != "All" and plan["difficulty"] != difficulty:
            continue
        results.append(plan)
    return results


def apply_workout_plan_to_week(
    user_id: int,
    plan_id: str,
    week_start: date | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> tuple[bool, str]:
    """Save each active day of a structured workout plan and assign it to the user's 7-day week."""
    plan = next((p for p in WORKOUT_PLANS if p["id"] == plan_id), None)
    if plan is None:
        return False, "Workout plan not found."

    start = get_week_start(week_start)
    for offset, day_spec in enumerate(plan["weekly_schedule"]):
        target_date = start + timedelta(days=offset)
        if day_spec["intensity"] == "Rest" or not day_spec["exercise_ids"]:
            assign_day_schedule(
                user_id=user_id,
                scheduled_date=target_date,
                is_rest_day=True,
                status="planned",
                notes=f"{plan['title']} — {day_spec['title']}",
                session_factory=session_factory,
            )
            continue

        resolved_exercises: list[dict[str, Any]] = []
        for ex_id in day_spec["exercise_ids"]:
            ex = get_exercise_by_id(ex_id, session_factory=session_factory)
            if ex is not None:
                entry = dict(ex)
                entry["prescribed_sets"] = ex["recommended_sets"]
                entry["prescribed_reps"] = ex["recommended_reps"]
                entry["prescribed_rest_sec"] = ex["rest_seconds"]
                entry["estimated_block_sec"] = ex["default_duration_sec"]
                entry["explanation"] = f"Part of {plan['title']} ({plan['framework']})."
                resolved_exercises.append(entry)

        routine_dict = {
            "title": f"{plan['sport']}: {day_spec['title']}",
            "routine_type": "Sport-specific conditioning routine" if plan["sport"] != "General Fitness" else "Custom personalized routine",
            "target_sport": plan["sport"],
            "difficulty_level": plan["difficulty"],
            "intensity": day_spec["intensity"],
            "estimated_duration_min": day_spec["duration_min"] or 20,
            "exercises": resolved_exercises,
        }
        routine_id = save_workout_routine(
            user_id=user_id,
            routine=routine_dict,
            is_favorite=False,
            session_factory=session_factory,
        )
        assign_day_schedule(
            user_id=user_id,
            scheduled_date=target_date,
            routine_id=routine_id,
            is_rest_day=False,
            status="planned",
            notes=f"From plan: {plan['title']}",
            session_factory=session_factory,
        )

    return True, f"Applied **{plan['title']}** to your Weekly Training Planner starting {start.strftime('%b %d, %Y')}!"
