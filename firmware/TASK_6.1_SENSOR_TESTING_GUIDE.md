# Task 6.1: Sensor Testing Guide

## Hardware Requirements

- **ESP32-S3** microcontroller
- **3x DS18B20** temperature sensors (OneWire)
- **USB cable** for serial communication
- **Breadboard and jumper wires** (optional, for prototyping)
- **4.7kΩ resistor** (pull-up resistor for OneWire bus)

## Pin Configuration

Before uploading, verify these pin assignments in `firmware/micropython/main.py`:

```python
PIN_ENGINE_TEMP = 4      # Engine temperature sensor
PIN_FUEL_LINE_TEMP = 5   # Fuel line temperature sensor
PIN_AMBIENT_TEMP = 6     # Ambient temperature sensor
```

**⚠️ IMPORTANT:** Adjust these pin numbers to match your actual hardware connections!

## DS18B20 Wiring

Each DS18B20 sensor has 3 pins:
- **VCC** (Red) → 3.3V on ESP32
- **GND** (Black) → GND on ESP32
- **Data** (Yellow) → GPIO pin (4, 5, or 6)

**Pull-up Resistor:** Connect a 4.7kΩ resistor between VCC and Data line for each sensor.

```
ESP32-S3                DS18B20 Sensors
┌─────────┐            ┌──────────────┐
│         │            │   Engine     │
│  3.3V   ├────────────┤ VCC          │
│         │     ┌──────┤ Data         │
│  GPIO4  ├─────┤      │ GND          │
│         │     │      └──────────────┘
│  GND    ├─────┼──────────────────────┐
│         │     │                       │
│  GPIO5  ├─────┼──┐   ┌──────────────┐│
│         │     │  └───┤ Data         ││
│  GPIO6  ├─────┼──┐   │ Fuel Line    ││
│         │     │  │   │ VCC          ││
└─────────┘     │  │   │ GND          ││
                │  │   └──────────────┘│
                │  │                    │
                │  │   ┌──────────────┐│
                │  └───┤ Data         ││
                │      │ Ambient      ││
                │      │ VCC          ││
                │      │ GND          ││
                │      └──────────────┘│
                │                       │
                └───────────────────────┘
```

## Step 1: Flash MicroPython to ESP32

If MicroPython is not already installed:

```bash
# Install esptool if not already installed
pip install esptool

# Erase flash (optional, but recommended for clean install)
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash

# Flash MicroPython firmware
# Download from: https://micropython.org/download/esp32s3/
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 esp32s3-firmware.bin
```

**Windows users:** Replace `/dev/ttyUSB0` with `COM3` (or appropriate COM port)

## Step 2: Upload Firmware Files

```bash
# Install ampy if not already installed
pip install adafruit-ampy

# Upload all firmware files
cd firmware/micropython
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 put sensors.py
ampy --port /dev/ttyUSB0 put relays.py
ampy --port /dev/ttyUSB0 put status_leds.py
ampy --port /dev/ttyUSB0 put telemetry.py
```

## Step 3: Connect to Serial Monitor

### Option A: Using screen (Linux/Mac)

```bash
screen /dev/ttyUSB0 115200
```

To exit screen: Press `Ctrl+A`, then `K`, then `Y`

### Option B: Using minicom (Linux)

```bash
minicom -D /dev/ttyUSB0 -b 115200
```

To exit minicom: Press `Ctrl+A`, then `X`

### Option C: Using PuTTY (Windows)

1. Open PuTTY
2. Select "Serial" connection type
3. Enter COM port (e.g., COM3)
4. Set speed to 115200
5. Click "Open"

### Option D: Using Python script (Cross-platform)

```bash
python -m serial.tools.miniterm /dev/ttyUSB0 115200
```

To exit: Press `Ctrl+]`

## Step 4: Reset ESP32 and Observe Output

Press the **RESET** button on the ESP32 or power cycle it.

### Expected Output

You should see output similar to:

```
============================================================
ESP32 Climate-Smart Telemetry Controller
============================================================
Architecture: Edge-Intelligence First
Fail-Safe: Active LOW relays + watchdog timer
============================================================

Initializing hardware...
Initializing temperature sensors...
✓ Engine Temp initialized on pin 4
✓ Fuel Line Temp initialized on pin 5
✓ Ambient Temp initialized on pin 6
✓ All sensors initialized
✓ Watchdog timer enabled (5s timeout)

============================================================
System initialized - entering main loop
============================================================

Temps: Engine=25.3°C, Fuel=24.8°C, Ambient=23.5°C
AI Recommendation: maintain
Relays: R1=OFF, R2=OFF
{"timestamp":"1970-01-01T00:00:02.000Z","engine_temperature":25.3,...}

Temps: Engine=25.4°C, Fuel=24.9°C, Ambient=23.5°C
AI Recommendation: maintain
Relays: R1=OFF, R2=OFF
{"timestamp":"1970-01-01T00:00:04.000Z","engine_temperature":25.4,...}
```

### Troubleshooting

#### No sensor readings / "WARNING: No DS18B20 found"

**Possible causes:**
1. Sensor not connected properly
2. Missing pull-up resistor (4.7kΩ)
3. Wrong GPIO pin number in code
4. Faulty sensor

**Solutions:**
- Check wiring: VCC to 3.3V, GND to GND, Data to GPIO
- Verify pull-up resistor is connected between VCC and Data
- Double-check pin numbers in `main.py` match your wiring
- Test sensor with a multimeter (should show ~5kΩ resistance between VCC and Data with pull-up)

#### Sensor readings are incorrect

**Possible causes:**
1. Sensor is reading ambient temperature (not connected to heat source)
2. Sensor is damaged
3. Electrical noise on OneWire bus

