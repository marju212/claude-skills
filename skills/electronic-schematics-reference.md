# Electronic Schematics - KiCad Component Library Reference

Complete KiCad library ID reference for the electronic schematics skill. Use these IDs with `kicad-sch-api` or the `kicad_helper` module.

## Library ID Format

KiCad library IDs follow the format: `LibraryName:SymbolName`

Example: `Device:R` = Symbol "R" from library "Device"

## Passive Components

### Resistors

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| Resistor | `Device:R` | 1, 2 | Standard resistor |
| Resistor (US) | `Device:R_US` | 1, 2 | US-style zigzag symbol |
| Potentiometer | `Device:R_Potentiometer` | 1, 2, 3 | Pin 3 = wiper |
| Potentiometer (trim) | `Device:R_Potentiometer_Trim` | 1, 2, 3 | Trimmer pot |
| Thermistor | `Device:Thermistor` | 1, 2 | NTC/PTC |
| Thermistor NTC | `Device:Thermistor_NTC` | 1, 2 | |
| Thermistor PTC | `Device:Thermistor_PTC` | 1, 2 | |
| Varistor | `Device:Varistor` | 1, 2 | MOV |
| Photoresistor | `Device:R_Photo` | 1, 2 | LDR |
| Resistor Network | `Device:R_Network04` | 1-5 | 4 resistors, common pin |

### Capacitors

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| Capacitor | `Device:C` | 1, 2 | Non-polarized |
| Capacitor (polarized) | `Device:CP` | 1 (+), 2 (-) | Electrolytic |
| Capacitor (small) | `Device:C_Small` | 1, 2 | Compact symbol |
| Variable Capacitor | `Device:C_Variable` | 1, 2 | Tuning cap |
| Supercap | `Device:SuperCapacitor` | 1, 2 | EDLC |

### Inductors

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| Inductor | `Device:L` | 1, 2 | Standard |
| Inductor (core) | `Device:L_Core_Iron` | 1, 2 | With core |
| Inductor (ferrite) | `Device:L_Core_Ferrite` | 1, 2 | Ferrite core |
| Transformer | `Device:Transformer_1P_1S` | 1-4 | 1 primary, 1 secondary |

### Fuses & Protection

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| Fuse | `Device:Fuse` | 1, 2 | |
| Polyfuse | `Device:Polyfuse` | 1, 2 | Resettable |
| Spark Gap | `Device:Spark_Gap` | 1, 2 | ESD protection |

## Diodes

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| Diode | `Device:D` | K (cathode), A (anode) | |
| LED | `Device:LED` | K, A | |
| LED (RGB) | `Device:LED_RGB` | R, G, B, K/A | Common cathode/anode |
| Zener | `Device:D_Zener` | K, A | |
| Schottky | `Device:D_Schottky` | K, A | |
| TVS | `Device:D_TVS` | K, A | Transient voltage suppressor |
| TVS (bidirectional) | `Device:D_TVS_Bidirectional` | 1, 2 | |
| Photodiode | `Device:D_Photo` | K, A | |
| Bridge Rectifier | `Device:D_Bridge` | +, -, ~, ~ | |
| Tunnel Diode | `Device:D_Tunnel` | K, A | |

## Transistors

### BJT

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| NPN | `Device:Q_NPN_BCE` | B, C, E | |
| NPN (ECB) | `Device:Q_NPN_ECB` | E, C, B | Alternate pinout |
| PNP | `Device:Q_PNP_BCE` | B, C, E | |
| PNP (ECB) | `Device:Q_PNP_ECB` | E, C, B | |
| Darlington NPN | `Device:Q_NPN_Darlington_BCE` | B, C, E | |
| Phototransistor | `Device:Q_Photo_NPN` | C, E | |

### MOSFET

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| N-MOSFET | `Device:Q_NMOS_GDS` | G, D, S | |
| N-MOSFET (SGD) | `Device:Q_NMOS_SGD` | S, G, D | Alternate pinout |
| P-MOSFET | `Device:Q_PMOS_GDS` | G, D, S | |
| P-MOSFET (SGD) | `Device:Q_PMOS_SGD` | S, G, D | |
| N-MOSFET (depletion) | `Device:Q_NMOS_DGS` | D, G, S | |

