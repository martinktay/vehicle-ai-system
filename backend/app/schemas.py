"""
Telemetry Data Contracts

This module defines telemetry message schemas for both v1 (MicroPython/serial)
and v2 (Arduino/cloud) telemetry pipelines.

Architecture: Type definitions layer
Purpose: Single source of truth for telemetry message structure

IMPORTANT: v1 field names are immutable. v2 is a new schema for cloud telemetry.
"""

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Literal, Optional


# ============================================================================
# TELEMETRY DATA CONTRACT v1 — MicroPython / Serial Pipeline
# ============================================================================
# DO NOT modify field names. These are immutable across the system.
# ============================================================================

class TelemetryMessage(BaseModel):
    """
    Telemetry Data Contract v1

    All field names must match TELEMETRY_SCHEMA.md exactly.
    These fields are immutable across the system.

    Configuration:
    - strict=True: Disables type coercion (strings won't convert to numbers, etc.)
    - This ensures type safety across the telemetry pipeline
    """
    model_config = ConfigDict(strict=True)

    # Timestamp
    timestamp: str  # ISO 8601 format

    # Temperature sensors ((C))
    engine_temperature: float
    fuel_line_temperature: float
    ambient_temperature: float

    # Fuel system
    current_fuel_mode: str

    # AI decision (computed by Edge_Controller)
    ai_recommendation: str

    # Relay states (controlled by Edge_Controller)
    relay_state_1: bool
    relay_state_2: bool

    # Safety flags
    overheat_flag: bool

    # System status
    system_status: str
    network_status: str
    power_source: str


# Type aliases for valid enum values (v1)
FuelMode = Literal["diesel", "biodiesel", "mixed"]
AIRecommendation = Literal["maintain", "switch_to_biodiesel", "switch_to_diesel", "activate_cooling", "reduce_load"]
SystemStatus = Literal["normal", "demo_mode", "live_mode", "fail_safe", "error"]
NetworkStatus = Literal["connected", "disconnected"]
PowerSource = Literal["battery", "solar", "grid"]


# ============================================================================
# TELEMETRY DATA CONTRACT v2 — Arduino / Cloud Pipeline
# ============================================================================
# This schema is used by the Arduino firmware (firmware/arduino/) and the
# POST /api/telemetry cloud endpoint.
# ============================================================================

class CloudTelemetryMessage(BaseModel):
    """
    Telemetry Data Contract v2 — Cloud Telemetry from ESP32 Arduino firmware.

    Received via HTTP POST from the ESP32 running Arduino firmware.
    Fields match the JSON output of vehicle_system.ino.
    """

    # Vehicle identity
    vehicle_id: str = "KKE-001"
    vehicle_type: str = "keke"  # keke | bus | taxi | company_vehicle

    # Sensor readings
    temperature: float           # DS18B20 engine temperature ((C))
    distance_cm: float           # Ultrasonic distance (cm)
    fuel_percent: int            # Calculated fuel level (0-100%)
    ldr: int                     # LDR / photoresistor analog value
    thermistor: int              # Thermistor analog value

    # Decision engine outputs
    fuel_mode: str               # PETROL | LPG | CNG
    status: str                  # NORMAL | EFFICIENT | HIGH TEMP | LOW FUEL
    relay1: str                  # ON | OFF
    relay2: str                  # ON | OFF
    reason: str                  # Human-readable decision reason

    # Impact metrics (calculated by ESP32)
    cost_saved: float            # Estimated cost saving
    co2_reduction: float         # Estimated CO2 reduction

    # Metadata
    timestamp_source: str = "device"

    @field_validator('vehicle_type')
    @classmethod
    def validate_vehicle_type(cls, v):
        valid = {"keke", "bus", "taxi", "company_vehicle"}
        if v.lower() not in valid:
            raise ValueError(f"vehicle_type must be one of {valid}, got '{v}'")
        return v.lower()

    @field_validator('fuel_mode')
    @classmethod
    def validate_fuel_mode(cls, v):
        valid = {"PETROL", "LPG", "CNG"}
        if v.upper() not in valid:
            raise ValueError(f"fuel_mode must be one of {valid}, got '{v}'")
        return v.upper()

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid = {"NORMAL", "EFFICIENT", "HIGH TEMP", "LOW FUEL"}
        if v.upper() not in valid:
            raise ValueError(f"status must be one of {valid}, got '{v}'")
        return v.upper()

    @field_validator('relay1', 'relay2')
    @classmethod
    def validate_relay(cls, v):
        valid = {"ON", "OFF"}
        if v.upper() not in valid:
            raise ValueError(f"relay must be ON or OFF, got '{v}'")
        return v.upper()

    @field_validator('fuel_percent')
    @classmethod
    def validate_fuel_percent(cls, v):
        if not 0 <= v <= 100:
            raise ValueError(f"fuel_percent must be 0-100, got {v}")
        return v


class AIInsightRequest(BaseModel):
    """Request body for AI insight endpoint."""
    vehicle_id: str = "KKE-001"
    temperature: float
    fuel_percent: int
    fuel_mode: str
    status: str
    relay1: str
    relay2: str
    ldr: int
    thermistor: int
    reason: str


class AIInsightResponse(BaseModel):
    """Response from AI insight endpoint."""
    recommendation: str
    confidence: str             # HIGH | MEDIUM | LOW
    risk_level: str             # LOW | MODERATE | HIGH | CRITICAL
    roadworthiness: str         # Human-readable note
    climate_note: str           # Environmental impact note
    operator_message: str       # Message for the vehicle operator
    source: str = "ai"         # "ai" or "fallback"


class FleetSummary(BaseModel):
    """Aggregated metrics for the entire fleet."""
    total_vehicles: int
    online_vehicles: int
    total_cost_saved: float
    total_co2_reduction: float
    fuel_mode_distribution: dict  # {"PETROL": 5, "LPG": 2, ...}
    status_distribution: dict     # {"NORMAL": 6, "HIGH TEMP": 1, ...}
    last_updated: str
