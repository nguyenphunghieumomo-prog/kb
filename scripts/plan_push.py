#!/usr/bin/env python3
"""Phân tích path trước khi đẩy bài lên GitHub. Dùng: python scripts/plan_push.py docs/<mục>/<mục-nhỏ>/<bài>.md
Không truyền tham số: tự lấy các bài .md đang thay đổi/mới trong git. Thoát mã 1 nếu có lỗi."""
import json, re, subprocess, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
def git(*a): return subprocess.run(['git', '-C', str(R), *a], capture_output=True, text=True).stdout.strip()
def fm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S); d = {}
    for ln in (m.group(1).splitlines() if m else []):
        if ':' in ln: k, v = ln.split(':', 1); d[k.strip()] = v.strip()
    return d
remote = git('remote', 'get-url', 'origin'); mm = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote)
owner, repo = mm.groups() if mm else ('<user>', '<repo>'); branch = git('rev-parse', '--abbrev-ref', 'HEAD') or 'main'
args = sys.argv[1:] or [l[3:].strip('"') for l in git('status', '--porcelain', '-uall').splitlines() if re.match(r'.. docs/.+\.md$', l)]
if not args: print('Không có bài nào để đẩy.'); sys.exit(0)
cfg = json.loads((R/'data/categories.json').read_text('utf-8')); known = {c['id']: {s['id'] for s in c['subs']} for c in cfg['categories']}
bad = 0
for a in args:
    f = (R/a).resolve(); rel = f.relative_to(R).as_posix(); parts = rel.split('/'); E, W = [], []
    if not f.exists(): print(f'LỖI: không thấy {rel}'); bad += 1; continue
    t = f.read_text('utf-8'); m = fm(t)
    if len(parts) != 4 or parts[0] != 'docs': E.append('Path phải là docs/<mục>/<mục-nhỏ>/<bài>.md')
    else:
        _, c, s, name = parts; slug = name[:-3]
        for x in (c, s, slug):
            if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', x): E.append(f'Tên "{x}" phải viết thường, không dấu, nối bằng "-"')
        if m.get('cat') != c or m.get('sub') != s: E.append(f'Front matter (cat={m.get("cat")}, sub={m.get("sub")}) không khớp thư mục ({c}/{s})')
        if c not in known: W.append(f'Mục MỚI "{c}" chưa có trong data/categories.json (web vẫn tự nhận, nên khai báo tên đẹp)')
        elif s not in known[c]: W.append(f'Mục nhỏ MỚI "{s}" trong mục {c} (web tự nhận tên từ thư mục)')
        if m.get('status') not in ('draft', 'approved'): E.append('status phải là draft hoặc approved')
        if not m.get('title'): E.append('Thiếu title')
        imgs = [x.split('#')[0] for x in re.findall(r'!\[[^\]]*\]\(([^)\s]+)', t)]
        files = [rel]
        for i in imgs:
            if i.startswith(('http', 'data:')): W.append(f'Ảnh ngoài/nhúng: {i[:50]}'); continue
            if not (R/i).exists(): E.append(f'Thiếu ảnh: {i}')
            elif not i.startswith(f'assets/img/{c}/{slug}/'): W.append(f'Ảnh nên nằm trong assets/img/{c}/{slug}/: {i}')
            files.append(i)
        if re.search(r'(?i)(password|passwd|mật khẩu\s*[:=]|api[_-]?key|secret|BEGIN [A-Z ]*PRIVATE KEY|ghp_[A-Za-z0-9]{20,})', t): W.append('Có thể chứa mật khẩu/token: kiểm tra trước khi đẩy (repo công khai)')
        if c not in known or s not in known.get(c, ()): files.append('data/categories.json (nếu bạn có sửa)')
        base = f'https://github.com/{owner}/{repo}'
        print(f'\n== {m.get("title", slug)} [{m.get("status")}]\n Mục: {c} > {s}\n Path GitHub: {base}/blob/{branch}/{rel}\n Link web: https://{owner}.github.io/{repo}/#post/{slug}\n File sẽ commit:')
        for x in dict.fromkeys(files): print('   +', x)
        print(f' Commit: docs({c}/{s}): {"thêm" if m.get("status")=="draft" else "duyệt"} bài {m.get("title", slug)}')
    for w in W: print(' CẢNH BÁO:', w)
    for e in E: print(' LỖI:', e)
    bad += bool(E)
print('\n=> ' + ('CÓ LỖI, chưa nên đẩy.' if bad else 'Path hợp lệ, chờ bạn xác nhận để commit + push.')); sys.exit(1 if bad else 0)
