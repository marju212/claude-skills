"""
KiCad Schematic Helper - Create KiCad schematics from connection definitions.

Uses kicad-sch-api to generate real .kicad_sch files that can be opened in KiCad
for PCB design, plus optionally rendered to SVG for visual verification.

Usage:
    from kicad_helper import create_schematic

    create_schematic(
        components={
            'U1': {
                'lib_id': 'MCU_Module:Teensy4.1',
                'value': 'Teensy 4.1',
                'pins': {'TX1': '1', 'RX1': '0', 'SDA': '18', 'SCL': '19', 'GND': 'GND', '3V3': '3V3'}
            },
            'U2': {
                'lib_id': 'MCU_Module:RP2040-Zero',
                'value': 'RP2040-Zero',
                'pins': {'RX': '1', 'TX': '0', 'SDA': '4', 'SCL': '5', 'GND': 'GND', '3V3': '3V3'}
            },
            'R1': {'lib_id': 'Device:R', 'value': '4.7k'},
            'R2': {'lib_id': 'Device:R', 'value': '4.7k'},
        },
        connections=[
            ('U1.TX1', 'U2.RX'),
            ('U1.RX1', 'U2.TX'),
            ('U1.SDA', 'R1.1'),
            ('R1.2', 'U2.SDA'),
            ('U1.SCL', 'R2.1'),
            ('R2.2', 'U2.SCL'),
        ],
        power_connections=[
            (['U1.3V3', 'U2.3V3', 'R1.2', 'R2.2'], 'VCC'),
            (['U1.GND', 'U2.GND'], 'GND'),
        ],
        filename='circuit.kicad_sch',
        title='Teensy ↔ RP2040',
        render_svg=True
    )

Requirements:
    pip install kicad-sch-api
    KiCad 9+ installed (for SVG rendering via kicad-cli)
"""

import subprocess
import os
import shutil
from typing import Dict, List, Tuple, Optional, Any

try:
    import kicad_sch_api as ksa
except ImportError:
    ksa = None
    print("Warning: kicad-sch-api not installed. Run: pip install kicad-sch-api")


# Grid spacing in KiCad (mm)
GRID_SPACING = 2.54
COMPONENT_SPACING_X = 40.0  # Horizontal spacing between components
COMPONENT_SPACING_Y = 10.0  # Vertical spacing between pins

# Default output directory (relative to current working directory)
DEFAULT_OUTPUT_DIR = "KiCad"


