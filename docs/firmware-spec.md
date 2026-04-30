# Firmware Specification

## Overview

The ESP32 firmware is the edge intelligence layer that reads sensors, makes decisions, controls relays, and generates telemetry. All decision logic executes locally on the microcontroller for real-time response and offline operation.

## Hardware Platform

- **Microcontroller:** ESP32-S3
- **Language:** MicroPython
- **Sensors:** 3x DS18B20 (OneWire temperature sensors)
- **Actuators:** 2-channel relay module (Active LOW)
- **Indicators:** 4x LEDs (status, warning, error, activity)
- **Communication:** UART serial (115200 baud)

## Pin Configuration

```
Temperature Sensors (DS18B20 OneWire):
├── GPIO 4  → Engine temperature sensor
├── GPIO 5  → Fuel line temperature sensor
└── GPIO 6  → Ambient temperature sensor

Relay Control (Active LOW):
├── GPIO 7  → Relay 1 (Cooling System)
└── GPIO 8  → Relay 2 (Fuel Switching)

Status LEDs:
├── GPIO 9  → Status LED (Green - System running)
├── GPIO 10 → Warning LED (Yellow - High temperature)
├── GPIO 11 → Error LED (Red - Overheat/Fail-safe)
└── GPIO 12 → Activity LED (Blue - Telemetry transmission)

Serial Communication:
├── GPIO 43 → UART TX (USB Serial to host)
└── GPIO 44 → UART RX (USB Serial from host)
```

## Module Structure

```
firmware/micropython/
├── main.py            # Main control loop, decision engine
├── sensors.py         # DS18B20 temperature sensor drivers
├── relays.py          # Relay control with fail-safe
├── status_leds.py     # LED indicator management
└── telemetry.py       # JSON telemetry builder and serial writer
```

## Core Principles

### 1. Edge-Intelligence First
**All decision logic executes on ESP32:**
- Sensor reading and processing
- AI recommendation computation
- Relay control decisions
- Safety monitoring
- Fail-safe activation

**No cloud dependency:**
- Works offline
- Real-time response (< 1 second)
- No network latency
- Autonomous operation

### 2. Fail-Safe Design
**Hardware fail-safe:**
- Active LOW relays (OFF when GPIO HIGH)
- On power loss → GPIO floats HIGH → Relays OFF
- On crash → Relays OFF during reset

**Software fail-safe:**
- Watchdog timer (5-second timeout)
- Overheat detection triggers immediate fail-safe
- Exception handling with fail-safe fallback
- Sensor failure fallback to last valid reading

### 3. Deterministic AI
**Rule-based decision logic:**
- Transparent thresholds
- Explainable recommendations
- No black-box machine learning
- Auditable decision rules

## Main Control Loop

### Timing

```
Every 2 seconds:
├── Read all sensors (engine, fuel line, ambient)
├── Check safety thresholds
├── Compute AI recommendation
├── Update relay states
├── Generate telemetry JSON
└── Transmit via serial
```

### Loop Structure

```python
while True:
    # Feed watchdog (prevent reset)
    watchdog.feed()
    
    # Sensor sampling (every 2 seconds)
    if time_for_sample():
        temps = sensors.read_all()
        
        # Safety monitoring (critical path)
        overheat = check_overheat(temps)
        if overheat:
            relays.set_fail_safe()
            leds.set_error(True)
        
        # AI decision engine
        ai_rec = compute_recommendation(temps, overheat)
        
        # Relay control
        if not overheat:
            relay1 = should_activate_cooling(temps['engine'])
            relay2 = should_switch_fuel(temps['fuel_line'])
            relays.set_both(relay1, relay2)
        
        # Telemetry transmission
        message = build_telemetry(temps, ai_rec, relays, overheat)
        serial_writer.write(message)
        leds.blink_activity()
    
    time.sleep_ms(100)  # Small delay
```

## Decision Engine

### AI Recommendation Logic

