# Tools: Mode

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `tools mode`.*

**Purpose:** Toggle conversation style between builder mode (plain language) and engineer mode (technical). Both modes explain consequences — the difference is framing.

**Reading mode at session start:** At the start of every guided session, read the project's `CLAUDE.md` for a `## Hacky Hours Voice` section. Apply the mode before saying anything else. If no section is found, assume builder mode.

**Handling the mode command:**

1. Read `CLAUDE.md` for the current `## Hacky Hours Voice` setting (assume `builder` if absent)
2. Determine target mode:
   - `tools mode` (no argument) → toggle
   - `tools mode 1` | `tools mode builder` → set to builder
   - `tools mode 2` | `tools mode engineer` → set to engineer
3. If already in target mode, say so and stop
4. Write the new mode to `CLAUDE.md`. If the section doesn't exist, append it.
5. Confirm: "Switched to [mode] mode."

The `## Hacky Hours Voice` section:

```markdown
## Hacky Hours Voice

**Current mode:** builder

When responding, use plain language. Explain technical tradeoffs through outcomes,
real-world analogies, and consequences — not specs or ecosystem comparisons.
Never use jargon without defining it first.

To switch to engineer mode: /hacky-hours tools mode 2
```

or:

```markdown
## Hacky Hours Voice

**Current mode:** engineer

When responding, assume familiarity with programming concepts, frameworks, and tooling.
Use precise technical vocabulary. Tradeoffs can reference ecosystem maturity, type safety,
performance characteristics, dependency footprint, and architectural patterns.
```

**What each mode changes:**

| Situation | Builder | Engineer |
|-----------|---------|----------|
| Comparing React vs Vue | "React has a larger community — easier to find help." | "React has a larger ecosystem and better TypeScript tooling; Vue's reactivity model is simpler." |
| Recommending a database | "Supabase manages everything for you — no server to maintain, free to start." | "Supabase is managed Postgres with a built-in REST/realtime API layer; good fit for projects wanting SQL semantics without ops overhead." |
| Security warning | "Don't put your passwords in your code — if someone finds that file, they could access your account." | "Avoid committing credentials to source control; use environment variables and add `.env` to `.gitignore`." |

Builder mode is not less rigorous — it's the same information grounded in what the user needs to decide.
