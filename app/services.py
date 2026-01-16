import requests
import base64
from PIL import Image
from io import BytesIO
from typing import Dict, Any, List
import logging
import os
import sys

# OCR configuration (using OCR.space free API)
OCR_API_KEY = 'helloworld'  # Free public key for demo
OCR_URL = 'https://api.ocr.space/parse/image'

# Try to import ML classifier
try:
    # Add parent directory to path to import from ml_models
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from ml_models.risk_classifier import get_classifier, predict_risk
    ML_AVAILABLE = True
    logging.info("ML models loaded successfully")
except Exception as e:
    ML_AVAILABLE = False
    logging.warning(f"ML models not available: {e}")

def parse_survey_from_image(image_bytes: bytes) -> Dict[str, Any]:
    """Extracts key-value pairs from an image using OCR.space API."""
    try:
        # Convert image bytes to base64 for API transmission
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        payload = {
            'apikey': OCR_API_KEY,
            'base64Image': f"data:image/jpeg;base64,{image_base64}",
            'language': 'eng',
            'isOverlayRequired': False
        }
        
        response = requests.post(OCR_URL, data=payload, timeout=10)
        result = response.json()
        
        if result.get('OCRExitCode') != 1:
            error_msg = result.get('ErrorMessage', 'Unknown OCR error')
            logging.error(f"OCR API Error: {error_msg}")
            return {"answers": {}, "confidence": 0.0}

        # Extract text from lines
        text_lines = []
        parsed_results = result.get('ParsedResults', [])
        for res in parsed_results:
            text_lines.extend(res.get('ParsedText', '').split('\n'))

        answers = {}
        for line in text_lines:
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip().lower().replace(" ", "").replace("-", "")
                val = val.strip().lower()
                
                if key in ["age"]:
                    try:
                        answers["age"] = int(val)
                    except ValueError:
                        logging.warning(f"Invalid age value: {val}")
                elif key in ["smoker", "smoking"]:
                    answers["smoker"] = any(word in val for word in ["yes", "true", "y", "1"])
                elif key in ["exercise", "activity"]:
                    answers["exercise"] = val
                elif key in ["diet", "food"]:
                    answers["diet"] = val

        logging.info(f"Parsed answers from API OCR: {answers}")
        return {"answers": answers, "confidence": 0.8} # Static confidence for API
    except Exception as e:
        logging.error(f"OCR API Call Error: {e}")
        return {"answers": {}, "confidence": 0.0}

def extract_factors(answers: Dict[str, Any]) -> List[str]:
    """Converts survey answers into standardized risk factors."""
    factors = []
    if answers.get("smoker"):
        factors.append("smoking")
    if answers.get("diet") in ["high sugar", "processed", "high-fat"]:
        factors.append("poor diet")
    if answers.get("exercise") in ["rarely", "never", "infrequently"]:
        factors.append("low exercise")
    return factors

FACTOR_RISK_SCORES = { "smoking": 35, "poor diet": 25, "low exercise": 20 }

def classify_risk(factors: List[str]) -> Dict[str, Any]:
    """Calculates a risk score and level based on factors."""
    score = sum(FACTOR_RISK_SCORES.get(factor, 0) for factor in factors)
    risk_level = "low"
    if score > 60: risk_level = "high"
    elif score > 30: risk_level = "medium"
    return {"risk_level": risk_level, "score": score, "rationale": factors}

RECOMMENDATION_MAP = {
    "smoking": "Quit smoking",
    "poor diet": "Reduce sugar",
    "low exercise": "Walk 30 mins daily"
}

def generate_recommendations(risk_level: str, factors: List[str]) -> Dict[str, Any]:
    """Generates actionable recommendations based on factors."""
    recs = [RECOMMENDATION_MAP.get(factor) for factor in factors if factor in RECOMMENDATION_MAP]
    return {"risk_level": risk_level, "factors": factors, "recommendations": recs, "status": "ok"}

# ML Prediction Functions
def predict_health_risk_ml(answers: Dict[str, Any]) -> Dict[str, Any]:
    """ML-based health risk prediction with explainability."""
    if not ML_AVAILABLE:
        return {"error": "ML models not available. Please train models first."}
    
    try:
        result = predict_risk(answers)
        return result
    except Exception as e:
        logging.error(f"ML prediction error: {e}")
        return {"error": f"ML prediction failed: {str(e)}"}

def is_ml_available() -> bool:
    """Check if ML models are available."""
    return ML_AVAILABLE
