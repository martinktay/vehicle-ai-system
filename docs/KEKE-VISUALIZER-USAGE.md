# Keke Visualizer Usage Guide

**Component**: KekeVisualizer  
**Version**: 1.0.0  
**Status**: Production Ready

---

## Quick Start

### Basic Usage

```tsx
import { KekeVisualizer } from './components/KekeVisualizer';

function Dashboard() {
  const { current } = useTelemetry();
  
  return (
    <KekeVisualizer current={current} />
  );
}
```

### With Scenario Label

```tsx
<KekeVisualizer 
  current={current} 
  scenario="Heavy Traffic" 
/>
```

### With Custom Styling

```tsx
<KekeVisualizer 
  current={current} 
  scenario="Normal Driving"
  className="my-custom-class"
/>
```

---

## Props API

### `current` (required)
**Type**: `TelemetryMessage`  
**Description**: Current telemetry data from the vehicle

**Required Fields**:
- `current_fuel_mode`: string - Active fuel type (petrol, cng, lpg)
- `engine_temperature`: number - Engine temp in °C
- `overheat_flag`: boolean - Overheat alert state
- `system_status`: string - System state (normal, fail_safe, etc.)
- `ai_recommendation`: string - AI recommendation text

**Example**:
```typescript
const current: TelemetryMessage = {
  timestamp: "2026-04-06T10:30:00Z",
  current_fuel_mode: "cng",
  engine_temperature: 85,
  overheat_flag: false,
  system_status: "live_mode",
  ai_recommendation: "maintain",
  // ... other fields
};
```

### `scenario` (optional)
**Type**: `string`  
**Default**: `undefined`  
**Description**: Driving scenario label displayed in top-right

**Common Values**:
- "Normal Driving"
- "Heavy Traffic"
- "Fuel Scarcity"
- "Optimization Mode"
- "Highway Cruising"
- "City Navigation"

**Example**:
```tsx
<KekeVisualizer 
  current={current} 
  scenario="Heavy Traffic" 
/>
```

### `className` (optional)
**Type**: `string`  
**Default**: `""`  
**Description**: Additional CSS classes for custom styling

**Example**:
```tsx
<KekeVisualizer 
  current={current} 
  className="dashboard-vehicle compact-mode"
/>
```

---

## Visual States

### Fuel Modes

The visualizer automatically displays the active fuel mode with appropriate colors:

