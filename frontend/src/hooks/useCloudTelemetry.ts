/**
 * Cloud Telemetry Hook
 * 
 * Architecture: Hooks Layer
 * Purpose: React hook for consuming cloud telemetry (v2 schema)
 * 
 * Supports multiple vehicles and fleet-wide monitoring.
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import type { CloudTelemetryMessage, AIInsightResponse, FleetSummary } from '../types/telemetry';
import { fetchCloudTelemetryLatest, fetchCloudTelemetryHistory, fetchAIInsight, checkBackendHealth, fetchFleetSummary } from '../api/telemetryApi';

type CloudMode = 'live' | 'mock' | 'checking';

interface UseCloudTelemetryResult {
  current: CloudTelemetryMessage | null;
  fleet: CloudTelemetryMessage[];
  history: CloudTelemetryMessage[];
  summary: FleetSummary | null;
  isConnected: boolean;
  mode: CloudMode;
  aiInsight: AIInsightResponse | null;
  refreshAIInsight: () => void;
}

const POLL_INTERVAL_MS = 3000;
const AI_REFRESH_INTERVAL_MS = 15000;

const VEHICLE_IDS = ['KKE-001', 'KKE-002', 'BUS-001', 'VAN-001', 'TXI-001'];
const VEHICLE_TYPES: Record<string, any> = {
  'KKE-001': 'keke',
  'KKE-002': 'keke',
  'BUS-001': 'bus',
  'VAN-001': 'company_vehicle',
  'TXI-001': 'taxi'
};

// ============================================================================
// MOCK DATA GENERATOR
// ============================================================================

function generateMockCloudData(vehicle_id: string): CloudTelemetryMessage {
  const type = VEHICLE_TYPES[vehicle_id] || 'keke';
  const temp = 25 + Math.random() * 35;
  const dist = 5 + Math.random() * 25;
  const fuelPct = Math.max(0, Math.min(100, Math.round(((30 - dist) / 25) * 100)));
  const ldr = Math.round(200 + Math.random() * 3800);
  const therm = Math.round(1000 + Math.random() * 3000);

  let fuelMode = 'PETROL';
  let status = 'NORMAL';
  let reason = 'Optimal operating conditions.';
  let costSaved = 0.5 + Math.random() * 0.5;
  let co2 = 0.3 + Math.random() * 0.4;

  if (temp > 55) {
    fuelMode = 'LPG';
    status = 'HIGH TEMP';
    reason = 'High engine temperature detected — switching to LPG for cooler combustion.';
    costSaved = 2.2;
    co2 = 1.4;
  } else if (fuelPct < 20) {
    fuelMode = 'CNG';
    status = 'LOW FUEL';
    reason = 'Low fuel level — engaged CNG reserve for range extension.';
    costSaved = 3.5;
    co2 = 2.1;
  } else if (ldr < 800) {
    fuelMode = 'LPG';
    status = 'EFFICIENT';
    reason = 'Night/low-light mode — LPG optimization active.';
    costSaved = 1.8;
    co2 = 1.1;
  }

  return {
    vehicle_id,
    vehicle_type: type,
    temperature: Math.round(temp * 10) / 10,
    distance_cm: Math.round(dist * 10) / 10,
    fuel_percent: fuelPct,
    ldr,
    thermistor: therm,
    fuel_mode: fuelMode as any,
    status: status as any,
    relay1: temp > 50 ? 'ON' : 'OFF',
    relay2: fuelPct < 25 ? 'ON' : 'OFF',
    reason,
    cost_saved: Math.round(costSaved * 100) / 100,
    co2_reduction: Math.round(co2 * 100) / 100,
    timestamp_source: 'device',
    timestamp: new Date().toISOString(),
  };
}

// ============================================================================
// HOOK
// ============================================================================

export function useCloudTelemetry(): UseCloudTelemetryResult {
  const [current, setCurrent] = useState<CloudTelemetryMessage | null>(null);
  const [fleet, setFleet] = useState<CloudTelemetryMessage[]>([]);
  const [history, setHistory] = useState<CloudTelemetryMessage[]>([]);
  const [summary, setSummary] = useState<FleetSummary | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [mode, setMode] = useState<CloudMode>('checking');
  const [aiInsight, setAiInsight] = useState<AIInsightResponse | null>(null);

  const pollRef = useRef<number | null>(null);
  const aiPollRef = useRef<number | null>(null);
  const mockIntervalRef = useRef<number | null>(null);

  const refreshAIInsight = useCallback(async () => {
    if (!current) return;
    const insight = await fetchAIInsight({
      vehicle_id: current.vehicle_id,
      temperature: current.temperature,
      fuel_percent: current.fuel_percent,
      fuel_mode: current.fuel_mode,
      status: current.status,
      relay1: current.relay1,
      relay2: current.relay2,
      ldr: current.ldr,
      thermistor: current.thermistor,
      reason: current.reason,
    });
    if (insight) setAiInsight(insight);
  }, [current]);

  useEffect(() => {
    let mounted = true;

    async function initialize() {
      const backendOk = await checkBackendHealth();
      if (!mounted) return;

      if (backendOk) {
        const latest = await fetchCloudTelemetryLatest();
        if (latest && mounted) {
          setMode('live');
          setIsConnected(true);
          setCurrent(latest);
          startLivePolling();
          return;
        }
      }

      setMode('mock');
      setIsConnected(true);
      startMockMode();
    }

    function startLivePolling() {
      pollRef.current = window.setInterval(async () => {
        try {
          const latest = await fetchCloudTelemetryLatest();
          if (latest) {
            setCurrent(latest);
            const hist = await fetchCloudTelemetryHistory(50);
            setHistory(hist);
            const fleetSum = await fetchFleetSummary();
            setSummary(fleetSum);
            
            // In live mode, we'd fetch all vehicles, but for demo we simulate the fleet list
            setFleet(VEHICLE_IDS.map(id => generateMockCloudData(id)));
          }
        } catch {}
      }, POLL_INTERVAL_MS);

      aiPollRef.current = window.setInterval(() => {
        refreshAIInsight();
      }, AI_REFRESH_INTERVAL_MS);
    }

    function startMockMode() {
      const initialFleet = VEHICLE_IDS.map(id => generateMockCloudData(id));
      setFleet(initialFleet);
      setCurrent(initialFleet[0]);
      setHistory([initialFleet[0]]);

      setSummary({
        total_vehicles: VEHICLE_IDS.length,
        online_vehicles: VEHICLE_IDS.length,
        total_cost_saved: 1250.40,
        total_co2_reduction: 184.2,
        fuel_mode_distribution: { "PETROL": 2, "LPG": 2, "CNG": 1 },
        status_distribution: { "NORMAL": 3, "EFFICIENT": 1, "HIGH TEMP": 1 },
        last_updated: new Date().toISOString()
      });

      mockIntervalRef.current = window.setInterval(() => {
        const updatedFleet = VEHICLE_IDS.map(id => generateMockCloudData(id));
        setFleet(updatedFleet);
        setCurrent(updatedFleet[0]);
        setHistory(prev => [...prev.slice(-49), updatedFleet[0]]);
      }, POLL_INTERVAL_MS);
    }

    initialize();

    return () => {
      mounted = false;
      if (pollRef.current) clearInterval(pollRef.current);
      if (aiPollRef.current) clearInterval(aiPollRef.current);
      if (mockIntervalRef.current) clearInterval(mockIntervalRef.current);
    };
  }, []);

  return { current, fleet, history, summary, isConnected, mode, aiInsight, refreshAIInsight };
}
