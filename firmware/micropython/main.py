"""
ESP32 Climate-Smart Telemetry Controller

Hardware: ESP32-S3
Sensors: DS18B20 temperature sensors (engine, fuel line, ambient)
Actuators: 2-channel relay module
Indicators: 4 status LEDs

Architecture: Edge-Intelligence First
- All decision logic executes on ESP32
- Bridge service only forwards telemetry
- Dashboard only displays data

Fail-Safe: Hardware + software fail-safe mechanisms
- Active LOW relays (OFF when GPIO HIGH)
- Watchdog timer (auto-reset on hang)
- Overheat detection and fail-safe activation
"""

import time
import machine
from sensors import SensorManager
from relays import RelayController
from status_leds import StatusLEDs
from telemetry import TelemetryBuilder, SerialWriter


# ============================================================================
# CONFIGURATION - EDIT THESE VALUES FOR YOUR HARDWARE
# ============================================================================

# Temperature Sensor Pins (DS18B20 OneWire)
PIN_ENGINE_TEMP = 4      # Engine temperature sensor
PIN_FUEL_LINE_TEMP = 5   # Fuel line temperature sensor
PIN_AMBIENT_TEMP = 6     # Ambient temperature sensor

# Relay Control Pins (Active LOW)
PIN_RELAY_1 = 7          # Relay 1: Cooling system
PIN_RELAY_2 = 8          # Relay 2: Fuel switching

# Status LED Pins
PIN_LED_STATUS = 9       # Green: System running
PIN_LED_WARNING = 10     # Yellow: High temperature
PIN_LED_ERROR = 11       # Red: Overheat / fail-safe
PIN_LED_ACTIVITY = 12    # Blue: Telemetry transmission

# Safety Thresholds (°C)
THRESHOLD_ENGINE_OVERHEAT = 100.0   # Fail-safe activation
THRESHOLD_FUEL_LINE_MAX = 90.0      # Fail-safe activation
THRESHOLD_ENGINE_OPTIMAL = 80.0     # Warning threshold
THRESHOLD_COOLING_ACTIVATE = 90.0   # Relay 1 activation
THRESHOLD_FUEL_SWITCH = 80.0        # Relay 2 activation

# Timing (milliseconds)
SAMPLE_INTERVAL_MS = 2000           # Sensor sampling every 2 seconds
TELEMETRY_INTERVAL_MS = 2000        # Telemetry transmission every 2 seconds

# ============================================================================
# DECISION ENGINE - Edge Intelligence
# ============================================================================

class DecisionEngine:
    """
    AI decision engine for climate-smart fuel management.
    
    Edge-Intelligence First:
    - All decision logic executes on ESP32
    - Deterministic, rule-based (no black-box ML)
    - Transparent and explainable
    """
    
    @staticmethod
    def compute_recommendation(engine_temp, fuel_line_temp, overheat):
        """
        Compute AI recommendation based on sensor readings.
        
        Args:
            engine_temp: Engine temperature (°C)
            fuel_line_temp: Fuel line temperature (°C)
            overheat: Overheat flag (bool)
        
        Returns:
            AI recommendation string
        """
        # Priority 1: Safety (highest priority)
        if overheat:
            return "activate_cooling"
        
        # Priority 2: Overheat prevention
        if engine_temp > 95:
            return "reduce_load"
        
        # Priority 3: Fuel optimization
        if engine_temp < THRESHOLD_ENGINE_OPTIMAL:
            return "switch_to_biodiesel"
        
        if engine_temp > 90:
            return "switch_to_diesel"
        
        # Priority 4: Maintain current state
        return "maintain"
    
    @staticmethod
    def should_activate_cooling(engine_temp):
        """
        Determine if cooling system should activate.
        
        Args:
            engine_temp: Engine temperature (°C)
        
        Returns:
            True if cooling should activate, False otherwise
        """
        return engine_temp > THRESHOLD_COOLING_ACTIVATE
    
    @staticmethod
    def should_switch_fuel(fuel_line_temp):
        """
        Determine if fuel switching should activate.
        
        Args:
            fuel_line_temp: Fuel line temperature (°C)
        
        Returns:
            True if fuel switch should activate, False otherwise
        """
        return fuel_line_temp > THRESHOLD_FUEL_SWITCH


# ============================================================================
# SAFETY MONITOR
# ============================================================================

