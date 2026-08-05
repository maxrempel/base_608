# -*- coding: utf-8 -*-
"""Import the scraped postcontact.world sections as real chapters (1..12) of
the 'postcontact' book on maxrempel.com. Chapter 0 (Summary) is left intact.

Reads the cleaned .md files in postcontact_scrape_v01/, converts the simple
markdown (## / ### headings, - lists, blank-line paragraphs) to HTML, strips
the site's prev/next arrow nav lines, and POSTs each as a chapter.
"""
import os, re, json, glob, urllib.request

API = "https://maxrempel.com/api/book"
TOKEN = "mxr-blog-7f3k9x2m4p"
SLUG = "postcontact"
SRC = r"C:\claude_base\scripts\book_format_fix\postcontact_scrape_v01"

# chapter title per file slug (first "# ..." line is also the title; we trust the map)
TITLES = {
    "01_introduction":   "Introduction",
    "02_telepathy":      "Telepathy",
    "03_economy":        "Economy",
    "04_awakening":      "Awakening",
    "05_healing":        "Healing",
    "06_technology":     "Technology",
    "07_religion":       "Religion",
    "08_foh":            "The Future of Humanity",
    "09_stories":        "Stories",
    "10_story_rachel":   "Story: Little by Little, A Lot by A Lot",
    "11_story_interview":"Story: Job Interview at the End of the World",
    "12_about":          "About",
}

NAV_RE = re.compile(r"^[\u2190\u2192\u2191\u2193]|[\u2190\u2192\u2191\u2193]\s*$|^(Home|Economy|Religion|Podcast|About|Future humanity)\s*[\u2192]")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


DEMOJIBAKE = {
    "\u00e2\u20ac\u201d": "\u2014",   # mangled em-dash -> em-dash
    "\u00e2\u20ac\u2122": "\u2019",   # mangled apostrophe
    "\u00e2\u20ac\u0153": "\u201c",   # mangled left double-quote
    "\u00e2\u20ac\u009d": "\u201d",   # mangled right double-quote
    "\u00e2\u20ac\u00a6": "\u2026",   # mangled ellipsis
    "\u00c2\u00a0": " ",                # mangled nbsp
}


def md_to_html(text):
    for bad, good in DEMOJIBAKE.items():
        text = text.replace(bad, good)
    # drop the leading "# Title" line and any prev/next arrow nav lines
    lines = text.split("\n")
    kept = []
    for ln in lines:
        s = ln.rstrip()
        if s.startswith("# "):
            continue
        if "\u2190" in s or "\u2192" in s:   # prev/next arrows
            continue
        kept.append(s)
    blocks = [b.strip() for b in "\n".join(kept).split("\n\n") if b.strip()]
    out = []
    pend_li = []

    def flush_li():
        if pend_li:
            out.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in pend_li) + "</ul>")
            pend_li.clear()

    for b in blocks:
        if b.startswith("## "):
            flush_li(); out.append(f"<h2>{esc(b[3:].strip())}</h2>")
        elif b.startswith("### "):
            flush_li(); out.append(f"<h3>{esc(b[4:].strip())}</h3>")
        elif b.startswith("- "):
            for ln in b.split("\n"):
                ln = ln.strip()
                if ln.startswith("- "):
                    pend_li.append(ln[2:].strip())
        else:
            flush_li(); out.append(f"<p>{esc(b)}</p>")
    flush_li()
    return "\n".join(out)


def post(payload):
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) postcontact-migrate/1.0"},
        method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    for fn in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        base = os.path.splitext(os.path.basename(fn))[0]
        if base not in TITLES:
            continue
        num = int(base[:2])
        with open(fn, encoding="utf-8") as f:
            html = md_to_html(f.read())
        r = post({"type": "chapter", "book_slug": SLUG, "chapter_num": num,
                  "title": TITLES[base], "content": html})
        print(f"ch{num:<2} {TITLES[base]:<44} {len(html):>6} chars -> {r.get('success')}")


if __name__ == "__main__":
    main()
