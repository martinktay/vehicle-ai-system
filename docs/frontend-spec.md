# Frontend Specification

## Overview

The dashboard is a React + TypeScript web application that visualizes telemetry data from the Climate-Smart Telemetry Platform. It provides real-time monitoring, decision transparency, and climate impact metrics.

## Technology Stack

- **Framework:** React 18
- **Language:** TypeScript
- **Build Tool:** Vite
- **Package Manager:** pnpm
- **Styling:** Custom CSS (no heavy UI library)
- **State Management:** React hooks (no Redux/Zustand)

## Architecture

### Component Structure

```
frontend/src/
├── main.tsx                    # Application entry point
├── App.tsx                     # Root component
├── index.css                   # Global styles
├── types/
│   └── telemetry.ts           # Telemetry type definitions
├── api/
│   └── telemetryApi.ts        # API client for backend
├── hooks/
│   └── useTelemetry.ts        # Telemetry data hook
├── data/
│   └── mockTelemetry.ts       # Mock data generator (fallback)
└── components/
    ├── StatusCard.tsx         # Status badge component
    ├── MetricCard.tsx         # Metric display with progress bar
    ├── RelayIndicator.tsx     # Relay ON/OFF indicator
    ├── TelemetryChart.tsx     # Time-series line chart
    └── AlertBadge.tsx         # Alert/warning messages
```

### Data Flow

```
Backend API
    ↓ HTTP polling (2s interval)
useTelemetry hook
    ↓ React state
App.tsx
    ↓ Props
Dashboard components
    ↓ Render
User interface
```

## Key Features

### 1. Real-Time Telemetry Display
- **Temperature monitoring:** Engine, fuel line, ambient
- **Update frequency:** Every 2 seconds
- **Visual indicators:** Color-coded thresholds
- **Progress bars:** Show temperature relative to threshold

### 2. Relay State Visualization
- **Visual feedback:** ON (green light) / OFF (gray)
- **State labels:** Clear ON/OFF text
- **Descriptions:** "Cooling System", "Fuel Switching"
- **Timestamp:** Last state change time

### 3. AI Decision Transparency
- **Current recommendation:** Display AI decision
- **Influencing factors:** Show which sensors triggered decision
- **Reasoning:** Explain why recommendation was made
- **Safety thresholds:** Display active limits

### 4. Climate Impact Metrics
- **Current efficiency:** Percentage based on fuel mode and temperature
- **CO₂ reduction:** Estimated savings vs. baseline
- **Calculation transparency:** Show formulas used
- **No exaggerated claims:** Conservative estimates

### 5. Live Telemetry Chart
- **Time-series visualization:** 60-second rolling window
- **Three temperature lines:** Engine, fuel line, ambient
- **Annotations:** Fuel mode changes, relay state changes
- **Auto-scaling:** Y-axis adjusts to data range

## Component Specifications

### StatusCard
**Purpose:** Display system status with color-coded badges

**Props:**
```typescript
interface StatusCardProps {
  label: string;
  value: string;
  variant: 'ok' | 'warning' | 'error' | 'info';
}
```

**Usage:**
```tsx
<StatusCard label="System" value="live_mode" variant="ok" />
```

### MetricCard
**Purpose:** Display numeric metrics with visual progress indicators

**Props:**
```typescript
interface MetricCardProps {
  label: string;
  value: number;
  unit: string;
  threshold?: number;
  warning?: boolean;
  showBar?: boolean;
}
```

**Usage:**
```tsx
<MetricCard 
  label="Engine Temperature" 
  value={85.3} 
  unit="°C" 
  threshold={100} 
  warning={false} 
/>
```

### RelayIndicator
**Purpose:** Visual ON/OFF indicator for relay states

**Props:**
```typescript
interface RelayIndicatorProps {
  label: string;
  state: boolean;
  description: string;
}
```

**Usage:**
```tsx
<RelayIndicator 
  label="Relay 1" 
  state={true} 
  description="Cooling System" 
/>
```

### TelemetryChart
**Purpose:** Time-series line chart for temperature data

**Props:**
```typescript
interface TelemetryChartProps {
  history: TelemetryMessage[];
  title?: string;
}
```

**Features:**
- SVG-based rendering
- Three colored lines (engine, fuel line, ambient)
- Legend with color indicators
- 60-second rolling window
- Auto-scaling Y-axis

### AlertBadge
**Purpose:** Display alert messages with severity styling

**Props:**
```typescript
interface AlertBadgeProps {
  message: string;
  variant: 'error' | 'warning' | 'info' | 'success';
  icon?: string;
}
```

**Usage:**
```tsx
<AlertBadge 
  message="Fail-safe mode active: Overheat detected" 
  variant="error" 
  icon="⚠️" 
/>
```

## API Integration

### Backend Endpoints

```typescript
// Get latest telemetry
GET /api/latest
Response: TelemetryMessage

// Get telemetry history (60s window)
GET /api/history?limit=30
Response: TelemetryMessage[]

// Health check
GET /api/health
Response: { status, mode, telemetry_available, ingestion_connected }
```

### Hybrid Mode (Backend + Fallback)

The dashboard automatically switches between backend and mock mode:

1. **Check backend health** on startup
2. **Backend available:** Poll API every 2 seconds
3. **Backend unavailable:** Use mock telemetry generator
4. **Visual indicator:** "Source" badge shows "Backend API" or "Simulator"

## Styling

### Design System

**Colors:**
- Background: `#0f1419` (dark)
- Surface: `#1a1f2e` (card background)
- Text: `#e4e6eb` (light)
- Primary: `#3b82f6` (blue)
- Success: `#10b981` (green)
- Warning: `#f59e0b` (yellow)
- Error: `#ef4444` (red)

**Typography:**
- Font: System fonts (no external fonts)
- Base size: 16px
- Line height: 1.6

**Layout:**
- Max width: 1400px
- Padding: 2rem
- Card grid: Auto-fit, min 280px
- Responsive: Mobile-friendly

### Dark Theme Rationale
- Reduces eye strain for monitoring
- Better contrast for telemetry data
- Professional appearance
- Lower power consumption on OLED displays

## Performance

### Optimization Strategies
- **React.memo:** Memoize expensive chart components
- **Efficient rendering:** Only update changed components
- **Bounded history:** Limit to 60 seconds (max ~30 messages)
- **Polling interval:** 2 seconds (not too frequent)

### Performance Targets
- **Initial load:** < 2 seconds
- **Update latency:** < 500 milliseconds
- **Memory usage:** < 100 MB
- **CPU usage:** < 5% (idle), < 20% (active)

## Accessibility

- **Semantic HTML:** Proper heading hierarchy
- **Color contrast:** WCAG AA compliant
- **Keyboard navigation:** All interactive elements accessible
- **Screen reader support:** ARIA labels where needed
- **Responsive design:** Works on mobile, tablet, desktop

## Development

### Setup
```bash
cd frontend
pnpm install
pnpm dev
```

### Build
```bash
pnpm build
```

### Testing
```bash
pnpm test
```

## Future Enhancements

- **WebSocket support:** Real-time streaming instead of polling
- **Historical data:** Time-range selector for past data
- **Export functionality:** Download telemetry as CSV
- **Alerts:** Configurable threshold alerts
- **Mobile app:** React Native version
- **Multi-node support:** Fleet dashboard for multiple ESP32 devices
