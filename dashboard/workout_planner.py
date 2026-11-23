"""Pages 14 & 15: Weekly Training Planner and Workout History."""

from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from dashboard.components import (
    get_active_profile,
    render_darebee_week_poster,
    render_safety_footer,
)
from exercises import get_all_exercises
from recommendation import get_user_routines
from training import (
    WORKOUT_PLANS,
    apply_workout_plan_to_week,
    assign_day_schedule,
    evaluate_weekly_load,
    generate_balanced_weekly_plan,
    get_week_schedule,
    get_week_start,
    get_workout_history,
    log_completed_workout,
    update_schedule_status,
)


def render_weekly_planner_page() -> None:
    """Page 14: Weekly Training Planner with rest-day management and load checks."""
    profile, is_auth = get_active_profile()
    user_id = profile.get("user_id")

    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Smart Load Management & Scheduling</span>
            <h1>Weekly Training Planner</h1>
            <p>Organize your 7-day training week, assign saved routines, protect rest days, and check off completed sessions—with built-in guardrails against excessive consecutive high-intensity loads.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not is_auth or not user_id:
        st.warning("Sign in via **Login & Registration** (or load the Demo Athlete account) to create and save your weekly training schedule.")
        render_safety_footer()
        return

    nav1, nav2, nav3 = st.columns([1.2, 1.4, 1.4])
    with nav1:
        week_offset = st.number_input("Week Offset (0 = This Week)", min_value=-4, max_value=8, value=0, step=1)
    week_start = get_week_start(date.today() + timedelta(weeks=int(week_offset)))
    week_end = week_start + timedelta(days=6)

    with nav2:
        st.markdown(f"#### {week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}")
    with nav3:
        if st.button("⚡ Auto-Generate Balanced Week", type="primary", width="stretch"):
            with st.spinner("Generating recovery-balanced weekly training plan..."):
                generate_balanced_weekly_plan(user_id, profile, week_start=week_start)
            st.success("Balanced weekly schedule generated with built-in rest/recovery days!")
            st.rerun()

    with st.expander("📋 Load a Complete Evidence-Based 4-Week Sport / Fitness Plan into This Week", expanded=False):
        plan_map = {f"{p['title']} ({p['difficulty']}, {p['days_per_week']}d/wk)": p["id"] for p in WORKOUT_PLANS}
        p_col1, p_col2 = st.columns([2.5, 1.0])
        chosen_plan_label = p_col1.selectbox("Select Complete Training Plan", options=list(plan_map.keys()))
        if p_col2.button("Apply Plan", type="primary", width="stretch", key="planner_apply_plan"):
            ok, msg = apply_workout_plan_to_week(user_id, plan_map[chosen_plan_label], week_start=week_start)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    week_days = get_week_schedule(user_id, week_start=week_start)
    load_summary = evaluate_weekly_load(week_days)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Planned Workouts", load_summary["planned_workouts"])
    m2.metric("Rest Days", load_summary["rest_days"])
    m3.metric("High-Intensity Days", load_summary["high_intensity_days"])
    m4.metric("Planned Volume", f"{load_summary['total_planned_minutes']} min")

    if load_summary["warnings"]:
        for warn in load_summary["warnings"]:
            st.warning(f"⚠️ **Load Balance Guidance:** {warn}")
    elif load_summary["planned_workouts"] > 0:
        st.success("Weekly training load looks well balanced with appropriate spacing and recovery.")

    st.markdown('<div class="fm-section-title">7-Day Visual Training Strip</div>', unsafe_allow_html=True)
    render_darebee_week_poster(week_days)

    st.markdown('<div class="fm-section-title">Edit & Check Off A Day</div>', unsafe_allow_html=True)
    saved_routines = get_user_routines(user_id)
    routine_options: dict[str, int | None] = {"Rest & Recovery Day": None}
    for r in saved_routines:
        star = "⭐ " if r["is_favorite"] else ""
        routine_options[f"{star}{r['title']} ({r['intensity']}, ~{r['estimated_duration_min']}m)"] = r["id"]

    day_labels = [f"{d['day_name']} ({d['date'].strftime('%b %d')}) — {d['routine_title'][:28]}" for d in week_days]
    selected_day_idx = st.selectbox(
        "Select Day to Edit or Complete",
        options=list(range(len(week_days))),
        format_func=lambda i: day_labels[i],
        key="planner_selected_day_idx",
    )
    day = week_days[selected_day_idx]

    status_icon = {
        "completed": "✅ Completed",
        "planned": "🗓️ Planned",
        "skipped": "⏭️ Skipped",
        "unscheduled": "○ Open",
    }.get(day["status"], day["status"])

    with st.container(border=True):
        c_day, c_assign, c_act = st.columns([1.3, 1.9, 1.0], gap="medium")
        with c_day:
            st.markdown(f"#### {day['day_name']} · {day['date'].strftime('%b %d')}")
            st.markdown(f"**{day['routine_title']}**")
            meta_bits = [status_icon]
            if day["intensity"]:
                meta_bits.append(f"Intensity: {day['intensity']}")
            if day["estimated_duration_min"]:
                meta_bits.append(f"~{day['estimated_duration_min']} min")
            st.caption(" · ".join(meta_bits))
            if day["notes"]:
                st.caption(f"_{day['notes']}_")

        with c_assign:
            labels = list(routine_options.keys())
            default_idx = 0
            if day["routine_id"] is not None:
                for idx, lbl in enumerate(labels):
                    if routine_options[lbl] == day["routine_id"]:
                        default_idx = idx
                        break
            chosen_lbl = st.selectbox(
                "Assign Routine or Rest Day",
                options=labels,
                index=default_idx,
                key=f"plan_sel_{day['date'].isoformat()}",
            )
            note_val = st.text_input(
                "Day Note",
                value=day["notes"],
                key=f"plan_note_{day['date'].isoformat()}",
                placeholder="Optional note (e.g., Evening match, focus on hips)...",
            )

        with c_act:
            st.write("")
            if st.button("Save Day", key=f"plan_save_{day['date'].isoformat()}", width="stretch"):
                rid = routine_options[chosen_lbl]
                assign_day_schedule(
                    user_id=user_id,
                    scheduled_date=day["date"],
                    routine_id=rid,
                    is_rest_day=(rid is None),
                    status="planned",
                    notes=note_val,
                )
                st.toast(f"Updated {day['day_name']}.")
                st.rerun()

            if day["schedule_id"] and not day["is_rest_day"] and day["status"] != "completed":
                if st.button("✅ Mark Done", key=f"plan_done_{day['date'].isoformat()}", type="primary", width="stretch"):
                    compact_ex = [
                        {
                            "exercise_id": e.get("exercise_id", ""),
                            "name": e.get("name", "Exercise"),
                            "category": e.get("category", ""),
                            "completed": True,
                        }
                        for e in day["exercises"]
                    ]
                    log_completed_workout(
                        user_id=user_id,
                        routine_id=day["routine_id"],
                        schedule_id=day["schedule_id"],
                        routine_title=day["routine_title"],
                        actual_duration_min=max(5, day["estimated_duration_min"] or 20),
                        exercises_completed=compact_ex,
                        perceived_effort_rpe=6,
                        completion_percentage=100.0,
                        notes=day["notes"] or f"Completed scheduled {day['day_name']} workout.",
                    )
                    st.success(f"Logged {day['routine_title']} to Workout History!")
                    st.rerun()
            elif day["schedule_id"] and day["status"] == "planned" and day["is_rest_day"]:
                if st.button("Confirm Rest", key=f"plan_rest_{day['date'].isoformat()}", width="stretch"):
                    update_schedule_status(user_id, day["schedule_id"], "completed")
                    st.rerun()

    render_safety_footer()


