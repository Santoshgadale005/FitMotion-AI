"""Recovery and cooldown exercise definitions for FitMotion AI."""

from __future__ import annotations

from typing import Any

RECOVERY_EXERCISES: list[dict[str, Any]] = [
    {
        "id": "rec-light-walking",
        "name": "Light Recovery Walking",
        "category": "Recovery and Cooldown",
        "description": "Easy-paced walking to gradually lower heart rate, promote circulation, and transition smoothly out of training.",
        "instructions": [
            "Walk at a slow, unhurried pace with relaxed shoulders and natural arm swing.",
            "Focus on lengthening your exhale gradually as your heart rate comes down.",
            "Shake out any lingering tension in your hands and jaw.",
            "Continue smoothly for the full cooldown block."
        ],
        "target_muscles": ["Lower Body", "Cardiovascular System"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 180,
        "recommended_sets": 1,
        "recommended_reps": "3-5 min easy pace",
        "rest_seconds": 10,
        "required_equipment": [],
        "safety_instructions": [
            "Keep pace relaxed—avoid sudden stops right after high-intensity cardio.",
            "Sip water gradually if needed."
        ],
        "common_mistakes": [
            "Sitting down immediately after intense exertion without tapering heart rate.",
            "Walking too fast and staying at high exertion."
        ],
        "beginner_modification": "Walk slowly around a room or march gently in place if space is limited.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Badminton", "Cricket", "Tennis", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "rec-gentle-stretching",
        "name": "Gentle Full-Body Stretching (Child's Pose & Reach)",
        "category": "Recovery and Cooldown",
        "description": "Restorative floor stretch releasing tension across the upper back, shoulders, hips, and lower back post-workout.",
        "instructions": [
            "Kneel comfortably on a mat with big toes close together and knees slightly wider than hips.",
            "Sit hips gently back toward your heels and walk your hands forward along the mat.",
            "Rest your forehead comfortably on the mat or stacked hands.",
            "Take slow, deep belly breaths, letting your shoulders and hips soften on each exhale."
        ],
        "target_muscles": ["Latissimus Dorsi", "Lower Back", "Hips", "Shoulders"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "45-60 sec relaxed hold",
        "rest_seconds": 15,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Place a folded towel behind your knees or under your hips if deep knee flexion feels tight.",
            "Keep breathing calm and unforced."
        ],
        "common_mistakes": [
            "Forcing hips down onto heels despite knee tightness.",
            "Tensing the shoulders near the ears."
        ],
        "beginner_modification": "Perform a seated forward fold in a chair resting forearms gently on thighs.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Running", "Swimming", "Football", "Basketball", "Badminton", "Cricket", "Tennis"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "rec-breathing",
        "name": "Diaphragmatic Box Breathing",
        "category": "Recovery and Cooldown",
        "description": "Paced parasympathetic breathing drill to down-regulate the nervous system and support post-training recovery.",
        "instructions": [
            "Lie comfortably on your back with knees bent (or sit upright) and place one hand on your chest and one on your belly.",
            "Inhale calmly through your nose for 4 seconds, feeling your lower ribs and belly expand gently.",
            "Hold gently for 4 seconds without straining.",
            "Exhale slowly for 4–6 seconds, pause softly for 4 seconds, and repeat."
        ],
        "target_muscles": ["Diaphragm", "Intercostals", "Nervous System Recovery"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 120,
        "recommended_sets": 1,
        "recommended_reps": "6-8 slow cycles",
        "rest_seconds": 10,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Never force breath holds—shorten the count to 3 seconds if you feel lightheaded.",
            "Keep shoulders completely relaxed."
        ],
        "common_mistakes": [
            "Breathing rapidly into the upper chest while shrugging shoulders.",
            "Holding breath until feeling strained."
        ],
        "beginner_modification": "Use a gentle 3-second inhale and 5-second exhale without holds.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Running", "Swimming", "Football", "Basketball", "Badminton", "Cricket", "Tennis"],
        "restriction_tags": [],
    },
    {
        "id": "rec-gentle-mobility",
        "name": "Gentle Cat-Cow Spinal Mobility",
        "category": "Recovery and Cooldown",
        "description": "Slow, rhythmic spinal flexion and extension drill to ease stiffness across the back and pelvis on recovery days.",
        "instructions": [
            "Begin on hands and knees with wrists under shoulders and knees under hips.",
            "Inhale smoothly as you gently drop your belly, lift your chest slightly, and look softly forward.",
            "Exhale as you press the floor away, gently rounding your spine toward the ceiling and tucking your chin.",
            "Flow seamlessly with your breath for the full set."
        ],
        "target_muscles": ["Thoracic Spine", "Lumbar Spine", "Core", "Shoulders"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "8-10 breath-paced cycles",
        "rest_seconds": 15,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Move gently within a comfortable arc—avoid forcing extreme spinal arching.",
            "Pad knees with a folded mat if kneeling feels tender."
        ],
        "common_mistakes": [
            "Rushing reps disconnected from breathing.",
            "Cranking the neck backward aggressively."
        ],
        "beginner_modification": "Perform seated cat-cow spinal waves with hands resting on your knees.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Running", "Swimming", "Football", "Basketball", "Badminton", "Cricket", "Tennis"],
        "restriction_tags": ["wrist_load"],
    },
    {
        "id": "rec-low-cycling",
        "name": "Low-Intensity Recovery Cycling",
        "category": "Recovery and Cooldown",
        "description": "Very light resistance spinning to flush legs gently after demanding field, court, or running workouts.",
        "instructions": [
            "Set the stationary bike to very low resistance so pedals spin effortlessly.",
            "Maintain a relaxed cadence (65–80 RPM) with upright, easy posture.",
            "Keep effort strictly light (Zone 1—effortless conversation).",
            "Finish smoothly without sprinting."
        ],
        "target_muscles": ["Quadriceps", "Hamstrings", "Calves", "Cardiovascular Recovery"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 300,
        "recommended_sets": 1,
        "recommended_reps": "5-10 min easy spin",
        "rest_seconds": 15,
        "required_equipment": ["Stationary Bike"],
        "safety_instructions": [
            "Keep resistance genuinely light—this session is meant to refresh, not fatigue.",
            "Stop if you feel knee discomfort."
        ],
        "common_mistakes": [
            "Increasing resistance too much and turning recovery into a workout.",
            "Slumping heavily over the handlebars."
        ],
        "beginner_modification": "Substitute with 5 minutes of easy flat walking if no bike is available.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Cricket", "Badminton", "Tennis", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
]
