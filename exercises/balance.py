"""Balance and stability exercise definitions for FitMotion AI."""

from __future__ import annotations

from typing import Any

BALANCE_EXERCISES: list[dict[str, Any]] = [
    {
        "id": "bal-single-leg",
        "name": "Single-Leg Balance Hold",
        "category": "Balance and Stability",
        "description": "Foundational proprioception drill strengthening ankle stabilizers, hip control, and single-leg posture.",
        "instructions": [
            "Stand tall near a wall or chair with feet hip-width apart.",
            "Shift weight smoothly onto your right foot, keep a soft micro-bend in the standing knee, and lift your left foot slightly off the floor.",
            "Fix your gaze on a steady point ahead and keep your pelvis level.",
            "Hold steadily for the target time, then switch legs."
        ],
        "target_muscles": ["Ankle Stabilizers", "Glute Medius", "Core", "Foot Intrinsic Muscles"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "30 sec per leg",
        "rest_seconds": 15,
        "required_equipment": [],
        "safety_instructions": [
            "Stand within arm's reach of a wall or sturdy support if balance feels unsteady.",
            "Avoid locking the standing knee backward."
        ],
        "common_mistakes": [
            "Letting the opposite hip drop downward.",
            "Gripping the floor aggressively with curled toes."
        ],
        "beginner_modification": "Lightly tap the toes of the lifted foot on the floor or place fingertips on a chair.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Running", "Basketball", "Badminton", "Tennis", "Cricket", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "bal-bird-dog",
        "name": "Bird Dog",
        "category": "Balance and Stability",
        "description": "Quadruped cross-body stability drill developing lumbar control, glute activation, and diagonal core coordination.",
        "instructions": [
            "Start on hands and knees with wrists under shoulders and knees under hips.",
            "Brace your core gently so your back stays flat like a tabletop.",
            "Slowly extend your right arm straight forward and your left leg straight backward without rotating your hips.",
            "Pause for 2 seconds with controlled breathing, return cleanly, and alternate sides."
        ],
        "target_muscles": ["Core", "Glutes", "Erector Spinae", "Shoulders"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "8-10 alternating reps",
        "rest_seconds": 30,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Avoid kicking the back leg too high and overarching your lower back.",
            "Keep your neck neutral by looking down at the mat."
        ],
        "common_mistakes": [
            "Twisting the pelvis open toward the lifted leg side.",
            "Rushing extensions with momentum."
        ],
        "beginner_modification": "Extend only one leg or one arm at a time until trunk control feels rock-solid.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Running", "Cricket", "Football", "Basketball", "Badminton", "Tennis", "General Fitness"],
        "restriction_tags": ["wrist_load"],
    },
    {
        "id": "bal-dead-bug",
        "name": "Dead Bug",
        "category": "Balance and Stability",
        "description": "Supine deep-core stabilization exercise teaching rib-to-pelvis control while moving opposite limbs.",
        "instructions": [
            "Lie on your back with arms extended straight toward the ceiling and knees bent at 90 degrees over your hips.",
            "Gently press your lower back flat into the mat by engaging your deep abdominal muscles.",
            "Exhale as you slowly lower your right arm overhead and extend your left leg just above the floor.",
            "Return to center without letting your lower back arch off the mat, then switch sides."
        ],
        "target_muscles": ["Transverse Abdominis", "Rectus Abdominis", "Hip Flexors", "Obliques"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "8-10 alternating reps",
        "rest_seconds": 30,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Keep your lower back continuously anchored to the floor—shorten leg range if it lifts.",
            "Breathe out smoothly on each extension."
        ],
        "common_mistakes": [
            "Allowing a gap to form under the lower back as the leg lowers.",
            "Moving both arms and legs too quickly."
        ],
        "beginner_modification": "Keep feet closer to the floor and tap one heel down gently at a time with arms steady.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Swimming", "Football", "Basketball", "Badminton", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "bal-single-leg-squats",
        "name": "Single-Leg Box Squats",
        "category": "Balance and Stability",
        "description": "Controlled unilateral squat progression building knee tracking stability, hip strength, and athletic deceleration.",
        "instructions": [
            "Stand in front of a sturdy chair or bench with feet hip-width apart.",
            "Lift one foot slightly forward off the floor and extend arms in front for counterbalance.",
            "Slowly sit your hips back and lower with control until your glutes lightly touch the bench.",
            "Drive steadily through your standing heel to rise tall without swinging your torso."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Glute Medius", "Ankle Stabilizers", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 75,
        "recommended_sets": 3,
        "recommended_reps": "6-8 per leg",
        "rest_seconds": 50,
        "required_equipment": [],
        "safety_instructions": [
            "Keep the standing knee aligned directly over the middle toes—do not let it buckle inward.",
            "Use a higher seat surface if balance or knee control feels shaky."
        ],
        "common_mistakes": [
            "Plopping suddenly onto the chair at the bottom.",
            "Allowing the standing knee to collapse inward."
        ],
        "beginner_modification": "Keep the non-working heel resting lightly on the floor as a kickstand for partial assistance.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Basketball", "Football", "Badminton", "Tennis", "Running", "Cricket", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "bal-side-plank",
        "name": "Side Plank Stability Hold",
        "category": "Balance and Stability",
        "description": "Lateral trunk and hip stability hold strengthening obliques and glute medius for cutting and rotational balance.",
        "instructions": [
            "Lie on your side with your bottom forearm planted directly under your shoulder and legs stacked.",
            "Lift your hips off the mat so your body forms a straight diagonal line from head to ankles.",
            "Keep your top hip stacked directly over your bottom hip and neck neutral.",
            "Hold steadily while breathing smoothly, then repeat on the opposite side."
        ],
        "target_muscles": ["Obliques", "Glute Medius", "Quadratus Lumborum", "Shoulder Stabilizers"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "25-35 sec per side",
        "rest_seconds": 30,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Stack your elbow directly beneath the shoulder to avoid excess joint strain.",
            "Lower immediately if your shoulder feels pinched."
        ],
        "common_mistakes": [
            "Letting hips sag downward or rolling the chest toward the floor.",
            "Holding your breath."
        ],
        "beginner_modification": "Bend your bottom knee to 90 degrees and support from the knee instead of the ankle.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Badminton", "Tennis", "Basketball", "Cricket", "Swimming", "Running", "General Fitness"],
        "restriction_tags": [],
    },
]
