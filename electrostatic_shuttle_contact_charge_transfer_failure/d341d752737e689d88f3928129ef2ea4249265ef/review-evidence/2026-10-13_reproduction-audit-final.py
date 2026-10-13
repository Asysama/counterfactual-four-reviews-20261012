"""Independent reproduction comparison, preserving exact masks and dynamics."""
import sys,json,hashlib,subprocess
from pathlib import Path
import numpy as np
base=Path('/opt/siyuan-cf-four-20261012');n=sys.argv[1];version=sys.argv[2] if len(sys.argv)>2 else 'v6';head=json.loads((base/('heads-'+version+'.json')).read_text())[n];cid=n+'_00000042';a=base/('formal-'+version)/n/cid;b=base/('reproduction-'+version)/n/cid;out=base/('independent-audits-'+version)/(n+'-reproduction-diagnostic.json')
ma=json.loads((a/'metadata.json').read_text());mb=json.loads((b/'metadata.json').read_text());assert ma['generation']['git']==mb['generation']['git']==head
for key in ['seed','onset_frame','intervention_frame','first_changed_frame','mask_start_frame','mask_end_frame','evidence_frame','render','camera','descriptions','phenomenon_data','timebase']:assert ma[key]==mb[key],key
for branch in ['true','counterfactual']:
 ta=dict(np.load(a/ma['paths'][branch]['trajectory']));tb=dict(np.load(b/mb['paths'][branch]['trajectory']));assert ta.keys()==tb.keys() and all(np.array_equal(ta[k],tb[k]) for k in ta)
def decode(p):
 proc=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(p),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE);size=2048*2048*3
 try:
  for i in range(120):
   data=bytearray()
   while len(data)<size:
    q=proc.stdout.read(size-len(data));assert q;data.extend(q)
   yield np.frombuffer(data,np.uint8).reshape(2048,2048,3)
  assert not proc.stdout.read(1) and proc.wait()==0
 finally:
  proc.stdout.close()
  if proc.poll() is None:proc.terminate();proc.wait()
results={}
rels=[ma['paths']['true']['video'],ma['paths']['counterfactual']['video'],ma['paths']['counterfactual']['mask'],ma['paths']['counterfactual']['mask_overlay']]
for rel in rels:
 readers=[decode(a/rel),decode(b/rel)];rows=[];maxdiff=0;total=0;maxpixels=0
 try:
  for i in range(120):
   x,y=[next(r) for r in readers];delta=abs(x.astype(np.int16)-y.astype(np.int16));pixels=np.any(delta!=0,axis=2);count=int(pixels.sum());total+=count;maxpixels=max(maxpixels,count);maxdiff=max(maxdiff,int(delta.max()))
   if count:
    yy,xx=np.where(pixels);rows.append(dict(frame=i,pixel_count=count,maximum_channel_difference=int(delta.max()),samples=[dict(x=int(j),y=int(k),original=x[k,j].tolist(),reproduced=y[k,j].tolist()) for k,j in zip(yy[:8],xx[:8])]))
  for r in readers:assert next(r,None) is None
 finally:
  for r in readers:r.close()
 results[rel]=dict(decoded_frames=120,max_channel_difference=maxdiff,total_differing_pixels=total,max_differing_pixels_per_frame=maxpixels,differences=rows,original_sha256=hashlib.sha256((a/rel).read_bytes()).hexdigest(),reproduced_sha256=hashlib.sha256((b/rel).read_bytes()).hexdigest())
 if rel==ma['paths']['counterfactual']['mask']:assert maxdiff==0
out.write_text(json.dumps(dict(head_sha=head,case_id=cid,trajectory_and_recipe_exact=True,streams=results),indent=2));print(json.dumps(results,indent=2))

# Across independent GPU runs only: tolerate sparse one-level RGB rounding.
# Within-pair decoded prefix and all masks still require exact equality.
assert all(x['max_channel_difference']<=1 and x['max_differing_pixels_per_frame']<=4 and x['total_differing_pixels']<=32 for x in results.values())
receipt=dict(status='PASS',head_sha=head,case_id=cid,trajectory_and_recipe_exact=True,mask_exact=True,decoded_frames_per_stream=120,independent_run_rgb_tolerance=dict(max_channel_difference=1,max_pixels_per_frame=4,max_pixels_per_stream=32),measured_streams=results,explanation='Independent GPU runs may differ at sparse one-level RGB rounding; this does not relax exact within-pair prefixes or formal masks. Original zero-difference comparison is retained.')
(out.parent/(n+'-reproduction-validated.json')).write_text(json.dumps(receipt,indent=2))
