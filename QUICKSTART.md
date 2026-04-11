"""
Quick Start Guide

This document provides instructions to run the Disease Prediction System.
"""

# INSTALLATION

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Download NLTK data:
   ```
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

# TRAINING MODELS

Run the training script to train on synthetic healthcare data:

```bash
cd backend
python training/train_models.py
```

This will:
- Generate 500 synthetic training samples
- Train Logistic Regression model
- Train Random Forest model
- Evaluate both models
- Save models to backend/models_saved/

Expected output:
- logistic_regression_model.pkl
- random_forest_model.pkl
- tfidf_vectorizer.pkl

# RUNNING THE API SERVER

Start the Flask API server:

```bash
cd backend
python app/main.py
```

Server will run at: http://localhost:5000

Available endpoints:
- POST   /predict_disease      - Predict disease
- POST   /explain_prediction   - Get explanation
- POST   /recommend_doctor     - Get doctor recommendations
- GET    /user/<id>/history    - Get user history
- GET    /statistics           - Get system statistics
- GET    /health               - Health check

# USING THE FRONTEND

Open the web interface:

1. Navigate to: backend/frontend/index.html in your browser
   (Or open it from VS Code using "Open with Live Server")

2. Enter patient information:
   - Symptoms (required)
   - Age (required)
   - Gender (required)
   - Height & Weight (required)
   - Vitals (optional)

3. Click "Predict Disease" to get predictions

# TESTING WITH CURL

Example prediction request:

```bash
curl -X POST http://localhost:5000/predict_disease \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "fever cough sore throat",
    "age": 35,
    "gender": "male",
    "height": 175,
    "weight": 75,
    "systolic_bp": 120,
    "diastolic_bp": 80,
    "blood_sugar": 100
  }'
```

# PROJECT STRUCTURE

```
disease_prediction_system/
├── backend/
│   ├── app/                 # Main Flask application
│   │   ├── preprocessing/   # NLP & data preprocessing
│   │   ├── feature_extraction/  # TF-IDF features
│   │   ├── fusion/          # Multimodal fusion
│   │   ├── models/          # ML models
│   │   ├── explainability/  # SHAP explanations
│   │   ├── severity/        # Severity assessment
│   │   ├── doctor_recommendation/  # Doctor recommender
│   │   ├── database/        # SQLite database
│   │   └── main.py          # Flask server
│   ├── training/            # Model training scripts
│   ├── models_saved/        # Trained models (.pkl)
│   └── data/                # Database and data
├── frontend/                # HTML/CSS/JS UI
├── README.md                # Full documentation
├── requirements.txt         # Python dependencies
└── config.py                # Configuration file

# KEY FEATURES

1. **Multimodal Data Fusion**
   - Combines symptom text (TF-IDF) with patient context
   - Feature-level fusion for integrated representation

2. **Multiple Prediction Models**
   - Logistic Regression (interpretable)
   - Random Forest (powerful ensemble)
   - Top-K predictions with probabilities

3. **Explainability (SHAP)**
   - Feature importance analysis
   - SHAP values for decision explanation
   - Human-readable explanations

4. **Severity Assessment**
   - Probability-based severity scoring
   - Rule-based medical logic
   - Emergency detection

5. **Doctor Recommendation**
   - Disease-to-specialist mapping
   - Ranked recommendations by relevance
   - Urgency-based prioritization

6. **Database Persistence**
   - SQLite database for data storage
   - User history tracking
   - Prediction logging

# TROUBLESHOOTING

Q: "Models not loaded" error
A: Run the training script first: python backend/training/train_models.py

Q: CORS errors when using frontend
A: Flask-CORS is enabled. Make sure frontend is accessing http://localhost:5000

Q: Port 5000 already in use
A: Change port in backend/app/main.py or kill existing process

Q: NLTK data not found
A: Run: python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# NOTES

- The system uses synthetic data for training. For production, use real medical datasets
- All predictions are for educational purposes only
- Always consult qualified healthcare professionals for medical advice
- Model accuracy depends on training data quality

# CONTACT & SUPPORT

For issues or questions, refer to README.md or modify config.py for settings
