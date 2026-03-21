# Import hacky-hours-docs as a Resource

You can bring the Hacky Hours framework into an existing project so Claude Code can reference it as in-session context. This is useful when you want Claude to follow the four-level system inside a codebase that already has its own structure.

Three approaches are described below, in order of recommendation.

---

## Option 1: Git Submodule (recommended)

A git submodule adds this repo as a versioned dependency inside your project. Claude can read its files, and you control exactly which version of the framework you're using.

### Setup

Inside your project:

```bash
# Add the submodule at docs/hacky-hours/
git submodule add https://github.com/empathetech/hacky-hours-docs.git docs/hacky-hours

# Commit the submodule reference
git add .gitmodules docs/hacky-hours
git commit -m "chore: add hacky-hours-docs as submodule"
```

### Cloning a project that already has the submodule

```bash
git clone --recurse-submodules https://github.com/your-username/your-project.git
```

Or, if you've already cloned:

```bash
git submodule update --init --recursive
```

### Updating to the latest framework version

```bash
cd docs/hacky-hours
git pull origin main
cd ../..
git add docs/hacky-hours
git commit -m "chore: update hacky-hours-docs submodule"
```

### Tell Claude where to look

Add this to your project's `CLAUDE.md`:

```markdown
## Hacky Hours Framework

This project uses the Hacky Hours documentation framework.
Framework artifacts live at `hacky-hours/` (default) or wherever you placed them.

Before starting work:
- For new features: read `hacky-hours/04-build/BACKLOG.md`
- For design decisions: read the relevant doc in `hacky-hours/02-design/`
- For security concerns: read `hacky-hours/02-design/SECURITY_PRIVACY.md` before any implementation that touches user data
- For licensing: read `hacky-hours/02-design/LICENSING.md` before adding any dependency or external service
```

---

## Option 2: CLAUDE.md Reference Snippet (lightweight)

If you don't want to add a submodule, you can tell Claude to reference the framework from wherever it's installed on your system. This works well if multiple projects share the same local copy.

Add to your project's `CLAUDE.md`:

```markdown
## Hacky Hours Framework

This project follows the Hacky Hours four-level documentation framework.
The framework reference lives at: `/path/to/hacky-hours-docs/` (adjust to your local path)

When helping with design decisions, read the relevant template from the framework before making suggestions.
When helping with implementation, read `hacky-hours/02-design/SECURITY_PRIVACY.md` before proceeding.
When adding any dependency, read `hacky-hours/02-design/LICENSING.md` to check compatibility.
```

This approach requires the framework to be available at a consistent path on every machine where you work.

---

## Option 3: Manual Copy

For the simplest setup — or if you only need one or two documents — copy the relevant folders into your project:

```bash
cp -r path/to/hacky-hours-docs/design/ my-project/docs/design-framework/
```

**Tradeoff:** Your copy won't receive updates from the original framework. This is fine for a stable reference, but you'll need to manually update if the framework evolves.

---

## Related

- [fork-vs-clone.md](./fork-vs-clone.md)
- [CLAUDE.md](../../CLAUDE.md)
- [03-git-basics.md](../getting-started/03-git-basics.md)
