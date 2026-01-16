# AI-Powered Health Risk Profiler - Testing Guide

## Manual Testing Guide (Step-by-Step)

This guide will help you test every feature of the ML-powered health risk profiler manually on your local machine.

---

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Dataset generated (`data/processed/health_dataset.csv` exists)
- [ ] Models trained (`saved_models/` directory with .pkl files)
- [ ] FastAPI server running (`uvicorn app.main:app --reload`)

---

## Test 1: Verify Server Status

### 1.1 Health Check Endpoint

**Command:**
```bash
curl http://127.0.0.1:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "ml_available": true
}
```

**✅ Success Criteria:**
- Status code: 200
- `ml_available` should be `true`
- Response time < 100ms

**Screenshot Location:** Take screenshot of terminal output

---

### 1.2 Interactive API Documentation

**Steps:**
1. Open browser
2. Navigate to `http://127.0.0.1:8000/docs`
3. Verify all endpoints are visible:
   - POST `/analyze`
   - POST `/predict`
   - GET `/model-info`

**✅ Success Criteria:**
- Swagger UI loads correctly
- All 3 endpoints visible
- Schemas section populated

**Screenshot Location:** Take screenshot of Swagger UI

---

## Test 2: Rule-Based Prediction (/analyze)

### 2.1 High Risk Case (Manual Testing)

**Steps:**
1. Open `http://127.0.0.1:8000/docs`
2. Expand POST `/analyze`
3. Click "Try it out"
4. Enter test data:
```json
{
  "age": 55,
  "smoker": true,
  "exercise": "never",
  "diet": "high fat"
}
```
5. Click "Execute"

**Expected Response:**
```json
{
  "risk_level": "high",
  "factors": ["smoking", "low exercise", "poor diet"],
  "recommendations": [
    "Quit smoking",
    "Walk 30 mins daily",
    "Reduce sugar"
  ],
  "status": "ok",
  "confidence": 1.0
}
```

**✅ Success Criteria:**
- Risk level = "high"
- All 3 factors identified
- 3 recommendations provided
- Confidence = 1.0

---

### 2.2 Low Risk Case

**Test Data:**
```json
{
  "age": 25,
  "smoker": false,
  "exercise": "daily",
  "diet": "balanced"
}
```

**Expected:**
- Risk level = "low"
- Factors = [] (empty)
- Status = "ok"

---

### 2.3 Medium Risk Case

**Test Data:**
```json
{
  "age": 45,
  "smoker": false,
  "exercise": "occasionally",
  "diet": "high sugar"
}
```

**Expected:**
- Risk level = "medium"
- Factors include "poor diet"

---

## Test 3: ML-Based Prediction (/predict)

### 3.1 Comprehensive High Risk Case

**Test Data:**
```json
{
  "age": 58,
  "bmi": 32.5,
  "systolic_bp": 160,
  "cholesterol": 280,
  "smoker": true,
  "exercise": "never",
  "diet": "high fat",
  "family_history": true,
  "sleep_hours": 5.0,
  "alcohol": "heavy",
  "stress_level": 9
}
```

**Manual Testing Steps:**
1. Open Swagger UI at `/docs`
2. Expand POST `/predict`
3. Click "Try it out"
4. Paste the JSON above
5. Click "Execute"
6. Record the response

**Expected Response Structure:**
```json
{
  "risk_level": "high",
  "risk_score": 70-90,
  "confidence": 0.75-0.95,
  "probabilities": {
    "low": 0.0-0.1,
    "medium": 0.0-0.15,
    "high": 0.75-1.0
  },
  "model_predictions": {
    "random_forest": "high",
    "xgboost": "high",
    "neural_network": "high"
  },
  "top_contributing_factors": [
    /* Array of 5 features with importance scores */
  ],
  "status": "ok"
}
```

**✅ Success Criteria:**
- Risk level = "high"
- Confidence > 0.7
- All 3 models agree (all predict "high")
- Top factors include: age, bmi, systolic_bp, family_history, smoker
- Feature importance values sum to ~1.0

**Record:** 
- Response time: ____ms
- Confidence score: ____
- Top contributing factor: ____

---

### 3.2 Healthy Profile (Low Risk)

**Test Data:**
```json
{
  "age": 28,
  "bmi": 22.0,
  "systolic_bp": 110,
  "cholesterol": 170,
  "smoker": false,
  "exercise": "daily",
  "diet": "balanced",
  "family_history": false,
  "sleep_hours": 8.0,
  "alcohol": "none",
  "stress_level": 2
}
```

**Expected:**
- Risk level = "low"
- Confidence > 0.80
- Probability for "low" > 0.7

---

### 3.3 Borderline Case (Test Model Uncertainty)

**Test Data:**
```json
{
  "age": 40,
  "bmi": 26.0,
  "systolic_bp": 130,
  "cholesterol": 210,
  "smoker": false,
  "exercise": "occasionally",
  "diet": "balanced",
  "family_history": false,
  "sleep_hours": 7.0,
  "alcohol": "light",
  "stress_level": 5
}
```

**Expected:**
- Risk level = "medium" or "low"
- Confidence might be lower (0.6-0.8)
- Probabilities more distributed
- Models might disagree slightly

**Analysis:** This tests how models handle uncertainty

---

### 3.4 Missing Optional Fields (Default Values)

**Test Data (Minimal):**
```json
{
  "age": 50
}
```

**Expected:**
- Should work with defaults
- BMI defaults to 25.0
- BP defaults to 120
- Cholesterol defaults to 200
- All lifestyle factors use safe defaults

---

## Test 4: Model Information (/model-info)

**Manual Testing:**
1. Navigate to Swagger UI
2. Expand GET `/model-info`
3. Click "Try it out"
4. Click "Execute"

