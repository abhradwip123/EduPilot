import streamlit as st


def render_header():
    st.markdown(
        """
        <div style="padding: 0.25rem 0 1.1rem 0; border-bottom: 1px solid #E5E7EB; margin-bottom: 1.4rem;">
            <h1 style="color:#1D4ED8; margin-bottom:0; font-size:2.1rem;">EduPilot</h1>
            <p style="color:#4B5563; font-size:1.05rem; margin:0.15rem 0 0.6rem 0;">
                Your Adaptive AI Learning Companion
            </p>
            <p style="color:#374151; font-size:0.95rem; max-width:760px; margin:0;">
                EduPilot assesses what you know, identifies where you struggle,
                teaches you, and adapts its strategy based on your performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )