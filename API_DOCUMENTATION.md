"""
API Documentation

Complete API reference for the Disease Prediction System
"""

# =============================================================================
# API ENDPOINTS DOCUMENTATION
# =============================================================================

"""
BASE URL: http://localhost:5000

All endpoints return JSON responses.
"""

# =============================================================================
# 1. HEALTH CHECK ENDPOINT
# =============================================================================

"""
Endpoint: GET /health
Description: Check if the API server is running and models are loaded

Request:
  No request body required

Response (200 OK):
{
  "status": "ok",
  "models_loaded": true,
  "timestamp": "2025-12-22T10:30:45.123456"
}

Example CURL:
  curl http://localhost:5000/health
"""

# =============================================================================
# 2. DISEASE PREDICTION ENDPOINT
# =============================================================================

"""
Endpoint: POST /predict_disease
Description: Predict diseases based on patient data

Request Headers:
  Content-Type: application/json

Request Body:
{
  "symptoms": "string (required) - Free-text symptom description",
  "age": "number (required) - Patient age in years",
  "gender": "string (required) - 'male' or 'female'",
  "height": "number (required) - Height in centimeters",
  "weight": "number (required) - Weight in kilograms",
  "systolic_bp": "number (optional) - Systolic blood pressure in mmHg",
  "diastolic_bp": "number (optional) - Diastolic blood pressure in mmHg",
  "blood_sugar": "number (optional) - Blood sugar level in mg/dL"
}

Response (200 OK):
{
  "success": true,
  "user_id": 1,
  "prediction_id": 1,
  "top_diseases": [
    {
      "disease": "common cold",
      "probability": 0.85
    },
    {
      "disease": "influenza",
      "probability": 0.65
    }
  ],
  "severity": {
    "level": "LOW",
    "urgency": "Low",
    "reasoning": "Disease: common cold (confidence: 85.0%)",
    "recommendation": "Consider home care and monitor symptoms. Schedule routine doctor visit."
  },
  "message": "Prediction successful"
}

Response (400 Bad Request):
{
  "error": "Error message describing what went wrong"
}

Response (503 Service Unavailable):
{
  "error": "Models not loaded. Please train models first."
}

Example CURL:
  curl -X POST http://localhost:5000/predict_disease \\
    -H "Content-Type: application/json" \\
    -d '{
      "symptoms": "fever, cough, sore throat",
      "age": 30,
      "gender": "male",
      "height": 175,
      "weight": 75,
      "systolic_bp": 120,
      "diastolic_bp": 80,
      "blood_sugar": 100
    }'
"""

# =============================================================================
# 3. PREDICTION EXPLANATION ENDPOINT
# =============================================================================

"""
Endpoint: POST /explain_prediction
Description: Get detailed explanation for a specific prediction

Request Body:
{
  "prediction_id": "number (required) - ID of prediction to explain"
}

Response (200 OK):
{
  "success": true,
  "prediction_id": 1,
  "disease": "common cold",
  "probability": 0.85,
  "explanation": "Detailed explanation of which features contributed to prediction",
  "top_features": {
    "tfidf_features": 100,
    "context_features": 6
  }
}

Response (404 Not Found):
{
  "error": "Prediction not found"
}

Example CURL:
  curl -X POST http://localhost:5000/explain_prediction \\
    -H "Content-Type: application/json" \\
    -d '{"prediction_id": 1}'
"""

# =============================================================================
# 4. DOCTOR RECOMMENDATION ENDPOINT
# =============================================================================

"""
Endpoint: POST /recommend_doctor
Description: Get recommended doctors/specialists for a prediction

Request Body:
{
  "prediction_id": "number (required) - ID of prediction"
}

Response (200 OK):
{
  "success": true,
  "prediction_id": 1,
  "disease": "common cold",
  "urgency": "Low",
  "recommendations": [
    {
      "rank": 1,
      "specialist": "General Practitioner",
      "relevance_score": 1.5,
      "details": {
        "specialization": "General medical care",
        "experience_years": 8,
        "availability": "Very High"
      }
    },
    {
      "rank": 2,
      "specialist": "Internal Medicine",
      "relevance_score": 1.0,
      "details": {
        "specialization": "Internal diseases and systemic disorders",
        "experience_years": 10,
        "availability": "High"
      }
    }
  ]
}

Response (404 Not Found):
{
  "error": "Prediction not found"
}

Example CURL:
  curl -X POST http://localhost:5000/recommend_doctor \\
    -H "Content-Type: application/json" \\
    -d '{"prediction_id": 1}'
"""

# =============================================================================
# 5. USER PREDICTION HISTORY ENDPOINT
# =============================================================================