### JFET

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| N-JFET | `Device:Q_NJFET_DGS` | D, G, S | |
| P-JFET | `Device:Q_PJFET_DGS` | D, G, S | |

### Thyristors

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| SCR | `Device:SCR` | A, K, G | Silicon controlled rectifier |
| TRIAC | `Device:TRIAC` | MT1, MT2, G | |
| DIAC | `Device:DIAC` | 1, 2 | |

## Integrated Circuits

### Operational Amplifiers

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| LM358 | `Amplifier_Operational:LM358` | 1-8 | Dual op-amp |
| LM324 | `Amplifier_Operational:LM324` | 1-14 | Quad op-amp |
| TL072 | `Amplifier_Operational:TL072` | 1-8 | JFET dual op-amp |
| TL074 | `Amplifier_Operational:TL074` | 1-14 | JFET quad op-amp |
| NE5532 | `Amplifier_Operational:NE5532` | 1-8 | Low-noise dual |
| OPA2134 | `Amplifier_Operational:OPA2134` | 1-8 | Audio dual |
| LM741 | `Amplifier_Operational:LM741` | 1-8 | Classic single |

### Voltage Regulators

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| 7805 | `Regulator_Linear:L7805` | IN, GND, OUT | 5V 1A |
| 7812 | `Regulator_Linear:L7812` | IN, GND, OUT | 12V 1A |
| 7905 | `Regulator_Linear:L7905` | IN, GND, OUT | -5V 1A |
| LM317 | `Regulator_Linear:LM317_TO-220` | ADJ, OUT, IN | Adjustable |
| LM337 | `Regulator_Linear:LM337_TO-220` | ADJ, OUT, IN | Neg adjustable |
| AMS1117-3.3 | `Regulator_Linear:AMS1117-3.3` | GND, OUT, IN | 3.3V LDO |
| AMS1117-5.0 | `Regulator_Linear:AMS1117-5.0` | GND, OUT, IN | 5V LDO |
| MCP1700 | `Regulator_Linear:MCP1700-3302E_TO92` | GND, OUT, IN | 3.3V 250mA |

### Voltage References

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| LM4040 | `Reference_Voltage:LM4040DBZ-2.5` | K, A | 2.5V shunt |
| REF3030 | `Reference_Voltage:REF3030` | IN, GND, OUT | 3.0V |
| TL431 | `Reference_Voltage:TL431DBZ` | K, A, REF | Adjustable |

### Timer ICs

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| NE555 | `Timer:NE555` | 1-8 | Classic 555 |
| TLC555 | `Timer:TLC555` | 1-8 | CMOS 555 |
| NE556 | `Timer:NE556` | 1-14 | Dual 555 |

### Logic ICs (74xx Series)

| Component | Library ID | Notes |
|-----------|------------|-------|
| 74HC00 | `74xx:74HC00` | Quad NAND |
| 74HC02 | `74xx:74HC02` | Quad NOR |
| 74HC04 | `74xx:74HC04` | Hex Inverter |
| 74HC08 | `74xx:74HC08` | Quad AND |
| 74HC14 | `74xx:74HC14` | Hex Schmitt Inverter |
| 74HC32 | `74xx:74HC32` | Quad OR |
| 74HC74 | `74xx:74HC74` | Dual D Flip-Flop |
| 74HC86 | `74xx:74HC86` | Quad XOR |
| 74HC125 | `74xx:74HC125` | Quad Buffer |
| 74HC138 | `74xx:74HC138` | 3-to-8 Decoder |
| 74HC164 | `74xx:74HC164` | 8-bit Shift Register |
| 74HC165 | `74xx:74HC165` | 8-bit PISO |
| 74HC245 | `74xx:74HC245` | Octal Bus Transceiver |
| 74HC595 | `74xx:74HC595` | 8-bit SIPO |

### ADC/DAC

