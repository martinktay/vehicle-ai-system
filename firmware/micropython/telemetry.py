"""
Telemetry Module

Purpose: Build and transmit telemetry messages via serial
Format: Newline-delimited JSON conforming to Telemetry Data Contract v1

Architecture: Telemetry layer
Edge-Intelligence: All decision values computed on ESP32
"""

import json
import time


class TelemetryBuilder:
    """
    Builds telemetry messages conforming to Telemetry Data Contract v1.
    
    Schema compliance:
    - All field names match TELEMETRY_SCHEMA.md exactly
    - Field names are immutable (no changes without version bump)
    """
    
    def __init__(self):
        """Initialize telemetry builder."""
        self.fuel_mode = "diesel"  # Current fuel mode state
        self.boot_time = time.ticks_ms()
    
    def build_message(self, temps, ai_rec, relay1, relay2, overheat, system_status):
        """
        Build telemetry message.
        
        Args:
            temps: Dictionary with 'engine', 'fuel_line', 'ambient' temperatures
            ai_rec: AI recommendation string
            relay1: Relay 1 state (bool)
            relay2: Relay 2 state (bool)
            overheat: Overheat flag (bool)
            system_status: System status string
        
        Returns:
            Dictionary conforming to Telemetry Data Contract v1
        """
        return {
            "timestamp": self._get_timestamp(),
            "engine_temperature": temps['engine'],
            "fuel_line_temperature": temps['fuel_line'],
            "ambient_temperature": temps['ambient'],
            "current_fuel_mode": self.fuel_mode,
            "ai_recommendation": ai_rec,
            "relay_state_1": relay1,
            "relay_state_2": relay2,
            "overheat_flag": overheat,
            "system_status": system_status,
            "network_status": "disconnected",  # No LTE in v1
            "power_source": "battery"
        }
    
    def _get_timestamp(self):
        """
        Generate ISO 8601 timestamp.
        
        Note: ESP32 RTC may not have accurate time without NTP.
        For v1, use uptime-based timestamp.
        
        Returns:
            ISO 8601 formatted timestamp string
        """
        # Simple uptime-based timestamp (seconds since boot)
        uptime_sec = time.ticks_diff(time.ticks_ms(), self.boot_time) // 1000
        
        # Format as ISO 8601 (simplified - no actual date/time)
        # In production, sync with NTP or use RTC
        return f"1970-01-01T00:{uptime_sec // 60:02d}:{uptime_sec % 60:02d}.000Z"


class SerialWriter:
    """
    Writes telemetry messages to serial port.
    
    Format: Newline-delimited JSON
    Example: {"timestamp":"...","engine_temperature":85.3,...}\n
    """
    
    def __init__(self):
        """Initialize serial writer."""
        print("✓ Serial writer initialized (USB UART)")
    
    def write(self, message_dict):
        """
        Write telemetry message to serial port.
        
        Args:
            message_dict: Telemetry message dictionary
        """
        try:
            # Convert to JSON string
            json_str = json.dumps(message_dict)
            
            # Write to serial with newline delimiter
            print(json_str)
            
        except Exception as e:
            print(f"ERROR: Failed to write telemetry: {e}")
