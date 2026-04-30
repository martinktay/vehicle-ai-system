/**
 * Vehicle Configuration Types
 * 
 * Defines the structure for different vehicle types (Keke, Bus, Motorcycle, SUV, Van)
 * to enable reusable vehicle visualizer component.
 */

export type VehicleType = 'keke' | 'bus' | 'motorcycle' | 'suv' | 'van';

export interface WheelPosition {
  x: number;
  y: number;
  radius: number;
}

export interface EngineZone {
  x: number;
  y: number;
  radiusLow: number;
  radiusMedium: number;
  radiusHigh: number;
}

export interface FuelNodePosition {
  x: number;
  y: number;
  radius: number;
  label: string;
}

export interface VehicleBodyPath {
  /** Main body silhouette path (SVG path data) */
  body: string;
  /** Cabin/window path (optional) */
  cabin?: string;
  /** Roof accent path (optional) */
  roofAccent?: string;
  /** Headlight position */
  headlight?: { cx: number; cy: number; r: number };
}

export interface VehicleConfig {
  type: VehicleType;
  name: string;
  
  /** SVG viewBox dimensions */
  viewBox: {
    width: number;
    height: number;
  };
  
  /** Vehicle body paths and shapes */
  body: VehicleBodyPath;
  
  /** Wheel positions (front, rear, or multiple) */
  wheels: WheelPosition[];
  
  /** Engine/thermal zone configuration */
  engineZone: EngineZone;
  
  /** Fuel node positions (Petrol, CNG, LPG) */
  fuelNodes: FuelNodePosition[];
  
  /** Status text position */
  statusText: { x: number; y: number };
  
  /** Scenario label position */
  scenarioLabel: { x: number; y: number };
  
  /** Vehicle-specific transform for body group */
  bodyTransform?: string;
}

