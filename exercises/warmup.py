"""Warm-up exercise definitions for FitMotion AI."""

from __future__ import annotations

from typing import Any

WARMUP_EXERCISES: list[dict[str, Any]] = [
    {
        "id": "wu-light-jogging",
        "name": "Light Jogging",
        "category": "Warm-up",
        "description": "Easy-paced jogging in place or over short space to gradually elevate heart rate and warm up lower-body musculature.",
        "instructions": [
            "Stand tall with relaxed shoulders and arms bent at roughly 90 degrees.",
            "Begin a gentle jog at a conversational pace, landing softly on the midfoot.",
            "Keep your cadence light and rhythmic while breathing steadily through your nose and mouth.",
            "Maintain steady movement for the full duration without sprinting."
        ],
        "target_muscles": ["Quadriceps", "Calves", "Hamstrings", "Glutes", "Cardiovascular System"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 120,
        "recommended_sets": 1,
        "recommended_reps": "2 min continuous",
        "rest_seconds": 20,
        "required_equipment": [],
        "safety_instructions": [
            "Keep impact low and avoid slamming heels into hard surfaces.",
            "Stop immediately if you feel sharp joint discomfort or dizziness."
        ],
        "common_mistakes": [
            "Starting too fast and fatiguing before the main session.",
            "Hunching shoulders upward or holding your breath."
        ],
        "beginner_modification": "Substitute with brisk marching in place while swinging arms gently.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Badminton", "Basketball", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": ["knee_impact", "ankle_impact"],
    },
    {
        "id": "wu-high-knees",
        "name": "High Knees",
        "category": "Warm-up",
        "description": "Dynamic running-in-place drill that activates hip flexors, calves, and core while raising body temperature rapidly.",
        "instructions": [
            "Stand tall with feet hip-width apart and core lightly braced.",
            "Drive your right knee upward toward hip height while swinging your left arm forward.",
            "Quickly switch legs, landing softly on the balls of your feet.",
            "Maintain an upright torso and rhythmic arm drive throughout."
        ],
        "target_muscles": ["Hip Flexors", "Quadriceps", "Calves", "Core"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 45,
        "recommended_sets": 2,
        "recommended_reps": "30-45 sec",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Land softly on the balls of your feet to absorb shock smoothly.",
            "Maintain neutral spine alignment rather than leaning back."
        ],
        "common_mistakes": [
            "Leaning the torso backward to lift knees higher.",
            "Landing heavily with stiff knees."
        ],
        "beginner_modification": "Perform standing high-knee marches without hopping.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Badminton", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": ["knee_impact", "jumping", "ankle_impact"],
    },
    {
        "id": "wu-butt-kicks",
        "name": "Butt Kicks",
        "category": "Warm-up",
        "description": "Rhythmic heel-to-glute drill that dynamically warms up the hamstrings and stretches the front of the thighs.",
        "instructions": [
            "Stand tall with feet hip-width apart and arms bent at your sides.",
            "Jog gently in place while curling each heel rapidly up toward your glutes.",
            "Keep thighs pointing downward rather than driving knees far forward.",
            "Pump arms smoothly in rhythm with your steps."
        ],
        "target_muscles": ["Hamstrings", "Quadriceps", "Calves"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 45,
        "recommended_sets": 2,
        "recommended_reps": "30-45 sec",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Stay light on the forefoot and avoid locking the knees on landing.",
            "Reduce speed if you feel tightness in the front of the knee."
        ],
        "common_mistakes": [
            "Kicking heels back aggressively while arching the lower back.",
            "Letting knees flare wide to the sides."
        ],
        "beginner_modification": "Perform alternating standing hamstring curls without jogging.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Running", "Football", "Basketball", "Badminton", "Cricket", "Tennis", "General Fitness"],
        "restriction_tags": ["knee_impact", "jumping"],
    },
    {
        "id": "wu-jumping-jacks",
        "name": "Jumping Jacks",
        "category": "Warm-up",
        "description": "Full-body rhythmic warm-up drill coordinating shoulder elevation, hip abduction, and cardiovascular activation.",
        "instructions": [
            "Stand upright with feet together and arms resting at your sides.",
            "Hop feet out wider than shoulder width while sweeping arms smoothly overhead.",
            "Reverse the motion immediately to return feet together and arms down.",
            "Keep knees slightly soft on every landing and breathe rhythmically."
        ],
        "target_muscles": ["Shoulders", "Calves", "Glutes", "Adductors", "Cardiovascular System"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 45,
        "recommended_sets": 2,
        "recommended_reps": "30-45 sec",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Keep landings quiet and soft to reduce ankle and knee stress.",
            "Avoid forcing arms overhead if shoulders feel pinched."
        ],
        "common_mistakes": [
            "Letting knees collapse inward when landing.",
            "Shrugging shoulders aggressively toward the ears."
        ],
        "beginner_modification": "Perform step-out jacks by stepping one foot out at a time with no jumping.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["General Fitness", "Basketball", "Badminton", "Tennis", "Football", "Cricket"],
        "restriction_tags": ["jumping", "knee_impact", "ankle_impact", "overhead"],
    },
    {
        "id": "wu-arm-circles",
        "name": "Arm Circles",
        "category": "Warm-up",
        "description": "Controlled circular shoulder warm-up that lubricates the glenohumeral joint and prepares the upper back for overhead activity.",
        "instructions": [
            "Stand tall with feet shoulder-width apart and extend arms straight out to the sides at shoulder height.",
            "Draw small forward circles for half the set, gradually widening the circle diameter.",
            "Reverse direction and perform controlled backward circles.",
            "Keep ribs down and neck relaxed throughout."
        ],
        "target_muscles": ["Deltoids", "Rotator Cuff", "Upper Back"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 45,
        "recommended_sets": 2,
        "recommended_reps": "15 forward + 15 backward",
        "rest_seconds": 15,
        "required_equipment": [],
        "safety_instructions": [
            "Move smoothly within a pain-free range of motion.",
            "Avoid swinging the torso to generate momentum."
        ],
        "common_mistakes": [
            "Rushing circles with uncontrolled momentum.",
            "Elevating the shoulders toward the ears."
        ],
        "beginner_modification": "Keep circles small and slightly below shoulder height.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Swimming", "Badminton", "Tennis", "Cricket", "Basketball", "General Fitness"],
        "restriction_tags": ["overhead"],
    },
    {
        "id": "wu-dynamic-lunges",
        "name": "Dynamic Lunges",
        "category": "Warm-up",
        "description": "Controlled alternating forward lunges with optional gentle torso reach to open hips and activate lower-body stabilizers.",
        "instructions": [
            "Stand tall with feet hip-width apart and hands on hips or across your chest.",
            "Step forward with your right leg and lower your back knee gently toward the floor until both knees bend comfortably.",
            "Push through your front heel to return to standing.",
            "Alternate sides smoothly with balanced control."
        ],
        "target_muscles": ["Quadriceps", "Glutes", "Hip Flexors", "Hamstrings"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "10 alternating reps",
        "rest_seconds": 25,
        "required_equipment": [],
        "safety_instructions": [
            "Keep your front knee tracking smoothly in line with your middle toes.",
            "Avoid letting your back knee slam onto the floor."
        ],
        "common_mistakes": [
            "Taking too narrow a stance, causing loss of side-to-side balance.",
            "Collapsing the torso forward over the front thigh."
        ],
        "beginner_modification": "Shorten the lunge depth or hold onto a stable chair/wall for balance.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Badminton", "Tennis", "Basketball", "Running", "Cricket", "General Fitness"],
        "restriction_tags": ["knee_flexion"],
    },
    {
        "id": "wu-leg-swings",
        "name": "Leg Swings",
        "category": "Warm-up",
        "description": "Dynamic front-to-back and side-to-side leg swings to dynamically loosen hip flexors, hamstrings, and adductors.",
        "instructions": [
            "Stand beside a wall, railing, or sturdy chair and place one hand lightly on it for balance.",
            "Keep your standing knee slightly soft and swing your outside leg gently forward and backward.",
            "Gradually increase range without forcing height or rounding your lower back.",
            "Complete swings on both legs, then face the support to perform gentle side-to-side swings."
        ],
        "target_muscles": ["Hip Flexors", "Hamstrings", "Adductors", "Glutes"],
        "difficulty_level": "Beginner",
        "default_duration_sec": 60,
        "recommended_sets": 2,
        "recommended_reps": "10 per leg each plane",
        "rest_seconds": 15,
        "required_equipment": [],
        "safety_instructions": [
            "Use controlled momentum rather than aggressive ballistic kicking.",
            "Keep your pelvis stable to avoid straining the lower back."
        ],
        "common_mistakes": [
            "Over-arching the lumbar spine as the leg swings backward.",
            "Swinging wildly without core control."
        ],
        "beginner_modification": "Keep swings low and slow within a small, comfortable arc.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Football", "Running", "Badminton", "Tennis", "Cricket", "Basketball", "Swimming", "General Fitness"],
        "restriction_tags": [],
    },
    {
        "id": "wu-side-shuffles",
        "name": "Side Shuffles",
        "category": "Warm-up",
        "description": "Athletic lateral movement drill that prepares hips, glutes, ankles, and change-of-direction mechanics.",
        "instructions": [
            "Drop into a light athletic stance with knees softly bent, hips slightly back, and chest upright.",
            "Push off the outside foot to glide laterally 3 to 4 steps without crossing your feet.",
            "Softly decelerate on the outside foot and reverse direction smoothly.",
            "Stay light on the balls of your feet and keep eyes forward."
        ],
        "target_muscles": ["Glute Medius", "Quadriceps", "Adductors", "Calves"],
        "difficulty_level": "Intermediate",
        "default_duration_sec": 45,
        "recommended_sets": 2,
        "recommended_reps": "30-45 sec",
        "rest_seconds": 30,
        "required_equipment": [],
        "safety_instructions": [
            "Keep feet uncrossed to prevent tripping.",
            "Use a clear, non-slip floor space."
        ],
        "common_mistakes": [
            "Standing completely upright instead of holding an athletic hip hinge.",
            "Clicking heels together or crossing ankles mid-shuffle."
        ],
        "beginner_modification": "Perform controlled lateral steps without hopping or speed bursts.",
        "suitable_levels": ["Beginner", "Intermediate", "Advanced"],
        "relevant_sports": ["Badminton", "Basketball", "Tennis", "Football", "Cricket", "General Fitness"],
        "restriction_tags": ["ankle_impact", "knee_impact"],
    },
]
