# /hacky-hours meta — cluster local feedback into framework patches

The dogfood-improvement-loop closer. Reads accumulated friction from `~/.hacky-hours/feedback/` and per-agent history signals, clusters by kind (tool / seam / role), and proposes specific diffs to specific files in the framework source.

This is the verb that turns "this felt clunky" into "here's the framework edit that fixes it."

## Step 0 — Pre-flight

1. **Feedback corpus exists:** if `~/.hacky-hours/feedback/` is empty, print *"No accumulated feedback yet. Use `/hacky-hours feedback <kind> '<message>'` during sessions to capture friction, then come back here."* and exit.
2. **Framework source available:** the framework lives at the install location (`~/.claude/skills/hacky-hours/`) but its source-of-truth is the empathetech repo. Check if user has the repo cloned locally — read `~/.hacky-hours/settings.yml` for `framework_repo_path` (if set) or fall back to letting user point at it interactively.

## Step 1 — Read and parse the corpus

Read every file in `~/.hacky-hours/feedback/`. Parse each:
- frontmatter (kind, target, captured date, etc.)
- body (what happened, what was expected)
- tags

Filter out items already submitted upstream (`submitted_upstream: true` in frontmatter) unless `--include-submitted` flag is passed.

## Step 2 — Cluster

Group feedback by:

### By kind + target
- All `tool` feedback for the `audit` verb
- All `role` feedback for the `security` agent
- All `seam` feedback from `audit→implement`

### By tag overlap
Items sharing 2+ tags get a candidate cluster.

### By similarity (heuristic)
Items mentioning the same files, the same verb names, or the same role names get bundled even without shared tags.

The output of clustering is a list of **patterns** — groups of 2+ feedback items that point at the same underlying issue.

## Step 3 — Propose patches per cluster

For each pattern, propose a specific diff. Patches target framework source files:

- `tool` cluster → diff against the relevant verb file (e.g., `tools/audit.md`, `reviews/audit.md`)
- `role` cluster → diff against the role's `system-prompt.md` in `templates/team/default/agents/<role>/`
- `seam` cluster → diff against the receiving end's handoff handling (often the verb file)

Patch format (for each):

```markdown
## Patch <N>: <one-line summary>

**Pattern:** <X feedback items across <Y> sessions over <Z> days>
**Kind:** <tool | seam | role>
**Target file:** <path in framework source>

### Symptom
<aggregated description from clustered feedback>

### Root cause hypothesis
<the assistant's best guess at why the symptom keeps occurring>

### Proposed diff
```diff
--- a/<path>
+++ b/<path>
@@ ... @@
<actual diff content>
```

### Confidence
<low | medium | high> — based on cluster size, pattern clarity, and how much of the symptom the diff actually addresses.

### Open questions
- <Anything the assistant isn't sure about — invite the conductor to weigh in>
```

## Step 4 — Present to conductor

Print all proposed patches. Then offer:

> *"<N> patterns clustered into <M> proposed patches. For each, you can:*
> *  - **apply** — apply the diff locally to your installed framework (test before pushing upstream)*
> *  - **submit as issue** — open a GitHub issue against empathetech with the patch as a suggestion (uses `/hacky-hours issue`)*
> *  - **submit as PR** — fork the repo, apply locally, push, open a PR (advanced; requires fork setup)*
> *  - **skip** — drop the patch; mark the feedback as 'reviewed but not actioned'*
> *  - **edit** — let me revise the diff before applying or submitting*"

Wait for the conductor's call per patch. Don't auto-apply.

## Step 5 — Apply / submit / mark

For each patch's resolution:

- **apply:** modify the file at the install path (`~/.claude/skills/hacky-hours/<file>`). Note: this will be overwritten on next `/hacky-hours update` unless you also push the change upstream. Warn the user.
- **submit as issue:** call `/hacky-hours issue` flow with the patch as the body.
- **submit as PR:** complex — for v4.0.0, print *"PR submission isn't automated yet. Apply the diff to your local fork manually and push. Patch content is above."*
- **skip:** mark the source feedback files with `meta_reviewed: skipped` in frontmatter.
- **edit:** re-prompt for diff revisions, then re-ask.

## Step 6 — Update feedback metadata

For every feedback file that was clustered, add to its frontmatter:

```yaml
meta_reviewed: <date>
meta_outcome: <applied | issue | pr | skipped>
meta_patch_ref: <issue URL or local patch sha if applied>
```

This prevents the same items from being re-clustered next time.

## Notes for the assistant

- **Be conservative on confidence.** Patches from 2-3 feedback items in similar shape can be medium-confidence. Patches from a single feedback item should be low-confidence and surface as "consider this, but I'd want to see more signal before applying."
- **Don't propose patches against agent system prompts lightly.** Those are the most carefully-written parts of the framework. A role-friction pattern needs at least 3 items before a system-prompt patch is proposed.
- **Surface patterns even if no patch is obvious.** Sometimes the meta-output is "I see a pattern here but I don't know the fix yet — you should look at this." That's still valuable.
- **The conductor is the gatekeeper.** This verb proposes; it never decides.

## What this verb completes

This is the dogfood-improvement-loop closer the design promised. Without it, agents and verbs are frozen at their initial implementations. With it, lived friction becomes framework edits, and the framework gets better the more it's used.

For v4.0.0: the loop is end-to-end functional but inherently as good as the patterns you accumulate. The first useful run probably needs 10+ feedback items to surface meaningful clusters. Until then, treat `/hacky-hours meta` as a "see what's accumulated" diagnostic rather than a patch-generator.
