import React from 'react';
import { useCloudTelemetry } from '../hooks/useCloudTelemetry';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Separator } from '@/components/ui/separator';
import { Activity, Fuel, ShieldCheck, Leaf, Info, Zap, AlertTriangle, RefreshCw } from 'lucide-react';

// ============================================================================
// HELPER COMPONENTS
// ============================================================================

function StatusBadge({ status }: { status: string }) {
  const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
    'NORMAL': 'outline',
    'EFFICIENT': 'secondary',
    'HIGH TEMP': 'destructive',
    'WARNING': 'destructive',
    'LOW FUEL': 'default',
  };

  const colors: Record<string, string> = {
    'NORMAL': 'border-emerald-500 text-emerald-700 font-bold',
    'EFFICIENT': 'bg-emerald-100 text-emerald-800 font-bold',
    'HIGH TEMP': 'bg-red-100 text-red-800 font-bold',
    'WARNING': 'bg-red-100 text-red-800 font-bold',
    'LOW FUEL': 'bg-amber-100 text-amber-800 font-bold',
  };

  return (
    <Badge 
      variant={variants[status] || 'outline'} 
      className={colors[status] || ''}
    >
      {status}
    </Badge>
  );
}

// ============================================================================
// MAIN DASHBOARD
// ============================================================================

