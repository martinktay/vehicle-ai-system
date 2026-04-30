# Climate-Smart Telemetry Platform - Architecture

## Overview

The Climate-Smart Telemetry Platform is an embedded AI + IoT system designed to optimize fuel efficiency and reduce emissions in real-time. The system uses edge computing to make intelligent decisions locally while providing remote monitoring capabilities.

## Core Principles

### 1. Edge-Intelligence First
All decision logic executes on the ESP32 microcontroller at the edge. This ensures:
- Real-time response (< 1 second)
- Operation without network connectivity
- Reduced latency for safety-critical decisions
- Lower cloud costs

### 2. Transparent AI
The system uses deterministic, rule-based AI that is:
- Explainable: Every decision can be traced to specific sensor readings
- Auditable: Decision logic is visible in the code
- Trustworthy: No black-box machine learning in v1

### 3. Fail-Safe Design
Hardware and software fail-safe mechanisms ensure:
- Relays default to safe state on power loss
- Watchdog timer prevents system hangs
- Overheat detection triggers immediate fail-safe
- Safety thresholds are configurable

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EDGE LAYER (ESP32)                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Sensors → AI Decision Engine → Relay Control          │ │
│  │  - DS18B20 temperature sensors (3x)                    │ │
│  │  - Rule-based AI recommendations                       │ │
│  │  - 2-channel relay control                             │ │
│  │  - Safety monitoring & fail-safe                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           │ Serial Telemetry (JSON)          │
│                           ▼                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  BRIDGE LAYER (Python)                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Telemetry Ingestion → Storage → API                   │ │
│  │  - Serial/Simulator/LTE ingestion                      │ │
│  │  - In-memory storage (60s window)                      │ │
│  │  - REST API endpoints                                  │ │
│  │  - No decision logic (display only)                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           │ HTTP API                         │
│                           ▼                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│               VISUALIZATION LAYER (React)                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Dashboard Components                                   │ │
│  │  - Real-time temperature charts                        │ │
│  │  - Relay state indicators                              │ │
│  │  - AI recommendation display                           │ │
│  │  - Climate impact metrics                              │ │
│  │  - Decision transparency panel                         │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### ESP32 Firmware (Edge Intelligence)
**Responsibilities:**
- Read temperature sensors every 2 seconds
- Compute AI recommendations based on thresholds
- Control relays based on decisions
- Monitor safety thresholds
- Generate telemetry JSON
- Transmit via serial port

**Does NOT:**
- Depend on network connectivity
- Wait for cloud decisions
- Modify behavior based on dashboard

### Bridge Service (Telemetry Aggregation)
**Responsibilities:**
- Ingest telemetry from ESP32 or simulator
- Store last 60 seconds of data in memory
- Expose REST API for dashboard
- Handle multiple ingestion modes

**Does NOT:**
- Make decisions about relay states
- Compute AI recommendations
- Modify telemetry data

### Dashboard (Visualization)
**Responsibilities:**
- Display real-time telemetry
- Show decision reasoning
- Visualize climate impact
- Provide user feedback

**Does NOT:**
- Make decisions about relay states
- Compute AI recommendations
- Control hardware directly

## Data Flow

```
1. Sensors → ESP32 reads temperature (2s interval)
2. ESP32 → Computes AI recommendation
3. ESP32 → Controls relays based on decision
4. ESP32 → Generates telemetry JSON
5. ESP32 → Transmits via serial (115200 baud)
6. Bridge → Parses JSON, validates schema
7. Bridge → Stores in memory (60s window)
8. Dashboard → Polls API every 2 seconds
9. Dashboard → Displays telemetry and decisions
```

## Telemetry Schema

All telemetry messages conform to **Telemetry Data Contract v1**:

