from PIL import Image
import os, pathlib

plates = [
    ("essay_nonhier/essay_nonhier_circle_a.png", "01_circle.jpg"),
    ("essay_nonhier/essay_nonhier_pencil_a.png", "02_pencil.jpg"),
    ("essays/nonhier/nonhier_v02_two_kinds_a.png", "03_two_kinds.jpg"),
    ("essay_nonhier/essay_nonhier_ai_vertical_a.png", "04_ai_vertical.jpg"),
    ("essay_nonhier/essay_nonhier_oracle_a.png", "05_oracle.jpg"),
    ("essay_nonhier/essay_nonhier_chickens_a.png", "06_chickens.jpg"),
    ("essays/nonhier/nonhier_v03_silent_circle_a.png", "07_silent_circle.jpg"),
    ("essay_nonhier/essay_nonhier_council_a.png", "08_council.jpg"),
    ("essays/nonhier/nonhier_v03_ai_vertical_a.png", "09_ai_connectivity.jpg"),
    ("essay_nonhier/essay_nonhier_symmetry_a.png", "10_symmetry.jpg"),
    ("essay_nonhier/essay_nonhier_two_children_a.png", "11_two_children.jpg"),
]

root = pathlib.Path(r"C:\Users\maxre\Nextcloud\ai_images\kazarian_episode")
out = pathlib.Path(r"C:\claude_base\essays\nonhierarchical_future\plates_web")
out.mkdir(exist_ok=True)

for src, dst in plates:
    img = Image.open(root / src).convert("RGB")
    w, h = img.size
    if w > 1200:
        img = img.resize((1200, int(h * 1200 / w)), Image.LANCZOS)
    img.save(out / dst, "JPEG", quality=82, optimize=True)
    print(f"{dst}: {(out / dst).stat().st_size // 1024}KB")
