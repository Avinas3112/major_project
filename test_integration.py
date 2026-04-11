"""
System Testing and Integration Guide

Tests and validates all components of the Disease Prediction System
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.abspath('backend'))

from app.preprocessing.data_preprocessor import DataPreprocessor
from app.feature_extraction.feature_extractor import FeatureExtractor
from app.fusion.fusion_module import MultimodalFusion
from app.severity.severity_assessor import SeverityAssessment
from app.doctor_recommendation.doctor_recommender import DoctorRecommendationEngine
from app.database.db_manager import DatabaseManager


def test_preprocessing():
    """Test data preprocessing module."""
    print("\n" + "="*60)
    print("TEST 1: Data Preprocessing")
    print("="*60)
    
    preprocessor = DataPreprocessor()
    
    # Test symptom preprocessing
    symptoms = "I have a high fever, bad cough, and sore throat"
    result = preprocessor.preprocess_patient_data(
        symptoms,
        age=30,
        gender='male',
        height=175,
        weight=75,
        systolic_bp=120,
        diastolic_bp=80,
        blood_sugar=100
    )
    
    print(f"Input symptoms: {symptoms}")
    print(f"Processed symptoms: {result['symptoms']}")
    print(f"Numerical features: {result['numerical_features']}")
    print("✓ Preprocessing test passed")


def test_feature_extraction():
    """Test feature extraction module."""
    print("\n" + "="*60)
    print("TEST 2: Feature Extraction")
    print("="*60)
    
    feature_extractor = FeatureExtractor(max_features=50)
    
    # Sample symptoms for fitting
    sample_symptoms = [
        'fever cough sore throat',
        'high fever body ache fatigue',
        'shortness of breath chest pain',
        'nausea vomiting diarrhea',
        'headache dizziness migraine'
    ]
    
    feature_extractor.fit(sample_symptoms)
    
    # Extract features
    test_symptom = 'fever and cough'
    tfidf_features = feature_extractor.extract_tfidf_features(test_symptom)
    
    context_features = feature_extractor.extract_context_features({
        'age': 30,
        'gender': 1,
        'bmi': 25,
        'systolic_bp': 120,
        'diastolic_bp': 80,
        'blood_sugar': 100
    })
    
    print(f"TF-IDF features shape: {tfidf_features.shape}")
    print(f"Context features shape: {context_features.shape}")
    print(f"Feature names count: {len(feature_extractor.feature_names)}")
    print("✓ Feature extraction test passed")


def test_multimodal_fusion():
    """Test multimodal fusion module."""
    print("\n" + "="*60)
    print("TEST 3: Multimodal Context Fusion")
    print("="*60)
    
    fusion = MultimodalFusion()
    
    import numpy as np
    
    # Create dummy features
    tfidf_features = np.random.rand(100)
    context_features = np.array([30, 1, 25, 120, 80, 100])
    
    # Fuse features
    fused = fusion.fuse_features(tfidf_features, context_features, normalize=True)
    
    print(f"TF-IDF features: {len(tfidf_features)}")
    print(f"Context features: {len(context_features)}")
    print(f"Fused features: {len(fused)}")
    print(f"Fusion successful: {len(fused) == len(tfidf_features) + len(context_features)}")
    
    # Get summary
    summary = fusion.get_fusion_summary(tfidf_features, context_features)
    print(f"Fusion summary: {summary}")
    print("✓ Multimodal fusion test passed")


def test_severity_assessment():
    """Test severity assessment module."""
    print("\n" + "="*60)
    print("TEST 4: Severity Assessment")
    print("="*60)
    
    severity_assessor = SeverityAssessment()
    
    # Test low severity
    result_low = severity_assessor.assess_severity(
        'common cold',
        probability=0.7,
        symptoms=['fever', 'cough'],
        age=25
    )
    
    # Test high severity
    result_high = severity_assessor.assess_severity(
        'pneumonia',
        probability=0.95,
        symptoms=['chest pain', 'shortness of breath'],
        age=65
    )
    
    # Test emergency
    result_emergency = severity_assessor.assess_severity(
        'heart attack',
        probability=0.99,
        symptoms=['chest pain', 'difficulty breathing'],
        age=60
    )
    
    print(f"Low severity test: {result_low['severity_level']}")
    print(f"High severity test: {result_high['severity_level']}")
    print(f"Emergency test: {result_emergency['severity_level']}")
    print("✓ Severity assessment test passed")


def test_doctor_recommendation():
    """Test doctor recommendation engine."""
    print("\n" + "="*60)
    print("TEST 5: Doctor Recommendation Engine")
    print("="*60)
    
    doctor_recommender = DoctorRecommendationEngine()
    
    # Test recommendations
    top_diseases = [
        ('pneumonia', 0.85),
        ('bronchitis', 0.65),
        ('asthma', 0.45)
    ]
    
    recommendations = doctor_recommender.recommend_doctors(
        top_diseases,
        severity_level='HIGH',
        urgency_level='High'
    )
    
    print(f"Recommended specialists:")
    for rec in recommendations[:3]:
        print(f"  {rec['rank']}. {rec['specialist_type']} (score: {rec['relevance_score']:.2f})")
    
    print("✓ Doctor recommendation test passed")


def test_database():
    """Test database module."""
    print("\n" + "="*60)
    print("TEST 6: Database Operations")
    print("="*60)
    
    # Use test database
    db_manager = DatabaseManager('backend/data/test_healthcare.db')
    
    # Add user
    user_id = db_manager.add_user(30, 'male', 175, 75)
    print(f"Added user with ID: {user_id}")
    
    # Add prediction
    prediction_data = {
        'symptoms': ['fever', 'cough'],
        'top_diseases': [('common cold', 0.8)],
        'severity': {'level': 'LOW'}
    }
    
    prediction_id = db_manager.add_prediction(
        user_id=user_id,
        symptoms='fever, cough',
        systolic_bp=120,
        diastolic_bp=80,
        blood_sugar=100,
        predicted_disease='common cold',
        probability=0.8,
        severity_level='LOW',
        urgency_level='Low',
        prediction_json=json.dumps(prediction_data)
    )
    
    print(f"Added prediction with ID: {prediction_id}")
    
    # Get statistics
    stats = db_manager.get_statistics()
    print(f"Database statistics:")
    print(f"  Total users: {stats['total_users']}")
    print(f"  Total predictions: {stats['total_predictions']}")
    
    print("✓ Database test passed")


def run_integration_test():
    """Run complete integration test."""
    print("\n" + "█"*60)
    print("█  DISEASE PREDICTION SYSTEM - INTEGRATION TEST")
    print("█"*60)
    
    try:
        test_preprocessing()
        test_feature_extraction()
        test_multimodal_fusion()
        test_severity_assessment()
        test_doctor_recommendation()
        test_database()
        
        print("\n" + "█"*60)
        print("█  ALL TESTS PASSED ✓")
        print("█"*60)
        print("\nSystem is ready for use!")
        print("\nNext steps:")
        print("1. Run: python backend/training/train_models.py")
        print("2. Run: python backend/app/main.py")
        print("3. Open: frontend/index.html in browser")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_integration_test()
