"""Reusable WHOOP / GOWOD / Darebee UI components and demo-account helper."""

from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st

import config
from athlete import (
    get_athlete_profile,
    get_user_feedback_map,
    save_athlete_profile,
    save_exercise_feedback,
)
from authentication import authenticate_user, register_user
from recommendation import generate_workout_routine, save_workout_routine
from training import generate_balanced_weekly_plan, log_completed_workout

DEMO_EMAIL = "demo@fitmotion.ai"
DEMO_PASSWORD = "FitMotion2026!"


def navigate_to(page_key: str) -> None:
    """Programmatically switch the active sidebar page and rerun cleanly."""
    st.session_state["active_page"] = page_key
    st.rerun()


def get_guest_profile() -> dict[str, Any]:
    """Return a clean default profile for visitors previewing before sign-in."""
    return {
        "user_id": None,
        "full_name": "Guest Athlete",
        "email": "",
        "age": 24,
        "height_cm": None,
        "weight_kg": None,
        "gender": None,
        "primary_sport": "Football",
        "experience_level": "Intermediate",
        "primary_goal": "Improve mobility",
        "secondary_goals": ["Improve flexibility"],
        "weekly_frequency": 4,
        "available_duration_min": 25,
        "available_equipment": [],
        "preferred_intensity": "Moderate",
        "excluded_exercises": [],
        "physical_restrictions": "",
    }


def get_active_user() -> dict[str, Any] | None:
    """Return the currently authenticated user dict from Streamlit session state."""
    return st.session_state.get("auth_user")


def get_active_profile() -> tuple[dict[str, Any], bool]:
    """Return (profile_dict, is_authenticated)."""
    user = get_active_user()
    if user and user.get("id"):
        profile = get_athlete_profile(user["id"])
        if profile is not None:
            return profile, True
        guest = get_guest_profile()
        guest["user_id"] = user["id"]
        guest["full_name"] = user["full_name"]
        guest["email"] = user["email"]
        return guest, True
    return get_guest_profile(), False


def ensure_demo_athlete_account() -> dict[str, Any]:
    """Create or authenticate the realistic demo athlete account on explicit user request."""
    ok, _, user = authenticate_user(DEMO_EMAIL, DEMO_PASSWORD)
    if ok and user is not None:
        return user

    ok, _, user = register_user("Aarav Sharma (Demo)", DEMO_EMAIL, DEMO_PASSWORD)
    assert ok and user is not None
    uid = user["id"]

    profile = save_athlete_profile(
        user_id=uid,
        age=23,
        height_cm=177.0,
        weight_kg=71.0,
        gender="Male",
        primary_sport="Football",
        experience_level="Intermediate",
        primary_goal="Improve mobility",
        secondary_goals=["Improve flexibility", "Improve athletic performance"],
        weekly_frequency=4,
        available_duration_min=25,
        available_equipment=["Yoga Mat", "Resistance Band"],
        preferred_intensity="Moderate",
        physical_restrictions="",
    )

    for ex_id, rating in [
        ("mob-hip-drills", 5),
        ("str-hamstring", 5),
        ("wu-leg-swings", 5),
        ("sp-football-cod-shuttle", 4),
        ("bal-single-leg", 4),
        ("st-glute-bridges", 4),
    ]:
        save_exercise_feedback(uid, ex_id, rating=rating, is_excluded=False)

    r1 = generate_workout_routine(profile, routine_type="Pre-sports warm-up", duration_min=12)
    r1_id = save_workout_routine(uid, r1, is_favorite=True)

    r2 = generate_workout_routine(profile, routine_type="10-minute mobility routine", duration_min=15)
    r2_id = save_workout_routine(uid, r2, is_favorite=True)

    generate_balanced_weekly_plan(uid, profile)

    now = datetime.now(timezone.utc)
    sample_logs = [
        (r1_id, r1["title"], 14, r1["exercises"], 5, 100.0, now - timedelta(days=9), "Smooth pre-match activation."),
        (r2_id, r2["title"], 16, r2["exercises"], 4, 100.0, now - timedelta(days=7), "Hips felt noticeably looser after 90/90 drills."),
        (r1_id, "Football Conditioning & Agility (25 min)", 26, r1["exercises"], 7, 92.0, now - timedelta(days=5), "Strong deceleration mechanics on turns."),
        (r2_id, r2["title"], 15, r2["exercises"], 4, 100.0, now - timedelta(days=3), "Great active recovery session."),
        (r1_id, r1["title"], 12, r1["exercises"], 5, 100.0, now - timedelta(days=1), "Ready for weekend game."),
    ]
    for rid, title, mins, exs, rpe, pct, ts, note in sample_logs:
        compact = [
            {"exercise_id": e["id"], "name": e["name"], "category": e["category"], "completed": True}
            for e in exs
        ]
        log_completed_workout(
            user_id=uid,
            routine_id=rid,
            routine_title=title,
            actual_duration_min=mins,
            exercises_completed=compact,
            perceived_effort_rpe=rpe,
            completion_percentage=pct,
            notes=note,
            completed_at=ts,
        )

    user["onboarding_completed"] = True
    return user


