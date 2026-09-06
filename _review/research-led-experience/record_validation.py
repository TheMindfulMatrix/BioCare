"""Record repeatable local validation and exact public-file fingerprints."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import subprocess
import sys
import argparse
import shutil

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scripts.site_paths import audited_page_paths
from scripts.daily_audit import build_bytes

def public_files():
    paths={ROOT/(p or 'index.html') for p in audited_page_paths(ROOT)}
    paths.update(ROOT/name for name in ('robots.txt','sitemap.xml','CNAME') if (ROOT/name).is_file())
    for folder in ('assets','img'):
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    return sorted(paths)

def fingerprint():
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(build_bytes(p)).hexdigest() for p in public_files()}
    digest=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
    return {'sha256':digest,'hash_basis':'GitHub/Linux LF text bytes via the existing audit build_bytes; binary files unchanged','files':files}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--node',default=shutil.which('node') or 'node')
    args=parser.parse_args()
    results=[]
    def run(label,command):
        done=subprocess.run(command,cwd=ROOT,capture_output=True,encoding='utf-8',errors='replace',
            env={**__import__('os').environ,'PYTHONIOENCODING':'utf-8'})
        output=done.stdout+done.stderr
        results.append({'name':label,'command':[Path(command[0]).name,*command[1:]],'exit_code':done.returncode,'output':output})
        print(f'{label}: exit {done.returncode}',flush=True)
        if done.returncode:raise RuntimeError(label+' failed: '+output[-2500:])
    run('build-first',[sys.executable,'scripts/build.py'])
    before=fingerprint()
    run('build-second',[sys.executable,'scripts/build.py'])
    after=fingerprint()
    assert before==after, 'Canonical output changed on second build'
    run('hard-validation',[sys.executable,'scripts/validate.py'])
    run('compliance-strict-dry-run',[sys.executable,'scripts/validate.py','--compliance-strict','--compliance-dry-run'])
    run('python-tests',[sys.executable,'-m','unittest','discover','-s','tests','-v'])
    run('javascript-tests',[args.node,'--test','tests/measurement.test.cjs'])
    run('public-safety',[sys.executable,'scripts/scan_v10_public_safety.py'])
    assert fingerprint()==after, 'Validation changed public files'
    (HERE/'validation-results.json').write_text(json.dumps({'checked_utc':datetime.now(timezone.utc).isoformat(),'deterministic':True,'results':results},indent=2)+'\n',encoding='utf-8')
    (HERE/'public-file-fingerprints.json').write_text(json.dumps(after,indent=2)+'\n',encoding='utf-8')
    print('Public artifact digest: '+after['sha256'])

if __name__=='__main__':main()
