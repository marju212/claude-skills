# Claude Skills

A collection of reusable Claude Code skills that can be added to any project. Skills are markdown instruction files that teach Claude how to perform specialized tasks.

## Quick Start

```bash
# Clone into your project
git clone git://github.com/marju212/claude-skills.git .claude-skills

# Install everything (skills + dependencies + KiCad + libraries)
./.claude-skills/install.sh --all

# Or just install the skills (no external dependencies)
./.claude-skills/install.sh
```

After installation, skills are symlinked to your project's `.claude/skills/` directory where Claude Code can use them.

## What Are Skills?

Skills are markdown files that provide Claude with:
- **Domain knowledge** - Component libraries, pin mappings, API references
- **Workflows** - Step-by-step procedures for complex tasks
- **Code templates** - Ready-to-use Python/JavaScript patterns
- **Best practices** - Guidelines for quality output

When you ask Claude to "draw a circuit" or "create a schematic", it uses the relevant skill to produce professional results.

## Supported Platforms

| Platform | KiCad Install Method |
|----------|---------------------|
| macOS | Homebrew |
| Ubuntu/Debian | PPA |
| Fedora | dnf |
| Arch Linux | pacman |

## Available Skills

### Electronic Schematics

Generate professional circuit diagrams that output real KiCad schematic files (`.kicad_sch`) for PCB design, plus SVG rendering and markdown documentation.

**Output files** (default directory: `./KiCad/`):

| File | Description |
|------|-------------|
| `.kicad_sch` | KiCad schematic (open in KiCad for PCB design) |
| `.svg` | Rendered image for visual verification |
| `.md` | Connection table documentation |

**Workflow:**
```
User request → Claude generates schematic → .kicad_sch + .svg + .md
```

**Example prompts:**
- "Draw a voltage divider with 10k resistors"
- "Create a Teensy 4.1 to RP2040 UART connection"
- "Show me an I2C bus with pullup resistors"
- "Draw an LED circuit with current limiting resistor"

## Installation

### Full Setup (Recommended)

```bash
# Clone repository
git clone <repo-url> .claude-skills

# Install everything (auto-detects your OS)
./.claude-skills/install.sh --all
```

This installs:
- Python dependencies (`kicad-sch-api`)
- KiCad 9 (macOS, Ubuntu, Debian, Fedora, Arch)
- 3rd party symbol libraries (Teensy, official KiCad symbols)

### Installation Options

```bash
./install.sh              # Just symlink skills (no dependencies)
./install.sh --deps       # Install Python dependencies only
./install.sh --kicad      # Install KiCad 9 only
./install.sh --libs       # Download 3rd party libraries only
./install.sh --all        # Install everything
./install.sh --help       # Show help
```

### Manual Setup

If you prefer manual installation:

1. **Python dependencies:**
   ```bash
   pip install kicad-sch-api
   ```

