# ESP32 MicroPython Firmware

Climate-Smart Telemetry Controller firmware for ESP32-S3.

## Hardware Requirements

- **ESP32-S3** microcontroller
- **3x DS18B20** temperature sensors (OneWire)
- **2-channel relay module** (Active LOW)
- **4x LEDs** with current-limiting resistors
- **USB cable** for serial communication

## Pin Configuration

**⚠️ IMPORTANT: Edit pin numbers in `main.py` to match your hardware!**

```python
# Temperature Sensors (DS18B20 OneWire)
PIN_ENGINE_TEMP = 4      # Engine temperature sensor
PIN_FUEL_LINE_TEMP = 5   # Fuel line temperature sensor
PIN_AMBIENT_TEMP = 6     # Ambient temperature sensor

# Relay Control (Active LOW)
PIN_RELAY_1 = 7          # Relay 1: Cooling system
PIN_RELAY_2 = 8          # Relay 2: Fuel switching

# Status LEDs
PIN_LED_STATUS = 9       # Green: System running
PIN_LED_WARNING = 10     # Yellow: High temperature
PIN_LED_ERROR = 11       # Red: Overheat / fail-safe
PIN_LED_ACTIVITY = 12    # Blue: Telemetry transmission
```

## Safety Thresholds

Edit these values in `main.py` to match your system requirements:

```python
THRESHOLD_ENGINE_OVERHEAT = 100.0   # °C - Fail-safe activation
THRESHOLD_FUEL_LINE_MAX = 90.0      # °C - Fail-safe activation
THRESHOLD_ENGINE_OPTIMAL = 80.0     # °C - Warning threshold
THRESHOLD_COOLING_ACTIVATE = 90.0   # °C - Relay 1 activation
THRESHOLD_FUEL_SWITCH = 80.0        # °C - Relay 2 activation
```

## Installation

### 1. Flash MicroPython to ESP32

```bash
# Download MicroPython firmware for ESP32-S3
# https://micropython.org/download/esp32s3/

# Erase flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash

# Flash MicroPython
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 esp32s3-firmware.bin
```

### 2. Upload Firmware Files

```bash
# Using ampy (install: pip install adafruit-ampy)
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 put sensors.py
ampy --port /dev/ttyUSB0 put relays.py
ampy --port /dev/ttyUSB0 put status_leds.py
ampy --port /dev/ttyUSB0 put telemetry.py
```

### 3. Connect to Serial Console

```bash
# Using screen
screen /dev/ttyUSB0 115200

# Or using minicom
minicom -D /dev/ttyUSB0 -b 115200
```

## Running the Firmware

The firmware starts automatically on boot. To manually run:

```python
import main
main.main()
```

## Architecture

### Edge-Intelligence First
- All decision logic executes on ESP32
- Bridge service only forwards telemetry
- Dashboard only displays data

### Fail-Safe Design
- **Hardware:** Active LOW relays (OFF when GPIO HIGH)
- **Software:** Watchdog timer (5s timeout)
- **Safety:** Overheat detection triggers fail-safe

### Module Structure

```
main.py           - Main control loop, decision engine
sensors.py        - DS18B20 temperature sensor drivers
relays.py         - Relay control with fail-safe
status_leds.py    - LED indicator management
telemetry.py      - JSON telemetry builder and serial writer
```

## Telemetry Output

The firmware outputs newline-delimited JSON via serial (115200 baud):

```json
{"timestamp":"1970-01-01T00:00:05.000Z","engine_temperature":85.3,...}\n
```

This telemetry is consumed by the Python bridge service.

## LED Indicators

- **Green (Status):** System running normally
- **Yellow (Warning):** Temperature above optimal threshold
- **Red (Error):** Overheat detected, fail-safe active
- **Blue (Activity):** Blinks on telemetry transmission

## Troubleshooting

### No sensor readings
- Check DS18B20 wiring (VCC, GND, Data)
- Verify OneWire pin connections
- Check serial console for "No DS18B20 found" warnings

### Relays not switching
- Verify relay module is Active LOW
- Check relay pin connections
- Test with multimeter (GPIO HIGH = Relay OFF)

### No telemetry output
- Check USB serial connection
- Verify baud rate (115200)
- Look for JSON output in serial console

### System resets frequently
- Watchdog timeout (5s) - main loop may be hanging
- Check for sensor read timeouts
- Verify power supply is stable

## Development

### Testing Individual Modules

```python
# Test sensors
from sensors import SensorManager
sensors = SensorManager(4, 5, 6)
print(sensors.read_all())

# Test relays
from relays import RelayController
relays = RelayController(7, 8)
relays.set_relay_1(True)  # Turn on
relays.set_relay_1(False) # Turn off

# Test LEDs
from status_leds import StatusLEDs
leds = StatusLEDs(9, 10, 11, 12)
leds.startup_sequence()
```

## Safety Notes

⚠️ **CRITICAL SAFETY INFORMATION:**

1. **Fail-Safe State:** Both relays OFF (GPIO HIGH)
2. **Overheat Thresholds:** Adjust for your specific application
3. **Watchdog Timer:** System auto-resets if main loop hangs
4. **Power Loss:** Relays default to OFF (safe state)
5. **Testing:** Always test fail-safe behavior before deployment

## License

Part of the Climate-Smart Telemetry Platform.
