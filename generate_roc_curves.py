"""
Generate ROC Curves for Disease Prediction Models
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc, roc_auc_score
from itertools import cycle
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from backend.app.preprocessing.data_preprocessor import DataPreprocessor
from backend.app.feature_extraction.feature_extractor import FeatureExtractor
from backend.app.fusion.fusion_module import MultimodalFusion
from backend.app.models.disease_predictor import DiseasePredictor


def generate_test_data(n_samples=500):
    """Generate test data for ROC curve evaluation."""
    print("Generating test data...")
    
    disease_symptoms = {
        'common cold': [
            ['fever', 'cough', 'sore throat', 'runny nose'],
            ['cough', 'runny nose', 'sneezing', 'headache'],
            ['fever', 'sore throat', 'nasal congestion', 'fatigue'],
            ['cough', 'sore throat', 'runny nose', 'mild fever'],
            ['sneezing', 'runny nose', 'headache', 'fatigue']
        ],
        'influenza': [
            ['high fever', 'body ache', 'fatigue', 'cough', 'headache'],
            ['fever', 'severe fatigue', 'body pain', 'chills'],
            ['high fever', 'headache', 'muscle ache', 'cough', 'weakness'],
            ['fever', 'body ache', 'sore throat', 'fatigue', 'sweating'],
            ['chills', 'fever', 'body pain', 'dry cough', 'headache']
        ],
        'pneumonia': [
            ['cough', 'fever', 'chest pain', 'shortness of breath', 'fatigue'],
            ['high fever', 'productive cough', 'chest pain', 'difficulty breathing'],
            ['cough with phlegm', 'fever', 'chest tightness', 'rapid breathing'],
            ['shortness of breath', 'chest pain', 'fever', 'cough', 'sweating'],
            ['fever', 'breathing difficulty', 'chest pain', 'cough', 'weakness']
        ],
        'bronchitis': [
            ['persistent cough', 'chest discomfort', 'fatigue', 'shortness of breath'],
            ['cough', 'mucus production', 'chest tightness', 'mild fever'],
            ['chronic cough', 'wheezing', 'chest discomfort', 'fatigue'],
            ['cough with mucus', 'chest pain', 'shortness of breath'],
            ['persistent cough', 'fatigue', 'low fever', 'chest discomfort']
        ],
        'asthma': [
            ['shortness of breath', 'wheezing', 'chest tightness', 'cough'],
            ['difficulty breathing', 'chest tightness', 'cough at night'],
            ['wheezing', 'breathlessness', 'cough', 'chest pressure'],
            ['shortness of breath', 'cough', 'rapid breathing', 'chest tightness'],
            ['wheezing', 'difficulty breathing', 'chest tightness', 'fatigue']
        ],
        'migraine': [
            ['severe headache', 'nausea', 'sensitivity to light', 'dizziness'],
            ['throbbing headache', 'vomiting', 'sensitivity to sound', 'visual disturbances'],
            ['intense headache', 'nausea', 'dizziness', 'blurred vision'],
            ['severe headache', 'sensitivity to light', 'neck pain', 'nausea'],
            ['pulsating headache', 'vomiting', 'sensitivity to light and sound']
        ],
        'gastroenteritis': [
            ['nausea', 'vomiting', 'diarrhea', 'abdominal pain', 'fever'],
            ['diarrhea', 'abdominal cramps', 'vomiting', 'nausea'],
            ['stomach pain', 'diarrhea', 'nausea', 'fever', 'dehydration'],
            ['vomiting', 'diarrhea', 'abdominal cramping', 'fever', 'weakness'],
            ['nausea', 'diarrhea', 'stomach pain', 'loss of appetite', 'fever']
        ],
        'hypertension': [
            ['headache', 'dizziness', 'chest pain', 'shortness of breath'],
            ['severe headache', 'fatigue', 'blurred vision', 'chest discomfort'],
            ['dizziness', 'headache', 'nosebleed', 'fatigue'],
            ['chest pain', 'headache', 'difficulty breathing', 'dizziness'],
            ['severe headache', 'confusion', 'chest pain', 'vision problems']
        ],
        'diabetes': [
            ['increased thirst', 'frequent urination', 'fatigue', 'blurred vision'],
            ['excessive hunger', 'fatigue', 'frequent urination', 'weight loss'],
            ['increased thirst', 'blurred vision', 'slow healing wounds', 'fatigue'],
            ['frequent urination', 'extreme hunger', 'tiredness', 'blurred vision'],
            ['excessive thirst', 'frequent urination', 'numbness in hands', 'fatigue']
        ],
        'urinary tract infection': [
            ['burning during urination', 'frequent urination', 'lower abdominal pain'],
            ['pain during urination', 'cloudy urine', 'pelvic pain', 'frequent urination'],
            ['burning sensation while urinating', 'urgent need to urinate', 'pelvic discomfort'],
            ['frequent urination', 'pain in lower abdomen', 'burning urination', 'fever'],
            ['painful urination', 'strong urge to urinate', 'lower back pain', 'cloudy urine']
        ],
    }
    
    data = []
    diseases = list(disease_symptoms.keys())
    
    for _ in range(n_samples):
        disease = np.random.choice(diseases)
        pattern_idx = np.random.randint(0, len(disease_symptoms[disease]))
        symptom_pattern = disease_symptoms[disease][pattern_idx]
        
        num_symptoms_to_use = np.random.randint(
            max(2, len(symptom_pattern) - 1), 
            len(symptom_pattern) + 1
        )
        symptoms_selected = np.random.choice(
            symptom_pattern,
            size=min(num_symptoms_to_use, len(symptom_pattern)),
            replace=False
        ).tolist()
        
        if np.random.random() < 0.1:
            all_other_symptoms = []
            for d in diseases:
                if d != disease:
                    for pattern in disease_symptoms[d]:
                        all_other_symptoms.extend(pattern)
            
            if all_other_symptoms:
                noise_symptom = np.random.choice(all_other_symptoms, size=1)[0]
                symptoms_selected.append(noise_symptom)
        
        symptoms = ' '.join(symptoms_selected)
        age = np.random.randint(5, 85)
        gender = np.random.choice(['male', 'female'])
        height = np.random.normal(170, 10)
        weight = np.random.normal(70, 15)
        
        if disease in ['hypertension', 'diabetes']:
            systolic_bp = np.random.normal(140, 15)
            diastolic_bp = np.random.normal(90, 10)
        else:
            systolic_bp = np.random.normal(120, 10)
            diastolic_bp = np.random.normal(80, 8)
        
        if disease == 'diabetes':
            blood_sugar = np.random.normal(150, 30)
        else:
            blood_sugar = np.random.normal(100, 15)
        
        data.append({
            'symptoms': symptoms,
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'blood_sugar': blood_sugar,
            'disease': disease
        })
    
    return pd.DataFrame(data)


def prepare_data_for_roc(df):
    """Prepare data with the same pipeline used in training."""
    print("Preparing features...")
    
    preprocessor = DataPreprocessor()
    feature_extractor = FeatureExtractor(max_features=100)
    
    # Load the trained TF-IDF vectorizer
    models_dir = 'backend/models_saved'
    feature_extractor.load(os.path.join(models_dir, 'tfidf_vectorizer.pkl'))
    
    # Preprocess symptoms
    preprocessed_symptoms = []
    for symptoms in df['symptoms']:
        processed = preprocessor.preprocess_symptoms(symptoms)
        # Join tokens back to string
        preprocessed_symptoms.append(' '.join(processed))
    
    # Extract TF-IDF features for all samples
    tfidf_features_list = []
    for symptom_text in preprocessed_symptoms:
        tfidf_feat = feature_extractor.extract_tfidf_features(symptom_text)
        tfidf_features_list.append(tfidf_feat)
    tfidf_features = np.array(tfidf_features_list)
    
    # Extract context features
    context_features_list = []
    for idx, row in df.iterrows():
        # Calculate BMI
        height_m = row['height'] / 100  # Convert cm to meters
        bmi = row['weight'] / (height_m ** 2)
        
        # Encode gender
        gender_encoded = 1 if row['gender'] == 'male' else 0
        
        patient_data = {
            'age': row['age'],
            'gender': gender_encoded,
            'bmi': bmi,
            'systolic_bp': row['systolic_bp'],
            'diastolic_bp': row['diastolic_bp'],
            'blood_sugar': row['blood_sugar']
        }
        context_feat = feature_extractor.extract_context_features(patient_data)
        context_features_list.append(context_feat)
    context_features = np.array(context_features_list)
    
    # Concatenate features manually (same as fusion module does)
    from sklearn.preprocessing import StandardScaler
    X = np.concatenate([tfidf_features, context_features], axis=1)
    
    # Normalize
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    y = df['disease'].values
    
    return X, y


def plot_multiclass_roc_curves(y_test, y_score, classes, model_name, filename):
    """Plot ROC curves for multiclass classification."""
    # Binarize the output
    y_test_bin = label_binarize(y_test, classes=classes)
    n_classes = len(classes)
    
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test_bin.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    
    # Compute macro-average ROC curve and ROC area
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
    mean_tpr /= n_classes
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    
    # Plot all ROC curves
    plt.figure(figsize=(12, 10))
    
    # Plot micro-average ROC curve
    plt.plot(fpr["micro"], tpr["micro"],
             label=f'Micro-average ROC (AUC = {roc_auc["micro"]:.3f})',
             color='deeppink', linestyle=':', linewidth=3)
    
    # Plot macro-average ROC curve
    plt.plot(fpr["macro"], tpr["macro"],
             label=f'Macro-average ROC (AUC = {roc_auc["macro"]:.3f})',
             color='navy', linestyle=':', linewidth=3)
    
    # Plot ROC curve for each class
    colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'green', 'red', 
                    'purple', 'brown', 'pink', 'gray', 'olive'])
    
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, linewidth=2,
                 label=f'{classes[i]} (AUC = {roc_auc[i]:.3f})')
    
    # Plot random classifier line
    plt.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Random Classifier (AUC = 0.500)')
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=14, fontweight='bold')
    plt.ylabel('True Positive Rate', fontsize=14, fontweight='bold')
    plt.title(f'ROC Curves - {model_name}', fontsize=16, fontweight='bold')
    plt.legend(loc="lower right", fontsize=9)
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ ROC curve saved: {filename}")
    plt.close()
    
    return roc_auc


def plot_combined_comparison(lr_auc, rf_auc, classes, filename):
    """Plot comparison of both models' performance."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Prepare data
    disease_names = [cls.replace('_', ' ').title() for cls in classes]
    lr_aucs = [lr_auc[i] for i in range(len(classes))]
    rf_aucs = [rf_auc[i] for i in range(len(classes))]
    
    x = np.arange(len(disease_names))
    width = 0.35
    
    # Bar chart comparison
    bars1 = ax1.bar(x - width/2, lr_aucs, width, label='Logistic Regression', 
                    color='#2196F3', alpha=0.8)
    bars2 = ax1.bar(x + width/2, rf_aucs, width, label='Random Forest', 
                    color='#4CAF50', alpha=0.8)
    
    ax1.set_xlabel('Disease', fontsize=12, fontweight='bold')
    ax1.set_ylabel('AUC Score', fontsize=12, fontweight='bold')
    ax1.set_title('Model Performance Comparison by Disease', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(disease_names, rotation=45, ha='right', fontsize=9)
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim([0, 1.1])
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=7)
    
    # Overall metrics comparison
    metrics = ['Micro-Avg AUC', 'Macro-Avg AUC']
    lr_overall = [lr_auc['micro'], lr_auc['macro']]
    rf_overall = [rf_auc['micro'], rf_auc['macro']]
    
    x2 = np.arange(len(metrics))
    bars3 = ax2.bar(x2 - width/2, lr_overall, width, label='Logistic Regression', 
                    color='#2196F3', alpha=0.8)
    bars4 = ax2.bar(x2 + width/2, rf_overall, width, label='Random Forest', 
                    color='#4CAF50', alpha=0.8)
    
    ax2.set_xlabel('Metric', fontsize=12, fontweight='bold')
    ax2.set_ylabel('AUC Score', fontsize=12, fontweight='bold')
    ax2.set_title('Overall Model Performance', fontsize=14, fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(metrics, fontsize=11)
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim([0, 1.1])
    
    # Add value labels
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Comparison chart saved: {filename}")
    plt.close()


def generate_roc_curves():
    """Main function to generate ROC curves."""
    print("\n" + "="*60)
    print("ROC Curve Generation for Disease Prediction Models")
    print("="*60 + "\n")
    
    # Generate test data
    df = generate_test_data(n_samples=500)
    print(f"Generated {len(df)} test samples\n")
    
    # Prepare features
    X, y = prepare_data_for_roc(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"Test set size: {len(X_test)}\n")
    
    # Load models
    print("Loading trained models...")
    predictor = DiseasePredictor()
    models_dir = 'backend/models_saved'
    
    predictor.load_logistic_regression(
        os.path.join(models_dir, 'logistic_regression_model.pkl')
    )
    predictor.load_random_forest(
        os.path.join(models_dir, 'random_forest_model.pkl')
    )
    
    classes = predictor.logistic_regression_model.classes_
    print(f"Number of classes: {len(classes)}")
    print(f"Classes: {', '.join(classes)}\n")
    
    # Generate predictions (probability scores)
    print("-"*60)
    print("Generating ROC curves for Logistic Regression...")
    print("-"*60)
    y_score_lr = predictor.predict_proba_logistic_regression(X_test)
    lr_auc = plot_multiclass_roc_curves(
        y_test, y_score_lr, classes, 
        'Logistic Regression Model',
        'ROC_CURVE_LOGISTIC_REGRESSION.png'
    )
    
    print("\n" + "-"*60)
    print("Generating ROC curves for Random Forest...")
    print("-"*60)
    y_score_rf = predictor.predict_proba_random_forest(X_test)
    rf_auc = plot_multiclass_roc_curves(
        y_test, y_score_rf, classes,
        'Random Forest Model',
        'ROC_CURVE_RANDOM_FOREST.png'
    )
    
    print("\n" + "-"*60)
    print("Generating comparison chart...")
    print("-"*60)
    plot_combined_comparison(
        lr_auc, rf_auc, classes,
        'ROC_CURVE_MODEL_COMPARISON.png'
    )
    
    # Print summary
    print("\n" + "="*60)
    print("ROC Curve Generation Complete!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. ROC_CURVE_LOGISTIC_REGRESSION.png")
    print("  2. ROC_CURVE_RANDOM_FOREST.png")
    print("  3. ROC_CURVE_MODEL_COMPARISON.png")
    print("\nSummary Statistics:")
    print(f"  Logistic Regression - Micro-avg AUC: {lr_auc['micro']:.4f}")
    print(f"  Logistic Regression - Macro-avg AUC: {lr_auc['macro']:.4f}")
    print(f"  Random Forest - Micro-avg AUC: {rf_auc['micro']:.4f}")
    print(f"  Random Forest - Macro-avg AUC: {rf_auc['macro']:.4f}")
    print("\n")


if __name__ == '__main__':
    generate_roc_curves()
