# Handoff

**Last updated:** 2026-10-28 by Mason Bindl with Claude
**Branch:** main
**Handed to:** nobody yet

## Where it stands

Fifteen skills are in the marketplace. Today adds `trpa-storymap-to-webpage`, which rebuilds an ArcGIS StoryMap (story, collection, or briefing) as a single-file TRPA web page on GitHub Pages. It was built in the PROTECT repo, where it produced the Connecting Tahoe home page, and tested end to end once by a fresh agent on the greenhouse gas emissions story. That test's gaps are fixed in this version: map sidecars that mix web maps, photos, and swipes (including swipes across two web maps) with a legend, a prose and chart block, per-layer health checks in the extractor, stat units, phone map spacing, a link checker, and an undersized image warning. The extractor runs clean on all 38 public TRPA story maps. The marketplace entry, the README row, layout entry, and install-all line are in; the install-all line also gained the missing `trpa-pod`. `dist/trpa-storymap-to-webpage.zip` is built locally for claude.ai upload.

The 2026-10-26 work stands: `trpa-monitoring-dashboard` carries the LT Info fragment form, templates, popups, and section guidance, and `ltinfo-platform` posts `document.body.scrollHeight` for frame height.

## Next steps

1. Push the two commits from 2026-10-28 to `main`.
2. Install the new skill on each machine: `/plugin marketplace update trpa-claude-skills`, then `/plugin install trpa-storymap-to-webpage@trpa-claude-skills`. Upload `dist/trpa-storymap-to-webpage.zip` to claude.ai and Cowork; an earlier upload of the draft never saved to the profile.
3. Run a second end-to-end test of `trpa-storymap-to-webpage` against the fixed version, ideally on "Lake Tahoe Shoreline Public Safety Facilities" (14 web maps, timelines, a slideshow). Then delete the pre-repo draft in Mason's local `Documents\GitHub\skills\` folder so only this copy remains.
4. Update installs from the 2026-10-26 work: upload `dist/trpa-monitoring-dashboard.zip` and a rebuilt `dist/ltinfo-platform.zip` to claude.ai and Cowork, which do not auto update.
5. Merge `MTB-Edits` in `trpa-agency/Monitoring` and `mtb-edits` in `trpa-agency/tools`. The monitoring skill's template copies load the kit from `https://trpa-agency.github.io/Monitoring/ltinfo/kit/`, which does not exist until that merge deploys.
6. Fix the stale design system links: the page moved from `qa/general/` to `qa/data/` in the tools repo, but `trpa-brand`, `trpa-eip-brand`, `tahoe-living-brand`, `trpa-dashboard-stack`, and the README still link `qa/general/design-system.html`. The README also has five em dashes in its skill table and two headings.
7. Install `trpa-pod` on each machine if not done, and merge `mtb-edits` in the tools repo so the pods folders and `qa/_template/` are live.
8. First real pod engagement with a proper intake doc: Long Range and Transportation Planning (TRIP is live) or Reporting and Accountability (fall reporting season).
9. Run the three eval prompts in `skills/trpa-repo-handoff/evals/` with skill-creator on a real pipeline repo.
10. Extend `trpa-dashboard-qa` into a full app verification skill (data integrity, UX states, security section, placeholder reviewer, runnable check script).
11. Create the "TRPA Skills" Project in claude.ai with project memory on, the repo link, and the maintainer instructions from `README.md`.
12. Decide whether `trpa-data-engineering` (currently an account skill) belongs in this marketplace.

## Open questions

- The story map extractor found 29 web map layers that will not load across 11 of TRPA's 38 public story maps, so those stories already show gaps. Nine are on `maps.trpa.org/server/rest/services/LTW_Base_Data/MapServer`, which was removed or renamed. Who repoints or retires those web maps? `maps.trpa.org` answers "Token Required" even for services that do not exist, so the layer URL ("Service not found") is the reliable check.
- `trpa-monitoring-dashboard` has not been run through skill-creator test prompts after the 2026-10-26 rewrite. Good prompts: "build the Streams program dashboard from the template", "add a highway noise section to the noise page", "write an Arcade popup for the noise sites".
- The Claude GitHub App was installed for trpa-agency on 2026-10-23, but a cloud session still got a 403 on push afterward. Check the app's repository access list includes this repo, then try a fresh session.
- `claude plugin validate ./skills/<skill>` fails by design (no per-plugin manifest); `claude plugin validate .` is the check. It warns that the marketplace's top-level `url` field is ignored, which is harmless.

## Blockers

- Cloud Claude sessions could not push here as of 2026-10-23; commits get applied and pushed from Mason's machine through the desktop app instead.

## Do not

- Do not restructure the marketplace into one bundled plugin. Staff already install skills one at a time; see DECISIONS 2026-10-23.
- Do not commit `evals/` folders. They are gitignored on purpose.
- Do not let `trpa-pod` and `tools/pods/README.md` drift apart. The repo playbook wins; update the skill to match.
- Do not edit the templates in `skills/trpa-monitoring-dashboard/assets/` first. Change `trpa-agency/Monitoring/ltinfo/templates/`, verify there, then recopy.
- Do not point the `trpa-storymap-to-webpage` template's example web maps at a map with a dead layer. The extractor's layer check tells you before you do.

## How to pick up

1. `git pull` on branch `main`.
2. Claude Code 2.1 or later; standard library Python 3.9 or later for the check script.
3. Open Claude Code in the repo and say "pick up this repo".
