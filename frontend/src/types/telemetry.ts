/**
 * Telemetry Data Contracts
 * 
 * This file defines schemas for both v1 (MicroPython/serial) and
 * v2 (Arduino/cloud) telemetry pipelines.
 * 
 * Architecture: Type definitions layer
 * Purpose: Single source of truth for telemetry message structure
 * 
 * IMPORTANT: v1 field names are immutable. v2 is a new schema for cloud telemetry.
 */

// ============================================================================
// TELEMETRY DATA CONTRACT v1 — MicroPython / Serial Pipeline (DO NOT MODIFY)
// ============================================================================

export interface TelemetryMessage {
  // Timestamp
  timestamp: string; // ISO 8601 format

  // Temperature sensors (°C)
  engine_temperature: number;
  fuel_line_temperature: number;
  ambient_temperature: number;

  // Fuel system
  current_fuel_mode: string;

  // AI decision (computed by Edge_Controller)
  ai_recommendation: string;

  // Relay states (controlled by Edge_Controller)
  relay_state_1: boolean;
  relay_state_2: boolean;

  // Safety flags
  overheat_flag: boolean;

  // System status
  system_status: string;
  network_status: string;
  power_source: string;
}

/**
 * Valid fuel modes (v1)
 */
export type FuelMode = 'cng' | 'petrol' | 'lpg' | 'diesel' | 'biodiesel' | 'mixed';

/**
 * Valid AI recommendations (v1)
 */
export type AIRecommendation = 
  | 'maintain' 
  | 'switch_to_biodiesel' 
  | 'switch_to_diesel'
  | 'activate_cooling'
  | 'reduce_load';

/**
 * Valid system status values (v1)
 */
export type SystemStatus = 
  | 'normal' 
  | 'demo_mode' 
  | 'live_mode' 
  | 'fail_safe' 
  | 'error';

/**
 * Valid network status values (v1)
 */
export type NetworkStatus = 'connected' | 'disconnected';

/**
 * Valid power source values (v1)
 */
export type PowerSource = 'battery' | 'solar' | 'grid';


// ============================================================================
// TELEMETRY DATA CONTRACT v2 — Arduino / Cloud Pipeline
// ============================================================================

export interface CloudTelemetryMessage {
  // Vehicle identity
  vehicle_id: string;
  vehicle_type: 'keke' | 'bus' | 'taxi' | 'company_vehicle';

  // Sensor readings
  temperature: number;       // DS18B20 engine temperature (°C)
  distance_cm: number;       // Ultrasonic distance (cm)
  fuel_percent: number;      // Calculated fuel level (0-100%)
  ldr: number;               // LDR / photoresistor analog value
  thermistor: number;        // Thermistor analog value

  // Decision engine outputs
  fuel_mode: string;         // PETROL | LPG | CNG
  status: string;            // NORMAL | EFFICIENT | HIGH TEMP | LOW FUEL
  relay1: string;            // ON | OFF
  relay2: string;            // ON | OFF
  reason: string;            // Human-readable decision reason

  // Impact metrics
  cost_saved: number;        // Estimated cost saving
  co2_reduction: number;     // Estimated CO2 reduction

  // Metadata
  timestamp_source: string;
  timestamp?: string;       // Client/mock timestamp
  received_at?: string;      // Server-added timestamp
}

/**
 * Valid fuel modes (v2)
 */
export type CloudFuelMode = 'PETROL' | 'LPG' | 'CNG';

/**
 * Valid status values (v2)
 */
export type CloudStatus = 'NORMAL' | 'EFFICIENT' | 'HIGH TEMP' | 'LOW FUEL' | 'WARNING';

/**
 * AI Insight response from backend
 */
export interface AIInsightResponse {
  recommendation: string;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  risk_level: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  roadworthiness: string;
  climate_note: string;
  operator_message: string;
  source: 'ai' | 'fallback';
}

export interface FleetSummary {
  total_vehicles: number;
  online_vehicles: number;
  total_cost_saved: number;
  total_co2_reduction: number;
  fuel_mode_distribution: Record<string, number>;
  status_distribution: Record<string, number>;
  last_updated: string;
}
