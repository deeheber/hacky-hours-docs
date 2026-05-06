#!/bin/bash
set -euo pipefail

REPO="empathetech/hacky-hours-docs"
BRANCH="${HH_BRANCH:-main}"
DEV_SUBPATH=".claude/skills/hacky-hours-dev"
SKILL_NAME="hacky-hours"
SKILLS_DIR="$HOME/.claude/skills"
DEST="$SKILLS_DIR/$SKILL_NAME"
OLD_COMMAND_FILE="$HOME/.claude/commands/hacky-hours.md"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "Downloading hacky-hours from $REPO ($BRANCH)..."
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" \
  | tar -xz -C "$TMP" --strip-components=1

if [ ! -d "$TMP/$DEV_SUBPATH" ]; then
  echo "Error: skill directory not found in repo archive at $DEV_SUBPATH" >&2
  exit 1
fi

mkdir -p "$SKILLS_DIR"
rm -rf "$DEST"
mv "$TMP/$DEV_SUBPATH" "$DEST"

# Transform SKILL.md from dev shape to installed shape:
# - name: hacky-hours-dev → hacky-hours
# - description: "... (dev) vX.Y.Z" → "... vX.Y.Z"
# Portable sed across macOS (BSD) and Linux (GNU).
sed -i.bak \
  -e '/^name:/ s/hacky-hours-dev/hacky-hours/' \
  -e '/^description:/ s/ (dev)//' \
  "$DEST/SKILL.md" && rm "$DEST/SKILL.md.bak"

# Clean up the v2.x single-file install if present.
if [ -f "$OLD_COMMAND_FILE" ]; then
  rm "$OLD_COMMAND_FILE"
  echo "Removed old v2.x slash command at $OLD_COMMAND_FILE"
fi

echo "Installed at $DEST"
echo "Restart Claude Code, then type /hacky-hours in any session."
