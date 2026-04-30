# Hardware Wiring Diagram

**ESP32 Climate-Smart Telemetry Controller**  
**Last Updated**: 2026-04-06

---

## Component List

### Required Components

1. **ESP32-S3 Development Board** (1x)
   - USB-C cable for programming and power
   - Built-in USB-to-Serial converter

2. **DS18B20 Temperature Sensors** (3x)
   - Waterproof version recommended
   - Operating range: -55°C to +125°C
   - Accuracy: ±0.5°C

3. **2-Channel Relay Module** (1x)
   - Active LOW trigger
   - 5V coil voltage
   - 10A/250VAC or 10A/30VDC contacts

4. **Status LEDs** (4x)
   - Green LED (status)
   - Yellow LED (warning)
   - Red LED (error)
   - Blue LED (activity)

5. **Resistors**
   - 4.7kΩ (1x) - DS18B20 pull-up
   - 220Ω-330Ω (4x) - LED current limiting

6. **Breadboard and Jumper Wires**
   - For prototyping
   - Or custom PCB for production

---

## Pin Assignments

| Component | GPIO Pin | Notes |
|-----------|----------|-------|
| Engine Temp Sensor | GPIO 4 | DS18B20 OneWire |
| Fuel Line Temp Sensor | GPIO 5 | DS18B20 OneWire |
| Ambient Temp Sensor | GPIO 6 | DS18B20 OneWire |
| Relay 1 (Cooling) | GPIO 7 | Active LOW |
| Relay 2 (Fuel Switch) | GPIO 8 | Active LOW |
| Status LED (Green) | GPIO 9 | Current-limited |
| Warning LED (Yellow) | GPIO 10 | Current-limited |
| Error LED (Red) | GPIO 11 | Current-limited |
| Activity LED (Blue) | GPIO 12 | Current-limited |

---

## Wiring Diagrams

### DS18B20 Temperature Sensors

```
DS18B20 Sensor Wiring (All 3 sensors):

         ESP32                    DS18B20
    ┌─────────────┐           ┌──────────┐
    │             │           │          │
    │     3.3V ───┼───────────┼─ VDD    │
    │             │           │          │
    │     GND  ───┼───────────┼─ GND    │
    │             │           │          │
    │     GPIO4───┼───────────┼─ DATA   │  (Engine sensor)
    │     GPIO5───┼───────────┼─ DATA   │  (Fuel line sensor)
    │     GPIO6───┼───────────┼─ DATA   │  (Ambient sensor)
    │             │           │          │
    └─────────────┘           └──────────┘
                │
                │  4.7kΩ Pull-up Resistor
                │  (between DATA and VDD)
                │
               ┌┴┐
               │ │ 4.7kΩ
               │ │
               └┬┘
                │
               3.3V

Note: Each sensor needs its own data line, but they share VDD and GND.
The 4.7kΩ pull-up resistor is required on each data line.
```

### 2-Channel Relay Module

```
Relay Module Wiring (Active LOW):

         ESP32                    Relay Module
    ┌─────────────┐           ┌──────────────┐
    │             │           │              │
    │     5V   ───┼───────────┼─ VCC        │
    │             │           │              │
    │     GND  ───┼───────────┼─ GND        │
    │             │           │              │
    │     GPIO7───┼───────────┼─ IN1 (R1)   │  Cooling system
    │             │           │              │
    │     GPIO8───┼───────────┼─ IN2 (R2)   │  Fuel switching
    │             │           │              │
    └─────────────┘           └──────────────┘

Active LOW Configuration:
- GPIO HIGH (3.3V) → Relay OFF
- GPIO LOW (0V)    → Relay ON

Relay Contacts (each relay):
- COM (Common)
- NO (Normally Open) - Closes when relay ON
- NC (Normally Closed) - Opens when relay ON

Fail-Safe Design:
- Default state (power off): GPIO HIGH → Relays OFF
- This ensures safe state during power loss
```

### Status LEDs

