"""
Model Trainer for Health Risk Classification
Trains and evaluates multiple ML models: RandomForest, XGBoost, and Neural Network
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import xgboost as xgb
import joblib
import json
import os
from datetime import datetime
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthRiskModelTrainer:
    """Trains and evaluates multiple ML models for health risk classification"""
    
    def __init__(self, data_path: str = "data/processed/health_dataset.csv"):
        self.data_path = data_path
        self.models = {}
        self.results = {}
        self.label_encoder = LabelEncoder()
        self.preprocessor = None
        
    def load_data(self) -> pd.DataFrame:
        """Load dataset from CSV"""
        logger.info(f"Loading dataset from {self.data_path}")
        df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(df)} samples with {len(df.columns)} features")
        return df
    
    def prepare_data(self, df: pd.DataFrame):
        """Prepare features and target for training"""
        logger.info("Preparing data for training...")
        
        # Define feature columns
        numeric_features = ['age', 'bmi', 'systolic_bp', 'cholesterol', 'sleep_hours', 'stress_level']
        categorical_features = ['smoker', 'exercise', 'diet', 'family_history', 'alcohol']
        
        # Features and target
        X = df[numeric_features + categorical_features]
        y = df['risk_level']
        
        # Encode target variable: low=0, medium=1, high=2
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Create preprocessing pipeline
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
            ]
        )
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        logger.info(f"Training set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
        logger.info(f"Class distribution: {np.bincount(y_encoded)}")
        
        return X_train, X_test, y_train, y_test
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest Classifier"""
        logger.info("Training Random Forest...")
        
        pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ))
        ])
        
        pipeline.fit(X_train, y_train)
        self.models['random_forest'] = pipeline
        logger.info("Random Forest trained successfully")
        
        return pipeline
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost Classifier"""
        logger.info("Training XGBoost...")
        
        pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', xgb.XGBClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                eval_metric='mlogloss',
                n_jobs=-1
            ))
        ])
        
        pipeline.fit(X_train, y_train)
        self.models['xgboost'] = pipeline
        logger.info("XGBoost trained successfully")
        
        return pipeline
    
    def train_neural_network(self, X_train, y_train):
        """Train Neural Network (MLP) Classifier"""
        logger.info("Training Neural Network...")
        
        pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', MLPClassifier(
                hidden_layer_sizes=(128, 64, 32),
                activation='relu',
                solver='adam',
                alpha=0.001,
                batch_size=32,
                learning_rate='adaptive',
                max_iter=500,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            ))
        ])
        
        pipeline.fit(X_train, y_train)
        self.models['neural_network'] = pipeline
        logger.info("Neural Network trained successfully")
        
        return pipeline
    
    def evaluate_model(self, model, X_test, y_test, model_name: str):
        """Evaluate model performance"""
        logger.info(f"Evaluating {model_name}...")
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # ROC-AUC (one-vs-rest for multiclass)
        try:
            roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='weighted')
        except:
            roc_auc = 0.0
        
        results = {
            'model_name': model_name,
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'roc_auc': float(roc_auc),
            'classification_report': classification_report(
                y_test, y_pred, 
                target_names=self.label_encoder.classes_,
                output_dict=True
            ),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        self.results[model_name] = results
        
        logger.info(f"{model_name} Results:")
        logger.info(f"  Accuracy: {accuracy:.4f}")
        logger.info(f"  Precision: {precision:.4f}")
        logger.info(f"  Recall: {recall:.4f}")
        logger.info(f"  F1 Score: {f1:.4f}")
        logger.info(f"  ROC-AUC: {roc_auc:.4f}")
        
        return results
    
    def save_models(self, output_dir: str = "saved_models"):
        """Save all trained models"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for model_name, model in self.models.items():
            model_path = os.path.join(output_dir, f"{model_name}_{timestamp}.pkl")
            joblib.dump(model, model_path)
            logger.info(f"Saved {model_name} to {model_path}")
            
            # Also save as "latest" version
            latest_path = os.path.join(output_dir, f"{model_name}_latest.pkl")
            joblib.dump(model, latest_path)
            logger.info(f"Saved {model_name} as latest version")
        
        # Save label encoder
        label_encoder_path = os.path.join(output_dir, "label_encoder.pkl")
        joblib.dump(self.label_encoder, label_encoder_path)
        logger.info(f"Saved label encoder to {label_encoder_path}")
    
    def save_results(self, output_dir: str = "saved_models"):
        """Save evaluation results"""
        os.makedirs(output_dir, exist_ok=True)
        
        results_path = os.path.join(output_dir, "training_results.json")
        
        # Add metadata
        results_with_metadata = {
            'timestamp': datetime.now().isoformat(),
            'models': self.results
        }
        
        with open(results_path, 'w') as f:
            json.dump(results_with_metadata, f, indent=2)
        
        logger.info(f"Saved results to {results_path}")
    
    def plot_confusion_matrices(self, X_test, y_test, output_dir: str = "saved_models"):
        """Plot confusion matrices for all models"""
        os.makedirs(output_dir, exist_ok=True)
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle('Confusion Matrices - Health Risk Classification', fontsize=16)
        
        for idx, (model_name, model) in enumerate(self.models.items()):
            y_pred = model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            
            sns.heatmap(
                cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=self.label_encoder.classes_,
                yticklabels=self.label_encoder.classes_,
                ax=axes[idx]
            )
            axes[idx].set_title(f'{model_name.replace("_", " ").title()}')
            axes[idx].set_ylabel('True Label')
            axes[idx].set_xlabel('Predicted Label')
        
        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'confusion_matrices.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved confusion matrices to {plot_path}")
        plt.close()
    
    def train_all_models(self):
        """Complete training pipeline"""
        # Load data
        df = self.load_data()
        
        # Prepare data
        X_train, X_test, y_train, y_test = self.prepare_data(df)
        
        # Train all models
        self.train_random_forest(X_train, y_train)
        self.train_xgboost(X_train, y_train)
        self.train_neural_network(X_train, y_train)
        
        # Evaluate all models
        for model_name, model in self.models.items():
            self.evaluate_model(model, X_test, y_test, model_name)
        
        # Save models and results
        self.save_models()
        self.save_results()
        self.plot_confusion_matrices(X_test, y_test)
        
        # Print summary
        print("\n" + "="*60)
        print("MODEL TRAINING COMPLETE - SUMMARY")
        print("="*60)
        for model_name, results in self.results.items():
            print(f"\n{model_name.upper()}:")
            print(f"  Accuracy:  {results['accuracy']:.4f}")
            print(f"  F1 Score:  {results['f1_score']:.4f}")
            print(f"  ROC-AUC:   {results['roc_auc']:.4f}")
        print("\n" + "="*60)
        
        # Find best model
        best_model = max(self.results.items(), key=lambda x: x[1]['f1_score'])
        print(f"\n🏆 Best Model: {best_model[0]} (F1: {best_model[1]['f1_score']:.4f})")
        print("="*60 + "\n")


def main():
    """Main training script"""
    trainer = HealthRiskModelTrainer()
    trainer.train_all_models()


if __name__ == "__main__":
    main()
