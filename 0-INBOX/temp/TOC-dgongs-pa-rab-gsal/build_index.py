import re,sys,glob,json,os
sys.stdout.reconfigure(encoding='utf-8')
D='0-INBOX/temp/TOC-dgongs-pa-rab-gsal'
src=D+'/source-snapshot.md'
text=open(src,encoding='utf-8').read()
def norm(s): return re.sub(r'[\s ]+','',s).replace('༌','་')
lines=text.split('\n')
lmap=[];nt=[]
for i,l in enumerate(lines):
    n=norm(l); nt.append(n); lmap+=[i+1]*len(n)
N=''.join(nt)
tree=open('0-INBOX/TOCs/toc-tree-dgongs-pa-rab-gsal.md',encoding='utf-8').read().split('\n')
nodes=[]
for l in tree:
    m=re.match(r'^(\s*)\* (\d+(?:\.\d+)*)\.? (.*)$',l)
    if m: nodes.append((m.group(2),m.group(3).strip()))
ORD=['དང་པོ་','གཉིས་པ་','གསུམ་པ་','བཞི་པ་','ལྔ་པ་','དྲུག་པ་','བདུན་པ་','བརྒྱད་པ་','དགུ་པ་','བཅུ་པ་']
def core(t):
    t=norm(t)
    for o in ORD:
        if t.startswith(o): return t[len(o):]
    return t
out=['idx\tnum\tdepth\tlabel\tlines_where_label_core_occurs']
for i,(num,t) in enumerate(nodes):
    c=core(t); ls=[]; s=0
    while True:
        p=N.find(c,s)
        if p<0: break
        if not ls or ls[-1]!=lmap[p]: ls.append(lmap[p])
        s=p+1
    out.append(f"{i}\t{num}\t{num.count('.')+1}\t{t}\t{','.join(map(str,ls[:12]))}{'…' if len(ls)>12 else ''}")
open(D+'/tree-index.tsv','w',encoding='utf-8').write('\n'.join(out)+'\n')
# windows by bytes
tot=sum(len(l.encode())+1 for l in lines); K=8; tgt=tot/K
w=[];start=1;acc=0
for i,l in enumerate(lines):
    acc+=len(l.encode())+1
    if acc>=tgt and len(w)<K-1 and (l.strip()==''):
        w.append((start,i+1)); start=i+2; acc=0
w.append((start,len(lines)))
open(D+'/windows.tsv','w').write('\n'.join(f"{k+1}\t{a}\t{b}" for k,(a,b) in enumerate(w))+'\n')
print(len(nodes),len(lines),w)
