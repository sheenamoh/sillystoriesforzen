# Builds words/index.html (Year 1 + Year 2) from data/year1-words.json and data/year2-words.json
import json,re,os,html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Y1=json.load(open(ROOT+'/data/year1-words.json')); Y2=json.load(open(ROOT+'/data/year2-words.json'))
old=open(ROOT+'/words/index.html').read()
head=old[:old.index('</style>')]
if '.yr{' not in head:
    head+=('.yr{display:flex;flex-direction:column;gap:18px;padding-top:6px}'
           '.yr>h2{font-family:"ZCOOL KuaiLe",sans-serif;font-weight:400;font-size:1.9rem;margin:0;color:var(--sea)}'
           '.yr>h2 small{font-family:Nunito,sans-serif;font-size:.9rem;color:var(--muted);margin-left:8px}'
           '.jump{display:flex;gap:8px;flex-wrap:wrap}.jump a{font-family:Nunito,sans-serif;font-weight:800;font-size:.85rem;color:var(--sea);text-decoration:none;border:2px solid var(--sea);border-radius:999px;padding:4px 14px}\n')
head=re.sub(r'<title>.*?</title>','<title>生字表</title>',head)
def lname(u,l):
    if u.startswith('识字'): return u
    return f'第{u}单元 · 第{l}课'
def chip(c,w):
    eps=c['episodes']; cls='chip'+(' done' if eps else '')+(' w' if w else '')
    t=f"{c['pinyin']} · {c['en']} · "+('Ep '+', '.join(map(str,eps)) if eps else 'not used yet')
    return f'<span class="{cls}" title="{html.escape(t)}"><b>{c["char"]}</b><i>{c["pinyin"]}</i><em>{html.escape(c["en"])}</em></span>'
def stat(n,tot,label):
    return f'<div class="stat"><b>{n} / {tot}</b><span>{label}</span><div class="bar"><i style="width:{round(n/tot*100)}%"></i></div></div>'
def year(D,first_only_new):
    W={c['char']:c for c in D['chars']}; secs=[]
    for L in D['lessons']:
        seen=[]; 
        for ch in L['read']+L['write']:
            if ch in seen: continue
            if W[ch]['lesson']==L['tag']: seen.append(ch)
        n=sum(1 for ch in seen if W[ch]['episodes'])
        chips=''.join(chip(W[ch],ch in L['write']) for ch in seen)
        secs.append(f'<section class="les"><h2>{lname(L["unit"],L["lesson"])}<small>{n}/{len(seen)}</small></h2><div class="chips">{chips}</div></section>')
    pool=[c for c in D['chars'] if (c.get('new',True) if first_only_new else True)]
    wr=[c for c in D['chars'] if c['write']]
    s1=stat(sum(1 for c in pool if c['episodes']),len(pool),'new characters already in a story' if first_only_new else 'characters already in a story')
    s2=stat(sum(1 for c in wr if c['episodes']),len(wr),'writing characters (习写) in a story')
    return f'<div class="sum">{s1}{s2}</div>'+''.join(secs)
key=('<div class="key"><span><i class="sw" style="background:var(--done)"></i>used in a story</span>'
     '<span><i class="sw" style="border:2px solid var(--crayon)"></i>must learn to write (习写)</span></div>')
body=(f'</style></head><body translate="no" class="notranslate"><div class="wrap">\n<a class="back" href="../">← All episodes</a>\n<h1>生字表</h1>\n'
      f'<nav class="jump"><a href="#y1">一年级 Year 1</a><a href="#y2">二年级 Year 2</a></nav>\n{key}\n'
      f'<section class="yr" id="y1"><h2>一年级<small>识字一 → 第十单元 · Year 1 exam</small></h2>{year(Y1,False)}</section>\n'
      f'<section class="yr" id="y2"><h2>二年级<small>第十一 → 第二十二单元 · Year 2</small></h2>{year(Y2,True)}</section>\n'
      '</div></body></html>')
open(ROOT+'/words/index.html','w').write(head+body)
y1c=sum(1 for c in Y1['chars'] if c['episodes']); y1w=[c for c in Y1['chars'] if c['write']]
print('Y1',y1c,len(Y1['chars']),sum(1 for c in y1w if c['episodes']),len(y1w))
n2=[c for c in Y2['chars'] if c['new']]; w2=[c for c in Y2['chars'] if c['write']]
print('Y2',sum(1 for c in n2 if c['episodes']),len(n2),sum(1 for c in w2 if c['episodes']),len(w2))