**Solutions:**
- Touch the sensor with your finger - temperature should increase to ~30-35°C
- Try a different sensor
- Shorten wire length between ESP32 and sensor
- Add a 100nF capacitor between VCC and GND near the sensor

#### System resets frequently

**Possible causes:**
1. Watchdog timeout (main loop hanging)
2. Power supply insufficient
3. Sensor read timeout

**Solutions:**
- Check power supply can provide at least 500mA
- Use a powered USB hub
- Check serial output for error messages before reset

## Step 5: Verify Temperature Readings

### Test 1: Ambient Temperature

All three sensors should read approximately the same temperature (room temperature, typically 20-25°C).

**Expected range:** 15-45°C (as per design spec)

### Test 2: Heat Response

1. Touch one sensor with your finger
2. Temperature should increase to 30-35°C within 5-10 seconds
3. Release sensor
4. Temperature should decrease back to ambient within 30-60 seconds

### Test 3: Sensor Identification

To verify which sensor is which:

1. Heat the sensor connected to GPIO 4 (engine temp)
   - Watch serial output: `Engine=XX.X°C` should increase
2. Heat the sensor connected to GPIO 5 (fuel line temp)
   - Watch serial output: `Fuel=XX.X°C` should increase
3. Heat the sensor connected to GPIO 6 (ambient temp)
   - Watch serial output: `Ambient=XX.X°C` should increase

### Test 4: Telemetry JSON Output

Verify JSON telemetry is being output every 2 seconds:

```json
{
  "timestamp": "1970-01-01T00:00:10.000Z",
  "engine_temperature": 25.3,
  "fuel_line_temperature": 24.8,
  "ambient_temperature": 23.5,
  "current_fuel_mode": "diesel",
  "ai_recommendation": "maintain",
  "relay_state_1": false,
  "relay_state_2": false,
  "overheat_flag": false,
  "system_status": "live_mode",
  "network_status": "disconnected",
  "power_source": "usb"
}
```

**Verify:**
- All fields are present
- Temperature values are numbers (not null)
- Timestamp is in ISO 8601 format
- Boolean fields are true/false (not strings)

## Step 6: Test Temperature Ranges

### Normal Operation Range

**Expected values at room temperature:**
- Engine: 20-30°C
- Fuel Line: 20-30°C
- Ambient: 20-30°C

### Simulated Operating Range

To test the full range without actual engine hardware:

1. **Cold test:** Place sensor in ice water
   - Expected: 0-5°C
   - Verify sensor reads correctly

2. **Warm test:** Place sensor in warm water (NOT boiling!)
   - Expected: 40-60°C
   - Verify sensor reads correctly

3. **Hot test:** Place sensor in hot water (be careful!)
   - Expected: 70-90°C
   - Verify sensor reads correctly
   - **DO NOT exceed 100°C** - sensor max is 125°C

### Design Spec Ranges

According to `design.md`, the expected ranges are:
- Engine: 60-120°C (operating range)
- Fuel Line: 40-100°C (operating range)
- Ambient: 15-45°C (environmental range)

**Note:** At room temperature, sensors will read below these ranges. This is normal for testing without actual engine hardware.

## Step 7: Verify AI Recommendations

The firmware should generate AI recommendations based on temperature:

### Test Scenarios

1. **Normal operation (all temps < 80°C):**
   - Expected: `ai_recommendation: "maintain"`
   - Relays: Both OFF

2. **High engine temp (> 90°C):**
   - Expected: `ai_recommendation: "activate_cooling"` or `"reduce_load"`
   - Relay 1: Should turn ON (cooling)

3. **High fuel line temp (> 80°C):**
   - Expected: `ai_recommendation: "switch_to_diesel"`
   - Relay 2: Should turn ON (fuel switch)

4. **Overheat (engine > 100°C or fuel line > 90°C):**
   - Expected: `ai_recommendation: "activate_cooling"`
   - Expected: `overheat_flag: true`
   - Expected: `system_status: "fail_safe"`
   - Both relays: Should turn OFF (fail-safe)

**Note:** To test these scenarios without actual engine hardware, you can temporarily modify the thresholds in `main.py` to lower values (e.g., 30°C, 40°C) and use warm water to trigger the conditions.

## Success Criteria

Task 6.1 is complete when:

- ✅ All three DS18B20 sensors are detected on startup
- ✅ Temperature readings are displayed every 2 seconds
- ✅ Readings are within expected ranges (15-45°C for ambient testing)
- ✅ Sensors respond to temperature changes (finger test)
- ✅ JSON telemetry is output correctly every 2 seconds
- ✅ All telemetry fields are present and valid
- ✅ AI recommendations are generated based on temperature
- ✅ No sensor read errors or warnings

## Next Steps

After completing Task 6.1, proceed to:
- **Task 6.2:** Test relay control
- **Task 6.3:** Test fail-safe behavior
- **Task 6.4:** Test watchdog timer

## Troubleshooting Reference

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| No sensor found | Wiring issue | Check VCC, GND, Data connections |
| No sensor found | Missing pull-up | Add 4.7kΩ resistor between VCC and Data |
| No sensor found | Wrong pin | Verify pin numbers in `main.py` |
| Reading always 85°C | Sensor not responding | Check wiring, try different sensor |
| Reading always 0°C | Sensor damaged | Replace sensor |
| Frequent resets | Power issue | Use powered USB hub |
| Frequent resets | Watchdog timeout | Check for errors in serial output |
| No JSON output | Code not running | Press RESET button, check serial connection |
| Garbled output | Wrong baud rate | Set serial monitor to 115200 baud |

## Additional Resources

- **MicroPython DS18X20 docs:** https://docs.micropython.org/en/latest/esp32/quickref.html#onewire-driver
- **DS18B20 datasheet:** https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf
- **ESP32-S3 pinout:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html
