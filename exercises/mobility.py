"""Mobility training exercise definitions for FitMotion AI."""

from __future__ import annotations

from typing import Any

MOBILITY_EXERCISES: list[dict[str, Any]] = [
    {
        "id": "mob-hip-drills",
        "name": "Hip Mobility Drills (90/90 Transitions)",
        "category": "Mobility",
        "description": "Seated internal and external hip rotation transitions designed to improve hip joint range of motion and athletic pivoting.",
        "instructions": [
            "Sit on a mat with your front leg bent at 90 degrees in front of you and your back leg bent at 90 degrees to the side.",
            "Keep your chest tall and place hands lightly behind you for support if needed.",
            "Slowly lift both knees and rotate smoothly across center until legs settle in the 90/90 position on the opposite side.",
            "Pause briefly on each side before transitioning back with control."
        ],
        "target_muscles": ["Hip Rotators", "Glutes", "Hip Flexors", "Adductors"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "8-10 slow transitions",
        "rest_seconds": 20,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Move slowly and stop short of any pinching sensation in the hip or knee.",
            "Keep both heels grounded as pivot points."
        ],
        "common_mistakes": [
            "Slumping the lower back aggressively to force the knee down.",
            "Rushing transitions instead of controlling internal hip rotation."
        ],
        "beginner_modification": "Sit on a folded towel or lean slightly back on both hands to reduce hip tightness.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Running", "Badminton", "Basketball", "Tennis", "Cricket", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "mob-ankle-mobility",
        "name": "Ankle Mobility (Knee-to-Wall Dorsiflexion)",
        "category": "Mobility",
        "description": "Targeted ankle dorsiflexion drill that improves squat depth, sprint push-off mechanics, and landing absorption.",
        "instructions": [
            "Adopt a half-kneeling stance facing a wall with your front toes placed 6–10 cm from the wall.",
            "Keeping your entire front heel glued to the floor, gently drive your knee forward toward the wall over your middle toes.",
            "Hold the end range for 2 seconds while feeling a gentle stretch at the back of the ankle.",
            "Return smoothly and repeat before switching ankles."
        ],
        "target_muscles": ["Soleus", "Achilles Complex", "Ankle Stabilizers"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "10-12 per ankle",
        "rest_seconds": 15,
        "required_equipment": [],
        "safety_instructions": [
            "Do not force forward motion if you feel sharp pinching at the front of the ankle.",
            "Keep your front heel firmly planted on the floor throughout."
        ],
        "common_mistakes": [
            "Allowing the heel to lift off the floor to reach the wall.",
            "Letting the knee cave inward instead of tracking over the toes."
        ],
        "beginner_modification": "Place your toes closer to the wall and perform smaller controlled rocks.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Basketball", "Running", "Football", "Badminton", "Tennis", "Cricket", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "mob-shoulder-rotations",
        "name": "Shoulder Rotations (Controlled Articular Rotations)",
        "category": "Mobility",
        "description": "Slow, controlled full-range circular shoulder rotations to build overhead control and scapular awareness.",
        "instructions": [
            "Stand tall with core lightly braced and one arm at your side, thumb pointing forward.",
            "Slowly raise your arm straight up overhead as far as comfortable without arching your lower back.",
            "At the top, gently rotate your palm outward and sweep your arm slowly behind you in a wide arc.",
            "Reverse the arc smoothly and repeat on the opposite arm."
        ],
        "target_muscles": ["Rotator Cuff", "Deltoids", "Scapular Stabilizers"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "5 slow reps per arm",
        "rest_seconds": 15,
        "required_equipment": [],
        "safety_instructions": [
            "Keep the motion slow and strictly pain-free; bypass any clicking or pinching angle with a smaller arc.",
            "Avoid twisting your torso to fake extra shoulder motion."
        ],
        "common_mistakes": [
            "Flaring the ribcage and arching the lower back overhead.",
            "Moving too quickly through sticky spots."
        ],
        "beginner_modification": "Perform smaller circles with a softly bent elbow.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Badminton", "Tennis", "Cricket", "Basketball", "General Fitness"],
        "restriction_tags": ["overhead"],
    },
    {
        "id": "mob-thoracic-rotations",
        "name": "Thoracic Rotations (Open Book)",
        "category": "Mobility",
        "description": "Side-lying upper-back rotation drill that restores thoracic spine mobility for overhead, throwing, and rotational sports.",
        "instructions": [
            "Lie on your side with knees bent at 90 degrees stacked in front of your hips and both arms extended straight ahead.",
            "Keep your knees pinned together on the floor (or resting on a cushion).",
            "Inhale, then exhale as you sweep your top arm across your chest and open toward the opposite floor, following your hand with your eyes.",
            "Hold briefly with a relaxed breath, then close smoothly and repeat on both sides."
        ],
        "target_muscles": ["Thoracic Spine", "Chest", "Obliques", "Upper Back"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "8 slow reps per side",
        "rest_seconds": 15,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Allow your top arm to hover naturally rather than forcing your shoulder blade flat onto the floor.",
            "Stop if you notice tingling in the arm or sharp spinal pain."
        ],
        "common_mistakes": [
            "Letting the top knee lift off the bottom knee, turning it into a lower-back twist.",
            "Holding the breath during rotation."
        ],
        "beginner_modification": "Place your top hand behind your ear instead of extending the full arm to reduce shoulder strain.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Cricket", "Tennis", "Badminton", "Basketball", "Running", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "mob-wrist-mobility",
        "name": "Wrist Mobility Drills",
        "category": "Mobility",
        "description": "Gentle multi-angle wrist flexion, extension, and circular mobilization ideal for racquet sports and floor-based training.",
        "instructions": [
            "Start on hands and knees with shoulders stacked above wrists and fingers spread comfortably.",
            "Gently rock your shoulders forward and backward in small circles to load wrist extension gradually.",
            "Turn fingertips slightly outward and sway gently side to side.",
            "Finish seated with slow figure-8 wrist rotations in the air."
        ],
        "target_muscles": ["Forearm Flexors", "Forearm Extensors", "Wrist Stabilizers"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 50,
        "recommended_sets": 2,
        "recommended_reps": "10 gentle rocks + 10 circles",
        "rest_seconds": 15,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Keep pressure light and stay well below any sharp wrist discomfort.",
            "Avoid locking elbows forcefully."
        ],
        "common_mistakes": [
            "Shifting too much body weight over stiff wrists too quickly.",
            "Lifting the base of the knuckles off the floor."
        ],
        "beginner_modification": "Perform wrist stretches seated by gently guiding one hand with the other without floor weight.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Tennis", "Cricket", "Basketball", "General Fitness"],
        "restriction_tags": ["wrist_load"],
    },
    {
        "id": "mob-deep-squat",
        "name": "Deep Squat Mobility Hold",
        "category": "Mobility",
        "description": "Assisted or bodyweight deep squat hold with gentle knee pry to open ankles, hips, and thoracic posture simultaneously.",
        "instructions": [
            "Stand with feet slightly wider than shoulder width and toes turned slightly outward.",
            "Lower smoothly into as deep a squat as you can maintain while keeping both heels flat on the ground.",
            "Place elbows gently inside your knees to maintain knee alignment and lift your chest tall.",
            "Shift weight softly side to side while breathing steadily."
        ],
        "target_muscles": ["Hips", "Ankles", "Adductors", "Thoracic Spine", "Glutes"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "30-45 sec hold",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Do not force depth if your knees or lower back feel compressed.",
            "Use heel elevation or hand support if heels lift."
        ],
        "common_mistakes": [
            "Rolling onto the toes with heels off the ground.",
            "Collapsing the chest completely downward onto the thighs."
        ],
        "beginner_modification": "Hold onto a sturdy doorframe or elevate heels on a rolled towel.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Basketball", "Badminton", "Running", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
]
