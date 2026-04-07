@echo off
REM Quick setup script for PB2 Natural Frequency Analysis
REM This script installs required Python packages

echo.
echo ============================================================
echo  PB2 Natural Frequency Analysis - Setup Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Installing required packages...
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing packages from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Setup completed successfully!
echo ============================================================
echo.
echo To run the program:
echo   1. Interactive Mode:
echo      python pb2_natural_frequency.py
echo.
echo   2. Run Examples:
echo      python examples.py
echo.
echo For more information, see README.md
echo.
pause
