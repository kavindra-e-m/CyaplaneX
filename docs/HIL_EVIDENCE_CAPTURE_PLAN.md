# CyaplaneX — Physical HIL Evidence Capture Plan

**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Document Classification:** Laboratory Evidence Capture Protocol  
**HIL STATUS = READY FOR PHYSICAL EXECUTION**  
*(Software boundary implemented & verified; benchtop physical execution pending physical laboratory access).*

---

## 1. Scope & Objective

This document defines the exact physical artifacts, photographs, data streams, and terminal logs required to record during benchtop Hardware-in-the-Loop (HIL) execution.

Under the **Zero Fabrication Standard**, no physical HIL data, oscilloscope waveforms, or laboratory photographs may be claimed or presented until actual physical testing is performed on the testbed.

---

## 2. Eleven Mandatory Physical Evidence Artifacts

When physical hardware benchtop execution is initiated, the engineering team must capture the following 11 items:

| # | Evidence Item | Format / Medium | Target Content / Measurement | Verification Criterion |
|:---:|---|---|---|---|
| **E1** | **Hardware Setup Photograph** | High-Res PNG / JPG | Clear, well-lit photograph showing the physical ESP32 board, ADXL345 accelerometer mounted on bearing housing, MAX6675 thermocouple, A3144 Hall-effect sensor, and DC motor rig connected via USB to the host computer. | All wire labels legible; acrylic safety shield mounted; motor unpowered. |
| **E2** | **ESP32 Serial Stream Log** | Raw `.txt` / `.log` terminal capture | Continuous UART serial output at 115200 baud showing the firmware boot banner and formatted sensor lines: `vib-phys-01,0.3421`, `temp-phys-01,42.50`, `rpm-phys-01,1750.0`. | Sequence monotonic; zero dropped lines over 500 consecutive cycles. |
| **E3** | **Physical Vibration Values** | Logic analyzer / CSV log | ADXL345 I2C register reads converted to g-force acceleration. Nominal baseline: RMS $\approx 0.15\text{g}$ to $0.35\text{g}$. Injected fault: RMS $> 1.20\text{g}$. | Accelerometer values dynamically respond to motor shaft spin-up. |
| **E4** | **Physical Temperature Values** | Digital Multimeter / CSV log | MAX6675 thermocouple readings from the bearing cap. Ambient room start: $\approx 24^\circ\text{C}$ to $28^\circ\text{C}$. Operating equilibrium: $40^\circ\text{C}$ to $55^\circ\text{C}$. | Temperature tracks friction heat dissipation over extended run. |
| **E5** | **Physical RPM Values** | Optical Tachometer vs. Serial Log | A3144 Hall-effect sensor pulse counter over motor shaft rotation. Comparison against handheld optical tachometer at 1000, 1500, and 2000 RPM. | Reading matches optical tachometer within $\pm 2.0\%$. |
| **E6** | **Edge Ingestion Confirmation** | Edge orchestrator log (`edge.log`) | Confirmation that [`SerialStreamSensorReader`](file:///d:/CyplaneX/edge/sensors/physical.py) ingests raw serial bytes without buffer overrun or Unicode decode errors. | Terminal prints: `Acquired vibration reading: ... g`. |
| **E7** | **Sensor Trust State Output** | JSON trust export / terminal log | [`SensorTrustEngine`](file:///d:/CyplaneX/edge/sensors/trust.py) output log evaluating range, freshness, stuck detection, and consensus across physical channels. | Status reports `TRUSTED` under normal rotation; `DEGRADED` under dynamic fault. |
| **E8** | **Production ML Diagnosis Output** | Manifest JSON / terminal log | Diagnosis emitted by [`CyaplaneXProductionModel`](file:///d:/CyplaneX/ml/export/model.py) (`cyaplanex-gb-aeromodel-v1`) against physical feature vector. | Outputs diagnosed condition, health score, and severity under physical inputs. |
| **E9** | **Web Dashboard Live Response** | Screen recording / screenshot | MRO Dashboard UI updating in real time with live physical gauges reflecting actual motor speed and bearing temperature. | Gauges update dynamically as motor speed controller is adjusted. |
| **E10** | **Cryptographic Provenance Record** | Signed manifest JSON | Output JSON containing physical `sensor_window_hash`, model hash (`95ae7ef3...`), and device HMAC-SHA256 signature. | Manifest independently verified by [`IndependentCloudVerifier`](file:///d:/CyplaneX/cloud/verification/verifier.py). |
| **E11** | **Post-Maintenance Fresh Re-Test** | Re-test log / Digital Passport closure | Fresh post-repair sensor window captured after removing eccentric fault collar, confirming health restoration and closure record generation. | Post-health returns to healthy range; repair effectiveness $\ge 0.80$. |

---

## 3. Physical Execution Procedure & Capture Workflow

```text
Step 1: Mount sensors & wire ESP32 (GPIO 21/22, 19/18/5, 4)
        │
        ▼
Step 2: Capture Photograph (Evidence E1)
        │
        ▼
Step 3: Flash ESP32 firmware (115200 baud) & log serial stream (Evidence E2, E3, E4, E5)
        │
        ▼
Step 4: Connect USB to edge host & verify SerialStreamSensorReader (Evidence E6)
        │
        ▼
Step 5: Run SensorTrustEngine & record Gate B trust adjudication (Evidence E7)
        │
        ▼
Step 6: Execute EdgeMLAdapter with cyaplanex-gb-aeromodel-v1 (Evidence E8)
        │
        ▼
Step 7: Launch dashboard & record live gauge responsiveness (Evidence E9)
        │
        ▼
Step 8: Generate cryptographic manifest with physical sensor window hash (Evidence E10)
        │
        ▼
Step 9: Inject fault collar, then remove & execute fresh re-test closure (Evidence E11)
```

---

## 4. Claim Control & Regulatory Statements

> [!CAUTION]
> **Mandatory Phrasing Restrictions:**  
> - **Permitted Status Before Physical Run:** `"HIL = READY FOR PHYSICAL EXECUTION"` or `"Physical HIL pending"`.  
> - **Prohibited Phrase:** `"HIL validated"` (Must NEVER be used prior to actual laboratory benchtop execution).  
> - Upon completion of physical testing, update this document with timestamped photos, logs, and measured CSV files.
