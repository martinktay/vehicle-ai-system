# SKILL: Agentic AI Smart Fleet Monitoring Platform

## Core Vision
Building the future of intelligent, sustainable, and connected mobility. A cloud-connected smart fleet monitoring platform for AI-driven multi-fuel vehicle optimization, climate impact tracking, and net-zero transport intelligence.

## Architectural Principles

### 1. Fleet Intelligence & Aggregation
- Support multiple vehicle types: `keke`, `bus`, `taxi`, `company_vehicle`.
- Aggregate fleet-level metrics (Total CO2 reduction, total cost saved).
- Maintain vehicle-specific registries with live tracking placeholders.

### 2. Agentic AI Engine (Observe, Decide, Act, Explain)
- **Observe**: Input telemetry (Temp, Fuel, LDR, Relay states, History).
- **Decide**: AI Engine predicts optimal fuel mode and switch timing.
- **Act**: Real-time edge relay control and fuel mode execution.
- **Explain**: Human-readable reasoning and climate impact modeling.

### 3. Smart Transport System Integration
- Design for integration with government city infrastructure and transport operators.
- Support for transport policy monitoring, roadworthiness auditing, and net-zero planning.
- Emission-aware routing and fleet optimization support.

### 4. Edge-Intelligence First
- All safety-critical decisions happen on the ESP32 edge device.
- The cloud provides high-level advisory, aggregation, and policy compliance verification.

## Telemetry Contract (v2)

| Field | Type | Purpose |
|-------|------|---------|
| `vehicle_id` | `string` | Unique identifier (e.g. KKE-001) |
| `vehicle_type` | `string` | keke, bus, taxi, company_vehicle |
| `temperature` | `number` | DS18B20 engine temperature |
| `fuel_percent` | `number` | Modeled fuel level |
| `fuel_mode` | `string` | PETROL, LPG, CNG |
| `status` | `string` | NORMAL, EFFICIENT, HIGH TEMP, LOW FUEL, WARNING |
| `co2_reduction`| `number` | Estimated kg CO2 saved |

## Deployment Strategy
- **Frontend**: Vercel/Netlify for global observability.
- **Backend**: Render/Netlify for fleet data aggregation.
- **Hardware**: ESP32 (Arduino) for real-time edge control.
