---
name: trpa-monitoring-dashboard
description: "Lake Tahoe Info Monitoring Dashboard (monitoring.laketahoeinfo.org) reference. Use this skill when building or updating a dashboard that embeds in the Dashboard card of a Monitoring Program page (Forest Health programs such as Subalpine Conifer, Forest Structure, and Fire Dynamics, Tahoe Yellow Cress, Streams, Air Quality, Bicycle and Pedestrian, Congestion, Transit, or any program under Air Quality, Noise, Transportation, Vegetation Preservation, Water Quality, Soil Conservation, or Fisheries), when reading program, site, or partner data from the LT Info API, or when drafting a program description. Covers the program types and categories, the page anatomy by type, the Dashboard card embed contract (a URL plus optional height and width), host styling, the anonymous internalapi routes, the Forest Health reference implementations, data patterns from maps.trpa.org, and stack gotchas. Trigger on: monitoring dashboard, monitoring program page, monitoring.laketahoeinfo.org, Dashboard card, program embed, monitoring sites, subalpine conifer dashboard, forest structure dashboard, fire dynamics dashboard, LT Info monitoring, monitoring program category."
---

# Monitoring Dashboard

Reference for [monitoring.laketahoeinfo.org](https://monitoring.laketahoeinfo.org/), the inventory of monitoring programs in the Tahoe Region: what is monitored, how, where, by whom, and the record so far. Featured programs carry sites, data, and photos. Programs of type Program With Dashboard carry an embedded dashboard that TRPA builds.

**Always pair with** `ltinfo-platform` for the shell, tokens, embed contract, and stack facts, `trpa-dashboard-stack` for libraries, and `forest-health-domain` for Forest Health vocabulary. Run `trpa-dashboard-qa` before pointing the CMS at a new URL. Sampled Oct. 13, 2026; first built from the Subalpine Conifer embed on Sept. 17, 2026.

---

## Two products, not one

TRPA builds two kinds of LT Info file. Decide which before writing anything.

| | Threshold element | Monitoring dashboard |
|---|---|---|
| Host | Status panel or Evaluation Map on `thresholds.laketahoeinfo.org` | Dashboard card on a Monitoring Program page |
| What we build | One chart or one map per file. The CMS supplies narrative, status, and structure. | One complete dashboard per program in one file. The card supplies only its header and a Fullscreen control. |
| Question it answers | Is the Region meeting the standard? | What is monitored, how, where, and what does the record show? |
| Numbers | Attainment against a target | Observed measurements, extents, counts, change over time |
| Tone | Evaluative, set by the CMS copy around it | Descriptive |

A monitoring dashboard may link to its threshold indicator in the footer. It does not repeat a status badge or target comparison. See `trpa-threshold-dashboard` for the other product.

---

## Programs, types, and categories

77 programs. Seven categories carry the 18 featured programs; the other 55 are uncategorized "Other Monitoring Programs" tracked for partners, related indicators, and documents only.

| Category | Featured programs (ID) |
|---|---|
| Air Quality | Air Quality (67) |
| Noise | Noise - Highways (65), Noise - Plan Areas (61), Noise - Shorezone (62) |
| Transportation | Bicycle and Pedestrian (33), Congestion-Travel Time (77), Safety (34), Socio-Economic (68), Traffic Volumes (64), Transit (36), Travel Behavior (69) |
| Vegetation Preservation | Tahoe Yellow Cress (39); Subalpine Conifer (83) is categorized but not featured |
| Water Quality | HAB Monitoring (82), Nearshore Human Health (76), Pelagic Water Quality (Clarity) (66), Periphyton (13), Regional Stormwater (16), Streams (63) |

Program types, with counts:

| Type ID | Type | Count | Page shape |
|---|---|---|---|
| 1 | Simple Program with no Backing Data | 58 | overview, images, partners, documents, indicators |
| 3 | Many Monitoring Sites but only One Monitoring Station per Site | 10 | adds a Monitoring Sites card: grid plus Leaflet map, site attributes |
| 2 | One Monitoring Site and One Monitoring Station Only | 1 | same with one site |
| 4 | Many Monitoring Sites and Many Monitoring Stations per Site | 1 | same with stations under sites |
| 6 | Program With Dashboard | 5 | adds a Dashboard card holding an iframe |
| 7 | Congestion | 1 | custom: 13 segments, median travel time |
| 8 | Safety | 1 | custom |

Programs with dashboards: 75 "bike ped test" (Shiny app at `trpa-shiny-apps.shinyapps.io/bike_ped_dashboard/`), 68 Socio-Economic (Tahoe Open Data demographics page), 76 Nearshore Human Health, 83 Subalpine Conifer, and 69 Travel Behavior (the last three have no URL set yet).

---

## Page anatomy

Above the cards: breadcrumb (MONITORING PROGRAMS, then the program name, green `#789440` with the active segment in `#616049`), the program name as an uppercase `#3e72b0` title, and the one-paragraph description. Then cards in this order, each with a green `#789440` header:

1. **Program Overview**: Program Name, Monitoring Program Category, Monitoring Approach.
2. **Images**: key photo with caption and a download link.
3. **Dashboard** (type 6 only): the iframe. Shows "No dashboard configured for this program." until a URL is set.
4. **Monitoring Sites** (site types only): AG Grid of sites with Status, Total Records, and a Leaflet map with the standard overlays.
5. **Partners**.
6. **Documents**: uploaded files with date, type, description.
7. **Associated Indicators**: links to threshold indicators.

### The Dashboard card contract, from the API

The program record's `Dashboard` object is what the admin sets:

```json
"Dashboard": { "MonitoringProgramDashboardID": 6, "DashboardUrl": "https://...", "DashboardDescription": "...",
               "DashboardHeight": null, "DashboardWidth": null, "FileResourceInfoID": null, "FileResourceGUID": null }
```

The page renders `<iframe class="dashboard-frame" allowfullscreen title="Monitoring Program Dashboard" src="{DashboardUrl}">` at the card body width (about 980 px at desktop), with a Fullscreen action in the card header. Height and width are optional overrides; a file resource can stand in for a URL. The LT Info admin sets these fields; TRPA supplies the URL. Until a height is set, the embed should post its height (see `ltinfo-platform`) and look right at the default.

---

## What the embed must do

- **No chrome.** No logo row, no page title, no footer nav. The card header says DASHBOARD and the program name sits above it.
- **Background `#f7f7f7`**, the card body color, so the embed reads as part of the card. White cards inside it with `#efefef` borders at 4px.
- **Host styling, not EIP brand.** Mason, Oct. 4, 2026: "make sure these use the same styling that monitoring.laketahoeinfo.org uses." Lexend Deca; card label bars like `h3.popover-header` (`#efefef`, `#3d3d3d`, 16.5px 600); section labels `#789440` uppercase 14px; links `#337ab7`; Calcite brand `#789440` through `--calcite-color-brand`; AG Grid Quartz at the host's 14px cells and `#fafafa` striping but with the `#efefef` label-bar header (the host's `#666` header looked odd inside a white card). Plotly font Lexend Deca, ink `#333333`, grid `#dcdcdc`. Data colors from the host variables: ordered hazard `#3e72b0`, `#e49937`, `#be4c4c`; seral classes `#e49937`, `#89cad7`, `#2c5f72`, `#89bf40`, `#0b5d0a`; forest types `#e49937`, `#3e72b0`, `#be4c4c`.
- **Fluid width.** About 980 px, checked at 375 px, no horizontal scroll.
- **Own its height, stop wheel zoom on maps, table and CSV behind every chart, explicit empty states**, per the platform contract.

