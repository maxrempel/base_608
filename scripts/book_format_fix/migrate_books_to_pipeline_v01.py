r"""
migrate_books_to_pipeline_v01.py  (2026-05-31)

Promotes the QC'd chapter split from staging into the live luminous pipeline:

  1. For each book: copy staging_v01/<slug>/  ->  ingest/.../books/<slug>/
     (fresh copy; if the dest subfolder already exists it is replaced)
  2. Move each clean whole-book .md OUT of ingest INTO preingest/.../books/
     (preingest is NOT scanned by the pusher, so the old single truncated
     whole-book Memex entries get reconciled-deleted, and the per-chapter
     files take their place)
  3. Collision safety: if a whole-book .md already exists in preingest and
     DIFFERS, the existing one is moved to _archive_book_originals with an
     obsolete_<date>_ prefix before the canonical (cleaned) one is moved in.

Non-destructive: nothing is deleted, only copied / moved / archived.
Run:  python migrate_books_to_pipeline_v01.py
"""
import os, shutil, filecmp

ROOT   = r"C:\Users\maxre\Nextcloud\zSyncMain\z_luminous_fixed"
ING    = os.path.join(ROOT, "ingest", "maxs_publications", "books")
PRE    = os.path.join(ROOT, "preingest", "maxs_publications", "books")
ARCH   = os.path.join(ROOT, "_archive_book_originals")
STAGE  = os.path.join(os.path.dirname(__file__), "staging_v01")
DATE   = "20260531"

# (whole-book .md filename in ingest, staging slug / new ingest subfolder)
BOOKS = [
    ("book1 celestial science rempel.md",                       "celestial_science"),
    ("book2 ts6 GLAVNYJ.md",                                     "bogi_o_nas"),
    ("book3d5 welcome to earth rempel no page numbers.md",       "welcome_to_earth"),
    ("book4 rempel METAPHYSICS FOR LIGHTWORKERS.md",            "metaphysics_for_lightworkers"),
    ("Book6 from the galaxy.md",                                 "from_the_galaxy"),
]

def main():
    os.makedirs(PRE, exist_ok=True)
    os.makedirs(ARCH, exist_ok=True)
    for whole, slug in BOOKS:
        src_dir = os.path.join(STAGE, slug)
        dst_dir = os.path.join(ING, slug)
        n = len([f for f in os.listdir(src_dir) if f.endswith(".md")])
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
        print(f"[chapters] {slug}/ <- {n} files")

        src_md = os.path.join(ING, whole)
        dst_md = os.path.join(PRE, whole)
        if not os.path.exists(src_md):
            print(f"  !! whole-book missing in ingest: {whole}")
            continue
        if os.path.exists(dst_md) and not filecmp.cmp(src_md, dst_md, shallow=False):
            obsolete = os.path.join(ARCH, f"obsolete_{DATE}_{whole}")
            shutil.move(dst_md, obsolete)
            print(f"  [archive] old preingest copy -> {os.path.basename(obsolete)}")
        if os.path.exists(dst_md):          # identical copy already there
            os.remove(dst_md)
        shutil.move(src_md, dst_md)
        print(f"  [whole]   {whole}  ingest -> preingest")
    print("DONE")

if __name__ == "__main__":
    main()
