from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
R=Path(__file__).resolve().parent;V=json.loads((R/'2026-10-13_current-versions.json').read_text());H=json.loads((R/'2026-10-13_current-heads.json').read_text())
for n,v in V.items():
 p=R/'backups'/('audits-'+v)/(n+'-axis-probes');j=p/'axis-probes.json'
 if not j.exists():continue
 d=json.loads(j.read_text());assert d['commit']==H[n] and not d['worktree'];rows=[]
 sheet=Image.new('RGB',(4*360,3*384),'white');draw=ImageDraw.Draw(sheet)
 for index,axis in enumerate(['length','response','onset','depth','appearance','view']):
  variants=['true-35','true-90','counterfactual-35','counterfactual-90']
  measurements={}
  for key in variants:
   lo=np.asarray(Image.open(p/(axis+'_low-'+key+'.png'))).astype(int);hi=np.asarray(Image.open(p/(axis+'_high-'+key+'.png'))).astype(int);measurements[key]=int(np.any(lo!=hi,axis=2).sum())
  variant=max(measurements,key=measurements.get)
  per=[]
  for level in ['low','high']:
   probe=d['probes'][axis+'_'+level]
   for fn,h in probe['images'].items():assert hashlib.sha256((p/fn).read_bytes()).hexdigest()==h
   fn=axis+'_'+level+'-'+variant+'.png';im=Image.open(p/fn);per.append(np.asarray(im));im=im.resize((360,360));col=index%2*2+(level=='high');row=index//2;sheet.paste(im,(col*360,row*384+24));draw.text((col*360+5,row*384+3),axis+' '+level+' '+variant,fill='black')
  delta=np.abs(per[0].astype(int)-per[1].astype(int));pixels=int(np.any(delta,axis=2).sum());assert pixels>100
  rows.append(dict(axis=axis,low_high_changed_pixels=pixels,mean_absolute_rgb_difference=float(delta.mean()),actual_rendered=True,inspected_variant=variant,all_variants_changed_pixels=measurements))
 out=R/'backups'/('independent-audits-'+v);out.mkdir(exist_ok=True,parents=True);sheet.save(out/(n+'-six-axis-inspection.jpg'));(out/(n+'-six-axis-independent.json')).write_text(json.dumps(dict(head_sha=H[n],status='PASS',image_hashes_verified=True,probes=rows),indent=2));print(n,rows)
