@echo off
REM Vehicle AI System - Live ESP32 Hardware Demo
REM Recommended judging path:
REM ESP32 on COM6 -> local FastAPI serial backend -> local dashboard

echo ========================================
echo Vehicle AI System
echo Live Hardware Demo Mode
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

echo This mode is for the real ESP32 board and LCD demonstration.
echo.
echo Expected path:
echo   ESP32 on COM6
echo   ^> local backend in serial mode
echo   ^> local dashboard
echo.
echo Make sure:
echo   - the ESP32 is connected over USB
echo   - the firmware is already uploaded
echo   - no other app is using COM6
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Starting backend in serial mode on COM6...
start "Backend (ESP32 Serial)" cmd /k "cd /d backend && set INGESTION_MODE=serial && set SERIAL_PORT=COM6 && set SERIAL_BAUD_RATE=115200 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting for backend to initialize...
timeout /t 6 /nobreak >nul

echo Starting frontend...
start "Frontend (Dashboard)" cmd /k "cd /d frontend && pnpm dev"

echo.
echo ========================================
echo Demo services started
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo In the dashboard, confirm the source shows ESP32.
echo Then demonstrate the LCD and dashboard changing together.
echo.
pause
