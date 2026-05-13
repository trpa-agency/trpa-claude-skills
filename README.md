# TRPA Claude Skills

A Claude plugin marketplace containing the skills used by Tahoe Regional Planning Agency staff for planning, data access, dashboard development, and brand-consistent design.

## What's in this marketplace

| Plugin | What it does |
|---|---|
| `trpa-brand` | TRPA agency brand — TRPA Blue, color palette, typography, logo usage, writing style |
| `trpa-eip-brand` | Lake Tahoe EIP brand — environmental program palette and styling |
| `tahoe-living-brand` | Tahoe Living housing initiative brand — warm, community-focused identity |
| `trpa-dashboard-stack` | Required tech stack for TRPA dashboards (Plotly + Calcite + ArcGIS SDK + AG Grid) |
| `trpa-data-services` | How to access TRPA's five data systems (ArcGIS Server, AGOL, LTInfo, Accela, GeoServer) |
| `trpa-zoning-services` | Zoning and permissible-use REST endpoints, schemas, and join logic |
| `trpa-climate-dashboard` | Climate Resilience Dashboard framework and patterns |

## For TRPA staff — installing the skills

You need Claude Code or Cowork installed first.

**One-time setup** (add this marketplace to your Claude install):

```
/plugin marketplace add trpa-agency/trpa-claude-skills
```

(Replace `trpa-agency` with the actual GitHub org/user that ends up hosting this repo.)

**Then install whichever plugins you want:**

```
/plugin install trpa-brand
/plugin install trpa-data-services
/plugin install trpa-dashboard-stack
# ...etc
```

Or install everything:

```
/plugin install trpa-brand trpa-eip-brand tahoe-living-brand trpa-dashboard-stack trpa-data-services trpa-zoning-services trpa-climate-dashboard
```

**To check what's installed:** `/plugin list`

**To update:** Claude pulls the latest from this repo automatically. If you want to force-refresh, run `/plugin marketplace update trpa-agency/trpa-claude-skills`.

## For maintainers — adding or updating a skill

1. Create or update the skill folder under `skills/`.
2. Add an entry to `.claude-plugin/marketplace.json` if it's a new skill.
3. Commit and push.
4. Staff get the update on their next install or refresh.

The `name` field inside each skill's `SKILL.md` frontmatter must match the `name` field used in `marketplace.json` for the install to work cleanly.

## Repo layout

```
trpa-claude-skills/
├── .claude-plugin/
│   └── marketplace.json        # the manifest staff install from
├── README.md                   # this file
├── LICENSE
└── skills/
    ├── tahoe-living-brand/
    ├── trpa-brand/
    ├── trpa-climate-dashboard/
    ├── trpa-dashboard-stack/
    ├── trpa-data-services/
    │   ├── SKILL.md
    │   └── references/
    │       ├── arcgis-server-catalog.md
    │       └── ltinfo-tabular-catalog.md
    ├── trpa-eip-brand/
    └── trpa-zoning-services/
```

## License

MIT. See `LICENSE`.

## Questions

Open an issue on this repo or contact the TRPA GIS team.
