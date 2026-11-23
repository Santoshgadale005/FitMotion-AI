"""Page 3: WHOOP × Nike × Strava Command Center (Main Dashboard)."""

from __future__ import annotations

import streamlit as st

import config
from dashboard.components import (
    get_active_profile,
    navigate_to,
    render_darebee_week_poster,
    render_safety_footer,
    render_svg_visual,
    render_whoop_ring_svg,
)
from database import check_database_health, get_table_counts
from recommendation import recommend_exercises
from training import compute_progress_summary, get_week_schedule


def render_main_dashboard() -> None:
    """Render the high-contrast WHOOP/Strava/Nike athlete command center."""
    profile, is_auth = get_active_profile()
    user_id = profile.get("user_id")
    db_health = check_database_health()
    table_counts = get_table_counts() if db_health["status"] == "connected" else {}

    rec_preview = recommend_exercises(profile, top_n=3)
    progress = (
        compute_progress_summary(user_id, weekly_target_frequency=int(profile.get("weekly_frequency", 3)))
        if user_id
        else None
    )
    week_days = get_week_schedule(user_id) if user_id else []

    ring_pct = progress["weekly_goal_adherence_pct"] if progress else 0.0
    ring_color = "#00E676" if ring_pct >= 75 else ("#FFB020" if ring_pct >= 40 else "#FC4C02")
    ring_sub = (
        f"{progress['workouts_last_7_days']}/{progress['weekly_target_frequency']} sessions this week"
        if progress
        else "Sign in to track weekly target"
    )

    engine_pill = (
        '<span class="fm-pill fm-pill-live">● Hybrid ML + Rules Active</span>'
        if rec_preview["ml_active"]
        else '<span class="fm-pill fm-pill-cyan">● Rule-Based AI Active</span>'
    )
    greeting = f"Ready to Train, {profile['full_name']}" if is_auth else f"{config.APP_NAME} Performance Hub"

    # Hero with WHOOP Consistency Ring
    hero_left, hero_right = st.columns([3.0, 1.0], gap="medium")
    with hero_left:
        st.markdown(
            f"""
            <div class="fm-hero" style="margin-bottom:0.5rem;">
                <div style="display:flex; gap:0.55rem; flex-wrap:wrap; align-items:center;">
                    <span class="fm-pill fm-pill-phase">{profile['primary_sport']} · {profile['experience_level']}</span>
                    {engine_pill}
                </div>
                <h1>{greeting}</h1>
                <p>
                    Primary Goal: <strong style="color:#FAFAFA;">{profile['primary_goal']}</strong> ·
                    Session Budget: <strong style="color:#FAFAFA;">{profile['available_duration_min']} min</strong> ·
                    Intensity: <strong style="color:#FAFAFA;">{profile['preferred_intensity']}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hero_right:
        st.markdown(
            f"""
            <div class="fm-card" style="display:flex; align-items:center; justify-content:center; min-height:158px;">
                {render_whoop_ring_svg(ring_pct, "Weekly Goal", ring_sub, ring_color)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 1-Click Quick-Start Action Strip
    qa1, qa2, qa3, qa4 = st.columns(4, gap="small")
    if qa1.button("☀️ Start Quick Warm-up", type="primary", width="stretch", key="qa_warmup"):
        navigate_to("warmup_assistant")
    if qa2.button("🔥 Build Workout / Plans", type="secondary", width="stretch", key="qa_gen"):
        navigate_to("workout_generator")
    if qa3.button("🏃 Browse 90 Exercises", type="secondary", width="stretch", key="qa_lib"):
        navigate_to("exercise_library")
    if qa4.button("🤖 Ask AI Coach", type="secondary", width="stretch", key="qa_ai"):
        navigate_to("ai_training_assistant")

    if not is_auth:
        st.info(
            "Exploring in **Guest Preview Mode**. Open **Login & Registration** in the sidebar to create your athlete account or click **Sign In as Demo Athlete** to preview live ML rankings, weekly schedules, and Plotly analytics."
        )

    # KPI Metric Row
    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="fm-card">
                <div class="fm-metric-label">Exercise Library</div>
                <div class="fm-metric-value">{table_counts.get('exercises', 0)}</div>
                <div class="fm-metric-sub">Animated drills across 8 sports</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        completed_val = progress["total_workouts"] if progress else 0
        sub_txt = f"{progress['workouts_last_7_days']} in last 7 days" if progress else "Log workouts to track"
        st.markdown(
            f"""
            <div class="fm-card">
                <div class="fm-metric-label">Sessions Logged</div>
                <div class="fm-metric-value" style="color:#00E676;">{completed_val}</div>
                <div class="fm-metric-sub">{sub_txt}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        mins_val = f"{progress['total_minutes']}m" if progress else f"{profile['available_duration_min']}m"
        mins_sub = f"{progress['total_hours']} total training hours" if progress else "Default session budget"
        st.markdown(
            f"""
            <div class="fm-card">
                <div class="fm-metric-label">{'Active Volume' if progress else 'Session Target'}</div>
                <div class="fm-metric-value" style="color:#00D4FF;">{mins_val}</div>
                <div class="fm-metric-sub">{mins_sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        ml_label = "ML ACTIVE" if rec_preview["ml_active"] else "RULES"
        ml_sub = (
            f"Scikit-learn ({rec_preview['ml_training_samples']} signals)"
            if rec_preview["ml_active"]
            else "Rate 2+ drills to train ML"
        )
        st.markdown(
            f"""
            <div class="fm-card">
                <div class="fm-metric-label">Recommendation AI</div>
                <div class="fm-metric-value" style="color:#FC4C02;">{ml_label}</div>
                <div class="fm-metric-sub">{ml_sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # GOWOD-style 3-Column Top AI Picks
    st.markdown('<div class="fm-section-title">Top Personalized Picks For You</div>', unsafe_allow_html=True)
    rec_cols = st.columns(3, gap="medium")
    for col, ex in zip(rec_cols, rec_preview["recommendations"]):
        with col:
            with st.container(border=True):
                render_svg_visual(ex.get("media_reference"))
                st.markdown(f"**{ex['name']}**")
                st.caption(f"{ex['category']} · Match **{ex['match_score']}%** · {ex['recommended_sets']}×{ex['recommended_reps']}")
                st.write(ex["explanation"])

    # Darebee-Style 7-Day Schedule Poster + Sport Demands
    st.markdown('<div class="fm-section-title">This Week At A Glance</div>', unsafe_allow_html=True)
    if week_days and any(d["schedule_id"] for d in week_days):
        render_darebee_week_poster(week_days)
    else:
        st.info("No weekly plan assigned yet — open **Weekly Training Planner** or **Workout Generator → Complete 4-Week Sport Plans** to apply a full program in one click.")

    sport_meta = rec_preview["sport_profile"]
    demands_chips = "".join(f'<span class="fm-chip fm-chip-accent">{d}</span>' for d in sport_meta["physical_demands"])
    st.markdown(
        f"""
        <div class="fm-card" style="margin-top:1rem;">
            <div class="fm-metric-label">{profile['primary_sport']} Athletic Demands Profile</div>
            <p style="color:#D4D4D8; font-size:0.9rem; line-height:1.5; margin:0.35rem 0 0.7rem 0;">{sport_meta['summary']}</p>
            <div class="fm-chip-row">{demands_chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_safety_footer()
