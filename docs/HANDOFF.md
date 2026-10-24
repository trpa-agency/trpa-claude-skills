# Handoff

**Last updated:** 2026-10-23 by Mason Bindl with Claude
**Branch:** main
**Handed to:** nobody yet

## Where it stands

Thirteen skills are live in the marketplace. The latest work adds `trpa-pod`, the department pod playbook: a forward deployed engineer, an implementation and project manager, and a QA engineer bring AI tooling to one TRPA department at a time. The skill is the process; the working material lives in `trpa-agency/tools` (branch `mtb-edits`): `pods/README.md` is the playbook source of truth, `pods/_intake-template.md` is the per-engagement intake, `pods/<department>/` folders exist for all eight departments (Legal, Finance, Science and Data, Long Range and Transportation Planning, EIP, Permitting and Compliance, Reporting and Accountability, Communications), and `qa/_template/` is the beta app scaffold on the dashboard stack. See DECISIONS 2026-10-23 for why the split goes that way.

Earlier today `trpa-repo-handoff` landed with this repo's own CLAUDE.md and docs; its eval prompts under `skills/trpa-repo-handoff/evals/` have still not been run.

## Next steps

1. Install the new skill on each machine: `/plugin install trpa-pod@trpa-claude-skills`, then `/plugin marketplace update trpa-claude-skills`.
2. Merge `mtb-edits` to `main` in `trpa-agency/tools` so the pods folders and `qa/_template/` are live.
3. First real pod engagement with a proper intake doc. Leading candidates per the playbook: Long Range and Transportation Planning (TRIP is live) or Reporting and Accountability (fall reporting season).
4. Run the three eval prompts in `skills/trpa-repo-handoff/evals/` with skill-creator on a real pipeline repo and tighten SKILL.md from the results.
5. Extend `trpa-dashboard-qa` into a full app verification skill (data integrity, UX states, security section, placeholder reviewer, runnable check script).
6. Create the "TRPA Skills" Project in claude.ai with project memory on, the repo link, and the maintainer instructions from `README.md`.
7. Decide whether `trpa-data-engineering` (currently an account skill) belongs in this marketplace.

## Open questions

- The Claude GitHub App was installed for trpa-agency on 2026-10-23, but a cloud session still got a 403 on push afterward. Check the app's repository access list includes this repo, then try a fresh session.

## Blockers

- Cloud Claude sessions could not push here as of 2026-10-23; commits get applied and pushed from Mason's machine through the desktop app instead.

## Do not

- Do not restructure the marketplace into one bundled plugin. Staff already install skills one at a time; see DECISIONS 2026-10-23.
- Do not commit `evals/` folders. They are gitignored on purpose.
- Do not let `trpa-pod` and `tools/pods/README.md` drift apart. The repo playbook wins; update the skill to match.

## How to pick up

1. `git pull` on branch `main`.
2. Claude Code 2.1 or later; standard library Python 3.9 or later for the check script.
3. Open Claude Code in the repo and say "pick up this repo".
