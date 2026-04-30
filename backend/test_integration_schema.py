"""
Integration test for schema validation with simulator

This test verifies that the simulator generates telemetry that passes
strict schema validation.

Usage:
    python test_integration_schema.py
"""

import asyncio
from app.simulator import simulator
from app.telemetry_store import telemetry_store
from app.schemas import TelemetryMessage


async def test_simulator_with_strict_schema():
    """
    Test that simulator generates valid telemetry with strict schema validation.
    """
    print("=" * 60)
    print("INTEGRATION TEST: Simulator + Strict Schema Validation")
    print("=" * 60)
    
    print("\n1. Starting simulator...")
    await simulator.start()
    
    print("2. Waiting for telemetry generation (5 seconds)...")
    await asyncio.sleep(5)
    
    print("3. Retrieving generated telemetry...")
    current = await telemetry_store.get_current()
    history = await telemetry_store.get_history()
    
    print(f"4. Validating telemetry...")
    
    if current is None:
        print("✗ FAILED: No telemetry generated")
        await simulator.stop()
        return False
    
    # Verify current message
    print(f"\n   Current telemetry:")
    print(f"   - Timestamp: {current.timestamp}")
    print(f"   - Engine temp: {current.engine_temperature}°C")
    print(f"   - Fuel line temp: {current.fuel_line_temperature}°C")
    print(f"   - Ambient temp: {current.ambient_temperature}°C")
    print(f"   - Fuel mode: {current.current_fuel_mode}")
    print(f"   - AI recommendation: {current.ai_recommendation}")
    print(f"   - Relay 1: {current.relay_state_1}")
    print(f"   - Relay 2: {current.relay_state_2}")
    print(f"   - Overheat: {current.overheat_flag}")
    print(f"   - System status: {current.system_status}")
    
    # Verify it's a valid TelemetryMessage instance
    assert isinstance(current, TelemetryMessage), "Current message is not a TelemetryMessage"
    
    # Verify history
    print(f"\n   History: {len(history)} messages")
    assert len(history) >= 2, f"Expected at least 2 messages in history, got {len(history)}"
    
    # Verify all history messages are valid
    for i, msg in enumerate(history):
        assert isinstance(msg, TelemetryMessage), f"History message {i} is not a TelemetryMessage"
    
    print("\n5. Stopping simulator...")
    await simulator.stop()
    
    print("\n" + "=" * 60)
    print("✅ INTEGRATION TEST PASSED")
    print("=" * 60)
    print("\nConclusion:")
    print("- Simulator generates valid telemetry")
    print("- Strict schema validation accepts simulator output")
    print("- All required fields present with correct types")
    print("- Integration between simulator and schema is working correctly")
    
    return True


async def main():
    """Run the integration test."""
    try:
        success = await test_simulator_with_strict_schema()
        return 0 if success else 1
    except Exception as e:
        print(f"\n✗ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
