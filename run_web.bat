@echo off
REM PB2 Natural Frequency Analysis - Web Application Launcher
REM This script starts the Flask web server

echo.
echo ============================================================
echo  PB2 Natural Frequency Analysis - Web Server
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo ============================================================
echo  Starting Web Server...
echo ============================================================
echo.
echo The web application will be available at:
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask app
python app.py

pause
