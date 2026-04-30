// ============================================================================
// config.h — Configuration for Vehicle AI System (Arduino)
// ============================================================================
// WARNING: Do NOT commit real credentials. This file contains PLACEHOLDERS ONLY.
// For local development, create a copy or edit these values locally.
// ============================================================================

#ifndef CONFIG_H
#define CONFIG_H

// ============================================================================
// WiFi Configuration — LOCAL DEV ONLY, do not commit real credentials
// ============================================================================
#define WIFI_SSID       "YOUR_WIFI_SSID"
#define WIFI_PASSWORD   "YOUR_WIFI_PASSWORD"

// ============================================================================
// Cloud Endpoint — where ESP32 sends telemetry via HTTP POST
// ============================================================================
#define CLOUD_ENDPOINT  "http://192.168.1.100:8000/api/telemetry"

// ============================================================================
// Vehicle Identity
// ============================================================================
#define VEHICLE_ID      "KKE-001"

// ============================================================================
// Pin Assignments — DO NOT CHANGE unless hardware wiring is changed
// ============================================================================

// Sensors
#define PIN_DS18B20       4    // DS18B20 temperature sensor (OneWire data)
#define PIN_ULTRASONIC_TRIG 18 // Ultrasonic sensor TRIG
#define PIN_ULTRASONIC_ECHO 19 // Ultrasonic sensor ECHO
#define PIN_LDR           34   // LDR / photoresistor (analog)
#define PIN_THERMISTOR    35   // Thermistor (analog)

// LEDs
#define PIN_LED_RED       2    // Red LED (error / high temp)
#define PIN_LED_GREEN     15   // Green LED (normal operation)
#define PIN_LED_YELLOW    16   // Yellow LED (warning / efficient)

// Buzzer
#define PIN_BUZZER        17   // Buzzer (alerts)

// Relays
#define PIN_RELAY_1       32   // Relay 1
#define PIN_RELAY_2       33   // Relay 2

// LCD 16x2 in 4-bit mode (D0-D3 are NOT used)
#define PIN_LCD_RS        21
#define PIN_LCD_E         22
#define PIN_LCD_D4        23
#define PIN_LCD_D5        25
#define PIN_LCD_D6        26
#define PIN_LCD_D7        27

// ============================================================================
// Timing Configuration
// ============================================================================
#define TELEMETRY_INTERVAL_MS   2000   // Send telemetry every 2 seconds
#define WIFI_RETRY_INTERVAL_MS  10000  // Retry WiFi connection every 10 seconds
#define WIFI_CONNECT_TIMEOUT_MS 15000  // WiFi connection timeout

// ============================================================================
// Fuel Thresholds (ultrasonic distance → fuel percentage)
// ============================================================================
#define FUEL_TANK_EMPTY_CM   30.0   // Distance when tank is empty
#define FUEL_TANK_FULL_CM    5.0    // Distance when tank is full

// ============================================================================
// Temperature Thresholds
// ============================================================================
#define TEMP_HIGH_THRESHOLD  50.0   // High temperature warning (°C)
#define TEMP_CRITICAL        70.0   // Critical temperature (°C)

// ============================================================================
// Serial Baud Rate
// ============================================================================
#define SERIAL_BAUD_RATE  115200

#endif // CONFIG_H
