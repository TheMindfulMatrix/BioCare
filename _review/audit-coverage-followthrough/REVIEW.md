# Audit coverage and editorial followthrough

September 10, 2026 — review candidate, not deployed.

Base: `ef36a71ecc3365fa1a03db18083ac75349c54574` on `main`.
Branch: `agent/audit-editorial-followthrough`.

## Implemented audit correction

The permanent daily auditor now explicitly requests live `robots.txt` and
`sitemap.xml`. Missing files, failed reads, unexpected redirects, malformed
metadata, restrictive crawl rules, wrong domains, and incomplete or duplicate
sitemap coverage produce `ACTION REQUIRED` and a nonzero CLI exit.

The expected domain comes from `content/site.json`; the requested host still
comes from `--base-url`, allowing local/preview checks without changing canonical
metadata. XML namespace and exact canonical page coverage are checked. Robots
must retain the site's unrestricted crawl policy and canonical sitemap URL.
Harmless comments, formatting and extension directives do not fail the check.
Metadata byte parity is also recorded, separately from its semantic gate.

Existing JSON fields remain; new crawl-metadata results and failures are additive.
The existing scheduled workflow already invokes this script, so no new workflow,
permissions, triggers, deployment or production behavior are required.

## Validation

- Canonical build: PASS; normalized generated output unchanged from the base.
- Standard validation: PASS, 71 public pages, 10 Library articles, 45 active and
  8 deferred products.
- Python suite: **124/124 PASS**, including **29 focused domain-audit tests**.
- Measurement suite: **9/9 PASS**.
- Compliance hard gate: PASS; **69 review warnings / 76 strict advisory items**
  preserved. All seven inherited human-review priorities remain open.
- Public safety scan: PASS, 114 files / 71 pages / zero findings.
- New live auditor against `https://themindfulmatrixhealth.com/`: HEALTHY;
  **71 pages and 168 referenced assets** matched the repository build.
- Live `robots.txt` and `sitemap.xml`: both HTTP 200, exact requested .com URLs,
  byte parity and semantic validation passed; sitemap declared all 71 expected
  URLs, with zero missing, unexpected or duplicate entries.

The machine-readable live result is [live-audit.json](live-audit.json). This
checks the unchanged live website using the new local auditor; it is not a claim
that the corrected auditor has already been released to the default branch.
Today's separately completed responsive audit remains historical evidence;
this maintenance change contains no visual or browser-functional edits.

## Editorial deliverables and honest boundaries

See the [editorial status](../audit-editorial-followthrough/EDITORIAL_STATUS.md)
for the Xtend+ substantiation review, completed K2 editorial revision, and new
zinc/copper and magnesium manuscripts with primary-source ledgers.

These are nonpublic research/draft deliverables, not simulated clinical or
company approval. Xtend+ wording, classifications, sources, qualifications and
disclosures are unchanged. Product-label gaps remain visible. The 69/76 counts
were not reduced by this work; their earlier change from 70/77 reflects the
already recorded duplicate-homepage occurrence change.

Publication still requires the documented source/label, qualified review and
release gates. No new guide route, search entry, public claim or product
association has been published. Academy storage work is a separate private
project and is not included in this repository candidate.

## Release handoff

Review this candidate through the normal PR process. No merge, deployment,
claim suppression, issue creation, or automatic implementation workflow was
performed. Once approved and merged, the existing default-branch daily audit
will exercise the new metadata checks.
