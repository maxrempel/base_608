r"""
chapter_split_v01.py  (2026-05-31)

Splits Max's 5 books into one-folder-per-book / one-file-per-chapter, with:
  - character simplification (English + Russian only; convert fancy punctuation
    to ASCII; keep the degree symbol; drop everything else exotic)
  - a reference annotation header on every chapter (book title + author)
  - oversized chapters (> CEILING chars) split into "(Part k of n)" at
    paragraph boundaries so no file exceeds Memex's 8000-char entry limit
  - tiny fragments (front matter, ToC lines, footnote-URL tail) glued backward
    into the preceding chapter so we don't emit hundreds of micro-files

OUTPUT IS STAGED, NOT LIVE. Everything is written under STAGE_DIR. Nothing in
the luminous ingest/preingest tree is touched by this script. After Max eyeballs
the staging output we copy chapters into ingest/<book>/ and move the clean
whole-book .md into preingest/.

Run:  python chapter_split_v01.py
"""
import os, re, io, unicodedata

BOOKS = r"C:\Users\maxre\Nextcloud\zSyncMain\z_luminous_fixed\ingest\maxs_publications\books"
STAGE_DIR = os.path.join(os.path.dirname(__file__), "staging_v01")

CEILING = 7000          # max body chars per file (header adds ~80; stays < 8000)
MIN_MERGE = 300         # segments smaller than this glue backward into previous

# ---- per-book config: (filename, English title, author line, marker kind, slug) ----
AUTHOR = "Max Rempel, Ph.D."
CONFIG = [
    ("book1 celestial science rempel.md",
     "Celestial Science", AUTHOR, "short", "celestial_science"),
    ("book2 ts6 GLAVNYJ.md",
     "\u0411\u043e\u0433\u0438 \u043e \u043d\u0430\u0441", "\u041c\u0430\u043a\u0441 \u0420\u0435\u043c\u043f\u0435\u043b\u044c",
     "strong", "bogi_o_nas"),
    ("book3d5 welcome to earth rempel no page numbers.md",
     "Welcome to Earth! A Guide for Aliens", AUTHOR, "strong", "welcome_to_earth"),
    ("book4 rempel METAPHYSICS FOR LIGHTWORKERS.md",
     "Metaphysics for Lightworkers", AUTHOR, "strong", "metaphysics_for_lightworkers"),
    ("Book6 from the galaxy.md",
     "From the Galaxy, With Love: A Lightworker's Textbook", AUTHOR, "strong", "from_the_galaxy"),
]

# ---------------- character simplification ----------------
CONV = {
    "\u2018": "'", "\u2019": "'", "\u201A": "'", "\u2032": "'", "\u0060": "'",
    "\u201C": '"', "\u201D": '"', "\u201E": '"', "\u00AB": '"', "\u00BB": '"', "\u2033": '"',
    "\u2013": "-", "\u2014": "-", "\u2012": "-", "\u2015": "-", "\u2212": "-",
    "\u2026": "...",
    "\u00A0": " ", "\u2009": " ", "\u200A": " ", "\u2007": " ", "\u202F": " ", "\u200B": "",
    "\u00A9": "(c)", "\u00AE": "(r)", "\u2122": "(tm)",
    "\u2022": "-", "\u00B7": "-", "\u2219": "-",
    "\u2192": "->", "\uFEFF": "",
}

def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "".join(CONV.get(ch, ch) for ch in text)
    out = []
    for ch in text:
        o = ord(ch)
        if ch in ("\n", "\u00B0"):          # newline + degree sign
            out.append(ch)
        elif 0x20 <= o <= 0x7E:             # printable ASCII
            out.append(ch)
        elif 0x0400 <= o <= 0x04FF:         # Cyrillic
            out.append(ch)
        elif ch == "\t":
            out.append(" ")
        else:                               # fold accented Latin -> ASCII (keep names)
            for c in unicodedata.normalize("NFKD", ch):
                if 0x20 <= ord(c) <= 0x7E:
                    out.append(c)
            # anything non-decomposable (emoji etc.) is dropped
    text = "".join(out)
    text = "\n".join(ln.rstrip() for ln in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text).strip("\n ") + "\n"
    return text

# ---------------- heading detection ----------------
def strong_heading(line):
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
    s = line.strip()
    if not s or len(s) > 70:
        return False
    if re.search(r"[.?!:,;]$", s) or s[0].islower():
        return False
    if re.fullmatch(r"[\d\s]+", s):
        return False
    return True

# ---------------- slug / translit ----------------
RU2LAT = {
    "\u0430":"a","\u0431":"b","\u0432":"v","\u0433":"g","\u0434":"d","\u0435":"e","\u0451":"e",
    "\u0436":"zh","\u0437":"z","\u0438":"i","\u0439":"y","\u043a":"k","\u043b":"l","\u043c":"m",
    "\u043d":"n","\u043e":"o","\u043f":"p","\u0440":"r","\u0441":"s","\u0442":"t","\u0443":"u",
    "\u0444":"f","\u0445":"h","\u0446":"ts","\u0447":"ch","\u0448":"sh","\u0449":"sch","\u044a":"",
    "\u044b":"y","\u044c":"","\u044d":"e","\u044e":"yu","\u044f":"ya",
}
def slugify(heading):
    s = heading.strip().lstrip("#").strip().strip("*").strip().lower()
    s = "".join(RU2LAT.get(c, c) for c in s)
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return (s[:40].rstrip("_")) or "chapter"

