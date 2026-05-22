# /hacky-hours audit — three-lane audit with traffic-light scorecard

Supersedes v3's `review 1`. Runs three parallel lanes that evaluate the project from different angles, then consolidates into a single scorecarded report.

**Pre-flight:** Before producing any output, Read `${CLAUDE_SKILL_DIR}/references/team-preflight.md` and run its checks. This verb assumes the global skeleton and the active team exist.

**Team chat mode:** Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. Lane A's role findings are an ideal chat-mode surface — when mode is `minimal` or `full`, render the per-role headers and let voices be distinct. **No tokens for tokens' sake** — every voice turn must add information.

**Team learning capture:** Audit is always multi-role (Lane A engages Security, A11y, Ops, QA, Architect at minimum). At the tail (Step 5 below), run **Stash** per `${CLAUDE_SKILL_DIR}/references/capture-format.md`: silent `history.md` append for each agent that produced findings, then the one-line behavior-feedback prompt. Lane B (doc-stranger) and Lane C (cross-ref) are framework-internal and do not count as agent participation.

**Cost instrumentation (v4.1+):** Audit is the heaviest verb in the framework. Each lane + each role-turn + the verb itself are loggable units per `${CLAUDE_SKILL_DIR}/references/cost-instrumentation.md`. Schema is stable; harness populates token counts as instrumentation rolls out.

The three lanes:

- **(a) Role-driven codebase audit** — Security, A11y, Ops, QA, Architect read the actual code and flag issues
- **(b) Doc audit** — a context-free Claude session reads only `hacky-hours/docs/` (or the project's design docs if there's no `docs/` folder yet) and answers structured questions about whether a stranger could onboard from the docs
- **(c) Cross-reference integrity** — broken links, stale paths, contradictions between docs

Output: `hacky-hours/audits/<YYYY-MM-DD>.md` with a scorecard at the top (traffic lights + numerical aggregate), at-a-glance section, and detailed findings.

---

## Step 0 — Pre-flight

1. **Project is adopted:** if no `hacky-hours/NARRATIVE.md` exists, this project hasn't been adopted into v4 yet. Print *"Audit assumes the project has been adopted. Run `/hacky-hours adopt` first, or use v3 `review 1` if you want the older single-lane audit."*
2. **Active team:** read `AGENTS.md` for team binding; default if absent.
3. **Settings & tier:** read `CLAUDE.md` for tier and voice; respect them in calibration.

## Step 0.5 — Cost preflight (v4.1+)

Read `${CLAUDE_SKILL_DIR}/references/cost-preflight.md` for the pattern. `audit` is the heaviest verb in the framework (typical 80K–200K tokens across three lanes; Lane A alone engages 5+ roles).

Read `~/.hacky-hours/settings.yml` for `profile.plan`. Surface to the conductor:

> *"`audit` typically uses ~80K–200K tokens (~80–200% of a daily Pro limit, ~2–4% of Max-5x).*
> *  - **Proceed** — three lanes (A: role-driven, B: doc-stranger, C: cross-ref)*
> *  - **Downshift** — Lane A only with top 3 roles (security, architect, qa); skip Lane B + C; narrate-only*
> *  - **Cancel*"*

Apply the conductor's choice for the remainder of this verb. **Always fire on `plan: pro` or `unspecified`. Always fire when estimate exceeds 50K input tokens — `audit` always exceeds that threshold, so this verb's preflight runs on all plan tiers.**

## Step 1 — Three-lane fan-out

Run the three lanes in parallel where possible (Agent tool); sequentially otherwise.

### Lane A — Role-driven codebase audit

For each of these roles, spawn or roleplay the agent reading the codebase:

- **Security (Alex)** — secrets, auth, input validation, dependency vulns, threat model coverage
- **Accessibility (Lena)** — WCAG conformance, semantic HTML, keyboard nav, contrast, screen reader correctness
- **Ops (Jordan)** — observability, runbook coverage, deploy automation, rollback story
- **QA (Emma)** — test coverage on critical paths, regression risk, integration test presence
- **Architect (Priya)** — accidental complexity, dependency hygiene, missing observability hooks, brittle integrations

Each role uses this task prompt:

```
You are <Name> (the <Role>). Your system prompt is your full context.

Your task: audit this codebase from your discipline's lens. Calibrate to tier <N>.

Produce findings in this exact format:

### <Role> findings

**Dimension scores:**
- <dimension 1>: 🟢 | 🟡 | 🔴 (numeric: 0-10) — <one-line summary>
- <dimension 2>: ...
- ...

**Findings:**
- **P0:** <Specific finding with file:line ref> — <impact>
- **P1:** <...>
- **P2:** <...>

**What I deliberately didn't flag at this tier:**
- <Something you'd flag at a higher tier but isn't worth surfacing here>

Calibrate honestly. Don't pad. If you have no findings, say so plainly.
```

### Lane B — Doc audit (context-free Claude)

Spawn an Agent subagent with **no project context** — fresh slate. Give it ONLY the contents of the docs folder (`hacky-hours/docs/` if present; else `hacky-hours/02-design/` + `hacky-hours/01-ideate/` + key root docs like `README.md`).

