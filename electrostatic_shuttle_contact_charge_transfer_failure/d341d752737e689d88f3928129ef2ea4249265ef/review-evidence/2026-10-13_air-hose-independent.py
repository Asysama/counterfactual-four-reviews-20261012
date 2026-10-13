"""Actual static hose mesh against all240 evaluated target poses, independent BVH."""
import sys,json,subprocess
from pathlib import Path
import bpy
from mathutils.bvhtree import BVHTree
root=Path(sys.argv[1]);gen=Path(sys.argv[2]);out=Path(sys.argv[3]);sys.path.insert(0,str(gen))
from src import violation
from engine import geometry as geo
import numpy as np
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=gen,text=True).strip();rows=[]
def bvh(obj):
 ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();tree=BVHTree.FromPolygons([ev.matrix_world@v.co for v in me.vertices],[tuple(p.vertices) for p in me.polygons],all_triangles=False,epsilon=.0001);ev.to_mesh_clear();return tree
for mf in root.glob('*/metadata.json'):
 m=json.loads(mf.read_text());assert m['generation']['git']==head;p=m['phenomenon_data']['scene_params'];look,dist=violation.camera(p);geo.setup(p,look,dist,2048);violation.scene(p);bpy.context.view_layer.update();hose=bvh(bpy.data.objects['connected_air_hose']);tested=0
 for branch in ['true','counterfactual']:
  state=dict(np.load(mf.parent/m['paths'][branch]['trajectory']))
  for i in range(120):
   geo.clear_dynamic();violation.frame(p,state,i);bpy.context.view_layer.update()
   for o in bpy.data.objects:
    if o.name.startswith('hinged_hard_card'):assert not hose.overlap(bvh(o)),(m['seed'],branch,i,o.name);tested+=1
 rows.append(dict(case_id=m['task_id'],evaluated_card_mesh_checks=tested,collision_pairs=0));assert tested==480
assert len(rows)==2
out.write_text(json.dumps(dict(status='PASS',head_sha=head,method='Actual evaluated world-space hose and card triangle BVH intersection;0.0001 tolerance',cases=rows),indent=2));print('HOSE GEOMETRY PASS',rows)
