"""Read-only source comparison; write evidence only under the private review tree."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT.parent / 'BioCare-growth-trust-conversion'
SHA = 'e0a668a10ddd6cafdf3f27ee4e6261f7e9caf27e'


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', '-c', 'safe.directory='+cwd.as_posix(), *args],cwd=cwd)


def audit(root):
    code = ('import json,sys; sys.path.insert(0,"scripts"); from validate_compliance import validate_compliance; '
            'from compliance_engine import ComplianceEngine; '
            'print(json.dumps({"standard":validate_compliance(),"strict":validate_compliance(strict=True),'
            '"review":ComplianceEngine().audit_repository()}))')
    return json.loads(subprocess.check_output([sys.executable,'-c',code],cwd=root))


def main():
    assert git('rev-parse','HEAD^{tree}',cwd=BASELINE).strip() == git('rev-parse',SHA+'^{tree}').strip()
    assert not git('diff','--name-only',cwd=BASELINE).strip()
    before,after=audit(BASELINE),audit(ROOT)
    protected=['content/catalog.json','content/product-labels.json','content/library.json','content/growth.json',
               'content/campaigns/core-four.json','content/site.json',
               'reports/v11-3/V11_3_COMPLIANCE_TRIAGE.json',
               'reports/v11-3/V11_3_COMPLIANCE_TRIAGE.md',
               '_review/domain-audit-hardening/XTEND_EDITORIAL_REVIEW.md']
    protected += [p.relative_to(ROOT).as_posix() for p in (ROOT/'content/compliance').glob('*.json')]
    hashes={path:hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for path in protected}
    assert all((ROOT/p).read_bytes().replace(b'\r\n',b'\n')==git('show',SHA+':'+p).replace(b'\r\n',b'\n') for p in protected)
    warnings_before=set(before['standard']['warnings']);warnings_after=set(after['standard']['warnings'])
    # Build line numbers move with layout; compare the underlying occurrences.
    def occurrences(warnings):
        return Counter(re.sub(r':\d+:', ':LINE:', warning) for warning in warnings)
    counts_before,counts_after=occurrences(warnings_before),occurrences(warnings_after)
    def inherited(data):
        return sorted({f['exact_text'] for f in data['review']['findings'] if f['required_action']=='HUMAN_REVIEW_REQUIRED'})
    payload={'baseline':SHA,'protected_files_sha256':hashes,'protected_files_unchanged':True,
        'before':{'warnings':len(warnings_before),'strict_items':len(before['strict']['errors'])},
        'after':{'warnings':len(warnings_after),'strict_items':len(after['strict']['errors']),
                 'red':after['review']['summary']['RED'],'hard_errors':after['standard']['errors']},
        'removed_warning_occurrences':dict(counts_before-counts_after),'added_warning_occurrences':dict(counts_after-counts_before),
        'human_review_text_unchanged':inherited(before)==inherited(after),'human_review_texts':inherited(after)}
    (Path(__file__).parent/'compliance-reconciliation.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,indent=2))
    assert not payload['after']['red'] and not payload['after']['hard_errors'] and payload['human_review_text_unchanged']


if __name__=='__main__':main()
