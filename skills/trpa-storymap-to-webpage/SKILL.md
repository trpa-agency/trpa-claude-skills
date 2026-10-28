---
name: trpa-storymap-to-webpage
description: Rebuild an ArcGIS StoryMap (story, collection, or briefing) as a single-file, TRPA-branded web page on GitHub Pages. Pulls the published story JSON and images through the public ArcGIS REST API, outlines every block in reading order, checks every web map layer, maps each block (cover, sidecars, slideshows, web maps, swipes, map tours, galleries, charts, timelines, big numbers, Survey123 and other embeds) to a tested web pattern, applies TRPA brand and house style, and verifies at desktop and phone widths. Use this whenever someone wants to turn a story map into a website, home page, or project page, move a story off storymaps.arcgis.com, "rebuild", "reimagine", "port", or "migrate" a story map, or point a vanity URL like trpa.gov/resilienttransportation at GitHub Pages, even if they only paste a storymaps.arcgis.com link or a trpa.gov short link. Pair with trpa-brand and trpa-dashboard-stack.
---

# TRPA story map to web page

A story map is a good draft and a poor home: the agency cannot style it, link it into its own
tools, add sections, or own the URL. This skill turns one into a single HTML file in a GitHub
Pages repo that keeps the story's content and pacing (cover, scrolling sidecars, galleries, maps)
and gains TRPA branding, house style, and links into the project's other pages.

The reference build is the PROTECT project home (`trpa-agency/PROTECT`, `index.html` at the repo
root, Oct. 2026), rebuilt from the Connecting Tahoe collection. `assets/template.html` is that page
with placeholders, plus blocks tested on TRPA's own stories: a map sidecar that mixes web maps,
photos, and swipes, a prose-and-chart block, before and after images, big numbers, and video.

## Workflow

### 1. Extract

Run the extractor into a new, empty folder in the scratchpad. It accepts a story or collection
URL, a vanity URL that redirects to one (it follows the redirect), or a bare item id:

```bash
python -I <skill>/scripts/extract_storymap.py "trpa.gov/resilienttransportation" --out <scratch>/story
```

Use the `arcgispro-py3` interpreter on TRPA machines. `-I` matters because the folder fills with
downloaded files. Add `--no-images` for a quick look and `--videos` for hosted video. A private story
needs a token in `ARCGIS_TOKEN`; ask the owner to share it publicly instead, because the rebuilt
page cannot use private content either.

It writes `outline.md` (read this), `manifest.json` (media, web maps with per-layer health, embeds,
links, credits, style flags), `raw/` (the JSON as served), and `images/` (originals). The console
summary flags what changes the plan:

- **Layers that will not load**: every web map layer's service was requested. A dead or secured
  layer is broken in the live story too. Leave it out of the page and tell the user which service
  to fix. "Secured" can also mean removed: maps.trpa.org answers "Token Required" for a service that
  does not exist, so check the layer URL (`/MapServer/<n>`), which says "Service not found" when the
  service is gone. In Oct. 2026, 29 layers in 11 of TRPA's 38 public stories would not load, most of
  them on the removed `LTW_Base_Data` service.
- **A web map that is not public**: an anonymous page cannot load it. Ask for it to be shared or
  use a static image.
- **Unpublished draft changes**: only the published version is readable, so the page matches what
  the public sees, not the author's latest draft.
- **No item description**: write the hero lede and meta description from the opening paragraph.
- **Bylines**: they are usually staff names. Leave them out and credit the agency.
- **Credits in text**: photo credits sitting in panel text or captions ("Credit: Placer County").
  Move each one to the image it describes.
- **Style flags**: em and en dashes, ampersands, percent signs, double spaces, hyphenated year
  ranges, and "e.g." or "i.e.", with samples.
- **Orphan nodes**: blocks nothing points to, usually deleted content. Skim the list in case one is real.

If the outline shows a block as raw JSON, or a classic Story Map with no node tree, read
`references/storymap-json.md`.

### 2. Plan the page

Read the whole outline, then decide where the page lives and what it links to before writing
any HTML. Those are the user's calls; everything else has a default.

- **Where it lives.** A project front door goes at the Pages repo root (`index.html`), so
  `<org>.github.io/<repo>/` lands on it. Jekyll then stops rendering the README there. A page
  inside an existing site goes beside the other pages and gets their header and Pages menu.
- **What it links to.** If the project has tools or other pages, add a links block that routes
  readers into them, and say which are drafts. A public page should not lead straight into internal
  task lists or open decisions. Link the project's page index instead.
- **Section order** follows the story. Drop what exists only because of the story map format, such
  as an "Overview" and "Overview: Continued" split or hidden navigation links. Merge or retitle them.

Map each block with the table below, then copy the matching blocks out of `assets/template.html`.
Each one is labeled with the story map type it replaces, and its CSS and JS are labeled to match.

