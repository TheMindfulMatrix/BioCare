# The Mindful Matrix — Compliance Engine v1 Legal Review Package

Prepared for Missouri counsel

Ruleset and current-site audit date: `2026-08-18`

> This system is a risk-control and workflow tool. It is not legal advice, regulatory approval, or a guarantee of compliance. No attorney review is represented in the current registry.

## 1. Business model summary

The Mindful Matrix is a US-focused educational wellness website with evidence-oriented Library content, a product-comparison/Shop layer, affiliate or partner-coded external links, and planned social-media content. The site does not complete checkout. Visitors leave the site for manufacturer/vendor destinations. V1 records Missouri as the business context but applies federal FTC/FDA controls; Missouri-specific questions are reserved for counsel.

## 2. Zinzino relationship

The public source model describes Gavin/The Mindful Matrix as an independent Zinzino Partner who may earn commission on purchases made through Zinzino links. The v1 catalog contains 36 active Zinzino products. The engine preserves this exact disclosure:

> Links below go to Zinzino's own site. I'm an independent Zinzino Partner and earn a commission on purchases made through them.

MLM customer/product marketing and recruitment are separate review contexts. The current audit found no active MLM earnings or lifestyle claim. Future recruitment content defaults to human review, and unsubstantiated earnings/lifestyle claims are blocked.

## 3. BioLimitless relationship

The public source model uses a Matrix partner referral and states that compensation may be earned on qualifying purchases. The v1 catalog has nine active and eight deferred BioLimitless products. The engine preserves this exact disclosure:

> BioLimitless links use the Matrix partner referral. I may earn compensation from qualifying purchases.

The eight deferred products cannot receive a public CTA, price CTA, Product Universe placement, Shop rendering, or promotional social generation without a documented status change.

## 4. Website and content model

The site is a generated static GitHub Pages project. Product, Library, site, and disclosure content are maintained in JSON source files; templates generate the homepage, Shop, Library, Start Here, and all ten published Library articles. Compliance metadata stays internal at build time and is not added to the public payload.

The audit covers 22 source, template, and generated-public files, including all required pages/articles, product copy, prices, CTAs, disclosures, founder/about copy, testing language, and Matrix copy.

## 5. Social-media model

Planned channels are Instagram, Facebook, Threads, Reels, and future short-form video. A commercial brief must identify approved claim IDs and pass claim, evidence, affiliate, disclosure-placement, testimonial, price, disease, and MLM-earnings checks. The production gate forbids strengthening, paraphrasing, or extending approved claims. Compliance review does not authorize publication.

## 6. Claim categories

The registry distinguishes product facts, prices, ingredients, nutrient content, structure/function, general wellbeing, authorized/qualified health claims, disease, diagnosis, safety, efficacy, comparisons, superiority, scientific evidence, research interpretation, endorsements/testimonials, before/after, professional authority, affiliate relationships, urgency/savings, and MLM earnings/lifestyle/recruitment. Commercial, editorial, social, recruitment, and mixed-public contexts are evaluated separately.

## 7. GREEN / YELLOW / RED rules

- `GREEN`: verified, lower-risk wording in its stated context; any recorded disclosure and exact-text controls still apply.
- `YELLOW`: evidence, qualification, disclosure, or human review is unresolved or context-dependent.
- `RED`: blocked for the specified context.
- `DEFERRED_COMPLIANCE_REVIEW`: intentionally withheld, not approved.

Machine review uses `PASS`, `PASS_WITH_QUALIFICATION`, `HUMAN REVIEW REQUIRED`, `BLOCKED`, and `DEFERRED_COMPLIANCE_REVIEW`. The machine is explicitly not treated as legal certification.

## 8. Disease claim policy

Commercial supplement/wellness wording that diagnoses, treats, cures, prevents, mitigates, or reverses disease is blocked without a specifically documented lawful basis and human/legal review. The engine also checks implied product/outcome combinations and treatment/professional-care replacement. A DSHEA disclaimer is not treated as a cure for an impermissible disease claim.

## 9. Structure/function policy

Structure/function wording is YELLOW unless the precise wording, evidence, context, product/formulation scope, qualification, and required disclaimer treatment are recorded. The registry carries `requires_dshea_disclaimer`, `requires_claim_adjacent_disclaimer`, exact wording, and placement rules. It does not presume that a footer alone satisfies claim-adjacent or same-panel requirements.

## 10. Affiliate disclosure policy

The engine requires clear and conspicuous material-connection disclosure near the recommendation/link as appropriate. It preserves the current Zinzino and BioLimitless wording exactly and validates it against the site source. Future partner configurations must carry their own relationship, compensation, disclosure, placement, identifier, and jurisdiction fields and cannot weaken RED controls.

