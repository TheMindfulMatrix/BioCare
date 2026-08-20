# V7 baseline reconciliation

## Claimed prior state

The V7 handoff originally described a 789,422-byte active product-image payload, later warning totals, released-final records, and a production tree without temporary V6 execution material.

## Persisted state

The actual `main` tree at `ff41ceecadfbded6e6702c5307754d5903c2f636` is the authoritative V7 baseline. Deterministic measurement found 45 active products, 8 deferred products, 1,405,208 bytes across the 45 active cutouts, 91 compliance review warnings, and 98 strict dry-run items. `reports/v6/V6_RELEASED_FINAL.md` and `.json` were absent. Four one-time V6 workflows plus encoded patch/transfer fragments remained.

## Decision

V7 proceeded from the persisted production tree. No V6 release record was recreated and no conversational metric was elevated above repository evidence.

## Cleanup

V7 removes `.github/workflows/v6-final-closure.yml`, `v6-finish-finalize-v2.yml`, `v6-pr-finalize.yml`, and `v6-release-closure.yml`; each was a one-time finalization runner superseded by `.github/workflows/validate.yml`. It also removes `reports/v6/finish-patch/` and `reports/v6/finish-transfer/`, whose contents were encoded execution-transfer fragments. Historical V6 candidate reports and audit evidence remain.

## Metric resets

- Active image payload: 1,405,208 B baseline → 1,103,598 B final candidate. The four-setting WebP study saved 301,610 B (21.46%) while preserving dimensions, aspect ratios, alpha and provenance. The contact sheet records the five largest savings; approximately 800 KB was not defensible without a more aggressive quality tradeoff.
- Compliance: 91 review warnings → 91; 98 strict dry-run items → 98.
- Catalog: 45 active and 8 deferred products, unchanged.

## Historical integrity

V6 history was not rewritten. `main` remains at `ff41ceecadfbded6e6702c5307754d5903c2f636`; annotated tag `v5.1` still resolves to `b5d35772e98580e253c08f6319aa8e412fa20aea`.
