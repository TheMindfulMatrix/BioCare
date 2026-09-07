# V9 Released and Verified

V9 is released, deployed, and independently verified at `https://themindfulmatrix.github.io/BioCare/`.

## Release identity

- V8 production baseline: `2bfabedfeaf86ec13bb479e6daa51d6df857bb46`
- Approved V9 functional/design candidate: `182e39a6beba1c735dfa699fb3a598d793e56b10`
- Final PR head after report reconciliation only: `2e8503bcf4b69545ab29822dda48a18120ce26e5`
- Candidate validation: run `32444530137`, success on the approved functional/design candidate
- Final PR-head validation: run `32448078439`, success on the exact final PR head
- V9 PR: [#11](https://github.com/TheMindfulMatrix/BioCare/pull/11), merged normally with a merge commit at `2026-08-21T04:52:56Z`
- Verified public-output merge SHA: `f205890e5e5635d87d6ff77da97eedc96d365041`
- Final main validation: run `32448506939`, success on the exact public-output merge SHA
- GitHub Pages deployment: run `32448506546`, deployment `6015686873`, success on the exact public-output merge SHA at `2026-08-21T04:53:48Z`
- Independent production verification completed at `2026-08-21T04:59:41Z`

The release-record publication branch contains only this Markdown file and its JSON counterpart. Its later report-only merge changes no generated page, asset, product data, template, style, script, test, or other public output; `f205890e…` remains the authoritative verified V9 public-output tree.

## Release decision

- Definition of Done: **96 MET / 0 NOT MET / 0 DEFERRED**
- Public pages: **22**, all successful and byte-for-byte identical to the released repository tree
- Products: **45 active / 8 deferred**
- Manufacturers: **2**
- Canonical intents: **6**, plus All
- Active product-image payload: **1,103,598 bytes**, unchanged
- Complete test suite: **26/26 passed**, including 11 V9-specific tests and 8 compliance fixtures
- Compliance hard gate: **passed**
- Advisory inventory: **70 review warnings / 77 strict dry-run items**, fully emitted and not suppressed

## Product-first result

The locked mobile order is the global header/search, horizontal intent rail, compact Product Universe header, catalog search, result/filter/sort toolbar, compact affiliate disclosure, and two-column product grid. Full relationship, pricing, checkout, evidence, New York, BioLimitless, and FDA disclosures remain after the catalog and in the inspector where applicable.

The intent rail preserves All plus Testing, Omega, Gut, Daily, Active, and Skin with canonical totals `45 / 7 / 10 / 3 / 15 / 8 / 2`. Search passed normalization, exact, partial, mixed-case, multi-term, clear, repeated-change, no-result, URL, reload, and history behavior. Filters passed both manufacturers, all six intents, all nine product kinds, all three label states, combined selections, removable chips, clear-all, and empty states. Canonical, A–Z, and manufacturer sorting passed; no price sort exists.

The first 12 canonical products render initially and progress deterministically through `12 → 24 → 36 → 45`, with 45 unique records, no duplicate products, and no broken artwork. The reusable native product inspector passed all 45 records in candidate QA and preserved title, SKU, pricing model, image, label state, official source, product-specific accessible name, sponsored relation, proximate disclosure, Escape close, URL/history, and focus return without stale data.

## Measured mobile improvement

| Metric | V8 | V9 |
|---|---:|---:|
| First product Y | 2,485px | 659px |
| Product 6 Y | 6,997px | 1,436px |
| Product 12 Y | 13,143px | 2,550px |
| Median card height | 931px | 363px |
| Initial DOM nodes | 1,760 | 509 |
| Page height | 49,722px | 8,212px |
| Initial product-image requests observed | 14 | 2 |
| Products HTML | 137,176 B | 136,174 B |

The live grid is exactly two columns at 375px and 390px, three at 768px, and four at 1440px. Live production showed zero horizontal overflow, broken product images, duplicate IDs, undersized visible text, actionable targets below 44×44, console errors, or console warnings.

## Production evidence

- All 22 sitemap pages returned successfully and matched the `f205890e…` repository blobs byte-for-byte.
- Live Products QA passed at desktop `1440×1000`, tablet `768×900`, mobile `390×844`, and mobile `375×812`.
- At 375px, live geometry reproduced 12 initial cards, first product Y `659px`, product 6 Y `1,436px`, product 12 Y `2,550px`, median card height `363px`, page height `8,212px`, and initial DOM size `509` elements.
- Live search `omega food` returned 5 results and normalized the URL; explicit clear restored 45 results and focus.
- Live Omega intent returned 10 products. Combined BioLimitless plus dietary-supplement filters returned 4, with correct removable chips.
- Live sort first items were Balance Test Basic Kit for A–Z, Becoming BioLimitless for manufacturer, and Balance Test Basic Kit for canonical order.
- Live progressive loading reached 24, 36, and 45 unique products with zero broken images.
- The live Balance Test Basic Kit inspector exposed the correct starter/subscription model and official Zinzino source, with `rel="sponsored noopener noreferrer"`, `aria-describedby="inspector-source-disclosure"`, product-specific source naming, initial close-button focus, and focus return.
- Reload preserved the live `balance test` search state and its two results.

## Compliance, disclosures, and links

The compliance hard gate and all 8 compliance fixtures passed. No unsupported diagnostic, disease, treatment, prevention, efficacy, dosage, guarantee, availability, outcome, rating, review, Product, or Offer claim was introduced. Truthful structured data, `/BioCare/` path safety, deterministic generation, JavaScript syntax, diff integrity, and secret-pattern checks passed.

The compact earning disclosure appears before the first product cards. Zinzino Independent Partner identification, commission wording, partner ID `2021428066`, BioLimitless compensation wording, dated pricing source, manufacturer-checkout separation, New York notice, evidence boundary, and applicable FDA language remain present. Official product links carry product-specific accessible names, sponsored/noopener/noreferrer relations, and a proximate disclosure reference.

All 45 unique active-product destinations reached their official manufacturer pages: 36 Zinzino URLs retained partner ID `2021428066`, and 9 BioLimitless URLs retained the Matrix referral. Across the 22 public pages, 98 unique external destinations were audited: 95 returned directly and 3 authoritative destinations were independently verified despite automated-request protection. Customer-facing broken destinations: **0**.

## Rollback and observations

- Historical tag `v5.1` remains unchanged at `b5d35772e98580e253c08f6319aa8e412fa20aea`.
- V8 rollback target remains `2bfabedfeaf86ec13bb479e6daa51d6df857bb46`.
- Repository-safe rollback process: create `agent/v9-rollback` from current `main`; revert merge commit `f205890e…` with mainline parent 1; regenerate and validate; open and merge a normal rollback PR; monitor Pages; and verify the V8 production identity and all public routes. Never reset or rewrite history, move `v5.1`, or patch production directly.
- No rollback was required. No fix-forward remains pending.
- GitHub emitted a non-blocking annotation that a Node 20-targeted action was forced onto Node 24. Validation and Pages deployment both completed successfully.

## Final status

**V9 RELEASED AND VERIFIED.**
