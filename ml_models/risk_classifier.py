"""
ML-based Risk Classifier
Uses trained models for health risk prediction with explainability
"""

import numpy as np
import pandas as pd
import joblib
import os
from typing import Dict, Any, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLRiskClassifier:
    """ML-based health risk classifier with model ensemble and explainability"""
    
    def __init__(self, models_dir: str = "saved_models"):
        self.models_dir = models_dir
        self.models = {}
        self.label_encoder = None
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        try:
            # Load Random Forest
            rf_path = os.path.join(self.models_dir, "random_forest_latest.pkl")
            if os.path.exists(rf_path):
                self.models['random_forest'] = joblib.load(rf_path)
                logger.info("Loaded Random Forest model")
            
            # Load XGBoost
            xgb_path = os.path.join(self.models_dir, "xgboost_latest.pkl")
            if os.path.exists(xgb_path):
                self.models['xgboost'] = joblib.load(xgb_path)
                logger.info("Loaded XGBoost model")
            
            # Load Neural Network
            nn_path = os.path.join(self.models_dir, "neural_network_latest.pkl")
            if os.path.exists(nn_path):
                self.models['neural_network'] = joblib.load(nn_path)
                logger.info("Loaded Neural Network model")
            
            # Load label encoder
            le_path = os.path.join(self.models_dir, "label_encoder.pkl")
            if os.path.exists(le_path):
                self.label_encoder = joblib.load(le_path)
                logger.info("Loaded label encoder")
            
            if not self.models:
                logger.warning("No models loaded. Please train models first.")
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def prepare_input(self, answers: Dict[str, Any]) -> pd.DataFrame:
        """Convert API input to model-compatible DataFrame"""
        # Map API fields to model features
        features = {
            'age': answers.get('age', 45),
            'bmi': answers.get('bmi', self._calculate_bmi(answers)),
            'systolic_bp': answers.get('systolic_bp', 120),
            'cholesterol': answers.get('cholesterol', 200),
            'sleep_hours': answers.get('sleep_hours', 7),
            'stress_level': answers.get('stress_level', 5),
            'smoker': answers.get('smoker', False),
            'exercise': answers.get('exercise', 'occasionally'),
            'diet': answers.get('diet', 'balanced'),
            'family_history': answers.get('family_history', False),
            'alcohol': answers.get('alcohol', 'none')
        }
        
        return pd.DataFrame([features])
    
    def _calculate_bmi(self, answers: Dict[str, Any]) -> float:
        """Calculate BMI if weight and height are provided"""
        weight = answers.get('weight_kg')
        height = answers.get('height_cm')
        
        if weight and height:
            height_m = height / 100
            return round(weight / (height_m ** 2), 1)
        
        # Default BMI if not provided
        return 25.0
    
    def predict(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Make ensemble prediction with confidence scores"""
        if not self.models:
            raise ValueError("No models loaded. Please train models first.")
        
        # Prepare input
        X = self.prepare_input(answers)
        
        # Get predictions from all models
        predictions = {}
        probabilities = {}
        
        for model_name, model in self.models.items():
            pred = model.predict(X)[0]
            pred_proba = model.predict_proba(X)[0]
            
            predictions[model_name] = pred
            probabilities[model_name] = pred_proba
        
        # Ensemble prediction: weighted average of probabilities
        weights = {
            'random_forest': 0.35,
            'xgboost': 0.40,
            'neural_network': 0.25
        }
        
        ensemble_proba = np.zeros(3)  # 3 classes: low, medium, high
        for model_name, proba in probabilities.items():
            weight = weights.get(model_name, 1.0 / len(probabilities))
            ensemble_proba += proba * weight
        
        # Final prediction
        ensemble_pred = np.argmax(ensemble_proba)
        confidence = float(ensemble_proba[ensemble_pred])
        
        # Decode risk level
        risk_level = self.label_encoder.inverse_transform([ensemble_pred])[0]
        
        # Calculate risk score (0-100)
        risk_score = self._calculate_risk_score(ensemble_proba)
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'confidence': confidence,
            'probabilities': {
                'low': float(ensemble_proba[0]),
                'medium': float(ensemble_proba[1]),
                'high': float(ensemble_proba[2])
            },
            'model_predictions': {
                name: self.label_encoder.inverse_transform([pred])[0]
                for name, pred in predictions.items()
            }
        }
    
    def _calculate_risk_score(self, probabilities: np.ndarray) -> float:
        """Convert probabilities to risk score (0-100)"""
        # Weighted average: low=0, medium=50, high=100
        score = probabilities[0] * 0 + probabilities[1] * 50 + probabilities[2] * 100
        return round(score, 1)
    
    def explain_prediction(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Provide explainability for predictions using feature importance"""
        if 'random_forest' not in self.models:
            return {}
        
        X = self.prepare_input(answers)
        
        # Get feature importances from Random Forest
        try:
            model = self.models['random_forest']
            
            # Transform features
            X_transformed = model.named_steps['preprocessor'].transform(X)
            
            # Get feature names after transformation
            feature_names = self._get_feature_names(model)
            
            # Get feature importances
            importances = model.named_steps['classifier'].feature_importances_
            
            # Create importance dictionary
            feature_importance = dict(zip(feature_names, importances))
            
            # Sort by importance
            sorted_importance = sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]  # Top 5 features
            
            return {
                'top_contributing_factors': [
                    {'feature': name, 'importance': float(imp)}
                    for name, imp in sorted_importance
                ]
            }
        except Exception as e:
            logger.error(f"Error explaining prediction: {e}")
            return {}
    
    def _get_feature_names(self, model) -> List[str]:
        """Extract feature names from pipeline"""
        preprocessor = model.named_steps['preprocessor']
        
        feature_names = []
        
        # Numeric features
        num_features = preprocessor.transformers_[0][2]
        feature_names.extend(num_features)
        
        # Categorical features (after one-hot encoding)
        cat_transformer = preprocessor.transformers_[1][1]
        cat_features = preprocessor.transformers_[1][2]
        
        try:
            cat_feature_names = cat_transformer.get_feature_names_out(cat_features)
            feature_names.extend(cat_feature_names)
        except:
            feature_names.extend(cat_features)
        
        return feature_names


# Singleton instance for use in API
_classifier = None


def get_classifier() -> MLRiskClassifier:
    """Get or create classifier instance"""
    global _classifier
    if _classifier is None:
        _classifier = MLRiskClassifier()
    return _classifier


def predict_risk(answers: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for risk prediction"""
    classifier = get_classifier()
    prediction = classifier.predict(answers)
    explanation = classifier.explain_prediction(answers)
    
    # Merge predictions and explanations
    result = {**prediction, **explanation}
    
    return result