```python
def compute_recommendation(engine_temp, fuel_line_temp, overheat):
    # Priority 1: Safety (highest priority)
    if overheat:
        return "activate_cooling"
    
    # Priority 2: Overheat prevention
    if engine_temp > 95:
        return "reduce_load"
    
    # Priority 3: Fuel optimization
    if engine_temp < 80:
        return "switch_to_biodiesel"
    
    if engine_temp > 90:
        return "switch_to_diesel"
    
    # Priority 4: Maintain current state
    return "maintain"
```

### Relay Control Logic

```python
def should_activate_cooling(engine_temp):
    # Relay 1: Cooling system
    return engine_temp > 90  # Activate above 90°C

def should_switch_fuel(fuel_line_temp):
    # Relay 2: Fuel switching
    return fuel_line_temp > 80  # Switch above 80°C
```

### Safety Thresholds

```python
# Configurable thresholds (edit in main.py)
THRESHOLD_ENGINE_OVERHEAT = 100.0   # °C - Fail-safe activation
THRESHOLD_FUEL_LINE_MAX = 90.0      # °C - Fail-safe activation
THRESHOLD_ENGINE_OPTIMAL = 80.0     # °C - Warning threshold
THRESHOLD_COOLING_ACTIVATE = 90.0   # °C - Relay 1 activation
THRESHOLD_FUEL_SWITCH = 80.0        # °C - Relay 2 activation
```

## Sensor Management

### DS18B20 Temperature Sensors

**Reading process:**
1. Start temperature conversion
2. Wait 750ms (12-bit resolution)
3. Read temperature from device
4. Validate reading (-55°C to 125°C)
5. Cache last valid reading

**Error handling:**
- Sensor not found → Use last valid reading
- Invalid reading → Use last valid reading
- Timeout → Use last valid reading
- Log warnings for debugging

**Fallback strategy:**
- Each sensor maintains last valid reading
- On error, use cached value
- Prevents system failure from sensor issues
- Allows operation with degraded sensors

## Relay Control

### Active LOW Configuration

```python
# Active LOW: GPIO HIGH = Relay OFF (safe state)
relay.value(1)  # Relay OFF
relay.value(0)  # Relay ON
```

**Fail-safe behavior:**
- Power loss → GPIO floats HIGH → Relay OFF
- Crash → GPIO resets HIGH → Relay OFF
- Explicit fail-safe → Set GPIO HIGH → Relay OFF

### Relay States

```python
# Relay 1: Cooling System
# ON when engine temperature > 90°C
# OFF otherwise

# Relay 2: Fuel Switching
# ON when fuel line temperature > 80°C
# OFF otherwise

# Fail-safe: Both relays OFF
# Activated when overheat detected
```

## LED Indicators

### LED Meanings

- **Green (Status):** System running normally
- **Yellow (Warning):** Temperature above optimal threshold
- **Red (Error):** Overheat detected, fail-safe active
- **Blue (Activity):** Blinks on telemetry transmission

### LED Patterns

```python
# Normal operation
status_led.on()
warning_led.off()
error_led.off()

# High temperature warning
status_led.on()
warning_led.on()
error_led.off()

# Overheat / fail-safe
status_led.on()
warning_led.on()
error_led.on()

# Telemetry transmission
activity_led.on()
time.sleep_ms(50)
activity_led.off()
```

## Telemetry Generation

### JSON Format

```json
{
  "timestamp": "1970-01-01T00:00:05.000Z",
  "engine_temperature": 85.3,
  "fuel_line_temperature": 62.1,
  "ambient_temperature": 28.5,
  "current_fuel_mode": "diesel",
  "ai_recommendation": "maintain",
  "relay_state_1": false,
  "relay_state_2": false,
  "overheat_flag": false,
  "system_status": "live_mode",
  "network_status": "disconnected",
  "power_source": "battery"
}
```

### Serial Transmission

- **Format:** Newline-delimited JSON
- **Baud rate:** 115200
- **Interval:** Every 2 seconds
- **Framing:** Each message ends with `\n`

### Timestamp Generation

