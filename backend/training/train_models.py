"""
Model Training Script

Trains Logistic Regression and Random Forest models on healthcare data.
Includes data preparation, model training, evaluation, and model saving.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.preprocessing.data_preprocessor import DataPreprocessor
from app.feature_extraction.feature_extractor import FeatureExtractor
from app.fusion.fusion_module import MultimodalFusion
from app.models.disease_predictor import DiseasePredictor


class ModelTrainer:
    """Trains and evaluates disease prediction models."""
    
    def __init__(self):
        """Initialize trainer with preprocessing and model components."""
        self.preprocessor = DataPreprocessor()
        self.feature_extractor = FeatureExtractor(max_features=100)
        self.fusion = MultimodalFusion()
        self.predictor = DiseasePredictor()
        
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def generate_synthetic_data(self, n_samples=500):
        """
        Generate synthetic healthcare data for training.
        
        Args:
            n_samples (int): Number of samples to generate
            
        Returns:
            pd.DataFrame: Synthetic training data
        """
        print(f"Generating {n_samples} synthetic samples...")
        
        # Disease-symptom mapping with more diverse and realistic symptoms
        disease_symptoms = {
            'common cold': [
                ['fever', 'cough', 'sore throat', 'runny nose'],
                ['cough', 'runny nose', 'sneezing', 'headache'],
                ['fever', 'sore throat', 'nasal congestion', 'fatigue'],
                ['cough', 'sore throat', 'runny nose', 'mild fever'],
                ['sneezing', 'runny nose', 'headache', 'fatigue']
            ],
            'influenza': [
                ['high fever', 'body ache', 'fatigue', 'cough', 'headache'],
                ['fever', 'severe fatigue', 'body pain', 'chills'],
                ['high fever', 'headache', 'muscle ache', 'cough', 'weakness'],
                ['fever', 'body ache', 'sore throat', 'fatigue', 'sweating'],
                ['chills', 'fever', 'body pain', 'dry cough', 'headache']
            ],
            'pneumonia': [
                ['cough', 'fever', 'chest pain', 'shortness of breath', 'fatigue'],
                ['high fever', 'productive cough', 'chest pain', 'difficulty breathing'],
                ['cough with phlegm', 'fever', 'chest tightness', 'rapid breathing'],
                ['shortness of breath', 'chest pain', 'fever', 'cough', 'sweating'],
                ['fever', 'breathing difficulty', 'chest pain', 'cough', 'weakness']
            ],
            'bronchitis': [
                ['persistent cough', 'chest discomfort', 'fatigue', 'shortness of breath'],
                ['cough', 'mucus production', 'chest tightness', 'mild fever'],
                ['chronic cough', 'wheezing', 'chest discomfort', 'fatigue'],
                ['cough with mucus', 'chest pain', 'shortness of breath'],
                ['persistent cough', 'fatigue', 'low fever', 'chest discomfort']
            ],
            'asthma': [
                ['shortness of breath', 'wheezing', 'chest tightness', 'cough'],
                ['difficulty breathing', 'chest tightness', 'cough at night'],
                ['wheezing', 'breathlessness', 'cough', 'chest pressure'],
                ['shortness of breath', 'cough', 'rapid breathing', 'chest tightness'],
                ['wheezing', 'difficulty breathing', 'chest tightness', 'fatigue']
            ],
            'migraine': [
                ['severe headache', 'nausea', 'sensitivity to light', 'dizziness'],
                ['throbbing headache', 'vomiting', 'sensitivity to sound', 'visual disturbances'],
                ['intense headache', 'nausea', 'dizziness', 'blurred vision'],
                ['severe headache', 'sensitivity to light', 'neck pain', 'nausea'],
                ['pulsating headache', 'vomiting', 'sensitivity to light and sound']
            ],
            'gastroenteritis': [
                ['nausea', 'vomiting', 'diarrhea', 'abdominal pain', 'fever'],
                ['diarrhea', 'abdominal cramps', 'vomiting', 'nausea'],
                ['stomach pain', 'diarrhea', 'nausea', 'fever', 'dehydration'],
                ['vomiting', 'diarrhea', 'abdominal cramping', 'fever', 'weakness'],
                ['nausea', 'diarrhea', 'stomach pain', 'loss of appetite', 'fever']
            ],
            'hypertension': [
                ['headache', 'dizziness', 'chest pain', 'shortness of breath'],
                ['severe headache', 'fatigue', 'blurred vision', 'chest discomfort'],
                ['dizziness', 'headache', 'nosebleed', 'fatigue'],
                ['chest pain', 'headache', 'difficulty breathing', 'dizziness'],
                ['severe headache', 'confusion', 'chest pain', 'vision problems']
            ],
            'diabetes': [
                ['increased thirst', 'frequent urination', 'fatigue', 'blurred vision'],
                ['excessive hunger', 'fatigue', 'frequent urination', 'weight loss'],
                ['increased thirst', 'blurred vision', 'slow healing wounds', 'fatigue'],
                ['frequent urination', 'extreme hunger', 'tiredness', 'blurred vision'],
                ['excessive thirst', 'frequent urination', 'numbness in hands', 'fatigue']
            ],
            'urinary tract infection': [
                ['burning during urination', 'frequent urination', 'lower abdominal pain'],
                ['pain during urination', 'cloudy urine', 'pelvic pain', 'frequent urination'],
                ['burning sensation while urinating', 'urgent need to urinate', 'pelvic discomfort'],
                ['frequent urination', 'pain in lower abdomen', 'burning urination', 'fever'],
                ['painful urination', 'strong urge to urinate', 'lower back pain', 'cloudy urine']
            ],
        }
        
        data = []
        diseases = list(disease_symptoms.keys())
        
        for _ in range(n_samples):
            # Select disease
            disease = np.random.choice(diseases)
            
            # Get a random symptom pattern for this disease
            pattern_idx = np.random.randint(0, len(disease_symptoms[disease]))
            symptom_pattern = disease_symptoms[disease][pattern_idx]
            
            # Use most symptoms from the pattern (to create more variation)
            num_symptoms_to_use = np.random.randint(
                max(2, len(symptom_pattern) - 1), 
                len(symptom_pattern) + 1
            )
            symptoms_selected = np.random.choice(
                symptom_pattern,
                size=min(num_symptoms_to_use, len(symptom_pattern)),
                replace=False
            ).tolist()
            
            # Occasionally add noise (10% chance instead of 30%)
            if np.random.random() < 0.1:
                all_other_symptoms = []
                for d in diseases:
                    if d != disease:
                        for pattern in disease_symptoms[d]:
                            all_other_symptoms.extend(pattern)
                
                if all_other_symptoms:
                    noise_symptom = np.random.choice(all_other_symptoms, size=1)[0]
                    symptoms_selected.append(noise_symptom)
            
            symptoms = ' '.join(symptoms_selected)
            
            # Generate patient demographics
            age = np.random.randint(5, 85)
            gender = np.random.choice(['male', 'female'])
            height = np.random.normal(170, 10)  # cm
            weight = np.random.normal(70, 15)   # kg
            
            # Generate vitals (can be abnormal for certain diseases)
            if disease in ['hypertension', 'heart disease']:
                systolic_bp = np.random.normal(160, 10)
                diastolic_bp = np.random.normal(100, 8)
            else:
                systolic_bp = np.random.normal(120, 10)
                diastolic_bp = np.random.normal(80, 8)
            
            if disease in ['diabetes']:
                blood_sugar = np.random.normal(160, 30)
            else:
                blood_sugar = np.random.normal(100, 15)
            
            data.append({
                'symptoms': symptoms,
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'blood_sugar': blood_sugar,
                'disease': disease
            })
        
        return pd.DataFrame(data)
    
    def prepare_features(self, df):
        """
        Prepare features from dataframe.
        
        Args:
            df (pd.DataFrame): Input data with symptoms and patient info
            
        Returns:
            tuple: (X, y) - Features and labels
        """
        print("Preparing features...")
        
        # Extract symptoms text and fit TF-IDF
        symptom_texts = df['symptoms'].tolist()
        self.feature_extractor.fit(symptom_texts)
        
        # Extract features for all samples
        X_tfidf_list = []
        X_context_list = []
        
        for idx, row in df.iterrows():
            # TF-IDF features
            tfidf = self.feature_extractor.extract_tfidf_features(row['symptoms'])
            X_tfidf_list.append(tfidf)
            
            # Context features
            context_dict = {
                'age': row['age'],
                'gender': 1 if row['gender'].lower() == 'male' else 0,
                'bmi': row['weight'] / ((row['height'] / 100) ** 2),
                'systolic_bp': row['systolic_bp'],
                'diastolic_bp': row['diastolic_bp'],
                'blood_sugar': row['blood_sugar']
            }
            context = self.feature_extractor.extract_context_features(context_dict)
            X_context_list.append(context)
        
        X_tfidf = np.array(X_tfidf_list)
        X_context = np.array(X_context_list)
        
        # Fuse features
        X_fused = self.fusion.fuse_batch(X_tfidf, X_context, normalize=True)
        
        # Extract labels
        y = df['disease'].values
        
        print(f"Features shape: {X_fused.shape}")
        print(f"Number of samples: {len(df)}")
        print(f"Number of features: {X_fused.shape[1]}")
        
        return X_fused, y
    
    def train(self, df):
        """
        Train models on data.
        
        Args:
            df (pd.DataFrame): Input training data
        """
        print("\n" + "="*60)
        print("MODEL TRAINING")
        print("="*60)
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTraining set size: {len(self.X_train)}")
        print(f"Test set size: {len(self.X_test)}")
        
        # Train Logistic Regression
        print("\n" + "-"*60)
        print("Training Logistic Regression...")
        print("-"*60)
        self.predictor.train_logistic_regression(self.X_train, self.y_train)
        
        # Train Random Forest
        print("\nTraining Random Forest...")
        self.predictor.train_random_forest(self.X_train, self.y_train)
        
        print("✓ Models trained successfully")
    
    def evaluate(self):
        """Evaluate models on test set."""
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        # Logistic Regression
        print("\nLogistic Regression:")
        print("-"*60)
        y_pred_lr = self.predictor.predict_logistic_regression(self.X_test)
        self._print_metrics("Logistic Regression", self.y_test, y_pred_lr)
        
        # Random Forest
        print("\nRandom Forest:")
        print("-"*60)
        y_pred_rf = self.predictor.predict_random_forest(self.X_test)
        self._print_metrics("Random Forest", self.y_test, y_pred_rf)
    
    def _print_metrics(self, model_name, y_true, y_pred):
        """Print evaluation metrics."""
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
    
    def save_models(self, save_dir='backend/models_saved'):
        """Save trained models and preprocessors."""
        print("\n" + "="*60)
        print("SAVING MODELS")
        print("="*60)
        
        os.makedirs(save_dir, exist_ok=True)
        
        # Save models
        lr_path = os.path.join(save_dir, 'logistic_regression_model.pkl')
        rf_path = os.path.join(save_dir, 'random_forest_model.pkl')
        tfidf_path = os.path.join(save_dir, 'tfidf_vectorizer.pkl')
        
        self.predictor.save_logistic_regression(lr_path)
        print(f"✓ Logistic Regression saved to {lr_path}")
        
        self.predictor.save_random_forest(rf_path)
        print(f"✓ Random Forest saved to {rf_path}")
        
        self.feature_extractor.save(tfidf_path)
        print(f"✓ TF-IDF Vectorizer saved to {tfidf_path}")
    
    def run_full_pipeline(self, n_samples=500):
        """Run complete training pipeline."""
        print("\n")
        print("█"*60)
        print("█  DISEASE PREDICTION MODEL TRAINING PIPELINE")
        print("█"*60)
        
        # Generate data
        df = self.generate_synthetic_data(n_samples)
        
        # Train models
        self.train(df)
        
        # Evaluate
        self.evaluate()
        
        # Save models
        self.save_models()
        
        print("\n" + "█"*60)
        print("█  TRAINING COMPLETE")
        print("█"*60)
        print("\nYou can now run the Flask API:")
        print("  python backend/app/main.py")
        print("\n")


if __name__ == '__main__':
    trainer = ModelTrainer()
    trainer.run_full_pipeline(n_samples=10000)  # Increased from 1000 to 10000 for better predictions
