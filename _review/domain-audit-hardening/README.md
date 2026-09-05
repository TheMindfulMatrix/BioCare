# Domain, Library and audit hardening — review candidate

Date: 2026-09-05

Status: **VALIDATED CANDIDATE — release authorized by the user on 2026-09-05.** Final deployment and production verification will be recorded on the release PR; this document records the pre-release validation, not a deployment claim.

- Branch: `agent/domain-audit-hardening`
- Production baseline: `57bc4256f48ea7346c5ac1d76bad3669b24829ca` (`Create CNAME`)
- Target domain: `https://themindfulmatrixhealth.com/`
- Separate V12 draft PR #26 and its worktree were left untouched.

## Requested work

| Item | Candidate result |
| --- | --- |
| Library with Reduce Motion | Decorative initialization is isolated; Library filtering and dock wayfinding always initialize. Search, category, Core Four, empty state, reset and collection URL state pass under both motion settings. Clear also removes the Core Four selection. |
| Domain migration | All 69 canonical/social/structured-data page URLs regenerated from the approved domain configuration. Sitemap and robots now reference the custom domain. Validation checks CNAME consistency and rejects the old host in generated public markup. Relative navigation remains subpath-compatible. |
| False healthy audit | Correct sitemap namespace; independent canonical-content page inventory; configured target base honored. Empty, partial, duplicate, wrong-domain, malformed or missing sitemap coverage fails closed. Missing assets, HTTP/network failures and byte drift fail. Asset discovery includes HTML, lazy attributes, social images, CSS and embedded search/catalog/structured data. |
| Tablet hero | Only the existing 44.01rem–56rem breakpoint changed. Product artwork and text have separate space; labels no longer cover packaging. An artwork-aware overlap assertion now supplements viewport-overflow checks. |
| Editorial queue | Xtend+ first-priority source/context review documented in [XTEND_EDITORIAL_REVIEW.md](XTEND_EDITORIAL_REVIEW.md). It remains open for human judgment; no claim rewritten, approved or suppressed. |

## Final validation

| Check | Result |
| --- | --- |
| Canonical build and structural validation | PASS — 69 pages; 10 guides; 45 active / 8 deferred products |
| Unit tests | **84/84 PASS**, including 17 new regression tests |
| Normal compliance hard gate | PASS; zero RED registry claims |
| Strict dry run | **70 review warnings / 77 strict advisory items**, unchanged; strict enforcement would still fail on that inherited backlog |
| Priority reconciliation | 7 P1 / 34 P2 / 36 P3; seven P1 items remain inherited `HUMAN_REVIEW_REQUIRED` |
| Deterministic rebuild | 72/72 generated files unchanged on repeat build |
| Canonical HTML content preservation | 69/69 equal to baseline after normalizing only domain URLs and CSS/JS cache-version strings |
| Public safety scanner | PASS — 69 public pages / 110 files; zero findings |
| JavaScript syntax / diff whitespace | PASS |
| Controlled preview parity | **69/69 pages + 164/164 referenced assets**, HTTP 200 and Linux-normalized build-byte parity; no coverage errors |
| Responsive browser run | **276 states** (69 pages at 1440, 768, 390 and 375px); zero recorded failures |
| Library motion checks | 8/8 viewport/motion combinations; search, empty state, category, Core Four, clear and current-page indicator pass |
| Additional tablet checks | 705, 768, 820 and 896px, under both motion settings; all packaging/label/copy separation assertions pass |
| Phone/desktop preservation | Hero geometry equals baseline CSS at 375, 390, 704, 897 and 1440px |
| Negative control | The new tablet overlap assertion detects the baseline CSS defect |

Browser run recorded zero viewport overflow, broken images, unexpected H1 counts, duplicate IDs, unnamed controls, HTTP errors, failed requests, console errors/warnings, functional failures or missing coverage. These are automated accessibility basics, not a complete accessibility certification.

Generated-output manifest SHA-256 (sorted compact JSON of path-to-LF-normalized-SHA-256 for the 69 pages, sitemap, robots and search index):

`9e2739c40bf430342198b346e3a835c30d5d7c914984371b7250c7afddf77ce7`

No catalog, pricing, manufacturer links, public-source records, campaign content, claims, qualifications or disclosures changed. No new runtime dependency or image asset was added. The existing audit schedule and read-only repository permissions were preserved.

## Review evidence

Evidence is retained locally under `outputs/domain-audit-hardening/`; do not add that folder to the production publishing tree merely to share screenshots.

- [Tablet after](../../outputs/domain-audit-hardening/browser/home-tablet-768.png) / [tablet before](../../outputs/domain-audit-hardening/browser/home-tablet-768-before.png)
- [390px phone](../../outputs/domain-audit-hardening/browser/home-mobile-390.png) / [375px phone](../../outputs/domain-audit-hardening/browser/home-mobile-375.png)
- [Desktop](../../outputs/domain-audit-hardening/browser/home-desktop-1440.png)
- [Full browser results](../../outputs/domain-audit-hardening/browser/browser-audit.json)
- [Page/asset parity](../../outputs/domain-audit-hardening/site-audit.json)
- [Breakpoint and baseline comparison](../../outputs/domain-audit-hardening/hero-layout-review.json)
- [Compliance triage](../../outputs/domain-audit-hardening/compliance-triage.json)
- [Asset inventory](../../outputs/domain-audit-hardening/asset-inventory.json)

The parity and candidate browser results use an isolated local preview, **not a deployed candidate**. Live production still needs the approved release to receive these fixes. Runtime inventory covers declared references, not a guarantee that every possible user interaction has been exhaustively simulated.

## Next steps

1. Publish this approved maintenance candidate through its own PR, leaving the separate V12 design candidate untouched.
2. Commit only scoped source/generated files and `_review` notes; leave local `outputs` evidence out of the public site. Revalidate the exact PR head and required checks.
3. Use the normal merge-commit and Pages workflow under the user's explicit release approval. Verify all 69 live pages and assets, HTTPS/custom-domain metadata, legacy redirects, Library motion behavior and tablet geometry against the exact deployed commit. Record the final deployment evidence on the PR.
4. Continue the Xtend+ human review separately without treating this technical release as claim clearance.

Rollback reference remains the unchanged production baseline above. No production rollback or fix-forward has been performed or required by this local candidate work.
