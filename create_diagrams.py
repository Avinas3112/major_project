"""
Generate Workflow and Architecture Diagrams for Disease Prediction System
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.lines as mlines

def create_workflow_diagram():
    """Create workflow diagram showing the complete process flow."""
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(5, 13.5, 'Disease Prediction System - Workflow Diagram', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Color scheme
    input_color = '#E3F2FD'
    process_color = '#FFF9C4'
    ml_color = '#F3E5F5'
    output_color = '#E8F5E9'
    
    # Step 1: User Input
    box1 = FancyBboxPatch((0.5, 11.5), 2, 1, boxstyle="round,pad=0.1", 
                          edgecolor='#1976D2', facecolor=input_color, linewidth=2)
    ax.add_patch(box1)
    ax.text(1.5, 12, 'User Input\n• Symptoms\n• Demographics\n• Vitals', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Arrow to preprocessing
    arrow1 = FancyArrowPatch((2.5, 12), (3.5, 12), 
                            arrowstyle='->', mutation_scale=30, linewidth=2, color='#424242')
    ax.add_patch(arrow1)
    
    # Step 2: Data Preprocessing
    box2 = FancyBboxPatch((3.5, 11), 3, 2, boxstyle="round,pad=0.1", 
                          edgecolor='#F57C00', facecolor=process_color, linewidth=2)
    ax.add_patch(box2)
    ax.text(5, 12.5, 'Data Preprocessing', ha='center', va='center', 
            fontsize=12, fontweight='bold')
    ax.text(5, 12, '• Tokenization\n• Stopword Removal\n• Lemmatization', 
            ha='center', va='center', fontsize=9)
    ax.text(5, 11.3, '• Symptom Normalization\n• Numerical Scaling', 
            ha='center', va='center', fontsize=9)
    
    # Arrow to feature extraction
    arrow2 = FancyArrowPatch((5, 11), (5, 10), 
                            arrowstyle='->', mutation_scale=30, linewidth=2, color='#424242')
    ax.add_patch(arrow2)
    
    # Step 3: Feature Extraction
    box3a = FancyBboxPatch((1, 8.5), 2.5, 1.3, boxstyle="round,pad=0.1", 
                           edgecolor='#F57C00', facecolor=process_color, linewidth=2)
    ax.add_patch(box3a)
    ax.text(2.25, 9.5, 'Text Features', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(2.25, 9, 'TF-IDF\nVectorization', ha='center', va='center', fontsize=9)
    
    box3b = FancyBboxPatch((6.5, 8.5), 2.5, 1.3, boxstyle="round,pad=0.1", 
                           edgecolor='#F57C00', facecolor=process_color, linewidth=2)
    ax.add_patch(box3b)
    ax.text(7.75, 9.5, 'Context Features', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(7.75, 9, 'Age, Gender, BMI\nVital Signs', ha='center', va='center', fontsize=9)
    
    # Arrows from preprocessing to features
    arrow3a = FancyArrowPatch((4, 11), (2.5, 9.8), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow3a)
    arrow3b = FancyArrowPatch((6, 11), (7.5, 9.8), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow3b)
    
    # Step 4: Multimodal Fusion
    box4 = FancyBboxPatch((3.5, 6.5), 3, 1.5, boxstyle="round,pad=0.1", 
                          edgecolor='#7B1FA2', facecolor=ml_color, linewidth=2)
    ax.add_patch(box4)
    ax.text(5, 7.6, 'Multimodal Fusion', ha='center', va='center', 
            fontsize=12, fontweight='bold')
    ax.text(5, 7, 'Feature Concatenation\n& Normalization', 
            ha='center', va='center', fontsize=9)
    
    # Arrows to fusion
    arrow4a = FancyArrowPatch((2.25, 8.5), (4.5, 8), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow4a)
    arrow4b = FancyArrowPatch((7.75, 8.5), (5.5, 8), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow4b)
    
    # Step 5: ML Models
    box5a = FancyBboxPatch((1, 4.5), 2.2, 1.5, boxstyle="round,pad=0.1", 
                           edgecolor='#7B1FA2', facecolor=ml_color, linewidth=2)
    ax.add_patch(box5a)
    ax.text(2.1, 5.6, 'Logistic\nRegression', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(2.1, 5, '(Primary)', ha='center', va='center', fontsize=9, style='italic')
    
    box5b = FancyBboxPatch((6.8, 4.5), 2.2, 1.5, boxstyle="round,pad=0.1", 
                           edgecolor='#7B1FA2', facecolor=ml_color, linewidth=2)
    ax.add_patch(box5b)
    ax.text(7.9, 5.6, 'Random\nForest', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(7.9, 5, '(Secondary)', ha='center', va='center', fontsize=9, style='italic')
    
    # Arrows from fusion to models
    arrow5a = FancyArrowPatch((4, 6.5), (2.5, 6), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow5a)
    arrow5b = FancyArrowPatch((6, 6.5), (7.5, 6), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow5b)
    
    # Step 6: Disease Predictions
    box6 = FancyBboxPatch((3.5, 3), 3, 1.2, boxstyle="round,pad=0.1", 
                          edgecolor='#388E3C', facecolor=output_color, linewidth=2)
    ax.add_patch(box6)
    ax.text(5, 3.9, 'Disease Predictions', ha='center', va='center', 
            fontsize=12, fontweight='bold')
    ax.text(5, 3.4, 'Top-K Diseases\nwith Probabilities', 
            ha='center', va='center', fontsize=9)
    
    # Arrows from models to predictions
    arrow6a = FancyArrowPatch((2.1, 4.5), (4.5, 4.2), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow6a)
    arrow6b = FancyArrowPatch((7.9, 4.5), (5.5, 4.2), 
                             arrowstyle='->', mutation_scale=25, linewidth=2, color='#424242')
    ax.add_patch(arrow6b)
    
    # Parallel Processing Branches
    # Explainability
    box7a = FancyBboxPatch((0.2, 1), 2, 1.5, boxstyle="round,pad=0.1", 
                           edgecolor='#388E3C', facecolor=output_color, linewidth=2)
    ax.add_patch(box7a)
    ax.text(1.2, 2, 'Explainability', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(1.2, 1.5, 'SHAP Analysis\nFeature Importance\nExplanations', 
            ha='center', va='center', fontsize=8)
    
    # Severity Assessment
    box7b = FancyBboxPatch((3, 1), 2, 1.5, boxstyle="round,pad=0.1", 
                           edgecolor='#388E3C', facecolor=output_color, linewidth=2)
    ax.add_patch(box7b)
    ax.text(4, 2, 'Severity\nAssessment', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(4, 1.4, 'Risk Level\nUrgency Score', 
            ha='center', va='center', fontsize=8)
    
    # Doctor Recommendation
    box7c = FancyBboxPatch((5.8, 1), 2, 1.5, boxstyle="round,pad=0.1", 
                           edgecolor='#388E3C', facecolor=output_color, linewidth=2)
    ax.add_patch(box7c)
    ax.text(6.8, 2, 'Doctor\nRecommendation', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(6.8, 1.4, 'Specialist Matching\nPriority Ranking', 
            ha='center', va='center', fontsize=8)
    
    # Database Storage
    box7d = FancyBboxPatch((8.2, 1), 1.6, 1.5, boxstyle="round,pad=0.1", 
                           edgecolor='#388E3C', facecolor=output_color, linewidth=2)
    ax.add_patch(box7d)
    ax.text(9, 2, 'Database', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(9, 1.5, 'SQLite\nHistory\nStorage', 
            ha='center', va='center', fontsize=8)
    
    # Arrows from predictions to outputs
    arrow7a = FancyArrowPatch((4, 3), (1.5, 2.5), 
                             arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#424242')
    ax.add_patch(arrow7a)
    arrow7b = FancyArrowPatch((5, 3), (4, 2.5), 
                             arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#424242')
    ax.add_patch(arrow7b)
    arrow7c = FancyArrowPatch((6, 3), (6.8, 2.5), 
                             arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#424242')
    ax.add_patch(arrow7c)
    arrow7d = FancyArrowPatch((6.5, 3), (9, 2.5), 
                             arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#424242')
    ax.add_patch(arrow7d)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=input_color, edgecolor='#1976D2', label='Input', linewidth=2),
        mpatches.Patch(facecolor=process_color, edgecolor='#F57C00', label='Processing', linewidth=2),
        mpatches.Patch(facecolor=ml_color, edgecolor='#7B1FA2', label='ML Models', linewidth=2),
        mpatches.Patch(facecolor=output_color, edgecolor='#388E3C', label='Output', linewidth=2)
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('WORKFLOW_DIAGRAM.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Workflow diagram saved: WORKFLOW_DIAGRAM.png")
    plt.close()


def create_architecture_diagram():
    """Create system architecture diagram showing all components."""
    fig, ax = plt.subplots(figsize=(18, 14))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(9, 13.5, 'Disease Prediction System - Architecture Diagram', 
            ha='center', va='center', fontsize=22, fontweight='bold')
    
    # Color scheme
    frontend_color = '#E3F2FD'
    api_color = '#FFF9C4'
    core_color = '#F3E5F5'
    data_color = '#FFE0B2'
    db_color = '#E0F2F1'
    
    # ========== LAYER 1: Frontend ==========
    ax.text(9, 12.5, 'PRESENTATION LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', style='italic')
    
    frontend_box = FancyBboxPatch((2, 11), 14, 1.2, boxstyle="round,pad=0.1", 
                                  edgecolor='#1976D2', facecolor=frontend_color, linewidth=3)
    ax.add_patch(frontend_box)
    ax.text(9, 11.8, 'Web Frontend (HTML/CSS/JavaScript)', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(9, 11.3, 'Responsive UI • Form Input • Results Display • Real-time API Communication', 
            ha='center', va='center', fontsize=9)
    
    # Arrow from frontend to API
    arrow_f2a = FancyArrowPatch((9, 11), (9, 10.3), 
                               arrowstyle='<->', mutation_scale=40, linewidth=3, color='#D32F2F')
    ax.add_patch(arrow_f2a)
    ax.text(9.5, 10.65, 'HTTP/REST', ha='left', va='center', fontsize=9, style='italic')
    
    # ========== LAYER 2: API Layer ==========
    ax.text(9, 10, 'API LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', style='italic')
    
    api_box = FancyBboxPatch((2, 8.5), 14, 1.3, boxstyle="round,pad=0.1", 
                             edgecolor='#F57C00', facecolor=api_color, linewidth=3)
    ax.add_patch(api_box)
    ax.text(9, 9.5, 'Flask REST API Server', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(5, 9, 'Endpoints:', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(5, 8.7, '/predict_disease\n/explain_prediction', 
            ha='center', va='center', fontsize=8)
    ax.text(9, 9, 'CORS Enabled', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(9, 8.7, 'JSON Responses\nError Handling', 
            ha='center', va='center', fontsize=8)
    ax.text(13, 9, 'More Endpoints:', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(13, 8.7, '/recommend_doctor\n/user/<id>/history', 
            ha='center', va='center', fontsize=8)
    
    # ========== LAYER 3: Core Processing Modules ==========
    ax.text(9, 7.8, 'CORE PROCESSING LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', style='italic')
    
    # Row 1: Preprocessing & Feature Extraction
    prep_box = FancyBboxPatch((0.5, 6.2), 3.5, 1.4, boxstyle="round,pad=0.1", 
                              edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(prep_box)
    ax.text(2.25, 7.2, 'Data Preprocessor', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(2.25, 6.7, 'NLTK Pipeline\nTokenization, Lemmatization\nSymptom Normalization', 
            ha='center', va='center', fontsize=8)
    
    feat_box = FancyBboxPatch((4.5, 6.2), 3.5, 1.4, boxstyle="round,pad=0.1", 
                              edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(feat_box)
    ax.text(6.25, 7.2, 'Feature Extractor', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(6.25, 6.7, 'TF-IDF Vectorization\nContext Features\nNumerical Processing', 
            ha='center', va='center', fontsize=8)
    
    fusion_box = FancyBboxPatch((8.5, 6.2), 3.5, 1.4, boxstyle="round,pad=0.1", 
                                edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(fusion_box)
    ax.text(10.25, 7.2, 'Multimodal Fusion', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(10.25, 6.7, 'Feature Concatenation\nStandardization\nBatch Processing', 
            ha='center', va='center', fontsize=8)
    
    explainer_box = FancyBboxPatch((12.5, 6.2), 3.5, 1.4, boxstyle="round,pad=0.1", 
                                   edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(explainer_box)
    ax.text(14.25, 7.2, 'Explainability', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(14.25, 6.7, 'SHAP Analysis\nFeature Importance\nNatural Language', 
            ha='center', va='center', fontsize=8)
    
    # Row 2: ML Models
    ml_box1 = FancyBboxPatch((2, 4.2), 3.2, 1.5, boxstyle="round,pad=0.1", 
                             edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(ml_box1)
    ax.text(3.6, 5.3, 'Disease Predictor', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(3.6, 4.8, 'Logistic Regression (Primary)\nRandom Forest (Secondary)\nTop-K Predictions', 
            ha='center', va='center', fontsize=8)
    
    severity_box = FancyBboxPatch((5.7, 4.2), 3.2, 1.5, boxstyle="round,pad=0.1", 
                                  edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(severity_box)
    ax.text(7.3, 5.3, 'Severity Assessor', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(7.3, 4.8, 'Hybrid Assessment\nRule-based + ML\n4 Severity Levels', 
            ha='center', va='center', fontsize=8)
    
    doctor_box = FancyBboxPatch((9.4, 4.2), 3.5, 1.5, boxstyle="round,pad=0.1", 
                                edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(doctor_box)
    ax.text(11.15, 5.3, 'Doctor Recommender', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(11.15, 4.8, '40+ Disease Mappings\n17 Specialist Types\nPriority Ranking', 
            ha='center', va='center', fontsize=8)
    
    db_manager_box = FancyBboxPatch((13.3, 4.2), 3, 1.5, boxstyle="round,pad=0.1", 
                                    edgecolor='#7B1FA2', facecolor=core_color, linewidth=2)
    ax.add_patch(db_manager_box)
    ax.text(14.8, 5.3, 'DB Manager', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(14.8, 4.8, 'CRUD Operations\nHistory Tracking\nStatistics', 
            ha='center', va='center', fontsize=8)
    
    # ========== LAYER 4: Data & Model Storage ==========
    ax.text(9, 3.5, 'DATA & MODEL STORAGE LAYER', ha='center', va='center', 
            fontsize=14, fontweight='bold', style='italic')
    
    models_box = FancyBboxPatch((1.5, 1.8), 4, 1.4, boxstyle="round,pad=0.1", 
                                edgecolor='#EF6C00', facecolor=data_color, linewidth=2)
    ax.add_patch(models_box)
    ax.text(3.5, 2.8, 'Trained Models', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(3.5, 2.3, 'logistic_regression_model.pkl\nrandom_forest_model.pkl\ntfidf_vectorizer.pkl', 
            ha='center', va='center', fontsize=8)
    
    db_box = FancyBboxPatch((6, 1.8), 4, 1.4, boxstyle="round,pad=0.1", 
                            edgecolor='#00897B', facecolor=db_color, linewidth=2)
    ax.add_patch(db_box)
    ax.text(8, 2.8, 'SQLite Database', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(8, 2.3, 'users • predictions\ndoctor_recommendations\nexplanations', 
            ha='center', va='center', fontsize=8)
    
    training_box = FancyBboxPatch((10.5, 1.8), 4, 1.4, boxstyle="round,pad=0.1", 
                                  edgecolor='#EF6C00', facecolor=data_color, linewidth=2)
    ax.add_patch(training_box)
    ax.text(12.5, 2.8, 'Training Pipeline', ha='center', va='center', 
            fontsize=11, fontweight='bold')
    ax.text(12.5, 2.3, 'Synthetic Data Generation\nModel Training & Evaluation\nScikit-learn Pipeline', 
            ha='center', va='center', fontsize=8)
    
    # ========== External Dependencies ==========
    ax.text(9, 1.1, 'EXTERNAL LIBRARIES', ha='center', va='center', 
            fontsize=14, fontweight='bold', style='italic')
    
    libs_box = FancyBboxPatch((1, 0.1), 16, 0.8, boxstyle="round,pad=0.05", 
                              edgecolor='#455A64', facecolor='#ECEFF1', linewidth=2)
    ax.add_patch(libs_box)
    ax.text(9, 0.5, 'Flask • Scikit-learn • NLTK • SHAP • NumPy • Pandas • Joblib • SQLite3 • Matplotlib • Seaborn', 
            ha='center', va='center', fontsize=9)
    
    # ========== Connection Arrows ==========
    # API to Core modules (downward)
    ax.plot([9, 2.25], [8.5, 7.6], 'k-', linewidth=1.5, alpha=0.4)
    ax.plot([9, 6.25], [8.5, 7.6], 'k-', linewidth=1.5, alpha=0.4)
    ax.plot([9, 10.25], [8.5, 7.6], 'k-', linewidth=1.5, alpha=0.4)
    ax.plot([9, 14.25], [8.5, 7.6], 'k-', linewidth=1.5, alpha=0.4)
    
    # Core modules to ML layer
    ax.plot([2.25, 3.6], [6.2, 5.7], 'k-', linewidth=1.5, alpha=0.4)
    ax.plot([6.25, 3.6], [6.2, 5.7], 'k-', linewidth=1.5, alpha=0.4)
    ax.plot([10.25, 7.3], [6.2, 5.7], 'k-', linewidth=1.5, alpha=0.4)
    ax.plot([10.25, 11.15], [6.2, 5.7], 'k-', linewidth=1.5, alpha=0.4)
    
    # ML layer to storage
    ax.plot([3.6, 3.5], [4.2, 3.2], 'k-', linewidth=1.5, alpha=0.4)
    ax.plot([14.8, 8], [4.2, 3.2], 'k-', linewidth=1.5, alpha=0.4)
    
    # Data flow indicators
    ax.text(16.5, 12.2, '▼', ha='center', va='center', fontsize=20, color='#D32F2F')
    ax.text(16.5, 11.8, 'Data Flow', ha='center', va='center', fontsize=9, style='italic')
    
    plt.tight_layout()
    plt.savefig('ARCHITECTURE_DIAGRAM.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Architecture diagram saved: ARCHITECTURE_DIAGRAM.png")
    plt.close()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Generating System Diagrams")
    print("="*60 + "\n")
    
    print("Creating workflow diagram...")
    create_workflow_diagram()
    
    print("\nCreating architecture diagram...")
    create_architecture_diagram()
    
    print("\n" + "="*60)
    print("Diagram Generation Complete!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. WORKFLOW_DIAGRAM.png - Complete process flow")
    print("  2. ARCHITECTURE_DIAGRAM.png - System architecture")
    print("\n")
