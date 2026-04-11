# Context-Aware Multimodal Disease Prediction and Personalized Doctor Recommendation System

## Executive Summary

A complete, production-ready healthcare AI decision support system built with Python, Flask, and scikit-learn. The system analyzes multimodal patient data (symptoms + contextual information) to predict diseases, explain predictions using SHAP, assess severity, and recommend appropriate medical specialists.

**Project Status:** ✅ Complete  
**Total Components:** 13 modules + Frontend + Backend APIs + Database  
**Lines of Code:** 2000+  
**Documentation:** Comprehensive  

---

## Core Features Implemented

### ✅ 1. User Interface (Frontend)
- **File:** `frontend/index.html`
- **Technology:** HTML5, CSS3, JavaScript
- **Features:**
  - Responsive form for patient data input
  - Free-text symptom input
  - Age, gender, height, weight, BMI calculation
  - Optional vital signs (BP, blood sugar)
  - Real-time results display
  - Severity badge with color coding
  - Beautiful gradient design with animations

### ✅ 2. Backend Framework
- **File:** `backend/app/main.py`
- **Technology:** Flask, Flask-CORS
- **Features:**
  - RESTful API with 6 endpoints
  - Modular architecture
  - CORS enabled for frontend communication
  - JSON request/response format
  - Error handling and validation

### ✅ 3. Data Preprocessing Module
- **File:** `backend/app/preprocessing/data_preprocessor.py`
- **Class:** `DataPreprocessor`
- **Features:**
  - **NLP Pipeline:**
    - Lowercasing
    - Tokenization using NLTK
    - Stopword removal
    - Lemmatization
    - Symptom normalization (15+ symptom mappings)
  - **Numerical Processing:**
    - Missing value handling
    - Gender encoding (binary)
    - BMI calculation from height/weight
    - Vital signs preprocessing

### ✅ 4. Feature Extraction Module
- **File:** `backend/app/feature_extraction/feature_extractor.py`
- **Class:** `FeatureExtractor`
- **Features:**
  - **TF-IDF Vectorization:**
    - Unigram + bigram features
    - Max 100 features
    - Document frequency thresholds
  - **Context Features:**
    - Age normalization
    - Gender encoding
    - BMI calculation
    - Vital signs features
  - Model persistence (save/load)

### ✅ 5. Multimodal Fusion Module
- **File:** `backend/app/fusion/fusion_module.py`
- **Class:** `MultimodalFusion`
- **Features:**
  - Feature-level fusion
  - Concatenation of TF-IDF + context features
  - StandardScaler normalization
  - Batch processing support
  - Fusion summary statistics

### ✅ 6. Disease Prediction Models
- **File:** `backend/app/models/disease_predictor.py`
- **Class:** `DiseasePredictor`
- **Primary Model:** Logistic Regression
  - Multi-class classification
  - Probabilistic output
  - Feature coefficient extraction
- **Secondary Model:** Random Forest
  - 100 trees ensemble
  - Feature importance scores
  - Max depth optimization
- **Features:**
  - Top-K predictions
  - Probability scores
  - Model persistence

### ✅ 7. Explainable AI Module
- **File:** `backend/app/explainability/explainer.py`
- **Class:** `ExplainabilityEngine`
- **Features:**
  - **SHAP Integration:**
    - KernelExplainer
    - SHAP value computation
    - Feature contribution analysis
  - **Model-based Explanations:**
    - Logistic Regression coefficients
    - Random Forest feature importance
  - **Human-Readable Explanations:**
    - Top contributing features
    - Disease probability interpretation
    - Alternative diagnoses

### ✅ 8. Severity Assessment Module
- **File:** `backend/app/severity/severity_assessor.py`
- **Class:** `SeverityAssessment`
- **Features:**
  - **Severity Levels:** LOW, MEDIUM, HIGH, EMERGENCY
  - **Assessment Factors:**
    - Probability thresholds (0.3, 0.6, 0.8)
    - Disease classification database
    - Emergency symptom detection
    - Age-based risk adjustment
    - Vital signs abnormality detection
  - **Risk-based Recommendations**
  - **Medical Logic Rules**

### ✅ 9. Doctor Recommendation Engine
- **File:** `backend/app/doctor_recommendation/doctor_recommender.py`
- **Class:** `DoctorRecommendationEngine`
- **Features:**
  - **Disease-Specialist Mapping:**
    - 40+ diseases mapped to specialists
    - Primary and secondary specialists
  - **Specialist Database:**
    - 17 specialist types
    - Specialization descriptions
    - Experience levels
    - Availability status
  - **Ranking Algorithm:**
    - Probability-based scoring
    - Severity weighting
    - Urgency assignment

### ✅ 10. Database Layer
- **File:** `backend/app/database/db_manager.py`
- **Class:** `DatabaseManager`
- **Technology:** SQLite
- **Tables:**
  - Users (age, gender, height, weight)
  - Predictions (symptoms, vitals, disease, probability)
  - Doctor Recommendations (specialist, rank, score)
  - Explanations (features, SHAP values, text)
