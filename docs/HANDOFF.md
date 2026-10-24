# Handoff

**Last updated:** 2026-10-23 by Mason Bindl
**Branch:** add-repo-handoff-skill, clean, not yet pushed
**Handed to:** nobody yet

## Where it stands

Twelve skills are live in the marketplace and installed by staff one plugin at a time. This branch adds `trpa-repo-handoff` (the convention these docs follow), lists it in the marketplace and the README, and gives this repo its own `CLAUDE.md` and `docs/` so maintainers start from the current state. The handoff skill's check script was tested against a throwaway repo; its three eval prompts under `skills/trpa-repo-handoff/evals/` have not been run yet and are gitignored.

## Next steps

1. Merge `add-repo-handoff-skill` into `main` and push. Then install it: `/plugin install trpa-repo-handoff@trpa-claude-skills`.
2. Run the three eval prompts in `skills/trpa-repo-handoff/evals/` with skill-creator on a real pipeline repo and tighten SKILL.md from the results.
3. Extend `trpa-dashboard-qa` into a full app verification skill: add a data integrity section (row counts, join cardinality, null rates, totals reconciled to source), a UX section (empty, loading, and error states, navigation, feedback), a security section (innerHTML of API data, SRI on CDN scripts, exposed endpoints, CORS, dependency versions), replace the hardcoded reviewer with a placeholder, and add a runnable check script.
4. Create the "TRPA Skills" Project in claude.ai with project memory on, the repo link, and the maintainer instructions from `README.md`, so new skills get built there with this repo attached.
5. Decide whether `trpa-data-engineering` (currently an account skill, referenced by `trpa-repo-handoff` and `trpa-dashboard-qa`) belongs in this marketplace.

## Open questions

- Should the Claude GitHub App be installed for the trpa-agency org so Claude sessions can push branches here? Mason decides; the install link is in DECISIONS.md.

## Blockers

- Claude sessions cannot push to this repo until the GitHub App is installed for trpa-agency or GitHub is reconnected in claude.ai settings. Work lands as a local branch or a patch until then.

## Do not

- Do not restructure the marketplace into one bundled plugin. Staff already install skills one at a time and the README documents that; see DECISIONS 2026-10-23.
- Do not commit `evals/` folders. They are gitignored on purpose.

## How to pick up

1. `git pull` on branch `main` (or `add-repo-handoff-skill` until it merges).
2. Claude Code 2.1 or later; no Python environment needed beyond standard library Python 3.9 or later for the check script.
3. Open Claude Code in the repo and say "pick up this repo".
