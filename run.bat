@echo off
title Fortnite Discord Bot
cd /d "%~dp0"

echo ===================================================
echo             Fortnite Discord Bot
echo ===================================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo Setting up Python virtual environment...
    python -m venv venv
    echo Installing requirements...
    call venv\Scripts\pip install -r requirements.txt
)

echo Starting bot...
venv\Scripts\python.exe bot.py
pause
