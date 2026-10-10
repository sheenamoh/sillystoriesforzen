import json,re
import os; ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=json.load(open(ROOT+'/data/year1-words.json'))
W={c['char']:c for c in D['chars']}
p=ROOT+'/words/index.html'; s=open(p).read()
def chip(m):
    cls,title,ch=m.group(1),m.group(2),m.group(3)
    c=W[ch]; eps=c['episodes']
    parts=[x for x in cls.split() if x not in('done',)]
    if eps: parts.insert(1,'done')
    head=' · '.join(title.split(' · ')[:2])
    t=head+' · '+('Ep '+', '.join(map(str,eps)) if eps else 'not used yet')
    return f'<span class="{" ".join(parts)}" title="{t}"><b>{ch}</b>'
s=re.sub(r'<span class="(chip[^"]*)" title="([^"]*)"><b>(.)</b>',chip,s)
def les(m):
    body=m.group(0); chars=re.findall(r'<b>(.)</b>',body.split('</h2>',1)[1])
    n=sum(1 for c in chars if W[c]['episodes'])
    return re.sub(r'<small>\d+/\d+</small>',f'<small>{n}/{len(chars)}</small>',body,count=1)
s=re.sub(r'<section class="les">.*?</section>',les,s,flags=re.S)
tot=len(W); cov=sum(1 for c in W.values() if c['episodes'])
wt=[c for c in W.values() if c['write']]; wc=sum(1 for c in wt if c['episodes'])
s=re.sub(r'<b>\d+ / 282</b>(<span>characters already)',f'<b>{cov} / {tot}</b>\\1',s)
s=re.sub(r'(<b>\d+ / 282</b><span>characters already in a story</span><div class="bar"><i style="width:)\d+%',lambda m:m.group(1)+f'{round(cov/tot*100)}%',s)
s=re.sub(r'<b>\d+ / \d+</b>(<span>writing characters)',f'<b>{wc} / {len(wt)}</b>\\1',s)
s=re.sub(r'(<span>writing characters \(习写\) in a story</span><div class="bar"><i style="width:)\d+%',lambda m:m.group(1)+f'{round(wc/len(wt)*100)}%',s)
open(p,'w').write(s); print(cov,tot,wc,len(wt))
