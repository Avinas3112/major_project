"""
Disease Prediction Models Module

This module contains:
- Logistic Regression (Primary model)
- Random Forest Classifier (Secondary model)
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


class DiseasePredictor:
    """
    Disease prediction using multiple classifiers.
    
    Attributes:
        lr_model: Logistic Regression classifier
        rf_model: Random Forest classifier
        disease_labels: List of disease class labels
    """
    
    def __init__(self):
        """Initialize disease prediction models."""
        self.lr_model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            multi_class='multinomial',
            solver='lbfgs'
        )
        
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        
        self.disease_labels = None
        self.lr_fitted = False
        self.rf_fitted = False
    
    def train_logistic_regression(self, X_train, y_train):
        """
        Train logistic regression model.
        
        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training labels
            
        Returns:
            self: Returns self for chaining
        """
        self.lr_model.fit(X_train, y_train)
        self.disease_labels = self.lr_model.classes_
        self.lr_fitted = True
        return self
    
    def train_random_forest(self, X_train, y_train):
        """
        Train random forest model.
        
        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training labels
            
        Returns:
            self: Returns self for chaining
        """
        self.rf_model.fit(X_train, y_train)
        self.disease_labels = self.rf_model.classes_
        self.rf_fitted = True
        return self
    
    def predict_logistic_regression(self, X):
        """
        Predict using logistic regression.
        
        Args:
            X (np.ndarray): Feature vector or batch
            
        Returns:
            np.ndarray: Predicted class labels
        """
        if not self.lr_fitted:
            raise ValueError("Logistic Regression model not trained yet")
        
        return self.lr_model.predict(X)
    
    def predict_random_forest(self, X):
        """
        Predict using random forest.
        
        Args:
            X (np.ndarray): Feature vector or batch
            
        Returns:
            np.ndarray: Predicted class labels
        """
        if not self.rf_fitted:
            raise ValueError("Random Forest model not trained yet")
        
        return self.rf_model.predict(X)
    
    def predict_proba_logistic_regression(self, X):
        """
        Get probability predictions from logistic regression.
        
        Args:
            X (np.ndarray): Feature vector or batch
            
        Returns:
            np.ndarray: Probability matrix
        """
        if not self.lr_fitted:
            raise ValueError("Logistic Regression model not trained yet")
        
        return self.lr_model.predict_proba(X)
    
    def predict_proba_random_forest(self, X):
        """
        Get probability predictions from random forest.
        
        Args:
            X (np.ndarray): Feature vector or batch
            
        Returns:
            np.ndarray: Probability matrix
        """
        if not self.rf_fitted:
            raise ValueError("Random Forest model not trained yet")
        
        return self.rf_model.predict_proba(X)
    
    def get_top_k_predictions(self, X, k=5, model='lr'):
        """
        Get top-K disease predictions with probabilities.
        
        Args:
            X (np.ndarray): Feature vector
            k (int): Number of top predictions to return
            model (str): 'lr' for logistic regression, 'rf' for random forest
            
        Returns:
            list: List of tuples (disease_name, probability)
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        if model == 'lr':
            proba = self.predict_proba_logistic_regression(X)[0]
        elif model == 'rf':
            proba = self.predict_proba_random_forest(X)[0]
        else:
            raise ValueError("Model must be 'lr' or 'rf'")
        
        # Get top-k indices
        top_k_indices = np.argsort(proba)[::-1][:k]
        
        predictions = []
        for idx in top_k_indices:
            disease = self.disease_labels[idx]
            probability = float(proba[idx])
            predictions.append((disease, probability))
        
        return predictions
    
    def get_feature_importance(self, model='rf'):
        """
        Get feature importance scores.
        
        Args:
            model (str): 'lr' for logistic regression, 'rf' for random forest
            
        Returns:
            np.ndarray: Feature importance scores
        """
        if model == 'rf':
            if not self.rf_fitted:
                raise ValueError("Random Forest model not trained yet")
            return self.rf_model.feature_importances_
        
        elif model == 'lr':
            if not self.lr_fitted:
                raise ValueError("Logistic Regression model not trained yet")
            # Get coefficient magnitudes for logistic regression
            return np.abs(self.lr_model.coef_[0])
        
        else:
            raise ValueError("Model must be 'lr' or 'rf'")
    
    def save_logistic_regression(self, filepath):
        """Save logistic regression model to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.lr_model, filepath)
    
    def save_random_forest(self, filepath):
        """Save random forest model to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.rf_model, filepath)
    
    def load_logistic_regression(self, filepath):
        """Load logistic regression model from disk."""
        self.lr_model = joblib.load(filepath)
        self.disease_labels = self.lr_model.classes_
        self.lr_fitted = True
        return self
    
    def load_random_forest(self, filepath):
        """Load random forest model from disk."""
        self.rf_model = joblib.load(filepath)
        self.disease_labels = self.rf_model.classes_
        self.rf_fitted = True
        return self
