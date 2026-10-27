# Monitoring page sections

The sections a monitoring program dashboard or staff topic page is built from, in the order they usually appear. Each entry says what the section answers, the markup and kit calls, the copy, and where a working example lives. Class names are the kit's (`ltinfo-embed.css`); element hooks are `data-ref` names inside the fragment root. Templates are in `../assets/templates/`; the canonical copies and the kit live in `trpa-agency/Monitoring`, folder `ltinfo/`.

Built and verified on Oct. 26, 2026 on Tahoe Yellow Cress, Bicycle and Pedestrian, and Noise data.

---

## Program dashboard sections

A program dashboard is one fragment for the Dashboard card of a program page (program type 6). The host supplies the program name, overview, partners, documents, and indicators above and below the card; the dashboard repeats none of them. Template: `program-dashboard.html` with its module `program-dashboard.js`.

### 1. At a glance

**Answers:** the headline question in one look. How big is the program's subject, how much was covered, what changed, where it stands against the standard.

**Markup:** `.section` with `.section-label` ("At a glance"), `.section-head` holding an `h2` and one lead paragraph, then `.tiles` (`data-ref="glance-tiles"`) and a small muted source line.

**Tiles:** four to six. Each is `.tile` with `.v` (the number, unit in `<small>`), `.l` (what it is), and `.d` (a direction line). Build direction lines with `LTI.change(now, before, unit, when)`: "down from 30 in 2022", "up from 6,224 ft in 2022". Other good `.d` lines: "first recorded 1978", "42 days ago", "6 short in 2023", "met in 2023". A tile for data not loaded yet is `.tile.pending` with "Not yet shown" and a `.d` that says why ("count field under review").

**Loading:** `LTI.skeletonTiles(el, n)` before the first query returns.

**Copy:** the lead paragraph is two or three sentences on what is monitored and what drives the number. The `h2` names the subject plainly ("Tahoe yellow cress on the shores of Lake Tahoe"), not the program.

### 2. Map

**Answers:** where the sites or the extent are, and the story of any one place in one click.

**Markup:** `.section`, then a `.card` with `.card-head` (an `h3` and a transparent "Map service" button), `.map-view` (`data-ref="map"`, `role="region"`, an `aria-label`) holding a `.map-placeholder` with a loader, then `.caption` and a source line.

**Kit:** `LTI.map(container, { center, zoom })` for the basemap, terrain switch, and docked popup; `LTI.popup([story, chart], { title: '{name}' })` for the template; `LTI.clientLayer({ features, fields, renderer, popupTemplate })` for the sites; `LTI.wire(view, layer, { onSelect })` for one-click select and hover; `LTI.legend(view, layer)`; `LTI.ringAt(view, lon, lat)` for the selection ring.

**Story numbers:** compute what the popup needs in the fragment (years tracked, years occupied, rank, trend, the last ten counts) and put it on the client-side layer's attributes. Do not lean on the service's raw fields.

**Caption:** say what the symbols mean and that the tables cover the same facts without the map, and invite the click: "Click a site for its story."

**Fallback:** if the SDK or the basemap fails, the placeholder text says the tiles and tables cover the same sites.

### 3. The record

**Answers:** how the measure has changed over time, against the standard.

**Markup:** `.section` with label, `h2`, and lead, then `.grid-2`. The main chart is `.card.span-2`; supporting charts sit in single cards. Each chart card has `.card-head` with an `h3` and a Calcite segmented control (`data-ref="...-toggle"`, items `chart` and `table`), `.plot`, a `.hidden` grid container, an optional HTML `.chart-legend`, `.caption`, and a source line.

**Kit:** `LTI.skeleton(plot, height)` first; `LTI.plot(el, traces, LTI.layout({ height, ... }, root))` to draw; `LTI.targetLine(y, label)` for the standard; `LTI.toggle(control, { chart, table })` with `LTI.grid(el, columns, rows, exportName)` on the table side; `LTI.hbar(el, entries, opts)` for a ranked bar.

**Comparison defaults:** the default view is the comparison that matters, not the raw series. Occupied sites against the standard with lake level on a second axis; a site's monthly counts against what is typical for that calendar month at the site; average level per period against each category's standard.

**Colors:** `LTI.colors(root)`. The first series is the site accent (`#789440` on Monitoring), the second the host navy `#2f3f56`. The standard is a dashed `#4e4e4e` line with a label at its right end, never a legend entry alone. Program-specific domain ramps (ordered hazard, seral stage) stay where the domain calls for them.

