#!/bin/bash

# Install Claude Skills
# This script symlinks skills from this repository to the target project's .claude/skills directory

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE="$SCRIPT_DIR/skills"

# Determine project root (parent of where this repo is cloned/submoduled)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_TARGET="$PROJECT_ROOT/.claude/skills"

echo "Installing Claude skills..."
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
            echo "Skipping template: $filename"
            continue
        fi

        target="$SKILLS_TARGET/$filename"

        # Remove existing symlink or file
        if [ -L "$target" ] || [ -f "$target" ]; then
            rm "$target"
        fi

        # Create symlink
        ln -s "$skill" "$target"
        echo "Linked: $filename"
        ((count++))
    fi
done

if [ $count -eq 0 ]; then
    echo ""
    echo "No skills installed. Add .md files to $SKILLS_SOURCE to get started."
    echo "See _example.md for a template."
else
    echo ""
    echo "Installed $count skill(s) to $SKILLS_TARGET"
fi
