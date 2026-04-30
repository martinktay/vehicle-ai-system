# Telemetry Bridge Service

Lightweight Python bridge service for the Climate-Smart Telemetry Platform.

## Architecture

This service follows the **Edge-Intelligence First** architecture:
- **Edge Controller (ESP32)**: Executes all decision logic
- **Bridge Service (Python)**: Lightweight telemetry forwarding only
- **Dashboard (React)**: Visualization only

The bridge service **never computes decisions** - it only forwards telemetry from the Edge Controller to the Dashboard.

## Features

- ✅ Simulator mode for demo/testing
- ✅ In-memory storage (no database)
- ✅ 60-second rolling window history
- ✅ REST API for frontend
- ✅ < 50MB memory footprint
- ✅ Non-blocking async I/O
- ✅ CORS-enabled for frontend access

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Service

### Simulator Mode (Default)

```bash
# From the backend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with explicit mode
INGESTION_MODE=simulator python -m app.main
```

### Serial Mode (ESP32 Connected)

```bash
# Linux/macOS
INGESTION_MODE=serial SERIAL_PORT=/dev/ttyUSB0 python -m app.main

# Windows (PowerShell)
$env:INGESTION_MODE="serial"; $env:SERIAL_PORT="COM3"; python -m app.main

# Windows (CMD)
set INGESTION_MODE=serial && set SERIAL_PORT=COM3 && python -m app.main
```

### Using .env File

```bash
# Create .env file from example
cp .env.example .env

# Edit .env to set your configuration
# INGESTION_MODE=serial
# SERIAL_PORT=/dev/ttyUSB0

# Run with .env configuration
python -m app.main
```

The service will start on `http://localhost:8000`

## API Endpoints

### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "mode": "simulator",
  "telemetry_available": true,
  "ingestion_connected": true
}
```

**Fields:**
- `status`: Service status (`ok`)
- `mode`: Ingestion mode (`serial` or `simulator`)
- `telemetry_available`: Whether telemetry data is available
- `ingestion_connected`: Whether ingestion source is connected (serial port or simulator)

### GET /api/latest
Get the latest telemetry message

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
  "system_status": "demo_mode",
  "network_status": "disconnected",
  "power_source": "battery"
}
```

### GET /api/history?limit=30
Get recent telemetry history (60-second rolling window)

**Query Parameters:**
- `limit` (optional): Maximum number of messages to return

**Response:**
```json
[
  { /* TelemetryMessage */ },
  { /* TelemetryMessage */ },
  ...
]
```

### GET /api/stats
Get telemetry statistics

**Response:**
```json
{
  "current_available": true,
  "history_count": 25,
  "history_window_seconds": 60
}
```

## Interactive API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `INGESTION_MODE` | `simulator` | Ingestion mode: `serial` or `simulator` |
| `SERIAL_PORT` | `/dev/ttyUSB0` | Serial port path (Linux: `/dev/ttyUSB0`, Windows: `COM3`) |
| `SERIAL_BAUD_RATE` | `115200` | Serial baud rate (must match ESP32 firmware) |

### Modes

**Simulator Mode:**
- Generates realistic mock telemetry
- No hardware required
- Ideal for development and testing

**Serial Mode:**
- Reads telemetry from ESP32 via USB serial
- Requires ESP32 connected and running firmware
- Automatic reconnection on disconnect

Future versions will support:
- LTE mode (ESP32 via LTE module)

## Memory Usage

- Current message: ~500 bytes
- History (60s): ~15 KB
- Total footprint: < 50 MB

## Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload

# Run tests (future)
pytest
```

## Architecture Compliance

✅ **Edge-Intelligence First**: No decision logic in bridge  
✅ **Lightweight**: < 50MB memory, minimal dependencies  
✅ **Stateless**: No database, in-memory only  
✅ **Non-blocking**: Async I/O throughout  
✅ **Schema Compliance**: Matches Telemetry Data Contract v1  

## Future Enhancements

- [ ] Serial port ingestion (ESP32 via USB)
- [ ] WebSocket streaming for real-time updates
- [ ] LTE transport layer
- [ ] Prometheus metrics endpoint
- [ ] Docker containerization
