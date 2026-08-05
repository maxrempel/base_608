#!/usr/bin/env python3
"""Slice 'Celestial Science' into 6 big parts as flat NN_slug.md files.

Each output file is in the format import_book_flat_v01.py expects:
  # Celestial Science - <PART NAME>
  *From "Celestial Science" by Max Rempel, Ph.D.*

  <body, one block per blank-line-separated paragraph>

The source has each paragraph on its own single line with NO blank line
between paragraphs, and sub-section headers as short standalone lines.
We re-join with blank lines (so the importer's blank-line block splitter
works) and promote detected short header lines to '## ' so they render as
sub-headings inside each part.
"""
import os, re

SRC = r"C:\Users\maxre\Nextcloud\zSyncMain\z_luminous_fixed\preingest\maxs_publications\books\book1 celestial science rempel.md"
OUT = r"C:\claude_base\scripts\book_format_fix\staging_6parts_v01\celestial_science"

# (chapter_num, slug_suffix, PART NAME, body_start_line, body_end_line)  -- 1-indexed inclusive
PARTS = [
    (1, "introduction",   "Introduction",                 26, 48),
    (2, "star_children",  "Star Children",                50, 177),
    (3, "our_future",     "Our Future",                   179, 355),
    (4, "religion",       "Transformation of Religion",   357, 608),
    (5, "reincarnation",  "Reincarnation",                610, 682),
    (6, "higher_self",    "Higher Self",                  684, 911),
]


def is_subheading(line):
    s = line.strip()
    if not s or len(s) >= 85:
        return False
    if s.startswith("\u2022") or s.startswith("-") or s.startswith("*"):
        return False
    if re.match(r"^\d+[\.\)]", s):          # numbered list item
        return False
    if re.match(r"^(Q:|A:|Bashar:|Elias:|Laura:)", s):
        return False
    if s[-1] in '.,:;"\u201d':               # ends like a sentence / lead-in
        return False
    if re.search(r"\b\d{4}\b", s):            # a year -> signature/date line
        return False
    if re.search(r",\s*[A-Z]{2}$", s):        # "City, ST" signoff line
        return False
    return True


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().split("\n")
    os.makedirs(OUT, exist_ok=True)
    for num, slug, name, a, b in PARTS:
        body = lines[a - 1:b]               # convert to 0-indexed slice
        blocks = []
        for ln in body:
            if not ln.strip():
                continue
            if is_subheading(ln):
                blocks.append("## " + ln.strip())
            else:
                blocks.append(ln.strip())
        md = (f"# Celestial Science - {name}\n"
              f'*From "Celestial Science" by Max Rempel, Ph.D.*\n\n'
              + "\n\n".join(blocks) + "\n")
        fn = os.path.join(OUT, f"{num:02d}_{slug}.md")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(md)
        sub = sum(1 for x in blocks if x.startswith("## "))
        print(f"part {num}: {name:<28} {len(blocks):>4} blocks, {sub:>3} subheadings -> {os.path.basename(fn)}")


if __name__ == "__main__":
    main()
