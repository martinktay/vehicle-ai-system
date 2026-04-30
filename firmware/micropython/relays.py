"""
Relay Control Module

Hardware: 2-channel relay module
Purpose: Control cooling system and fuel switching

Architecture: Actuator layer
Fail-Safe: Active LOW configuration (relays OFF when GPIO HIGH)
"""

from machine import Pin


class RelayController:
    """
    Controls 2-channel relay module with fail-safe behavior.
    
    Fail-Safe Design:
    - Active LOW: GPIO HIGH = Relay OFF (safe state)
    - On power loss: GPIO floats HIGH → Relays OFF
    - On crash: Relays default to OFF during reset
    """
    
    def __init__(self, relay1_pin, relay2_pin):
        """
        Initialize relay controller.
        
        Args:
            relay1_pin: GPIO pin for Relay 1 (Cooling System)
            relay2_pin: GPIO pin for Relay 2 (Fuel Switching)
        """
        print("Initializing relay controller...")
        
        # Initialize relay pins as outputs
        self.relay1 = Pin(relay1_pin, Pin.OUT)
        self.relay2 = Pin(relay2_pin, Pin.OUT)
        
        # Set fail-safe state (both OFF)
        self.set_fail_safe()
        
        print(f"✓ Relay 1 (Cooling) on pin {relay1_pin}")
        print(f"✓ Relay 2 (Fuel Switch) on pin {relay2_pin}")
        print("✓ Relays initialized in fail-safe state (OFF)")
    
    def set_relay_1(self, state):
        """
        Set Relay 1 state (Cooling System).
        
        Args:
            state: True = ON, False = OFF
        """
        # Active LOW: Write inverse of desired state
        self.relay1.value(0 if state else 1)
    
    def set_relay_2(self, state):
        """
        Set Relay 2 state (Fuel Switching).
        
        Args:
            state: True = ON, False = OFF
        """
        # Active LOW: Write inverse of desired state
        self.relay2.value(0 if state else 1)
    
    def get_relay_1(self):
        """
        Get Relay 1 current state.
        
        Returns:
            True if ON, False if OFF
        """
        # Active LOW: Invert reading
        return self.relay1.value() == 0
    
    def get_relay_2(self):
        """
        Get Relay 2 current state.
        
        Returns:
            True if ON, False if OFF
        """
        # Active LOW: Invert reading
        return self.relay2.value() == 0
    
    def set_fail_safe(self):
        """
        Activate fail-safe state (both relays OFF).
        
        Called on:
        - Initialization
        - Overheat detection
        - System error
        """
        self.set_relay_1(False)
        self.set_relay_2(False)
        print("⚠ FAIL-SAFE: All relays OFF")
    
    def set_both(self, relay1_state, relay2_state):
        """
        Set both relays simultaneously.
        
        Args:
            relay1_state: True = ON, False = OFF
            relay2_state: True = ON, False = OFF
        """
        self.set_relay_1(relay1_state)
        self.set_relay_2(relay2_state)
