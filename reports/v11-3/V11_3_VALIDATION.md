# V11.3 Validation

Candidate evidence source: `2d44a2f9d334501e815da2a1f1ed4da40e5ed519`

## Local candidate

- Two deterministic builds: PASS; no generated public-site drift
- Permanent validator: PASS
- Public pages: 69
- Published articles: 10
- Products: 45 active / 8 deferred
- Compliance hard gate: PASS with 0 errors
- Review warnings: 70
- Strict advisory items: 77
- Unit tests: 67 PASS, including two new workflow-governance tests
- JavaScript syntax: PASS
- Git diff check: PASS
- Legacy Actions major scan: PASS
- Secret scan: PASS
- Private-resource boundary tests: PASS

## GitHub-hosted workflow

- Manual daily audit run: https://github.com/TheMindfulMatrix/BioCare/actions/runs/32749131195
- Result: SUCCESS
- Workflow source SHA: `2d44a2f9d334501e815da2a1f1ed4da40e5ed519`
- Audited default-branch content: `af75af00ddb5c41b72e08d9e094c0c4f609cc0f9`
- Repository tests in the default-branch audit snapshot: 65 PASS
- Responsive states: 276
- Overflow failures: 0
- Broken images: 0
- Failed requests: 0
- Console errors: 0
- Functional failures: 0
- Node.js 20 deprecation annotations: 0

The workflow intentionally checks out the authoritative default branch even when manually dispatched from the candidate ref. PR validation separately tests the candidate branch.
