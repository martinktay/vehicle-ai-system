/**
 * StatusCard Component
 * 
 * Purpose: Display status information with color-coded badges
 * Used for: System status, connection status, power source indicators
 */

interface StatusCardProps {
  label: string;
  value: string;
  variant: 'ok' | 'warning' | 'error' | 'info';
}

export function StatusCard({ label, value, variant }: StatusCardProps) {
  const className = `status-badge status-${variant}`;
  
  return (
    <div className={className}>
      <span className="status-label">{label}:</span>
      <span className="status-value">{value}</span>
    </div>
  );
}
