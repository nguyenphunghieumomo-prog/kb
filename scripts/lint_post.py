#!/usr/bin/env python3
"""Kiểm tra bố cục ảnh trong bài. Dùng: python scripts/lint_post.py docs/<mục>/<mục-nhỏ>/<bài>.md [...]
LỖI: có mục "Hình minh họa từ tài liệu"/gallery cuối bài, thiếu file ảnh. CẢNH BÁO: nhiều ảnh liền nhau, ảnh dồn cuối bài, ảnh có vẻ là chụp cả trang."""
import re, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
try:
    from PIL import Image
except Exception:
    Image = None
BAD = re.compile(r'hình\s*minh\s*họa\s*(từ|trong)|ảnh\s*(gốc|từ\s*tài\s*liệu)|hình\s*ảnh\s*(gốc|từ\s*tài\s*liệu)|thư\s*viện\s*ảnh|phụ\s*lục\s*ảnh', re.I)
IMG = re.compile(r'^\s*!\[[^\]]*\]\(([^)\s]+)')
bad = 0
for a in sys.argv[1:] or ['--']:
    if a == '--': print(__doc__); sys.exit(2)
    f = (R/a).resolve()
    if not f.exists(): print(f'LỖI: không thấy {a}'); bad += 1; continue
    t = re.sub(r'^---\r?\n.*?\r?\n---\r?\n', '', f.read_text('utf-8'), flags=re.S); lines = t.splitlines(); E, W = [], []
    for i, l in enumerate(lines, 1):
        m = re.match(r'^#{1,6}\s+(.*)', l)
        if m and BAD.search(m.group(1)): E.append(f'Dòng {i}: mục "{m.group(1).strip()}" — cấm mục ảnh gom cuối bài; đặt ảnh vào đúng đoạn văn hoặc bỏ')
    # nhóm ảnh liền nhau (bỏ qua dòng trống và chú thích in nghiêng)
    seq, run = [], 0; last_text = 0
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if not s: continue
        if IMG.match(l): run += 1; seq.append(i)
        elif re.match(r'^[*_].*[*_]$', s) or s.startswith('<img') : continue
        else:
            if run >= 2: W.append(f'Dòng {seq[0]}-{seq[-1]}: {run} ảnh liền nhau không có văn bản xen giữa (giống thư viện ảnh)')
            run, seq = 0, []; last_text = i
    if run >= 2: E.append(f'Cuối bài có {run} ảnh liền nhau (dòng {seq[0]}-{seq[-1]}): ảnh dồn cuối bài là không được phép')
    tail = [l for l in lines if l.strip()][-3:]
    if any(IMG.match(x) for x in tail) and not any(BAD.search(e) for e in E) and run < 2:
        W.append('Bài kết thúc bằng ảnh: kiểm tra ảnh có đúng chỗ của đoạn văn tương ứng không')
    for l in lines:
        m = IMG.match(l)
        if not m or m.group(1).startswith(('http', 'data:')): continue
        p = R/m.group(1)
        if not p.exists(): E.append(f'Thiếu file ảnh: {m.group(1)}'); continue
        if Image:
            w, h = Image.open(p).size
            if h > 1400 or (h > 900 and h / w > 1.25): W.append(f'{m.group(1)}: {w}x{h} — có vẻ là ảnh chụp cả trang, cắt lấy phần hình chính hoặc bỏ')
            if w * h > 6_000_000: W.append(f'{m.group(1)}: ảnh quá lớn ({w}x{h})')
    print(f'\n== {a}')
    for w in W: print(' CẢNH BÁO:', w)
    for e in E: print(' LỖI:', e)
    if not (W or E): print(' OK')
    bad += bool(E)
print('\n=> ' + ('CÓ LỖI, sửa trước khi đẩy.' if bad else 'Đạt.')); sys.exit(1 if bad else 0)
