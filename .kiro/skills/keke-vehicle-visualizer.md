# Keke Vehicle Visualizer - Design Skill

## Context

This skill defines the design principles and implementation guidelines for the premium, minimal SVG-based Keke vehicle visualizer for the Nigerian transport-focused AI vehicle optimization dashboard.

## Design Philosophy

### Visual Identity
- **Minimal**: Clean lines, no unnecessary decoration
- **Professional**: Dashboard-grade quality, technical feel
- **Premium**: Restrained colors, subtle animations
- **Contextual**: Nigerian transport context (Keke = auto-rickshaw/tricycle)

### Color Palette

**Base Colors**:
- Silhouette: `#2d3748` (neutral charcoal)
- Background: `#1a202c` (dark slate)
- Inactive elements: `#4a5568` (muted gray)

**Fuel Mode Colors** (muted, professional):
- Petrol: `#d97706` (muted amber/orange)
- CNG: `#059669` (muted emerald green)
- LPG: `#2563eb` (muted blue)

**Heat Alert Colors**:
- Low heat: `#78716c` (stone gray)
- Medium heat: `#f59e0b` (soft amber)
- High heat: `#dc2626` (soft red)

**Accent Colors**:
- Active glow: `rgba(255, 255, 255, 0.2)`
- Flow animation: Current fuel color at 60% opacity
- Text: `#e5e7eb` (light gray)

## SVG Architecture

### Layer Structure (Z-Index Order)

1. **Background Layer** (`z-index: 1`)
   - Subtle road grid/track
   - Horizontal scrolling animation
   - Low opacity (0.15-0.25)

2. **Vehicle Body Layer** (`z-index: 2`)
   - Keke silhouette (side profile)
   - Cabin, body, chassis
   - Static structure

3. **Wheel Layer** (`z-index: 3`)
   - Front wheel (separate group)
   - Rear wheel (separate group)
   - Rotation animation support

4. **Engine/Thermal Zone Layer** (`z-index: 4`)
   - Radial gradient glow
   - Heat-responsive intensity
   - Positioned at lower body/engine area

5. **Energy Source Nodes Layer** (`z-index: 5`)
   - Three nodes: Petrol, CNG, LPG
   - Positioned below/behind cabin
   - Active/inactive states

6. **Energy Flow Paths Layer** (`z-index: 6`)
   - Animated paths from nodes to engine
   - Pulse/dot animation
   - Only active source animates

7. **Status Text Layer** (`z-index: 7`)
   - Fuel mode status
   - Switching indicators
   - Alert messages

8. **Scenario Label Layer** (`z-index: 8`)
   - Traffic conditions
   - Operating mode
   - Optimization status

## Component Structure

### React Component Props

```typescript
interface KekeVisualizerProps {
  current: TelemetryMessage;
  isMoving?: boolean;
  showLabels?: boolean;
  compact?: boolean;
}
```

### SVG Coordinate System

**Canvas**: 800×400 viewBox
- Origin: (0, 0) top-left
- Vehicle centered horizontally: x=400
- Vehicle baseline: y=280

**Key Coordinates**:
- Keke body: (250, 150) to (550, 280)
- Front wheel center: (480, 270)
- Rear wheel center: (320, 270)
- Engine zone: (360, 240)
- Fuel nodes: (280, 300), (320, 300), (360, 300)
- Status text: (400, 80)
- Scenario label: (400, 360)

## Animation Guidelines

### Motion Principles
- **Subtle**: No aggressive movements
- **Smooth**: Ease-in-out transitions
- **Purposeful**: Every animation conveys information
- **Performance**: GPU-accelerated CSS animations

### Animation Specifications

**Background Motion**:
```css
animation: roadScroll 20s linear infinite;
transform: translateX(-100px to 0);
```

**Wheel Rotation** (when moving):
```css
animation: wheelSpin 1s linear infinite;
transform-origin: center;
```

**Heat Glow Pulse**:
```css
animation: heatPulse 2s ease-in-out infinite;
opacity: 0.3 to 0.8 (based on heat level);
```

**Energy Flow**:
```css
animation: energyFlow 2s ease-in-out infinite;
stroke-dashoffset: 0 to -20;
```

**Fuel Switching**:
```css
transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
```

## State Management

### Visual States

**Fuel Mode States**:
- `petrol-active`: Orange glow, petrol node bright, petrol path animated
- `cng-active`: Green glow, CNG node bright, CNG path animated
- `lpg-active`: Blue glow, LPG node bright, LPG path animated
- `switching`: All nodes pulse, transition animation

**Heat States**:
- `heat-low`: Minimal glow, gray tone
- `heat-medium`: Moderate glow, amber tone
- `heat-high`: Strong glow, red tone, pulsing

