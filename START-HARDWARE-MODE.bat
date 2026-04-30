@echo off
REM Climate-Smart Telemetry Platform - Hardware Mode Startup
REM This script starts the backend in serial mode for hardware integration

echo ========================================
echo Climate-Smart Telemetry Platform
echo Hardware Mode Startup
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "backend\app\main.py" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "backend\venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found
    echo Please run: cd backend ^&^& python -m venv venv ^&^& venv\Scripts\activate.bat ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo WARNING: backend\.env not found
    echo Creating from .env.example...
    copy backend\.env.example backend\.env
    echo.
    echo IMPORTANT: Please edit backend\.env and set:
    echo   INGESTION_MODE=serial
    echo   SERIAL_PORT=COM3  (change to your COM port)
    echo.
    echo Press any key to open .env file in Notepad...
    pause >nul
    notepad backend\.env
    echo.
    echo After saving, press any key to continue...
    pause >nul
)

echo Starting backend in serial mode...
echo.
echo Configuration:
type backend\.env
echo.
echo ========================================
echo.

REM Start backend
cd backend
call venv\Scripts\activate.bat
python -m app.main

REM If we get here, backend stopped
echo.
echo ========================================
echo Backend stopped
echo ========================================
pause
