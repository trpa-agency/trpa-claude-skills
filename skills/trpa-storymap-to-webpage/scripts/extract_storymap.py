"""Pull an ArcGIS StoryMap (story, collection, or briefing) into a readable outline plus its media.

Reads the published story JSON through the ArcGIS REST API, walks every block in reading order
(following the node references that map tours, swipes, briefing slides, and action buttons keep in
their data, not their children), downloads the images the story uses, and requests every web map
layer's service once so dead or secured layers surface now instead of in the browser.

Usage (run with -I; the downloads are untrusted data):
    python -I extract_storymap.py <story-url | vanity-url | item-id> --out <empty-dir>
        [--portal https://www.arcgis.com] [--no-images] [--videos]

A private story needs a token in the ARCGIS_TOKEN environment variable (never on the command line).

Writes to --out:
    outline.md      every block in reading order: headings, text, lists, tables, images with their
                    files, captions, credits, and alt text, sidecars and slides, web maps with
                    viewpoint and layers, tours, swipes, timelines, embeds, buttons, credits
    manifest.json   item metadata, images, web maps, embeds, links, house-style flags, orphan nodes
    raw/            the item metadata and story JSON exactly as served
    images/         original media files, named <story id prefix>_<resource id>
"""
import argparse
import html
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "trpa-storymap-to-webpage/1.0"}
ID_RE = re.compile(r"(?<![0-9a-f])([0-9a-f]{32})(?![0-9a-f])")
TEXT_PREFIX = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "quote": "> ",
               "large-paragraph": "", "paragraph": ""}
# House-style problems worth fixing in the rebuilt copy (trpa-brand writing style)
STYLE_PATTERNS = [(name, re.compile(p)) for name, p in (
    ("em dash", "—"), ("en dash", "–"), ("ampersand", "&"), ("percent sign", "%"),
    ("double space", "  "), ("hyphenated year range", r"\b(?:19|20)\d\d ?- ?(?:(?:19|20)?\d\d)\b"),
    ("e.g. or i.e.", r"\b(?:e\.g\.|i\.e\.)"))]
CREDIT_RE = re.compile(r"(?i)\b(?:photos?|images?|pictures?)\b[^.\n]{0,40}\b(?:by|courtesy|credit)|courtesy of|\bcredits?:")


# ---------------------------------------------------------------- fetching

def http_get(url, binary=False):
    token = os.environ.get("ARCGIS_TOKEN")
    if token and "/sharing/rest/" in url:
        url += ("&" if "?" in url else "?") + "token=" + urllib.parse.quote(token)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
        return (body, r.geturl()) if binary else (body.decode("utf-8"), r.geturl())


def rest_json(portal, path):
    text, _ = http_get(f"{portal}/sharing/rest/{path}{'&' if '?' in path else '?'}f=json")
    d = json.loads(text)
    if isinstance(d, dict) and "error" in d:
        err = d["error"]
        raise PermissionError(f"{path}: {err.get('code')} {err.get('message')}"
                              " (private or deleted; share it publicly or set ARCGIS_TOKEN)")
    return d


def resolve(source, portal_override):
    """Return (portal, item id, final url) for an item id, story URL, or vanity redirect."""
    if ID_RE.fullmatch(source.strip().lower()):
        return portal_override or "https://www.arcgis.com", source.strip().lower(), None
    url = source if "://" in source else "https://" + source
    try:
        _, final = http_get(url)
    except urllib.error.HTTPError as e:
        final = e.geturl() or url
    m = ID_RE.search(final.lower()) or ID_RE.search(url.lower())
    if not m:
        sys.exit(f"No 32-character item id in {url} (resolved to {final}).")
    portal = portal_override
    if not portal:
        p = urllib.parse.urlparse(final)
        if "/apps/storymaps/" in p.path and not p.netloc.endswith("arcgis.com"):
            portal = f"{p.scheme}://{p.netloc}{p.path.split('/apps/storymaps/')[0]}"  # Enterprise
        else:
            portal = "https://www.arcgis.com"
    return portal, m.group(1), final


# ---------------------------------------------------------------- text

