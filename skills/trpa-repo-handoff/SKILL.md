---
name: trpa-repo-handoff
description: "How TRPA hands off repo work between staff and their Claude Code instances. Use this skill at the start of any session in a TRPA repo (read docs/HANDOFF.md and docs/CONTEXT.md before touching code), when setting up a new repo or one missing those files, and whenever someone says hand off, handoff, wrap up, pick up where someone left off, continue their work, what is the status of this repo, or ends a session that changed code or data. It standardizes the tracked repo memory (root CLAUDE.md plus docs/CONTEXT.md, docs/HANDOFF.md, and docs/DECISIONS.md) so git pull is the handoff. Pairs with trpa-data-engineering (which owns docs/METHODS.md and docs/CHANGELOG.md in pipeline repos) and trpa-dashboard-qa."
---

# TRPA repo handoff

Claude Code remembers a repo in `~/.claude/projects/<repo>/memory/`. That folder is machine local and never reaches a coworker. The only memory that travels is what is committed. This skill keeps the parts a coworker needs in four tracked files, so `git pull` is the handoff and the next person's Claude starts where yours stopped.

Rule zero: HANDOFF.md is the current state, not a diary. Rewrite it at every handoff. Git history is the diary.

## The files

| File | Holds | Changes | Loaded |
|---|---|---|---|
| `CLAUDE.md` (repo root) | The protocol, the skills this repo uses, and imports of the two docs below. Under 40 lines. | Rarely | Every session, automatically |
| `docs/CONTEXT.md` | Stable facts: purpose, how to run it, layout, data and services, conventions, gotchas, who to ask | When a stable fact changes | Every session, through the import |
| `docs/HANDOFF.md` | Where it stands, next steps, open questions, blockers, do not list, how to pick up | Every handoff, rewritten | Every session, through the import |
| `docs/DECISIONS.md` | Dated log of choices and why, newest first | When a decision is made | On demand, before changing an approach |

`CLAUDE.md` imports the two docs with `@docs/HANDOFF.md` and `@docs/CONTEXT.md`, so they load with it at launch. That is what makes "always look there first" automatic instead of a habit. It also means both docs cost context every turn, so keep HANDOFF.md near 40 lines and CONTEXT.md under 100. DECISIONS.md grows, so it is not imported.

The repo carries its own protocol in `CLAUDE.md`. A coworker without this skill still gets the pickup and handoff behavior; the skill adds the checks, the templates, and the handoff note.

Data pipeline repos built with the `trpa-data-engineering` conventions already have `docs/METHODS.md` and `docs/CHANGELOG.md`. Keep them. CONTEXT.md links to METHODS.md instead of repeating it, and CHANGELOG.md stays the record of logic changes. DECISIONS.md is for the why, including choices that changed no code.

## Pick the mode

- No `CLAUDE.md` or `docs/HANDOFF.md` in the repo: run **Init**, then continue with the task.
- Session start in a repo that has them, or anyone says pick up, continue, status, or what was I doing: run **Pickup**.
- Anyone says hand off, wrap up, send this to someone, or the session changed code, data, or config and is ending: run **Handoff**.

## Init

Create the four files from `assets/` and fill them from what the repo already says. Read `README.md`, `config.yaml`, `environment.md`, `package.json`, existing `docs/`, the folder tree, and `git log --oneline -30`. Fill only what you can trace to the repo or the conversation; leave `<placeholders>` for the rest. Then ask for the gaps in one message, grouped: owner, repo type, how to run it, who it will be handed to, and anything blocked. Do not invent an owner or a next step.

Add the repo's skills to `CLAUDE.md`. Pick from the TRPA marketplace by repo type: `trpa-data-services` for anything that reads TRPA data, `trpa-data-engineering` for pipelines and notebooks where that skill is in use, `trpa-dashboard-stack` plus a brand skill (`trpa-brand`, `trpa-eip-brand`, or `tahoe-living-brand`) for anything in a browser, `ltinfo-platform` plus the site skill for LT Info embeds, and `trpa-dashboard-qa` before any browser tool ships. If the repo has a `.claude/skills/` folder, list those too.

Put personal preferences in `CLAUDE.local.md` and gitignore it. The tracked `CLAUDE.md` is for the team.

Commit as `docs: add handoff docs`. Do not push on init unless asked; the person may want to review the gaps first.

## Pickup

The imports already put HANDOFF.md and CONTEXT.md in context. If you do not see a handoff in context (a Cowork session, a different tool, or the import failed), read both files now.

Then check the docs against reality, because a handoff written on Tuesday can be stale by Thursday:

