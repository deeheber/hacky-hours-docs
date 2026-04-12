# TESTING.md

**Level 2 — Design** | hacky-hours-docs

---

## What is This?

A testing design document describes how you verify that what you built actually works the way you intended. It covers your testing strategy, what kinds of tests you'll write (or run manually), and what "good enough" looks like before you ship.

For most projects this means code tests. For hacky-hours-docs, which has no code, it means something different — see below.

---

## Testing Strategy

hacky-hours-docs has no runtime code. The "product" is a command prompt and a set of Markdown templates. Testing here means verifying that:

1. **The command routes correctly** — every argument lands in the right workflow
2. **The generated artifacts are correct** — scaffolded files have the right structure, paths, and content
3. **The guidance is internally consistent** — docs referenced in one place exist and say what they're claimed to say
4. **New commands behave as specified** — the guidance matches what the command prompt actually does

### Testing Layers

| Layer | What it covers | How it's done |
|-------|----------------|---------------|
| Command routing | Does `/hacky-hours <arg>` land in the right section? | Manual invocation + eval scripts |
| Scaffold output | Does scaffold produce the correct file structure? | Manual dry-run review |
| Cross-reference integrity | Do links between docs point to real targets? | `/hacky-hours optimize` Phase 3 |
| Command guidance accuracy | Does the help text match the actual behavior? | Manual review before release |
| Generated Astro sites (v1.8.0+) | Do tour/quiz sites render correctly and meet WCAG 2.1 AA? | Manual browser testing + axe/Lighthouse |

### What We Don't Test (and Why)

- **LLM output quality** — Claude's responses are non-deterministic. We can test routing and structure, not the quality of every conversation.
- **User project outcomes** — we can't verify that a user's PRODUCT_OVERVIEW.md is "good." We verify that the command asked the right questions.
- **Every edge case of `--root` paths** — accepted fragility. We test the default (`hacky-hours/`) and the project root (`--root .`) and treat other paths as best-effort.

---

## Pre-Release Checklist

Before tagging any release:

- [ ] All new command arguments tested via manual invocation in a clean repo
- [ ] `dry-run` tested for any new scaffold changes
- [ ] `audit` run against this repo — scorecard reviewed
- [ ] `optimize` run — Phase 3 cross-reference check passes
- [ ] Version strings bumped in all three places (routing table, help message, subcommand help)
- [ ] For releases with new web artifacts (v1.8.0+): Astro sites tested in browser, Lighthouse accessibility score reviewed

---

## Eval Framework (Command Behavior)

The `hacky-hours-workspace` skill eval system provides structured test cases for command behavior. Evals compare responses with and without the skill loaded to measure behavioral consistency.

Current eval coverage:
- `version` — verifies version string matches latest tag
- `status` — verifies correct level detection
- `dry-run` — verifies no files are written
- `audit` — verifies help text format

Gaps (not yet covered by evals):
- `iterate`, `optimize`, `pivot` workflows
- `learn` suite (v1.8.0 — needs evals written as part of implementation)
- `upgrade` (v1.8.0 — needs evals written as part of implementation)

---

## v1.8.0 Testing Notes

The learn suite introduces the first interactive web artifacts in the framework. Before these ship:

1. **Astro build:** Run `npm run build` in each generated site (`learn/tour/`, `learn/quiz/`) and verify no build errors
2. **Feedback form:** Test that submitting the feedback form writes a correctly named file to `hacky-hours/feedback/`
3. **`onboard` git push:** Test in a repo with a remote that the feedback commit stages only the feedback file (not other working tree changes)
4. **Node.js fallback:** Test that all three learn modes degrade cleanly to conversation mode when Node is not installed

---

## Related

- [ARCHITECTURE.md](./ARCHITECTURE.md) — Known Fragility section
- [ACCESSIBILITY.md](./ACCESSIBILITY.md) — WCAG 2.1 AA requirements for generated sites
- [SECURITY_PRIVACY.md](./SECURITY_PRIVACY.md) — Risk Surface section on automated git push