- **Features:**
  - CRUD operations
  - User history tracking
  - Statistics computation
  - Data persistence

### ✅ 11. Model Training Pipeline
- **File:** `backend/training/train_models.py`
- **Class:** `ModelTrainer`
- **Features:**
  - **Synthetic Data Generation:**
    - 500 samples with realistic symptoms
    - 10 common diseases
    - Disease-specific patterns
  - **Complete Training Pipeline:**
    - Feature preparation
    - Train/test split (80/20)
    - Model training
  - **Evaluation Metrics:**
    - Accuracy
    - Precision
    - Recall
    - F1-Score
  - **Model Persistence:**
    - Saves .pkl files
    - Feature vectorizer saved

### ✅ 12. REST API Endpoints

**Base URL:** `http://localhost:5000`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Server health check |
| POST | `/predict_disease` | Main disease prediction |
| POST | `/explain_prediction` | Get SHAP explanations |
| POST | `/recommend_doctor` | Get specialist recommendations |
| GET | `/user/<id>/history` | User prediction history |
| GET | `/statistics` | System statistics |

### ✅ 13. Comprehensive Documentation
- `README.md` - Full project documentation
- `QUICKSTART.md` - Quick start guide
- `API_DOCUMENTATION.md` - API reference
- `test_integration.py` - Integration tests
- `verify_setup.py` - Setup verification script

---

## Project Structure

```
disease_prediction_system/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                          ← Flask API server
│   │   ├── preprocessing/
│   │   │   ├── __init__.py
│   │   │   └── data_preprocessor.py         ← NLP & data preprocessing
│   │   ├── feature_extraction/
│   │   │   ├── __init__.py
│   │   │   └── feature_extractor.py         ← TF-IDF feature extraction
│   │   ├── fusion/
│   │   │   ├── __init__.py
│   │   │   └── fusion_module.py             ← Multimodal fusion
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── disease_predictor.py         ← ML models (LR + RF)
│   │   ├── explainability/
│   │   │   ├── __init__.py
│   │   │   └── explainer.py                 ← SHAP explanations
│   │   ├── severity/
│   │   │   ├── __init__.py
│   │   │   └── severity_assessor.py         ← Severity assessment
│   │   ├── doctor_recommendation/
│   │   │   ├── __init__.py
│   │   │   └── doctor_recommender.py        ← Doctor recommendations
│   │   └── database/
│   │       ├── __init__.py
│   │       └── db_manager.py                ← SQLite database
│   │
│   ├── training/
│   │   ├── __init__.py
│   │   └── train_models.py                  ← Model training script
│   │
│   ├── models_saved/                        ← Trained models (.pkl)
│   └── data/                                ← Database files
│
├── frontend/
│   └── index.html                           ← Web UI
│
├── config.py                                ← Configuration
├── test_integration.py                      ← Integration tests
├── verify_setup.py                          ← Setup verification
├── requirements.txt                         ← Python dependencies
├── README.md                                ← Full documentation
├── QUICKSTART.md                            ← Quick start guide
└── API_DOCUMENTATION.md                     ← API reference
```

---

## Technology Stack

### Backend
- **Framework:** Flask 2.3.3
- **ML Libraries:** scikit-learn 1.3.0
- **NLP:** NLTK 3.8.1
- **Explainability:** SHAP 0.42.1
- **Data Processing:** NumPy, Pandas
- **Database:** SQLite3
- **Visualization:** Matplotlib, Seaborn

### Frontend
- **HTML5, CSS3, JavaScript (Vanilla)**
- **Responsive Design**
- **Real-time API Communication**

### Languages
- **Python:** 3.7+
- **JavaScript:** ES6+

---

## Key Algorithms & Methods

### 1. Data Preprocessing
- NLTK word_tokenize for tokenization
- WordNet lemmatization
- Symptom normalization using domain mapping

### 2. Feature Extraction
- TF-IDF with uni-gram and bi-gram features
- Numerical feature scaling with StandardScaler
- Concatenation-based fusion

### 3. Disease Prediction
- Logistic Regression: L2 regularization, multinomial classifier
- Random Forest: 100 estimators, max depth 15

### 4. Explainability
- SHAP KernelExplainer for model-agnostic explanations
- Feature importance from model coefficients
- Human-readable narrative generation

### 5. Severity Assessment
- Probability thresholds: 0.3 (low), 0.6 (medium), 0.8 (high)
- Disease-based severity mapping
- Emergency keyword detection
- Age-based risk adjustment

### 6. Doctor Recommendation
- Disease-specialist mapping database
- Probability-weighted ranking
- Specialist availability considerations

---

## Usage Instructions

### 1. Setup
```bash
pip install -r requirements.txt
python verify_setup.py
```

