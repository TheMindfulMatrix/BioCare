# The Mindful Matrix Compliance Engine v1

Version: `1.0.0`

Primary jurisdiction: United States; Missouri business context

Last federal policy review: `2026-08-18`

> This system is a risk-control and workflow tool. It is not legal advice, regulatory approval, or a guarantee of compliance.

## What the engine does

Compliance Engine v1 puts the site's health, product, testing, evidence, price, affiliate, testimonial, and MLM-related statements into one auditable workflow. It:

- keeps exact controlled wording in a central claim registry;
- links claims to evidence without treating an ingredient study as proof for a finished product;
- separates commercial, editorial, social, mixed-public, and MLM-recruitment contexts;
- applies machine-readable FTC/FDA-based rules to source content, templates, generated pages, and future social drafts;
- validates current prices, disclosures, product status, evidence references, and review dates;
- blocks hard-rule failures and reports ambiguous or review-dependent language without silently rewriting it;
- prevents deferred products from receiving public CTAs, prices, Shop/Product Universe placement, or promotional social generation; and
- produces a complete machine-readable and human-readable audit trail.

The engine does not interpret every possible net impression, replace counsel, establish that a claim is lawful, certify a manufacturer statement, or turn a disclaimer into permission to make a disease claim. A machine `PASS` means the configured rules found no blocking condition for the registered wording and context. It is not a legal conclusion.

## Architecture

| File | Purpose |
| --- | --- |
| `content/compliance/version.json` | Engine/ruleset versions, jurisdiction, policy-review dates, and recheck intervals. |
| `content/compliance/authoritative-sources.json` | Official FTC/FDA policy sources, URLs, topics, review date, and rulemaking status. |
| `content/compliance/rules.json` | Human-auditable rules, contexts, patterns, risk, actions, and source IDs. |
| `content/compliance/claims.json` | Exact claims, context, evidence, qualifications, disclosures, state, and review history. |
| `content/compliance/evidence.json` | Regulatory, Library, and manufacturer-source evidence with limitations and scope. |
| `content/compliance/products.json` | Product publication permissions and compliance status. |
| `content/compliance/disclosures.json` | Exact preserved affiliate/material-connection and FDA disclaimer wording. |
| `content/compliance/social-policy.json` | Required checks for Instagram, Facebook, Threads, Reels, and short-form video. |
| `content/compliance/codex-production-gate.txt` | Reusable gate for future Codex production briefs. |
| `scripts/compliance_engine.py` | Deterministic extraction, exact-match lookup, rule evaluation, implied-claim heuristics, and audit generation. |
| `scripts/validate_compliance.py` | Registry, product, disclosure, price, evidence, status, review, and hard/strict gate validator. |
| `scripts/check_claims.py` | Preflight helper for inline text, a draft file, or the catalog. |
| `scripts/bootstrap_compliance.py` | Reproducible v1 baseline generator for the current source model; it does not publish public pages. |
| `reports/compliance-audit-v1.json` | Full machine-readable current-site audit. |
| `reports/compliance-audit-v1.md` | Grouped human-readable non-PASS findings and summary. |

Compliance files remain build-time/internal. The public site generator does not ship the registries or internal review notes.

## States and publication decisions

- `GREEN`: factually verified and low-risk for the specific registered context. It may still require its listed disclosure or exact wording.
- `YELLOW`: evidence, qualification, disclosure, context control, or human review is required. It is not automatically approved.
- `RED`: blocked in the specified context. It must not be approved for commercial rendering.
- `DEFERRED_COMPLIANCE_REVIEW`: intentionally withheld until a documented status change.

Review results use `PASS`, `PASS_WITH_QUALIFICATION`, `HUMAN_REVIEW_REQUIRED`, `BLOCKED`, and `DEFERRED_COMPLIANCE_REVIEW`. Strict mode treats unresolved commercial YELLOW claims as failures.

The audit report maps those states to:

- `LAUNCH_BLOCKER_COMPLIANCE`
- `HIGH_PRIORITY_REVIEW`
- `YELLOW_REVIEW`
- `LOW_RISK`
- `PASS`

## Claim types and context

