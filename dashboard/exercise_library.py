"""Page 5: GOWOD-Inspired 2-Column Visual Exercise Library with Quick Category Pills & Pagination."""

from __future__ import annotations

from math import ceil

import streamlit as st

import config
from athlete import get_user_feedback_map
from dashboard.components import (
    get_active_profile,
    render_gowod_grid_card,
    render_safety_footer,
)
from exercises import get_all_exercises, search_exercises

PAGE_SIZE = 12


def render_exercise_library_page() -> None:
    """Render the GOWOD-inspired visual 2-column Exercise Library."""
    profile, _ = get_active_profile()
    user_id = profile.get("user_id")
    all_exercises = get_all_exercises()

    beg_count = sum(1 for e in all_exercises if e["difficulty_level"] == "Beginner")
    int_count = sum(1 for e in all_exercises if e["difficulty_level"] == "Intermediate")
    adv_count = sum(1 for e in all_exercises if e["difficulty_level"] == "Advanced")

    st.markdown(
        f"""
        <div class="fm-hero">
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                <span class="fm-pill fm-pill-live">● {len(all_exercises)} Motion Demos</span>
                <span class="fm-pill fm-pill-cyan">{beg_count} Beginner · {int_count} Intermediate · {adv_count} Advanced</span>
            </div>
            <h1>Exercise Library</h1>
            <p>GOWOD-inspired visual movement catalog across 8 training categories and 8 sports. Select any sport to surface sport-specific drills first.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Category Pill Bar (GOWOD-style 1-click category switcher)
    if "lib_category" not in st.session_state:
        st.session_state["lib_category"] = "All"

    cat_options = ["All"] + config.EXERCISE_CATEGORIES
    pill_cols = st.columns(len(cat_options))
    short_names = {
        "All": "All",
        "Warm-up": "Warm-up",
        "Mobility": "Mobility",
        "Stretching and Flexibility": "Stretch",
        "Strength Training": "Strength",
        "Cardiovascular Training": "Cardio",
        "Balance and Stability": "Balance",
        "Recovery and Cooldown": "Recovery",
        "Sport-Specific Conditioning": "Sport Drills",
    }
    for col, cat_val in zip(pill_cols, cat_options):
        is_sel = st.session_state["lib_category"] == cat_val
        if col.button(
            short_names[cat_val],
            key=f"catpill_{cat_val}",
            type="primary" if is_sel else "secondary",
            width="stretch",
        ):
            st.session_state["lib_category"] = cat_val
            st.session_state["lib_page"] = 1
            st.rerun()

    category = st.session_state["lib_category"]

    # Search, Sport, Difficulty & Bodyweight Controls
    f1, f2, f3, f4 = st.columns([2.0, 1.1, 1.0, 1.0])
    with f1:
        query = st.text_input("Search movement or target muscle", placeholder="e.g., Nordic, Copenhagen, hip, swimming, badminton...")
    with f2:
        sport = st.selectbox("Relevant Sport", options=["All"] + config.SUPPORTED_SPORTS, key="lib_sport_sel")
    with f3:
        difficulty = st.selectbox("Difficulty", options=["All"] + config.EXPERIENCE_LEVELS, key="lib_diff_sel")
    with f4:
        st.write("")
        st.write("")
        bodyweight_only = st.checkbox("Bodyweight Only", value=False)

    filtered = search_exercises(
        query=query,
        category=category,
        difficulty=difficulty,
        sport=sport,
        bodyweight_only=bodyweight_only,
    )

    # Pagination
    total_results = len(filtered)
    total_pages = max(1, ceil(total_results / PAGE_SIZE))
    current_page = min(int(st.session_state.get("lib_page", 1)), total_pages)

    info_c, pag_c = st.columns([2.4, 1.2])
    sport_tag = f" prioritized for **{sport}**" if sport != "All" else ""
    diff_tag = f" · **{difficulty}**" if difficulty != "All" else ""
    info_c.caption(f"Showing **{total_results}** exercises{sport_tag}{diff_tag} (Page {current_page} of {total_pages})")

    if total_pages > 1:
        p1, p2, p3 = pag_c.columns([1, 1.2, 1])
        if p1.button("← Prev", disabled=(current_page <= 1), width="stretch", key="lib_prev"):
            st.session_state["lib_page"] = current_page - 1
            st.rerun()
        p2.markdown(
            f'<div style="text-align:center; padding-top:0.45rem; font-size:0.82rem; color:#A1A1AA; font-weight:600;">{current_page} / {total_pages}</div>',
            unsafe_allow_html=True,
        )
        if p3.button("Next →", disabled=(current_page >= total_pages), width="stretch", key="lib_next"):
            st.session_state["lib_page"] = current_page + 1
            st.rerun()

    if not filtered:
        st.info("No exercises match your current filters. Try switching Sport, Category, or Difficulty to 'All'.")
    else:
        start_idx = (current_page - 1) * PAGE_SIZE
        page_slice = filtered[start_idx : start_idx + PAGE_SIZE]
        feedback_map = get_user_feedback_map(user_id) if user_id else {}

        # GOWOD-style crisp 2-column grid
        for row_start in range(0, len(page_slice), 2):
            row_items = page_slice[row_start : row_start + 2]
            cols = st.columns(2, gap="medium")
            for col, ex in zip(cols, row_items):
                with col:
                    render_gowod_grid_card(
                        ex=ex,
                        user_id=user_id,
                        key_prefix=f"libg_{sport}_{difficulty}_{current_page}",
                        feedback_map=feedback_map,
                    )

    render_safety_footer()
