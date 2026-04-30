"""
Telemetry Bridge Service - Agentic AI Smart Fleet Monitoring Platform

Architecture: Application entry point
Purpose: Lightweight Python bridge between Edge Controller and Dashboard
"""

import os
import asyncio
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional, Dict

from app.schemas import TelemetryMessage, CloudTelemetryMessage, AIInsightRequest, AIInsightResponse, FleetSummary
from app.telemetry_store import telemetry_store
from app.simulator import simulator
try:
    from app.serial_reader import SerialReader
except ImportError:
    SerialReader = None
    print("[WARN] serial_asyncio not installed - Serial mode will be unavailable")


# ============================================================================
# CONFIGURATION
# ============================================================================

# Ingestion mode: "serial" or "simulator"
INGESTION_MODE = os.getenv("INGESTION_MODE", "simulator")

# Serial configuration (for serial mode)
SERIAL_PORT = os.getenv("SERIAL_PORT", "COM6")
SERIAL_BAUD_RATE = int(os.getenv("SERIAL_BAUD_RATE", "115200"))

# Global ingestion source
ingestion_source = None


# ============================================================================
# FLEET TELEMETRY STORE (v2 - Multi-vehicle support)
# ============================================================================

# In-memory storage for fleet telemetry (v2 schema)
fleet_telemetry: Dict[str, dict] = {}
cloud_telemetry_history: List[dict] = []
CLOUD_HISTORY_MAX = 500  # Keep last 500 messages


# ============================================================================
# MODE SELECTION
# ============================================================================

def select_ingestion_source():
    """Select ingestion source based on configuration."""
    global ingestion_source
    mode = INGESTION_MODE.lower()
    
    if mode == "serial":
        if SerialReader:
            print(f"Mode: Serial ({SERIAL_PORT} @ {SERIAL_BAUD_RATE} baud)")
            ingestion_source = SerialReader(SERIAL_PORT, SERIAL_BAUD_RATE)
        else:
            print("[WARN] Serial dependencies missing, falling back to simulator")
            ingestion_source = simulator
    elif mode == "simulator":
        print("Mode: Simulator (mock telemetry)")
        ingestion_source = simulator
    else:
        print(f"WARNING: Invalid INGESTION_MODE '{INGESTION_MODE}', defaulting to simulator")
        ingestion_source = simulator
    
    return ingestion_source


# ============================================================================
# APP LIFECYCLE
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start and stop background ingestion task."""
    print("--------------------------------------------------")
    print("   Agentic AI Smart Fleet Bridge starting...      ")
    print("--------------------------------------------------")
    
    source = select_ingestion_source()
    task = asyncio.create_task(source.start())
    
    yield
    
    print("Shutting down bridge service...")
    await source.stop()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# ============================================================================
# API INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Agentic AI Smart Fleet Monitoring API",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - service info."""
    return {
        "service": "Agentic AI Smart Fleet Monitoring Platform",
        "version": "2.0.0",
        "mode": INGESTION_MODE,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check for Render/Netlify."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/health")
async def api_health():
    """Detailed health check for the bridge service."""
    current = await telemetry_store.get_current()
    ingestion_connected = True

    if INGESTION_MODE.lower() == "serial":
        ingestion_connected = bool(
            ingestion_source and hasattr(ingestion_source, "is_connected") and ingestion_source.is_connected()
        )

    return {
        "status": "ok",
        "mode": INGESTION_MODE,
        "telemetry_available": current is not None,
        "fleet_size": len(fleet_telemetry),
        "ingestion_connected": ingestion_connected
    }


@app.get("/api/latest", response_model=TelemetryMessage)
async def get_latest_telemetry():
    """Get the latest telemetry message (v1 pipeline)."""
    current = await telemetry_store.get_current()
    if current is None:
        raise HTTPException(status_code=503, detail="No telemetry data available yet.")
    return current


@app.get("/api/history", response_model=List[TelemetryMessage])
async def get_telemetry_history(limit: Optional[int] = None):
    """Get telemetry history (v1 pipeline)."""
    return await telemetry_store.get_history(limit=limit)


# --- CLOUD TELEMETRY (v2) ---

@app.post("/api/telemetry")
async def receive_cloud_telemetry(message: CloudTelemetryMessage):
    """Ingest telemetry from ESP32 Cloud Client (v2)."""
    global fleet_telemetry, cloud_telemetry_history
    data = message.model_dump()
    data["timestamp"] = datetime.utcnow().isoformat() + "Z"
    fleet_telemetry[message.vehicle_id] = data
    cloud_telemetry_history.append(data)
    if len(cloud_telemetry_history) > CLOUD_HISTORY_MAX:
        cloud_telemetry_history.pop(0)
    return {"status": "success", "vehicle_id": message.vehicle_id}


@app.get("/api/telemetry/latest")
async def get_cloud_telemetry_latest(vehicle_id: Optional[str] = None):
    """Get latest telemetry for a vehicle or fleet."""
    if vehicle_id:
        if vehicle_id in fleet_telemetry:
            return fleet_telemetry[vehicle_id]
        raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found")
    if not fleet_telemetry:
        return {"status": "no_data"}
    return cloud_telemetry_history[-1] if cloud_telemetry_history else list(fleet_telemetry.values())[-1]


@app.get("/api/telemetry/history")
async def get_cloud_telemetry_history(limit: Optional[int] = 50, vehicle_id: Optional[str] = None):
    """Get cloud telemetry history."""
    history = cloud_telemetry_history
    if vehicle_id:
        history = [m for m in history if m.get("vehicle_id") == vehicle_id]
    if limit:
        return history[-limit:]
    return history


@app.get("/api/fleet/summary")
async def get_fleet_summary():
    """Get aggregated fleet metrics."""
    if not fleet_telemetry:
        return {
            "total_vehicles": 0, "online_vehicles": 0,
            "total_cost_saved": 0.0, "total_co2_reduction": 0.0,
            "fuel_mode_distribution": {}, "status_distribution": {},
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
    vehicles = list(fleet_telemetry.values())
    total_vehicles = len(vehicles)
    fuel_dist, status_dist = {}, {}
    total_cost, total_co2 = 0.0, 0.0
    for v in vehicles:
        fm = v.get("fuel_mode", "UNKNOWN")
        st = v.get("status", "NORMAL")
        fuel_dist[fm] = fuel_dist.get(fm, 0) + 1
        status_dist[st] = status_dist.get(st, 0) + 1
        total_cost += v.get("cost_saved", 0)
        total_co2 += v.get("co2_reduction", 0)
    return {
        "total_vehicles": total_vehicles,
        "online_vehicles": total_vehicles,
        "total_cost_saved": round(total_cost, 2),
        "total_co2_reduction": round(total_co2, 2),
        "fuel_mode_distribution": fuel_dist,
        "status_distribution": status_dist,
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/api/ai-insight", response_model=AIInsightResponse)
async def get_ai_insight(request: AIInsightRequest):
    """Get AI-powered fleet advice."""
    from app.ai_service import generate_ai_insight
    return await generate_ai_insight(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
