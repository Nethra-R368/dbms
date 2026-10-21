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
echo 3. Launching Public HTTPS Deployment Tunnel...
& "%LOCALAPPDATA%\npm-cache\_npx\672a10a4508cee26\node_modules\bore-cli\bin\bore.exe" -url http://127.0.0.1:8000 -inspect=false
pause
