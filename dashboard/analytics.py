"""Page 16: Interactive Plotly Progress Dashboard."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.components import get_active_profile, render_safety_footer
from training import compute_progress_summary

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(18, 19, 24, 0.9)",
    plot_bgcolor="rgba(9, 9, 11, 0.65)",
    font=dict(color="#FAFAFA", family="Inter, sans-serif"),
    margin=dict(l=24, r=24, t=48, b=24),
)


def render_progress_dashboard_page() -> None:
    """Render interactive Plotly workout tracking and consistency visualizations."""
    profile, is_auth = get_active_profile()
    user_id = profile.get("user_id")

    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-phase">Plotly Activity Analytics</span>
            <h1>Progress Dashboard</h1>
            <p>Track your completed workouts, weekly training consistency, total active minutes, completion rate, and most frequently performed exercises.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not is_auth or not user_id:
        st.warning("Sign in via **Login & Registration** (or load the Demo Athlete account) to view your personal activity charts.")
        render_safety_footer()
        return

    summary = compute_progress_summary(
        user_id=user_id,
        weekly_target_frequency=int(profile.get("weekly_frequency", 3)),
    )

    # Top KPI Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Completed Workouts", summary["total_workouts"])
    k2.metric(
        "Last 7 Days Frequency",
        f"{summary['workouts_last_7_days']} / {summary['weekly_target_frequency']} target",
    )
    k3.metric("Total Training Duration", f"{summary['total_minutes']} min ({summary['total_hours']} hrs)")
    k4.metric("Avg. Workout Completion", f"{summary['avg_completion_pct']}%")

    st.markdown('<div class="fm-section-title">Weekly Schedule Goal Adherence</div>', unsafe_allow_html=True)
    st.progress(
        min(1.0, summary["weekly_goal_adherence_pct"] / 100.0),
        text=f"Weekly consistency toward your {summary['weekly_target_frequency']}-session target: {summary['weekly_goal_adherence_pct']}% ({profile['primary_goal']})",
    )
    st.caption(
        "Measurement note: These metrics track logged workout attendance, duration, and completion consistency. "
        "Workout completion alone does not directly measure physiological improvements in strength, flexibility, or cardiovascular health."
    )

    if summary["total_workouts"] == 0:
        st.info("Complete and log your first workout from the **Workout Generator**, **Weekly Planner**, or **Workout History** to populate your charts.")
        render_safety_footer()
        return

    # Row 1 Charts: Weekly Activity Volume & Daily Duration Trend
    c1, c2 = st.columns(2, gap="large")
    with c1:
        weekly_df = summary["weekly_df"]
        fig_week = go.Figure()
        fig_week.add_trace(
            go.Bar(
                x=weekly_df["week"],
                y=weekly_df["total_minutes"],
                name="Training Minutes",
                marker_color="#FC4C02",
            )
        )
        fig_week.add_trace(
            go.Scatter(
                x=weekly_df["week"],
                y=weekly_df["workouts"],
                name="Sessions",
                yaxis="y2",
                mode="lines+markers",
                line=dict(color="#00E676", width=3),
            )
        )
        fig_week.update_layout(
            title="Weekly Training Duration & Sessions",
            yaxis=dict(title="Minutes", gridcolor="rgba(148,163,184,0.12)"),
            yaxis2=dict(title="Workouts", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", y=1.12),
            **PLOTLY_LAYOUT,
        )
        st.plotly_chart(fig_week, width="stretch")

    with c2:
        daily_df = summary["daily_df"]
        fig_daily = px.area(
            daily_df,
            x="date",
            y="total_minutes",
            title="Daily Training Volume (Minutes)",
            markers=True,
            color_discrete_sequence=["#00D4FF"],
        )
        fig_daily.update_layout(
            xaxis_title="Date",
            yaxis_title="Minutes",
            yaxis=dict(gridcolor="rgba(148,163,184,0.12)"),
            **PLOTLY_LAYOUT,
        )
        st.plotly_chart(fig_daily, width="stretch")

    # Row 2 Charts: Top Performed Exercises & Category Distribution
    c3, c4 = st.columns(2, gap="large")
    with c3:
        top_df = summary["top_exercises_df"]
        if not top_df.empty:
            fig_top = px.bar(
                top_df.sort_values("Times Completed"),
                x="Times Completed",
                y="Exercise",
                orientation="h",
                title="Most Frequently Performed Exercises",
                color="Times Completed",
                color_continuous_scale=["#9A3412", "#FC4C02", "#FFB020"],
            )
            fig_top.update_layout(coloraxis_showscale=False, **PLOTLY_LAYOUT)
            st.plotly_chart(fig_top, width="stretch")
        else:
            st.info("Log exercises inside your workouts to see your top performed exercises.")

    with c4:
        cat_df = summary["category_df"]
        if not cat_df.empty:
            fig_cat = px.pie(
                cat_df,
                names="Category",
                values="Exercises Completed",
                hole=0.58,
                title="Training Category Balance",
                color_discrete_sequence=["#FC4C02", "#00E676", "#00D4FF", "#FFB020", "#A855F7", "#FF3B30", "#38BDF8", "#34D399"],
            )
            fig_cat.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig_cat, width="stretch")
        else:
            st.info("Category breakdown appears once exercises are logged.")

    render_safety_footer()
