"""Convert heavy PNG/JPG assets to WebP next to the source. Idempotent; never overwrites sources."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
NAMES = ["hero-render.png", "struktur-kimia.png"] + [f"project{i}.jpg" for i in range(1, 11)]
MAX_W = 1600

for name in NAMES:
    src = ROOT / name
    if not src.exists():
        print("skip (missing):", name)
        continue
    out = src.with_suffix(".webp")
    im = Image.open(src)
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and "A" in im.getbands() else "RGB")
    im.save(out, "WEBP", quality=80, method=6)
    print(f"{name}: {src.stat().st_size//1024} KB -> {out.name}: {out.stat().st_size//1024} KB  ({im.width}x{im.height})")