**Expected Response:**
```json
{
  "models_loaded": [
    "random_forest",
    "xgboost",
    "neural_network"
  ],
  "timestamp": "2026-01-16T...",
  "performance": {
    "neural_network": {
      "accuracy": ~0.96,
      "f1_score": ~0.96,
      "roc_auc": ~0.99
    },
    "xgboost": {
      "accuracy": ~0.93,
      "f1_score": ~0.93,
      "roc_auc": ~0.99
    },
    "random_forest": {
      "accuracy": ~0.88,
      "f1_score": ~0.88,
      "roc_auc": ~0.96
    }
  }
}
```

**✅ Success Criteria:**
- All 3 models listed
- Neural Network has highest accuracy
- All F1 scores > 0.85
- ROC-AUC scores > 0.95

---

## Test 5: Automated Testing Script

Create and run comprehensive automated tests:

**File: `tests/test_api_comprehensive.py`**

Run with:
```bash
python tests/test_api_comprehensive.py
```

**Expected Output:**
```
========================================
Running Comprehensive API Tests
========================================

Test 1: Health Check ..................... ✓ PASSED
Test 2: Model Info ....................... ✓ PASSED
Test 3: Rule-Based High Risk ............. ✓ PASSED
Test 4: Rule-Based Low Risk .............. ✓ PASSED
Test 5: ML High Risk ..................... ✓ PASSED
Test 6: ML Low Risk ...................... ✓ PASSED
Test 7: ML Borderline Case ............... ✓ PASSED
Test 8: ML Minimal Input ................. ✓ PASSED
Test 9: Performance (< 500ms) ............ ✓ PASSED

========================================
Results: 9/9 tests passed ✓
========================================
```

---

## Test 6: Load Testing

### 6.1 Concurrent Requests Test

**Script: `tests/load_test.py`**

Run:
```bash
python tests/load_test.py
```

**Success Criteria:**
- Handle 10 concurrent requests
- Average response time < 1000ms
- No errors or timeouts
- Memory usage stable

---

## Test 7: Edge Cases & Error Handling

### 7.1 Invalid Input (Age Out of Range)

**Test Data:**
```json
{
  "age": 200,
  "smoker": false,
  "exercise": "daily",
  "diet": "balanced"
}
```

**Expected:** Model should still predict (data validation in schema allows it)

---

### 7.2 Invalid Enum Value

**Test Data:**
```json
{
  "age": 40,
  "exercise": "invalid_value",
  "smoker": false,
  "diet": "balanced"
}
```

**Expected:** Model handles unknown categories gracefully

---

### 7.3 Models Not Available (Simulate Failure)

**Steps:**
1. Temporarily rename `saved_models/` to `saved_models_backup/`
2. Restart server
3. Try calling `/predict`

**Expected:**
- 503 Service Unavailable
- Error message: "ML models not available"
- `/analyze` endpoint still works (fallback)

4. Rename folder back and restart

---

## Test 8: End-to-End User Scenarios

### Scenario 1: Young Healthy Individual

**Profile:**
- Age: 25
- Athletic, non-smoker
- Good sleep, low stress

**Test:**
1. Call `/predict` with healthy parameters
2. Verify low risk prediction
3. Check that no recommendations needed

---

### Scenario 2: At-Risk Executive

**Profile:**
- Age: 52
- Sedentary job, high stress
- Family history of heart disease
- Poor sleep

**Test:**
1. Call `/predict` with risk factors
2. Verify medium/high risk
3. Verify top factors include stress, sleep, family_history

---

### Scenario 3: Lifestyle Improvement

**Test:**
1. Submit high-risk profile
2. Note recommendations
3. Submit improved profile (e.g., stopped smoking, exercise daily)
4. Verify risk level decreased

---

## Test 9: Documentation Completeness

### 9.1 OpenAPI Schema

**Steps:**
1. Visit `http://127.0.0.1:8000/openapi.json`
2. Verify all endpoints documented
3. Check schema definitions complete

---

### 9.2 Example Responses

**Verify:**
- Each endpoint has example responses
- Schemas show all fields
- Data types are correct

---

## Test 10: Performance Benchmarking

**Run:**
```bash
python tests/benchmark.py
```

**Metrics to Record:**

| Endpoint | Avg Time (ms) | Min (ms) | Max (ms) | Throughput (req/s) |
|----------|---------------|----------|----------|-------------------|
| /health  |               |          |          |                   |
| /analyze |               |          |          |                   |
| /predict |               |          |          |                   |
| /model-info |            |          |          |                   |

**Target Performance:**
- `/health`: < 50ms
- `/analyze`: < 100ms
- `/predict`: < 500ms
- `/model-info`: < 100ms

---

## Manual Testing Checklist

After completing all tests, verify:

- [ ] All endpoints return correct status codes
- [ ] ML predictions have > 80% confidence for clear cases
- [ ] All 3 models loaded successfully
- [ ] Feature importance always returns 5 factors
- [ ] Response times acceptable (< 500ms)
- [ ] No memory leaks during load testing
- [ ] Error handling works correctly
- [ ] Documentation is complete
- [ ] Screenshots captured for all key features
- [ ] Test results documented

---

## Recording Test Results

Create a test report:

**File: `TEST_RESULTS.md`**

Structure:
```markdown
# Test Execution Report
Date: [Date]
Tester: [Your Name]

## Summary
- Total Tests: X
- Passed: X
- Failed: X
- Success Rate: X%

## Individual Test Results
[Table with all test results]

## Issues Found
[List any issues]

## Screenshots
[Embed screenshots]

## Recommendations
[Any improvements needed]
```

---

## Next Steps

After manual testing:
1. Document all results
2. Take screenshots of key features
3. Create video demo (optional)
4. Update README with test results
5. Prepare project presentation
