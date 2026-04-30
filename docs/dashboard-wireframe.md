# Dashboard Wireframe

## Overview

The Climate-Smart Telemetry Dashboard provides real-time monitoring of the embedded AI system. This document describes the layout, components, and user interface design.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  🌱 Climate-Smart Telemetry Dashboard                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ System:  │ │Connection│ │ Source:  │ │ Power:   │          │
│  │live_mode │ │  active  │ │ Backend  │ │ battery  │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Temperature Monitoring                                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │   Engine     │ │  Fuel Line   │ │   Ambient    │           │
│  │              │ │              │ │              │           │
│  │   85.3°C     │ │   62.1°C     │ │   28.5°C     │           │
│  │              │ │              │ │              │           │
│  │ ████████░░░░ │ │ ██████░░░░░░ │ │ ████░░░░░░░░ │           │
│  │ Threshold:   │ │ Threshold:   │ │ Threshold:   │           │
│  │ 100°C        │ │ 90°C         │ │ 40°C         │           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Intelligent Fuel Management                                     │
│  ┌────────────────────────┐ ┌────────────────────────────────┐ │
│  │  ⛽ Current Fuel Mode   │ │  🤖 AI Recommendation          │ │
│  │                        │ │                                │ │
│  │  🌿 Biodiesel          │ │  ✓ Maintain Current Mode       │ │
│  │                        │ │                                │ │
│  │                        │ │  Based on: Engine 85.3°C,      │ │
│  │                        │ │  Fuel Line 62.1°C              │ │
│  └────────────────────────┘ └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Relay Control Status                                            │
│  ┌────────────────────┐ ┌────────────────────┐                 │
│  │  ● Relay 1         │ │  ○ Relay 2         │                 │
│  │                    │ │                    │                 │
│  │  ON                │ │  OFF               │                 │
│  │                    │ │                    │                 │
│  │  Cooling System    │ │  Fuel Switching    │                 │
│  └────────────────────┘ └────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Live Telemetry Stream                                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  ─── Engine  ─── Fuel Line  ─── Ambient                   │ │
│  │                                                            │ │
│  │  120°C ┤                                                   │ │
│  │        │     ╱─────╲                                       │ │
│  │  100°C ┤    ╱       ╲                                      │ │
│  │        │   ╱         ╲─────                                │ │
│  │   80°C ┤  ╱                ╲                               │ │
│  │        │ ╱                  ╲                              │ │
│  │   60°C ┤╱                    ╲─────                        │ │
│  │        │                           ╲                       │ │
│  │   40°C ┤                            ╲─────                 │ │
│  │        │                                  ╲                │ │
│  │   20°C ┤                                   ╲─────          │ │
│  │        └────────────────────────────────────────────       │ │
│  │        0s    15s    30s    45s    60s                      │ │
│  │                                                            │ │
│  │  Showing last 25 readings (60s window)                    │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Climate Impact                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  ┌──────────────┐         ┌──────────────┐                │ │
│  │  │     85%      │         │   12.5 kg    │                │ │
│  │  │              │         │              │                │ │
│  │  │   Current    │         │ CO₂ Reduction│                │ │
│  │  │  Efficiency  │         │   (est.)     │                │ │
│  │  └──────────────┘         └──────────────┘                │ │
│  │                                                            │ │
│  │  Calculation: Efficiency based on fuel mode and           │ │
│  │  temperature optimization. CO₂ reduction estimated from   │ │
│  │  fuel savings vs. baseline diesel operation.              │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Header Section
**Purpose:** System status at a glance

**Components:**
- **System badge:** Current system status (live_mode, fail_safe, demo_mode)
- **Connection badge:** Connection status (active, disconnected)
- **Source badge:** Data source (Backend API, Simulator)
- **Power badge:** Power source (battery, solar, grid)

**Color coding:**
- Green: Normal operation
- Yellow: Warning state
- Red: Error or fail-safe
- Blue: Informational

### Temperature Monitoring Section
**Purpose:** Real-time temperature display with visual indicators

**Components:**
- **Three metric cards:** Engine, Fuel Line, Ambient
- **Large temperature value:** Easy to read at a glance
- **Progress bar:** Visual representation of temperature relative to threshold
- **Threshold label:** Shows safety limit

**Visual feedback:**
- Normal: Green progress bar
- Warning: Yellow/orange progress bar
- Critical: Red progress bar, red border

### Intelligent Fuel Management Section
**Purpose:** Display current fuel mode and AI recommendations

**Components:**
- **Fuel mode card:** Shows current fuel type with icon
- **AI recommendation card:** Shows AI decision with reasoning

**AI recommendation examples:**
- "✓ Maintain Current Mode"
- "→ Switch to Biodiesel"
- "❄️ Activate Cooling"
- "⚠️ Reduce Engine Load"

**Reasoning display:**
- Shows which sensors influenced the decision
- Example: "Based on: Engine 85.3°C, Fuel Line 62.1°C"

### Relay Control Status Section
**Purpose:** Visual feedback for relay states

**Components:**
- **Two relay indicators:** Relay 1 and Relay 2
- **Visual state:** Glowing green circle (ON) or gray circle (OFF)
- **State label:** Clear "ON" or "OFF" text
- **Description:** What each relay controls

**Visual design:**
- ON state: Green glowing circle, green text
- OFF state: Gray circle, gray text
- Fail-safe alert: Red banner if overheat detected

