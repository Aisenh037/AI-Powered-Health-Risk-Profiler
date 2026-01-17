import streamlit as st
from frontend.utils.api import analyze_document, get_model_info

def render_sidebar():
    """Render the sidebar configuration and tools"""
    with st.sidebar:
        st.header("Configuration")
        
        # API status
        st.caption("System Status")
        st.success("Connected")
        
        st.divider()
        
        # OCR Upload Section
        st.subheader("📄 OCR Data Import")
        uploaded_file = st.file_uploader("Upload Medical Report / Survey", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            if st.button("Extract Data from Image", type="primary", use_container_width=True):
                with st.spinner("Scanning document with OCR.space engine..."):
                    ocr_result = analyze_document(uploaded_file)
                    
                    if "error" in ocr_result:
                        st.error("OCR Failed. Please try a clearer image.")
                    else:
                        st.success("Data Extracted Successfully!")
                        # Auto-fill session state from OCR results
                        extracted = ocr_result.get("answers", {})
                        
                        # Map keys to session state
                        if 'age' in extracted: st.session_state['age'] = int(extracted['age'])
                        if 'bmi' in extracted: st.session_state['bmi'] = float(extracted['bmi'])
                        if 'smoker' in extracted: st.session_state['smoker'] = bool(extracted['smoker'])
                        if 'systolic_bp' in extracted: st.session_state['systolic_bp'] = int(extracted.get('systolicbp', extracted.get('systolic_bp', 120)))
                        if 'cholesterol' in extracted: st.session_state['cholesterol'] = int(extracted['cholesterol'])
                        
                        st.rerun()

        st.divider()
        
        # Quick test profiles
        st.subheader("Test Profiles")
        
        if st.button("Load High Risk Profile"):
            st.session_state.update({
                'age': 55, 'bmi': 32.0, 'systolic_bp': 160, 'cholesterol': 260,
                'smoker': True, 'exercise': 'never', 'diet': 'high fat',
                'family_history': True, 'sleep_hours': 5.0, 'alcohol': 'heavy',
                'stress_level': 9
            })
        
        if st.button("Load Low Risk Profile"):
            st.session_state.update({
                'age': 28, 'bmi': 22.0, 'systolic_bp': 110, 'cholesterol': 170,
                'smoker': False, 'exercise': 'daily', 'diet': 'balanced',
                'family_history': False, 'sleep_hours': 8.0, 'alcohol': 'none',
                'stress_level': 2
            })
            
        st.divider()
        
        # Model info
        with st.expander("Model Architecture"):
            st.caption("Ensemble Model Performance")
            model_info = get_model_info()
            if model_info:
                for model_name, metrics in model_info.get('performance', {}).items():
                    st.text(f"{model_name.replace('_', ' ').title()}")
                    st.progress(metrics['accuracy'])
                    st.caption(f"Accuracy: {metrics['accuracy']*100:.1f}%")
