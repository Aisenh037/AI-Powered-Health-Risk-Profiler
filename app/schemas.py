from pydantic import BaseModel
from typing import List, Optional

# Input schema for JSON requests
class SurveyInput(BaseModel):
    age: int
    smoker: bool
    exercise: str
    diet: str

# Schema for the parsed answers from Step 1
class ParsedAnswers(BaseModel):
    answers: dict
    missing_fields: List[str]
    confidence: float

# Schema for the extracted factors from Step 2
class ExtractedFactors(BaseModel):
    factors: List[str]
    confidence: float

# Schema for the risk classification from Step 3
class RiskProfile(BaseModel):
    risk_level: str
    score: int
    rationale: List[str]

# Schema for the final recommendations from Step 4
class Recommendations(BaseModel):
    risk_level: str
    factors: List[str]
    recommendations: List[str]
    status: str
    confidence: float

# Schema for guardrail/error responses
class IncompleteProfileError(BaseModel):
    status: str
    reason: str