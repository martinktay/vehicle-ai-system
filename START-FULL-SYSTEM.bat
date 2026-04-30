@echo off
REM Climate-Smart Telemetry Platform - Full System Startup
REM This script starts both backend (serial mode) and frontend

echo ========================================
echo Climate-Smart Telemetry Platform
echo Full System Startup
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "backend\app\main.py" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo This will start:
echo   1. Backend (serial mode) - reads from ESP32
echo   2. Frontend (dashboard) - displays telemetry
echo.
echo Make sure:
echo   - ESP32 is connected via USB
echo   - backend\.env is configured with correct COM port
echo   - Firmware is uploaded to ESP32
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM Start backend in new window
echo.
echo Starting backend...
start "Backend (Serial Mode)" cmd /k "cd backend && venv\Scripts\activate.bat && python -m app.main"

REM Wait for backend to start
echo Waiting for backend to start (5 seconds)...
timeout /t 5 /nobreak >nul

REM Start frontend in new window
echo.
echo Starting frontend...
start "Frontend (Dashboard)" cmd /k "cd frontend && pnpm dev"

echo.
echo ========================================
echo System started!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Two new windows opened:
echo   1. Backend (Serial Mode)
echo   2. Frontend (Dashboard)
echo.
echo Close those windows to stop the system.
echo.
echo Press any key to exit this window...
pause >nul
