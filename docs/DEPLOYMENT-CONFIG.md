# Deployment Configuration Guide

This guide explains how to configure the Climate-Smart Telemetry Platform for different deployment scenarios.

---

## Frontend Configuration

### Environment Variables

Create a `.env` file in the `frontend/` directory (copy from `.env.example`):

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000/api
```

### Deployment Scenarios

#### Local Development
```bash
VITE_API_URL=http://localhost:8000/api
```

#### Production (Same Host)
```bash
VITE_API_URL=http://your-domain.com/api
```

#### Production (Different Host)
```bash
VITE_API_URL=https://api.your-domain.com/api
```

### Build Commands

```bash
# Development
cd frontend
pnpm install
pnpm dev

# Production Build
pnpm build
# Output: frontend/dist/
```

---

## Backend Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory (copy from `.env.example`):

```bash
# Ingestion mode: "simulator" or "serial"
INGESTION_MODE=simulator

# Serial port configuration (for serial mode)
SERIAL_PORT=/dev/ttyUSB0
SERIAL_BAUD_RATE=115200
```

### Deployment Scenarios

#### Demo Mode (No Hardware)
```bash
INGESTION_MODE=simulator
```

#### Serial Mode (USB Connection)
```bash
INGESTION_MODE=serial
SERIAL_PORT=/dev/ttyUSB0    # Linux
# SERIAL_PORT=COM3          # Windows
SERIAL_BAUD_RATE=115200
```

#### LTE Mode (Future)
```bash
INGESTION_MODE=lte
LTE_ENDPOINT=https://your-lte-gateway.com/ingest
```

### Run Commands

```bash
# Development
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Firmware Configuration

### Pin Configuration

Edit `firmware/micropython/main.py`:

```python
# Temperature Sensor Pins (DS18B20 OneWire)
PIN_ENGINE_TEMP = 4      # Engine temperature sensor
PIN_FUEL_LINE_TEMP = 5   # Fuel line temperature sensor
PIN_AMBIENT_TEMP = 6     # Ambient temperature sensor

# Relay Control Pins (Active LOW)
PIN_RELAY_1 = 7          # Relay 1: Cooling system
PIN_RELAY_2 = 8          # Relay 2: Fuel switching

# Status LED Pins
PIN_LED_STATUS = 9       # Green: System running
PIN_LED_WARNING = 10     # Yellow: High temperature
PIN_LED_ERROR = 11       # Red: Overheat / fail-safe
PIN_LED_ACTIVITY = 12    # Blue: Telemetry transmission
```

### Safety Thresholds

Edit `firmware/micropython/main.py`:

```python
# Safety Thresholds (°C)
THRESHOLD_ENGINE_OVERHEAT = 100.0   # Fail-safe activation
THRESHOLD_FUEL_LINE_MAX = 90.0      # Fail-safe activation
THRESHOLD_ENGINE_OPTIMAL = 80.0     # Warning threshold
THRESHOLD_COOLING_ACTIVATE = 90.0   # Relay 1 activation
THRESHOLD_FUEL_SWITCH = 80.0        # Relay 2 activation
```

### Upload to ESP32

```bash
# Install ampy (if not already installed)
pip install adafruit-ampy

# Upload files
cd firmware/micropython
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 put sensors.py
ampy --port /dev/ttyUSB0 put relays.py
ampy --port /dev/ttyUSB0 put status_leds.py
ampy --port /dev/ttyUSB0 put telemetry.py

# Reset ESP32 to run
# Press reset button or:
ampy --port /dev/ttyUSB0 reset
```

---

## Mode Combinations

### Competition Demo (Offline)
- **Frontend**: Mock mode (no backend needed)
- **Backend**: Not running
- **Firmware**: Not needed
- **Use Case**: Offline dashboard demonstration

### Development (Simulator)
- **Frontend**: Backend API mode (`VITE_API_URL=http://localhost:8000/api`)
- **Backend**: Simulator mode (`INGESTION_MODE=simulator`)
- **Firmware**: Not needed
- **Use Case**: Full-stack development without hardware

