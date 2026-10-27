---
name: ltinfo-platform
description: "Lake Tahoe Info (LT Info) platform reference for every laketahoeinfo.org dashboard: the shared shell, design tokens sampled from the live site, card and grid styling, the anonymous internalapi.laketahoeinfo.org routes, and the embed contract for charts, maps, and dashboards that TRPA hosts on GitHub Pages and the CMS pulls in by URL. Use this skill whenever building, styling, or debugging anything that will be embedded in or must match thresholds.laketahoeinfo.org, monitoring.laketahoeinfo.org, transportation.laketahoeinfo.org, climate.laketahoeinfo.org, eip.laketahoeinfo.org, clarity.laketahoeinfo.org, or parcels.laketahoeinfo.org. Pair it with the dashboard skill for the specific site (trpa-threshold-dashboard, trpa-monitoring-dashboard, trpa-transportation-tracker, trpa-climate-dashboard) and with trpa-dashboard-stack for libraries. Trigger on: LT Info, laketahoeinfo.org, Lake Tahoe Info, LT Info embed, internalapi, ESA dashboard, CMS embed, iframe for LT Info, LT Info styling, Lexend Deca host styles."
---

# Lake Tahoe Info platform

Lake Tahoe Info is TRPA's data platform, built and hosted by Environmental Science Associates (ESA). It was re-platformed in 2026 as an Angular single-page application with a shared backend at `internalapi.laketahoeinfo.org`. Seven dashboards share one shell, one token set, and one embed pattern. TRPA staff manage content through the CMS and supply the data visualizations as standalone HTML files on GitHub Pages that the CMS references by URL.

This skill holds what is common. The per-dashboard skills hold the frameworks, routes, and file conventions for each site.

| Dashboard | URL | Dashboard skill |
|---|---|---|
| Threshold Dashboard | thresholds.laketahoeinfo.org | `trpa-threshold-dashboard` |
| Monitoring Dashboard | monitoring.laketahoeinfo.org | `trpa-monitoring-dashboard` |
| Transportation Tracker | transportation.laketahoeinfo.org | `trpa-transportation-tracker` |
| Climate Resilience Dashboard | climate.laketahoeinfo.org | `trpa-climate-dashboard` |
| EIP Project Tracker | eip.laketahoeinfo.org | `trpa-data-services` (data), `trpa-eip-brand` (outreach materials, not the tracker itself) |
| Lake Clarity Tracker | clarity.laketahoeinfo.org | none yet |
| Parcel Tracker | parcels.laketahoeinfo.org | `trpa-data-services` |

Sampled from the live sites on Oct. 13, 2026. The sites are JavaScript-rendered, so WebFetch returns only a title. Read them with the browser tools and wait five to seven seconds for the main element to render.

---

## The rule that matters most

Embeds match the host, not a TRPA brand. An LT Info page is Lexend Deca on white and light gray, with the dashboard's own accent color on card headers. The TRPA agency blue, the EIP palette, and the Tahoe Living palette belong on trpa.gov, tools.trpa.gov, and outreach materials. Inside an LT Info page they look pasted in. Use the tokens below.

---

## Shell anatomy

Every dashboard renders the same chrome around its content.

1. **Header**, navy `#2f3f56`, with the LT Info logo (`/assets/logos/LT_INFO_LOGO2025-white.png`), the dashboard name, an Explore menu listing all seven dashboards plus Projects, Data Center, and News, then Log In, Request Support, and About. Each dashboard has a header image at `/assets/header-images/{dashboard}.png` and a white icon at `/assets/icons/{dashboard}-icon-white.png`.
2. **Dashboard nav**, a second row of links specific to the site (for thresholds: Evaluations and Threshold Categories; for transportation: Projects and Program Info).
3. **Breadcrumb**, uppercase, white on the dashboard accent.
4. **Main column**, about 1,000 px wide at a 1,024 px viewport, narrower inside two-column panels (a threshold Status panel gives a chart about 400 px).
5. **Cards**, each with a colored header bar and a light gray body. Nearly all content, including every embed, sits inside a card body.
6. **Footer**, navy, with "Implementation & Hosting by Environmental Science Associates," the open source note about ProjectFirma, and the TRPA copyright.

The chrome is the CMS's job. An embed never reproduces any of it.

---

## Design tokens

The site defines 167 custom properties on `:root`. These are the ones embeds use. Values are hex as served.

The TRPA design system mirrors them as a preview layer: `assets/trpa-tokens.css` in the `trpa-agency/tools` repo has a `[data-brand="ltinfo"]` block that maps these values onto the `--brand-*`, `--gray-*`, `--status-*`, `--chart-*`, and Calcite variables, and the page at https://tools.trpa.gov/qa/general/design-system.html (trpa-agency.github.io/tools/qa/general/design-system.html until DNS is live; the link drops `qa/` when the page is promoted) has a Lake Tahoe Info embeds section with the palette, slot sizes, and contract. Use the layer to prototype an embed with the shared components; the values here are the source.

### Brand and semantic

```css
--primary: #3e72b0;          /* page titles, links in nav, primary chart series */
--secondary: #5a9cb0;        /* teal, secondary series */
--ltinfo-blue: #2f3f56;      /* header and footer navy */
--ltinfo-green: #89bf40;     /* platform green */
--ltinfo-orange: #e49937;    /* platform orange, highlights */
--ltinfo-olive: #646820;
--color-text: #4b4b4b;       /* body text (cards render #333) */
--color-link: #337ab7;       /* links in content */
--danger: #a94442;
--help-icon-color: #6c91a4;
--tan: #f4f3ef;
```

### Status scales (each has lighter, light, default, dark, darker)

```css
--green-default: #2cb92a;  --green-dark: #188c16;  --green-darker: #0b5d0a;
--red-default: #ed6969;    --red-dark: #be4c4c;    --red-darker: #822d2d;
--orange-default: #ffa62b; --orange-dark: #e69527;
--yellow-default: #ffe66d; --yellow-dark: #efd13d;
--blue-default: #0d5b73;   --teal-default: #5a9cb0;
```

### Grays (a 50 to 1000 scale)

```css
--gray-50: #fafafa; --gray-100: #efefef; --gray-200: #dcdcdc; --gray-300: #bdbdbd;
--gray-400: #989898; --gray-500: #7c7c7c; --gray-600: #656565; --gray-700: #525252;
--gray-800: #464646; --gray-900: #3d3d3d;
```

Blue scale for sequential data: `--blue-50 #f0f9fb`, `--blue-100 #daf0f3`, `--blue-200 #b9e1e8`, `--blue-300 #89cad7`, `--blue-400 #52aabe`, `--blue-500 #368ea4`, `--blue-600 #30748a`, `--blue-700 #2c5f72`, `--blue-800 #2b4f5f`, `--blue-900 #2a4755`.

### Cards, buttons, shape

```css
--card-header-bg-color: #969eac;     /* default; each dashboard overrides it, see below */
--card-title-text-color: #ffffff;
--card-body-bg-color: #f7f7f7;        /* an embed's page background should match this when it sits in a card */
--card-border-color: #efefef;
--btn-primary-bg-color: #2f3f56;      /* hover #305d8e */
--btn-secondary-bg-color: #7a8190;    /* hover #5e6370 */
--border-radius-200: .25rem;  --border-radius-300: .5rem;   /* cards use 4px */
--shadow-100: 0 4px 6px 0 hsla(0, 0%, 0%, .1);
--spacing-unit: 1rem;  /* spacing-100 .25rem, -200 .5rem, -400 1rem, -600 2rem */
```

### Card header color by dashboard (computed on the live pages)

| Dashboard | Card header | Notes |
|---|---|---|
| Threshold Dashboard | `#6c91a4` | steel blue; category pages also carry each category's theme color |
| Monitoring Dashboard | `#789440` | green; breadcrumb and primary buttons use it too |
| Transportation Tracker | `#2c5282` | navy blue; strategies carry their own colors |
| Climate Resilience Dashboard | no cards on outcome pages | goal colors drive the page instead |

### Typography

Lexend Deca, self-hosted at `/assets/fonts/lexend-deca/` in Regular, Medium, SemiBold, and Bold. Base 16px, line height 1.4, body `#4b4b4b`, card text `#333`. The type scale is fluid:

| Token | Clamp | Used for |
|---|---|---|
| `--type-size-300` | .87rem to 1.13rem | body in cards |
| `--type-size-400` | 1.04rem to 1.35rem | card titles (18px, uppercase, white, 700) |
| `--type-size-500` | 1.25rem to 1.63rem | page titles (21.6px, uppercase, `--primary`, 600) |
| `--type-size-200` | .72rem to .94rem | captions, grid cells (14px) |

