"""Independent evaluated-mesh/support audit on exact submitted trajectories."""
import sys,json,math,subprocess
from pathlib import Path
import numpy as np
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
root=Path(sys.argv[1]);gen=Path(sys.argv[2]);out=Path(sys.argv[3]);sys.path.insert(0,str(gen))
from src import violation
from engine import geometry as geo
rows=[]
for mf in sorted(root.glob('*/metadata.json')):
 m=json.loads(mf.read_text());p=m['phenomenon_data']['scene_params'];name=m['phenomenon'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=gen,text=True).strip()==m['generation']['git']
 look,dist=violation.camera(p);s,cam,pos,target=geo.setup(p,look,dist,2048);violation.scene(p);minimum=1.;low=10.;high=-10.;seen=set()
 if name.startswith('electrostatic'):
  mounts=[o for o in bpy.data.objects if o.name.startswith('electrode_grounded_mount')]
  assert len(mounts)==2
  for o in mounts:assert abs(o.location.z-o.dimensions.z/2-.20)<1e-6
 if name.startswith('air_gap'):
  mounts=[o for o in bpy.data.objects if o.name.startswith('hinge_mount')]
  for o in mounts:assert o.location.y-o.dimensions.y/2>(p['card_width']+.02)/2
 for branch in ['true','counterfactual']:
  state=dict(np.load(root/m['task_id']/m['paths'][branch]['trajectory']))
  for i in range(120):
   geo.clear_dynamic();violation.frame(p,state,i);bpy.context.view_layer.update()
   cam.location=pos.copy();cam.location.x+=.025*i/119;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
   targets=[o for o in bpy.data.objects if o.get('target')];assert {o.name for o in targets}==set(m['mask_spec']['target_entities'])
   for o in targets:
    seen.add(o.name);ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
    world=np.array([list(ev.matrix_world@v.co) for v in mesh.vertices]);low=min(low,float(world[:,2].min()));high=max(high,float(world[:,2].max()))
    for k in np.linspace(0,len(world)-1,min(200,len(world)),dtype=int):
     uv=world_to_camera_view(s,cam,Vector(world[k]));assert uv.z>0
     margin=min(uv.x,uv.y,1-uv.x,1-uv.y);minimum=min(minimum,margin);assert margin>.008,(name,branch,i,o.name,margin)
    if name.startswith('rattleback'):
     assert world[:,2].min()>=.44-1e-6
     if o.name=='continuous_convex_rattleback':assert world[:,2].min()<.443,(branch,i,world[:,2].min())
    elif name.startswith('electrostatic'):
     assert world[:,0].max()<=p['plate_half_gap']+1e-6 and world[:,0].min()>=-p['plate_half_gap']-1e-6
    elif name.startswith('copper'):
     assert world[:,0].max()<p['screen_x']-.02
    elif name.startswith('air_gap'):assert world[:,2].min()>.55
    ev.to_mesh_clear()
 rows.append(dict(case_id=m['task_id'],head_sha=m['generation']['git'],status='PASS',tested_frames_per_branch=120,minimum_target_camera_margin=float(minimum),target_z_bounds=[low,high],target_objects=sorted(seen),support_checks='evaluated vertices / analytic support dimensions, followed by separate decoded visual inspection'))
 print('GEOMETRY PASS',m['task_id'],flush=True)
assert len(rows)==2
out.write_text(json.dumps(dict(status='PASS',cases=rows),indent=2))
