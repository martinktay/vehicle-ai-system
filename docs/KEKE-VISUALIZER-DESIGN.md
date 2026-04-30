# Keke Vehicle Visualizer - Design Specification

**Project**: Nigerian Transport AI Optimization System  
**Component**: Premium SVG-Based Keke Visualizer  
**Version**: 1.0  
**Date**: 2026-04-06

---

## Executive Summary

This document specifies the design and implementation of a premium, minimal SVG-based Keke (auto-rickshaw) vehicle visualizer for the dashboard. The visualizer provides real-time visual feedback for fuel mode, engine heat, and system state through subtle, professional animations.

---

## Design Goals

### Primary Objectives
1. **Visual Clarity**: Instantly communicate vehicle state
2. **Professional Aesthetic**: Dashboard-grade quality
3. **Performance**: Smooth 60fps animations
4. **Extensibility**: Support future vehicle types
5. **Integration**: Seamless dashboard integration

### Non-Goals
- Photorealistic rendering
- Complex 3D effects
- Gamification elements
- Excessive decoration

---

## Visual Design System

### Typography

**Status Text:**
- Font: System UI (sans-serif)
- Size: 14px
- Weight: 500 (medium)
- Color: `#e2e8f0` (light slate)
- Letter spacing: 0.5px

**Scenario Label:**
- Font: System UI (sans-serif)
- Size: 12px
- Weight: 400 (regular)
- Color: `#94a3b8` (slate)
- Letter spacing: 0.3px

**Node Labels:**
- Font: System UI (sans-serif)
- Size: 10px
- Weight: 600 (semibold)
- Color: Inherits from node state

### Spacing & Layout

**Grid System:**
- Canvas: 800×400px
- Margins: 50px (top/bottom), 50px (left/right)
- Content area: 700×300px
- Component spacing: 40px

**Visual Hierarchy:**
```
Primary: Vehicle silhouette (largest, central)
Secondary: Energy nodes, status text
Tertiary: Background pattern, scenario label
```

### Color System

**Neutral Palette:**
```css
--bg-primary: #1a202c;      /* Dark slate */
--bg-secondary: #2d3748;    /* Charcoal */
--text-primary: #e2e8f0;    /* Light slate */
--text-secondary: #94a3b8;  /* Slate */
--border: #4a5568;          /* Gray */
```

**Fuel Mode Palette (Muted):**
```css
--fuel-petrol: #d97706;     /* Muted orange */
--fuel-cng: #059669;        /* Muted green */
--fuel-lpg: #2563eb;        /* Muted blue */
```

**Heat Alert Palette:**
```css
--heat-low: #78716c;        /* Stone */
--heat-medium: #f59e0b;     /* Soft amber */
--heat-high: #dc2626;       /* Soft red */
```

**Opacity Levels:**
```css
--opacity-inactive: 0.2;
--opacity-dim: 0.4;
--opacity-active: 0.8;
--opacity-full: 1.0;
```

---

## SVG Layer Architecture

### Layer 1: Background (Road Pattern)

**Purpose**: Create motion illusion  
**Animation**: Horizontal scroll  
**Opacity**: 0.1-0.15

```xml
<g id="background-layer">
  <defs>
    <pattern id="road-grid" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
      <line x1="0" y1="50" x2="100" y2="50" stroke="#4a5568" stroke-width="1" opacity="0.3"/>
      <line x1="0" y1="80" x2="100" y2="80" stroke="#4a5568" stroke-width="0.5" opacity="0.2"/>
    </pattern>
  </defs>
  <rect x="0" y="300" width="800" height="100" fill="url(#road-grid)" className="road-surface"/>
</g>
```

**Animation:**
```css
.road-surface {
  animation: roadScroll 3s linear infinite;
}

@keyframes roadScroll {
  from { transform: translateX(0); }
  to { transform: translateX(-100px); }
}
```

### Layer 2: Vehicle Body (Keke Silhouette)

**Purpose**: Main vehicle representation  
**Style**: Clean side profile  
**Color**: `#2d3748` (charcoal)

**Keke Proportions:**
- Total width: 300px
- Total height: 150px
- Cabin height: 100px
- Roof height: 120px
- Ground clearance: 30px

**SVG Path Structure:**
```xml
<g id="vehicle-body-layer" transform="translate(250, 125)">
  <!-- Main body -->
  <path id="keke-body" d="M 0,80 L 0,40 Q 0,20 20,20 L 80,20 L 100,0 L 180,0 L 200,20 L 280,20 Q 300,20 300,40 L 300,80 Z" fill="#2d3748"/>
  
  <!-- Cabin windows -->
  <path id="cabin-window" d="M 90,25 L 110,10 L 170,10 L 190,25 Z" fill="#1a202c" opacity="0.6"/>
  
  <!-- Roof line -->
  <path id="roof-accent" d="M 85,20 L 105,5 L 175,5 L 195,20" stroke="#4a5568" stroke-width="2" fill="none"/>
</g>
```

### Layer 3: Wheels

**Purpose**: Rotation animation  
**Style**: Simple circles with spokes  
**Positions**: Front (520, 280), Rear (320, 280)

```xml
<g id="wheel-layer">
  <!-- Rear wheel -->
  <g id="rear-wheel" transform="translate(320, 280)">
    <circle cx="0" cy="0" r="35" fill="#1a202c" stroke="#4a5568" stroke-width="3"/>
    <circle cx="0" cy="0" r="10" fill="#2d3748"/>
    <line x1="-25" y1="0" x2="25" y2="0" stroke="#4a5568" stroke-width="2"/>
    <line x1="0" y1="-25" x2="0" y2="25" stroke="#4a5568" stroke-width="2"/>
  </g>
  
  <!-- Front wheel (same structure) -->
  <g id="front-wheel" transform="translate(520, 280)">
    <!-- Same as rear wheel -->
  </g>
</g>
```

**Animation:**
```css
.wheel {
  transform-origin: center;
  animation: wheelRotate 1.5s linear infinite;
}

@keyframes wheelRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Pause when not moving */
.vehicle-stopped .wheel {
  animation-play-state: paused;
}
```

### Layer 4: Engine/Thermal Zone

**Purpose**: Heat visualization  
**Style**: Radial gradient glow  
**Position**: (380, 240)

```xml
<g id="thermal-layer">
  <defs>
    <radialGradient id="heat-glow-low">
      <stop offset="0%" stop-color="#78716c" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#78716c" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="heat-glow-medium">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="heat-glow-high">
      <stop offset="0%" stop-color="#dc2626" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#dc2626" stop-opacity="0"/>
    </radialGradient>
  </defs>
  
  <circle 
    id="engine-glow" 
    cx="380" 
    cy="240" 
    r="60" 
    fill="url(#heat-glow-low)"
    className="heat-glow heat-low"
  />
</g>
```

**Animation:**
```css
.heat-glow {
  animation: heatPulse 2s ease-in-out infinite;
}

@keyframes heatPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 1.3; }
}

.heat-low { animation-duration: 3s; }
.heat-medium { animation-duration: 2s; }
.heat-high { animation-duration: 1s; }
```

### Layer 5: Energy Source Nodes

**Purpose**: Fuel type indicators  
**Style**: Small circles with labels  
**Positions**: Petrol (300, 320), CNG (340, 320), LPG (380, 320)

```xml
<g id="energy-nodes-layer">
  <!-- Petrol Node -->
  <g id="petrol-node" className="node node-inactive">
    <circle cx="300" cy="320" r="12" fill="#1a202c" stroke="#d97706" stroke-width="2" className="node-outer"/>
    <circle cx="300" cy="320" r="6" fill="#d97706" opacity="0.2" className="node-inner"/>
    <text x="300" y="345" text-anchor="middle" className="node-label">P</text>
  </g>
  
  <!-- CNG Node -->
  <g id="cng-node" className="node node-inactive">
    <circle cx="340" cy="320" r="12" fill="#1a202c" stroke="#059669" stroke-width="2" className="node-outer"/>
    <circle cx="340" cy="320" r="6" fill="#059669" opacity="0.2" className="node-inner"/>
    <text x="340" y="345" text-anchor="middle" className="node-label">C</text>
  </g>
  
  <!-- LPG Node -->
  <g id="lpg-node" className="node node-inactive">
    <circle cx="380" cy="320" r="12" fill="#1a202c" stroke="#2563eb" stroke-width="2" className="node-outer"/>
    <circle cx="380" cy="320" r="6" fill="#2563eb" opacity="0.2" className="node-inner"/>
    <text x="380" y="345" text-anchor="middle" className="node-label">L</text>
  </g>
</g>
```

