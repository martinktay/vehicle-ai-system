#!/usr/bin/env python3
"""
Test Script for Task 5.2: Backend API Mode

This script verifies:
1. Backend starts in simulator mode
2. Frontend connects to backend API
3. Mode indicator shows "Backend API"
4. Telemetry updates every 2 seconds

Test Procedure:
1. Start backend in simulator mode (port 8000)
2. Verify backend health endpoint
3. Verify backend returns telemetry data
4. Verify telemetry updates over time
5. Manual verification: Frontend shows "Backend API" mode
"""

import asyncio
import time
import requests
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api"

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{YELLOW}ℹ {text}{RESET}")


def test_backend_health():
    """Test 1: Verify backend health endpoint."""
    print_header("Test 1: Backend Health Check")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is healthy")
            print(f"  Status: {data.get('status')}")
            print(f"  Mode: {data.get('mode')}")
            print(f"  Telemetry Available: {data.get('telemetry_available')}")
            print(f"  Ingestion Connected: {data.get('ingestion_connected')}")
            
            # Verify mode is simulator
            if data.get('mode') == 'simulator':
                print_success("Backend is running in simulator mode")
                return True
            else:
                print_error(f"Expected simulator mode, got: {data.get('mode')}")
                return False
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Is it running on port 8000?")
        print_info("Start backend with: cd backend && python -m app.main")
        return False
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False


def test_latest_telemetry():
    """Test 2: Verify backend returns telemetry data."""
    print_header("Test 2: Latest Telemetry Endpoint")
    
    try:
        response = requests.get(f"{API_BASE}/latest", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Backend returned telemetry data")
            print(f"  Timestamp: {data.get('timestamp')}")
            print(f"  Engine Temp: {data.get('engine_temperature')}°C")
            print(f"  Fuel Mode: {data.get('current_fuel_mode')}")
            print(f"  System Status: {data.get('system_status')}")
            return True
        else:
            print_error(f"Latest telemetry failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Latest telemetry failed: {e}")
        return False


def test_telemetry_updates():
    """Test 3: Verify telemetry updates over time."""
    print_header("Test 3: Telemetry Update Rate")
    
    print_info("Fetching telemetry 3 times with 2-second intervals...")
    
    timestamps = []
    
    try:
        for i in range(3):
            response = requests.get(f"{API_BASE}/latest", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                timestamp = data.get('timestamp')
                timestamps.append(timestamp)
                print(f"  Sample {i+1}: {timestamp}")
                
                if i < 2:  # Don't sleep after last sample
                    time.sleep(2)
            else:
                print_error(f"Failed to fetch telemetry (attempt {i+1})")
                return False
        
        # Verify timestamps are different (data is updating)
        if len(set(timestamps)) == 3:
            print_success("Telemetry is updating (all timestamps unique)")
            return True
        else:
            print_error("Telemetry is not updating (duplicate timestamps)")
            print(f"  Timestamps: {timestamps}")
            return False
            
    except Exception as e:
        print_error(f"Telemetry update test failed: {e}")
        return False


def test_history_endpoint():
    """Test 4: Verify history endpoint."""
    print_header("Test 4: Telemetry History Endpoint")
    
    try:
        response = requests.get(f"{API_BASE}/history?limit=5", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend returned {len(data)} history records")
            
            if len(data) > 0:
                print(f"  Oldest: {data[0].get('timestamp')}")
                print(f"  Newest: {data[-1].get('timestamp')}")
                return True
            else:
                print_info("History is empty (backend may have just started)")
                return True
        else:
            print_error(f"History endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"History endpoint test failed: {e}")
        return False


def print_manual_verification_steps():
    """Print manual verification steps for frontend."""
    print_header("Manual Verification: Frontend Integration")
    
    print("To verify the frontend connects to the backend:")
    print()
    print("1. Open a new terminal and run:")
    print(f"   {YELLOW}cd frontend{RESET}")
    print(f"   {YELLOW}VITE_API_URL=http://localhost:8000/api pnpm run dev{RESET}")
    print()
    print("2. Open the frontend in your browser (usually http://localhost:5173)")
    print()
    print("3. Verify the following:")
    print(f"   {GREEN}✓{RESET} Mode indicator in header shows: {GREEN}Backend API{RESET}")
    print(f"   {GREEN}✓{RESET} Connection status shows: {GREEN}active{RESET}")
    print(f"   {GREEN}✓{RESET} Telemetry data updates every 2 seconds")
    print(f"   {GREEN}✓{RESET} Temperature values change over time")
    print(f"   {GREEN}✓{RESET} Chart shows live data")
    print()
    print("4. Check browser console for:")
    print(f"   {GREEN}✓{RESET} Message: '✓ Backend available - using API mode'")
    print(f"   {GREEN}✓{RESET} No error messages about failed fetches")
    print()


def main():
    """Run all tests."""
    print_header("Task 5.2: Backend API Mode Test")
    print(f"Testing backend at: {BACKEND_URL}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run automated tests
    results.append(("Backend Health", test_backend_health()))
    results.append(("Latest Telemetry", test_latest_telemetry()))
    results.append(("Telemetry Updates", test_telemetry_updates()))
    results.append(("History Endpoint", test_history_endpoint()))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name}: {status}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All automated tests passed!")
        print()
        print_manual_verification_steps()
        return 0
    else:
        print_error("Some tests failed. Please check the backend setup.")
        return 1


if __name__ == "__main__":
    exit(main())