```
LED Wiring (All 4 LEDs):

         ESP32                    LED Circuit
    ┌─────────────┐           
    │             │           
    │     GPIO9───┼────┬──────┐
    │             │    │      │
    │     GPIO10──┼────┤      │
    │             │    │      │
    │     GPIO11──┼────┤      │
    │             │    │      │
    │     GPIO12──┼────┤      │
    │             │    │      │
    │     GND  ───┼────┼──────┼───┐
    │             │    │      │   │
    └─────────────┘    │      │   │
                       │      │   │
                      ┌┴┐    ┌┴┐  │
                      │ │    │ │  │
                      │ │R   │ │R │
                      └┬┘    └┬┘  │
                       │      │   │
                      ┌▼┐    ┌▼┐  │
                      │ │    │ │  │  (Repeat for all 4 LEDs)
                      │ │LED │ │LED
                      └┬┘    └┬┘  │
                       │      │   │
                       └──────┴───┘
                              │
                             GND

R = 220Ω - 330Ω (current limiting resistor)

LED Colors:
- GPIO 9  → Green LED  (Status: System running)
- GPIO 10 → Yellow LED (Warning: High temperature)
- GPIO 11 → Red LED    (Error: Fail-safe active)
- GPIO 12 → Blue LED   (Activity: Telemetry transmission)
```

---

## Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         ESP32-S3                                 │
│                                                                  │
│  GPIO 4 ──────────────────────── Engine Temp Sensor (DS18B20)  │
│  GPIO 5 ──────────────────────── Fuel Line Temp Sensor         │
│  GPIO 6 ──────────────────────── Ambient Temp Sensor           │
│                                                                  │
│  GPIO 7 ──────────────────────── Relay 1 (Cooling System)      │
│  GPIO 8 ──────────────────────── Relay 2 (Fuel Switching)      │
│                                                                  │
│  GPIO 9  ──────────────────────── Green LED (Status)           │
│  GPIO 10 ──────────────────────── Yellow LED (Warning)         │
│  GPIO 11 ──────────────────────── Red LED (Error)              │
│  GPIO 12 ──────────────────────── Blue LED (Activity)          │
│                                                                  │
│  USB-C ─────────────────────────── Computer (Serial + Power)   │
│                                                                  │
│  3.3V ──────────────────────────── Sensor Power                │
│  5V ────────────────────────────── Relay Module Power          │
│  GND ───────────────────────────── Common Ground               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Power Requirements

### ESP32
- **Input**: 5V via USB-C (500mA typical)
- **Output**: 3.3V for sensors (max 600mA)

### DS18B20 Sensors (3x)
- **Voltage**: 3.0V - 5.5V (using 3.3V from ESP32)
- **Current**: 1mA per sensor (3mA total)

### Relay Module
- **Voltage**: 5V (from ESP32 5V pin)
- **Current**: 70mA per relay (140mA total when both ON)

### LEDs (4x)
- **Voltage**: 2.0V - 3.3V (forward voltage)
- **Current**: 10-20mA per LED (80mA total max)

### Total Power Budget
- ESP32: 100mA
- Sensors: 3mA
- Relays: 140mA (worst case)
- LEDs: 80mA (worst case)
- **Total**: ~323mA (well within USB 500mA limit)

---

## Assembly Instructions

### Step 1: Prepare Components

1. **Test ESP32**:
   - Connect via USB
   - Verify it powers on
   - Check serial communication

2. **Test DS18B20 Sensors**:
   - Measure resistance: should be ~5kΩ
   - Check for shorts between pins

3. **Test Relay Module**:
   - Apply 5V to VCC/GND
   - Manually connect IN1/IN2 to GND
   - Verify relays click

4. **Test LEDs**:
   - Use multimeter diode test mode
   - Verify forward voltage ~2V

---

### Step 2: Breadboard Assembly

1. **Mount ESP32** on breadboard (center position)

2. **Connect Power Rails**:
   - ESP32 3.3V → Breadboard + rail (red)
   - ESP32 5V → Breadboard + rail (red, separate section)
   - ESP32 GND → Breadboard - rail (blue)

