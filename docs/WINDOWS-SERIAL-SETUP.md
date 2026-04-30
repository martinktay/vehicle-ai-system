# Windows Serial Port Setup Guide

**For ESP32 Climate-Smart Telemetry Controller**  
**Platform**: Windows 10/11  
**Last Updated**: 2026-04-06

---

## Overview

This guide helps you set up serial communication between your Windows PC and the ESP32 hardware. Windows handles serial ports differently than Linux, so this guide provides Windows-specific instructions.

---

## Step 1: Install USB Drivers

### Check if Drivers are Needed

1. **Connect ESP32** via USB cable
2. **Open Device Manager**:
   - Press `Win + X`
   - Select "Device Manager"
3. **Look for ESP32** under "Ports (COM & LPT)":
   - Should show: "USB-SERIAL CH340 (COM3)" or similar
   - If you see "Unknown Device" with yellow warning, drivers are needed

### Install CH340 Drivers (if needed)

Most ESP32 boards use CH340 USB-to-Serial chip:

1. **Download driver**:
   - Visit: https://www.wch.cn/downloads/CH341SER_EXE.html
   - Or search: "CH340 driver Windows"

2. **Install driver**:
   - Run `CH341SER.EXE`
   - Click "INSTALL"
   - Restart computer if prompted

3. **Verify installation**:
   - Open Device Manager again
   - Should now show "USB-SERIAL CH340 (COM3)"
   - Note the COM port number (e.g., COM3, COM4)

---

## Step 2: Find COM Port Number

### Method 1: Device Manager

1. **Open Device Manager** (`Win + X` → Device Manager)
2. **Expand "Ports (COM & LPT)"**
3. **Find your ESP32**:
   - Look for "USB-SERIAL CH340 (COM3)"
   - Or "Silicon Labs CP210x (COM4)"
   - Note the COM number

### Method 2: PowerShell

```powershell
# List all COM ports
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID

# Output example:
# Name                          DeviceID
# ----                          --------
# USB-SERIAL CH340 (COM3)       COM3
```

### Method 3: Python

```python
# Install pyserial first: pip install pyserial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"{port.device}: {port.description}")

# Output example:
# COM3: USB-SERIAL CH340 (COM3)
```

---

## Step 3: Configure Backend for Windows

### Edit Backend Configuration

1. **Navigate to backend folder**:
   ```powershell
   cd backend
   ```

2. **Copy environment template**:
   ```powershell
   copy .env.example .env
   ```

3. **Edit .env file** (use Notepad or VS Code):
   ```powershell
   notepad .env
   ```

4. **Set Windows COM port**:
   ```bash
   INGESTION_MODE=serial
   SERIAL_PORT=COM3          # Change to your COM port number
   SERIAL_BAUD_RATE=115200
   ```

5. **Save and close**

---

## Step 4: Test Serial Connection

### Method 1: PuTTY (Recommended)

1. **Download PuTTY**:
   - Visit: https://www.putty.org/
   - Download and install

2. **Configure PuTTY**:
   - Connection type: Serial
   - Serial line: COM3 (your port)
   - Speed: 115200
   - Click "Open"

3. **Expected output**:
   - JSON telemetry messages every 2 seconds
   - If blank, press ESP32 reset button

4. **Exit**: Close PuTTY window

### Method 2: Python Serial Monitor

```python
# Install pyserial: pip install pyserial
import serial

# Open serial port
ser = serial.Serial('COM3', 115200, timeout=1)

print("Listening on COM3...")
try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(line)
except KeyboardInterrupt:
    print("\nStopped")
finally:
    ser.close()
```

### Method 3: Arduino IDE Serial Monitor

1. **Open Arduino IDE**
2. **Select port**: Tools → Port → COM3
3. **Open Serial Monitor**: Tools → Serial Monitor
4. **Set baud rate**: 115200
5. **Expected output**: JSON messages every 2 seconds

---

## Step 5: Start Backend on Windows

### Using PowerShell

1. **Open PowerShell** in backend folder:
   ```powershell
   cd path\to\backend
   ```

2. **Create virtual environment** (first time only):
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   If you get an error about execution policy:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies** (first time only):
   ```powershell
   pip install -r requirements.txt
   ```

5. **Start backend**:
   ```powershell
   python -m app.main
   ```

6. **Expected output**:
   ```
   🚀 Starting Telemetry Bridge Service...
   Configuration: INGESTION_MODE=serial
   Mode: Serial (COM3 @ 115200 baud)
   Connecting to serial port COM3...
   ✓ Connected to COM3
   ✓ Service ready
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

### Using Command Prompt (cmd)

1. **Open Command Prompt** in backend folder

2. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate.bat
   ```

3. **Start backend**:
   ```cmd
   python -m app.main
   ```

---

## Step 6: Start Frontend on Windows

### Using PowerShell

1. **Open new PowerShell window** in frontend folder:
   ```powershell
   cd path\to\frontend
   ```

2. **Install pnpm** (first time only):
   ```powershell
   npm install -g pnpm
   ```

3. **Install dependencies** (first time only):
   ```powershell
   pnpm install
   ```

4. **Start frontend**:
   ```powershell
   pnpm dev
   ```