def heading_text(line):
    return line.strip().lstrip("#").strip().strip("*").strip()

# ---------------- segmentation ----------------
def segment(text, kind):
    marker = strong_heading if kind == "strong" else short_titleish
    lines = text.split("\n")
    idx = [i for i, ln in enumerate(lines) if marker(ln)]
    if not idx:
        return [("", text)]
    segs = []
    # preamble before first heading
    if idx[0] > 0:
        pre = "\n".join(lines[:idx[0]]).strip()
        if pre:
            segs.append(("", pre))
    for k, i in enumerate(idx):
        end = idx[k + 1] if k + 1 < len(idx) else len(lines)
        head = heading_text(lines[i])
        body = "\n".join(lines[i + 1:end]).strip()
        segs.append((head, body))
    return segs

def merge_small(segs):
    """Glue segments whose whole size < MIN_MERGE backward into previous."""
    out = []
    for head, body in segs:
        size = len(head) + len(body)
        if out and size < MIN_MERGE:
            ph, pb = out[-1]
            glued = (pb + "\n\n" + (head + "\n" + body if head else body)).strip()
            out[-1] = (ph, glued)
        else:
            out.append((head, body))
    return out

def bundle_refs(segs):
    """Collapse a trailing run of footnote segments (heading starts with a
    number, e.g. '187 http://...') into one 'References' chapter."""
    i = len(segs)
    while i > 0 and re.match(r"^\d+\s", segs[i - 1][0]):
        i -= 1
    if i <= len(segs) - 2:               # at least 2 trailing numbered segments
        body = "\n\n".join((h + "\n" + b) if b else h for h, b in segs[i:]).strip()
        segs = segs[:i] + [("References", body)]
    return segs

def split_parts(body):
    """Split a long body into <=CEILING pieces at paragraph boundaries."""
    if len(body) <= CEILING:
        return [body]
    paras = body.split("\n\n")
    parts, cur = [], ""
    for p in paras:
        if len(p) > CEILING:             # single giant paragraph: hard wrap first
            if cur:
                parts.append(cur.strip()); cur = ""
            for j in range(0, len(p), CEILING):
                parts.append(p[j:j + CEILING].strip())
        elif cur and len(cur) + len(p) + 2 > CEILING:
            parts.append(cur.strip())
            cur = p
        else:
            cur = (cur + "\n\n" + p) if cur else p
    if cur.strip():
        parts.append(cur.strip())
    return parts

# ---------------- main ----------------
def process_book(fn, title, author, kind, slug):
    raw = open(os.path.join(BOOKS, fn), "r", encoding="utf-8").read()
    text = clean_text(raw)
    stem = os.path.splitext(fn)[0]                 # drop junk H1 == filename
    lines = text.split("\n")
    if lines and lines[0].strip() == "# " + stem:
        text = "\n".join(lines[1:]).lstrip("\n")
    segs = bundle_refs(merge_small(segment(text, kind)))
    outdir = os.path.join(STAGE_DIR, slug)
    os.makedirs(outdir, exist_ok=True)
    n = 0
    log = []
    for head, body in segs:
        if not body.strip():
            continue
        chap = head if head else "Front Matter"
        parts = split_parts(body)
        for pk, part in enumerate(parts, 1):
            n += 1
            label = chap if len(parts) == 1 else f"{chap} (Part {pk} of {len(parts)})"
            ru = any(0x0400 <= ord(c) <= 0x04FF for c in author)
            ref = (f"*\u0418\u0437 \u043a\u043d\u0438\u0433\u0438 \"{title}\", {author}*"
                   if ru else f"*From \"{title}\" by {author}*")
            header = f"# {title} - {label}\n\n{ref}\n\n"
            fname = f"{n:02d}_{slugify(head if head else 'opening')}"
            if len(parts) > 1:
                fname += f"_p{pk}"
            fname += ".md"
            content = header + part.strip() + "\n"
            open(os.path.join(outdir, fname), "w", encoding="utf-8").write(content)
            log.append((fname, len(content)))
    return n, log, len(text)

def main():
    os.makedirs(STAGE_DIR, exist_ok=True)
    rep = io.StringIO()
    grand = 0
    for fn, title, author, kind, slug in CONFIG:
        n, log, tot = process_book(fn, title, author, kind, slug)
        grand += n
        over = [f for f, L in log if L > 8000]
        rep.write(f"\n### {title}  ->  {slug}/  ({n} files, source {tot} chars)\n")
        biggest = sorted(log, key=lambda x: -x[1])[:3]
        for f, L in biggest:
            rep.write(f"    biggest: [{L:5d}] {f}\n")
        if over:
            rep.write(f"    !!! OVER 8000: {over}\n")
    rep.write(f"\nTOTAL files: {grand}\n")
    report = rep.getvalue()
    open(os.path.join(os.path.dirname(__file__), "split_report_v01.txt"),
         "w", encoding="utf-8").write(report)
    print(report)

if __name__ == "__main__":
    main()
