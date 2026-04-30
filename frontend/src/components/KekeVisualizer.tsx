/**
 * Premium Vehicle Visualizer
 * 
 * A minimal, professional SVG-based visualization for transport AI system.
 * Displays fuel mode, engine heat, and vehicle state with subtle animations.
 * 
 * Design: Dashboard-grade, technical aesthetic
 * Style: Minimal, clean, restrained
 * Colors: Muted palette, soft accents
 * 
 * Supports multiple vehicle types through configuration system.
 */

import { useEffect, useState } from 'react';
import type { TelemetryMessage } from '../types/telemetry';
import type { VehicleType } from '../types/vehicle';
import { getVehicleConfig } from '../config/vehicleConfigs';

interface KekeVisualizerProps {
  current: TelemetryMessage;
  scenario?: string;
  className?: string;
  vehicleType?: VehicleType;
}

export function KekeVisualizer({ current, scenario, className = '', vehicleType = 'keke' }: KekeVisualizerProps) {
  const [isSwitching, setIsSwitching] = useState(false);
  const [prevFuelMode, setPrevFuelMode] = useState(current.current_fuel_mode);

  // Get vehicle configuration
  const config = getVehicleConfig(vehicleType);

  // Detect fuel mode changes
  useEffect(() => {
    if (prevFuelMode !== current.current_fuel_mode) {
      setIsSwitching(true);
      const timer = setTimeout(() => setIsSwitching(false), 600);
      setPrevFuelMode(current.current_fuel_mode);
      return () => clearTimeout(timer);
    }
  }, [current.current_fuel_mode, prevFuelMode]);

  // Compute derived state
  const fuelMode = current.current_fuel_mode.toLowerCase();
  const heatLevel = getHeatLevel(current.engine_temperature, current.overheat_flag);
  const isMoving = current.system_status !== 'fail_safe';
  const statusMessage = getStatusMessage(current);
  const fuelColor = getFuelColor(fuelMode);

  return (
    <div className={`keke-visualizer-container ${className}`}>
      <svg
        viewBox={`0 0 ${config.viewBox.width} ${config.viewBox.height}`}
        className="keke-visualizer"
        role="img"
        aria-label={`${config.name} vehicle status visualizer`}
      >
        <title>Vehicle Status - {config.name}</title>
        <desc>Shows current fuel mode, engine heat, and driving state</desc>

        {/* Definitions */}
        <defs>
          {/* Road pattern */}
          <pattern id="road-grid" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
            <line x1="0" y1="50" x2="100" y2="50" stroke="#4a5568" strokeWidth="1" opacity="0.3" />
            <line x1="0" y1="80" x2="100" y2="80" stroke="#4a5568" strokeWidth="0.5" opacity="0.2" />
          </pattern>

          {/* Heat glow gradients */}
          <radialGradient id="heat-glow-low">
            <stop offset="0%" stopColor="#78716c" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#78716c" stopOpacity="0" />
          </radialGradient>
          <radialGradient id="heat-glow-medium">
            <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
          </radialGradient>
          <radialGradient id="heat-glow-high">
            <stop offset="0%" stopColor="#dc2626" stopOpacity="0.7" />
            <stop offset="100%" stopColor="#dc2626" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* Layer 1: Background */}
        <g id="background-layer" className="background">
          <rect
            x="0"
            y="300"
            width="800"
            height="100"
            fill="url(#road-grid)"
            className={`road-surface ${isMoving ? 'moving' : ''}`}
          />
        </g>

        {/* Layer 4: Engine/Thermal Zone (behind vehicle, positioned at engine) */}
        <g id="thermal-layer" className="thermal-zone" transform={config.bodyTransform || ''}>
          <circle
            cx={config.engineZone.x}
            cy={config.engineZone.y}
            r={heatLevel === 'high' ? config.engineZone.radiusHigh : heatLevel === 'medium' ? config.engineZone.radiusMedium : config.engineZone.radiusLow}
            fill={`url(#heat-glow-${heatLevel})`}
            className={`heat-glow heat-${heatLevel}`}
          />
        </g>

        {/* Layer 2: Vehicle Body */}
        <g id="vehicle-body-layer" className="vehicle-body" transform={config.bodyTransform || ''}>
          {/* Main body silhouette */}
          <path
            d={config.body.body}
            fill="#2d3748"
            className="keke-body"
          />
          
          {/* Cabin window (if defined) */}
          {config.body.cabin && (
            <path
              d={config.body.cabin}
              fill="#1a202c"
              opacity="0.6"
              className="cabin-window"
            />
          )}
          
          {/* Roof accent line (if defined) */}
          {config.body.roofAccent && (
            <path
              d={config.body.roofAccent}
              stroke="#4a5568"
              strokeWidth="2"
              fill="none"
              className="roof-accent"
            />
          )}

          {/* Headlight (if defined) */}
          {config.body.headlight && (
            <circle 
              cx={config.body.headlight.cx} 
              cy={config.body.headlight.cy} 
              r={config.body.headlight.r} 
              fill="#4a5568" 
              opacity="0.5" 
              className="headlight" 
            />
          )}

          {/* Internal Fuel System Components (INSIDE vehicle body) */}
          <g className="fuel-system-internal">
            {/* Fuel Tank Visual (rear of vehicle) */}
            <rect
              x="20"
              y="85"
              width="35"
              height="20"
              rx="3"
              fill="#1a202c"
              stroke="#4a5568"
              strokeWidth="1.5"
              opacity="0.7"
              className="fuel-tank"
            />
            
            {/* Engine Compartment Visual (front of vehicle) */}
            <rect
              x="295"
              y="60"
              width="30"
              height="35"
              rx="2"
              fill="#1a202c"
              stroke="#78716c"
              strokeWidth="1.5"
              opacity="0.6"
              className="engine-compartment"
            />
            
            {/* Engine block detail */}
            <rect
              x="300"
              y="65"
              width="20"
              height="25"
              rx="1"
              fill="#2d3748"
              stroke="#78716c"
              strokeWidth="1"
              opacity="0.8"
              className="engine-block"
            />
          </g>
        </g>

        {/* Layer 3: Wheels */}
        <g id="wheel-layer" className={`wheels ${isMoving ? 'rotating' : ''}`}>
          {config.wheels.map((wheel, index) => (
            <g key={index} className="wheel" transform={`translate(${wheel.x}, ${wheel.y})`}>
              <circle cx="0" cy="0" r={wheel.radius} fill="#1a202c" stroke="#4a5568" strokeWidth="3" />
              <circle cx="0" cy="0" r={wheel.radius * 0.3} fill="#2d3748" />
              <line x1={-wheel.radius * 0.7} y1="0" x2={wheel.radius * 0.7} y2="0" stroke="#4a5568" strokeWidth="2" />
              <line x1="0" y1={-wheel.radius * 0.7} x2="0" y2={wheel.radius * 0.7} stroke="#4a5568" strokeWidth="2" />
            </g>
          ))}
        </g>

        {/* Layer 5: Energy Source Nodes (INSIDE vehicle body) */}
        <g id="energy-nodes-layer" className="energy-nodes" transform={config.bodyTransform || ''}>
          {config.fuelNodes.map((node, index) => {
            const nodeFuelType = index === 0 ? 'petrol' : index === 1 ? 'cng' : 'lpg';
            const isActive = fuelMode === nodeFuelType;
            const nodeColor = getFuelColor(nodeFuelType);
            
            return (
              <g key={index} className={`node ${isActive ? 'node-active' : 'node-inactive'}`}>
                {/* Fuel source container/tank */}
                <circle
                  cx={node.x}
                  cy={node.y}
                  r={node.radius + 2}
                  fill="#1a202c"
                  stroke={nodeColor}
                  strokeWidth="2"
                  opacity="0.8"
                  className="node-outer"
                />
                {/* Active fuel indicator */}
                <circle
                  cx={node.x}
                  cy={node.y}
                  r={node.radius * 0.6}
                  fill={nodeColor}
                  className="node-inner"
                />
                {/* Fuel type label */}
                <text
                  x={node.x}
                  y={node.y + 4}
                  textAnchor="middle"
                  fill="#e2e8f0"
                  fontSize="9"
                  fontWeight="700"
                  className="node-label-internal"
                >
                  {node.label}
                </text>
              </g>
            );
          })}
        </g>

        {/* Layer 6: Energy Flow Paths (INSIDE vehicle body - realistic fuel lines) */}
        <g id="flow-paths-layer" className="flow-paths" transform={config.bodyTransform || ''}>
          {config.fuelNodes.map((node, index) => {
            const nodeFuelType = index === 0 ? 'petrol' : index === 1 ? 'cng' : 'lpg';
            const isActive = fuelMode === nodeFuelType;
            const nodeColor = getFuelColor(nodeFuelType);
            
            // Calculate realistic internal fuel line path from node to engine zone
            // Route through the vehicle interior with proper curves
            const midX = (node.x + config.engineZone.x) / 2;
            const controlY = node.y - 15; // Route slightly upward for realistic piping
            const pathData = `M ${node.x},${node.y} Q ${midX},${controlY} ${config.engineZone.x},${config.engineZone.y}`;
            
            return (
              <g key={index} className="fuel-line-group">
                {/* Fuel line pipe (background) */}
                <path
                  d={pathData}
                  stroke="#1a202c"
                  strokeWidth="5"
                  fill="none"
                  opacity="0.6"
                  className="fuel-pipe-bg"
                />
                {/* Fuel line (colored, animated when active) */}
                <path
                  d={pathData}
                  stroke={nodeColor}
                  strokeWidth="3"
                  fill="none"
                  strokeDasharray="8 4"
                  opacity={isActive ? 0.9 : 0.2}
                  className={`flow-path ${isActive ? 'flow-active' : 'flow-inactive'}`}
                />
              </g>
            );
          })}
        </g>

        {/* Layer 7: Status Text */}
        <g id="status-text-layer" className="status-text-layer">
          <text
            x={config.statusText.x}
            y={config.statusText.y}
            fill="#e2e8f0"
            fontSize="14"
            fontWeight="500"
            className="status-text"
          >
            {statusMessage}
          </text>
          {isSwitching && (
            <text
              x={config.statusText.x}
              y={config.statusText.y + 20}
              fill={fuelColor}
              fontSize="12"
              fontWeight="400"
              className="switching-indicator"
            >
              Switching...
            </text>
          )}
        </g>

        {/* Layer 8: Scenario Label */}
        {scenario && (
          <g id="scenario-label-layer" className="scenario-label-layer">
            <text
              x={config.scenarioLabel.x}
              y={config.scenarioLabel.y}
              fill="#94a3b8"
              fontSize="12"
              fontWeight="400"
              textAnchor="end"
              className="scenario-label"
            >
              {scenario}
            </text>
          </g>
        )}
      </svg>

      {/* Fuel mode details */}
      <div className="fuel-details">
        <div className="fuel-badge" style={{ borderColor: fuelColor }}>
          <span className="fuel-icon" style={{ color: fuelColor }}>
            {getFuelIcon(fuelMode)}
          </span>
          <span className="fuel-name">{fuelMode.toUpperCase()}</span>
        </div>
        <div className="heat-indicator">
          <span className="heat-label">Heat:</span>
          <span className="heat-value" style={{ color: getHeatColor(heatLevel) }}>
            {current.engine_temperature}°C
          </span>
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// Helper Functions
// ============================================================================

function getHeatLevel(temperature: number, overheatFlag: boolean): 'low' | 'medium' | 'high' {
  if (overheatFlag || temperature > 100) return 'high';
  if (temperature > 80) return 'medium';
  return 'low';
}

function getStatusMessage(telemetry: TelemetryMessage): string {
  if (telemetry.overheat_flag) return 'Overheat Alert';
  if (telemetry.system_status === 'fail_safe') return 'Fail-Safe Active';
  
  const rec = telemetry.ai_recommendation.toLowerCase();
  if (rec.includes('switch_to_cng') || rec.includes('cng')) return 'Switching to CNG';
  if (rec.includes('switch_to_lpg') || rec.includes('lpg')) return 'Switching to LPG';
  if (rec.includes('switch_to_petrol') || rec.includes('petrol')) return 'Switching to Petrol';
  
  const mode = telemetry.current_fuel_mode.toUpperCase();
  return `${mode} Active`;
}

function getFuelColor(fuelMode: string): string {
  const colors: Record<string, string> = {
    petrol: '#d97706',
    cng: '#059669',
    lpg: '#2563eb',
    diesel: '#78716c',
    biodiesel: '#84cc16',
    mixed: '#a855f7',
  };
  return colors[fuelMode] || colors.petrol;
}

function getFuelIcon(fuelMode: string): string {
  const icons: Record<string, string> = {
    petrol: '⛽',
    cng: '💨',
    lpg: '🔥',
    diesel: '🛢️',
    biodiesel: '🌿',
    mixed: '🔄',
  };
  return icons[fuelMode] || icons.petrol;
}

function getHeatColor(heatLevel: string): string {
  const colors: Record<string, string> = {
    low: '#78716c',
    medium: '#f59e0b',
    high: '#dc2626',
  };
  return colors[heatLevel] || colors.low;
}
