"""
Serial Telemetry Reader

Architecture: Data ingestion layer
Purpose: Read telemetry from ESP32 via USB serial port

This module:
- Reads newline-delimited JSON from serial port
- Parses and validates telemetry messages
- Stores valid messages in TelemetryStore
- Handles disconnections and errors gracefully
- Supports automatic reconnection

Design: Non-blocking async I/O
"""

import asyncio
import json
import serial_asyncio
from datetime import datetime
from typing import Optional
from app.schemas import TelemetryMessage
from app.telemetry_store import telemetry_store


class SerialReader:
    """
    Reads telemetry from ESP32 via serial port.
    
    Features:
    - Async serial reading (non-blocking)
    - Line-by-line JSON parsing
    - Schema validation
    - Auto-reconnection on disconnect
    - Error handling and logging
    """
    
    def __init__(self, port: str = "/dev/ttyUSB0", baud_rate: int = 115200):
        """
        Initialize serial reader.
        
        Args:
            port: Serial port path (e.g., "/dev/ttyUSB0" on Linux, "COM3" on Windows)
            baud_rate: Baud rate (default: 115200)
        """
        self.port = port
        self.baud_rate = baud_rate
        self.running = False
        self.task: Optional[asyncio.Task] = None
        self.connected = False
        
        print(f"Serial reader configured: {port} @ {baud_rate} baud")
    
    async def start(self) -> None:
        """Start the serial reader loop."""
        if self.running:
            return
        
        self.running = True
        self.task = asyncio.create_task(self._read_loop())
        print("[OK] Serial reader started")
    
    async def stop(self) -> None:
        """Stop the serial reader loop."""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        print("[OK] Serial reader stopped")
    
    def is_connected(self) -> bool:
        """
        Check if serial port is connected.
        
        Returns:
            True if connected, False otherwise
        """
        return self.connected
    
    async def _read_loop(self) -> None:
        """
        Main serial read loop with automatic reconnection.
        
        Handles:
        - Connection failures
        - Disconnections during operation
        - Exponential backoff on errors
        """
        retry_delay = 1  # Start with 1 second
        max_retry_delay = 60  # Max 60 seconds
        
        while self.running:
            try:
                # Attempt to connect
                print(f"Connecting to serial port {self.port}...")
                reader, writer = await serial_asyncio.open_serial_connection(
                    url=self.port,
                    baudrate=self.baud_rate
                )
                
                self.connected = True
                print(f"[OK] Connected to {self.port}")
                
                # Reset retry delay on successful connection
                retry_delay = 1
                
                # Read loop
                while self.running:
                    try:
                        # Read one line (newline-delimited JSON)
                        line = await reader.readline()
                        
                        if not line:
                            # EOF or disconnect
                            print("Serial connection closed")
                            break
                        
                        # Decode and process line
                        line_str = line.decode('utf-8').strip()
                        if line_str:
                            await self._process_line(line_str)
                    
                    except UnicodeDecodeError as e:
                        print(f"WARNING: Failed to decode line: {e}")
                        continue
                    
                    except Exception as e:
                        print(f"ERROR: Error reading line: {e}")
                        break
                
                # Close connection
                writer.close()
                await writer.wait_closed()
                self.connected = False
            
            except serial_asyncio.SerialException as e:
                self.connected = False
                print(f"ERROR: Serial connection failed: {e}")
                
                if not self.running:
                    break
                
                # Exponential backoff
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)
            
            except Exception as e:
                self.connected = False
                print(f"ERROR: Unexpected error: {e}")
                
                if not self.running:
                    break
                
                await asyncio.sleep(retry_delay)
    
    async def _process_line(self, line: str) -> None:
        """
        Process a single line of telemetry.
        
        Args:
            line: JSON string from serial port
        """
        try:
            # Ignore boot logs and status chatter; only JSON telemetry matters here.
            if not line.startswith("{"):
                return

            # Parse JSON
            data = json.loads(line)

            # The ESP32 serial stream may use device uptime milliseconds instead of
            # an ISO timestamp. Normalize to server receive time for the v1 contract.
            timestamp = data.get("timestamp")
            if not isinstance(timestamp, str) or not self._is_iso_timestamp(timestamp):
                data["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            # Validate against schema
            message = TelemetryMessage(**data)
            
            # Store in telemetry store
            await telemetry_store.store(message)
            
            # Log successful ingestion (optional, can be verbose)
            # print(f"✓ Telemetry: Engine={message.engine_temperature}°C")
        
        except json.JSONDecodeError as e:
            print(f"WARNING: Invalid JSON: {line[:100]}... Error: {e}")
        
        except Exception as e:
            print(f"WARNING: Failed to process telemetry: {e}")

    @staticmethod
    def _is_iso_timestamp(value: str) -> bool:
        """Return True when a timestamp already matches ISO 8601 expectations."""
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False
