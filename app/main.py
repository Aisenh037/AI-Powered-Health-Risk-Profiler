from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Body, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Optional
from . import schemas, services
import os
import json

app = FastAPI(title="AI-Powered Health Risk Profiler")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check ---
@app.get("/health", summary="Health Check", include_in_schema=False)
async def health_check():
    return {"status": "healthy", "ml_available": services.is_ml_available()}

# --- Serve the Simulator ---
@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_simulator():
    simulator_path = os.path.join(os.path.dirname(__file__), '..', 'simulator.html')
    if not os.path.exists(simulator_path):
        raise HTTPException(status_code=404, detail="simulator.html not found")
    return FileResponse(simulator_path)


# --- Analyze Endpoint (Rule-based) ---
@app.post("/analyze",
          response_model=Union[schemas.Recommendations, schemas.IncompleteProfileError],
          summary="Analyze Health Survey from JSON or Image (Rule-based)")
async def analyze_survey(
    request: Request,
    file: Optional[UploadFile] = File(None)
):
    answers = {}
    confidence = 0.0
    if file:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
        image_bytes = await file.read()
        parsed = services.parse_survey_from_image(image_bytes)
        answers = parsed["answers"]
        confidence = parsed["confidence"]
    else:
        try:
            survey_json = await request.json()
            survey_data = schemas.SurveyInput(**survey_json)
            answers = survey_data.dict()
            confidence = 1.0
        except Exception:
            raise HTTPException(status_code=422, detail="Invalid JSON format in request body.")

    required_fields = ["age", "smoker", "exercise", "diet"]
    missing_fields = [field for field in required_fields if field not in answers]
    if len(missing_fields) > len(required_fields) / 2:
        return schemas.IncompleteProfileError(status="incomplete_profile", reason=f">50% fields missing. Missing: {', '.join(missing_fields)}")

    factors = services.extract_factors(answers)
    risk_profile = services.classify_risk(factors)
    final_recommendations = services.generate_recommendations(risk_level=risk_profile["risk_level"], factors=factors)
    final_recommendations["confidence"] = confidence
    return schemas.Recommendations(**final_recommendations)


# --- ML Prediction Endpoint ---
@app.post("/predict",
          response_model=schemas.MLPredictionResponse,
          summary="ML-based Health Risk Prediction with Explainability")
async def predict_health_risk(input_data: schemas.MLPredictionInput):
    """
    ML-based health risk prediction using ensemble of Random Forest, XGBoost, and Neural Network.
    Provides risk level, confidence scores, probabilities, and explainability features.
    """
    if not services.is_ml_available():
        raise HTTPException(status_code=503, detail="ML models not available. Please train models first.")
    
    # Convert input to dict
    answers = input_data.dict()
    
    # Get ML prediction
    result = services.predict_health_risk_ml(answers)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return schemas.MLPredictionResponse(**result)


# --- Model Info Endpoint ---
@app.get("/model-info",
         response_model=schemas.ModelInfo,
         summary="Get ML Model Information and Performance Metrics")
async def get_model_info():
    """Returns information about loaded ML models and their performance metrics."""
    if not services.is_ml_available():
        raise HTTPException(status_code=503, detail="ML models not available.")
    
    try:
        # Load training results
        results_path = os.path.join(os.path.dirname(__file__), '..', 'saved_models', 'training_results.json')
        
        if not os.path.exists(results_path):
            raise HTTPException(status_code=404, detail="Training results not found.")
        
        with open(results_path, 'r') as f:
            data = json.load(f)
        
        # Extract model names and performance
        models_loaded = list(data['models'].keys())
        performance = {
            model_name: {
                'accuracy': model_data['accuracy'],
                'f1_score': model_data['f1_score'],
                'roc_auc': model_data['roc_auc']
            }
            for model_name, model_data in data['models'].items()
        }
        
        return schemas.ModelInfo(
            models_loaded=models_loaded,
            timestamp=data['timestamp'],
            performance=performance
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model info: {str(e)}")

