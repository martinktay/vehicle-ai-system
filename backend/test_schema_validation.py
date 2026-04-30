"""
Test script for telemetry schema validation (Task 4.3)

This script tests schema validation requirements:
- Valid telemetry messages are accepted
- Missing required fields are rejected
- Incorrect field types are rejected

Usage:
    python test_schema_validation.py

Prerequisites:
    - Backend dependencies installed (pydantic)
"""

import sys
from typing import Dict, Any
from pydantic import ValidationError

# Import the schema
try:
    from app.schemas import TelemetryMessage
except ImportError:
    print("Error: Could not import app.schemas. Make sure you're in the backend directory.")
    sys.exit(1)


def test_valid_telemetry_message() -> bool:
    """
    Test that valid telemetry messages are accepted.
    
    Tests multiple valid message variations to ensure schema accepts
    all valid combinations of field values.
    """
    print("\n=== Testing Valid Telemetry Messages ===")
    
    valid_messages = [
        # Standard message
        {
            "timestamp": "2024-03-20T10:30:00Z",
            "engine_temperature": 85.5,
            "fuel_line_temperature": 65.2,
            "ambient_temperature": 25.0,
            "current_fuel_mode": "diesel",
            "ai_recommendation": "maintain",
            "relay_state_1": True,
            "relay_state_2": False,
            "overheat_flag": False,
            "system_status": "normal",
            "network_status": "connected",
            "power_source": "battery"
        },
        # Boundary values - minimum temperatures
        {
            "timestamp": "2024-03-20T10:30:00Z",
            "engine_temperature": 60.0,
            "fuel_line_temperature": 40.0,
            "ambient_temperature": 15.0,
            "current_fuel_mode": "biodiesel",
            "ai_recommendation": "switch_to_diesel",
            "relay_state_1": False,
            "relay_state_2": False,
            "overheat_flag": False,
            "system_status": "demo_mode",
            "network_status": "disconnected",
            "power_source": "solar"
        },
        # Boundary values - maximum temperatures
        {
            "timestamp": "2024-03-20T10:30:00Z",
            "engine_temperature": 120.0,
            "fuel_line_temperature": 100.0,
            "ambient_temperature": 45.0,
            "current_fuel_mode": "mixed",
            "ai_recommendation": "activate_cooling",
            "relay_state_1": True,
            "relay_state_2": True,
            "overheat_flag": True,
            "system_status": "fail_safe",
            "network_status": "connected",
            "power_source": "grid"
        },
        # All relays on, overheat condition
        {
            "timestamp": "2024-03-20T10:30:00Z",
            "engine_temperature": 105.0,
            "fuel_line_temperature": 85.0,
            "ambient_temperature": 35.0,
            "current_fuel_mode": "diesel",
            "ai_recommendation": "reduce_load",
            "relay_state_1": True,
            "relay_state_2": True,
            "overheat_flag": True,
            "system_status": "error",
            "network_status": "connected",
            "power_source": "battery"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, msg_data in enumerate(valid_messages, 1):
        try:
            msg = TelemetryMessage(**msg_data)
            print(f"✓ Valid message {i} accepted: {msg.system_status}, {msg.engine_temperature}°C")
            passed += 1
        except ValidationError as e:
            print(f"✗ Valid message {i} rejected (should be accepted): {e}")
            failed += 1
    
    if failed == 0:
        print(f"\n✓ All {passed} valid messages accepted")
        return True
    else:
        print(f"\n✗ {failed}/{len(valid_messages)} valid messages incorrectly rejected")
        return False


def test_missing_required_fields() -> bool:
    """
    Test that messages with missing required fields are rejected.
    
    Each test case removes one required field and verifies rejection.
    """
    print("\n=== Testing Missing Required Fields ===")
    
    # Base valid message
    base_message = {
        "timestamp": "2024-03-20T10:30:00Z",
        "engine_temperature": 85.5,
        "fuel_line_temperature": 65.2,
        "ambient_temperature": 25.0,
        "current_fuel_mode": "diesel",
        "ai_recommendation": "maintain",
        "relay_state_1": True,
        "relay_state_2": False,
        "overheat_flag": False,
        "system_status": "normal",
        "network_status": "connected",
        "power_source": "battery"
    }
    
    # Test each required field
    required_fields = list(base_message.keys())
    
    passed = 0
    failed = 0
    
    for field in required_fields:
        # Create message with missing field
        incomplete_message = base_message.copy()
        del incomplete_message[field]
        
        try:
            msg = TelemetryMessage(**incomplete_message)
            print(f"✗ Message missing '{field}' was accepted (should be rejected)")
            failed += 1
        except ValidationError as e:
            print(f"✓ Message missing '{field}' correctly rejected")
            passed += 1
    
    if failed == 0:
        print(f"\n✓ All {passed} incomplete messages correctly rejected")
        return True
    else:
        print(f"\n✗ {failed}/{len(required_fields)} incomplete messages incorrectly accepted")
        return False


def test_incorrect_field_types() -> bool:
    """
    Test that messages with incorrect field types are rejected.
    
    Tests various type mismatches:
    - String instead of number
    - Number instead of boolean
    - Boolean instead of string
    - Invalid type combinations
    """
    print("\n=== Testing Incorrect Field Types ===")
    
    # Base valid message
    base_message = {
        "timestamp": "2024-03-20T10:30:00Z",
        "engine_temperature": 85.5,
        "fuel_line_temperature": 65.2,
        "ambient_temperature": 25.0,
        "current_fuel_mode": "diesel",
        "ai_recommendation": "maintain",
        "relay_state_1": True,
        "relay_state_2": False,
        "overheat_flag": False,
        "system_status": "normal",
        "network_status": "connected",
        "power_source": "battery"
    }
    
    # Test cases with incorrect types
    invalid_type_tests = [
        # Temperature fields should be numbers
        ("engine_temperature", "85.5", "string instead of number"),
        ("fuel_line_temperature", "65.2", "string instead of number"),
        ("ambient_temperature", "25.0", "string instead of number"),
        
        # Boolean fields should be booleans
        ("relay_state_1", "true", "string instead of boolean"),
        ("relay_state_2", 1, "number instead of boolean"),
        ("overheat_flag", "false", "string instead of boolean"),
        
        # String fields should be strings
        ("current_fuel_mode", 123, "number instead of string"),
        ("ai_recommendation", True, "boolean instead of string"),
        ("system_status", 456, "number instead of string"),
        
        # Timestamp should be string
        ("timestamp", 1234567890, "number instead of string"),
        
        # Null values should be rejected
        ("engine_temperature", None, "null value"),
        ("relay_state_1", None, "null value"),
        ("current_fuel_mode", None, "null value"),
        
        # Array/object types should be rejected
        ("engine_temperature", [85.5], "array instead of number"),
        ("relay_state_1", {"state": True}, "object instead of boolean"),
    ]
    
    passed = 0
    failed = 0
    
    for field, invalid_value, description in invalid_type_tests:
        # Create message with incorrect type
        invalid_message = base_message.copy()
        invalid_message[field] = invalid_value
        
        try:
            msg = TelemetryMessage(**invalid_message)
            print(f"✗ Message with {field}={invalid_value} ({description}) was accepted (should be rejected)")
            failed += 1
        except (ValidationError, TypeError) as e:
            print(f"✓ Message with {field}={invalid_value} ({description}) correctly rejected")
            passed += 1
    
    if failed == 0:
        print(f"\n✓ All {passed} type-invalid messages correctly rejected")
        return True
    else:
        print(f"\n✗ {failed}/{len(invalid_type_tests)} type-invalid messages incorrectly accepted")
        return False


def test_extra_fields() -> bool:
    """
    Test that messages with extra fields are handled correctly.
    
    Pydantic by default ignores extra fields, which is acceptable behavior.
    This test documents that behavior.
    """
    print("\n=== Testing Extra Fields (Documentation) ===")
    
    message_with_extra = {
        "timestamp": "2024-03-20T10:30:00Z",
        "engine_temperature": 85.5,
        "fuel_line_temperature": 65.2,
        "ambient_temperature": 25.0,
        "current_fuel_mode": "diesel",
        "ai_recommendation": "maintain",
        "relay_state_1": True,
        "relay_state_2": False,
        "overheat_flag": False,
        "system_status": "normal",
        "network_status": "connected",
        "power_source": "battery",
        # Extra fields
        "extra_field_1": "should be ignored",
        "extra_field_2": 123,
    }
    
    try:
        msg = TelemetryMessage(**message_with_extra)
        print(f"✓ Message with extra fields accepted (extra fields ignored)")
        print(f"  Note: Pydantic ignores extra fields by default")
        return True
    except ValidationError as e:
        print(f"✗ Message with extra fields rejected: {e}")
        return False


def main():
    """Run all schema validation tests."""
    print("=" * 60)
    print("TELEMETRY SCHEMA VALIDATION TEST SUITE (Task 4.3)")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Valid Telemetry Messages", test_valid_telemetry_message()))
    results.append(("Missing Required Fields", test_missing_required_fields()))
    results.append(("Incorrect Field Types", test_incorrect_field_types()))
    results.append(("Extra Fields Handling", test_extra_fields()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} test categories passed")
    
    if passed == total:
        print("\n🎉 All schema validation tests PASSED!")
        print("\nConclusion:")
        print("- ✓ Valid telemetry messages are accepted")
        print("- ✓ Missing required fields are rejected")
        print("- ✓ Incorrect field types are rejected")
        print("- ✓ Schema validation is working correctly")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test category(ies) FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
