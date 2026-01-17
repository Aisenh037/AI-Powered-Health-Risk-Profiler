import streamlit as st

# API Configuration
# Reads from Streamlit secrets or defaults to local development URL
API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")

def setup_page_config():
    """Initialize Streamlit page settings"""
    st.set_page_config(
        page_title="AI Health Risk Profiler",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def inject_custom_css():
    """Inject global CSS styles"""
    st.markdown("""
    <style>
        .main-header {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 1.1rem;
            color: #7f8c8d;
            margin-bottom: 2rem;
        }
        .metric-container {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1.5rem;
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 1rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 4px;
            height: 3rem;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
