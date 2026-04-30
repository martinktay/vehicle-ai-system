# Requirements Document

## Introduction

The Competition Demonstration Mode enables the embedded AI + IoT telemetry platform to operate in demonstration scenarios where real sensor hardware may not be available or where controlled telemetry scenarios are needed for evaluation. This feature maintains the Edge-Intelligence First architecture while providing mock telemetry simulation, visual feedback for relay switching, offline operation, and transparent climate impact narratives. The system must support seamless switching between mock and real sensor data while preserving decision logic at the edge (ESP32) and maintaining the existing Telemetry Data Contract v1.

## Glossary

- **Edge_Controller**: The ESP32 microcontroller where all decision logic executes
- **Telemetry_Bridge**: The Python service that ingests serial data from Edge_Controller in a lightweight, non-blocking manner
- **Dashboard**: The React + TypeScript + Vite + pnpm visualization interface
- **Mock_Telemetry_Generator**: Component that produces simulated sensor data conforming to Telemetry Data Contract v1
- **Telemetry_Data_Contract_v1**: JSON schema with fields: timestamp, engine_temperature, fuel_line_temperature, ambient_temperature, current_fuel_mode, ai_recommendation, relay_state_1, relay_state_2, overheat_flag, system_status, network_status, power_source
- **Demo_Mode**: Operating state where Mock_Telemetry_Generator provides simulated data
- **Live_Mode**: Operating state where real sensor hardware provides telemetry data
- **Relay_Visualizer**: Dashboard component that displays relay switching states with visual feedback
- **Climate_Impact_Display**: Dashboard component showing efficiency calculations and environmental scoring
- **Fail_Safe_State**: Predetermined relay configuration activated when system detects unsafe conditions

## Requirements

### Requirement 1: Mock Telemetry Generation

**User Story:** As a competition demonstrator, I want to generate realistic mock telemetry data, so that I can showcase the system without physical sensors.

#### Acceptance Criteria

1. WHEN Demo_Mode is activated, THE Mock_Telemetry_Generator SHALL produce telemetry data conforming to Telemetry_Data_Contract_v1
2. THE Mock_Telemetry_Generator SHALL emit data at intervals between 2 and 5 seconds
3. THE Mock_Telemetry_Generator SHALL generate realistic value ranges for engine_temperature (60-120°C), fuel_line_temperature (40-100°C), and ambient_temperature (15-45°C)
4. THE Mock_Telemetry_Generator SHALL produce valid state transitions for current_fuel_mode, relay_state_1, relay_state_2, overheat_flag, system_status, network_status, and power_source
5. THE Mock_Telemetry_Generator SHALL include timestamp values in ISO 8601 format
6. THE Mock_Telemetry_Generator SHALL preserve all field names from Telemetry_Data_Contract_v1 without modification

### Requirement 2: Mode Switching

**User Story:** As a competition demonstrator, I want to switch between mock and real sensor data, so that I can transition from demo to live hardware seamlessly.

#### Acceptance Criteria

1. THE Edge_Controller SHALL support configuration to operate in Demo_Mode or Live_Mode
2. WHEN switching from Demo_Mode to Live_Mode, THE Edge_Controller SHALL begin reading from physical sensor hardware within 5 seconds
3. WHEN switching from Live_Mode to Demo_Mode, THE Edge_Controller SHALL begin using Mock_Telemetry_Generator within 5 seconds
4. THE Telemetry_Bridge SHALL process telemetry data identically regardless of Demo_Mode or Live_Mode
5. THE Dashboard SHALL display telemetry data identically regardless of Demo_Mode or Live_Mode
6. THE Edge_Controller SHALL indicate current operating mode in system_status field

### Requirement 3: Relay State Visualization

**User Story:** As a competition judge, I want to see visual feedback when relays switch, so that I can verify AI decisions are reflected in hardware state.

#### Acceptance Criteria

1. THE Relay_Visualizer SHALL display the current state of relay_state_1 and relay_state_2
2. WHEN relay_state_1 changes value, THE Relay_Visualizer SHALL update within 500 milliseconds
3. WHEN relay_state_2 changes value, THE Relay_Visualizer SHALL update within 500 milliseconds
4. THE Relay_Visualizer SHALL use distinct visual indicators for ON state and OFF state
5. THE Relay_Visualizer SHALL display the timestamp of the most recent relay state change
6. THE Relay_Visualizer SHALL show the correlation between ai_recommendation and current relay states

### Requirement 4: Offline Dashboard Operation

**User Story:** As a competition demonstrator, I want the dashboard to operate without network connectivity, so that I can demonstrate in venues without reliable internet.

#### Acceptance Criteria