Task prompt for the doc-audit subagent:

```
You are a senior engineer joining a project for the first time. You have NO prior context. You are reading these docs to onboard.

Read every doc in the input bundle. Answer these questions honestly:

1. **Onboarding signal:** Could you onboard from this? Give a traffic-light score (🟢 ready / 🟡 mostly / 🔴 not really) and explain in 2-3 sentences.
2. **Comprehension gaps:** What's missing or confusing? List the 3 biggest gaps a new contributor would hit.
3. **Voice & tone consistency:** Do the docs read like they were authored by a coherent team? Score 🟢/🟡/🔴 + one-sentence diagnosis.
4. **Cross-reference clarity:** Do the docs reference each other usefully, or do you feel orphaned reading any of them? Score + diagnosis.
5. **Decision visibility:** Can you see *why* this project made its key choices? (E.g., are ADRs present and readable? Are non-obvious trade-offs explained?) Score + diagnosis.
6. **First fix to onboarding friction:** If you could change ONE thing about these docs to make onboarding smoother, what would it be?

Be direct. The team wants honest signal, not validation.
```

The subagent's response becomes the doc-audit section.

#### Saturation guard (post Lane B, conductor-side, before consolidation)

Once Lane B's response is in hand and before it lands in the consolidated report, the conductor (this assistant, not the subagent) does a saturation check against the project's audit history. This addresses the failure mode where a context-free stranger keeps surfacing "first-fix" recommendations that are factually already in the docs they just read — the lane's prompt has no way to know it's already iterated against those gaps in prior runs.

Procedure:

1. **Read prior audit reports** in `hacky-hours/audits/` (most-recent first; cap at the last 3 to bound cost).
2. **Cross-check the "First fix" recommendation against current doc state.** If the stranger says "add an anchor callout to the README opening paragraph" and the README's first 10 lines already contain an anchor callout — that's a saturation signal. Use Grep/Read against the actual doc files cited in the recommendation.
3. **Cross-check against Lane C's cross-reference scan from this same run.** If Lane C verified the structure the stranger asked to be added, that's strong saturation evidence.
4. **Cross-check against prior audit asks.** If the same recommendation appears in any of the last 3 audits' "Recommended actions" sections and that action has subsequently been addressed (it's present in the current docs), saturation is highly likely.

If saturation is detected on the "First fix" item:

- **Preserve the lane's traffic-light score and the first 5 question answers.** Don't override the stranger's judgment on overall onboarding signal — they're allowed to remain 🟡 on a saturated project; that's the lane being honest about "I can't find a 🟢-tier improvement here."
- **Replace the "First fix" answer with a saturation note**: *"Lane B saturation flag: stranger's proposed first-fix [<verbatim recommendation>] is already present at [<file:line citation>] (verified during Lane C cross-ref scan / verified against [<prior audit YYYY-MM-DD>]'s recommendations). No actionable first-fix this round — the lane has run out of onboarding-gap signal for the current doc state. Consider this a graduation indicator: stranger-test is saturated."*
- **Annotate the scorecard**: append `· saturated (N)` to the Documentation dimension where N is the number of consecutive audits the lane has saturated on. Track this in `hacky-hours/audits/.lane-b-saturation` (a single-line counter file) so the count is durable across audits.
- **Honestly note in the audit report's "At-a-glance" section**: the Documentation dimension is graduation-saturated and that's a *positive* signal, not a stuck 🟡 score.

If saturation is *not* detected, pass Lane B's response through verbatim. The default behavior is unchanged.

This preserves the stranger's purity (Lane B itself is unchanged — it still reads only the docs with no prior context) while letting the conductor calibrate against the project's audit history. The stranger is the test; the conductor is the test interpreter.

### Lane C — Cross-reference integrity

Spawn or roleplay a brief framework-internal check:
- Find all internal links in markdown files (`[text](relative/path.md)`, `[link](#anchor)`, etc.)
- Verify each target exists
- Find file path references in design docs and verify they match actual file paths
- Find contradictions between docs (e.g., README says Python 3.11, but `pyproject.toml` says Python 3.10) — heuristic check

Output:

```
### Cross-reference integrity

**Broken links:** <count>
- <list>

**Stale paths:** <count>
- <list>

**Contradictions:** <count>
- <list with file refs>

Overall: 🟢 / 🟡 / 🔴
```

## Step 2 — Consolidate into audit report

Write to `hacky-hours/audits/<YYYY-MM-DD>.md`:

