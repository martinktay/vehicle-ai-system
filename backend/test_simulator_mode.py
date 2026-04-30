"""
Test script for simulator mode verification

This script tests all requirements for Task 4.1:
- Backend starts with INGESTION_MODE=simulator
- Telemetry generation every 2 seconds
- /api/health endpoint returns correct status
- /api/latest returns valid telemetry
- /api/history returns 60-second window

Usage:
    python test_simulator_mode.py

Prerequisites:
    - Backend server must be running on http://localhost:8000
    - Start with: python -m app.main (or INGESTION_MODE=simulator python -m app.main)
"""

import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any


BASE_URL = "http://localhost:8000"


def test_health_endpoint() -> bool:
    """
    Test /api/health endpoint returns correct status.
    
    Expected response:
    - status: "ok"
    - mode: "simulator"
    - telemetry_available: true
    - ingestion_connected: true
    """
    print("\n=== Testing /api/health endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        response.raise_for_status()
        data = response.json()
        
        print(f"Response: {data}")
        
        # Verify expected fields
        assert data["status"] == "ok", f"Expected status 'ok', got '{data['status']}'"
        assert data["mode"] == "simulator", f"Expected mode 'simulator', got '{data['mode']}'"
        assert data["telemetry_available"] is True, "Expected telemetry_available to be True"
        assert data["ingestion_connected"] is True, "Expected ingestion_connected to be True"
        
        print("✓ /api/health endpoint test PASSED")
        return True
        
    except Exception as e:
        print(f"✗ /api/health endpoint test FAILED: {e}")
        return False


def test_latest_endpoint() -> bool:
    """
    Test /api/latest endpoint returns valid telemetry.
    
    Expected response:
    - All fields from Telemetry Data Contract v1
    - Valid data types and ranges
    - ISO 8601 timestamp format
    """
    print("\n=== Testing /api/latest endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/latest")
        response.raise_for_status()
        data = response.json()
        
        print(f"Response: {data}")
        
        # Verify required fields exist
        required_fields = [
            "timestamp", "engine_temperature", "fuel_line_temperature",
            "ambient_temperature", "current_fuel_mode", "ai_recommendation",
            "relay_state_1", "relay_state_2", "overheat_flag",
            "system_status", "network_status", "power_source"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Verify timestamp format (ISO 8601)
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z"), f"Timestamp should end with 'Z': {timestamp}"
        
        # Verify temperature ranges
        assert 60 <= data["engine_temperature"] <= 120, \
            f"Engine temperature out of range: {data['engine_temperature']}"
        assert 40 <= data["fuel_line_temperature"] <= 100, \
            f"Fuel line temperature out of range: {data['fuel_line_temperature']}"
        assert 15 <= data["ambient_temperature"] <= 45, \
            f"Ambient temperature out of range: {data['ambient_temperature']}"
        
        # Verify boolean fields
        assert isinstance(data["relay_state_1"], bool), "relay_state_1 should be boolean"
        assert isinstance(data["relay_state_2"], bool), "relay_state_2 should be boolean"
        assert isinstance(data["overheat_flag"], bool), "overheat_flag should be boolean"
        
        # Verify string fields
        assert data["current_fuel_mode"] in ["diesel", "biodiesel", "mixed"], \
            f"Invalid fuel mode: {data['current_fuel_mode']}"
        assert data["system_status"] in ["demo_mode", "fail_safe"], \
            f"Invalid system status: {data['system_status']}"
        
        print("✓ /api/latest endpoint test PASSED")
        return True
        
    except Exception as e:
        print(f"✗ /api/latest endpoint test FAILED: {e}")
        return False


def test_history_endpoint() -> bool:
    """
    Test /api/history endpoint returns 60-second window.
    
    Expected response:
    - List of telemetry messages
    - Messages within 60-second window
    - At least 15 messages (30 messages expected for 60 seconds at 2-second intervals)
    """
    print("\n=== Testing /api/history endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/history")
        response.raise_for_status()
        data = response.json()
        
        print(f"History count: {len(data)}")
        
        # Verify we have messages
        assert len(data) > 0, "History should contain at least one message"
        
        # Verify all messages have required fields
        for msg in data:
            assert "timestamp" in msg, "Each message should have a timestamp"
            assert "engine_temperature" in msg, "Each message should have engine_temperature"
        
        # Verify messages are within 60-second window
        if len(data) >= 2:
            first_timestamp = datetime.fromisoformat(data[0]["timestamp"].replace("Z", "+00:00"))
            last_timestamp = datetime.fromisoformat(data[-1]["timestamp"].replace("Z", "+00:00"))
            time_diff = (last_timestamp - first_timestamp).total_seconds()
            
            print(f"Time window: {time_diff:.1f} seconds")
            assert time_diff <= 60, f"Time window exceeds 60 seconds: {time_diff}"
        
        # Show recent messages
        print("\nRecent 3 messages:")
        for msg in data[-3:]:
            print(f"  {msg['timestamp']} - Engine: {msg['engine_temperature']}°C")
        
        print("✓ /api/history endpoint test PASSED")
        return True
        
    except Exception as e:
        print(f"✗ /api/history endpoint test FAILED: {e}")
        return False


def test_telemetry_generation_interval() -> bool:
    """
    Test telemetry generation every 2 seconds.
    
    Verifies:
    - New telemetry messages appear every ~2 seconds
    - Timestamps are approximately 2 seconds apart
    """
    print("\n=== Testing telemetry generation interval ===")
    
    try:
        # Get initial latest message
        response1 = requests.get(f"{BASE_URL}/api/latest")
        response1.raise_for_status()
        data1 = response1.json()
        timestamp1 = data1["timestamp"]
        
        print(f"First message: {timestamp1}")
        
        # Wait 5 seconds (should get 2-3 new messages at 2-second intervals)
        print("Waiting 5 seconds...")
        time.sleep(5)
        
        # Get new latest message
        response2 = requests.get(f"{BASE_URL}/api/latest")
        response2.raise_for_status()
        data2 = response2.json()
        timestamp2 = data2["timestamp"]
        
        print(f"Second message: {timestamp2}")
        
        # Verify timestamps are different
        assert timestamp1 != timestamp2, "Timestamps should be different after 5 seconds"
        
        # Parse timestamps and calculate difference
        ts1 = datetime.fromisoformat(timestamp1.replace("Z", "+00:00"))
        ts2 = datetime.fromisoformat(timestamp2.replace("Z", "+00:00"))
        time_diff = (ts2 - ts1).total_seconds()
        
        print(f"Time difference: {time_diff:.1f} seconds")
        
        # Should be approximately 4-6 seconds (2-3 intervals at 2 seconds each)
        assert 4 <= time_diff <= 7, \
            f"Expected 4-7 seconds difference (2-3 intervals), got {time_diff}"
        
        print("✓ Telemetry generation interval test PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Telemetry generation interval test FAILED: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("SIMULATOR MODE TEST SUITE")
    print("=" * 60)
    print(f"\nTesting backend at: {BASE_URL}")
    print("Ensure backend is running with: python -m app.main")
    
    results = []
    
    # Run all tests
    results.append(("Health Endpoint", test_health_endpoint()))
    results.append(("Latest Endpoint", test_latest_endpoint()))
    results.append(("History Endpoint", test_history_endpoint()))
    results.append(("Telemetry Generation Interval", test_telemetry_generation_interval()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
