# shadcn/ui Migration Guide

## Overview

Complete systematic refactor from custom CSS to shadcn/ui + Tailwind CSS for professional, polished UI components.

## Migration Steps

### Phase 1: Installation & Setup

```bash
cd frontend

# Install Tailwind CSS and dependencies
pnpm add -D tailwindcss postcss autoprefixer
pnpm add -D tailwindcss-animate class-variance-authority clsx tailwind-merge

# Install Radix UI primitives (shadcn/ui foundation)
pnpm add @radix-ui/react-slot @radix-ui/react-separator @radix-ui/react-alert-dialog

# Install lucide-react for icons
pnpm add lucide-react

# Initialize Tailwind
npx tailwindcss init -p
```

### Phase 2: Configuration Files

#### tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

#### components.json (shadcn/ui config)
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

### Phase 3: Utility Functions

#### src/lib/utils.ts
```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Phase 4: Base CSS Update

Replace `src/index.css` with Tailwind directives and CSS variables.

### Phase 5: shadcn/ui Components to Install

```bash
# Core components
npx shadcn-ui@latest add card
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add alert
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add skeleton
```

### Phase 6: Component Migration Map

| Current Component | shadcn/ui Component | Icons |
|-------------------|---------------------|-------|
| StatusCard | Card + Badge | CheckCircle2, AlertCircle, Info |
| MetricCard | Card | TrendingUp, TrendingDown, AlertTriangle |
| RelayIndicator | Card + Badge | Power, PowerOff |
| AlertBadge | Alert | AlertTriangle, Info, CheckCircle2 |
| Economic Impact | Card | DollarSign, Calendar, TrendingUp, Zap |
| Nigerian Context | Card | MapPin, Droplet, Cloud, Settings |
| Decision Panel | Card + Separator | Brain, CheckCircle2, ArrowRight |
| Performance Comparison | Card + Table | BarChart3, TrendingUp |

## Implementation Order

1. ✅ Install dependencies
2. ✅ Configure Tailwind
3. ✅ Update base CSS
4. ✅ Create utility functions
5. ✅ Install shadcn/ui components
6. Refactor StatusCard
7. Refactor MetricCard
8. Refactor RelayIndicator
9. Refactor AlertBadge
10. Refactor Economic Impact section
11. Refactor Nigerian Context section
12. Refactor Decision Transparency Panel
13. Refactor Performance Comparison
14. Refactor Climate Impact
15. Refactor Telemetry Chart
16. Update App.tsx layout
17. Remove old CSS files
18. Test all components
19. Verify responsiveness
20. Final polish

## Breaking Changes

- Custom CSS classes will be replaced with Tailwind utilities
- Color system will use CSS variables
- Component APIs remain the same (props unchanged)
- Visual appearance will be more polished and consistent

## Benefits

- Professional, polished UI out of the box
- Consistent design system
- Better accessibility (Radix UI primitives)
- Responsive by default
- Dark mode support ready
- Icon system (lucide-react)
- Smaller bundle size (tree-shaking)
- Easier maintenance

## Timeline

- Phase 1-2: 30 minutes (setup)
- Phase 3-5: 1 hour (base components)
- Phase 6: 2-3 hours (component refactoring)
- Phase 7: 30 minutes (testing & polish)

**Total: ~4-5 hours**
