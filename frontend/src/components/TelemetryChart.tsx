/**
 * TelemetryChart Component
 * 
 * Purpose: Display live telemetry data as time-series line chart
 * Used for: Temperature monitoring over 60-second rolling window
 */

import type { TelemetryMessage } from '../types/telemetry';

interface TelemetryChartProps {
  history: TelemetryMessage[];
  title?: string;
}

interface ChartLine {
  label: string;
  color: string;
  dataKey: keyof Pick<TelemetryMessage, 'engine_temperature' | 'fuel_line_temperature' | 'ambient_temperature'>;
}

const CHART_LINES: ChartLine[] = [
  { label: 'Engine', color: '#e74c3c', dataKey: 'engine_temperature' },
  { label: 'Fuel Line', color: '#f39c12', dataKey: 'fuel_line_temperature' },
  { label: 'Ambient', color: '#3498db', dataKey: 'ambient_temperature' },
];

export function TelemetryChart({ history, title = 'Live Telemetry Stream' }: TelemetryChartProps) {
  if (history.length === 0) {
    return (
      <section className="section">
        <h2>{title}</h2>
        <div className="card">
          <p className="chart-placeholder">Collecting data...</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section">
      <h2>{title}</h2>
      <div className="card chart-card">
        <ChartLegend lines={CHART_LINES} />
        <div className="chart">
          <Chart history={history} lines={CHART_LINES} />
        </div>
        <div className="chart-info">
          <div className="chart-info-item">
            <strong>Data Points:</strong> {history.length} readings
          </div>
          <div className="chart-info-item">
            <strong>Time Window:</strong> Last 60 seconds
          </div>
          <div className="chart-info-item">
            <strong>Optimal Range:</strong> 80-90°C (green zone)
          </div>
          <div className="chart-info-item">
            <strong>Critical Threshold:</strong> 100°C (red line)
          </div>
        </div>
      </div>
    </section>
  );
}

/**
 * Chart Legend Component
 */
function ChartLegend({ lines }: { lines: ChartLine[] }) {
  return (
    <div className="chart-legend">
      {lines.map((line) => (
        <span key={line.dataKey} className="legend-item">
          <span className="legend-color" style={{ backgroundColor: line.color }}></span>
          {line.label}
        </span>
      ))}
    </div>
  );
}

/**
 * SVG Chart Component with Calibrated Axes
 */
function Chart({ history, lines }: { 
  history: TelemetryMessage[]; 
  lines: ChartLine[];
}) {
  const chartHeight = 300;
  const chartWidth = 900;
  const paddingLeft = 65;
  const paddingRight = 30;
  const paddingTop = 20;
  const paddingBottom = 45;
  
  const plotWidth = chartWidth - paddingLeft - paddingRight;
  const plotHeight = chartHeight - paddingTop - paddingBottom;

  // Y-axis calibration: Dynamic scale based on data with padding
  const allTemps = history.flatMap(msg => [
    msg.engine_temperature,
    msg.fuel_line_temperature,
    msg.ambient_temperature
  ]);
  
  const dataMinY = Math.min(...allTemps);
  const dataMaxY = Math.max(...allTemps);
  
  // Add 10% padding above and below, but ensure we include critical thresholds
  const padding = (dataMaxY - dataMinY) * 0.15;
  let minY = Math.max(0, Math.floor((dataMinY - padding) / 10) * 10);
  let maxY = Math.ceil((dataMaxY + padding) / 10) * 10;
  
  // Ensure we always show the optimal range (80-90°C) and critical threshold (100°C)
  if (maxY < 100) maxY = 110;
  if (minY > 70) minY = Math.max(0, Math.floor(dataMinY / 10) * 10 - 10);
  
  // Ensure minimum range of 40°C for readability
  if (maxY - minY < 40) {
    const center = (maxY + minY) / 2;
    minY = Math.max(0, Math.floor((center - 20) / 10) * 10);
    maxY = Math.ceil((center + 20) / 10) * 10;
  }
  
  // Calculate Y-axis tick marks (every 10°C for better granularity)
  const yTicks = [];
  const yTickInterval = (maxY - minY) > 60 ? 20 : 10;
  for (let temp = minY; temp <= maxY; temp += yTickInterval) {
    const y = paddingTop + plotHeight - ((temp - minY) / (maxY - minY)) * plotHeight;
    yTicks.push({ value: temp, y });
  }
  
  // Calculate X-axis tick marks (every 10 seconds)
  const xTicks = [];
  const timeSpan = 60; // 60 second window
  for (let sec = 0; sec <= timeSpan; sec += 10) {
    const x = paddingLeft + (sec / timeSpan) * plotWidth;
    xTicks.push({ value: sec, x });
  }

  // Map data points to chart coordinates
  const points = history.map((msg, i) => {
    const x = paddingLeft + (i / Math.max(history.length - 1, 1)) * plotWidth;
    const point: any = { x };
    
    lines.forEach((line) => {
      const value = msg[line.dataKey] as number;
      const normalizedValue = Math.max(minY, Math.min(maxY, value));
      point[line.dataKey] = paddingTop + plotHeight - ((normalizedValue - minY) / (maxY - minY)) * plotHeight;
    });
    
    return point;
  });

  const createPath = (dataKey: string) => {
    return points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p[dataKey]}`).join(' ');
  };

  return (
    <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="chart-svg">
      {/* Grid lines (horizontal) */}
      {yTicks.map((tick) => (
        <line
          key={`grid-h-${tick.value}`}
          x1={paddingLeft}
          y1={tick.y}
          x2={chartWidth - paddingRight}
          y2={tick.y}
          stroke="#2d3748"
          strokeWidth="1"
          strokeDasharray="3 3"
          opacity="0.4"
        />
      ))}
      
      {/* Grid lines (vertical) */}
      {xTicks.map((tick) => (
        <line
          key={`grid-v-${tick.value}`}
          x1={tick.x}
          y1={paddingTop}
          x2={tick.x}
          y2={chartHeight - paddingBottom}
          stroke="#2d3748"
          strokeWidth="1"
          strokeDasharray="3 3"
          opacity="0.4"
        />
      ))}
      
      {/* Y-axis */}
      <line
        x1={paddingLeft}
        y1={paddingTop}
        x2={paddingLeft}
        y2={chartHeight - paddingBottom}
        stroke="#4a5568"
        strokeWidth="2"
      />
      
      {/* X-axis */}
      <line
        x1={paddingLeft}
        y1={chartHeight - paddingBottom}
        x2={chartWidth - paddingRight}
        y2={chartHeight - paddingBottom}
        stroke="#4a5568"
        strokeWidth="2"
      />
      
      {/* Y-axis labels */}
      {yTicks.map((tick) => (
        <text
          key={`label-y-${tick.value}`}
          x={paddingLeft - 10}
          y={tick.y + 4}
          textAnchor="end"
          fill="#94a3b8"
          fontSize="12"
          fontFamily="system-ui, sans-serif"
        >
          {tick.value}°C
        </text>
      ))}
      
      {/* X-axis labels */}
      {xTicks.map((tick) => (
        <text
          key={`label-x-${tick.value}`}
          x={tick.x}
          y={chartHeight - paddingBottom + 20}
          textAnchor="middle"
          fill="#94a3b8"
          fontSize="12"
          fontFamily="system-ui, sans-serif"
        >
          -{timeSpan - tick.value}s
        </text>
      ))}
      
      {/* Axis titles */}
      <text
        x={paddingLeft / 2 - 15}
        y={chartHeight / 2}
        textAnchor="middle"
        fill="#e2e8f0"
        fontSize="14"
        fontWeight="600"
        fontFamily="system-ui, sans-serif"
        transform={`rotate(-90, ${paddingLeft / 2 - 15}, ${chartHeight / 2})`}
      >
        Temperature (°C)
      </text>
      
      <text
        x={chartWidth / 2}
        y={chartHeight - 5}
        textAnchor="middle"
        fill="#e2e8f0"
        fontSize="14"
        fontWeight="600"
        fontFamily="system-ui, sans-serif"
      >
        Time (seconds ago)
      </text>
      
      {/* Critical threshold line (100°C overheat) - only show if in range */}
      {minY <= 100 && maxY >= 100 && (() => {
        const criticalY = paddingTop + plotHeight - ((100 - minY) / (maxY - minY)) * plotHeight;
        return (
          <>
            <line
              x1={paddingLeft}
              y1={criticalY}
              x2={chartWidth - paddingRight}
              y2={criticalY}
              stroke="#dc2626"
              strokeWidth="2.5"
              strokeDasharray="8 4"
              opacity="0.7"
            />
            <text
              x={chartWidth - paddingRight - 5}
              y={criticalY - 6}
              textAnchor="end"
              fill="#dc2626"
              fontSize="11"
              fontWeight="700"
              fontFamily="system-ui, sans-serif"
            >
              ⚠ Critical (100°C)
            </text>
          </>
        );
      })()}
      
      {/* Optimal range indicator (80-90°C) - only show if in range */}
      {minY <= 90 && maxY >= 80 && (() => {
        const optimalTop = paddingTop + plotHeight - ((Math.min(90, maxY) - minY) / (maxY - minY)) * plotHeight;
        const optimalBottom = paddingTop + plotHeight - ((Math.max(80, minY) - minY) / (maxY - minY)) * plotHeight;
        return (
          <>
            <rect
              x={paddingLeft}
              y={optimalTop}
              width={plotWidth}
              height={optimalBottom - optimalTop}
              fill="#10b981"
              opacity="0.12"
            />
            <text
              x={paddingLeft + 5}
              y={optimalTop + (optimalBottom - optimalTop) / 2 + 4}
              fill="#10b981"
              fontSize="10"
              fontWeight="600"
              fontFamily="system-ui, sans-serif"
              opacity="0.7"
            >
              Optimal Range
            </text>
          </>
        );
      })()}
      
      {/* Data lines with smooth curves */}
      {lines.map((line) => (
        <path
          key={line.dataKey}
          d={createPath(line.dataKey)}
          stroke={line.color}
          strokeWidth="2.5"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          opacity="0.9"
        />
      ))}
      
      {/* Data points (last point for each line with glow effect) */}
      {points.length > 0 && lines.map((line) => {
        const lastPoint = points[points.length - 1];
        return (
          <g key={`point-${line.dataKey}`}>
            {/* Glow effect */}
            <circle
              cx={lastPoint.x}
              cy={lastPoint[line.dataKey]}
              r="6"
              fill={line.color}
              opacity="0.3"
            />
            {/* Main point */}
            <circle
              cx={lastPoint.x}
              cy={lastPoint[line.dataKey]}
              r="4"
              fill={line.color}
              stroke="#1a202c"
              strokeWidth="2"
            />
          </g>
        );
      })}
    </svg>
  );
}
