# Claude Skills

A collection of reusable Claude Code skills that can be added to any project.

## Usage

### Option 1: Git Submodule (Recommended)

Add this repository as a submodule to your project:

```bash
git submodule add <repo-url> .claude-skills
```

Then run the install script to symlink skills to your project:

```bash
./.claude-skills/install.sh
```

### Option 2: Clone Directly

Clone this repository into your project:

```bash
git clone <repo-url> .claude-skills
./.claude-skills/install.sh
```

### Option 3: Manual Copy

Copy the desired skill files from `skills/` to your project's `.claude/skills/` directory.

## Structure

```
claude-skills/
├── skills/           # Skill files (.md)
│   └── _example.md   # Example skill template
├── install.sh        # Installation script
└── README.md
```

## Creating Skills

Skills are markdown files that provide context and instructions to Claude Code. Place your skill files in the `skills/` directory.

See `skills/_example.md` for a template.

## Installed Skills

After running `install.sh`, skills are symlinked to `.claude/skills/` in your project root.

## Updating Skills

If you added this repo as a submodule, update with:

```bash
git submodule update --remote .claude-skills
./.claude-skills/install.sh
```
