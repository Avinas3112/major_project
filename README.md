# Context-Aware Multimodal Disease Prediction System

## Project Overview
A full-stack healthcare AI decision support system that predicts possible diseases and recommends appropriate medical specialists by analyzing multimodal patient data.

## Features
- Symptom text analysis with NLP preprocessing
- Multimodal context fusion (text + numerical patient data)
- Disease prediction using Logistic Regression & Random Forest
- Explainable AI using SHAP values
- Severity assessment with hybrid rule-based logic
- Intelligent doctor recommendation engine
- SQLite database for data persistence
- Clean, modular architecture

## Project Structure
```
disease_prediction_system/
├── backend/
│   ├── app/
│   │   ├── models/              # Trained ML models
│   │   ├── preprocessing/       # NLP & data preprocessing
│   │   ├── feature_extraction/  # TF-IDF & feature engineering
│   │   ├── fusion/              # Multimodal context fusion
│   │   ├── explainability/      # SHAP explanations
│   │   ├── severity/            # Severity assessment
│   │   ├── doctor_recommendation/ # Doctor recommendation
│   │   ├── database/            # Database operations
│   │   └── main.py              # Flask API server
│   ├── training/                # Model training scripts
│   └── models_saved/            # Saved .pkl models
├── frontend/                    # HTML/CSS/JS UI
├── data/                        # Training datasets
└── requirements.txt

## Installation

1. Clone or navigate to project directory
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download NLTK data:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

## Usage

### Training the Model
```bash
python backend/training/train_models.py
```

### Running the API Server
```bash
python backend/app/main.py
```

Server will run on: `http://localhost:5000`

### API Endpoints
- `POST /predict_disease` - Predict disease
- `POST /explain_prediction` - Get SHAP explanations
- `POST /recommend_doctor` - Get doctor recommendations

## Key Components

### 1. Data Preprocessing Module
- Lowercasing, tokenization, stopword removal
- Lemmatization and symptom normalization
- Missing value handling
- Gender encoding and feature scaling

### 2. Feature Extraction
- TF-IDF vectorization (uni-gram + bi-gram)
- Combines symptom text with patient context

### 3. Multimodal Fusion
- Feature-level fusion of text and numerical data
- Concatenates TF-IDF features with context features

### 4. Disease Prediction
- Primary: Multiclass Logistic Regression
- Secondary: Random Forest Classifier
- Outputs top-K diseases with probabilities

### 5. Explainability
- SHAP values for feature importance
- Human-readable explanations

### 6. Severity Assessment
- Probability thresholds
- Medical rule-based logic
- Emergency detection

### 7. Doctor Recommendation
- Maps disease to specialist
- Ranks by probability and severity
- Provides urgency level

## Database
SQLite database stores:
- User inputs
- Prediction results
- Doctor & specialization data

## Model Evaluation
- Accuracy, Precision, Recall, F1-score
- Cross-validation results
- Confusion matrices

## Author
Created for Final Year Major Project

## License
MIT License
