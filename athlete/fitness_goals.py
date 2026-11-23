"""Fitness goal metadata and physical restriction taxonomy for FitMotion AI."""

from __future__ import annotations

from typing import Any

GOAL_CONFIG: dict[str, dict[str, Any]] = {
    "Improve flexibility": {
        "primary_categories": ["Stretching and Flexibility", "Mobility", "Recovery and Cooldown"],
        "secondary_categories": ["Warm-up"],
        "focus_summary": "Prioritizes static stretching, controlled joint range-of-motion drills, and relaxed breathing.",
    },
    "Improve mobility": {
        "primary_categories": ["Mobility", "Stretching and Flexibility", "Warm-up"],
        "secondary_categories": ["Balance and Stability", "Recovery and Cooldown"],
        "focus_summary": "Targets hip, ankle, thoracic, wrist, and shoulder mobility with active end-range control.",
    },
    "Build strength": {
        "primary_categories": ["Strength Training", "Sport-Specific Conditioning", "Balance and Stability"],
        "secondary_categories": ["Warm-up", "Recovery and Cooldown"],
        "focus_summary": "Focuses on progressive compound and unilateral strength with dynamic prep and cooldown.",
    },
    "Improve endurance": {
        "primary_categories": ["Cardiovascular Training", "Sport-Specific Conditioning", "Strength Training"],
        "secondary_categories": ["Warm-up", "Recovery and Cooldown"],
        "focus_summary": "Balances sustained aerobic stamina, muscular endurance, and structured interval work.",
    },
    "Improve cardiovascular fitness": {
        "primary_categories": ["Cardiovascular Training", "Warm-up", "Recovery and Cooldown"],
        "secondary_categories": ["Sport-Specific Conditioning"],
        "focus_summary": "Emphasizes aerobic conditioning, heart-rate transitions, and sustainable cardio volume.",
    },
    "Improve balance": {
        "primary_categories": ["Balance and Stability", "Mobility", "Strength Training"],
        "secondary_categories": ["Warm-up", "Recovery and Cooldown"],
        "focus_summary": "Develops single-leg stability, deep-core bracing, and proprioceptive joint control.",
    },
    "Improve athletic performance": {
        "primary_categories": ["Sport-Specific Conditioning", "Warm-up", "Strength Training", "Balance and Stability"],
        "secondary_categories": ["Mobility", "Cardiovascular Training", "Recovery and Cooldown"],
        "focus_summary": "Combines sport-matched agility, power, stability, and mobility aligned to your discipline.",
    },
    "General fitness and wellness": {
        "primary_categories": ["Warm-up", "Strength Training", "Cardiovascular Training", "Mobility", "Stretching and Flexibility"],
        "secondary_categories": ["Balance and Stability", "Recovery and Cooldown"],
        "focus_summary": "Well-rounded blend of strength, cardio, mobility, and flexibility for daily health.",
    },
    "Recovery and active recovery": {
        "primary_categories": ["Recovery and Cooldown", "Stretching and Flexibility", "Mobility"],
        "secondary_categories": ["Cardiovascular Training"],
        "focus_summary": "Low-strain movement, gentle mobility, breathing drills, and restorative stretching.",
    },
}

RESTRICTION_OPTIONS: dict[str, str] = {
    "Avoid high-impact jumping": "jumping",
    "Limit high-impact knee landings": "knee_impact",
    "Avoid deep knee bending / kneeling": "knee_flexion",
    "Avoid high-impact ankle drills": "ankle_impact",
    "Limit overhead shoulder loading": "overhead",
    "Avoid floor wrist-bearing pressure": "wrist_load",
    "Limit heavy lower-back hinging/rotation": "lower_back_load",
}

TAG_TO_RESTRICTION_LABEL: dict[str, str] = {v: k for k, v in RESTRICTION_OPTIONS.items()}


def parse_restriction_tags(raw_restrictions: str | None) -> set[str]:
    """Extract normalized restriction tags from comma-separated profile storage."""
    if not raw_restrictions:
        return set()
    tags: set[str] = set()
    for part in raw_restrictions.split(","):
        cleaned = part.strip()
        if cleaned in TAG_TO_RESTRICTION_LABEL:
            tags.add(cleaned)
        elif cleaned in RESTRICTION_OPTIONS:
            tags.add(RESTRICTION_OPTIONS[cleaned])
    return tags
