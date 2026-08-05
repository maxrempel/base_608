r"""
analyze_books_v01.py - read-only structure map of Max's books in the luminous
ingest/books folder. Prints, per book: total chars and candidate chapter
headings with the char length of each section, so we can design chapter splits
that stay under Memex's 8000-char per-entry limit.

Heading heuristic: a non-empty line that is markdown (# / ** **) OR is short
(<= 70 chars) and does not end in sentence punctuation.
"""
import os, re, sys, io

OUT = io.StringIO()
def emit(s=""):
    OUT.write(s + "\n")

BOOKS = r"C:\Users\maxre\Nextcloud\zSyncMain\z_luminous_fixed\ingest\maxs_publications\books"
FILES = [
    "book1 celestial science rempel.md",
    "book2 ts6 GLAVNYJ.md",
    "book3d5 welcome to earth rempel no page numbers.md",
    "book4 rempel METAPHYSICS FOR LIGHTWORKERS.md",
    "Book6 from the galaxy.md",
]

def strong_heading(line):
    """Markdown header, fully-bold line, or ALL-CAPS short line."""
    s = line.strip()
    if not s:
        return False
    if s.startswith("#"):
        return True
    if s.startswith("**") and s.endswith("**") and len(s) <= 100:
        return True
    letters = [c for c in s if c.isalpha()]
    if letters and len(s) <= 70 and all(c.isupper() for c in letters):
        return True
    return False

def short_titleish(line):
    """Loose: short non-sentence line (catches plain-text subheadings)."""
    s = line.strip()
    if not s or len(s) > 70:
        return False
    if re.search(r"[.?!:,;\u2026]$", s) or s[0].islower():
        return False
    if re.fullmatch(r"[\d\s]+", s):
        return False
    return True

for fn in FILES:
    p = os.path.join(BOOKS, fn)
    if not os.path.exists(p):
        emit(f"\n### MISSING: {fn}")
        continue
    text = open(p, "r", encoding="utf-8").read()
    lines = text.split("\n")
    total = len(text)
    n_strong = sum(1 for ln in lines if strong_heading(ln))
    n_short = sum(1 for ln in lines if short_titleish(ln))
    # choose markers: prefer strong headings; if too few, fall back to short-titleish
    use_strong = n_strong >= 3
    marker = strong_heading if use_strong else short_titleish
    heads = [(i, lines[i].strip()) for i in range(len(lines)) if marker(lines[i])]
    emit(f"\n### {fn}")
    emit(f"    total {total} chars | strong-headings {n_strong} | short-titleish {n_short} | using {'STRONG' if use_strong else 'SHORT'} markers ({len(heads)})")
    char_pos = []
    pos = 0
    for ln in lines:
        char_pos.append(pos)
        pos += len(ln) + 1
    for k, (i, h) in enumerate(heads):
        start = char_pos[i]
        end = char_pos[heads[k+1][0]] if k+1 < len(heads) else total
        seg = end - start
        flag = "  <<<OVER8000" if seg > 8000 else ""
        emit(f"  [{seg:6d}] {h[:75]}{flag}")

report_path = os.path.join(os.path.dirname(__file__), "book_structure_report.txt")
open(report_path, "w", encoding="utf-8").write(OUT.getvalue())
print("wrote", report_path)
