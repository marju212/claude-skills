# Electronic Schematics Skill

Generate professional electronic circuit schematics using the `kicad-sch-api` Python library. This creates real `.kicad_sch` files that open in KiCad for PCB design, plus renders to SVG for visual verification.

## When to Use

Activate this skill when the user:
- Asks to "draw a circuit", "create a schematic", or "generate a diagram"
- Mentions circuit components (resistor, capacitor, op-amp, transistor, MCU, etc.)
- Requests visualization of filters, amplifiers, power supplies, or other circuits
- Needs documentation for electronics projects
- Wants a schematic they can use for PCB design

## Workflow

```
User request → Claude generates connection table → kicad-sch-api → .kicad_sch
                                                                  ↓
                                                     kicad-cli → .svg (verification)
```

**Output files** (default directory: `./KiCad/`):
1. `.kicad_sch` - Real KiCad file for PCB workflow
2. `.svg` - Rendered image for visual verification (via KiCad CLI)
3. `.md` - Connection table documentation

## Setup

```bash
pip install kicad-sch-api
```

For SVG rendering, KiCad 9+ must be installed (provides `kicad-cli`).

## Quick Method: MCU/IC Connections

For **MCU-to-MCU or multi-chip connections**, use the helper module:

```python
# If using installed skills (via install.sh), import directly:
from kicad_helper import draw_mcu_connection

# Or if accessing from the repo:
# import sys
# sys.path.insert(0, '.claude-skills/skills')
# from kicad_helper import draw_mcu_connection

draw_mcu_connection(
    mcu1_name='U1',
    mcu1_lib_id='MCU_Module:Teensy4.1',
    mcu1_pins={
        'TX1': '1', 'RX1': '0',
        'SDA': '18', 'SCL': '19',
        'GND': 'GND', '3V3': '3V3'
    },
    mcu2_name='U2',
    mcu2_lib_id='MCU_Module:RP2040-Zero',
    mcu2_pins={
        'RX': '1', 'TX': '0',
        'SDA': '4', 'SCL': '5',
        'GND': 'GND', '3V3': '3V3'
    },
    connections=[
        ('TX1', 'RX'),      # UART
        ('RX1', 'TX'),
        ('SDA', 'SDA'),     # I2C
        ('SCL', 'SCL'),
        ('GND', 'GND'),     # Power
        ('3V3', '3V3'),
    ],
    i2c_pins=['SDA', 'SCL'],      # Auto-adds 4.7k pullups
    filename='teensy_rp2040.kicad_sch',
    title='Teensy ↔ RP2040'
)
```

**When parsing user requests for MCU connections:**
1. Identify the components/MCUs mentioned
2. Look up the KiCad library ID (see Component Library Reference below)
3. Determine pin mappings (name → pin number)
4. Identify I2C pins (SDA/SCL) → add to `i2c_pins`
5. Generate the `draw_mcu_connection()` call

## General Method: Any Circuit

For **any circuit**, use `create_schematic()`:

```python
from kicad_helper import create_schematic

create_schematic(
    components={
        'R1': {'lib_id': 'Device:R', 'value': '10k'},
        'R2': {'lib_id': 'Device:R', 'value': '10k'},
        'C1': {'lib_id': 'Device:C', 'value': '100nF'},
    },
    connections=[
        ('R1.2', 'R2.1'),
        ('R2.2', 'C1.1'),
    ],
    power_connections=[
        (['R1.1'], 'VIN'),
        (['C1.2'], 'GND'),
    ],
    filename='circuit.kicad_sch',
    title='RC Circuit'
)
```

## Direct kicad-sch-api Usage

For **full control**, use the library directly:

```python
import kicad_sch_api as ksa

# Create schematic
sch = ksa.create_schematic("My Circuit")

# Add components
r1 = sch.components.add(
    lib_id="Device:R",
    reference="R1",
    value="10k",
    position=(100.0, 100.0),
    footprint="Resistor_SMD:R_0603_1608Metric"
)

r2 = sch.components.add(
    lib_id="Device:R",
    reference="R2",
    value="10k",
    position=(140.0, 100.0)
)

# Connect pins with auto-routing
sch.auto_route_pins("R1", "2", "R2", "1",
    routing_mode="manhattan",
    avoid_components=True
)

# Or direct wire
sch.add_wire_between_pins("R1", "2", "R2", "1")

# Add net labels
sch.add_label("VCC", position=(100.0, 90.0))

# Save
sch.save("circuit.kicad_sch")
```

