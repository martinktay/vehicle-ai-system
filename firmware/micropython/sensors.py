"""
Temperature Sensor Module

Hardware: DS18B20 OneWire temperature sensors
Purpose: Read temperature from engine, fuel line, and ambient sensors

Architecture: Sensor layer
Edge-Intelligence: Sensor readings feed decision logic on ESP32
"""

import time
import onewire
import ds18x20
from machine import Pin


class TemperatureSensor:
    """
    DS18B20 temperature sensor wrapper.
    
    Provides:
    - OneWire communication
    - Temperature reading in Celsius
    - Error handling and fallback
    """
    
    def __init__(self, pin_number, name="Sensor"):
        """
        Initialize DS18B20 sensor.
        
        Args:
            pin_number: GPIO pin number for OneWire data
            name: Human-readable sensor name for logging
        """
        self.name = name
        self.pin = Pin(pin_number)
        self.ow = onewire.OneWire(self.pin)
        self.ds = ds18x20.DS18X20(self.ow)
        
        # Scan for devices
        self.devices = self.ds.scan()
        
        if not self.devices:
            print(f"WARNING: No DS18B20 found on pin {pin_number} ({name})")
        else:
            print(f"✓ {name} initialized on pin {pin_number}")
        
        # Cache last valid reading for fallback
        self.last_valid_temp = 25.0  # Default fallback temperature
    
    def read_temperature(self):
        """
        Read temperature from sensor.
        
        Returns:
            Temperature in Celsius (float)
            Falls back to last valid reading on error
        """
        if not self.devices:
            print(f"WARNING: {self.name} not connected, using fallback")
            return self.last_valid_temp
        
        try:
            # Start temperature conversion
            self.ds.convert_temp()
            
            # Wait for conversion (750ms for 12-bit resolution)
            time.sleep_ms(750)
            
            # Read temperature from first device
            temp = self.ds.read_temp(self.devices[0])
            
            # Validate reading
            if temp is not None and -55 <= temp <= 125:
                self.last_valid_temp = temp
                return round(temp, 1)
            else:
                print(f"WARNING: {self.name} invalid reading: {temp}")
                return self.last_valid_temp
        
        except Exception as e:
            print(f"ERROR: {self.name} read failed: {e}")
            return self.last_valid_temp


class SensorManager:
    """
    Manages all temperature sensors.
    
    Provides unified interface for reading all sensors.
    """
    
    def __init__(self, engine_pin, fuel_line_pin, ambient_pin):
        """
        Initialize all temperature sensors.
        
        Args:
            engine_pin: GPIO pin for engine temperature sensor
            fuel_line_pin: GPIO pin for fuel line temperature sensor
            ambient_pin: GPIO pin for ambient temperature sensor
        """
        print("Initializing temperature sensors...")
        
        self.engine_sensor = TemperatureSensor(engine_pin, "Engine Temp")
        self.fuel_line_sensor = TemperatureSensor(fuel_line_pin, "Fuel Line Temp")
        self.ambient_sensor = TemperatureSensor(ambient_pin, "Ambient Temp")
        
        print("✓ All sensors initialized")
    
    def read_all(self):
        """
        Read all temperature sensors.
        
        Returns:
            Dictionary with temperature readings:
            {
                'engine': float,
                'fuel_line': float,
                'ambient': float
            }
        """
        return {
            'engine': self.engine_sensor.read_temperature(),
            'fuel_line': self.fuel_line_sensor.read_temperature(),
            'ambient': self.ambient_sensor.read_temperature()
        }
