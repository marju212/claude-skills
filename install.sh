#!/bin/bash

# Install Claude Skills
# This script:
# 1. Symlinks skills from this repository to the target project's .claude/skills directory
# 2. Installs required dependencies for electronic schematics skill

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE="$SCRIPT_DIR/skills"

# Determine project root (parent of where this repo is cloned/submoduled)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_TARGET="$PROJECT_ROOT/.claude/skills"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "  Claude Skills Installer"
echo "========================================"
echo ""

# -----------------------------------------------------------------------------
# Parse arguments
# -----------------------------------------------------------------------------
INSTALL_DEPS=false
INSTALL_KICAD=false
INSTALL_LIBS=false

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --deps       Install Python dependencies (kicad-sch-api)"
    echo "  --kicad      Install KiCad 9 (macOS/Ubuntu/Debian/Fedora/Arch)"
    echo "  --libs       Download 3rd party KiCad libraries (Teensy, etc.)"
    echo "  --all        Install everything (deps + kicad + libs)"
    echo "  --help       Show this help message"
    echo ""
    echo "Without options, only symlinks skills to project."
    echo ""
    echo "Supported platforms:"
    echo "  - macOS (via Homebrew)"
    echo "  - Ubuntu/Debian (via PPA)"
    echo "  - Fedora (via dnf)"
    echo "  - Arch Linux (via pacman)"
}

for arg in "$@"; do
    case $arg in
        --deps)
            INSTALL_DEPS=true
            ;;
        --kicad)
            INSTALL_KICAD=true
            ;;
        --libs)
            INSTALL_LIBS=true
            ;;
        --all)
            INSTALL_DEPS=true
            INSTALL_KICAD=true
            INSTALL_LIBS=true
            ;;
        --help)
            usage
            exit 0
            ;;
    esac
done

# -----------------------------------------------------------------------------
# Install Python dependencies
# -----------------------------------------------------------------------------
if [ "$INSTALL_DEPS" = true ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"

    if command -v pip &> /dev/null; then
        pip install kicad-sch-api
        echo -e "${GREEN}✓ kicad-sch-api installed${NC}"
    elif command -v pip3 &> /dev/null; then
        pip3 install kicad-sch-api
        echo -e "${GREEN}✓ kicad-sch-api installed${NC}"
    else
        echo -e "${RED}✗ pip not found. Please install Python and pip first.${NC}"
        exit 1
    fi
    echo ""
fi

# -----------------------------------------------------------------------------
# Install KiCad 9
# -----------------------------------------------------------------------------
if [ "$INSTALL_KICAD" = true ]; then
    echo -e "${YELLOW}Installing KiCad 9...${NC}"

    # Check for existing kicad-cli
    KICAD_CLI=""
    if command -v kicad-cli &> /dev/null; then
        KICAD_CLI="kicad-cli"
    elif [ -f "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" ]; then
        KICAD_CLI="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
    fi

    if [ -n "$KICAD_CLI" ]; then
        KICAD_VERSION=$("$KICAD_CLI" --version 2>/dev/null || echo "unknown")
        echo "KiCad already installed: $KICAD_VERSION"

        if [[ "$KICAD_VERSION" == 9.* ]]; then
            echo -e "${GREEN}✓ KiCad 9 already installed${NC}"
            echo ""
            # Skip installation if already at version 9
            INSTALL_KICAD=false
        else
            echo -e "${YELLOW}Upgrading to KiCad 9...${NC}"
        fi
    fi

    # Detect OS and install accordingly
    if [ "$INSTALL_KICAD" = false ]; then
        : # Skip - already installed
    else
    case "$(uname -s)" in
        Darwin)
            # macOS
            echo "Detected: macOS"
            if command -v brew &> /dev/null; then
                echo "Installing KiCad via Homebrew..."
                brew install --cask kicad
                echo -e "${GREEN}✓ KiCad installed${NC}"

                # Add kicad-cli to PATH hint
                KICAD_CLI_PATH="/Applications/KiCad/KiCad.app/Contents/MacOS"
                if [[ ":$PATH:" != *":$KICAD_CLI_PATH:"* ]]; then
                    echo ""
                    echo -e "${YELLOW}Add kicad-cli to PATH:${NC}"
                    echo "  export PATH=\"\$PATH:$KICAD_CLI_PATH\""
                    echo ""
                    echo "Or add to ~/.zshrc (or ~/.bash_profile):"
                    echo "  echo 'export PATH=\"\$PATH:$KICAD_CLI_PATH\"' >> ~/.zshrc"
                fi
            else
                echo -e "${RED}✗ Homebrew not found${NC}"
                echo "  Install Homebrew first: https://brew.sh"
                echo "  Or download KiCad manually: https://www.kicad.org/download/macos/"
            fi
            ;;

        Linux)
            # Linux - check for distro
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                if [[ "$ID" == "ubuntu" || "$ID" == "debian" || "$ID_LIKE" == *"ubuntu"* || "$ID_LIKE" == *"debian"* ]]; then
                    echo "Detected: Ubuntu/Debian"

                    # Remove KiCad 8 PPA if present
                    if [ -f /etc/apt/sources.list.d/kicad-ubuntu-kicad-8_0-releases-*.sources ]; then
                        echo "Removing KiCad 8 PPA..."
                        sudo add-apt-repository -r -y ppa:kicad/kicad-8.0-releases 2>/dev/null || true
                    fi

                    # Add KiCad 9 PPA
                    echo "Adding KiCad 9 PPA..."
                    sudo add-apt-repository -y ppa:kicad/kicad-9.0-releases
                    sudo apt-get update
                    sudo apt-get install -y kicad

                    echo -e "${GREEN}✓ KiCad 9 installed${NC}"

                elif [[ "$ID" == "fedora" ]]; then
                    echo "Detected: Fedora"
                    sudo dnf install -y kicad
                    echo -e "${GREEN}✓ KiCad installed${NC}"

                elif [[ "$ID" == "arch" || "$ID_LIKE" == *"arch"* ]]; then
                    echo "Detected: Arch Linux"
                    sudo pacman -S --noconfirm kicad kicad-library
                    echo -e "${GREEN}✓ KiCad installed${NC}"

                else
                    echo -e "${YELLOW}Unsupported Linux distro: $ID${NC}"
                    echo "  Please install KiCad 9 manually from: https://www.kicad.org/download/"
                fi
            else
                echo -e "${YELLOW}Cannot detect Linux distro.${NC}"
                echo "  Please install KiCad 9 manually from: https://www.kicad.org/download/"
            fi
            ;;

        *)
            echo -e "${YELLOW}Unsupported OS: $(uname -s)${NC}"
            echo "  Please install KiCad 9 manually from: https://www.kicad.org/download/"
            ;;
    esac
    fi
    echo ""