3. **Connect DS18B20 Sensors**:
   - Sensor 1 (Engine): VDD→3.3V, GND→GND, DATA→GPIO4
   - Sensor 2 (Fuel): VDD→3.3V, GND→GND, DATA→GPIO5
   - Sensor 3 (Ambient): VDD→3.3V, GND→GND, DATA→GPIO6
   - Add 4.7kΩ pull-up resistor on each DATA line (DATA to 3.3V)

4. **Connect Relay Module**:
   - VCC → 5V rail
   - GND → GND rail
   - IN1 → GPIO7
   - IN2 → GPIO8

5. **Connect LEDs** (with current-limiting resistors):
   - Green: GPIO9 → 220Ω → LED+ → LED- → GND
   - Yellow: GPIO10 → 220Ω → LED+ → LED- → GND
   - Red: GPIO11 → 220Ω → LED+ → LED- → GND
   - Blue: GPIO12 → 220Ω → LED+ → LED- → GND

---

### Step 3: Verification

1. **Visual Inspection**:
   - Check all connections
   - Verify no shorts between power rails
   - Confirm LED polarity (long leg = +)

2. **Continuity Test** (power OFF):
   - Test 3.3V rail to ESP32 3.3V pin
   - Test GND rail to ESP32 GND pin
   - Test each GPIO connection

3. **Power-On Test**:
   - Connect USB (no firmware yet)
   - Check 3.3V rail voltage (should be 3.3V ±0.1V)
   - Check 5V rail voltage (should be 5.0V ±0.2V)
   - Verify no components get hot

---

### Step 4: Firmware Upload

1. **Upload firmware** (see HARDWARE-READINESS-CHECKLIST.md)

2. **Monitor serial output**:
   ```bash
   screen /dev/ttyUSB0 115200
   ```

3. **Expected startup sequence**:
   - LEDs flash in sequence (green → yellow → red → blue)
   - Green LED stays ON (system running)
   - JSON telemetry messages every 2 seconds

---

## Testing Procedures

### Test 1: Temperature Sensors

**Objective**: Verify all 3 sensors are reading correctly

**Procedure**:
1. Monitor serial output
2. Note ambient temperature (should be room temp ~20-30°C)
3. Touch engine sensor with warm hand
4. Verify temperature increases
5. Repeat for fuel line and ambient sensors

**Pass Criteria**:
- All 3 sensors show reasonable values
- Sensors respond to temperature changes
- No -127°C or 85°C errors (indicates wiring issue)

---

### Test 2: Relay Control

**Objective**: Verify relays switch based on temperature

**Procedure**:
1. Heat engine sensor above 90°C (hot water or heat gun)
2. Listen for relay 1 click
3. Observe relay LED indicator
4. Cool sensor below 90°C
5. Verify relay 1 turns OFF

**Pass Criteria**:
- Relay 1 clicks ON when temp > 90°C
- Relay 1 clicks OFF when temp < 90°C
- Serial output shows relay state changes

---

### Test 3: Status LEDs

**Objective**: Verify all LEDs function correctly

**Procedure**:
1. Power on: Green LED should turn ON
2. Heat engine to 85°C: Yellow LED should turn ON
3. Heat engine to 100°C: Red LED should turn ON
4. Observe blue LED: Should blink every 2 seconds

**Pass Criteria**:
- Green LED ON during normal operation
- Yellow LED ON when temp > 80°C
- Red LED ON when temp > 100°C (fail-safe)
- Blue LED blinks with telemetry transmission

---

### Test 4: Fail-Safe Activation

**Objective**: Verify fail-safe activates on overheat

**Procedure**:
1. Heat engine sensor above 100°C
2. Observe both relays turn OFF
3. Observe red LED turn ON
4. Cool sensor below 100°C
5. Verify system recovers

**Pass Criteria**:
- Both relays turn OFF when temp > 100°C
- Red LED turns ON
- Serial output shows "fail_safe" status
- System recovers when temp drops

---

## Troubleshooting

### Issue: Sensor reads -127°C

**Cause**: Sensor not detected (wiring issue)

