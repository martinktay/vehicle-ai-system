@echo off
REM Vehicle AI System - Full Demo Startup
REM Starts the local serial proof path and leaves room for cloud/fleet storytelling.

echo ========================================
echo Vehicle AI System
echo Full Demo Startup
echo ========================================
echo.

if not exist "backend\app\main.py" (
    echo ERROR: Run this script from the project root.
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ERROR: Frontend folder not found.
    pause
    exit /b 1
)

echo This startup path is optimized for the final demo:
echo   1. Real ESP32 telemetry on the Serial Dashboard
echo   2. LCD correspondence with dashboard values
echo   3. Optional cloud/fleet storytelling afterward
echo.
echo Expected board port: COM6
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

start "Backend (ESP32 Serial)" cmd /k "cd /d backend && set INGESTION_MODE=serial && set SERIAL_PORT=COM6 && set SERIAL_BAUD_RATE=115200 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting for backend to initialize...
timeout /t 6 /nobreak >nul

start "Frontend (Dashboard)" cmd /k "cd /d frontend && pnpm dev"

echo.
echo ========================================
echo System started
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Primary proof:
echo   ESP32 -> local backend -> Serial Dashboard
echo.
echo Secondary story:
echo   Cloud Dashboard -> fleet monitoring vision
echo.
pause