## Component Library Reference

### Passive Components

| Component | Library ID | Pins |
|-----------|------------|------|
| Resistor | `Device:R` | 1, 2 |
| Capacitor | `Device:C` | 1, 2 |
| Polarized Cap | `Device:CP` | 1 (+), 2 (-) |
| Inductor | `Device:L` | 1, 2 |
| Potentiometer | `Device:R_Potentiometer` | 1, 2, 3 (wiper) |
| Thermistor | `Device:Thermistor` | 1, 2 |
| Fuse | `Device:Fuse` | 1, 2 |

### Diodes

| Component | Library ID | Pins |
|-----------|------------|------|
| Diode | `Device:D` | K, A |
| LED | `Device:LED` | K, A |
| Zener | `Device:D_Zener` | K, A |
| Schottky | `Device:D_Schottky` | K, A |
| TVS | `Device:D_TVS` | K, A |

### Transistors

| Component | Library ID | Pins |
|-----------|------------|------|
| NPN BJT | `Device:Q_NPN_BCE` | B, C, E |
| PNP BJT | `Device:Q_PNP_BCE` | B, C, E |
| N-MOSFET | `Device:Q_NMOS_GDS` | G, D, S |
| P-MOSFET | `Device:Q_PMOS_GDS` | G, D, S |

### Op-Amps

| Component | Library ID | Pins |
|-----------|------------|------|
| Generic Op-Amp | `Amplifier_Operational:LM358` | 1 (OUT), 2 (-), 3 (+), 4 (V-), 8 (V+) |
| TL072 | `Amplifier_Operational:TL072` | Dual op-amp |
| LM324 | `Amplifier_Operational:LM324` | Quad op-amp |

### Voltage Regulators

| Component | Library ID |
|-----------|------------|
| 7805 | `Regulator_Linear:L7805` |
| LM317 | `Regulator_Linear:LM317_TO-220` |
| AMS1117-3.3 | `Regulator_Linear:AMS1117-3.3` |

### MCU Modules

| Component | Library ID |
|-----------|------------|
| Teensy 4.1 | `MCU_Module:Teensy4.1` |
| Teensy 4.0 | `MCU_Module:Teensy4.0` |
| RP2040-Zero | `MCU_Module:RP2040-Zero` |
| Arduino Nano | `MCU_Module:Arduino_Nano_v3.x` |
| ESP32 DevKit | `MCU_Module:ESP32-DevKitC` |
| Raspberry Pi Pico | `MCU_Module:RaspberryPi_Pico` |

### Connectors

| Component | Library ID |
|-----------|------------|
| 1x2 Header | `Connector_Generic:Conn_01x02` |
| 1x4 Header | `Connector_Generic:Conn_01x04` |
| 1x6 Header | `Connector_Generic:Conn_01x06` |
| 2x3 Header | `Connector_Generic:Conn_02x03` |
| USB-C | `Connector:USB_C_Receptacle_USB2.0` |

### Power Symbols

| Symbol | Library ID |
|--------|------------|
| VCC | `power:VCC` |
| VDD | `power:VDD` |
| GND | `power:GND` |
| +3.3V | `power:+3.3V` |
| +5V | `power:+5V` |
| +12V | `power:+12V` |

## Common Circuit Examples

### Voltage Divider

```python
from kicad_helper import create_schematic

create_schematic(
    components={
        'R1': {'lib_id': 'Device:R', 'value': '10k'},
        'R2': {'lib_id': 'Device:R', 'value': '10k'},
    },
    connections=[
        ('R1.2', 'R2.1'),
    ],
    power_connections=[
        (['R1.1'], 'VIN'),
        (['R2.2'], 'GND'),
    ],
    filename='voltage_divider.kicad_sch',
    title='Voltage Divider'
)
```

### RC Low-Pass Filter

```python
create_schematic(
    components={
        'R1': {'lib_id': 'Device:R', 'value': '1.6k'},
        'C1': {'lib_id': 'Device:C', 'value': '100nF'},
    },
    connections=[
        ('R1.2', 'C1.1'),
    ],
    power_connections=[
        (['R1.1'], 'VIN'),
        (['C1.2'], 'GND'),
    ],
    filename='rc_lowpass.kicad_sch',
    title='RC Low-Pass Filter (1kHz)'
)
```