def render_whoop_ring_svg(percentage: float, label: str, sublabel: str, color: str = "#00E676") -> str:
    """Return a crisp WHOOP-inspired radial progress ring SVG string."""
    pct = max(0.0, min(100.0, float(percentage)))
    radius = 44
    circumference = 2 * 3.14159265 * radius
    dash_offset = circumference * (1.0 - pct / 100.0)
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:0.2rem;">
      <svg width="116" height="116" viewBox="0 0 116 116">
        <circle cx="58" cy="58" r="{radius}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="9"/>
        <circle cx="58" cy="58" r="{radius}" fill="none" stroke="{color}" stroke-width="9"
                stroke-linecap="round"
                stroke-dasharray="{circumference:.1f}"
                stroke-dashoffset="{dash_offset:.1f}"
                transform="rotate(-90 58 58)"/>
        <text x="58" y="57" text-anchor="middle" font-family="Barlow Condensed, Inter, sans-serif"
              font-size="28" font-weight="800" fill="#FFFFFF">{pct:.0f}%</text>
        <text x="58" y="73" text-anchor="middle" font-family="Inter, sans-serif"
              font-size="8.5" font-weight="700" fill="#9CA3AF" letter-spacing="1.0">{escape(label.upper())}</text>
      </svg>
      <div style="font-size:0.74rem; color:#A1A1AA; margin-top:0.15rem; text-align:center;">{escape(sublabel)}</div>
    </div>
    """


def render_darebee_week_poster(weekly_schedule: list[dict[str, Any]]) -> None:
    """Render a Darebee-inspired 7-day visual program grid poster."""
    tiles: list[str] = []
    for idx, day in enumerate(weekly_schedule, start=1):
        intensity = day.get("intensity", "Rest")
        cls = {
            "High": "fm-day-tile-high",
            "Moderate": "fm-day-tile-mod",
            "Low": "fm-day-tile-low",
        }.get(intensity, "fm-day-tile-rest")
        day_label = day.get("day") or day.get("day_name") or f"Day {idx}"
        title = escape(str(day.get("title") or day.get("routine_title") or "Rest Day")[:44])
        dur = int(day.get("duration_min") or day.get("estimated_duration_min") or 0)
        status = day.get("status", "")
        status_mark = "✓ " if status == "completed" else ""
        meta = "REST DAY" if intensity == "Rest" else f"{status_mark}{intensity.upper()} · {dur}M"
        tiles.append(
            f"""
            <div class="fm-day-tile {cls}">
                <div class="fm-day-num">D{idx:02d} · {escape(day_label[:3])}</div>
                <div class="fm-day-title">{title}</div>
                <div class="fm-day-meta">{escape(meta)}</div>
            </div>
            """
        )
    st.markdown(f'<div class="fm-poster-grid">{"".join(tiles)}</div>', unsafe_allow_html=True)


def render_svg_visual(media_reference: str | None) -> None:
    """Render a verified local animated SVG exercise visual cleanly."""
    if not media_reference:
        return
    svg_path: Path = config.BASE_DIR / media_reference
    if not svg_path.exists():
        return
    raw_bytes = svg_path.read_bytes()
    encoded = base64.b64encode(raw_bytes).decode("ascii")
    st.markdown(
        f'<img src="data:image/svg+xml;base64,{encoded}" style="width:100%; border-radius:12px; display:block;" alt="Animated exercise demonstration"/>',
        unsafe_allow_html=True,
    )


def render_safety_footer() -> None:
    """Display FitMotion AI's mandatory non-medical safety disclaimer."""
    st.markdown(
        f"""
        <div class="fm-safety-box">
            <strong>Wellness & Safety Notice:</strong> {config.SAFETY_DISCLAIMER}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_gowod_grid_card(
    ex: dict[str, Any],
    user_id: int | None,
    key_prefix: str,
    feedback_map: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Render a clean GOWOD-style vertical exercise card ideal for 2-column grid layouts."""
    fb = (feedback_map or {}).get(ex["id"], {})
    current_rating = ex.get("user_rating") or fb.get("rating")
    is_excluded = bool(fb.get("is_excluded", False))

    equip_list = ex.get("required_equipment", [])
    equip_text = ", ".join(equip_list) if equip_list else "Bodyweight"
    diff_cls = {
        "Advanced": "fm-chip-orange",
        "Intermediate": "fm-chip-accent",
        "Beginner": "fm-chip-green",
    }.get(ex["difficulty_level"], "")

    muscle_chips = "".join(
        f'<span class="fm-chip">{escape(m)}</span>' for m in ex.get("target_muscles", [])[:3]
    )
    sport_chips = "".join(
        f'<span class="fm-chip fm-chip-accent">{escape(s)}</span>' for s in ex.get("relevant_sports", [])[:3]
    )

    with st.container(border=True):
        render_svg_visual(ex.get("media_reference"))
        st.markdown(
            f"""
            <div style="margin-top:0.55rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:0.4rem;">
                    <span class="fm-chip {diff_cls}">{escape(ex['difficulty_level'])}</span>
                    <span style="font-size:0.74rem; color:#9CA3AF; font-weight:600;">{escape(equip_text)}</span>
                </div>
                <div style="font-family:'Barlow Condensed',sans-serif; font-size:1.35rem; font-weight:800; color:#FFFFFF; margin:0.45rem 0 0.2rem 0; line-height:1.15; text-transform:uppercase;">
                    {escape(ex['name'])}
                </div>
                <div style="font-size:0.83rem; color:#A1A1AA; line-height:1.45; margin-bottom:0.45rem;">
                    {escape(ex['description'])}
                </div>
                <div class="fm-chip-row">{muscle_chips}{sport_chips}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Form Cues, Safety & Modifications"):
            st.markdown("**Step-by-Step Instructions**")
            for idx, step in enumerate(ex.get("instructions", []), start=1):
                st.markdown(f"{idx}. {step}")
            st.markdown("**Safety Precautions**")
            for cue in ex.get("safety_instructions", []):
                st.markdown(f"- {cue}")
            st.markdown("**Common Mistakes**")
            for mistake in ex.get("common_mistakes", []):
                st.markdown(f"- {mistake}")
            if ex.get("beginner_modification"):
                st.success(f"**Beginner Modification:** {ex['beginner_modification']}")

        if user_id:
            c1, c2, c3 = st.columns([1.2, 0.85, 0.95])
            with c1:
                rating_choice = st.selectbox(
                    "Rate",
                    options=[0, 1, 2, 3, 4, 5],
                    index=int(current_rating) if current_rating in (1, 2, 3, 4, 5) else 0,
                    format_func=lambda v: "Rate..." if v == 0 else f"{'★' * v}",
                    key=f"{key_prefix}_rate_{ex['id']}",
                    label_visibility="collapsed",
                )
            with c2:
                if st.button("Save ★", key=f"{key_prefix}_sr_{ex['id']}", width="stretch"):
                    if rating_choice > 0:
                        save_exercise_feedback(user_id, ex["id"], rating=rating_choice)
                        st.toast(f"Rated {ex['name']} {rating_choice}/5 (ML ranker updated).")
            with c3:
                if st.button("Restore" if is_excluded else "Exclude", key=f"{key_prefix}_ex_{ex['id']}", width="stretch"):
                    save_exercise_feedback(user_id, ex["id"], is_excluded=not is_excluded)
                    st.toast(f"{'Restored' if is_excluded else 'Excluded'} {ex['name']}.")
                    st.rerun()


def render_exercise_card(
    ex: dict[str, Any],
    user_id: int | None,
    key_prefix: str,
    show_explanation: bool = False,
    show_prescription: bool = False,
    feedback_map: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Render a full-width horizontal Nike/GOWOD exercise card with telemetry & AI explanation."""
    fb = (feedback_map or {}).get(ex["id"], {})
    current_rating = ex.get("user_rating") or fb.get("rating")
    is_excluded = bool(fb.get("is_excluded", False))

    with st.container(border=True):
        vis_col, info_col = st.columns([1.05, 1.45], gap="medium")

        with vis_col:
            render_svg_visual(ex.get("media_reference"))
            if show_explanation and ex.get("match_score") is not None:
                st.caption(
                    f"AI Match: **{ex['match_score']}%** · Rule: {ex.get('rule_score', 0)} · ML: {ex.get('ml_score', 0):+.1f}"
                )

        with info_col:
            equip_list = ex.get("required_equipment", [])
            equip_text = ", ".join(equip_list) if equip_list else "Bodyweight"
            sets_val = ex.get("prescribed_sets", ex.get("recommended_sets", 2))
            reps_val = ex.get("prescribed_reps", ex.get("recommended_reps", "10"))
            rest_val = ex.get("prescribed_rest_sec", ex.get("rest_seconds", 30))

            st.markdown(f"#### {ex['name']}")
            st.caption(f"**{ex['category']}** · {ex['difficulty_level']} · Equipment: `{equip_text}`")
            st.write(ex["description"])

            if show_prescription:
                st.markdown(
                    f"**Prescription:** `{sets_val} sets × {reps_val}` · **Rest:** `{rest_val}s` · **Est:** `{max(1, round(ex.get('estimated_block_sec', ex.get('default_duration_sec', 60)) / 60))} min`"
                )
            else:
                st.markdown(
                    f"**Recommended:** `{sets_val} sets × {reps_val}` · **Rest:** `{rest_val}s` · **Muscles:** {', '.join(ex.get('target_muscles', []))}"
                )

            if show_explanation and ex.get("explanation"):
                st.info(f"**Why selected:** {ex['explanation']}")

            with st.expander("Instructions, Safety Cues, Common Mistakes & Beginner Modification"):
                st.markdown("**Step-by-Step Instructions**")
                for idx, step in enumerate(ex.get("instructions", []), start=1):
                    st.markdown(f"{idx}. {step}")

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Safety Precautions**")
                    for cue in ex.get("safety_instructions", []):
                        st.markdown(f"- {cue}")
                with c2:
                    st.markdown("**Common Mistakes**")
                    for mistake in ex.get("common_mistakes", []):
                        st.markdown(f"- {mistake}")

                if ex.get("beginner_modification"):
                    st.success(f"**Beginner Modification:** {ex['beginner_modification']}")

                st.caption(f"Relevant sports: {', '.join(ex.get('relevant_sports', []))}")

            if user_id:
                ctrl1, ctrl2, ctrl3 = st.columns([1.3, 0.9, 1.0])
                with ctrl1:
                    rating_choice = st.selectbox(
                        "Rate for ML personalization",
                        options=[0, 1, 2, 3, 4, 5],
                        index=int(current_rating) if current_rating in (1, 2, 3, 4, 5) else 0,
                        format_func=lambda v: "Rate exercise..." if v == 0 else f"{'★' * v} ({v}/5)",
                        key=f"{key_prefix}_rate_{ex['id']}",
                        label_visibility="collapsed",
                    )
                with ctrl2:
                    if st.button("Save Rating", key=f"{key_prefix}_saverate_{ex['id']}", width="stretch"):
                        if rating_choice > 0:
                            save_exercise_feedback(user_id, ex["id"], rating=rating_choice)
                            st.toast(f"Saved {rating_choice}/5 rating for {ex['name']}.")
                with ctrl3:
                    btn_label = "Restore" if is_excluded else "Exclude"
                    if st.button(btn_label, key=f"{key_prefix}_excl_{ex['id']}", width="stretch"):
                        save_exercise_feedback(user_id, ex["id"], is_excluded=not is_excluded)
                        st.toast(f"{'Restored' if is_excluded else 'Excluded'} {ex['name']}.")
                        st.rerun()


def render_routine_panel(
    routine: dict[str, Any],
    user_id: int | None,
    key_prefix: str,
) -> None:
    """Render a Darebee/Nike-style guided workout panel with live completion checklist & logging."""
    exercises = routine.get("exercises", [])
    if not exercises:
        st.warning(
            "No exercises matched your current combination of filters, equipment, and restrictions. "
            "Try widening your categories or adjusting equipment settings."
        )
        return

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Duration", f"{routine['estimated_duration_min']} min")
    m2.metric("Exercises", len(exercises))
    m3.metric("Intensity", routine["intensity"])
    m4.metric("AI Ranker", "Hybrid ML" if routine.get("ml_active") else "Rule-Based")

    # Guided Workout Checklist Progress Bar
    completed_flags: list[bool] = []
    for idx, ex in enumerate(exercises, start=1):
        chk_key = f"{key_prefix}_done_{idx}_{ex['id']}"
        completed_flags.append(bool(st.session_state.get(chk_key, False)))

    done_count = sum(completed_flags)
    pct_done = round((done_count / len(exercises)) * 100.0, 1) if exercises else 0.0
    st.progress(
        pct_done / 100.0,
        text=f"Guided Session Progress: {done_count} / {len(exercises)} exercises checked off ({pct_done:.0f}%)",
    )

    if user_id:
        act1, act2, act3 = st.columns([1.1, 1.1, 1.3])
        with act1:
            if st.button("💾 Save Routine", key=f"{key_prefix}_save", width="stretch", type="secondary"):
                rid = save_workout_routine(user_id, routine, is_favorite=False)
                st.success(f"Saved routine (#{rid}) to your library!")
        with act2:
            if st.button("⭐ Save Favorite", key=f"{key_prefix}_fav", width="stretch", type="secondary"):
                rid = save_workout_routine(user_id, routine, is_favorite=True)
                st.success(f"Saved routine (#{rid}) to Favorites!")
        with act3:
            log_pct = pct_done if done_count > 0 else 100.0
            if st.button(f"✅ Log Workout ({log_pct:.0f}%)", key=f"{key_prefix}_log", width="stretch", type="primary"):
                compact = [
                    {
                        "exercise_id": e["id"],
                        "name": e["name"],
                        "category": e["category"],
                        "completed": completed_flags[i] if done_count > 0 else True,
                    }
                    for i, e in enumerate(exercises)
                ]
                log_completed_workout(
                    user_id=user_id,
                    routine_title=routine["title"],
                    actual_duration_min=routine["estimated_duration_min"],
                    exercises_completed=compact,
                    perceived_effort_rpe=6 if routine["intensity"] == "Moderate" else (8 if routine["intensity"] == "High" else 4),
                    completion_percentage=log_pct,
                    notes=f"Completed {routine['routine_type']} ({routine['target_sport']}).",
                )
                st.success("Workout logged to Workout History & Progress Dashboard!")
    else:
        st.info("Sign in via **Login & Registration** to save routines, rate exercises for ML ranking, and track workout history.")

    feedback_map = get_user_feedback_map(user_id) if user_id else {}
    for idx, ex in enumerate(exercises, start=1):
        head_c1, head_c2 = st.columns([3.2, 1.0])
        head_c1.markdown(
            f'<span class="fm-pill fm-pill-phase">STEP {idx:02d}</span> &nbsp; <strong style="color:#E4E4E7;">{escape(ex.get("phase", ex["category"]))}</strong>',
            unsafe_allow_html=True,
        )
        head_c2.checkbox("Mark Complete", key=f"{key_prefix}_done_{idx}_{ex['id']}")
        render_exercise_card(
            ex=ex,
            user_id=user_id,
            key_prefix=f"{key_prefix}_{idx}",
            show_explanation=True,
            show_prescription=True,
            feedback_map=feedback_map,
        )
