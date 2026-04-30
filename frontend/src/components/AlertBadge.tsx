/**
 * AlertBadge Component
 * 
 * Purpose: Display alert messages with appropriate severity styling
 * Used for: Fail-safe warnings, error notifications, system alerts
 */

interface AlertBadgeProps {
  message: string;
  variant: 'error' | 'warning' | 'info' | 'success';
  icon?: string;
}

export function AlertBadge({ message, variant, icon }: AlertBadgeProps) {
  const className = `alert alert-${variant}`;
  
  return (
    <div className={className}>
      {icon && <span>{icon} </span>}
      {message}
    </div>
  );
}
