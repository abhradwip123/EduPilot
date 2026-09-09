import streamlit as st

# Order matters: this is the pipeline from the spec.
#   Goal -> Assess -> Analyze -> Teach -> Quiz -> Evaluate -> Adapt
STAGES = [
    ("goal", "Goal"),
    ("assess", "Assessment"),
    ("analyze", "Weakness Analysis"),
    ("teach", "Teaching"),
    ("quiz", "Quiz"),
    ("evaluate", "Evaluation"),
    ("adapt", "Adaptation"),
]

_STAGE_KEYS = [key for key, _ in STAGES]


def render_agent_workflow(current_stage: str):
    """Renders a simple ✓ / ● / ○ workflow strip so judges can see, at a
    glance, which stage of the agent loop EduPilot is currently in."""

    current_index = (
        _STAGE_KEYS.index(current_stage) if current_stage in _STAGE_KEYS else 0
    )

    with st.container(border=True):
        st.caption("EduPilot Agent Status")
        cols = st.columns(len(STAGES))

        for i, (_, label) in enumerate(STAGES):
            with cols[i]:
                if i < current_index:
                    st.markdown(f"✅\n\n{label}")
                elif i == current_index:
                    st.markdown(f"**●**\n\n**{label}**")
                else:
                    st.markdown(f"○\n\n{label}")