fi

# -----------------------------------------------------------------------------
# Install 3rd party KiCad libraries
# -----------------------------------------------------------------------------
KICAD_3RDPARTY_DIR="$SCRIPT_DIR/kicad-libs"

if [ "$INSTALL_LIBS" = true ]; then
    echo -e "${YELLOW}Installing 3rd party KiCad libraries...${NC}"

    mkdir -p "$KICAD_3RDPARTY_DIR"

    # Official KiCad symbols
    if [ ! -d "$KICAD_3RDPARTY_DIR/kicad-symbols" ]; then
        echo "Downloading official KiCad symbols..."
        git clone --depth 1 https://gitlab.com/kicad/libraries/kicad-symbols.git "$KICAD_3RDPARTY_DIR/kicad-symbols"
        echo -e "${GREEN}✓ KiCad symbols downloaded${NC}"
    else
        echo "KiCad symbols already present"
    fi

    # Teensy library (XenGi)
    if [ ! -d "$KICAD_3RDPARTY_DIR/teensy_library" ]; then
        echo "Downloading Teensy symbols..."
        git clone --depth 1 https://github.com/XenGi/teensy_library.git "$KICAD_3RDPARTY_DIR/teensy_library"
        echo -e "${GREEN}✓ Teensy symbols downloaded${NC}"
    else
        echo "Teensy symbols already present"
    fi

    # Teensy footprints (XenGi)
    if [ ! -d "$KICAD_3RDPARTY_DIR/teensy.pretty" ]; then
        echo "Downloading Teensy footprints..."
        git clone --depth 1 https://github.com/XenGi/teensy.pretty.git "$KICAD_3RDPARTY_DIR/teensy.pretty"
        echo -e "${GREEN}✓ Teensy footprints downloaded${NC}"
    else
        echo "Teensy footprints already present"
    fi

    # Set environment variable hint
    echo ""
    echo -e "${YELLOW}To use these libraries, set environment variable:${NC}"
    echo "  export KICAD_SYMBOL_DIR=\"$KICAD_3RDPARTY_DIR\""
    echo ""
    echo "Or add to your shell profile (~/.bashrc or ~/.zshrc):"
    echo "  echo 'export KICAD_SYMBOL_DIR=\"$KICAD_3RDPARTY_DIR\"' >> ~/.bashrc"
    echo ""
fi

# -----------------------------------------------------------------------------
# Symlink skills to project
# -----------------------------------------------------------------------------
echo -e "${YELLOW}Installing skills...${NC}"
echo "Source: $SKILLS_SOURCE"
echo "Target: $SKILLS_TARGET"

# Create target directory if it doesn't exist
mkdir -p "$SKILLS_TARGET"

# Count for reporting
count=0

# Symlink each skill file (excluding files starting with underscore)
for skill in "$SKILLS_SOURCE"/*.md; do
    if [ -f "$skill" ]; then
        filename=$(basename "$skill")

        # Skip files starting with underscore (templates/examples)
        if [[ "$filename" == _* ]]; then
            echo "  Skipping template: $filename"
            continue
        fi

        target="$SKILLS_TARGET/$filename"

        # Remove existing symlink or file
        if [ -L "$target" ] || [ -f "$target" ]; then
            rm "$target"
        fi

        # Create symlink
        ln -s "$skill" "$target"
        echo "  Linked: $filename"
        count=$((count + 1))
    fi
done

# Also symlink Python helper modules
for helper in "$SKILLS_SOURCE"/*.py; do
    if [ -f "$helper" ]; then
        filename=$(basename "$helper")
        target="$SKILLS_TARGET/$filename"

        if [ -L "$target" ] || [ -f "$target" ]; then
            rm "$target"
        fi

        ln -s "$helper" "$target"
        echo "  Linked: $filename"
        count=$((count + 1))
    fi
done

echo ""
if [ $count -eq 0 ]; then
    echo -e "${YELLOW}No skills installed. Add .md files to $SKILLS_SOURCE to get started.${NC}"
else
    echo -e "${GREEN}✓ Installed $count file(s) to $SKILLS_TARGET${NC}"
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "========================================"
echo "  Installation Complete"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Ask Claude to 'draw a schematic for...'"
echo "  2. Output files: .kicad_sch, .svg, .md"
echo ""
if [ "$INSTALL_LIBS" = true ]; then
    echo "3rd party libraries installed to:"
    echo "  $KICAD_3RDPARTY_DIR"
    echo ""
fi
echo "For more info, see: $SCRIPT_DIR/README.md"