def lists_to_md(s):
    """<li> items to '- ' lines, indenting nested <ul>/<ol> levels."""
    out, depth = [], 0
    for tok in re.split(r"(</?(?:ul|ol)[^>]*>|<li[^>]*>|</li>)", s, flags=re.I):
        low = tok.lower()
        if re.match(r"<(ul|ol)\b", low):
            depth += 1
        elif re.match(r"</(ul|ol)\b", low):
            depth = max(0, depth - 1)
        elif low.startswith("<li"):
            out.append("\n" + "  " * depth + "- ")  # story maps leave the top level unwrapped
        elif low != "</li>":
            out.append(tok)
    return "".join(out)


def clean_text(s):
    """Story map rich text to markdown-ish plain text."""
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s)  # source whitespace carries no meaning
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = lists_to_md(s)
    s = re.sub(r"</?(strong|b)>", "**", s, flags=re.I)
    s = re.sub(r"</?(em|i)>", "*", s, flags=re.I)
    s = re.sub(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    lines = [ln.rstrip() for ln in s.splitlines()]
    lines = [ln if re.match(r"\s+- ", ln) else ln.strip() for ln in lines]
    return "\n".join(ln for ln in lines if ln).strip()


def merc_to_lonlat(x, y):
    lon = x / 6378137.0 * 180 / math.pi
    lat = (2 * math.atan(math.exp(y / 6378137.0)) - math.pi / 2) * 180 / math.pi
    return round(lon, 5), round(lat, 5)


def safe_name(s):
    return re.sub(r"[^A-Za-z0-9._-]", "_", s)


# ---------------------------------------------------------------- the walker

class Story:
    def __init__(self, portal, item_id, out, args, manifest, label=""):
        self.portal, self.id, self.out, self.args, self.m = portal, item_id, out, args, manifest
        self.label = label
        self.item = rest_json(portal, f"content/items/{item_id}")
        self.data = rest_json(portal, f"content/items/{item_id}/data")
        os.makedirs(os.path.join(out, "raw"), exist_ok=True)
        for name, obj in (("item", self.item), ("data", self.data)):
            with open(os.path.join(out, "raw", f"{item_id}_{name}.json"), "w", encoding="utf-8") as f:
                json.dump(obj, f, indent=1, ensure_ascii=False)
        self.nodes = self.data.get("nodes", {})
        self.res = self.data.get("resources", {})
        self.seen = set()
        self.lines = []

    # -- helpers
    def emit(self, depth, text):
        pad = "  " * depth
        for i, line in enumerate(str(text).splitlines() or [""]):
            self.lines.append(pad + ("" if i == 0 else "  ") + line)

    def flag_style(self, text, where):
        text = re.sub(r"\]\([^)]*\)", "]", text)  # link targets are not copy
        for name, pat in STYLE_PATTERNS:
            hits = list(pat.finditer(text))
            if hits:
                f = self.m["style_flags"].setdefault(name, {"count": 0, "samples": []})
                f["count"] += len(hits)
                if len(f["samples"]) < 4:
                    i = hits[0].start()
                    f["samples"].append(f"{where}: ...{text[max(0, i - 40):i + 40]}...")
        # Credits often live in panel text or captions rather than the image's attribution field
        for m in CREDIT_RE.finditer(text):
            line = text[max(0, text.rfind("\n", 0, m.start()) + 1):].split("\n")[0]
            self.m["credit_text"].append({"node": where, "text": line[:200]})
            break

    def media_file(self, rid, kind="image"):
        """Download an image or video resource; return its outline label."""
        r = self.res.get(rid)
        if not r:
            return f"(missing resource {rid})"
        d = r.get("data", {})
        size = f" {d.get('width')}x{d.get('height')}" if d.get("width") else ""
        if d.get("provider") == "item-resource" or d.get("resourceId"):
            url = f"{self.portal}/sharing/rest/content/items/{self.id}/resources/{d['resourceId']}"
        else:
            url = d.get("src") or d.get("url") or ""
        fname = safe_name(f"{self.id[:8]}_{d.get('resourceId') or os.path.basename(urllib.parse.urlparse(url).path) or rid}")
        entry = {"resource": rid, "story": self.id, "file": f"images/{fname}", "url": url,
                 "width": d.get("width"), "height": d.get("height"), "kind": kind}
        want = (kind == "image" and not self.args.no_images) or (kind == "video" and self.args.videos)
        dest = os.path.join(self.out, "images", fname)
        if want and url and not os.path.exists(dest):
            try:
                body, _ = http_get(url, binary=True)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(body)
            except Exception as e:  # keep going; the outline records the failure
                entry["error"] = str(e)
        if os.path.exists(dest):
            entry["bytes"] = os.path.getsize(dest)
        if not any(e["resource"] == rid and e["story"] == self.id for e in self.m["media"]):
            self.m["media"].append(entry)
        return f"{entry['file']}{size}" + (" (not downloaded)" if not os.path.exists(dest) else "")

    def webmap(self, rid, node_data=None):
        # The block's own viewpoint and layer list override the web map resource's saved state;
        # that is what gives each sidecar slide its own view.
        d = dict(self.res.get(rid, {}).get("data", {}))
        d.update({k: v for k, v in (node_data or {}).items()
                  if k in ("viewpoint", "center", "zoom", "extent", "mapLayers") and v})
        wid = d.get("itemId")
        info = {"resource": rid, "story": self.id, "itemId": wid, "itemType": d.get("itemType")}
        try:
            meta = rest_json(self.portal, f"content/items/{wid}")
            info.update(title=meta.get("title"), access=meta.get("access"))
            info["layer_health"] = self.layer_health(wid)
        except Exception as e:
            info.update(access="unreadable", error=str(e))
        info["dead_layers"] = [f"{h['title']} ({h['status']})" for h in info.get("layer_health", [])
                               if h["status"] in ("dead", "secured")]
        vp = d.get("viewpoint") or {}
        tg = vp.get("targetGeometry") or d.get("center") or {}
        if "x" in tg and "y" in tg:
            sr = (tg.get("spatialReference") or {}).get("wkid")
            lon, lat = merc_to_lonlat(tg["x"], tg["y"]) if sr in (102100, 3857) else (tg["x"], tg["y"])
            info.update(center=[lon, lat], scale=round(vp.get("scale") or 0) or None, zoom=d.get("zoom"))
        layers = d.get("mapLayers") or []
        info["layers_on"] = [l.get("title") for l in layers if l.get("visible")]
        info["layers_off"] = [l.get("title") for l in layers if not l.get("visible")]
        self.m["webmaps"].append(info)
        where = f" at {info['center'][1]}, {info['center'][0]}" if info.get("center") else ""
        scale = f" 1:{info['scale']:,}" if info.get("scale") else ""
        dead = f"; LAYERS THAT WILL NOT LOAD: {', '.join(info['dead_layers'])}" if info["dead_layers"] else ""
        off = f"; off: {', '.join(info['layers_off'])}" if info["layers_off"] else ""
        return (f"web map {wid} \"{info.get('title')}\" ({info.get('access')}){scale}{where}; "
                f"layers on: {', '.join(info['layers_on']) or 'as saved'}{off}{dead}")

    def layer_health(self, wid):
        """Request every operational layer's service once; a dead one breaks the rebuilt map too."""
        if wid in self.m["_health"]:
            return self.m["_health"][wid]
        out = []

        def walk(layers):
            for l in layers or []:
                url = l.get("url") or l.get("styleUrl")
                if url:
                    out.append({"title": l.get("title"), "url": url, "status": self.service_status(url)})
                elif l.get("itemId"):
                    out.append({"title": l.get("title"), "url": None, "status": "by item"})
                elif l.get("layerType") != "GroupLayer":
                    out.append({"title": l.get("title"), "url": None, "status": "embedded"})
                walk(l.get("layers"))

        try:
            walk(rest_json(self.portal, f"content/items/{wid}/data").get("operationalLayers"))
        except Exception as e:
            out.append({"title": "(web map JSON)", "url": None, "status": "dead", "error": str(e)})
        self.m["_health"][wid] = out
        return out

    def service_status(self, url):
        if url in self.m["_status"]:
            return self.m["_status"][url]
        probe = url + ("&" if "?" in url else "?") + "f=json"
        try:
            text, _ = http_get(probe)
            body = json.loads(text) if text.strip().startswith("{") else {}
            code = (body.get("error") or {}).get("code")
            status = "ok" if "error" not in body else "secured" if code in (403, 498, 499) else "dead"
        except urllib.error.HTTPError as e:
            status = "secured" if e.code in (401, 403) else "dead"
        except Exception:
            status = "dead"
        self.m["_status"][url] = status
        return status

    # -- node rendering
    def render(self, nid, depth):
        if nid in self.seen or nid not in self.nodes:
            return
        self.seen.add(nid)
        n = self.nodes[nid]
        t, d, kids = n["type"], n.get("data", {}) or {}, n.get("children", [])
        anchor = f"  {{#{nid}}}" if nid in self.m["_nav_targets"] else ""

        if t == "text":
            txt = clean_text(d.get("text", ""))
            if not txt:
                return
            self.flag_style(txt, nid)
            kind = d.get("type", "paragraph")
            if kind in ("bullet-list", "numbered-list"):
                if kind == "numbered-list":
                    txt = "\n".join(re.sub(r"^- ", f"{i + 1}. ", l) for i, l in enumerate(txt.splitlines()))
                self.emit(depth, f"[{kind}]{anchor}\n{txt}")
            else:
                self.emit(depth, f"{TEXT_PREFIX.get(kind, '')}{txt}{anchor}"
                          + ("  [large]" if kind == "large-paragraph" else ""))
        elif t == "image":
            bits = [self.media_file(d.get("image"))]
            for k in ("caption", "alt", "attribution"):
                if d.get(k):
                    bits.append(f'{k}="{clean_text(d[k])}"')
            if d.get("caption"):
                self.flag_style(clean_text(d["caption"]), nid)
            if d.get("expressImage"):
                bits.append("annotated version: " + self.media_file(d["expressImage"]))
            self.emit(depth, "[image] " + " ".join(bits) + anchor)
        elif t == "video":
            line = "[video] " + self.media_file(d.get("video"), "video")
            if d.get("thumbnail"):
                line += " poster: " + self.media_file(d["thumbnail"])
            self.emit(depth, line + (f' caption="{clean_text(d["caption"])}"' if d.get("caption") else ""))
        elif t == "webmap":
            cap = f' caption="{clean_text(d["caption"])}"' if d.get("caption") else ""
            self.emit(depth, "[webmap] " + self.webmap(d.get("map"), d) + cap
                      + (" legend shown" if d.get("isShowingLegend") else "") + anchor)
        elif t == "expressmap":
            self.emit(depth, "[express map] drawn in the StoryMaps builder; no web map item behind it."
                      " Rebuild as a static image or a small MapView with graphics.")
        elif t in ("storycover", "collection-cover"):
            bits = [f"{k}: {clean_text(d[k])}" for k in ("title", "summary", "byline") if (d.get(k) or "").strip()]
            if (d.get("byline") or "").strip():
                self.m["bylines"].append(clean_text(d["byline"]))
            self.emit(depth, f"[cover {d.get('type', '')}] " + " | ".join(bits))
            for c in kids:
                self.render(c, depth + 1)
        elif t == "navigation":
            labels = []
            for link in d.get("links", []):
                tgt = self.nodes.get(link.get("nodeId"), {})
                label = clean_text((tgt.get("data") or {}).get("text", "")) or link.get("nodeId")
                labels.append(label + (" (hidden)" if link.get("isHidden") else ""))
            self.emit(depth, "[navigation] " + " | ".join(labels))
        elif t == "immersive":
            sub = "/".join(x for x in (d.get("type"), d.get("subtype")) if x)
            self.emit(depth, f"[{sub} panel={d.get('narrativePanelPosition', '-')} "
                             f"size={d.get('narrativePanelSize', '-')}, {len(kids)} slide(s)]{anchor}")
            for i, c in enumerate(kids, 1):
                self.emit(depth + 1, f"slide {i}")
                self.render(c, depth + 2)
        elif t == "immersive-slide":
            panels = [c for c in kids if self.nodes.get(c, {}).get("type") == "immersive-narrative-panel"]
            media = [c for c in kids if c not in panels]
            for c in media:
                self.emit(depth, "media:")
                self.render(c, depth + 1)
            for c in panels:
                self.render(c, depth)
        elif t == "immersive-narrative-panel":
            pos = d.get("position") or ""
            self.emit(depth, f"panel{(' ' + pos) if pos else ''}:")
            for c in kids:
                self.render(c, depth + 1)
        elif t == "tour":
            self.emit(depth, f"[map tour {d.get('type')}/{d.get('subtype')}, {len(d.get('places', []))} places]")
            geoms = (self.nodes.get(d.get("map"), {}).get("data") or {}).get("geometries", {})
            self.seen.add(d.get("map"))
            for i, p in enumerate(d.get("places", []), 1):
                g = geoms.get(p.get("featureId"), {})
                pt = (g.get("nodes") or [{}])[0]
                loc = f" at {round(pt['lat'], 5)}, {round(pt['long'], 5)}" if "lat" in pt else ""
                title = clean_text((self.nodes.get(p.get("title"), {}).get("data") or {}).get("text", ""))
                self.seen.add(p.get("title"))
                self.emit(depth + 1, f"place {i}: {title}{loc}")
                for c in [p.get("media")] + p.get("contents", []):
                    if c:
                        self.render(c, depth + 2)
        elif t == "swipe":
            self.emit(depth, "[swipe] left/right:")
            for k in sorted((d.get("contents") or {}).keys()):
                self.render(d["contents"][k], depth + 1)
        elif t in ("gallery", "carousel"):
            cap = f' caption="{clean_text(d["caption"])}"' if d.get("caption") else ""
            if cap:
                self.flag_style(clean_text(d["caption"]), nid)
            self.emit(depth, f"[{t} {d.get('galleryLayout', '')}, {len(kids)} images]{cap}")
            for c in kids:
                self.render(c, depth + 1)
        elif t == "timeline":
            self.emit(depth, f"[timeline {d.get('type', '')}, {len(kids)} events]")
            for i, c in enumerate(kids, 1):
                self.emit(depth + 1, f"event {i}")
                for cc in self.nodes.get(c, {}).get("children", []):
                    self.render(cc, depth + 2)
                self.seen.add(c)
        elif t == "table":
            cells = d.get("cells", {})
            rows = []
            for r in sorted(cells, key=int):
                row = cells[r]
                rows.append("| " + " | ".join(clean_text(row[c].get("value", "")) for c in sorted(row, key=int)) + " |")
            if rows:
                ncol = rows[0].count("|") - 1
                rows.insert(1, "|" + "---|" * ncol)
            self.emit(depth, f"[table {d.get('numRows')}x{d.get('numColumns')}]\n" + "\n".join(rows))
        elif t in ("button", "action-button"):
            link = d.get("link") or ""
            if link:
                self.m["links"].append({"text": d.get("text"), "url": link, "story": self.id})
            swap = (n.get("dependents") or {}).get("actionMedia")
            target = link or ("swaps the slide's media to:" if swap else "(story action, no link)")
            self.emit(depth, f"[{t}] \"{d.get('text')}\" -> {target}")
            if swap:  # action buttons hold their media outside the children list
                self.render(swap, depth + 1)
        elif t == "embed":
            self.emit(depth, "[embed] " + self.embed(d))
        elif t == "large-number":
            self.emit(depth, f"[big number] {d.get('title')} {clean_text(d.get('description', ''))}"
                             f" (icon {d.get('icon')})")
        elif t == "code":
            self.emit(depth, "[code block]\n" + html.unescape(d.get("content", ""))[:600])
        elif t == "separator":
            self.emit(depth, "---")
        elif t == "credits":
            self.emit(depth, "[credits]")
            for c in kids:
                self.render(c, depth + 1)
        elif t == "attribution":
            label, value = clean_text(d.get("content", "")), clean_text(d.get("attribution", ""))
            if label or value:
                self.emit(depth, f"[attribution] {label}: {value}")
        elif t == "briefing-slide":
            # Slides point at their title, subtitle, and panels through data, like tours do
            self.emit(depth, f"[briefing slide, layout {d.get('layout')}{', ' + d['sublayout'] if d.get('sublayout') else ''}]")
            for k in ("title", "subtitle"):
                if d.get(k):
                    self.render(d[k], depth + 1)
            for k in sorted(d.get("contents") or {}, key=str):
                v = d["contents"][k]
                self.emit(depth + 1, f"panel {int(k) + 1}:")
                for c in (v if isinstance(v, list) else [v]):
                    self.render(c, depth + 2)
            for c in kids:
                self.render(c, depth + 1)
        elif t in ("story", "briefing", "briefing-ui", "collection", "collection-nav", "collection-map",
                   "collection-ui"):
            for c in kids:
                self.render(c, depth)
        else:
            self.emit(depth, f"[{t}] " + json.dumps(d, ensure_ascii=False)[:400])
            for c in kids:
                self.render(c, depth + 1)

    def embed(self, d):
        url = d.get("url") or d.get("embedSrc") or ""
        info = {"story": self.id, "type": d.get("embedType"), "title": d.get("title"), "url": url,
                "display": d.get("display")}
        line = f"{d.get('embedType')} \"{d.get('title') or ''}\" {url}"
        if "survey123.arcgis.com" in url:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            m = ID_RE.search(url)
            sid = (q.get("id") or [None])[0] or (m.group(1) if m else None)
            portal = (q.get("portalUrl") or [""])[0]
            base = f"https://survey123.arcgis.com/share/{sid}" + (f"?portalUrl={portal}" if portal else "")
            info["survey_share"] = base
            info["survey_iframe"] = base + ("&" if portal else "?") + "embed=fullscreen&hide=footer,theme"
            line += f"\n  Survey123 form {sid}: iframe {info['survey_iframe']}"
        if d.get("caption") or d.get("description"):
            line += f'\n  text="{clean_text(d.get("caption") or d.get("description"))}"'
        self.m["embeds"].append(info)
        return line

    def walk(self):
        it = self.item
        kw = it.get("typeKeywords", [])
        status = "published; the draft has unpublished changes" if "smstatusunpublishedchanges" in kw else "published"
        kind = ("collection" if "storymapcollection" in kw else "briefing" if "storymapbriefing" in kw else "story")
        self.m["items"].append({"id": self.id, "title": it.get("title"), "kind": kind, "access": it.get("access"),
                                "owner": it.get("owner"), "modified": it.get("modified"), "status": status,
                                "snippet": it.get("snippet"), "description": clean_text(it.get("description") or ""),
                                "url": it.get("url"), "label": self.label})
        if "nodes" not in self.data:
            self.lines.append(f"# {it.get('title')}\nClassic Story Map ({it.get('type')}): no node tree. "
                              f"Read raw/{self.id}_data.json directly.")
            return self.lines
        for n in self.nodes.values():
            if n["type"] == "navigation":
                self.m["_nav_targets"].update(l.get("nodeId") for l in n.get("data", {}).get("links", []))
        theme = next((r["data"].get("themeId") for r in self.res.values() if r["type"] == "story-theme"), None)
        self.lines += [f"# {self.label}{it.get('title')}",
                       f"{kind}, item {self.id}, {status}, theme {theme}",
                       f"Source: {it.get('url')}", ""]
        if kind == "collection":
            self.walk_collection()
        else:
            self.render(self.data["root"], 0)
        skip = {"story-theme", "collection-map", "tour-map"}
        orphans = [k for k, v in self.nodes.items() if k not in self.seen and v["type"] not in skip
                   and not (v["type"] == "text" and not clean_text((v.get("data") or {}).get("text", "")))]
        if orphans:
            self.m["orphan_nodes"][self.id] = {k: self.nodes[k]["type"] for k in orphans}
        return self.lines

    def walk_collection(self):
        root = self.nodes[self.data["root"]]
        self.seen.add(self.data["root"])
        ui_id = next((c for c in root.get("children", []) if self.nodes[c]["type"] == "collection-ui"), None)
        self.seen.add(ui_id)
        ui = self.nodes.get(ui_id, {})
        for c in ui.get("children", []):
            self.render(c, 0)  # cover and its item descriptions
        for i, entry in enumerate(ui.get("data", {}).get("items", []), 1):
            thumb = f" thumbnail: {self.media_file(entry['customThumbnail'])}" if entry.get("customThumbnail") else ""
            r = self.res.get(entry.get("resourceId"), {}).get("data", {})
            child = None
            if r.get("itemType") == "StoryMap" and r.get("itemId"):
                child = Story(self.portal, r["itemId"], self.out, self.args, self.m, label=f"Item {i}: ")
            title = entry.get("customTitle") or (child.item.get("title") if child else "")
            self.lines += ["", f"## Collection item {i}: {title}{thumb}"]
            if entry.get("customSummary"):
                self.lines.append(f"summary: {entry['customSummary']}")
            if entry.get("nodeId"):
                self.render(entry["nodeId"], 0)
            elif child:
                self.lines += ["", *child.walk()]
            elif r:
                self.lines.append(f"[{r.get('itemType')}] item {r.get('itemId')}: "
                                  f"{self.portal}/home/item.html?id={r.get('itemId')}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", help="story or collection URL, vanity URL that redirects to one, or item id")
    ap.add_argument("--out", required=True, help="output folder (new or empty)")
    ap.add_argument("--portal", help="portal base, e.g. https://maps.trpa.org/portal (default from the URL)")
    ap.add_argument("--no-images", action="store_true", help="skip image downloads")
    ap.add_argument("--videos", action="store_true", help="also download hosted video files")
    args = ap.parse_args()

    if os.path.isdir(args.out) and os.listdir(args.out):
        sys.exit(f"{args.out} is not empty; give a new folder so downloads stay separate.")
    os.makedirs(args.out, exist_ok=True)

    portal, item_id, final = resolve(args.source, args.portal)
    manifest = {"source": args.source, "resolved_url": final, "portal": portal, "items": [], "media": [],
                "webmaps": [], "embeds": [], "links": [], "style_flags": {}, "credit_text": [],
                "bylines": [], "orphan_nodes": {}, "_nav_targets": set(), "_health": {}, "_status": {}}
    try:
        lines = Story(portal, item_id, args.out, args, manifest).walk()
    except PermissionError as e:
        sys.exit(str(e))
    for k in ("_nav_targets", "_health", "_status"):
        manifest.pop(k)

    with open(os.path.join(args.out, "outline.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)

    got = [m for m in manifest["media"] if m.get("bytes")]
    print(f"{manifest['items'][0]['title']} ({manifest['items'][0]['kind']}, {len(manifest['items'])} item(s))")
    if final:
        print(f"resolved {args.source} -> {final}")
    print(f"outline: {os.path.join(args.out, 'outline.md')} ({len(lines)} lines)")
    print(f"media: {len(got)} of {len(manifest['media'])} downloaded, "
          f"{sum(m['bytes'] for m in got) / 1e6:.1f} MB")
    warned = set()
    for w in manifest["webmaps"]:
        if w["itemId"] in warned:
            continue
        warned.add(w["itemId"])
        if w.get("access") != "public":
            print(f"WARNING web map {w['itemId']} is {w.get('access')}: an anonymous page cannot load it")
        elif w.get("dead_layers"):
            print(f"WARNING web map {w['itemId']} \"{w.get('title')}\" has layers that will not load: "
                  f"{', '.join(w['dead_layers'])}")
    for it in manifest["items"]:
        if "unpublished" in it["status"]:
            print(f"NOTE {it['id']} has unpublished draft changes; only the published version is readable")
        if not it["description"] and it["kind"] != "collection":
            print(f"NOTE {it['id']} has no item description: write the hero lede and meta description "
                  "from the opening paragraph")
    for b in manifest["bylines"]:
        print(f"NOTE byline \"{b}\": bylines are usually staff names; the page credits the agency instead")
    if manifest["credit_text"]:
        print(f"credits: {len(manifest['credit_text'])} photo credit(s) sit in text or captions, not image "
              "attributions; listed in manifest.json")
    for name, f in manifest["style_flags"].items():
        print(f"style: {f['count']} {name}(s)")
    if manifest["orphan_nodes"]:
        print(f"orphans: {sum(len(v) for v in manifest['orphan_nodes'].values())} unreferenced node(s), "
              "usually deleted blocks; listed in manifest.json")


if __name__ == "__main__":
    main()
