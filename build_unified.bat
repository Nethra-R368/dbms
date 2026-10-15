@echo off
echo ==========================================
echo Building React Frontend for Production...
echo ==========================================
cd /d "%~dp0frontend"
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo Error: Frontend build failed!
    exit /b %ERRORLEVEL%
)

echo.
echo ==========================================
echo Packaging into backend/static for Unified Deployment...
echo ==========================================
xcopy /E /I /Y dist "..\backend\static"

echo.
echo [SUCCESS] Frontend successfully bundled into backend/static!
echo You can now deploy the 'backend' folder to Azure App Service.
