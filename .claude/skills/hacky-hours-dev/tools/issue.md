# /hacky-hours issue — submit a GitHub issue to empathetech (opt-in)

Composes a GitHub issue against `empathetech/hacky-hours-docs` from local feedback or a direct user description. **Permission-gated each submission — never auto-submits.**

This is the opt-in bridge from local-only `/hacky-hours feedback` to the upstream framework improvement process.

## Step 0 — Pre-flight

1. **`gh` CLI installed and authenticated:** if `gh auth status` fails, print *"This verb needs the GitHub CLI (`gh`) installed and authenticated. Install: https://cli.github.com/. Then run `gh auth login`."* and exit.
2. **Argument parsing:** `/hacky-hours issue [<source>]`
   - `--from-feedback <file>` — use a specific feedback file as the source
   - `--from-recent` — let user pick from recent feedback files
   - (no arg) — interactive composition from scratch

## Step 1 — Source the content

### Mode A — From a specific feedback file

Read `~/.hacky-hours/feedback/<file>` and use it as the seed for the issue body.

### Mode B — Pick from recent feedback

List the most recent 10 feedback files. Let user pick one or more. If multiple: bundle them into one issue with a clear "Multiple feedback notes" header.

### Mode C — Compose from scratch

Prompt:
> *"What's the issue about? (one sentence — this becomes the title)"*
> *"More detail? (description, reproduction steps if applicable)"*
> *"Category? (bug / feature request / framework improvement / documentation)"*

## Step 2 — Compose the issue body

Generate this structure:

```markdown
**Hacky Hours version:** <from ~/.hacky-hours/version>
**Category:** <bug | feature | improvement | docs>
**Submitted via:** /hacky-hours issue

## Summary
<one-paragraph synthesis from feedback or user description>

## Detail
<longer description, reproduction steps if applicable>

## Context
- Framework version: <version>
- OS: <darwin | linux>
- Verb(s) involved: <if applicable>
- Role(s) involved: <if applicable>

<If from feedback file(s), include a "Source feedback" footer with the captured notes condensed>

---
🤖 Submitted via Hacky Hours v<version>'s /hacky-hours issue command.
```

## Step 3 — Permission gate (required)

Print the proposed issue title + body. Then:

> *"Ready to submit this to https://github.com/empathetech/hacky-hours-docs/issues?*
> *  - **yes** — submit now*
> *  - **edit** — let me revise before submitting*
> *  - **save draft** — keep it locally, don't submit (saves to `~/.hacky-hours/feedback/draft-issue-<date>.md`)*
> *  - **cancel** — drop it"*

Wait for explicit user confirmation. **Never submit on default.** Never submit without seeing the user say "yes" or equivalent.

## Step 4 — Submit (only on explicit yes)

```bash
gh issue create \
  --repo empathetech/hacky-hours-docs \
  --title "<title>" \
  --body "<body>" \
  --label "user-feedback,v<framework-major-version>"
```

If `gh issue create` succeeds: print the issue URL + confirmation.
If it fails: print the error, keep the draft locally, suggest filing manually at https://github.com/empathetech/hacky-hours-docs/issues.

## Step 5 — Update local feedback record (if applicable)

If the issue came from a `~/.hacky-hours/feedback/<file>`, update that file's frontmatter:

```yaml
submitted_upstream: true
upstream_url: https://github.com/empathetech/hacky-hours-docs/issues/<N>
submitted_at: <ISO datetime>
```

Don't delete the local file — keep the local record. The annotation just notes it went upstream.

## Privacy & control

- **You see everything before it goes.** No silent submission.
- **You can save drafts indefinitely** if you're not ready to submit yet.
- **Local-only is the default** for `/hacky-hours feedback` — `issue` is the explicit opt-in step.
- **No PII auto-stripping.** You're the reviewer. If your feedback contains paths, project names, or content you don't want public, edit before submitting.

## Notes for the assistant

- The "edit" branch can go through a few rounds. Always re-print the full title + body after each edit and re-ask the four-option permission gate.
- Bundle related feedback notes when the user picks multiple — don't open multiple issues for the same underlying problem.
- If `gh` isn't available, fall back gracefully: *"Can't submit directly (no gh CLI). Issue body is below — copy-paste to https://github.com/empathetech/hacky-hours-docs/issues/new:"* + print the body.
