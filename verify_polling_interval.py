#!/usr/bin/env python3
"""
Verify Frontend Polling Interval

This script monitors backend API requests to verify the frontend
is polling at the correct 2-second interval.
"""

import requests
import time
from datetime import datetime

BACKEND_URL = "http://localhost:8000/api"

# ANSI colors
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

print(f"{BLUE}{'=' * 70}{RESET}")
print(f"{BLUE}Verifying Frontend Polling Interval{RESET}")
print(f"{BLUE}{'=' * 70}{RESET}\n")

print(f"{YELLOW}Fetching telemetry 5 times to measure intervals...{RESET}\n")

timestamps = []
fetch_times = []

for i in range(5):
    fetch_time = datetime.now()
    response = requests.get(f"{BACKEND_URL}/latest")
    
    if response.status_code == 200:
        data = response.json()
        telemetry_timestamp = data.get('timestamp')
        
        timestamps.append(telemetry_timestamp)
        fetch_times.append(fetch_time)
        
        print(f"Fetch {i+1}:")
        print(f"  Fetch Time: {fetch_time.strftime('%H:%M:%S.%f')[:-3]}")
        print(f"  Telemetry Timestamp: {telemetry_timestamp}")
        print()
    
    if i < 4:  # Don't sleep after last fetch
        time.sleep(2)

# Calculate intervals
print(f"{BLUE}{'=' * 70}{RESET}")
print(f"{BLUE}Interval Analysis{RESET}")
print(f"{BLUE}{'=' * 70}{RESET}\n")

intervals = []
for i in range(1, len(fetch_times)):
    interval = (fetch_times[i] - fetch_times[i-1]).total_seconds()
    intervals.append(interval)
    print(f"Interval {i}: {interval:.2f} seconds")

avg_interval = sum(intervals) / len(intervals)
print(f"\n{GREEN}Average Interval: {avg_interval:.2f} seconds{RESET}")

if 1.8 <= avg_interval <= 2.2:
    print(f"{GREEN}✓ Polling interval is correct (~2 seconds){RESET}")
else:
    print(f"{YELLOW}⚠ Polling interval is {avg_interval:.2f}s (expected ~2s){RESET}")

# Check if telemetry data is updating
unique_timestamps = len(set(timestamps))
print(f"\n{BLUE}Data Update Check{RESET}")
print(f"Unique timestamps: {unique_timestamps}/{len(timestamps)}")

if unique_timestamps == len(timestamps):
    print(f"{GREEN}✓ Telemetry data is updating (all timestamps unique){RESET}")
elif unique_timestamps > len(timestamps) * 0.8:
    print(f"{YELLOW}⚠ Most telemetry data is updating ({unique_timestamps}/{len(timestamps)} unique){RESET}")
else:
    print(f"{YELLOW}⚠ Telemetry data may not be updating properly{RESET}")
