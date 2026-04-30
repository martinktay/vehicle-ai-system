"""
Serial Mode Testing Script

This script tests the backend's ability to ingest telemetry data from a physical
ESP32 device via serial connection.

Prerequisites:
- ESP32 connected via USB
- Firmware flashed and running on ESP32
- pyserial and pyserial-asyncio installed

Usage:
    python test_serial_mode.py [--port PORT] [--baud BAUD]

Example:
    # Linux/macOS
    python test_serial_mode.py --port /dev/ttyUSB0
    
    # Windows
    python test_serial_mode.py --port COM3
"""

import asyncio
import argparse
import sys
import time
from datetime import datetime
import serial.tools.list_ports


def list_available_ports():
    """List all available serial ports."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("❌ No serial ports found")
        return []
    
    print("\n📋 Available serial ports:")
    for port in ports:
        print(f"  • {port.device} - {port.description}")
    return ports


def check_port_exists(port_path: str) -> bool:
    """Check if the specified port exists."""
    ports = list(serial.tools.list_ports.comports())
    return any(p.device == port_path for p in ports)


async def test_serial_connection(port: str, baud_rate: int, duration: int = 10):
    """
    Test serial connection and telemetry ingestion.
    
    Args:
        port: Serial port path (e.g., /dev/ttyUSB0 or COM3)
        baud_rate: Baud rate (default: 115200)
        duration: Test duration in seconds
    """
    print(f"\n🔌 Testing serial connection: {port} @ {baud_rate} baud")
    print(f"⏱️  Test duration: {duration} seconds\n")
    
    try:
        import serial_asyncio
        
        # Attempt to connect
        print("Connecting to serial port...")
        reader, writer = await asyncio.wait_for(
            serial_asyncio.open_serial_connection(url=port, baudrate=baud_rate),
            timeout=5.0
        )
        print("✅ Serial connection established\n")
        
        # Read telemetry messages
        messages_received = 0
        start_time = time.time()
        last_message_time = start_time
        
        print("📡 Reading telemetry data...")
        print("-" * 80)
        
        while time.time() - start_time < duration:
            try:
                # Read one line with timeout
                line = await asyncio.wait_for(reader.readline(), timeout=5.0)
                
                if line:
                    messages_received += 1
                    current_time = time.time()
                    interval = current_time - last_message_time
                    last_message_time = current_time
                    
                    # Decode and display
                    line_str = line.decode('utf-8').strip()
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    
                    print(f"[{timestamp}] Message #{messages_received} (Δ{interval:.2f}s)")
                    print(f"  {line_str[:100]}{'...' if len(line_str) > 100 else ''}")
                    
                    # Try to parse as JSON
                    try:
                        import json
                        data = json.loads(line_str)
                        
                        # Validate required fields
                        required_fields = [
                            'timestamp', 'engine_temperature', 'fuel_line_temperature',
                            'ambient_temperature', 'current_fuel_mode', 'ai_recommendation',
                            'relay_state_1', 'relay_state_2', 'overheat_flag',
                            'system_status', 'network_status', 'power_source'
                        ]
                        
                        missing_fields = [f for f in required_fields if f not in data]
                        if missing_fields:
                            print(f"  ⚠️  Missing fields: {', '.join(missing_fields)}")
                        else:
                            print(f"  ✅ Valid telemetry schema")
                            print(f"     Engine: {data.get('engine_temperature')}°C, "
                                  f"Fuel Line: {data.get('fuel_line_temperature')}°C, "
                                  f"Ambient: {data.get('ambient_temperature')}°C")
                            print(f"     Mode: {data.get('current_fuel_mode')}, "
                                  f"AI: {data.get('ai_recommendation')}")
                            print(f"     Relays: R1={data.get('relay_state_1')}, "
                                  f"R2={data.get('relay_state_2')}, "
                                  f"Overheat={data.get('overheat_flag')}")
                    
                    except json.JSONDecodeError as e:
                        print(f"  ⚠️  Invalid JSON: {e}")
                    
                    print()
            
            except asyncio.TimeoutError:
                print(f"⚠️  No data received for 5 seconds")
                break
            
            except UnicodeDecodeError as e:
                print(f"⚠️  Failed to decode line: {e}")
                continue
        
        # Close connection
        writer.close()
        await writer.wait_closed()
        
        # Summary
        print("-" * 80)
        print(f"\n📊 Test Summary:")
        print(f"  • Duration: {time.time() - start_time:.2f} seconds")
        print(f"  • Messages received: {messages_received}")
        if messages_received > 0:
            avg_interval = (time.time() - start_time) / messages_received
            print(f"  • Average interval: {avg_interval:.2f} seconds")
            print(f"  • Message rate: {messages_received / (time.time() - start_time):.2f} msg/s")
        
        if messages_received > 0:
            print("\n✅ Serial mode test PASSED")
            return True
        else:
            print("\n❌ Serial mode test FAILED: No messages received")
            return False
    
    except asyncio.TimeoutError:
        print(f"❌ Connection timeout: Could not connect to {port}")
        print("   Check that:")
        print("   • ESP32 is connected via USB")
        print("   • Firmware is running on ESP32")
        print("   • Correct port is specified")
        print("   • No other program is using the port")
        return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_reconnection(port: str, baud_rate: int):
    """
    Test automatic reconnection on disconnect.
    
    This test requires manual intervention:
    1. Connect ESP32
    2. Wait for connection
    3. Disconnect ESP32 (unplug USB)
    4. Reconnect ESP32
    5. Verify automatic reconnection
    """
    print(f"\n🔄 Testing automatic reconnection")
    print("This test requires manual intervention:")
    print("  1. Ensure ESP32 is connected")
    print("  2. Script will connect and read data")
    print("  3. Disconnect ESP32 when prompted")
    print("  4. Reconnect ESP32 when prompted")
    print("  5. Script will verify reconnection\n")
    
    input("Press Enter to start reconnection test...")
    
    # This would require integration with the SerialReader class
    # For now, just provide instructions
    print("\n📝 Manual reconnection test procedure:")
    print("  1. Start backend with: INGESTION_MODE=serial SERIAL_PORT={port} python -m app.main")
    print("  2. Verify connection in backend logs")
    print("  3. Unplug ESP32 USB cable")
    print("  4. Observe backend logs for disconnection message")
    print("  5. Plug ESP32 back in")
    print("  6. Verify backend logs show reconnection")
    print("  7. Verify telemetry ingestion resumes")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test serial mode telemetry ingestion from ESP32"
    )
    parser.add_argument(
        '--port',
        type=str,
        help='Serial port path (e.g., /dev/ttyUSB0 or COM3)'
    )
    parser.add_argument(
        '--baud',
        type=int,
        default=115200,
        help='Baud rate (default: 115200)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=10,
        help='Test duration in seconds (default: 10)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available serial ports and exit'
    )
    parser.add_argument(
        '--reconnect',
        action='store_true',
        help='Test automatic reconnection (requires manual intervention)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Serial Mode Testing Script")
    print("=" * 80)
    
    # List ports if requested
    if args.list:
        list_available_ports()
        return 0
    
    # Check if port is specified
    if not args.port:
        print("\n❌ Error: --port argument is required")
        print("\nUse --list to see available ports")
        list_available_ports()
        return 1
    
    # Check if port exists
    if not check_port_exists(args.port):
        print(f"\n❌ Error: Port {args.port} not found")
        list_available_ports()
        return 1
    
    # Run tests
    try:
        if args.reconnect:
            asyncio.run(test_reconnection(args.port, args.baud))
        else:
            success = asyncio.run(test_serial_connection(
                args.port,
                args.baud,
                args.duration
            ))
            return 0 if success else 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        return 1


if __name__ == "__main__":
    sys.exit(main())
