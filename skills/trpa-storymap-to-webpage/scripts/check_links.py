"""Check a rebuilt page served locally: links, images, anchors, alt text, and the social image.

Usage (run with -I):
    python -I check_links.py http://localhost:8012/path/index.html [--external]

Fetches the page, then requests every same-origin href and src (HEAD, falling back to GET),
confirms every #fragment link has a matching id, and lists images with no alt attribute.
--external also requests off-site links (slower; some sites refuse HEAD and scripted requests).
Exits 1 when anything fails so it can gate a commit.
"""
import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = {"User-Agent": "trpa-storymap-to-webpage/1.0"}
URL_ATTRS = {("a", "href"), ("img", "src"), ("link", "href"), ("script", "src"), ("iframe", "src"),
             ("source", "src"), ("video", "src"), ("video", "poster"), ("audio", "src")}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.no_alt, self.og_image = [], set(), [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for t, attr in URL_ATTRS:
            if tag == t and a.get(attr):
                self.refs.append((tag, a[attr]))
        if tag == "img" and "alt" not in a:
            self.no_alt.append(a.get("src", "?"))
        if tag == "meta" and a.get("property") == "og:image":
            self.og_image = a.get("content")


def status(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "GET" or e.code not in (403, 405, 501):
                return e.code
        except Exception as e:
            if method == "GET":
                return f"error: {e.__class__.__name__}"
    return "error"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("url")
    ap.add_argument("--external", action="store_true", help="also check off-site links")
    args = ap.parse_args()

    with urllib.request.urlopen(urllib.request.Request(args.url, headers=UA), timeout=30) as r:
        page = Page()
        page.feed(r.read().decode("utf-8", "replace"))
    origin = urllib.parse.urlparse(args.url)._replace(path="", query="", fragment="").geturl()

    bad, checked, skipped = [], {}, 0
    for tag, ref in page.refs:
        if ref.startswith(("mailto:", "tel:", "javascript:", "data:")) or ref == "#":
            continue
        if ref.startswith("#"):
            if ref[1:] not in page.ids:
                bad.append((tag, ref, "no element with that id"))
            continue
        full = urllib.parse.urljoin(args.url, ref)
        base, _, frag = full.partition("#")
        if not base.startswith(origin) and not args.external:
            skipped += 1
            continue
        if base not in checked:
            checked[base] = status(base)
        if checked[base] != 200:
            bad.append((tag, ref, checked[base]))
        elif frag and base == args.url.partition("#")[0] and frag not in page.ids:
            bad.append((tag, ref, "no element with that id"))

    print(f"{len(checked)} URL(s) checked, {skipped} external skipped (use --external), "
          f"{len(page.ids)} ids on the page")
    for tag, ref, why in bad:
        print(f"FAIL <{tag}> {ref}: {why}")
    for src in page.no_alt:
        print(f"ALT missing on <img src=\"{src}\">")
    if page.og_image and not page.og_image.startswith("http"):
        print(f"OG og:image is relative ({page.og_image}); link previews need an absolute URL")
    if not bad and not page.no_alt:
        print("all links, images, and anchors OK")
    sys.exit(1 if bad or page.no_alt else 0)


if __name__ == "__main__":
    main()
