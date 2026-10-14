from pathlib import Path
import json,subprocess,os,time
R=Path('/opt/siyuan-cf-four-20261012');H=json.loads((R/'owner-heads-v2.json').read_text());py=str(R/'runtime/bin/python');env=os.environ|{'DISPLAY':':60','OPENBLAS_NUM_THREADS':'1'}
for n,h in H.items():
 start=time.monotonic()
 while not (R/(n+'-owner-v2-complete')).exists():
  if (R/'owner-v2-results.json').exists():
   for a,b in json.loads((R/'owner-v2-results.json').read_text()):
    if a==n and b!='PASS':raise RuntimeError((a,b))
  assert time.monotonic()-start<6500;time.sleep(15)
 repo=R/'owner-verified-v2'/n;g=repo/'generators'/n;ev=R/'owner-audits-v2'/n;orig=R/'owner-formal-v2'/n;out=R/'owner-reproduction-v2'/n
 def run(args,log,expected=0):
  with (ev/log).open('w') as f:p=subprocess.run([str(a) for a in args],cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT)
  assert (p.returncode==0)==(expected==0),(n,log,p.returncode)
 run([py,g/'examples/generate.py','--num-cases','2','--seeds','42,98','--output',orig,'--resume'],'resume.log')
 run([py,g/'examples/generate.py','--num-cases','3','--seeds','42,98','--output',orig,'--resume'],'incompatible-resume.log',1)
 assert 'incompatible resume' in (ev/'incompatible-resume.log').read_text()
 run([py,R/'review-scripts/run_with_provenance.py','--generator',n,'--case-set','owner-reproduction-seed42','--artifact-root',out,'--record',out/'runtime-witness.json','--dependency-lock',g/'requirements.txt','--runtime-component','purpose=independent_reproduction','--',py,g/'examples/reproduce.py','--case',orig/(n+'_00000042'),'--output',out],'reproduce.log')
 run([py,R/'review-scripts/audit_runtime_witness.py','--witness',out/'runtime-witness.json','--artifact-root',out],'reproduce-runtime.json')
 run([py,R/'owner-reproduction-check.py',n],'reproduction-check.log')
 subprocess.run(['tar','czf',str(R/(n+'-owner-v2-final.tar.gz')),'owner-audits-v2/'+n,'owner-reproduction-v2/'+n],cwd=R,check=True)
 (R/(n+'-owner-v2-final-complete')).write_text(h);print('FINAL CHECK COMPLETE',n,flush=True)
