"""Page 13: Conversational AI Training Assistant with grounded exercise engine."""

from __future__ import annotations

import streamlit as st

from assistant import answer_training_question
from dashboard.components import get_active_profile, render_safety_footer
from recommendation import save_workout_routine

QUICK_PROMPTS: list[str] = [
    "What should I do before playing football?",
    "Give me a 15-minute full-body mobility routine.",
    "How can I improve my flexibility?",
    "Suggest a warm-up before badminton.",
    "What exercises can I do without gym equipment?",
    "Give me a beginner-friendly stretching routine.",
    "Suggest a cooldown after running.",
]


def render_ai_assistant_page() -> None:
    """Render the interactive AI Training Assistant chat interface."""
    profile, _ = get_active_profile()
    user_id = profile.get("user_id")

    st.markdown(
        """
        <div class="fm-hero">
            <span class="fm-pill fm-pill-live">● Grounded in Exercise Database · Offline Fallback Ready</span>
            <h1>AI Training Assistant</h1>
            <p>Ask natural-language questions about warm-ups, mobility, flexibility, equipment-free workouts, cooldowns, or sport-specific preparation. Responses pull directly from FitMotion AI's exercise catalog and recommendation engine.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "assistant_messages" not in st.session_state:
        st.session_state["assistant_messages"] = [
            {
                "role": "assistant",
                "content": (
                    f"Hi **{profile['full_name']}**! I'm your FitMotion AI Training Assistant. "
                    f"I'm currently calibrated for **{profile['primary_sport']}** ({profile['experience_level']}). "
                    "Click any quick question below or ask your own training question!"
                ),
                "mode": "FitMotion Local Engine (Offline-Ready)",
                "routine": None,
            }
        ]

    st.caption("Quick sample questions:")
    cols = st.columns(4)
    selected_prompt: str | None = None
    for idx, prompt_text in enumerate(QUICK_PROMPTS):
        if cols[idx % 4].button(prompt_text, key=f"qp_{idx}", width="stretch"):
            selected_prompt = prompt_text

    # Display chat history
    for msg_idx, msg in enumerate(st.session_state["assistant_messages"]):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("mode"):
                st.caption(f"Engine: `{msg['mode']}`")
            if msg.get("routine") and user_id:
                if st.button("💾 Save Suggested Routine to My Library", key=f"save_chat_r_{msg_idx}"):
                    rid = save_workout_routine(user_id, msg["routine"], is_favorite=False)
                    st.success(f"Saved routine (#{rid}) to your Workout Generator library!")

    typed_prompt = st.chat_input("Ask a training question (e.g., 'Suggest a 15-minute mobility routine without equipment')...")
    active_prompt = selected_prompt or typed_prompt

    if active_prompt:
        st.session_state["assistant_messages"].append({"role": "user", "content": active_prompt})
        with st.spinner("Consulting FitMotion AI exercise database and recommender..."):
            reply = answer_training_question(active_prompt, profile)

        st.session_state["assistant_messages"].append(
            {
                "role": "assistant",
                "content": reply["answer"],
                "mode": reply["mode"],
                "routine": reply.get("suggested_routine"),
            }
        )
        st.rerun()

    if len(st.session_state["assistant_messages"]) > 1:
        if st.button("Clear Conversation", type="secondary"):
            st.session_state.pop("assistant_messages", None)
            st.rerun()

    render_safety_footer()
