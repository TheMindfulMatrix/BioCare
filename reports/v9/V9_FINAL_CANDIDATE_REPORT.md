# V9 final candidate report

Approved candidate: `182e39a6beba1c735dfa699fb3a598d793e56b10` on `agent/v9-mobile-catalog`, based on V8 production `2bfabedfeaf86ec13bb479e6daa51d6df857bb46`. Permanent validation run `32444530137` passed this exact SHA before report reconciliation.

## Outcome

V9 replaces the oversized mobile Product Universe opening with a compact, product-first catalog. The locked mobile order is global header/search, horizontal intent rail, compact universe header, catalog search, sticky result/filter/sort toolbar, compact affiliate disclosure, and the two-column product grid. Full disclosures and education remain below the catalog.

The first 12 canonical products render initially, then progress deterministically to 24, 36, and all 45. One generated canonical payload drives counts, intents, search, filters, sort, cards, pricing, labels, sources, education, and the reusable inspector. No parallel mobile catalog exists.

## Measured improvement at 375px

| Metric | V8 | V9 |
|---|---:|---:|
| First product Y | 2,485px | 659px |
| Product 6 Y | 6,997px | 1,436px |
| Product 12 Y | 13,143px | 2,550px |
| Median card height | 931px | 363px |
| Initial DOM nodes | 1,760 | 509 |
| Page height | 49,722px | 8,212px |
| Initial product-image requests | 14 observed | 2 |
| Products HTML | 137,176 B | 136,174 B |

The grid is exactly two columns at 375px and 390px, three at 768px, and four at 1440px. There is no page-level overflow. Maximum sticky UI is 167px (107px header + 60px toolbar) at both mobile widths; product anchors include sticky offset and no card starts beneath the controls.

## Discovery and detail

- Intent rail: All plus six canonical intents; counts 45 / 7 / 10 / 3 / 15 / 8 / 2; keyboard arrows, pointer/touch, URL state, and back/forward passed.
- Search: normalized multi-term matching, exact/partial/mixed case/no-result/clear/repeated changes passed; verified label ingredients are indexed only when approved.
- Filters: both manufacturers, all six intents, all nine product kinds, all three label states, combinations, chips, clear-all, and no-result passed.
- Sort: canonical, A-Z, and manufacturer only; no price sort.
- Inspector: all 45 records exercised; subscription, one-time, long name, Zinzino, BioLimitless, complete/partial/unavailable labels, Escape, focus return, URL, history, disclosure, and official source passed.

## Pricing, disclosure, and compliance

Canonical pricing models remain: 35 retail/premier, 7 one-time/autoship, 1 starter subscription, 1 one-time, and 1 one-time range. Comparison semantics are unchanged. A compact affiliate disclosure precedes the first commercial cards; relationship, pricing-date, checkout, New York, BioLimitless, evidence-boundary, and FDA disclosures remain in the inspector and full lower section as applicable.

Hard compliance gate passed. Eight compliance fixtures passed. Advisory inventory is 70 review warnings / 77 strict dry-run items, fully emitted by the validator and not suppressed. The reduction from V8's 91 / 98 results from removing repeated full-detail public card copy, not weakening the rules.

## Validation

- deterministic build: identical diff hash `30b472a2b1f78f156a203b1b4d5e3040737ef527`
- `python scripts/validate.py`: pass; 22 public pages, 10 articles, 45 active, 8 deferred, `/BioCare/` safe
- strict dry run: pass as an inventory operation; 77 unresolved strict items reported
- unit tests: 26/26 pass, including 11 V9-specific tests and 8 compliance fixtures
- JavaScript syntax: pass
- `git diff --check`: pass
- secret-pattern scan: no matches

## Evidence

Screenshots are under `outputs/v9/before` and `outputs/v9/after`. Machine-readable QA, accessibility, performance, discovery, disclosure, and DoD records are adjacent to this report.

No merge or deployment is authorized. The draft PR must remain unmerged until explicit user approval.
