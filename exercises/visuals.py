"""Animated biomechanical SVG demonstration generator for FitMotion AI.

Generates smooth, looping, resolution-independent vector animations stored
locally in `assets/images/<exercise_id>.svg`. Each exercise maps to an
articulated 11-joint human figure animated with eased SMIL keyframes plus
exercise-specific props (wall, bar, dumbbells, jump rope, bike, water, band,
or breathing aura) so users see the exact movement pattern clearly offline.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

import config

CATEGORY_ACCENTS: dict[str, str] = {
    "Warm-up": "#FFB020",
    "Mobility": "#00D4FF",
    "Stretching and Flexibility": "#00E676",
    "Strength Training": "#FC4C02",
    "Cardiovascular Training": "#FF3B30",
    "Balance and Stability": "#A855F7",
    "Recovery and Cooldown": "#00E676",
    "Sport-Specific Conditioning": "#FC4C02",
}

Pose = dict[str, tuple[float, float]]

# Joint keys expected in every Pose:
# head, neck, hip, l_elbow, l_hand, r_elbow, r_hand, l_knee, l_foot, r_knee, r_foot


def _vals(poses: list[Pose], joint: str, axis: int) -> str:
    """Build a semicolon-separated SMIL values string for a joint's x (0) or y (1)."""
    return ";".join(f"{p[joint][axis]:.1f}" for p in poses)


def _anim(attr: str, values: str, dur: float) -> str:
    """Emit a smooth looping SMIL <animate> element."""
    return (
        f'<animate attributeName="{attr}" values="{values}" '
        f'dur="{dur:.2f}s" repeatCount="indefinite" calcMode="linear"/>'
    )


def _anim_line(
    poses: list[Pose],
    j1: str,
    j2: str,
    dur: float,
    color: str,
    width: float,
) -> str:
    """Emit an articulated limb segment animated across all keyframes."""
    p0 = poses[0]
    x1_0, y1_0 = p0[j1]
    x2_0, y2_0 = p0[j2]
    return (
        f'<line x1="{x1_0:.1f}" y1="{y1_0:.1f}" x2="{x2_0:.1f}" y2="{y2_0:.1f}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round">'
        f'{_anim("x1", _vals(poses, j1, 0), dur)}'
        f'{_anim("y1", _vals(poses, j1, 1), dur)}'
        f'{_anim("x2", _vals(poses, j2, 0), dur)}'
        f'{_anim("y2", _vals(poses, j2, 1), dur)}'
        f"</line>"
    )


def _anim_circle(
    poses: list[Pose],
    joint: str,
    dur: float,
    radius: float,
    fill: str,
    opacity: float = 1.0,
) -> str:
    """Emit a moving head or joint marker circle."""
    x0, y0 = poses[0][joint]
    return (
        f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="{radius}" fill="{fill}" opacity="{opacity}">'
        f'{_anim("cx", _vals(poses, joint, 0), dur)}'
        f'{_anim("cy", _vals(poses, joint, 1), dur)}'
        f"</circle>"
    )


def _render_figure(
    poses: list[Pose],
    dur: float,
    accent: str,
    highlight_arms: bool = False,
    highlight_legs: bool = True,
    extra_props: str = "",
) -> str:
    """Compile articulated human skeleton + optional props into SVG markup."""
    # Ensure cyclic loop back to start pose
    loop_poses = poses if poses[0] == poses[-1] else poses + [poses[0]]
    arm_front = accent if highlight_arms else "#E2E8F0"
    arm_back = "#64748B"
    leg_front = accent if highlight_legs else "#CBD5E1"
    leg_back = "#64748B"

    parts = [
        # Floor baseline
        '<line x1="26" y1="126" x2="188" y2="126" stroke="#334155" stroke-width="2.5" stroke-linecap="round"/>',
        extra_props,
        # Back limbs first for clean 2.5D depth
        _anim_line(loop_poses, "neck", "l_elbow", dur, arm_back, 4.5),
        _anim_line(loop_poses, "l_elbow", "l_hand", dur, arm_back, 4.0),
        _anim_line(loop_poses, "hip", "l_knee", dur, leg_back, 5.2),
        _anim_line(loop_poses, "l_knee", "l_foot", dur, leg_back, 4.8),
        # Torso
        _anim_line(loop_poses, "neck", "hip", dur, "#F8FAFC", 6.2),
        # Front limbs
        _anim_line(loop_poses, "hip", "r_knee", dur, leg_front, 5.4),
        _anim_line(loop_poses, "r_knee", "r_foot", dur, leg_front, 5.0),
        _anim_line(loop_poses, "neck", "r_elbow", dur, arm_front, 4.6),
        _anim_line(loop_poses, "r_elbow", "r_hand", dur, arm_front, 4.2),
        # Head & subtle hip/knee articulation joints
        _anim_circle(loop_poses, "head", dur, 8.5, accent),
        _anim_circle(loop_poses, "hip", dur, 3.0, "#F8FAFC", 0.9),
        _anim_circle(loop_poses, "r_knee", dur, 2.5, "#F8FAFC", 0.8),
    ]
    return "\n  ".join(p for p in parts if p)


def _pose(
    head: tuple[float, float],
    neck: tuple[float, float],
    hip: tuple[float, float],
    l_elbow: tuple[float, float],
    l_hand: tuple[float, float],
    r_elbow: tuple[float, float],
    r_hand: tuple[float, float],
    l_knee: tuple[float, float],
    l_foot: tuple[float, float],
    r_knee: tuple[float, float],
    r_foot: tuple[float, float],
) -> Pose:
    return {
        "head": head,
        "neck": neck,
        "hip": hip,
        "l_elbow": l_elbow,
        "l_hand": l_hand,
        "r_elbow": r_elbow,
        "r_hand": r_hand,
        "l_knee": l_knee,
        "l_foot": l_foot,
        "r_knee": r_knee,
        "r_foot": r_foot,
    }


