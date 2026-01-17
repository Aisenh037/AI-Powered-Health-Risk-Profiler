import plotly.graph_objects as go
from typing import Dict, List

def create_risk_gauge(risk_score: float, risk_level: str) -> go.Figure:
    """Create a gauge chart showing the risk score"""
    colors = {'low': '#2ecc71', 'medium': '#f39c12', 'high': '#e74c3c'}
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 20, 'color': '#2c3e50'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#7f8c8d"},
            'bar': {'color': "#2c3e50"},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#e0e0e0",
            'steps': [
                {'range': [0, 30], 'color': '#ebfbf0'},  # Very light green
                {'range': [30, 60], 'color': '#fef7e6'}, # Very light orange
                {'range': [60, 100], 'color': '#fdedec'} # Very light red
            ],
            'threshold': {
                'line': {'color': colors.get(risk_level, '#2c3e50'), 'width': 4},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        font={'family': "Arial, sans-serif"}
    )
    return fig

def create_probability_chart(probabilities: Dict[str, float]) -> go.Figure:
    """Create a bar chart of class probabilities"""
    categories = [k.capitalize() for k in probabilities.keys()]
    values = [probabilities[k.lower()] * 100 for k in categories]
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f"{v:.1f}%" for v in values],
            textposition='auto',
            width=0.5
        )
    ])
    
    fig.update_layout(
        title="Prediction Probabilities",
        xaxis_title="Risk Category",
        yaxis_title="Probability (%)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(range=[0, 100]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_feature_importance_chart(factors: List[Dict[str, float]]) -> go.Figure:
    """Create a horizontal bar chart of top contributing factors"""
    features = [f['feature'].replace('_', ' ').title() for f in factors]
    importances = [f['importance'] * 100 for f in factors]
    
    fig = go.Figure(go.Bar(
        x=importances,
        y=features,
        orientation='h',
        marker=dict(color='#3498db'),
        text=[f"{imp:.1f}%" for imp in importances],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Key Contributing Factors",
        xaxis_title="Impact (%)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig
