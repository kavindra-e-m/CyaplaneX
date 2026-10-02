# CyaplaneX Hardware-in-the-Loop (HIL) Execution Runbook

**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Document Classification:** Benchtop Verification Runbook  
**HIL STATUS = READY FOR PHYSICAL EXECUTION** (Physical benchtop execution pending physical laboratory access)

---

## 1. Required Hardware

The physical Hardware-in-the-Loop (HIL) testbed utilizes the following benchtop components:

| Item | Component | Specification | Function |
| :--- | :--- | :--- | :--- |
| **H1** | Microcontroller | ESP32-WROOM-32D Development Board (Dual-core Tensilica Xtensa 32-bit LX6 @ 240 MHz, 520 KB SRAM, USB CDC UART) | Sensor sampling, local framing, and serial telemetry transmission |
| **H2** | Edge Host Gateway | Raspberry Pi 4 Model B (4 GB / 8 GB RAM, Raspberry Pi OS 64-bit) OR x86_64 Host Laptop (Linux / Windows 11) | Runs CyaplaneX Edge Orchestrator, Trust Engine, Preprocessing, Production ML Adapter, and Provenance Signer |
| **H3** | Vibration Sensor | ADXL345 3-Axis Digital Accelerometer (I2C interface, configured for $\pm 16\text{g}$, 800 Hz ODR) or Piezoelectric Analog Transducer | High-frequency radial bearing housing acceleration measurement |
| **H4** | Temperature Sensor | MAX6675 Cold-Junction-Compensated K-Type Thermocouple Digitizer (SPI read-only, $0^\circ\text{C}$ to $+1024^\circ\text{C}$, $0.25^\circ\text{C}$ resolution) | Bearing cap surface temperature measurement |
| **H5** | Speed / RPM Sensor | A3144 Hall-Effect Digital Switch with 10 kΩ pull-up resistor + Neodymium magnet ring collar | Shaft rotation pulse detection and RPM calculation |
| **H6** | Motor & Mechanical Rig | 12V–24V DC motor with PWM speed controller (0–3000 RPM), 8 mm hardened steel shaft, two pillow-block ball bearings, flexible spider coupling | Rotating machinery demonstrator test rig |
| **H7** | Electrical Accessories | Breadboard / custom protoboard, 3.3V power rails, 4.7 kΩ I2C pull-up resistors, 100 nF ceramic decoupling capacitors, USB-A to Micro-USB / USB-C data cable | Interconnect, signal conditioning, and host connection |

---

## 2. Wiring

### 2.1 Complete Pinout Interconnect Matrix

All logic signals operate at **3.3V LVTTL**. Under no circumstances should 5V logic be applied to ESP32 GPIO pins.

```
                      +-----------------------------+
                      |   ESP32-WROOM-32D Board     |
                      |                             |
    [ADXL345 SDA] <-->| GPIO 21 (I2C SDA)           |
    [ADXL345 SCL] --->| GPIO 22 (I2C SCL)           |
                      |                             |
    [MAX6675 SO]  --->| GPIO 19 (SPI MISO)          |
    [MAX6675 SCK] --->| GPIO 18 (SPI SCK)           |
    [MAX6675 CS]  --->| GPIO 5  (SPI CS)            |
                      |                             |
    [A3144 Hall]  --->| GPIO 4  (Interrupt Pull-Up) |
                      |                             |
    [Host USB CDC]--->| Micro-USB / UART0 (TX0/RX0) |---> Host USB Port (115200 baud)
                      |                             |
    [Regulated 3V3]---| 3V3 Rail                    |
    [Common Ground]---| GND Rail                    |
                      +-----------------------------+
```

### 2.2 Discrete Sensor Wiring Specifics

1. **ADXL345 Accelerometer (I2C Mode):**
   - `VCC` $\rightarrow$ ESP32 `3V3`
   - `GND` $\rightarrow$ ESP32 `GND`
   - `CS` $\rightarrow$ Tied to `3V3` (enables I2C mode instead of SPI)
   - `SDO` $\rightarrow$ Tied to `GND` (sets I2C address to `0x53`)
   - `SDA` $\rightarrow$ ESP32 `GPIO 21` (with $4.7\text{ k}\Omega$ pull-up to 3.3V)
   - `SCL` $\rightarrow$ ESP32 `GPIO 22` (with $4.7\text{ k}\Omega$ pull-up to 3.3V)
