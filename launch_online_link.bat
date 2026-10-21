@echo off
echo ========================================================
echo SmartHostel Public Online Deployment Launcher
echo ========================================================
echo.
echo 1. Ensuring PostgreSQL 18 Windows Service is running...
net start postgresql-x64-18 2>nul
echo.
echo 2. Ensuring Backend Server is running on port 8000...
start /b "" powershell -Command "if (-not (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue)) { & '.\venv\Scripts\python.exe' -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend }"
timeout /t 3 /nobreak >nul
echo.
echo 3. Launching Public HTTPS Tunnel via SSH...
echo.
echo ========================================================
echo  LIVE PUBLIC DEPLOYMENT LINK IS STARTING BELOW:
echo  (Open the generated HTTPS URL on any laptop or phone)
echo ========================================================
ssh -T -o StrictHostKeyChecking=no -R 80:127.0.0.1:8000 nokey@localhost.run
pause
