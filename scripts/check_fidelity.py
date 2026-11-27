#!/usr/bin/env python3
"""Kiểm tra bài đã giữ nguyên văn bản gốc chưa.
  python scripts/check_fidelity.py inbox/_converted/.../raw.md docs/<mục>/<mục-nhỏ>/<bài>.md [--min 0.97]
So từng dòng văn bản của raw.md với bài (bỏ định dạng markdown, bỏ qua dòng ảnh/đường kẻ). Thoát mã 1 nếu thiếu."""
import re, sys, unicodedata, pathlib
def norm(s):
    s = unicodedata.normalize('NFC', s).lower()
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', s)            # ảnh
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)          # link -> chữ
    s = re.sub(r'[*_`>#|\\\-]+', ' ', s)                    # ký hiệu markdown
    s = re.sub(r'^\s*\d+[.)]\s+', ' ', s)                   # số thứ tự đầu dòng
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', s, flags=re.U)).strip()
def body(p):
    t = pathlib.Path(p).read_text('utf-8'); return re.sub(r'^---\r?\n.*?\r?\n---\r?\n', '', t, flags=re.S)
args = [a for a in sys.argv[1:] if not a.startswith('--')]; mn = 0.97
if '--min' in sys.argv: mn = float(sys.argv[sys.argv.index('--min') + 1]); args = [a for a in args if a != str(mn) and a != sys.argv[sys.argv.index('--min') + 1]]
if len(args) != 2: print(__doc__); sys.exit(2)
raw, post = body(args[0]), body(args[1]); P = norm(post); Pw = P.split()
grams = {tuple(Pw[i:i+3]) for i in range(max(len(Pw)-2, 1))}
total = miss = 0; lost = []
for ln in raw.splitlines():
    n = norm(ln); w = n.split()
    if len(w) < 2: continue
    total += len(w)
    if n in P: continue
    g = [tuple(w[i:i+3]) for i in range(max(len(w)-2, 1))]; hit = sum(1 for x in g if x in grams) / len(g)
    if hit < 0.9: miss += len(w); lost.append(ln.strip())
cov = 1 - miss / total if total else 1
print(f'Độ phủ văn bản gốc: {cov:.1%} ({total-miss}/{total} từ)')
for l in lost[:25]: print(' THIẾU:', l[:140])
if len(lost) > 25: print(f' ... và {len(lost)-25} dòng nữa')
print('=> ' + ('ĐẠT' if cov >= mn else 'CHƯA ĐẠT: bổ sung các dòng thiếu đúng nguyên văn rồi chạy lại')); sys.exit(0 if cov >= mn else 1)
