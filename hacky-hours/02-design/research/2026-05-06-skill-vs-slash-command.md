# Research: Skill format vs. slash command format

**Status:** Complete — recommends ADR + migration
**Date:** 2026-05-06
**Branch:** `research/skill-vs-slash-command`
**Triggered by:** v2.1.0 ITERATION research spike

---

## TL;DR

Anthropic has officially **merged custom slash commands into skills**. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Slash commands are not deprecated, but **skills are the documented forward-looking format**.

For `hacky-hours`, migrating from `commands/hacky-hours.md` to `skills/hacky-hours/SKILL.md` is:

- **Non-disruptive to users** — same `/hacky-hours` invocation, same arguments, same behavior
- **Mechanically simple** — move the file, update install scripts
- **Strategically aligned** — unlocks bundled supporting files, which is the missing primitive for the two-tier artifacts spike (the other open backlog item)

**Recommendation:** Migrate, alongside the two-tier artifacts work. Treat as v3.0.0 due to install-path change. Spawn an ADR + migration task.

---

## What's already true (no migration needed)

The slash command currently uses every feature available to skills' inline content:

| Feature | Available in slash commands? |
|---|---|
| `$ARGUMENTS` substitution | ✓ |
| `!` `` `<shell command>` `` `` injection | ✓ |
| Frontmatter (per Anthropic docs) | ✓ — same fields as skills |
| User invocation via `/name` | ✓ |
| Live edits picked up mid-session | ✓ |

The "skill" entries in the available-skills list this session (`hacky-hours`, `hacky-hours-dev`) are not separately authored SKILL.md files — they are the harness auto-presenting the slash commands. Verified locally: only `~/.claude/commands/hacky-hours.md` and `.claude/commands/hacky-hours-dev.md` exist; no SKILL.md anywhere.

The skill-creator workspace at `~/.claude/commands/hacky-hours-workspace/iteration-1/` evaluates the slash command file as the "skill" — `with_skill` means "with the slash command's instructions loaded."

---

## What skills offer that slash commands don't

These are the deltas — capabilities the SKILL.md format provides that a single `commands/*.md` file does not.

### 1. Bundled supporting files

A skill is a **directory**, not a file:

```
hacky-hours/
├── SKILL.md          # entrypoint
├── templates/        # design doc templates (ARCHITECTURE.md, DATA_MODEL.md, ...)
├── references/       # extended guidance (loaded only when needed)
└── scripts/          # helpers Claude can execute
```

**Why this matters for us:** The slash command is currently ~1,500 lines and growing. Most of that is template content and per-step guidance that gets inlined into the prompt every session, even when only one step is active. With a skill, the SKILL.md stays small (orientation + routing) and step-specific or template content lives in separate files Claude only reads when it needs them.

This is the **direct enabler for the two-tier artifacts spike** (the other open backlog item). If each design doc has a summary template and a deep template, those are natural skill files — the skill loads them when the user is in Step 2, not before.

### 2. Auto-invocation by Claude

Skills can be loaded automatically when their `description` matches the conversation, without the user typing `/hacky-hours`. For a framework command, this is **probably undesirable** — `hacky-hours` is workflow-driven, and silent auto-invocation would surprise users. We'd set `disable-model-invocation: true` to opt out.

But the inverse — the auto-discovery mechanism — means a skill's `description` is what surfaces it in the menu and what Claude uses to decide relevance. Worth tuning carefully.

### 3. Frontmatter capabilities (selected)

| Field | Useful for `hacky-hours`? |
|---|---|
| `disable-model-invocation: true` | Yes — keep invocation user-only |
| `allowed-tools` | Maybe — pre-approve `Read`, `Bash(git ...)` to reduce permission prompts during sessions |
| `argument-hint` | Yes — `[step | review | learn | update | tools | ...]` autocomplete |
| `arguments` | Maybe — named positional args could replace the manual `--root` parsing |
| `paths` | Probably no — framework is project-agnostic |
| `context: fork` | No — needs main conversation |
| `model` / `effort` | Probably no — let session settings govern |
| `hooks` | Possibly later |

