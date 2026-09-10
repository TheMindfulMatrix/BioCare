# Editorial followthrough — September 10, 2026

NON-PUBLIC. The requested editorial sequence is complete at the research/draft stage. Human clinical and company/compliance review remain open; nothing in this packet is publication approval.

| Order | Deliverable | Completed work | Still needed |
| --- | --- | --- | --- |
| 1 | [Xtend+ substantiation review](XTEND_SUBSTANTIATION_REVIEW.md) | Exact registered phrase, component-by-component evidence analysis, adjacent manufacturer-claim screen, updated primary ingredient studies, label discrepancy retained, concrete identity-only proposal. | Current controlling US label and finished-product substantiation; responsible human judgment. `YELLOW / HUMAN_REVIEW_REQUIRED` remains intact. |
| 2 | [K2 editorial review](K2_EDITORIAL_REVIEW.md) and [refined manuscript](VITAMIN_K2_DRAFT_REFINED.md) | Original plus September 6 addendum reviewed; 2026 coronary result integrated; positive and contrasting bone studies included; anticoagulant boundaries preserved. | Full papers/supplements, formal evidence synthesis and clinical/company review before publication. |
| 3 | [Zinc/copper draft](ZINC_COPPER_DRAFT.md) | Sourced reader manuscript, intake/upper-limit context, concrete ratio arithmetic, dose/duration evidence and medication boundaries. | Clinical review, full source/bias assessment, and separately verified product facts if any commercial connection is later proposed. |
| 4 | [Magnesium draft](MAGNESIUM_DRAFT.md) | Sourced reader manuscript, elemental/form distinction, food versus supplemental upper-limit scope, 2025 bisglycinate sleep evidence and mixed cramp studies including 2026. | Renal/medication review, full source/bias assessment, and separately verified product facts if any commercial connection is later proposed. |

## Verification of the editorial changes

- Every added manuscript is marked nonpublic and states its outstanding human/publication gates.
- All six internal Markdown links present in the five substantive files were resolved against the filesystem and exist. This index adds links to those same existing files.
- The claim/evidence registries, product-label registry, original September 6 manuscript and September 6 K2 addendum have no Git diff from this worktree's base at the time of this check.
- Editorial writes were confined to this directory. Other concurrent audit-code changes belong to their assigned worker. No public copy, canonical article, product association, search record, sitemap or deployment was edited by this editorial work.
- Source checks distinguish direct page access, indexed primary abstracts/publisher sections, blocked full-text routes and historical PDF findings. No inaccessible paper is represented as fully reviewed. Dates in each source ledger describe actual publication/update versus retrieval dates.
- No messages, accounts, purchases, PRs, merging, publishing, medical approval or company approval were performed by this editorial work.

## Repository evidence for the next reviewer

`content/catalog.json:1324` is the canonical Xtend+ description. `content/compliance/claims.json:9120` begins its claim record; lines 9140–9165 contain the qualification, disclosures, risk/state/review status, dates and disclaimer controls. `content/compliance/evidence.json:3153` begins its manufacturer-only evidence record; the empty population/comparator/outcomes and explicit limitation are at lines 3163–3167.

`scripts/build.py:1226` feeds the product description into search records; `scripts/build.py:1724` uses it for the product document head and structured data, and `scripts/build.py:1727` uses it for visible product copy. A later approved wording change therefore needs regeneration and review across placements.

Pending BioLimitless label records begin at `content/product-labels.json:1112` (magnesium), `:1130` (zinc/copper) and `:1148` (D3/K2). Each has empty ingredients, a missing checked date, pending approval and `public: false`. No form, dose or equivalence claim was invented to fill those gaps.
