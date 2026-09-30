# Rotating Machinery Test Rig Specification

**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Status:** Architecture Specified; Physical Rig Assembly & Validation Pending (See [HIL Specification](../../docs/HIL_SPECIFICATION.md))

## Mechanical Architecture

The physical test rig simulates rotating aircraft auxiliary power unit (APU) or starter-generator mechanical dynamics under controlled laboratory conditions:

1. **Drive Unit:**
   - 12V–24V DC motor with pulse-width modulated (PWM) speed governor (0–3000 RPM).
   - Dynamic operating setpoint: $1750 \pm 10\text{ RPM}$ baseline nominal speed.

2. **Transmission & Bearings:**
   - Flexible elastomeric spider coupling to dampen motor commutation harmonics.
   - 8 mm diameter precision-ground hardened shaft.
   - Dual pillow-block deep-groove ball bearings (bearing model: 608ZZ / KP08).

3. **Controlled Fault Injection:**
   - **Vibration Anomaly:** Calibrated eccentric set-screw mass attached to shaft collar ($M = 2.5\text{ g}$ at $R = 15\text{ mm}$), generating dynamic unbalance at $1\times$ rotational frequency ($f_0 \approx 29.2\text{ Hz}$).
   - **Thermal Drift:** Controlled thermal pad / radiant heat source simulating friction-induced thermal degradation ($>75^\circ\text{C}$).
