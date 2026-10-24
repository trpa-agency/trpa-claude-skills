# Context

**Owner:** mason.bindl@trpa.gov
**Repo type:** skills
**Last reviewed:** 2026-10-23

## Purpose

This repo is the source of truth for the Claude skills TRPA staff use: brands, the dashboard stack, data services, the Lake Tahoe Info dashboards, QA, and repo handoff. It is a Claude Code plugin marketplace, so staff add it once and install the plugins they want. The brand and stack skills are the machine-readable half of the TRPA Design System; the human half lives in the `trpa-agency/tools` repo and at tools.trpa.gov.

## Run it

Nothing runs. To release a change: edit the skill, run `claude plugin validate .` from the repo root, commit, and push to `main`. Staff pick it up with `/plugin marketplace update trpa-claude-skills`. To try a skill locally without installing, run `claude --plugin-dir ./skills/<skill>` and `/reload-plugins` after edits. The handoff pre-flight is `python skills/trpa-repo-handoff/scripts/handoff_check.py .` and needs only standard library Python 3.9 or later.

## Layout

One plugin per folder under `skills/`, each with `SKILL.md` at its root and optional `references/`, `assets/`, `scripts/`, and `logos/`. `.claude-plugin/marketplace.json` lists every plugin with its folder as the source; there are no per-plugin `plugin.json` files. `skills/*/evals/`, `*-workspace/`, and `dist/` are gitignored: evals and iteration output stay local, and `dist/` holds per-skill zips for manual upload to claude.ai.

## Data and services

| Source or destination | Type | Where | Notes |
|---|---|---|---|
| Design system page | Web page | tools.trpa.gov/qa/general/design-system.html | GitHub Pages at trpa-agency.github.io/tools until DNS is live; the path drops qa/ when promoted |
| Token stylesheet | CSS | trpa-agency/tools, assets/trpa-tokens.css | When a brand rule changes, change it here and in the brand skill |
| Marketplace consumers | Claude Code, Cowork, claude.ai | Staff machines | claude.ai and Cowork take the skill folder as an upload, no auto update |

## Conventions and skills

Every skill is built or revised with `skill-creator`: short interview, draft, two or three test prompts, then polish. SKILL.md follows the TRPA writing rules from `trpa-brand`: no em dashes, Oxford commas, no symbols in body text, sentence case headings. Descriptions are the trigger, so they name the phrases staff actually say and stay under the 1,024 character limit claude.ai enforces. Anything longer than a screen goes in `references/`; templates go in `assets/`; scripts are standard library Python that runs under `arcgispro-py3`.

## Gotchas

- Skill descriptions over 1,024 characters fail to upload to claude.ai; two were shortened on 2026-10-13.
- The skill `name` in SKILL.md must equal the marketplace entry `name` or the install fails.
- Design system links moved twice in October 2026 (apps.trpa.gov, then tools.trpa.gov); check the README and the brand skills together when the domain changes again.
- Cowork and claude.ai users get no automatic updates; tell them when a skill changes.

## People

- Mason Bindl, Senior GIS Analyst, owns the framework and every skill until a skill names another owner.
- Jeanne, LT Info product manager, for anything the LT Info skills say about the vendor platform.
