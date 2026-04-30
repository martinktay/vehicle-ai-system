#!/usr/bin/env python3
"""
Automated Test for Task 5.3: Test fallback behavior

This script automatically tests the frontend's resilience when the backend becomes unavailable.
It uses Playwright to control the browser and verify the UI behavior.

Test Steps:
1. Start backend
2. Start frontend (using Playwright)
3. Verify initial connection state
4. Stop backend while frontend is running
5. Verify frontend shows disconnected state
6. Restart backend
7. Verify frontend reconnects automatically
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
FRONTEND_URL = "http://localhost:5173"
BACKEND_DIR = Path(__file__).parent / "backend"
FRONTEND_DIR = Path(__file__).parent / "frontend"
BACKEND_PROCESS = None
FRONTEND_PROCESS = None

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

def check_frontend_health():
    """Check if frontend is responding"""
    try:
        response = requests.get(FRONTEND_URL, timeout=2)
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

def start_frontend():
    """Start the frontend dev server"""
    global FRONTEND_PROCESS
    
    print("Starting frontend dev server...")
    
    # Start vite dev server
    FRONTEND_PROCESS = subprocess.Popen(
        ["pnpm", "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for frontend to start
    print("Waiting for frontend to start...")
    for i in range(60):
        time.sleep(1)
        if check_frontend_health():
            print(f"✓ Frontend started successfully (took {i+1}s)")
            return True
    
    print("✗ Frontend failed to start within 60 seconds")
    return False

def stop_frontend():
    """Stop the frontend dev server"""
    global FRONTEND_PROCESS
    
    if FRONTEND_PROCESS:
        print("Stopping frontend dev server...")
        FRONTEND_PROCESS.terminate()
        try:
            FRONTEND_PROCESS.wait(timeout=5)
            print("✓ Frontend stopped")
        except subprocess.TimeoutExpired:
            print("Frontend didn't stop gracefully, killing...")
            FRONTEND_PROCESS.kill()
            FRONTEND_PROCESS.wait()
        FRONTEND_PROCESS = None

def verify_backend_stopped():
    """Verify backend is not responding"""
    if check_backend_health():
        print("✗ Backend is still responding!")
        return False
    else:
        print("✓ Backend is not responding (as expected)")
        return True

def test_with_browser():
    """Test using browser automation (requires playwright)"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("\nLaunching browser for automated testing...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            # Navigate to frontend
            print(f"Navigating to {FRONTEND_URL}...")
            page.goto(FRONTEND_URL)
            page.wait_for_load_state("networkidle")
            
            # Wait for initial load
            time.sleep(3)
            
            # Step 3: Verify initial connection
            print_step(3, "Verify Initial Connection State")
            
            # Check for connection status
            connection_status = page.locator('text=Connection').locator('..').locator('.status-value')
            if connection_status.count() > 0:
                status_text = connection_status.inner_text()
                print(f"Connection status: {status_text}")
                
                if 'active' in status_text.lower():
                    print("✓ Frontend shows 'active' connection")
                else:
                    print(f"✗ Expected 'active', got '{status_text}'")
                    browser.close()
                    return False
            else:
                print("✗ Could not find connection status element")
                browser.close()
                return False
            
            # Check data source
            source_status = page.locator('text=Source').locator('..').locator('.status-value')
            if source_status.count() > 0:
                source_text = source_status.inner_text()
                print(f"Data source: {source_text}")
                
                if 'backend' in source_text.lower() or 'api' in source_text.lower():
                    print("✓ Frontend shows 'Backend API' source")
                else:
                    print(f"⚠ Expected 'Backend API', got '{source_text}'")
            
            # Step 4: Stop backend
            print_step(4, "Stop Backend While Frontend is Running")
            stop_backend()
            
            # Step 5: Verify graceful degradation
            print_step(5, "Verify Graceful Degradation")
            verify_backend_stopped()
            
            # Wait for frontend to detect disconnection (max 10 seconds)
            print("\nWaiting for frontend to detect disconnection...")
            disconnected = False
            for i in range(10):
                time.sleep(1)
                status_text = connection_status.inner_text()
                print(f"  [{i+1}s] Connection status: {status_text}")
                
                if 'disconnected' in status_text.lower() or 'warning' in status_text.lower():
                    print(f"✓ Frontend detected disconnection after {i+1}s")
                    disconnected = True
                    break
            
            if not disconnected:
                print("✗ Frontend did not show disconnected state within 10 seconds")
                browser.close()
                return False
            
            # Verify page didn't crash
            try:
                page.title()
                print("✓ Frontend did not crash")
            except:
                print("✗ Frontend appears to have crashed")
                browser.close()
                return False
            
            # Step 6: Restart backend
            print_step(6, "Restart Backend")
            if not start_backend():
                print("Failed to restart backend")
                browser.close()
                return False
            
            # Step 7: Verify automatic reconnection
            print_step(7, "Verify Automatic Reconnection")
            
            # Wait for frontend to reconnect (max 15 seconds)
            print("\nWaiting for frontend to reconnect...")
            reconnected = False
            for i in range(15):
                time.sleep(1)
                status_text = connection_status.inner_text()
                print(f"  [{i+1}s] Connection status: {status_text}")
                
                if 'active' in status_text.lower():
                    print(f"✓ Frontend reconnected after {i+1}s")
                    reconnected = True
                    break
            
            if not reconnected:
                print("✗ Frontend did not reconnect within 15 seconds")
                browser.close()
                return False
            
            # Verify source is back to backend
            source_text = source_status.inner_text()
            print(f"Data source after reconnection: {source_text}")
            
            if 'backend' in source_text.lower() or 'api' in source_text.lower():
                print("✓ Frontend reconnected to Backend API")
            else:
                print(f"⚠ Expected 'Backend API', got '{source_text}'")
            
            browser.close()
            return True
            
    except ImportError:
        print("\n⚠ Playwright not installed. Falling back to manual testing.")
        print("To enable automated browser testing, run:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return None

def manual_test():
    """Run manual test with user verification"""
    print("\n" + "="*60)
    print("MANUAL TESTING MODE")
    print("="*60)
    
    # Step 3: Manual step - verify frontend
    print_step(3, "Verify Frontend (MANUAL)")
    print("\nPlease open http://localhost:5173 in your browser")
    print("\nVerify that:")
    print("  - Dashboard loads successfully")
    print("  - Connection status shows 'active'")
    print("  - Source shows 'Backend API'")
    print("  - Telemetry data is updating")
    
    response = input("\nIs the frontend showing backend data correctly? (y/n): ")
    if response.lower() != 'y':
        print("✗ Frontend not showing backend data")
        return False
    print("✓ Frontend connected to backend")
    
    # Step 4: Stop backend
    print_step(4, "Stop Backend While Frontend is Running")
    stop_backend()
    
    # Step 5: Verify graceful degradation
    print_step(5, "Verify Graceful Degradation")
    verify_backend_stopped()
    
    print("\nPlease check the frontend in your browser:")
    print("  Expected behavior:")
    print("    - Connection status should show 'disconnected' or 'warning'")
    print("    - Dashboard should NOT crash or freeze")
    print("    - Console may show connection errors (this is expected)")
    
    response = input("\nDoes the frontend show disconnected state? (y/n): ")
    if response.lower() != 'y':
        print("✗ Frontend did not show disconnected state")
        return False
    print("✓ Frontend shows disconnected state")
    
    # Step 6: Restart backend
    print_step(6, "Restart Backend")
    if not start_backend():
        print("Failed to restart backend")
        return False
    
    # Step 7: Verify automatic reconnection
    print_step(7, "Verify Automatic Reconnection")
    print("\nPlease check the frontend in your browser:")
    print("  Expected behavior:")
    print("    - Frontend should automatically reconnect (may take up to 5 seconds)")
    print("    - Connection status should show 'active'")
    print("    - Source should show 'Backend API'")
    print("    - Telemetry data should resume updating")
    
    response = input("\nDid the frontend reconnect automatically? (y/n): ")
    if response.lower() != 'y':
        print("✗ Frontend did not reconnect automatically")
        return False
    print("✓ Frontend reconnected automatically")
    
    return True

def main():
    """Run the fallback behavior test"""
    
    print("="*60)
    print("TASK 5.3: Fallback Behavior Test (Automated)")
    print("="*60)
    
    try:
        # Step 1: Start backend
        print_step(1, "Start Backend")
        if not start_backend():
            print("Failed to start backend. Exiting.")
            return 1
        
        # Step 2: Start frontend
        print_step(2, "Start Frontend")
        if not start_frontend():
            print("Failed to start frontend. Exiting.")
            return 1
        
        # Try automated testing first
        result = test_with_browser()
        
        if result is None:
            # Playwright not available, fall back to manual
            result = manual_test()
        
        if result:
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
        else:
            print("\n" + "="*60)
            print("✗ TESTS FAILED")
            print("="*60)
            return 1
        
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
        stop_frontend()
        stop_backend()

if __name__ == "__main__":
    sys.exit(main())