1. THE Dashboard SHALL load and render without external network requests
2. THE Dashboard SHALL receive telemetry data via local serial connection through Telemetry_Bridge
3. THE Dashboard SHALL function identically whether network_status indicates connected or disconnected
4. THE Dashboard SHALL bundle all required assets locally during build process
5. WHERE LTE module is absent, THE Dashboard SHALL continue operating without degradation

### Requirement 5: Climate Impact Narrative Display

**User Story:** As a competition judge, I want to see transparent efficiency calculations and climate impact scoring, so that I can evaluate the environmental benefits of the AI system.

#### Acceptance Criteria

1. THE Climate_Impact_Display SHALL show efficiency calculations based on current_fuel_mode and temperature readings
2. THE Climate_Impact_Display SHALL display the formula used for each efficiency calculation
3. THE Climate_Impact_Display SHALL show cumulative fuel savings compared to baseline operation
4. THE Climate_Impact_Display SHALL display CO2 emission reduction estimates with calculation methodology
5. THE Climate_Impact_Display SHALL update efficiency metrics within 1 second of receiving new telemetry data
6. THE Climate_Impact_Display SHALL show the reasoning behind ai_recommendation values

### Requirement 6: Decision Logic Transparency

**User Story:** As a competition judge, I want to understand why the AI made specific recommendations, so that I can evaluate the intelligence and safety of the system.

#### Acceptance Criteria

1. THE Dashboard SHALL display the current ai_recommendation value
2. THE Dashboard SHALL show which sensor readings influenced the current ai_recommendation
3. WHEN ai_recommendation changes, THE Dashboard SHALL display the triggering conditions within 1 second
4. THE Dashboard SHALL show active safety thresholds for engine_temperature, fuel_line_temperature, and overheat_flag
5. THE Dashboard SHALL indicate when Fail_Safe_State is active
6. THE Dashboard SHALL display decision logic without executing decision logic itself

### Requirement 7: Streaming Telemetry Visualization

**User Story:** As a competition demonstrator, I want real-time charts of telemetry data, so that I can show system behavior over time.

#### Acceptance Criteria

1. THE Dashboard SHALL display time-series charts for engine_temperature, fuel_line_temperature, and ambient_temperature
2. WHEN new telemetry data arrives, THE Dashboard SHALL update charts within 500 milliseconds
3. THE Dashboard SHALL maintain a rolling window of at least 60 seconds of historical data
4. THE Dashboard SHALL display current_fuel_mode transitions on the time-series charts
5. THE Dashboard SHALL show relay state changes as annotations on the time-series charts

### Requirement 8: Safety Threshold Configuration

**User Story:** As a system operator, I want to configure safety thresholds, so that I can adapt the system to different operating environments.

#### Acceptance Criteria

1. THE Edge_Controller SHALL load safety threshold parameters for engine_temperature, fuel_line_temperature, and overheat_flag from configuration
2. WHEN engine_temperature exceeds configured threshold, THE Edge_Controller SHALL set overheat_flag to true
3. WHEN fuel_line_temperature exceeds configured threshold, THE Edge_Controller SHALL activate Fail_Safe_State
4. THE Edge_Controller SHALL validate threshold parameters are within safe operating ranges before applying them
5. THE Dashboard SHALL display currently active safety threshold values

### Requirement 9: Fail-Safe Relay Behavior

**User Story:** As a safety engineer, I want guaranteed fail-safe relay behavior, so that the system defaults to a safe state during anomalies.

#### Acceptance Criteria

1. THE Edge_Controller SHALL define a Fail_Safe_State configuration for relay_state_1 and relay_state_2
2. WHEN overheat_flag is true, THE Edge_Controller SHALL activate Fail_Safe_State within 100 milliseconds
3. WHEN system_status indicates error condition, THE Edge_Controller SHALL activate Fail_Safe_State within 100 milliseconds
4. WHEN Edge_Controller loses power, THE relay hardware SHALL default to Fail_Safe_State through hardware design
5. THE Edge_Controller SHALL log all Fail_Safe_State activations with timestamp and triggering condition

### Requirement 10: Telemetry Schema Immutability

**User Story:** As a platform architect, I want field names in the telemetry schema to remain unchanged, so that I maintain backward compatibility across system components.

#### Acceptance Criteria

1. THE Edge_Controller SHALL emit telemetry using exactly the field names defined in Telemetry_Data_Contract_v1
2. THE Telemetry_Bridge SHALL parse telemetry using exactly the field names defined in Telemetry_Data_Contract_v1
3. THE Dashboard SHALL consume telemetry using exactly the field names defined in Telemetry_Data_Contract_v1
4. IF new telemetry fields are needed, THE system SHALL add new fields without renaming existing fields
5. THE system SHALL reject telemetry messages that omit required fields from Telemetry_Data_Contract_v1

