# ArcGIS StoryMaps JSON, as the extractor reads it

Read this when `outline.md` shows a block as raw JSON, when the extractor fails on a story, or
for a classic Story Map. Learned from TRPA's 38 public stories (Oct. 2026): 2,080 text nodes,
784 images, 140 web maps, 75 sidecars, 62 carousels, 20 swipes, 4 map tours, 3 collections,
1 briefing.

## Endpoints

Base is `https://www.arcgis.com/sharing/rest` for ArcGIS Online, including org subdomains like
`trpa.maps.arcgis.com`. For Enterprise it is `https://<host>/<webadaptor>/sharing/rest`. Add
`?f=json` and, for a private item, `&token=`.

| What | Path |
|---|---|
| Item metadata (title, description, typeKeywords, access) | `content/items/<id>` |
| Published story JSON | `content/items/<id>/data` |
| An image or video the story uploaded | `content/items/<id>/resources/<resourceId>` |
| Org search | `search?q=orgid:<orgId> AND type:"StoryMap"&num=100` |

`typeKeywords` tell the kind and state: `storymapcollection`, `storymapbriefing`,
`smstatusunpublishedchanges` (the draft is newer than what `/data` returns, and the draft file named
in `smdraftresourceid:` is readable only by the owner).

## Shape

```json
{ "root": "n-abc", "nodes": { "n-abc": { "type": "story", "children": ["n-..."], "data": {} } },
  "resources": { "r-xyz": { "type": "image", "data": { "resourceId": "file.jpg", "provider": "item-resource" } } },
  "actions": [ ... ] }
```

Reading order is a depth-first walk of `children` from `root`. **Several block types point at
other nodes through `data` instead of `children`**, so a children-only walk drops them:

| Block | Where its content is |
|---|---|
| `tour` | `data.places[]`: `title` (text node), `contents[]` (text nodes), `media` (image or carousel node), `featureId` (a point in the `tour-map` node's `data.geometries`, with `lat` and `long`) |
| `swipe` | `data.contents` = `{"0": leftNodeId, "1": rightNodeId}`. Of TRPA's 20 swipes, 16 pair two images, 2 pair one web map with different layers per side, and 2 pair two different web maps. |
| `briefing-slide` | `data.title`, `data.subtitle`, `data.contents` = `{"0": id or [ids], "1": ...}`; `layout` and `sublayout` (for example `section-double`, `3-7`) |
| `action-button` | `dependents.actionMedia` = the node that replaces the slide's media; the top-level `actions[]` says the same thing |
| `navigation` | `data.links[].nodeId` = heading nodes to anchor to; `isHidden` links are not shown |

Values beginning `r-` are resource ids. Values beginning `n-` are node ids.

## Node types

- `text`: `data.type` is one of `paragraph`, `large-paragraph`, `h2`, `h3`, `h4`, `quote`, `bullet-list`,
  or `numbered-list`. `data.text` is HTML with entities (`&apos;`, `&amp;`), `\xa0`, and `<li>` items with
  no outer `<ul>`, though nested `<ul>` occur.
- `image`: `data.image` points to the resource. Also `caption`, `alt` (rarely filled), and `attribution`
  (the credit). `expressImage` points to an annotated PNG version.
- `webmap`: `data.map` points to a resource `{itemId, itemType: "Web Map", viewpoint, center, zoom, extent, mapLayers}`.
  The node's own `viewpoint`, `center`, `extent`, and `mapLayers` override the resource's, which is how each
  sidecar slide gets its own view. `mapLayers` is `[{id, title, visible}]`. Coordinates are Web Mercator
  (wkid 102100); the extractor converts them with `merc_to_lonlat()`.
  The web map item's own `/data` holds `operationalLayers` (`title`, `url` or `styleUrl` or `itemId`,
  and nested `layers` for groups). The extractor requests each `url` with `?f=json`. A JSON `error` with
  code 403, 498, or 499 means secured. Any other error or a failed request means dead. maps.trpa.org
  also answers 499 for a service that does not exist, so a "secured" service-level URL may be
  removed. Its layer URLs answer 404 "Service not found" in that case. Of the
  seven web maps in the GHG emissions story, two had layers whose services were gone.
- `expressmap`: `data.map` points to a resource `{itemId: "expressmap_<n>.json"}`, a sketch map stored as an
  item resource with no web map behind it.
- `immersive`: `data.type` is `sidecar` (`subtype` is `docked-panel`, `floating-panel`, or `slideshow`) or `slideshow`.
  Its children are `immersive-slide` nodes, each holding one `immersive-narrative-panel` (text children,
  `position`) and one media node.
- `gallery` or `carousel`: image children, plus `caption` and `galleryLayout`.
- `timeline`: `timeline-event` children, each with text children (usually an h3 date and a paragraph).
- `table`: `data.cells[row][col].value` (HTML), `numRows`, and `numColumns`.
- `embed`: `embedType` is `link`, `pdf`, `rich`, or `video`. `url` is the target. `embedSrc` is the iframe source the
  story used. For video it is an embedly wrapper, so use the provider URL instead. `display` is `card` or
  `inline`.
- `video`: `data.video` points to an `.mp4` item resource and `data.thumbnail` to an image resource.
- `button`: `text` and `link`. `action-button`: `text`, with the action held in `dependents`.
- `large-number`: `title` (the number as text), `description`, and `icon`.
- `storycover`: `title`, `summary`, `byline`, and `type` (`full`, `sidebyside`, `minimal`), with an image child.
- `credits`: text and `attribution` children (`content` is the label and `attribution` the value).
- Collections: `collection` holds `collection-ui`, whose `data.items[]` each point to a `portal-item`
  story by `resourceId` or to an embed by `nodeId`, plus `customTitle`, `customSummary`, and
  `customThumbnail`. Its children are `collection-cover` and `collection-nav`.
- `separator`, `code` (author notes, rarely worth porting), and `story-theme` resources (`themeId`, such as `summit`).

## Classic Story Maps

Items of type "Web Mapping Application" with a "Story Map" keyword (Cascade, Journal, Series,
Tour) have no node tree. `/data` returns `values` with an app-specific layout: Cascade uses
`values.sections[]` with `foreground` and `background` blocks, Journal uses
`values.story.sections[]` with `content` HTML and `media`, and Series uses `values.story.entries[]`.
The extractor saves the raw JSON and stops, so read it directly and outline it by hand in the
same format.