Section pattern, top to bottom, that works:

1. At a glance: five or six stat tiles, pending tiles grayed for data not yet loaded
2. Extent map with a layer toggle
3. Composition and structure charts, each with a Chart / Table toggle and CSV download
4. "How it is measured" definition grid
5. Program-specific measurement sections, empty-state until data exists
6. Footer: about the program, links to the threshold indicator, StoryMap, and report, data vintage

---

## API routes

Base `https://internalapi.laketahoeinfo.org`, anonymous GET.

| Route | Returns |
|---|---|
| `/monitoring-programs` | 77 programs: ID, name, short name, type, category, `IsFeaturedProgram`, `NumberOfSites`, key photo GUID |
| `/monitoring-programs/featured` | the five categories with their featured programs |
| `/monitoring-programs/{id}` | the program record: `MonitoringApproach`, `MonitoringProgramDescription`, `VanityUrl`, `OrganizationRelationshipLabel`, `SiteLabel`, type and category, `Dashboard`, `HasExternalDataSources` |
| `/monitoring-programs/{id}/sites?activeOnly=false`, `/site-attributes`, `/sites-as-feature-collection` | sites as rows, attribute definitions, and GeoJSON points |
| `/monitoring-programs/{id}/images`, `/documents`, `/partners`, `/indicators` | the remaining cards |
| `/custom-rich-texts/89` | the Other Monitoring Programs text |