```json
{
  "timestamp": "2024-03-20T10:30:45.123Z",
  "engine_temperature": 85.3,
  "fuel_line_temperature": 62.1,
  "ambient_temperature": 28.5,
  "current_fuel_mode": "biodiesel",
  "ai_recommendation": "maintain",
  "relay_state_1": true,
  "relay_state_2": false,
  "overheat_flag": false,
  "system_status": "live_mode",
  "network_status": "disconnected",
  "power_source": "battery"
}
```

**Schema Immutability:** Field names never change without a version bump.

## Deployment Modes

### Mode 1: Competition Demo (Offline)
- **Hardware:** ESP32 + Laptop
- **Ingestion:** Simulator or Serial
- **Network:** None required
- **Use case:** Competition demonstrations, development

### Mode 2: Local Deployment (USB Serial)
- **Hardware:** ESP32 + Host computer
- **Ingestion:** Serial (USB)
- **Network:** Local only
- **Use case:** Single-node testing, lab deployment

### Mode 3: Remote Deployment (LTE)
- **Hardware:** ESP32 + LTE dongle
- **Ingestion:** LTE uplink
- **Network:** Cellular (4G/LTE)
- **Use case:** Fleet deployment, remote monitoring

## Climate Impact

### Efficiency Optimization
The system optimizes fuel efficiency by:
- Monitoring engine and fuel line temperatures
- Recommending optimal fuel modes (diesel, biodiesel, mixed)
- Activating cooling when needed
- Reducing unnecessary load

### Transparent Calculations
All efficiency metrics are calculated with visible formulas:
- Current efficiency percentage
- Fuel savings vs. baseline
- CO₂ emission reduction estimates
- Calculation methodology displayed on dashboard

### No Exaggerated Claims
- Efficiency improvements depend on specific use case
- CO₂ reduction estimates are based on fuel savings
- System provides data for informed decisions
- Actual impact varies by deployment scenario

## Safety Features

### Hardware Fail-Safe
- **Active LOW relays:** Relays turn OFF when GPIO is HIGH
- **Power loss:** Relays default to OFF (safe state)
- **Crash recovery:** Relays OFF during system reset

### Software Fail-Safe
- **Watchdog timer:** 5-second timeout, auto-reset on hang
- **Overheat detection:** Immediate fail-safe activation
- **Threshold monitoring:** Configurable safety limits
- **Error handling:** Graceful degradation on sensor failure

### Fail-Safe Activation
Triggered by:
- Engine temperature > 100°C
- Fuel line temperature > 90°C
- System error or crash
- Watchdog timeout

## Technology Stack

### Firmware
- **Platform:** ESP32-S3 (MicroPython)
- **Sensors:** DS18B20 (OneWire)
- **Actuators:** 2-channel relay module
- **Communication:** UART serial (115200 baud)

### Backend
- **Language:** Python 3.8+
- **Framework:** FastAPI (async)
- **Storage:** In-memory (no database)
- **Communication:** REST API, Serial I/O

### Frontend
- **Framework:** React 18 + TypeScript
- **Build tool:** Vite
- **Package manager:** pnpm
- **Styling:** Custom CSS (no heavy UI library)

## Scalability

### Current (v1)
- Single ESP32 node
- Local or remote monitoring
- In-memory storage (60s window)

### Future (v2+)
- Multi-node fleet management
- Time-series database for historical data
- WebSocket for real-time streaming
- Mobile app for remote monitoring
- Advanced analytics and reporting

## Performance Characteristics

- **Sensor sampling:** 2 seconds
- **Decision latency:** < 1 second
- **Telemetry transmission:** 2 seconds
- **Dashboard update:** 2 seconds (polling)
- **Fail-safe activation:** < 100 milliseconds
- **Memory footprint:** < 50 MB (bridge service)

## Compliance and Standards

- **Edge-Intelligence First:** Decision logic at edge
- **Schema Immutability:** Telemetry contract versioning
- **Fail-Safe Design:** Hardware + software safety
- **Transparent AI:** Explainable decision logic
- **Offline Operation:** No network dependency for core functions
