/**
 * MetricCard Component
 * 
 * Purpose: Display metric values with visual progress indicators
 * Used for: Temperature monitoring, efficiency metrics, any numeric KPIs
 */

interface MetricCardProps {
  label: string;
  value: number;
  unit: string;
  threshold?: number;
  warning?: boolean;
  showBar?: boolean;
  icon?: string;
}

export function MetricCard({ 
  label, 
  value, 
  unit, 
  threshold, 
  warning = false,
  showBar = true,
  icon
}: MetricCardProps) {
  const cardClass = warning ? 'card temp-card warning' : 'card temp-card';
  const percentage = threshold ? Math.min((value / threshold) * 100, 100) : 0;

  return (
    <div className={cardClass}>
      {icon && <div className="card-icon">{icon}</div>}
      <h3>{label}</h3>
      <div className="temp-value">
        {value.toFixed(1)} <span className="temp-unit">{unit}</span>
      </div>
      {showBar && threshold && (
        <>
          <div className="temp-bar">
            <div 
              className="temp-bar-fill" 
              style={{ width: `${percentage}%` }}
            ></div>
          </div>
          <div className="temp-threshold">Threshold: {threshold}{unit}</div>
        </>
      )}
    </div>
  );
}
