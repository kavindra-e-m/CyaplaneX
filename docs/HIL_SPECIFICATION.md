# CyaplaneX Hardware-in-the-Loop (HIL) Testbed Specification

**Document Version:** 1.0.0  
**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Status:** **PENDING PHYSICAL VALIDATION** (Software Boundary Prepared & Tested)  

---

## 1. Scope & Objective

This document specifies the physical Hardware-in-the-Loop (HIL) testbed architecture, electrical wiring, telemetry framing protocols, and verification gates for CyaplaneX.

The purpose of this architecture is to allow physical sensor streams from rotating machinery to feed directly into the edge software stack:
$$\text{Physical Sensor} \longrightarrow \text{ESP32 Sampling} \longrightarrow \text{UART / USB CDC Stream} \longrightarrow \text{SerialStreamSensorReader} \longrightarrow \text{SensorAcquisitionService} \longrightarrow \text{SensorTrustEngine} \longrightarrow \text{FeaturePipeline} \longrightarrow \text{EdgeMLAdapter}$$

> **CRITICAL FACTUAL CONSTRAINT:**  
> The software boundary adapter ([`SerialStreamSensorReader`](file:///d:/CyplaneX/edge/sensors/physical.py)) has been fully implemented and verified via automated tests ([`tests/unit/test_sensor_acquisition.py`](file:///d:/CyplaneX/tests/unit/test_sensor_acquisition.py)).  
> However, **physical benchtop acquisition and physical HIL execution remain PENDING**. No physical hardware results are claimed in this release.

---

## 2. Testbed Hardware Architecture

The target rotating-machinery test assembly comprises:

| Component | Target Hardware Specification | Function |
| :--- | :--- | :--- |
| **Microcontroller** | ESP32-WROOM-32D (Dual-Core 240 MHz, 520 KB SRAM) | Sensor sampling, local framing, serial transmission |
| **Edge Compute Host** | Host Computer / Raspberry Pi 4 Model B (Linux/Windows) | CyaplaneX Edge Orchestrator, Trust Engine, ML Adapter, Provenance Signer |
| **Vibration Sensor** | ADXL345 3-Axis Digital Accelerometer (I2C/SPI, $\pm 16\text{g}$) or Analog Piezo | Bearing/housing radial vibration monitoring ($g$) |
| **Temperature Sensor**| MAX6675 K-Type Thermocouple Amplifier ($0^\circ\text{C}$ to $+1024^\circ\text{C}$) | Bearing cap surface temperature ($^\circ\text{C}$) |
| **Speed (RPM) Sensor**| A3144 Digital Hall-Effect Sensor + Neodymium Magnet Collar | Shaft rotational frequency measurement (RPM) |
| **Prime Mover** | 12V–24V Brushed/Brushless DC Motor (0–3000 RPM) | Controlled shaft rotation |
| **Coupling & Shaft** | Flexible spider coupling, 8 mm hardened steel shaft, pillow-block bearings | Mechanical transmission |
| **Fault Mechanism** | Unbalanced mass collar / seeded outer-race bearing defect | Controlled vibration anomaly injection |

---

## 3. Electrical Wiring & Pinout (ESP32-WROOM-32)

### 3.1 Pin Assignment Matrix

```
                      +-------------------+
                      |   ESP32-WROOM-32  |
                      |                   |
    [ADXL345 SDA] <-->| GPIO 21 (SDA)     |
    [ADXL345 SCL] --->| GPIO 22 (SCL)     |
                      |                   |
    [MAX6675 SO]  --->| GPIO 19 (MISO)    |
    [MAX6675 SCK] --->| GPIO 18 (SCK)     |
    [MAX6675 CS]  --->| GPIO 5  (SS)      |
                      |                   |
    [A3144 Hall]  --->| GPIO 4  (INT/PULL)|
                      |                   |
    [USB UART TX] --->| GPIO 1  (TX0)     |---> Host USB CDC Serial (115200 baud)
    [USB UART RX] <---| GPIO 3  (RX0)     |<---
                      |                   |
    [VCC 3.3V]    --->| 3V3 Rail          |
    [GND]         --->| GND Rail          |
                      +-------------------+
```

### 3.2 Electrical Characteristics
- **Logic Level:** 3.3V LVTTL throughout.
- **Hall Effect Pull-Up:** $10\text{ k}\Omega$ pull-up resistor between GPIO 4 and 3.3V.
- **I2C Pull-Up:** $4.7\text{ k}\Omega$ pull-ups on SDA (GPIO 21) and SCL (GPIO 22).
- **Decoupling:** $100\text{ nF}$ ceramic capacitor adjacent to each sensor supply pin.

---

## 4. Telemetry Stream Protocol

The ESP32 communicates with the edge computing host via USB CDC or hardware UART at **115200 baud, 8-N-1**.

### 4.1 Telemetry Framing Formats
The host adapter ([`SerialStreamSensorReader`](file:///d:/CyplaneX/edge/sensors/physical.py)) supports two stream framing formats:

#### Format A: Key-Value CSV (Default Stream)
```text
vib-01,0.342
temp-01,42.50
rpm-01,1750.0
```

#### Format B: Structured JSON Packet
```json
{"sensor_id": "vib-01", "value": 0.342, "unit": "g", "seq": 104}
{"sensor_id": "temp-01", "value": 42.50, "unit": "deg_c", "seq": 105}
{"sensor_id": "rpm-01", "value": 1750.0, "unit": "rpm", "seq": 106}
```

### 4.2 Architectural Constraint: No Edge Trust Logic in Firmware
> **Architectural Separation:** The ESP32 is strictly an **acquisition and transmission peripheral**.  
> Outlier filtering, stuck-value detection, noise estimation, and Byzantine consensus must **NOT** be embedded into microcontroller firmware.  
> All trust adjudication belongs exclusively in the [`SensorTrustEngine`](file:///d:/CyplaneX/edge/sensors/trust.py) running on the edge compute host.

---

## 5. Software Integration Pattern

To switch from simulated telemetry to physical hardware, instantiate `SerialStreamSensorReader` in [`edge/main.py`](file:///d:/CyplaneX/edge/main.py):

```python
import serial
from edge.sensors.acquisition import SensorAcquisitionService
from edge.sensors.physical import SerialStreamSensorReader

# Connect physical serial port
ser = serial.Serial("COM3", 115200, timeout=1.0)  # On Linux: "/dev/ttyUSB0"

# Instantiate readers binding to the stream
vib_reader = SerialStreamSensorReader(sensor_id="vib-phys-01", stream=ser, default_fallback=0.0)
temp_reader = SerialStreamSensorReader(sensor_id="temp-phys-01", stream=ser, default_fallback=25.0)
rpm_reader = SerialStreamSensorReader(sensor_id="rpm-phys-01", stream=ser, default_fallback=0.0)

# Register with existing acquisition boundary
service = SensorAcquisitionService(device_id="edge-dev-01")
service.register_sensor("vib-phys-01", "vibration", "g", "cal-2026-v1", vib_reader)
service.register_sensor("temp-phys-01", "temperature", "deg_c", "cal-2026-v1", temp_reader)
service.register_sensor("rpm-phys-01", "rpm", "rpm", "cal-2026-v1", rpm_reader)
```

The rest of the pipeline ([`SensorTrustEngine`](file:///d:/CyplaneX/edge/sensors/trust.py), [`FeaturePipeline`](file:///d:/CyplaneX/edge/preprocessing/pipeline.py), [`EdgeMLAdapter`](file:///d:/CyplaneX/edge/ai/adapter.py), [`ProvenanceSigner`](file:///d:/CyplaneX/edge/provenance/signer.py)) operates with zero modifications.

---

## 6. HIL Execution Checklist (Status: PENDING)

| Step | Verification Milestone | Status |
| :---: | :--- | :---: |
| 1 | ESP32 serial communication link established at 115200 baud | PENDING |
| 2 | Accelerometer (ADXL345) signal verified on benchtop | PENDING |
| 3 | Thermocouple (MAX6675) ambient temperature verified | PENDING |
| 4 | Hall-effect sensor shaft RPM pulses counted and calibrated | PENDING |
| 5 | Host timestamp and sequential monotonic packet numbering confirmed | PENDING |
| 6 | Sensor calibration ID matched in device configuration | PENDING |
| 7 | `SensorTrustEngine` reports `TRUSTED` for normal motor idle | PENDING |
| 8 | Healthy baseline captured across 100 consecutive windows | PENDING |
| 9 | Controlled mechanical fault injected (unbalanced mass attached) | PENDING |
| 10 | Edge ML Adapter evaluates degraded health and outputs anomaly code | PENDING |
| 11 | Device-local HMAC-SHA256 signature generated and verified | PENDING |
| 12 | Maintenance workflow initiated on MRO dashboard | PENDING |
| 13 | Post-repair fresh sensor acquisition captured | PENDING |
| 14 | Digital Passport closure record appended and verified | PENDING |

**Conclusion:**  
Software integration boundary: **READY**.  
Physical testbed benchtop execution: **PENDING HARDWARE ACCESS**.
