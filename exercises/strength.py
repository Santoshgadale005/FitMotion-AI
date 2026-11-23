"""Strength training exercise definitions for FitMotion AI."""

from __future__ import annotations

from typing import Any

STRENGTH_EXERCISES: list[dict[str, Any]] = [
    {
        "id": "st-squats",
        "name": "Bodyweight Squats",
        "category": "Strength Training",
        "description": "Foundational lower-body compound movement building quadriceps, glute, and core strength with zero required equipment.",
        "instructions": [
            "Stand with feet shoulder-width apart and toes turned slightly outward.",
            "Brace your core, keep your chest proud, and sit your hips back and down as if lowering onto a chair.",
            "Lower until thighs are comfortable (up to parallel) while keeping heels flat and knees tracking over toes.",
            "Drive steadily through your midfoot and heels to stand tall."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Hamstrings", "Core"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "12-15",
        "rest_seconds": 45,
        "required_equipment": [],
        "safety_instructions": [
            "Keep your entire foot grounded and avoid letting knees collapse inward.",
            "Maintain a neutral spine rather than rounding the lower back at the bottom."
        ],
        "common_mistakes": [
            "Rising onto the toes as you descend.",
            "Rushing repetitions without controlling the descent."
        ],
        "beginner_modification": "Perform sit-to-stand squats tapping a sturdy chair behind you.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Basketball", "Badminton", "Running", "Cricket", "Tennis", "Swimming", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "st-lunges",
        "name": "Reverse Lunges",
        "category": "Strength Training",
        "description": "Unilateral lower-body strength exercise developing single-leg stability, glute power, and hip control.",
        "instructions": [
            "Stand tall with feet hip-width apart and core lightly braced.",
            "Step one foot cleanly backward onto the ball of your foot and lower your back knee toward the floor with control.",
            "Keep your front shin relatively vertical and torso tall.",
            "Push strongly through your front heel to bring your back foot forward and alternate sides."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Hamstrings", "Core Stabilizers"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 75,
        "recommended_sets": 3,
        "recommended_reps": "10 per leg",
        "rest_seconds": 45,
        "required_equipment": [],
        "safety_instructions": [
            "Step back with hip-width spacing (like train tracks, not a tightrope) for balance.",
            "Lower slowly so the back knee never strikes the floor hard."
        ],
        "common_mistakes": [
            "Stepping directly behind the front foot and wobbling sideways.",
            "Letting the front knee collapse inward."
        ],
        "beginner_modification": "Use a smaller depth or rest one hand lightly on a wall for balance.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Football", "Tennis", "Basketball", "Running", "Cricket", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "st-pushups",
        "name": "Push-ups",
        "category": "Strength Training",
        "description": "Classic upper-body pushing and anterior core strength exercise scalable for every fitness level.",
        "instructions": [
            "Start in a high plank with hands slightly wider than shoulders and body forming a straight line from head to heels.",
            "Brace your core and glutes, then lower your chest smoothly toward the floor with elbows angled roughly 45 degrees from your ribs.",
            "Pause briefly just above the floor without letting your hips sag.",
            "Press evenly through both palms back to full extension."
        ],
        "target_muscles": ["Chest", "Triceps", "Anterior Deltoids", "Core"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "8-15",
        "rest_seconds": 50,
        "required_equipment": [],
        "safety_instructions": [
            "Maintain a neutral neck—look slightly ahead of your fingertips rather than craning upward.",
            "Stop the set if your lower back begins to sag."
        ],
        "common_mistakes": [
            "Flaring elbows straight out to 90 degrees.",
            "Dropping the hips before the chest descends."
        ],
        "beginner_modification": "Perform incline push-ups with hands elevated on a sturdy bench, desk, or wall.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Basketball", "Cricket", "Tennis", "Badminton", "Football", "General Fitness"],
        "restriction_tags": ["wrist_load"],
    },
    {
        "id": "st-pullups",
        "name": "Pull-ups",
        "category": "Strength Training",
        "description": "Compound vertical pulling exercise strengthening the lats, upper back, grip, and shoulder stability.",
        "instructions": [
            "Grip an overhead pull-up bar slightly wider than shoulder width with palms facing away.",
            "Engage your shoulder blades downward before bending your elbows.",
            "Pull your chest smoothly toward the bar while keeping ribs tucked and legs steady.",
            "Lower back to a controlled dead hang over 2–3 seconds."
        ],
        "target_muscles": ["Latissimus Dorsi", "Upper Back", "Biceps", "Forearms", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "5-10",
        "rest_seconds": 75,
        "required_equipment": ["Pull-up Bar"],
        "safety_instructions": [
            "Avoid kipping or jerking your neck over the bar.",
            "Ensure the pull-up bar is securely anchored before hanging."
        ],
        "common_mistakes": [
            "Half-reps that skip the bottom or top range of motion.",
            "Shrugging shoulders upward at the top of the pull."
        ],
        "beginner_modification": "Use a resistance band loop for assistance or perform slow 4-second eccentric lowers.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Basketball", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": ["overhead"],
    },
    {
        "id": "st-planks",
        "name": "Forearm Plank",
        "category": "Strength Training",
        "description": "Isometric trunk stability exercise training anti-extension core strength essential for every sport.",
        "instructions": [
            "Place forearms on a mat with elbows directly beneath your shoulders.",
            "Extend legs straight back onto your toes and lift your hips into a level straight line.",
            "Gently squeeze glutes, press forearms into the floor, and keep breathing steadily.",
            "Hold cleanly for the target duration without letting hips drop or pike."
        ],
        "target_muscles": ["Transverse Abdominis", "Rectus Abdominis", "Obliques", "Shoulders", "Glutes"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 45,
        "recommended_sets": 3,
        "recommended_reps": "30-45 sec hold",
        "rest_seconds": 35,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "End the hold as soon as your lower back begins to sag or feel strained.",
            "Avoid holding your breath during isometric holds."
        ],
        "common_mistakes": [
            "Letting hips droop toward the floor.",
            "Piking hips high into a triangle."
        ],
        "beginner_modification": "Drop knees gently to the mat while maintaining a straight torso line from head to knees.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Swimming", "Football", "Basketball", "Badminton", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "st-glute-bridges",
        "name": "Glute Bridges",
        "category": "Strength Training",
        "description": "Posterior-chain hip extension exercise that strengthens glutes and hamstrings with minimal lower-back stress.",
        "instructions": [
            "Lie on your back with knees bent, feet flat on the floor hip-width apart, and arms relaxed at your sides.",
            "Brace your core lightly and drive evenly through both heels to lift your hips until shoulders, hips, and knees align.",
            "Squeeze your glutes for 1–2 seconds at the top without hyperextending your lower back.",
            "Lower smoothly back to the mat and repeat."
        ],
        "target_muscles": ["Glutes", "Hamstrings", "Core"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "12-15",
        "rest_seconds": 40,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Lift using hip extension rather than overarching your lower back.",
            "Keep knees aligned with hips rather than collapsing inward."
        ],
        "common_mistakes": [
            "Pushing hips excessively high into lumbar hyperextension.",
            "Placing feet too far away, causing hamstring cramping."
        ],
        "beginner_modification": "Perform shorter-range lifts with a slower 2-second pause at the top.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Badminton", "Cricket", "Tennis", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "st-calf-raises",
        "name": "Standing Calf Raises",
        "category": "Strength Training",
        "description": "Lower-leg strength builder improving ankle stiffness, sprint propulsion, and jumping resilience.",
        "instructions": [
            "Stand tall with feet hip-width apart near a wall or chair for light fingertip balance.",
            "Rise smoothly onto the balls of your feet as high as comfortable, keeping weight centered over your first and second toes.",
            "Pause for 1 second at the top.",
            "Lower heels back down slowly over 2–3 seconds."
        ],
        "target_muscles": ["Gastrocnemius", "Soleus", "Ankle Stabilizers"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 50,
        "recommended_sets": 3,
        "recommended_reps": "15-20",
        "rest_seconds": 35,
        "required_equipment": [],
        "safety_instructions": [
            "Control the downward phase—do not bounce quickly at the bottom.",
            "Keep ankles straight rather than rolling outward."
        ],
        "common_mistakes": [
            "Bouncing rapidly through partial reps.",
            "Rolling weight onto the outer edges of the feet."
        ],
        "beginner_modification": "Perform seated calf raises or hold firmly onto a wall while doing smaller lifts.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Basketball", "Badminton", "Tennis", "Football", "Cricket", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "st-deadlifts",
        "name": "Romanian Deadlifts (Dumbbell)",
        "category": "Strength Training",
        "description": "Hip-hinge posterior-chain strength exercise developing hamstring strength, glute power, and spinal bracing.",
        "instructions": [
            "Stand tall with feet hip-width apart holding dumbbells lightly in front of your thighs.",
            "Soften your knees slightly, brace your core, and push your hips straight backward while keeping the weights close to your legs.",
            "Lower until you feel a strong, controlled hamstring stretch (typically mid-shin level) with a completely flat back.",
            "Drive hips forward by squeezing glutes to return to a tall standing posture."
        ],
        "target_muscles": ["Hamstrings", "Glutes", "Erector Spinae", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 75,
        "recommended_sets": 3,
        "recommended_reps": "10-12",
        "rest_seconds": 60,
        "required_equipment": ["Dumbbells"],
        "safety_instructions": [
            "Keep your spine completely neutral—stop descending the moment your lower back starts to round.",
            "Start with light weights until hip-hinge mechanics feel automatic."
        ],
        "common_mistakes": [
            "Turning the movement into a squat by bending knees too much.",
            "Letting weights drift forward away from the shins."
        ],
        "beginner_modification": "Practice bodyweight hip hinges with hands on hips or using a light broomstick along the back.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Running", "Basketball", "Cricket", "Tennis", "Badminton", "General Fitness"],
        "restriction_tags": ["lower_back_load"],
    },
]