```python
# Simple uptime-based timestamp (v1)
uptime_sec = (time.ticks_ms() - boot_time) // 1000
timestamp = f"1970-01-01T00:{uptime_sec // 60:02d}:{uptime_sec % 60:02d}.000Z"

# Future: Sync with NTP for accurate timestamps
```

## Watchdog Timer

### Purpose
Automatically reset system if main loop hangs or crashes

### Configuration
```python
wdt = machine.WDT(timeout=5000)  # 5-second timeout
```

### Usage
```python
while True:
    wdt.feed()  # Reset watchdog timer
    # ... main loop logic ...
```

### Behavior
- If `wdt.feed()` not called within 5 seconds → System resets
- On reset → Firmware restarts from beginning
- Relays default to fail-safe state during reset

## Fail-Safe Activation

### Triggers
- Engine temperature > 100°C
- Fuel line temperature > 90°C
- System error or exception
- Watchdog timeout (automatic reset)

### Actions
1. Set both relays to OFF (GPIO HIGH)
2. Turn on error LED (red)
3. Set `system_status` to "fail_safe"
4. Set `overheat_flag` to true
5. Log fail-safe event
6. Continue telemetry transmission

### Recovery
- Automatic recovery when temperatures drop below thresholds
- Hysteresis: Require 5°C drop below threshold
- Resume normal operation
- Log recovery event

## Configuration

### Editable Constants (main.py)

```python
# Pin assignments
PIN_ENGINE_TEMP = 4
PIN_FUEL_LINE_TEMP = 5
PIN_AMBIENT_TEMP = 6
PIN_RELAY_1 = 7
PIN_RELAY_2 = 8
PIN_LED_STATUS = 9
PIN_LED_WARNING = 10
PIN_LED_ERROR = 11
PIN_LED_ACTIVITY = 12

# Safety thresholds (°C)
THRESHOLD_ENGINE_OVERHEAT = 100.0
THRESHOLD_FUEL_LINE_MAX = 90.0
THRESHOLD_ENGINE_OPTIMAL = 80.0
THRESHOLD_COOLING_ACTIVATE = 90.0
THRESHOLD_FUEL_SWITCH = 80.0

# Timing (milliseconds)
SAMPLE_INTERVAL_MS = 2000
TELEMETRY_INTERVAL_MS = 2000
```

## Installation

### 1. Flash MicroPython
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 firmware.bin
```

### 2. Upload Firmware Files
```bash
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 put sensors.py
ampy --port /dev/ttyUSB0 put relays.py
ampy --port /dev/ttyUSB0 put status_leds.py
ampy --port /dev/ttyUSB0 put telemetry.py
```

### 3. Reset ESP32
Firmware starts automatically on boot

## Testing

### Individual Module Testing
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

### Serial Console Monitoring
```bash
screen /dev/ttyUSB0 115200
# Watch telemetry JSON output
```

## Performance Characteristics

- **Sensor read time:** ~750ms per sensor (DS18B20 conversion)
- **Decision latency:** < 50ms (simple rule-based logic)
- **Relay switching:** < 5ms (GPIO write)
- **Telemetry generation:** < 100ms (JSON serialization)
- **Total cycle time:** ~2 seconds (configurable)
- **Fail-safe activation:** < 100ms (critical safety requirement)

## Memory Usage

- **MicroPython runtime:** ~30 KB
- **Application code:** ~20 KB
- **Total RAM usage:** < 100 KB
- **Flash usage:** < 500 KB

## Power Consumption

- **Active (all sensors + relays):** ~200 mA @ 3.3V
- **Idle (no relays):** ~100 mA @ 3.3V
- **Sleep mode:** Not implemented in v1 (future enhancement)

## Future Enhancements

- **NTP time sync:** Accurate timestamps
- **SD card logging:** Local telemetry storage
- **WiFi connectivity:** Direct cloud upload
- **OTA updates:** Remote firmware updates
- **Power management:** Sleep modes for battery operation
- **Additional sensors:** Pressure, humidity, vibration
- **CAN bus:** Vehicle integration