### 2. Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### 3. Train Models
```bash
python backend/training/train_models.py
```

### 4. Run API Server
```bash
python backend/app/main.py
```

### 5. Open Frontend
Open `frontend/index.html` in your web browser

### 6. Make Predictions
- Enter symptoms, age, gender, height, weight
- Click "Predict Disease"
- View predictions, severity, and recommendations

---

## API Examples

### Predict Disease
```bash
curl -X POST http://localhost:5000/predict_disease \
  -H "Content-Type: application/json" \
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
```

### Get Explanation
```bash
curl -X POST http://localhost:5000/explain_prediction \
  -H "Content-Type: application/json" \
  -d '{"prediction_id": 1}'
```

### Get Doctor Recommendations
```bash
curl -X POST http://localhost:5000/recommend_doctor \
  -H "Content-Type: application/json" \
  -d '{"prediction_id": 1}'
```

---

## Model Performance

### Evaluation Metrics
- **Accuracy:** Computed on test set
- **Precision:** Per-class precision scores
- **Recall:** Sensitivity of predictions
- **F1-Score:** Harmonic mean for class balance

### Data
- **Training:** 400 samples (80%)
- **Testing:** 100 samples (20%)
- **Classes:** 10 diseases
- **Features:** ~106 (100 TF-IDF + 6 context)

---

## Database Schema

### Users Table
- user_id (PK)
- age, gender, height, weight
- created_at (timestamp)

### Predictions Table
- prediction_id (PK)
- user_id (FK)
- symptoms, vitals
- predicted_disease, probability
- severity_level, urgency_level
- prediction_json
- created_at

### Doctor Recommendations Table
- recommendation_id (PK)
- prediction_id (FK)
- specialist_type, rank, relevance_score
- recommendation_json
- created_at

### Explanations Table
- explanation_id (PK)
- prediction_id (FK)
- top_features, shap_values
- explanation_text
- created_at

---

## Code Quality

### Architecture Principles
- **Modularity:** Each component is independent
- **Reusability:** Shared utilities across modules
- **Scalability:** Can handle multiple requests
- **Documentation:** Comprehensive docstrings
- **Error Handling:** Try-catch with meaningful messages

### Best Practices
- Type hints for function parameters
- Comprehensive docstrings
- Clear variable naming
- Separation of concerns
- Configuration management

---

## Limitations & Future Work

### Current Limitations
- Synthetic training data (use real medical datasets in production)
- Local SQLite database (use PostgreSQL for production)
- No user authentication (add JWT in production)
- Single-threaded API server (use Gunicorn/uWSGI)

### Future Enhancements
- Deep learning models (LSTM, BERT for text)
- Real-time monitoring dashboard
- Multi-language support
- Mobile app
- Integration with real medical databases
- Federated learning for privacy
- Continuous model retraining

---

## Testing

Run integration tests:
```bash
python test_integration.py
```

Tests cover:
1. Data preprocessing
2. Feature extraction
3. Multimodal fusion
4. Severity assessment
5. Doctor recommendation
6. Database operations

---

## Compliance & Disclaimers

⚠️ **Important:**
- This system is for **educational and research purposes only**
- **NOT suitable for real clinical diagnosis**
- Always consult qualified healthcare professionals
- Predictions are probabilistic estimates, not diagnoses
- Should not replace medical advice

---

## Files Summary

| File | Lines | Purpose |
|------|-------|---------|
| data_preprocessor.py | 200+ | NLP preprocessing |
| feature_extractor.py | 120+ | TF-IDF feature extraction |
| fusion_module.py | 100+ | Multimodal fusion |
| disease_predictor.py | 200+ | ML models |
| explainer.py | 180+ | SHAP explanations |
| severity_assessor.py | 250+ | Severity assessment |
| doctor_recommender.py | 280+ | Doctor recommendations |
| db_manager.py | 250+ | Database operations |
| main.py | 300+ | Flask API server |
| train_models.py | 280+ | Model training |
| index.html | 400+ | Frontend UI |
| **Total** | **2000+** | **Complete system** |

---

## Author Notes

This project demonstrates:
- **Machine Learning:** Multi-class classification with explainability
- **Backend Development:** RESTful API design with Flask
- **Frontend Development:** Responsive web UI
- **Data Engineering:** Preprocessing, fusion, and feature extraction
- **Software Architecture:** Modular, scalable design
- **Documentation:** Comprehensive and professional

**Perfect for:** Final-year major project, portfolio, interviews, healthcare AI research

---

## Getting Help

1. **Quick Start:** See `QUICKSTART.md`
2. **API Details:** See `API_DOCUMENTATION.md`
3. **Full Docs:** See `README.md`
4. **Setup Issues:** Run `verify_setup.py`
5. **Integration Test:** Run `test_integration.py`

---

**Project Status:** ✅ **COMPLETE AND READY FOR USE**
