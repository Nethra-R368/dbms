@echo off
echo ========================================================
echo Starting SmartHostel Full Application (Backend + Frontend)
echo ========================================================
echo.
echo 1. Ensuring PostgreSQL 18 Service is running...
net start postgresql-x64-18 2>nul
echo.
echo 2. Launching Backend FastAPI Server (Port 8000)...
start "SmartHostel Backend" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd backend && python -m uvicorn app.main:app --reload --port 8000"
echo.
echo 3. Launching Frontend React App (Port 5173)...
start "SmartHostel Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"
echo.
echo ========================================================
echo Servers launched!
echo Backend API & Swagger: http://localhost:8000/docs
echo Frontend Web UI:       http://localhost:5173
echo ========================================================
