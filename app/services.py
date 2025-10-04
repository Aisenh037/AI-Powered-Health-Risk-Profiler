import easyocr
from PIL import Image
from io import BytesIO
from typing import Dict, Any, List
import logging

# Initialize the reader. This is done once when the app starts.
reader = easyocr.Reader(['en'])

def parse_survey_from_image(image_bytes: bytes) -> Dict[str, Any]:
    """Extracts key-value pairs from an image using EasyOCR."""
    try:
        results = reader.readtext(image_bytes)
        text = '\n'.join([res[1] for res in results])
        answers = {}
        confidences = []
        for res in results:
            if ':' in res[1]:
                line = res[1]
                confidences.append(res[2])
                key, val = line.split(':', 1)
                key = key.strip().lower().replace(" ", "").replace("-", "")
                val = val.strip().lower()
                if key in ["age"]:
                    try:
                        answers["age"] = int(val)
                    except ValueError:
                        logging.warning(f"Invalid age value: {val}")
                elif key in ["smoker", "smoking"]:
                    answers["smoker"] = val in ["yes", "true", "y", "1"]
                elif key in ["exercise", "activity"]:
                    answers["exercise"] = val
                elif key in ["diet", "food"]:
                    answers["diet"] = val
        confidence = sum(confidences) / len(confidences) if confidences else 0.0
        logging.info(f"Parsed answers from image: {answers}, confidence: {confidence}")
        return {"answers": answers, "confidence": confidence}
    except Exception as e:
        logging.error(f"OCR Error: {e}")
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