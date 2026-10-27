# Handoff

**Last updated:** 2026-10-26 by Mason Bindl with Claude
**Branch:** main
**Handed to:** nobody yet

## Where it stands

Fourteen skills are live in the marketplace. Today's work extends `trpa-monitoring-dashboard` for the LT Info Monitoring prototypes built in `trpa-agency/Monitoring`, folder `ltinfo/`: the fragment form for inline rendering in ESA's framework, the four templates and the review frame in `assets/templates/`, the Arcade story and chart popups in `assets/popups/`, section by section guidance in `references/sections.md`, the map and popup rules, the LTInfo_Monitoring data table, pointers to the kit and to design system section 19, and a new checklist. The marketplace description and the README row match. See DECISIONS 2026-10-26 for why the templates are copied but the kit is not.

`ltinfo-platform` got a one-line fix in its height snippet: it now posts `document.body.scrollHeight`, because `document.documentElement.scrollHeight` never reports less than the frame and a frame sized from it could grow but never shrink.

The 2026-10-23 work stands: `trpa-pod` and `trpa-repo-handoff` are live; the repo-handoff eval prompts have still not been run.

## Next steps

1. Update installs on each machine: `/plugin marketplace update trpa-claude-skills`. Upload `dist/trpa-monitoring-dashboard.zip` to claude.ai and Cowork, which do not auto update; it was rebuilt today with its assets and references. Rebuild and upload `dist/ltinfo-platform.zip` too, for the height fix.
2. Merge `MTB-Edits` in `trpa-agency/Monitoring` and `mtb-edits` in `trpa-agency/tools`. The skill's template copies load the kit from `https://trpa-agency.github.io/Monitoring/ltinfo/kit/`, which does not exist until that merge deploys; until then a template copied out of the skill renders unstyled and does not mount.
3. Fix the stale design system links: the page moved from `qa/general/` to `qa/data/` in the tools repo, but `trpa-brand`, `trpa-eip-brand`, `tahoe-living-brand`, `trpa-dashboard-stack`, and the README still link `qa/general/design-system.html`. The README also has five em dashes in its skill table and two headings.
4. Install `trpa-pod` on each machine if not done: `/plugin install trpa-pod@trpa-claude-skills`. Merge `mtb-edits` in the tools repo so the pods folders and `qa/_template/` are live.
5. First real pod engagement with a proper intake doc. Leading candidates per the playbook: Long Range and Transportation Planning (TRIP is live) or Reporting and Accountability (fall reporting season).
6. Run the three eval prompts in `skills/trpa-repo-handoff/evals/` with skill-creator on a real pipeline repo and tighten SKILL.md from the results.
7. Extend `trpa-dashboard-qa` into a full app verification skill (data integrity, UX states, security section, placeholder reviewer, runnable check script).
8. Create the "TRPA Skills" Project in claude.ai with project memory on, the repo link, and the maintainer instructions from `README.md`.
9. Decide whether `trpa-data-engineering` (currently an account skill) belongs in this marketplace.

## Open questions

- `trpa-monitoring-dashboard` has not been run through skill-creator test prompts after today's rewrite. Good prompts: "build the Streams program dashboard from the template", "add a highway noise section to the noise page", "write an Arcade popup for the noise sites".
- The Claude GitHub App was installed for trpa-agency on 2026-10-23, but a cloud session still got a 403 on push afterward. Check the app's repository access list includes this repo, then try a fresh session.
- `claude plugin validate ./skills/<skill>` fails by design (no per-plugin manifest); `claude plugin validate .` is the check. It warns that the marketplace's top-level `url` field is ignored, which is harmless.

## Blockers

- Cloud Claude sessions could not push here as of 2026-10-23; commits get applied and pushed from Mason's machine through the desktop app instead.

## Do not

- Do not restructure the marketplace into one bundled plugin. Staff already install skills one at a time; see DECISIONS 2026-10-23.
- Do not commit `evals/` folders. They are gitignored on purpose.
- Do not let `trpa-pod` and `tools/pods/README.md` drift apart. The repo playbook wins; update the skill to match.
- Do not edit the templates in `skills/trpa-monitoring-dashboard/assets/` first. Change `trpa-agency/Monitoring/ltinfo/templates/`, verify there, then recopy.

## How to pick up

1. `git pull` on branch `main`.
2. Claude Code 2.1 or later; standard library Python 3.9 or later for the check script.
3. Open Claude Code in the repo and say "pick up this repo".
