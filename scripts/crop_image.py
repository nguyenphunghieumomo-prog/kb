#!/usr/bin/env python3
"""Cắt ảnh minh họa. Cần: pip install pillow
  python scripts/crop_image.py vao.png ra.png --trim            # tự cắt viền đồng màu
  python scripts/crop_image.py vao.png ra.png --box 100,50,900,600   # x0,y0,x1,y1 (pixel)
  python scripts/crop_image.py vao.png ra.png --box 0.1,0.05,0.9,0.8 # hoặc tỷ lệ 0..1
Có thể kết hợp: --box rồi --trim. --info chỉ in kích thước."""
import argparse
from PIL import Image, ImageChops
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('dst', nargs='?')
ap.add_argument('--box'); ap.add_argument('--trim', action='store_true'); ap.add_argument('--pad', type=int, default=6)
ap.add_argument('--info', action='store_true'); a = ap.parse_args()
im = Image.open(a.src).convert('RGB'); W, H = im.size
if a.info or not a.dst: print(f'{a.src}: {W}x{H}'); raise SystemExit
if a.box:
    v = [float(x) for x in a.box.split(',')]
    if max(v) <= 1: v = [v[0]*W, v[1]*H, v[2]*W, v[3]*H]
    im = im.crop(tuple(int(x) for x in v))
if a.trim:
    bg = Image.new('RGB', im.size, im.getpixel((0, 0)))
    bb = ImageChops.difference(im, bg).point(lambda p: 255 if p > 12 else 0).getbbox()
    if bb:
        p = a.pad; bb = (max(bb[0]-p, 0), max(bb[1]-p, 0), min(bb[2]+p, im.size[0]), min(bb[3]+p, im.size[1])); im = im.crop(bb)
im.save(a.dst, optimize=True); print(f'Đã lưu {a.dst}: {im.size[0]}x{im.size[1]} (gốc {W}x{H})')
