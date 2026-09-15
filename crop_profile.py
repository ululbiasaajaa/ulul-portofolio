"""
Crop foto jadi bulat (PNG transparan) buat dipasang di cover slide.
Pakai ini SEBELUM jalanin generate_ppt.py, soalnya generate_ppt.py
butuh file "profile_circle.png" yang sudah bulat.

Cara pakai:
    pip install Pillow
    python crop_profile.py foto_asli.jpg profile_circle.png
"""
import sys
from PIL import Image, ImageDraw

def crop_circle(input_path, output_path, size=800, top_offset_ratio=0.0):
    """
    input_path       : path foto asli (jpg/png, sebaiknya potret/formal)
    output_path      : path hasil PNG bulat transparan
    size              : lebar & tinggi output dalam px (persegi)
    top_offset_ratio  : geser crop vertikal, 0.0 = mulai dari atas,
                        0.5 = mulai dari tengah. Atur ini kalau wajah
                        kepotong / posisinya kurang pas.
    """
    im = Image.open(input_path).convert("RGB")
    w, h = im.size
    side = min(w, h)

    # crop jadi persegi dulu (ambil bagian tengah horizontal)
    left = (w - side) // 2
    max_top = h - side
    top = int(max_top * top_offset_ratio)
    im_square = im.crop((left, top, left + side, top + side))

    # resize ke ukuran output & bikin mask lingkaran
    im_square = im_square.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    im_square.putalpha(mask)

    im_square.save(output_path)
    print(f"Saved: {output_path} ({size}x{size})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python crop_profile.py <foto_input> <output.png> [top_offset_ratio]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    top_offset = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    crop_circle(input_path, output_path, top_offset_ratio=top_offset)