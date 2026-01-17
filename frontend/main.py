import streamlit as st
from datetime import datetime

# Import modular components
from frontend.config import setup_page_config, inject_custom_css
from frontend.utils.api import check_api_health, predict_health_risk
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.forms import render_form
from frontend.components.charts import (
    create_risk_gauge, 
    create_probability_chart, 
    create_feature_importance_chart
)
from frontend.components.reports import generate_report

# Initialize Page
setup_page_config()
inject_custom_css()

def main():
    render_header()
    
    # Check Backend Connection
    if not check_api_health():
        st.error("Backend API is unavailable. Please check connection.")
        st.stop()
    
    # Render Sidebar (OCR, Config, Tests)
    render_sidebar()
    
    # Main Tabs
    tab1, tab2, tab3 = st.tabs(["Assessment", "Model Details", "Documentation"])
    
    with tab1:
        st.subheader("Patient Data Entry")
        input_data = render_form()
        
        if input_data:
            with st.spinner("Processing data..."):
                result = predict_health_risk(input_data)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Parse results
                    risk_level = result['risk_level']
                    confidence = result['confidence']
                    risk_score = result['risk_score']
                    
                    # 1. Result Banner
                    color_map = {"low": "#27ae60", "medium": "#f39c12", "high": "#c0392b"}
                    bg_color = color_map.get(risk_level, "#34495e")
                    
                    st.markdown(f'''
                    <div style="background-color: {bg_color}; color: white; padding: 1rem; border-radius: 5px; margin-bottom: 2rem; text-align: center;">
                        <h2 style="margin:0; font-family: sans-serif;">{risk_level.upper()} RISK DETECTED</h2>
                        <p style="margin:0; opacity: 0.9;">Confidence Level: {confidence*100:.1f}%</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # 2. Charts
                    col_metrics, col_chart = st.columns([1, 1])
                    
                    with col_metrics:
                        fig_gauge = create_risk_gauge(risk_score, risk_level)
                        st.plotly_chart(fig_gauge, use_container_width=True)
                        
                        st.markdown("#### Top Risk Contributors")
                        factors = result.get('top_contributing_factors', [])
                        if factors:
                            for factor in factors:
                                name = factor['feature'].replace('_', ' ').title()
                                importance = factor['importance'] * 100
                                st.progress(factor['importance'], text=f"{name} ({importance:.1f}%)")
                    
                    with col_chart:
                        probabilities = result.get('probabilities', {})
                        fig_prob = create_probability_chart(probabilities)
                        st.plotly_chart(fig_prob, use_container_width=True)
                        
                        st.markdown("#### Model Consensus")
                        model_preds = result.get('model_predictions', {})
                        for model, pred in model_preds.items():
                            st.write(f"**{model.replace('_', ' ').title()}**: {pred.upper()}")
                    
                    # 3. Recommendations
                    st.markdown("---")
                    st.subheader("Clinical Recommendations")
                    
                    if risk_level == "high":
                        st.warning("⚠️ Immediate clinical consultation recommended. Monitor cardiovascular metrics.")
                    elif risk_level == "medium":
                        st.info("ℹ️ Lifestyle modification recommended. Follow up in 3-6 months.")
                    else:
                        st.success("✅ Maintain current healthy lifestyle habits. Standard annual check-up.")
                    
                    # 4. Report Download
                    st.markdown("---")
                    col_dl1, col_dl2 = st.columns([3, 1])
                    with col_dl2:
                        report_text = generate_report(input_data, result)
                        st.download_button(
                            label="📥 Download Clinical Report",
                            data=report_text,
                            file_name=f"risk_report_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

    with tab2:
        st.subheader("Model Performance Metrics")
        st.markdown("""
        The system utilizes an ensemble of three distinct machine learning architectures:
        1.  **Random Forest**: For robust feature importance analysis.
        2.  **XGBoost**: Gradient boosting for high predictive accuracy.
        3.  **Neural Network**: Multilayer Perceptron for complex pattern recognition.
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Random Forest Accuracy", "88.2%")
        with col2:
            st.metric("XGBoost Accuracy", "93.3%")
        with col3:
            st.metric("Neural Network Accuracy", "95.9%")
            
    with tab3:
        st.subheader("System Documentation")
        st.markdown("""
        ### Methodology
        This tool aggregates inputs across 3 vectors (Physical, Lifestyle, Medical History) to generate a composite risk score.
        
        **Privacy Note**: Use compliant data handling practices. No PII is stored.
        
        **Version**: 1.0.0-Production
        """)
        
        st.subheader("System Architecture")
        st.markdown("""
        ```mermaid
        graph LR
            A[User / Streamlit UI] -->|JSON/Image| B(FastAPI Gateway)
            B -->|Image| C[OCR Service]
            B -->|Structured Data| D{Model Ensemble}
            D -->|Vote| E[Random Forest]
            D -->|Vote| F[XGBoost]
            D -->|Vote| G[Neural Network]
            E & F & G -->|Weighted Avg| H[Final Risk Score]
            H -->|JSON| A
        ```
        """)

if __name__ == "__main__":
    main()
