"""
Status LED Module

Hardware: 4 indicator LEDs
Purpose: Visual feedback for system status

LEDs:
- Status (Green): System running normally
- Warning (Yellow): High temperature warning
- Error (Red): Overheat / fail-safe active
- Activity (Blue): Telemetry transmission
"""

from machine import Pin
import time


class StatusLEDs:
    """
    Controls status indicator LEDs.
    
    Provides visual feedback for:
    - System status (running, error)
    - Temperature warnings
    - Telemetry activity
    """
    
    def __init__(self, status_pin, warning_pin, error_pin, activity_pin):
        """
        Initialize status LEDs.
        
        Args:
            status_pin: GPIO pin for status LED (green)
            warning_pin: GPIO pin for warning LED (yellow)
            error_pin: GPIO pin for error LED (red)
            activity_pin: GPIO pin for activity LED (blue)
        """
        print("Initializing status LEDs...")
        
        self.status_led = Pin(status_pin, Pin.OUT)
        self.warning_led = Pin(warning_pin, Pin.OUT)
        self.error_led = Pin(error_pin, Pin.OUT)
        self.activity_led = Pin(activity_pin, Pin.OUT)
        
        # Turn all LEDs off initially
        self.all_off()
        
        print(f"✓ Status LED (green) on pin {status_pin}")
        print(f"✓ Warning LED (yellow) on pin {warning_pin}")
        print(f"✓ Error LED (red) on pin {error_pin}")
        print(f"✓ Activity LED (blue) on pin {activity_pin}")
    
    def all_off(self):
        """Turn all LEDs off."""
        self.status_led.off()
        self.warning_led.off()
        self.error_led.off()
        self.activity_led.off()
    
    def set_status(self, state):
        """
        Set status LED (green).
        
        Args:
            state: True = ON, False = OFF
        """
        self.status_led.value(1 if state else 0)
    
    def set_warning(self, state):
        """
        Set warning LED (yellow).
        
        Args:
            state: True = ON, False = OFF
        """
        self.warning_led.value(1 if state else 0)
    
    def set_error(self, state):
        """
        Set error LED (red).
        
        Args:
            state: True = ON, False = OFF
        """
        self.error_led.value(1 if state else 0)
    
    def blink_activity(self):
        """
        Blink activity LED (blue) briefly.
        
        Non-blocking: Quick pulse to indicate telemetry transmission.
        """
        self.activity_led.on()
        time.sleep_ms(50)
        self.activity_led.off()
    
    def startup_sequence(self):
        """
        Run LED startup sequence (visual test).
        
        Blinks all LEDs in sequence to verify functionality.
        """
        print("Running LED startup sequence...")
        
        leds = [
            (self.status_led, "Status"),
            (self.warning_led, "Warning"),
            (self.error_led, "Error"),
            (self.activity_led, "Activity")
        ]
        
        for led, name in leds:
            led.on()
            print(f"  {name} LED: ON")
            time.sleep_ms(200)
            led.off()
        
        print("✓ LED test complete")
