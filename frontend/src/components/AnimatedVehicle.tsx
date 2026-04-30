/**
 * Fuel Mode Indicator Component
 * 
 * Professional fuel mode visualization with smooth transitions
 * Supports: CNG, Petrol, LPG
 */

import { useEffect, useState } from 'react';
import type { TelemetryMessage } from '../types/telemetry';

interface AnimatedVehicleProps {
  current: TelemetryMessage;
}

export function AnimatedVehicle({ current }: AnimatedVehicleProps) {
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [prevFuelMode, setPrevFuelMode] = useState(current.current_fuel_mode);

  // Detect fuel mode changes and trigger transition
  useEffect(() => {
    if (prevFuelMode !== current.current_fuel_mode) {
      setIsTransitioning(true);
      setTimeout(() => setIsTransitioning(false), 600);
      setPrevFuelMode(current.current_fuel_mode);
    }
  }, [current.current_fuel_mode, prevFuelMode]);

  const fuelConfig = getFuelConfig(current.current_fuel_mode);

  return (
    <div className="fuel-mode-display">
      <div className={`fuel-mode-card ${isTransitioning ? 'transitioning' : ''}`}>
        {/* Header */}
        <div className="fuel-mode-header">
          <h3>Active Fuel Mode</h3>
          {isTransitioning && (
            <span className="transition-badge">Switching...</span>
          )}
        </div>

        {/* Main fuel indicator */}
        <div className={`fuel-indicator ${fuelConfig.className}`}>
          <div className="fuel-icon-large">{fuelConfig.icon}</div>
          <div className="fuel-name-large">{fuelConfig.name}</div>
          <div className="fuel-type-label">{fuelConfig.fullName}</div>
        </div>

        {/* Metrics grid */}
        <div className="fuel-metrics">
          <div className="metric">
            <div className="metric-label">Efficiency</div>
            <div className="metric-value" style={{ color: fuelConfig.color }}>
              {fuelConfig.efficiency}
            </div>
          </div>
          <div className="metric">
            <div className="metric-label">Emissions</div>
            <div className="metric-value" style={{ color: fuelConfig.emissionColor }}>
              {fuelConfig.emissions}
            </div>
          </div>
          <div className="metric">
            <div className="metric-label">Cost/Unit</div>
            <div className="metric-value">{fuelConfig.cost}</div>
          </div>
        </div>

        {/* Status bar */}
        <div className="fuel-status-bar">
          <div 
            className="fuel-status-fill" 
            style={{ 
              backgroundColor: fuelConfig.color,
              width: fuelConfig.efficiency
            }}
          />
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// Helper Functions
// ============================================================================

interface FuelConfig {
  name: string;
  fullName: string;
  icon: string;
  className: string;
  color: string;
  emissionColor: string;
  efficiency: string;
  emissions: string;
  cost: string;
}

function getFuelConfig(fuelMode: string): FuelConfig {
  const configs: Record<string, FuelConfig> = {
    cng: {
      name: 'CNG',
      fullName: 'Compressed Natural Gas',
      icon: '💨',
      className: 'fuel-cng',
      color: '#10b981',
      emissionColor: '#34d399',
      efficiency: '85%',
      emissions: 'Low',
      cost: '₹60/kg',
    },
    petrol: {
      name: 'Petrol',
      fullName: 'Gasoline',
      icon: '⛽',
      className: 'fuel-petrol',
      color: '#f59e0b',
      emissionColor: '#fbbf24',
      efficiency: '75%',
      emissions: 'Medium',
      cost: '₹100/L',
    },
    lpg: {
      name: 'LPG',
      fullName: 'Liquefied Petroleum Gas',
      icon: '🔥',
      className: 'fuel-lpg',
      color: '#3b82f6',
      emissionColor: '#60a5fa',
      efficiency: '80%',
      emissions: 'Low-Med',
      cost: '₹75/L',
    },
    // Fallback for old fuel modes
    diesel: {
      name: 'Diesel',
      fullName: 'Diesel Fuel',
      icon: '🛢️',
      className: 'fuel-diesel',
      color: '#78716c',
      emissionColor: '#a8a29e',
      efficiency: '70%',
      emissions: 'High',
      cost: '₹90/L',
    },
    biodiesel: {
      name: 'Biodiesel',
      fullName: 'Biodiesel Blend',
      icon: '🌿',
      className: 'fuel-biodiesel',
      color: '#84cc16',
      emissionColor: '#a3e635',
      efficiency: '82%',
      emissions: 'Low',
      cost: '₹85/L',
    },
    mixed: {
      name: 'Mixed',
      fullName: 'Mixed Fuel Blend',
      icon: '🔄',
      className: 'fuel-mixed',
      color: '#a855f7',
      emissionColor: '#c084fc',
      efficiency: '78%',
      emissions: 'Medium',
      cost: '₹88/L',
    },
  };

  return configs[fuelMode.toLowerCase()] || configs.petrol;
}
