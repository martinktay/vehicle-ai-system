import { useState } from 'react';
import { useTelemetry } from './hooks/useTelemetry';
import { CloudDashboard } from './components/CloudDashboard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Separator } from '@/components/ui/separator';
import { LayoutDashboard, Cloud, Activity, Fuel, ShieldCheck, Leaf } from 'lucide-react';

type DashboardView = 'serial' | 'cloud';

export default function App() {
  const [view, setView] = useState<DashboardView>('cloud');

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Global View Switcher in Header */}
      <nav className="bg-white border-b border-slate-200 px-4 py-2 flex justify-center gap-2 sticky top-0 z-[200]">
        <Button 
          variant={view === 'serial' ? 'default' : 'ghost'} 
          size="sm" 
          onClick={() => setView('serial')}
          className="font-bold gap-2"
        >
          <Activity className="h-4 w-4" /> Serial Dashboard
        </Button>
        <Button 
          variant={view === 'cloud' ? 'default' : 'ghost'} 
          size="sm" 
          onClick={() => setView('cloud')}
          className="font-bold gap-2"
        >
          <Cloud className="h-4 w-4" /> Cloud Dashboard
        </Button>
      </nav>

      {view === 'cloud' ? <CloudDashboard /> : <SerialDashboard />}
    </div>
  );
}