## 11. Testimonial policy

Testimonials and endorsements cannot communicate claims that the business could not otherwise substantiate. Personal-results, before/after, professional-authority, influencer, and imported manufacturer-testimonial content defaults to review. Fabricated testimonials are prohibited; credentials must be independently verified and cannot imply efficacy or regulatory approval without support.

## 12. MLM earnings policy

Income, income replacement, passive income, debt payoff, wealth, luxury lifestyle, vacation/car/mansion imagery, and earnings screenshots are blocked unless reliable evidence shows what typical participants are likely to achieve after typical expenses and counsel approves the use. “Results not typical” is not treated as a cure. The FTC earnings-claim rulemaking is recorded as a proposal, not a final rule, as of the review date.

## 13. High-risk product policy

Products may be `ACTIVE`, `ACTIVE_WITH_RESTRICTIONS`, `DEFERRED_COMPLIANCE_REVIEW`, or `BLOCKED_PUBLIC`. Deferred/blocked controls are enforced independently across CTAs, prices, Shop, Product Universe, and social production. Peptide/research-compound and other flagged products require a separate documented legal/evidence review before status change; the engine does not infer approval from a manufacturer page.

## 14. Current unresolved findings

The machine audit extracted 2,111 claim-bearing records: 1,886 GREEN, 225 YELLOW, and zero RED. It identified zero `LAUNCH_BLOCKER_COMPLIANCE` findings, 151 `HIGH_PRIORITY_REVIEW` findings, 74 `YELLOW_REVIEW` findings, and six ambiguous/implied combinations.

The high-priority group consists primarily of 107 efficacy-like statements, eight structure/function statements, nine scientific-evidence statements, six implied combinations, and 21 product/testing or deferred facts that require registration, status control, or human confirmation. The YELLOW review group includes 70 editorial research interpretations, two relationship/disclosure placement items, and two general-wellbeing statements. Many duplicate occurrences arise because the same source text is deliberately audited in both content JSON and generated pages.

The current build retains 45 active products and eight deferred BioLimitless products. All deferred publication/promotional controls are false. The full text, exact locations, matched rules, reasons, evidence status, and next actions appear in `reports/compliance-audit-v1.md` and `reports/compliance-audit-v1.json`. The audit made no marketing/editorial rewrites.

Priority counsel decisions:

1. Determine which current product/testing/structure-function statements need claim-adjacent disclaimer treatment and product-specific substantiation.
2. Confirm whether the current site-level and link-adjacent affiliate placement is sufficient on each public surface.
3. Establish approval criteria and vendor-record requirements for the eight deferred BioLimitless products.
4. Review whether any unregistered efficacy-like catalog or Matrix wording should be registered, qualified, relocated to editorial context, or removed in a later separately authorized change.

## 15. Questions for counsel

1. Are the current commercial claim categories and GREEN/YELLOW/RED decision boundaries sufficient for this business model?
2. Are any Missouri-specific consumer-protection registrations, notices, or disclosures required?
3. How should claim-adjacent DSHEA disclaimers be implemented on this affiliate site, including cards, modals, linked Shop controls, and social/video?
4. Do the Zinzino, BioLimitless, or other partner/vendor agreements impose stricter copy, disclosure, testimonial, social, or recordkeeping rules?
5. What liability, media, cyber, product, or other insurance should the LLC consider?
6. How should future partner-configured sites allocate disclosure placement, substantiation, content approval, recordkeeping, and responsibility?
7. What legal/evidence review process should apply to peptide, research-compound, or similarly high-risk products?
8. What records and source snapshots should be retained to document substantiation before publication, and for how long?
9. Does the current distinction between educational Library content and mixed/commercial surfaces sufficiently avoid misleading net impressions?
10. What review and retention standard should apply before any future MLM recruitment or earnings communication?
11. Should a qualified professional review test/biomarker copy that could influence medical decisions, and what exact limitation language should be used?
12. Which authorized or qualified health claims, if any, may be relevant, and what exact FDA-reviewed language must be preserved?

## Materials for review

- `content/compliance/authoritative-sources.json`
- `content/compliance/rules.json`
- `content/compliance/claims.json`
- `content/compliance/evidence.json`
- `content/compliance/products.json`
- `content/compliance/disclosures.json`
- `content/compliance/social-policy.json`
- `reports/compliance-audit-v1.md`
- `reports/compliance-audit-v1.json`

The source index contains only official FTC/FDA materials for the federal policy layer and records each page's review date/status. Manufacturer sources are separately labeled and are not treated as regulatory authority or independent product substantiation.
