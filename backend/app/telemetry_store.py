"""
In-Memory Telemetry Storage

Architecture: Storage layer
Purpose: Thread-safe storage for telemetry with 60-second rolling window

This module provides:
- Current telemetry message storage
- 60-second history buffer
- Thread-safe access
- Automatic pruning of old messages
"""

import asyncio
from collections import deque
from datetime import datetime, timedelta
from typing import Optional, List
from app.schemas import TelemetryMessage


class TelemetryStore:
    """
    In-memory storage for telemetry data.
    
    Maintains:
    - Latest telemetry message
    - 60-second rolling window of historical messages
    - Thread-safe access via asyncio.Lock
    """
    
    def __init__(self, history_duration_seconds: int = 60):
        self._current: Optional[TelemetryMessage] = None
        self._history: deque[TelemetryMessage] = deque()
        self._lock = asyncio.Lock()
        self._history_duration = timedelta(seconds=history_duration_seconds)
    
    async def store(self, message: TelemetryMessage) -> None:
        """
        Store a new telemetry message.
        
        Updates current message and appends to history.
        Automatically prunes messages older than 60 seconds.
        """
        async with self._lock:
            self._current = message
            self._history.append(message)
            self._prune_history()
    
    async def get_current(self) -> Optional[TelemetryMessage]:
        """
        Get the latest telemetry message.
        
        Returns None if no messages have been received yet.
        """
        async with self._lock:
            return self._current
    
    async def get_history(self, limit: Optional[int] = None) -> List[TelemetryMessage]:
        """
        Get recent telemetry history.
        
        Args:
            limit: Maximum number of messages to return (None = all)
        
        Returns:
            List of telemetry messages from the last 60 seconds
        """
        async with self._lock:
            history_list = list(self._history)
            if limit is not None:
                history_list = history_list[-limit:]
            return history_list
    
    def _prune_history(self) -> None:
        """
        Remove messages older than the history duration.
        
        Called automatically after each store operation.
        """
        if not self._history:
            return
        
        cutoff = datetime.fromisoformat(self._current.timestamp.replace('Z', '+00:00')) - self._history_duration
        
        while self._history:
            oldest = self._history[0]
            oldest_time = datetime.fromisoformat(oldest.timestamp.replace('Z', '+00:00'))
            
            if oldest_time < cutoff:
                self._history.popleft()
            else:
                break


# Global singleton instance
telemetry_store = TelemetryStore()
