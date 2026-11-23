"""Stretching and flexibility exercise definitions for FitMotion AI."""

from __future__ import annotations

from typing import Any

STRETCHING_EXERCISES: list[dict[str, Any]] = [
    {
        "id": "str-hamstring",
        "name": "Hamstring Stretch",
        "category": "Stretching and Flexibility",
        "description": "Gentle seated or standing posterior-thigh stretch to relieve hamstring tightness after running or lower-body workouts.",
        "instructions": [
            "Sit tall on a mat with your right leg extended forward and your left foot resting against your inner right thigh.",
            "Keep your spine long and hinge gently forward from the hips rather than rounding your back.",
            "Stop when you feel a mild, comfortable tension along the back of the extended thigh.",
            "Hold steady with slow exhalations, then switch sides."
        ],
        "target_muscles": ["Hamstrings", "Calves"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "30 sec per side",
        "rest_seconds": 10,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Stretch to mild tension only—never push into sharp pulling behind the knee.",
            "Keep a micro-bend in the extended knee if hamstrings are very tight."
        ],
        "common_mistakes": [
            "Rounding the upper back aggressively to grab the toes.",
            "Bouncing into the stretch."
        ],
        "beginner_modification": "Loop a towel around your foot or bend the extended knee slightly while hinging.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Badminton", "Basketball", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "str-quadriceps",
        "name": "Quadriceps Stretch",
        "category": "Stretching and Flexibility",
        "description": "Standing or side-lying front-thigh stretch that eases quadriceps tension from jumping, squatting, and sprinting.",
        "instructions": [
            "Stand tall near a wall or chair with one hand resting lightly on it for balance.",
            "Bend your right knee and gently hold your right ankle or foot behind you.",
            "Keep both knees close together and tuck your tailbone slightly to avoid arching your lower back.",
            "Hold steadily while breathing calmly, then switch legs."
        ],
        "target_muscles": ["Quadriceps", "Hip Flexors"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "30 sec per side",
        "rest_seconds": 10,
        "required_equipment": [],
        "safety_instructions": [
            "Avoid yanking the heel forcefully if you experience front-of-knee discomfort.",
            "Use wall support so you can relax the stretched thigh."
        ],
        "common_mistakes": [
            "Letting the bent knee flare far out to the side.",
            "Arching the lower back excessively."
        ],
        "beginner_modification": "Lie on your side on a mat and loop a towel around the top ankle.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Badminton", "Tennis", "Cricket", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "str-calf",
        "name": "Calf Stretch",
        "category": "Stretching and Flexibility",
        "description": "Wall-assisted gastrocnemius and soleus stretch to maintain ankle flexibility and ease lower-leg tightness.",
        "instructions": [
            "Stand facing a wall with hands placed flat at chest height.",
            "Step your right leg straight back with your heel pressed firmly into the floor and toes pointing forward.",
            "Gently bend your front knee and lean toward the wall until you feel a comfortable stretch in the back calf.",
            "Hold, then slightly bend the back knee for 10 seconds to target the deeper soleus before switching sides."
        ],
        "target_muscles": ["Gastrocnemius", "Soleus", "Achilles Tendon"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "30 sec per side",
        "rest_seconds": 10,
        "required_equipment": [],
        "safety_instructions": [
            "Keep the back foot aligned straight ahead rather than rolling onto the inner arch.",
            "Ease off if you feel sharp discomfort near the heel."
        ],
        "common_mistakes": [
            "Lifting the back heel off the ground.",
            "Turning the back toes far outward."
        ],
        "beginner_modification": "Shorten the stride distance between front and back feet for a gentler stretch.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Basketball", "Football", "Badminton", "Tennis", "Cricket", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "str-hip-flexor",
        "name": "Hip Flexor Stretch",
        "category": "Stretching and Flexibility",
        "description": "Half-kneeling stretch targeting tight hip flexors from prolonged sitting, running, and sprinting.",
        "instructions": [
            "Kneel on a mat with your right foot planted flat in front of you at a 90-degree knee angle.",
            "Keep your torso upright and gently tuck your pelvis under by lightly squeezing your back glute.",
            "Shift your hips forward just a few centimeters until you feel a comfortable stretch along the front of the back hip.",
            "Hold with relaxed breathing, then switch sides."
        ],
        "target_muscles": ["Hip Flexors", "Psoas", "Quadriceps"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "30 sec per side",
        "rest_seconds": 10,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Place a folded towel or mat under the kneeling knee for cushioning.",
            "Avoid arching the lower back to chase a deeper lunge."
        ],
        "common_mistakes": [
            "Lunging far forward with an overarching lumbar spine instead of tucking the pelvis.",
            "Letting the front heel lift off the ground."
        ],
        "beginner_modification": "Perform a standing split-stance hip flexor stretch if kneeling is uncomfortable.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Badminton", "Tennis", "Cricket", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "str-groin",
        "name": "Groin Stretch (Seated Butterfly)",
        "category": "Stretching and Flexibility",
        "description": "Seated inner-thigh adductor stretch supporting lateral agility, lunging, and kicking comfort.",
        "instructions": [
            "Sit tall on a mat and bring the soles of your feet together in front of you.",
            "Let your knees relax naturally outward toward the floor while holding your ankles or shins.",
            "Lengthen your spine upward and lean slightly forward from your hips if comfortable.",
            "Breathe deeply and allow inner thighs to release gently without bouncing."
        ],
        "target_muscles": ["Adductors", "Inner Thighs", "Hips"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 50,
        "recommended_sets": 2,
        "recommended_reps": "30-40 sec hold",
        "rest_seconds": 15,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Never press forcefully down on the knees.",
            "Keep feet slightly farther from your hips if inner thighs feel tight."
        ],
        "common_mistakes": [
            "Bouncing the knees rapidly up and down.",
            "Slouching the upper back."
        ],
        "beginner_modification": "Sit on a folded cushion to tilt the pelvis gently forward and support upright posture.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Badminton", "Tennis", "Basketball", "Cricket", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "str-shoulder",
        "name": "Shoulder Stretch (Cross-Body)",
        "category": "Stretching and Flexibility",
        "description": "Gentle posterior-shoulder stretch to relieve tension after racquet swings, throwing, swimming, or upper-body strength work.",
        "instructions": [
            "Stand or sit tall with shoulders relaxed away from your ears.",
            "Extend your right arm across your chest at roughly shoulder height.",
            "Use your left forearm gently above or below the right elbow to draw the arm closer to your chest.",
            "Hold steadily while keeping the right shoulder down, then switch arms."
        ],
        "target_muscles": ["Posterior Deltoid", "Rotator Cuff", "Upper Back"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 50,
        "recommended_sets": 2,
        "recommended_reps": "25 sec per side",
        "rest_seconds": 10,
        "required_equipment": [],
        "safety_instructions": [
            "Avoid pressing directly on the elbow joint.",
            "Stop if you feel pinching at the front of the shoulder."
        ],
        "common_mistakes": [
            "Shrugging the stretched shoulder upward toward the chin.",
            "Twisting the torso away to force extra stretch."
        ],
        "beginner_modification": "Keep the arm slightly lower than shoulder height for a gentler posterior stretch.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Tennis", "Swimming", "Cricket", "Basketball", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "str-chest",
        "name": "Chest Stretch (Open Doorway)",
        "category": "Stretching and Flexibility",
        "description": "Pectoral and anterior-shoulder stretch to counteract rounded posture and open breathing mechanics.",
        "instructions": [
            "Stand in a doorway or beside a wall with your forearm resting vertically against the frame at roughly shoulder height.",
            "Take a small step forward with the same-side foot.",
            "Gently lean forward and slightly rotate your chest away until you feel a mild stretch across the front of your chest.",
            "Hold calmly without letting your shoulder roll forward, then switch sides."
        ],
        "target_muscles": ["Pectoralis Major", "Pectoralis Minor", "Anterior Deltoid"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 50,
        "recommended_sets": 2,
        "recommended_reps": "25 sec per side",
        "rest_seconds": 10,
        "required_equipment": [],
        "safety_instructions": [
            "Keep the stretch gentle—avoid feeling tingling in the hand or pinching at the front of the shoulder.",
            "Maintain neutral neck alignment."
        ],
        "common_mistakes": [
            "Over-extending the lower back while leaning forward.",
            "Positioning the elbow too high above shoulder level if mobility is limited."
        ],
        "beginner_modification": "Keep the elbow slightly below shoulder height and take a smaller step forward.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Badminton", "Tennis", "Cricket", "Basketball", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "str-triceps",
        "name": "Triceps Stretch (Overhead)",
        "category": "Stretching and Flexibility",
        "description": "Overhead stretch targeting the long head of the triceps and latissimus dorsi after overhead or pushing sessions.",
        "instructions": [
            "Stand or sit tall with ribs stacked over your pelvis.",
            "Raise your right arm overhead and bend the elbow so your right hand reaches gently toward the upper middle back.",
            "Place your left hand lightly on your right elbow to guide a mild stretch along the back of the upper arm.",
            "Hold steadily with smooth breathing, then switch arms."
        ],
        "target_muscles": ["Triceps", "Latissimus Dorsi", "Shoulders"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 50,
        "recommended_sets": 2,
        "recommended_reps": "25 sec per side",
        "rest_seconds": 10,
        "required_equipment": [],
        "safety_instructions": [
            "Keep your chin neutral instead of pushing your head forward with your arm.",
            "Avoid yanking the elbow forcefully."
        ],
        "common_mistakes": [
            "Flaring the ribs and arching the lower back.",
            "Tucking the chin tightly into the chest."
        ],
        "beginner_modification": "Hold a towel in both hands behind your back to reduce overhead shoulder demand.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Badminton", "Tennis", "Cricket", "Basketball", "General Fitness"],
        "restriction_tags": ["overhead"],
    },
]