"""
Endpoint: GET /user/<user_id>/history
Description: Get prediction history for a specific user

Parameters:
  user_id (integer) - ID of the user in URL path

Response (200 OK):
{
  "success": true,
  "user_id": 1,
  "predictions_count": 5,
  "predictions": [
    {
      "prediction_id": 1,
      "disease": "common cold",
      "probability": 0.85,
      "severity": "LOW",
      "date": "2025-12-22T10:30:45"
    },
    {
      "prediction_id": 2,
      "disease": "influenza",
      "probability": 0.72,
      "severity": "MEDIUM",
      "date": "2025-12-21T14:22:30"
    }
  ]
}

Response (400 Bad Request):
{
  "error": "Error message"
}

Example CURL:
  curl http://localhost:5000/user/1/history
"""

# =============================================================================
# 6. SYSTEM STATISTICS ENDPOINT
# =============================================================================

"""
Endpoint: GET /statistics
Description: Get overall system statistics

Request:
  No parameters required

Response (200 OK):
{
  "success": true,
  "total_users": 42,
  "total_predictions": 128,
  "models_loaded": true,
  "timestamp": "2025-12-22T10:35:20.456789"
}

Example CURL:
  curl http://localhost:5000/statistics
"""

# =============================================================================
# SEVERITY LEVELS EXPLANATION
# =============================================================================

"""
Severity Levels:

1. LOW
   - Probability < 0.6
   - Mild to minor conditions
   - Recommendation: Home care, routine follow-up
   - Urgency: Low

2. MEDIUM
   - Probability 0.6 - 0.8
   - Moderate conditions
   - Recommendation: Urgent appointment within 1-2 days
   - Urgency: Medium

3. HIGH
   - Probability > 0.8
   - Serious conditions
   - Recommendation: Immediate medical consultation
   - Urgency: High

4. EMERGENCY
   - Life-threatening symptoms
   - Emergency keywords detected (chest pain, difficulty breathing, etc.)
   - Abnormal vital signs
   - Recommendation: Call emergency services immediately
   - Urgency: Immediate
"""

# =============================================================================
# DISEASE-SPECIALIST MAPPING
# =============================================================================

"""
Common Disease to Specialist Mappings:

Cardiovascular:
  - Heart attack → Cardiologist
  - Hypertension → Cardiologist
  - Stroke → Neurologist

Respiratory:
  - Pneumonia → Pulmonologist
  - Asthma → Pulmonologist
  - Bronchitis → Pulmonologist

Neurological:
  - Migraine → Neurologist
  - Meningitis → Neurologist

Gastrointestinal:
  - Gastroenteritis → Gastroenterologist
  - Pancreatitis → Gastroenterologist

Endocrine:
  - Diabetes → Endocrinologist
  - Thyroid Disease → Endocrinologist

Infectious:
  - UTI → Urologist
  - Sepsis → Infectious Disease Specialist

General:
  - Common Cold → General Practitioner
  - Influenza → General Practitioner
"""

# =============================================================================
# ERROR CODES
# =============================================================================

"""
HTTP Status Codes:

200 OK
  - Request successful, valid response returned

400 Bad Request
  - Invalid request data, missing required fields
  - Invalid data format

404 Not Found
  - Requested resource (e.g., prediction) not found

500 Internal Server Error
  - Server-side error occurred

503 Service Unavailable
  - Models not loaded, training required
"""

# =============================================================================
# AUTHENTICATION & SECURITY
# =============================================================================

"""
Current Implementation:
  - No authentication required (development mode)
  - CORS enabled for frontend access
  - All data stored in local SQLite database

For Production:
  - Implement JWT authentication
  - Add HTTPS/TLS encryption
  - Use secure database with access controls
  - Implement rate limiting
  - Add input validation and sanitization
  - Use environment variables for sensitive data
"""

# =============================================================================
# FEATURE DETAILS
# =============================================================================

"""
TF-IDF Features:
  - Unigram and bigram text features from symptoms
  - Max 100 features per model
  - Min document frequency: 1
  - Max document frequency: 95%

Numerical Context Features (6 features):
  1. Age (years)
  2. Gender (0/1 encoding)
  3. BMI (calculated from height/weight)
  4. Systolic Blood Pressure (mmHg)
  5. Diastolic Blood Pressure (mmHg)
  6. Blood Sugar (mg/dL)

Total Features: ~106 (100 TF-IDF + 6 context)
"""

# =============================================================================
# EXAMPLE WORKFLOWS
# =============================================================================

"""
Workflow 1: Complete Prediction
  1. POST /predict_disease → Get prediction_id
  2. POST /explain_prediction → Get explanation
  3. POST /recommend_doctor → Get doctor recommendations

Workflow 2: User Follow-up
  1. GET /user/{user_id}/history → See previous predictions
  2. POST /explain_prediction → Review past explanation
  3. POST /recommend_doctor → Get current recommendations

Workflow 3: System Monitoring
  1. GET /health → Check server status
  2. GET /statistics → Monitor usage
"""

print("API Documentation loaded successfully")
