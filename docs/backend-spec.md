# Backend Specification

## Overview

The bridge service is a lightweight Python application that ingests telemetry from the ESP32, stores it in memory, and exposes a REST API for the dashboard. It acts as a stateless relay between the edge device and visualization layer.

## Technology Stack

- **Language:** Python 3.8+
- **Framework:** FastAPI (async)
- **Server:** Uvicorn (ASGI)
- **Validation:** Pydantic
- **Serial I/O:** pyserial-asyncio
- **Storage:** In-memory (no database)

## Architecture

### Module Structure

```
backend/app/
├── main.py                # Application entry point
├── schemas.py             # Telemetry data models
├── telemetry_store.py     # In-memory storage
├── simulator.py           # Mock telemetry generator
├── serial_reader.py       # Serial port ingestion
└── lte_ingestion.py       # LTE ingestion endpoint (future)
```

### Data Flow

```
Ingestion Sources:
├── Simulator → generates mock data
├── Serial → reads from ESP32 via USB
└── LTE → receives HTTP POST (future)
         ↓
    TelemetryStore (in-memory)
         ↓
    REST API endpoints
         ↓
    Dashboard (HTTP polling)
```

## Core Principles

### 1. Lightweight
- **Memory:** < 50 MB footprint
- **CPU:** < 5% idle, < 10% active
- **Dependencies:** Minimal (4 packages)
- **No database:** In-memory storage only

### 2. Non-Blocking
- **Async I/O:** All operations use asyncio
- **Concurrent requests:** Handle multiple API calls
- **Serial reading:** Non-blocking serial port reads
- **No blocking delays:** Event-driven architecture

### 3. Stateless
- **No decision logic:** Only forwards telemetry
- **No data modification:** Telemetry passed through unchanged
- **No persistent state:** Restart-safe (except in-memory data)

### 4. Mode-Agnostic
- **Simulator mode:** Works without hardware
- **Serial mode:** Reads from ESP32
- **LTE mode:** Receives from remote gateway (future)
- **Same API:** Dashboard doesn't know the mode

## Ingestion Modes

### Mode 1: Simulator (Default)
**Purpose:** Development and demos without hardware

**Configuration:**
```bash
INGESTION_MODE=simulator
```

**Behavior:**
- Generates realistic mock telemetry
- Updates every 2 seconds
- Smooth temperature transitions
- Valid state changes

**Use cases:**
- Frontend development
- Competition demos without ESP32
- Testing and CI/CD

### Mode 2: Serial (Production)
**Purpose:** Read from ESP32 via USB serial

**Configuration:**
```bash
INGESTION_MODE=serial
SERIAL_PORT=/dev/ttyUSB0  # Linux
SERIAL_BAUD_RATE=115200
```

**Behavior:**
- Opens serial port connection
- Reads newline-delimited JSON
- Parses and validates each line
- Auto-reconnects on disconnect

**Use cases:**
- Local deployment with ESP32
- Lab testing
- Single-node monitoring

### Mode 3: LTE (Future)
**Purpose:** Receive telemetry from remote LTE gateway

**Configuration:**
```bash
INGESTION_MODE=lte
LTE_INGEST_ENABLED=true
```

**Behavior:**
- Exposes `/api/ingest` endpoint
- Receives HTTP POST from LTE gateway
- Validates and stores telemetry
- Same API for dashboard

**Use cases:**
- Fleet deployment
- Remote monitoring
- Cloud-hosted bridge

## API Endpoints

### GET /api/health
**Purpose:** Health check and status

**Response:**
```json
{
  "status": "ok",
  "mode": "serial",
  "telemetry_available": true,
  "ingestion_connected": true
}
```

**Fields:**
- `status`: Service status (always "ok" if responding)
- `mode`: Ingestion mode ("simulator", "serial", "lte")
- `telemetry_available`: Whether telemetry data exists
- `ingestion_connected`: Whether ingestion source is connected

### GET /api/latest
**Purpose:** Get the most recent telemetry message

**Response:**
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

**Status codes:**
- `200 OK`: Telemetry available
- `503 Service Unavailable`: No telemetry received yet

### GET /api/history
**Purpose:** Get recent telemetry history (60-second rolling window)

**Query parameters:**
- `limit` (optional): Max number of messages to return

**Response:**
```json
[
  { /* TelemetryMessage */ },
  { /* TelemetryMessage */ },
  ...
]
```

**Status codes:**
- `200 OK`: History available (may be empty array)

### GET /api/stats
**Purpose:** Get telemetry statistics

**Response:**
```json
{
  "current_available": true,
  "history_count": 25,
  "history_window_seconds": 60
}
```

### POST /api/ingest (Future - LTE mode)
**Purpose:** Receive telemetry from LTE gateway

**Request body:**
```json
{
  "timestamp": "...",
  "engine_temperature": 85.3,
  ...
}
```

**Response:**
```json
{
  "status": "ok",
  "message": "Telemetry ingested"
}
```

## In-Memory Storage

### TelemetryStore Class

**Purpose:** Thread-safe storage for telemetry data

**Storage:**
- `_current`: Latest telemetry message
- `_history`: deque of messages (60-second window)
- `_lock`: asyncio.Lock for thread safety

