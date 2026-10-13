"""Save decoded native temporal crops and full scenes; no source imports."""
from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False);rows=[]
def frame(path,i):
 data=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-i',str(path),'-vf',f'select=eq(n\\,{i})','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
 assert len(data)==2048*2048*3;return np.frombuffer(data,np.uint8).reshape(2048,2048,3)
for mf in sorted(root.glob('*/metadata.json')):
 m=json.loads(mf.read_text());case=mf.parent;d=out/m['task_id'];d.mkdir();e=m['evidence_frame'];frames=sorted(set([0,m['intervention_frame'],e,max(e+1,70),119]));sheet=Image.new('RGB',(512*len(frames),2*536),'white');draw=ImageDraw.Draw(sheet)
 for row,b in enumerate(['true','counterfactual']):
  for col,i in enumerate(frames):
   a=frame(case/m['paths'][b]['video'],i);sheet.paste(Image.fromarray(a).resize((512,512)),(512*col,row*536+24));draw.text((512*col+5,row*536+4),f'{b} frame {i}',fill='black')
 sheet.save(d/'full-scenes.jpg',quality=95)
 mask=frame(case/m['paths']['counterfactual']['mask'],e);yy,xx=np.where(mask[:,:,0]>0);assert len(xx);box=(max(0,int(xx.min())-64),max(0,int(yy.min())-64),min(2048,int(xx.max())+65),min(2048,int(yy.max())+65))
 for i in range(max(0,e-1),min(120,e+3)):
  for label,rel in [('cf',m['paths']['counterfactual']['video']),('mask',m['paths']['counterfactual']['mask']),('overlay',m['paths']['counterfactual']['mask_overlay'])]:
   im=Image.fromarray(frame(case/rel,i));im.crop(box).save(d/f'native-{label}-{i:03d}.png')
 rows.append(dict(case_id=m['task_id'],head_sha=m['generation']['git'],source_native_resolution=[2048,2048],full_scene_frames=frames,native_crop_box=box,native_consecutive_frames=list(range(max(0,e-1),min(120,e+3))),files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in d.iterdir()}))
 print('NATIVE INSPECTION MATERIAL',m['task_id'],flush=True)
(out/'manifest.json').write_text(json.dumps(rows,indent=2))