| Story map block (outline tag) | Web pattern | Template block |
|---|---|---|
| `[cover ...]` with image | Full-bleed hero: eyebrow, title, subtitle, one-sentence lede, one or two buttons | hero |
| `[navigation]` | Section links in the sticky top bar (hidden under 1,060 px) | topbar |
| `[sidecar/docked-panel]` with 1 slide | Text beside a full-height photo; alternate sides | split |
| sidecar or `[slideshow]` with several image slides | Sticky image that crossfades as step cards scroll past; inline images on phones | scrolly |
| sidecar whose slides mix `[webmap]`s, photos, and `[swipe]`s, or a `[map tour]` | One MapView: each step sets its web map, view, and layers; photo steps fade over the map; swipe steps split it; Legend in an Expand | map scrolly |
| `[sidecar/floating-panel]` | White panel over a full-bleed photo | panel-over-photo |
| Paragraphs with a chart, diagram, or infographic image | Readable column, then the image at full width with a caption and a full-size link | prose-figure |
| `[table]` of parallel items, two to four short parallel paragraphs | Numbered cards | cards |
| A sentence that lists goals or themes | One tile each, with a simple stroke icon | tiles |
| `[big number]`, a headline statistic in the text | Stat tiles; a spelled-out unit goes in `<small>` | tiles (stats) |
| `> quote` | Pull quote | tiles (blockquote) |
| `[bullet-list]` or `[numbered-list]` next to a `[gallery]` or `[carousel]` | List beside an image grid with a label and credit on each image | list-gallery |
| `[swipe]` of two images | Before and after slider | compare |
| `[timeline]` | Horizontal timeline that marks finished phases and "We are here" from today's date | timeline |
| `[embed] link` or `pdf` card, `[button]` to another site | Link cards | links |
| `[embed] video`, `[video]` | 16:9 frame or a `<video>` element | video |
| `[embed]` Survey123 | Click-to-load iframe plus "open in a new tab" | survey |
| `[credits]`, `[attribution]`, logo images | Stay informed, contact, logo strip, footer | closing |
| `[express map]` | No web map behind it: a static image, or a small MapView with graphics | (by hand) |
| `[code block]` | Usually leave it out; it is author notes | none |

### 3. Prepare images

Pick the images the page uses and give them names that say what they show. Then write a plan CSV
(`source,name,max_width`) and run:

```bash
python -I <skill>/scripts/prep_images.py <scratch>/story/images <site>/img/<page> --plan plan.csv
```

It resizes, applies EXIF orientation, strips EXIF (drone photos carry GPS), flattens to
progressive JPEG (keep `.png` names for logos), and flags files over 600 KB. It also flags any source
much narrower than its planned width: place that image smaller (in a split or a gallery, not
full-bleed) rather than stretching it. Target widths: hero 2,000, sidecars and scrolly 1,600 to
1,800, gallery 900, charts at their native size. A page of about 15 images lands near 4 MB, which is
fine because everything below the hero lazy-loads and the hero gets `fetchpriority="high"`.

### 4. Build

Start from `assets/template.html`, keep the blocks you mapped, and delete the rest along with
their CSS and JS groups. Fill the copy from the outline.

