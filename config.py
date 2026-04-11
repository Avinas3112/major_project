"""
Project Configuration and Setup
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'healthcare_predictions.db')

# Models
MODELS_DIR = os.path.join(BASE_DIR, 'models_saved')

# API Configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
API_DEBUG = True

# Model Parameters
TFIDF_MAX_FEATURES = 100
TFIDF_NGRAM_RANGE = (1, 2)

# Severity Thresholds
SEVERITY_THRESHOLDS = {
    'low': 0.3,
    'medium': 0.6,
    'high': 0.8
}

# Feature Engineering
NUMERIC_FEATURES = ['age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp', 'blood_sugar']

print("Configuration loaded successfully")