def render_workout_history_page() -> None:
    """Page 15: Workout History & Manual Session Logger."""
    profile, is_auth = get_active_profile()
    user_id = profile.get("user_id")

    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Session Logbook</span>
            <h1>Workout History</h1>
            <p>Review completed workouts, training duration, completion percentages, and log custom sessions directly to your history.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not is_auth or not user_id:
        st.warning("Sign in via **Login & Registration** to log workouts and view your workout history.")
        render_safety_footer()
        return

    with st.expander("➕ Log a Completed Workout Manually", expanded=False):
        all_exercises = get_all_exercises()
        ex_map = {f"{e['name']} ({e['category']})": e for e in all_exercises}
        with st.form("manual_log_form"):
            c1, c2 = st.columns(2)
            title = c1.text_input("Workout Title", value=f"{profile['primary_sport']} Training Session")
            duration = c2.number_input("Actual Duration (minutes)", min_value=5, max_value=180, value=25)
            c3, c4 = st.columns(2)
            completion_pct = c3.slider("Completion Percentage (%)", min_value=10, max_value=100, value=100, step=5)
            rpe = c4.slider("Perceived Effort (RPE 1 = Very Easy, 10 = Max)", min_value=1, max_value=10, value=6)
            selected_ex_labels = st.multiselect("Exercises Performed", options=list(ex_map.keys()))
            notes = st.text_area("Session Notes (optional)", placeholder="How did the session feel? Any adjustments made?")
            submitted = st.form_submit_button("Save Workout Log", type="primary", width="stretch")

        if submitted:
            compact = [
                {
                    "exercise_id": ex_map[lbl]["id"],
                    "name": ex_map[lbl]["name"],
                    "category": ex_map[lbl]["category"],
                    "completed": True,
                }
                for lbl in selected_ex_labels
            ]
            log_completed_workout(
                user_id=user_id,
                routine_title=title,
                actual_duration_min=int(duration),
                exercises_completed=compact,
                perceived_effort_rpe=int(rpe),
                completion_percentage=float(completion_pct),
                notes=notes,
            )
            st.success("Workout saved to history! Your Progress Dashboard and ML ranker have been updated.")
            st.rerun()

    logs = get_workout_history(user_id)
    if not logs:
        st.info("No completed workouts recorded yet. Log a session above or complete a routine from the Workout Generator or Weekly Planner.")
    else:
        for log in logs:
            ts_str = log["completed_at"].strftime("%b %d, %Y · %H:%M UTC")
            with st.container(border=True):
                h1, h2 = st.columns([2.5, 1.0])
                h1.markdown(f"#### {log['routine_title']}")
                h1.caption(f"{ts_str} · Duration: **{log['actual_duration_min']} min** · Completion: **{log['completion_percentage']}%**" + (f" · RPE: **{log['perceived_effort_rpe']}/10**" if log["perceived_effort_rpe"] else ""))
                h2.metric("Completed", f"{log['completion_percentage']:.0f}%")

                if log["notes"]:
                    st.write(f"_{log['notes']}_")
                if log["exercises_completed"]:
                    names = [e.get("name", e.get("exercise_id", "")) for e in log["exercises_completed"]]
                    st.caption("Exercises: " + ", ".join(names))

    render_safety_footer()
