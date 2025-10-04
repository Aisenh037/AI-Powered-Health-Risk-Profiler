from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Body, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Optional
from . import schemas, services
import os

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
    return {"status": "healthy"}

# --- Serve the Simulator ---
@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_simulator():
    simulator_path = os.path.join(os.path.dirname(__file__), '..', 'simulator.html')
    if not os.path.exists(simulator_path):
        raise HTTPException(status_code=404, detail="simulator.html not found")
    return FileResponse(simulator_path)


# --- Analyze Endpoint ---
@app.post("/analyze",
          response_model=Union[schemas.Recommendations, schemas.IncompleteProfileError],
          summary="Analyze Health Survey from JSON or Image")
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
