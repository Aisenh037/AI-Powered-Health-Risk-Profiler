import streamlit as st
from typing import Dict, Any

def render_form() -> Dict[str, Any]:
    """Render the patient data entry form and return inputs"""
    with st.form("risk_assessment_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Physical Metrics**")
            age = st.number_input("Age (years)", min_value=18, max_value=100, 
                                 value=st.session_state.get('age', 45))
            bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, 
                                 value=st.session_state.get('bmi', 25.0), step=0.1)
            systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=90, max_value=200,
                                         value=st.session_state.get('systolic_bp', 120))
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400,
                                         value=st.session_state.get('cholesterol', 200))
        
        with col2:
            st.markdown("**Lifestyle Indicators**")
            smoker = st.checkbox("Current Smoker", value=st.session_state.get('smoker', False))
            exercise = st.selectbox("Exercise Frequency", 
                                   ['never', 'rarely', 'occasionally', 'regularly', 'daily'],
                                   index=['never', 'rarely', 'occasionally', 'regularly', 'daily'].index(
                                       st.session_state.get('exercise', 'occasionally')))
            diet = st.selectbox("Diet Quality",
                               ['poor', 'average', 'good', 'balanced', 'high fat', 'high sugar'],
                               index=['poor', 'average', 'good', 'balanced', 'high fat', 'high sugar'].index(
                                   st.session_state.get('diet', 'balanced')))
            alcohol = st.selectbox("Alcohol Consumption",
                                  ['none', 'light', 'moderate', 'heavy'],
                                  index=['none', 'light', 'moderate', 'heavy'].index(
                                      st.session_state.get('alcohol', 'light')))
        
        with col3:
            st.markdown("**Medical History**")
            family_history = st.checkbox("Family History of Heart Disease",
                                        value=st.session_state.get('family_history', False))
            sleep_hours = st.slider("Daily Sleep (hours)", 3.0, 12.0,
                                   value=st.session_state.get('sleep_hours', 7.0), step=0.5)
            stress_level = st.slider("Stress Level (Self-reported 1-10)", 1, 10,
                                    value=st.session_state.get('stress_level', 5))
        
        st.markdown("---")
        submitted = st.form_submit_button("Analyze Risk Profile", type="primary", use_container_width=True)
        
        if submitted:
            return {
                "age": age, "bmi": bmi, "systolic_bp": systolic_bp, "cholesterol": cholesterol,
                "smoker": smoker, "exercise": exercise, "diet": diet,
                "family_history": family_history, "sleep_hours": sleep_hours,
                "alcohol": alcohol, "stress_level": stress_level
            }
        return None
