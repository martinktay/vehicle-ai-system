"""
Mock Telemetry Simulator

Architecture: Data ingestion layer
Purpose: Generate realistic telemetry for demo mode

This module simulates the ESP32 Edge Controller by generating
realistic telemetry data with smooth transitions and valid state changes.

Design principle: Edge-Intelligence First
- All decision logic (ai_recommendation, relay states) is simulated here
- In production, these values come from the ESP32 Edge Controller
- The bridge service never computes these values, only forwards them
"""

import asyncio
import random
from datetime import datetime
from typing import Optional
from app.schemas import TelemetryMessage
from app.telemetry_store import telemetry_store


class TelemetrySimulator:
    """
    Generates realistic mock telemetry data.
    
    Simulates:
    - Temperature drift (smooth changes, not random jumps)
    - Valid state transitions
    - AI recommendations based on conditions
    - Relay switching logic
    """
    
    def __init__(self):
        self.running = False
        self.task = None
        
        # Internal state for smooth transitions
        self.engine_temp = 75.0
        self.fuel_line_temp = 55.0
        self.ambient_temp = 25.0
        self.fuel_mode = "petrol"
        self.relay1 = False
        self.relay2 = False
        self.overheat = False
    
    async def start(self) -> None:
        """Start the simulator loop."""
        if self.running:
            return
        
        self.running = True
        self.task = asyncio.create_task(self._simulation_loop())
        print("[OK] Telemetry simulator started")
    
    async def stop(self) -> None:
        """Stop the simulator loop."""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        print("[OK] Telemetry simulator stopped")
    
    async def _simulation_loop(self) -> None:
        """
        Main simulation loop.
        
        Generates telemetry every 2 seconds with realistic state transitions.
        """
        while self.running:
            try:
                self._update_state()
                message = self._generate_message()
                await telemetry_store.store(message)
                await asyncio.sleep(2.0)  # 2-second interval
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in simulation loop: {e}")
                await asyncio.sleep(2.0)
    
    def _update_state(self) -> None:
        """
        Update internal state with realistic transitions.
        
        Simulates:
        - Temperature drift (small random changes)
        - Occasional fuel mode changes
        - Relay switching based on temperature
        - Overheat detection
        """
        # Temperature drift (smooth changes)
        self.engine_temp += random.uniform(-2, 2)
        self.fuel_line_temp += random.uniform(-1.5, 1.5)
        self.ambient_temp += random.uniform(-0.5, 0.5)
        
        # Clamp to realistic ranges
        self.engine_temp = max(60, min(120, self.engine_temp))
        self.fuel_line_temp = max(40, min(100, self.fuel_line_temp))
        self.ambient_temp = max(15, min(45, self.ambient_temp))
        
        # Check overheat condition
        self.overheat = self.engine_temp > 100
        
        # Simulate occasional fuel mode changes (5% chance)
        if random.random() < 0.05:
            self.fuel_mode = random.choice(["cng", "petrol", "lpg"])
        
        # Simulate relay switching based on temperature
        self.relay1 = self.engine_temp > 90
        self.relay2 = self.fuel_line_temp > 80
    
    def _generate_message(self) -> TelemetryMessage:
        """
        Generate a telemetry message from current state.
        
        Returns:
            TelemetryMessage conforming to Telemetry Data Contract v1
        """
        return TelemetryMessage(
            timestamp=datetime.utcnow().isoformat() + "Z",
            engine_temperature=round(self.engine_temp, 1),
            fuel_line_temperature=round(self.fuel_line_temp, 1),
            ambient_temperature=round(self.ambient_temp, 1),
            current_fuel_mode=self.fuel_mode,
            ai_recommendation=self._compute_ai_recommendation(),
            relay_state_1=self.relay1,
            relay_state_2=self.relay2,
            overheat_flag=self.overheat,
            system_status="fail_safe" if self.overheat else "demo_mode",
            network_status="disconnected",
            power_source="battery"
        )
    
    def _compute_ai_recommendation(self) -> str:
        """
        Compute AI recommendation based on current state.
        
        In production, this logic lives on the ESP32 Edge Controller.
        The bridge service never computes recommendations.
        """
        if self.overheat:
            return "activate_cooling"
        if self.engine_temp > 95:
            return "reduce_load"
        if self.engine_temp < 80 and self.fuel_mode != "cng":
            return "switch_to_biodiesel"  # Generic recommendation
        return "maintain"


# Global singleton instance
simulator = TelemetrySimulator()
