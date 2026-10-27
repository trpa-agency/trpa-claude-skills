---
name: trpa-monitoring-dashboard
description: "Lake Tahoe Info Monitoring Dashboard (monitoring.laketahoeinfo.org) reference. Use when building or updating a program dashboard, a section, or a staff topic page for a Monitoring Program (Forest Health, Tahoe Yellow Cress, Bicycle and Pedestrian, Noise, Streams, Air Quality, Transit, or any monitoring program), working with the LT Info fragment kit in trpa-agency/Monitoring/ltinfo, writing Arcade popups for monitoring maps, or reading program and site data from the LT Info API or the LTInfo_Monitoring map service. Covers the fragment form for inline rendering in ESA's framework, the four templates, page anatomy, host styling and palettes, map and popup rules, the data table, API routes, the Forest Health reference dashboards, and stack gotchas. Trigger on: monitoring dashboard, monitoring program page, monitoring.laketahoeinfo.org, Dashboard card, LT Info fragment, ltinfo kit, topic page, Arcade popup, monitoring sites, bike ped page, noise page, subalpine conifer dashboard, LT Info monitoring."
---

# Monitoring Dashboard

Reference for [monitoring.laketahoeinfo.org](https://monitoring.laketahoeinfo.org/), the inventory of monitoring programs in the Tahoe Region: what is monitored, how, where, by whom, and the record so far. TRPA builds the dashboards, sections, and staff pages that show the record.

**Always pair with** `ltinfo-platform` for the shell, tokens, and platform facts, `trpa-dashboard-stack` for libraries, and `forest-health-domain` for Forest Health vocabulary. Run `trpa-dashboard-qa` before anything goes to the LT Info admin or ESA. Program facts sampled Oct. 13, 2026; the kit, templates, and rules below built and verified Oct. 26, 2026.

**Where the work lives.** The kit, templates, pages, contract, and plan are in `trpa-agency/Monitoring`, folder `ltinfo/`, published at `https://trpa-agency.github.io/Monitoring/ltinfo/`. Read `ltinfo/CONTRACT.md` (what every fragment does, and what the port needs from ESA) and `ltinfo/PLAN.md` (phases, data, open items) before changing anything there. The design system documents the same pattern with live specimens in section 19, LT Info Monitoring: https://tools.trpa.gov/qa/data/design-system.html#ltinfo-monitoring (served at https://trpa-agency.github.io/tools/qa/data/design-system.html until the tools.trpa.gov DNS is live).

---

## Two products, not one

TRPA builds two kinds of LT Info content. Decide which before writing anything.

| | Threshold element | Monitoring content |
|---|---|---|
| Host | Status panel or Evaluation Map on `thresholds.laketahoeinfo.org` | A Monitoring Program page or a staff page on `monitoring.laketahoeinfo.org` |
| What we build | One chart or one map per file. The CMS supplies narrative, status, and structure. | A program dashboard, a section, or a topic page, built as fragments |
| Question it answers | Is the Region meeting the standard? | What is monitored, how, where, and what does the record show? |
| Numbers | Attainment against a target | Observed measurements, extents, counts, change over time |
| Tone | Evaluative, set by the CMS copy around it | Descriptive |

Monitoring content may link to its threshold indicator in the footer, and may draw the standard as a line on a chart. It does not repeat a status badge. See `trpa-threshold-dashboard` for the other product.

Three kinds of monitoring content:

| Kind | Where it appears | What TRPA supplies |
|---|---|---|
| Program dashboard | The Dashboard card on a program page (program type 6) | One fragment: at a glance, map, charts with tables, measurement notes, sources |
| Section | A section on any program page, beside the program's own LT Info data (a requested framework change) | One chart, map, or table fragment with its title, caption, and source |
| Staff topic page | A page at a vanity URL inside the LT Info shell (a requested framework change) | Narrative blocks plus one or more section fragments |

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

### The Dashboard card today, from the API

The program record's `Dashboard` object is what the admin sets:

```json
"Dashboard": { "MonitoringProgramDashboardID": 6, "DashboardUrl": "https://...", "DashboardDescription": "...",
               "DashboardHeight": null, "DashboardWidth": null, "FileResourceInfoID": null, "FileResourceGUID": null }
```

The page renders `<iframe class="dashboard-frame" allowfullscreen title="Monitoring Program Dashboard" src="{DashboardUrl}">` at the card body width (about 980 px at desktop), with a Fullscreen action in the card header. Height and width are optional overrides; a file resource can stand in for a URL. The LT Info admin sets these fields; TRPA supplies the URL. This iframe is the interim path; see the fragment form below.

---

## The fragment form

ESA is scoping a collaborative integration in which TRPA content renders inline in LT Info pages and staff eventually author in ESA's repository. No iframes in the end state. TRPA builds prototypes in the Monitoring repo in the shape that ports.

**A fragment** is one `<section class="lti" data-site="monitoring" data-kind="section-embed">` holding:

- its markup, with `data-ref` hooks and no element ids,
- `<script type="application/json" data-lti="config">`: service, fields, labels, captions,
- `<script type="application/json" data-lti="snapshot">`: rows with the same shape as the live query, plus `captured`.

No executable script inside the fragment, no styles outside `.lti`, nothing that reaches outside its root. Two fragments on one page do not interact.

**A module** gives a kind its behavior: `LTI.define(kind, async (root, CONFIG, SNAPSHOT) => { ... })`, with lookups through `LTI.ref(root, name)`. Generic kinds live in `kit/fragments/<kind>.js` and load on demand. A program dashboard is specific to its program, so its module sits next to the page and the fragment names it with `data-module`.

**The kit mounts.** `ltinfo-embed.js` mounts every `.lti[data-kind]` on DOMContentLoaded (`LTI.mount`, `LTI.mountAll`), and resolves every `<div data-lti-include="url">` by fetching that page, lifting its fragment, and mounting it inline. The placeholder's own children are the fallback.

**A harness page** is the standalone file that wraps one fragment for review on GitHub Pages: the document, the pinned libraries, the kit, `<body class="lti-harness" data-slot="card">` (or `white`), and the fragment between `<!-- fragment:start -->` and `<!-- fragment:end -->`. In ESA's framework the harness is their layout.

**Interim.** Today's Dashboard card is an iframe, and a harness page works in it unchanged. When framed, and only then, the kit posts `{ type: 'ltinfo-embed:height', height, source }` with the body's content height, and accepts and posts `{ type: 'ltinfo-embed:params', params }`. Deep links otherwise live in the page URL (`LTI.params`, `LTI.setParam`).

**Kit files**, in `ltinfo/kit/`:

| File | What it gives |
|---|---|
| `ltinfo-embed.css` | Host tokens and every style, scoped under `.lti`; per-site accents and series palettes keyed on `data-site`; harness styles under `.lti-harness` |
| `ltinfo-embed.js` | `define`, `mount`, `include`, `query` with JSONP fallback, `load` with snapshot first if live is slow, `plot`, `layout`, `colors`, `targetLine`, `hbar`, `grid` with CSV, `toggle`, `skeleton`, `skeletonTiles`, `change`, `emptyState`, `showEmpty`, `sourceText`, `params`, `setParam` |
| `ltinfo-map.js` | `map`, `popup`, `clientLayer`, `wire`, `updateFeature`, `openFeature`, `legend`, `ringAt` |
| `fragments/` | `section-embed.js`, `sites-timeseries.js` |
| `popups/` | Arcade story and chart files per layer |

Pages link the kit by absolute URL (`https://trpa-agency.github.io/Monitoring/ltinfo/kit/...`) when they live outside the Monitoring repo. Breaking changes go to `kit/v2/`.

---

## Templates

Copies are in `assets/templates/` with the kit linked by absolute URL; the canonical copies are in `ltinfo/templates/`. Each file's head comment says what to replace.

| Template | What it is | Default data |
|---|---|---|
| `program-dashboard.html` with `program-dashboard.js` | The full program dashboard pattern | Tahoe Yellow Cress, layer 9 and table 86 |
| `section-embed.html` | One config-driven chart with Chart/Table, CSV, caption, source | Plan area noise, table 74 |
| `sites-timeseries.html` | Map, picker, tiles, monthly record against the typical month, table, `?site=` deep link | Bike ped counters, layer 5 and table 1 |
| `topic-page.html` | Narrative blocks with sections included inline | A short noise page |
| `_frame.html` | Review mock of an LT Info page in Dashboard card, section, or topic mode | Any of the above |

Arcade files are in `assets/popups/`: `bike-ped-counter.arcade` and `yellow-cress-site.arcade` (story text), and a `-chart` pair for each (column chart). Section by section guidance, with copy, markup, and kit calls, is in `references/sections.md`.

Built pages to copy from: `ltinfo/pages/bike-ped/` (the sites fragment filled), `ltinfo/pages/noise/` (topic page with two sections inline and a pending highway section), `ltinfo/pages/forest-health/` (a hub of the three Forest Health programs).

To start a page: copy the closest template, set `data-site` and `data-kind`, edit the config block, capture a snapshot from the same query, write the copy, then check it in `_frame.html` at 980 and 375 px.

---

## What the content must do

- **No chrome.** No logo row, page title, or footer nav. The host provides them. Program name, partners, documents, and indicators stay in the CMS and are not repeated.
- **Host styling, not a TRPA brand.** Mason, Oct. 4, 2026: "make sure these use the same styling that monitoring.laketahoeinfo.org uses." Lexend Deca everywhere, including Plotly and AG Grid; card label bars `#efefef` with `#3d3d3d` 600 headings; section labels `#789440` uppercase 14px; links `#337ab7`; Calcite brand `#789440` with hover `#61783a` and press `#4e6230`; AG Grid Quartz at 14px cells, `#fafafa` striping, and the `#efefef` label-bar header.
- **Background matches the slot.** `#f7f7f7` in a Dashboard card, white on a topic page or a white card body.
- **Series colors from `LTI.colors(root)`.** On Monitoring the palette is `#789440`, `#2f3f56`, `#b5a64c`, `#5a9cb0`, `#e49937`, `#4e6230`, `#89cad7`, `#9c3e27`: the accent first, the host navy second. Thresholds leads with `#6c91a4`, Transportation with `#2c5282`. Domain ramps stay where the domain calls for them: ordered hazard `#3e72b0`, `#e49937`, `#be4c4c`; seral classes `#e49937`, `#89cad7`, `#2c5f72`, `#89bf40`, `#0b5d0a`.
- **The standard is a labeled dashed line** (`LTI.targetLine`, `#4e4e4e`), never only a legend entry.
- **Fluid width.** About 980 px in the card, about 1,000 px on a topic page, checked at 375 px, no horizontal scroll.
- **Every chart has a table and a CSV**, every card a source line, the footer a data vintage line.
- **Live with a fallback.** Query at mount, fall back to the snapshot, say which is showing. Skeletons while queries run; the snapshot within a second if live is slow. `?lti-snapshot=1` and `?lti-slow=1` exercise both paths.
- **Explicit empty states.** Never a chart from placeholder numbers.

---

## Maps and popups

Monitoring maps depart from the agency map conventions because they sit inside the host's pages.

- **Basemap: Esri Human Geography**, built by `LTI.map` from the three public vector tile items (base `2afe5b807fa74006be6363fd243ffb30`, detail `97fa1365da1e43eabb90d0364326bc2d`, label `ba52238d338745b1a355407ec9df6768`). The `arcgis/human-geography` style needs a token, so do not use it. All three are base layers, so the data points draw above the roads and labels.
- **Terrain switch** under the zoom controls: the World Hillshade layer between the base and the detail layer, multiply blend at 60 percent, off by default, remembers nothing.
- **Popup docks in the top right corner** at every width, no collapse button, no feature navigation.
- **Popup content is Arcade files**, one per element, stacked: a text element that leads with the sentence a reader wants (where this site stands, how it compares, what changed), then the record; then a media element returning a `columnchart` in the accent `#789440`. No field lists. The same files run in ArcGIS Pro and Portal web maps on any layer with the same attribute names.
- **Story numbers on a client-side layer.** Service fields rarely carry the story, so the fragment computes rank, trend, years occupied, and the last ten or twelve values, builds the layer with `LTI.clientLayer`, and the Arcade reads those attributes. Chart attributes follow a fixed pattern: label `l01` to `l12` with value `m01` to `m12`, or year `y01` to `y10` with count `c01` to `c10`. Push late-arriving values in with `LTI.updateFeature`.
- **One click.** Clicking a point selects the site, opens its story, and the tiles, chart, facts, and table follow. The site list does the same and pans to it. Hover highlights with a pointer. No "view details" step.
- **Selection** is one orange ring, `#e49937`, at a time (`LTI.ringAt`).
- **Legend** bottom left on wide screens, a drawer on phones. The top right belongs to the popup.
- **Wheel zoom stopped** inside the page so scrolling does not become zooming.

Arcade popup element shape that renders:

```javascript
return { type: 'media', title: 'Plants counted', attributes: attrs,
  mediaInfos: [{ type: 'columnchart', value: { fields: fields, colors: ['#789440'] } }] };
```

---

## Data: the LTInfo_Monitoring map service

`https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer`, anonymous, CORS enabled from outside the office network (JSONP `callback=` is the office fallback, built into `LTI.query`), `maxRecordCount` 2,000,000. Checked Oct. 26, 2026.

| Use | Layer or table | Records | Notes |
|---|---|---|---|
| Bike ped sites | 5 Bike and Pedestrian Counter Location (point) | 56 | `counter_id`, `counter_name` |
| Bike ped counts | 1 Bike and Pedestrian Counts (table) | 73,245 | daily `count_of_bike_ped`, `counter_name`, `count_date`, 2016-11-01 to 2026-09-15. `counter_id` is null, so join on `counter_name`: 54 of 56 counters match. Eight table-only names are spelling variants and two counters have no rows; fix at the source. |
| Plan area noise sites | 6 Plan Area Noise Monitoring (point) | 409 | one row per site, year, and category; `CNEL_LAND_USE`, `COUNT_VALUE`, `LTINFO` site link |
| Shoreline noise sites | 7 Shoreline Noise Monitoring (point) | 133 | `COUNT_VALUE` is a string |
| Highway noise sites | 11 Transportation Noise Monitoring (point) | 103 | `HIGHWAY`, `CNEL_LIMIT`, `CNEL_MAX_VALUE`, `CNEL_AVG_VALUE`, `DISTANCE_FROM_EDGE`; no summary table yet |
| Plan area noise averages | 74 Plan Area Noise Average (table) | 55 | `Category`, `Year` (a period label such as 2016-2019), `Value`, `Threshold_Value` |
| Shoreline exceedances | 78 Shoreline Noise Average Exceedances Per Day (table) | 12 | `Year`, `Value`, `Threshold_Value` 0; 2009 to 2023 with gaps |
| Yellow cress sites | 9 Tahoe Yellowcress (point) | 2,576 | one row per site and year, 65 sites, 1978 to 2025; `STATUS` is Surveyed or No Survey; `COUNT_VALUE` is assumed to be the plant count and must be confirmed with the program lead before a page shows it as settled |
| Yellow cress summary | 86 Occupied Sites by Year (table) | 40 | `Occupied_Sites`, `Lake_Level`, `Threshold` 26, 1978 to 2023 |

Forest Health numbers keep their own sources; see below.

---

## API routes

Base `https://internalapi.laketahoeinfo.org`, anonymous GET. Pages do not call it from the browser; where LT Info data is needed, a server-side job snapshots it to GitHub Pages first.

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

These predate the kit. They live in the ForestHealth repo under `monitoring/`, run in today's Dashboard card, and publish at `https://trpa-agency.github.io/ForestHealth/monitoring/<program-slug>.html`. Whether they move into `ltinfo/pages/forest-health/` or stay and adopt the kit is open (see PLAN.md); `ltinfo/qa/subalpine-conifer-kit.html` is the Subalpine Conifer page rebuilt on the kit as a fixture.

| Program | LT Info program | File | Built |
|---|---|---|---|
| Subalpine Conifer | 83 | `ForestHealth/monitoring/subalpine-conifer.html` | Sept. 17, 2026 |
| Forest Structure | no program yet | `ForestHealth/monitoring/forest-structure.html` | Oct. 2, 2026 |
| Fire Dynamics | no program yet | `ForestHealth/monitoring/fire-dynamics.html` | Oct. 2, 2026 |

`ltinfo/pages/forest-health/` is the hub that gathers the three. The older `ForestHealth/monitoring/index.html` is a standalone card index with a header, not an embed. As of Oct. 13, 2026 program 83's Dashboard card is still unset and the host has no program pages for Forest Structure or Fire Dynamics; ask the LT Info admin to create them. The three embeds load `ag-grid-community` unpinned; pin it to 36.2.0.

Two data patterns, settled Oct. 2, 2026:

- **Analysis outputs as data of record.** When the numbers come from the repo's analysis (Forest Structure), fetch `../output/*.csv` relative to the page and embed the same rows as a `SNAPSHOT` fallback, so page and data move together by branch.
- **Live service where the service is current.** Fire Dynamics queries `Fire/MapServer/3` (severity by management zone) and `Fire/MapServer/6` (CAL FIRE perimeters, envelope-filtered to the Basin) at load.

Do not query `Vegetation/FeatureServer` layers 3 (Composition) or 4 (Stand Density Classified) for numbers: as of Oct. 2, 2026 they carry the superseded run (transposed canopy classes, 177,540-acre frame). Use the `Forest_Health_*` tile services for display only, captioned as the 2023 assessment as published.

Plot data for Subalpine Conifer: where it will live (SDE feature class, hosted feature service, or repo CSV) and the field names are still open. The page documents the shape it expects in its `DATA.plots` and `DATA.health` comments.

---

## Data patterns from maps.trpa.org

ArcGIS Server on `maps.trpa.org` answers cross-origin `query` requests, so a page can pull summary statistics at load and fall back to a snapshot. With the kit:

```javascript
const { data, live } = await LTI.load(() => LTI.query(`${service}/${layer}`, {
  where: "WHRTYPE = 'SCN'", groupByFieldsForStatistics: 'REGIONAL_DOMINANCE_TYPE_1', returnGeometry: 'false',
  outStatistics: [{ statisticType: 'sum', onStatisticField: 'Acres', outStatisticFieldName: 'acres' }],
}), SNAPSHOT, showSnapshotFirst);
```

| Service | What it holds |
|---|---|
| `LTInfo_Monitoring/MapServer` | monitoring sites and summary tables; see the data table above |
| `Vegetation_Type/MapServer/0` | EVeg polygons: `WHRTYPE`, `TRPA_VegType`, `REGIONAL_DOMINANCE_TYPE_1`, `WHRSIZE`, `WHRDENSITY`, `Ownership`, `Elev_Ft`, `Acres`. 694,422 polygons; dynamic layers supported |
| `Vegetation/FeatureServer` | Composition (3), Stand Density Classified (4), USFS Sensitive Plants, Tree Mortality ADS 2023 |
| `Forest_Health_Stand_Density`, `Forest_Health_Composition_Age` | map services behind the threshold web maps |

Public web maps (ArcGIS Online item IDs): stand density `24fc43584a354f789f283df388bf723d`, seral stage `07d6ccd3c6f94425be295b9a6db043aa`, fire severity `35dc3ddb4ff546d2a169f6fdeb945320`, fuels treatments `0303bdff0aa04b628f8a60a8c72c53a1`.

---

## Stack gotchas confirmed on this site

- **Script order.** Plotly and AG Grid before the ArcGIS SDK, or they register as AMD modules and the globals stay undefined.
- **Pinned versions.** Plotly 2.35.2, ag-grid-community 36.2.0 (Theming API), Calcite 2.13.2 with ArcGIS Maps SDK 4.31. Calcite must match the SDK release: SDK widgets render through Calcite components and whichever definitions register first win. 3.3.0 against 4.31 left the Expand popover unpositioned; the `5.0` path is a different build with no `calcite.css`. A host page on Calcite 5 (the design system page is one) cannot mount the kit's fragments inline; frame them there.
- **Draw with `LTI.plot`, never `Plotly.newPlot`.** Plotly's responsive resize switches a chart with no definite height to autosize and a 100 percent tall container, which collapses it when its container changes size after the first draw. `LTI.plot` sets a pixel height from `layout.height`.
- **Report the body's height.** Inside a frame, `document.documentElement.scrollHeight` never reports less than the frame, so a frame could grow but never shrink. Report `document.body.scrollHeight`.
- **Plotly font and legends.** Set `font.family` to Lexend Deca in every layout. Render legends as HTML with `showlegend: false`, set `uniformtext: { minsize: 9, mode: 'hide' }` and `xaxis.automargin: true`, and wrap long category labels with `<br>` under 640 px. A plot div inside a card with side margins is `width: auto`, not `100%`.
- **Arcade popup content.** Use `{ type: 'expression', expressionInfo: { expression, title } }` with no `returnType`; setting it logs "cannot assign to read-only property 'returnType'". `collapseEnabled` on the popup is deprecated; use `visibleElements.collapseButton`.
- **A reloaded page can keep its old console.** Open a fresh tab before reading errors after a kit change, and reload kit files with `fetch(url, { cache: 'reload' })` when testing.
- **Editing from PowerShell 5.1.** `Get-Content` reads BOM-less UTF-8 as ANSI and double-encodes dashes on write. Use `[IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)` and `WriteAllText` with a BOM-less `UTF8Encoding`.
- **Palette validation.** Run the `dataviz` validator on any new categorical set. EIP green `#6EBE44` next to EIP orange `#F16022` fails the colorblind check.

---

## Message and copy

Write the monitoring approach in plain terms: what is measured, by whom, how often, at what resolution, and what it will show over time. Name the protocol and partners when known. Popups and tiles lead with the finding, then the facts. TRPA style: spell out percent in prose, Oxford comma, numerals for 10 and up, no em dashes, define acronyms at first use (CNEL, WUI, EVeg, CWHR). Symbols are fine inside charts and tables. The program description on the host page is not repeated. Standard empty-state wording: "No {measurement} loaded yet. This section will show {what}." Section by section copy is in `references/sections.md`.

---

## Checklist before a fragment goes to ESA or the LT Info admin

1. Renders at the slot width and at 375 px with no horizontal scroll, on the right background.
2. Lexend Deca everywhere, including Plotly and AG Grid.
3. No console errors on mount, alone and with a second fragment on the same page.
4. Live query succeeds, and the snapshot renders with `?lti-snapshot=1`.
5. Every chart has a working Table toggle and CSV download. Sources and vintage are stated.
6. No element ids, no styles outside `.lti`, no executable script inside the fragment.
7. Map on Human Geography with the points above its labels, terrain switch works, the popup docks top right with its story and chart, and one click selects.
8. Skeletons show while loading; nothing renders blank.
9. Height message observed in `_frame.html`, for today's Dashboard card.
10. Committed, pushed, and the GitHub Pages URL returns the page.
11. `trpa-dashboard-qa` run and passed. Then send the URL, and a `DashboardHeight` if the default is wrong, to the LT Info admin.
