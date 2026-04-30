/**
 * Mock Telemetry Generator
 * 
 * Architecture: Data Layer
 * Purpose: Generate realistic telemetry data for demo mode
 * 
 * This module produces simulated sensor data conforming to Telemetry Data Contract v1.
 * It generates realistic temperature ranges, valid state transitions, and smooth
 * value changes (not random jumps).
 * 
 * Design principle: Edge-Intelligence First
 * - All decision logic (ai_recommendation, relay states) is simulated here
 * - In production, these values come from the ESP32 Edge Controller
 * - The dashboard never computes these values, only displays them
 */

import type { 
  TelemetryMessage, 
  FuelMode, 
  AIRecommendation
} from '../types/telemetry';

interface MockState {
  engineTemp: number;
  fuelLineTemp: number;
  ambientTemp: number;
  fuelMode: FuelMode;
  relay1: boolean;
  relay2: boolean;
  overheat: boolean;
}

class MockTelemetryGenerator {
  private state: MockState;
  private intervalId: number | null = null;
  private listeners: Array<(message: TelemetryMessage) => void> = [];

  constructor() {
    // Initialize with realistic starting values
    this.state = {
      engineTemp: 75,
      fuelLineTemp: 55,
      ambientTemp: 25,
      fuelMode: 'petrol',
      relay1: false,
      relay2: false,
      overheat: false,
    };
  }

  /**
   * Start generating telemetry every 2 seconds
   */
  start(): void {
    if (this.intervalId !== null) return;

    this.intervalId = window.setInterval(() => {
      this.updateState();
      const message = this.generateMessage();
      this.notifyListeners(message);
    }, 2000);

    // Send initial message immediately
    const initialMessage = this.generateMessage();
    this.notifyListeners(initialMessage);
  }

  /**
   * Stop generating telemetry
   */
  stop(): void {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  /**
   * Subscribe to telemetry updates
   * Returns unsubscribe function
   */
  subscribe(callback: (message: TelemetryMessage) => void): () => void {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  /**
   * Update internal state with realistic transitions
   */
  private updateState(): void {
    // Simulate temperature drift (small random changes)
    this.state.engineTemp += this.randomDrift(-2, 2);
    this.state.fuelLineTemp += this.randomDrift(-1.5, 1.5);
    this.state.ambientTemp += this.randomDrift(-0.5, 0.5);

    // Clamp to realistic ranges
    this.state.engineTemp = this.clamp(this.state.engineTemp, 60, 120);
    this.state.fuelLineTemp = this.clamp(this.state.fuelLineTemp, 40, 100);
    this.state.ambientTemp = this.clamp(this.state.ambientTemp, 15, 45);

    // Check overheat condition
    this.state.overheat = this.state.engineTemp > 100;

    // Simulate occasional fuel mode changes (10% chance - increased for demo visibility)
    if (Math.random() < 0.10) {
      this.state.fuelMode = this.randomFuelMode();
    }

    // Simulate relay switching based on temperature (simple logic)
    this.state.relay1 = this.state.engineTemp > 90;
    this.state.relay2 = this.state.fuelLineTemp > 80;
  }

  /**
   * Generate a telemetry message from current state
   */
  private generateMessage(): TelemetryMessage {
    return {
      timestamp: new Date().toISOString(),
      engine_temperature: Math.round(this.state.engineTemp * 10) / 10,
      fuel_line_temperature: Math.round(this.state.fuelLineTemp * 10) / 10,
      ambient_temperature: Math.round(this.state.ambientTemp * 10) / 10,
      current_fuel_mode: this.state.fuelMode,
      ai_recommendation: this.computeAIRecommendation(),
      relay_state_1: this.state.relay1,
      relay_state_2: this.state.relay2,
      overheat_flag: this.state.overheat,
      system_status: this.state.overheat ? 'fail_safe' : 'demo_mode',
      network_status: 'disconnected',
      power_source: 'battery',
    };
  }

  /**
   * Compute AI recommendation based on current state
   * (In production, this logic lives on the ESP32)
   */
  private computeAIRecommendation(): AIRecommendation {
    if (this.state.overheat) {
      return 'activate_cooling';
    }
    if (this.state.engineTemp > 95) {
      return 'reduce_load';
    }
    if (this.state.engineTemp < 80 && (this.state.fuelMode === 'petrol' || this.state.fuelMode === 'diesel')) {
      return 'switch_to_biodiesel'; // Recommend switching to cleaner fuel
    }
    return 'maintain';
  }

  /**
   * Notify all subscribers of new message
   */
  private notifyListeners(message: TelemetryMessage): void {
    this.listeners.forEach(callback => callback(message));
  }

  /**
   * Generate random drift within range
   */
  private randomDrift(min: number, max: number): number {
    return Math.random() * (max - min) + min;
  }

  /**
   * Clamp value to range
   */
  private clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  }

  /**
   * Select random fuel mode (weighted towards CNG/LPG for Nigerian context)
   */
  private randomFuelMode(): FuelMode {
    const modes: FuelMode[] = ['cng', 'petrol', 'lpg', 'cng', 'lpg']; // CNG and LPG appear more frequently
    return modes[Math.floor(Math.random() * modes.length)];
  }
}

// Export singleton instance
export const mockTelemetry = new MockTelemetryGenerator();