### Requirement 11: Lightweight Bridge Service

**User Story:** As a system architect, I want the Telemetry_Bridge to remain lightweight and non-blocking, so that it does not become a performance bottleneck.

#### Acceptance Criteria

1. THE Telemetry_Bridge SHALL use asynchronous I/O for serial port reading
2. THE Telemetry_Bridge SHALL forward telemetry data without performing decision logic
3. THE Telemetry_Bridge SHALL buffer at most 100 telemetry messages before dropping oldest messages
4. THE Telemetry_Bridge SHALL consume less than 50MB of memory during normal operation
5. WHEN telemetry data arrives, THE Telemetry_Bridge SHALL forward it to Dashboard within 50 milliseconds

### Requirement 12: Edge-First Architecture Preservation

**User Story:** As a platform architect, I want decision logic to remain on the Edge_Controller, so that the system maintains its Edge-Intelligence First design.

#### Acceptance Criteria

1. THE Edge_Controller SHALL execute all decision logic for ai_recommendation
2. THE Edge_Controller SHALL execute all decision logic for relay_state_1 and relay_state_2
3. THE Dashboard SHALL display decisions without computing ai_recommendation values
4. THE Dashboard SHALL display relay states without computing relay_state_1 or relay_state_2 values
5. THE Telemetry_Bridge SHALL forward telemetry without computing ai_recommendation, relay_state_1, or relay_state_2 values

### Requirement 13: Economic Impact Visualization

**User Story:** As a competition judge, I want to see economic value in Nigerian Naira, so that I can evaluate the financial benefits of the AI system.

#### Acceptance Criteria

1. THE Dashboard SHALL display hourly fuel cost savings in Nigerian Naira
2. THE Dashboard SHALL calculate daily savings based on 12 hours of operation
3. THE Dashboard SHALL project annual savings based on 26 working days per month
4. THE Dashboard SHALL calculate system payback period in months based on ₦150,000 system cost
5. THE Dashboard SHALL display ROI percentage based on annual savings
6. THE Dashboard SHALL show current fuel price and baseline cost comparison
7. THE Dashboard SHALL use Nigerian fuel prices: Petrol ₦700/L, CNG ₦250/L, LPG ₦450/L, Diesel ₦800/L

### Requirement 14: Nigerian Context Awareness

**User Story:** As a competition judge, I want to see how the system addresses Nigerian transport challenges, so that I can evaluate its local relevance.

#### Acceptance Criteria

1. THE Dashboard SHALL detect and display traffic scenarios (Heavy Lagos Traffic or Normal Driving)
2. THE Dashboard SHALL indicate fuel availability status (Petrol Scarce or Normal Supply)
3. THE Dashboard SHALL detect and display season (Harmattan, Rainy Season, or Normal)
4. THE Dashboard SHALL show current AI optimization strategy
5. THE Dashboard SHALL provide context-aware explanations for AI decisions
6. WHEN engine temperature exceeds 85°C with cooling active, THE Dashboard SHALL indicate Heavy Lagos Traffic scenario
7. WHEN using CNG or LPG fuel modes, THE Dashboard SHALL indicate fuel scarcity adaptation

### Requirement 15: Decision Transparency Panel

**User Story:** As a competition judge, I want to understand the AI decision-making process, so that I can evaluate the system's intelligence and safety.

#### Acceptance Criteria

1. THE Dashboard SHALL display current sensor readings with status indicators (✓/⚠/○)
2. THE Dashboard SHALL show which decision rules are currently active
3. THE Dashboard SHALL explain why the current recommendation was made
4. THE Dashboard SHALL display what conditions would trigger different recommendations
5. THE Dashboard SHALL update decision transparency within 1 second of new telemetry
6. THE Dashboard SHALL show optimal temperature range (80-90°C) in current state
7. THE Dashboard SHALL indicate safety thresholds (100°C overheat, 90°C fuel line)

### Requirement 16: Performance Comparison Display

**User Story:** As a competition judge, I want to see before-and-after comparison, so that I can evaluate the system's impact.

#### Acceptance Criteria

1. THE Dashboard SHALL display side-by-side comparison of "Without AI" vs "With AI System"
2. THE Dashboard SHALL compare fuel cost (daily) in Nigerian Naira
3. THE Dashboard SHALL compare CO₂ emissions (daily) in kilograms
4. THE Dashboard SHALL compare engine life expectancy in years
5. THE Dashboard SHALL compare overheat risk (High vs Prevented)
6. THE Dashboard SHALL compare fuel switching capability (Manual vs Automatic)
7. THE Dashboard SHALL compare efficiency percentage
8. THE Dashboard SHALL show total daily and annual savings
9. THE Dashboard SHALL display system payback period in the comparison summary
