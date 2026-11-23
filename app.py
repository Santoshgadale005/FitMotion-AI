"""FitMotion AI — Main Streamlit Entrypoint with 1-Click Sports-Tech Navigation."""

from __future__ import annotations

import streamlit as st

import config
from dashboard.analytics import render_progress_dashboard_page
from dashboard.assistant_page import render_ai_assistant_page
from dashboard.auth_pages import (
    render_athlete_profile_page,
    render_login_registration_page,
    render_onboarding_page,
)
from dashboard.components import get_active_user
from dashboard.exercise_library import render_exercise_library_page
from dashboard.home import render_main_dashboard
from dashboard.navigation import PAGE_BY_KEY, PAGES, SECTIONS
from dashboard.recommendations import (
    render_ai_recommendations_page,
    render_specialized_module_page,
    render_sport_specific_page,
    render_workout_generator_page,
)
from dashboard.styles import inject_custom_css
from dashboard.workout_planner import (
    render_weekly_planner_page,
    render_workout_history_page,
)
from database import init_db
from exercises import sync_exercises_to_db


@st.cache_resource
def _bootstrap_backend() -> int:
    """Initialize SQLite schema and ensure the 90-exercise catalog is synced once."""
    init_db()
    return sync_exercises_to_db()


def _render_sidebar() -> str:
    """Render sleek 1-click grouped navigation (WHOOP / Strava / Nike precision sidebar)."""
    if "active_page" not in st.session_state or st.session_state["active_page"] not in PAGE_BY_KEY:
        st.session_state["active_page"] = "main_dashboard"

    active_key = st.session_state["active_page"]
    active_user = get_active_user()

    with st.sidebar:
        st.markdown(
            f"""
            <div class="fm-brand-box">
                <div class="fm-brand-title">⚡ {config.APP_NAME}</div>
                <div class="fm-brand-sub">Performance · Mobility · AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if active_user:
            st.markdown(
                f'<div style="padding:0.4rem 0.65rem; border-radius:10px; background:rgba(0,230,118,0.09); border:1px solid rgba(0,230,118,0.28); font-size:0.8rem; color:#69F0AE; font-weight:600; margin-bottom:0.4rem;">● {active_user["full_name"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="padding:0.38rem 0.65rem; border-radius:10px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); font-size:0.78rem; color:#9CA3AF; margin-bottom:0.4rem;">○ Guest Preview Mode</div>',
                unsafe_allow_html=True,
            )

        for section in SECTIONS:
            st.markdown(f'<div class="fm-nav-group">{section}</div>', unsafe_allow_html=True)
            for page in [p for p in PAGES if p.section == section]:
                is_current = page.key == active_key
                if st.button(
                    f"{page.icon}  {page.title}",
                    key=f"snav_{page.key}",
                    type="primary" if is_current else "secondary",
                    width="stretch",
                ):
                    st.session_state["active_page"] = page.key
                    st.rerun()

        st.divider()
        if active_user:
            if st.button("Sign Out", key="sidebar_logout", width="stretch"):
                st.session_state.pop("auth_user", None)
                st.rerun()
        st.caption(f"FitMotion AI v{config.APP_VERSION} · 90 Exercises")

    return st.session_state["active_page"]


def _dispatch_page(page_key: str) -> None:
    """Route to the active FitMotion AI page renderer."""
    if page_key == "main_dashboard":
        render_main_dashboard()
    elif page_key == "login_registration":
        render_login_registration_page()
    elif page_key == "onboarding":
        render_onboarding_page()
    elif page_key == "athlete_profile":
        render_athlete_profile_page()
    elif page_key == "exercise_library":
        render_exercise_library_page()
    elif page_key == "ai_recommendations":
        render_ai_recommendations_page()
    elif page_key == "workout_generator":
        render_workout_generator_page()
    elif page_key == "sport_specific":
        render_sport_specific_page()
    elif page_key == "warmup_assistant":
        render_specialized_module_page(
            page_title="Warm-up Assistant",
            badge_text="Dynamic Preparation",
            subtitle="Prepare joints, raise core temperature, and activate key muscle groups safely before sports or training.",
            default_routine_type="Pre-sports warm-up",
            category_scope=["Warm-up", "Mobility"],
            default_duration=10,
            default_intensity="Low",
            state_key="mod_warmup",
        )
    elif page_key == "mobility_flexibility":
        render_specialized_module_page(
            page_title="Mobility & Flexibility",
            badge_text="GOWOD-Style Mobility Flow",
            subtitle="Build smooth joint control and relieve muscular tightness with guided mobility drills and targeted stretching.",
            default_routine_type="15-minute flexibility routine",
            category_scope=["Mobility", "Stretching and Flexibility"],
            default_duration=15,
            default_intensity="Low",
            state_key="mod_mobility",
        )
    elif page_key == "strength_conditioning":
        render_specialized_module_page(
            page_title="Strength & Conditioning",
            badge_text="Force, Stability & Endurance",
            subtitle="Equipment-aware strength, balance, and cardiovascular conditioning scaled to your athlete profile.",
            default_routine_type="30-minute strength routine",
            category_scope=["Warm-up", "Strength Training", "Balance and Stability", "Cardiovascular Training"],
            default_duration=25,
            default_intensity="Moderate",
            state_key="mod_strength",
        )
    elif page_key == "recovery_assistant":
        render_specialized_module_page(
            page_title="Recovery Assistant",
            badge_text="WHOOP-Style Active Recovery",
            subtitle="Down-regulate heart rate, ease post-session stiffness, and support rest-day recovery with low-strain routines.",
            default_routine_type="Recovery-focused routine",
            category_scope=["Recovery and Cooldown", "Stretching and Flexibility", "Mobility"],
            default_duration=15,
            default_intensity="Low",
            state_key="mod_recovery",
        )
    elif page_key == "ai_training_assistant":
        render_ai_assistant_page()
    elif page_key == "weekly_planner":
        render_weekly_planner_page()
    elif page_key == "workout_history":
        render_workout_history_page()
    elif page_key == "progress_dashboard":
        render_progress_dashboard_page()
    else:
        st.error(f"Unknown page key: {page_key}")


def main() -> None:
    """Configure Streamlit, bootstrap backend, and render the active page."""
    st.set_page_config(
        page_title=f"{config.APP_NAME} — Athlete Performance & Mobility AI",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _bootstrap_backend()
    inject_custom_css()

    selected_page_key = _render_sidebar()
    _dispatch_page(PAGE_BY_KEY[selected_page_key].key)


if __name__ == "__main__":
    main()