class SafetyMonitor:
    """
    Monitors safety thresholds and triggers fail-safe.
    
    Safety-critical: Highest priority in system
    """
    
    @staticmethod
    def check_overheat(engine_temp, fuel_line_temp):
        """
        Check if overheat condition exists.
        
        Args:
            engine_temp: Engine temperature (°C)
            fuel_line_temp: Fuel line temperature (°C)
        
        Returns:
            True if overheat detected, False otherwise
        """
        return (engine_temp > THRESHOLD_ENGINE_OVERHEAT or 
                fuel_line_temp > THRESHOLD_FUEL_LINE_MAX)
    
    @staticmethod
    def check_warning(engine_temp):
        """
        Check if warning condition exists.
        
        Args:
            engine_temp: Engine temperature (°C)
        
        Returns:
            True if warning threshold exceeded, False otherwise
        """
        return engine_temp > THRESHOLD_ENGINE_OPTIMAL


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """
    Main application entry point.
    
    Initializes hardware and runs main control loop.
    """
    print("\n" + "="*60)
    print("ESP32 Climate-Smart Telemetry Controller")
    print("="*60)
    print("Architecture: Edge-Intelligence First")
    print("Fail-Safe: Active LOW relays + watchdog timer")
    print("="*60 + "\n")
    
    # ────────────────────────────────────────────────────────────
    # INITIALIZATION
    # ────────────────────────────────────────────────────────────
    
    print("Initializing hardware...")
    
    # Initialize hardware modules
    sensors = SensorManager(PIN_ENGINE_TEMP, PIN_FUEL_LINE_TEMP, PIN_AMBIENT_TEMP)
    relays = RelayController(PIN_RELAY_1, PIN_RELAY_2)
    leds = StatusLEDs(PIN_LED_STATUS, PIN_LED_WARNING, PIN_LED_ERROR, PIN_LED_ACTIVITY)
    
    # Initialize telemetry
    telemetry_builder = TelemetryBuilder()
    serial_writer = SerialWriter()
    
    # Initialize decision engine and safety monitor
    decision_engine = DecisionEngine()
    safety_monitor = SafetyMonitor()
    
    # Run LED startup sequence
    leds.startup_sequence()
    
    # Enable watchdog timer (5 second timeout)
    wdt = machine.WDT(timeout=5000)
    print("✓ Watchdog timer enabled (5s timeout)")
    
    print("\n" + "="*60)
    print("System initialized - entering main loop")
    print("="*60 + "\n")
    
    # Turn on status LED (system running)
    leds.set_status(True)
    
    # ────────────────────────────────────────────────────────────
    # MAIN CONTROL LOOP
    # ────────────────────────────────────────────────────────────
    
    last_sample_time = time.ticks_ms()
    last_telemetry_time = time.ticks_ms()
    
    while True:
        try:
            # Feed watchdog (prevent reset)
            wdt.feed()
            
            current_time = time.ticks_ms()
            
            # ────────────────────────────────────────────────────
            # SENSOR SAMPLING (every 2 seconds)
            # ────────────────────────────────────────────────────
            if time.ticks_diff(current_time, last_sample_time) >= SAMPLE_INTERVAL_MS:
                last_sample_time = current_time
                
                # Read all sensors
                temps = sensors.read_all()
                
                print(f"Temps: Engine={temps['engine']}°C, "
                      f"Fuel={temps['fuel_line']}°C, "
                      f"Ambient={temps['ambient']}°C")
                
                # ────────────────────────────────────────────────
                # SAFETY MONITORING (critical path)
                # ────────────────────────────────────────────────
                overheat = safety_monitor.check_overheat(
                    temps['engine'], 
                    temps['fuel_line']
                )
                
                warning = safety_monitor.check_warning(temps['engine'])
                
                if overheat:
                    # FAIL-SAFE ACTIVATION
                    print("⚠ FAIL-SAFE ACTIVATED: Overheat detected!")
                    relays.set_fail_safe()
                    leds.set_error(True)
                    system_status = "fail_safe"
                else:
                    leds.set_error(False)
                    system_status = "live_mode"
                
                # Update warning LED
                leds.set_warning(warning)
                
                # ────────────────────────────────────────────────
                # DECISION ENGINE (AI recommendation)
                # ────────────────────────────────────────────────
                ai_recommendation = decision_engine.compute_recommendation(
                    temps['engine'],
                    temps['fuel_line'],
                    overheat
                )
                
                print(f"AI Recommendation: {ai_recommendation}")
                
                # ────────────────────────────────────────────────
                # RELAY CONTROL (based on AI recommendation)
                # ────────────────────────────────────────────────
                if not overheat:
                    # Normal operation - apply AI recommendations
                    relay1_state = decision_engine.should_activate_cooling(temps['engine'])
                    relay2_state = decision_engine.should_switch_fuel(temps['fuel_line'])
                    
                    relays.set_both(relay1_state, relay2_state)
                    
                    print(f"Relays: R1={'ON' if relay1_state else 'OFF'}, "
                          f"R2={'ON' if relay2_state else 'OFF'}")
                
                # ────────────────────────────────────────────────
                # TELEMETRY TRANSMISSION (every 2 seconds)
                # ────────────────────────────────────────────────
                if time.ticks_diff(current_time, last_telemetry_time) >= TELEMETRY_INTERVAL_MS:
                    last_telemetry_time = current_time
                    
                    # Build telemetry message
                    message = telemetry_builder.build_message(
                        temps=temps,
                        ai_rec=ai_recommendation,
                        relay1=relays.get_relay_1(),
                        relay2=relays.get_relay_2(),
                        overheat=overheat,
                        system_status=system_status
                    )
                    
                    # Transmit via serial
                    serial_writer.write(message)
                    leds.blink_activity()
            
            # Small delay to prevent busy-waiting
            time.sleep_ms(100)
        
        except KeyboardInterrupt:
            print("\n\nShutdown requested by user")
            break
        
        except Exception as e:
            # Error handling - log and activate fail-safe
            print(f"\nERROR in main loop: {e}")
            relays.set_fail_safe()
            leds.set_error(True)
            time.sleep(1)  # Brief pause before retry
    
    # ────────────────────────────────────────────────────────────
    # SHUTDOWN
    # ────────────────────────────────────────────────────────────
    
    print("\nShutting down...")
    relays.set_fail_safe()
    leds.all_off()
    print("✓ System shutdown complete")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