**Copy**
- **Keep the agency's words.** It is approved public copy, so edit for house style, not voice.
- **House style** (trpa-brand): no em or en dashes (use a colon or rewrite), "to" for ranges ("2005
  to 2018", "Spring to summer 2026"), "and" for "&", "percent" for "%", "for example" for "e.g.",
  "U.S.", Oxford commas, one to nine spelled out, abbreviated months with dates (Jan. 1, 2026), and
  sentence-case headings and captions. Fix the comma splices and typos the story map let through.
- **Headings say the point.** Pair a short kicker (the story's own heading, like "Goals") with an h2
  that says something ("What the plan aims to do").
- **Missing pieces get defaults.** With no item description, write a one-sentence lede from the
  opening paragraph. With no survey, point the top-bar button at the story's main action (the report,
  a sign-up) or drop it. A slideshow intro with no photo of its own reuses the first slide's image.
- **Report numbers as written**, even when the text and a chart disagree. List the mismatch for
  the user instead of choosing one.

**Images**
- **Alt text for every image**, written from the image itself, because story maps rarely carry it.
  Images behind a sticky crossfade or a map overlay are decorative (`alt=""`); their inline phone
  copies carry the alt text.
- **Credits stay with their image** ("Photo: Sierra Sun" in the caption or corner), including the
  ones the extractor found in panel text.
- **Charts and infographics stay images.** Put the numbers a reader needs in the paragraph or alt
  text, link the full-size file, and rely on the block's "Open full size" link on phones, where the
  image's own text is too small to read.

**Names and contacts**
- TRPA repos keep staff names out of committed files, and that includes bylines. Name the agency or
  program and link trpa.gov/contact. Tell the user what you swapped in case they want a named
  contact back.

**Interactive blocks**
- **Survey123**: the story's embed URL uses `embed=jsapi`, which expects the story map host to drive
  it and shows nothing in a plain iframe. Use the extractor's `survey_iframe`
  (`/share/<id>?portalUrl=...&embed=fullscreen&hide=footer,theme`) and `survey_share` for the
  new-tab link. Open the form once to describe what it asks.
- **Map scrolly**: each map step copies its `[webmap]` outline line into data attributes (the block's
  comment lists them all):
  - `data-webmap`, `data-lat`, `data-lon`, and `data-scale`
  - `data-layers` and `data-layers-off`, with layer titles separated by `|`. List both every time,
    because visibility carries over between steps on the same map.
  - Photo steps use `data-figure`.
  - Swipe steps use `data-swipe-leading` and `data-swipe-trailing`, plus `data-swipe-webmap` when
    the right side comes from a different web map, and `data-swipe-labels`.

  Leave "will not load" layers out. The swipe skips them anyway, because the Swipe widget throws on a
  failed layer. The block loads ArcGIS Maps SDK 4.31 only when the page has a map, and it never
  scroll-zooms the map.
- **Top-bar underline**: when one story section becomes two page sections, give the second
  `data-nav="<first id>"`.
- **Social preview**: `og:image` needs an absolute URL on the final host.
- **Timeline**: give each phase `data-from` and `data-to` (YYYY-MM) so the current phase marks itself.

If the page shares a site with ArcGIS pages that also load Plotly or AG Grid, load those before
the ArcGIS script (trpa-dashboard-stack covers the AMD conflict).

### 5. Wire it into the site

- Add the page to the site's Pages menu or index on every page that has one. When the page
  becomes the new Home, relabel the old landing page ("All pages") rather than deleting it.
- Record the page in the repo's CLAUDE.md, including where images live and which preview server
  can reach it. A preview server rooted at a subfolder cannot serve a root `index.html`.

### 6. Verify

Serve the repo locally, then:

1. Run the link check. It requests every same-origin `href` and `src`, confirms each `#anchor` has
   a matching id, lists images with no `alt`, and flags a relative `og:image`. Leftover template
   placeholders show up as failures. Add `--external` to request off-site links too.

   ```bash
   python -I <skill>/scripts/check_links.py http://localhost:<port>/<path>/index.html
   ```

2. Check the console for errors. A dead layer from step 1 logs one here, so that error is expected.
3. At desktop width (1,440), scroll the page. Check the hero, the section underline, and each scrolly step.
4. At phone width (375), confirm **no horizontal scroll**. The top bar is the usual culprit: the
   wordmark hides under 440 px so the logo, button, and Pages menu fit. Open the Pages menu and check
   that it fits too.
5. Check each map step's state from the console. Find the view by its container, because
   `View.views` is not in page order:

   ```js
   const sec = document.getElementById("map-story");  // the map section's id
   require(['esri/views/View'], V => console.log(V.views.find(v => sec.contains(v.container))))
   ```

   Compare its web map id, scale, visible layer titles, and whether a swipe is up against the step's
   data attributes.

Known preview-pane limits, so you don't chase phantom bugs:
- WebGL map canvases and cross-origin iframes (Survey123) can screenshot blank while working.
  Confirm with the view's state or the iframe's load event.
- The pane may not run render frames, so IntersectionObserver callbacks never fire, until you take
  a screenshot. Screenshot, then read the step state.
- A screenshot can catch a crossfade or a map that is still loading tiles. Wait a few seconds and
  take it again before calling it broken.

### 7. Hosting and the URL

GitHub Pages serves `<org>.github.io/<repo>/` or a custom domain or subdomain set in the repo
(a CNAME at DNS, which DTS handles for trpa.gov). It cannot serve a path on someone else's domain.
A link like `trpa.gov/<project>` is a redirect configured on trpa.gov's web server. Check it with
`curl -sIL <url>` and look for `301` and `location:`. Going live means having whoever runs trpa.gov
retarget that redirect to the Pages URL, with no DNS change. Pointing a public link at the site
publishes it broadly, so leave the timing to the user and mention any draft pages it links to.

### 8. Report

Lead with where the page is and how it was verified. Then list what needs the user's eye:

- copy you retitled, merged, or edited beyond house style, and any new copy you wrote (lede, kickers, stat labels)
- photos credited to news outlets or other third parties, and photos with no credit at all: TRPA
  should confirm reuse rights before the page goes public, because a standalone site is more visible
  than the story map was
- layers that will not load and the services behind them, and any web map that is not public
- number or attribution mismatches between the text and its charts, and data that is dated
- commercial vendors named in the copy (TRPA public pages avoid naming them)
- the contact and byline swap, unpublished draft changes, and the redirect step and who makes it

## Files

- `scripts/extract_storymap.py`: story, collection, or briefing to `outline.md`, `manifest.json` (with per-layer health), and `images/`
- `scripts/prep_images.py`: resize, strip EXIF, rename from a plan CSV, flag heavy and undersized images (needs Pillow, which `arcgispro-py3` includes; the other two scripts are standard library)
- `scripts/check_links.py`: links, images, anchors, alt text, and `og:image` on the served page
- `assets/template.html`: every block, labeled, tested at 1,440 and 375 px against live TRPA web maps
- `references/storymap-json.md`: the story JSON structure, for blocks the extractor does not know