def _get_output_path(filename: str, output_dir: Optional[str] = None) -> str:
    """
    Get the full output path for a schematic file.

    If filename has no directory component, use the output_dir (default: ./KiCad/).
    Creates the output directory if it doesn't exist.
    """
    # If filename already has a directory path, use it as-is
    if os.path.dirname(filename):
        output_path = filename
    else:
        # Use specified output_dir or default
        dir_path = output_dir or DEFAULT_OUTPUT_DIR
        output_path = os.path.join(dir_path, filename)

    # Create directory if it doesn't exist
    dir_path = os.path.dirname(output_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

    return output_path


def _ensure_ksa():
    """Ensure kicad-sch-api is available."""
    if ksa is None:
        raise ImportError(
            "kicad-sch-api is required. Install with: pip install kicad-sch-api"
        )


def _snap_to_grid(value: float, grid: float = GRID_SPACING) -> float:
    """Snap a value to the nearest grid point."""
    return round(value / grid) * grid


def create_schematic(
    components: Dict[str, Dict[str, Any]],
    connections: List[Tuple[str, str]],
    filename: str,
    title: Optional[str] = None,
    power_connections: Optional[List[Tuple[List[str], str]]] = None,
    render_svg: bool = True,
    auto_layout: bool = True,
    output_dir: Optional[str] = None,
) -> str:
    """
    Create a KiCad schematic from components and connections.

    Args:
        components: Dict mapping reference designators to component specs.
            Each component spec contains:
            - lib_id: KiCad library ID (e.g., 'Device:R', 'MCU_Module:Teensy4.1')
            - value: Component value (e.g., '10k', 'Teensy 4.1')
            - pins: Optional dict mapping pin names to pin numbers (for MCUs/ICs)
            - footprint: Optional footprint ID
            - position: Optional (x, y) tuple for manual placement

        connections: List of (source, destination) tuples.
            Format: ('RefDes.PinName', 'RefDes.PinName') or ('RefDes.PinNum', 'RefDes.PinNum')

        filename: Output filename (should end in .kicad_sch).
            If no directory path, outputs to output_dir (default: ./KiCad/)

        title: Optional title for the schematic

        power_connections: Optional list of (pin_list, net_name) tuples.
            Groups pins that share a power net (VCC, GND, etc.)

        render_svg: If True, also export SVG via kicad-cli

        auto_layout: If True, automatically position components

        output_dir: Output directory for files (default: ./KiCad/)

    Returns:
        Path to the created schematic file

    Example:
        create_schematic(
            components={
                'R1': {'lib_id': 'Device:R', 'value': '10k'},
                'R2': {'lib_id': 'Device:R', 'value': '10k'},
            },
            connections=[('R1.2', 'R2.1')],
            filename='voltage_divider.kicad_sch'
        )
        # Output: ./KiCad/voltage_divider.kicad_sch
    """
    _ensure_ksa()

    # Resolve output path
    filename = _get_output_path(filename, output_dir)

    # Create new schematic
    sch = ksa.create_schematic(title or "Schematic")

    # Calculate component positions if auto_layout enabled
    positions = {}
    if auto_layout:
        positions = _auto_layout_components(components)

    # Add components
    for ref, spec in components.items():
        lib_id = spec.get('lib_id', 'Device:R')
        value = spec.get('value', '')
        footprint = spec.get('footprint', '')

        # Get position
        if 'position' in spec:
            pos = spec['position']
        elif ref in positions:
            pos = positions[ref]
        else:
            pos = (100.0, 100.0)

        # Snap to grid
        pos = (_snap_to_grid(pos[0]), _snap_to_grid(pos[1]))

        try:
            sch.components.add(
                lib_id=lib_id,
                reference=ref,
                value=value,
                position=pos,
                footprint=footprint if footprint else None
            )
        except Exception as e:
            print(f"Warning: Could not add component {ref} ({lib_id}): {e}")

    # Create pin name to number mapping for each component
    pin_maps = {}
    for ref, spec in components.items():
        if 'pins' in spec:
            pin_maps[ref] = spec['pins']
        else:
            pin_maps[ref] = {}

    # Add wire connections
    for conn in connections:
        src, dst = conn
        try:
            src_ref, src_pin = _parse_pin_ref(src, pin_maps)
            dst_ref, dst_pin = _parse_pin_ref(dst, pin_maps)
        except Exception as e:
            print(f"Warning: Could not parse pin reference {src} or {dst}: {e}")
            continue

        try:
            # Use auto_route_pins for manhattan routing with obstacle avoidance
            sch.auto_route_pins(
                src_ref, src_pin,
                dst_ref, dst_pin,
                routing_mode="manhattan",
                avoid_components=True
            )
        except Exception as e:
            # Fall back to direct wire
            try:
                sch.add_wire_between_pins(src_ref, src_pin, dst_ref, dst_pin)
            except Exception as e2:
                print(f"Warning: Could not connect {src} -> {dst}: {e2}")

    # Add power connections with labels
    if power_connections:
        for pin_list, net_name in power_connections:
            _add_power_net(sch, pin_list, net_name, pin_maps)

    # Save schematic
    sch.save(filename)
    print(f"Saved: {filename}")

    # Render SVG if requested
    if render_svg:
        svg_path = _render_svg(filename)
        if svg_path:
            print(f"Rendered: {svg_path}")

    # Generate connection table markdown
    md_path = _generate_connection_md(
        filename, title, components, connections, power_connections
    )
    if md_path:
        print(f"Documentation: {md_path}")

    return filename


def _parse_pin_ref(pin_ref: str, pin_maps: Dict[str, Dict[str, str]]) -> Tuple[str, str]:
    """
    Parse a pin reference like 'U1.TX1' into (reference, pin_number).

    Args:
        pin_ref: Pin reference string (e.g., 'U1.TX1', 'R1.2')
        pin_maps: Dict mapping component refs to pin name->number mappings

    Returns:
        Tuple of (reference_designator, pin_number)
    """
    parts = pin_ref.split('.')
    if len(parts) != 2:
        raise ValueError(f"Invalid pin reference: {pin_ref}")

    ref, pin_name = parts

    # Check if we have a pin mapping for this component
    if ref in pin_maps and pin_name in pin_maps[ref]:
        pin_num = pin_maps[ref][pin_name]
    else:
        # Assume pin_name is already the pin number
        pin_num = pin_name

    return ref, str(pin_num)


def _auto_layout_components(components: Dict[str, Dict]) -> Dict[str, Tuple[float, float]]:
    """
    Automatically calculate component positions.

    Places components in a grid pattern, grouping by type:
    - MCUs/large ICs on the left
    - Passive components (R, C, L) in the middle
    - Connectors on the right
    """
    positions = {}

    # Categorize components
    mcus = []
    passives = []
    others = []

    for ref, spec in components.items():
        lib_id = spec.get('lib_id', '')
        if any(x in lib_id for x in ['MCU', 'Module', 'IC']):
            mcus.append(ref)
        elif any(lib_id.startswith(f'Device:{x}') for x in ['R', 'C', 'L']):
            passives.append(ref)
        else:
            others.append(ref)

    # Position MCUs on the left
    y_offset = 50.0
    for i, ref in enumerate(mcus):
        x = 50.0 + (i * COMPONENT_SPACING_X * 2)
        positions[ref] = (x, y_offset)

    # Position passives in the middle
    passive_x = 50.0 + (len(mcus) * COMPONENT_SPACING_X * 2) + COMPONENT_SPACING_X
    for i, ref in enumerate(passives):
        row = i // 4
        col = i % 4
        x = passive_x + (col * COMPONENT_SPACING_X / 2)
        y = y_offset + (row * COMPONENT_SPACING_Y)
        positions[ref] = (x, y)

    # Position others on the right
    other_x = passive_x + COMPONENT_SPACING_X * 2
    for i, ref in enumerate(others):
        y = y_offset + (i * COMPONENT_SPACING_Y)
        positions[ref] = (other_x, y)

    return positions


def _add_power_net(
    sch,
    pin_list: List[str],
    net_name: str,
    pin_maps: Dict[str, Dict[str, str]]
):
    """Add a power net connecting multiple pins with a net label."""
    if not pin_list:
        return

    # Add label at first pin position
    first_ref, first_pin = _parse_pin_ref(pin_list[0], pin_maps)
    try:
        pin_pos = sch.get_component_pin_position(first_ref, first_pin)
        # Offset label slightly
        label_pos = (pin_pos[0] + 2.54, pin_pos[1])
        sch.add_label(net_name, position=label_pos)
    except Exception as e:
        # Label positioning may fail if pin position can't be determined
        print(f"Note: Could not add label '{net_name}' at pin {first_ref}.{first_pin}")

    # Connect all pins in the list
    for i in range(len(pin_list) - 1):
        src = pin_list[i]
        dst = pin_list[i + 1]
        try:
            src_ref, src_pin = _parse_pin_ref(src, pin_maps)
            dst_ref, dst_pin = _parse_pin_ref(dst, pin_maps)
            sch.add_wire_between_pins(src_ref, src_pin, dst_ref, dst_pin)
        except Exception as e:
            print(f"Warning: Could not connect power {src} -> {dst}: {e}")


def _render_svg(kicad_sch_path: str) -> Optional[str]:
    """
    Render a .kicad_sch file to SVG using kicad-cli.

    Args:
        kicad_sch_path: Path to the .kicad_sch file

    Returns:
        Path to the SVG file, or None if rendering failed
    """
    output_dir = os.path.dirname(kicad_sch_path) or '.'
    base_name = os.path.basename(kicad_sch_path).replace('.kicad_sch', '')
    svg_path = os.path.join(output_dir, f'{base_name}.svg')

    try:
        result = subprocess.run(
            ['kicad-cli', 'sch', 'export', 'svg',
             '-o', output_dir,
             kicad_sch_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            # KiCad 9 may create svg in a subdirectory, move it up if so
            subdir_svg = os.path.join(output_dir, base_name + '.svg', base_name + '.svg')
            if os.path.exists(subdir_svg):
                shutil.move(subdir_svg, svg_path)
                try:
                    os.rmdir(os.path.dirname(subdir_svg))
                except OSError:
                    pass  # Directory not empty or already removed
            # Also check if SVG was created directly
            if not os.path.exists(svg_path):
                direct_svg = os.path.join(output_dir, base_name + '.svg')
                if os.path.isfile(direct_svg):
                    return direct_svg
            return svg_path
        else:
            print(f"kicad-cli error: {result.stderr}")
            return None
    except FileNotFoundError:
        print("Warning: kicad-cli not found. Install KiCad 9+ for SVG rendering.")
        return None
    except subprocess.TimeoutExpired:
        print("Warning: kicad-cli timed out")
        return None
    except Exception as e:
        print(f"Warning: SVG rendering failed: {e}")
        return None


def _generate_connection_md(
    kicad_sch_path: str,
    title: Optional[str],
    components: Dict[str, Dict[str, Any]],
    connections: List[Tuple[str, str]],
    power_connections: Optional[List[Tuple[List[str], str]]] = None,
) -> Optional[str]:
    """
    Generate a markdown file with the connection table.

    Args:
        kicad_sch_path: Path to the .kicad_sch file
        title: Schematic title
        components: Component definitions
        connections: List of connections
        power_connections: Power net connections

    Returns:
        Path to the markdown file, or None if generation failed
    """
    md_path = kicad_sch_path.replace('.kicad_sch', '.md')
    base_name = os.path.basename(kicad_sch_path).replace('.kicad_sch', '')

    try:
        lines = []

        # Title
        lines.append(f"# {title or base_name}\n")

        # Component list
        lines.append("## Components\n")
        lines.append("| Reference | Type | Value |")
        lines.append("|-----------|------|-------|")
        for ref, spec in components.items():
            lib_id = spec.get('lib_id', 'Unknown')
            value = spec.get('value', '')
            # Extract component type from lib_id
            comp_type = lib_id.split(':')[-1] if ':' in lib_id else lib_id
            lines.append(f"| {ref} | {comp_type} | {value} |")
        lines.append("")

        # Connection table
        lines.append("## Connections\n")
        lines.append("| From | To | Net/Notes |")
        lines.append("|------|-----|-----------|")

        for src, dst in connections:
            # Try to determine the signal type
            signal_type = _infer_signal_type(src, dst)
            lines.append(f"| {src} | {dst} | {signal_type} |")
        lines.append("")

        # Power connections
        if power_connections:
            lines.append("## Power Nets\n")
            lines.append("| Net | Connected Pins |")
            lines.append("|-----|----------------|")
            for pin_list, net_name in power_connections:
                pins_str = ", ".join(pin_list)
                lines.append(f"| {net_name} | {pins_str} |")
            lines.append("")

        # Notes
        lines.append("## Notes\n")
        lines.append(f"- Schematic file: `{os.path.basename(kicad_sch_path)}`")
        lines.append(f"- SVG render: `{base_name}.svg`")

        # Add voltage level notes if MCUs detected
        mcu_refs = [ref for ref, spec in components.items()
                    if any(x in spec.get('lib_id', '') for x in ['MCU', 'Module', 'Teensy', 'Arduino', 'Pico', 'ESP'])]
        if len(mcu_refs) >= 2:
            lines.append("- Check voltage levels between MCUs (3.3V vs 5V logic)")
            lines.append("- Add level shifters if needed for voltage compatibility")

        lines.append("")

        # Write file
        with open(md_path, 'w') as f:
            f.write('\n'.join(lines))

        return md_path

    except Exception as e:
        print(f"Warning: Could not generate markdown: {e}")
        return None


# Signal type detection patterns (can be extended)
SIGNAL_PATTERNS = {
    # Pattern: (keywords_in_combined, signal_type)
    # For cross-connections (TX<->RX), handled specially below
    'SDA': 'I2C Data',
    'SCL': 'I2C Clock',
    'MOSI': 'SPI Data',
    'MISO': 'SPI Data',
    'SCK': 'SPI Clock',
    'SCLK': 'SPI Clock',
    'CS': 'SPI Select',
    'SS': 'SPI Select',
    'NSS': 'SPI Select',
    'GND': 'Ground',
    'VCC': 'Power',
    'VDD': 'Power',
    '3V3': 'Power',
    '3.3V': 'Power',
    '5V': 'Power',
    '12V': 'Power',
    'VBAT': 'Power',
    'VIN': 'Power',
    'VOUT': 'Power',
    'PWM': 'PWM',
    'ADC': 'Analog',
    'DAC': 'Analog',
    'INT': 'Interrupt',
    'IRQ': 'Interrupt',
    'RST': 'Reset',
    'RESET': 'Reset',
    'EN': 'Enable',
    'ENABLE': 'Enable',
    # RS-485 / RS-422
    'RS485': 'RS-485',
    'RS422': 'RS-422',
    '485_DE': 'RS-485 Driver Enable',
    '485_RE': 'RS-485 Receiver Enable',
    '485_DI': 'RS-485 Driver Input',
    '485_RO': 'RS-485 Receiver Output',
    'DATA+': 'RS-485 Data+',
    'DATA-': 'RS-485 Data-',
    # CAN Bus
    'CANH': 'CAN High',
    'CANL': 'CAN Low',
    'CAN_H': 'CAN High',
    'CAN_L': 'CAN Low',
    'CAN_TX': 'CAN TX',
    'CAN_RX': 'CAN RX',
}


def _infer_signal_type(src: str, dst: str) -> str:
    """
    Infer the signal type from pin names.

    Uses SIGNAL_PATTERNS dict for keyword matching.
    Add custom patterns to SIGNAL_PATTERNS to extend detection.
    """
    src_upper = src.upper()
    dst_upper = dst.upper()
    combined = src_upper + dst_upper

    # Special case: CAN bus signals (check before UART to avoid CAN_TX/CAN_RX matching as UART)
    if 'CAN' in combined:
        if 'CANH' in combined or 'CAN_H' in combined:
            return "CAN High"
        if 'CANL' in combined or 'CAN_L' in combined:
            return "CAN Low"
        if 'CAN_TX' in combined or 'CANTX' in combined:
            return "CAN TX"
        if 'CAN_RX' in combined or 'CANRX' in combined:
            return "CAN RX"
        return "CAN"

    # Special case: RS-485 transceiver pins (MAX485, etc.)
    # These short names need context - check if both pins suggest RS-485
    rs485_pins = {'DI', 'RO', 'DE', 'RE', '/RE', '~RE'}
    src_pin = src.split('.')[-1].upper() if '.' in src else src_upper
    dst_pin = dst.split('.')[-1].upper() if '.' in dst else dst_upper
    if src_pin in rs485_pins or dst_pin in rs485_pins:
        return "RS-485"

    # Special case: UART cross-connection (TX<->RX)
    if ('TX' in src_upper and 'RX' in dst_upper) or ('RX' in src_upper and 'TX' in dst_upper):
        return "UART"

    # Check against pattern dictionary
    for keyword, signal_type in SIGNAL_PATTERNS.items():
        if keyword in combined:
            return signal_type

    return ""


# Convenience function for simple 2-component diagrams
def draw_mcu_connection(
    mcu1_name: str,
    mcu1_lib_id: str,
    mcu1_pins: Dict[str, str],
    mcu2_name: str,
    mcu2_lib_id: str,
    mcu2_pins: Dict[str, str],
    connections: List[Tuple[str, str]],
    filename: str = 'mcu_connection.kicad_sch',
    title: Optional[str] = None,
    i2c_pins: Optional[List[str]] = None,
    pullup_value: str = '4.7k',
    render_svg: bool = True,
    output_dir: Optional[str] = None,
) -> str:
    """
    Simplified function for drawing MCU-to-MCU connections.

    Args:
        mcu1_name: Reference designator for first MCU (e.g., 'U1')
        mcu1_lib_id: KiCad library ID (e.g., 'MCU_Module:Teensy4.1')
        mcu1_pins: Dict mapping pin names to pin numbers
        mcu2_name: Reference designator for second MCU (e.g., 'U2')
        mcu2_lib_id: KiCad library ID
        mcu2_pins: Dict mapping pin names to pin numbers
        connections: List of (mcu1_pin_name, mcu2_pin_name) tuples
        filename: Output filename (default output to ./KiCad/)
        title: Optional title
        i2c_pins: List of pin names that are I2C (will add pullup resistors)
        pullup_value: Resistor value for I2C pullups
        render_svg: Whether to also render SVG
        output_dir: Output directory (default: ./KiCad/)

    Returns:
        Path to the created schematic file

    Example:
        draw_mcu_connection(
            mcu1_name='U1',
            mcu1_lib_id='MCU_Module:Teensy4.1',
            mcu1_pins={'TX1': '1', 'RX1': '0', 'SDA': '18', 'SCL': '19'},
            mcu2_name='U2',
            mcu2_lib_id='MCU_Module:RP2040-Zero',
            mcu2_pins={'RX': '1', 'TX': '0', 'SDA': '4', 'SCL': '5'},
            connections=[('TX1', 'RX'), ('RX1', 'TX'), ('SDA', 'SDA'), ('SCL', 'SCL')],
            i2c_pins=['SDA', 'SCL'],
            filename='teensy_rp2040.kicad_sch'
        )
    """
    i2c_pins = i2c_pins or []

    # Build component dict
    components = {
        mcu1_name: {
            'lib_id': mcu1_lib_id,
            'value': mcu1_lib_id.split(':')[-1],
            'pins': mcu1_pins,
        },
        mcu2_name: {
            'lib_id': mcu2_lib_id,
            'value': mcu2_lib_id.split(':')[-1],
            'pins': mcu2_pins,
        },
    }

    # Build connection list, adding pullup resistors for I2C
    full_connections = []
    power_connections = []
    pullup_count = 0
    processed_i2c_pins = set()  # Track which I2C pins already have pullups

    for mcu1_pin, mcu2_pin in connections:
        # Direct connection between MCUs
        full_connections.append((f'{mcu1_name}.{mcu1_pin}', f'{mcu2_name}.{mcu2_pin}'))

        # Add pullup resistor for I2C lines (once per signal line)
        i2c_signal = None
        if mcu1_pin in i2c_pins:
            i2c_signal = mcu1_pin
        elif mcu2_pin in i2c_pins:
            i2c_signal = mcu2_pin

        if i2c_signal and i2c_signal not in processed_i2c_pins:
            processed_i2c_pins.add(i2c_signal)
            pullup_count += 1
            r_ref = f'R{pullup_count}'
            components[r_ref] = {
                'lib_id': 'Device:R',
                'value': pullup_value,
            }
            # Pullup: R.1 connects to signal line, R.2 goes to VCC
            full_connections.append((f'{mcu1_name}.{mcu1_pin}', f'{r_ref}.1'))
            # Collect pullup resistor pins for VCC connection
            power_connections.append(([f'{r_ref}.2'], 'VCC'))

    return create_schematic(
        components=components,
        connections=full_connections,
        filename=filename,
        title=title,
        power_connections=power_connections if power_connections else None,
        render_svg=render_svg,
        output_dir=output_dir,
    )


# Common KiCad library IDs for quick reference
COMMON_COMPONENTS = {
    # Passives
    'resistor': 'Device:R',
    'capacitor': 'Device:C',
    'capacitor_polarized': 'Device:CP',
    'inductor': 'Device:L',
    'potentiometer': 'Device:R_Potentiometer',

    # Diodes
    'diode': 'Device:D',
    'led': 'Device:LED',
    'zener': 'Device:D_Zener',
    'schottky': 'Device:D_Schottky',

    # Transistors
    'npn': 'Device:Q_NPN_BCE',
    'pnp': 'Device:Q_PNP_BCE',
    'nmos': 'Device:Q_NMOS_GDS',
    'pmos': 'Device:Q_PMOS_GDS',

    # MCU Modules
    'teensy41': 'MCU_Module:Teensy4.1',
    'teensy40': 'MCU_Module:Teensy4.0',
    'rp2040_zero': 'MCU_Module:RP2040-Zero',
    'arduino_nano': 'MCU_Module:Arduino_Nano_v3.x',
    'esp32_devkit': 'MCU_Module:ESP32-DevKitC',

    # Connectors
    'conn_1x2': 'Connector_Generic:Conn_01x02',
    'conn_1x4': 'Connector_Generic:Conn_01x04',
    'conn_1x6': 'Connector_Generic:Conn_01x06',
    'conn_2x3': 'Connector_Generic:Conn_02x03',

    # Power
    'vcc': 'power:VCC',
    'gnd': 'power:GND',
    'vdd': 'power:VDD',
    'vss': 'power:VSS',
}


if __name__ == '__main__':
    # Example: Teensy to RP2040 connection
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
            ('TX1', 'RX'),
            ('RX1', 'TX'),
            ('SDA', 'SDA'),
            ('SCL', 'SCL'),
            ('GND', 'GND'),
            ('3V3', '3V3'),
        ],
        i2c_pins=['SDA', 'SCL'],
        filename='teensy_rp2040.kicad_sch',
        title='Teensy ↔ RP2040'
    )