| Component | Library ID | Notes |
|-----------|------------|-------|
| MCP3008 | `Analog_ADC:MCP3008` | 8-ch 10-bit SPI ADC |
| MCP3208 | `Analog_ADC:MCP3208` | 8-ch 12-bit SPI ADC |
| ADS1115 | `Analog_ADC:ADS1115` | 16-bit I2C ADC |
| MCP4725 | `Analog_DAC:MCP4725` | 12-bit I2C DAC |

## Microcontroller Modules

### Arduino Family

| Component | Library ID | Notes |
|-----------|------------|-------|
| Arduino Nano | `MCU_Module:Arduino_Nano_v3.x` | ATmega328P |
| Arduino Nano Every | `MCU_Module:Arduino_Nano_Every` | ATmega4809 |
| Arduino Pro Mini | `MCU_Module:Arduino_Pro_Mini` | ATmega328P |
| Arduino Uno R3 | `MCU_Module:Arduino_UNO_R3` | Full pinout |

### Teensy Family

| Component | Library ID | Notes |
|-----------|------------|-------|
| Teensy 4.1 | `MCU_Module:Teensy4.1` | i.MX RT1062 600MHz |
| Teensy 4.0 | `MCU_Module:Teensy4.0` | i.MX RT1062 600MHz |
| Teensy 3.6 | `MCU_Module:Teensy3.6` | MK66FX1M0 180MHz |
| Teensy 3.5 | `MCU_Module:Teensy3.5` | MK64FX512 120MHz |
| Teensy 3.2 | `MCU_Module:Teensy3.2` | MK20DX256 72MHz |
| Teensy LC | `MCU_Module:Teensy_LC` | MKL26Z64 48MHz |

### Raspberry Pi

| Component | Library ID | Notes |
|-----------|------------|-------|
| Pi Pico | `MCU_Module:RaspberryPi_Pico` | RP2040 |
| RP2040-Zero | `MCU_Module:RP2040-Zero` | RP2040 compact |

### ESP Family

| Component | Library ID | Notes |
|-----------|------------|-------|
| ESP32-DevKitC | `MCU_Module:ESP32-DevKitC` | ESP32 |
| ESP32-WROOM | `MCU_Module:ESP32-WROOM-32` | Module |
| ESP32-S3 | `MCU_Module:ESP32-S3-WROOM-1` | USB OTG |
| ESP8266 NodeMCU | `MCU_Module:NodeMCU-32S` | |

### STM32 (Nucleo)

| Component | Library ID | Notes |
|-----------|------------|-------|
| Nucleo-F401RE | `MCU_Module:ST_Nucleo_F401RE` | STM32F4 |
| Nucleo-F411RE | `MCU_Module:ST_Nucleo_F411RE` | STM32F4 |
| Blue Pill | `MCU_Module:BluePill_STM32F103C` | STM32F103 |

## Communication ICs

### RS-485 Transceivers

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| SN65HVD75 | `Interface_UART:SN65HVD75DR` | R, RE, DE, D, GND, A, B, VCC | 3.3V |
| MAX485 | `Interface_UART:MAX485E` | Same | 5V |
| SP3485 | `Interface_UART:SP3485EN` | Same | 3.3V low power |

### CAN Transceivers

| Component | Library ID | Notes |
|-----------|------------|-------|
| MCP2551 | `Interface_CAN_LIN:MCP2551-I-SN` | 5V CAN |
| MCP2562 | `Interface_CAN_LIN:MCP2562-E-SN` | 3.3V/5V CAN FD |
| SN65HVD230 | `Interface_CAN_LIN:SN65HVD230` | 3.3V CAN |

### I2C Buffer/Expander

| Component | Library ID | Notes |
|-----------|------------|-------|
| PCA9306 | `Interface_Expansion:PCA9306` | Level shifter |
| PCA9548A | `Interface_Expansion:PCA9548A` | 8-ch I2C mux |
| PCF8574 | `Interface_Expansion:PCF8574` | 8-bit I/O expander |

### USB Interface

| Component | Library ID | Notes |
|-----------|------------|-------|
| FT232RL | `Interface_USB:FT232RL` | USB-Serial |
| CH340G | `Interface_USB:CH340G` | USB-Serial |
| CP2102 | `Interface_USB:CP2102N-A01-GQFN24` | USB-Serial |

## Sensors

### Temperature

