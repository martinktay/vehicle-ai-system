#!/usr/bin/env python3
"""Kill any process listening on port 8000"""

import psutil
import sys

def kill_port_8000():
    """Kill any process listening on port 8000"""
    killed = False
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if hasattr(conn.laddr, 'port') and conn.laddr.port == 8000:
                    print(f"Killing process: PID {proc.pid}, Name: {proc.name()}")
                    proc.kill()
                    proc.wait(timeout=3)
                    killed = True
                    print(f"✓ Killed PID {proc.pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
            print(f"Could not kill process: {e}")
            pass
    
    if not killed:
        print("No process found listening on port 8000")
    
    return killed

if __name__ == "__main__":
    kill_port_8000()
