"""
Streamlit Frontend for AI-Powered Health Risk Profiler
Connects to FastAPI backend for ML predictions
"""

import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any

# Configuration
st.set_page_config(
    page_title="AI Health Risk Profiler",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")  # Change after deployment

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .risk-high {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .risk-medium {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333 !important;
    }
    .risk-low {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333 !important;
    }
</style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if API is available"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200 and response.json().get("ml_available", False)
    except:
        return False


def get_model_info() -> Dict[str, Any]:
    """Get ML model performance metrics"""
    try:
        response = requests.get(f"{API_URL}/model-info", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}


def predict_health_risk(data: Dict[str, Any]) -> Dict[str, Any]:
    """Call ML prediction endpoint"""
    try:
        response = requests.post(f"{API_URL}/predict", json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def create_risk_gauge(risk_score: float, risk_level: str) -> go.Figure:
    """Create a gauge chart for risk score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 24}},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#a8edea'},
                {'range': [30, 60], 'color': '#ffecd2'},
                {'range': [60, 100], 'color': '#f5576c'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig


def create_probability_chart(probabilities: Dict[str, float]) -> go.Figure:
    """Create bar chart for probability distribution"""
    categories = list(probabilities.keys())
    values = [probabilities[cat] * 100 for cat in categories]
    colors = ['#a8edea', '#ffecd2', '#f5576c']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f"{v:.1f}%" for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Probability Distribution",
        xaxis_title="Risk Level",
        yaxis_title="Probability (%)",
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(range=[0, 100])
    )
    
    return fig


def create_feature_importance_chart(factors: list) -> go.Figure:
    """Create horizontal bar chart for feature importance"""
    features = [f['feature'] for f in factors]
    importances = [f['importance'] * 100 for f in factors]
    
    fig = go.Figure(go.Bar(
        x=importances,
        y=features,
        orientation='h',
        marker=dict(
            color=importances,
            colorscale='Viridis',
            showscale=True
        ),
        text=[f"{imp:.1f}%" for imp in importances],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Top Contributing Risk Factors",
        xaxis_title="Importance (%)",
        yaxis_title="Health Factor",
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


# Main App
def main():
    # Header
    st.markdown('<div class="main-header">🩺 AI-Powered Health Risk Profiler</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">ML-powered cardiovascular risk assessment with 95.86% accuracy</div>',
        unsafe_allow_html=True
    )
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ **Backend API is not available.** Please ensure the FastAPI server is running.")
        st.info(f"Looking for API at: `{API_URL}`")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API status
        st.success("✅ Backend API Connected")
        
        # Model info
        with st.expander("📊 Model Performance", expanded=False):
            model_info = get_model_info()
            if model_info:
                st.metric("Models Loaded", len(model_info.get('models_loaded', [])))
                
                for model_name, metrics in model_info.get('performance', {}).items():
                    st.markdown(f"**{model_name.replace('_', ' ').title()}**")
                    col1, col2 = st.columns(2)
                    col1.metric("Accuracy", f"{metrics['accuracy']*100:.1f}%")
                    col2.metric("F1 Score", f"{metrics['f1_score']:.3f}")
        
        st.markdown("---")
        
        # Quick test profiles
        st.header("🧪 Quick Test Profiles")
        
        if st.button("High Risk Profile", use_container_width=True):
            st.session_state.update({
                'age': 55, 'bmi': 32.0, 'systolic_bp': 160, 'cholesterol': 260,
                'smoker': True, 'exercise': 'never', 'diet': 'high fat',
                'family_history': True, 'sleep_hours': 5.0, 'alcohol': 'heavy',
                'stress_level': 9
            })
        
        if st.button("Low Risk Profile", use_container_width=True):
            st.session_state.update({
                'age': 28, 'bmi': 22.0, 'systolic_bp': 110, 'cholesterol': 170,
                'smoker': False, 'exercise': 'daily', 'diet': 'balanced',
                'family_history': False, 'sleep_hours': 8.0, 'alcohol': 'none',
                'stress_level': 2
            })
        
        st.markdown("---")
        st.markdown("Built with ❤️ using FastAPI + Streamlit")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🏥 Health Assessment", "📊 About Models", "ℹ️ How It Works"])
    
    with tab1:
        st.header("Enter Health Information")
        
        # Create form
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📏 Physical Metrics")
            age = st.number_input("Age", min_value=18, max_value=100, 
                                 value=st.session_state.get('age', 45), key='age')
            bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, 
                                 value=st.session_state.get('bmi', 25.0), step=0.1, key='bmi')
            systolic_bp = st.number_input("Systolic Blood Pressure", min_value=90, max_value=200,
                                         value=st.session_state.get('systolic_bp', 120), key='systolic_bp')
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400,
                                         value=st.session_state.get('cholesterol', 200), key='cholesterol')
        
        with col2:
            st.subheader("🚬 Lifestyle Factors")
            smoker = st.checkbox("Smoker", value=st.session_state.get('smoker', False), key='smoker')
            exercise = st.selectbox("Exercise Frequency", 
                                   ['never', 'rarely', 'occasionally', 'regularly', 'daily'],
                                   index=['never', 'rarely', 'occasionally', 'regularly', 'daily'].index(
                                       st.session_state.get('exercise', 'occasionally')), key='exercise')
            diet = st.selectbox("Diet Quality",
                               ['poor', 'average', 'good', 'balanced', 'high fat', 'high sugar'],
                               index=['poor', 'average', 'good', 'balanced', 'high fat', 'high sugar'].index(
                                   st.session_state.get('diet', 'balanced')), key='diet')
            alcohol = st.selectbox("Alcohol Consumption",
                                  ['none', 'light', 'moderate', 'heavy'],
                                  index=['none', 'light', 'moderate', 'heavy'].index(
                                      st.session_state.get('alcohol', 'light')), key='alcohol')
        
        with col3:
            st.subheader("🧬 Health History")
            family_history = st.checkbox("Family History of Heart Disease",
                                        value=st.session_state.get('family_history', False), key='family_history')
            sleep_hours = st.slider("Average Sleep (hours/night)", 3.0, 12.0,
                                   value=st.session_state.get('sleep_hours', 7.0), step=0.5, key='sleep_hours')
            stress_level = st.slider("Stress Level (1-10)", 1, 10,
                                    value=st.session_state.get('stress_level', 5), key='stress_level')
        
        # Predict button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            predict_button = st.button("🔮 Assess Health Risk", use_container_width=True, type="primary")
        
        # Make prediction
        if predict_button:
            with st.spinner("🤖 Analyzing health data with ML models..."):
                # Prepare data
                input_data = {
                    "age": age,
                    "bmi": bmi,
                    "systolic_bp": systolic_bp,
                    "cholesterol": cholesterol,
                    "smoker": smoker,
                    "exercise": exercise,
                    "diet": diet,
                    "family_history": family_history,
                    "sleep_hours": sleep_hours,
                    "alcohol": alcohol,
                    "stress_level": stress_level
                }
                
                # Get prediction
                result = predict_health_risk(input_data)
                
                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Analysis Complete!")
                    
                    # Display results
                    st.markdown("---")
                    st.header("📋 Risk Assessment Results")
                    
                    # Risk level banner
                    risk_level = result['risk_level']
                    risk_score = result['risk_score']
                    confidence = result['confidence']
                    
                    risk_class = f"risk-{risk_level}"
                    emoji = {"low": "✅", "medium": "⚠️", "high": "🚨"}
                    
                    st.markdown(f"""
                    <div class="metric-card {risk_class}">
                        <h1>{emoji.get(risk_level, '⚠️')} {risk_level.upper()} RISK</h1>
                        <h3>Confidence: {confidence*100:.1f}%</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Risk gauge
                        fig_gauge = create_risk_gauge(risk_score, risk_level)
                        st.plotly_chart(fig_gauge, use_container_width=True)
                        
                        # Model predictions
                        st.subheader("🤖 Model Consensus")
                        model_preds = result.get('model_predictions', {})
                        for model, pred in model_preds.items():
                            pred_emoji = emoji.get(pred, '⚠️')
                            st.markdown(f"**{model.replace('_', ' ').title()}**: {pred_emoji} {pred.upper()}")
                    
                    with col2:
                        # Probability distribution
                        probabilities = result.get('probabilities', {})
                        fig_prob = create_probability_chart(probabilities)
                        st.plotly_chart(fig_prob, use_container_width=True)
                    
                    # Feature importance
                    st.markdown("---")
                    st.subheader("🔍 Top Risk Factors")
                    factors = result.get('top_contributing_factors', [])
                    
                    if factors:
                        fig_factors = create_feature_importance_chart(factors)
                        st.plotly_chart(fig_factors, use_container_width=True)
                        
                        # Detailed breakdown
                        with st.expander("📝 Detailed Factor Analysis"):
                            for factor in factors:
                                st.markdown(f"- **{factor['feature'].replace('_', ' ').title()}**: "
                                          f"{factor['importance']*100:.1f}% contribution")
                    
                    # Recommendations (placeholder)
                    st.markdown("---")
                    st.subheader("💡 Health Recommendations")
                    
                    if risk_level == "high":
                        st.warning("""
                        **Based on your risk profile, consider:**
                        - 🏥 Consult with a healthcare provider immediately
                        - 🚭 Quit smoking if applicable
                        - 🏃 Increase physical activity to at least 30 minutes daily
                        - 🥗 Adopt a heart-healthy diet (Mediterranean style)
                        - 💊 Monitor blood pressure and cholesterol regularly
                        - 😌 Manage stress through meditation or counseling
                        """)
                    elif risk_level == "medium":
                        st.info("""
                        **To reduce your risk:**
                        - 🏃 Exercise at least 150 minutes per week
                        - 🥗 Improve diet quality with more fruits and vegetables
                        - 😴 Ensure 7-8 hours of quality sleep
                        - 🧘 Practice stress management techniques
                        - 📊 Regular health check-ups
                        """)
                    else:
                        st.success("""
                        **Keep up the good work!**
                        - ✅ Maintain your healthy lifestyle
                        - 🏃 Continue regular exercise
                        - 🥗 Keep eating a balanced diet
                        - 😴 Maintain good sleep habits
                        - 📊 Annual health check-ups for monitoring
                        """)
    
    with tab2:
        st.header("📊 About the ML Models")
        
        st.markdown("""
        This health risk profiler uses an **ensemble of three machine learning models** 
        trained on 10,000 synthetic health records to predict cardiovascular risk.
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🌳 Random Forest
            - **Accuracy**: 88.20%
            - **F1 Score**: 0.8761
            - **ROC-AUC**: 0.9592
            
            Provides feature importance for explainability.
            """)
        
        with col2:
            st.markdown("""
            ### 🚀 XGBoost
            - **Accuracy**: 93.25%
            - **F1 Score**: 0.9299
            - **ROC-AUC**: 0.9865
            
            Gradient boosting for high accuracy.
            """)
        
        with col3:
            st.markdown("""
            ### 🧠 Neural Network
            - **Accuracy**: 95.86%
            - **F1 Score**: 0.9586
            - **ROC-AUC**: 0.9945
            
            Deep learning for complex patterns.
            """)
        
        st.markdown("---")
        st.markdown("""
        ### Ensemble Method
        
        Predictions are combined using **weighted averaging**:
        - XGBoost: 40% weight
        - Random Forest: 35% weight
        - Neural Network: 25% weight
        
        This approach improves robustness and reduces overfitting.
        """)
    
    with tab3:
        st.header("ℹ️ How It Works")
        
        st.markdown("""
        ## 🔄 Prediction Pipeline
        
        1. **Input Collection**: You provide health metrics and lifestyle information
        2. **Data Preprocessing**: Values are standardized and encoded
        3. **ML Inference**: Three models make independent predictions
        4. **Ensemble**: Predictions are combined with weighted averaging
        5. **Explainability**: Feature importance shows which factors matter most
        6. **Results**: Risk level, score, confidence, and recommendations
        
        ## 🎯 Risk Levels
        
        - **Low Risk (0-30)**: Healthy profile, low probability of cardiovascular events
        - **Medium Risk (30-60)**: Some risk factors present, lifestyle changes recommended
        - **High Risk (60-100)**: Multiple risk factors, medical consultation advised
        
        ## 🔍 Key Features Analyzed
        
        - Physical metrics (age, BMI, blood pressure, cholesterol)
        - Lifestyle factors (smoking, exercise, diet, alcohol)
        - Health history (family history, sleep, stress)
        
        ## ⚡ Performance
        
        - **Accuracy**: 95.86% on test set
        - **Response Time**: <500ms
        - **Confidence**: Provided for transparency
        
        ## 🔒 Privacy
        
        - No data is stored permanently
        - All predictions are stateless
        - HIPAA-compliant design (when deployed with proper infrastructure)
        """)


if __name__ == "__main__":
    main()
