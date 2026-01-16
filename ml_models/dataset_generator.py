"""
Synthetic Health Dataset Generator
Generates realistic health survey data for training ML models
"""

import numpy as np
import pandas as pd
from typing import Tuple
import os
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthDatasetGenerator:
    """Generates synthetic health data with realistic distributions"""
    
    def __init__(self, n_samples: int = 10000, random_state: int = 42):
        self.n_samples = n_samples
        self.random_state = random_state
        np.random.seed(random_state)
        
    def generate_dataset(self) -> pd.DataFrame:
        """Generate comprehensive synthetic health dataset"""
        logger.info(f"Generating {self.n_samples} synthetic health records...")
        
        # Age: Normal distribution centered at 45, range 18-85
        age = np.clip(np.random.normal(45, 15, self.n_samples), 18, 85).astype(int)
        
        # BMI: Normal distribution centered at 26, range 15-50
        bmi = np.clip(np.random.normal(26, 5, self.n_samples), 15, 50).round(1)
        
        # Blood Pressure (Systolic): Normal distribution, influenced by age and BMI
        bp_base = 120 + (age - 45) * 0.3 + (bmi - 26) * 0.5
        systolic_bp = np.clip(np.random.normal(bp_base, 15, self.n_samples), 90, 200).astype(int)
        
        # Cholesterol: Normal distribution, influenced by age and BMI
        cholesterol_base = 200 + (age - 45) * 0.5 + (bmi - 26) * 1.5
        cholesterol = np.clip(np.random.normal(cholesterol_base, 30, self.n_samples), 120, 350).astype(int)
        
        # Smoking: Age-dependent probability
        smoking_prob = 0.15 + (age > 40) * 0.05 - (age > 60) * 0.08
        smoker = np.random.random(self.n_samples) < smoking_prob
        
        # Exercise: Categorical with age dependency
        exercise_choices = ['daily', 'frequently', 'occasionally', 'rarely', 'never']
        exercise_probs_young = [0.25, 0.30, 0.25, 0.15, 0.05]  # Age < 40
        exercise_probs_old = [0.15, 0.25, 0.30, 0.20, 0.10]    # Age >= 40
        
        exercise = []
        for a in age:
            probs = exercise_probs_young if a < 40 else exercise_probs_old
            exercise.append(np.random.choice(exercise_choices, p=probs))
        
        # Diet: Categorical with BMI dependency
        diet_choices = ['balanced', 'high protein', 'high sugar', 'high fat', 'vegetarian']
        diet = []
        for b in bmi:
            if b < 22:
                probs = [0.40, 0.20, 0.10, 0.10, 0.20]
            elif b < 28:
                probs = [0.35, 0.20, 0.20, 0.15, 0.10]
            else:
                probs = [0.20, 0.15, 0.30, 0.25, 0.10]
            diet.append(np.random.choice(diet_choices, p=probs))
        
        # Family History: Random with slight age dependency
        family_history_prob = 0.30 + (age > 50) * 0.10
        family_history = np.random.random(self.n_samples) < family_history_prob
        
        # Sleep Hours: Normal distribution
        sleep_hours = np.clip(np.random.normal(7, 1.5, self.n_samples), 3, 12).round(1)
        
        # Alcohol Consumption: Categorical
        alcohol_choices = ['none', 'light', 'moderate', 'heavy']
        alcohol_probs = [0.35, 0.35, 0.20, 0.10]
        alcohol = np.random.choice(alcohol_choices, self.n_samples, p=alcohol_probs)
        
        # Stress Level: 1-10 scale
        stress_level = np.random.randint(1, 11, self.n_samples)
        
        # Calculate risk score based on multiple factors
        risk_score = self._calculate_risk_score(
            age, bmi, systolic_bp, cholesterol, smoker, exercise, 
            diet, family_history, sleep_hours, alcohol, stress_level
        )
        
        # Assign risk levels based on score
        risk_level = pd.cut(
            risk_score, 
            bins=[-np.inf, 30, 60, np.inf], 
            labels=['low', 'medium', 'high']
        )
        
        # Create DataFrame
        df = pd.DataFrame({
            'age': age,
            'bmi': bmi,
            'systolic_bp': systolic_bp,
            'cholesterol': cholesterol,
            'smoker': smoker,
            'exercise': exercise,
            'diet': diet,
            'family_history': family_history,
            'sleep_hours': sleep_hours,
            'alcohol': alcohol,
            'stress_level': stress_level,
            'risk_score': risk_score,
            'risk_level': risk_level
        })
        
        logger.info(f"Dataset generated successfully with {len(df)} records")
        logger.info(f"Risk level distribution:\n{df['risk_level'].value_counts()}")
        
        return df
    
    def _calculate_risk_score(
        self, age, bmi, bp, cholesterol, smoker, exercise, diet, 
        family_history, sleep_hours, alcohol, stress_level
    ) -> np.ndarray:
        """Calculate comprehensive risk score from all factors"""
        score = np.zeros(self.n_samples)
        
        # Age factor (0-20 points)
        score += np.clip((age - 18) / 67 * 20, 0, 20)
        
        # BMI factor (0-15 points)
        bmi_risk = np.where(bmi < 18.5, (18.5 - bmi) * 0.5,
                   np.where(bmi > 25, (bmi - 25) * 0.6, 0))
        score += np.clip(bmi_risk, 0, 15)
        
        # Blood pressure factor (0-20 points)
        bp_risk = np.maximum(0, (bp - 120) / 80 * 20)
        score += np.clip(bp_risk, 0, 20)
        
        # Cholesterol factor (0-15 points)
        chol_risk = np.maximum(0, (cholesterol - 200) / 150 * 15)
        score += np.clip(chol_risk, 0, 15)
        
        # Smoking factor (0-15 points)
        score += smoker * 15
        
        # Exercise factor (0-10 points)
        exercise_risk_map = {
            'daily': 0, 'frequently': 2, 'occasionally': 5, 
            'rarely': 8, 'never': 10
        }
        exercise_risk = np.array([exercise_risk_map[e] for e in exercise])
        score += exercise_risk
        
        # Diet factor (0-10 points)
        diet_risk_map = {
            'balanced': 0, 'high protein': 2, 'vegetarian': 1,
            'high sugar': 8, 'high fat': 9
        }
        diet_risk = np.array([diet_risk_map[d] for d in diet])
        score += diet_risk
        
        # Family history factor (0-10 points)
        score += family_history * 10
        
        # Sleep factor (0-5 points)
        sleep_risk = np.where((sleep_hours >= 6) & (sleep_hours <= 8), 0, 5)
        score += sleep_risk
        
        # Alcohol factor (0-8 points)
        alcohol_risk_map = {'none': 0, 'light': 1, 'moderate': 4, 'heavy': 8}
        alcohol_risk = np.array([alcohol_risk_map[a] for a in alcohol])
        score += alcohol_risk
        
        # Stress factor (0-7 points)
        score += (stress_level - 1) / 9 * 7
        
        return score.round(1)
    
    def save_dataset(self, df: pd.DataFrame, output_dir: str = "data/processed"):
        """Save dataset to CSV and JSON formats"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to CSV
        csv_path = os.path.join(output_dir, "health_dataset.csv")
        df.to_csv(csv_path, index=False)
        logger.info(f"Dataset saved to {csv_path}")
        
        # Save metadata
        metadata = {
            "n_samples": len(df),
            "features": list(df.columns),
            "generated_at": datetime.now().isoformat(),
            "risk_distribution": df['risk_level'].value_counts().to_dict(),
            "statistics": {
                "age": {"mean": float(df['age'].mean()), "std": float(df['age'].std())},
                "bmi": {"mean": float(df['bmi'].mean()), "std": float(df['bmi'].std())},
                "systolic_bp": {"mean": float(df['systolic_bp'].mean()), "std": float(df['systolic_bp'].std())},
                "cholesterol": {"mean": float(df['cholesterol'].mean()), "std": float(df['cholesterol'].std())},
            }
        }
        
        metadata_path = os.path.join(output_dir, "dataset_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved to {metadata_path}")
        
        return csv_path, metadata_path


def main():
    """Generate and save the dataset"""
    # Generate 10,000 samples
    generator = HealthDatasetGenerator(n_samples=10000, random_state=42)
    dataset = generator.generate_dataset()
    
    # Display basic statistics
    print("\n=== Dataset Statistics ===")
    print(f"Total samples: {len(dataset)}")
    print(f"\nRisk Level Distribution:")
    print(dataset['risk_level'].value_counts())
    print(f"\nFeature Summary:")
    print(dataset.describe())
    
    # Save dataset
    generator.save_dataset(dataset)
    print("\n✅ Dataset generation complete!")


if __name__ == "__main__":
    main()
