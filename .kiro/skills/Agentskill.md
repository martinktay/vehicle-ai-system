# Agentskill — Development Guardrails for AI Agents

## Purpose
This file defines strict rules that any AI coding agent must follow when modifying this codebase. Violations of these rules may break hardware, expose secrets, or corrupt the system.

---

## 🚫 NEVER Do These

### Hardware Safety
- **NEVER include DHT11** — it has been dropped from this project permanently.
- **NEVER change Arduino pin mappings** unless the user explicitly confirms a conflict:
  - DS18B20: GPIO 4
  - Ultrasonic TRIG: GPIO 18, ECHO: GPIO 19
  - LDR: GPIO 34
  - Thermistor: GPIO 35
  - Red LED: GPIO 2
  - Green LED: GPIO 15
  - Yellow LED: GPIO 16
  - Buzzer: GPIO 17
  - Relay 1: GPIO 32
  - Relay 2: GPIO 33
  - LCD RS=21, E=22, D4=23, D5=25, D6=26, D7=27 (4-bit mode, D0-D3 unused)
- **NEVER remove LCD display logic** from the Arduino firmware.
- **NEVER remove LED, buzzer, or relay logic** from the Arduino firmware.
- **NEVER remove existing sensor reading logic** from the Arduino firmware.

### Security
- **NEVER hardcode real WiFi passwords, API keys, or tokens** in source files.
- **NEVER expose `OPENAI_API_KEY`** in frontend/browser code.
- **NEVER expose Supabase service role keys** in frontend code.
- **NEVER commit `.env` files** — only `.env.example` with placeholder values.
- **NEVER remove `.gitignore`** or weaken its rules.

### Architecture
- **NEVER break offline operation** — if WiFi or cloud upload fails, the ESP32 LCD/LED/buzzer/relay system must continue working.
- **NEVER remove existing MicroPython firmware** in `firmware/micropython/`.
- **NEVER modify existing backend endpoints** (`/api/health`, `/api/latest`, `/api/history`) in ways that break the v1 telemetry contract.

---

## ✅ ALWAYS Do These

### Before Any Change
- **ALWAYS check this file** and `SKILL.md` before making changes.
- **ALWAYS preserve existing working code** — add, don't replace.
- **ALWAYS add comments** explaining new cloud/WiFi functions.

### Firmware (Arduino)
- **ALWAYS use configurable constants** for WiFi credentials and endpoints.
- **ALWAYS implement `sendTelemetryToCloud()` with error handling** — failures must not crash the main loop.
- **ALWAYS print WiFi status and upload status** to Serial for debugging.
- **ALWAYS keep the telemetry interval at 2 seconds** unless user specifies otherwise.

### Backend
- **ALWAYS validate incoming telemetry payloads** with Pydantic.
- **ALWAYS return clean JSON responses** with proper HTTP status codes.
- **ALWAYS read secrets from environment variables**, never from code.
- **ALWAYS provide graceful fallback** if OPENAI_API_KEY is missing.

### Frontend
- **ALWAYS poll telemetry endpoints** (2-5 second interval).
- **ALWAYS fall back to mock data** if backend is unavailable.
- **ALWAYS display the data source** (Backend API vs Mock) to the user.

---

## 📋 Telemetry Schemas

### v1 Schema (MicroPython — DO NOT MODIFY)
Used by `firmware/micropython/` and existing backend/frontend.
Fields: `timestamp`, `engine_temperature`, `fuel_line_temperature`, `ambient_temperature`, `current_fuel_mode`, `ai_recommendation`, `relay_state_1`, `relay_state_2`, `overheat_flag`, `system_status`, `network_status`, `power_source`

### v2 Schema (Arduino — Cloud Telemetry)
Used by `firmware/arduino/` and new cloud endpoints.
Fields: `vehicle_id`, `temperature`, `distance_cm`, `fuel_percent`, `fuel_mode`, `status`, `relay1`, `relay2`, `ldr`, `thermistor`, `cost_saved`, `co2_reduction`, `reason`, `timestamp_source`

**Rule:** Both schemas must be supported simultaneously. Never remove v1 to replace with v2.

---

## 🔌 Hardware Reference

- **Board:** ESP32 (not ESP32-S3 for Arduino firmware)
- **USB:** CH340 USB-Serial on COM6
- **Baud Rate:** 115200
- **LCD:** 16×2, 4-bit mode (D0-D3 NOT USED)
- **Relay Config:** Active control via GPIO 32, 33

---

*Last Updated: 2026-04-30*
