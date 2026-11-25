# Gộp site thành 1 file preview.html (nhúng dữ liệu + ảnh) để xem nhanh, không cần server
import json,re,base64,pathlib,subprocess,sys
r=pathlib.Path(__file__).parent;subprocess.run([sys.executable,str(r/'scripts/build_index.py')],check=True);idx=json.loads((r/'data/index.json').read_text('utf-8'));files={}
for p in idx['posts']:
    t=(r/p['path']).read_text('utf-8')
    t=re.sub(r'\((assets/img/[^)]+)\)',lambda m:'(data:image/png;base64,'+base64.b64encode((r/m.group(1)).read_bytes()).decode()+')',t)
    files[p['path']]=t
h=(r/'index.html').read_text('utf-8')
h=h.replace('<script>\nconst $=','<script>window.__KB__='+json.dumps({'index':idx,'files':files},ensure_ascii=False)+';</script>\n<script>\nconst $=',1)
(r/'preview.html').write_text(h,'utf-8');print(len(h)//1024,'KB')