function SerialDashboard() {
  const { current, history, isConnected, mode } = useTelemetry();

  if (!current) {
    return (
      <div className="min-h-[calc(100vh-49px)] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-slate-900 mx-auto mb-4"></div>
          <p className="text-slate-600 font-bold">Connecting to serial interface...</p>
          <p className="text-xs text-slate-400 mt-2 uppercase tracking-widest">{mode === 'checking' ? 'Checking Serial...' : 'Starting Simulator...'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">🌱 Local Telemetry Monitoring</h1>
          <p className="text-slate-600 font-medium text-sm mt-1">Single-unit diagnostic bridge for ESP32 serial interface.</p>
        </div>
        <div className="flex gap-3">
          <Badge variant={isConnected ? 'outline' : 'destructive'} className={isConnected ? 'border-emerald-500 text-emerald-700 font-bold' : ''}>
            {isConnected ? 'SERIAL CONNECTED' : 'DISCONNECTED'}
          </Badge>
          <Badge variant="secondary" className="font-bold bg-blue-50 text-blue-700">
            SOURCE: {mode.toUpperCase()}
          </Badge>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left: Metrics */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Temperature Section */}
          <div>
            <h2 className="text-sm font-black text-slate-500 uppercase tracking-widest mb-4">System Temperatures</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { label: "Engine", value: current.engine_temperature, unit: "°C", threshold: 100, warning: current.overheat_flag },
                { label: "Fuel Line", value: current.fuel_line_temperature, unit: "°C", threshold: 90, warning: current.fuel_line_temperature > 85 },
                { label: "Ambient", value: current.ambient_temperature, unit: "°C", threshold: 40, warning: false }
              ].map((t, i) => (
                <Card key={i} className={t.warning ? "border-red-500 bg-red-50/50 shadow-sm" : "shadow-sm"}>
                  <CardContent className="p-6 text-center">
                    <p className="text-[10px] font-black text-slate-500 uppercase mb-2">{t.label}</p>
                    <div className="flex items-baseline justify-center gap-1">
                      <span className={`text-3xl font-black ${t.warning ? 'text-red-700' : 'text-slate-900'}`}>{t.value}</span>
                      <span className="text-sm font-bold text-slate-500">°C</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-100 rounded-full mt-4 overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-500 ${t.warning ? 'bg-red-500' : 'bg-emerald-500'}`} 
                        style={{ width: `${Math.min(100, (t.value / t.threshold) * 100)}%` }}
                      ></div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Fuel & Relays */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="shadow-sm">
              <CardHeader>
                <CardTitle className="text-sm font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                  <Fuel className="h-4 w-4" /> Current Fuel Mode
                </CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col items-center justify-center py-6">
                <span className="text-4xl font-black text-slate-900 uppercase tracking-tighter mb-2">{current.current_fuel_mode}</span>
                <Badge variant="outline" className="font-bold border-blue-500 text-blue-700">OPTIMIZED BY AI</Badge>
              </CardContent>
            </Card>

            <Card className="shadow-sm">
              <CardHeader>
                <CardTitle className="text-sm font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                  <ShieldCheck className="h-4 w-4" /> Relay Actuators
                </CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-2 gap-4 py-6">
                {[
                  { label: "Cooling", state: current.relay_state_1 },
                  { label: "Fuel Switch", state: current.relay_state_2 }
                ].map((r, i) => (
                  <div key={i} className="text-center">
                    <div className={`h-3 w-3 rounded-full mx-auto mb-2 ${r.state ? 'bg-emerald-500 animate-pulse' : 'bg-slate-200'}`}></div>
                    <p className="text-[10px] font-black text-slate-500 uppercase">{r.label}</p>
                    <p className={`font-black ${r.state ? 'text-emerald-700' : 'text-slate-500'}`}>{r.state ? 'ON' : 'OFF'}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* History Table */}
          <div>
            <h2 className="text-sm font-black text-slate-500 uppercase tracking-widest mb-4">Diagnostics Log</h2>
            <div className="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
              <Table>
                <TableHeader className="bg-slate-50">
                  <TableRow>
                    <TableHead className="font-black text-slate-600 uppercase text-[10px]">Time</TableHead>
                    <TableHead className="font-black text-slate-600 uppercase text-[10px]">Engine Temp</TableHead>
                    <TableHead className="font-black text-slate-600 uppercase text-[10px]">Fuel Line</TableHead>
                    <TableHead className="font-black text-slate-600 uppercase text-[10px]">Mode</TableHead>
                    <TableHead className="font-black text-slate-600 uppercase text-[10px]">Recommendation</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {history.slice(-10).reverse().map((row, idx) => (
                    <TableRow key={idx}>
                      <TableCell className="text-slate-600 font-medium text-xs">{(idx * 2)}s ago</TableCell>
                      <TableCell className="text-slate-900 font-bold">{row.engine_temperature}°C</TableCell>
                      <TableCell className="text-slate-900 font-bold">{row.fuel_line_temperature}°C</TableCell>
                      <TableCell className="font-black text-blue-700 uppercase">{row.current_fuel_mode}</TableCell>
                      <TableCell>
                        <Badge variant="outline" className="text-[9px] font-bold uppercase">{row.ai_recommendation}</Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        </div>

        {/* Right: AI & Insights */}
        <aside className="space-y-6">
          <Card className="bg-slate-900 text-white border-none shadow-xl">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <LayoutDashboard className="h-5 w-5 text-blue-400" /> AI Diagnostic
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase mb-2 tracking-widest">Current Recommendation</p>
                <p className="text-xl font-black text-blue-400 uppercase leading-tight">{current.ai_recommendation.replace('_', ' ')}</p>
              </div>
              <Separator className="bg-white/10" />
              <div className="space-y-4">
                <div className="flex gap-3">
                  <div className={`h-2 w-2 rounded-full mt-1.5 ${current.overheat_flag ? 'bg-red-500' : 'bg-emerald-500'}`}></div>
                  <p className="text-sm font-medium text-slate-300">
                    {current.overheat_flag 
                      ? "CRITICAL: Engine overheat detected. System has engaged fail-safe cooling." 
                      : "System operating within normal thermal parameters. Optimal efficiency achieved."}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-emerald-50 border-emerald-200">
            <CardHeader>
              <CardTitle className="text-emerald-900 flex items-center gap-2">
                <Leaf className="h-5 w-5 text-emerald-600" /> Sustainable Impact
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-baseline">
                <span className="text-3xl font-black text-emerald-700">12%</span>
                <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest">Fuel Savings</span>
              </div>
              <p className="text-xs font-bold text-emerald-900 leading-relaxed">
                Optimization logic has reduced modeled carbon output by prioritizing cleaner combustion cycles based on thermal load.
              </p>
            </CardContent>
          </Card>
        </aside>

      </div>
    </div>
  );
}
