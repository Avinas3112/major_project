"""
Explainability Module using SHAP

Provides interpretable explanations for model predictions using:
- SHAP (SHapley Additive exPlanations) values
- Feature importance analysis
"""

import numpy as np
import shap
from sklearn.linear_model import LogisticRegression
import warnings

warnings.filterwarnings('ignore')


class ExplainabilityEngine:
    """
    Provides explainable AI for disease predictions.
    
    Uses SHAP values to explain which features contribute most to predictions.
    
    Attributes:
        explainer: SHAP explainer object
        base_model: Trained ML model for explanation
        feature_names: Names of input features
    """
    
    def __init__(self, model, X_background=None):
        """
        Initialize explainability engine.
        
        Args:
            model: Trained sklearn model (LogisticRegression or RandomForest)
            X_background (np.ndarray): Background data for SHAP (optional)
        """
        self.base_model = model
        self.explainer = None
        self.X_background = X_background
        self.feature_names = None
        
        # Initialize SHAP explainer
        if X_background is not None:
            try:
                self.explainer = shap.KernelExplainer(
                    model.predict_proba,
                    X_background
                )
            except Exception as e:
                print(f"Warning: Could not initialize SHAP KernelExplainer: {e}")
    
    def set_feature_names(self, feature_names):
        """
        Set feature names for better interpretability.
        
        Args:
            feature_names (list): List of feature names
            
        Returns:
            self: Returns self for chaining
        """
        self.feature_names = feature_names
        return self
    
    def explain_prediction(self, X, disease_index=None):
        """
        Explain a single prediction using SHAP.
        
        Args:
            X (np.ndarray): Feature vector for a single sample
            disease_index (int): Index of disease class (optional)
            
        Returns:
            dict: Explanation with SHAP values and feature contributions
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        explanation = {
            'prediction': self.base_model.predict(X)[0],
            'probabilities': self.base_model.predict_proba(X)[0],
            'feature_contributions': None,
            'top_features': None
        }
        
        # Try to compute SHAP values
        try:
            if self.explainer is not None:
                shap_values = self.explainer.shap_values(X)
                explanation['shap_values'] = shap_values
                explanation['feature_contributions'] = self._summarize_shap(
                    shap_values, X[0], disease_index
                )
        except Exception as e:
            print(f"Warning: Could not compute SHAP values: {e}")
        
        # Get feature importance from model coefficients
        explanation['top_features'] = self._get_top_contributing_features(X[0])
        
        return explanation
    
    def _summarize_shap(self, shap_values, X_sample, disease_index=None):
        """
        Summarize SHAP values into interpretable explanations.
        
        Args:
            shap_values: SHAP value output
            X_sample (np.ndarray): Single sample features
            disease_index (int): Disease class index
            
        Returns:
            dict: Summary of feature contributions
        """
        summary = {
            'contributing_features': [],
            'positive_features': [],
            'negative_features': []
        }
        
        # Handle SHAP values structure
        if isinstance(shap_values, list):
            # Multi-class output
            if disease_index is not None and disease_index < len(shap_values):
                sv = shap_values[disease_index]
            else:
                sv = shap_values[0]
        else:
            sv = shap_values
        
        if isinstance(sv, np.ndarray):
            # Get top contributing features
            importance = np.abs(sv).flatten()
            top_indices = np.argsort(importance)[::-1][:5]
            
            for idx in top_indices:
                if idx < len(sv):
                    feature_name = self.feature_names[idx] if self.feature_names else f"Feature_{idx}"
                    value = float(sv[idx])
                    summary['contributing_features'].append({
                        'feature': feature_name,
                        'shap_value': value,
                        'sample_value': float(X_sample[idx])
                    })
                    
                    if value > 0:
                        summary['positive_features'].append(feature_name)
                    else:
                        summary['negative_features'].append(feature_name)
        
        return summary
    
    def _get_top_contributing_features(self, X_sample, top_k=5):
        """
        Get top contributing features using model coefficients.
        
        Args:
            X_sample (np.ndarray): Feature vector
            top_k (int): Number of top features to return
            
        Returns:
            list: List of top contributing features with values
        """
        try:
            # For logistic regression
            if hasattr(self.base_model, 'coef_'):
                coef = np.abs(self.base_model.coef_[0])
                top_indices = np.argsort(coef)[::-1][:top_k]
                
                features = []
                for idx in top_indices:
                    feature_name = self.feature_names[idx] if self.feature_names else f"Feature_{idx}"
                    features.append({
                        'feature': feature_name,
                        'importance': float(coef[idx]),
                        'value': float(X_sample[idx])
                    })
                return features
            
            # For random forest
            elif hasattr(self.base_model, 'feature_importances_'):
                importances = self.base_model.feature_importances_
                top_indices = np.argsort(importances)[::-1][:top_k]
                
                features = []
                for idx in top_indices:
                    feature_name = self.feature_names[idx] if self.feature_names else f"Feature_{idx}"
                    features.append({
                        'feature': feature_name,
                        'importance': float(importances[idx]),
                        'value': float(X_sample[idx])
                    })
                return features
        
        except Exception as e:
            print(f"Warning: Could not extract feature importance: {e}")
        
        return []
    
    def generate_human_readable_explanation(self, top_diseases, explanation, symptoms):
        """
        Generate human-readable explanation text.
        
        Args:
            top_diseases (list): List of (disease, probability) tuples
            explanation (dict): Explanation from explain_prediction
            symptoms (list): List of symptom strings
            
        Returns:
            str: Human-readable explanation
        """
        text = []
        
        if top_diseases:
            main_disease, main_prob = top_diseases[0]
            text.append(f"Based on the provided symptoms ({', '.join(symptoms)}), "
                       f"the model predicts {main_disease} with {main_prob*100:.1f}% confidence.")
        
        if explanation.get('top_features'):
            text.append("\nKey contributing factors:")
            for i, feature in enumerate(explanation['top_features'][:3], 1):
                text.append(f"  {i}. {feature['feature']} (importance: {feature['importance']:.3f})")
        
        if len(top_diseases) > 1:
            text.append("\nOther possible conditions:")
            for disease, prob in top_diseases[1:4]:  # Top 3 alternatives
                text.append(f"  - {disease} ({prob*100:.1f}%)")
        
        return '\n'.join(text)
