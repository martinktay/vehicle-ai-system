# Deployment Configuration Guide

This guide is the practical deployment map for the current codebase.

It is written around the architecture that actually works today:

- **live board demo:** ESP32 connected locally over USB serial
- **cloud/fleet view:** ESP32 posts telemetry to a reachable backend over Wi-Fi
- **frontend deployment:** Netlify-hosted static React app
- **backend deployment:** local machine for hardware demos, Render or similar for cloud-only access

## Recommended Deployment Modes

### Mode A: Live Hardware Demo

Use this when you need the judge to see:

- the **ESP32 board**
- the **LCD**
- the **local dashboard**
- the **same telemetry flowing end to end**

Architecture:

```text
ESP32 on COM6
-> local FastAPI backend in serial mode
-> local React dashboard
```

This is the **recommended competition demo mode**.

### Mode B: Cloud / Fleet Monitoring Demo

Use this when you want to show fleet-style presentation beyond one board.

Architecture:

```text
ESP32
-> Wi-Fi POST /api/telemetry
-> backend reachable on LAN or public internet
-> Cloud Dashboard / fleet summary
```

This is best presented as the **scalable extension layer**, not the main proof that the board works.

### Mode C: UI-Only Backup Demo

Use this when hardware is unavailable.

Architecture:

```text
Frontend
-> backend simulator mode
-> simulated telemetry
```

This is your fallback, not your primary demo.

## Frontend Configuration

Location:

- `frontend/`

Key environment variable:

```bash
VITE_API_URL=http://localhost:8000/api
```

### Local Demo

```bash
VITE_API_URL=http://localhost:8000/api
```

### Netlify Production

```bash
VITE_API_URL=https://your-backend-domain/api
```

### Build

```bash
cd frontend
npm install
npm run build
```

Output:

- `frontend/dist/`

## Netlify Configuration

The project already includes:

- [`frontend/netlify.toml`](../frontend/netlify.toml)

When connecting the repo in Netlify, use:

- **Base directory:** `frontend`
- **Build command:** `pnpm run build`
- **Publish directory:** `dist`
- **Node version:** `20`

Set this production environment variable in Netlify:

```text
VITE_API_URL=https://your-real-backend/api
```

## Backend Configuration

Location:

- `backend/`

Example environment values:

```bash
INGESTION_MODE=simulator
SERIAL_PORT=COM6
SERIAL_BAUD_RATE=115200
OPENAI_API_KEY=sk-your-key-here
```

## Backend Modes

### Simulator Mode

```powershell
cd backend
$env:INGESTION_MODE="simulator"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Serial Mode (Live ESP32 Demo)

```powershell
cd backend
$env:INGESTION_MODE="serial"
$env:SERIAL_PORT="COM6"
$env:SERIAL_BAUD_RATE="115200"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Important:

- `serial` mode only works on the machine physically connected to the board
- a cloud host such as Render cannot read your laptop USB serial port

### Public Backend For Cloud Telemetry

If the ESP32 is posting to `/api/telemetry`, the backend must be reachable from the board:

- over the same LAN, or
- over a public hostname/IP

## Firmware Configuration

Current working firmware location:

- [`firmware/arduino/vehicle_system/vehicle_system.ino`](../firmware/arduino/vehicle_system/vehicle_system.ino)

Configuration file:

- [`firmware/arduino/vehicle_system/config.h`](../firmware/arduino/vehicle_system/config.h)

### Serial Dashboard Demo

The firmware already emits dashboard-compatible serial JSON at:

- `115200` baud

### Cloud Dashboard Demo

For cloud posting, set local values in `config.h`:

```cpp
#define WIFI_SSID       "YOUR_WIFI_SSID"
#define WIFI_PASSWORD   "YOUR_WIFI_PASSWORD"
#define CLOUD_ENDPOINT  "http://192.168.x.x:8000/api/telemetry"
```

Important:

- do not commit real Wi-Fi credentials
- do not commit your private LAN IP unless you intentionally want it public

## Windows Networking Notes

For LAN cloud telemetry to work on Windows:

1. backend must run with `--host 0.0.0.0`
2. the ESP32 and laptop must be on the same network
3. inbound TCP `8000` may need to be allowed through Windows Firewall

Administrator PowerShell example:

```powershell
netsh advfirewall firewall add rule name="Vehicle AI Backend 8000" dir=in action=allow protocol=TCP localport=8000
```

## Health Checks

### Backend

```bash
http://localhost:8000/api/health
```

Expected example:

```json
{
  "status": "ok",
  "mode": "serial",
  "telemetry_available": true,
  "fleet_size": 0,
  "ingestion_connected": true
}
```

### Live Serial Telemetry

```bash
http://localhost:8000/api/latest
```

### Cloud Telemetry

```bash
http://localhost:8000/api/telemetry/latest
```

## Recommended Demo Startup Order

### Live Board Demo

1. connect ESP32 over USB
2. confirm the board is on `COM6`
3. start backend in `serial` mode
4. start frontend locally
5. confirm dashboard source is `ESP32`
6. demonstrate sensor change, LCD change, and dashboard change together

### Cloud View Demo

1. update `config.h` locally with Wi-Fi and `CLOUD_ENDPOINT`
2. flash firmware
3. start backend with `--host 0.0.0.0`
4. confirm `/api/telemetry/latest` receives posts
5. open the Cloud Dashboard

## What To Deploy Publicly

### Safe To Deploy

- frontend on Netlify
- backend on Render or similar for simulator/cloud HTTP APIs
- README, docs, screenshots, architecture assets

### Not A Public Deployment Primitive

- USB serial access to the board
- local COM-port-dependent ingestion
- real Wi-Fi credentials inside firmware config

## Final Recommendation

For final judging, treat the system as two connected stories:

1. **proof of real hardware intelligence**
   - ESP32 + LCD + local serial dashboard

2. **proof of scalable fleet vision**
   - cloud dashboard + fleet summary + AI insight API

That keeps the demo honest, strong, and easy to explain.
