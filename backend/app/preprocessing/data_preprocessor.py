"""
Data Preprocessing Module

This module handles:
- NLP preprocessing: lowercasing, tokenization, stopword removal, lemmatization
- Symptom normalization
- Numerical preprocessing: missing values, encoding, scaling
"""

import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    Handles all preprocessing tasks for patient data.
    
    Attributes:
        lemmatizer: NLTK WordNetLemmatizer instance
        stop_words: Set of English stopwords
        scaler: StandardScaler for numerical features
    """
    
    def __init__(self):
        """Initialize preprocessor with NLTK tools."""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.scaler = StandardScaler()
        
        # Symptom normalization dictionary
        self.symptom_mapping = {
            'fever': ['high fever', 'temperature', 'hot', 'burning'],
            'cough': ['dry cough', 'wet cough', 'persistent cough'],
            'headache': ['head pain', 'migraine', 'head ache'],
            'chest pain': ['chest ache', 'chest discomfort', 'heart pain'],
            'shortness of breath': ['breathlessness', 'difficulty breathing', 'dyspnea'],
            'nausea': ['feeling sick', 'sick feeling', 'queasiness'],
            'vomiting': ['throwing up', 'puking', 'vomit'],
            'diarrhea': ['loose motions', 'diarrhea', 'loose stool'],
            'fatigue': ['tiredness', 'weakness', 'exhaustion'],
            'body ache': ['muscle pain', 'body pain', 'joint pain'],
            'sore throat': ['throat pain', 'throat ache'],
            'runny nose': ['nasal discharge', 'nose running'],
            'rash': ['skin rash', 'red spots', 'skin irritation'],
            'dizziness': ['vertigo', 'lightheadedness', 'dizzy'],
            'abdominal pain': ['stomach pain', 'belly pain', 'stomach ache'],
        }
    
    def preprocess_symptoms(self, symptoms_text):
        """
        Preprocess symptom text through NLP pipeline.
        
        Args:
            symptoms_text (str): Raw symptom text from user
            
        Returns:
            list: Processed symptom tokens
        """
        # Lowercase
        text = symptoms_text.lower()
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Remove stopwords
        tokens = [t for t in tokens if t.isalpha() and t not in self.stop_words]
        
        # Lemmatization
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
        
        return tokens
    
    def normalize_symptoms(self, tokens):
        """
        Normalize symptom tokens using predefined mapping.
        
        Args:
            tokens (list): Preprocessed symptom tokens
            
        Returns:
            list: Normalized symptom tokens
        """
        normalized = []
        for token in tokens:
            found = False
            for canonical, variants in self.symptom_mapping.items():
                if token in [v.split() for v in variants] or token == canonical.split()[0]:
                    normalized.append(canonical)
                    found = True
                    break
            if not found:
                normalized.append(token)
        
        return list(set(normalized))  # Remove duplicates
    
    def preprocess_numerical_features(self, data_dict):
        """
        Preprocess numerical features (age, BMI, vitals).
        
        Args:
            data_dict (dict): Dictionary with keys: age, gender, height, weight, bp, sugar
            
        Returns:
            dict: Preprocessed numerical features
        """
        processed = {}
        
        # Age
        age = data_dict.get('age', 30)
        processed['age'] = float(age) if age else 30
        
        # Gender encoding (binary)
        gender = str(data_dict.get('gender', 'male')).lower()
        processed['gender'] = 1 if gender == 'male' else 0
        
        # BMI calculation
        height = float(data_dict.get('height', 170))  # cm
        weight = float(data_dict.get('weight', 70))   # kg
        
        if height > 0:
            height_m = height / 100
            processed['bmi'] = weight / (height_m ** 2)
        else:
            processed['bmi'] = 0
        
        # Vitals (optional)
        processed['systolic_bp'] = float(data_dict.get('systolic_bp', 120))
        processed['diastolic_bp'] = float(data_dict.get('diastolic_bp', 80))
        processed['blood_sugar'] = float(data_dict.get('blood_sugar', 100))
        
        return processed
    
    def handle_missing_values(self, df, strategy='mean'):
        """
        Handle missing values in dataframe.
        
        Args:
            df (pd.DataFrame): Input dataframe
            strategy (str): 'mean', 'median', or 'drop'
            
        Returns:
            pd.DataFrame: Dataframe with missing values handled
        """
        if strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
        elif strategy == 'drop':
            return df.dropna()
        else:
            return df
    
    def scale_features(self, X_train, X_test=None, fit=True):
        """
        Scale numerical features using StandardScaler.
        
        Args:
            X_train (np.ndarray): Training features
            X_test (np.ndarray): Testing features (optional)
            fit (bool): Whether to fit the scaler
            
        Returns:
            tuple: Scaled training and test features
        """
        if fit:
            X_train_scaled = self.scaler.fit_transform(X_train)
        else:
            X_train_scaled = self.scaler.transform(X_train)
        
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def preprocess_patient_data(self, symptoms_text, age, gender, height, weight, 
                               systolic_bp=None, diastolic_bp=None, blood_sugar=None):
        """
        Complete preprocessing pipeline for patient data.
        
        Args:
            symptoms_text (str): Raw symptom text
            age (float): Patient age
            gender (str): 'male' or 'female'
            height (float): Height in cm
            weight (float): Weight in kg
            systolic_bp (float): Systolic blood pressure
            diastolic_bp (float): Diastolic blood pressure
            blood_sugar (float): Blood sugar level
            
        Returns:
            dict: Preprocessed data with symptoms and numerical features
        """
        # Process symptoms
        tokens = self.preprocess_symptoms(symptoms_text)
        symptoms = self.normalize_symptoms(tokens)
        
        # Process numerical features
        numerical_data = {
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'systolic_bp': systolic_bp or 120,
            'diastolic_bp': diastolic_bp or 80,
            'blood_sugar': blood_sugar or 100
        }
        
        numerical_features = self.preprocess_numerical_features(numerical_data)
        
        return {
            'symptoms': symptoms,
            'symptoms_text': ' '.join(symptoms),
            'numerical_features': numerical_features
        }