| Component | Library ID | Notes |
|-----------|------------|-------|
| DS18B20 | `Sensor_Temperature:DS18B20` | 1-Wire digital |
| LM35 | `Sensor_Temperature:LM35-LP` | Analog |
| TMP36 | `Sensor_Temperature:TMP36` | Analog |

### Environmental

| Component | Library ID | Notes |
|-----------|------------|-------|
| BME280 | `Sensor_Humidity:BME280` | Temp/Hum/Press I2C |
| BMP280 | `Sensor_Pressure:BMP280` | Temp/Press I2C |
| SHT31 | `Sensor_Humidity:SHT31-DIS` | Temp/Hum I2C |
| DHT22 | `Sensor_Humidity:DHT22` | Temp/Hum 1-Wire |

### Motion/Position

| Component | Library ID | Notes |
|-----------|------------|-------|
| MPU6050 | `Sensor_Motion:MPU-6050` | 6-axis IMU I2C |
| MPU9250 | `Sensor_Motion:MPU-9250` | 9-axis IMU I2C |
| AS5600 | `Sensor_Motion:AS5600` | Magnetic encoder I2C |

## Power Components

### Power Symbols

| Symbol | Library ID | Notes |
|--------|------------|-------|
| VCC | `power:VCC` | General positive supply |
| VDD | `power:VDD` | Digital positive |
| GND | `power:GND` | Ground |
| GNDA | `power:GNDA` | Analog ground |
| GNDPWR | `power:GNDPWR` | Power ground |
| +3.3V | `power:+3.3V` | 3.3V rail |
| +5V | `power:+5V` | 5V rail |
| +12V | `power:+12V` | 12V rail |
| +24V | `power:+24V` | 24V rail |
| -5V | `power:-5V` | -5V rail |
| -12V | `power:-12V` | -12V rail |
| VBUS | `power:VBUS` | USB power |
| VBAT | `power:VBAT` | Battery |

### Batteries

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| Battery | `Device:Battery` | +, - | Single cell |
| Battery Cell | `Device:Battery_Cell` | +, - | |

### DC-DC Converters

| Component | Library ID | Notes |
|-----------|------------|-------|
| LM2596 | `Regulator_Switching:LM2596S-5` | 5V 3A buck |
| MP1584 | `Regulator_Switching:MP1584` | Adj buck |
| MT3608 | `Regulator_Switching:MT3608` | Boost |

## Connectors

### Pin Headers

| Component | Library ID | Notes |
|-----------|------------|-------|
| 1x1 | `Connector_Generic:Conn_01x01` | Single pin |
| 1x2 | `Connector_Generic:Conn_01x02` | 2-pin |
| 1x3 | `Connector_Generic:Conn_01x03` | 3-pin |
| 1x4 | `Connector_Generic:Conn_01x04` | 4-pin |
| 1x5 | `Connector_Generic:Conn_01x05` | 5-pin |
| 1x6 | `Connector_Generic:Conn_01x06` | 6-pin |
| 1x8 | `Connector_Generic:Conn_01x08` | 8-pin |
| 1x10 | `Connector_Generic:Conn_01x10` | 10-pin |
| 2x3 | `Connector_Generic:Conn_02x03` | 6-pin dual row |
| 2x5 | `Connector_Generic:Conn_02x05_Odd_Even` | 10-pin (JTAG) |
| 2x10 | `Connector_Generic:Conn_02x10_Odd_Even` | 20-pin |

### USB Connectors

| Component | Library ID | Notes |
|-----------|------------|-------|
| USB-A | `Connector:USB_A` | Type A receptacle |
| USB-B | `Connector:USB_B` | Type B receptacle |
| USB-C | `Connector:USB_C_Receptacle_USB2.0` | Type C USB 2.0 |
| Micro-USB | `Connector:USB_Micro-B` | Micro B |
| Mini-USB | `Connector:USB_Mini-B` | Mini B |

### Audio

| Component | Library ID | Notes |
|-----------|------------|-------|
| 3.5mm Jack | `Connector:AudioJack3` | Stereo |
| 3.5mm TRRS | `Connector:AudioJack4` | TRRS |

### Power Connectors

