# Research-led experience — candidate QA

Review candidate only. **Not merged, not deployed.** Production baseline: `e0a668a10ddd6cafdf3f27ee4e6261f7e9caf27e`.

Prepared: 2026-09-06T23:02:24.521103+00:00. Branch: `agent/research-led-experience`.

## Result

| Gate | Result |
|---|---|
| Canonical build | Two consecutive builds produced identical public-file fingerprints |
| Public inventory | 71 pages; 45 active and 8 deferred products; 10 published guides |
| Python suite | **112 / 112 passed** (105 inherited + 7 new regression tests) |
| JavaScript suite | **9 / 9 passed**; dormant measurement remains inert |
| Normal validation / compliance hard gate | PASS; zero RED findings and no hard errors |
| Strict dry-run | Executed successfully; strict mode **would fail** with 76 unresolved advisory occurrences |
| Full responsive sweep | **568 states**: 71 pages × desktop 1440 / tablet 768 / phone 390 / phone 375 × normal / reduced motion |
| Responsive failures | Zero overflow, missing images, bad page status, duplicate IDs, unnamed controls, console errors/warnings, non-navigation-abort failed requests, or tested functional failures |
| Extended usability | **40 route/viewport cases passed**: skip links, focus indication, 200% root-text sizing, heading clipping and solid-background contrast checks |
| Deeper discovery interactions | **8 suites passed** across four sizes and both motion preferences |
| JavaScript-disabled fallback | Five representative routes passed; all three homepage paths remain available |
| Local HTTP inventory | **71 pages + 168 referenced assets** returned 200 and matched canonical production-style bytes |
| Public safety scan | 71 public pages / 114 files, zero findings |
| Review presentation | 13 actual browser screenshots, 1,472,973 bytes total; gallery search and comparison toggle checked |
| Protected source data | Product catalog, labels, Library, site metadata, Core Four, growth settings, compliance registries and inherited triage records unchanged |

These are local candidate checks in installed Chrome, not a production deployment or a WCAG certification. Viewport emulation is not a physical-device test. Safari, Firefox, assistive-technology user testing and field performance were not measured in this pass.

## Exact artifact identity

Canonical public-file digest: `04870e4119b3ec3c2e5b2bbecbf3af471398954d986d32a853d7afba9e4d8e12`.

[public-file-fingerprints.json](public-file-fingerprints.json) contains each page/asset hash. Text uses the existing audit's GitHub/Linux LF normalization; binary files are unchanged. The PR's final head identifies the candidate commit; this digest binds the tested public output without putting a self-referential commit SHA inside a commit.

## What the interaction checks actually did

- Opened and closed optional kit pricing; verified that the concise affiliate disclosure is outside that collapsed content.
- Combined manufacturer and magnesium searches, confirming both the standalone product and the canonical Core Four bundle.
- Exercised the no-result state, reset, alphabetical sorting, next-product control and arrow-key intent navigation.
- Submitted the header search and switched product/learning result modes.
- Applied the catalog manufacturer filter, checked URL state, opened the product inspector, pressed Escape, and verified focus returned to a product trigger.
- The full sweep separately exercised Library query/category/Core Four/reset behavior, catalog sorting/load-more/inspector, About FAQ keyboard toggle, privacy off states, purchase-option disclosures and the new three-path navigator.

The catalog's inherited `scrollIntoView` call was moving the document on initial load and changing the sequential keyboard entry point. It now scrolls only the horizontal intent rail. The final sweep checks initial scroll position, skip-link order and focus transfer into the main content.

## Accessibility scope

The targeted scan examined 3952 text candidates. It found zero failing contrast ratios among the cases it could resolve against solid backgrounds. 100 cases involved gradients, images, opacity or another unsupported background and require human interpretation; representative page images were visually inspected. Do **not** present this as an automated WCAG pass.

All 40 cases passed 200% root-text sizing without document overflow or horizontally clipped main headings. Keyboard skip links and visible focus were tested. Reduced motion does not disable search, filters or the new navigator. The no-JavaScript checks verify useful static routes rather than claiming that every enhanced filter works without JavaScript.

