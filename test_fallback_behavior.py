#!/usr/bin/env python3
"""
Test script for Task 5.3: Test fallback behavior

This script tests the frontend's resilience when the backend becomes unavailable.

Test Steps:
1. Start backend
2. Verify backend is running
3. Start frontend (manual step - will provide instructions)
4. Stop backend while frontend is running
5. Verify frontend shows disconnected state
6. Restart backend
7. Verify frontend reconnects automatically

Expected Behavior:
- Frontend should detect backend disconnection
- Frontend should show "disconnected" status
- Frontend should NOT crash or freeze
- Frontend should automatically reconnect when backend comes back
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
BACKEND_HEALTH_URL = f"{BACKEND_URL}/api/health"
BACKEND_DIR = Path(__file__).parent / "backend"
BACKEND_PROCESS = None

def print_step(step_num, message):
    """Print a test step with formatting"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {message}")
    print('='*60)

def check_backend_health():
    """Check if backend is responding"""
    try:
        response = requests.get(BACKEND_HEALTH_URL, timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_backend():
    """Start the backend server"""
    global BACKEND_PROCESS
    
    print("Starting backend server...")
    
    # Change to backend directory and start uvicorn
    BACKEND_PROCESS = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    for i in range(30):
        time.sleep(1)
        if check_backend_health():
            print(f"✓ Backend started successfully (took {i+1}s)")
            return True
    
    print("✗ Backend failed to start within 30 seconds")
    return False

def stop_backend():
    """Stop the backend server"""
    global BACKEND_PROCESS
    
    if BACKEND_PROCESS:
        print("Stopping backend server...")
        BACKEND_PROCESS.terminate()
        try:
            BACKEND_PROCESS.wait(timeout=5)
            print("✓ Backend stopped")
        except subprocess.TimeoutExpired:
            print("Backend didn't stop gracefully, killing...")
            BACKEND_PROCESS.kill()
            BACKEND_PROCESS.wait()
        BACKEND_PROCESS = None
    else:
        print("Backend process not found")

def verify_backend_stopped():
    """Verify backend is not responding"""
    if check_backend_health():
        print("✗ Backend is still responding!")
        return False
    else:
        print("✓ Backend is not responding (as expected)")
        return True

def main():
    """Run the fallback behavior test"""
    
    print("="*60)
    print("TASK 5.3: Fallback Behavior Test")
    print("="*60)
    
    try:
        # Step 1: Start backend
        print_step(1, "Start Backend")
        if not start_backend():
            print("Failed to start backend. Exiting.")
            return 1
        
        # Step 2: Verify backend is running
        print_step(2, "Verify Backend is Running")
        if not check_backend_health():
            print("✗ Backend health check failed")
            return 1
        print("✓ Backend is healthy")
        
        # Step 3: Manual step - start frontend
        print_step(3, "Start Frontend (MANUAL STEP)")
        print("\nPlease open a new terminal and run:")
        print("  cd frontend")
        print("  pnpm run dev")
        print("\nThen open http://localhost:5173 in your browser")
        print("\nVerify that:")
        print("  - Dashboard loads successfully")
        print("  - Connection status shows 'active'")
        print("  - Source shows 'Backend API'")
        print("  - Telemetry data is updating")
        
        input("\nPress ENTER when frontend is running and showing backend data...")
        
        # Step 4: Stop backend while frontend is running
        print_step(4, "Stop Backend While Frontend is Running")
        stop_backend()
        
        # Step 5: Verify graceful degradation
        print_step(5, "Verify Graceful Degradation")
        if not verify_backend_stopped():
            return 1
        
        print("\nPlease check the frontend in your browser:")
        print("  Expected behavior:")
        print("    - Connection status should show 'disconnected' or 'warning'")
        print("    - Dashboard should NOT crash or freeze")
        print("    - Console may show connection errors (this is expected)")
        print("    - Frontend may fall back to mock mode OR show stale data")
        
        response = input("\nDoes the frontend show disconnected state? (y/n): ")
        if response.lower() != 'y':
            print("✗ Frontend did not show disconnected state")
            return 1
        print("✓ Frontend shows disconnected state")
        
        # Step 6: Restart backend
        print_step(6, "Restart Backend")
        if not start_backend():
            print("Failed to restart backend")
            return 1
        
        # Step 7: Verify automatic reconnection
        print_step(7, "Verify Automatic Reconnection")
        print("\nPlease check the frontend in your browser:")
        print("  Expected behavior:")
        print("    - Frontend should automatically reconnect (may take up to 2 seconds)")
        print("    - Connection status should show 'active'")
        print("    - Source should show 'Backend API'")
        print("    - Telemetry data should resume updating")
        
        response = input("\nDid the frontend reconnect automatically? (y/n): ")
        if response.lower() != 'y':
            print("✗ Frontend did not reconnect automatically")
            return 1
        print("✓ Frontend reconnected automatically")
        
        # Success
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED")
        print("="*60)
        print("\nFallback behavior verified:")
        print("  - Frontend detects backend disconnection")
        print("  - Frontend shows disconnected status")
        print("  - Frontend does not crash")
        print("  - Frontend automatically reconnects when backend returns")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return 1
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        print("\nCleaning up...")
        stop_backend()

if __name__ == "__main__":
    sys.exit(main())
