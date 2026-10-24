# Handoff

**Last updated:** 2026-10-23 by Mason Bindl
**Branch:** main, clean and pushed
**Handed to:** nobody yet

## Where it stands

Twelve skills are live in the marketplace and installed by staff one plugin at a time. The latest commit adds `trpa-repo-handoff` (the convention these docs follow), lists it in the marketplace and the README, and gives this repo its own `CLAUDE.md` and `docs/` so maintainers start from the current state. The handoff skill's check script was tested against a throwaway repo; its three eval prompts under `skills/trpa-repo-handoff/evals/` have not been run yet and are gitignored.

## Next steps

1. Install the new skill: `/plugin install trpa-repo-handoff@trpa-claude-skills`, then `/plugin marketplace update trpa-claude-skills` on each machine.
2. Run the three eval prompts in `skills/trpa-repo-handoff/evals/` with skill-creator on a real pipeline repo and tighten SKILL.md from the results.
3. Extend `trpa-dashboard-qa` into a full app verification skill: add a data integrity section (row counts, join cardinality, null rates, totals reconciled to source), a UX section (empty, loading, and error states, navigation, feedback), a security section (innerHTML of API data, SRI on CDN scripts, exposed endpoints, CORS, dependency versions), replace the hardcoded reviewer with a placeholder, and add a runnable check script.
4. Create the "TRPA Skills" Project in claude.ai with project memory on, the repo link, and the maintainer instructions from `README.md`, so new skills get built there with this repo attached.
5. Decide whether `trpa-data-engineering` (currently an account skill, referenced by `trpa-repo-handoff` and `trpa-dashboard-qa`) belongs in this marketplace.

## Open questions

- The Claude GitHub App was installed for trpa-agency on 2026-10-23, but a cloud session still got a 403 on push afterward. Check the app's repository access list includes this repo, then try a fresh session.

## Blockers

- Cloud Claude sessions could not push here as of 2026-10-23 even after the GitHub App install; this commit was applied and pushed from Mason's machine through the desktop app instead.

## Do not

- Do not restructure the marketplace into one bundled plugin. Staff already install skills one at a time and the README documents that; see DECISIONS 2026-10-23.
- Do not commit `evals/` folders. They are gitignored on purpose.

## How to pick up

1. `git pull` on branch `main`.
2. Claude Code 2.1 or later; no Python environment needed beyond standard library Python 3.9 or later for the check script.
3. Open Claude Code in the repo and say "pick up this repo".