Field label bars inside cards (`h3.popover-header`) are `#efefef` with `#3d3d3d` text at 16.5px 600, 8px 16px padding, rounded top corners. Section labels are uppercase 14px in the dashboard accent.

Google Fonts serves Lexend Deca for embeds: `https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@400;500;600;700&display=swap`. Plotly does not inherit the page font; set `font.family` on every layout.

### Grids and maps on the host

AG Grid at 14px, cells `#181d1f`, header `#666` with white 600 text, rows `#fff` and `#fafafa`, row border `rgba(0,0,0,.15)`, row height 48, "Total Records: N" under the grid. Maps are Leaflet with a basemap toggle (Aerial, Street, Terrain) and overlay toggles (Street Labels, Watersheds, Jurisdictions, TRPA Boundary, plus the page's own layers). Embeds may use the ArcGIS Maps SDK per `trpa-dashboard-stack`, but the look should read as the same family: gray or terrain basemap, the same overlay names, a plain legend.

---

## Embeds: what TRPA builds

Three kinds of file, one contract. Decide which one before writing anything.

| Kind | Host | What it is | Size it lives in |
|---|---|---|---|
| **Threshold element** | Status panel, Evaluation Map, Additional Figures on an indicator page | One chart or one map per file. The CMS supplies narrative, status, and structure. | chart about 400 by 400 px, map about 435 by 300 px, inside a two-column card |
| **Climate chart or map** | Outcome page | One chart or map per file, registered in the indicator's Additional Charts list or Indicator Map URL. | iframe classes `primary-chart`, `map`, `secondary-chart`; full column width |
| **Monitoring dashboard** | Dashboard card on a program page | One complete dashboard per program in one file: at a glance, map, charts with tables, sections, sources. The card supplies only its header and a Fullscreen control. | full card width, about 980 px, iframe class `dashboard-frame` |

Transportation Data Trends take the same kind of embed as a monitoring dashboard (content type `EmbedUrl`).

### Contract

- **No chrome.** No logo, no page title, no footer. The host card or panel provides them.
- **Background matches the host.** White for threshold and climate embeds, `#f7f7f7` for a monitoring Dashboard card. Never a brand color.
- **Lexend Deca everywhere**, including Plotly layouts and AG Grid themes.
- **Fluid width.** Design for the slot (400 px for a threshold chart, 980 px for a dashboard) and check 375 px. No horizontal scroll.
- **Own your height.** The CMS iframe has a fixed height set by the admin (`ContentHeight`, `DashboardHeight`) or a default. Post the document height on load and on resize so a host that listens can size the frame, and make sure nothing breaks if it does not:
  ```javascript
  // body, not documentElement: inside a frame documentElement.scrollHeight never reports less than the frame, so it could grow but never shrink
  const post = () => window.parent.postMessage({ type: 'ltinfo-embed:height', height: document.body.scrollHeight }, '*');
  window.addEventListener('load', post); window.addEventListener('resize', post);
  ```
- **Stop wheel zoom on maps** (`view.on('mouse-wheel', e => e.stopPropagation())`) so page scrolling inside the iframe does not become map zooming.
- **`allow="fullscreen"`** is set by the host; design so the page also works at full screen.
- **Every chart has a table view and a CSV download.** Every map has the same facts in text or a table nearby.
- **Load Plotly from a CDN**, never inline the 3.6 MB bundle that a Python `fig.write_html()` produces. The legacy threshold and climate charts were written that way and weigh 3 to 4 MB each.
- **Empty states are explicit.** Never render a chart from placeholder numbers.

### Plotly layout for an LT Info embed

```javascript
const LTI_COLORS = ['#3e72b0', '#e49937', '#89bf40', '#5a9cb0', '#be4c4c', '#646820', '#89cad7', '#2c5f72'];
const LTI_LAYOUT = {
  font: { family: 'Lexend Deca, sans-serif', color: '#333333', size: 13 },
  paper_bgcolor: 'white', plot_bgcolor: 'white',   // '#f7f7f7' inside a monitoring Dashboard card
  margin: { t: 10, r: 10, b: 40, l: 50 },
  xaxis: { gridcolor: '#dcdcdc', linecolor: '#dcdcdc', automargin: true },
  yaxis: { gridcolor: '#dcdcdc', linecolor: '#dcdcdc', zeroline: false },
  colorway: LTI_COLORS, hovermode: 'x unified',
  legend: { orientation: 'h', y: -0.2 }, uniformtext: { minsize: 9, mode: 'hide' }
};
const LTI_CONFIG = { displayModeBar: false, responsive: true };
```

A target or standard line is dashed `#4e4e4e` with a label at the right end. Sequential data uses the blue scale. Ordered hazard uses `#3e72b0`, `#e49937`, `#be4c4c`. Validate any new categorical set with the `dataviz` skill; `#89bf40` next to `#e49937` is the pair to watch.

### AG Grid theme for an LT Info embed

```javascript
const theme = agGrid.themeQuartz.withParams({
  accentColor: '#3e72b0', fontFamily: 'Lexend Deca, sans-serif', fontSize: 14,
  headerBackgroundColor: '#efefef', headerTextColor: '#3d3d3d', headerFontWeight: 600,
  oddRowBackgroundColor: '#fafafa', borderColor: 'rgba(0,0,0,.15)', rowHeight: 48, headerHeight: 44
});
```

The host's own grids use a `#666` header. Inside a white card the `#efefef` label bar reads better, which is what the Forest Health embeds use.

---

## The API

Base `https://internalapi.laketahoeinfo.org`. Anonymous GET on the routes the public pages call; list and admin routes return 401. The old `www.laketahoeinfo.org/WebServices/.../{token}` routes are dead and return the Angular shell. Each dashboard skill lists its routes and the JSON shapes. Shared routes:

| Route | Returns |
|---|---|
| `/file-resources/{guid}` | an uploaded image or document; every `*FileResourceGUID` field resolves here |
| `/custom-rich-texts/{id}` | a CMS rich text block (`CorralPageContent` HTML) that fills a page section |
| `/field-definitions/labels` | the 549 field labels the pages use for tooltips |

The pages fetch these from the browser, so the API allows the laketahoeinfo.org origins. Fetching from an embed on GitHub Pages has not been verified; the EIP snapshot ETL in `trpa-agency/EIP` reads the API server side and publishes JSON to GitHub Pages, which is the safe pattern for any embed that needs LT Info data.

---

## Stack facts verified Oct. 13, 2026

- **Script order.** Plotly, AG Grid, and jsPDF are UMD bundles. Load them before the ArcGIS Maps SDK, or Dojo's AMD loader claims them and `window.Plotly` stays undefined.
- **Calcite on the CDN.** `js.arcgis.com/calcite-components/5.0` redirects to `5.0/index.js`, a lazy-loading build; there is no `5.0/calcite.css` or `5.0/calcite.esm.js` (both 404). Load 5.0 with the module script alone. The 2.x and 3.x builds are `{version}/calcite.esm.js` plus `{version}/calcite.css`. When the ArcGIS SDK 4.31 is on the page, its widgets render through the Calcite version it bundles, so load `2.13.2` to match and avoid mispositioned popovers.
- **Plotly legends are not responsive.** Render the legend as HTML with `showlegend: false` when the chart must survive a phone width, and redraw on a debounced resize.
- **Expand widgets in short iframes.** Put the Legend directly in `view.ui` on wide screens; use `new Expand({ mode: 'drawer' })` on phones.

---

## Writing

Field copy lives in the CMS, not in the embed. Follow the TRPA Style Guide: spell out percent in prose, Oxford comma, numerals for 10 and up, define acronyms at first use (SEZ, VMT, CFA, TAU, BMP). Symbols are fine inside charts and tables. An embed carries only chart titles, axis labels, captions, and source lines.

---

## Checklist before pointing the CMS at a URL

1. Renders at the slot width and at 375 px with no horizontal scroll.
2. Lexend Deca on every text element, including Plotly and AG Grid.
3. Background matches the host slot. No TRPA, EIP, or Tahoe Living brand chrome.
4. No console errors on load. Reload before reading the console; the pane keeps old errors.
5. Live query succeeds, and the snapshot fallback renders when the network is blocked.
6. Every chart has a working Table toggle and CSV download. Sources and data vintage are stated.
7. Committed, pushed, and the GitHub Pages URL returns the new file.
8. Run `trpa-dashboard-qa` before handing the URL to the LT Info admin.
