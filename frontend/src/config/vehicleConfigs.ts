/**
 * Vehicle Configurations
 * 
 * Defines specific configurations for each vehicle type.
 * Currently implemented: Keke
 * Future: Bus, Motorcycle, SUV, Delivery Van
 */

import type { VehicleConfig } from '../types/vehicle';

/**
 * Keke (Auto-Rickshaw) Configuration
 * 
 * Three-wheeled vehicle common in Nigerian urban transport.
 * Compact design with open/semi-enclosed cabin.
 * Realistic fuel system routing from tank (rear) to engine (front).
 */
export const kekeConfig: VehicleConfig = {
  type: 'keke',
  name: 'Keke',
  
  viewBox: {
    width: 900,
    height: 450,
  },
  
  body: {
    // Main body silhouette (side profile) - more detailed and realistic
    body: 'M 10,100 L 10,50 Q 10,35 25,35 L 90,35 L 115,15 L 200,15 L 225,35 L 320,35 Q 335,35 335,50 L 335,100 L 320,100 L 10,100 Z',
    
    // Cabin window - larger and more prominent
    cabin: 'M 105,40 L 125,20 L 195,20 L 215,40 L 195,40 L 125,40 Z',
    
    // Roof accent line
    roofAccent: 'M 100,35 L 120,18 L 195,18 L 215,35',
    
    // Headlight - more prominent
    headlight: { cx: 325, cy: 65, r: 6 },
  },
  
  wheels: [
    // Rear wheel (larger, more detailed)
    { x: 110, y: 330, radius: 42 },
    // Front wheel
    { x: 510, y: 330, radius: 42 },
  ],
  
  engineZone: {
    // Engine at front (realistic for Keke) - INSIDE vehicle body
    x: 505,
    y: 175,
    radiusLow: 35,
    radiusMedium: 42,
    radiusHigh: 50,
  },
  
  fuelNodes: [
    // Fuel tank at rear INSIDE vehicle body - Petrol
    { x: 235, y: 185, radius: 12, label: 'P' },
    // CNG cylinder (under seat area) INSIDE vehicle body
    { x: 360, y: 180, radius: 12, label: 'C' },
    // LPG tank (rear, slightly offset) INSIDE vehicle body
    { x: 270, y: 170, radius: 12, label: 'L' },
  ],
  
  statusText: { x: 60, y: 60 },
  
  scenarioLabel: { x: 840, y: 60 },
  
  bodyTransform: 'translate(200, 100)',
};

/**
 * Bus Configuration (Future Implementation)
 * 
 * Larger vehicle with multiple axles and passenger capacity.
 */
export const busConfig: VehicleConfig = {
  type: 'bus',
  name: 'Bus',
  
  viewBox: {
    width: 800,
    height: 400,
  },
  
  body: {
    // Placeholder - to be implemented
    body: 'M 0,100 L 0,40 L 400,40 L 400,100 Z',
  },
  
  wheels: [
    { x: 150, y: 280, radius: 40 },
    { x: 350, y: 280, radius: 40 },
    { x: 550, y: 280, radius: 40 },
  ],
  
  engineZone: {
    x: 200,
    y: 240,
    radiusLow: 60,
    radiusMedium: 70,
    radiusHigh: 80,
  },
  
  fuelNodes: [
    { x: 250, y: 320, radius: 14, label: 'P' },
    { x: 300, y: 320, radius: 14, label: 'C' },
    { x: 350, y: 320, radius: 14, label: 'L' },
  ],
  
  statusText: { x: 50, y: 50 },
  scenarioLabel: { x: 750, y: 50 },
  bodyTransform: 'translate(150, 125)',
};

/**
 * Motorcycle Configuration (Future Implementation)
 * 
 * Two-wheeled vehicle with single rider.
 */
export const motorcycleConfig: VehicleConfig = {
  type: 'motorcycle',
  name: 'Motorcycle',
  
  viewBox: {
    width: 800,
    height: 400,
  },
  
  body: {
    // Placeholder - to be implemented
    body: 'M 0,60 L 0,40 L 200,40 L 200,60 Z',
  },
  
  wheels: [
    { x: 300, y: 280, radius: 35 },
    { x: 500, y: 280, radius: 35 },
  ],
  
  engineZone: {
    x: 400,
    y: 240,
    radiusLow: 45,
    radiusMedium: 55,
    radiusHigh: 65,
  },
  
  fuelNodes: [
    { x: 350, y: 320, radius: 10, label: 'P' },
    { x: 385, y: 320, radius: 10, label: 'C' },
    { x: 420, y: 320, radius: 10, label: 'L' },
  ],
  
  statusText: { x: 50, y: 50 },
  scenarioLabel: { x: 750, y: 50 },
  bodyTransform: 'translate(250, 140)',
};

/**
 * SUV Configuration (Future Implementation)
 * 
 * Four-wheeled enclosed vehicle with larger cabin.
 */
export const suvConfig: VehicleConfig = {
  type: 'suv',
  name: 'SUV',
  
  viewBox: {
    width: 800,
    height: 400,
  },
  
  body: {
    // Placeholder - to be implemented
    body: 'M 0,80 L 0,30 L 350,30 L 350,80 Z',
  },
  
  wheels: [
    { x: 280, y: 280, radius: 38 },
    { x: 520, y: 280, radius: 38 },
  ],
  
  engineZone: {
    x: 350,
    y: 240,
    radiusLow: 55,
    radiusMedium: 65,
    radiusHigh: 75,
  },
  
  fuelNodes: [
    { x: 300, y: 320, radius: 12, label: 'P' },
    { x: 340, y: 320, radius: 12, label: 'C' },
    { x: 380, y: 320, radius: 12, label: 'L' },
  ],
  
  statusText: { x: 50, y: 50 },
  scenarioLabel: { x: 750, y: 50 },
  bodyTransform: 'translate(200, 125)',
};

/**
 * Delivery Van Configuration (Future Implementation)
 * 
 * Commercial vehicle with cargo area.
 */
export const vanConfig: VehicleConfig = {
  type: 'van',
  name: 'Delivery Van',
  
  viewBox: {
    width: 800,
    height: 400,
  },
  
  body: {
    // Placeholder - to be implemented
    body: 'M 0,90 L 0,30 L 380,30 L 380,90 Z',
  },
  
  wheels: [
    { x: 270, y: 280, radius: 38 },
    { x: 530, y: 280, radius: 38 },
  ],
  
  engineZone: {
    x: 320,
    y: 240,
    radiusLow: 55,
    radiusMedium: 65,
    radiusHigh: 75,
  },
  
  fuelNodes: [
    { x: 280, y: 320, radius: 12, label: 'P' },
    { x: 320, y: 320, radius: 12, label: 'C' },
    { x: 360, y: 320, radius: 12, label: 'L' },
  ],
  
  statusText: { x: 50, y: 50 },
  scenarioLabel: { x: 750, y: 50 },
  bodyTransform: 'translate(180, 125)',
};

/**
 * Get vehicle configuration by type
 */
export function getVehicleConfig(type: string): VehicleConfig {
  const configs: Record<string, VehicleConfig> = {
    keke: kekeConfig,
    bus: busConfig,
    motorcycle: motorcycleConfig,
    suv: suvConfig,
    van: vanConfig,
  };
  
  return configs[type.toLowerCase()] || kekeConfig;
}

/**
 * Get all available vehicle types
 */
export function getAvailableVehicleTypes(): string[] {
  return ['keke', 'bus', 'motorcycle', 'suv', 'van'];
}

