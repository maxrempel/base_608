r"""
book_format_fix_v01.py  (2026-05-31)

Fixes format problems in two of Max's books in the luminous ingest folder so
they ingest cleanly into Memex. NON-DESTRUCTIVE to originals: book1's original
.txt is left in place (caller archives it separately); book4 is rewritten in
place (the pusher replaces its Memex entry by same path on next sync).

book1 (Celestial Science): file is Windows-1252 encoded and has extension .txt,
so the Memex pusher (which only takes .md, UTF-8) never ingested it. We decode
cp1252 -> proper Unicode (recovers ©, curly quotes, em-dashes, ellipses, nbsp),
fix one lost glyph (?iurlionis -> Ciurlionis with the correct C-caron), turn
non-breaking spaces into normal spaces, collapse runs of blank lines, and write
a clean UTF-8 .md alongside the siblings.

book4 (Metaphysics): pandoc left 25 backslash escapes (\- and \.). Strip them.

Run:  python book_format_fix_v01.py
"""
import re, os

BOOKS = r"C:\Users\maxre\Nextcloud\zSyncMain\z_luminous_fixed\ingest\maxs_publications\books"

B1_TXT = os.path.join(BOOKS, "book1_celestial_science_rempel_3 ebook_isbn9781105358074.txt")
B1_MD  = os.path.join(BOOKS, "book1 celestial science rempel.md")
B4_MD  = os.path.join(BOOKS, "book4 rempel METAPHYSICS FOR LIGHTWORKERS.md")

def fix_book1():
    raw = open(B1_TXT, "rb").read()
    text = raw.decode("cp1252")
    # the artist's name lost its C-caron to a literal '?'
    text = text.replace("Konstantinas ?iurlionis", "Konstantinas \u010ciurlionis")
    # non-breaking space -> normal space
    text = text.replace("\u00a0", " ")
    # normalise newlines, collapse 3+ blank lines to a single blank line
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text).lstrip("\n ")
    # trim trailing spaces per line
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    open(B1_MD, "w", encoding="utf-8").write(text)
    return len(text)

def fix_book4():
    text = open(B4_MD, "r", encoding="utf-8").read()
    n = len(re.findall(r"\\[-.]", text))
    text = re.sub(r"\\([-.])", r"\1", text)
    open(B4_MD, "w", encoding="utf-8").write(text)
    return n

if __name__ == "__main__":
    l1 = fix_book1()
    print(f"book1: wrote clean UTF-8 .md, {l1} chars -> {B1_MD}")
    n4 = fix_book4()
    print(f"book4: removed {n4} backslash escapes in place")
