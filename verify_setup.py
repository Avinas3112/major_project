#!/usr/bin/env python3
"""
Setup Verification Script

Verifies that all project components are properly set up and ready to use.
"""

import os
import sys
import importlib.util

def check_python_version():
    """Check Python version compatibility."""
    print("\n[1] Checking Python Version...")
    version = sys.version_info
    required_version = (3, 7)
    
    if version >= required_version:
        print(f"    ✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"    ✗ Python 3.7+ required (found {version.major}.{version.minor})")
        return False


def check_project_structure():
    """Check if all required directories exist."""
    print("\n[2] Checking Project Structure...")
    
    required_dirs = [
        'backend/app',
        'backend/app/preprocessing',
        'backend/app/feature_extraction',
        'backend/app/fusion',
        'backend/app/models',
        'backend/app/explainability',
        'backend/app/severity',
        'backend/app/doctor_recommendation',
        'backend/app/database',
        'backend/training',
        'backend/models_saved',
        'backend/data',
        'frontend',
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"    ✓ {directory}/")
        else:
            print(f"    ✗ {directory}/ (missing)")
            all_exist = False
    
    return all_exist


def check_required_files():
    """Check if all required files exist."""
    print("\n[3] Checking Required Files...")
    
    required_files = [
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'API_DOCUMENTATION.md',
        'config.py',
        'test_integration.py',
        'backend/app/main.py',
        'backend/app/preprocessing/data_preprocessor.py',
        'backend/app/feature_extraction/feature_extractor.py',
        'backend/app/fusion/fusion_module.py',
        'backend/app/models/disease_predictor.py',
        'backend/app/explainability/explainer.py',
        'backend/app/severity/severity_assessor.py',
        'backend/app/doctor_recommendation/doctor_recommender.py',
        'backend/app/database/db_manager.py',
        'backend/training/train_models.py',
        'frontend/index.html',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"    ✓ {file_path}")
        else:
            print(f"    ✗ {file_path} (missing)")
            all_exist = False
    
    return all_exist


def check_dependencies():
    """Check if required Python packages are installed."""
    print("\n[4] Checking Python Dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'numpy',
        'pandas',
        'sklearn',
        'nltk',
        'shap',
        'matplotlib',
        'seaborn',
        'joblib',
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            # Special case for scikit-learn
            if package == 'sklearn':
                importlib.import_module('sklearn')
            else:
                importlib.import_module(package)
            print(f"    ✓ {package}")
        except ImportError:
            print(f"    ✗ {package} (not installed)")
            all_installed = False
    
    return all_installed


def check_nltk_data():
    """Check if NLTK data is downloaded."""
    print("\n[5] Checking NLTK Data...")
    
    try:
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        
        # Try to use the data
        word_tokenize("test")
        stopwords.words('english')
        WordNetLemmatizer().lemmatize("testing")
        
        print("    ✓ NLTK punkt")
        print("    ✓ NLTK stopwords")
        print("    ✓ NLTK wordnet")
        return True
    except LookupError as e:
        print(f"    ✗ NLTK data missing: {e}")
        print("    → Run: python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')\"")
        return False


def print_next_steps(checks):
    """Print next steps based on verification results."""
    print("\n" + "="*70)
    print("SETUP VERIFICATION SUMMARY")
    print("="*70)
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("\n✓ All checks passed! Your system is ready to use.\n")
        print("Next steps:")
        print("1. Train models:")
        print("   python backend/training/train_models.py\n")
        print("2. Start the API server:")
        print("   python backend/app/main.py\n")
        print("3. Open the frontend:")
        print("   Open frontend/index.html in your web browser\n")
        print("Documentation:")
        print("  - README.md - Complete project documentation")
        print("  - QUICKSTART.md - Quick start guide")
        print("  - API_DOCUMENTATION.md - API reference")
    else:
        print("\n✗ Some checks failed. Please fix the issues:\n")
        
        if not checks['Python Version']:
            print("• Install Python 3.7 or higher")
        
        if not checks['Project Structure']:
            print("• Ensure all directories are created")
        
        if not checks['Required Files']:
            print("• Ensure all required files are present")
        
        if not checks['Dependencies']:
            print("• Install requirements: pip install -r requirements.txt")
        
        if not checks['NLTK Data']:
            print("• Download NLTK data: python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')\"")


def run_verification():
    """Run all verification checks."""
    print("\n" + "█"*70)
    print("█  SETUP VERIFICATION SCRIPT")
    print("█  Context-Aware Disease Prediction System")
    print("█"*70)
    
    checks = {
        'Python Version': check_python_version(),
        'Project Structure': check_project_structure(),
        'Required Files': check_required_files(),
        'Dependencies': check_dependencies(),
        'NLTK Data': check_nltk_data(),
    }
    
    print_next_steps(checks)
    
    # Print summary
    print("\n" + "="*70)
    print("Check Status:")
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {check_name:<30} {status}")
    print("="*70 + "\n")
    
    return all(checks.values())


if __name__ == '__main__':
    success = run_verification()
    sys.exit(0 if success else 1)
