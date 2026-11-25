#!/usr/bin/env python3
"""Quét docs/<mục>/<mục nhỏ>/*.md (đọc front matter) + data/categories.json -> data/index.json.
Mục/mục nhỏ chưa khai báo trong categories.json sẽ được tự thêm từ tên thư mục."""
import json, re, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
def fm(text):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
    d = {}
    if m:
        for ln in m.group(1).splitlines():
            if ':' in ln:
                k, v = ln.split(':', 1); d[k.strip()] = v.strip().strip('"')
    return d
def title_of(s): return s.replace('-', ' ').title()
cfg = json.loads((R/'data/categories.json').read_text('utf-8'))
cats = {c['id']: c for c in cfg['categories']}
posts, warn = [], []
for f in sorted((R/'docs').rglob('*.md')):
    rel = f.relative_to(R).as_posix(); parts = f.relative_to(R/'docs').parts
    if len(parts) != 3: warn.append(f'Bỏ qua (cần docs/<mục>/<mục nhỏ>/<bài>.md): {rel}'); continue
    cid, sid = parts[0], parts[1]; m = fm(f.read_text('utf-8'))
    c = cats.setdefault(cid, {'id': cid, 'name': title_of(cid), 'desc': '', 'ic': cid[:2].upper(), 'subs': []})
    if sid not in [s['id'] for s in c['subs']]: c['subs'].append({'id': sid, 'name': title_of(sid)})
    for k in ('title',):
        if k not in m: warn.append(f'Thiếu {k}: {rel}')
    posts.append({'id': f.stem, 'title': m.get('title', title_of(f.stem)), 'cat': cid, 'sub': sid,
        'type': m.get('type', 'Bài viết'), 'tags': [t.strip() for t in m.get('tags', '').strip('[]').split(',') if t.strip()],
        'status': m.get('status', 'draft'), 'updated': m.get('updated', ''), 'summary': m.get('summary', ''),
        'review_note': m.get('review_note', ''), 'path': rel})
ids = [p['id'] for p in posts]
for i in set(ids):
    if ids.count(i) > 1: warn.append(f'Trùng tên file: {i}')
out = {'site': cfg['site'], 'categories': list(cats.values()), 'posts': posts}
(R/'data/index.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), 'utf-8')
print(f'OK: {len(cats)} mục, {len(posts)} bài'); [print('CẢNH BÁO:', w) for w in warn]
sys.exit(0)
