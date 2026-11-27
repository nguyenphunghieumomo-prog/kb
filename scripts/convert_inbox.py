#!/usr/bin/env python3
"""Chuyển file trong inbox/ sang văn bản để Copilot đọc được.
File đặt trong inbox/<mục>/ hoặc inbox/<mục>/<mục-nhỏ>/ thì tên thư mục là gợi ý phân loại.
Kết quả: inbox/_converted/<cùng cấu trúc>/<tên-file>/raw.md (+ media/). Cần pandoc (docx), poppler pdftotext (pdf), openpyxl (xlsx)."""
import pathlib, subprocess, shutil, sys
R = pathlib.Path(__file__).resolve().parent.parent; IN = R/'inbox'; OUT = IN/'_converted'
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
n = 0
for f in sorted(IN.rglob('*')):
    rel = f.relative_to(IN)
    if f.is_dir() or any(x.startswith(('.', '_')) for x in rel.parts): continue
    d = OUT/rel.parent/f.stem; d.mkdir(parents=True, exist_ok=True); ext = f.suffix.lower(); ok = True
    if ext in ('.docx', '.odt', '.pptx'):
        r = run(['pandoc', str(f), '-t', 'gfm', '--extract-media', str(d), '-o', str(d/'raw.md')]); ok = r.returncode == 0
    elif ext == '.pdf':
        r = run(['pdftotext', '-layout', str(f), str(d/'raw.md')]); ok = r.returncode == 0
        if ok:
            media = d/'media'; media.mkdir(exist_ok=True)
            rpages = run(['pdftoppm', '-png', '-r', '120', str(f), str(media/'page')])
            if rpages.returncode == 0:
                with (d/'raw.md').open('a', encoding='utf-8') as out:
                    out.write('\n\n## Hình minh họa từ tài liệu PDF\n')
                    for page in sorted(media.glob('page-*.png')):
                        out.write(f'![Trang {page.stem.split("-")[-1]}](media/{page.name})\n\n')
            else:
                print(f'Không thể trích xuất ảnh PDF: {f.name}')
    elif ext in ('.xlsx', '.xlsm'):
        import openpyxl
        wb = openpyxl.load_workbook(f, data_only=True); L = []
        for ws in wb:
            L.append(f'## Sheet: {ws.title}\n')
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                L.append('| ' + ' | '.join('' if c is None else str(c) for c in row) + ' |')
                if i == 0: L.append('|' + '---|' * len(row))
        (d/'raw.md').write_text('\n'.join(L), 'utf-8')
    elif ext in ('.md', '.txt'): shutil.copy(f, d/'raw.md')
    elif ext in ('.png', '.jpg', '.jpeg', '.webp'): (d/'media').mkdir(exist_ok=True); shutil.copy(f, d/'media'/f.name); (d/'raw.md').write_text(f'![{f.stem}](media/{f.name})\n', 'utf-8')
    else: ok = False; print(f'Chưa hỗ trợ {ext}: {f.name} (xmind: xuất ra .md/.docx rồi đưa vào inbox)')
    if ok: n += 1; print('Đã chuyển:', f.name)
print(f'Xong {n} file -> {OUT}')