```markdown
# Audit — <project name> — <date>

**Tier:** <N>  ·  **Team:** <team-name>  ·  **Framework:** v4.0.1

---

## Scorecard

| Dimension | Current | Target (Tier <N>) | Δ |
|-----------|---------|--------------------|---|
| Security | 🟢/🟡/🔴 (X/10) | 🟢 (10/10) | <delta> |
| Accessibility | ... | ... | ... |
| Ops readiness | ... | ... | ... |
| Test coverage | ... | ... | ... |
| Architecture | ... | ... | ... |
| Documentation (stranger-test) | ... | ... | ... |
| Cross-reference integrity | ... | ... | ... |
| **Aggregate** | **🟢/🟡/🔴 (X/10)** | **🟢 (10/10)** | **<delta>** |

**At-a-glance:**
- <count> P0 findings (must fix before next ship)
- <count> P1 findings (should fix before next milestone)
- <count> P2 findings (improve over time)

Aggregate computed as the mean of dimension scores. Delta is current minus target.

---

## Findings by lane

### Lane A — Role audits

<concatenate Security / A11y / Ops / QA / Architect sections from fan-out>

### Lane B — Doc audit (context-free reader)

<doc audit subagent response, verbatim>

### Lane C — Cross-reference integrity

<from Lane C output>

---

## Recommended actions

**Before next ship (address all P0):**
- <list>

**Before next milestone (address P1):**
- <list>

**Improve over time (P2):**
- <list>

**Audit→CLAUDE.md threading:** Every P0 finding should produce a corresponding guardrail + enforcement mechanism in CLAUDE.md. Recommended additions:

| New guardrail | Owning role | Suggested enforcement |
|---------------|-------------|----------------------|
| <derived from P0> | <role> | <hook/CI/script suggestion> |

After this audit, run `/hacky-hours team update` to absorb durable findings into agent feedback files, and add the guardrails above to CLAUDE.md (the team will pair each with an enforcement mechanism — or honestly note "manual review only" where no automation exists yet).
```

## Step 3 — Update state

After writing the audit report:

1. Update `hacky-hours/NARRATIVE.md` — replace its trailing sentence with a fresh one: *"Last action: audit complete on <date>; <P0 count> P0s, <P1 count> P1s. Next likely action: address P0s before shipping."*
2. Update `hacky-hours/STATE.md` `last_action` and `pending_actions`.
3. Add a handoff in `hacky-hours/HANDOFFS.yml`:
   ```yaml
   - from: audit
     to: implement
     reason: "<count> P0 findings staged. Recommend fix-first iteration before further feature work."
     created: <date>
     expires: +7d
   ```
4. Optionally add P0 items to `hacky-hours/04-build/BACKLOG.md` (ask the conductor first — *"Want me to queue the P0s into BACKLOG.md?"*).

## Step 4 — Print summary

Print to the conductor:

> *"Audit complete. Aggregate score: <traffic light> (<X>/10), <delta> from Tier <N> target.*
> *  - <P0 count> P0 findings — must fix before next ship*
> *  - <P1 count> P1 findings*
> *  - <P2 count> P2 findings*
> *  - Doc audit (stranger-test) verdict: <traffic light>*
>
> *Full report: `hacky-hours/audits/<date>.md`*
>
> *Suggested next step: review the P0s, then `/hacky-hours implement` to start fixing them, or `/hacky-hours arbitrate` if any findings sit at a cross-role conflict point.*"

## Step 5 — Stash (team learning)

Run per `${CLAUDE_SKILL_DIR}/references/capture-format.md`:

1. List the Lane A agents that actually produced findings (typically: Security, A11y, Ops, QA, Architect; skip any that returned "no findings at this tier"). Lane B and Lane C are framework-internal — do not capture for them.
2. Compose a one-sentence past-tense contribution summary per participant (concrete — what they flagged and at what priority).
3. Resolve the session ID per the algorithm in `capture-format.md`.
4. **History append + metrics refresh (silent):** for each participant, append `- <date> · <project-slug> · audit · <summary>` to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md`. Then refresh the `metrics:` block in each participating agent's `profile.md` per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Commit both files together: `git -C ~/.hacky-hours/teams/<active>/ add agents/*/history.md agents/*/profile.md && git commit -m "history: audit @ <project> @ <date> — <N> agent(s)"`.
5. **Behavior feedback prompt:** ask the conductor *"Anything you said during this audit that should change how an agent works in future sessions? Free-form by agent, or `none`."* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema.
6. **Footer:** print *"Stashed <N> behavior note(s) for <agents>. Appended history to <count> agent(s) (commit <sha>). Promote with `/hacky-hours team update` when ready."*

If Lane B's saturation guard fired, the footer additionally notes: *"Lane B saturation noted — graduation indicator, not a stuck score."*

## Notes for the assistant running this

- **Parallelism via Agent tool** is the high-fidelity path. Sequential roleplay is the fallback.
- **Tier calibration is mandatory.** A 🔴 on observability at Tier 1 is wrong if a managed-host log file is sufficient for a personal tool. Re-read tier guide before scoring.
- **Cost awareness:** all-lane fan-out is the most token-expensive verb in v4. Surface a budget bar before starting.
- **Scorecard math:** dimension scores 0-10. 🟢 = 8-10, 🟡 = 4-7, 🔴 = 0-3. Aggregate = mean. Numbers are diagnostic, not gospel — the prose findings matter more.
- **Doc audit lane (b) is the "stranger test" from the design conversation, now named honestly as an audit lane.** This is the built-in graduation test — if a context-free Claude session can onboard from the docs, the graduation property is working.
