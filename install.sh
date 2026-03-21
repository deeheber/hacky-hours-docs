#!/bin/bash
set -e

DEST="$HOME/.claude/commands/hacky-hours.md"
SRC="https://raw.githubusercontent.com/empathetech/hacky-hours-docs/main/.claude/commands/hacky-hours-dev.md"

mkdir -p "$HOME/.claude/commands"
curl -fsSL "$SRC" -o "$DEST"
sed -i '' '/^description:/ s/ (dev)//' "$DEST"

echo "Installed. Type /hacky-hours in any Claude Code session."