2. **KiCad 9** (for SVG rendering):

   **macOS:**
   ```bash
   brew install --cask kicad
   # Add kicad-cli to PATH:
   echo 'export PATH="$PATH:/Applications/KiCad/KiCad.app/Contents/MacOS"' >> ~/.zshrc
   source ~/.zshrc
   ```

   **Ubuntu/Debian:**
   ```bash
   sudo add-apt-repository ppa:kicad/kicad-9.0-releases
   sudo apt-get update
   sudo apt-get install kicad
   ```

   **Fedora:**
   ```bash
   sudo dnf install kicad
   ```

   **Arch Linux:**
   ```bash
   sudo pacman -S kicad kicad-library
   ```

   **Other OS:** Download from [kicad.org/download](https://www.kicad.org/download/)

3. **3rd party libraries** (optional, for Teensy symbols):
   ```bash
   mkdir -p kicad-libs
   git clone https://github.com/XenGi/teensy_library.git kicad-libs/teensy_library
   git clone https://github.com/XenGi/teensy.pretty.git kicad-libs/teensy.pretty
   export KICAD_SYMBOL_DIR="$(pwd)/kicad-libs"
   ```

### As Git Submodule

```bash
git submodule add <repo-url> .claude-skills
./.claude-skills/install.sh --all
```

## 3rd Party Libraries

The `--libs` option downloads these libraries to `kicad-libs/`:

| Library | Source | Contents |
|---------|--------|----------|
| kicad-symbols | [GitLab](https://gitlab.com/kicad/libraries/kicad-symbols) | Official KiCad symbols |
| teensy_library | [XenGi/teensy_library](https://github.com/XenGi/teensy_library) | Teensy 4.0, 4.1, etc. |
| teensy.pretty | [XenGi/teensy.pretty](https://github.com/XenGi/teensy.pretty) | Teensy footprints |

**Other 3rd party sources:**
- [SnapEDA](https://www.snapeda.com/) - Symbols & footprints for many components
- [DigiKey](https://github.com/Digi-Key/digikey-kicad-library) - Atomic parts library
- [SparkFun](https://github.com/sparkfun/SparkFun-KiCad-Libraries) - SparkFun products

See [kicad.org/libraries/third_party](https://www.kicad.org/libraries/third_party/) for more.

## Project Structure

```
claude-skills/
├── skills/
│   ├── electronic-schematics.md          # Main skill instructions
│   ├── electronic-schematics-reference.md # Component library reference
│   └── kicad_helper.py                   # Python helper module
├── examples/
│   ├── teensy41_rp2040_uart.kicad_sch    # Example schematic
│   ├── teensy41_rp2040_uart.svg          # Rendered SVG
│   ├── teensy41_rp2040_uart.md           # Connection docs
│   └── ...
├── kicad-libs/                           # 3rd party libs (after --libs)
│   ├── kicad-symbols/
│   ├── teensy_library/
│   └── teensy.pretty/
├── install.sh
├── .gitignore
└── README.md
```

## Verification

Test the installation:

```python
from skills.kicad_helper import create_schematic

create_schematic(
    components={
        'R1': {'lib_id': 'Device:R', 'value': '10k'},
        'R2': {'lib_id': 'Device:R', 'value': '10k'},
    },
    connections=[('R1.2', 'R2.1')],
    filename='test.kicad_sch',
    title='Test Schematic'
)
```

**Expected output:**
```
Created directory: KiCad
Saved: KiCad/test.kicad_sch
Rendered: KiCad/test.svg
Documentation: KiCad/test.md
```

## Usage

### Electronic Schematics

Once installed, simply ask Claude to draw circuits:

```
> Draw a voltage divider with two 10k resistors

> Create a schematic connecting Teensy 4.1 to RP2040 over UART and I2C

> Show me an LED circuit with a 330 ohm current limiting resistor for 3.3V
```

Claude will:
1. Parse your request and identify components
2. Generate a `.kicad_sch` file using the `kicad-sch-api` library
3. Render an `.svg` preview (if KiCad CLI is installed)
4. Create a `.md` connection table for documentation

**Programmatic usage:**

```python
from kicad_helper import create_schematic, draw_mcu_connection

# Simple circuit
create_schematic(
    components={
        'R1': {'lib_id': 'Device:R', 'value': '10k'},
        'R2': {'lib_id': 'Device:R', 'value': '10k'},
    },
    connections=[('R1.2', 'R2.1')],
    power_connections=[
        (['R1.1'], 'VIN'),
        (['R2.2'], 'GND'),
    ],
    filename='voltage_divider.kicad_sch',
    title='Voltage Divider'
)

# MCU-to-MCU connection
draw_mcu_connection(
    mcu1_name='U1',
    mcu1_lib_id='MCU_Module:Teensy4.1',
    mcu1_pins={'TX1': '1', 'RX1': '0', 'SDA': '18', 'SCL': '19'},
    mcu2_name='U2',
    mcu2_lib_id='MCU_Module:RP2040-Zero',
    mcu2_pins={'RX': '1', 'TX': '0', 'SDA': '4', 'SCL': '5'},
    connections=[('TX1', 'RX'), ('RX1', 'TX'), ('SDA', 'SDA'), ('SCL', 'SCL')],
    i2c_pins=['SDA', 'SCL'],  # Adds 4.7k pullup resistors
    filename='mcu_connection.kicad_sch'
)
```

### Output Directory

By default, all output files go to `./KiCad/`. Override with:

```python
create_schematic(..., output_dir='./my-schematics/')
```

Or specify a full path in the filename:

```python
create_schematic(..., filename='/path/to/output/circuit.kicad_sch')
```

## Creating New Skills

Skills are markdown files in `skills/`. See `skills/_example.md` for a template.

**Skill file structure:**
```markdown
# Skill Name

Description of what this skill does.

## When to Use

Trigger conditions for Claude to activate this skill.

## Workflow

Step-by-step process.

## Examples

Code examples and usage patterns.
```

## Updating

```bash
# If using submodule
git submodule update --remote .claude-skills
./.claude-skills/install.sh

# If cloned directly
cd .claude-skills && git pull && ./install.sh
```

## Troubleshooting

**kicad-cli not found (macOS):**
```bash
export PATH="$PATH:/Applications/KiCad/KiCad.app/Contents/MacOS"
```

**Permission denied on install.sh:**
```bash
chmod +x install.sh
```

**Python module not found:**
```bash
pip install kicad-sch-api
```
