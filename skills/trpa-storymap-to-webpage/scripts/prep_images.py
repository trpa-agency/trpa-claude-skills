"""Resize story map images for the web and strip their EXIF (drone photos often carry GPS).

Usage (run with -I):
    python -I prep_images.py <images-dir> <out-dir> [--plan plan.csv] [--max 1800] [--quality 74]

Without --plan every image becomes <stem>.jpg at most --max pixels wide.
With --plan, a CSV with columns source,name,max_width picks, renames, and sizes each image:

    source,name,max_width
    6b67742e_5462a284-f34c-4b75-9d8c-de5066bba236.jpeg,hero-shoreline-winter.jpg,2000
    6b67742e_M7p80NIkl8dXZJLtbWVZJ.png,partner-logos.png,1200

A name ending in .png stays PNG (logos, transparency); everything else is flattened onto white
and saved as progressive JPEG. Prints each size, warns on any file over 600 KB, and warns when a
source is much narrower than the width it is planned for (it never upscales; place it smaller).
"""
import argparse
import csv
import os
import sys

from PIL import Image, ImageOps

WARN_KB = 600


def convert(src, dest, max_w, quality):
    im = ImageOps.exif_transpose(Image.open(src))
    source_w = im.width
    if dest.lower().endswith(".png"):
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(dest, optimize=True)  # PNG carries no EXIF unless asked
    else:
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        im = im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)  # no exif= drops it
    return im.size, os.path.getsize(dest) // 1024, source_w


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--plan", help="CSV with source,name,max_width")
    ap.add_argument("--max", type=int, default=1800, help="default max width in pixels")
    ap.add_argument("--quality", type=int, default=74)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.plan:
        with open(args.plan, newline="", encoding="utf-8") as f:
            jobs = [(r["source"].strip(), r["name"].strip(), int(r.get("max_width") or args.max))
                    for r in csv.DictReader(f) if r.get("source")]
    else:
        jobs = [(n, os.path.splitext(n)[0] + ".jpg", args.max) for n in sorted(os.listdir(args.src))
                if n.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"))]

    total, missing = 0, []
    for source, name, max_w in jobs:
        path = os.path.join(args.src, source)
        if not os.path.exists(path):
            missing.append(source)
            continue
        size, kb, source_w = convert(path, os.path.join(args.out, name), max_w, args.quality)
        total += kb
        notes = ["heavy"] if kb > WARN_KB else []
        if source_w < max_w * 0.75:
            notes.append(f"source is only {source_w} px wide; it will look soft at {max_w}, so place it smaller")
        print(f"{name:36s} {size[0]}x{size[1]:<5} {kb:>5} KB" + ("  <- " + "; ".join(notes) if notes else ""))
    print(f"total {total / 1024:.1f} MB in {args.out}")
    if missing:
        sys.exit("missing sources: " + ", ".join(missing))


if __name__ == "__main__":
    main()
