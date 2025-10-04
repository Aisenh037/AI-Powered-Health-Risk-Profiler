# AI-Powered Health Risk Profiler

A FastAPI-based service that analyzes lifestyle survey responses from JSON or image inputs using OCR, extracts risk factors, classifies health risk levels, and provides actionable recommendations.

## Architecture

The application follows a modular architecture with the following components:

- **FastAPI App**: Main application with CORS middleware and endpoints.
- **Schemas**: Pydantic models for input validation and response formatting.
- **Services**: Business logic for OCR parsing, factor extraction, risk classification, and recommendations.
- **Simulator**: HTML frontend for testing the API.

### Workflow

1. **Input Processing**: Accepts JSON survey data or image files.
2. **OCR/Text Parsing**: Extracts key fields (age, smoker, exercise, diet) from images using EasyOCR.
3. **Factor Extraction**: Converts answers into risk factors (smoking, poor diet, low exercise).
4. **Risk Classification**: Calculates risk score and level based on factors.
5. **Recommendations**: Generates personalized health recommendations.

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd health-risk-profiles
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the simulator at `http://127.0.0.1:8000/`

6. API documentation at `http://127.0.0.1:8000/docs`

## API Usage

### Endpoint: POST /analyze

Analyzes health survey data and returns risk profile and recommendations.

#### Request

- **Content-Type**: `application/json` for JSON input or `multipart/form-data` for image input.

#### JSON Input Example

```json
{
  "age": 42,
  "smoker": true,
  "exercise": "rarely",
  "diet": "high sugar"
}
```

#### Image Input

Upload an image file with survey text in key-value format (e.g., "Age: 42\nSmoker: yes").

#### Sample Curl Requests

**JSON Input:**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"age":42,"smoker":true,"exercise":"rarely","diet":"high sugar"}'
```

**Image Input:**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -F "file=@survey_image.jpg"
```

**Incomplete Profile (JSON with missing fields):**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"age":42,"smoker":true}'
```

#### Response

**Successful Analysis:**
```json
{
  "risk_level": "high",
  "factors": ["smoking", "poor diet", "low exercise"],
  "recommendations": ["Quit smoking", "Reduce sugar", "Walk 30 mins daily"],
  "status": "ok",
  "confidence": 0.92
}
```

**Incomplete Profile:**
```json
{
  "status": "incomplete_profile",
  "reason": ">50% fields missing. Missing: exercise, diet"
}
```

## Features

- **Dual Input Support**: JSON and image (OCR) inputs.
- **Guardrails**: Handles incomplete profiles with >50% missing fields.
- **Error Handling**: Validates inputs and provides meaningful error messages.
- **Modular Design**: Separates concerns for easy maintenance and extension.
- **CORS Enabled**: Supports cross-origin requests for web integration.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **EasyOCR**: OCR library for text extraction from images.
- **Pillow**: Image processing.
- **Pydantic**: Data validation and serialization.
- **Uvicorn**: ASGI server.

## Evaluation Notes

- **Correctness**: API responses adhere to defined schemas.
- **OCR Handling**: Robust parsing with logging and error handling.
- **Guardrails**: Incomplete data detection and appropriate responses.
- **Code Quality**: Organized, documented, and reusable code.
- **AI Integration**: Uses OCR for input processing and rule-based logic for analysis.

For demo purposes, run locally and use ngrok for public access if needed.