### Lab Testing (Serial)
- **Frontend**: Backend API mode (`VITE_API_URL=http://localhost:8000/api`)
- **Backend**: Serial mode (`INGESTION_MODE=serial`, `SERIAL_PORT=/dev/ttyUSB0`)
- **Firmware**: Running on ESP32
- **Use Case**: Hardware integration testing

### Production (LTE) - Future
- **Frontend**: Backend API mode (`VITE_API_URL=https://api.your-domain.com/api`)
- **Backend**: LTE mode (`INGESTION_MODE=lte`)
- **Firmware**: Running on ESP32 with LTE dongle
- **Use Case**: Remote fleet deployment

---

## Port Configuration

### Default Ports
- **Frontend Dev Server**: `http://localhost:5173` (Vite default)
- **Backend API**: `http://localhost:8000`
- **Serial Communication**: 115200 baud

### Firewall Rules (Production)
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow backend API (if on different port)
sudo ufw allow 8000/tcp
```

---

## Health Checks

### Frontend
```bash
# Check if frontend is running
curl http://localhost:5173
```

### Backend
```bash
# Health check endpoint
curl http://localhost:8000/api/health

# Expected response:
# {
#   "status": "ok",
#   "mode": "simulator",
#   "telemetry_available": true,
#   "ingestion_connected": true
# }
```

### Firmware
```bash
# Monitor serial output
screen /dev/ttyUSB0 115200
# or
python -m serial.tools.miniterm /dev/ttyUSB0 115200

# Expected output: JSON telemetry messages every 2 seconds
```

---

## Troubleshooting

### Frontend can't connect to backend
1. Check `VITE_API_URL` in `.env`
2. Verify backend is running: `curl http://localhost:8000/api/health`
3. Check CORS configuration in `backend/app/main.py`

### Backend can't read serial port
1. Check port name: `ls /dev/tty*` (Linux) or Device Manager (Windows)
2. Check permissions: `sudo usermod -a -G dialout $USER` (Linux)
3. Verify baud rate matches firmware (115200)
4. Check `SERIAL_PORT` in backend `.env`

### Firmware not transmitting
1. Check serial connection: `screen /dev/ttyUSB0 115200`
2. Verify sensors are connected (check startup messages)
3. Check pin configuration matches hardware
4. Press reset button on ESP32

### Dashboard shows "Initializing..."
1. Check if backend is running
2. Check if telemetry is being generated (backend logs)
3. Verify API URL is correct
4. Check browser console for errors

---

## Security Considerations

### Development
- CORS allows all origins (`allow_origins=["*"]`)
- No authentication required
- Suitable for local development only

### Production
- Restrict CORS to frontend domain
- Add API key authentication
- Use HTTPS for all connections
- Implement rate limiting
- Add input validation and sanitization

---

## Performance Tuning

### Frontend
- Adjust polling interval in `useTelemetry.ts` (default: 2000ms)
- Adjust history window in `useTelemetry.ts` (default: 60000ms)

### Backend
- Adjust history duration in `telemetry_store.py` (default: 60s)
- Adjust simulator interval in `simulator.py` (default: 2.0s)

### Firmware
- Adjust sampling interval in `main.py` (default: 2000ms)
- Adjust telemetry interval in `main.py` (default: 2000ms)

---

## Monitoring

### Logs

**Frontend** (Browser Console):
- Connection status
- API errors
- Telemetry updates

**Backend** (stdout):
- Ingestion mode
- Connection status
- Telemetry processing
- Errors and warnings

**Firmware** (Serial Monitor):
- Sensor readings
- AI recommendations
- Relay states
- Fail-safe activations

### Metrics to Monitor

- Telemetry message rate (should be ~0.5 Hz)
- API response time (should be < 100ms)
- Memory usage (backend should be < 50MB)
- Temperature readings (should be in valid ranges)
- Fail-safe activations (should be rare)

