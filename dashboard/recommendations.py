"""Pages 6–12: AI Recommendations, Workout Generator, Specialized Modules & Sport-Specific Training."""

from __future__ import annotations

import streamlit as st

import config
from athlete import get_user_feedback_map
from dashboard.components import (
    get_active_profile,
    render_darebee_week_poster,
    render_exercise_card,
    render_routine_panel,
    render_safety_footer,
)
from exercises import ALL_EQUIPMENT_OPTIONS, get_exercise_by_id, load_sport_profiles
from recommendation import (
    ROUTINE_BLUEPRINTS,
    generate_workout_routine,
    get_user_routines,
    recommend_exercises,
    toggle_favorite_routine,
    delete_workout_routine,
)
from training import apply_workout_plan_to_week, get_workout_plans


def render_ai_recommendations_page() -> None:
    """Page 6: Explainable Rule-Based + Scikit-learn Personalized Recommendations."""
    profile, is_auth = get_active_profile()
    user_id = profile.get("user_id")

    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Hybrid AI Engine · Rule-Based + Scikit-learn</span>
            <h1>AI Exercise Recommendations</h1>
            <p>Every exercise is ranked for your sport, goals, experience, equipment, and movement restrictions—with transparent explanations and adaptive Scikit-learn preference learning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not is_auth:
        st.info("Previewing with default Football / Intermediate / Mobility profile. Sign in to personalize with your own profile and ML ratings.")

    with st.expander("Customize Recommendation Parameters (Quick What-If Explorer)", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        sport = c1.selectbox(
            "Sport",
            options=config.SUPPORTED_SPORTS,
            index=config.SUPPORTED_SPORTS.index(profile["primary_sport"]) if profile["primary_sport"] in config.SUPPORTED_SPORTS else 0,
        )
        goal = c2.selectbox(
            "Primary Goal",
            options=config.FITNESS_GOALS,
            index=config.FITNESS_GOALS.index(profile["primary_goal"]) if profile["primary_goal"] in config.FITNESS_GOALS else 0,
        )
        exp = c3.selectbox(
            "Experience",
            options=config.EXPERIENCE_LEVELS,
            index=config.EXPERIENCE_LEVELS.index(profile["experience_level"]) if profile["experience_level"] in config.EXPERIENCE_LEVELS else 0,
        )
        intensity = c4.selectbox(
            "Intensity",
            options=config.INTENSITY_LEVELS,
            index=config.INTENSITY_LEVELS.index(profile["preferred_intensity"]) if profile["preferred_intensity"] in config.INTENSITY_LEVELS else 1,
        )
        equip = st.multiselect(
            "Available Equipment",
            options=ALL_EQUIPMENT_OPTIONS,
            default=list(profile.get("available_equipment", [])),
        )
        top_n = st.slider("Number of recommendations", min_value=5, max_value=20, value=10)
    working_profile = dict(profile)
    working_profile.update(
        {
            "primary_sport": sport,
            "primary_goal": goal,
            "experience_level": exp,
            "preferred_intensity": intensity,
            "available_equipment": equip,
        }
    )

    with st.spinner("Scoring and ranking exercises..."):
        result = recommend_exercises(working_profile, top_n=top_n)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Engine Mode", "Hybrid ML + Rules" if result["ml_active"] else "Rule-Based")
    k2.metric("ML Training Signals", result["ml_training_samples"])
    k3.metric("Top Matches Returned", len(result["recommendations"]))
    k4.metric("Safety / Equip Filtered", result["filtered_out_count"])

    if not result["ml_active"]:
        st.caption(
            "Tip: Rate at least 2 exercises (1–5 stars) or complete 2 workouts to activate personalized Scikit-learn Ridge + cosine-similarity reranking."
        )

    feedback_map = get_user_feedback_map(user_id) if user_id else {}
    for ex in result["recommendations"]:
        render_exercise_card(
            ex=ex,
            user_id=user_id,
            key_prefix="airec",
            show_explanation=True,
            show_prescription=False,
            feedback_map=feedback_map,
        )

    render_safety_footer()


def render_workout_generator_page() -> None:
    """Page 7: Personalized Workout Generator & Saved Routine Library."""
    profile, _ = get_active_profile()
    user_id = profile.get("user_id")

    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Custom Routine Builder</span>
            <h1>Personalized Workout Generator</h1>
            <p>Generate time-budgeted workouts across 9 specialized presets or build a fully custom session tailored to your equipment, difficulty, and training focus.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_gen, tab_plans, tab_saved = st.tabs(
        ["Generate Custom Routine", "Complete 4-Week Sport Plans", "Saved & Favorite Routines"]
    )

    with tab_gen:
        preset_names = list(ROUTINE_BLUEPRINTS.keys())
        c1, c2, c3 = st.columns(3)
        with c1:
            routine_type = st.selectbox("Routine Type", options=preset_names, index=0)
            default_dur = ROUTINE_BLUEPRINTS[routine_type]["default_duration"]
            duration_min = st.slider("Target Duration (minutes)", min_value=5, max_value=60, step=5, value=default_dur)
        with c2:
            difficulty = st.selectbox(
                "Exercise Difficulty",
                options=config.EXPERIENCE_LEVELS,
                index=config.EXPERIENCE_LEVELS.index(profile["experience_level"]) if profile["experience_level"] in config.EXPERIENCE_LEVELS else 0,
            )
            intensity = st.select_slider(
                "Training Intensity",
                options=config.INTENSITY_LEVELS,
                value=ROUTINE_BLUEPRINTS[routine_type]["default_intensity"],
            )
        with c3:
            sport = st.selectbox(
                "Sport Focus",
                options=config.SUPPORTED_SPORTS,
                index=config.SUPPORTED_SPORTS.index(profile["primary_sport"]) if profile["primary_sport"] in config.SUPPORTED_SPORTS else 0,
            )
            equipment = st.multiselect(
                "Available Equipment",
                options=ALL_EQUIPMENT_OPTIONS,
                default=list(profile.get("available_equipment", [])),
            )

        selected_categories = st.multiselect(
            "Filter Specific Exercise Categories (optional — leave empty for smart phase blueprint)",
            options=config.EXERCISE_CATEGORIES,
            default=[],
        )
        custom_title = st.text_input("Custom Routine Title (optional)", placeholder="Leave blank to auto-name")

        if st.button("⚡ Generate Personalized Routine", type="primary", width="stretch"):
            working_profile = dict(profile)
            working_profile["primary_sport"] = sport
            with st.spinner("Assembling balanced workout sequence..."):
                routine = generate_workout_routine(
                    profile=working_profile,
                    routine_type=routine_type,
                    duration_min=duration_min,
                    difficulty=difficulty,
                    intensity=intensity,
                    selected_categories=selected_categories or None,
                    available_equipment=equipment,
                    title=custom_title.strip() or None,
                )
            st.session_state["generated_routine"] = routine

        active_routine = st.session_state.get("generated_routine")
        if active_routine:
            st.divider()
            st.subheader(active_routine["title"])

            # Allow user to drop any unwanted exercise before saving/logging
            ex_names = [e["name"] for e in active_routine["exercises"]]
            keep_names = st.multiselect(
                "Customize Exercises Included in This Routine",
                options=ex_names,
                default=ex_names,
                key="gen_keep_exercises",
            )
            customized = dict(active_routine)
            customized["exercises"] = [e for e in active_routine["exercises"] if e["name"] in keep_names]
            customized["estimated_duration_min"] = max(
                1, round(sum(e.get("estimated_block_sec", 60) for e in customized["exercises"]) / 60)
            ) if customized["exercises"] else 0

            render_routine_panel(customized, user_id=user_id, key_prefix="gen")

    with tab_plans:
        st.markdown("### Evidence-Based 4-Week Sport & Fitness Workout Plans")
        st.caption("Complete weekly programs grounded in NSCA, ACSM, FIFA 11+, BWF, USTA, and USA Swimming conditioning guidelines.")
        pf1, pf2 = st.columns(2)
        plan_sport = pf1.selectbox("Filter Plans by Sport", options=["All"] + config.SUPPORTED_SPORTS, key="plan_sport_flt")
        plan_diff = pf2.selectbox("Filter Plans by Difficulty", options=["All"] + config.EXPERIENCE_LEVELS, key="plan_diff_flt")
        plans = get_workout_plans(sport=plan_sport, difficulty=plan_diff)

        if not plans:
            st.info("No structured plans match that exact filter. Switch Sport or Difficulty to 'All' to view all 9 complete plans.")
        else:
            for plan in plans:
                with st.container(border=True):
                    p_left, p_right = st.columns([2.4, 1.0])
                    p_left.markdown(f"#### {plan['title']}")
                    p_left.caption(
                        f"**{plan['sport']}** · **{plan['difficulty']}** · {plan['duration_weeks']} Weeks · {plan['days_per_week']} Days/Week · _{plan['framework']}_"
                    )
                    p_left.write(plan["summary"])
                    if user_id:
                        if p_right.button("📅 Apply Plan to Weekly Planner", key=f"apply_p_{plan['id']}", type="primary", width="stretch"):
                            ok, msg = apply_workout_plan_to_week(user_id, plan["id"])
                            if ok:
                                st.success(msg)
                            else:
                                st.error(msg)
                    else:
                        p_right.caption("Sign in to apply this plan to your Weekly Planner.")

                    render_darebee_week_poster(plan["weekly_schedule"])

                    with st.expander("View Exercise-by-Exercise Breakdown"):
                        for day_spec in plan["weekly_schedule"]:
                            if day_spec["intensity"] == "Rest":
                                st.markdown(f"- **{day_spec['day']}:** _{day_spec['title']}_ (Rest Day)")
                            else:
                                ex_names = []
                                for eid in day_spec["exercise_ids"]:
                                    e = get_exercise_by_id(eid)
                                    if e:
                                        ex_names.append(f"{e['name']} ({e['recommended_sets']}×{e['recommended_reps']})")
                                st.markdown(
                                    f"- **{day_spec['day']} — {day_spec['title']}** *({day_spec['intensity']} · ~{day_spec['duration_min']} min)*\n"
                                    f"  - " + " → ".join(ex_names)
                                )

    with tab_saved:
        if not user_id:
            st.info("Sign in via **Login & Registration** to save and manage favorite routines.")
        else:
            fav_only = st.checkbox("Show Favorites Only", value=False)
            routines = get_user_routines(user_id, favorites_only=fav_only)
            if not routines:
                st.info("No saved routines yet. Generate a routine and click **Save Routine** or **Save as Favorite**.")
            else:
                for r in routines:
                    with st.container(border=True):
                        h1, h2, h3 = st.columns([2.6, 0.8, 0.7])
                        star = "⭐ " if r["is_favorite"] else ""
                        h1.markdown(f"#### {star}{r['title']}")
                        h1.caption(
                            f"{r['routine_type']} · {r['target_sport']} · {r['difficulty_level']} · {r['intensity']} · ~{r['estimated_duration_min']} min"
                        )
                        if h2.button("Unfavorite" if r["is_favorite"] else "Favorite", key=f"fav_t_{r['id']}", width="stretch"):
                            toggle_favorite_routine(user_id, r["id"])
                            st.rerun()
                        if h3.button("Delete", key=f"del_r_{r['id']}", width="stretch"):
                            delete_workout_routine(user_id, r["id"])
                            st.rerun()
                        for idx, item in enumerate(r["exercises"], start=1):
                            st.markdown(
                                f"{idx}. **{item['name']}** ({item['category']}) — `{item['prescribed_sets']} sets × {item['prescribed_reps']}` · Rest {item['prescribed_rest_sec']}s"
                            )

    render_safety_footer()


def render_specialized_module_page(
    page_title: str,
    badge_text: str,
    subtitle: str,
    default_routine_type: str,
    category_scope: list[str],
    default_duration: int,
    default_intensity: str,
    state_key: str,
) -> None:
    """Shared interactive builder for Pages 8–11 (Warm-up, Mobility, Strength, Recovery)."""
    profile, _ = get_active_profile()
    user_id = profile.get("user_id")

    st.markdown(
        f"""
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">{badge_text}</span>
            <h1>{page_title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    sport = c1.selectbox(
        "Sport / Activity Context",
        options=config.SUPPORTED_SPORTS,
        index=config.SUPPORTED_SPORTS.index(profile["primary_sport"]) if profile["primary_sport"] in config.SUPPORTED_SPORTS else 0,
        key=f"{state_key}_sport",
    )
    duration = c2.slider(
        "Duration (minutes)",
        min_value=5,
        max_value=45,
        step=5,
        value=default_duration,
        key=f"{state_key}_dur",
    )
    intensity = c3.select_slider(
        "Intensity",
        options=config.INTENSITY_LEVELS,
        value=default_intensity,
        key=f"{state_key}_int",
    )

    working_profile = dict(profile)
    working_profile["primary_sport"] = sport

    if st.button(f"Generate {page_title} Routine", type="primary", key=f"{state_key}_btn"):
        routine = generate_workout_routine(
            profile=working_profile,
            routine_type=default_routine_type,
            duration_min=duration,
            intensity=intensity,
            selected_categories=category_scope,
        )
        st.session_state[state_key] = routine

    if state_key not in st.session_state:
        st.session_state[state_key] = generate_workout_routine(
            profile=working_profile,
            routine_type=default_routine_type,
            duration_min=duration,
            intensity=intensity,
            selected_categories=category_scope,
        )

    render_routine_panel(st.session_state[state_key], user_id=user_id, key_prefix=state_key)
    render_safety_footer()


def render_sport_specific_page() -> None:
    """Page 12: Dedicated Sport-Specific Conditioning Module."""
    profile, _ = get_active_profile()
    user_id = profile.get("user_id")
    sport_profiles = load_sport_profiles()

    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Multi-Sport Conditioning Science</span>
            <h1>Sport-Specific Training</h1>
            <p>Explore the physical demands of each sport and generate conditioning routines aligned with your individual level, equipment, and movement preferences.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_sport = st.selectbox(
        "Select Sport",
        options=config.SUPPORTED_SPORTS,
        index=config.SUPPORTED_SPORTS.index(profile["primary_sport"]) if profile["primary_sport"] in config.SUPPORTED_SPORTS else 0,
    )
    meta = sport_profiles[selected_sport]

    col_left, col_right = st.columns([1.2, 1.0], gap="large")
    with col_left:
        with st.container(border=True):
            st.markdown(f"### {selected_sport} Physical Demands")
            st.write(meta["summary"])
            for demand in meta["physical_demands"]:
                st.markdown(f"- {demand}")
    with col_right:
        with st.container(border=True):
            st.markdown("### Preparation & Recovery Focus")
            st.markdown(f"**Pre-Session Warm-up:** {meta['warmup_focus']}")
            st.markdown(f"**Post-Session Recovery:** {meta['recovery_focus']}")
            st.markdown("**Priority Muscle Groups:** " + ", ".join(meta["priority_muscles"]))

    st.divider()
    c1, c2 = st.columns([1, 1])
    duration = c1.slider("Conditioning Session Duration (min)", min_value=10, max_value=45, step=5, value=25)
    mode = c2.selectbox(
        "Session Focus",
        options=["Sport-specific conditioning routine", "Pre-sports warm-up", "Post-workout cooldown"],
    )

    working_profile = dict(profile)
    working_profile["primary_sport"] = selected_sport

    routine = generate_workout_routine(
        profile=working_profile,
        routine_type=mode,
        duration_min=duration,
    )
    st.subheader(routine["title"])
    render_routine_panel(routine, user_id=user_id, key_prefix=f"sport_{selected_sport}")

    # Dedicated multi-week sport workout plan right inside Sport-Specific Training
    sport_plans = get_workout_plans(sport=selected_sport)
    if sport_plans:
        st.divider()
        st.markdown(f'<div class="fm-section-title">Complete {selected_sport} 4-Week Training Plan</div>', unsafe_allow_html=True)
        for plan in sport_plans:
            with st.container(border=True):
                c_p1, c_p2 = st.columns([2.5, 1.0])
                c_p1.markdown(f"#### {plan['title']}")
                c_p1.caption(f"{plan['difficulty']} · {plan['duration_weeks']} Weeks · {plan['days_per_week']} Days/Week · _{plan['framework']}_")
                c_p1.write(plan["summary"])
                if user_id:
                    if c_p2.button("📅 Apply Plan to My Week", key=f"sp_apply_{plan['id']}", type="primary", width="stretch"):
                        ok, msg = apply_workout_plan_to_week(user_id, plan["id"])
                        if ok:
                            st.success(msg)
                else:
                    c_p2.caption("Sign in to apply this plan.")
                render_darebee_week_poster(plan["weekly_schedule"])
                with st.expander("Inspect Exercise Breakdown"):
                    for day_spec in plan["weekly_schedule"]:
                        st.markdown(f"- **{day_spec['day']}:** {day_spec['title']} ({day_spec['intensity']})")

    render_safety_footer()
