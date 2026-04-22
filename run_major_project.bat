@echo off
echo ============================================================
echo Starting HealthPredict AI - Major Project Edition
echo ============================================================

echo Starting Backend API...
start cmd /k "python backend/app/main.py"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

echo Starting Modern React Frontend...
cd modern_frontend
start cmd /k "npm run dev"

echo.
echo ============================================================
echo Backend running on http://localhost:5000
echo Frontend will open in your default browser shortly...
echo ============================================================
pause
