# BACKLOG.md

**Level 4 — Build** | hacky-hours-docs

---

## Next Milestone

*Empty — milestone complete.*

## Future — v2.0.0: Command Audit & Revamp

Full audit and restructure of the command surface. Goal: less cumbersome, more intuitive.

- [ ] **Level → Step** throughout all docs, help text, templates, and ARCHITECTURE.md. "Step" reflects the cyclical nature; "level" implies a one-way ladder.
- [ ] **Promote `iterate` as Step 5** — it's the main loop after shipping, not an optional chore. Numeric alias `5` added alongside word alias `iterate`.
- [ ] **`--version` and `--status` as flags** — metadata about the tool belongs as flags per CLI convention. `help [cmd]` stays as subcommand (takes an argument).
- [ ] **`checklist` folded into `help build`** — it's a printout, not an operation. Undocumented in CHANGELOG; was likely added without a version entry (flag as documentation gap).
- [ ] **`migrate` absorbed into `upgrade`** — `migrate` is already handled by `upgrade` as of v1.8.0; remove the standalone `migrate` command and routing entry.
- [ ] **Evaluate flattening `learn [tour|onboard|quiz]`** — with a leaner top-level after other consolidations, assess whether flat top-level commands (`tour`, `onboard`, `quiz`) are more intuitive than the grouped `learn` approach.
- [ ] **Audit all command descriptions** — ensure every command in the help message has a clear, consistent one-line description that distinguishes it from adjacent commands.