### Live Telemetry Stream Section
**Purpose:** Time-series visualization of temperature data

**Components:**
- **Line chart:** Three colored lines for three sensors
- **Legend:** Color-coded labels
- **Time axis:** 60-second rolling window
- **Temperature axis:** Auto-scaling based on data range
- **Info text:** Number of readings and time window

**Chart features:**
- Smooth line rendering
- Auto-scaling Y-axis
- Fixed 60-second X-axis
- Color-coded lines (red, orange, blue)

### Climate Impact Section
**Purpose:** Show efficiency and environmental impact

**Components:**
- **Efficiency metric:** Current efficiency percentage
- **CO₂ reduction metric:** Estimated savings in kg
- **Calculation note:** Transparent methodology

**Calculation transparency:**
- Shows formula used
- Conservative estimates
- No exaggerated claims
- Based on fuel savings vs. baseline

## Color Palette

### Background Colors
- **Primary background:** `#0f1419` (dark)
- **Card background:** `#1a1f2e` (slightly lighter)
- **Hover state:** `#252b3b` (interactive elements)

### Status Colors
- **Success/OK:** `#10b981` (green)
- **Warning:** `#f59e0b` (yellow/orange)
- **Error:** `#ef4444` (red)
- **Info:** `#06b6d4` (cyan)
- **Primary:** `#3b82f6` (blue)

### Text Colors
- **Primary text:** `#e4e6eb` (light gray)
- **Secondary text:** `#9ca3af` (medium gray)
- **Muted text:** `#6b7280` (dark gray)

### Chart Colors
- **Engine temperature:** `#e74c3c` (red)
- **Fuel line temperature:** `#f39c12` (orange)
- **Ambient temperature:** `#3498db` (blue)

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
```

### Font Sizes
- **Heading 1:** 1.5rem (24px) - Dashboard title
- **Heading 2:** 1.25rem (20px) - Section titles
- **Heading 3:** 1rem (16px) - Card titles
- **Body text:** 1rem (16px) - Normal text
- **Small text:** 0.875rem (14px) - Labels, captions
- **Large numbers:** 2.5rem (40px) - Temperature values

### Font Weights
- **Normal:** 400 - Body text
- **Medium:** 500 - Labels
- **Semibold:** 600 - Headings
- **Bold:** 700 - Large numbers

## Responsive Design

### Desktop (> 1024px)
- Full layout as shown above
- Three-column grid for temperature cards
- Two-column grid for fuel management
- Full-width chart

### Tablet (768px - 1024px)
- Two-column grid for temperature cards
- Two-column grid for fuel management
- Full-width chart
- Slightly reduced padding

### Mobile (< 768px)
- Single-column layout
- Stacked temperature cards
- Stacked fuel management cards
- Full-width chart (scrollable if needed)
- Reduced font sizes

## Accessibility

### Keyboard Navigation
- All interactive elements accessible via Tab key
- Focus indicators visible
- Logical tab order

### Screen Readers
- Semantic HTML (proper heading hierarchy)
- ARIA labels for icons and visual elements
- Alt text for images

### Color Contrast
- WCAG AA compliant
- Minimum 4.5:1 contrast ratio for text
- Minimum 3:1 contrast ratio for UI components

### Visual Indicators
- Not relying on color alone
- Icons + text for status
- Patterns + colors for charts

## Animation and Transitions

### Smooth Transitions
- Temperature value changes: 0.3s ease
- Progress bar updates: 0.3s ease
- Relay state changes: 0.3s ease
- Chart updates: 0.5s ease

### Activity Indicators
- Loading spinner: Rotating animation
- Activity LED: Brief pulse (50ms)
- New data: Subtle highlight

### Performance
- CSS transitions (GPU-accelerated)
- No JavaScript animations for simple transitions
- Debounced updates to prevent jank

## User Interactions

### Hover States
- Cards: Slight elevation shadow
- Buttons: Background color change
- Links: Underline appears

### Click/Tap Feedback
- Buttons: Slight scale down (0.98)
- Cards: No click action (display only)
- Links: Standard browser behavior

### Loading States
- Initial load: Spinner with message
- Data updates: Smooth transitions (no spinner)
- Error states: Clear error message with retry option

## Error States

### No Data Available
```
┌─────────────────────────────────────┐
│  Initializing telemetry system...   │
│                                     │
│  ⟳ Loading...                       │
│                                     │
│  Checking backend availability...   │
└─────────────────────────────────────┘
```

### Connection Lost
```
┌─────────────────────────────────────┐
│  ⚠️ Connection Lost                  │
│                                     │
│  Attempting to reconnect...         │
│  Last update: 30 seconds ago        │
└─────────────────────────────────────┘
```

### Fail-Safe Active
```
┌─────────────────────────────────────┐
│  ⚠️ FAIL-SAFE MODE ACTIVE            │
│                                     │
│  Overheat detected                  │
│  All relays set to safe state       │
└─────────────────────────────────────┘
```

## Future Enhancements

- **Historical data view:** Date range selector
- **Export functionality:** Download telemetry as CSV
- **Alerts:** Configurable threshold alerts
- **Multi-node view:** Fleet dashboard for multiple devices
- **Mobile app:** Native iOS/Android app
- **Dark/light theme toggle:** User preference