Observed data behind the site types (counts, samples) is not exposed on anonymous routes that the pages reveal; the transit and bike data routes on the old WebServices host are dead.

---

## Forest Health reference implementations

Files live in the program's analysis repo under `monitoring/` and publish through GitHub Pages at `https://trpa-agency.github.io/<Repo>/monitoring/<program-slug>.html`.

| Program | LT Info program | File | Built |
|---|---|---|---|
| Subalpine Conifer | 83 | `ForestHealth/monitoring/subalpine-conifer.html` | Sept. 17, 2026 |
| Forest Structure | no program yet | `ForestHealth/monitoring/forest-structure.html` | Oct. 2, 2026 |
| Fire Dynamics | no program yet | `ForestHealth/monitoring/fire-dynamics.html` | Oct. 2, 2026 |

`ForestHealth/monitoring/index.html` is a card index linking the three, a standalone entry page with a header, not an embed. The old `ForestHealth/monitoring/index.html` threshold-status dashboard moved to `archive/` and is not a pattern. As of Oct. 13, 2026 program 83's Dashboard card is still unset and the host has no program pages for Forest Structure or Fire Dynamics; ask the LT Info admin to create them.

Two data patterns, settled Oct. 2, 2026:

- **Analysis outputs as data of record.** When the numbers come from the repo's analysis (Forest Structure), fetch `../output/*.csv` relative to the page and embed the same rows as a `SNAPSHOT` fallback, so page and data move together by branch.
- **Live service where the service is current.** Fire Dynamics queries `Fire/MapServer/3` (severity by management zone) and `Fire/MapServer/6` (CAL FIRE perimeters, envelope-filtered to the Basin) at load.

Do not query `Vegetation/FeatureServer` layers 3 (Composition) or 4 (Stand Density Classified) for numbers: as of Oct. 2, 2026 they carry the superseded run (transposed canopy classes, 177,540-acre frame). Use the `Forest_Health_*` tile services for display only, captioned as the 2023 assessment as published.

Plot data for Subalpine Conifer: where it will live (SDE feature class, hosted feature service, or repo CSV) and the field names are still open. The page documents the shape it expects in its `DATA.plots` and `DATA.health` comments.

---

## Data patterns from maps.trpa.org

ArcGIS Server on `maps.trpa.org` answers cross-origin `query` requests, so a page can pull summary statistics at load and fall back to an embedded snapshot:

```javascript
const params = new URLSearchParams({
  where: "WHRTYPE = 'SCN'", groupByFieldsForStatistics: 'REGIONAL_DOMINANCE_TYPE_1',
  returnGeometry: 'false', f: 'json',
  outStatistics: JSON.stringify([{ statisticType: 'sum', onStatisticField: 'Acres', outStatisticFieldName: 'acres' }]),
});
const json = await (await fetch(`${service}/${layer}/query?${params}`)).json();
```

