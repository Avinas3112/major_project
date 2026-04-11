"""
Multimodal Context Fusion Module

This module handles feature-level fusion of:
- Text features (TF-IDF from symptoms)
- Numerical context features (age, BMI, vitals, gender)
"""

import numpy as np
from sklearn.preprocessing import StandardScaler


class MultimodalFusion:
    """
    Fuses textual and numerical features at feature level.
    
    This module concatenates TF-IDF features with patient context features
    to create a unified multimodal representation.
    
    Attributes:
        scaler: StandardScaler for feature normalization
    """
    
    def __init__(self):
        """Initialize the fusion module."""
        self.scaler = StandardScaler()
        self.fitted = False
    
    def fuse_features(self, tfidf_features, context_features, normalize=True):
        """
        Fuse text and context features through concatenation.
        
        Args:
            tfidf_features (np.ndarray): TF-IDF feature vector from symptoms
            context_features (np.ndarray): Numerical context features (age, BMI, bp, etc.)
            normalize (bool): Whether to normalize the fused features
            
        Returns:
            np.ndarray: Concatenated and optionally normalized feature vector
        """
        # Ensure features are 1D
        if tfidf_features.ndim == 1:
            tfidf_features = tfidf_features.reshape(1, -1)
        if context_features.ndim == 1:
            context_features = context_features.reshape(1, -1)
        
        # Concatenate along feature axis
        fused = np.hstack([tfidf_features, context_features])
        
        # Normalize if requested
        if normalize:
            if self.fitted:
                fused = self.scaler.transform(fused)
            else:
                fused = self.scaler.fit_transform(fused)
                self.fitted = True
        
        return fused.flatten()
    
    def fuse_batch(self, tfidf_features_batch, context_features_batch, normalize=True):
        """
        Fuse features for a batch of samples.
        
        Args:
            tfidf_features_batch (np.ndarray): Batch of TF-IDF features (N, D_text)
            context_features_batch (np.ndarray): Batch of context features (N, D_context)
            normalize (bool): Whether to normalize the fused features
            
        Returns:
            np.ndarray: Fused feature matrix (N, D_text + D_context)
        """
        # Concatenate along feature axis
        fused = np.hstack([tfidf_features_batch, context_features_batch])
        
        # Normalize if requested
        if normalize:
            if self.fitted:
                fused = self.scaler.transform(fused)
            else:
                fused = self.scaler.fit_transform(fused)
                self.fitted = True
        
        return fused
    
    def get_fusion_summary(self, tfidf_features, context_features):
        """
        Get summary statistics of fused features.
        
        Args:
            tfidf_features (np.ndarray): TF-IDF features
            context_features (np.ndarray): Context features
            
        Returns:
            dict: Summary statistics
        """
        fused = self.fuse_features(tfidf_features, context_features, normalize=False)
        
        return {
            'tfidf_features_count': len(tfidf_features),
            'context_features_count': len(context_features),
            'total_features': len(fused),
            'tfidf_sum': np.sum(tfidf_features),
            'context_sum': np.sum(context_features),
            'fused_mean': np.mean(fused),
            'fused_std': np.std(fused)
        }