def _get_exercise_animation(exercise_id: str, category: str, accent: str) -> str:
    """Return custom animated SVG scene tailored specifically to `exercise_id`."""

    # 1. HIGH KNEES / RUNNING A-SKIPS
    if exercise_id in ("wu-high-knees", "sp-running-a-skips"):
        p1 = _pose((108, 36), (107, 48), (105, 78), (94, 62), (86, 56), (118, 60), (128, 50), (105, 102), (104, 123), (128, 76), (124, 98))
        p2 = _pose((108, 32), (107, 44), (105, 74), (106, 62), (110, 58), (106, 62), (110, 58), (112, 98), (108, 118), (110, 96), (108, 116))
        p3 = _pose((108, 36), (107, 48), (105, 78), (118, 60), (128, 50), (94, 62), (86, 56), (128, 76), (124, 98), (105, 102), (104, 123))
        return _render_figure([p1, p2, p3, p2], dur=0.95, accent=accent, highlight_arms=True, highlight_legs=True)

    # 2. BUTT KICKS
    if exercise_id == "wu-butt-kicks":
        p1 = _pose((110, 36), (108, 48), (104, 78), (95, 62), (88, 56), (118, 62), (126, 54), (106, 102), (105, 123), (100, 103), (84, 84))
        p2 = _pose((110, 33), (108, 45), (104, 75), (106, 62), (112, 58), (106, 62), (112, 58), (104, 100), (102, 120), (104, 100), (102, 120))
        p3 = _pose((110, 36), (108, 48), (104, 78), (118, 62), (126, 54), (95, 62), (88, 56), (100, 103), (84, 84), (106, 102), (105, 123))
        return _render_figure([p1, p2, p3, p2], dur=0.95, accent=accent, highlight_legs=True)

    # 3. LIGHT JOGGING / STEADY-STATE RUNNING / ACCELERATION SPRINTS / LIGHT WALKING / INTERVALS
    if exercise_id in ("wu-light-jogging", "cardio-running", "sp-football-acceleration", "rec-light-walking", "cardio-interval-training", "cardio-low-intensity"):
        speed = 0.72 if exercise_id in ("sp-football-acceleration", "cardio-interval-training") else (1.45 if exercise_id in ("rec-light-walking", "cardio-low-intensity") else 1.05)
        lean = 8 if exercise_id == "sp-football-acceleration" else (4 if exercise_id != "rec-light-walking" else 1)
        p1 = _pose((108 + lean, 37), (106 + lean * 0.6, 49), (102, 79), (88, 62), (78, 58), (118, 60), (128, 52), (86, 100), (74, 118), (122, 96), (130, 121))
        p2 = _pose((108 + lean, 34), (106 + lean * 0.6, 46), (102, 76), (104, 62), (108, 60), (104, 62), (108, 60), (104, 100), (100, 122), (106, 98), (104, 116))
        p3 = _pose((108 + lean, 37), (106 + lean * 0.6, 49), (102, 79), (118, 60), (128, 52), (88, 62), (78, 58), (122, 96), (130, 121), (86, 100), (74, 118))
        motion_lines = (
            f'<g opacity="0.65">'
            f'<line x1="36" y1="54" x2="60" y2="54" stroke="{accent}" stroke-width="2" stroke-linecap="round">'
            f'<animate attributeName="x1" values="42;28;42" dur="{speed:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="64;46;64" dur="{speed:.2f}s" repeatCount="indefinite"/></line>'
            f'<line x1="32" y1="68" x2="54" y2="68" stroke="{accent}" stroke-width="2" stroke-linecap="round">'
            f'<animate attributeName="x1" values="34;24;34" dur="{speed:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="56;40;56" dur="{speed:.2f}s" repeatCount="indefinite"/></line></g>'
        )
        return _render_figure([p1, p2, p3, p2], dur=speed, accent=accent, highlight_arms=True, highlight_legs=True, extra_props=motion_lines)

    # 4. JUMPING JACKS (Front view star jump)
    if exercise_id == "wu-jumping-jacks":
        p_in = _pose((107, 40), (107, 52), (107, 82), (96, 68), (94, 84), (118, 68), (120, 84), (103, 104), (102, 124), (111, 104), (112, 124))
        p_out = _pose((107, 34), (107, 46), (107, 76), (84, 38), (96, 22), (130, 38), (118, 22), (88, 100), (78, 122), (126, 100), (136, 122))
        return _render_figure([p_in, p_out], dur=1.1, accent=accent, highlight_arms=True, highlight_legs=True)

    # 5. ARM CIRCLES / SHOULDER ROTATIONS
    if exercise_id in ("wu-arm-circles", "mob-shoulder-rotations"):
        dur = 1.6 if exercise_id == "wu-arm-circles" else 2.6
        p1 = _pose((107, 38), (107, 50), (107, 82), (86, 52), (68, 52), (128, 52), (146, 52), (101, 104), (99, 124), (113, 104), (115, 124))
        p2 = _pose((107, 38), (107, 50), (107, 82), (92, 34), (96, 20), (122, 34), (118, 20), (101, 104), (99, 124), (113, 104), (115, 124))
        p3 = _pose((107, 38), (107, 50), (107, 82), (94, 68), (92, 82), (120, 68), (122, 82), (101, 104), (99, 124), (113, 104), (115, 124))
        arc = f'<circle cx="107" cy="50" r="34" fill="none" stroke="{accent}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.45"/>'
        return _render_figure([p1, p2, p1, p3], dur=dur, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=arc)

    # 6. DYNAMIC LUNGES / REVERSE LUNGES / HIP FLEXOR STRETCH
    if exercise_id in ("wu-dynamic-lunges", "st-lunges", "str-hip-flexor"):
        p_stand = _pose((106, 36), (106, 48), (106, 79), (96, 64), (102, 76), (116, 64), (110, 76), (103, 102), (102, 124), (109, 102), (110, 124))
        p_lunge = _pose((108, 50), (108, 62), (106, 92), (96, 76), (102, 88), (118, 76), (114, 88), (86, 114), (70, 123), (132, 95), (134, 124))
        if exercise_id == "str-hip-flexor":
            p_kneel1 = _pose((102, 52), (102, 64), (100, 94), (94, 78), (102, 88), (112, 78), (118, 88), (88, 122), (66, 124), (124, 96), (126, 124))
            p_kneel2 = _pose((112, 54), (112, 66), (112, 96), (104, 80), (112, 90), (122, 80), (128, 90), (88, 122), (66, 124), (134, 98), (128, 124))
            return _render_figure([p_kneel1, p_kneel2], dur=2.8, accent=accent, highlight_legs=True)
        return _render_figure([p_stand, p_lunge], dur=2.2, accent=accent, highlight_legs=True)

    # 7. LEG SWINGS
    if exercise_id == "wu-leg-swings":
        wall = '<line x1="66" y1="26" x2="66" y2="126" stroke="#475569" stroke-width="3.5" stroke-linecap="round"/>'
        p_fwd = _pose((102, 36), (102, 48), (102, 79), (84, 54), (68, 54), (114, 62), (118, 76), (102, 102), (102, 124), (128, 86), (150, 84))
        p_mid = _pose((102, 36), (102, 48), (102, 79), (84, 54), (68, 54), (114, 62), (118, 76), (102, 102), (102, 124), (104, 102), (106, 122))
        p_bck = _pose((104, 36), (103, 48), (102, 79), (84, 54), (68, 54), (114, 62), (118, 76), (102, 102), (102, 124), (86, 98), (74, 114))
        return _render_figure([p_fwd, p_mid, p_bck, p_mid], dur=1.6, accent=accent, highlight_legs=True, extra_props=wall)

    # 8. SIDE SHUFFLES / DEFENSIVE SLIDES / SPLIT-STEP / 5-5 SHUTTLE
    if exercise_id in ("wu-side-shuffles", "sp-basketball-defensive-slides", "sp-badminton-split-step", "sp-football-cod-shuttle"):
        p_left = _pose((74, 48), (74, 60), (74, 88), (58, 70), (50, 66), (90, 70), (98, 66), (58, 106), (54, 124), (90, 106), (94, 124))
        p_mid = _pose((107, 44), (107, 56), (107, 84), (92, 66), (84, 62), (122, 66), (130, 62), (98, 104), (96, 122), (116, 104), (118, 122))
        p_right = _pose((140, 48), (140, 60), (140, 88), (124, 70), (116, 66), (156, 70), (164, 66), (124, 106), (120, 124), (156, 106), (160, 124))
        arrows = f'<path d="M44 40 L34 40 M170 40 L180 40" stroke="{accent}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>'
        return _render_figure([p_left, p_mid, p_right, p_mid], dur=1.5, accent=accent, highlight_legs=True, extra_props=arrows)

    # 9. LATERAL LUNGE
    if exercise_id == "sp-badminton-lateral-lunge":
        p_c = _pose((107, 38), (107, 50), (107, 80), (96, 66), (104, 72), (118, 66), (110, 72), (102, 103), (100, 124), (112, 103), (114, 124))
        p_r = _pose((132, 50), (130, 62), (126, 92), (118, 76), (126, 82), (140, 76), (132, 82), (96, 108), (70, 124), (146, 104), (148, 124))
        p_l = _pose((82, 50), (84, 62), (88, 92), (74, 76), (82, 82), (96, 76), (88, 82), (68, 104), (66, 124), (118, 108), (144, 124))
        return _render_figure([p_c, p_r, p_c, p_l], dur=2.6, accent=accent, highlight_legs=True)

    # 10. SQUATS / DEEP SQUAT / GOBLET SQUAT / SINGLE-LEG BOX SQUAT
    if exercise_id in ("st-squats", "mob-deep-squat", "sp-gym-goblet-squat", "bal-single-leg-squats"):
        if exercise_id == "bal-single-leg-squats":
            bench = '<rect x="52" y="96" width="32" height="28" rx="4" fill="#1E293B" stroke="#475569" stroke-width="1.5"/>'
            p_up = _pose((104, 36), (104, 48), (104, 78), (118, 56), (136, 54), (118, 58), (136, 56), (124, 96), (144, 104), (104, 102), (104, 124))
            p_dn = _pose((92, 54), (90, 66), (76, 94), (112, 70), (132, 68), (112, 72), (132, 70), (106, 98), (134, 102), (104, 100), (104, 124))
            return _render_figure([p_up, p_dn], dur=2.4, accent=accent, highlight_legs=True, extra_props=bench)

        p_up = _pose((106, 36), (106, 48), (104, 78), (96, 62), (114, 62), (116, 62), (126, 60), (104, 102), (104, 124), (106, 102), (106, 124))
        depth = 104 if exercise_id == "mob-deep-squat" else 96
        p_dn = _pose((108, 56), (102, 68), (82, depth), (114, 74), (132, 70), (116, 74), (136, 70), (114, 98), (104, 124), (116, 98), (106, 124))
        prop = ""
        if exercise_id == "sp-gym-goblet-squat":
            prop = (
                f'<rect x="112" y="54" width="12" height="16" rx="3" fill="{accent}">'
                f'<animate attributeName="y" values="54;70;54" dur="2.20s" repeatCount="indefinite"/>'
                f'<animate attributeName="x" values="112;114;112" dur="2.20s" repeatCount="indefinite"/></rect>'
            )
        return _render_figure([p_up, p_dn], dur=2.2, accent=accent, highlight_legs=True, extra_props=prop)

    # 11. JUMP & SOFT-LANDING MECHANICS
    if exercise_id == "sp-basketball-landing":
        p_load = _pose((108, 52), (104, 64), (88, 92), (86, 78), (74, 86), (92, 78), (80, 86), (112, 98), (104, 124), (114, 98), (106, 124))
        p_air = _pose((106, 22), (106, 34), (106, 62), (110, 26), (114, 14), (114, 26), (118, 14), (106, 84), (104, 102), (108, 84), (106, 102))
        return _render_figure([p_load, p_air, p_load], dur=1.8, accent=accent, highlight_arms=True, highlight_legs=True)

    # 12. ANKLE MOBILITY (KNEE-TO-WALL) & CALF STRETCH
    if exercise_id in ("mob-ankle-mobility", "str-calf"):
        wall = '<line x1="154" y1="26" x2="154" y2="126" stroke="#475569" stroke-width="3.5" stroke-linecap="round"/>'
        if exercise_id == "mob-ankle-mobility":
            p1 = _pose((112, 54), (112, 66), (106, 94), (126, 68), (150, 66), (126, 70), (150, 68), (94, 122), (70, 124), (128, 96), (132, 124))
            p2 = _pose((122, 56), (122, 68), (118, 96), (134, 70), (150, 66), (134, 72), (150, 68), (94, 122), (70, 124), (146, 98), (132, 124))
            return _render_figure([p1, p2], dur=2.2, accent=accent, highlight_legs=True, extra_props=wall)
        p1 = _pose((116, 40), (118, 52), (108, 82), (134, 56), (150, 56), (134, 58), (150, 58), (94, 104), (78, 124), (126, 102), (126, 124))
        p2 = _pose((124, 42), (126, 54), (116, 84), (138, 58), (150, 56), (138, 60), (150, 58), (96, 104), (78, 124), (136, 102), (126, 124))
        return _render_figure([p1, p2], dur=2.6, accent=accent, highlight_legs=True, extra_props=wall)

    # 13. HIP MOBILITY 90/90 & GROIN BUTTERFLY
    if exercise_id in ("mob-hip-drills", "str-groin"):
        p1 = _pose((107, 54), (107, 66), (107, 102), (92, 84), (84, 102), (122, 84), (130, 102), (82, 100), (74, 122), (132, 104), (142, 122))
        p2 = _pose((107, 54), (107, 66), (107, 102), (92, 84), (84, 102), (122, 84), (130, 102), (74, 114), (96, 122), (140, 114), (118, 122))
        if exercise_id == "mob-hip-drills":
            p3 = _pose((107, 54), (107, 66), (107, 102), (92, 84), (84, 102), (122, 84), (130, 102), (132, 100), (142, 122), (82, 104), (74, 122))
            return _render_figure([p1, p2, p3, p2], dur=2.8, accent=accent, highlight_legs=True)
        return _render_figure([p1, p2], dur=2.6, accent=accent, highlight_legs=True)

    # 14. HAMSTRING STRETCH (Seated hinge)
    if exercise_id == "str-hamstring":
        p1 = _pose((78, 56), (78, 68), (80, 106), (92, 82), (108, 92), (94, 82), (110, 92), (98, 114), (108, 122), (118, 114), (156, 120))
        p2 = _pose((104, 68), (98, 78), (80, 106), (116, 94), (144, 112), (118, 94), (146, 112), (98, 114), (108, 122), (118, 114), (156, 120))
        return _render_figure([p1, p2], dur=2.8, accent=accent, highlight_arms=True, highlight_legs=True)

    # 15. QUADRICEPS STRETCH (Standing heel pull)
    if exercise_id == "str-quadriceps":
        wall = '<line x1="72" y1="26" x2="72" y2="126" stroke="#475569" stroke-width="3.5" stroke-linecap="round"/>'
        p1 = _pose((108, 36), (108, 48), (108, 78), (88, 54), (74, 54), (116, 66), (120, 82), (108, 102), (108, 124), (110, 102), (124, 92))
        p2 = _pose((108, 36), (108, 48), (108, 78), (88, 54), (74, 54), (118, 68), (122, 82), (108, 102), (108, 124), (108, 104), (120, 82))
        return _render_figure([p1, p2], dur=2.6, accent=accent, highlight_legs=True, extra_props=wall)

    # 16. SHOULDER / CHEST / TRICEPS STRETCHES
    if exercise_id in ("str-shoulder", "str-chest", "str-triceps"):
        if exercise_id == "str-triceps":
            p1 = _pose((107, 40), (107, 52), (107, 84), (94, 62), (98, 46), (120, 44), (110, 56), (102, 105), (100, 124), (112, 105), (114, 124))
            p2 = _pose((107, 40), (107, 52), (107, 84), (98, 40), (114, 32), (116, 30), (107, 48), (102, 105), (100, 124), (112, 105), (114, 124))
            return _render_figure([p1, p2], dur=2.6, accent=accent, highlight_arms=True, highlight_legs=False)
        if exercise_id == "str-chest":
            p1 = _pose((107, 40), (107, 52), (107, 84), (86, 56), (76, 46), (128, 56), (138, 46), (102, 105), (100, 124), (112, 105), (114, 124))
            p2 = _pose((107, 40), (107, 52), (107, 84), (76, 52), (62, 40), (138, 52), (152, 40), (102, 105), (100, 124), (112, 105), (114, 124))
            return _render_figure([p1, p2], dur=2.8, accent=accent, highlight_arms=True, highlight_legs=False)
        p1 = _pose((107, 40), (107, 52), (107, 84), (92, 62), (98, 60), (122, 60), (114, 60), (102, 105), (100, 124), (112, 105), (114, 124))
        p2 = _pose((107, 40), (107, 52), (107, 84), (96, 64), (104, 58), (104, 58), (84, 56), (102, 105), (100, 124), (112, 105), (114, 124))
        return _render_figure([p1, p2], dur=2.6, accent=accent, highlight_arms=True, highlight_legs=False)

    # 17. PUSH-UPS
    if exercise_id == "st-pushups":
        p_up = _pose((148, 68), (136, 76), (92, 92), (134, 98), (134, 122), (138, 98), (138, 122), (66, 108), (44, 122), (68, 108), (46, 122))
        p_dn = _pose((150, 96), (138, 104), (92, 110), (126, 102), (134, 122), (130, 102), (138, 122), (66, 116), (44, 122), (68, 116), (46, 122))
        return _render_figure([p_up, p_dn], dur=2.0, accent=accent, highlight_arms=True, highlight_legs=False)

    # 18. PULL-UPS
    if exercise_id == "st-pullups":
        bar = '<line x1="48" y1="24" x2="166" y2="24" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>'
        p_dn = _pose((107, 56), (107, 68), (107, 94), (92, 46), (86, 26), (122, 46), (128, 26), (103, 110), (102, 122), (111, 110), (112, 122))
        p_up = _pose((107, 22), (107, 36), (107, 66), (82, 46), (86, 26), (132, 46), (128, 26), (103, 86), (102, 104), (111, 86), (112, 104))
        return _render_figure([p_dn, p_up], dur=2.2, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=bar)

    # 19. FOREARM PLANK & SIDE PLANK
    if exercise_id in ("st-planks", "bal-side-plank"):
        p1 = _pose((150, 86), (136, 92), (90, 96), (134, 114), (150, 120), (136, 116), (154, 120), (66, 108), (44, 122), (68, 108), (46, 122))
        p2 = _pose((150, 84), (136, 90), (90, 93), (134, 114), (150, 120), (136, 116), (154, 120), (66, 106), (44, 122), (68, 106), (46, 122))
        pulse = (
            f'<ellipse cx="106" cy="96" rx="22" ry="7" fill="{accent}" opacity="0.18">'
            f'<animate attributeName="opacity" values="0.12;0.34;0.12" dur="2.0s" repeatCount="indefinite"/></ellipse>'
        )
        return _render_figure([p1, p2], dur=2.0, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=pulse)

    # 20. GLUTE BRIDGES
    if exercise_id == "st-glute-bridges":
        p_dn = _pose((52, 114), (66, 118), (106, 118), (82, 120), (102, 122), (84, 120), (104, 122), (128, 94), (144, 122), (130, 94), (146, 122))
        p_up = _pose((52, 114), (66, 116), (104, 92), (82, 120), (102, 122), (84, 120), (104, 122), (132, 86), (144, 122), (134, 86), (146, 122))
        return _render_figure([p_dn, p_up], dur=2.2, accent=accent, highlight_legs=True)

    # 21. STANDING CALF RAISES
    if exercise_id == "st-calf-raises":
        p_dn = _pose((107, 42), (107, 54), (107, 84), (96, 70), (96, 84), (118, 70), (118, 84), (103, 104), (103, 124), (111, 104), (111, 124))
        p_up = _pose((107, 30), (107, 42), (107, 72), (96, 58), (96, 72), (118, 58), (118, 72), (103, 94), (103, 121), (111, 94), (111, 121))
        return _render_figure([p_dn, p_up], dur=1.8, accent=accent, highlight_legs=True)

    # 22. ROMANIAN DEADLIFTS (DUMBBELL)
    if exercise_id == "st-deadlifts":
        p_up = _pose((108, 36), (106, 48), (102, 78), (108, 66), (112, 86), (110, 66), (114, 86), (104, 102), (104, 124), (106, 102), (106, 124))
        p_dn = _pose((136, 62), (124, 68), (86, 80), (122, 88), (120, 108), (124, 88), (122, 108), (102, 102), (104, 124), (104, 102), (106, 124))
        db = (
            f'<circle cx="114" cy="88" r="5" fill="{accent}">'
            f'<animate attributeName="cx" values="114;122;114" dur="2.40s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="88;110;88" dur="2.40s" repeatCount="indefinite"/></circle>'
        )
        return _render_figure([p_up, p_dn], dur=2.4, accent=accent, highlight_arms=True, highlight_legs=True, extra_props=db)

    # 23. SINGLE-ARM DUMBBELL ROW
    if exercise_id == "sp-gym-dumbbell-row":
        p_dn = _pose((136, 56), (124, 64), (86, 80), (122, 84), (114, 100), (124, 86), (124, 108), (84, 104), (78, 124), (114, 102), (118, 124))
        p_up = _pose((136, 56), (124, 64), (86, 80), (122, 84), (114, 100), (104, 62), (100, 82), (84, 104), (78, 124), (114, 102), (118, 124))
        db = (
            f'<circle cx="124" cy="110" r="5" fill="{accent}">'
            f'<animate attributeName="cx" values="124;100;124" dur="1.90s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="110;84;110" dur="1.90s" repeatCount="indefinite"/></circle>'
        )
        return _render_figure([p_dn, p_up], dur=1.9, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=db)

    # 24. CYCLING / LOW-INTENSITY RECOVERY CYCLING
    if exercise_id in ("cardio-cycling", "rec-low-cycling"):
        dur = 1.1 if exercise_id == "cardio-cycling" else 1.7
        bike = (
            '<circle cx="132" cy="108" r="16" fill="none" stroke="#475569" stroke-width="2.5"/>'
            '<line x1="76" y1="86" x2="108" y2="108" stroke="#475569" stroke-width="2.5"/>'
            '<line x1="108" y1="108" x2="132" y2="72" stroke="#475569" stroke-width="2.5"/>'
            '<line x1="126" y1="70" x2="140" y2="70" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>'
        )
        p1 = _pose((112, 42), (104, 54), (82, 82), (118, 62), (134, 70), (120, 62), (136, 70), (102, 88), (116, 104), (104, 100), (100, 116))
        p2 = _pose((112, 42), (104, 54), (82, 82), (118, 62), (134, 70), (120, 62), (136, 70), (104, 100), (100, 116), (102, 88), (116, 104))
        return _render_figure([p1, p2], dur=dur, accent=accent, highlight_legs=True, extra_props=bike)

    # 25. JUMP ROPE CONDITIONING
    if exercise_id == "cardio-jump-rope":
        p_dn = _pose((107, 42), (107, 54), (107, 84), (92, 68), (82, 74), (122, 68), (132, 74), (103, 105), (102, 124), (111, 105), (112, 124))
        p_up = _pose((107, 32), (107, 44), (107, 74), (92, 58), (82, 64), (122, 58), (132, 64), (103, 95), (102, 114), (111, 95), (112, 114))
        rope = (
            f'<path d="M82 74 Q107 132 132 74" fill="none" stroke="{accent}" stroke-width="2" stroke-dasharray="3 2">'
            f'<animate attributeName="d" values="M82 74 Q107 134 132 74;M82 64 Q107 10 132 64;M82 74 Q107 134 132 74" dur="0.75s" repeatCount="indefinite"/>'
            f"</path>"
        )
        return _render_figure([p_dn, p_up], dur=0.75, accent=accent, highlight_arms=True, highlight_legs=True, extra_props=rope)

    # 26. LAP SWIMMING
    if exercise_id == "cardio-swimming":
        water = (
            f'<path d="M24 96 Q44 90 64 96 T104 96 T144 96 T184 96" fill="none" stroke="{accent}" stroke-width="2" opacity="0.55">'
            f'<animate attributeName="d" values="M24 96 Q44 90 64 96 T104 96 T144 96 T184 96;M24 96 Q44 102 64 96 T104 96 T144 96 T184 96;M24 96 Q44 90 64 96 T104 96 T144 96 T184 96" dur="1.4s" repeatCount="indefinite"/>'
            f"</path>"
        )
        p1 = _pose((144, 72), (130, 76), (86, 80), (146, 62), (166, 70), (112, 92), (96, 88), (64, 76), (40, 72), (64, 86), (40, 92))
        p2 = _pose((144, 72), (130, 76), (86, 80), (112, 92), (96, 88), (146, 62), (166, 70), (64, 86), (40, 92), (64, 76), (40, 72))
        return _render_figure([p1, p2], dur=1.2, accent=accent, highlight_arms=True, highlight_legs=True, extra_props=water)

    # 27. SINGLE-LEG BALANCE HOLD
    if exercise_id == "bal-single-leg":
        p1 = _pose((107, 36), (107, 48), (107, 79), (86, 56), (66, 58), (128, 56), (148, 54), (107, 102), (107, 124), (124, 92), (120, 110))
        p2 = _pose((109, 36), (108, 48), (107, 79), (86, 52), (66, 50), (128, 60), (148, 62), (107, 102), (107, 124), (126, 90), (122, 108))
        return _render_figure([p1, p2], dur=2.2, accent=accent, highlight_arms=True, highlight_legs=True)

    # 28. BIRD DOG
    if exercise_id == "bal-bird-dog":
        p_base = _pose((142, 74), (130, 82), (86, 84), (128, 102), (128, 122), (132, 102), (132, 122), (84, 104), (72, 122), (88, 104), (76, 122))
        p_ext1 = _pose((144, 74), (130, 82), (86, 84), (128, 102), (128, 122), (150, 76), (172, 74), (62, 82), (38, 80), (88, 104), (76, 122))
        p_ext2 = _pose((144, 74), (130, 82), (86, 84), (150, 76), (172, 74), (132, 102), (132, 122), (84, 104), (72, 122), (62, 82), (38, 80))
        return _render_figure([p_base, p_ext1, p_base, p_ext2], dur=3.0, accent=accent, highlight_arms=True, highlight_legs=True)

    # 29. DEAD BUG
    if exercise_id == "bal-dead-bug":
        p_c = _pose((56, 112), (70, 118), (112, 118), (72, 96), (72, 76), (76, 96), (76, 76), (112, 94), (134, 94), (116, 94), (138, 94))
        p_1 = _pose((56, 112), (70, 118), (112, 118), (72, 96), (72, 76), (52, 106), (34, 114), (136, 112), (164, 116), (116, 94), (138, 94))
        p_2 = _pose((56, 112), (70, 118), (112, 118), (52, 106), (34, 114), (76, 96), (76, 76), (112, 94), (134, 94), (136, 112), (164, 116))
        return _render_figure([p_c, p_1, p_c, p_2], dur=3.0, accent=accent, highlight_arms=True, highlight_legs=True)

    # 30. THORACIC ROTATIONS (OPEN BOOK)
    if exercise_id == "mob-thoracic-rotations":
        p_closed = _pose((112, 76), (102, 86), (74, 108), (120, 88), (144, 90), (122, 86), (146, 88), (104, 116), (86, 122), (106, 114), (88, 122))
        p_open = _pose((104, 74), (102, 86), (74, 108), (120, 88), (144, 90), (84, 62), (62, 52), (104, 116), (86, 122), (106, 114), (88, 122))
        return _render_figure([p_closed, p_open], dur=2.8, accent=accent, highlight_arms=True, highlight_legs=False)

    # 31. WRIST MOBILITY ROCKS & CAT-COW SPINAL MOBILITY
    if exercise_id in ("mob-wrist-mobility", "rec-gentle-mobility"):
        if exercise_id == "mob-wrist-mobility":
            p1 = _pose((136, 74), (124, 82), (82, 84), (126, 102), (128, 122), (130, 102), (132, 122), (80, 106), (62, 122), (84, 106), (66, 122))
            p2 = _pose((148, 74), (136, 82), (94, 84), (132, 102), (128, 122), (136, 102), (132, 122), (84, 106), (62, 122), (88, 106), (66, 122))
            return _render_figure([p1, p2], dur=2.2, accent=accent, highlight_arms=True, highlight_legs=False)
        p_cat = _pose((140, 82), (128, 76), (82, 82), (128, 100), (128, 122), (132, 100), (132, 122), (80, 106), (64, 122), (84, 106), (68, 122))
        p_cow = _pose((144, 68), (130, 88), (82, 88), (128, 104), (128, 122), (132, 104), (132, 122), (80, 106), (64, 122), (84, 106), (68, 122))
        return _render_figure([p_cat, p_cow], dur=2.8, accent=accent, highlight_arms=False, highlight_legs=False)

    # 32. GENTLE STRETCHING (CHILD'S POSE)
    if exercise_id == "rec-gentle-stretching":
        p1 = _pose((126, 86), (114, 92), (76, 102), (136, 104), (158, 120), (138, 104), (160, 120), (92, 120), (62, 122), (94, 120), (64, 122))
        p2 = _pose((128, 104), (112, 106), (72, 108), (138, 114), (168, 122), (140, 114), (170, 122), (92, 120), (62, 122), (94, 120), (64, 122))
        return _render_figure([p1, p2], dur=3.2, accent=accent, highlight_arms=True, highlight_legs=False)

    # 33. DIAPHRAGMATIC BOX BREATHING
    if exercise_id == "rec-breathing":
        p1 = _pose((52, 114), (66, 118), (108, 118), (82, 110), (96, 112), (84, 110), (98, 112), (130, 96), (146, 122), (132, 96), (148, 122))
        p2 = _pose((52, 114), (66, 116), (108, 116), (82, 104), (96, 104), (84, 104), (98, 104), (130, 96), (146, 122), (132, 96), (148, 122))
        aura = (
            f'<circle cx="96" cy="74" r="14" fill="{accent}" fill-opacity="0.16" stroke="{accent}" stroke-width="1.8">'
            f'<animate attributeName="r" values="12;26;26;12;12" dur="4.0s" repeatCount="indefinite"/>'
            f'<animate attributeName="fill-opacity" values="0.10;0.28;0.28;0.10;0.10" dur="4.0s" repeatCount="indefinite"/>'
            f"</circle>"
        )
        return _render_figure([p1, p2], dur=4.0, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=aura)

    # 34. ROTATIONAL CORE CHOP / BANDED EXTERNAL ROTATION
    if exercise_id in ("sp-cricket-rotational-core", "sp-tennis-external-rotation"):
        anchor = (
            f'<line x1="36" y1="66" x2="108" y2="66" stroke="{accent}" stroke-width="2" stroke-dasharray="4 3">'
            f'<animate attributeName="x2" values="84;142;84" dur="2.0s" repeatCount="indefinite"/></line>'
            '<line x1="36" y1="30" x2="36" y2="126" stroke="#475569" stroke-width="3.5" stroke-linecap="round"/>'
        )
        p1 = _pose((108, 38), (108, 50), (108, 82), (92, 64), (82, 66), (96, 66), (84, 66), (98, 104), (94, 124), (118, 104), (122, 124))
        p2 = _pose((112, 38), (110, 50), (108, 82), (124, 64), (140, 66), (128, 66), (144, 66), (98, 104), (94, 124), (118, 104), (122, 124))
        return _render_figure([p1, p2], dur=2.0, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=anchor)

    # 35. SCAPULAR WALL SLIDES
    if exercise_id == "sp-cricket-scapular-slides":
        wall = '<line x1="68" y1="24" x2="68" y2="126" stroke="#475569" stroke-width="3.5" stroke-linecap="round"/>'
        p_w = _pose((107, 42), (107, 54), (107, 84), (86, 62), (82, 46), (128, 62), (132, 46), (102, 104), (100, 124), (112, 104), (114, 124))
        p_y = _pose((107, 42), (107, 54), (107, 84), (90, 38), (82, 22), (124, 38), (132, 22), (102, 104), (100, 124), (112, 104), (114, 124))
        return _render_figure([p_w, p_y], dur=2.4, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=wall)

    # 36. PRONE Y-T-W ACTIVATION
    if exercise_id == "sp-swimming-ytw-activation":
        p_rest = _pose((144, 110), (128, 114), (82, 118), (142, 118), (160, 120), (144, 118), (162, 120), (58, 120), (36, 122), (60, 120), (38, 122))
        p_y = _pose((146, 102), (128, 110), (82, 118), (148, 94), (170, 86), (150, 94), (172, 86), (58, 120), (36, 122), (60, 120), (38, 122))
        p_w = _pose((146, 102), (128, 110), (82, 118), (118, 96), (132, 92), (120, 96), (134, 92), (58, 120), (36, 122), (60, 120), (38, 122))
        return _render_figure([p_rest, p_y, p_w], dur=2.6, accent=accent, highlight_arms=True, highlight_legs=False)

    # 37. CARIOCA / 6-CORNER GHOSTING / SKATER BOUNDS
    if exercise_id in ("wu-carioca-footwork", "sp-badminton-skater-bounds", "sp-badminton-six-corner-ghosting"):
        p_l = _pose((72, 46), (72, 58), (74, 86), (56, 66), (48, 58), (90, 68), (100, 62), (64, 106), (58, 124), (92, 104), (104, 116))
        p_mid = _pose((107, 36), (107, 48), (107, 76), (88, 56), (78, 52), (126, 56), (136, 52), (98, 98), (94, 114), (116, 98), (120, 114))
        p_r = _pose((142, 46), (142, 58), (140, 86), (124, 68), (114, 62), (158, 66), (166, 58), (122, 104), (110, 116), (150, 106), (156, 124))
        return _render_figure([p_l, p_mid, p_r, p_mid], dur=1.35, accent=accent, highlight_arms=True, highlight_legs=True)

    # 38. INCHWORM TO WORLD'S GREATEST LUNGE FLOW
    if exercise_id == "wu-inchworm-spiderman":
        p_stand = _pose((84, 38), (84, 50), (84, 80), (86, 66), (88, 82), (88, 66), (90, 82), (84, 102), (84, 124), (86, 102), (86, 124))
        p_plank = _pose((152, 74), (140, 82), (94, 94), (138, 102), (138, 122), (142, 102), (142, 122), (68, 108), (46, 122), (70, 108), (48, 122))
        p_open = _pose((136, 62), (126, 72), (92, 94), (132, 96), (136, 122), (128, 46), (132, 24), (68, 108), (46, 122), (130, 98), (134, 122))
        return _render_figure([p_stand, p_plank, p_open, p_plank], dur=3.2, accent=accent, highlight_arms=True, highlight_legs=True)

    # 39. COSSACK SQUAT MOBILITY
    if exercise_id == "mob-cossack-squat":
        p_r = _pose((136, 58), (134, 70), (132, 102), (124, 80), (134, 74), (144, 80), (154, 74), (94, 114), (58, 122), (150, 102), (144, 124))
        p_m = _pose((107, 46), (107, 58), (107, 88), (94, 70), (104, 68), (120, 70), (110, 68), (84, 106), (68, 124), (130, 106), (146, 124))
        p_l = _pose((78, 58), (80, 70), (82, 102), (70, 80), (60, 74), (90, 80), (80, 74), (64, 102), (70, 124), (120, 114), (156, 122))
        return _render_figure([p_r, p_m, p_l, p_m], dur=3.0, accent=accent, highlight_legs=True)

    # 40. OVERHEAD SQUAT MOBILITY / DUMBBELL THRUSTERS
    if exercise_id in ("mob-overhead-squat-drill", "sp-gym-dumbbell-thrusters"):
        p_up = _pose((107, 38), (107, 50), (107, 80), (96, 32), (90, 16), (118, 32), (124, 16), (102, 102), (100, 124), (112, 102), (114, 124))
        p_dn = _pose((107, 58), (104, 70), (92, 98), (92, 48), (88, 30), (118, 48), (124, 30), (112, 100), (100, 124), (116, 100), (114, 124))
        bar = (
            f'<line x1="82" y1="16" x2="132" y2="16" stroke="{accent}" stroke-width="3" stroke-linecap="round">'
            f'<animate attributeName="y1" values="16;30;16" dur="2.20s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="16;30;16" dur="2.20s" repeatCount="indefinite"/></line>'
        )
        return _render_figure([p_up, p_dn], dur=2.2, accent=accent, highlight_arms=True, highlight_legs=True, extra_props=bar)

    # 41. COUCH STRETCH & BULGARIAN SPLIT SQUAT (Bench rear-foot elevated)
    if exercise_id in ("str-couch-stretch", "st-bulgarian-split-squat"):
        bench = '<rect x="44" y="92" width="32" height="32" rx="4" fill="#1E293B" stroke="#475569" stroke-width="1.5"/>'
        if exercise_id == "str-couch-stretch":
            p1 = _pose((112, 50), (110, 62), (106, 92), (100, 76), (110, 86), (118, 76), (124, 86), (92, 122), (62, 94), (134, 96), (136, 124))
            p2 = _pose((118, 52), (116, 64), (114, 94), (106, 78), (116, 88), (124, 78), (130, 88), (92, 122), (62, 94), (142, 98), (136, 124))
            return _render_figure([p1, p2], dur=2.8, accent=accent, highlight_legs=True, extra_props=bench)
        p_up = _pose((114, 36), (114, 48), (112, 78), (104, 64), (108, 78), (124, 64), (120, 78), (88, 96), (66, 92), (126, 102), (130, 124))
        p_dn = _pose((114, 54), (112, 66), (106, 96), (102, 80), (106, 94), (122, 80), (118, 94), (88, 114), (66, 92), (136, 98), (130, 124))
        return _render_figure([p_up, p_dn], dur=2.2, accent=accent, highlight_legs=True, extra_props=bench)

    # 42. PNF HAMSTRING STRETCH & 90/90 WALL BREATHING DECOMPRESSION
    if exercise_id in ("str-pnf-hamstring", "rec-contrast-breathing-decompression"):
        if exercise_id == "str-pnf-hamstring":
            p1 = _pose((50, 114), (64, 118), (108, 118), (82, 100), (106, 74), (84, 100), (108, 74), (134, 120), (162, 122), (114, 88), (118, 58))
            p2 = _pose((50, 114), (64, 118), (108, 118), (80, 96), (96, 68), (82, 96), (98, 68), (134, 120), (162, 122), (104, 84), (98, 54))
            return _render_figure([p1, p2], dur=2.8, accent=accent, highlight_legs=True)
        box = '<rect x="138" y="88" width="38" height="36" rx="4" fill="#1E293B" stroke="#475569" stroke-width="1.5"/>'
        p1 = _pose((48, 114), (62, 118), (106, 118), (78, 110), (94, 112), (80, 110), (96, 112), (118, 86), (154, 86), (120, 86), (156, 86))
        p2 = _pose((48, 114), (62, 116), (106, 116), (78, 104), (94, 104), (80, 104), (96, 104), (118, 86), (154, 86), (120, 86), (156, 86))
        aura = (
            f'<circle cx="92" cy="70" r="14" fill="{accent}" fill-opacity="0.16" stroke="{accent}" stroke-width="1.8">'
            f'<animate attributeName="r" values="11;24;24;11" dur="4.2s" repeatCount="indefinite"/></circle>'
        )
        return _render_figure([p1, p2], dur=4.2, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=box + aura)

    # 43. NORDIC HAMSTRING ECCENTRIC LOWERS
    if exercise_id == "st-nordic-hamstring":
        p_up = _pose((104, 48), (104, 60), (102, 90), (108, 74), (116, 82), (112, 74), (120, 82), (98, 120), (62, 122), (100, 120), (64, 122))
        p_dn = _pose((152, 86), (140, 92), (114, 104), (144, 106), (156, 122), (148, 106), (160, 122), (98, 120), (62, 122), (100, 120), (64, 122))
        return _render_figure([p_up, p_dn], dur=3.2, accent=accent, highlight_legs=True)

    # 44. SINGLE-LEG ROMANIAN DEADLIFT
    if exercise_id == "st-single-leg-rdl":
        p_up = _pose((106, 36), (106, 48), (106, 78), (108, 66), (110, 84), (110, 66), (112, 84), (104, 102), (104, 124), (108, 102), (108, 124))
        p_hinge = _pose((146, 68), (132, 72), (96, 78), (132, 92), (132, 110), (134, 92), (134, 110), (70, 74), (44, 72), (102, 102), (106, 124))
        return _render_figure([p_up, p_hinge], dur=2.6, accent=accent, highlight_legs=True)

    # 45. PIKE PUSH-UPS
    if exercise_id == "st-pike-pushups":
        p_up = _pose((130, 82), (120, 76), (92, 46), (130, 98), (136, 122), (134, 98), (140, 122), (76, 84), (58, 122), (78, 84), (60, 122))
        p_dn = _pose((144, 106), (130, 94), (96, 56), (124, 104), (136, 122), (128, 104), (140, 122), (78, 88), (58, 122), (80, 88), (60, 122))
        return _render_figure([p_up, p_dn], dur=2.1, accent=accent, highlight_arms=True, highlight_legs=False)

    # 46. SINGLE-LEG ECCENTRIC CALF RAISES & POGO HOPS
    if exercise_id in ("st-heavy-calf-eccentric", "sp-running-pogo-hops"):
        dur = 0.68 if exercise_id == "sp-running-pogo-hops" else 2.4
        p_dn = _pose((107, 40), (107, 52), (107, 82), (96, 66), (94, 78), (118, 66), (120, 78), (103, 104), (103, 124), (111, 104), (111, 124))
        p_up = _pose((107, 24), (107, 36), (107, 66), (96, 50), (94, 62), (118, 50), (120, 62), (103, 88), (103, 110), (111, 88), (111, 110))
        return _render_figure([p_dn, p_up], dur=dur, accent=accent, highlight_legs=True)

    # 47. TABATA / TEMPO / RSA SPRINTS / BETWEEN-WICKETS SHUTTLE
    if exercise_id in ("cardio-tabata-sprints", "cardio-tempo-threshold", "sp-football-rsa-sprints", "sp-cricket-between-wickets-shuttle"):
        speed = 0.65 if exercise_id != "cardio-tempo-threshold" else 0.92
        p1 = _pose((116, 38), (112, 50), (102, 78), (86, 60), (74, 54), (124, 58), (136, 48), (82, 100), (66, 116), (126, 94), (138, 118))
        p2 = _pose((116, 34), (112, 46), (102, 74), (108, 60), (114, 56), (108, 60), (114, 56), (104, 98), (98, 120), (108, 96), (106, 116))
        p3 = _pose((116, 38), (112, 50), (102, 78), (124, 58), (136, 48), (86, 60), (74, 54), (126, 94), (138, 118), (82, 100), (66, 116))
        return _render_figure([p1, p2, p3, p2], dur=speed, accent=accent, highlight_arms=True, highlight_legs=True)

    # 48. DOUBLE-UNDER JUMP ROPE
    if exercise_id == "cardio-double-under-rope":
        p_dn = _pose((107, 42), (107, 54), (107, 84), (92, 68), (82, 74), (122, 68), (132, 74), (103, 105), (102, 124), (111, 105), (112, 124))
        p_up = _pose((107, 26), (107, 38), (107, 68), (92, 52), (82, 58), (122, 52), (132, 58), (103, 89), (102, 108), (111, 89), (112, 108))
        rope = (
            f'<path d="M82 74 Q107 134 132 74" fill="none" stroke="{accent}" stroke-width="2">'
            f'<animate attributeName="d" values="M82 74 Q107 134 132 74;M82 58 Q107 6 132 58;M82 74 Q107 134 132 74" dur="0.45s" repeatCount="indefinite"/></path>'
        )
        return _render_figure([p_dn, p_up], dur=0.72, accent=accent, highlight_arms=True, highlight_legs=True, extra_props=rope)

    # 49. COPENHAGEN ADDUCTOR PLANK & HOLLOW BODY HOLD
    if exercise_id in ("bal-copenhagen-plank", "bal-hollow-body-hold"):
        if exercise_id == "bal-copenhagen-plank":
            bench = '<rect x="34" y="94" width="38" height="30" rx="4" fill="#1E293B" stroke="#475569" stroke-width="1.5"/>'
            p1 = _pose((152, 86), (138, 92), (96, 94), (136, 112), (150, 120), (136, 74), (136, 56), (72, 110), (54, 114), (74, 94), (50, 94))
            p2 = _pose((152, 82), (138, 88), (96, 88), (136, 112), (150, 120), (136, 70), (136, 52), (74, 104), (56, 108), (74, 92), (50, 94))
            return _render_figure([p1, p2], dur=2.2, accent=accent, highlight_legs=True, extra_props=bench)
        p1 = _pose((66, 104), (78, 112), (114, 116), (52, 98), (34, 92), (54, 98), (36, 92), (140, 108), (168, 98), (142, 108), (170, 98))
        p2 = _pose((66, 100), (78, 110), (114, 116), (52, 94), (34, 86), (54, 94), (36, 86), (140, 104), (168, 92), (142, 104), (170, 92))
        return _render_figure([p1, p2], dur=2.4, accent=accent, highlight_arms=True, highlight_legs=True)

    # 50. PALLOF PRESS / BAND PULL-APARTS / SWIM-CORD PULL / SERVE POWER SLAMS / FOREARM ECCENTRICS
    if exercise_id in ("bal-pallof-press", "sp-swimming-band-pull-aparts", "sp-swimming-band-pull", "sp-tennis-serve-power-slams", "sp-tennis-forearm-eccentrics"):
        if exercise_id == "sp-swimming-band-pull":
            anchor = '<line x1="168" y1="36" x2="168" y2="126" stroke="#475569" stroke-width="3.5"/>'
            band = (
                f'<line x1="168" y1="74" x2="148" y2="74" stroke="{accent}" stroke-width="2" stroke-dasharray="4 3">'
                f'<animate attributeName="x2" values="148;90;148" dur="2.0s" repeatCount="indefinite"/>'
                f'<animate attributeName="y2" values="74;86;74" dur="2.0s" repeatCount="indefinite"/></line>'
            )
            p1 = _pose((126, 56), (114, 62), (76, 80), (132, 68), (148, 74), (134, 68), (150, 74), (78, 102), (74, 124), (82, 102), (78, 124))
            p2 = _pose((126, 56), (114, 62), (76, 80), (104, 78), (88, 86), (106, 78), (90, 86), (78, 102), (74, 124), (82, 102), (78, 124))
            return _render_figure([p1, p2], dur=2.0, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=anchor + band)
        if exercise_id == "sp-tennis-serve-power-slams":
            p_hi = _pose((104, 36), (104, 48), (104, 80), (112, 34), (120, 18), (118, 32), (128, 16), (96, 102), (90, 124), (114, 102), (118, 124))
            p_lo = _pose((112, 48), (108, 60), (102, 86), (88, 76), (72, 92), (92, 76), (76, 92), (96, 104), (90, 124), (116, 104), (120, 124))
            return _render_figure([p_hi, p_lo], dur=1.5, accent=accent, highlight_arms=True, highlight_legs=False)
        p1 = _pose((107, 40), (107, 52), (107, 84), (96, 60), (102, 60), (118, 60), (112, 60), (102, 104), (100, 124), (112, 104), (114, 124))
        p2 = _pose((107, 40), (107, 52), (107, 84), (80, 56), (62, 56), (134, 56), (152, 56), (102, 104), (100, 124), (112, 104), (114, 124))
        band = (
            f'<line x1="102" y1="60" x2="112" y2="60" stroke="{accent}" stroke-width="2.5">'
            f'<animate attributeName="x1" values="102;62;102" dur="2.0s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="112;152;112" dur="2.0s" repeatCount="indefinite"/></line>'
        )
        return _render_figure([p1, p2], dur=2.0, accent=accent, highlight_arms=True, highlight_legs=False, extra_props=band)

    # 51. PISTOL SQUAT, DEPTH JUMP, BURPEE BROAD JUMP
    if exercise_id in ("bal-pistol-squat-progression", "sp-basketball-depth-jump", "sp-gym-burpee-broad-jump"):
        if exercise_id == "bal-pistol-squat-progression":
            p_up = _pose((100, 36), (100, 48), (100, 78), (116, 56), (136, 54), (118, 56), (138, 54), (124, 92), (148, 96), (100, 102), (100, 124))
            p_dn = _pose((96, 62), (92, 74), (82, 104), (114, 78), (136, 76), (116, 78), (138, 76), (118, 104), (146, 104), (108, 102), (100, 124))
            return _render_figure([p_up, p_dn], dur=2.6, accent=accent, highlight_legs=True)
        if exercise_id == "sp-basketball-depth-jump":
            box = '<rect x="38" y="96" width="36" height="28" rx="4" fill="#1E293B" stroke="#475569" stroke-width="1.5"/>'
            p_box = _pose((58, 28), (58, 40), (58, 66), (52, 52), (56, 64), (66, 52), (70, 64), (58, 82), (58, 96), (62, 82), (62, 96))
            p_land = _pose((112, 54), (108, 66), (96, 94), (96, 78), (86, 86), (100, 78), (90, 86), (116, 100), (110, 124), (118, 100), (112, 124))
            p_jump = _pose((126, 20), (126, 32), (126, 60), (126, 24), (130, 12), (130, 24), (134, 12), (126, 82), (124, 100), (128, 82), (126, 100))
            return _render_figure([p_box, p_land, p_jump, p_land], dur=2.2, accent=accent, highlight_arms=True, highlight_legs=True, extra_props=box)
        p_plank = _pose((128, 86), (116, 92), (74, 104), (114, 108), (114, 122), (118, 108), (118, 122), (54, 114), (36, 122), (56, 114), (38, 122))
        p_leap = _pose((144, 34), (136, 46), (118, 72), (150, 42), (166, 36), (152, 44), (168, 38), (130, 92), (144, 106), (124, 92), (138, 106))
        p_land = _pose((152, 54), (146, 66), (132, 94), (154, 72), (168, 70), (156, 72), (170, 70), (152, 100), (146, 124), (154, 100), (148, 124))
        return _render_figure([p_plank, p_leap, p_land], dur=2.2, accent=accent, highlight_arms=True, highlight_legs=True)

    # Fallback dynamic athletic motion
    p1 = _pose((107, 38), (107, 50), (107, 80), (92, 62), (82, 56), (122, 62), (132, 56), (102, 102), (100, 124), (112, 102), (114, 124))
    p2 = _pose((107, 46), (107, 58), (107, 88), (92, 68), (82, 60), (122, 68), (132, 60), (96, 106), (96, 124), (118, 106), (118, 124))
    return _render_figure([p1, p2], dur=2.0, accent=accent, highlight_arms=True, highlight_legs=True)