**States:**
```css
.node-inactive .node-inner {
  opacity: 0.2;
}

.node-active .node-inner {
  opacity: 0.8;
  animation: nodePulse 1.5s ease-in-out infinite;
}

@keyframes nodePulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}
```

### Layer 6: Energy Flow Paths

**Purpose**: Visualize energy flow  
**Style**: Curved paths with animated dashes  
**Paths**: From each node to engine zone

```xml
<g id="flow-paths-layer">
  <!-- Petrol flow path -->
  <path 
    id="petrol-flow" 
    d="M 300,320 Q 320,280 380,240" 
    stroke="#d97706" 
    stroke-width="2" 
    fill="none"
    stroke-dasharray="10 5"
    opacity="0.2"
    className="flow-path flow-inactive"
  />
  
  <!-- CNG flow path -->
  <path 
    id="cng-flow" 
    d="M 340,320 Q 360,280 380,240" 
    stroke="#059669" 
    stroke-width="2" 
    fill="none"
    stroke-dasharray="10 5"
    opacity="0.2"
    className="flow-path flow-inactive"
  />
  
  <!-- LPG flow path -->
  <path 
    id="lpg-flow" 
    d="M 380,320 L 380,240" 
    stroke="#2563eb" 
    stroke-width="2" 
    fill="none"
    stroke-dasharray="10 5"
    opacity="0.2"
    className="flow-path flow-inactive"
  />
</g>
```

**Animation:**
```css
.flow-path {
  stroke-dasharray: 10 5;
  stroke-dashoffset: 0;
}

.flow-active {
  opacity: 0.8;
  animation: energyFlow 1.5s linear infinite;
}

@keyframes energyFlow {
  from { stroke-dashoffset: 15; }
  to { stroke-dashoffset: 0; }
}
```

### Layer 7: Status Text

**Purpose**: Display current state  
**Position**: Top-left (50, 50)  
**Content**: Dynamic based on telemetry

```xml
<g id="status-text-layer">
  <text 
    x="50" 
    y="50" 
    className="status-text"
    fill="#e2e8f0"
    font-size="14"
    font-weight="500"
  >
    Petrol Active
  </text>
</g>
```

### Layer 8: Scenario Label

**Purpose**: Display driving scenario  
**Position**: Top-right (750, 50)  
**Content**: Optional scenario name

```xml
<g id="scenario-label-layer">
  <text 
    x="750" 
    y="50" 
    className="scenario-label"
    fill="#94a3b8"
    font-size="12"
    text-anchor="end"
  >
    Normal Driving
  </text>
</g>
```

---

## State Management

### State Interface

```typescript
interface VisualizerState {
  // Core state
  fuelMode: 'petrol' | 'cng' | 'lpg';
  heatLevel: 'low' | 'medium' | 'high';
  isMoving: boolean;
  isSwitching: boolean;
  
  // Display state
  statusMessage: string;
  scenario?: string;
  
  // Animation state
  wheelRotation: boolean;
  backgroundScroll: boolean;
  heatPulse: boolean;
}
```

### State Transitions

**Fuel Mode Change:**
```
1. Detect fuel mode change
2. Set isSwitching = true
3. Fade out old node, fade in new node (300ms)
4. Transition flow path (300ms)
5. Update status text
6. Set isSwitching = false after 600ms
```

**Heat Level Change:**
```
1. Detect temperature threshold crossed
2. Transition glow gradient (500ms)
3. Adjust pulse speed
4. Update glow radius
```

