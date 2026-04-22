"""
Flask API Backend

Main Flask application with REST API endpoints for disease prediction,
explanation, and doctor recommendation.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import numpy as np
from datetime import datetime

# Import custom modules
from preprocessing.data_preprocessor import DataPreprocessor
from feature_extraction.feature_extractor import FeatureExtractor
from fusion.fusion_module import MultimodalFusion
from models.disease_predictor import DiseasePredictor
from explainability.explainer import ExplainabilityEngine
from severity.severity_assessor import SeverityAssessment
from doctor_recommendation.doctor_recommender import DoctorRecommendationEngine
from database.db_manager import DatabaseManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
preprocessor = DataPreprocessor()
feature_extractor = FeatureExtractor(max_features=100)
fusion = MultimodalFusion()
predictor = DiseasePredictor()
severity_assessor = SeverityAssessment()
doctor_recommender = DoctorRecommendationEngine()
db_manager = DatabaseManager('backend/data/healthcare_predictions.db')

# Global variables for models
models_loaded = False

def load_models():
    """Load trained models from disk."""
    global models_loaded
    
    try:
        # Get absolute path to models directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(current_dir, '..', 'models_saved')
        
        # Load preprocessor and feature extractor
        if os.path.exists(os.path.join(models_dir, 'tfidf_vectorizer.pkl')):
            feature_extractor.load(os.path.join(models_dir, 'tfidf_vectorizer.pkl'))
        
        # Load logistic regression model
        if os.path.exists(os.path.join(models_dir, 'logistic_regression_model.pkl')):
            predictor.load_logistic_regression(
                os.path.join(models_dir, 'logistic_regression_model.pkl')
            )
        
        # Load random forest model
        if os.path.exists(os.path.join(models_dir, 'random_forest_model.pkl')):
            predictor.load_random_forest(
                os.path.join(models_dir, 'random_forest_model.pkl')
            )
        
        models_loaded = True
        print("✓ Models loaded successfully")
        
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        print("  Run training script first: python backend/training/train_models.py")


def startup():
    """Run startup tasks."""
    load_models()

# Call startup at module load
startup()


@app.route('/favicon.ico')
def favicon():
    """Return empty response for favicon."""
    return '', 204


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'models_loaded': models_loaded,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/predict_disease', methods=['POST'])
def predict_disease():
    """
    Predict disease from patient data.
    
    Request JSON:
    {
        "symptoms": "fever, cough, body ache",
        "age": 35,
        "gender": "male",
        "height": 175,
        "weight": 75,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "blood_sugar": 100
    }
    
    Returns:
    {
        "success": true,
        "user_id": 1,
        "prediction_id": 1,
        "top_diseases": [
            {"disease": "common cold", "probability": 0.85},
            ...
        ],
        "severity": {...},
        "urgency": "Low"
    }
    """
    try:
        if not models_loaded:
            return jsonify({'error': 'Models not loaded. Please train models first.'}), 503
        
        # Parse request data
        data = request.get_json()
        symptoms = data.get('symptoms', '')
        age = float(data.get('age', 30))
        gender = data.get('gender', 'male')
        height = float(data.get('height', 170))
        weight = float(data.get('weight', 70))
        systolic_bp = float(data.get('systolic_bp', 120))
        diastolic_bp = float(data.get('diastolic_bp', 80))
        blood_sugar = float(data.get('blood_sugar', 100))
        
        # Preprocess patient data
        preprocessed = preprocessor.preprocess_patient_data(
            symptoms, age, gender, height, weight,
            systolic_bp, diastolic_bp, blood_sugar
        )
        
        # Extract features
        tfidf_features = feature_extractor.extract_tfidf_features(
            preprocessed['symptoms_text']
        )
        context_features = feature_extractor.extract_context_features(
            preprocessed['numerical_features']
        )
        
        # Fuse features
        fused_features = fusion.fuse_features(tfidf_features, context_features)
        
        # Predict using logistic regression
        top_predictions = predictor.get_top_k_predictions(fused_features, k=5, model='lr')
        
        # Extract primary disease info
        primary_disease, primary_prob = top_predictions[0]
        
        # Assess severity
        severity_result = severity_assessor.assess_severity(
            primary_disease, primary_prob, preprocessed['symptoms']
        )
        
        # Store user in database
        user_id = db_manager.add_user(age, gender, height, weight)
        
        # Store prediction
        prediction_data = {
            'symptoms': preprocessed['symptoms'],
            'top_diseases': top_predictions,
            'severity': severity_result,
            'features_summary': {
                'tfidf_features': int(len(tfidf_features)),
                'context_features': int(len(context_features))
            }
        }
        
        prediction_id = db_manager.add_prediction(
            user_id=user_id,
            symptoms=', '.join(preprocessed['symptoms']),
            systolic_bp=systolic_bp,
            diastolic_bp=diastolic_bp,
            blood_sugar=blood_sugar,
            predicted_disease=primary_disease,
            probability=primary_prob,
            severity_level=severity_result['severity_level'],
            urgency_level=severity_result['urgency'],
            prediction_json=json.dumps(prediction_data, default=str)
        )
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'prediction_id': prediction_id,
            'top_diseases': [
                {'disease': d, 'probability': float(p)} for d, p in top_predictions
            ],
            'severity': {
                'level': severity_result['severity_level'],
                'urgency': severity_result['urgency'],
                'reasoning': severity_result['reasoning'],
                'recommendation': severity_result['recommendation']
            },
            'message': 'Prediction successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/explain_prediction', methods=['POST'])
def explain_prediction():
    """
    Get explanation for a prediction.
    
    Request JSON:
    {
        "prediction_id": 1
    }
    
    Returns explanation with feature importance and SHAP values.
    """
    try:
        if not models_loaded:
            return jsonify({'error': 'Models not loaded'}), 503
        
        data = request.get_json()
        prediction_id = data.get('prediction_id')
        
        # Get prediction from database
        details = db_manager.get_prediction_details(prediction_id)
        
        if not details:
            return jsonify({'error': 'Prediction not found'}), 404
        
        # Prepare explanation
        prediction = details['prediction']
        explanation_obj = details['explanation']
        
        explanation_text = "Explanation not available"
        if explanation_obj:
            explanation_text = explanation_obj['explanation_text']
        
        return jsonify({
            'success': True,
            'prediction_id': prediction_id,
            'disease': prediction['predicted_disease'],
            'probability': prediction['probability'],
            'explanation': explanation_text,
            'top_features': json.loads(prediction['prediction_json']).get('features_summary', {})
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/recommend_doctor', methods=['POST'])
def recommend_doctor():
    """
    Get doctor recommendations for a prediction.
    
    Request JSON:
    {
        "prediction_id": 1
    }
    
    Returns recommended specialists.
    """
    try:
        data = request.get_json()
        prediction_id = data.get('prediction_id')
        
        # Get prediction from database
        details = db_manager.get_prediction_details(prediction_id)
        
        if not details:
            return jsonify({'error': 'Prediction not found'}), 404
        
        prediction = details['prediction']
        recommendations = details['recommendations']
        
        # Format recommendations
        formatted_recs = []
        for rec in recommendations:
            formatted_recs.append({
                'rank': rec['rank'],
                'specialist': rec['specialist_type'],
                'relevance_score': rec['relevance_score'],
                'details': json.loads(rec['recommendation_json']).get('details', {})
            })
        
        return jsonify({
            'success': True,
            'prediction_id': prediction_id,
            'disease': prediction['predicted_disease'],
            'urgency': prediction['urgency_level'],
            'recommendations': formatted_recs
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/user/<int:user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Get prediction history for a user."""
    try:
        history = db_manager.get_user_predictions(user_id)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'predictions_count': len(history),
            'predictions': [
                {
                    'prediction_id': p['prediction_id'],
                    'disease': p['predicted_disease'],
                    'probability': p['probability'],
                    'severity': p['severity_level'],
                    'date': p['created_at']
                }
                for p in history
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics."""
    try:
        stats = db_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'total_users': stats['total_users'],
            'total_predictions': stats['total_predictions'],
            'models_loaded': models_loaded,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('backend/models_saved', exist_ok=True)
    os.makedirs('backend/data', exist_ok=True)
    
    # Run Flask app
    print("🏥 Healthcare Disease Prediction System")
    print("Starting Flask API server...")
    print("Available endpoints:")
    print("  POST   /predict_disease      - Predict disease")
    print("  POST   /explain_prediction   - Get explanation")
    print("  POST   /recommend_doctor     - Get doctor recommendations")
    print("  GET    /user/<id>/history    - Get user history")
    print("  GET    /statistics           - Get system statistics")
    print("  GET    /health               - Health check")
    print("\nServer running at: http://localhost:5000")
    print("Press CTRL+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
