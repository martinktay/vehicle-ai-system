# 🚛 Agentic AI Smart Fleet Monitoring Platform

> **Building the Future of Intelligent, Sustainable, and Connected Mobility.**

The **Agentic AI Smart Fleet Monitoring Platform** is a professional-grade fleet management system designed for AI-driven multi-fuel vehicle optimization, roadworthiness monitoring, and net-zero transport intelligence.

## 🌟 Strategic Vision
This platform provides a high-credibility operational interface for **keke, buses, taxis, and company vehicles**. It bridges the gap between raw hardware telemetry and actionable insights for fleet operators and government regulators.

---

## 🛠️ System Capabilities

### 1. Real-Time Fleet Observability
Track temperature, fuel levels, and relay states across a heterogeneous fleet using ESP32 edge intelligence. 
*   **KPI Tracking**: Monitor fleet efficiency, CO2 reduction, and economic savings in real-time.
*   **Operational Logging**: Full transparency with the Telemetry Transaction Log.

### 2. Agentic AI Decision Engine
The AI agent operates in a continuous **Observe → Decide → Act → Explain** loop:
*   **Observe**: Ingests sensor data (DS18B20, Ultrasonic, LDR, Thermistor).
*   **Decide**: Recommends optimal fuel modes (LPG/CNG/Petrol) based on environmental conditions.
*   **Act**: Executes relay switching for cooling systems and fuel modes.
*   **Explain**: Provides human-readable reasoning for transparency and auditability.

### 3. Sustainability & Net-Zero Impact
Designed to support transport companies in meeting sustainability goals:
*   **Emissions Modeling**: Estimated CO2 reduction tracking.
*   **Fuel Arbitrage**: Optimization for lower-cost, cleaner fuels.
*   **Disclaimer**: Emissions values are modeled prototype estimates pending field calibration.

### 4. Policy & Regulatory Readiness
Engineered as a compliance-ready layer for future smart transport regulations:
*   Roadworthiness alerts (High temp / Sensor anomalies).
*   Fuel usage transparency for government auditing.
*   Keke and bus compliance program integration.

---

## 🏗️ Architecture

1.  **Edge (ESP32)**: Hardware-level control and sensor ingestion.
2.  **Bridge (FastAPI)**: Multi-vehicle fleet registry and AI advisory.
3.  **Cloud (React/Shadcn)**: Professional operational dashboard deployed on **Netlify**.

---

## 🚀 Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

### Frontend (Netlify Ready)
```bash
cd frontend
pnpm install
pnpm run build
```
*The `netlify.toml` file is configured for single-page application routing.*

---

*Developed for the Antigravity Smart Transport Competition | Towards Sustainable Mobility.*
