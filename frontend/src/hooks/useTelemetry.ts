/**
 * Telemetry Hook
 * 
 * Architecture: Hooks Layer
 * Purpose: React hook for consuming telemetry stream
 * 
 * This hook provides components with access to the telemetry data stream.
 * It manages subscription lifecycle and maintains a rolling window of historical data.
 * 
 * Usage:
 *   const { current, history, isConnected, mode } = useTelemetry();
 * 
 * Design: Hybrid mode with automatic fallback
 * - Attempts to fetch from backend API first
 * - Falls back to mock telemetry if backend unavailable
 * - Polls every 2 seconds in API mode
 * - Seamless transition between modes
 */

import { useState, useEffect, useRef } from 'react';
import type { TelemetryMessage } from '../types/telemetry';
import { mockTelemetry } from '../data/mockTelemetry';
import { fetchLatestTelemetry, fetchTelemetryHistory, fetchBackendHealth } from '../api/telemetryApi';

type TelemetryMode = 'esp32' | 'simulator' | 'mock' | 'checking';

interface UseTelemetryResult {
  current: TelemetryMessage | null;
  history: TelemetryMessage[];
  isConnected: boolean;
  mode: TelemetryMode;
}

const POLL_INTERVAL_MS = 2000; // 2 seconds
const HISTORY_DURATION_MS = 60000; // 60 seconds
const RECONNECT_INTERVAL_MS = 5000; // 5 seconds - retry connection
const MAX_CONSECUTIVE_FAILURES = 3; // Number of failures before marking disconnected

/**
 * Hook for consuming telemetry stream
 * 
 * Returns:
 * - current: Latest telemetry message
 * - history: Array of messages from last 60 seconds
 * - isConnected: Whether telemetry source is active
 * - mode: Current data source ('backend' | 'mock' | 'checking')
 */
export function useTelemetry(): UseTelemetryResult {
  const [current, setCurrent] = useState<TelemetryMessage | null>(null);
  const [history, setHistory] = useState<TelemetryMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [mode, setMode] = useState<TelemetryMode>('checking');
  
  const pollIntervalRef = useRef<number | null>(null);
  const unsubscribeRef = useRef<(() => void) | null>(null);
  const consecutiveFailuresRef = useRef<number>(0);
  const reconnectIntervalRef = useRef<number | null>(null);

  useEffect(() => {
    let mounted = true;

    // Check backend availability and start appropriate mode
    async function initialize() {
      const backendHealth = await fetchBackendHealth();

      if (!mounted) return;

      if (backendHealth) {
        console.log('✓ Backend available - using API mode');
        startBackendMode(getTelemetryModeFromBackend(backendHealth.mode));
      } else {
        console.log('⚠ Backend unavailable - falling back to mock mode');
        startMockMode();
      }
    }

    initialize();

    // Cleanup on unmount
    return () => {
      mounted = false;
      cleanup();
    };
  }, []);

  /**
   * Start backend API polling mode
   */
  function startBackendMode(sourceMode: TelemetryMode) {
    setMode(sourceMode);
    setIsConnected(true);

    // Initial fetch
    fetchAndUpdate();

    // Poll every 2 seconds
    pollIntervalRef.current = window.setInterval(() => {
      fetchAndUpdate();
    }, POLL_INTERVAL_MS);
  }

  /**
   * Start mock telemetry mode
   */
  function startMockMode() {
    setMode('mock');
    setIsConnected(true);

    // Start mock generator
    mockTelemetry.start();

    // Subscribe to mock updates
    unsubscribeRef.current = mockTelemetry.subscribe((message) => {
      setCurrent(message);
      
      setHistory((prev) => {
        const updated = [...prev, message];
        return pruneHistory(updated);
      });
    });
  }

  /**
   * Fetch telemetry from backend and update state
   */
  async function fetchAndUpdate() {
    try {
      // Fetch latest message
      const latest = await fetchLatestTelemetry();
      
      if (latest) {
        setCurrent(latest);
        
        // Fetch history (limit to 30 messages for efficiency)
        const historyData = await fetchTelemetryHistory(30);
        setHistory(historyData);
        
        // Reset failure counter on success
        consecutiveFailuresRef.current = 0;
        
        // Ensure connected state is true
        if (!isConnected) {
          console.log('✓ Backend reconnected successfully');
          setIsConnected(true);
        }
      } else {
        // Backend returned null - might be starting up
        console.warn('Backend returned no data');
        handleBackendFailure();
      }
    } catch (error) {
      console.error('Error fetching telemetry:', error);
      handleBackendFailure();
    }
  }

  /**
   * Handle backend fetch failure
   */
  function handleBackendFailure() {
    consecutiveFailuresRef.current += 1;
    
    if (consecutiveFailuresRef.current >= MAX_CONSECUTIVE_FAILURES) {
      if (isConnected) {
        console.warn('⚠ Backend disconnected - marking as disconnected');
        setIsConnected(false);
        
        // Start reconnection attempts
        startReconnectionAttempts();
      }
    }
  }

  /**
   * Start periodic reconnection attempts
   */
  function startReconnectionAttempts() {
    // Don't start if already running
    if (reconnectIntervalRef.current !== null) {
      return;
    }
    
    console.log('Starting reconnection attempts...');
    
    reconnectIntervalRef.current = window.setInterval(async () => {
      console.log('Attempting to reconnect to backend...');
      const backendHealth = await fetchBackendHealth();
      
      if (backendHealth) {
        console.log('✓ Backend is back online - reconnecting');
        stopReconnectionAttempts();
        consecutiveFailuresRef.current = 0;
        setMode(getTelemetryModeFromBackend(backendHealth.mode));
        setIsConnected(true);
        
        // Resume polling
        fetchAndUpdate();
      }
    }, RECONNECT_INTERVAL_MS);
  }

  /**
   * Stop reconnection attempts
   */
  function stopReconnectionAttempts() {
    if (reconnectIntervalRef.current !== null) {
      clearInterval(reconnectIntervalRef.current);
      reconnectIntervalRef.current = null;
    }
  }

  /**
   * Cleanup resources
   */
  function cleanup() {
    // Clear polling interval
    if (pollIntervalRef.current !== null) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }

    // Clear reconnection interval
    stopReconnectionAttempts();

    // Unsubscribe from mock telemetry
    if (unsubscribeRef.current) {
      unsubscribeRef.current();
      unsubscribeRef.current = null;
    }

    // Stop mock generator
    mockTelemetry.stop();
    
    setIsConnected(false);
  }

  return { current, history, isConnected, mode };
}

function getTelemetryModeFromBackend(mode?: string): TelemetryMode {
  return mode?.toLowerCase() === 'serial' ? 'esp32' : 'simulator';
}

/**
 * Remove messages older than 60 seconds
 */
function pruneHistory(messages: TelemetryMessage[]): TelemetryMessage[] {
  if (messages.length === 0) return messages;

  const now = Date.now();
  const cutoff = now - HISTORY_DURATION_MS;

  return messages.filter((msg) => {
    const timestamp = new Date(msg.timestamp).getTime();
    return timestamp >= cutoff;
  });
}