**Methods:**
```python
async def store(message: TelemetryMessage) -> None
async def get_current() -> Optional[TelemetryMessage]
async def get_history(limit: Optional[int]) -> List[TelemetryMessage]
```

**Pruning strategy:**
- Automatic pruning on each store operation
- Removes messages older than 60 seconds
- Bounded memory (max ~30 messages at 2s intervals)

**Thread safety:**
- All operations protected by asyncio.Lock
- Safe for concurrent API requests
- Safe for concurrent ingestion and API access

## Serial Reader

### SerialReader Class

**Purpose:** Read telemetry from ESP32 via serial port

**Features:**
- Async serial reading (non-blocking)
- Line-by-line JSON parsing
- Schema validation
- Auto-reconnection on disconnect
- Exponential backoff on errors

**Connection management:**
```python
async def start() -> None  # Start read loop
async def stop() -> None   # Stop read loop
def is_connected() -> bool # Check connection status
```

**Error handling:**
- **Connection errors:** Retry with exponential backoff (1s → 2s → 4s → ... → 60s)
- **Parse errors:** Log warning, skip line, continue reading
- **Validation errors:** Log warning, skip message, continue reading
- **Timeout:** Detect disconnect, attempt reconnection

**Reconnection strategy:**
- Automatic reconnection on disconnect
- Exponential backoff prevents rapid retry loops
- Resets delay on successful connection
- Continues indefinitely until stopped

## Simulator

### TelemetrySimulator Class

**Purpose:** Generate realistic mock telemetry

**Features:**
- Smooth temperature transitions (not random jumps)
- Valid state changes
- Realistic value ranges
- 2-second update interval

**Temperature simulation:**
- Engine: 60-120°C (drift ±2°C per update)
- Fuel line: 40-100°C (drift ±1.5°C per update)
- Ambient: 15-45°C (drift ±0.5°C per update)

**State simulation:**
- Fuel mode: Occasional changes (5% probability)
- Relay 1: ON when engine > 90°C
- Relay 2: ON when fuel line > 80°C
- Overheat: Triggered when engine > 100°C

## Configuration

### Environment Variables

```bash
# Ingestion mode
INGESTION_MODE=simulator  # "simulator", "serial", "lte"

# Serial configuration (for serial mode)
SERIAL_PORT=/dev/ttyUSB0  # Linux: /dev/ttyUSB0, Windows: COM3
SERIAL_BAUD_RATE=115200

# LTE configuration (for lte mode, future)
LTE_INGEST_ENABLED=true
LTE_AUTH_TOKEN=your-secret-token
```

### Configuration file (.env)

```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

## Running the Service

### Simulator Mode
```bash
python -m app.main
```

### Serial Mode
```bash
# Linux/macOS
INGESTION_MODE=serial SERIAL_PORT=/dev/ttyUSB0 python -m app.main

# Windows (PowerShell)
$env:INGESTION_MODE="serial"; $env:SERIAL_PORT="COM3"; python -m app.main
```

### Using .env file
```bash
# Edit .env
INGESTION_MODE=serial
SERIAL_PORT=/dev/ttyUSB0

# Run
python -m app.main
```

## Error Handling

### Connection Errors
- Log error with details
- Attempt reconnection with exponential backoff
- Update health endpoint to reflect disconnected state
- Continue serving last valid telemetry

### Parse Errors
- Log warning with line content (truncated)
- Skip invalid line
- Continue reading next line
- Don't crash ingestion loop

### Validation Errors
- Log validation error details
- Skip invalid message
- Continue reading next message
- Track validation failure rate

### Timeout Errors
- Detect timeout vs. disconnect
- Attempt reconnection if disconnected
- Keep last valid telemetry available
- Update health endpoint status

## Performance Characteristics

- **Latency:** Serial read → API response < 50ms
- **Throughput:** Handles 2-5 second telemetry intervals easily
- **Memory:** < 50 MB total footprint
- **CPU:** < 5% idle, < 10% active
- **Concurrent requests:** Handles 100+ simultaneous API calls

## Security Considerations

### Current (v1)
- **CORS:** Enabled for all origins (development)
- **Authentication:** None (local deployment)
- **HTTPS:** Not required (local HTTP)

### Future (v2+)
- **CORS:** Restrict to specific origins
- **Authentication:** API key or JWT tokens
- **HTTPS:** Required for cloud deployment
- **Rate limiting:** Prevent abuse
- **Input validation:** Strict schema enforcement

## Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Future)
```bash
docker build -t telemetry-bridge .
docker run -p 8000:8000 telemetry-bridge
```

## Monitoring

### Health Checks
- `/api/health` endpoint for liveness probes
- Check `ingestion_connected` for readiness
- Monitor `last_message_age_seconds` for stale data

### Logging
- Startup/shutdown events
- Connection status changes
- Parse/validation errors
- Performance warnings

### Metrics (Future)
- Telemetry message rate
- API request rate
- Error rates
- Latency percentiles

## Future Enhancements

- **WebSocket support:** Real-time streaming to dashboard
- **Time-series database:** PostgreSQL + TimescaleDB for historical data
- **Multi-node support:** Handle multiple ESP32 devices
- **Authentication:** API key or JWT tokens
- **Rate limiting:** Prevent abuse
- **Metrics:** Prometheus integration
- **Docker:** Containerized deployment
