"""E2 applier. usage: apply_placements.py check|apply [--out PATH]
Reads placements/*.json (list of {idx,num,line,anchor[,occurrence]}), validates against the
tree and the source snapshot, and (apply) writes the headed file. Prose is never altered:
the proof strips all whitespace and heading lines and compares to the original."""
import re,sys,glob,json
sys.stdout.reconfigure(encoding='utf-8')
D='0-INBOX/temp/TOC-dgongs-pa-rab-gsal'
SRC=D+'/source-snapshot.md'
orig=open(SRC,encoding='utf-8').read()
lines=orig.split('\n')
tree=open('0-INBOX/TOCs/toc-tree-dgongs-pa-rab-gsal.md',encoding='utf-8').read().split('\n')
nodes=[]
for l in tree:
    m=re.match(r'^(\s*)\* (\d+(?:\.\d+)*)\.? (.*)$',l)
    if m: nodes.append((m.group(2),m.group(3).strip()))
def squash(s): return re.sub(r'[\s ]+','',s).replace('༌','་')
def find_anchor(line,anchor,occ=1,minpos=0):
    # whitespace-insensitive search; returns char offset in original line of anchor start
    idxmap=[];buf=[]
    for i,ch in enumerate(line):
        if re.match(r'[\s ]',ch): continue
        buf.append('་' if ch=='༌' else ch); idxmap.append(i)
    s=''.join(buf); a=squash(anchor)
    hits=[];p=0
    while True:
        p=s.find(a,p)
        if p<0: break
        hits.append(idxmap[p]); p+=1
    hits=[h for h in hits if h>=minpos]
    return hits
pl=[]
for f in sorted(glob.glob(D+'/placements/*.json')):
    pl+=json.load(open(f,encoding='utf-8'))
by={}
errs=[]
for p in pl:
    if p['idx'] in by: errs.append(f"duplicate idx {p['idx']} ({p['num']})")
    by[p['idx']]=p
missing=[i for i in range(len(nodes)) if i not in by]
if missing: errs.append(f"missing {len(missing)} nodes: {missing[:40]}{'…' if len(missing)>40 else ''}")
res=[];prev=(0,-1)
for i in range(len(nodes)):
    if i not in by: continue
    p=by[i]
    if p['num']!=nodes[i][0]: errs.append(f"idx {i}: num {p['num']} != tree {nodes[i][0]}")
    ln=p['line']
    if not (1<=ln<=len(lines)): errs.append(f"idx {i}: line {ln} out of range"); continue
    minpos=prev[1] if ln==prev[0] else 0
    hits=find_anchor(lines[ln-1],p['anchor'],minpos=minpos)
    if not hits: errs.append(f"idx {i} {p['num']}: anchor not found at line {ln} (>= offset {minpos}): {p['anchor'][:40]}"); continue
    occ=p.get('occurrence',1)
    if len(hits)>1 and 'occurrence' not in p: errs.append(f"idx {i} {p['num']}: anchor ambiguous ({len(hits)} hits) at line {ln}; give occurrence")
    off=hits[min(occ,len(hits))-1]
    if (ln,off)<prev: errs.append(f"idx {i} {p['num']}: out of document order ({ln},{off}) < {prev}")
    prev=(ln,off); res.append((i,ln,off))
print('placements',len(pl),'resolved',len(res),'errors',len(errs))
for e in errs[:80]: print('ERR',e)
if sys.argv[1]!='apply' or errs: sys.exit(1 if errs else 0)
def heading(num,label):
    k=num.count('.')+1
    h='#'*min(k+1,6)
    t=label.strip()
    t=t.rstrip('་')
    if not t.endswith('།'): t+='།'
    if k+1>6: t=f'**{t}**'
    return f"{h} {t} ^{num.replace('.','-')}-0"
ins={}
for i,ln,off in res: ins.setdefault(ln,[]).append((off,i))
out=[]
for n,l in enumerate(lines,1):
    if n not in ins: out.append(l); continue
    cuts=sorted(ins[n])
    # build: groups of headings sharing an offset
    groups={}
    for off,i in cuts: groups.setdefault(off,[]).append(i)
    p=0
    for off in sorted(groups):
        pre=l[p:off]
        if pre.strip(): out.append(pre); out.append('')
        for i in groups[off]:
            out.append(heading(*nodes[i])); out.append('')
        p=off
    rest=l[p:]
    out.append(rest)
new='\n'.join(out)
# proof: removing heading lines (only those we inserted) leaves same non-whitespace content
hd=set(heading(*nodes[i]) for i in range(len(nodes)))
kept=[x for x in new.split('\n') if x not in hd]
assert squash(''.join(kept))==squash(orig),'PROSE CHANGED'
assert sum(1 for x in new.split('\n') if x in hd)==len(nodes)
outp=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else D+'/headed-candidate.md'
open(outp,'w',encoding='utf-8',newline='').write(new)
print('wrote',outp,'headings',len(nodes),'lines',len(lines),'->',len(new.split('\n')))