**Legend:** HTML in `.chart-legend` with `showlegend: false`, so it wraps on phones.

**Caption and source:** the caption says what bars, lines, and dashes are. The source line comes from `LTI.sourceText(live, captured, serviceName)` and says live or snapshot.

### 4. How it is measured

**Answers:** what each number means and where it comes from.

**Markup:** `.section` with label and `h2`, then `.grid-3` of `.def` cards, each an `h3` and one or two short paragraphs. A `.def` can hold a small table for class breaks.

**Copy:** one card per concept (the site, the survey or instrument, the unit, the standard). Define acronyms here at first use. Two or three sentences each.

### 5. Program-specific section, empty until data exists

**Answers:** what this section will show once the data is in, so a reader is not left wondering.

**Markup:** `.section` with label, `h2`, and a lead saying when it fills in, then `LTI.emptyState(title, bullets)` in a `data-ref` container.

**Copy:** "Per-site plant counts are not shown yet. When they are, this section will show:" followed by two or three bullets naming the views. Never draw a chart from placeholder numbers.

### 6. Footer

**Markup:** `.footer` with a strong "About the program." sentence pair, a `.links` row (the LT Info program page, the Threshold Dashboard category, a StoryMap or report), and a vintage line (`data-ref="footer-vintage"`) that says live or snapshot and the latest record date.

---

## Site explorer

A sites fragment for any program whose data is a point layer of sites plus a table of observations. Template: `sites-timeseries.html`, module `kit/fragments/sites-timeseries.js`. Used whole as the Bicycle and Pedestrian page and inside a topic page.

**Sections:** At a glance tiles (sites, records, most recent count, busiest site), then the sites card (picker in the card head, map, a facts list `dl.site-facts`), then the series card (monthly bars against the typical-month line, Chart/Table, CSV), then How it is measured, then the footer.

**Interaction:** clicking a point or picking from the list selects the site; the story popup opens, the facts and chart follow, and `?site=<id>` is written to the URL with `LTI.setParam`. A deep link lands on that site. When the site's record loads, its trend and last 12 months are pushed into the map feature with `LTI.updateFeature` so the popup chart fills.

**Join quality:** say in a tile how many sites carry a record ("54 with counts in the record") when the join is not perfect.

---

## Section fragment

One chart with a title, Chart/Table control, CSV, caption, and source. Template: `section-embed.html`, module `kit/fragments/section-embed.js`. Config-driven, no code changes per use: `service`, `where`, `orderBy`, `xField`, `yField`, `seriesField` (null for one series), `targetField` (null for no standard), `chartType` (`line` or `bar`), `xCategorical`, labels, `decimals`, `caption`, `sourceName`, `exportName`.

Built uses: plan area noise by land use against each standard (table 74, lines, four series); shoreline exceedances per day against a standard of zero (table 78, bars, one series).

---

## Staff topic page blocks

A topic page is a CMS page at a vanity URL in ESA's framework; today it is a harness page (`topic-page.html`) with fragments included inline. Built use: `pages/noise/index.html`, and `pages/forest-health/index.html` for a hub without fragments.

1. **Lead.** `.section-label` ("Overview" or the program family), an `h2` stating the question the page answers, a `.lead` paragraph, and a `.jump` list of the sections below.
2. **Narrative plus a section.** `.section` with label and `h2`, a `.prose` block of two short paragraphs (what is measured, then what the record shows, in plain words with the numbers that matter), then `<div data-lti-include="section.html">` whose own child is the fallback: an `.empty` block with a direct link.
3. **Pending section.** Narrative plus an `.empty` block saying what will appear, when a record has no summary yet (the highway noise section).
4. **How it is measured.** A `.grid-3` of `.def` cards for the shared concepts across the page.
5. **Program cards (hubs).** A grid of `.card` blocks, each with what the program measures as a short list and two buttons: the dashboard and the program page.
6. **Related.** A `.related` grid of link cards: each program page, the Threshold Dashboard category, the EIP tracker or StoryMap.
7. **Footer.** Who wrote the narrative, that the charts are TRPA fragments with their own sources, and the page date.

Narrative copy follows TRPA style: plain conversational language for a public and board audience, Oxford commas, percent spelled out, numerals for 10 and up, no em dashes, define every acronym at first use.
