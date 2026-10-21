@echo off
echo Starting PostgreSQL 18 Windows Service...
net start postgresql-x64-18 2>nul
echo PostgreSQL 18 is active on port 5432 (Database: smarthostel).
echo Testing connection with password Nark@1231...
cd /d "%~dp0"
.\venv\Scripts\python.exe test_conn_again.py
pause
