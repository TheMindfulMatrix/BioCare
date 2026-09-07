# Testing, Library, and learning — review candidate

Status: **DRAFT — not merged, deployed, enrolled, or sold.**

Baseline: `ef36a71ecc3365fa1a03db18083ac75349c54574` (main, PR #32).
Branch: `agent/testing-library-partner-learning`.
Prepared September 6, 2026.

## What is ready to review

- Four distinct US Zinzino testing journeys: BalanceTest, Gut Health Test, Vitamin D, and HbA1c.
- Five standalone test product records, because Gut Health Test x2 is a quantity variant, not a fifth test. The Balance Test Basic Kit stays a separate bundle.
- 24 Library guides: ten existing guides retained, 14 new short educational guides.
- 40 health references from 15 publisher labels, including government agencies, medical organizations, primary studies, and expert consensus.
- All 45 active products have at least one mapped topic reference and department reading. Eight deferred products remain excluded.
- Testing journeys plus image-led Matrix Academy and Partner Practice pages; two working free samples and two clearly separated course outlines.
- Existing approved home design, product records, prices, purchase destinations, label-approval states, and compliance registries preserved.

## What is not ready for sale

Everyday Matrix has eight original lesson manuscripts; Partner Practice has ten. Full lessons include practice worksheets, knowledge checks, answer rationales, and contextual reading. They are stored locally outside this public repository and are not delivered in Pages or preview artifacts. The public candidate contains outlines and two interactive free samples only.

The manuscripts are first editorial drafts, not clinically reviewed, company-approved, pilot-tested, video-produced, or enrolled-student courses. No payment processor, LMS, accounts, certificates, subscription, data-collection form, or price has been added. Paid launch requires approval of course quality, audience/market, seller identity, pricing/currency, taxes, refunds, support, accessibility, delivery, and checkout. No earnings or health-outcome promises are made.

No private back-office documents or training videos were accessed or copied. Public partner-training availability does not establish a license for public redistribution or resale in a paid course. Specific asset/use permission remains a gate before incorporating proprietary material. Original lesson-writing has continued independently.

## Academy visual and interactive revision

The plain-text candidate at `d4dc7dd91fc61c40fd04797271f70524b3cb7d92` was revised in response to the owner's request for visual branding and engagement.

- Sites' design workflow informed the image-first layouts, compact course maps, visual hierarchy and progressive-enhancement approach; existing Python generation and GitHub Pages hosting remain in place.
- The imagegen skill produced exactly two original illustrative course covers. People are fictional, not students, instructors, testimonials or real company events. Both pages disclose this.
- Four responsive WebP exports total **246,560 bytes**; each is under 96 KB. The asset manifest records exact final prompts, generate mode and output paths/dimensions.
- Forest/citron Everyday Matrix and warm-copper Partner Practice use shared Academy CSS and JavaScript, loaded only on these two pages.
- The Everyday free sample teaches cue/action/fallback planning, generates a fixed-choice practice plan, checks understanding and supports retry/reset.
- The Partner sample teaches a permission-based invitation, retains commercial disclosure in all nine draft combinations, checks respect for a refusal, and never sends a message.
- Progress and choices are memory-only and reset on reload. No accounts, tracking, storage, payments or enrollment were introduced.
- Native controls, live feedback, focus handling, reduced-motion-safe initialization and no-JavaScript reading/answer fallbacks are tested as code/markup contracts, not as browser or screen-reader certification.
- Canonical practice copy remains in the two audited course JSON files. The expanded partner content adds **104 net review locations** compared with the previous 225/232 candidate. All remain reviewable; none were suppressed.
- A question containing the word “guarantee” triggered the hard claim detector during development. The question was rewritten as “What should I expect from the course?” while preserving the explicit no-earnings-promise answer. No rule or classification was weakened.

Supporting records: `academy-image-provenance.json`, `academy-redesign.json`, and the updated compliance/parity reports.

Paid-course delivery has NOT been built. Stripe prohibits certain commission- or recruitment-based MLM services; a separately sold course needs an honest provider eligibility review. A course platform that relies on Stripe is not automatically a workaround. Pricing, provider acceptance, rights, actual teaching quality, student privacy and owner identity/banking remain prerequisites. The local course-launch plan describes private delivery and secure checkout separately from this public repository.

## Evidence method and boundaries

This is a curated education expansion, not a systematic review or an exhaustive review of every product formulation. Source inclusion depends on identifiable publisher, a public HTTPS destination, relevant scope, and explicit limits. Every new guide states that it has received an editorial source check, not independent clinician review.

1. Government fact sheets and guidelines: general education; not a catalog endorsement.
2. Professional/medical education: clinical context, not an assigned reviewer or invented credential.
3. Primary studies: preserve design and population limits; distinguish main outcomes from secondary observations and association from causation. Funding and author disclosures still need consideration.
4. Manufacturer test descriptions: sampling/measurement and logistics only, clearly distinguished from independent clinical validation.
5. Product associations: ingredient/topic navigation, **not finished-product effectiveness evidence**. The old “product-specific documentation” wording was corrected to avoid that implication.

The VITAL omega-3 trial is not evidence that the catalog's oils prevent disease; its main outcomes and population cannot be replaced with a stronger sales claim. The IPA study is observational. The microbiome consensus is not a direct evaluation of Zinzino's blood-metabolite test. Supplements, test results, and genetics are not used to calculate diagnoses or personal treatment plans.

Named clinicians appear only as authors/speakers within their actual public sources, not as endorsers or reviewers of The Mindful Matrix.

## Validation

- Canonical build: **88 public pages**, 24 published-candidate guides, 45 active / 8 deferred products.
- Python tests: **137 passed**, including nine new Academy static/accessibility/privacy contracts and the 16 learning/evidence/privacy regression tests.
- JavaScript tests: **24 passed** — nine existing measurement tests and 15 new Academy state/event-binding tests. The event fixtures are not real-browser tests.
- Deterministic rebuild: all 88 generated-page hashes unchanged.
- Local HTTP coverage: **88 pages / 175 assets**, zero failed requests or content mismatches after text-only CRLF/LF normalization for the Windows preview. Production audit comparison is unchanged.
- Static validation: links, fragments, images and dimensions, duplicate IDs, headings, canonical/social metadata, sitemap, product gating, and disclosures pass.
- Public safety scan: **88 pages**, zero findings.
- No interactive browser/responsive, console, or screenshot QA was performed for this expansion. Do not interpret the static and HTTP checks as that coverage.
- No live production migration or deployment was attempted.

### External-source availability

The independent HTTP/title checker confirmed **33/40** source destinations. Seven exceptions are retained honestly in `source-link-audit.json`: three HTTP 403 responses, two transport failures, and two PubMed responses whose titles did not contain the article title.

A separate web-content check read the two AAD pages, CDC sleep page, AHA omega page, Johns Hopkins enzyme page, and VITAL PubMed record. The microbiome consensus title, PMID 39647502, DOI 10.1016/S2468-1253(24)00311-X, abstract, and author disclosures were retrieved from the indexed PubMed record; direct PubMed/PMC reads presented a browser challenge. This verifies bibliographic identity, not uninterrupted client access. No checker exceptions were suppressed or relabeled as HTTP success.

## Compliance reconciliation

Fresh execution of the baseline's own validator gives **69 review warnings / 76 strict advisory items**. The candidate gives **329 / 336**, with **zero RED findings and no hard-rule violations detected by Compliance Engine v1**.

The entire increase of **260** strict finding locations is explained by the newly covered partner surfaces:
- `content/partner-learning.json`: 51
- `partners.html`: 209

The engine deliberately sends partner/recruitment-context text to human review. That includes ordinary headings, educational business text, navigation, and protective statements. The new health guides and source manifest added no net strict-advisory increase. The exact records are retained in `new-review-advisories.json`; passing a hard gate does not approve these statements for release.

The seven inherited Priority 1 findings remain inherited human-review items. Registry classifications, sources, qualifications, and disclosures are unchanged. Xtend+ “multi-immune” wording remains unchanged and remains the first future editorial-review priority.

## Review decision

1. Review Testing, the new Library guides, Evidence classifications, and both redesigned Academy experiences.
2. Resolve/approve the new partner human-review findings before merging; do not suppress them.
3. Review the two local course manuscripts separately. Establish permissions for any proposed proprietary teaching asset.
4. Perform a requested visual/responsive review and any needed expert editorial review.
5. Authorize release separately. No merge or deployment is authorized by this packet.

## Reproduce

```text
python scripts/build.py
python scripts/validate.py
python scripts/validate.py --compliance-strict --compliance-dry-run
python -m unittest discover -s tests -v
node --test tests/measurement.test.cjs tests/academy.test.cjs
python scripts/scan_v10_public_safety.py
python scripts/validate_public_sources.py --check-urls --timeout 12 --report _review/testing-library-partner-learning/source-link-audit.json
python scripts/audit_learning_candidate.py --local-url http://127.0.0.1:8775/
```

Serve the candidate locally before the final command. The source checker intentionally exits nonzero for unresolved transport/title failures. Its report is evidence to review, not a reason to disable checks.

## Source inventory

- **government fact sheet** — [Omega-3 Fatty Acids — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: The page is broad reference material. Individual studies and qualified claims still require context, and it does not establish personal need or treatment advice.
- **government fact sheet** — [Vitamin D — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Population guidance cannot determine an individual dose or explain a result without clinical context, and evidence varies by outcome.
- **government fact sheet** — [Probiotics: Usefulness and Safety](https://www.nccih.nih.gov/health/probiotics-usefulness-and-safety) (National Center for Complementary and Integrative Health). Limits: Effects can depend on strain, formulation, population, and outcome. Safety evidence is more limited for vulnerable populations and long-term use.
- **government consumer guide** — [Hemoglobin A1C (HbA1c) Test](https://medlineplus.gov/lab-tests/hemoglobin-a1c-hba1c-test/) (MedlinePlus, U.S. National Library of Medicine). Limits: Interpretation can be affected by health conditions and clinical context; visitors should use their clinician and laboratory report for personal decisions.
- **regulatory guidance** — [Dietary Supplement Labeling Guide](https://www.fda.gov/food/dietary-supplements-guidance-documents-regulatory-information/dietary-supplement-labeling-guide) (U.S. Food and Drug Administration). Limits: The guide contains nonbinding recommendations and must be read alongside current statutes, regulations, and later FDA updates.
- **regulatory guidance** — [Label Claims for Food and Dietary Supplements](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/label-claims-food-dietary-supplements) (U.S. Food and Drug Administration). Limits: Claim requirements depend on wording, evidence, product category, and current law; the page is not a substitute for product-specific review.
- **government consumer guide** — [Background Information: Dietary Supplements](https://ods.od.nih.gov/factsheets/dietarysupplements-Consumer/) (National Institutes of Health, Office of Dietary Supplements). Limits: The page cannot determine whether a specific supplement is appropriate, effective, or safe for an individual and does not replace professional advice.
- **government guideline** — [About the Physical Activity Guidelines](https://odphp.health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines/about-physical-activity-guidelines) (HHS Office of Disease Prevention and Health Promotion). Limits: The current public edition dates to 2018, individual abilities and health conditions vary, and the source does not evaluate supplements or branded tools.
- **government fact sheet** — [Magnesium — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Does not establish that glycinate is best for everyone or validate any catalog formulation.
- **government fact sheet** — [Zinc — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Does not prescribe a zinc-to-copper ratio or substantiate a branded immune claim.
- **government fact sheet** — [Copper — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/Copper-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: A paired supplement is not automatically needed; individual health conditions matter.
- **government fact sheet** — [Vitamin K — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Does not establish that everyone taking vitamin D needs K2 or that a product prevents vascular calcification.
- **government fact sheet** — [Vitamin B12 — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Does not establish energy or cognitive benefits in a person whose B12 status is adequate.
- **government fact sheet** — [Vitamin C — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Nutrient function is not proof that an immune-marketed product prevents infection.
- **government fact sheet** — [Iodine — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/Iodine-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Does not establish that more iodine improves thyroid function or validate a mood claim.
- **government fact sheet** — [Folate — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Not evidence for a genetic-personalization promise or a whole-formula outcome.
- **government fact sheet** — [Multivitamin/mineral Supplements — Health Professional Fact Sheet](https://ods.od.nih.gov/factsheets/MVMS-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Does not establish disease prevention or an outcome for a particular multi-nutrient product.
- **government fact sheet** — [Dietary Supplements for Exercise and Athletic Performance](https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: Single-ingredient research cannot establish the performance or safety of a multi-ingredient product.
- **government fact sheet** — [Dietary Supplements for Immune Function and Infectious Diseases](https://ods.od.nih.gov/factsheets/ImmuneFunction-HealthProfessional/) (National Institutes of Health, Office of Dietary Supplements). Limits: This is not product substantiation; it does not resolve inherited commercial wording that still needs human review.
- **government fact sheet** — [Turmeric: Usefulness and Safety](https://www.nccih.nih.gov/health/turmeric) (National Center for Complementary and Integrative Health). Limits: Enhanced absorption is not the same as improved clinical outcomes; evidence cannot be transferred between formulations.
- **government fact sheet** — [Antioxidant Supplements: What You Need To Know](https://www.nccih.nih.gov/health/antioxidant-supplements-what-you-need-to-know) (National Center for Complementary and Integrative Health). Limits: Does not validate a particular extract, establish a benefit from a laboratory antioxidant score, or confirm product purity.
- **government fact sheet** — [Detoxes and Cleanses: What You Need To Know](https://www.nccih.nih.gov/health/detoxes-and-cleanses-what-you-need-to-know) (National Center for Complementary and Integrative Health). Limits: Not an endorsement of cleansing, binders or any catalog product; persistent symptoms need clinical assessment.
- **government fact sheet** — [Using Dietary Supplements Wisely](https://www.nccih.nih.gov/health/using-dietary-supplements-wisely) (National Center for Complementary and Integrative Health). Limits: Does not verify ingredient amounts, quality or effectiveness of individual catalog products.
- **government fact sheet** — [Vitamin D Test](https://medlineplus.gov/lab-tests/vitamin-d-test/) (MedlinePlus, U.S. National Library of Medicine). Limits: Does not endorse a home collection method, prescribe a dose or interpret a person's result.
- **government fact sheet** — [How to Understand Your Lab Results](https://medlineplus.gov/lab-tests/how-to-understand-your-lab-results/) (MedlinePlus, U.S. National Library of Medicine). Limits: An in-range result is not a complete health assessment; methods and ranges can differ between laboratories.
- **government fact sheet** — [Pros and Cons of Direct-to-Consumer Genetic Testing](https://medlineplus.gov/genetics/understanding/dtcgenetictesting/dtcrisksbenefits/) (MedlinePlus, U.S. National Library of Medicine). Limits: Does not validate a specific report, supplement recommendation or prediction from a genetic variant.
- **government fact sheet** — [Before Direct-to-Consumer Genetic Testing](https://medlineplus.gov/genetics/understanding/dtcgenetictesting/dtcknow/) (MedlinePlus, U.S. National Library of Medicine). Limits: Provider policies require separate current review; this source does not certify any vendor's privacy practices.
- **government fact sheet** — [The A1C Test & Diabetes](https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test) (National Institute of Diabetes and Digestive and Kidney Diseases). Limits: Not real-time glucose monitoring. A clinician must choose and interpret appropriate diagnostic testing.
- **government fact sheet** — [Eating, Diet, & Nutrition for Constipation](https://www.niddk.nih.gov/health-information/digestive-diseases/constipation/eating-diet-nutrition) (National Institute of Diabetes and Digestive and Kidney Diseases). Limits: This condition-specific guidance does not mean a catalog fiber product treats constipation or is appropriate for everyone.
- **government guideline** — [Physical Activity](https://www.who.int/news-room/fact-sheets/detail/physical-activity) (World Health Organization). Limits: Does not prescribe an individual exercise program or endorse accessories.
- **government fact sheet** — [About Sleep](https://www.cdc.gov/sleep/about/index.html) (Centers for Disease Control and Prevention). Limits: Sleep difficulties can have medical causes; this page is not evidence for a sleep supplement.
- **professional guideline** — [Vitamin D for the Prevention of Disease](https://www.endocrine.org/clinical-practice-guidelines/vitamin-d-for-prevention-of-disease) (Endocrine Society). Limits: Not guidance for every patient or existing clinical indication. It does not support indiscriminate testing.
- **professional education** — [Should I Take Vitamins or Supplements for My Skin?](https://www.aad.org/public/everyday-care/skin-care-secrets/routine/supplements-for-your-skin) (American Academy of Dermatology). Limits: Does not test the catalog collagen drink or topical serum; nutrient roles are not proof of a cosmetic outcome.
- **professional education** — [Supplement Secrets Unveiled: Debunking Common Myths About Beauty Boosters](https://www.aad.org/news/supplements-debunking-common-myths) (American Academy of Dermatology). Limits: Reported possibilities should not be read as guaranteed improvements; more research is needed.
- **professional education** — [Sunscreen FAQs](https://www.aad.org/media/stats-sunscreen) (American Academy of Dermatology). Limits: Not evidence that an ordinary serum or an oral supplement offers sunscreen protection.
- **professional education** — [Fish and Omega-3 Fatty Acids](https://www.heart.org/en/healthy-living/healthy-eating/eat-smart/fats/fish-and-omega-3-fatty-acids) (American Heart Association). Limits: Does not mean a fish-oil product reproduces the effects of a dietary pattern.
- **professional education** — [Digestive Enzymes and Digestive Enzyme Supplements](https://www.hopkinsmedicine.org/health/wellness-and-prevention/digestive-enzymes-and-digestive-enzyme-supplements) (Johns Hopkins Medicine). Limits: Does not validate the 17-enzyme formula or justify treating persistent symptoms without assessment.
- **randomized trial** — [Marine n-3 Fatty Acids and Prevention of Cardiovascular Disease and Cancer](https://pubmed.ncbi.nlm.nih.gov/30415637/) (New England Journal of Medicine (PubMed record)). Limits: Primary and secondary outcomes must be distinguished. Not a trial of catalog products; author and funding disclosures remain relevant.
- **observational study** — [Indolepropionic Acid and Novel Lipid Metabolites in the Finnish Diabetes Prevention Study](https://www.nature.com/articles/srep46337) (Scientific Reports). Limits: An association does not prove causation, validate a commercial index, or show that raising a marker with a supplement improves outcomes.
- **expert consensus** — [International Consensus Statement on Microbiome Testing in Clinical Practice](https://pubmed.ncbi.nlm.nih.gov/39647502/) (The Lancet Gastroenterology & Hepatology (PubMed record)). Limits: Microbiome profiling is not the same method as a blood-metabolite test. This consensus does not validate or directly evaluate Zinzino's test.

Detailed per-product coverage: `product-evidence-coverage.json`. No source connection is a claim that the corresponding finished product works.