1. `git status --porcelain` and `git branch --show-current`. Uncommitted files or a branch other than the one HANDOFF.md names are drift.
2. `git log --oneline --since=<HANDOFF last updated date>`. Commits after the handoff date that touch files outside `docs/` are drift; read the diff summary before trusting the next steps.
3. `python scripts/handoff_check.py` from this skill, if Python is available. It runs the file, git, secrets, path, and style checks in one go.
4. Compare the skills CONTEXT.md lists against what is installed (`~/.claude/skills/synced/` and `~/.claude/skills/`). A missing skill is a fix item for the person, not a reason to stop.

Report in this shape, short, then wait:

```
Repo: <name>, branch <branch>, last handoff <date> by <person>
State: two or three lines from HANDOFF.md
Next: the numbered steps from HANDOFF.md
Open questions: from HANDOFF.md, or none
Drift: commits since handoff, uncommitted files, missing skills, or none
Which step do you want to start with?
```

Do not start on step one unprompted. The person may have pulled the repo to do something else.

## Handoff

The goal is that the next person can run the next step without asking you or the previous owner anything.

1. Move what you know into the docs. Anything you learned this session that a coworker would need, including project and reference entries in your own auto memory for this repo, belongs in CONTEXT.md (stable), HANDOFF.md (state), or DECISIONS.md (why). If it is in your memory and not in the docs, it does not travel.
2. Rewrite `docs/HANDOFF.md` from the template. Update the date, the author, the branch, and the handed-to line. Next steps are ordered and specific enough to start cold: name the file, the function, the notebook, or the command. Open questions name who can answer them. The do not list carries anything that looks like a good idea and is not, with a one-line reason or a pointer into DECISIONS.md.
3. Append to `docs/DECISIONS.md` for every choice made this session that someone could reasonably re-litigate. Why, alternatives considered, and when to revisit. One entry per decision, newest first.
4. Edit `docs/CONTEXT.md` only if a stable fact changed: a new data source, a new run command, a new gotcha, a new person.
5. For a data pipeline, add a line to `docs/CHANGELOG.md` if logic changed.
6. Run `python scripts/handoff_check.py` and fix every FAIL. Read the WARN lines and fix the ones that matter. The script checks that the files exist, that CLAUDE.md imports the docs, that HANDOFF.md is dated today or later than the last code commit, that there is nothing uncommitted or unpushed, and that the docs hold no secrets, no machine-specific paths, no leftover placeholders, and no em dashes.
7. If the script is not available, read the docs once for the Style rules below.
8. Commit as `docs: handoff YYYY-MM-DD` and push. If you cannot push, say so in the note; a handoff that is not on the remote is not a handoff.
9. Write the handoff note below for the person to paste into Teams or email.

### Handoff note

```
Handoff: <repo name>
Repo: <url>, branch <branch>, pushed <date>
Where it stands: one sentence
Next step: one sentence, the first item from HANDOFF.md
To pick up: git clone or git pull, open Claude Code in the repo, and say "pick up this repo"
Needs: skills <list from CONTEXT.md>; access <SDE, AGOL, shared drive, or none>
Questions for you: <from HANDOFF.md, or none>
```

Short enough to read on a phone. Everything else is in the repo.

## What stays out of the docs

- Secrets, tokens, connection strings with passwords, and anything from `.env`. Name the variable, never the value.
- Machine-specific absolute paths such as `C:\Users\mbindl\...` or `/Users/mason/...`. Use repo-relative paths, or the standard TRPA paths from `trpa-data-engineering` (the `arcgispro-py3` interpreter path is shared across workstations and is fine).
- Session narration. "Spent an hour debugging the join" is not state. "The jurisdiction join drops rows when the layer is stale; see DECISIONS 2026-10-20" is.
- Anything the code or git history already says. The docs are for what cannot be derived.
- Personal preferences. Those go in `CLAUDE.local.md`.

## Style

TRPA writing rules apply to the docs: no em dashes, Oxford commas, no symbols in body text (write percent, and, to), sentence case headings, acronyms spelled out on first use, plain language. The check script flags dashes and symbols. The full style guide is in `trpa-brand`.

## Reference files

- `assets/CLAUDE.md` is the root file template.
- `assets/docs/CONTEXT.md`, `assets/docs/HANDOFF.md`, and `assets/docs/DECISIONS.md` are the doc templates.
- `scripts/handoff_check.py` is the pre-flight check. Standard library only. Runs under `arcgispro-py3` or any Python 3.9 or later. Usage: `python scripts/handoff_check.py <repo path>`; the path defaults to the current directory. Exit code 1 on any FAIL.