## Compliance reconciliation: 70/77 → 69/76

[compliance-reconciliation.json](compliance-reconciliation.json) compares the baseline and candidate using fresh execution. Exactly one rendered occurrence disappeared: the repeated Balance Test Basic Kit description in the former duplicate homepage testing promotion.

- No new warning occurrence appeared after ignoring moved HTML line numbers.
- The canonical description and every unique inherited human-review text remain unchanged.
- All seven inherited P1 findings remain `HUMAN_REVIEW_REQUIRED` advisory priorities.
- Claims, classifications, qualifications, sources and disclosures were not weakened or suppressed.
- Xtend+ “multi-immune” remains unchanged and remains the first future editorial-review priority.
- K2, zinc/copper and magnesium editorial work remains unpublished.

The lower count is **not** seven resolved findings, a claim clearance, or a clean strict-compliance pass.

## Performance tradeoff, measured honestly

The homepage HTML shrank from 204,049 to 184,130 LF bytes (19,919 bytes, approximately 9.8%). The new local navigation script is 964 bytes. The new visual stylesheet is 37,400 bytes; no framework, video, third-party script, new font download or tracking service was introduced.

The fresh loopback first-viewport sample was **976,230 decoded document/resource bytes** at desktop versus **958,061** for the baseline: approximately **18.2 KB / 1.9% more**, with one additional total resource request. The corresponding phone samples were 947,816 versus 929,647 bytes. This records the cost of the shared visual layer rather than claiming an unmeasured speed improvement.

See [local-payload-comparison.json](local-payload-comparison.json). These are uncompressed decoded resources on loopback at fixed viewport heights, not production transfer size, real-user Core Web Vitals, mobile-network timing or revenue evidence. The larger artwork uses existing official image files; no product-image payload was replaced.

## Windows line endings and the parity check

The first direct Windows-server run, retained as [local-parity.json](local-parity.json), reported 17 text-asset byte mismatches even though all 71 pages and all 168 asset URLs returned 200. Direct comparison confirmed that the raw local server served the exact CRLF worktree files, while the permanent audit intentionally expects LF bytes from GitHub's Linux checkout.

No audit assertion was weakened and no website content was changed to hide this. [export_preview.py](export_preview.py) exported the same canonical pages/assets using the audit's existing `build_bytes` normalization. Against that production-style local server, the unchanged audit passed all 71 pages and 168 assets: [production-style-parity.json](production-style-parity.json).

## Evidence and reproducibility

- [validation-results.json](validation-results.json): command outcomes and logs.
- [browser-audit.json](browser-audit.json): all 568 page states.
- [review-qa.json](review-qa.json): extended usability and no-JavaScript evidence.
- [interaction-qa.json](interaction-qa.json): deeper discovery checks.
- [RESEARCH_REPORT.md](RESEARCH_REPORT.md): 100-site findings and explicit methodology limits.
- [index.html](index.html): local before/after gallery and searchable research notes.
- [screenshots/](screenshots/): committed actual browser captures. Larger full-page PNGs remain ignored in `_preview/research-led-experience/review/`.

Standard checks remain `python scripts/build.py`, `python scripts/validate.py`, `python scripts/validate.py --compliance-strict --compliance-dry-run`, `python -m unittest discover -s tests -v`, `node --test tests/measurement.test.cjs`, and `python scripts/scan_v10_public_safety.py`.

Local review scripts use the existing Playwright 1.55.0 testing dependency and installed Chrome. Start a loopback server at port 8772 for the worktree; optional before/after capture uses port 8773 for the verified baseline tree. The production-style export uses port 8774. No account browser profile, password, session cookie, analytics dataset or purchase flow is used.

## Review boundary and remaining decision

The candidate is complete for visual review. The remaining decision is the owner's approval of the new direction. No production issue requiring rollback was introduced because production was not changed. Before a later approved release, recheck the exact PR head, required CI, current main and production health; then use the normal protected merge/deploy workflow.

The Sites building guidance influenced this work by keeping the existing static architecture, emphasizing readable hierarchy and purposeful imagery, and requiring an early working local preview. Hosting was intentionally not changed because this is a review-only candidate.
