@echo off
REM Climate-Smart Telemetry Platform - Demo Mode Startup
REM This script starts only the frontend with mock telemetry (no hardware needed)

echo ========================================
echo Climate-Smart Telemetry Platform
echo Demo Mode Startup (No Hardware)
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "frontend\package.json" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo WARNING: node_modules not found
    echo Installing dependencies...
    cd frontend
    call pnpm install
    cd ..
    echo.
)

echo Starting frontend in demo mode...
echo.
echo Features:
echo   - Mock telemetry (no hardware needed)
echo   - All NLNG award sections
echo   - Offline operation
echo   - Realistic sensor simulation
echo.
echo Dashboard will open at: http://localhost:5173
echo.
echo ========================================
echo.

REM Start frontend
cd frontend
call pnpm dev

REM If we get here, frontend stopped
echo.
echo ========================================
echo Frontend stopped
echo ========================================
pause