5. **Expected output**:
   ```
   VITE v5.0.0  ready in 500 ms
   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

6. **Open browser**: Navigate to http://localhost:5173

---

## Troubleshooting

### Issue: "Access Denied" on COM port

**Symptoms**:
```
ERROR: Serial connection failed: [Errno 13] Permission denied: 'COM3'
```

**Solutions**:
1. **Close other programs** using the COM port:
   - Arduino IDE Serial Monitor
   - PuTTY
   - Other serial terminals
2. **Unplug and replug** USB cable
3. **Restart backend** after closing other programs
4. **Check Device Manager** for port conflicts

---

### Issue: COM port not found

**Symptoms**:
```
ERROR: Serial connection failed: could not open port 'COM3'
```

**Solutions**:
1. **Verify COM port number** in Device Manager
2. **Update .env file** with correct COM port
3. **Check USB cable** (some cables are power-only)
4. **Try different USB port** on computer
5. **Reinstall CH340 driver**

---

### Issue: No data from ESP32

**Symptoms**: Backend connects but no telemetry appears

**Solutions**:
1. **Press reset button** on ESP32
2. **Check firmware** is uploaded correctly
3. **Verify baud rate** is 115200 in both firmware and backend
4. **Test with PuTTY** to confirm ESP32 is transmitting
5. **Check ESP32 power** (LED should be on)

---

### Issue: PowerShell execution policy error

**Symptoms**:
```
.\venv\Scripts\Activate.ps1 : File cannot be loaded because running scripts is disabled
```

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating virtual environment again.

---

### Issue: Python not found

**Symptoms**:
```
'python' is not recognized as an internal or external command
```

**Solutions**:
1. **Install Python**:
   - Download from: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation
2. **Restart PowerShell** after installation
3. **Verify installation**:
   ```powershell
   python --version
   ```

---

### Issue: pnpm not found

**Symptoms**:
```
'pnpm' is not recognized as an internal or external command
```

**Solutions**:
1. **Install Node.js** first:
   - Download from: https://nodejs.org/
   - Install LTS version
2. **Install pnpm**:
   ```powershell
   npm install -g pnpm
   ```
3. **Restart PowerShell**
4. **Verify installation**:
   ```powershell
   pnpm --version
   ```

---

## Windows-Specific Tips

### Tip 1: Keep COM Port Consistent

Windows may assign different COM port numbers when you:
- Plug into different USB ports
- Restart computer
- Unplug/replug device

**Solution**: Always use the same USB port for consistency.

### Tip 2: Disable USB Selective Suspend

Prevents Windows from turning off USB ports to save power:

1. **Open Power Options**:
   - Control Panel → Power Options
   - Click "Change plan settings"
   - Click "Change advanced power settings"

2. **Disable USB suspend**:
   - Expand "USB settings"
   - Expand "USB selective suspend setting"
   - Set to "Disabled"
   - Click "Apply"

### Tip 3: Use Windows Terminal

Modern alternative to PowerShell/cmd:

1. **Install from Microsoft Store**: "Windows Terminal"
2. **Set as default**: Settings → Startup → Default profile
3. **Benefits**: Tabs, better colors, easier copy/paste

### Tip 4: Create Startup Scripts

**Backend startup script** (`start-backend.bat`):
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m app.main
pause
```

**Frontend startup script** (`start-frontend.bat`):
```batch
@echo off
cd /d "%~dp0"
pnpm dev
pause
```

Double-click these files to start services quickly.

---

## Quick Reference

### Common Commands

```powershell
# List COM ports
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID

# Activate Python venv
.\venv\Scripts\Activate.ps1

# Start backend
python -m app.main

# Start frontend
pnpm dev

# Check if port is in use
netstat -ano | findstr :8000
```

### File Paths

```
Backend config:  backend\.env
Frontend config: frontend\.env
Firmware:        firmware\micropython\main.py
```

### Default Settings

```
Backend API:     http://localhost:8000
Frontend:        http://localhost:5173
Serial baud:     115200
COM port:        COM3 (varies)
```

---

## Testing Checklist

Before running full system:

- [ ] ESP32 connected via USB
- [ ] COM port identified in Device Manager
- [ ] CH340 driver installed (if needed)
- [ ] Backend `.env` configured with correct COM port
- [ ] Frontend `.env` configured with API URL
- [ ] Python virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Firmware uploaded to ESP32
- [ ] Serial output verified with PuTTY

---

## Next Steps

After completing this setup:

1. **Test serial connection** with PuTTY
2. **Start backend** in serial mode
3. **Start frontend** and verify connection
4. **Run integration tests** (see HARDWARE-READINESS-CHECKLIST.md)
5. **Practice demo scenarios**

---

## Additional Resources

### Windows Serial Tools

- **PuTTY**: https://www.putty.org/
- **Tera Term**: https://ttssh2.osdn.jp/
- **RealTerm**: https://realterm.sourceforge.io/
- **Arduino IDE**: https://www.arduino.cc/en/software

### Python Serial Libraries

```powershell
# Install pyserial
pip install pyserial

# Install pyserial-asyncio (for backend)
pip install pyserial-asyncio
```

### Useful PowerShell Commands

```powershell
# Find Python location
Get-Command python | Select-Object Source

# Check Python version
python --version

# List installed Python packages
pip list

# Check if port is open
Test-NetConnection -ComputerName localhost -Port 8000
```

---

## Conclusion

Your Windows system is now configured for serial communication with the ESP32 hardware. The backend will automatically connect to the specified COM port and start receiving telemetry data.

**Status**: Windows serial setup complete ✅

**Next Action**: Follow HARDWARE-READINESS-CHECKLIST.md to complete hardware integration.
