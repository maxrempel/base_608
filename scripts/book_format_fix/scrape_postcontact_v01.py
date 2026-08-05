# -*- coding: utf-8 -*-
"""Scrape postcontact.world into per-section markdown files on disk.

One file per route. Extracts the <main> region, converts block tags to
markdown-ish text (## for h2/h3, blank-line-separated paragraphs, - for li).
Saves raw HTML too (heavy/restorable) for re-processing if the cleaner misses.
"""
import os, re, html, urllib.request

BASE = "https://postcontact.world"
OUT = r"C:\claude_base\scripts\book_format_fix\postcontact_scrape_v01"
RAW = os.path.join(OUT, "raw_html")

# (order, slug, route, Chapter Title)
PAGES = [
    (1,  "introduction", "/introduction",      "Introduction"),
    (2,  "telepathy",    "/telepathy",         "Telepathy"),
    (3,  "economy",      "/economy",           "Economy"),
    (4,  "awakening",    "/awakening",         "Awakening"),
    (5,  "healing",      "/healing",           "Healing"),
    (6,  "technology",   "/technology",        "Technology"),
    (7,  "religion",     "/religion",          "Religion"),
    (8,  "foh",          "/foh",               "The Future of Humanity"),
    (9,  "stories",      "/stories",           "Stories"),
    (10, "story_rachel", "/stories/rachel",    "Story: Little by Little, A Lot by A Lot"),
    (11, "story_interview","/stories/interview","Story: Job Interview at the End of the World"),
    (12, "about",        "/about",             "About"),
]


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) postcontact-migrate/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main_region(h):
    m = re.search(r"<main\b[^>]*>(.*?)</main>", h, re.S | re.I)
    return m.group(1) if m else h


def to_blocks(frag):
    # drop script/style/svg/nav/noscript
    frag = re.sub(r"<(script|style|svg|nav|noscript)\b.*?</\1>", " ", frag, flags=re.S | re.I)
    # promote headings
    frag = re.sub(r"<h[12][^>]*>(.*?)</h[12]>", r"\n\n## \1\n\n", frag, flags=re.S | re.I)
    frag = re.sub(r"<h[3-6][^>]*>(.*?)</h[3-6]>", r"\n\n### \1\n\n", frag, flags=re.S | re.I)
    # list items
    frag = re.sub(r"<li[^>]*>(.*?)</li>", r"\n- \1\n", frag, flags=re.S | re.I)
    # paragraphs / breaks / block ends -> newlines
    frag = re.sub(r"</(p|div|section|ul|ol|blockquote|figure)>", "\n\n", frag, flags=re.I)
    frag = re.sub(r"<br\s*/?>", "\n", frag, flags=re.I)
    # strip all remaining tags
    frag = re.sub(r"<[^>]+>", "", frag)
    frag = html.unescape(frag)
    # collapse whitespace per line, then blank-line-separate blocks
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in frag.split("\n")]
    out, blank = [], False
    for ln in lines:
        if not ln:
            blank = True
            continue
        if out and blank:
            out.append("")
        out.append(ln)
        blank = False
    # merge consecutive non-heading lines that belong to the same paragraph?
    # keep simple: each surviving line is its own block separated by blanks
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def main():
    os.makedirs(RAW, exist_ok=True)
    for num, slug, route, title in PAGES:
        h = fetch(BASE + route)
        with open(os.path.join(RAW, f"{num:02d}_{slug}.html"), "w", encoding="utf-8") as f:
            f.write(h)
        body = to_blocks(main_region(h))
        md = f"# {title}\n\n{body}\n"
        fn = os.path.join(OUT, f"{num:02d}_{slug}.md")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"{num:02d} {slug:<16} raw={len(h):>6}  text={len(body):>6}")


if __name__ == "__main__":
    main()