The registry supports factual product and price facts; ingredient, nutrient-content, structure/function, general-wellbeing, authorized and qualified health claims; disease, diagnostic, safety, efficacy, comparative, superiority, price-savings, and scarcity claims; testimonials, before/after, endorsements, professional-authority, scientific-evidence, and research-interpretation claims; affiliate relationships; and MLM earnings, lifestyle, and recruitment claims.

Every claim is evaluated in one context: `COMMERCIAL_PRODUCT`, `EDITORIAL`, `SOCIAL_COMMERCIAL`, `MLM_RECRUITMENT`, or `MIXED_PUBLIC`. A statement permitted in an evidence-limited editorial discussion is not automatically permitted in product copy or a Reel.

## Evidence rules

Each evidence record identifies its type, scope, relevance, limitations, manufacturer relationship, and exact claim links. Evidence quality states are `ESTABLISHED`, `SUPPORTED`, `DEBATED`, `INSUFFICIENT`, and `MANUFACTURER_ONLY`.

The hierarchy distinguishes regulatory primary material, systematic reviews/meta-analyses, randomized controlled trials, prospective observational evidence, cross-sectional evidence, mechanistic/preclinical evidence, case reports, expert opinion, manufacturer sources, and other clearly labeled material. Study design alone is not proof. Population, formulation, dose, outcome, consistency, relevance, and limitations must match the wording.

`INGREDIENT_ONLY` evidence never automatically authorizes a finished-product outcome. Other scopes are `FORMULATION_SPECIFIC`, `PRODUCT_SPECIFIC`, `GENERAL_NUTRITION`, `OBSERVATIONAL_ONLY`, `MECHANISTIC_ONLY`, and `OTHER`.

Authorized and qualified health claims have explicit registry sections. They are empty in the v1 baseline because no such wording was independently authorized for current use. Any future entry must preserve the authoritative wording, required qualification, source URL, and last-verification date; wording must not be strengthened by paraphrase.

## Disease, structure/function, safety, and test controls

Commercial language that diagnoses, treats, cures, prevents, mitigates, or reverses disease is blocked unless a specific lawful basis is documented and human-reviewed. The FDA disclaimer does not cure an otherwise impermissible disease claim.

Structure/function wording requires substantiation, truthful net impression, the proper evidence/formulation match, and the applicable exact DSHEA disclaimer. The registry tracks whether the disclaimer is required and whether it must be claim-adjacent. A global footer is not assumed sufficient.

Absolute safety, guaranteed outcomes, universal applicability, treatment replacement, and professional-diagnosis replacement are blocked. Other safety, medication, pregnancy, testing, biomarker, and professional-interpretation statements require human review when their use could affect care.

The medical-advice firewall flags individualized diagnosis, treatment plans, medication changes, prescription guidance, or instructions to replace professional care.

## Prices, disclosures, endorsements, and testimonials

An active price requires a verified amount, currency, price type, official manufacturer source, and verification date. Unsupported savings, comparisons, scarcity, and urgency are blocked or escalated. The engine does not change a catalog price.

The Zinzino and BioLimitless disclosures are preserved byte-for-byte in `disclosures.json` and cross-checked against the public source model. A material-connection disclosure must be clear, understandable, conspicuous, and close to the recommendation or link; the phrase “affiliate link” alone is not treated as sufficient.

Testimonials, personal results, before/after content, and professional authority cannot make a claim the business could not substantiate directly. Before/after content and future recruitment copy default to human review. Fabricated testimonials and unverified credentials are prohibited.

## MLM firewall

MLM recruitment is a separate context. Earnings and lifestyle claims—including explicit income, income replacement, passive income, typical part-time income, luxury imagery, or income screenshots—are blocked unless reliable substantiation reflects what typical participants are likely to achieve after typical expenses and the claim receives human/legal review. A “results not typical” disclaimer does not fix a misleading net impression.

The official FTC MLM earnings-rule page is stored as `PROPOSED_RULE_NOT_FINAL_AS_REVIEWED`; v1 does not treat the proposal as a final rule. Every future recruiting item receives `HUMAN REVIEW REQUIRED` unless a separately reviewed recruitment policy is adopted.

## Product statuses

- `ACTIVE`: product may appear publicly, but every claim, price, CTA, and disclosure remains independently controlled.
- `ACTIVE_WITH_RESTRICTIONS`: only the recorded permissions and claim contexts are allowed.
- `DEFERRED_COMPLIANCE_REVIEW`: no public CTA, price CTA, Product Universe placement, Shop rendering, or promotional social generation.
- `BLOCKED_PUBLIC`: no public promotion or rendering.

