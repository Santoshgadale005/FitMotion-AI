"""Evidence-based Advanced, Intermediate, and Sport-Specific exercise expansions.

Grounded in NSCA, ACSM, FIFA 11+, BWF, USTA, ECB, and USA Swimming conditioning
frameworks so every difficulty tier (Beginner, Intermediate, Advanced) and every
supported sport has distinct, authentic exercises.
"""

from __future__ import annotations

from typing import Any

EXPANDED_EXERCISES: list[dict[str, Any]] = [
    # --- ADVANCED WARM-UP ---
    {
        "id": "wu-carioca-footwork",
        "name": "Carioca (Grapevine) Agility Warm-up",
        "category": "Warm-up",
        "description": "High-tempo lateral crossover footwork drill integrating hip rotation, foot speed, and multi-planar coordination for field and court athletes.",
        "instructions": [
            "Start in a balanced athletic stance with arms relaxed out to the sides for counterbalance.",
            "Step laterally by crossing your trailing foot in front of your lead foot, then uncross, then cross behind.",
            "Keep your shoulders square to the front while allowing hips to pivot briskly.",
            "Move smoothly 10–15 meters each way, building rhythm without stiffness."
        ],
        "target_muscles": ["Hip Rotators", "Obliques", "Calves", "Adductors", "Ankle Stabilizers"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 50,
        "recommended_sets": 3,
        "recommended_reps": "2 × 15m each direction",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Stay light on the balls of your feet and perform on a clear, non-slip surface.",
            "Start slow until foot crossover timing feels automatic."
        ],
        "common_mistakes": [
            "Looking down at the feet instead of keeping eyes up.",
            "Twisting the upper chest instead of isolating hip rotation."
        ],
        "beginner_modification": "Walk slowly through the front-and-back crossover pattern before speeding up.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Badminton", "Tennis", "Basketball", "Cricket"],
        "restriction_tags": ["ankle_impact", "knee_impact"],
    },
    {
        "id": "wu-inchworm-spiderman",
        "name": "Inchworm to World's Greatest Lunge Flow",
        "category": "Warm-up",
        "description": "Full-body dynamic warm-up combining hamstring lengthening, plank shoulder activation, deep hip opening, and thoracic rotation.",
        "instructions": [
            "Stand tall, hinge at the hips to touch the floor, and walk your hands forward into a strong high plank.",
            "Step your right foot outside your right hand into a deep lunge while keeping your back leg straight.",
            "Rotate your right arm smoothly toward the ceiling, following your hand with your eyes.",
            "Return your hand to the floor, step back to plank, repeat on the left, then walk hands back to stand."
        ],
        "target_muscles": ["Hamstrings", "Hip Flexors", "Thoracic Spine", "Core", "Shoulders"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 75,
        "recommended_sets": 2,
        "recommended_reps": "6 full alternating flows",
        "rest_seconds": 25,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Brace your core firmly in the plank phase so hips never sag.",
            "Bend knees softly if hamstrings feel tight during the walk-out."
        ],
        "common_mistakes": [
            "Rushing the thoracic reach without pausing to breathe.",
            "Dropping the back knee heavily onto the floor."
        ],
        "beginner_modification": "Rest the back knee gently on a mat during the thoracic rotation.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Football", "Cricket", "Swimming", "Running"],
        "restriction_tags": ["wrist_load"],
    },
    # --- ADVANCED MOBILITY ---
    {
        "id": "mob-cossack-squat",
        "name": "Cossack Squat Mobility Transitions",
        "category": "Mobility",
        "description": "Deep lateral hip, adductor, and ankle mobility flow transitioning smoothly side to side while keeping torso upright.",
        "instructions": [
            "Take a wide stance with toes turned slightly outward and arms extended forward for balance.",
            "Shift weight smoothly over your right leg, sitting deep into a single-leg squat while your left leg stays straight with toes pointing up.",
            "Keep your right heel firmly planted and chest proud for 2 seconds.",
            "Glide low across center (or rise slightly first) to transition cleanly onto the left leg."
        ],
        "target_muscles": ["Adductors", "Hip Joint", "Ankles", "Glutes", "Quadriceps"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 70,
        "recommended_sets": 2,
        "recommended_reps": "8-10 alternating reps",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Only descend as deep as your heel stays flat and knees remain pain-free.",
            "Use fingertips lightly on the floor for assistance if ankles feel tight."
        ],
        "common_mistakes": [
            "Lifting the working heel off the floor.",
            "Collapsing the working knee inward."
        ],
        "beginner_modification": "Perform higher lateral squats holding a sturdy doorframe or chair.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Football", "Tennis", "Basketball", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "mob-overhead-squat-drill",
        "name": "Overhead Stick/Towel Squat Mobility",
        "category": "Mobility",
        "description": "Full-chain thoracic extension, shoulder flexion, hip, and ankle mobility test and drill using a light towel or PVC dowel.",
        "instructions": [
            "Hold a light towel or stick wide overhead with straight elbows and active shoulder blades.",
            "Stand with feet shoulder-width apart and brace your core lightly.",
            "Descend slowly into a controlled squat while keeping your arms stacked vertically above your midfoot.",
            "Pause 2 seconds at the bottom without letting your chest collapse, then stand smoothly."
        ],
        "target_muscles": ["Thoracic Spine", "Shoulders", "Hips", "Ankles", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "8 slow controlled reps",
        "rest_seconds": 30,
        "required_equipment": [],
        "safety_instructions": [
            "Use zero weight (a light towel or broomstick only) and stay in a pain-free range.",
            "Stop descending as soon as arms pitch forward or heels lift."
        ],
        "common_mistakes": [
            "Over-arching the lower back to force arms behind the head.",
            "Dropping rapidly without controlling posture."
        ],
        "beginner_modification": "Elevate heels on a folded towel and perform half-depth overhead squats.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Basketball", "Cricket", "General Fitness"],
        "restriction_tags": ["overhead", "knee_flexion"],
    },
    # --- ADVANCED STRETCHING & FLEXIBILITY ---
    {
        "id": "str-couch-stretch",
        "name": "Couch Stretch (Deep Hip Flexor & Quad)",
        "category": "Stretching and Flexibility",
        "description": "Deep wall- or bench-assisted anterior hip and quadriceps flexibility drill counteracting sprint tightness and sitting posture.",
        "instructions": [
            "Kneel on a padded mat facing away from a wall or sturdy bench and place your back shin/foot gently up against the wall.",
            "Step your front foot forward into a stable 90-degree lunge stance.",
            "Lightly squeeze your back glute and rise gradually toward an upright torso without overarching your lower back.",
            "Hold steadily with calm, slow exhales, then switch legs."
        ],
        "target_muscles": ["Hip Flexors", "Rectus Femoris", "Quadriceps"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 70,
        "recommended_sets": 2,
        "recommended_reps": "35 sec per side",
        "rest_seconds": 15,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Pad the back knee well and keep knee further from the wall if quad tension is intense.",
            "Avoid jamming the lumbar spine into hyperextension."
        ],
        "common_mistakes": [
            "Leaning torso far back with a flared ribcage instead of tucking the pelvis.",
            "Holding your breath through intense stretch tension."
        ],
        "beginner_modification": "Perform standard half-kneeling hip flexor stretch with back foot flat on the floor.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "str-pnf-hamstring",
        "name": "Active Contract-Relax (PNF) Hamstring Stretch",
        "category": "Stretching and Flexibility",
        "description": "Supine resistance-band or towel PNF flexibility technique using gentle isometric contractions to safely expand hamstring range.",
        "instructions": [
            "Lie on your back and loop a resistance band or towel around your right foot, extending the leg toward the ceiling.",
            "Hold a mild stretch for 10 seconds with your opposite leg flat on the mat.",
            "Gently press your raised heel downward against the band at 30% effort for 5 seconds while keeping the leg stationary.",
            "Exhale, relax the muscle completely, and gently draw the leg a few degrees closer for 15 seconds. Repeat twice per side."
        ],
        "target_muscles": ["Hamstrings", "Calves", "Posterior Chain"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 75,
        "recommended_sets": 2,
        "recommended_reps": "2 contract-relax cycles per leg",
        "rest_seconds": 15,
        "required_equipment": ["Resistance Band"],
        "safety_instructions": [
            "Keep isometric contractions gentle (30–40% effort)—never push into sharp pain.",
            "Maintain a relaxed head and shoulders on the mat."
        ],
        "common_mistakes": [
            "Pulling maximally during the contraction phase.",
            "Lifting the opposite hip off the mat."
        ],
        "beginner_modification": "Hold a gentle static seated hamstring stretch without PNF contractions.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Running", "Badminton", "Tennis", "Cricket"],
        "restriction_tags": [],
    },
    # --- ADVANCED STRENGTH TRAINING ---
    {
        "id": "st-bulgarian-split-squat",
        "name": "Bulgarian Split Squats (Rear-Foot Elevated)",
        "category": "Strength Training",
        "description": "Gold-standard unilateral lower-body strength builder targeting single-leg force, glute power, and hip stability for field and court athletes.",
        "instructions": [
            "Stand about two feet in front of a sturdy bench and rest the top of your rear foot comfortably behind you.",
            "Brace your core, keep your torso tall or slightly hinged forward, and lower your back knee smoothly toward the floor.",
            "Keep your front knee aligned directly over your front toes with full midfoot contact.",
            "Drive powerfully through your front foot to stand tall, completing all reps before switching legs."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Hamstrings", "Hip Stabilizers"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 80,
        "recommended_sets": 3,
        "recommended_reps": "8-10 per leg",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Master bodyweight balance cleanly before adding dumbbells.",
            "Avoid letting your front heel peel off the ground."
        ],
        "common_mistakes": [
            "Standing too close to the bench, jamming the front knee forward.",
            "Pushing mostly with the back leg instead of the front leg."
        ],
        "beginner_modification": "Perform standard floor split squats with both feet grounded.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Basketball", "Badminton", "Cricket", "Tennis", "Running", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "st-nordic-hamstring",
        "name": "Nordic Hamstring Eccentric Lowers",
        "category": "Strength Training",
        "description": "FIFA 11+ gold-standard eccentric posterior-chain exercise building high-speed sprint deceleration resilience in the hamstrings.",
        "instructions": [
            "Kneel on a cushioned mat with ankles firmly anchored by a training partner or secure padded anchor.",
            "Keep hips extended and torso straight from knees to shoulders—do not hinge at the waist.",
            "Slowly lower your chest forward toward the floor over 3–4 seconds, resisting gravity purely with your hamstrings.",
            "Catch yourself smoothly with hands in a push-up position and lightly press back to the start."
        ],
        "target_muscles": ["Hamstrings", "Glutes", "Calves", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 70,
        "recommended_sets": 3,
        "recommended_reps": "4-6 slow eccentric reps",
        "rest_seconds": 75,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Start with low volume (3–5 reps) because eccentric hamstring loading produces strong muscle fatigue.",
            "Stop immediately if you feel cramping or sharp posterior-thigh pulling."
        ],
        "common_mistakes": [
            "Bending forward at the hips instead of staying straight from knees to head.",
            "Falling rapidly without controlling the first half of the descent."
        ],
        "beginner_modification": "Perform slow 4-second single-leg glute bridge lowers (hamstring walk-outs) on a mat.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Football", "Running", "Cricket", "Basketball"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "st-single-leg-rdl",
        "name": "Single-Leg Romanian Deadlift",
        "category": "Strength Training",
        "description": "Unilateral hip-hinge strength and proprioception exercise correcting side-to-side imbalances in runners, cricketers, and footballers.",
        "instructions": [
            "Stand tall on your left foot with a soft micro-bend in the knee and dumbbells (or bodyweight hands) in front of thighs.",
            "Hinge smoothly at the hip, extending your right leg straight backward as your flat torso lowers near parallel.",
            "Keep both hip bones pointing straight down toward the floor (do not open the lifted hip sideways).",
            "Squeeze your standing glute and hamstring to drive back to tall standing."
        ],
        "target_muscles": ["Hamstrings", "Glutes", "Glute Medius", "Ankle Stabilizers", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 75,
        "recommended_sets": 3,
        "recommended_reps": "8 per leg",
        "rest_seconds": 50,
        "required_equipment": ["Dumbbells"],
        "safety_instructions": [
            "Keep your spine completely neutral and move slowly under balance.",
            "Start unweighted or with light dumbbells until hips stay square."
        ],
        "common_mistakes": [
            "Rotating the lifted hip open toward the ceiling.",
            "Rounding the upper back to reach lower."
        ],
        "beginner_modification": "Perform kickstand (B-stance) RDLs with back toes lightly resting on the floor for balance.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Cricket", "Football", "Badminton", "Tennis", "General Fitness"],
        "restriction_tags": ["lower_back_load"],
    },
    {
        "id": "st-pike-pushups",
        "name": "Pike Push-ups (Overhead Pressing Strength)",
        "category": "Strength Training",
        "description": "Advanced bodyweight vertical pressing movement developing deltoid, triceps, and scapular upward-rotation strength without gym weights.",
        "instructions": [
            "Start in a high plank, then walk your feet slightly closer to your hands while lifting your hips high into an inverted 'V' pike.",
            "Keep core braced and elbows angled slightly back (not flared straight out).",
            "Lower the crown of your head cleanly toward a spot slightly ahead of your fingertips.",
            "Press smoothly back to full arm extension while maintaining the pike angle."
        ],
        "target_muscles": ["Deltoids", "Triceps", "Upper Chest", "Serratus Anterior", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "6-10",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Control the descent completely so your head never bumps the floor.",
            "Skip if you have overhead shoulder or wrist load restrictions."
        ],
        "common_mistakes": [
            "Flaring elbows out to 90 degrees.",
            "Lowering directly between the hands instead of creating a tripod slightly ahead."
        ],
        "beginner_modification": "Perform standard push-ups or elevated incline push-ups.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Swimming", "Basketball", "General Fitness"],
        "restriction_tags": ["overhead", "wrist_load"],
    },
    {
        "id": "st-heavy-calf-eccentric",
        "name": "Single-Leg Slow Eccentric Calf Raises",
        "category": "Strength Training",
        "description": "Evidence-based heavy-slow tendon-stiffness drill strengthening the gastrocnemius and soleus for running economy and jumping power.",
        "instructions": [
            "Stand on one foot (optionally on the edge of a low step) holding a wall lightly for balance.",
            "Rise smoothly onto the ball of your foot over 2 seconds using full ankle range.",
            "Pause 1 second at the top with weight centered over the big and second toe.",
            "Lower slowly over 3 full seconds back to neutral, then repeat."
        ],
        "target_muscles": ["Gastrocnemius", "Soleus", "Achilles Tendon", "Ankle Stabilizers"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 65,
        "recommended_sets": 3,
        "recommended_reps": "10-12 per leg",
        "rest_seconds": 45,
        "required_equipment": [],
        "safety_instructions": [
            "Use a flat floor first if stepping off a ledge feels sensitive in the Achilles.",
            "Never bounce at the bottom of the rep."
        ],
        "common_mistakes": [
            "Rushing the lowering phase instead of counting 3 seconds.",
            "Rolling outward onto the pinky-toe side of the foot."
        ],
        "beginner_modification": "Rise with two feet and lower slowly on one foot.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Basketball", "Badminton", "Tennis"],
        "restriction_tags": [],
    },
    # --- ADVANCED CARDIOVASCULAR TRAINING ---
    {
        "id": "cardio-tabata-sprints",
        "name": "Tabata High-Intensity Interval Conditioning (20s/10s)",
        "category": "Cardiovascular Training",
        "description": "Advanced anaerobic power conditioning protocol alternating 20 seconds of crisp high-output effort with 10 seconds of recovery for 8 rounds.",
        "instructions": [
            "Complete at least a 5-minute dynamic warm-up before starting.",
            "Choose a crisp athletic drill (shuttle runs, fast high-knees, or shadow footwork bursts).",
            "Perform 20 seconds at high controlled output (~8.5/10 effort), followed immediately by 10 seconds of standing recovery.",
            "Complete 8 rounds (4 minutes total) and finish with 3 minutes of light walking."
        ],
        "target_muscles": ["Cardiovascular System", "Anaerobic System", "Quadriceps", "Calves", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 240,
        "recommended_sets": 1,
        "recommended_reps": "8 rounds × (20s on / 10s off)",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Limit all-out interval protocols to 1–2 non-consecutive days per week.",
            "Stop immediately if form deteriorates or dizziness occurs."
        ],
        "common_mistakes": [
            "Skipping the warm-up or cooldown.",
            "Pacing poorly so rounds 5–8 collapse into sloppy mechanics."
        ],
        "beginner_modification": "Use 20 seconds moderate work with 40 seconds easy walking for 5 rounds.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Football", "Basketball", "Badminton", "Tennis", "General Fitness"],
        "restriction_tags": ["knee_impact", "jumping", "ankle_impact"],
    },
    {
        "id": "cardio-tempo-threshold",
        "name": "Lactate-Threshold Tempo Running",
        "category": "Cardiovascular Training",
        "description": "Sustained 'comfortably hard' aerobic threshold run engineered to raise sustainable race pace and endurance capacity.",
        "instructions": [
            "Warm up with 5 minutes of easy jogging and leg swings.",
            "Settle into a brisk, controlled tempo pace (~7/10 effort where only short phrases can be spoken).",
            "Maintain tall posture, quick cadence, and steady rhythmic breathing for the target block.",
            "Ease smoothly into 3 minutes of light walking to cool down."
        ],
        "target_muscles": ["Cardiovascular System", "Quadriceps", "Hamstrings", "Calves", "Glutes"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 600,
        "recommended_sets": 1,
        "recommended_reps": "10-20 min threshold effort",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Tempo effort should feel challenging yet sustainable—not an all-out sprint.",
            "Avoid scheduling back-to-back hard running days."
        ],
        "common_mistakes": [
            "Starting at race-sprint pace and slowing dramatically halfway through.",
            "Tensing shoulders and clenching fists under fatigue."
        ],
        "beginner_modification": "Perform 3 × 3-minute brisk intervals separated by 2 minutes of easy walking.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Cricket"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    {
        "id": "cardio-double-under-rope",
        "name": "Double-Under / High-Cadence Jump Rope",
        "category": "Cardiovascular Training",
        "description": "Advanced elastic footwork and anaerobic jump-rope conditioning building reactive calf spring and hand-foot timing.",
        "instructions": [
            "Establish a smooth rhythm with 10 single-under bounces keeping elbows tucked.",
            "Perform a slightly higher elastic pogo jump while snapping wrists crisply so the rope passes twice per jump (or alternate rapid high-knee singles).",
            "Land quietly on the balls of your feet with neutral posture.",
            "Work in crisp 30-second intervals with full 30-second recovery breaths."
        ],
        "target_muscles": ["Calves", "Achilles Complex", "Forearms", "Shoulders", "Cardiovascular System"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 180,
        "recommended_sets": 4,
        "recommended_reps": "30s intervals",
        "rest_seconds": 35,
        "required_equipment": ["Jump Rope"],
        "safety_instructions": [
            "Use a shock-absorbing surface and supportive footwear.",
            "Keep total jump volume progressive to protect shins and calves."
        ],
        "common_mistakes": [
            "Tucking knees up toward the chest ('donkey kicking') instead of keeping body straight.",
            "Swinging arms wide out from the ribs."
        ],
        "beginner_modification": "Perform steady single-unders alternating 20s jump / 20s rest.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Badminton", "Tennis", "Basketball", "General Fitness"],
        "restriction_tags": ["jumping", "ankle_impact", "knee_impact"],
    },
    # --- ADVANCED BALANCE & STABILITY ---
    {
        "id": "bal-copenhagen-plank",
        "name": "Copenhagen Adductor Plank",
        "category": "Balance and Stability",
        "description": "Elite FIFA-backed lateral groin and oblique strength-stability hold proven to fortify adductors for cutting and kicking sports.",
        "instructions": [
            "Lie on your side beside a sturdy low bench with your bottom forearm planted directly under your shoulder.",
            "Place your top inner foot (or inner knee for a shorter lever) securely on top of the bench.",
            "Brace your core and lift your hips into a straight line, holding your bottom leg hovered cleanly beneath the bench.",
            "Maintain steady breathing for 15–25 seconds, lower smoothly, and switch sides."
        ],
        "target_muscles": ["Hip Adductors", "Obliques", "Glute Medius", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "15-25 sec per side",
        "rest_seconds": 45,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Begin with the top KNEE resting on the bench (shorter lever) before progressing to the ankle.",
            "Lower immediately if you feel sharp groin or shoulder discomfort."
        ],
        "common_mistakes": [
            "Letting hips sag downward toward the floor.",
            "Starting immediately with a full straight-leg lever before building adductor tolerance."
        ],
        "beginner_modification": "Rest the top knee on the bench and keep the bottom foot lightly touching the floor.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Football", "Badminton", "Tennis", "Basketball"],
        "restriction_tags": [],
    },
    {
        "id": "bal-hollow-body-hold",
        "name": "Hollow Body Streamline Hold",
        "category": "Balance and Stability",
        "description": "USA Swimming & gymnastics-grade anti-extension core stability hold teaching full-body streamline tension from fingertips to toes.",
        "instructions": [
            "Lie flat on your back with arms extended overhead and legs straight together.",
            "Press your lower back firmly into the mat by posteriorly tilting your pelvis and bracing your deep abs.",
            "Lift shoulder blades and straight legs slightly off the mat to form a subtle banana-shaped streamline.",
            "Hold cleanly with controlled breaths without allowing any gap beneath your lower back."
        ],
        "target_muscles": ["Transverse Abdominis", "Rectus Abdominis", "Hip Flexors", "Lats"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 50,
        "recommended_sets": 3,
        "recommended_reps": "25-35 sec hold",
        "rest_seconds": 40,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "End the hold immediately if your lower back arches away from the floor.",
            "Avoid straining your neck—keep chin gently tucked."
        ],
        "common_mistakes": [
            "Lowering legs too close to the floor while losing lower-back contact.",
            "Holding breath completely."
        ],
        "beginner_modification": "Tuck one or both knees toward chest and place arms alongside hips.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Basketball", "General Fitness"],
        "restriction_tags": ["lower_back_load", "overhead"],
    },
    {
        "id": "bal-pallof-press",
        "name": "Banded Pallof Press (Anti-Rotation Core)",
        "category": "Balance and Stability",
        "description": "NSCA-recommended anti-rotation trunk stability exercise protecting the spine against forceful rotational torques in cricket and racquet sports.",
        "instructions": [
            "Anchor a resistance band at chest height and stand sideways with feet shoulder-width apart and knees softly bent.",
            "Hold the band handle with both hands centered against your sternum, creating moderate side tension.",
            "Exhale and press your hands straight forward until elbows lock cleanly without letting the band twist your torso.",
            "Hold for 3 full seconds resisting rotation, return slowly to chest, and repeat both sides."
        ],
        "target_muscles": ["Obliques", "Transverse Abdominis", "Glutes", "Scapular Stabilizers"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "10 reps (3s hold) per side",
        "rest_seconds": 35,
        "required_equipment": ["Resistance Band"],
        "safety_instructions": [
            "Keep ribs stacked directly over pelvis and shoulders relaxed downward.",
            "Choose band tension you can resist cleanly without leaning sideways."
        ],
        "common_mistakes": [
            "Allowing hands to drift back toward the anchor point.",
            "Locking the knees rigidly."
        ],
        "beginner_modification": "Step closer to the anchor point for lighter band resistance.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Cricket", "Tennis", "Badminton", "Football", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "bal-pistol-squat-progression",
        "name": "Assisted / Full Single-Leg Pistol Squat",
        "category": "Balance and Stability",
        "description": "Advanced unilateral lower-body balance, ankle mobility, and maximal relative leg strength skill.",
        "instructions": [
            "Stand tall on your right leg with your left leg extended straight ahead and arms forward for counterbalance.",
            "Keeping your standing heel flat and knee tracking straight over toes, lower slowly with full control.",
            "Descend as deep as mobility and balance allow (touching a low box or full depth).",
            "Drive smoothly straight up through the standing midfoot without twisting."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Ankle Stabilizers", "Hip Flexors", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 75,
        "recommended_sets": 3,
        "recommended_reps": "5-6 per leg",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Hold a doorframe or suspension strap lightly until full range feels controlled and knee-friendly.",
            "Stop if you experience anterior knee pinching."
        ],
        "common_mistakes": [
            "Collapsing the standing knee inward on ascent.",
            "Dropping rapidly into the bottom position."
        ],
        "beginner_modification": "Perform single-leg box squats onto a chair-height seat.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Basketball", "Football", "Running", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    # --- ADVANCED / ENHANCED SPORT-SPECIFIC CONDITIONING ---
    {
        "id": "sp-badminton-skater-bounds",
        "name": "Lateral Skater Bounds (Stick & Stabilize)",
        "category": "Sport-Specific Conditioning",
        "description": "Explosive single-leg lateral plyometric bound training explosive court push-off and quiet single-leg deceleration for badminton and tennis.",
        "instructions": [
            "Start balanced on your right leg in an athletic quarter-squat.",
            "Push explosively sideways off your right foot to leap laterally onto your left foot.",
            "Absorb the landing quietly with hips back, knee aligned over toes, and trailing foot hovered behind—sticking the hold for 2 seconds.",
            "Explode back across to the right leg with crisp arm swing."
        ],
        "target_muscles": ["Glute Medius", "Glutes", "Quadriceps", "Calves", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "8-10 per side",
        "rest_seconds": 50,
        "required_equipment": [],
        "safety_instructions": [
            "Stick every landing cleanly with zero knee wobble before bounding back.",
            "Perform on a grippy, flat surface."
        ],
        "common_mistakes": [
            "Rushing side-to-side without absorbing and stabilizing the landing.",
            "Landing stiff-legged with an upright torso."
        ],
        "beginner_modification": "Perform controlled wide lateral steps with a 2-second single-leg balance hold.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Tennis", "Basketball", "Football"],
        "restriction_tags": ["jumping", "knee_impact", "ankle_impact"],
    },
    {
        "id": "sp-badminton-six-corner-ghosting",
        "name": "Badminton 6-Corner Ghosting Intervals",
        "category": "Sport-Specific Conditioning",
        "description": "BWF-style high-speed multi-corner shadow footwork replicating full singles court coverage, net lunges, and overhead rear-court recovery.",
        "instructions": [
            "Imagine all 6 badminton court corners (front-left, front-right, mid-left, mid-right, rear-left, rear-right) around a central base.",
            "Initiate every move with a crisp split-step from center, sprint/chassé smoothly to a chosen corner, mimic a clean shot, and recover back to center.",
            "Keep heel-to-toe braking smooth on front lunges and pivot hips rapidly for rear-court moves.",
            "Maintain crisp court posture for 35–45 second work bouts."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Calves", "Adductors", "Cardiovascular System"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 4,
        "recommended_reps": "40s work / 40s rest",
        "rest_seconds": 40,
        "required_equipment": [],
        "safety_instructions": [
            "Ensure at least 3m × 3m of clear, non-slip space before moving at high speed.",
            "Maintain front-knee alignment over toes on every net lunge."
        ],
        "common_mistakes": [
            "Skipping the center split-step reset between corners.",
            "Collapsing the chest down toward the front knee when fatigued."
        ],
        "beginner_modification": "Practice 4-corner walking/jogging shadow footwork at 60% tempo.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Badminton"],
        "restriction_tags": ["knee_impact", "ankle_impact", "jumping"],
    },
    {
        "id": "sp-football-rsa-sprints",
        "name": "Football Repeated Sprint Ability (RSA) 30m",
        "category": "Sport-Specific Conditioning",
        "description": "NSCA-backed repeated 20–30m high-speed sprint intervals with brief 25–30s recoveries mirroring match-play sprint demands.",
        "instructions": [
            "Mark a clear 20–30 meter straight lane on turf, grass, or track after a full warm-up.",
            "Accelerate explosively from a staggered athletic stance to high speed through the far cone.",
            "Decelerate smoothly over 5–8 meters past the finish marker.",
            "Walk calmly back to the start so total rest is 25–30 seconds before the next rep."
        ],
        "target_muscles": ["Hamstrings", "Glutes", "Quadriceps", "Calves", "Anaerobic System"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 120,
        "recommended_sets": 2,
        "recommended_reps": "6 × 25-30m (25s rest)",
        "rest_seconds": 90,
        "required_equipment": [],
        "safety_instructions": [
            "Always warm up progressively with dynamic strides before maximal sprinting.",
            "Stop immediately if you feel hamstring tightness."
        ],
        "common_mistakes": [
            "Stopping abruptly at the finish cone instead of decelerating gradually.",
            "Running maximal sprints on cold muscles."
        ],
        "beginner_modification": "Perform 6 × 15m build-up runs at 75% controlled speed with 45s walk recovery.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Football", "Cricket"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    {
        "id": "sp-basketball-depth-jump",
        "name": "Basketball Depth-Drop to Reactive Vertical Jump",
        "category": "Sport-Specific Conditioning",
        "description": "Advanced plyometric reactive-strength drill building explosive vertical rebound jump height and rapid ground-contact stiffness.",
        "instructions": [
            "Stand on a low sturdy step or plyo box (25–35 cm high).",
            "Step (do not jump) smoothly off the edge, landing softly on both balls of your feet simultaneously.",
            "Minimize ground contact time and immediately explode vertically upward reaching both hands toward the ceiling.",
            "Stick the second landing quietly in an athletic quarter-squat, then rest 10 seconds before the next rep."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Calves", "Reactive Elastic System"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 65,
        "recommended_sets": 3,
        "recommended_reps": "5 crisp reps",
        "rest_seconds": 75,
        "required_equipment": [],
        "safety_instructions": [
            "Use a low box (under 35 cm) and prioritize crisp mechanics over volume.",
            "Avoid when legs are heavily fatigued."
        ],
        "common_mistakes": [
            "Jumping upward off the box instead of stepping off.",
            "Letting knees buckle inward during ground contact."
        ],
        "beginner_modification": "Perform standard countermovement vertical jumps from the floor with a 2-second landing stick.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["Basketball", "Badminton"],
        "restriction_tags": ["jumping", "knee_impact", "ankle_impact"],
    },
    {
        "id": "sp-cricket-between-wickets-shuttle",
        "name": "Cricket 20m Between-Wickets Sprint Shuttles",
        "category": "Sport-Specific Conditioning",
        "description": "Pitch-length (20.12m) sprint, low-center turn, and re-acceleration conditioning replicating quick singles, twos, and threes.",
        "instructions": [
            "Set two markers 20 meters apart on a safe running surface.",
            "Sprint briskly from crease to crease, dropping hips low on the final 2 steps to plant cleanly and turn 180 degrees.",
            "Drive powerfully back to the starting line to simulate running a quick two.",
            "Recover 30–40 seconds walking before beginning the next shuttle set."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Hamstrings", "Calves", "Anaerobic System"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 90,
        "recommended_sets": 4,
        "recommended_reps": "3 × 20m turn shuttles",
        "rest_seconds": 50,
        "required_equipment": [],
        "safety_instructions": [
            "Alternate left-foot and right-foot pivot turns to keep joint loading symmetrical.",
            "Wear turf/running shoes with reliable traction."
        ],
        "common_mistakes": [
            "Turning upright with a wide slow loop instead of dropping hips cleanly.",
            "Always pivoting off the same dominant leg."
        ],
        "beginner_modification": "Perform 2 × 15m controlled-pace turn shuttles focusing on low-hip deceleration.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Cricket"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    {
        "id": "sp-tennis-serve-power-slams",
        "name": "Explosive Overhead Rotational Chop / Slam",
        "category": "Sport-Specific Conditioning",
        "description": "High-velocity overhead-to-hip kinetic-chain power drill mimicking tennis serve and badminton smash acceleration.",
        "instructions": [
            "Stand in a balanced split athletic stance holding a high-anchored resistance band (or light medicine ball).",
            "Reach tall overhead with ribs braced and hips loaded.",
            "Drive smoothly downward and across your front hip using coordinated lat, oblique, and hip power.",
            "Control the reset slowly and perform equal reps on both sides."
        ],
        "target_muscles": ["Latissimus Dorsi", "Obliques", "Core", "Shoulders", "Hips"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "8 explosive reps per side",
        "rest_seconds": 45,
        "required_equipment": ["Resistance Band"],
        "safety_instructions": [
            "Keep power smooth and controlled—never yank the lower back into sharp extension.",
            "Warm up shoulders thoroughly beforehand."
        ],
        "common_mistakes": [
            "Using only arm strength without engaging hips and obliques.",
            "Arching the lower back excessively at the top reach."
        ],
        "beginner_modification": "Perform slow-tempo diagonal band woodchoppers at light resistance.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Tennis", "Badminton", "Cricket"],
        "restriction_tags": ["overhead", "lower_back_load"],
    },
    {
        "id": "sp-tennis-forearm-eccentrics",
        "name": "Wrist & Forearm Eccentric Conditioning",
        "category": "Sport-Specific Conditioning",
        "description": "USTA-inspired forearm extensor and flexor strength drill supporting grip stability and racquet shock absorption.",
        "instructions": [
            "Sit tall with your forearm resting comfortably along your thigh or a bench, wrist hanging just past the edge holding a light dumbbell.",
            "Use your free hand to assist lifting the wrist into extension.",
            "Lower the light dumbbell slowly over 3 full seconds using only your forearm muscles.",
            "Complete controlled reps palm-down (extensors) and palm-up (flexors) on both arms."
        ],
        "target_muscles": ["Forearm Extensors", "Forearm Flexors", "Wrist Stabilizers"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "12 slow reps each way",
        "rest_seconds": 25,
        "required_equipment": ["Dumbbells"],
        "safety_instructions": [
            "Use a very light dumbbell (1–3 kg)—forearm tendons thrive on slow control, not heavy loads.",
            "Stop if you feel sharp pain on the outside of the elbow."
        ],
        "common_mistakes": [
            "Using weights that are too heavy and rushing the lowering phase.",
            "Lifting the forearm off the thigh."
        ],
        "beginner_modification": "Use a filled 500 ml water bottle or light resistance band underfoot.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Tennis", "Badminton", "Cricket"],
        "restriction_tags": ["wrist_load"],
    },
    {
        "id": "sp-swimming-band-pull",
        "name": "Dryland Swim-Cord Catch & Lat Pull",
        "category": "Sport-Specific Conditioning",
        "description": "USA Swimming dryland staple replicating the freestyle high-elbow catch and pull-through phase for stroke power and shoulder endurance.",
        "instructions": [
            "Anchor a resistance band at chest/door height and hinge forward at the hips with a flat back and arms extended ahead.",
            "Initiate the 'catch' by bending elbows slightly high while keeping fingertips angled downward.",
            "Sweep both hands smoothly past your hips to full triceps finish using your lats and upper back.",
            "Return smoothly under control without shrugging shoulders."
        ],
        "target_muscles": ["Latissimus Dorsi", "Triceps", "Posterior Deltoids", "Core"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 65,
        "recommended_sets": 3,
        "recommended_reps": "12-15 smooth pulls",
        "rest_seconds": 40,
        "required_equipment": ["Resistance Band"],
        "safety_instructions": [
            "Keep your spine flat and neck neutral looking slightly downward.",
            "Use smooth resistance that lets you hold high-elbow mechanics."
        ],
        "common_mistakes": [
            "Dropping elbows down first instead of setting an early catch.",
            "Standing upright and swinging the lower back."
        ],
        "beginner_modification": "Step closer to the anchor point and pull one arm at a time.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming"],
        "restriction_tags": [],
    },
    {
        "id": "sp-swimming-band-pull-aparts",
        "name": "Band Pull-Aparts & Scapular Retraction",
        "category": "Sport-Specific Conditioning",
        "description": "Upper-back and posterior-shoulder endurance exercise balancing heavy forward-pulling and overhead sports.",
        "instructions": [
            "Stand tall holding a light resistance band straight out at chest height with palms facing up or down.",
            "Keep elbows nearly straight and pull the band smoothly apart until it lightly touches your chest.",
            "Squeeze shoulder blades cleanly together and down (away from ears) for 1 second.",
            "Return slowly to start resisting the band recoil."
        ],
        "target_muscles": ["Rhomboids", "Mid Trapezius", "Posterior Deltoids", "Rotator Cuff"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 55,
        "recommended_sets": 3,
        "recommended_reps": "15 controlled reps",
        "rest_seconds": 25,
        "required_equipment": ["Resistance Band"],
        "safety_instructions": [
            "Keep lower ribs tucked so your lower back does not arch.",
            "Select a band tension that permits smooth full range."
        ],
        "common_mistakes": [
            "Shrugging shoulders upward toward the ears.",
            "Snapping the arms rapidly back together."
        ],
        "beginner_modification": "Widen your grip on the band to decrease tension.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Tennis", "Badminton", "Cricket", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "sp-running-pogo-hops",
        "name": "Plyometric Pogo Hops (Ankle Stiffness)",
        "category": "Sport-Specific Conditioning",
        "description": "Low-amplitude, quick-contact elastic hops recommended by running scientists to sharpen Achilles spring and running economy.",
        "instructions": [
            "Stand tall with core braced, ankles dorsiflexed, and hands on hips or softly bent.",
            "Bounce rapidly straight up and down off the balls of your feet using minimal knee bend.",
            "Focus on crisp, quiet, quick ground contacts (like a coiled spring).",
            "Perform short high-quality sets and rest fully between sets."
        ],
        "target_muscles": ["Calves", "Achilles Tendon", "Foot Intrinsics", "Ankle Stabilizers"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 45,
        "recommended_sets": 3,
        "recommended_reps": "15-20 quick elastic hops",
        "rest_seconds": 45,
        "required_equipment": [],
        "safety_instructions": [
            "Build ankle strength with slow calf raises before advancing to pogo hops.",
            "Perform on a forgiving track, grass, or rubber surface."
        ],
        "common_mistakes": [
            "Bending the knees deeply like squat jumps instead of keeping contact quick.",
            "Allowing heels to slam heavily onto the ground."
        ],
        "beginner_modification": "Perform low two-foot rhythmic toe bounces holding lightly onto a counter.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Basketball", "Badminton"],
        "restriction_tags": ["jumping", "ankle_impact", "knee_impact"],
    },
    {
        "id": "sp-gym-dumbbell-thrusters",
        "name": "Dumbbell Squat-to-Press Thrusters",
        "category": "Sport-Specific Conditioning",
        "description": "High-efficiency compound strength and metabolic conditioning movement uniting front squats and overhead presses in one fluid chain.",
        "instructions": [
            "Hold dumbbells racked cleanly at shoulder height with elbows slightly forward and feet shoulder-width apart.",
            "Lower smoothly into a controlled squat with chest upright and heels planted.",
            "Drive explosively upward through your legs and use that momentum to press both dumbbells smoothly overhead.",
            "Lower weights cleanly back to shoulders and transition into the next rep."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Shoulders", "Triceps", "Core"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 65,
        "recommended_sets": 3,
        "recommended_reps": "8-12",
        "rest_seconds": 60,
        "required_equipment": ["Dumbbells"],
        "safety_instructions": [
            "Brace your core firmly overhead so the lower back stays neutral.",
            "Start with light-to-moderate dumbbells to preserve crisp squat and press alignment."
        ],
        "common_mistakes": [
            "Letting elbows drop and rounding the upper back in the squat.",
            "Pressing weights forward instead of directly over shoulders."
        ],
        "beginner_modification": "Perform bodyweight squats followed by light seated overhead presses separately.",
        "suitable_levels": ["Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Basketball", "Football"],
        "restriction_tags": ["overhead", "knee_flexion"],
    },
    {
        "id": "sp-gym-burpee-broad-jump",
        "name": "Burpee Broad Jump Conditioning",
        "category": "Sport-Specific Conditioning",
        "description": "Advanced total-body anaerobic power drill combining floor push-up mechanics with explosive horizontal jumping.",
        "instructions": [
            "Drop smoothly into a controlled plank/push-up on the floor, then pop feet cleanly up into an athletic squat.",
            "Swing arms back and launch forward into a controlled two-foot broad jump.",
            "Land quietly with knees bent and hips back, absorbing impact cleanly.",
            "Reset smoothly and repeat down a clear 10m path or turn around cleanly."
        ],
        "target_muscles": ["Full Body", "Glutes", "Quadriceps", "Chest", "Cardiovascular System"],
        "difficulty_level": "Advanced",
        "default_duration_sec": 60,
        "recommended_sets": 3,
        "recommended_reps": "6-8 controlled reps",
        "rest_seconds": 60,
        "required_equipment": [],
        "safety_instructions": [
            "Focus on quiet, stable broad-jump landings—do not sacrifice form for speed.",
            "Avoid if you have jumping, knee-impact, or wrist restrictions."
        ],
        "common_mistakes": [
            "Sagging the lower back during the burpee drop.",
            "Landing stiff-legged with loud floor impact."
        ],
        "beginner_modification": "Step back into plank (no jump), step forward, and stand tall with an overhead reach.",
        "suitable_levels": ["Advanced"],
        "relevant_sports": ["General Fitness", "Football", "Basketball"],
        "restriction_tags": ["jumping", "knee_impact", "ankle_impact", "wrist_load"],
    },
    # --- ENHANCED RECOVERY ---
    {
        "id": "rec-contrast-breathing-decompression",
        "name": "90/90 Wall-Supported Parasympathetic Breathing",
        "category": "Recovery and Cooldown",
        "description": "Post-competition spinal decompression and extended-exhale breathing drill used by elite athletes to accelerate nervous-system down-regulation.",
        "instructions": [
            "Lie on your back with calves resting comfortably on a chair or bench so hips and knees both form 90-degree angles.",
            "Place hands gently on your lower ribs and allow your lower back to relax completely into the mat.",
            "Inhale calmly through your nose for 4 seconds feeling 360-degree rib expansion.",
            "Exhale softly through pursed lips for 6–8 seconds, pausing gently for 2 seconds before the next breath."
        ],
        "target_muscles": ["Diaphragm", "Lumbar Spine Decompression", "Nervous System Recovery"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 150,
        "recommended_sets": 1,
        "recommended_reps": "8-10 slow cycles",
        "rest_seconds": 10,
        "required_equipment": ["Yoga Mat"],
        "safety_instructions": [
            "Keep breaths completely effortless—shorten the exhale if you feel air hunger.",
            "Use a folded pillow under your head if your chin tilts backward."
        ],
        "common_mistakes": [
            "Forcing the exhale aggressively instead of letting air release smoothly.",
            "Elevating shoulders toward ears on inhale."
        ],
        "beginner_modification": "Lie with feet flat on the floor and knees bent using a simple 3s inhale / 5s exhale.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Swimming", "Basketball", "Badminton", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": [],
    },
]
