"""
Generate Feature Importance Analysis Diagrams
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from backend.app.preprocessing.data_preprocessor import DataPreprocessor
from backend.app.feature_extraction.feature_extractor import FeatureExtractor
from backend.app.models.disease_predictor import DiseasePredictor


def generate_test_data(n_samples=500):
    """Generate test data for feature importance analysis."""
    print("Generating test data...")
    
    disease_symptoms = {
        'common cold': [
            ['fever', 'cough', 'sore throat', 'runny nose'],
            ['cough', 'runny nose', 'sneezing', 'headache'],
            ['fever', 'sore throat', 'nasal congestion', 'fatigue'],
        ],
        'influenza': [
            ['high fever', 'body ache', 'fatigue', 'cough', 'headache'],
            ['fever', 'severe fatigue', 'body pain', 'chills'],
            ['high fever', 'headache', 'muscle ache', 'cough', 'weakness'],
        ],
        'pneumonia': [
            ['cough', 'fever', 'chest pain', 'shortness of breath', 'fatigue'],
            ['high fever', 'productive cough', 'chest pain', 'difficulty breathing'],
        ],
        'bronchitis': [
            ['persistent cough', 'chest discomfort', 'fatigue', 'shortness of breath'],
            ['cough', 'mucus production', 'chest tightness', 'mild fever'],
        ],
        'asthma': [
            ['shortness of breath', 'wheezing', 'chest tightness', 'cough'],
            ['difficulty breathing', 'chest tightness', 'cough at night'],
        ],
        'migraine': [
            ['severe headache', 'nausea', 'sensitivity to light', 'dizziness'],
            ['throbbing headache', 'vomiting', 'sensitivity to sound', 'visual disturbances'],
        ],
        'gastroenteritis': [
            ['nausea', 'vomiting', 'diarrhea', 'abdominal pain', 'fever'],
            ['diarrhea', 'abdominal cramps', 'vomiting', 'nausea'],
        ],
        'hypertension': [
            ['headache', 'dizziness', 'chest pain', 'shortness of breath'],
            ['severe headache', 'fatigue', 'blurred vision', 'chest discomfort'],
        ],
        'diabetes': [
            ['increased thirst', 'frequent urination', 'fatigue', 'blurred vision'],
            ['excessive hunger', 'fatigue', 'frequent urination', 'weight loss'],
        ],
        'urinary tract infection': [
            ['burning during urination', 'frequent urination', 'lower abdominal pain'],
            ['pain during urination', 'cloudy urine', 'pelvic pain', 'frequent urination'],
        ],
    }
    
    data = []
    diseases = list(disease_symptoms.keys())
    
    for _ in range(n_samples):
        disease = np.random.choice(diseases)
        pattern_idx = np.random.randint(0, len(disease_symptoms[disease]))
        symptom_pattern = disease_symptoms[disease][pattern_idx]
        
        symptoms = ' '.join(symptom_pattern)
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


def prepare_features(df):
    """Prepare features using the same pipeline."""
    print("Preparing features...")
    
    preprocessor = DataPreprocessor()
    feature_extractor = FeatureExtractor(max_features=100)
    
    # Load the trained TF-IDF vectorizer
    models_dir = 'backend/models_saved'
    feature_extractor.load(os.path.join(models_dir, 'tfidf_vectorizer.pkl'))
    
    # Preprocess and extract TF-IDF features
    tfidf_features_list = []
    for symptoms in df['symptoms']:
        processed = preprocessor.preprocess_symptoms(symptoms)
        symptom_text = ' '.join(processed)
        tfidf_feat = feature_extractor.extract_tfidf_features(symptom_text)
        tfidf_features_list.append(tfidf_feat)
    tfidf_features = np.array(tfidf_features_list)
    
    # Extract context features
    context_features_list = []
    for idx, row in df.iterrows():
        height_m = row['height'] / 100
        bmi = row['weight'] / (height_m ** 2)
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
    
    # Concatenate features
    from sklearn.preprocessing import StandardScaler
    X = np.concatenate([tfidf_features, context_features], axis=1)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Get feature names
    tfidf_feature_names = feature_extractor.tfidf_vectorizer.get_feature_names_out().tolist()
    context_feature_names = ['age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp', 'blood_sugar']
    feature_names = tfidf_feature_names + context_feature_names
    
    y = df['disease'].values
    
    return X, y, feature_names


def plot_logistic_regression_importance(model, feature_names, top_n=20):
    """Plot feature importance for Logistic Regression."""
    # Get coefficients for each class
    coefs = model.lr_model.coef_
    classes = model.lr_model.classes_
    
    # Calculate mean absolute coefficient across all classes
    mean_abs_coef = np.mean(np.abs(coefs), axis=0)
    
    # Get top N features
    top_indices = np.argsort(mean_abs_coef)[-top_n:]
    top_features = [feature_names[i] for i in top_indices]
    top_importance = mean_abs_coef[top_indices]
    
    # Plot overall importance
    fig, axes = plt.subplots(2, 1, figsize=(14, 12))
    
    # Plot 1: Overall Feature Importance
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_features)))
    bars = axes[0].barh(range(len(top_features)), top_importance, color=colors)
    axes[0].set_yticks(range(len(top_features)))
    axes[0].set_yticklabels(top_features, fontsize=10)
    axes[0].set_xlabel('Mean Absolute Coefficient', fontsize=12, fontweight='bold')
    axes[0].set_title('Top 20 Most Important Features (Logistic Regression)', 
                     fontsize=14, fontweight='bold')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, top_importance)):
        axes[0].text(val, i, f' {val:.3f}', va='center', fontsize=9)
    
    # Plot 2: Heatmap of coefficients per class
    # Select top features for heatmap
    top_15_indices = np.argsort(mean_abs_coef)[-15:]
    heatmap_data = coefs[:, top_15_indices].T
    
    sns.heatmap(heatmap_data, 
                xticklabels=[cls.replace('_', ' ').title() for cls in classes],
                yticklabels=[feature_names[i] for i in top_15_indices],
                cmap='RdYlGn', center=0, annot=False, 
                cbar_kws={'label': 'Coefficient Value'},
                ax=axes[1])
    axes[1].set_title('Feature Coefficients by Disease Class (Top 15 Features)', 
                     fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Disease', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Feature', fontsize=12, fontweight='bold')
    plt.setp(axes[1].get_xticklabels(), rotation=45, ha='right', fontsize=9)
    plt.setp(axes[1].get_yticklabels(), fontsize=10)
    
    plt.tight_layout()
    plt.savefig('FEATURE_IMPORTANCE_LOGISTIC_REGRESSION.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Feature importance (Logistic Regression) saved: FEATURE_IMPORTANCE_LOGISTIC_REGRESSION.png")
    plt.close()


def plot_random_forest_importance(model, feature_names, top_n=20):
    """Plot feature importance for Random Forest."""
    # Get feature importances
    importances = model.rf_model.feature_importances_
    
    # Get top N features
    top_indices = np.argsort(importances)[-top_n:]
    top_features = [feature_names[i] for i in top_indices]
    top_importance = importances[top_indices]
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Plot 1: Bar chart
    colors = plt.cm.plasma(np.linspace(0.3, 0.9, len(top_features)))
    bars = axes[0].barh(range(len(top_features)), top_importance, color=colors)
    axes[0].set_yticks(range(len(top_features)))
    axes[0].set_yticklabels(top_features, fontsize=10)
    axes[0].set_xlabel('Feature Importance', fontsize=12, fontweight='bold')
    axes[0].set_title('Top 20 Most Important Features (Random Forest)', 
                     fontsize=14, fontweight='bold')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, top_importance)):
        axes[0].text(val, i, f' {val:.3f}', va='center', fontsize=9)
    
    # Plot 2: Pie chart of feature type distribution
    # Categorize features
    tfidf_importance = 0
    context_importance = 0
    context_features = ['age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp', 'blood_sugar']
    
    for i, feat_name in enumerate(feature_names):
        if feat_name in context_features:
            context_importance += importances[i]
        else:
            tfidf_importance += importances[i]
    
    # Pie chart
    sizes = [tfidf_importance, context_importance]
    labels = ['Symptom Features\n(TF-IDF)', 'Context Features\n(Demographics & Vitals)']
    colors_pie = ['#FF6B6B', '#4ECDC4']
    explode = (0.05, 0.05)
    
    wedges, texts, autotexts = axes[1].pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                                            autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(13)
    
    axes[1].set_title('Feature Type Importance Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('FEATURE_IMPORTANCE_RANDOM_FOREST.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Feature importance (Random Forest) saved: FEATURE_IMPORTANCE_RANDOM_FOREST.png")
    plt.close()


def plot_feature_comparison(lr_model, rf_model, feature_names, top_n=15):
    """Compare feature importance between models."""
    # Get importances from both models
    lr_importance = np.mean(np.abs(lr_model.lr_model.coef_), axis=0)
    rf_importance = rf_model.rf_model.feature_importances_
    
    # Normalize to 0-1 scale for comparison
    lr_importance_norm = (lr_importance - lr_importance.min()) / (lr_importance.max() - lr_importance.min())
    rf_importance_norm = (rf_importance - rf_importance.min()) / (rf_importance.max() - rf_importance.min())
    
    # Get top features from both models combined
    combined_importance = lr_importance_norm + rf_importance_norm
    top_indices = np.argsort(combined_importance)[-top_n:]
    
    top_features = [feature_names[i] for i in top_indices]
    lr_top = lr_importance_norm[top_indices]
    rf_top = rf_importance_norm[top_indices]
    
    # Create comparison plot
    fig, ax = plt.subplots(figsize=(14, 10))
    
    y_pos = np.arange(len(top_features))
    width = 0.35
    
    bars1 = ax.barh(y_pos - width/2, lr_top, width, label='Logistic Regression', 
                    color='#2196F3', alpha=0.8)
    bars2 = ax.barh(y_pos + width/2, rf_top, width, label='Random Forest', 
                    color='#4CAF50', alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_features, fontsize=10)
    ax.set_xlabel('Normalized Feature Importance', fontsize=12, fontweight='bold')
    ax.set_title('Feature Importance Comparison: Logistic Regression vs Random Forest', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            width_val = bar.get_width()
            ax.text(width_val, bar.get_y() + bar.get_height()/2., 
                   f'{width_val:.2f}', ha='left', va='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('FEATURE_IMPORTANCE_COMPARISON.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Feature importance comparison saved: FEATURE_IMPORTANCE_COMPARISON.png")
    plt.close()


def generate_feature_importance_analysis():
    """Main function to generate feature importance analysis."""
    print("\n" + "="*60)
    print("Feature Importance Analysis")
    print("="*60 + "\n")
    
    # Generate and prepare data
    df = generate_test_data(n_samples=1000)
    X, y, feature_names = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Number of features: {len(feature_names)}\n")
    
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
    
    print("Models loaded successfully\n")
    
    # Generate visualizations
    print("-"*60)
    print("Generating Logistic Regression feature importance...")
    print("-"*60)
    plot_logistic_regression_importance(
        predictor, 
        feature_names, 
        top_n=20
    )
    
    print("\n" + "-"*60)
    print("Generating Random Forest feature importance...")
    print("-"*60)
    plot_random_forest_importance(
        predictor, 
        feature_names, 
        top_n=20
    )
    
    print("\n" + "-"*60)
    print("Generating model comparison...")
    print("-"*60)
    plot_feature_comparison(
        predictor,
        predictor,
        feature_names,
        top_n=15
    )
    
    # Print summary
    print("\n" + "="*60)
    print("Feature Importance Analysis Complete!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. FEATURE_IMPORTANCE_LOGISTIC_REGRESSION.png")
    print("  2. FEATURE_IMPORTANCE_RANDOM_FOREST.png")
    print("  3. FEATURE_IMPORTANCE_COMPARISON.png")
    print("\n")


if __name__ == '__main__':
    generate_feature_importance_analysis()
