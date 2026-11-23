"""AI Training Assistant grounded in FitMotion AI's exercise DB & recommendation engine.

Features:
1. Strict medical/pain/injury safety guardrail (never diagnoses or prescribes rehab).
2. Natural-language intent extraction (sport, duration, category, equipment, level).
3. Direct integration with `recommend_exercises`, `generate_workout_routine`, and `sports.json`.
4. Optional external LLM conversational refinement (via `.env` keys) with seamless
   deterministic offline fallback whenever no API key is configured or reachable.
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

import config
from exercises.exercise_database import load_sport_profiles
from recommendation.routine_generator import generate_workout_routine

MEDICAL_SAFETY_KEYWORDS: tuple[str, ...] = (
    "injury",
    "injured",
    "sharp pain",
    "chest pain",
    "swollen",
    "swelling",
    "sprain",
    "fracture",
    "broken",
    "torn",
    "tear",
    "dizzy",
    "dizziness",
    "faint",
    "diagnose",
    "diagnosis",
    "medical",
    "numbness",
    "tingling",
    "hurts",
    "painful",
    "severe pain",
)

DURATION_REGEX = re.compile(r"(\d{1,2})\s*(?:min|mins|minute|minutes|-minute)", re.IGNORECASE)


def _detect_medical_concern(question: str) -> bool:
    """Return True if the user describes pain, injury, or medical symptoms."""
    lower = question.lower()
    return any(kw in lower for kw in MEDICAL_SAFETY_KEYWORDS)


def _parse_query_intent(question: str, profile: dict[str, Any]) -> dict[str, Any]:
    """Extract structured intent (sport, duration, routine_type, equipment, level) from text."""
    q = question.lower()

    # 1. Sport detection
    detected_sport = profile.get("primary_sport", "General Fitness")
    for sport in config.SUPPORTED_SPORTS:
        if sport.lower() in q:
            detected_sport = sport
            break
    if "soccer" in q:
        detected_sport = "Football"
    if "run" in q or "running" in q or "jog" in q:
        detected_sport = "Running"
    if "swim" in q:
        detected_sport = "Swimming"

    # 2. Duration detection
    match = DURATION_REGEX.search(q)
    detected_duration = int(match.group(1)) if match else None
    if detected_duration is not None:
        detected_duration = max(5, min(90, detected_duration))

    # 3. Equipment override detection
    no_equipment = any(
        phrase in q
        for phrase in ("without gym", "no equipment", "bodyweight", "at home", "without equipment")
    )

    # 4. Experience override detection
    difficulty_override: str | None = None
    if "beginner" in q:
        difficulty_override = "Beginner"
    elif "advanced" in q:
        difficulty_override = "Advanced"
    elif "intermediate" in q:
        difficulty_override = "Intermediate"

    # 5. Routine / topic intent detection
    routine_type = "Custom personalized routine"
    categories: list[str] | None = None

    if any(w in q for w in ("before playing", "warm-up", "warmup", "warm up", "pre-match", "pre-game", "before badminton", "before football", "before running")):
        routine_type = "Pre-sports warm-up" if detected_sport != "General Fitness" else "5-minute quick warm-up"
        detected_duration = detected_duration or 10
    elif any(w in q for w in ("cooldown", "cool down", "cool-down", "after running", "after playing", "after workout", "post-workout")):
        routine_type = "Post-workout cooldown"
        detected_duration = detected_duration or 10
    elif any(w in q for w in ("recovery", "rest day", "sore", "active recovery")):
        routine_type = "Recovery-focused routine"
        detected_duration = detected_duration or 15
    elif "flexibility" in q or "stretch" in q or "stretching" in q:
        routine_type = "15-minute flexibility routine"
        detected_duration = detected_duration or 15
    elif "mobility" in q:
        routine_type = "10-minute mobility routine"
        detected_duration = detected_duration or 15
    elif "strength" in q or "stronger" in q or "muscle" in q:
        routine_type = "30-minute strength routine"
        detected_duration = detected_duration or 25
    elif "balance" in q or "stability" in q or "core" in q:
        categories = ["Balance and Stability", "Mobility", "Strength Training"]
        detected_duration = detected_duration or 15
    elif "cardio" in q or "endurance" in q or "stamina" in q:
        categories = ["Warm-up", "Cardiovascular Training", "Recovery and Cooldown"]
        detected_duration = detected_duration or 20
    elif no_equipment:
        routine_type = "20-minute full-body workout"
        detected_duration = detected_duration or 20
    elif detected_sport != "General Fitness":
        routine_type = "Sport-specific conditioning routine"
        detected_duration = detected_duration or 20

    return {
        "sport": detected_sport,
        "duration_min": detected_duration or int(profile.get("available_duration_min", 20)),
        "routine_type": routine_type,
        "categories": categories,
        "no_equipment": no_equipment,
        "difficulty": difficulty_override or profile.get("experience_level", "Beginner"),
    }


def _try_optional_llm_polish(question: str, grounded_answer: str) -> tuple[str, str]:
    """Optionally polish the grounded answer via OpenAI if configured in `.env`.

    Always falls back cleanly to the deterministic grounded answer if no API key
    is set or if any network/API error occurs.
    """
    provider = config.LLM_PROVIDER.strip().lower()
    if provider == "openai" and config.OPENAI_API_KEY:
        try:
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are FitMotion AI's wellness assistant. Present the provided grounded "
                            "exercise recommendations clearly and encouragingly. Never invent exercises "
                            "outside the provided list and never give medical diagnoses."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"User question: {question}\n\nGrounded recommendation data:\n{grounded_answer}",
                    },
                ],
                "temperature": 0.3,
                "max_tokens": 550,
            }
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {config.OPENAI_API_KEY}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                content = body["choices"][0]["message"]["content"].strip()
                if content:
                    return content, "LLM + FitMotion Engine"
        except Exception:
            pass

    return grounded_answer, "FitMotion Local Engine (Offline-Ready)"


def answer_training_question(
    question: str,
    profile: dict[str, Any],
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any]:
    """Generate a safe, exercise-database-grounded answer to a user's fitness question."""
    clean_q = question.strip()
    if not clean_q:
        return {
            "answer": "Ask me anything about warm-ups, mobility, flexibility, equipment-free workouts, cooldowns, or sport-specific conditioning!",
            "mode": "FitMotion Local Engine (Offline-Ready)",
            "safety_triggered": False,
            "suggested_routine": None,
        }

    # 1. Mandatory safety check for injuries, pain, or medical concerns
    if _detect_medical_concern(clean_q):
        safety_reply = (
            "### Health & Safety Guidance\n\n"
            "It sounds like you may be experiencing **pain, an injury, or a medical symptom**. "
            "FitMotion AI is a general fitness and exercise recommendation tool—not a medical application—and "
            "cannot diagnose injuries or prescribe rehabilitation exercises.\n\n"
            "**Recommended next steps:**\n"
            "- Pause any movement that triggers sharp pain, swelling, dizziness, or discomfort.\n"
            "- Consult a qualified **physician, sports medicine specialist, or licensed physiotherapist** for an individual assessment.\n"
            "- Once cleared to train, you can add movement restrictions or exclude specific exercises in your **Athlete Profile** so FitMotion AI automatically avoids them."
        )
        return {
            "answer": safety_reply,
            "mode": "Safety Guardrail",
            "safety_triggered": True,
            "suggested_routine": None,
        }

    # 2. Extract intent and run FitMotion AI's recommendation & routine engine
    intent = _parse_query_intent(clean_q, profile)
    query_profile = dict(profile)
    query_profile["primary_sport"] = intent["sport"]
    query_profile["experience_level"] = intent["difficulty"]
    if intent["no_equipment"]:
        query_profile["available_equipment"] = []

    routine = generate_workout_routine(
        profile=query_profile,
        routine_type=intent["routine_type"],
        duration_min=intent["duration_min"],
        difficulty=intent["difficulty"],
        selected_categories=intent["categories"],
        available_equipment=[] if intent["no_equipment"] else query_profile.get("available_equipment", []),
        session_factory=session_factory,
    )

    sport_profiles = load_sport_profiles()
    sport_meta = sport_profiles.get(intent["sport"], sport_profiles["General Fitness"])

    lines: list[str] = [
        f"### {routine['title']}",
        f"**Tailored for:** {intent['sport']} · **{intent['difficulty']}** level · **~{routine['estimated_duration_min']} min** ({routine['intensity']} intensity)",
        "",
    ]

    if "warm-up" in intent["routine_type"].lower():
        lines.append(f"**{intent['sport']} Warm-up Focus:** {sport_meta['warmup_focus']}")
    elif "cooldown" in intent["routine_type"].lower() or "recovery" in intent["routine_type"].lower():
        lines.append(f"**{intent['sport']} Recovery Focus:** {sport_meta['recovery_focus']}")
    else:
        lines.append(f"**Coaching Focus:** {sport_meta['summary']}")

    lines.append("")
    if not routine["exercises"]:
        lines.append(
            "No exercises matched all current filters and restrictions. Try adjusting your equipment or excluded exercises in your Athlete Profile."
        )
    else:
        lines.append("#### Recommended Sequence")
        for idx, ex in enumerate(routine["exercises"], start=1):
            equip_note = "No gym equipment" if not [e for e in ex["required_equipment"] if e.lower() != "yoga mat"] else ", ".join(ex["required_equipment"])
            lines.append(
                f"{idx}. **{ex['name']}** *({ex['category']})* — "
                f"**{ex['prescribed_sets']} sets × {ex['prescribed_reps']}** · Rest {ex['prescribed_rest_sec']}s · _{equip_note}_\n"
                f"   - *Why selected:* {ex['explanation']}\n"
                f"   - *Safety cue:* {ex['safety_instructions'][0] if ex['safety_instructions'] else 'Move with controlled form.'}"
            )

    lines.append("")
    lines.append(
        "_Tip: You can save this routine directly to your library or schedule it in the Weekly Training Planner. Stop if any exercise feels uncomfortable._"
    )

    grounded_text = "\n".join(lines)
    final_answer, mode = _try_optional_llm_polish(clean_q, grounded_text)

    return {
        "answer": final_answer,
        "mode": mode,
        "safety_triggered": False,
        "suggested_routine": routine,
    }