2. **MAX6675 Thermocouple Digitizer (SPI Mode):**
   - `VCC` $\rightarrow$ ESP32 `3V3`
   - `GND` $\rightarrow$ ESP32 `GND`
   - `SO` (Data Out) $\rightarrow$ ESP32 `GPIO 19`
   - `SCK` (Clock) $\rightarrow$ ESP32 `GPIO 18`
   - `CS` (Chip Select) $\rightarrow$ ESP32 `GPIO 5`
   - K-type thermocouple leads connected to screw terminals with correct polarity (+ / -).
3. **A3144 Hall-Effect RPM Sensor:**
   - `Pin 1 (VCC)` $\rightarrow$ ESP32 `3V3`
   - `Pin 2 (GND)` $\rightarrow$ ESP32 `GND`
   - `Pin 3 (OUT)` $\rightarrow$ ESP32 `GPIO 4` with $10\text{ k}\Omega$ pull-up resistor to `3V3`.
   - Neodymium magnet mounted on the motor shaft collar with south pole facing outward.

---

## 3. ESP32 Firmware Procedure

The ESP32 firmware source is located in [`hardware/esp32/src/main.cpp`](file:///d:/CyplaneX/hardware/esp32/src/main.cpp).

### 3.1 Toolchain Prerequisites
- [PlatformIO Core](https://platformio.org/) or [Arduino IDE](https://www.arduino.cc/) with the ESP32 Arduino Core (`>= 2.0.0`).
- Silicon Labs CP210x or CH340 USB-to-UART bridge drivers installed on the host.

### 3.2 Compilation and Flashing Steps
1. Navigate to the firmware directory:
   ```bash
   cd hardware/esp32
   ```
2. Inspect the PlatformIO configuration or open `src/main.cpp` in Arduino IDE.
3. Connect the ESP32 board to the host edge machine via a USB data cable.
4. Verify port recognition:
   - **Linux / Raspberry Pi:** `ls -l /dev/ttyUSB*` or `ls -l /dev/ttyACM*`
   - **Windows:** Check Device Manager under `Ports (COM & LPT)` (e.g., `COM3`, `COM4`)
5. Build and flash the firmware:
   ```bash
   pio run --target upload
   ```
6. Monitor the initial serial bootloader output:
   ```bash
   pio device monitor -b 115200
   ```
   **Expected boot confirmation:**
   ```text
   # CyaplaneX ESP32 Firmware Initialized (Build: HIL-v1.0.0)
   ```

---

## 4. Sensor Calibration Procedure

Calibration must be performed prior to running diagnostic tests:

1. **Accelerometer Calibration (Zero-g Offset & Scale Factor):**
   - Mount the ADXL345 securely to the bearing housing while the motor is stationary and completely powered off.
   - Collect 500 samples. Compute the mean static acceleration.
   - Adjust offset registers so that the stationary radial RMS measures $\le 0.05\text{g}$ with zero mechanical excitation.
2. **Thermocouple Verification (Cold-Junction Calibration):**
   - With the motor at room temperature, measure ambient room temperature with an independent reference thermometer.
   - Verify that `temp-phys-01` reads within $\pm 1.5^\circ\text{C}$ of the reference ambient value before operating the motor.
3. **Hall-Effect Pulse Calibration:**
   - Rotate the shaft by hand exactly 10 full revolutions while observing the raw pulse counter.
   - Verify that exactly 10 falling edges trigger on `GPIO 4`.
   - Spin up the motor to an externally verified optical tachometer speed (e.g., 1500 RPM) and confirm `rpm-phys-01` displays within $\pm 2\%$ of the reference tachometer.

---

## 5. Serial Protocol

The ESP32 streams telemetry continuously over USB CDC UART at:
- **Baud Rate:** `115200`
- **Data Bits:** `8`
- **Parity:** `None`
- **Stop Bits:** `1`
- **Flow Control:** None

### 5.1 Framing Formats
The host ingest adapter ([`edge/sensors/physical.py`](file:///d:/CyplaneX/edge/sensors/physical.py): `SerialStreamSensorReader`) parses incoming lines in two formats:

1. **Standard Key-Value CSV (Default):**
   ```text
   <sensor_id>,<value>
   ```
   *Example:*
   ```text
   vib-phys-01,0.3421
   temp-phys-01,42.50
   rpm-phys-01,1750.0
   ```
2. **Structured JSON Packet (Optional):**
   ```json
   {"sensor_id": "vib-phys-01", "value": 0.3421, "unit": "g"}
   ```

### 5.2 Architectural Constraint: Firmware Purity
The ESP32 is strictly an acquisition peripheral. Outlier detection, noise filtering, window aggregation, and Byzantine consensus are **strictly executed on the Edge Compute Host** within [`edge/sensors/trust.py`](file:///d:/CyplaneX/edge/sensors/trust.py).

---

## 6. Edge Computer Setup

1. **Install Python Environment:**
   Ensure Python 3.11+ is installed on the host edge gateway:
   ```bash
   cd CyplaneX
   uv sync
   ```
2. **Install Serial Dependencies:**
   Ensure `pyserial` is available in the virtual environment:
   ```bash
   uv pip install pyserial
   ```
3. **Identify Serial Port Permissions (Linux / Raspberry Pi):**
   ```bash
   sudo usermod -a -G dialout $USER
   # Ensure read/write access to /dev/ttyUSB0
   ```

---

## 7. Data Acquisition Command

To verify continuous physical telemetry streaming from the ESP32 into the edge reader:

```bash
# On Linux / Raspberry Pi:
uv run python -c "
import serial
from edge.sensors.physical import SerialStreamSensorReader

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1.0)
reader = SerialStreamSensorReader('vib-phys-01', stream=ser)
for _ in range(10):
    val = reader.read()
    print(f'Acquired vibration reading: {val:.4f} g')
"

# On Windows:
uv run python -c "
import serial
from edge.sensors.physical import SerialStreamSensorReader

ser = serial.Serial('COM3', 115200, timeout=1.0)
reader = SerialStreamSensorReader('vib-phys-01', stream=ser)
for _ in range(10):
    val = reader.read()
    print(f'Acquired vibration reading: {val:.4f} g')
"
```

---

## 8. Production ML Execution Command

To execute the full edge pipeline using the production machine learning artifact against the physical sensor stream:

```bash
# Run orchestrator binding physical sensors via configuration or e2e runner:
uv run python scripts/e2e_demo.py
```
*(By default, `scripts/e2e_demo.py` executes using the production Joblib model `95ae7ef3...` with fail-closed strict contract verification).*

---

## 9. Expected Telemetry Format

The physical telemetry window consists of the 6-feature contract consumed by [`CyaplaneXProductionModel`](file:///d:/CyplaneX/ml/export/model.py):

| Feature Name | Physics Description | Unit | Healthy Operating Range | Degraded Range |
| :--- | :--- | :---: | :---: | :---: |
| `vib_rms` | Root Mean Square acceleration | $\text{g}$ | $0.10 \le \text{vib\_rms} \le 0.45$ | $> 0.80$ |
| `vib_p2p` | Peak-to-peak shock acceleration | $\text{g}$ | $0.25 \le \text{vib\_p2p} \le 1.20$ | $> 2.50$ |
| `temp_mean` | Bearing housing mean temperature | $^\circ\text{C}$ | $30.0 \le \text{temp\_mean} \le 55.0$ | $> 70.0$ |
| `temp_max` | Bearing housing peak temperature | $^\circ\text{C}$ | $32.0 \le \text{temp\_max} \le 60.0$ | $> 75.0$ |
| `rpm_mean` | Rotational speed mean | $\text{RPM}$ | $1450.0 \le \text{rpm\_mean} \le 1850.0$ | Any deviation |
| `rpm_std` | Speed stability standard deviation | $\text{RPM}$ | $0.5 \le \text{rpm\_std} \le 15.0$ | $> 45.0$ |

---

## 10. Fault Injection Procedure

To evaluate edge fault classification and maintenance reasoning under physical conditions:

1. **Unbalance Fault:**
   - Attach a calibrated eccentric mass screw ($2.5\text{ g}$) to the motor coupling collar.
   - Run the motor at 1750 RPM.
   - *Expected Symptom:* Elevated `vib_rms` ($> 1.2\text{g}$) and elevated `vib_p2p` with 1X rotational frequency harmonics.
2. **Outer Race Bearing Flaw:**
   - Swap the normal pillow-block bearing with a test bearing possessing an electro-discharge machined (EDM) notch on the outer raceway.
   - *Expected Symptom:* Repetitive impact spikes in `vib_p2p` ($> 2.8\text{g}$) and high-frequency vibration envelope rise.
3. **Thermal Runaway / Lubrication Starvation:**
   - Apply friction load band to bearing cap or remove lubrication.
   - *Expected Symptom:* `temp_mean` rising progressively past $65^\circ\text{C}$.

---

## 11. Healthy Condition Procedure

To restore and verify the baseline healthy condition:

1. Disconnect eccentric balance weights.
2. Verify shaft alignment using a dial indicator ($\le 0.05\text{ mm}$ radial runout).
3. Ensure bearings are lubricated with standard NLGI Grade 2 lithium grease.
4. Power motor at nominal 1750 RPM.
5. Confirm sensor trust engine outputs `TRUSTED` across all channels (`vib`, `temp`, `rpm`).
6. Verify production ML inference reports:
   - `Condition = HEALTHY`
   - `Health Score = 100.0%`
   - `Severity = LOW`
   - `Maintenance Priority = P3` (Normal monitoring)

---

## 12. Safety Precautions

> [!CAUTION]
> Mechanical and Electrical Hazards on Rotating Machinery:
> 1. **Rotating Shaft Guard:** Always ensure a transparent acrylic safety enclosure covers the rotating shaft and motor coupling before energizing the DC power supply.
> 2. **Emergency Stop (E-Stop):** A physical normally-closed emergency kill-switch must be wired in series with the motor power supply within immediate reach of the operator.
> 3. **Thermal Hazard:** Motor housing and bearing caps can exceed $80^\circ\text{C}$ during extended friction runs. Do not touch bare metal surfaces during or immediately after testing.
> 4. **Eye Protection:** ANSI Z87.1 certified safety glasses must be worn during all high-speed mechanical rotation and fault injection tests.

---

## 13. Expected Outputs

When the HIL run is executed, the following outputs will be emitted to stdout and persisted locally:

```text
[HIL TESTBED] Connecting to physical telemetry serial stream on COM3 / /dev/ttyUSB0...
[HIL TESTBED] Stream connected. Baud: 115200. Reader: SerialStreamSensorReader.
[STEP 01] Active Model: cyaplanex-production-joblib (v1.0.0) | SHA-256: 95ae7ef3...
[STEP 02] Baseline Healthy: Condition=HEALTHY, Health Score=100.0%, Trust=TRUSTED
[STEP 03] Injected Fault: Condition=BEARING_OUTER_RACE_FAULT
[STEP 04] Production ML Evaluation:
         Condition: BEARING_OUTER_RACE_FAULT
         Health Score: 7.7%
         Severity: CRITICAL
         Maintenance Priority: P1
[STEP 05] Provenance Signed: HMAC-SHA256 signature generated with device key
[STEP 06] Closure Record: Post-repair Health Score restored to 100.0%
         Repair Effectiveness: 0.92 [PRODUCTION MODEL METRIC]
```

---

## 14. Evidence to Capture

For physical competition submission or jury audit, capture and archive:

1. **Oscilloscope / Logic Analyzer Trace:** CSV export of ADXL345 I2C transactions and A3144 Hall-effect square-wave pulses.
2. **Serial Log File:** Complete raw terminal log of ESP32 UART streaming matching `scripts/e2e_demo.py` execution.
3. **Cryptographic Manifest:** Output JSON manifest containing the physical `sensor_window_hash`, `model_hash` (`95ae7ef3...`), and device HMAC signature.
4. **Physical Photographs / Video:** High-resolution photograph of the testbed showing ESP32, sensors, motor, and laptop running the live dashboard.

---

## 15. Troubleshooting

| Symptom | Root Cause | Corrective Action |
| :--- | :--- | :--- |
| Serial port `Permission Denied` on Linux | User lacks membership in `dialout` group | Run `sudo usermod -a -G dialout $USER` and log back in. |
| Ingest reader returns `0.0` or fallback | Baud rate mismatch or loose wiring | Confirm baud is set to `115200` in both ESP32 firmware and host reader. Check GND wire between ESP32 and host. |
| `SensorTrustEngine` reports `STUCK_VALUE` | Sensor disconnected or bus hanging | Check I2C pull-up resistors ($4.7\text{ k}\Omega$). Verify sensor power rail is clean 3.3V. |
| Hall-effect RPM reads 0 continuously | Pull-up missing or magnet orientation inverted | A3144 requires South pole facing branded side. Confirm $10\text{ k}\Omega$ pull-up resistor to 3.3V on GPIO 4. |
| ML model rejects input features | Feature count mismatch or NaN value | Ensure 6-feature tuple is provided in exact order: `[vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]`. |
