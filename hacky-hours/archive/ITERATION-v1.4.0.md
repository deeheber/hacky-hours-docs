# ITERATION.md

**Post-v1.3.0 iteration** | hacky-hours-docs

---

## Capture

Organic observation from using the framework on a real multi-repo project (808bit/ideation-tracker + ideation-tracker-ui):

When the framework's design phase recommends splitting into multiple repos (backend + frontend, service + UI, etc.), there is no supported path for seeding the new repo with context about the existing one. The current workaround is to manually create a seed folder (`hacky-hours/ui-repo-seed/`) with hand-crafted files — a `BACKEND_REFS.md` routing table, a pre-populated `IDEATION.md`, and a `PRODUCT_OVERVIEW.md` scoped to the new repo's role.

This pattern is valuable and repeatable, but there is no command to generate it, no standard artifact format, and no way to re-sync when the authoritative repo's design docs change.

The most useful generalization is not a "seed" command (one-directional, point-in-time) but a `link` command that:
1. Reads the authoritative repo's design docs
2. Infers the dependent repo's role and what it needs to know
3. Scaffolds the dependent repo with pre-populated context
4. Updates the authoritative repo to record the relationship
5. Can be re-run with `--sync` to surface what's changed in the authoritative repo since the link was established

The core artifact is `RELATED_REPOS.md` — a question-to-doc routing table ("when I need to know X, read Y in the other repo"), not a copy of the other repo's content.

---

## Design Decisions

- **`link` not `seed`** — seed implies a one-time handoff; link implies an ongoing relationship that can be re-synced
- **Routing table, not content copy** — `RELATED_REPOS.md` maps decision types to source doc locations; it does not duplicate content from the other repo
- **Relative local path** — `../other-repo` is portable across machines; avoids machine-specific absolute paths
- **`--sync` included in v1.4.0** — re-sync is not significantly more complex than initial link in a prompt-based framework; surfaces discrepancies without auto-updating

---

## Design Docs Needing Amendment

- **ARCHITECTURE.md** — add `link` as a new command in the Key Components table; note `RELATED_REPOS.md` as a new artifact type
- **Level 2 guidance in command prompt** — add `RELATED_REPOS.md` to the "which docs does your project need?" table, prompted when ARCHITECTURE.md indicates multi-repo

---

## Triage

| Item | Disposition |
|------|-------------|
| `/hacky-hours link` (initial + --sync) | Next milestone (v1.4.0) |
| `RELATED_REPOS.md` template | Next milestone (v1.4.0) |
| Level 2 guidance update | Next milestone (v1.4.0) |
| Help message + `help link` entry | Next milestone (v1.4.0) |
