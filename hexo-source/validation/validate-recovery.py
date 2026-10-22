from pathlib import Path
from bs4 import BeautifulSoup
import json, re, hashlib, difflib
from urllib.parse import urlsplit, unquote
R=Path(__file__).resolve().parents[2]
H=R/'hexo-source'; manifest=json.loads((H/'RECOVERY_MANIFEST.json').read_text(encoding='utf-8'))
def codes(b):
    return ['\n'.join(x.get_text() for x in f.select('td.code > pre > span.line')) for f in b.select('figure.highlight')]
def norm(b):
    b=BeautifulSoup(str(b),'html.parser')
    for x in b.select('header,.gutter,a.headerlink'): x.decompose()
    return re.sub(r'\s+', '', b.get_text())
checks=[]
for rec in manifest['records']:
    assert hashlib.sha256((R/rec['source']).read_bytes()).hexdigest()==rec['source_sha256']
    fm=(R/rec['markdown']).read_text(encoding='utf-8').split('---',2)[1]
    assert 'date: '+json.dumps(rec['date']) in fm
    assert 'updated: '+json.dumps(rec['updated']) in fm
    s=BeautifulSoup((R/rec['source']).read_text(encoding='utf-8'),'html.parser'); g=BeautifulSoup((H/'public'/rec['source']).read_text(encoding='utf-8'),'html.parser')
    a=s.select_one('#article-container') or s.select_one('.article-entry'); b=g.select_one('#article-container')
    if a.select_one('header'): a.select_one('header').decompose()
    expected=norm(a); actual=norm(b)
    # The sole added content is a real download link replacing the nonfunctional
    # presentation of that link only as an HTML code example.
    extra=b.select_one('a[download]')
    if extra: extra.decompose()
    actual=norm(b)
    result={'url':'/'+rec['permalink'],'body_equal':expected==actual,'code_equal':codes(a)==codes(b),'code_blocks':len(codes(a)),'title_equal':g.select_one('h1').get_text(strip=True)==rec['title'],'date_equal':g.select_one('.post-meta-date-created')['datetime']==rec['date'] if g.select_one('.post-meta-date-created') else 'preserved in page front matter','images_equal':[x.get('src') for x in a.select('img')]==[x.get('src') for x in b.select('img')],'missing_anchors':[],'missing_content_links':[]}
    for x in a.select('[id]'):
        if not g.find(id=x['id']): result['missing_anchors'].append(x['id'])
    for x in a.select('a[href],img[src]'):
        u=x.get('href') or x.get('src'); v=urlsplit(u)
        if v.scheme or v.netloc: continue
        path=unquote(v.path)
        if path.startswith('/'): dest=H/'public'/path.lstrip('/')
        else: dest=(H/'public'/rec['source']).parent/path
        if not path: dest=H/'public'/rec['source']
        if dest.is_dir(): dest=dest/'index.html'
        if not dest.exists(): result['missing_content_links'].append(u)
    result['taxonomy_equal'] = all(g.select_one('a[href="/categories/'+ '/'.join(rec['categories'][:i+1]) +'/"]') for i in range(len(rec['categories']))) if rec['classification']=='recovered article' else True
    if rec['classification']=='recovered article':
        hrefs={unquote(x.get('href','')) for x in g.select('a[href]')}
        result['taxonomy_equal'] = result['taxonomy_equal'] and all('/tags/'+t+'/' in hrefs for t in rec['tags'])
    if expected!=actual:
        result['text_diff']='\n'.join(difflib.unified_diff([expected],[actual]))[:4000]
    checks.append(result)
asset=H/'public/files/pve9-upgrade-kit.sh'
report={'checks':checks,'asset_byte_equal':asset.read_bytes()==(R/'files/pve9-upgrade-kit.sh').read_bytes(),'asset_sha256':hashlib.sha256(asset.read_bytes()).hexdigest()}
missing=set()
for p in (H/'public').rglob('*.html'):
    s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    for x in s.select('a[href],img[src],script[src],link[href]'):
        u=x.get('href') or x.get('src'); v=urlsplit(u)
        if v.scheme or v.netloc or not v.path: continue
        d=H/'public'/unquote(v.path).lstrip('/') if v.path.startswith('/') else p.parent/unquote(v.path)
        if d.is_dir(): d=d/'index.html'
        if not d.exists(): missing.add(u)
report['missing_site_local_links']=sorted(missing)
report['status']='PASS' if report['asset_byte_equal'] and not missing and all(c['images_equal'] and c['body_equal'] and c['code_equal'] and c['title_equal'] and c['taxonomy_equal'] and c['date_equal'] and not c['missing_anchors'] and not c['missing_content_links'] for c in checks) else 'FAIL'
print(json.dumps(report,ensure_ascii=False,indent=2))
(H/'RECOVERY_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
assert report['status']=='PASS'
