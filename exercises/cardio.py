"""Cardiovascular training exercise definitions for FitMotion AI."""

from __future__ import annotations

from typing import Any

CARDIO_EXERCISES: list[dict[str, Any]] = [
    {
        "id": "cardio-running",
        "name": "Steady-State Running",
        "category": "Cardiovascular Training",
        "description": "Aerobic endurance running at a sustainable effort level to develop cardiovascular stamina and running economy.",
        "instructions": [
            "Begin with 2–3 minutes of easy jogging to settle into a rhythmic stride.",
            "Maintain an upright posture with relaxed shoulders and midfoot landings under your center of mass.",
            "Hold a conversational-to-moderate effort (Zone 2–3) throughout the target interval.",
            "Taper into a light walk for the final 1–2 minutes."
        ],
        "target_muscles": ["Cardiovascular System", "Quadriceps", "Hamstrings", "Calves", "Glutes"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 600,
        "recommended_sets": 1,
        "recommended_reps": "10-20 min steady pace",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Wear supportive running shoes and build weekly mileage gradually.",
            "Slow to a walk if breathing becomes uncomfortably labored or joint pain appears."
        ],
        "common_mistakes": [
            "Starting out too fast and burning out early.",
            "Overstriding with heavy heel strikes far ahead of the hips."
        ],
        "beginner_modification": "Alternate 2 minutes of brisk walking with 1 minute of easy jogging.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Cricket", "Basketball", "Tennis", "Badminton", "General Fitness"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    {
        "id": "cardio-cycling",
        "name": "Moderate-Intensity Cycling",
        "category": "Cardiovascular Training",
        "description": "Low-impact aerobic cycling session building leg endurance and cardiovascular capacity without joint pounding.",
        "instructions": [
            "Adjust saddle height so your knee maintains a slight bend at the bottom of the pedal stroke.",
            "Pedal at a smooth cadence (75–90 RPM) with light-to-moderate resistance.",
            "Keep shoulders relaxed and avoid gripping the handlebars tightly.",
            "Maintain steady aerobic effort and cool down with 2 minutes of easy spinning."
        ],
        "target_muscles": ["Quadriceps", "Hamstrings", "Glutes", "Calves", "Cardiovascular System"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 600,
        "recommended_sets": 1,
        "recommended_reps": "10-20 min steady spin",
        "rest_seconds": 45,
        "required_equipment": ["Stationary Bike"],
        "safety_instructions": [
            "Verify bike seat height before starting to prevent anterior knee strain.",
            "Hydrate regularly during longer sessions."
        ],
        "common_mistakes": [
            "Setting the saddle too low, overloading the knees.",
            "Grinding heavy gears at very low cadence."
        ],
        "beginner_modification": "Keep resistance light and start with 8–10 minutes at an easy conversational effort.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Running", "Football", "Swimming", "Cricket", "Basketball", "Badminton", "Tennis"],
        "restriction_tags": [],
    },
    {
        "id": "cardio-jump-rope",
        "name": "Jump Rope Conditioning",
        "category": "Cardiovascular Training",
        "description": "Rhythmic footwork and aerobic conditioning drill sharpening calf elasticity, coordination, and court stamina.",
        "instructions": [
            "Hold handles lightly at hip height with elbows close to your ribs.",
            "Turn the rope mainly from your wrists rather than swinging whole arms.",
            "Hop only 2–3 cm off the floor on the balls of your feet with soft knees.",
            "Perform timed work intervals followed by brief active recovery breaths."
        ],
        "target_muscles": ["Calves", "Quadriceps", "Forearms", "Shoulders", "Cardiovascular System"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 180,
        "recommended_sets": 3,
        "recommended_reps": "45-60 sec intervals",
        "rest_seconds": 45,
        "required_equipment": ["Jump Rope"],
        "safety_instructions": [
            "Jump on a forgiving surface such as wood, rubber mat, or track when possible.",
            "Stop if you experience shin or Achilles soreness."
        ],
        "common_mistakes": [
            "Jumping too high and landing heavily on flat feet.",
            "Flaring arms wide away from the torso."
        ],
        "beginner_modification": "Practice shadow jump-rope bounces without a rope or step-overs for 20-second intervals.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Tennis", "Basketball", "Football", "Running", "General Fitness"],
        "restriction_tags": ["jumping", "ankle_impact", "knee_impact"],
    },
    {
        "id": "cardio-swimming",
        "name": "Lap Swimming (Aerobic Pace)",
        "category": "Cardiovascular Training",
        "description": "Zero-impact full-body cardiovascular conditioning combining rhythmic breathing, upper-body pull, and core alignment.",
        "instructions": [
            "Begin with 2 easy warm-up laps focusing on long, streamlined body position.",
            "Swim steady freestyle or breaststroke laps at a smooth, sustainable breathing cadence.",
            "Keep head aligned neutrally with your spine and rotate from the hips rather than over-twisting the neck.",
            "Rest 20–30 seconds between sets of 2–4 laps."
        ],
        "target_muscles": ["Latissimus Dorsi", "Shoulders", "Core", "Quadriceps", "Cardiovascular System"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 600,
        "recommended_sets": 4,
        "recommended_reps": "2-4 laps per set",
        "rest_seconds": 30,
        "required_equipment": ["Swimming Pool"],
        "safety_instructions": [
            "Swim only in supervised or safe pool environments appropriate to your swimming ability.",
            "Never push through dizziness or breath-holding distress."
        ],
        "common_mistakes": [
            "Lifting the head too high to breathe, causing hips and legs to sink.",
            "Holding breath underwater instead of exhaling smoothly."
        ],
        "beginner_modification": "Use a kickboard or pull buoy and take generous rest between single laps.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "General Fitness", "Running", "Cricket", "Football"],
        "restriction_tags": ["overhead"],
    },
    {
        "id": "cardio-interval-training",
        "name": "Bodyweight Interval Training (Shuttle / Tempo)",
        "category": "Cardiovascular Training",
        "description": "Structured work-to-rest cardiovascular intervals designed to build anaerobic repeat-effort stamina.",
        "instructions": [
            "Select a controlled athletic movement (fast high-knee march, shadow footwork, or short shuttle runs).",
            "Work briskly for 30 seconds at a challenging yet controlled effort (about 7–8/10).",
            "Recover actively by walking gently for 30–45 seconds until breathing settles.",
            "Repeat cleanly for the prescribed rounds without letting form deteriorate."
        ],
        "target_muscles": ["Cardiovascular System", "Quadriceps", "Glutes", "Calves", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 300,
        "recommended_sets": 5,
        "recommended_reps": "30 sec work / 30 sec walk",
        "rest_seconds": 30,
        "required_equipment": [],
        "safety_instructions": [
            "Always warm up for at least 5 minutes before high-effort intervals.",
            "Scale effort down immediately if form breaks down or you feel lightheaded."
        ],
        "common_mistakes": [
            "Going all-out on round 1 and unable to complete remaining rounds safely.",
            "Skipping recovery intervals."
        ],
        "beginner_modification": "Use 20 seconds of brisk marching followed by 40 seconds of gentle walking.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Basketball", "Badminton", "Tennis", "Cricket", "Running", "General Fitness"],
        "restriction_tags": ["knee_impact", "jumping"],
    },
    {
        "id": "cardio-low-intensity",
        "name": "Low-Intensity Cardio (Brisk Marching / Step-Touch)",
        "category": "Cardiovascular Training",
        "description": "Accessible, equipment-free low-impact aerobic movement suitable for beginners, general wellness, and active endurance days.",
        "instructions": [
            "Stand tall with relaxed shoulders and begin brisk marching or rhythmic step-touches side to side.",
            "Swing arms naturally in rhythm to elevate heart rate gently into an easy aerobic zone.",
            "Maintain steady nasal-or-conversational breathing throughout.",
            "Keep movements smooth and joint-friendly."
        ],
        "target_muscles": ["Cardiovascular System", "Calves", "Hip Flexors", "Glutes"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 300,
        "recommended_sets": 1,
        "recommended_reps": "5-10 min continuous",
        "rest_seconds": 20,
        "required_equipment": [],
        "safety_instructions": [
            "Keep space clear around your feet to avoid tripping.",
            "Maintain a comfortable conversational effort."
        ],
        "common_mistakes": [
            "Slouching forward while marching.",
            "Holding tension in the neck and shoulders."
        ],
        "beginner_modification": "Slow the cadence and take brief standing breathers as needed.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Running", "Cricket", "Football", "Badminton", "Tennis", "Basketball", "Swimming"],
        "restriction_tags": [],
    },
]