`allowed-tools` is the most immediately valuable one. Right now, every session triggers permission prompts for Read, Bash, etc. A skill could pre-approve a narrow set.

### 4. Subagent execution

Skills can run with `context: fork` to execute in an isolated subagent. Not relevant for the main `hacky-hours` command (it needs the conversation), but **could be relevant for sub-skills** — e.g., a `hacky-hours-research` sub-skill that runs investigation in an `Explore` agent and reports back.

---

## What migration looks like

### File moves

```
~/.claude/commands/hacky-hours.md           →  ~/.claude/skills/hacky-hours/SKILL.md
.claude/commands/hacky-hours-dev.md         →  .claude/skills/hacky-hours-dev/SKILL.md
```

### SKILL.md frontmatter (proposed)

```yaml
---
name: hacky-hours
description: Guide your project through the Hacky Hours framework — five-step LLM-assisted app development (ideate → design → roadmap → build → iterate). Invoke with /hacky-hours [command].
disable-model-invocation: true
argument-hint: [step | review | learn | update | tools | help]
allowed-tools: Read Bash(git status*) Bash(git log*) Bash(git diff*) Bash(gh issue list*) Bash(gh release*)
---
```

### Install script changes

`install.sh` and `install.ps1` currently write a single file to `~/.claude/commands/hacky-hours.md`. They'd need to:

1. Create directory `~/.claude/skills/hacky-hours/`
2. Write `SKILL.md` (with frontmatter prepended)
3. Optionally write supporting files
4. Detect and remove old `~/.claude/commands/hacky-hours.md` to avoid duplicate `/hacky-hours` entries

### Backward compat

Per Anthropic: "if a skill and a command share the same name, the skill takes precedence." So leaving the old file in place is non-fatal but creates clutter. Install script should clean up.

### Version bump

Install path change → **v3.0.0**. Major version is also a good signal for the framework's strategic direction (artifact bundling, two-tier docs, etc.).

---

## Open questions

1. **Should we go further than a mechanical move?** A naive migration just relocates the file. The bigger win is breaking the SKILL.md into entrypoint + supporting files. That's more work, but it's a one-time refactor that compounds (every future doc/template lives in its own file).
2. **Sequencing with the two-tier artifacts spike.** If we migrate first, the supporting-files structure is ready when we design the two-tier templates. If we do them together, we can co-design the skill layout and the artifact pattern. Probably the latter is better — the structure should be informed by the artifact design.
3. **Sub-skills?** Skills can reference other skills indirectly. Worth exploring whether `hacky-hours review`, `hacky-hours learn`, `hacky-hours tools upgrade` etc. should become standalone skills (`/hh-review`, `/hh-learn`) or stay as routes inside one skill. Probably stay routed for now — too much surface fragmentation otherwise.
4. **What does `hacky-hours-dev` become?** Project-local skill at `.claude/skills/hacky-hours-dev/SKILL.md` — same migration shape.

---

## Recommendation

Spawn two follow-on items:

1. **ADR** — `02-design/decisions/2026-MM-DD-migrate-to-skill-format.md`
   - Decision: migrate from slash command file to SKILL.md skill format
   - Rationale: (this writeup, summarized)
   - Consequences: install path change, major version bump, enables artifact bundling
   - Sequencing: do alongside two-tier artifacts spike, not before

2. **Migration task in BACKLOG** — gated on the two-tier artifacts spike completing or running concurrently. Branch `feat/migrate-to-skill-format`. Targets v3.0.0.

Do not retire the slash command surface (`.claude/commands/`); it remains supported and projects using older versions of `hacky-hours` should continue to work.

---

## References

- Anthropic Skills docs: https://code.claude.com/docs/en/skills
- Agent Skills open standard: https://agentskills.io
- Existing slash command: `~/.claude/commands/hacky-hours.md`
- Skill-creator eval workspace (proves slash command is treated as a skill): `~/.claude/commands/hacky-hours-workspace/iteration-1/`