### LED with Current Limiting Resistor

```python
create_schematic(
    components={
        'R1': {'lib_id': 'Device:R', 'value': '330'},
        'D1': {'lib_id': 'Device:LED', 'value': 'Red'},
    },
    connections=[
        ('R1.2', 'D1.A'),
    ],
    power_connections=[
        (['R1.1'], 'VCC'),
        (['D1.K'], 'GND'),
    ],
    filename='led_circuit.kicad_sch',
    title='LED Circuit'
)
```

### I2C Bus with Pullups

```python
create_schematic(
    components={
        'U1': {
            'lib_id': 'MCU_Module:Teensy4.1',
            'value': 'Teensy 4.1',
            'pins': {'SDA': '18', 'SCL': '19', '3V3': '3V3', 'GND': 'GND'}
        },
        'U2': {
            'lib_id': 'Sensor:BME280',
            'value': 'BME280',
            'pins': {'SDA': '1', 'SCL': '2', 'VCC': '3', 'GND': '4'}
        },
        'R1': {'lib_id': 'Device:R', 'value': '4.7k'},
        'R2': {'lib_id': 'Device:R', 'value': '4.7k'},
    },
    connections=[
        ('U1.SDA', 'R1.1'),
        ('R1.1', 'U2.SDA'),
        ('U1.SCL', 'R2.1'),
        ('R2.1', 'U2.SCL'),
    ],
    power_connections=[
        (['R1.2', 'R2.2', 'U1.3V3', 'U2.VCC'], '3V3'),
        (['U1.GND', 'U2.GND'], 'GND'),
    ],
    filename='i2c_bus.kicad_sch',
    title='I2C Bus Connection'
)
```

## Key API Reference

### create_schematic()

```python
create_schematic(
    components: dict,      # {'R1': {'lib_id': 'Device:R', 'value': '10k', ...}}
    connections: list,     # [('R1.2', 'R2.1'), ...]
    filename: str,         # Output .kicad_sch file (default to ./KiCad/)
    title: str = None,     # Schematic title
    power_connections: list = None,  # [(['R1.1'], 'VCC'), ...]
    render_svg: bool = True,         # Also export SVG
    auto_layout: bool = True,        # Auto-position components
    output_dir: str = None,          # Output directory (default: ./KiCad/)
)
```

### draw_mcu_connection()

```python
draw_mcu_connection(
    mcu1_name: str,        # Reference designator 'U1'
    mcu1_lib_id: str,      # KiCad library ID
    mcu1_pins: dict,       # {'TX': '1', 'RX': '0', ...}
    mcu2_name: str,
    mcu2_lib_id: str,
    mcu2_pins: dict,
    connections: list,     # [('TX', 'RX'), ...]
    filename: str,         # Output file (default to ./KiCad/)
    title: str = None,
    i2c_pins: list = None, # Pins that need pullups
    pullup_value: str = '4.7k',
    render_svg: bool = True,
    output_dir: str = None,# Output directory (default: ./KiCad/)
)
```

### Direct kicad-sch-api methods

```python
sch = ksa.create_schematic("name")
sch.components.add(lib_id, reference, value, position, footprint)
sch.add_wire_between_pins(ref1, pin1, ref2, pin2)
sch.auto_route_pins(ref1, pin1, ref2, pin2, routing_mode, avoid_components)
sch.add_label(text, position)
sch.save(filename)
```

## Output

**Primary:** `.kicad_sch` file that opens in KiCad for:
- Schematic review and editing
- ERC (Electrical Rules Check)
- PCB layout (KiCad Pcbnew)
- BOM generation

**Secondary:** `.svg` file for visual verification (requires KiCad CLI)

## KiCad Coordinate System

- KiCad uses mm for coordinates
- Default grid: 2.54mm (0.1 inch)
- **Inverted Y-axis**: Lower Y values appear higher visually
- Component positions snap to grid automatically

## Best Practices

1. **Use standard library IDs** - Check the reference for correct `lib_id` values
2. **Specify pin numbers** - For MCUs/ICs, always map pin names to numbers
3. **Group power connections** - Use `power_connections` for cleaner routing
4. **Add I2C pullups** - Use `i2c_pins` parameter for automatic pullup resistors
5. **Review in KiCad** - Always open the `.kicad_sch` to verify before PCB design
6. **Ask for clarification** - If the circuit request is ambiguous, ask what topology is needed
