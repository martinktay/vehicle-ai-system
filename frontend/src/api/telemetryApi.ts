/**
 * Telemetry API Client
 * 
 * Architecture: API layer
 * Purpose: Fetch telemetry data from backend bridge service
 * 
 * This module provides API clients for both:
 * - v1 (serial/simulator) endpoints: /api/latest, /api/history
 * - v2 (cloud/Arduino) endpoints: /api/telemetry/latest, /api/telemetry/history
 * - AI insight endpoint: /api/ai-insight
 */

import type { TelemetryMessage, CloudTelemetryMessage, AIInsightResponse, FleetSummary } from '../types/telemetry';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface BackendHealth {
  status: string;
  mode?: 'serial' | 'simulator' | string;
  telemetry_available?: boolean;
  fleet_size?: number;
  ingestion_connected?: boolean;
}

// ============================================================================
// v1 ENDPOINTS — Serial / Simulator Pipeline
// ============================================================================

/**
 * Fetch the latest telemetry message from backend (v1)
 */
export async function fetchLatestTelemetry(): Promise<TelemetryMessage | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/latest`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) return null;
    return await response.json() as TelemetryMessage;
  } catch {
    return null;
  }
}

/**
 * Fetch telemetry history from backend (v1)
 */
export async function fetchTelemetryHistory(limit?: number): Promise<TelemetryMessage[]> {
  try {
    const url = limit 
      ? `${API_BASE_URL}/history?limit=${limit}`
      : `${API_BASE_URL}/history`;
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) return [];
    return await response.json() as TelemetryMessage[];
  } catch {
    return [];
  }
}

/**
 * Check if backend is available
 */
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Fetch backend health details, including active ingestion mode.
 */
export async function fetchBackendHealth(): Promise<BackendHealth | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) return null;
    return await response.json() as BackendHealth;
  } catch {
    return null;
  }
}

// ============================================================================
// v2 ENDPOINTS — Cloud / Arduino Pipeline
// ============================================================================

/**
 * Fetch the latest cloud telemetry (v2) from backend
 */
export async function fetchCloudTelemetryLatest(vehicle_id?: string): Promise<CloudTelemetryMessage | null> {
  try {
    const url = vehicle_id 
      ? `${API_BASE_URL}/telemetry/latest?vehicle_id=${vehicle_id}`
      : `${API_BASE_URL}/telemetry/latest`;
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) return null;
    const data = await response.json();
    if (data.status === "no_data") return null;
    return data as CloudTelemetryMessage;
  } catch {
    return null;
  }
}

/**
 * Fetch cloud telemetry history (v2) from backend
 */
export async function fetchCloudTelemetryHistory(limit?: number): Promise<CloudTelemetryMessage[]> {
  try {
    const url = limit
      ? `${API_BASE_URL}/telemetry/history?limit=${limit}`
      : `${API_BASE_URL}/telemetry/history`;
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) return [];
    return await response.json() as CloudTelemetryMessage[];
  } catch {
    return [];
  }
}

// ============================================================================
// AI INSIGHT ENDPOINT
// ============================================================================

/**
 * Fetch AI insight from backend
 */
export async function fetchAIInsight(data: {
  vehicle_id: string;
  temperature: number;
  fuel_percent: number;
  fuel_mode: string;
  status: string;
  relay1: string;
  relay2: string;
  ldr: number;
  thermistor: number;
  reason: string;
}): Promise<AIInsightResponse | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/ai-insight`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) return null;
    return await response.json() as AIInsightResponse;
  } catch {
    return null;
  }
}
/**
 * Fetch fleet-level summary metrics
 */
export async function fetchFleetSummary(): Promise<FleetSummary | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/fleet/summary`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) return null;
    return await response.json() as FleetSummary;
  } catch {
    return null;
  }
}
