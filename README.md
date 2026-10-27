# TRPA Claude Skills

A Claude plugin marketplace containing the skills used by Tahoe Regional Planning Agency staff for planning, data access, dashboard development, and brand-consistent design.

## What's in this marketplace

| Plugin | What it does |
|---|---|
| `trpa-brand` | TRPA agency brand — TRPA Blue, color palette, typography, logo usage, writing style |
| `trpa-eip-brand` | Lake Tahoe EIP brand — environmental program palette and styling |
| `tahoe-living-brand` | Tahoe Living housing initiative brand — warm, community-focused identity |
| `trpa-dashboard-stack` | Required tech stack for TRPA dashboards (Plotly + Calcite + ArcGIS SDK + AG Grid) |
| `trpa-dashboard-qa` | Pre-deploy QA checklist for dashboards and web tools |
| `trpa-repo-handoff` | How we hand off repo work between people: root CLAUDE.md plus docs/CONTEXT.md, HANDOFF.md, and DECISIONS.md, with a pre-flight check script |
| `trpa-data-services` | How to access TRPA's five data systems (ArcGIS Server, AGOL, LTInfo, Accela, GeoServer) |
| `trpa-zoning-services` | Zoning and permissible-use REST endpoints, schemas, and join logic |
| `ltinfo-platform` | Lake Tahoe Info platform: shared shell, design tokens, embed contract, API conventions. Load with any LT Info dashboard skill |
| `trpa-threshold-dashboard` | Threshold Dashboard: categories, indicators, evaluation vocabulary, indicator page fields, ThresholdEvaluation repo conventions |
| `trpa-monitoring-dashboard` | Monitoring Dashboard: the LT Info fragment form, four templates and Arcade popups, section guidance, map and popup rules, the LTInfo_Monitoring data table, program types, Forest Health reference dashboards |
| `trpa-transportation-tracker` | Transportation Tracker: strategies and colors, projects and funding routes, Data Trend embeds, data repos |
| `trpa-climate-dashboard` | Climate Resilience Dashboard framework and patterns |
| `trpa-pod` | Department pod playbook, one department at a time: intake, scoping, the beta app template, and the graduate-or-archive rule |

## Design system

The brand and stack skills are the machine-readable half of the TRPA Design System. The human half, with live specimens of every component and a brand switcher, is at https://tools.trpa.gov/qa/general/design-system.html (https://trpa-agency.github.io/tools/qa/general/design-system.html until the tools.trpa.gov DNS is live; the link drops `qa/` when the page is promoted out of beta). The shared token stylesheet those skills point to lives in the `trpa-agency/tools` repo at `assets/trpa-tokens.css`. When a rule changes, change it in both places.

## Lake Tahoe Info dashboards

Four skills cover the laketahoeinfo.org dashboards TRPA feeds with embedded charts, maps, and dashboards: `ltinfo-platform` holds what the sites share (shell, tokens sampled from the live site, the embed contract, the anonymous `internalapi.laketahoeinfo.org` conventions), and `trpa-threshold-dashboard`, `trpa-monitoring-dashboard`, `trpa-transportation-tracker`, and `trpa-climate-dashboard` hold each site's framework, page anatomy, API routes, and file conventions. Always load `ltinfo-platform` with a dashboard skill. LT Info embeds use the platform's own styling, not the TRPA, EIP, or Tahoe Living brands.

## Without Claude Code

Cowork and claude.ai take a skill as an uploaded folder. Use **Code → Download ZIP** on this repo, unzip it, and upload the folder for the skill you want (for example `skills/trpa-brand`) through the Skills settings. You will not get automatic updates that way, so check back when the design system page changes.

## For TRPA staff — installing the skills

You need Claude Code or Cowork installed first.

**One-time setup** (add this marketplace to your Claude install):

```
/plugin marketplace add trpa-agency/trpa-claude-skills
```

**Then install whichever plugins you want:**

```
/plugin install trpa-brand@trpa-claude-skills
/plugin install trpa-dashboard-stack@trpa-claude-skills
/plugin install trpa-data-services@trpa-claude-skills
# ...etc
```

Or install everything:

```
/plugin install trpa-brand@trpa-claude-skills trpa-eip-brand@trpa-claude-skills tahoe-living-brand@trpa-claude-skills trpa-dashboard-stack@trpa-claude-skills trpa-dashboard-qa@trpa-claude-skills trpa-repo-handoff@trpa-claude-skills trpa-data-services@trpa-claude-skills trpa-zoning-services@trpa-claude-skills trpa-climate-dashboard@trpa-claude-skills ltinfo-platform@trpa-claude-skills trpa-threshold-dashboard@trpa-claude-skills trpa-monitoring-dashboard@trpa-claude-skills trpa-transportation-tracker@trpa-claude-skills
```

**To check what's installed:** `/plugin list`

**To update:** Claude pulls the latest from this repo automatically. If you want to force-refresh, run `/plugin marketplace update trpa-claude-skills`.

## For maintainers — adding or updating a skill

1. Open Claude Code in this repo. The root `CLAUDE.md` loads `docs/HANDOFF.md` and `docs/CONTEXT.md`, so you start with the current state of skill work.
2. Create or update the skill folder under `skills/`. Build new skills with the `skill-creator` skill.
3. Add an entry to `.claude-plugin/marketplace.json` if it's a new skill, and a row to the table above.
4. Run `claude plugin validate .` from the repo root.
5. Before you stop, update `docs/HANDOFF.md` (the `trpa-repo-handoff` skill does this and runs `skills/trpa-repo-handoff/scripts/handoff_check.py`), commit, and push.
6. Staff get the update on their next install or refresh.

The `name` field inside each skill's `SKILL.md` frontmatter must match the `name` field used in `marketplace.json` for the install to work cleanly. Evals under `skills/*/evals/` are gitignored on purpose; skills are the deliverable.

## Repo layout

```
trpa-claude-skills/
├── .claude-plugin/
│   └── marketplace.json        # the manifest staff install from
├── CLAUDE.md                   # loads docs/HANDOFF.md and docs/CONTEXT.md for maintainers
├── docs/
│   ├── CONTEXT.md              # what this repo is and how skills get made and released
│   ├── HANDOFF.md              # current state of skill work, rewritten at every handoff
│   └── DECISIONS.md            # why the repo and the skills are shaped the way they are
├── README.md                   # this file
├── LICENSE
└── skills/
    ├── tahoe-living-brand/
    ├── trpa-brand/
    ├── ltinfo-platform/
    ├── trpa-climate-dashboard/
    ├── trpa-dashboard-qa/
    ├── trpa-dashboard-stack/
    ├── trpa-data-services/
    │   ├── SKILL.md
    │   └── references/
    │       ├── arcgis-server-catalog.md
    │       └── ltinfo-tabular-catalog.md
    ├── trpa-eip-brand/
    ├── trpa-monitoring-dashboard/
    ├── trpa-repo-handoff/
    │   ├── SKILL.md
    │   ├── assets/             # CLAUDE.md and docs templates
    │   └── scripts/
    │       └── handoff_check.py
    ├── trpa-threshold-dashboard/
    ├── trpa-transportation-tracker/
    └── trpa-zoning-services/
```

## License

MIT. See `LICENSE`.

## Questions

Open an issue on this repo or contact the TRPA GIS team.