**Motion States**:
- `moving`: Wheels rotate, background scrolls
- `stationary`: Wheels static, background static

## Integration Requirements

### Telemetry Schema Compatibility

Must read from existing `TelemetryMessage`:
- `current_fuel_mode`: "petrol" | "cng" | "lpg"
- `engine_temperature`: number (for heat visualization)
- `ai_recommendation`: string (for status text)
- `system_status`: string (for scenario label)

### Dashboard Integration

- Replace existing `AnimatedVehicle` component
- Maintain same props interface
- No breaking changes to parent components
- Responsive sizing support

## Extensibility

### Vehicle Type System

The visualizer must support future vehicle types:
- **Keke** (current): Tricycle/auto-rickshaw
- **Bus**: Larger profile, more passengers
- **Motorcycle**: Two wheels, single rider
- **SUV**: Four wheels, enclosed cabin
- **Delivery Van**: Cargo area, commercial use

**Implementation Strategy**:
```typescript
type VehicleType = 'keke' | 'bus' | 'motorcycle' | 'suv' | 'van';

interface VehicleConfig {
  type: VehicleType;
  svgPath: string;
  wheelPositions: Array<{x: number, y: number}>;
  engineZone: {x: number, y: number, radius: number};
  fuelNodePositions: Array<{x: number, y: number}>;
}
```

## Performance Targets

- **Initial render**: < 16ms
- **Animation frame rate**: 60fps
- **Memory footprint**: < 2MB
- **Bundle size**: < 15KB (component + styles)

## Accessibility

- Provide `aria-label` for vehicle state
- Include `role="img"` on SVG
- Ensure text contrast ratio ≥ 4.5:1
- Support reduced motion preferences

## Testing Checklist

- [ ] Renders correctly on load
- [ ] Fuel mode switching animates smoothly
- [ ] Heat glow responds to temperature
- [ ] Wheels rotate when moving
- [ ] Background scrolls appropriately
- [ ] Energy flow paths animate correctly
- [ ] Status text updates in real-time
- [ ] Responsive on mobile (320px+)
- [ ] Works in all major browsers
- [ ] No performance degradation over time

## File Structure

```
frontend/src/
├── components/
│   ├── KekeVisualizer.tsx          # Main component
│   └── vehicle/
│       ├── VehicleBase.tsx         # Reusable base
│       └── vehicles/
│           ├── KekeSVG.tsx         # Keke-specific SVG
│           ├── BusSVG.tsx          # Future
│           └── MotorcycleSVG.tsx   # Future
├── styles/
│   └── KekeVisualizer.css          # Component styles
└── types/
    └── vehicle.ts                   # Type definitions

docs/
├── KEKE-VISUALIZER-DESIGN.md       # Design specification
└── KEKE-VISUALIZER-IMPLEMENTATION.md # Implementation guide
```

## Design Tokens

```css
:root {
  /* Keke Visualizer Tokens */
  --keke-silhouette: #2d3748;
  --keke-bg: #1a202c;
  --keke-inactive: #4a5568;
  
  --fuel-petrol: #d97706;
  --fuel-cng: #059669;
  --fuel-lpg: #2563eb;
  
  --heat-low: #78716c;
  --heat-medium: #f59e0b;
  --heat-high: #dc2626;
  
  --keke-text: #e5e7eb;
  --keke-glow: rgba(255, 255, 255, 0.2);
  
  /* Animation Timings */
  --keke-transition: 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  --keke-pulse: 2s ease-in-out infinite;
  --keke-flow: 2s ease-in-out infinite;
  --keke-wheel: 1s linear infinite;
  --keke-road: 20s linear infinite;
}
```

## Nigerian Context

### Keke (Auto-Rickshaw) Characteristics
- Three-wheeled vehicle
- Open or semi-enclosed cabin
- Common in Nigerian urban transport
- Typically seats 3-4 passengers
- Engine at rear
- Fuel-efficient, maneuverable

### Cultural Considerations
- Recognizable silhouette for Nigerian users
- Respect for local transport culture
- Professional representation (not toy-like)
- Emphasis on efficiency and optimization

## Success Criteria

1. **Visual Quality**: Looks premium and professional
2. **Performance**: Smooth 60fps animations
3. **Clarity**: Fuel mode immediately obvious
4. **Responsiveness**: Works on all screen sizes
5. **Extensibility**: Easy to add new vehicle types
6. **Integration**: Drops into existing dashboard seamlessly
7. **Maintainability**: Clean, documented code

## References

- Existing `AnimatedVehicle.tsx` component
- Dashboard color scheme in `index.css`
- Telemetry schema in `types/telemetry.ts`
- Nigerian transport context and Keke design