export function CloudDashboard() {
  const { current, fleet, history, summary, isConnected, mode, aiInsight, refreshAIInsight } = useCloudTelemetry();

  if (!current) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900 mx-auto mb-4"></div>
          <p className="text-slate-700 font-bold">Synchronizing with Fleet Infrastructure...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans p-4 md:p-8">
      {/* Header */}
      <header className="max-w-7xl mx-auto mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 flex items-center gap-2">
            🚛 Agentic AI Smart Fleet Monitoring
          </h1>
          <p className="text-slate-600 font-medium text-sm mt-1">
            Real-time multi-fuel optimization, roadworthiness alerts, and climate impact analytics.
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-full border border-slate-200 shadow-sm">
            <span className={`h-2.5 w-2.5 rounded-full ${isConnected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></span>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
              {mode === 'live' ? 'Live Telemetry' : 'Prototype Demo'}
            </span>
          </div>
          <Button variant="outline" size="sm" onClick={() => window.location.reload()} className="font-bold">
            <RefreshCw className="h-4 w-4 mr-2" /> System Sync
          </Button>
        </div>
      </header>

      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Hero Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="shadow-md border-slate-200">
            <CardHeader>
              <CardTitle className="text-xl flex items-center gap-2">
                <Info className="h-5 w-5 text-blue-600" /> Strategic Intelligence
              </CardTitle>
              <CardDescription className="text-slate-600 font-medium leading-relaxed">
                A scalable IoT platform bridging edge sensor data (ESP32) with cloud-based Agentic AI. 
                Optimizing Keke, Bus, and Taxi fleets for fuel efficiency and sustainability.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2 items-center">
                <Badge variant="secondary" className="bg-blue-50 text-blue-700">Observe</Badge>
                <span className="text-slate-300">→</span>
                <Badge variant="secondary" className="bg-blue-50 text-blue-700">Decide</Badge>
                <span className="text-slate-300">→</span>
                <Badge variant="secondary" className="bg-blue-50 text-blue-700">Act</Badge>
                <span className="text-slate-300">→</span>
                <Badge variant="secondary" className="bg-blue-50 text-blue-700">Explain</Badge>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-md border-slate-200">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-bold text-slate-500 uppercase tracking-widest">Data Control Pipeline</CardTitle>
            </CardHeader>
            <CardContent className="flex justify-between items-center py-6">
              {[
                { icon: "📟", label: "ESP32" },
                { icon: "☁️", label: "Cloud" },
                { icon: "🤖", label: "AI" },
                { icon: "📊", label: "Live" }
              ].map((node, i) => (
                <React.Fragment key={node.label}>
                  <div className="flex flex-col items-center gap-2">
                    <div className="h-12 w-12 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-center text-2xl shadow-inner">
                      {node.icon}
                    </div>
                    <span className="text-[10px] font-black text-slate-600 uppercase">{node.label}</span>
                  </div>
                  {i < 3 && <div className="flex-1 h-0.5 bg-slate-100 mx-2"></div>}
                </React.Fragment>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Fleet KPI Row */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { label: "Vehicles Online", value: summary?.total_vehicles || 5, unit: "", icon: Activity, color: "text-blue-600" },
            { label: "High Temp Alerts", value: summary?.status_distribution['HIGH TEMP'] || 0, unit: "", icon: AlertTriangle, color: "text-red-600" },
            { label: "Avg. Fuel Level", value: "64", unit: "%", icon: Fuel, color: "text-amber-600" },
            { label: "CO2 Reduced", value: summary?.total_co2_reduction || 0, unit: "kg", icon: Leaf, color: "text-emerald-600" },
            { label: "Estimated Savings", value: summary?.total_cost_saved || 0, unit: "₦", icon: Zap, color: "text-blue-700" },
            { label: "Active Fuel", value: current.fuel_mode, unit: "", icon: ShieldCheck, color: "text-indigo-600" }
          ].map((kpi, i) => (
            <Card key={i} className="shadow-sm border-slate-200 hover:border-slate-300 transition-colors">
              <CardContent className="p-4">
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
                  <kpi.icon className={`h-3 w-3 ${kpi.color}`} /> {kpi.label}
                </p>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-black text-slate-900">{kpi.value}</span>
                  {kpi.unit && <span className="text-xs font-bold text-slate-500 uppercase">{kpi.unit}</span>}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Operational Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Vehicle List */}
          <div className="lg:col-span-2 space-y-6">
            <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              🚛 Live Vehicle Monitoring
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {fleet.map((v, i) => (
                <Card key={i} className="shadow-sm hover:shadow-md transition-shadow border-slate-200">
                  <CardContent className="p-4">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="font-black text-lg text-slate-900 leading-none">{v.vehicle_id}</h4>
                        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-tighter">{v.vehicle_type.replace('_', ' ')}</span>
                      </div>
                      <StatusBadge status={v.status} />
                    </div>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-[9px] font-black text-slate-500 uppercase block mb-1">Temperature</span>
                        <span className="font-bold text-slate-700">{v.temperature}°C</span>
                      </div>
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-[9px] font-black text-slate-500 uppercase block mb-1">Fuel Percent</span>
                        <span className="font-bold text-slate-700">{v.fuel_percent}%</span>
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-xs border-t border-slate-100 pt-3">
                      <div className="flex gap-3 text-slate-600 font-bold">
                        <span className={v.relay1 === 'ON' ? 'text-blue-600' : ''}>R1: {v.relay1}</span>
                        <span className={v.relay2 === 'ON' ? 'text-blue-600' : ''}>R2: {v.relay2}</span>
                      </div>
                      <span className="font-black text-blue-700 uppercase tracking-widest">{v.fuel_mode}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Telemetry Log Table */}
            <div className="mt-12">
              <h3 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
                📋 Telemetry Transaction Log
              </h3>
              <div className="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
                <Table>
                  <TableHeader className="bg-slate-50">
                    <TableRow>
                      <TableHead className="font-black text-slate-600 uppercase text-[10px]">Timestamp</TableHead>
                      <TableHead className="font-black text-slate-600 uppercase text-[10px]">Vehicle</TableHead>
                      <TableHead className="font-black text-slate-600 uppercase text-[10px]">Temp</TableHead>
                      <TableHead className="font-black text-slate-600 uppercase text-[10px]">Fuel</TableHead>
                      <TableHead className="font-black text-slate-600 uppercase text-[10px]">Mode</TableHead>
                      <TableHead className="font-black text-slate-600 uppercase text-[10px]">Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {history.slice(-10).reverse().map((row, idx) => (
                      <TableRow key={idx} className="hover:bg-slate-50/50">
                        <TableCell className="text-slate-600 font-medium text-xs">
                          {new Date(row.received_at || row.timestamp || Date.now()).toLocaleTimeString()}
                        </TableCell>
                        <TableCell className="font-black text-slate-900">{row.vehicle_id}</TableCell>
                        <TableCell className="text-slate-700 font-bold">{row.temperature}°C</TableCell>
                        <TableCell className="text-slate-700 font-bold">{row.fuel_percent}%</TableCell>
                        <TableCell className="font-black text-blue-700">{row.fuel_mode}</TableCell>
                        <TableCell><StatusBadge status={row.status} /></TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>
          </div>

          {/* Sidebar Panels */}
          <aside className="space-y-6">
            
            {/* AI Insight Panel */}
            <Card className="bg-slate-900 text-white border-none shadow-xl overflow-hidden">
              <CardHeader className="pb-4">
                <div className="flex justify-between items-center">
                  <CardTitle className="text-white flex items-center gap-2">
                    <Zap className="h-5 w-5 text-amber-400" /> AI Agent Logic
                  </CardTitle>
                  <Button variant="ghost" size="sm" onClick={refreshAIInsight} className="text-white hover:bg-white/10 p-0 h-auto">
                    <RefreshCw className="h-4 w-4" />
                  </Button>
                </div>
                <CardDescription className="text-slate-400 font-bold text-xs uppercase tracking-widest">Observe → Decide → Act → Explain</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6 pt-2">
                {aiInsight ? (
                  <div className="space-y-6">
                    {[
                      { num: 1, title: "Observe", text: `Processing ${current.temperature}°C and ${current.fuel_percent}% fuel sensors.` },
                      { num: 2, title: "Decide", text: aiInsight.recommendation },
                      { num: 3, title: "Act", text: `Relay systems optimized. Current Mode: ${current.fuel_mode}.` },
                      { num: 4, title: "Explain", text: aiInsight.climate_note }
                    ].map((step) => (
                      <div key={step.num} className="flex gap-4">
                        <div className="h-6 w-6 rounded-full bg-blue-600 flex items-center justify-center text-[10px] font-black shrink-0 border border-white/20 shadow-lg shadow-blue-500/20">
                          {step.num}
                        </div>
                        <div>
                          <h5 className="text-[10px] font-black text-slate-500 uppercase mb-1 tracking-tighter">{step.title}</h5>
                          <p className="text-sm font-bold leading-tight text-slate-100">{step.text}</p>
                        </div>
                      </div>
                    ))}
                    <Separator className="bg-white/10" />
                    <div className="p-3 bg-white/5 rounded-lg border border-white/10 italic text-xs text-slate-300 font-medium leading-relaxed">
                      "Operator: {aiInsight.operator_message}"
                    </div>
                  </div>
                ) : (
                  <div className="py-12 text-center text-slate-500 font-bold text-sm">Synchronizing fleet decision matrix...</div>
                )}
              </CardContent>
            </Card>

            {/* Climate & Policy Impact */}
            <Card className="bg-emerald-50 border-emerald-200 shadow-sm">
              <CardHeader>
                <CardTitle className="text-emerald-900 flex items-center gap-2">
                  <Leaf className="h-5 w-5 text-emerald-600" /> Climate Intelligence
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex justify-between items-end">
                  <div>
                    <span className="text-3xl font-black text-emerald-700">-{current.co2_reduction}kg</span>
                    <span className="block text-[10px] font-black text-emerald-600 uppercase tracking-wider">Estimated CO2 Reduction</span>
                  </div>
                  <div className="text-right">
                    <span className="text-xl font-black text-emerald-800">92%</span>
                    <span className="block text-[10px] font-black text-emerald-600 uppercase tracking-wider">Net-Zero Alignment</span>
                  </div>
                </div>
                <Separator className="bg-emerald-200" />
                <div className="space-y-4">
                  <h4 className="text-[10px] font-black text-emerald-800 uppercase tracking-tighter">📜 Policy & Adoption Readiness</h4>
                  <ul className="space-y-3">
                    {[
                      "Real-time roadworthiness monitoring",
                      "Government emission regulation auditing",
                      "Fuel usage transparency & cost verification",
                      "Keke/Bus compliance program ready"
                    ].map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-xs font-bold text-emerald-900">
                        <ShieldCheck className="h-3.5 w-3.5 text-emerald-600 shrink-0" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <p className="text-[10px] italic text-emerald-700/70 font-bold border-t border-emerald-200 pt-4 leading-normal">
                  *CO2 values are modeled prototype estimates pending hardware calibration.
                </p>
              </CardContent>
            </Card>
          </aside>
        </div>
      </div>

      <footer className="max-w-7xl mx-auto mt-16 pt-8 border-t border-slate-200 text-center text-slate-500 font-bold text-[10px] uppercase tracking-widest">
        Agentic AI Smart Fleet Monitoring Platform | Designed for Net-Zero Mobility | v2.2.0
      </footer>
    </div>
  );
}