| Component | Library ID | Notes |
|-----------|------------|-------|
| Barrel Jack | `Connector:Barrel_Jack_Switch` | DC power |
| Screw Terminal 2P | `Connector:Screw_Terminal_01x02` | 2-pin |
| Screw Terminal 3P | `Connector:Screw_Terminal_01x03` | 3-pin |

## Switches & Buttons

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| SPST Switch | `Switch:SW_SPST` | 1, 2 | |
| SPDT Switch | `Switch:SW_SPDT` | 1, 2, 3 | |
| Pushbutton | `Switch:SW_Push` | 1, 2 | Momentary |
| Pushbutton (DPST) | `Switch:SW_Push_DPST` | 1-4 | |
| DIP Switch 4 | `Switch:SW_DIP_x04` | 1-8 | 4-position |
| Rotary Encoder | `Device:RotaryEncoder` | A, B, C | With switch |
| Rotary Switch | `Switch:SW_Rotary4` | 1-5 | 4-position |

## Crystals & Oscillators

| Component | Library ID | Pins | Notes |
|-----------|------------|------|-------|
| Crystal | `Device:Crystal` | 1, 2 | |
| Crystal (4-pin) | `Device:Crystal_GND24` | 1-4 | With ground pins |
| Oscillator | `Oscillator:Oscillator_Crystal` | EN, GND, OUT, VDD | |
| Resonator | `Device:Resonator` | 1, 2, 3 | Ceramic |

## Displays

| Component | Library ID | Notes |
|-----------|------------|-------|
| SSD1306 64x32 | `Display:SSD1306-128x32` | I2C OLED |
| SSD1306 128x64 | `Display:SSD1306-128x64` | I2C OLED |
| HD44780 16x2 | `Display:LCD_16x2` | Character LCD |
| 7-Segment | `Display:7SEGMENT-LED` | Single digit |

## Project-Specific Components

### Common MCU Pin Mappings

#### Teensy 4.1 Key Pins
```
Pin 0  = RX1 (Serial1)
Pin 1  = TX1 (Serial1)
Pin 7  = RX2 (Serial2)
Pin 8  = TX2 (Serial2)
Pin 13 = LED / SCK0
Pin 18 = SDA0 / A4
Pin 19 = SCL0 / A5
Pin 22 = CAN-TX (CAN1)
Pin 23 = CAN-RX (CAN1)
```

#### RP2040-Zero Key Pins
```
GP0  = UART0 TX / I2C0 SDA / SPI0 RX
GP1  = UART0 RX / I2C0 SCL / SPI0 CSn
GP2  = I2C1 SDA / SPI0 SCK
GP3  = I2C1 SCL / SPI0 TX
GP4  = I2C0 SDA / UART1 TX
GP5  = I2C0 SCL / UART1 RX
GP26 = ADC0
GP27 = ADC1
GP28 = ADC2
GP29 = ADC3
```

#### ESP32-DevKitC Key Pins
```
GPIO1  = TX0 (UART0)
GPIO3  = RX0 (UART0)
GPIO21 = SDA (I2C)
GPIO22 = SCL (I2C)
GPIO18 = SCK (SPI)
GPIO19 = MISO (SPI)
GPIO23 = MOSI (SPI)
GPIO5  = CS (SPI)
GPIO32-39 = ADC1
GPIO25-27 = DAC
```

## Finding Components

If a component isn't listed:

1. **Search in KiCad:** Open Symbol Editor > Browse Libraries
2. **Check library name:** Common libraries:
   - `Device:` - Generic passives, semiconductors
   - `MCU_Module:` - Development boards
   - `Connector:` - All connectors
   - `Connector_Generic:` - Pin headers
   - `Interface_*:` - Communication ICs
   - `Sensor_*:` - Sensors by type
   - `Regulator_*:` - Power regulators
   - `Amplifier_*:` - Op-amps, audio amps
   - `74xx:` - Logic ICs
   - `power:` - Power symbols

3. **Create custom:** For custom parts, use:
```python
sch.components.add(
    lib_id="Device:R",  # Use generic symbol
    reference="U1",
    value="Custom Part",
    # Add custom properties
)
```
