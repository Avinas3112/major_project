"""
Feature Extraction Module

This module handles:
- TF-IDF vectorization (uni-gram and bi-gram)
- Feature engineering for symptom text
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os


class FeatureExtractor:
    """
    Handles feature extraction from preprocessed data.
    
    Attributes:
        tfidf_vectorizer: TfidfVectorizer for symptom text
        feature_names: List of feature names
    """
    
    def __init__(self, max_features=100):
        """
        Initialize feature extractor.
        
        Args:
            max_features (int): Maximum number of TF-IDF features to keep
        """
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),  # Uni-gram and bi-gram
            min_df=1,
            max_df=0.95,
            lowercase=True
        )
        self.feature_names = None
        self.max_features = max_features
    
    def fit(self, symptom_texts):
        """
        Fit TF-IDF vectorizer on symptom texts.
        
        Args:
            symptom_texts (list): List of symptom text strings
            
        Returns:
            self: Returns self for chaining
        """
        self.tfidf_vectorizer.fit(symptom_texts)
        self.feature_names = self.tfidf_vectorizer.get_feature_names_out()
        return self
    
    def extract_tfidf_features(self, symptom_text):
        """
        Extract TF-IDF features from symptom text.
        
        Args:
            symptom_text (str): Preprocessed symptom text
            
        Returns:
            np.ndarray: TF-IDF feature vector (sparse to dense)
        """
        tfidf_vector = self.tfidf_vectorizer.transform([symptom_text])
        return tfidf_vector.toarray().flatten()
    
    def extract_context_features(self, numerical_features_dict):
        """
        Extract numerical context features.
        
        Args:
            numerical_features_dict (dict): Dictionary with age, bmi, bp, sugar, gender
            
        Returns:
            np.ndarray: Numerical context feature vector
        """
        context_features = np.array([
            numerical_features_dict['age'],
            numerical_features_dict['gender'],
            numerical_features_dict['bmi'],
            numerical_features_dict['systolic_bp'],
            numerical_features_dict['diastolic_bp'],
            numerical_features_dict['blood_sugar']
        ])
        
        return context_features
    
    def get_feature_importance_mapping(self):
        """
        Get mapping of feature indices to feature names.
        
        Returns:
            dict: Mapping of feature names to indices
        """
        if self.feature_names is None:
            return {}
        
        feature_map = {name: idx for idx, name in enumerate(self.feature_names)}
        return feature_map
    
    def save(self, filepath):
        """
        Save the fitted vectorizer to disk.
        
        Args:
            filepath (str): Path to save the vectorizer
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.tfidf_vectorizer, filepath)
    
    def load(self, filepath):
        """
        Load a saved vectorizer from disk.
        
        Args:
            filepath (str): Path to the saved vectorizer
            
        Returns:
            self: Returns self for chaining
        """
        self.tfidf_vectorizer = joblib.load(filepath)
        self.feature_names = self.tfidf_vectorizer.get_feature_names_out()
        return self
