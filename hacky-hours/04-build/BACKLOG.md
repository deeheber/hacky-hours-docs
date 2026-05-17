# BACKLOG.md

**Step 4 — Build** | hacky-hours-docs

---

## Next Milestone — v4.0.0

### Slice 11 — Team chat (tiered closed-captioned multi-agent dialogue)

**Type:** Implementation (v4.0.0 requirement)
**Branch:** `feat/v4-team-chat`
**Design:** `02-design/V4_DESIGN.md` §4.20
**Origin:** Pilot feedback — orchestra was inaudible; thesis underdelivered.

Make the team visibly present during multi-role verbs, tiered so the cost premium matches the user's appetite. Adds `/hacky-hours team chat <off | minimal | full>` (default `minimal`), upfront cost surfacing, and threads tiered dialogue rendering through verbs that fan out to multiple roles.

**Scope:**

*Settings & command:*
- `~/.hacky-hours/settings.yml` — add `team_chat: off | minimal | full` (default `minimal`)
- `tools/team.md` — extend routing to handle `team chat <mode>` subcommand; emit a one-line caveat when switching to `full` that it costs meaningfully more than `off`/`minimal` (no numeric estimate — we don't have calibration)
- `SKILL.md` — register the subcommand in the routing table and help text

*Render contract (new shared reference):*
- `references/chat-format.md` — canonical role emoji from §5 + bold `**Name (Role) [HH:MM]**` header, content on next line, blank line between turns
- Render rules for `minimal` (header only at meaningful moments — concern introduction, disagreement, hand-off) and `full` (full closed-captioned dialogue with side chatter)

*The hard rule:*
- Each affected verb's guidance file gets a "no tokens for tokens' sake" enforcement block: every voice turn must add information the conductor needs. Empty acknowledgments, filler agreement, manufactured disagreement, and restating another role's point are forbidden. Documented and surfaced as a constraint on the assistant's rendering.

*Fan-out hook:*
- Verbs in scope (`ideate`, `design`, `audit`, `adopt`, `arbitrate`, `implement`, `ship`) read `team_chat` mode
- When `minimal` or `full`, the verb's role fan-out must genuinely happen and captured per-role reasoning is what renders — not a single voice dressed in name tags
- When `off`, current behavior unchanged

*Voice fidelity:*
- Turns render in each agent's `profile.md` voice baseline so voices are recognizable from tone before the speaker tag

*Budget integration (existing infra, no new estimation):*
- Existing `session_budget_warn` from §4.3 still applies — it fires on actual consumption, no estimation needed
- No preflight cost block, no per-mode token forecasts, no subscription tier mapping. We do not have calibration data, Anthropic doesn't publish tier envelopes precisely, and skills can't read `/usage`. Any number would be folklore.
- Per-verb calibration data accumulation (`~/.hacky-hours/sessions/`) is **deferred to v4.1+**, where it may unlock honest cost surfacing.

*Misc:*
- CHANGELOG entry under `[Unreleased] — feat/v4.0.0` as "Slice 11 — team chat (tiered)"
- V4_QA.md test plan additions for each of the three modes

**Done when:**
- `/hacky-hours team chat full` then running a multi-role verb produces closed-captioned dialogue with canonical emoji + bold attribution, distinct voices, hand-offs as turns, and no filler.
- `/hacky-hours team chat minimal` produces attribution only at meaningful moments — clearly less verbose than `full`, clearly more present than `off`.
- `/hacky-hours team chat off` restores single-narrator output verbatim — no residual chat artifacts.
- Switching to `full` prints a one-line caveat that it costs meaningfully more than the other modes (no numbers).
- The "no tokens for tokens' sake" rule is documented in `references/chat-format.md` and enforced in verb guidance files — a manual review of a `full`-mode run produces zero filler turns.

---

## Backlog (unscheduled)

### BACKLOG hygiene pass (post-v4.0.0)

Cross-check `02-design/V4_DESIGN.md` deferred-scope list against shipped slices and re-seed the unscheduled backlog with the actual v4.1+ candidates (extensibility for additional roles, implicit feedback capture, etc.). The list below is intentionally empty until that pass — better empty than stale.
