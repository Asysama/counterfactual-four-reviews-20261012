"""Independent full decoded media and phenomenon audit; no generator imports."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
import numpy as np

def decode(path):
 p=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(path),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE);size=2048*2048*3
 try:
  for i in range(120):
   b=bytearray()
   while len(b)<size:
    q=p.stdout.read(size-len(b));assert q,'truncated frame';b.extend(q)
   yield np.frombuffer(b,dtype=np.uint8).reshape(2048,2048,3)
  assert not p.stdout.read(1) and p.wait()==0
 finally:
  p.stdout.close()
  if p.poll() is None:p.terminate();p.wait()

def physical(m,t,c):
 from scipy.integrate import solve_ivp
 p=m['phenomenon_data']['scene_params'];n=m['phenomenon'];on=p['onset'];cut=m['intervention_frame']
 assert p['gravity']==9.81
 for state in [t,c]:assert np.array_equal(state['time'],np.arange(120)/24)
 for key in set(t)&set(c):
  if t[key].ndim and t[key].shape[0]==120:assert np.array_equal(t[key][:cut],c[key][:cut]),key
 tb=m['timebase'];assert abs(tb['physical_dt']*tb['outer_steps_per_recorded_frame']*24-tb['physical_seconds_per_video_second'])<1e-12
 tau=np.arange(120-on)/24
 def ode(rhs,y0):return solve_ivp(rhs,(0,float(tau[-1])),y0,t_eval=tau,rtol=1e-10,atol=1e-12).y.T
 if n.startswith('copper'):
  th=p['theta_equilibrium'];L=p['physical_length'];r=.1*p['bob_radius'];V=4*math.pi*r**3/3;mu0=4*math.pi*1e-7;d=p['magnetic_gap_m']
  B=mu0*p['dipole_moment_Am2']/(2*math.pi*d**3);F=9*V*B*B/(mu0*d)
  assert abs(F/(p['bob_mass']*9.81)-math.tan(th))<1e-10
  expected=ode(lambda tt,y:[y[1],-9.81/L*math.sin(y[0])-p['damping_rate']*y[1]],[th,0])
  assert np.max(abs(c['theta'][on:]-expected[:,0]))<1e-7
  assert np.all(t['theta']==th) and abs(c['theta'][-1])<.006
  assert np.array_equal(t['screen_z'],c['screen_z']) and np.all(np.diff(t['screen_z'][on-6:])==0)
  for s in [t,c]:
   assert np.allclose(np.linalg.norm(s['pos']-p['bob_anchor'],axis=1),p['length'])
   assert np.min(p['screen_x']-.02-s['pos'][:,0]-p['bob_radius'])>.2
  assert np.all(t['transmission']==1) and np.all(c['transmission'][cut:]==0)
  evidence=int(np.flatnonzero((np.arange(120)>=cut)&(abs(c['theta'])<.25*th))[0])
  w=dict(force_to_weight=F/(p['bob_mass']*9.81),equilibrium_tangent=math.tan(th),cf_final_angle=float(c['theta'][-1]),independent_ode_error=float(np.max(abs(c['theta'][on:]-expected[:,0]))))
 elif n.startswith('electrostatic'):
  L=p['physical_length'];q=p['charge_magnitude'];mass=p['bob_mass'];E=p['electric_field'];lim=p['theta_limit']
  assert math.isclose(q,6*math.pi*8.8541878128e-12*(.1*p['bob_radius'])**2*E,rel_tol=1e-12)
  for s in [t,c]:
   assert np.max(abs(s['theta']))<=lim+1e-12
   assert np.allclose(np.linalg.norm(s['pos']-p['bob_anchor'],axis=1),L/.1)
   assert np.max(abs(s['pos'][:,0])+p['bob_radius'])<=p['plate_half_gap']+1e-12
   assert np.min(np.diff(s['contact_times']))>.02
  assert int(t['contact_count'][-1])>=5 and int(c['contact_count'][-1])==3
  assert np.all(c['charge'][cut:]==q) and np.all(c['theta'][cut:]==lim)
  assert np.all(t['charge']==np.where(t['contact_count'].astype(int)%2,-q,q))
  assert q*E*math.cos(lim)-mass*9.81*math.sin(lim)>0
  assert np.all(c['omega'][cut:]==0) and np.all(c['fault'][:cut]==0) and np.all(c['fault'][cut:]==1)
  evidence=int(np.flatnonzero((np.arange(120)>cut)&(t['pos'][:,0]<c['pos'][:,0]-.1))[0])
  w=dict(true_contacts=int(t['contact_count'][-1]),cf_contacts=int(c['contact_count'][-1]),true_contact_times=t['contact_times'].tolist(),contact_charge_retained_C=q,cf_terminal_contact_x=float(c['pos'][-1,0]))
 elif n.startswith('air_gap'):
  L=p['physical_length'];mass=p['card_mass'];arm=L/2+.1*p['card_hinge_offset'];I=mass*(L*L/12+arm*arm);dp=.65*.5*1.2*p['air_speed']**2;F=dp*p['card_area']
  assert math.isclose(I,p['hinge_inertia'],rel_tol=1e-12) and math.isclose(dp,p['pressure_drop'],rel_tol=1e-12)
  errors=[]
  for sign,s in [(1,t),(-1,c)]:
   e=ode(lambda tt,y:[y[1],(sign*F*arm*math.cos(y[0])-mass*9.81*arm*math.sin(y[0]))/I-5*y[1]],[0,0])
   err=float(np.max(abs(e[:,0]-s['theta'][on:])));assert err<1e-7;errors.append(err)
   assert np.min(s['bottom_gap'])>.35 and abs(s['omega'][-1])<.03
   assert np.allclose(s['pressure_difference'][cut:],sign*dp,rtol=1e-12,atol=1e-12)
  eq=math.atan(F/(mass*9.81));assert abs(t['theta'][-1]-eq)<.005 and abs(c['theta'][-1]+eq)<.005
  assert np.allclose(t['theta'],-c['theta'])
  evidence=int(np.flatnonzero((t['theta']>.045)&(c['theta']<-.045))[0])
  w=dict(pressure_drop_Pa=dp,equilibrium_angle=eq,true_final_angle=float(t['theta'][-1]),cf_final_angle=float(c['theta'][-1]),minimum_gap=float(min(t['bottom_gap'].min(),c['bottom_gap'].min())),independent_ode_errors=errors)
 elif n.startswith('rattleback'):
  assert p['skew_angle']<0 and t['spin'][-1]<0
  a,b,z=p['body_axes'];k=p['coupling_rate'];mu=p['mode_damping'];nu=p['spin_damping'];errors=[]
  for sign,s in [(1,t),(-1,c)]:
   e=ode(lambda tt,y:[sign*k*y[1]*y[0]-mu*y[0],-sign*k*y[0]**2-nu*y[1],y[1]],[p['initial_mode_amplitude'],0,0])
   err=float(np.max(abs(e-np.column_stack([s['mode_amplitude'],s['spin'],s['yaw']])[on:])));assert err<1e-7;errors.append(err)
   energy=.5*(s['mode_amplitude']**2+s['spin']**2);assert np.allclose(energy,s['energy']) and np.all(np.diff(energy)<=1e-9)
   assert abs(s['spin'][-1])>.5 and np.max(abs(s['tilt']))<.15 and np.max(np.linalg.norm(s['xy'],axis=1))<.35
   # Independent kinematic reconstruction: no-slip translation matches the moving convex contact.
   theta=s['tilt'];psi=s['yaw'];h=np.sqrt((a*np.sin(theta))**2+(z*np.cos(theta))**2);lever=(a*a-z*z)*np.sin(theta)*np.cos(theta)/h
   td=np.gradient(theta,1/24);vel=np.column_stack([h*td*np.cos(psi)+s['spin']*lever*np.sin(psi),h*td*np.sin(psi)-s['spin']*lever*np.cos(psi)])
   observed=np.gradient(s['xy'],1/24,axis=0);assert np.max(abs(observed[on+2:-2]-vel[on+2:-2]))<.018
  assert t['yaw'][-1]<-2 and c['yaw'][-1]>2 and np.allclose(t['yaw'],-c['yaw'])
  assert p['time_scale']==.25 and tb['physical_seconds_per_video_second']==.25
  evidence=int(np.flatnonzero((t['yaw']<-.25)&(c['yaw']>.25))[0])
  w=dict(true_final_yaw=float(t['yaw'][-1]),cf_final_yaw=float(c['yaw'][-1]),modal_energy_start=float(t['energy'][0]),modal_energy_end=float(t['energy'][-1]),independent_ode_errors=errors,model_scope='declared averaged small-angle modal model; normalized modal energy, not full Newton-Euler')
 else:raise ValueError(n)
 assert evidence==m['evidence_frame'];w['evidence_frame']=evidence;return w

def review(case,head):
 m=json.loads((case/'metadata.json').read_text());assert m['generation']['git']==head and m['render']['native'] and m['render']['res']==[2048,2048]
 paths=[case/m['paths'][b]['video'] for b in ['true','counterfactual']]+[case/m['paths']['counterfactual'][k] for k in ['mask','mask_overlay']]
 for f in paths:
  d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));s=d['streams'][0]
  assert s['codec_name']=='h264' and s['width']==s['height']==2048 and s['avg_frame_rate']=='24/1' and int(s['nb_frames'])==120 and float(d['format']['duration'])==5
 for k,v in json.loads((case/'manifest.json').read_text()).items():
  f=case/k;assert f.stat().st_size==v['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
 readers=[decode(f) for f in paths];first=None;active_frames=[];border_min=2048;mask_min=2048*2048
 try:
  for i in range(120):
   a,b,mask,overlay=[next(q) for q in readers]
   if first is None and not np.array_equal(a,b):first=i
   assert i>=m['intervention_frame'] or np.array_equal(a,b)
   assert np.array_equal(mask[:,:,0],mask[:,:,1]) and np.array_equal(mask[:,:,0],mask[:,:,2]) and np.all((mask==0)|(mask==255))
   active=mask[:,:,0]>0
   if active.any():
    yy,xx=np.where(active);border=min(xx.min(),yy.min(),2047-xx.max(),2047-yy.max());assert border>2 and len(xx)>500
    border_min=min(border_min,int(border));mask_min=min(mask_min,len(xx));active_frames.append(i)
    assert np.all(overlay[active]==[255,0,0])
   assert np.array_equal(overlay[~active],b[~active])
  for q in readers:assert next(q,None) is None
 finally:
  for q in readers:q.close()
 assert first==m['first_changed_frame']==m['mask_start_frame'] and active_frames==list(range(first,120))
 t=dict(np.load(case/m['paths']['true']['trajectory']));c=dict(np.load(case/m['paths']['counterfactual']['trajectory']));w=physical(m,t,c)
 for b in ['true','counterfactual']:assert (case/m['paths'][b]['prompt']).read_text()==m['descriptions'][b]
 return dict(status='PASS',head_sha=head,case_id=m['task_id'],first_changed_frame=first,minimum_target_border_px=border_min,minimum_mask_pixels=mask_min,physical_witnesses=w,decoded_frames_each_stream=120,visual_inspection='PENDING',browser_playback='PENDING')

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('root',type=Path);a.add_argument('--heads',type=Path,required=True);a.add_argument('--output',type=Path,required=True);v=a.parse_args();h=json.loads(v.heads.read_text());rows=[]
 for mf in sorted(v.root.rglob('metadata.json')):
  n=json.loads(mf.read_text())['phenomenon'];rows.append(review(mf.parent,h[n]));print('INDEPENDENT PASS',mf.parent.name,flush=True)
 assert len(rows)==2*len(h) and all(sum(z['case_id'].startswith(n+'_') for z in rows)==2 for n in h)
 v.output.write_text(json.dumps(dict(status='PASS',cases=rows,formal_streams=8*len(h),visual_and_browser_pending=True),indent=2))
