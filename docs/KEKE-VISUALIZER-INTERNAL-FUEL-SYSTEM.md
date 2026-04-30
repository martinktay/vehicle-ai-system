# Keke Visualizer - Internal Fuel System Redesign

## Overview

Redesigned the Keke vehicle visualizer to show a realistic internal fuel system with fuel flow paths INSIDE the vehicle body, rather than external paths below the vehicle.

## Changes Made

### 1. Fuel Node Repositioning (vehicleConfigs.ts)

**Before**: Fuel nodes positioned below vehicle (y: 270-290)
**After**: Fuel nodes positioned INSIDE vehicle body (y: 170-185)

```typescript
fuelNodes: [
  // Fuel tank at rear INSIDE vehicle body - Petrol
  { x: 235, y: 185, radius: 12, label: 'P' },
  // CNG cylinder (under seat area) INSIDE vehicle body
  { x: 360, y: 180, radius: 12, label: 'C' },
  // LPG tank (rear, slightly offset) INSIDE vehicle body
  { x: 270, y: 170, radius: 12, label: 'L' },
]
```

### 2. Engine Zone Repositioning

**Before**: Engine positioned outside/below vehicle (x: 480, y: 260)
**After**: Engine positioned INSIDE vehicle at front (x: 505, y: 175)

```typescript
engineZone: {
  x: 505,
  y: 175,
  radiusLow: 35,
  radiusMedium: 42,
  radiusHigh: 50,
}
```

### 3. Internal Fuel System Components (KekeVisualizer.tsx)

Added visual representations of internal fuel system components:

- **Fuel Tank Visual**: Rectangle at rear of vehicle showing fuel storage
- **Engine Compartment**: Rectangle at front showing engine location
- **Engine Block Detail**: Nested rectangle for realistic engine appearance

```tsx
<g className="fuel-system-internal">
  {/* Fuel Tank Visual (rear of vehicle) */}
  <rect x="20" y="85" width="35" height="20" rx="3" ... />
  
  {/* Engine Compartment Visual (front of vehicle) */}
  <rect x="295" y="60" width="30" height="35" rx="2" ... />
  
  {/* Engine block detail */}
  <rect x="300" y="65" width="20" height="25" rx="1" ... />
</g>
```

### 4. Realistic Fuel Line Routing

**Before**: Simple quadratic curves from external nodes to engine
**After**: Internal fuel lines with realistic piping appearance

- Dual-layer rendering (background pipe + colored flow line)
- Curved routing through vehicle interior
- Animated flow when active
- Subtle upward curve for realistic piping layout

```tsx
// Calculate realistic internal fuel line path
const midX = (node.x + config.engineZone.x) / 2;
const controlY = node.y - 15; // Route slightly upward
const pathData = `M ${node.x},${node.y} Q ${midX},${controlY} ${config.engineZone.x},${config.engineZone.y}`;
```

### 5. Enhanced Visual Styling (KekeVisualizer.css)

- Added drop shadows for fuel tank and engine compartment
- Enhanced fuel line appearance with background pipe layer
- Improved node visibility with better opacity control
- Smoother animations for fuel flow
- Better contrast for internal components

## Visual Improvements

### Professional Design Elements

1. **Layered Fuel Lines**: Background pipe (dark) + colored flow line (animated)
2. **Component Shadows**: Subtle drop shadows for depth
3. **Realistic Positioning**: Fuel tank at rear, engine at front, lines connecting through interior
4. **Enhanced Contrast**: Better visibility of internal components against vehicle body
5. **Smooth Animations**: Refined fuel flow animation (1.2s cycle, 8-4 dash pattern)

### Color Palette

- Fuel Tank: `#1a202c` with `#4a5568` stroke
- Engine Compartment: `#1a202c` with `#78716c` stroke
- Engine Block: `#2d3748` with `#78716c` stroke
- Fuel Lines: Colored by fuel type (Petrol: `#d97706`, CNG: `#059669`, LPG: `#2563eb`)

## Technical Details

### Transform Coordination

All internal components use the same `bodyTransform` as the vehicle body to ensure proper positioning:

```tsx
<g transform={config.bodyTransform || ''}>
  {/* Fuel nodes, flow paths, thermal zone */}
</g>
```

### Accessibility

- Maintained all ARIA labels and descriptions
- Preserved reduced-motion support
- Enhanced high-contrast mode compatibility
- Print-friendly styling

## Result

The Keke visualizer now displays a realistic internal fuel system with:

- Fuel storage at the rear of the vehicle
- Fuel lines routing through the vehicle interior
- Engine compartment at the front
- Animated fuel flow showing active fuel source
- Professional, technical aesthetic suitable for dashboard presentation

## Files Modified

1. `frontend/src/config/vehicleConfigs.ts` - Repositioned fuel nodes and engine zone
2. `frontend/src/components/KekeVisualizer.tsx` - Added internal fuel system components and updated rendering
3. `frontend/src/styles/KekeVisualizer.css` - Enhanced styling for internal components

## Compatibility

- No breaking changes to telemetry schema
- No changes to component API
- Fully backward compatible with existing dashboard integration
- Extensible for future vehicle types (Bus, Motorcycle, SUV, Van)