Keep a `SNAPSHOT` with the same shape and the capture date, and say on the page which is showing. From the office network these fetches fail on CORS; JSONP with `callback=` is the fallback.

| Service | What it holds |
|---|---|
| `Vegetation_Type/MapServer/0` | EVeg polygons: `WHRTYPE`, `TRPA_VegType`, `REGIONAL_DOMINANCE_TYPE_1`, `WHRSIZE`, `WHRDENSITY`, `Ownership`, `Elev_Ft`, `Acres`. 694,422 polygons; dynamic layers supported |
| `Vegetation/FeatureServer` | Composition (3), Stand Density Classified (4), USFS Sensitive Plants, Tree Mortality ADS 2023 |
| `Forest_Health_Stand_Density`, `Forest_Health_Composition_Age` | map services behind the threshold web maps |

Public web maps (ArcGIS Online item IDs): stand density `24fc43584a354f789f283df388bf723d`, seral stage `07d6ccd3c6f94425be295b9a6db043aa`, fire severity `35dc3ddb4ff546d2a169f6fdeb945320`, fuels treatments `0303bdff0aa04b628f8a60a8c72c53a1`.

---

## Stack gotchas confirmed on this site

- **Script order.** Plotly and AG Grid before the ArcGIS SDK, or they register as AMD modules and the globals stay undefined.
- **Calcite version must match the ArcGIS SDK release.** SDK widgets render through Calcite components, and whichever definitions register first win. With SDK 4.31 load `2.13.2` (`calcite.esm.js` plus `calcite.css`); 3.3.0 against 4.31 left the Expand popover unpositioned. The `5.0` path serves a different build with no `calcite.css`, so do not mix it with SDK pages.
- **Plotly font.** Set `font.family` to Lexend Deca in every layout.
- **Plotly legends and labels are not responsive.** Render the legend as HTML with `showlegend: false`, set `uniformtext: { minsize: 9, mode: 'hide' }`, `xaxis.automargin: true`, wrap long category labels with `<br>` under 640 px, and redraw on a debounced resize. A plot div inside a card with side margins must be `width: auto`, not `100%`.
- **Editing from PowerShell 5.1.** `Get-Content` reads BOM-less UTF-8 as ANSI and double-encodes dashes on write. Use `[IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)` and `WriteAllText` with a BOM-less `UTF8Encoding`.
- **Legend in a short iframe.** Legend directly in `view.ui` on wide screens; `new Expand({ mode: 'drawer', expanded: false })` on phones.
- **Palette validation.** EIP green `#6EBE44` next to EIP orange `#F16022` fails the colorblind check. Pairs that pass: `#007DC3` with `#F16022`; blue, orange, forest `#4A6118`, olive `#B5A64C` as four; blue, amber `#E8A33D`, brick `#9C3E27` for ordered hazard. Run the `dataviz` validator on any new set.

---

## Message and copy

Write the monitoring approach in plain terms: what is measured, by whom, how often, at what resolution, and what it will show over time. Name the protocol and partners when known. TRPA style: spell out percent in prose, Oxford comma, numerals for 10 and up, define acronyms at first use (WUI, EVeg, CWHR). Symbols are fine inside charts and tables. The program description on the host page is not repeated in the embed. Standard empty-state wording: "No {measurement} loaded yet. This section will show {what}."

---

## Checklist before pointing the CMS at a URL

1. Renders at 375 px and 980 px with no horizontal scroll, on `#f7f7f7`.
2. No console errors on load (reload before reading; the pane keeps old errors).
3. Live query succeeds, and the snapshot fallback renders when the network is blocked.
4. Every chart has a working Table toggle and CSV download.
5. Sources and data vintage stated under every card.
6. Committed and pushed; the GitHub Pages URL returns the new file.
7. Send the URL and, if the default height is wrong, a `DashboardHeight`, to the LT Info admin.