**Motion State Change:**
```
1. Detect isMoving change
2. Start/stop wheel rotation
3. Start/stop background scroll
4. Transition duration: 300ms
```

---

## Performance Optimization

### GPU Acceleration

```css
.wheel,
.road-surface,
.heat-glow,
.flow-path {
  will-change: transform;
}
```

### Animation Throttling

- Limit simultaneous animations to 4
- Use `requestAnimationFrame` for smooth updates
- Debounce state changes (300ms)

### Memory Management

- Reuse gradient definitions
- Minimize DOM updates
- Use CSS transforms over position changes

---

## Responsive Design

### Breakpoints

**Desktop (≥1024px):**
- Full size: 800×400px
- All features enabled

**Tablet (768px - 1023px):**
- Scaled: 600×300px
- All features enabled

**Mobile (≤767px):**
- Scaled: 400×200px
- Simplified animations
- Larger touch targets

### Scaling Strategy

```css
.keke-visualizer {
  width: 100%;
  height: auto;
  max-width: 800px;
  aspect-ratio: 2 / 1;
}

@media (max-width: 767px) {
  .keke-visualizer {
    max-width: 400px;
  }
  
  /* Simplify animations on mobile */
  .flow-path,
  .heat-glow {
    animation: none;
  }
}
```

---

## Accessibility

### ARIA Labels

```xml
<svg role="img" aria-label="Keke vehicle status visualizer">
  <title>Vehicle Status</title>
  <desc>Shows current fuel mode, engine heat, and driving state</desc>
  ...
</svg>
```

### Keyboard Navigation

- Component is informational (no interactive elements)
- Screen reader announces state changes
- High contrast mode support

### Color Contrast

- All text meets WCAG AA standards (4.5:1 minimum)
- Status indicators use both color and shape
- Heat levels distinguishable in grayscale

---

## Browser Compatibility

**Supported Browsers:**
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android 90+)

**Fallbacks:**
- CSS animations → static display
- SVG filters → solid colors
- Gradients → flat fills

---

## Testing Requirements

### Visual Regression Tests
- [ ] All fuel modes render correctly
- [ ] Heat levels display appropriate colors
- [ ] Animations run smoothly (60fps)
- [ ] Responsive scaling works
- [ ] High contrast mode supported

### Functional Tests
- [ ] Fuel mode changes trigger transitions
- [ ] Heat level updates glow intensity
- [ ] Motion state controls animations
- [ ] Status text updates correctly
- [ ] Scenario label displays properly

### Performance Tests
- [ ] Initial render < 100ms
- [ ] State update < 16ms (60fps)
- [ ] Memory usage < 5MB
- [ ] CPU usage < 5%

---

## Implementation Checklist

- [ ] Create SVG layer structure
- [ ] Implement Keke silhouette path
- [ ] Add wheel components with rotation
- [ ] Create heat glow gradients
- [ ] Add energy source nodes
- [ ] Implement flow path animations
- [ ] Add status text layer
- [ ] Add scenario label layer
- [ ] Implement state management
- [ ] Add CSS animations
- [ ] Create React component wrapper
- [ ] Add TypeScript types
- [ ] Write unit tests
- [ ] Perform visual QA
- [ ] Optimize performance
- [ ] Document usage

---

## Future Enhancements

### Phase 2 Features
- Multiple vehicle type support (Bus, Motorcycle, SUV, Van)
- Advanced heat visualization (thermal camera effect)
- Route path animation
- Traffic density indicator
- Weather effects overlay

### Phase 3 Features
- 3D vehicle model (Three.js)
- Real-time fuel consumption graph
- Historical state playback
- Customizable color themes
- Export as video/GIF

---

## References

- **Telemetry Schema**: `frontend/src/types/telemetry.ts`
- **Dashboard Layout**: `frontend/src/App.tsx`
- **Existing Component**: `frontend/src/components/AnimatedVehicle.tsx`
- **Styling Guide**: `frontend/src/index.css`
- **Skill Document**: `.kiro/skills/keke-vehicle-visualizer.md`
