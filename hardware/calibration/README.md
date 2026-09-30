# Sensor Calibration Procedures

**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Status:** Procedures Defined; Physical Benchtop Execution Pending (See [HIL Specification](../../docs/HIL_SPECIFICATION.md))

## Calibration Regimes

Each physical sensor deployed to the CyaplaneX edge testbed must be mapped to a versioned calibration identifier (`cal_id`):

1. **Accelerometer (ADXL345):**
   - **Procedure:** 6-orientation static tumble test on a precision surface plate to determine axis offset ($0\text{g}$) and sensitivity ($1\text{g}$ Earth gravity vector).
   - **Target Version:** `cal-adxl345-2026-v1`
   - **Acceptance Criterion:** Static resting magnitude $|a| = 1.000 \pm 0.025\text{ g}$.

2. **Thermocouple (MAX6675 / K-Type):**
   - **Procedure:** Dual-point calibration at ice-point bath ($0.0^\circ\text{C}$) and boiling water ($100.0^\circ\text{C}$ at local atmospheric pressure).
   - **Target Version:** `cal-max6675-2026-v1`
   - **Acceptance Criterion:** Linearity error $< 1.5^\circ\text{C}$ across $0^\circ\text{C}$ to $120^\circ\text{C}$.

3. **Hall-Effect Speed Sensor (A3144):**
   - **Procedure:** Optical stroboscope / tachometer cross-validation against shaft rotation across 500–2500 RPM.
   - **Target Version:** `cal-hall-2026-v1`
   - **Acceptance Criterion:** Pulse count error $< 0.5\%$ across 60-second window.
