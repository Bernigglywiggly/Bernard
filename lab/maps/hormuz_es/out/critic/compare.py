import json, re, unicodedata, difflib, sys
sys.path.insert(0,'.')
import importlib.util
spec=importlib.util.spec_from_file_location('s','script.py'); s=importlib.util.module_from_spec(spec)
# script references nothing external
spec.loader.exec_module(s)
said=[]
for ch in s.CHAPTERS:
    for k,b in enumerate(ch['beats']):
        t=b[0]; said.append((f"{ch['id']}_{k:02d}", t[1] if isinstance(t,tuple) else t))
tr={json.loads(l)['id'][4:]: json.loads(l) for l in open('out/critic/transcripts.jsonl')}
N={'0':'cero','1':'uno','2':'dos','3':'tres','4':'cuatro','5':'cinco','6':'seis','7':'siete','8':'ocho','9':'nueve','10':'diez','11':'once','12':'doce','13':'trece','18':'dieciocho','20':'veinte','21':'veintiuno','28':'veintiocho','39':'treinta y nueve','125':'ciento veinticinco','1971':'mil novecientos setenta y uno','2008':'dos mil ocho','2024':'dos mil veinticuatro'}
def norm(x):
    x=unicodedata.normalize('NFD',x.lower()); x=''.join(c for c in x if unicodedata.category(c)!='Mn')
    x=re.sub(r'%',' por ciento',x)
    x=re.sub(r"[^\w\s]",' ',x)
    w=x.split(); out=[]
    for t in w: out+= N.get(t,t).split()
    return out
for i,(id_,t) in enumerate(said):
    h=tr[id_]['text']; a=norm(t); b=norm(h)
    sm=difflib.SequenceMatcher(None,a,b)
    diffs=[(op,' '.join(a[i1:i2]),' '.join(b[j1:j2])) for op,i1,i2,j1,j2 in sm.get_opcodes() if op!='equal']
    low=[w for w in tr[id_]['words'] if w[3]<0.5]
    if diffs or low:
        print(f"{i:02d} {id_}: ratio={sm.ratio():.3f}")
        for d in diffs: print("    ",d)
        if low: print("     lowprob:",[(w[0].strip(),w[3]) for w in low])
