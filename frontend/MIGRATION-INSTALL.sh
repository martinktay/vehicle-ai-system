#!/bin/bash

# shadcn/ui Migration Installation Script
# Run this from the frontend directory

echo "🚀 Starting shadcn/ui migration installation..."

# Install Tailwind CSS and dependencies
echo "📦 Installing Tailwind CSS..."
pnpm add -D tailwindcss postcss autoprefixer
pnpm add -D tailwindcss-animate class-variance-authority clsx tailwind-merge

# Install Radix UI primitives
echo "📦 Installing Radix UI primitives..."
pnpm add @radix-ui/react-slot @radix-ui/react-separator @radix-ui/react-alert-dialog @radix-ui/react-label

# Install lucide-react for icons
echo "📦 Installing lucide-react icons..."
pnpm add lucide-react

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Run: npx tailwindcss init -p"
echo "2. Update tailwind.config.js with the configuration from SHADCN-UI-MIGRATION-GUIDE.md"
echo "3. Create components.json"
echo "4. Install shadcn/ui components: npx shadcn-ui@latest add card badge separator alert"
