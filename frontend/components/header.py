import streamlit as st

def render_header():
    """Render the application header and intro"""
    st.markdown('<div class="main-header">Health Risk Profiler</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Professional cardiovascular risk assessment system using ensemble machine learning</div>',
        unsafe_allow_html=True
    )
