# CyaplaneX — Physical HIL Benchtop Checklist

**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**HIL STATUS = READY FOR PHYSICAL EXECUTION**  
*(Software boundary implemented & verified; benchtop physical execution pending laboratory hardware access).*

---

## One-Page Benchtop Verification Checklist

| Item | Subsystem / Step | Verification Procedure | Acceptance Gate | Status |
| :---: | :--- | :--- | :--- | :---: |
| **01** | **Microcontroller (ESP32)** | ESP32-WROOM-32D flashed with [`hardware/esp32/src/main.cpp`](file:///d:/CyplaneX/hardware/esp32/src/main.cpp) | Boots cleanly at 115200 baud; emits `# CyaplaneX ESP32 Firmware Initialized` | `READY` |
| **02** | **Vibration Sensor (ADXL345)** | ADXL345 connected via I2C (`GPIO 21` SDA, `GPIO 22` SCL) with 4.7 kΩ pull-ups | I2C address `0x53` acknowledged; $\pm 16\text{g}$ mode configured | `READY` |
| **03** | **Temperature Sensor (MAX6675)** | MAX6675 K-type thermocouple amplifier on SPI (`GPIO 19` SO, `GPIO 18` SCK, `GPIO 5` CS) | Cold junction ambient temperature reads within $\pm 1.5^\circ\text{C}$ of reference | `READY` |
| **04** | **Speed Sensor (A3144 Hall-Effect)** | A3144 digital Hall switch on `GPIO 4` with 10 kΩ pull-up to 3.3V | Pulses counted per rotation of motor shaft collar with neodymium magnet | `READY` |
| **05** | **Motor Test Rig** | 12V–24V DC motor with PWM controller, flexible coupling, 8 mm steel shaft, pillow-block bearings | Smooth rotation 0–3000 RPM; acrylic safety shield mounted in place | `READY` |
| **06** | **Electrical Wiring & Power** | Common ground established; 3.3V LVTTL rails verified with digital multimeter | Zero 5V lines connected to ESP32 GPIOs; decoupling caps in place | `READY` |
| **07** | **Static Sensor Calibration** | Zero-g offset compensation on ADXL345; baseline tachometer calibration on A3144 | Radial static RMS $\le 0.05\text{g}$; RPM within $\pm 2\%$ of optical tachometer | `READY` |
| **08** | **Serial Telemetry Stream** | USB CDC serial stream ingested via [`SerialStreamSensorReader`](file:///d:/CyplaneX/edge/sensors/physical.py) | Stream active at 115200 baud; parses `vib-phys-01,temp-phys-01,rpm-phys-01` | `READY` |
| **09** | **Sensor Trust Adjudication** | [`SensorTrustEngine`](file:///d:/CyplaneX/edge/sensors/trust.py) evaluates incoming physical telemetry stream | Outputs `TRUSTED` across range, freshness, stuck detection, and consensus | `READY` |
| **10** | **Production ML Inference** | Stream fed into [`EdgeMLAdapter`](file:///d:/CyplaneX/edge/ai/adapter.py) with [`CyaplaneXProductionModel`](file:///d:/CyplaneX/ml/export/model.py) | Model computes health score, anomaly severity, and condition code | `READY` |
| **11** | **Controlled Fault Injection** | Attach 2.5g eccentric screw collar to motor coupling or install seeded-flaw bearing | Machine vibration rises; model classifies anomaly and outputs `P1` priority | `READY` |
| **12** | **Evidence & Video Capture** | Archive terminal logs, oscilloscope traces, manifest JSON, and photo/video records | Artifacts saved for competition submission and technical audit | `READY` |

---

## Target Telemetry Stream Format (USB CDC UART @ 115200 Baud)

```text
vib-phys-01,0.3421
temp-phys-01,42.50
rpm-phys-01,1750.0
```

## Architectural Decoupling Rule
> **Firmware Boundary:** The ESP32 firmware is strictly an acquisition and framing peripheral. Outlier filtering, stuck-value detection, and Byzantine consensus are **strictly executed on the Edge Compute Host** within [`edge/sensors/trust.py`](file:///d:/CyplaneX/edge/sensors/trust.py).
