"""Sport-specific conditioning exercise definitions across all 8 sports."""

from __future__ import annotations

from typing import Any

SPORT_CONDITIONING_EXERCISES: list[dict[str, Any]] = [
    # BADMINTON
    {
        "id": "sp-badminton-split-step",
        "name": "Badminton Split-Step & Shadow Footwork",
        "category": "Sport-Specific Conditioning",
        "description": "Court-inspired split-step and directional lunge drill building rapid reaction speed and lateral agility for badminton.",
        "instructions": [
            "Start in a balanced athletic ready stance in a clear 3m x 3m space.",
            "Perform a small, light split-step hop, then immediately push off toward a front-right, front-left, or side corner.",
            "Plant softly into a controlled lunge mimicking a net or side return, then push back crisply to center.",
            "Alternate corners rhythmically while keeping chest upright."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Calves", "Adductors", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "30-45 sec rounds",
        "rest_seconds": 40,
        "required_equipment": [],
        "safety_instructions": [
            "Keep the lead knee aligned over the toes on every directional lunge.",
            "Practice on a grippy, clutter-free floor surface."
        ],
        "common_mistakes": [
            "Lunging heavily with the front knee diving inward.",
            "Dropping the torso forward instead of staying balanced."
        ],
        "beginner_modification": "Step smoothly into each corner without hopping on the split-step.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Tennis"],
        "restriction_tags": ["knee_impact", "jumping", "ankle_impact"],
    },
    {
        "id": "sp-badminton-lateral-lunge",
        "name": "Lateral Lunge & Recovery Push-Off",
        "category": "Sport-Specific Conditioning",
        "description": "Side-to-side lower-body conditioning drill strengthening groin mobility and explosive return-to-base power.",
        "instructions": [
            "Stand tall with feet hip-width apart.",
            "Take a controlled wide step to the right, sitting hips back over your right heel while keeping your left leg straight.",
            "Push briskly off your right foot to return smoothly to a balanced upright stance.",
            "Alternate left and right sides with clean posture."
        ],
        "target_muscles": ["Adductors", "Glutes", "Quadriceps", "Core"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "8-10 per side",
        "rest_seconds": 40,
        "required_equipment": [],
        "safety_instructions": [
            "Keep both feet pointing forward rather than rolling the trailing ankle.",
            "Control your hip depth to stay pain-free in the groin and knees."
        ],
        "common_mistakes": [
            "Leaning chest completely down instead of pushing hips back.",
            "Allowing the lunging knee to cave inward."
        ],
        "beginner_modification": "Take a shorter lateral step and pause briefly before pushing back.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Tennis", "Basketball", "Football", "Cricket", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    # FOOTBALL
    {
        "id": "sp-football-acceleration",
        "name": "Short-Burst Acceleration Starts",
        "category": "Sport-Specific Conditioning",
        "description": "Explosive 10–15 meter sprint starts (or high-tempo wall/space drives) targeting first-step acceleration for football.",
        "instructions": [
            "Set into a staggered two-point athletic stance with weight slightly forward on the front ball of your foot.",
            "Drive arms powerfully and accelerate sharply for 10–15 meters (or 5 seconds of brisk forward-lean sprint marches indoors).",
            "Decelerate smoothly over several steps rather than stopping abruptly.",
            "Walk back calmly to recover fully before the next rep."
        ],
        "target_muscles": ["Glutes", "Hamstrings", "Quadriceps", "Calves", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 90,
        "recommended_sets": 4,
        "recommended_reps": "4 short bursts with full walk-back",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Always complete a thorough dynamic warm-up before sprinting.",
            "Decelerate gradually on a safe, even surface."
        ],
        "common_mistakes": [
            "Popping upright immediately on step one instead of building momentum gradually.",
            "Skipping rest between high-output bursts."
        ],
        "beginner_modification": "Perform controlled wall-drive knee marches at 70% effort to practice posture safely.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Cricket", "Basketball", "Running"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    {
        "id": "sp-football-cod-shuttle",
        "name": "Change-of-Direction 5-5 Shuttle",
        "category": "Sport-Specific Conditioning",
        "description": "Controlled deceleration, hip drop, and re-acceleration drill building cutting balance and field agility.",
        "instructions": [
            "Mark two points 5 meters apart on a non-slip surface.",
            "Run briskly to the far marker, lower your hips to decelerate cleanly, plant your outside foot, and pivot smoothly back.",
            "Focus on quiet, stable foot plants and sharp arm drive out of the turn.",
            "Alternate which leg plants on the turn across sets."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Calves", "Adductors", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "4-6 shuttles per set",
        "rest_seconds": 50,
        "required_equipment": [],
        "safety_instructions": [
            "Avoid sharp cuts on wet or slippery floors.",
            "Keep your plant knee aligned over your foot when changing direction."
        ],
        "common_mistakes": [
            "Staying tall and stiff when attempting to turn quickly.",
            "Always pivoting off the same dominant leg."
        ],
        "beginner_modification": "Perform at a controlled jog pace focusing strictly on low-hip deceleration mechanics.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Basketball", "Badminton", "Tennis", "Cricket"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    # BASKETBALL
    {
        "id": "sp-basketball-landing",
        "name": "Jump & Soft-Landing Mechanics Drill",
        "category": "Sport-Specific Conditioning",
        "description": "Controlled countermovement vertical jump emphasizing quiet, balanced athletic landing mechanics for basketball.",
        "instructions": [
            "Stand with feet shoulder-width apart and arms raised slightly.",
            "Swing arms back into a quarter-squat, then jump smoothly upward into a controlled vertical leap.",
            "Land quietly on the balls of your feet transitioning smoothly to flat feet with hips back and knees aligned over toes.",
            "Stick and hold the balanced landing for 2 full seconds before resetting."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Calves", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "6-8 controlled reps",
        "rest_seconds": 55,
        "required_equipment": [],
        "safety_instructions": [
            "Prioritize silent, knee-aligned landings over maximum jump height.",
            "Rest sufficiently between sets to keep landing mechanics crisp."
        ],
        "common_mistakes": [
            "Landing stiff-legged with loud impact.",
            "Letting knees knock inward upon landing."
        ],
        "beginner_modification": "Perform snap-downs (rise onto toes, then drop quickly into a quiet athletic squat without leaving the floor).",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Basketball", "Badminton", "Football", "General Fitness"],
        "restriction_tags": ["jumping", "knee_impact", "ankle_impact"],
    },
    {
        "id": "sp-basketball-defensive-slides",
        "name": "Defensive Lateral Slide Conditioning",
        "category": "Sport-Specific Conditioning",
        "description": "Low-stance lateral slide intervals strengthening hip endurance, ankle stability, and court defensive speed.",
        "instructions": [
            "Set into a low athletic stance with hips back, chest tall, and hands active at sides.",
            "Slide 3–4 steps laterally pushing off the trailing leg without bouncing up and down.",
            "Plant cleanly and slide back across to the starting mark.",
            "Keep head level and feet uncrossed throughout the interval."
        ],
        "target_muscles": ["Glute Medius", "Quadriceps", "Adductors", "Calves", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 50,
        "recommended_sets": 3,
        "recommended_reps": "30 sec rounds",
        "rest_seconds": 40,
        "required_equipment": [],
        "safety_instructions": [
            "Maintain wide foot spacing to avoid tripping.",
            "Stand upright briefly if quadriceps fatigue compromises knee alignment."
        ],
        "common_mistakes": [
            "Bobbing vertically instead of staying level.",
            "Rounding the upper back and looking straight at the floor."
        ],
        "beginner_modification": "Use a slightly higher athletic stance and slower 20-second intervals.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Basketball", "Tennis", "Badminton", "Football"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    # CRICKET
    {
        "id": "sp-cricket-rotational-core",
        "name": "Rotational Core Chop / Band Twist",
        "category": "Sport-Specific Conditioning",
        "description": "Controlled rotational trunk conditioning supporting batting power, throwing control, and bowling stability in cricket.",
        "instructions": [
            "Stand in a balanced athletic stance holding a resistance band anchored at chest height (or clasp hands / hold a light dumbbell).",
            "Keep hips stable and rotate your ribcage smoothly across your body with engaged obliques.",
            "Pause briefly at the finish with shoulders down, then return slowly resisting the pull.",
            "Complete equal repetitions on both sides for balanced rotational strength."
        ],
        "target_muscles": ["Obliques", "Transverse Abdominis", "Hips", "Shoulders"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "10-12 per side",
        "rest_seconds": 35,
        "required_equipment": ["Resistance Band"],
        "safety_instructions": [
            "Rotate through the hips and thoracic spine rather than jerking the lower back.",
            "Choose a light-to-medium band tension that allows smooth control."
        ],
        "common_mistakes": [
            "Pulling purely with the arms instead of rotating the torso.",
            "Twisting rapidly without controlling the return."
        ],
        "beginner_modification": "Perform standing bodyweight Russian-twist reaches with slow tempo if no band is available.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Cricket", "Tennis", "Badminton", "Basketball", "General Fitness"],
        "restriction_tags": ["lower_back_load"],
    },
    {
        "id": "sp-cricket-scapular-slides",
        "name": "Scapular Wall Slides",
        "category": "Sport-Specific Conditioning",
        "description": "Overhead scapular upward-rotation and shoulder-health drill ideal for bowlers, throwers, and racquet athletes.",
        "instructions": [
            "Stand with your back, hips, and head gently against a wall and feet stepped 15 cm forward.",
            "Raise arms into a 'W' position with forearms and backs of hands lightly touching the wall.",
            "Slowly slide arms upward into a 'Y' while keeping lower ribs tucked and shoulders relaxed away from ears.",
            "Lower smoothly back to 'W' and repeat."
        ],
        "target_muscles": ["Lower Trapezius", "Serratus Anterior", "Rotator Cuff"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "10-12 slow reps",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Only slide as high as you can maintain pain-free movement without overarching your back.",
            "Stop if you feel shoulder pinching."
        ],
        "common_mistakes": [
            "Arching the lower back far off the wall to force wrists flat.",
            "Shrugging shoulders upward as arms rise."
        ],
        "beginner_modification": "Perform seated or stand slightly farther from the wall with forearms off the wall.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Cricket", "Swimming", "Badminton", "Tennis", "Basketball", "General Fitness"],
        "restriction_tags": ["overhead"],
    },
    # TENNIS
    {
        "id": "sp-tennis-external-rotation",
        "name": "Banded External Shoulder Rotation",
        "category": "Sport-Specific Conditioning",
        "description": "Targeted rotator-cuff conditioning supporting serve deceleration, overhead stability, and shoulder endurance.",
        "instructions": [
            "Anchor a light resistance band at elbow height and stand sideways to the anchor.",
            "Hold the band with your outside hand, bend that elbow to 90 degrees, and tuck a folded towel lightly between elbow and ribs.",
            "Rotate your forearm smoothly outward away from your stomach while keeping the elbow pinned at your side.",
            "Return slowly over 2–3 seconds and switch arms."
        ],
        "target_muscles": ["Infraspinatus", "Teres Minor", "Rotator Cuff"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "12-15 per arm",
        "rest_seconds": 25,
        "required_equipment": ["Resistance Band"],
        "safety_instructions": [
            "Use light resistance—rotator cuff muscles respond best to high control, not heavy load.",
            "Keep wrist neutral and straight."
        ],
        "common_mistakes": [
            "Pulling the elbow away from the torso to cheat the motion.",
            "Twisting the whole torso outward."
        ],
        "beginner_modification": "Perform side-lying external rotations without resistance or with a very light water bottle.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Tennis", "Badminton", "Cricket", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
    # SWIMMING
    {
        "id": "sp-swimming-ytw-activation",
        "name": "Prone Y-T-W Shoulder & Back Activation",
        "category": "Sport-Specific Conditioning",
        "description": "Dryland upper-back and posterior-shoulder conditioning drill building stroke stability and posture for swimmers.",
        "instructions": [
            "Lie face down on a mat with your forehead resting gently on a folded towel and toes relaxed on the floor.",
            "Engage your core lightly and lift straight arms softly off the mat into a 'Y' shape (thumbs up) for 2 seconds.",
            "Transition smoothly into a 'T' (arms out to sides) and then a 'W' (elbows bent, squeezing shoulder blades down and together).",
            "Lower smoothly and repeat with calm neck alignment."
        ],
        "target_muscles": ["Mid/Lower Trapezius", "Rhomboids", "Posterior Deltoids", "Upper Back"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "6-8 Y-T-W complexes",
        "rest_seconds": 30,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Keep your neck long and forehead low—do not crank your head upward.",
            "Lift arms only a few centimeters using upper-back control."
        ],
        "common_mistakes": [
            "Over-arching the lower back to lift the chest high off the floor.",
            "Shrugging shoulders into the ears."
        ],
        "beginner_modification": "Perform standing hinged slightly forward with knees soft if lying prone is uncomfortable.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Cricket", "Badminton", "Tennis", "General Fitness"],
        "restriction_tags": ["overhead"],
    },
    # RUNNING
    {
        "id": "sp-running-a-skips",
        "name": "Running A-Skips & Cadence Drill",
        "category": "Sport-Specific Conditioning",
        "description": "Rhythmic running-mechanics drill reinforcing tall posture, ankle dorsiflexion, and snappy hip drive.",
        "instructions": [
            "Stand tall with elbows bent at 90 degrees and gaze straight ahead.",
            "Drive one knee crisply upward to hip height with toes pulled up toward the shin while adding a light rhythmic skip on the stance leg.",
            "Strike the ground cleanly underneath your hips on the ball of your foot.",
            "Coordinate opposite arm and leg swings smoothly down a 15-meter path or in place."
        ],
        "target_muscles": ["Hip Flexors", "Calves", "Glutes", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 50,
        "recommended_sets": 3,
        "recommended_reps": "25-30 sec intervals",
        "rest_seconds": 35,
        "required_equipment": [],
        "safety_instructions": [
            "Stay light and elastic—avoid heavy pounding.",
            "Warm up ankles and calves first."
        ],
        "common_mistakes": [
            "Leaning backward instead of maintaining tall running posture.",
            "Letting toes point downward instead of staying dorsiflexed."
        ],
        "beginner_modification": "Perform A-marches (walking tempo with crisp knee drive and zero hopping).",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Cricket"],
        "restriction_tags": ["jumping", "ankle_impact", "knee_impact"],
    },
    # GENERAL GYM TRAINING
    {
        "id": "sp-gym-goblet-squat",
        "name": "Dumbbell Goblet Squat",
        "category": "Sport-Specific Conditioning",
        "description": "Front-loaded lower-body and core strength movement reinforcing upright squat mechanics for gym and athletic conditioning.",
        "instructions": [
            "Hold one dumbbell vertically against your chest with elbows tucked down comfortably.",
            "Stand with feet slightly wider than shoulder width and brace your torso.",
            "Sit hips down smoothly between your knees while keeping chest upright and heels planted.",
            "Drive cleanly back up through the midfoot to standing."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Core", "Upper Back"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 70,
        "recommended_sets": 3,
        "recommended_reps": "10-12",
        "rest_seconds": 55,
        "required_equipment": ["Dumbbells"],
        "safety_instructions": [
            "Select a manageable weight that allows full posture control.",
            "Keep knees tracking smoothly in line with toes."
        ],
        "common_mistakes": [
            "Holding the dumbbell far away from the chest, straining the lower back.",
            "Dropping chest forward at the bottom."
        ],
        "beginner_modification": "Use a very light dumbbell or perform bodyweight squats.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Football", "Basketball", "Cricket", "Tennis", "Badminton", "Running", "Swimming"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "sp-gym-dumbbell-row",
        "name": "Supported Single-Arm Dumbbell Row",
        "category": "Sport-Specific Conditioning",
        "description": "Unilateral horizontal pulling exercise strengthening the lats, rhomboids, and anti-rotation core stability.",
        "instructions": [
            "Place one hand and same-side knee on a sturdy bench (or stagger stance with front forearm resting on front thigh).",
            "Hold a dumbbell in your free hand hanging straight beneath your shoulder with a flat back.",
            "Pull the dumbbell smoothly back toward your hip pocket, squeezing your shoulder blade back without twisting.",
            "Lower under control over 2 seconds and switch sides."
        ],
        "target_muscles": ["Latissimus Dorsi", "Rhomboids", "Biceps", "Core"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 75,
        "recommended_sets": 3,
        "recommended_reps": "10-12 per side",
        "rest_seconds": 45,
        "required_equipment": ["Dumbbells"],
        "safety_instructions": [
            "Keep your spine neutral and avoid jerking the weight upward.",
            "Choose a weight you can control smoothly on the lowering phase."
        ],
        "common_mistakes": [
            "Pulling straight up to the shoulder while shrugging instead of rowing toward the hip.",
            "Twisting the torso open on every rep."
        ],
        "beginner_modification": "Use a light dumbbell or perform resistance-band seated rows.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Swimming", "Cricket", "Tennis", "Badminton", "Basketball", "Football"],
        "restriction_tags": [],
    },
]