def build_exercise_svg(exercise: dict[str, Any]) -> str:
    """Render a GOWOD / Nike studio-style animated SVG demonstration card."""
    accent = CATEGORY_ACCENTS.get(exercise["category"], "#00D4FF")
    title = escape(exercise["name"][:34] + ("..." if len(exercise["name"]) > 34 else ""))
    category = escape(exercise["category"].upper())
    difficulty = escape(exercise["difficulty_level"].upper())
    muscles = escape(" · ".join(exercise["target_muscles"][:3]))
    prescription = escape(f"{exercise['recommended_sets']} SETS × {exercise['recommended_reps']}")
    animated_scene = _get_exercise_animation(exercise["id"], exercise["category"], accent)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 162" width="480" height="162" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#121318"/>
      <stop offset="100%" stop-color="#09090B"/>
    </linearGradient>
    <radialGradient id="studioGlow" cx="22%" cy="54%" r="44%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="topBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.1"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="478" height="160" rx="16" fill="url(#bg)" stroke="#242632" stroke-width="1.5"/>
  <rect x="1" y="1" width="478" height="160" rx="16" fill="url(#studioGlow)"/>
  <rect x="16" y="1" width="182" height="2.5" rx="1" fill="url(#topBar)"/>
  <!-- GOWOD-style dark motion studio stage -->
  <rect x="14" y="14" width="186" height="134" rx="12" fill="#08090C" stroke="#22242F" stroke-width="1.2"/>
  <line x1="22" y1="126" x2="192" y2="126" stroke="#27272A" stroke-width="1.5"/>
  <line x1="44" y1="133" x2="170" y2="133" stroke="#18181B" stroke-width="1"/>
  {animated_scene}
  <!-- Live tempo pulse indicator -->
  <circle cx="28" cy="26" r="3.2" fill="{accent}">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.3s" repeatCount="indefinite"/>
  </circle>
  <text x="36" y="29" font-family="Inter, Arial, sans-serif" font-size="8" font-weight="700" fill="#A1A1AA" letter-spacing="1.1">MOTION DEMO</text>
  <!-- Right telemetry panel -->
  <rect x="216" y="16" width="248" height="22" rx="6" fill="{accent}" fill-opacity="0.13" stroke="{accent}" stroke-opacity="0.28" stroke-width="0.8"/>
  <text x="226" y="30.5" font-family="Inter, Arial, sans-serif" font-size="9.5" font-weight="700" fill="{accent}" letter-spacing="1.1">{category}</text>
  <text x="216" y="65" font-family="Inter, Arial, sans-serif" font-size="15.5" font-weight="700" fill="#FAFAFA">{title}</text>
  <text x="216" y="88" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="500" fill="#9CA3AF">{muscles}</text>
  <rect x="216" y="106" width="104" height="26" rx="7" fill="#181A22" stroke="#272A36" stroke-width="1"/>
  <text x="226" y="122.5" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="700" fill="#E4E4E7" letter-spacing="0.7">{difficulty}</text>
  <rect x="328" y="106" width="136" height="26" rx="7" fill="#181A22" stroke="{accent}" stroke-opacity="0.35" stroke-width="1"/>
  <text x="338" y="122.5" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="700" fill="{accent}" letter-spacing="0.4">{prescription[:21]}</text>
  <rect x="216" y="142" width="248" height="3" rx="1.5" fill="#1F222E"/>
  <rect x="216" y="142" width="70" height="3" rx="1.5" fill="{accent}">
    <animate attributeName="x" values="216;394;216" dur="2.6s" repeatCount="indefinite"/>
  </rect>
</svg>
"""


def ensure_exercise_visual(exercise: dict[str, Any], overwrite: bool = False) -> str:
    """Create (or regenerate) the animated local SVG file and return its relative path."""
    images_dir: Path = config.ASSETS_DIR / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{exercise['id']}.svg"
    target = images_dir / filename
    if overwrite or not target.exists():
        target.write_text(build_exercise_svg(exercise), encoding="utf-8")
    return f"assets/images/{filename}"
