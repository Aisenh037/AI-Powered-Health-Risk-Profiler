import requests
from typing import Dict, Any, Optional
from frontend.config import API_URL

def check_api_health() -> bool:
    """Check if API is available and ML models are loaded"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200 and response.json().get("ml_available", False)
    except:
        return False

def get_model_info() -> Dict[str, Any]:
    """Fetch ML model performance metrics"""
    try:
        response = requests.get(f"{API_URL}/model-info", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def predict_health_risk(data: Dict[str, Any]) -> Dict[str, Any]:
    """Send patient data for risk prediction"""
    try:
        response = requests.post(f"{API_URL}/predict", json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def analyze_document(file) -> Dict[str, Any]:
    """Upload document image for OCR processing"""
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{API_URL}/analyze", files=files, timeout=15)
        if response.status_code == 200:
            return response.json()
        return {"error": f"OCR failed: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
