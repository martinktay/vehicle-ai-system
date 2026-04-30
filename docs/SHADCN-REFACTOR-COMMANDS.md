# shadcn/ui Refactor - Step-by-Step Commands

## ⚠️ IMPORTANT: Complete Refactor Required

This is a **major architectural change** that requires:
- Installing new dependencies
- Updating configuration files
- Refactoring all components
- Testing thoroughly

**Estimated Time: 4-5 hours**

## Step 1: Install Dependencies

```bash
cd frontend

# Install Tailwind CSS
pnpm add -D tailwindcss postcss autoprefixer

# Install Tailwind plugins and utilities
pnpm add -D tailwindcss-animate
pnpm add class-variance-authority clsx tailwind-merge

# Install Radix UI primitives (shadcn/ui foundation)
pnpm add @radix-ui/react-slot
pnpm add @radix-ui/react-separator
pnpm add @radix-ui/react-alert-dialog
pnpm add @radix-ui/react-label
pnpm add @radix-ui/react-progress

# Install lucide-react for icons
pnpm add lucide-react
```

## Step 2: Update package.json

The dependencies should now include:
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-separator": "^1.0.3",
    "@radix-ui/react-alert-dialog": "^1.0.5",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-progress": "^1.0.3",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.294.0",
    "tailwind-merge": "^2.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/user-event": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "fast-check": "^3.0.0",
    "jsdom": "^23.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16",
    "tailwindcss-animate": "^1.0.7"
  }
}
```

## Step 3: Configuration Files Created

✅ `tailwind.config.js` - Created
✅ `postcss.config.js` - Created
✅ `components.config.json` - Created
✅ `src/lib/utils.ts` - Created
✅ `src/components/ui/card.tsx` - Created

## Step 4: Update tsconfig.json

Add path aliases:

```json
{
  "compilerOptions": {
    // ... existing config
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Step 5: Update vite.config.ts

Add path resolution:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

## Step 6: Install Additional shadcn/ui Components

```bash
# Create remaining UI components manually or use shadcn CLI
# Badge component
# Alert component
# Separator component
# Progress component
```

## Step 7: Update index.css

Replace the entire file with Tailwind directives and CSS variables (see SHADCN-UI-MIGRATION-GUIDE.md)

## Step 8: Refactor Components (In Order)

1. StatusCard → Card + Badge
2. MetricCard → Card + lucide icons
3. RelayIndicator → Card + Badge
4. AlertBadge → Alert component
5. Economic Impact → Card + lucide icons
6. Nigerian Context → Card + lucide icons
7. Decision Transparency → Card + Separator
8. Performance Comparison → Card + custom table
9. Climate Impact → Card
10. Telemetry Chart → Keep SVG, wrap in Card

## Step 9: Test Each Component

After refactoring each component:
```bash
pnpm run dev
```

Check:
- Visual appearance
- Responsiveness
- Functionality
- No console errors

## Step 10: Remove Old Files

After successful migration:
- Remove old CSS files (if any custom ones remain)
- Clean up unused imports
- Remove old component files

## Current Status

✅ Phase 1: Configuration files created
✅ Phase 2: Base utilities created
✅ Phase 3: Card component created
⏳ Phase 4: Need to install dependencies (run commands above)
⏳ Phase 5: Need to create remaining UI components
⏳ Phase 6: Need to refactor existing components
⏳ Phase 7: Need to test and validate

## Next Actions Required

**YOU MUST RUN THESE COMMANDS:**

```bash
cd frontend
pnpm add -D tailwindcss postcss autoprefixer tailwindcss-animate
pnpm add class-variance-authority clsx tailwind-merge lucide-react
pnpm add @radix-ui/react-slot @radix-ui/react-separator @radix-ui/react-alert-dialog @radix-ui/react-label @radix-ui/react-progress
```

Then I can continue with the component refactoring.

## Why This is Complex

1. **Dependency Installation**: Requires pnpm commands (I cannot run these)
2. **Build System**: Vite needs to be restarted after config changes
3. **Type Checking**: TypeScript paths need to resolve correctly
4. **Component Refactoring**: Every component needs manual conversion
5. **Testing**: Each component must be tested after refactoring

## Recommendation

Given the complexity and time required (4-5 hours), I suggest:

**Option A**: I create all the refactored components as new files, and you can test them incrementally

**Option B**: We do this after the NLNG award submission to avoid breaking the working dashboard

**Option C**: We proceed systematically, but you'll need to run the installation commands and test after each phase

Which approach would you prefer?
