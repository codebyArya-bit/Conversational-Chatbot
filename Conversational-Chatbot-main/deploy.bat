@echo off
REM Deployment script for College IT Support Chatbot
REM This script helps set up and run the chatbot application

echo ========================================
echo College IT Support Chatbot Deployment
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✓ Python is installed

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo ✓ pip is available

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed successfully

REM Check for OpenAI API key
if "%OPENAI_API_KEY%"=="" (
    echo.
    echo WARNING: OPENAI_API_KEY environment variable is not set!
    echo Please set your OpenAI API key before running the application:
    echo.
    echo   set OPENAI_API_KEY=your_api_key_here
    echo.
    echo You can get an API key from: https://platform.openai.com/api-keys
    echo.
    pause
)

REM Check for CSV file
if not exist "ICT Cell Common problems - Hardware issues.csv" (
    echo.
    echo WARNING: FAQ data file not found!
    echo Please ensure 'ICT Cell Common problems - Hardware issues.csv' exists
    echo in the same directory as this script.
    echo.
    pause
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the chatbot:
echo   1. Set your OpenAI API key: set OPENAI_API_KEY=your_key_here
echo   2. Run: python run.py
echo   3. Open browser to: http://localhost:5000
echo.
echo Press any key to start the application now...
pause >nul

REM Start the application
echo.
echo Starting the chatbot application...
python run.py

echo.
echo Application stopped.
pause