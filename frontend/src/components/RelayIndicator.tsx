/**
 * RelayIndicator Component
 * 
 * Purpose: Visual indicator for relay state (ON/OFF)
 * Used for: Hardware relay status display with visual feedback
 */

interface RelayIndicatorProps {
  label: string;
  state: boolean;
  description: string;
}

export function RelayIndicator({ label, state, description }: RelayIndicatorProps) {
  return (
    <div className={`relay-indicator ${state ? 'relay-on' : 'relay-off'}`}>
      <div className="relay-status">
        <div className="relay-light"></div>
        <div className="relay-label">{label}</div>
      </div>
      <div className="relay-state">{state ? 'ON' : 'OFF'}</div>
      <div className="relay-description">{description}</div>
    </div>
  );
}
