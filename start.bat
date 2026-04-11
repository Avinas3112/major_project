@echo off
REM Start Script for Disease Prediction System (Windows)
REM Run this script to start the entire system

echo.
echo ================================
echo Disease Prediction System Startup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

echo [1] Verifying setup...
python verify_setup.py
if errorlevel 1 (
    echo.
    echo Setup verification failed. Please fix issues before continuing.
    pause
    exit /b 1
)

echo.
echo [2] Checking if models are trained...
if not exist "backend\models_saved\logistic_regression_model.pkl" (
    echo.
    echo Models not found. Training models now...
    echo This may take 1-2 minutes...
    echo.
    cd backend
    python training\train_models.py
    cd ..
    if errorlevel 1 (
        echo.
        echo Model training failed.
        pause
        exit /b 1
    )
) else (
    echo Models found. Skipping training.
)

echo.
echo [3] Starting Flask API server...
echo.
echo Server will run at: http://localhost:5000
echo Frontend at: frontend/index.html
echo.
echo Press CTRL+C to stop the server
echo.

cd backend
python app\main.py
