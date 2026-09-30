# Hardware Wiring Specification

**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Status:** Architecture Specified; Physical Validation Pending (See [HIL Specification](../../docs/HIL_SPECIFICATION.md))

## Microcontroller Pinouts (ESP32-WROOM-32)

1. **Vibration Sensor (ADXL345 3-Axis I2C Accelerometer)**
   - `VCC` -> ESP32 3V3
   - `GND` -> ESP32 GND
   - `SDA` -> ESP32 GPIO 21 ($4.7\text{ k}\Omega$ pull-up to 3.3V)
   - `SCL` -> ESP32 GPIO 22 ($4.7\text{ k}\Omega$ pull-up to 3.3V)
   - `CS`  -> Tied to 3.3V (Selects I2C mode, address `0x53`)

2. **Temperature Sensor (MAX6675 SPI Thermocouple Amplifier)**
   - `VCC` -> ESP32 3V3
   - `GND` -> ESP32 GND
   - `SO`  -> ESP32 GPIO 19 (MISO)
   - `SCK` -> ESP32 GPIO 18 (SCK)
   - `CS`  -> ESP32 GPIO 5 (Chip Select)

3. **Rotational Speed Sensor (A3144 Digital Hall-Effect Sensor)**
   - `VCC` -> ESP32 3V3
   - `GND` -> ESP32 GND
   - `OUT` -> ESP32 GPIO 4 ($10\text{ k}\Omega$ pull-up to 3.3V)

4. **Host Communication Link**
   - Micro-USB / USB-C connection to Edge Computing Host via CP2102/CH340 USB-UART bridge at 115200 baud, 8-N-1.