To change a deferred product, obtain the required human/legal review, document the reason and supporting evidence, update its catalog status and `products.json` permissions together, register every intended public claim, add disclosure requirements, update `reviewed_at`/`reviewed_by`, then run normal and strict validation. Never change status merely to make a validator pass.

## Adding or changing a claim

1. Write the exact proposed wording and intended context. Do not start from a broad marketing paraphrase.
2. Run `scripts/check_claims.py` to identify likely rules and risk.
3. Add or verify evidence records first. Record null when metadata is unknown; never infer authors, DOI, PMID, population, outcomes, or study design.
4. Add a unique claim record to `claims.json` with the complete schema, exact evidence IDs, scope, qualifications, disclosures, allowed/prohibited contexts, state, reason, recheck date, and transparent reviewer identity.
5. For a human-reviewed decision, record the actual reviewer role/name only with authorization. Do not imply attorney review.
6. If the current baseline generator owns that record, update `bootstrap_compliance.py` so regeneration remains deterministic.
7. Run the fixture suite, normal validator, and strict dry run. Inspect the audit rather than allowing the tool to rewrite public copy.

Changing a sentence requires a new exact-text review. GREEN approval does not authorize strengthened, shortened, or context-shifted wording.

## Adding evidence

Add the evidence to `evidence.json` with its exact source URL and known metadata. State the limitations, manufacturer relationship, commercial relevance, what it supports, and what it does not support. Link it from only those claims whose wording, product/formulation, population, dose, context, and outcomes actually match. Re-run validation so stale or unknown references fail before publication.

## Social and Codex production workflow

Every commercial website or social brief must run claim classification, evidence, material-connection disclosure, testimonial, price, disease, and MLM earnings checks. The brief must cite approved claim IDs and an eligible product status before production begins.

The required instruction is: **“Do not strengthen, paraphrase, or extend approved claims.”**

Copy the complete block from `content/compliance/codex-production-gate.txt` into future master prompts. If one statement conflicts with the registry, stop that statement and report the conflict without blocking unrelated production. Do not publish directly from the compliance tool.

## Partner and jurisdiction inheritance

The model separates brand rules, manufacturer evidence, partner-specific disclosure, partner ID, and jurisdiction. A future partner configuration may add stricter rules and its own disclosure, destination, and identifier. It must not override RED rules or activate a deferred product. V1 is configured for `US` / `MO`; federal controls apply, while Missouri-specific questions remain `STATE_LEGAL_REVIEW_REQUIRED` until counsel supplies authoritative requirements.

## Commands

```text
python scripts/check_claims.py --text "Supports immune function." --context SOCIAL_COMMERCIAL
python scripts/check_claims.py --file draft-caption.txt --context SOCIAL_COMMERCIAL
python scripts/check_claims.py --catalog
python scripts/validate_compliance.py
python scripts/validate.py
python scripts/validate.py --compliance-strict
python scripts/validate.py --compliance-strict --compliance-dry-run
python -m unittest discover -s tests -v
```

Normal validation blocks hard failures and reports review items as warnings. Strict mode also fails unresolved YELLOW commercial claims, unregistered commercial health claims, missing evidence, and expired required reviews. Dry-run mode reports what strict mode would block without changing content or failing the command.

## Escalation and periodic review

1. Do not publish RED, BLOCKED, or DEFERRED items.
2. Route YELLOW, implied claims, testimonials, before/after, professional authority, safety, structure/function, MLM recruitment, and evidence mismatches to the appropriate human reviewer.
3. Route legal interpretation, Missouri requirements, partner agreements, claim-adjacent disclaimer implementation, and high-risk research-product decisions to counsel.
4. Preserve the reviewed wording, source snapshot, decision, reviewer, date, context, and recheck date.
5. Re-run both validators and inspect the generated audit before release.

FTC/FDA guidance and rulemaking should be reviewed at least every 90 days under the v1 configuration. Claims and product/manufacturer agreements should be rechecked on their recorded schedule; prices are configured for a 180-day recheck and claim records for a 365-day recheck. High-risk products require separate approval. State law and insurance questions require counsel.