| Fuel Mode | Color | Icon | Node Position |
|-----------|-------|------|---------------|
| Petrol | Muted Orange (#d97706) | ⛽ | Left |
| CNG | Muted Green (#059669) | 💨 | Center |
| LPG | Muted Blue (#2563eb) | 🔥 | Right |

**Behavior**:
- Active fuel node glows and pulses
- Energy flow path animates from node to engine
- Fuel badge updates with icon and name
- Smooth transition when switching modes

### Heat Levels

Heat visualization based on engine temperature:

| Level | Temperature Range | Glow Color | Glow Size | Pulse Speed |
|-------|------------------|------------|-----------|-------------|
| Low | < 80°C | Stone (#78716c) | 50px | 3s |
| Medium | 80-100°C | Amber (#f59e0b) | 60px | 2s |
| High | > 100°C or overheat | Red (#dc2626) | 70px | 1s |

**Behavior**:
- Glow intensity increases with temperature
- Pulse speed increases with heat level
- Overheat flag triggers high heat state immediately

### Motion States

Vehicle motion based on system status:

| State | Road Animation | Wheel Rotation | Description |
|-------|---------------|----------------|-------------|
| Moving | Scrolling | Rotating | Normal operation |
| Stopped | Static | Static | Fail-safe or stopped |

**Behavior**:
- Road pattern scrolls horizontally when moving
- Wheels rotate continuously when moving
- All motion stops in fail-safe mode

### Status Messages

Automatically generated based on telemetry:

| Condition | Message |
|-----------|---------|
| Overheat flag | "Overheat Alert" |
| Fail-safe mode | "Fail-Safe Active" |
| Switching to CNG | "Switching to CNG" |
| Switching to LPG | "Switching to LPG" |
| Switching to Petrol | "Switching to Petrol" |
| Normal operation | "[FUEL] Active" |

---

## Customization

### Color Customization

Override fuel colors in your CSS:

```css
/* Custom fuel colors */
.keke-visualizer .node[data-fuel="petrol"] .node-outer {
  stroke: #your-color;
}

.keke-visualizer .node[data-fuel="petrol"] .node-inner {
  fill: #your-color;
}

/* Custom heat colors */
.keke-visualizer .heat-high {
  fill: url(#your-gradient);
}
```

### Animation Speed

Adjust animation timing:

```css
/* Faster wheel rotation */
.keke-visualizer .wheels.rotating .wheel {
  animation-duration: 1s; /* default: 1.5s */
}

/* Slower road scroll */
.keke-visualizer .road-surface.moving {
  animation-duration: 5s; /* default: 3s */
}

/* Faster energy flow */
.keke-visualizer .flow-active {
  animation-duration: 1s; /* default: 1.5s */
}
```

### Size Customization

Control visualizer dimensions:

```css
/* Larger visualizer */
.keke-visualizer-container {
  max-width: 1000px; /* default: 800px */
}

/* Compact mode */
.keke-visualizer-container.compact-mode {
  max-width: 600px;
  padding: 0.5rem;
}

.keke-visualizer-container.compact-mode .fuel-details {
  font-size: 0.75rem;
}
```

### Layout Customization

Position within your dashboard:

```css
/* Center in container */
.dashboard .keke-visualizer-container {
  margin: 2rem auto;
}

/* Full width */
.dashboard .keke-visualizer-container {
  max-width: 100%;
}

/* Sidebar placement */
.sidebar .keke-visualizer-container {
  max-width: 400px;
}
```

---

## Advanced Usage

### Dynamic Scenario Updates

Update scenario based on telemetry:

```tsx
function SmartKekeVisualizer({ current }: { current: TelemetryMessage }) {
  const scenario = useMemo(() => {
    if (current.overheat_flag) return "Overheat Alert";
    if (current.engine_temperature > 90) return "High Load";
    if (current.ai_recommendation.includes("switch")) return "Fuel Optimization";
    return "Normal Driving";
  }, [current]);

  return <KekeVisualizer current={current} scenario={scenario} />;
}
```

### Conditional Rendering

Show visualizer only when relevant:

```tsx
function ConditionalVisualizer({ current }: { current: TelemetryMessage }) {
  const showVisualizer = current.system_status !== 'offline';

  if (!showVisualizer) {
    return <div className="visualizer-placeholder">Vehicle Offline</div>;
  }

  return <KekeVisualizer current={current} />;
}
```

### Multiple Vehicles

Display multiple vehicles side-by-side:

```tsx
function FleetDashboard({ vehicles }: { vehicles: TelemetryMessage[] }) {
  return (
    <div className="fleet-grid">
      {vehicles.map((vehicle, index) => (
        <KekeVisualizer 
          key={vehicle.timestamp}
          current={vehicle}
          scenario={`Vehicle ${index + 1}`}
          className="fleet-vehicle"
        />
      ))}
    </div>
  );
}
```

---

## Performance Tips

### Optimize Re-renders

Use React.memo for expensive parent components:

```tsx
const MemoizedKekeVisualizer = React.memo(KekeVisualizer, (prev, next) => {
  return (
    prev.current.current_fuel_mode === next.current.current_fuel_mode &&
    prev.current.engine_temperature === next.current.engine_temperature &&
    prev.current.overheat_flag === next.current.overheat_flag &&
    prev.current.system_status === next.current.system_status
  );
});
```

### Reduce Animation Complexity

For low-end devices:

```css
/* Disable complex animations */
@media (max-width: 480px) {
  .keke-visualizer .flow-active,
  .keke-visualizer .heat-glow,
  .keke-visualizer .node-active .node-inner {
    animation: none !important;
  }
}
```

### Lazy Loading

Load visualizer only when visible:

```tsx
import { lazy, Suspense } from 'react';

const KekeVisualizer = lazy(() => import('./components/KekeVisualizer'));

function Dashboard() {
  return (
    <Suspense fallback={<div>Loading visualizer...</div>}>
      <KekeVisualizer current={current} />
    </Suspense>
  );
}
```

---

## Accessibility

### Screen Reader Support

The visualizer includes ARIA labels:

```tsx
<svg
  viewBox="0 0 800 400"
  role="img"
  aria-label="Keke vehicle status visualizer"
>
  <title>Vehicle Status</title>
  <desc>Shows current fuel mode, engine heat, and driving state</desc>
  {/* ... */}
</svg>
```

### Keyboard Navigation

Fuel details are keyboard accessible:

```tsx
<div className="fuel-badge" tabIndex={0} role="button">
  <span className="fuel-icon">{icon}</span>
  <span className="fuel-name">{name}</span>
</div>
```

### Reduced Motion

Respects user preferences:

```css
@media (prefers-reduced-motion: reduce) {
  .keke-visualizer * {
    animation: none !important;
  }
}
```

---

## Troubleshooting

### Visualizer Not Displaying

**Problem**: Component renders but SVG is blank

**Solutions**:
1. Check telemetry data is valid
2. Verify CSS is imported: `@import './styles/KekeVisualizer.css';`
3. Check browser console for errors
4. Ensure viewBox is not clipped by parent container

### Animations Not Working

**Problem**: Static visualizer with no motion

**Solutions**:
1. Check `system_status` is not "fail_safe"
2. Verify CSS animations are not disabled
3. Check for `prefers-reduced-motion` setting
4. Ensure GPU acceleration is available

### Wrong Fuel Mode Color

**Problem**: Fuel node shows incorrect color

**Solutions**:
1. Verify `current_fuel_mode` value is lowercase
2. Check supported modes: petrol, cng, lpg
3. Ensure CSS is not overriding colors
4. Check for typos in fuel mode string

### Performance Issues

**Problem**: Laggy animations or high CPU usage

**Solutions**:
1. Reduce animation complexity on mobile
2. Use `will-change` CSS property
3. Limit number of simultaneous visualizers
4. Consider disabling animations on low-end devices

---

## Examples

### Example 1: Basic Dashboard Integration

```tsx
import { KekeVisualizer } from './components/KekeVisualizer';
import { useTelemetry } from './hooks/useTelemetry';

function Dashboard() {
  const { current } = useTelemetry();

  return (
    <div className="dashboard">
      <header>
        <h1>Vehicle Monitoring</h1>
      </header>
      
      <main>
        <KekeVisualizer current={current} />
        
        <div className="metrics">
          {/* Other dashboard components */}
        </div>
      </main>
    </div>
  );
}
```

### Example 2: With Scenario Detection

```tsx
function SmartDashboard() {
  const { current } = useTelemetry();
  
  const scenario = useMemo(() => {
    const temp = current.engine_temperature;
    const fuel = current.current_fuel_mode;
    
    if (current.overheat_flag) return "Emergency";
    if (temp > 95) return "High Load";
    if (fuel === "cng") return "Eco Mode";
    if (fuel === "petrol") return "Performance Mode";
    return "Normal Driving";
  }, [current]);

  return (
    <KekeVisualizer 
      current={current} 
      scenario={scenario}
    />
  );
}
```

### Example 3: Compact Sidebar View

```tsx
function Sidebar() {
  const { current } = useTelemetry();

  return (
    <aside className="sidebar">
      <KekeVisualizer 
        current={current}
        className="compact-mode"
      />
      
      <div className="sidebar-stats">
        {/* Additional stats */}
      </div>
    </aside>
  );
}
```

---

## Best Practices

### 1. Always Provide Valid Telemetry

```tsx
// ✅ Good
<KekeVisualizer current={validTelemetryData} />

// ❌ Bad
<KekeVisualizer current={null} />
<KekeVisualizer current={undefined} />
```

### 2. Use Meaningful Scenarios

```tsx
// ✅ Good
<KekeVisualizer scenario="Heavy Traffic" />
<KekeVisualizer scenario="Fuel Optimization" />

// ❌ Bad
<KekeVisualizer scenario="Scenario 1" />
<KekeVisualizer scenario="Test" />
```

### 3. Optimize for Mobile

```tsx
// ✅ Good - Responsive
<div className="dashboard-container">
  <KekeVisualizer current={current} />
</div>

// ❌ Bad - Fixed width
<div style={{ width: '800px' }}>
  <KekeVisualizer current={current} />
</div>
```

### 4. Handle Loading States

```tsx
// ✅ Good
function Dashboard() {
  const { current, isLoading } = useTelemetry();
  
  if (isLoading) return <LoadingSpinner />;
  if (!current) return <ErrorMessage />;
  
  return <KekeVisualizer current={current} />;
}
```

---

## Support

### Documentation
- Design Spec: `docs/KEKE-VISUALIZER-DESIGN.md`
- Implementation: `docs/KEKE-VISUALIZER-IMPLEMENTATION.md`
- Summary: `docs/KEKE-VISUALIZER-SUMMARY.md`

### Component Files
- Component: `frontend/src/components/KekeVisualizer.tsx`
- Styles: `frontend/src/styles/KekeVisualizer.css`
- Types: `frontend/src/types/telemetry.ts`

### Development
- Skill Guide: `.kiro/skills/keke-vehicle-visualizer.md`

---

**Last Updated**: 2026-04-06  
**Version**: 1.0.0  
**Status**: Production Ready