**Solutions**:
1. Check VDD and GND connections
2. Verify 4.7kΩ pull-up resistor on DATA line
3. Check DATA line connection to GPIO
4. Try different GPIO pin
5. Test sensor with multimeter (should show ~5kΩ)

---

### Issue: Sensor reads 85°C constantly

**Cause**: Sensor power issue or fake sensor

**Solutions**:
1. Check 3.3V power supply voltage
2. Verify sensor is genuine DS18B20 (not clone)
3. Try different sensor
4. Check for shorts on DATA line

---

### Issue: Relay doesn't click

**Cause**: Insufficient power or wrong trigger level

**Solutions**:
1. Verify relay module gets 5V (not 3.3V)
2. Check relay module is Active LOW type
3. Measure voltage on IN1/IN2 (should be 0V when ON)
4. Try manual trigger: connect IN1 to GND
5. Check relay module LED indicators

---

### Issue: LED doesn't light up

**Cause**: Wrong polarity or insufficient current

**Solutions**:
1. Check LED polarity (long leg = +)
2. Verify current-limiting resistor (220-330Ω)
3. Test LED with multimeter diode mode
4. Check GPIO connection
5. Try different LED

---

## Safety Warnings

⚠️ **IMPORTANT SAFETY NOTES**:

1. **Relay Contacts**: Do NOT connect high voltage (110V/220V AC) during testing. Use low voltage (12V DC) or LED indicators only.

2. **Temperature Sensors**: DS18B20 sensors can handle up to 125°C, but be careful with heat sources. Use hot water (80-90°C) for safe testing.

3. **Power Supply**: Do not exceed 5V on ESP32 5V pin. USB provides sufficient power for this project.

4. **Relay Module**: Ensure relay module is rated for your intended load (10A typical). Add fuses for safety.

5. **Fail-Safe**: The fail-safe mechanism turns relays OFF. Ensure this is the safe state for your application.

---

## Production Considerations

For production deployment:

1. **PCB Design**: Replace breadboard with custom PCB
2. **Enclosure**: Use IP65-rated enclosure for harsh environments
3. **Connectors**: Use screw terminals or JST connectors
4. **Fuses**: Add fuses on relay outputs
5. **Isolation**: Use optocouplers for relay control
6. **EMI Protection**: Add capacitors and ferrite beads
7. **Mounting**: Secure all components with standoffs
8. **Labeling**: Label all connections clearly

---

## Bill of Materials (BOM)

| Item | Quantity | Unit Price | Total | Notes |
|------|----------|------------|-------|-------|
| ESP32-S3 Dev Board | 1 | $8 | $8 | USB-C version |
| DS18B20 Sensor | 3 | $2 | $6 | Waterproof |
| 2-Ch Relay Module | 1 | $3 | $3 | Active LOW, 5V |
| Green LED | 1 | $0.10 | $0.10 | 5mm |
| Yellow LED | 1 | $0.10 | $0.10 | 5mm |
| Red LED | 1 | $0.10 | $0.10 | 5mm |
| Blue LED | 1 | $0.10 | $0.10 | 5mm |
| 4.7kΩ Resistor | 3 | $0.05 | $0.15 | Pull-up |
| 220Ω Resistor | 4 | $0.05 | $0.20 | LED current |
| Breadboard | 1 | $3 | $3 | 830 points |
| Jumper Wires | 1 set | $2 | $2 | M-M, M-F |
| USB-C Cable | 1 | $3 | $3 | Data + Power |
| **TOTAL** | | | **$25.75** | Prototype cost |

---

## Conclusion

This wiring diagram provides complete instructions for assembling the ESP32 Climate-Smart Telemetry Controller. Follow the assembly instructions carefully, test each component individually, and verify all connections before powering on.

**Next Steps**:
1. Assemble hardware following this guide
2. Upload firmware (see HARDWARE-READINESS-CHECKLIST.md)
3. Run verification tests
4. Configure backend for serial mode
5. Start full system integration testing

**Status**: Ready for hardware assembly ✅
