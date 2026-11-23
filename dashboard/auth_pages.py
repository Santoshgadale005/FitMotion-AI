"""Pages 1, 2 & 4: Login & Registration, Onboarding, and Athlete Profile."""

from __future__ import annotations

import streamlit as st

import config
from athlete import (
    RESTRICTION_OPTIONS,
    TAG_TO_RESTRICTION_LABEL,
    get_athlete_profile,
    parse_restriction_tags,
    save_athlete_profile,
    save_exercise_feedback,
)
from authentication import authenticate_user, register_user
from dashboard.components import (
    DEMO_EMAIL,
    DEMO_PASSWORD,
    ensure_demo_athlete_account,
    get_active_user,
    render_safety_footer,
)
from exercises import ALL_EQUIPMENT_OPTIONS, get_exercise_by_id


def render_login_registration_page() -> None:
    """Page 1: Login, Registration, and optional 1-click Demo Athlete loader."""
    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Account & Access</span>
            <h1>Login & Registration</h1>
            <p>Create your FitMotion AI athlete account to unlock personalized routines, Scikit-learn preference ranking, weekly schedules, and progress analytics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_user = get_active_user()
    if active_user:
        st.success(f"Signed in as **{active_user['full_name']}** (`{active_user['email']}`).")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Log Out", type="secondary", width="stretch"):
                st.session_state.pop("auth_user", None)
                st.rerun()
        render_safety_footer()
        return

    tab_login, tab_register, tab_demo = st.tabs(["Sign In", "Create Account", "Portfolio Demo Athlete"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In", type="primary", width="stretch")

        if submitted:
            ok, msg, user = authenticate_user(email, password)
            if ok and user:
                st.session_state["auth_user"] = user
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    with tab_register:
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="e.g., Priya Nair")
            email = st.text_input("Email Address", placeholder="priya@example.com")
            password = st.text_input("Password (min 8 characters)", type="password")
            confirm_pw = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Create Account", type="primary", width="stretch")

        if submitted:
            if password != confirm_pw:
                st.error("Passwords do not match. Please re-enter them.")
            else:
                ok, msg, user = register_user(full_name, email, password)
                if ok and user:
                    st.session_state["auth_user"] = user
                    st.success(msg + " Head to the **Onboarding** page in the sidebar to set up your profile.")
                    st.rerun()
                else:
                    st.error(msg)

    with tab_demo:
        st.markdown(
            """
            Want to explore all features immediately (including **Scikit-learn ML ranking**, a populated **Weekly Training Planner**, **Workout History**, and **Plotly Progress Charts**)?

            Load our pre-configured Football Intermediate demo athlete account with real logged sessions and exercise ratings.
            """
        )
        st.caption(f"Demo credentials: `{DEMO_EMAIL}` / `{DEMO_PASSWORD}`")
        if st.button("⚡ Sign In as Demo Athlete", type="primary"):
            with st.spinner("Preparing demo athlete profile, schedule, and workout logs..."):
                demo_user = ensure_demo_athlete_account()
                st.session_state["auth_user"] = demo_user
            st.success("Loaded Demo Athlete account!")
            st.rerun()

    render_safety_footer()


def _render_profile_form(user: dict, existing: dict | None, is_onboarding: bool) -> None:
    """Shared form for both Onboarding (Page 2) and Athlete Profile editing (Page 4)."""
    existing_tags = parse_restriction_tags(existing.get("physical_restrictions") if existing else "")
    existing_restriction_labels = [
        TAG_TO_RESTRICTION_LABEL[t] for t in existing_tags if t in TAG_TO_RESTRICTION_LABEL
    ]

    with st.form("athlete_profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("Name", value=(existing or user).get("full_name", ""))
            age = st.number_input("Age", min_value=10, max_value=110, value=int(existing["age"]) if existing else 22)
            height_cm = st.number_input(
                "Height in cm (optional, 0 to skip)",
                min_value=0.0,
                max_value=250.0,
                value=float(existing["height_cm"]) if (existing and existing.get("height_cm")) else 0.0,
                step=0.5,
            )
            weight_kg = st.number_input(
                "Weight in kg (optional, 0 to skip)",
                min_value=0.0,
                max_value=250.0,
                value=float(existing["weight_kg"]) if (existing and existing.get("weight_kg")) else 0.0,
                step=0.5,
            )
            gender_opts = ["Prefer not to say", "Female", "Male", "Non-binary"]
            cur_gender = existing.get("gender") if existing else None
            gender = st.selectbox(
                "Gender (optional)",
                options=gender_opts,
                index=gender_opts.index(cur_gender) if cur_gender in gender_opts else 0,
            )

        with c2:
            cur_sport = existing["primary_sport"] if existing else "General Fitness"
            sport = st.selectbox(
                "Primary Sport or Physical Activity",
                options=config.SUPPORTED_SPORTS,
                index=config.SUPPORTED_SPORTS.index(cur_sport) if cur_sport in config.SUPPORTED_SPORTS else 0,
            )
            cur_exp = existing["experience_level"] if existing else "Beginner"
            experience = st.selectbox(
                "Fitness Experience Level",
                options=config.EXPERIENCE_LEVELS,
                index=config.EXPERIENCE_LEVELS.index(cur_exp) if cur_exp in config.EXPERIENCE_LEVELS else 0,
            )
            cur_goal = existing["primary_goal"] if existing else "General fitness and wellness"
            primary_goal = st.selectbox(
                "Primary Fitness Goal",
                options=config.FITNESS_GOALS,
                index=config.FITNESS_GOALS.index(cur_goal) if cur_goal in config.FITNESS_GOALS else 0,
            )
            secondary_goals = st.multiselect(
                "Secondary Fitness Goals (optional)",
                options=[g for g in config.FITNESS_GOALS if g != primary_goal],
                default=[g for g in (existing.get("secondary_goals", []) if existing else []) if g != primary_goal],
            )
            cur_int = existing["preferred_intensity"] if existing else "Moderate"
            intensity = st.select_slider(
                "Preferred Exercise Intensity",
                options=config.INTENSITY_LEVELS,
                value=cur_int if cur_int in config.INTENSITY_LEVELS else "Moderate",
            )

        st.divider()
        c3, c4 = st.columns(2)
        with c3:
            weekly_freq = st.slider(
                "Weekly Training Frequency (days/week)",
                min_value=1,
                max_value=7,
                value=int(existing["weekly_frequency"]) if existing else 3,
            )
            duration_min = st.slider(
                "Available Workout Duration (minutes)",
                min_value=5,
                max_value=90,
                step=5,
                value=int(existing["available_duration_min"]) if existing else 25,
            )
        with c4:
            equipment = st.multiselect(
                "Available Equipment (leave empty for No Equipment)",
                options=ALL_EQUIPMENT_OPTIONS,
                default=list(existing.get("available_equipment", [])) if existing else [],
            )
            restriction_labels = st.multiselect(
                "Movement Restrictions to Avoid (safety filter)",
                options=list(RESTRICTION_OPTIONS.keys()),
                default=existing_restriction_labels,
                help="Exercises matching any selected restriction will be automatically filtered out of recommendations.",
            )

        btn_text = "Complete Onboarding & Save Profile" if is_onboarding else "Save Profile Changes"
        saved = st.form_submit_button(btn_text, type="primary", width="stretch")

    if saved:
        tags_csv = ",".join(RESTRICTION_OPTIONS[lbl] for lbl in restriction_labels)
        updated = save_athlete_profile(
            user_id=user["id"],
            full_name=full_name,
            age=int(age),
            height_cm=height_cm if height_cm > 0 else None,
            weight_kg=weight_kg if weight_kg > 0 else None,
            gender=gender,
            primary_sport=sport,
            experience_level=experience,
            primary_goal=primary_goal,
            secondary_goals=secondary_goals,
            weekly_frequency=int(weekly_freq),
            available_duration_min=int(duration_min),
            available_equipment=equipment,
            preferred_intensity=intensity,
            physical_restrictions=tags_csv,
        )
        st.session_state["auth_user"]["full_name"] = updated["full_name"]
        st.session_state["auth_user"]["onboarding_completed"] = True
        st.success("Your athlete profile has been saved! AI recommendations will now adapt automatically.")


def render_onboarding_page() -> None:
    """Page 2: Guided Athlete Onboarding."""
    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Personalization Setup</span>
            <h1>Athlete Onboarding</h1>
            <p>Tell FitMotion AI about your sport, experience, goals, time budget, and equipment so every recommendation is tailored to you.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user = get_active_user()
    if not user:
        st.warning("Please sign in or create an account in **Login & Registration** first to save your onboarding profile.")
        render_safety_footer()
        return

    existing = get_athlete_profile(user["id"])
    _render_profile_form(user, existing, is_onboarding=True)
    render_safety_footer()


def render_athlete_profile_page() -> None:
    """Page 4: Editable Athlete Profile & Excluded Exercises Manager."""
    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Athlete Settings</span>
            <h1>Athlete Profile</h1>
            <p>Update your sport, goals, equipment inventory, movement restrictions, and excluded exercises at any time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user = get_active_user()
    if not user:
        st.warning("Sign in via **Login & Registration** to view and edit your saved athlete profile.")
        render_safety_footer()
        return

    profile = get_athlete_profile(user["id"])
    _render_profile_form(user, profile, is_onboarding=False)

    # Excluded exercises management
    if profile and profile.get("excluded_exercises"):
        st.markdown('<div class="fm-section-title">Excluded Exercises</div>', unsafe_allow_html=True)
        st.caption("These exercises are currently hidden from your AI recommendations and generated routines.")
        for ex_id in profile["excluded_exercises"]:
            ex = get_exercise_by_id(ex_id)
            label = f"{ex['name']} ({ex['category']})" if ex else ex_id
            col_name, col_btn = st.columns([3, 1])
            col_name.write(f"🚫 {label}")
            if col_btn.button("Restore", key=f"restore_prof_{ex_id}", width="stretch"):
                save_exercise_feedback(user["id"], ex_id, is_excluded=False)
                st.toast(f"Restored {label}.")
                st.rerun()

    render_safety_footer()
