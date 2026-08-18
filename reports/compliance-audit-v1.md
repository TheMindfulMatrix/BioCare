# The Mindful Matrix — Compliance Audit v1

Audit date: `2026-08-18`

Engine/ruleset: `1.0.0` / `1.0.0`

Scope: `22` source, template, and generated-public files

> This is a machine-assisted risk-control audit. It is not legal advice, regulatory approval, or a guarantee of compliance.

## Summary

- Total claim-bearing records: **2111**
- GREEN: **1886**
- YELLOW: **225**
- RED: **0**
- Ambiguous/implied: **6**
- Exact registry matches: **310**

## Finding classification

- HIGH_PRIORITY_REVIEW: **151**
- LOW_RISK: **1677**
- PASS: **209**
- YELLOW_REVIEW: **74**

## Non-PASS findings

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “A framework for taking a more informed, intentional role in your wellness.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.matrix.conclusionCopy`
  - `index.html:863`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “A manufacturer-formulated powder included for visitors comparing ordinary non-peptide wellness formats.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[42].whyItsHere`
  - `index.html:706`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “A non-peptide digestive-enzyme format grouped with other gut and digestion tools.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[51].whyItsHere`
  - `index.html:786`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “A practical hierarchy for sleep, food, fluid, training load and recovery tools—without pretending every workout needs a product.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:978`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “A practical map of the gut microbiome, the factors that shape it, and the line between useful evidence and confident-sounding speculation.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:964`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “A repeatable way to inspect the question, design, population, outcome, effect size, uncertainty and conflicts behind a health headline.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:992`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “At-home blood sample card moving through a precise omega measurement interface”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:941`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Athletic energy pathways connecting whole-food fuel, hydration and muscle signals”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:983`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Balance Test Basic Kit official Zinzino product packaging”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[0].cutout.alt`
  - `index.html:116`
  - `index.html:77`
  - `index.html:913`
  - `shop.html:93`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Browse the current gut health collection on Zinzino.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.fallbackDestinations[2].description`
  - `shop.html:236`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Browse the current home health tests collection on Zinzino.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.fallbackDestinations[0].description`
  - `shop.html:236`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Browse verified daily supplement formats from the current catalog.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.intents[3].description`
  - `shop.html:152`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Education is here to support the decision—not stand between you and it.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.hero.copy`
  - `index.html:59`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Energy Bar Nut & Seed official Zinzino product packaging”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[32].cutout.alt`
  - `index.html:596`
  - `shop.html:216`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Evidence-aware wellness education, clearer questions, and transparent optional tools—organized from information to action.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.site.description`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Explore verified omega and nutrition formats in the current US catalog.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.intents[1].description`
  - `shop.html:113`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Gut Health 101: The Microbiome—and What We Actually Know”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:964`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Gut Health Test official Zinzino product packaging”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[2].cutout.alt`
  - `index.html:156`
  - `shop.html:99`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Gut Health Test x2 official Zinzino product packaging”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[3].cutout.alt`
  - `shop.html:102`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Gut Testing: What Biomarkers Can—and Can’t—Tell You”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:971`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “HbA1c Test official Zinzino product packaging”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[5].cutout.alt`
  - `index.html:196`
  - `shop.html:108`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “How to Read a Health Study Without Getting Fooled”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:992`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “How to Read a Supplement Label Without Overreading It”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:957`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “How to read a supplement label”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[48].relatedEducation.label`
  - `content/catalog.json:$.products[49].relatedEducation.label`
  - `content/catalog.json:$.products[50].relatedEducation.label`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “How to read a supplement label →”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:727`
  - `index.html:747`
  - `index.html:767`
  - `shop.html:187`
  - `shop.html:190`
  - `shop.html:193`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “If we can financially benefit from something, visitors should know.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.standards.principles[3].copy`
  - `index.html:1011`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Laboratory sample channel, biomarker bands and microbial signals in a dark diagnostic interface”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:969`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Learn what a Supplement Facts panel can establish, what claims and disclaimers do not prove, and how to compare serving size, amounts, ingredients and quality signals.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:957`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Learn what an omega-3 blood test can—and can’t—tell you.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.testing.education.heading`
  - `index.html:926`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Learn what omega-3 blood tests measure, what can affect a result, and why a number is information—not a diagnosis.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:943`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Omega-3 lipid molecules and blood-status signals in a dark biological matrix”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:934`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Omega-3: What It Is, What You Can Measure, and What the Numbers Actually Mean”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:936`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Organize energy, protein, carbohydrate, hydration and meal timing before deciding whether a supplement solves anything.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:985`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Our featured test-first route, pairing the measurement with the included product format.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[0].whyItsHere`
  - `index.html:126`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “People are surrounded by health advice, supplements, diets, studies, opinions, and trends.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.problem.copy`
  - `index.html:830`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Performance Nutrition: The Basics Before Supplements”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:985`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Practical wellness education built around credible sources, context, and useful next steps.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.site.metadata.pages.library.description`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Should You Test Your Omega-3 Levels?”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:943`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Start with what omega-3 blood testing can—and can’t—tell you.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.startHere.pathways.items[1].copy`
  - `start.html:78`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Supplement label under an evidence-reading scanner with ingredient and dose fields”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:955`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The Balance Test Basic Kit preserves the previously approved site summary.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.contentPolicy`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The Plus variant in the Xtend daily supplement range.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[22].whyItsHere`
  - `index.html:486`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The dietary-fiber format in the gut and digestion collection.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[16].whyItsHere`
  - `index.html:386`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The individual at-home test dedicated to HbA1c measurement.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[5].whyItsHere`
  - `index.html:206`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The individual at-home test dedicated to vitamin D measurement.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[4].whyItsHere`
  - `index.html:186`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The individual fatty-acid test for visitors who want the test without a kit.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[1].whyItsHere`
  - `index.html:146`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The liquid spirulina format in the active-nutrition group.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[26].whyItsHere`
  - `index.html:566`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The liquid turmeric-root format listed in Zinzino’s gut-health collection.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[17].whyItsHere`
  - `index.html:406`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The single-pack Viva+ option in the daily supplement group.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[19].whyItsHere`
  - `index.html:446`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The single-test option in the home health testing range.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[2].whyItsHere`
  - `index.html:166`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The solid-food option in the active-nutrition assortment.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[32].whyItsHere`
  - `index.html:606`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The standard variant in the Xtend daily supplement range.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[23].whyItsHere`
  - `index.html:506`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “The two-test option for visitors comparing single- and two-test quantities.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[3].whyItsHere`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Understand ALA, EPA, DHA, the Omega-3 Index, fatty-acid ratios and what blood measurements can—and cannot—tell you.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:936`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Understand the difference between ALA, EPA and DHA, where food fits, when supplements may be useful, and why changing a biomarker is not the same as guaranteeing a health outcome.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:950`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Understand the difference between clinically ordered stool or blood markers and consumer microbiome profiles before acting on a result.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:971`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “View Balance Test Basic Kit on Zinzino (opens in a new tab)”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:74`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Vitamin D Test official Zinzino product packaging”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/catalog.json:$.products[4].cutout.alt`
  - `index.html:176`
  - `shop.html:105`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “We're creating practical wellness guides grounded in credible sources—not more noise.”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.library.statusCopy`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “What a Blood Test Can—and Can’t—Tell You”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:943`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “What does this information support?”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `content/site.json:$.homepage.startHere.stages[1].question`
  - `start.html:66`

### HIGH_PRIORITY_REVIEW — EFFICACY_CLAIM

- Exact text: “Whole-food omega sources balanced against a neutral supplement form”
- Risk: `YELLOW`
- Reason: Unregistered commercial or mixed-context health language requires claim classification and evidence review.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `REGISTER_CLAIM_OR_HUMAN_REVIEW`
- Locations:
  - `index.html:948`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer bundle combining multiple BioLimitless formulas, including Cellular Reset and Neuro Reboot.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[47].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer bundle containing Cellular Reset and other BioLimitless formulas.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[45].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer bundle containing Neuro Reboot and other BioLimitless formulas.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[46].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer bundle containing formulas from the BioLimitless product line, including Master Microbiotics.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[44].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer bundle that includes Cell Signals, Detox Pro Plus and Master Microbiotics.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[43].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer-described capsule formula that lists BPC-157 among its ingredients.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[36].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer-described formula that lists 5-Amino-1-MQ, BPC-157 and SLU-PP-332 among its ingredients.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[40].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “A manufacturer-described formula that lists Tesofensine, Dihexa and BPC-157 among its ingredients.”
- Risk: `YELLOW`
- Reason: Exact registered wording is not approved for the COMMERCIAL_PRODUCT context.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `DEFERRED_COMPLIANCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[41].description`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “An at-home saliva collection kit used for BioLimitless's SNP-based genomic report and app experience.”
- Risk: `YELLOW`
- Reason: Current wording registered without strengthening; manufacturer sourcing is not independent efficacy substantiation.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/catalog.json:$.products[37].description`
  - `index.html:663`
  - `shop.html:112`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “The test plus BalanceOil+, with the monthly subscription. You test at home, post it to the lab, and choose from there.”
- Risk: `YELLOW`
- Reason: Current wording registered without strengthening; manufacturer sourcing is not independent efficacy substantiation.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/catalog.json:$.products[0].description`
  - `index.html:123`
  - `index.html:917`
  - `shop.html:94`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “Track your fatty acid profile from home”
- Risk: `YELLOW`
- Reason: Current wording registered without strengthening; manufacturer sourcing is not independent efficacy substantiation.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/catalog.json:$.products[1].description`
  - `index.html:143`
  - `shop.html:97`

### HIGH_PRIORITY_REVIEW — FACTUAL_PRODUCT_FACT

- Exact text: “Track your long-term blood sugar levels”
- Risk: `YELLOW`
- Reason: Current wording registered without strengthening; manufacturer sourcing is not independent efficacy substantiation.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/catalog.json:$.products[5].description`
  - `index.html:203`
  - `shop.html:109`

### HIGH_PRIORITY_REVIEW — IMPLIED_CLAIM_REVIEW

- Exact text: “Cellular Reset”
- Risk: `YELLOW`
- Reason: Escalates suspicious heading/copy/image combinations because deterministic rules cannot resolve the complete net impression.
- Source/rule: `CE_YELLOW_IMPLIED_CLAIM`
- Recommended next action: `IMPLIED_CLAIM_REVIEW`
- Locations:
  - `content/catalog.json:$.products[40].name`

### HIGH_PRIORITY_REVIEW — IMPLIED_CLAIM_REVIEW

- Exact text: “Cellular Reset official BioLimitless product presentation”
- Risk: `YELLOW`
- Reason: Escalates suspicious heading/copy/image combinations because deterministic rules cannot resolve the complete net impression.
- Source/rule: `CE_YELLOW_IMPLIED_CLAIM`
- Recommended next action: `IMPLIED_CLAIM_REVIEW`
- Locations:
  - `content/catalog.json:$.products[40].cutout.alt`

### HIGH_PRIORITY_REVIEW — IMPLIED_CLAIM_REVIEW

- Exact text: “Cellular Reset | Peptide formula | formula | Inventoried for catalog completeness; multiple research-compound ingredients require elevated compliance review. | A manufacturer-described formula that lists 5-Amino-1-MQ, BPC-157 and SLU-PP-332 among its ingredients. | Official BioLimitless Cellular Reset”
- Risk: `YELLOW`
- Reason: Escalates suspicious heading/copy/image combinations because deterministic rules cannot resolve the complete net impression.
- Source/rule: `CE_YELLOW_IMPLIED_CLAIM`
- Recommended next action: `IMPLIED_CLAIM_REVIEW`
- Locations:
  - `content/catalog.json:$.products[40]`

### HIGH_PRIORITY_REVIEW — IMPLIED_CLAIM_REVIEW

- Exact text: “Cellular Stack | Power stack | stack | Inventoried as a manufacturer bundle; it includes deferred research-compound formulas. | A manufacturer bundle containing Cellular Reset and other BioLimitless formulas. | Official BioLimitless Cellular Stack”
- Risk: `YELLOW`
- Reason: Escalates suspicious heading/copy/image combinations because deterministic rules cannot resolve the complete net impression.
- Source/rule: `CE_YELLOW_IMPLIED_CLAIM`
- Recommended next action: `IMPLIED_CLAIM_REVIEW`
- Locations:
  - `content/catalog.json:$.products[45]`

### HIGH_PRIORITY_REVIEW — IMPLIED_CLAIM_REVIEW

- Exact text: “Includes Cellular Reset, which lists 5-Amino-1-MQ, BPC-157 and SLU-PP-332; elevated owner-approved compliance review is required.”
- Risk: `YELLOW`
- Reason: Escalates suspicious heading/copy/image combinations because deterministic rules cannot resolve the complete net impression.
- Source/rule: `CE_GREEN_FACTUAL_COUNT, CE_YELLOW_IMPLIED_CLAIM`
- Recommended next action: `IMPLIED_CLAIM_REVIEW`
- Locations:
  - `content/catalog.json:$.products[45].complianceReview.reason`

### HIGH_PRIORITY_REVIEW — IMPLIED_CLAIM_REVIEW

- Exact text: “Master Stack | Power stack | stack | Inventoried as the broad manufacturer bundle; it includes multiple deferred research-compound formulas. | A manufacturer bundle combining multiple BioLimitless formulas, including Cellular Reset and Neuro Reboot. | Official BioLimitless Master Stack”
- Risk: `YELLOW`
- Reason: Escalates suspicious heading/copy/image combinations because deterministic rules cannot resolve the complete net impression.
- Source/rule: `CE_YELLOW_IMPLIED_CLAIM`
- Recommended next action: `IMPLIED_CLAIM_REVIEW`
- Locations:
  - `content/catalog.json:$.products[47]`

### HIGH_PRIORITY_REVIEW — SCIENTIFIC_EVIDENCE_CLAIM

- Exact text: “A proven performance use at an appropriate dose?”
- Risk: `YELLOW`
- Reason: The advertiser must possess at least the level and type of substantiation communicated by the claim.
- Source/rule: `CE_YELLOW_SCIENTIFIC_LANGUAGE`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/library.json:$.articles[7].bodySections[4].blocks[0].text`
  - `library/performance-nutrition-basics.html:66`

### HIGH_PRIORITY_REVIEW — SCIENTIFIC_EVIDENCE_CLAIM

- Exact text: “If only a surrogate marker changed, ask whether changing that marker has been shown to improve outcomes people care about.”
- Risk: `YELLOW`
- Reason: The advertiser must possess at least the level and type of substantiation communicated by the claim.
- Source/rule: `CE_YELLOW_SCIENTIFIC_LANGUAGE`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/library.json:$.articles[8].bodySections[3].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### HIGH_PRIORITY_REVIEW — SCIENTIFIC_EVIDENCE_CLAIM

- Exact text: “Phrases such as ‘premium,’ ‘clean,’ ‘medical grade,’ ‘clinically tested’ or ‘science-backed’ need definitions.”
- Risk: `YELLOW`
- Reason: The advertiser must possess at least the level and type of substantiation communicated by the claim.
- Source/rule: `CE_YELLOW_SCIENTIFIC_LANGUAGE`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/library.json:$.articles[3].bodySections[5].blocks[2].text`
  - `library/how-to-read-a-supplement-label.html:64`

### HIGH_PRIORITY_REVIEW — SCIENTIFIC_EVIDENCE_CLAIM

- Exact text: “What research suggests and what we personally think should not be presented as the same thing.”
- Risk: `YELLOW`
- Reason: The advertiser must possess at least the level and type of substantiation communicated by the claim.
- Source/rule: `CE_YELLOW_SCIENTIFIC_LANGUAGE`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/site.json:$.homepage.standards.principles[2].copy`
  - `index.html:1010`
  - `library.html:147`

### HIGH_PRIORITY_REVIEW — STRUCTURE_FUNCTION_CLAIM

- Exact text: “Home health blood spot test to track gut and metabolic markers”
- Risk: `YELLOW`
- Reason: Current wording registered without strengthening; manufacturer sourcing is not independent efficacy substantiation.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/catalog.json:$.products[2].description`
  - `content/catalog.json:$.products[3].description`
  - `index.html:163`
  - `shop.html:100`
  - `shop.html:103`

### HIGH_PRIORITY_REVIEW — STRUCTURE_FUNCTION_CLAIM

- Exact text: “Multi-immune food supplement with 22 naturally derived micro- and phytonutrients”
- Risk: `YELLOW`
- Reason: Current wording registered without strengthening; manufacturer sourcing is not independent efficacy substantiation.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `HUMAN_REVIEW_REQUIRED`
- Locations:
  - `content/catalog.json:$.products[22].description`
  - `index.html:483`
  - `shop.html:166`

### YELLOW_REVIEW — AFFILIATE_RELATIONSHIP_CLAIM

- Exact text: “Federal Trade Commission”
- Risk: `YELLOW`
- Reason: Material-connection language requires exact approved disclosure wording and clear, conspicuous placement.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_DISCLOSURE_AND_PLACEMENT`
- Locations:
  - `content/library.json:$.articles[3].sources[6].organization`
  - `library/how-to-read-a-supplement-label.html:68`

### YELLOW_REVIEW — GENERAL_WELLBEING_CLAIM

- Exact text: “Testing is one possible way to become more informed. It is a starting point for asking better questions—not the entire Mindful Matrix philosophy.”
- Risk: `YELLOW`
- Reason: Registered as education-first testing language with explicit limitations.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/site.json:$.homepage.testing.copy`
  - `index.html:909`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “A universal intake or biomarker target for every person.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.groups[2].items[0]`
  - `library/food-vs-omega-3-supplements.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “A universal normal or optimal target for every person.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[1].evidenceSummary.groups[2].items[0]`
  - `library/should-you-test-your-omega-3-levels.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “A universal threshold or single criterion that proves causality in every health question.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[9].evidenceSummary.groups[2].items[0]`
  - `library/correlation-causation-relative-risk.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “A universally optimal omega-3 status or omega-6:omega-3 ratio.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[0].evidenceSummary.groups[2].items[1]`
  - `library/omega-3-what-the-numbers-mean.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “ALA conversion contributes to EPA and DHA availability, but conversion—particularly to DHA—is limited and variable.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.groups[1].items[1]`
  - `library/food-vs-omega-3-supplements.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Appropriately selected biomarkers can contribute to a clinical evaluation when interpreted with symptoms and history.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[5].evidenceSummary.groups[1].items[0]`
  - `library/gut-testing-biomarkers.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Blood biomarkers can provide information about EPA and DHA exposure or status.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[1].evidenceSummary.groups[1].items[0]`
  - `library/should-you-test-your-omega-3-levels.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Broad consumer scores as diagnostic tools or as reliable selectors of personalized treatments.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[5].evidenceSummary.groups[2].items[0]`
  - `library/gut-testing-biomarkers.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Comparable repeat testing can document biomarker change after sufficient time, but response varies between people.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[1].evidenceSummary.groups[1].items[1]`
  - `library/should-you-test-your-omega-3-levels.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Converging evidence from stronger designs, replication and plausible mechanisms can increase causal confidence.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[9].evidenceSummary.groups[1].items[0]`
  - `library/correlation-causation-relative-risk.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Dose, ingredient form and serving size improve evidence comparison.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.groups[1].items[1]`
  - `library/how-to-read-a-supplement-label.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Food variety and certain fibers can support useful microbial functions for many people.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[4].evidenceSummary.groups[1].items[0]`
  - `library/gut-health-101.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Food-first seafood guidance can be a practical starting point for many adults.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.groups[1].items[2]`
  - `library/food-vs-omega-3-supplements.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Health claims should be evaluated for both their express and implied meaning.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.groups[1].items[2]`
  - `library/how-to-read-a-supplement-label.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “How individual fatty-acid indices should be translated into clinical decisions across different populations.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[0].evidenceSummary.groups[2].items[2]`
  - `library/omega-3-what-the-numbers-mean.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “How one result should predict outcomes or direct clinical decisions for an individual.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[1].evidenceSummary.groups[2].items[2]`
  - `library/should-you-test-your-omega-3-levels.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Independent testing can verify defined quality attributes when its scope is clear.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.groups[1].items[0]`
  - `library/how-to-read-a-supplement-label.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Planned protein distribution, carbohydrate timing and hydration can improve recovery or performance in appropriate contexts.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[7].evidenceSummary.groups[1].items[0]`
  - `library/performance-nutrition-basics.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Preregistration, replication and rigorous systematic review can strengthen the evidence base.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[8].evidenceSummary.groups[1].items[0]`
  - `library/how-to-read-a-health-study.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Selected nutrition timing and recovery modalities can help in specific high-demand contexts.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[6].evidenceSummary.groups[1].items[0]`
  - `library/recovery-after-training.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Specific probiotics can help in specific contexts.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[4].evidenceSummary.groups[1].items[1]`
  - `library/gut-health-101.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Supplemental EPA and DHA can raise measured EPA and DHA status.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.groups[1].items[0]`
  - `library/food-vs-omega-3-supplements.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “The Omega-3 Index provides information about erythrocyte EPA and DHA status and is used in omega-3 research.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[0].evidenceSummary.groups[1].items[0]`
  - `library/omega-3-what-the-numbers-mean.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “The best PUFA biomarker for every situation.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[0].evidenceSummary.groups[2].items[0]`
  - `library/omega-3-what-the-numbers-mean.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “The best specimen or biomarker for every population and purpose.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[1].evidenceSummary.groups[2].items[1]`
  - `library/should-you-test-your-omega-3-levels.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “The best supplement form for every use, population and outcome.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.groups[2].items[2]`
  - `library/food-vs-omega-3-supplements.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “The clinical importance of a specific biomarker change for an individual.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.groups[2].items[1]`
  - `library/food-vs-omega-3-supplements.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “The testing guide explains what is measured, what can affect a result, and where interpretation stops.”
- Risk: `YELLOW`
- Reason: Registered as education-first testing language with explicit limitations.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/site.json:$.homepage.testing.education.copy`
  - `index.html:926`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Universal macro targets and broad multi-ingredient supplement claims.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[7].evidenceSummary.groups[2].items[0]`
  - `library/performance-nutrition-basics.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Universal microbial targets and broad treatment plans derived from commercial profiles.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[4].evidenceSummary.groups[2].items[0]`
  - `library/gut-health-101.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Universal timing rules, recovery scores and tool stacks that apply to everyone.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[6].evidenceSummary.groups[2].items[0]`
  - `library/recovery-after-training.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Using a single checklist score or journal label as a substitute for topic-specific judgment.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[8].evidenceSummary.groups[2].items[0]`
  - `library/how-to-read-a-health-study.html:67`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Whether a broad quality phrase corresponds to a meaningful verified standard.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.groups[2].items[1]`
  - `library/how-to-read-a-supplement-label.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Whether a product will improve a particular outcome for an individual.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.groups[2].items[0]`
  - `library/how-to-read-a-supplement-label.html:65`

### YELLOW_REVIEW — RESEARCH_INTERPRETATION

- Exact text: “Whether the labeled serving is appropriate in a person's medical and dietary context.”
- Risk: `YELLOW`
- Reason: Registered from the article's existing evidence summary without strengthening its wording.
- Source/rule: `CLAIM_REGISTRY_EXACT_MATCH`
- Recommended next action: `PASS_WITH_QUALIFICATION`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.groups[2].items[2]`
  - `library/how-to-read-a-supplement-label.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “% Daily Value: the proportion of an established Daily Value supplied by one serving, when a Daily Value exists.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[1].items[3]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “30 tablets”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `index.html:424`
  - `shop.html:154`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “60 capsules”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `index.html:524`
  - `shop.html:172`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “60 tablets”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `index.html:444`
  - `index.html:464`
  - `shop.html:157`
  - `shop.html:163`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “80 tablets”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `index.html:544`
  - `shop.html:175`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A careful label read can reduce uncertainty.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.statement`
  - `library/how-to-read-a-supplement-label.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A direct-to-consumer microbiome service may sequence microbial DNA and compare relative abundance or diversity with its own reference database.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].bodySections[1].blocks[0].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A full critical appraisal may require subject-matter and statistical expertise.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].limitations[1]`
  - `library/how-to-read-a-health-study.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A label is useful because it organizes specific declarations: what the product is, how large a serving is, which dietary ingredients are listed, how much is declared per serving, and what other ingredients are present.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[0].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A large relative change can describe a tiny absolute change when the starting risk is low.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].bodySections[3].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A longer measurement window does not make the result a permanent average or a day-by-day record.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[2].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A measurement-first option for visitors specifically exploring manufacturer-provided genomic information.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/catalog.json:$.products[37].whyItsHere`
  - `index.html:666`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A nondietary component such as a filler, binder, capsule material, flavor, color or sweetener.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[2].blocks[1].items[2].definition`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A number can provide information without independently telling you whether you're healthy, unhealthy, or whether you have a disease.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[3].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A personal philosophy about agency—not a replacement for professional healthcare.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.founder.philosophyContext`
  - `index.html:900`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A powder can be convenient; convenience is not proof that it is superior to food.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].bodySections[1].blocks[1].items[3]`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A probiotic name at the species level may not tell you what a specific strain does.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[1].blocks[1].items[3]`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A ratio can describe a relationship between numbers.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[4].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A real measurement is not automatically a clinically useful answer.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].evidenceSummary.statement`
  - `library/gut-testing-biomarkers.html:67`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A reasonable decision may be a food change, a professionally guided plan, more investigation, or no change at all.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[6].blocks[0].items[2].definition`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A recent meal can affect plasma or serum more than an erythrocyte measurement.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A result in one population, dose or outcome should not be silently generalized to another.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[4].blocks[2].items[2]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A structure/function claim describes an intended effect on normal body structure or function and is commonly paired with the statement that FDA has not evaluated the claim and that the product is not intended to diagnose, treat, cure or prevent disease.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[4].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A sudden large increase in fiber can cause symptoms, and probiotic or fermented products are not appropriate for everyone.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[3].blocks[1].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “A wide confidence interval may include both trivial and meaningful effects.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[8].bodySections[3].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Absolute risk difference describes the difference in event rates.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].evidenceLabels[0].items[1]`
  - `library/correlation-causation-relative-risk.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Absolute risk difference: exposed event rate minus comparison event rate.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[2].blocks[2].items[1]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Action might mean learning more, changing a habit, asking a better question, discussing it with a healthcare professional, measuring when appropriate, doing nothing yet, or considering a tool for a clear reason.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.startHere.stages[2].copy`
  - `start.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Active ingredients can cause adverse effects, add to nutrients from other products, or interact with medications and medical care.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[6].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Amount per serving: the declared weight or quantity of each dietary ingredient.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[1].items[2]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “An independent certification can add useful information when the certifier is identifiable and the tested attributes are clear.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[5].blocks[1].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “And a large relative change can describe a very small absolute difference.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].dek`
  - `library/correlation-causation-relative-risk.html:58`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Ask what result would change the next step.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[3].items[1]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Ask whether its design can answer the claim being made.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].bodySections[1].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “At its most direct, a result reports the relative amount of selected fatty acids in the analyzed specimen using a particular method.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Baseline risk changes the practical meaning.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[2].blocks[1].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Baseline → action → retest can be a useful organizational framework when there is a clear question and the measurements are comparable.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[6].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Benefits from a branded multi-ingredient formula without product-specific trials.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].evidenceLabels[2].items[2]`
  - `library/performance-nutrition-basics.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Blinding, complete follow-up and valid outcome measurement can reduce bias.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].evidenceLabels[0].items[1]`
  - `library/how-to-read-a-health-study.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “But trials can be short, small, unblinded, poorly adhered to or focused on surrogate outcomes.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[3].blocks[0].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “But understanding what the numbers actually measure is more useful than chasing a single ‘perfect’ score.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].dek`
  - `library/omega-3-what-the-numbers-mean.html:56`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “But where the measurement comes from matters.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[0].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Can a follow-up use a comparable specimen and method?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[7].blocks[0].items[6]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Check inclusion criteria, sample size, randomization, blinding, comparison group, duration, dropouts, adherence and whether the outcome measure was valid.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].bodySections[2].blocks[0].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Check the exact ingredient and dose.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].bodySections[4].blocks[1].items[0]`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Checkout reflects the current applicable price.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.site.premierPricingNote`
  - `index.html:145`
  - `index.html:165`
  - `index.html:185`
  - `index.html:205`
  - `index.html:225`
  - `index.html:245`
  - `index.html:265`
  - `index.html:285`
  - `index.html:305`
  - `index.html:325`
  - `index.html:345`
  - `index.html:365`
  - `index.html:385`
  - `index.html:405`
  - `index.html:425`
  - `index.html:445`
  - `index.html:465`
  - `index.html:485`
  - `index.html:505`
  - `index.html:525`
  - `index.html:545`
  - `index.html:565`
  - `index.html:585`
  - `index.html:605`
  - `index.html:625`
  - `index.html:645`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Collection timing, storage temperature, shipping time, extraction method, sequencing technology, reference databases and analysis software can all affect the final profile.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].bodySections[2].blocks[0].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Collection, storage, specimen preparation, analytical method, calculation, and reporting conventions can affect how directly results can be compared.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[5].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Common food sources include flaxseed, chia seeds, walnuts and certain plant oils.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[2].bodySections[1].blocks[1].items[0].definition`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Comparing amount per serving is more informative than comparing front-label slogans.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[1].items[0]`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Competitive athletes should consider anti-doping contamination risk and governing-body rules.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].limitations[2]`
  - `library/performance-nutrition-basics.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Confirm whether the result is a measurement, percentile, proprietary score or interpretation.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].bodySections[3].blocks[0].items[0]`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Confounding, selection, measurement error, reverse causation and chance can create or distort associations.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].keyTakeaways[1]`
  - `library/correlation-causation-relative-risk.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Contains 5-Amino-1-MQ, BPC-157 and SLU-PP-332; elevated owner-approved compliance review is required before public commercial treatment.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[40].complianceReview.reason`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Contains BPC-157; elevated owner-approved compliance review is required before public commercial treatment.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[36].complianceReview.reason`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Contains Tesofensine, Dihexa and BPC-157; elevated owner-approved compliance review is required before public commercial treatment.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[41].complianceReview.reason`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Correlation, Causation, and Relative Risk | The Mindful Matrix”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].seoTitle`
  - `library/correlation-causation-relative-risk.html:6`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Correlation, Causation, and Relative Risk: A Practical Guide”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].title`
  - `index.html:999`
  - `library.html:136`
  - `library/correlation-causation-relative-risk.html:58`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Correlation, Causation, and Relative Risk: A Practical Guide →”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `library/how-to-read-a-health-study.html:71`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Decide what question the change is meant to answer before buying or testing anything.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[6].blocks[0].items[4]`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Diet can change microbial activity quickly, while lasting community changes are harder to predict.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[1].blocks[1].items[1]`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Diet, medications, age, environment and many other factors can shift microbial communities.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].keyTakeaways[1]`
  - `library/gut-health-101.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Dietary supplements are not approved by FDA for safety and effectiveness before sale.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[0].items[2]`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Different laboratories may use different samples, methods, indices and reporting systems.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “During or immediately after exercise, rapid carbohydrate may be useful when the workload is long or the turnaround is short.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].bodySections[2].blocks[1].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “EPA and DHA supplements can increase measured EPA and DHA status.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[1].items[0]`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Estimation of Risk and Inferring Causality in Epidemiology”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].sources[3].title`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Estimation of Risk and Inferring Causality in Epidemiology ↗”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `library/correlation-causation-relative-risk.html:70`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Evaluate supplements one ingredient, dose, purpose and risk at a time.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].evidenceLabels[3].items[2]`
  - `library/performance-nutrition-basics.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Even then, results from a narrow population may not transfer to everyone.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[2].blocks[1].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Everything I use and recommend, in one place.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.site.lede`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Examples include salmon, sardines, mackerel and herring.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[1].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Explore verified Zinzino and BioLimitless products by visitor intent, with current official US pricing and transparent partner links.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.site.metadata.pages.shop.description`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “FDA and EPA guidance is designed to preserve the nutritional value of fish while reducing exposure for groups who need extra caution.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[5].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “FDA and EPA provide more specific fish-choice and serving guidance for people who might become pregnant, are pregnant or breastfeeding, and for children.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[3].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “FDA permits a proprietary blend to list the total weight of the blend while listing its components in descending order by weight.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[3].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “FDA sources establish required label elements, permitted claim categories and the distinction between dietary ingredients and other ingredients.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceNotes[0]`
  - `library/how-to-read-a-supplement-label.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “FDA states that these qualified claims must include a disclaimer or other qualifying language that accurately describes the level of scientific evidence supporting them.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[5].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “FDA's good manufacturing practice requirements address identity, purity, strength, composition and contamination controls, but a consumer still may not be able to verify those attributes from packaging.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[5].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Find the comparison group, event counts, absolute difference, relative measure and confidence interval.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].optionalAction.copy`
  - `library/correlation-causation-relative-risk.html:71`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Fish intake and EPA or DHA supplementation can influence measured status.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Food and supplements can both be reasonable sources.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.statement`
  - `library/food-vs-omega-3-supplements.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Food-first patterns can provide EPA and DHA while also providing protein, vitamins, minerals and other nutrients.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[1].items[2]`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “For many generally healthy adults, the practical foundation is not exotic: eat a varied, adequate diet; include fiber-rich foods you tolerate; stay physically active; protect sleep; and use antibiotics only as prescribed.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[4].bodySections[3].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “How is the result calculated and reported?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[7].blocks[0].items[2]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “How the result compares with a laboratory's stated reference or interpretive framework.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].blocks[1].items[1]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “I want to know what a measurement can—and can’t—tell me.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.choosePath.paths[1].copy`
  - `index.html:876`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Identify the specimen, method, units, and calculation before interpreting a result.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[3].items[0]`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Identify what any certification actually tested and whether medical or medication context requires professional input.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[3].items[2]`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “If a serving is two capsules, every amount in the panel applies to those two capsules unless the label says otherwise.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “If testing still seems useful after understanding its limits, the Testing and Shelf sections collect the available pathways.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].optionalAction.copy`
  - `library/should-you-test-your-omega-3-levels.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “If those questions cannot be answered, more testing may add another number without adding useful clarity.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[7].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “If we recommend something, we tell you why.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.standards.principles[0].copy`
  - `index.html:1008`
  - `library.html:147`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Immediate intake can be convenient, but the idea that progress disappears if a shake is not consumed within a tiny window is too rigid.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[6].bodySections[2].blocks[0].text`
  - `library/recovery-after-training.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Include sodium and food when losses are substantial or recovery time is short.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[7].bodySections[3].blocks[1].items[2]`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Includes Master Microbiotics, which lists BPC-157; elevated owner-approved compliance review is required before public commercial treatment.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[43].complianceReview.reason`
  - `content/catalog.json:$.products[44].complianceReview.reason`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Includes Neuro Reboot, which lists Tesofensine, Dihexa and BPC-157; elevated owner-approved compliance review is required.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[46].complianceReview.reason`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Includes formulas listing 5-Amino-1-MQ, Tesofensine, Dihexa, BPC-157 and SLU-PP-332; elevated owner-approved compliance review is required.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[47].complianceReview.reason`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Independent testing can provide information about specific quality attributes when the certifier and scope are identifiable.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[1].items[1]`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Individual amounts for each component may not be shown.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[3].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Information without understanding can create more confusion.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.matrix.stages[1].copy`
  - `index.html:849`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “International consensus statement on microbiome testing in clinical practice”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].sources[3].title`
  - `content/library.json:$.articles[5].sources[0].title`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “International consensus statement on microbiome testing in clinical practice ↗”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `library/gut-health-101.html:70`
  - `library/gut-testing-biomarkers.html:70`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Inventoried as a manufacturer bundle; it includes Master Microbiotics and therefore inherits its compliance hold.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[43].whyItsHere`
  - `content/catalog.json:$.products[44].whyItsHere`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Inventoried as a manufacturer bundle; it includes deferred research-compound formulas.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[45].whyItsHere`
  - `content/catalog.json:$.products[46].whyItsHere`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Inventoried as the broad manufacturer bundle; it includes multiple deferred research-compound formulas.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/catalog.json:$.products[47].whyItsHere`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It can also create false confidence if the specimen, method, units, and limits are ignored.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It cannot identify the exact reason for the result without additional context.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].blocks[1].items[2]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It cannot make results from different specimens, methods, or laboratories automatically interchangeable.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].blocks[1].items[5]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It does not claim that fish-oil or algae-oil supplements prevent, diagnose or treat disease.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].limitations[2]`
  - `library/food-vs-omega-3-supplements.html:67`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It does not treat a third-party seal as proof of effectiveness.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].limitations[1]`
  - `library/how-to-read-a-supplement-label.html:67`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It is whether a specific measurement would answer a question that matters—and whether the result would change a decision.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It means FDA has not established a Daily Value for that dietary ingredient.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[2].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “It means beginning with the overall eating pattern and using food when it can reasonably meet the need.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[3].blocks[0].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Knowing that an ingredient appears in a blend is not the same as knowing whether the serving contains the amount used in a relevant study.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[3].bodySections[3].blocks[1].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Knowing what to actually do with that information can be difficult.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.problem.copy`
  - `index.html:830`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Learn how associations form, where confounding hides, and why absolute risk often changes the meaning of a dramatic relative number.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].summary`
  - `index.html:999`
  - `library.html:136`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Learn what they measure before deciding whether they're right for you.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].optionalAction.copy`
  - `library/omega-3-what-the-numbers-mean.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Look for the listed amounts per serving.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[2].blocks[2].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Measurement error: exposure or outcome is classified inaccurately.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[1].blocks[0].items[3]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Measure—but understand what you're measuring.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[4].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Multiple testing: many comparisons increase the chance of an apparently positive result.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[1].blocks[0].items[4]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “NIH notes that the optimal ratio—if one exists—has not been defined, and that a ratio can be too nonspecific because it can hide the actual amounts of individual fatty acids.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[4].blocks[1].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Observational associations can be distorted by confounding and bias.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].evidenceLabels[0].items[2]`
  - `library/correlation-causation-relative-risk.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Odds ratio: compares odds, not risks; it can look more dramatic when outcomes are common.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[2].blocks[2].items[2]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Official price source (opens in a new tab)”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `index.html:125`
  - `index.html:145`
  - `index.html:165`
  - `index.html:185`
  - `index.html:205`
  - `index.html:225`
  - `index.html:245`
  - `index.html:265`
  - `index.html:285`
  - `index.html:305`
  - `index.html:325`
  - `index.html:345`
  - `index.html:365`
  - `index.html:385`
  - `index.html:405`
  - `index.html:425`
  - `index.html:445`
  - `index.html:465`
  - `index.html:485`
  - `index.html:505`
  - `index.html:525`
  - `index.html:545`
  - `index.html:565`
  - `index.html:585`
  - `index.html:60`
  - `index.html:605`
  - `index.html:625`
  - `index.html:645`
  - `index.html:665`
  - `index.html:685`
  - `index.html:705`
  - `index.html:725`
  - `index.html:745`
  - `index.html:765`
  - `index.html:785`
  - `index.html:805`
  - `index.html:918`
  - `shop.html:100`
  - `shop.html:103`
  - `shop.html:106`
  - `shop.html:109`
  - `shop.html:112`
  - `shop.html:115`
  - `shop.html:118`
  - `shop.html:121`
  - `shop.html:124`
  - `shop.html:127`
  - `shop.html:130`
  - `shop.html:133`
  - `shop.html:136`
  - `shop.html:139`
  - `shop.html:142`
  - `shop.html:145`
  - `shop.html:148`
  - `shop.html:151`
  - `shop.html:154`
  - `shop.html:157`
  - `shop.html:160`
  - `shop.html:163`
  - `shop.html:166`
  - `shop.html:169`
  - `shop.html:172`
  - `shop.html:175`
  - `shop.html:178`
  - `shop.html:181`
  - `shop.html:184`
  - `shop.html:187`
  - `shop.html:190`
  - `shop.html:193`
  - `shop.html:196`
  - `shop.html:199`
  - `shop.html:202`
  - `shop.html:205`
  - `shop.html:208`
  - `shop.html:211`
  - `shop.html:214`
  - `shop.html:217`
  - `shop.html:220`
  - `shop.html:223`
  - `shop.html:226`
  - `shop.html:94`
  - `shop.html:97`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “On lighter days, normal meals may be enough.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].bodySections[2].blocks[1].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Open the verified Mindful Matrix BioLimitless partner destination.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/catalog.json:$.fallbackDestinations[4].description`
  - `shop.html:236`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Opinion of an international panel of experts on the clinical use of microbiome testing”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].sources[2].title`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Opinion of an international panel of experts on the clinical use of microbiome testing ↗”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `library/gut-testing-biomarkers.html:70`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Other ingredients such as capsule materials, binders, colors, sweeteners, flavors and preservatives appear in a separate ingredient list.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[2].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Persistent fatigue, disordered eating concerns, injury symptoms or heat illness require appropriate professional care.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[6].limitations[2]`
  - `library/recovery-after-training.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Planned carbohydrate and fluid strategies can improve performance in longer or repeated demanding sessions.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].evidenceLabels[1].items[1]`
  - `library/performance-nutrition-basics.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Plasma and serum fatty-acid values can vary substantially based on a person's most recent meal.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[1].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Plasma and serum values can vary substantially with a recent meal and are less representative of long-term intake.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[2].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Preprints, secondary analyses and adaptive trials can require additional questions not covered here.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].limitations[2]`
  - `library/how-to-read-a-health-study.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Preregistration and transparent protocols can reduce selective reporting.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].evidenceLabels[1].items[1]`
  - `library/how-to-read-a-health-study.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Prices, purchase options, and eligibility can change; the manufacturer checkout shows the current applicable price.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.site.pricingDisclosure`
  - `index.html:102`
  - `shop.html:86`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Product concentration, serving size and the combined intake from food and supplements all affect context.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[5].blocks[0].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Protein and carbohydrate timing can matter more when the next demanding session is soon.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[6].evidenceLabels[1].items[0]`
  - `library/recovery-after-training.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Protein supports repair and adaptation; carbohydrate availability supports many high-intensity and endurance demands.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].keyTakeaways[1]`
  - `library/performance-nutrition-basics.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Put the result back in context”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].relatedReadingHeading`
  - `library/gut-testing-biomarkers.html:71`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Questions & Answers from the FDA/EPA Advice about Eating Fish”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].sources[2].title`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Questions & Answers from the FDA/EPA Advice about Eating Fish ↗”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `library/food-vs-omega-3-supplements.html:68`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Record the result, specimen, method, units, date, and relevant intake context.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[6].blocks[0].items[0].definition`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Regular aggressive cooling immediately after resistance training, for example, may not be the same choice for maximizing adaptation as it is for restoring short-term comfort.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[6].bodySections[3].blocks[1].text`
  - `library/recovery-after-training.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Relative risk compares groups; absolute risk shows the size of the difference in context.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].keyTakeaways[2]`
  - `library/correlation-causation-relative-risk.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Relative risk needs an absolute baseline”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[2].heading`
  - `library/correlation-causation-relative-risk.html:62`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Repeated measurements may be useful only when the method and decision threshold are reliable.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[1].items[1]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Researchers can measure parts of that ecosystem, but no single list of organisms captures every function that matters.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Residual confounding: statistical adjustment cannot fully measure or remove every important difference.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[1].blocks[0].items[5]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Review the full serving, not only the highlighted ingredient.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[6].blocks[1].items[0]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Risk ratio: event risk in the exposed group divided by event risk in the comparison group.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[2].blocks[2].items[0]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Risk ratios compare event probability between groups.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].evidenceLabels[0].items[0]`
  - `library/correlation-causation-relative-risk.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Sample collection, transport, sequencing and analysis pipelines can change results.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].keyTakeaways[2]`
  - `library/gut-testing-biomarkers.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Selected clinician-ordered biomarkers can assist evaluation when used for an appropriate indication.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[1].items[0]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Serving size: the quantity used for the panel's declared amounts.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[1].items[0]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Servings per container: how many labeled servings the package contains.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[1].items[1]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Several sports-nutrition position papers include expert interpretation; they are not equivalent to a single randomized trial.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[6].evidenceNotes[0]`
  - `library/recovery-after-training.html:68`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “So before deciding what to change, start by understanding what can actually be measured.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[0].blocks[4].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Some interventions may trade one goal for another.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[6].bodySections[3].blocks[1].text`
  - `library/recovery-after-training.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Some modalities can reduce perceived soreness, but outcomes and tradeoffs differ.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[6].evidenceLabels[1].items[1]`
  - `library/recovery-after-training.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Spread meaningful protein servings across meals rather than relying on one large dose.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].bodySections[1].blocks[1].items[0]`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Start with a measurement you can inspect and discuss in context.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/catalog.json:$.intents[0].description`
  - `index.html:820`
  - `shop.html:92`
  - `templates/index.html:58`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Start with serving size and amount per serving.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[3].items[0]`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Start with the question, pattern, or measurement you actually have.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.startHere.stages[0].copy`
  - `start.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Start with what you can measure.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.testing.heading`
  - `index.html:909`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Still considering an omega-3 test?”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[1].optionalAction.heading`
  - `library/should-you-test-your-omega-3-levels.html:69`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Symptom questionnaire: reported experience, not a biological measurement.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].bodySections[1].blocks[2].items[2]`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Targeted clinical evaluation can be appropriate when symptoms, history and professional judgment point to a specific question.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].bodySections[4].blocks[0].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “That can be useful during tournaments or congested schedules.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[6].bodySections[3].blocks[0].text`
  - `library/recovery-after-training.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “That can make dose-based comparison difficult.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[3].blocks[1].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “That context is not a weakness of measurement.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[8].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “That is why a result that labels one organism ‘good’ or ‘bad’ without context should trigger questions, not instant action.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].blocks[1].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “That measurement can reduce some uncertainty.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “That outcome may be interesting, but it is not the same claim.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].bodySections[0].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “That turns a number into information you can use thoughtfully.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[10].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The appropriate interval depends on the specimen, the change being evaluated, and the purpose of testing.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[6].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The body can convert some ALA into EPA and then DHA, but NIH describes that conversion as very limited.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[1].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The body can convert some ALA into EPA and then DHA.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[1].blocks[2].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The compound or material that supplies the dietary ingredient, sometimes shown in parentheses.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[2].blocks[1].items[1].definition`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The condition, medication, diet, age or another factor may have produced the difference.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[2].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The current Dietary Guidelines for Americans includes seafood among nutrient-dense protein foods and emphasizes low-mercury omega-3-rich seafood during pregnancy.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[2].bodySections[3].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The gut microbiome includes bacteria, archaea, fungi, viruses and their collective genetic material.”
- Risk: `GREEN`
- Reason: Factual product attributes remain subject to source and version verification.
- Source/rule: `CE_GREEN_FACTUAL_COUNT`
- Recommended next action: `PASS_IF_SOURCE_VERIFIED`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The microbial difference may contribute, merely accompany the condition, or have no practical role at all.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[2].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The microbiome is worth understanding, but useful decisions still require symptoms, context, validated methods and humility about what a profile can prove.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].evidenceSummary.statement`
  - `library/gut-health-101.html:67`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The relative risk is doubled, but the absolute difference is one additional event per 1,000.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[2].blocks[0].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The same person can also show variation across samples.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].blocks[1].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The same two-fold relative risk represents an absolute difference of 100 per 1,000.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[2].blocks[1].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The total amount of oil in a capsule is not necessarily the amount of EPA plus DHA.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[2].blocks[2].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “The value of testing is not the number alone.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].evidenceSummary.statement`
  - `library/should-you-test-your-omega-3-levels.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Then list at least two alternative explanations before deciding what the result supports.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].optionalAction.copy`
  - `library/correlation-causation-relative-risk.html:71`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “These verified collection and partner routes remain available as fallbacks.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `shop.html:234`
  - `templates/shop.html:56`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “They can identify signals, generate hypotheses and reveal patterns that cannot be tested experimentally for ethical or practical reasons.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[0].blocks[1].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Treat post-training protein as one meal in the daily pattern, not a rescue for an inadequate diet.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].bodySections[1].blocks[1].items[2]`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Treat testing as information—not a verdict.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[7].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Treat the front of the bottle as advertising until its claims are checked.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[0].blocks[2].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Treat the ratio as one piece of a larger fatty-acid profile.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[4].blocks[5].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Treat ‘natural,’ ‘pharmaceutical grade’ and similar front-label phrases as claims to examine, not conclusions.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[5].blocks[2].items[2]`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Two data pathways diverging through confounders into relative and absolute risk frames”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].hero.alt`
  - `index.html:997`
  - `library.html:134`
  - `library/correlation-causation-relative-risk.html:58`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Two people can have different microbial communities and both be healthy.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].blocks[1].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Two reports can use similar language while measuring different specimens or calculating different outputs.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[1].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Two things can move together without one causing the other.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].dek`
  - `library/correlation-causation-relative-risk.html:58`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Understand what that measurement can—and cannot—tell you.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[7].blocks[1].items[1].definition`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Use FDA and EPA fish-choice guidance when mercury exposure requires extra attention.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].bodySections[3].blocks[2].items[1]`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for adverse-effect and interaction context and for the limited role of independent quality testing.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].sources[5].detail`
  - `library/how-to-read-a-supplement-label.html:68`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for bias, allocation, blinding, dropout, outcome measurement and systematic-review quality questions.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].sources[2].detail`
  - `library/how-to-read-a-health-study.html:70`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for confounding, temporality, selection and measurement-bias questions.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].sources[2].detail`
  - `library/correlation-causation-relative-risk.html:70`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for lower-mercury fish selection and the 2-to-3-servings guidance for people who might become pregnant, are pregnant or breastfeeding.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[2].sources[2].detail`
  - `library/food-vs-omega-3-supplements.html:68`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for risk measures and the complexity of causal inference in chronic-disease epidemiology.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].sources[3].detail`
  - `library/correlation-causation-relative-risk.html:70`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for serving size, declared amounts, Daily Values, other dietary ingredients and proprietary-blend disclosure rules.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].sources[1].detail`
  - `library/how-to-read-a-supplement-label.html:68`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for the original definition and proposed role of the erythrocyte EPA plus DHA index; its proposed risk thresholds are not presented as universal clinical targets in this guide.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].sources[1].detail`
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Used for the structured reading path through abstract, methods, results and discussion.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].sources[1].detail`
  - `library/how-to-read-a-health-study.html:70`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Using the same laboratory can reduce another source of variation, but results from different laboratories are not automatically unusable.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[6].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “We don't turn ‘may’ into ‘will.’”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[6].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What a label can establish — and what it cannot”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.heading`
  - `library/how-to-read-a-supplement-label.html:65`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What a result can tell you”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].heading`
  - `library/should-you-test-your-omega-3-levels.html:60`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What a result cannot tell you”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].heading`
  - `library/should-you-test-your-omega-3-levels.html:60`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What confounders were measured—and which important ones may remain?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[9].bodySections[4].blocks[0].items[2]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What happens if the result is high, low or inconclusive?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].bodySections[0].blocks[1].items[3]`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What is one serving, and how many units does it contain?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[7].blocks[0].items[0]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What question was I trying to answer by testing?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[7].blocks[0].items[0]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “What was measured, how stable is that measurement, and has the result been linked to a decision that improves outcomes?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].blocks[2].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “When testing may be worth discussing”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[5].bodySections[4].heading`
  - `library/gut-testing-biomarkers.html:62`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Whether a comparable follow-up result moved up, down, or remained similar.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].blocks[1].items[2]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Which dietary ingredients are listed, in what forms, and at what amounts per serving?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[7].blocks[0].items[1]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Without a clear purpose, a stack mostly adds cost, complexity and interaction risk.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[7].bodySections[4].blocks[0].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “Would a change in the result actually alter a reasonable decision?”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[1].bodySections[7].blocks[0].items[5]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “You can learn more or do nothing yet.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/site.json:$.homepage.startHere.pathways.items[3].copy`
  - `start.html:84`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “label elements and regulatory distinctions are documented by FDA.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[0].meaning`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — FACTUAL_PRODUCT_FACT

- Exact text: “‘Daily Value not established’ does not mean an ingredient is ineffective or unsafe.”
- Risk: `GREEN`
- Reason: Likely factual claim; verify the underlying source and current scope.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_SOURCE`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[2].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$112”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:365`
  - `shop.html:139`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$116”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:305`
  - `index.html:645`
  - `shop.html:130`
  - `shop.html:226`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$127”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:125`
  - `index.html:145`
  - `index.html:60`
  - `index.html:918`
  - `shop.html:94`
  - `shop.html:97`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$133”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `shop.html:121`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$145”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:165`
  - `shop.html:100`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$159.60/mo”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:805`
  - `shop.html:196`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$16”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `shop.html:142`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$168”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:805`
  - `shop.html:196`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$17”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:605`
  - `shop.html:217`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$179”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:145`
  - `shop.html:97`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$18”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:245`
  - `index.html:465`
  - `shop.html:118`
  - `shop.html:163`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$205”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:165`
  - `shop.html:100`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$209”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `shop.html:103`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$24”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:605`
  - `shop.html:217`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$26”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:245`
  - `index.html:465`
  - `shop.html:118`
  - `shop.html:163`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$31”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:545`
  - `shop.html:175`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$32”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:445`
  - `shop.html:157`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$35”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:385`
  - `index.html:505`
  - `shop.html:145`
  - `shop.html:169`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$39.90/mo”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:725`
  - `index.html:745`
  - `index.html:765`
  - `index.html:785`
  - `shop.html:151`
  - `shop.html:187`
  - `shop.html:190`
  - `shop.html:193`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$410”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `shop.html:103`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$42”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:725`
  - `index.html:745`
  - `index.html:765`
  - `index.html:785`
  - `shop.html:151`
  - `shop.html:187`
  - `shop.html:190`
  - `shop.html:193`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$44”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:545`
  - `shop.html:175`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$45”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:445`
  - `shop.html:157`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$46”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:485`
  - `shop.html:166`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$47”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:225`
  - `index.html:325`
  - `index.html:345`
  - `index.html:525`
  - `shop.html:115`
  - `shop.html:133`
  - `shop.html:136`
  - `shop.html:172`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$47/mo”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:125`
  - `index.html:60`
  - `index.html:918`
  - `shop.html:94`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$50”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:385`
  - `index.html:505`
  - `index.html:565`
  - `shop.html:145`
  - `shop.html:169`
  - `shop.html:199`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$52.25/mo”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:705`
  - `shop.html:184`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$54”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:285`
  - `shop.html:127`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$55”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:185`
  - `index.html:205`
  - `index.html:705`
  - `shop.html:106`
  - `shop.html:109`
  - `shop.html:184`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$56”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `shop.html:160`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$58”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:585`
  - `index.html:645`
  - `shop.html:202`
  - `shop.html:205`
  - `shop.html:208`
  - `shop.html:211`
  - `shop.html:226`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$60”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:405`
  - `shop.html:148`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$61”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:425`
  - `index.html:625`
  - `shop.html:154`
  - `shop.html:223`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$65”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:485`
  - `shop.html:166`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$66”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:265`
  - `shop.html:124`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$67”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:225`
  - `index.html:325`
  - `index.html:345`
  - `index.html:525`
  - `shop.html:115`
  - `shop.html:133`
  - `shop.html:136`
  - `shop.html:172`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$71”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:565`
  - `shop.html:199`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$77”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:285`
  - `shop.html:127`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$78”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:185`
  - `index.html:205`
  - `shop.html:106`
  - `shop.html:109`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$79”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:365`
  - `shop.html:139`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$80.75/mo”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:685`
  - `shop.html:181`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$82”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:305`
  - `index.html:585`
  - `shop.html:130`
  - `shop.html:202`
  - `shop.html:205`
  - `shop.html:208`
  - `shop.html:211`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$85”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:405`
  - `index.html:685`
  - `shop.html:148`
  - `shop.html:181`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$86”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `shop.html:160`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$87”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:425`
  - `index.html:625`
  - `shop.html:154`
  - `shop.html:223`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$9.99–$29.33”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `shop.html:178`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$900”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:665`
  - `shop.html:112`

### LOW_RISK — PRICE_CLAIM

- Exact text: “$94”
- Risk: `GREEN`
- Reason: The validator separately enforces currency, price type, source URL, and verification date.
- Source/rule: `CE_GREEN_PRICE_FORMAT`
- Recommended next action: `PASS_IF_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:265`
  - `shop.html:121`
  - `shop.html:124`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Additional Premier Kits beyond SKU 910465”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/catalog.json:$.deferredCatalog[0].scope`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Browse current omega Premier Kit options on Zinzino.”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/catalog.json:$.fallbackDestinations[1].description`
  - `shop.html:236`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Cross-sectional study: one-time snapshot; cannot reliably establish which came first.”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/library.json:$.articles[8].bodySections[1].blocks[0].items[3]`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Monthly subscription”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/catalog.json:$.products[0].price.recurring_label`
  - `index.html:125`
  - `index.html:60`
  - `index.html:918`
  - `shop.html:94`

### LOW_RISK — PRICE_CLAIM

- Exact text: “One-time or monthly subscription”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/catalog.json:$.products[36].purchaseModel`
  - `content/catalog.json:$.products[39].purchaseModel`
  - `content/catalog.json:$.products[40].purchaseModel`
  - `content/catalog.json:$.products[41].purchaseModel`
  - `content/catalog.json:$.products[42].purchaseModel`
  - `content/catalog.json:$.products[43].purchaseModel`
  - `content/catalog.json:$.products[44].purchaseModel`
  - `content/catalog.json:$.products[45].purchaseModel`
  - `content/catalog.json:$.products[46].purchaseModel`
  - `content/catalog.json:$.products[47].purchaseModel`
  - `content/catalog.json:$.products[48].purchaseModel`
  - `content/catalog.json:$.products[49].purchaseModel`
  - `content/catalog.json:$.products[50].purchaseModel`
  - `content/catalog.json:$.products[51].purchaseModel`
  - `content/catalog.json:$.products[52].purchaseModel`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Premier price”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:145`
  - `index.html:165`
  - `index.html:185`
  - `index.html:205`
  - `index.html:225`
  - `index.html:245`
  - `index.html:265`
  - `index.html:285`
  - `index.html:305`
  - `index.html:325`
  - `index.html:345`
  - `index.html:365`
  - `index.html:385`
  - `index.html:405`
  - `index.html:425`
  - `index.html:445`
  - `index.html:465`
  - `index.html:485`
  - `index.html:505`
  - `index.html:525`
  - `index.html:545`
  - `index.html:565`
  - `index.html:585`
  - `index.html:605`
  - `index.html:625`
  - `index.html:645`
  - `shop.html:100`
  - `shop.html:103`
  - `shop.html:106`
  - `shop.html:109`
  - `shop.html:115`
  - `shop.html:118`
  - `shop.html:121`
  - `shop.html:124`
  - `shop.html:127`
  - `shop.html:130`
  - `shop.html:133`
  - `shop.html:136`
  - `shop.html:139`
  - `shop.html:145`
  - `shop.html:148`
  - `shop.html:154`
  - `shop.html:157`
  - `shop.html:160`
  - `shop.html:163`
  - `shop.html:166`
  - `shop.html:169`
  - `shop.html:172`
  - `shop.html:175`
  - `shop.html:199`
  - `shop.html:202`
  - `shop.html:205`
  - `shop.html:208`
  - `shop.html:211`
  - `shop.html:217`
  - `shop.html:220`
  - `shop.html:223`
  - `shop.html:226`
  - `shop.html:97`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Premier pricing may require an eligible Premier purchase or customer status.”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/site.json:$.site.premierPricingNote`
  - `index.html:145`
  - `index.html:165`
  - `index.html:185`
  - `index.html:205`
  - `index.html:225`
  - `index.html:245`
  - `index.html:265`
  - `index.html:285`
  - `index.html:305`
  - `index.html:325`
  - `index.html:345`
  - `index.html:365`
  - `index.html:385`
  - `index.html:405`
  - `index.html:425`
  - `index.html:445`
  - `index.html:465`
  - `index.html:485`
  - `index.html:505`
  - `index.html:525`
  - `index.html:545`
  - `index.html:565`
  - `index.html:585`
  - `index.html:605`
  - `index.html:625`
  - `index.html:645`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Premier subscription kit”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/catalog.json:$.products[0].purchaseModel`

### LOW_RISK — PRICE_CLAIM

- Exact text: “Purchases are completed on Zinzino's own site at their listed retail price.”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `content/site.json:$.site.disclosure`
  - `index.html:1017`
  - `index.html:1029`
  - `library.html:159`
  - `library/correlation-causation-relative-risk.html:81`
  - `library/food-vs-omega-3-supplements.html:79`
  - `library/gut-health-101.html:81`
  - `library/gut-testing-biomarkers.html:81`
  - `library/how-to-read-a-health-study.html:81`
  - `library/how-to-read-a-supplement-label.html:79`
  - `library/omega-3-what-the-numbers-mean.html:79`
  - `library/performance-nutrition-basics.html:81`
  - `library/recovery-after-training.html:81`
  - `library/should-you-test-your-omega-3-levels.html:79`
  - `shop.html:243`
  - `shop.html:253`
  - `start.html:94`

### LOW_RISK — PRICE_CLAIM

- Exact text: “retail”
- Risk: `GREEN`
- Reason: Price-like language requires current manufacturer source and verification metadata.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE`
- Locations:
  - `index.html:145`
  - `index.html:165`
  - `index.html:185`
  - `index.html:205`
  - `index.html:225`
  - `index.html:245`
  - `index.html:265`
  - `index.html:285`
  - `index.html:305`
  - `index.html:325`
  - `index.html:345`
  - `index.html:365`
  - `index.html:385`
  - `index.html:405`
  - `index.html:425`
  - `index.html:445`
  - `index.html:465`
  - `index.html:485`
  - `index.html:505`
  - `index.html:525`
  - `index.html:545`
  - `index.html:565`
  - `index.html:585`
  - `index.html:605`
  - `index.html:625`
  - `index.html:645`
  - `shop.html:100`
  - `shop.html:103`
  - `shop.html:106`
  - `shop.html:109`
  - `shop.html:115`
  - `shop.html:118`
  - `shop.html:121`
  - `shop.html:124`
  - `shop.html:127`
  - `shop.html:130`
  - `shop.html:133`
  - `shop.html:136`
  - `shop.html:139`
  - `shop.html:142`
  - `shop.html:145`
  - `shop.html:148`
  - `shop.html:154`
  - `shop.html:157`
  - `shop.html:160`
  - `shop.html:163`
  - `shop.html:166`
  - `shop.html:169`
  - `shop.html:172`
  - `shop.html:175`
  - `shop.html:199`
  - `shop.html:202`
  - `shop.html:205`
  - `shop.html:208`
  - `shop.html:211`
  - `shop.html:214`
  - `shop.html:217`
  - `shop.html:220`
  - `shop.html:223`
  - `shop.html:226`
  - `shop.html:97`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A Supplement Facts panel identifies serving size, dietary ingredients and declared amounts per serving.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[0].items[0]`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A biomarker is useful only in relation to a defined question and validated interpretation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].keyTakeaways[0]`
  - `library/gut-testing-biomarkers.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A biomarker may be associated with an exposure or an outcome in research without functioning as a standalone diagnosis or treatment instruction for an individual.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A blood test answers a different question: what selected fatty acids were present in a particular blood sample when it was analyzed?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A blood test can replace some guessing with a measurement.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].dek`
  - `library/should-you-test-your-omega-3-levels.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A broad wellness profile should not be read as a diagnosis.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[1].blocks[1].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A clinician may order targeted tests for a pathogen, blood loss, inflammation, malabsorption or another specific concern.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[1].blocks[0].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A commercial test report and this guide are not substitutes for individualized medical interpretation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[8].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A comparable repeat measurement can show whether the measured biomarker changed over time.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[1].items[1]`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A dried blood spot is a collection format; the laboratory method and calculation still determine what the report represents.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[1].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A drink or supplement cannot compensate for a schedule that repeatedly removes sleep, enough food or appropriate training variation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].bodySections[1].blocks[1].text`
  - `library/recovery-after-training.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A fatty-acid blood test can help you understand aspects of your current fatty-acid profile.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[8].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A gut-related test can measure something real and still fail to answer the question you care about.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].dek`
  - `library/gut-testing-biomarkers.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A headline may say a food ‘improves health’ while the study measured one laboratory marker for four weeks.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[0].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A large Cochrane review found that increasing long-chain omega-3 intake had little or no effect on several broad cardiovascular outcomes, with modest effects for some outcomes and reduced triglycerides.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[4].blocks[2].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A living ecosystem, not a personality test”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].heading`
  - `library/gut-health-101.html:62`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A practical evidence-aware guide to performance nutrition fundamentals before supplements.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A practical evidence-based guide to Supplement Facts, serving size, ingredient amounts, proprietary blends, health claims, disclaimers and quality signals.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A practical hierarchy for sleep, food, fluid, training load and recovery tools—without pretending every workout needs a product.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].summary`
  - `library.html:115`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A practical map of the gut microbiome, the factors that shape it, and the line between useful evidence and confident-sounding speculation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].summary`
  - `library.html:101`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A qualified clinician can consider the result alongside symptoms, diagnoses, medications, dietary pattern, other laboratory findings, and the reason the test was ordered.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[8].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A reasonable next step that follows from the evidence without turning uncertainty into a promise.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[3].meaning`
  - `content/library.json:$.articles[5].evidenceLabels[3].meaning`
  - `content/library.json:$.articles[6].evidenceLabels[3].meaning`
  - `content/library.json:$.articles[7].evidenceLabels[3].meaning`
  - `content/library.json:$.articles[8].evidenceLabels[3].meaning`
  - `content/library.json:$.articles[9].evidenceLabels[3].meaning`
  - `library/correlation-causation-relative-risk.html:65`
  - `library/gut-health-101.html:65`
  - `library/gut-testing-biomarkers.html:65`
  - `library/how-to-read-a-health-study.html:65`
  - `library/performance-nutrition-basics.html:65`
  - `library/recovery-after-training.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A reasonable practical next step supported by the preceding evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceLabels[3].meaning`
  - `library/omega-3-what-the-numbers-mean.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A repeat result can show that the biomarker changed.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A repeatable way to inspect the question, design, population, outcome, effect size, uncertainty and conflicts behind a health headline.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].summary`
  - `library.html:129`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A report that moves directly from one microbial pattern to a long supplement protocol without showing validated clinical utility is making a larger claim than the measurement alone can support.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[3].blocks[1].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A restrained next step supported by the preceding evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[3].meaning`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A serving of salmon, a spoonful of ground flax, and a fish- or algae-oil capsule can all be called omega-3 sources.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[0].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A single universal hierarchy that makes every randomized trial better than every observational study.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].evidenceLabels[2].items[0]`
  - `library/how-to-read-a-health-study.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A study can be real, peer-reviewed and statistically significant—and still fail to support the headline built around it.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].dek`
  - `library/how-to-read-a-health-study.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A study on an ingredient does not automatically validate every product containing that ingredient.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[4].blocks[2].items[1]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A supplement can be a practical option when a person does not eat fish, has limited access to suitable seafood, prefers an algae-derived source, or has a specific intake goal discussed with an appropriate healthcare professional.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[4].blocks[0].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A supplement label can tell you what the company declares is in a serving.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].dek`
  - `library/how-to-read-a-supplement-label.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A supplement should answer a specific question: Is there a diagnosed deficiency?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[4].blocks[0].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A sustainable plan may use portions and performance trends, while higher-level sport can warrant support from a qualified sports dietitian.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[0].blocks[1].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A test becomes useful when it measures the right target accurately enough, has a valid reference or decision framework, and can change a reasonable next step.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[0].blocks[0].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “A test can narrow uncertainty about a biomarker.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “AA/EPA is not a standalone diagnosis, and one result should not become a sweeping conclusion about someone's health.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[5].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Adequate total energy and a sustainable eating pattern come before optimization.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].keyTakeaways[0]`
  - `library/performance-nutrition-basics.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Algae-derived products can provide a non-fish source; the amounts of EPA and DHA vary by product, so the Supplement Facts panel matters more than a front-label phrase such as ‘omega-3.’”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[2].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “American College of Sports Medicine, Academy of Nutrition and Dietetics, Dietitians of Canada”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].sources[1].organization`
  - `content/library.json:$.articles[7].sources[0].organization`
  - `library/performance-nutrition-basics.html:70`
  - `library/recovery-after-training.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “An Evidence-Based Approach for Choosing Post-exercise Recovery Techniques”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].sources[3].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “An Evidence-Based Approach for Choosing Post-exercise Recovery Techniques ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/recovery-after-training.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “An interlaboratory study of dried blood spots found that standardizing reporting reduced variability between laboratories.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[5].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “An omega-3 blood result is one biomarker.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “An optional manufacturer-authored education title, kept distinct from independent Mindful Matrix evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[38].whyItsHere`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “And none of them, by themselves, provide a complete picture of your health.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[0].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Another controlled analysis found substantial individual variability across erythrocyte, plasma, and whole-blood measurements.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Antibiotics and dietary patterns can alter gut microbial communities.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[0].items[2]`
  - `library/gut-health-101.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Antibiotics can produce large shifts, although recovery patterns differ.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[1].blocks[1].items[0]`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Ask what was tested, by whom, against what standard, and whether the evidence concerns the finished product or only one ingredient.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[5].blocks[2].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Ask what you need to be ready for, how soon, and which resource—sleep, energy, fluid, carbohydrate, protein or reduced load—is most likely limiting.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].bodySections[0].blocks[1].text`
  - `library/recovery-after-training.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Assessing the Quality of Individual Studies in Systematic Reviews of Health Care Interventions”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].sources[3].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Assessing the Quality of Individual Studies in Systematic Reviews of Health Care Interventions ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/how-to-read-a-health-study.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Associations between microbes and health are common; direct cause-and-effect conclusions are much harder.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].keyTakeaways[2]`
  - `library/gut-health-101.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “At-home blood sample card moving through a precise omega measurement interface”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].hero.alt`
  - `library.html:92`
  - `library/should-you-test-your-omega-3-levels.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Athletic energy pathways connecting whole-food fuel, hydration and muscle signals”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].hero.alt`
  - `library.html:120`
  - `library/performance-nutrition-basics.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Blood biomarkers can provide information about EPA and DHA status or exposure.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[1].items[0]`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Blood in stool, unexplained weight loss, persistent vomiting, severe pain, fever, dehydration, or a major change in bowel habits deserves clinical attention—not a wellness score.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[3].blocks[2].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Blood is not one uniform measurement space.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[1].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Blood marker: systemic information that may be relevant but is rarely specific to the gut by itself.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[1].blocks[2].items[3]`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Browse practical guides that show sources, evidence, and uncertainty.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/site.json:$.homepage.startHere.pathways.items[0].copy`
  - `start.html:75`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “But a biomarker is not automatically a diagnosis.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[3].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Carbohydrate supports blood glucose and muscle glycogen.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[2].blocks[0].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Case-control study: starts with an outcome and looks backward; efficient for rare outcomes, sensitive to selection and recall bias.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[1].blocks[0].items[2]`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Causal confidence grows from converging evidence, not one impressive number.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].keyTakeaways[3]`
  - `library/correlation-causation-relative-risk.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Change confidence in proportion to the evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[4].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Check limitations, funding, registration and the wider evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].evidenceLabels[3].items[2]`
  - `library/how-to-read-a-health-study.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Chronic under-fueling can appear as declining performance, persistent fatigue, impaired recovery, menstrual disturbance, recurrent injury or other health effects.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[0].blocks[0].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Clinical conditions, pregnancy, eating disorders and medication use can change nutrition decisions.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].limitations[1]`
  - `library/performance-nutrition-basics.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Clinical stool and blood tests are not interchangeable with direct-to-consumer microbiome profiles.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].keyTakeaways[1]`
  - `library/gut-testing-biomarkers.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Cohort study: follows exposures and outcomes over time; useful for association and risk patterns, still vulnerable to confounding.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[1].blocks[0].items[1]`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Compare food and omega-3 supplements, including ALA conversion, fatty fish, EPA and DHA sources, biomarker response, safety, and food-first next steps.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Consider discussing the result with an appropriate healthcare professional when it could affect medical care or a meaningful treatment or supplement decision—especially in the context of pregnancy, a medical condition, or prescribed treatment.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[8].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Consumer testing may still satisfy curiosity or support learning, but the user should understand that educational interest and medical utility are different standards.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[4].blocks[0].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Continue with the foundation guide to see how ALA, EPA, DHA and common blood measurements fit together.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].relatedReadingIntro`
  - `library/food-vs-omega-3-supplements.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Cross-company comparison of diversity or wellness scores.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[2].items[2]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Departments of Agriculture and Health and Human Services”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].sources[1].organization`
  - `library/food-vs-omega-3-supplements.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Diet is one influence, but so are geography, age, recent illness, medications, sanitation, sleep, activity, host genetics and ordinary day-to-day variation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[1].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Diet records and supplement labels can estimate omega-3 intake.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Dietary Supplement Labeling Guide: Chapter IV.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].sources[1].title`
  - `library/how-to-read-a-supplement-label.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Dietary Supplement Labeling Guide: Chapter V.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].sources[2].title`
  - `library/how-to-read-a-supplement-label.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Dietary ingredients appear in Supplement Facts.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[2].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Different tests measure different targets: organisms, genes, inflammation, digestion, immune response or other processes.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[0].items[0]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Discuss a supplement with an appropriate healthcare professional when it could affect treatment or meaningful medical decisions.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[6].blocks[1].items[3]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Discuss substantial supplement changes when pregnancy, breastfeeding, surgery, bleeding risk, medication use or medical care is involved.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[5].blocks[2].items[1]`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Do not ask whether the study is ‘good’ in the abstract.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[1].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Do not assume a green score proves health or a red score proves disease.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[3].blocks[0].items[5]`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Do not let one exciting abstract rewrite an entire health plan.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[4].blocks[1].text`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Do not treat wearable recovery scores as diagnoses.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].bodySections[3].blocks[2].items[1]`
  - `library/recovery-after-training.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “EPA and DHA Omega-3 Consumption and the Risk of Hypertension and Coronary Heart Disease”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].sources[2].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “EPA and DHA Omega-3 Consumption and the Risk of Hypertension and Coronary Heart Disease ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/omega-3-what-the-numbers-mean.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “EPA and DHA supplements may increase omega-3 intake, but more isn't automatically better, and supplements should not be treated as universal disease-prevention products.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[4].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “EPA plus DHA in red-blood-cell membranes, expressed as a percentage—not a disease score.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[2].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “EPA plus DHA in your red blood cells, expressed as a percentage.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[3].blocks[1].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Education — When a supplement may fit”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[4].heading`
  - `library/food-vs-omega-3-supplements.html:60`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Energy needs change with body size, training volume, goals and season.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[0].blocks[1].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Energy: chronic under-fueling can undermine performance and recovery.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].bodySections[1].blocks[0].items[2]`
  - `library/recovery-after-training.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Establish regular meals, adequate energy and a training-matched plan.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].evidenceLabels[3].items[0]`
  - `library/performance-nutrition-basics.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evaluating the analytical performance of direct-to-consumer gut microbiome testing services”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].sources[1].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evaluating the analytical performance of direct-to-consumer gut microbiome testing services ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/gut-testing-biomarkers.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evidence for one ingredient does not automatically validate every blend.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].optionalAction.copy`
  - `library/performance-nutrition-basics.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evidence from one population or sample type may not generalize to another.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].limitations[2]`
  - `library/gut-health-101.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evidence is incomplete, inconsistent, or not ready for universal interpretation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[2].meaning`
  - `content/library.json:$.articles[5].evidenceLabels[2].meaning`
  - `content/library.json:$.articles[6].evidenceLabels[2].meaning`
  - `content/library.json:$.articles[7].evidenceLabels[2].meaning`
  - `content/library.json:$.articles[8].evidenceLabels[2].meaning`
  - `content/library.json:$.articles[9].evidenceLabels[2].meaning`
  - `library/correlation-causation-relative-risk.html:65`
  - `library/gut-health-101.html:65`
  - `library/gut-testing-biomarkers.html:65`
  - `library/how-to-read-a-health-study.html:65`
  - `library/performance-nutrition-basics.html:65`
  - `library/recovery-after-training.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evidence supports the direction, while the size and relevance of the response depend on context.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[1].meaning`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evidence supports the idea, but effect size and application depend on context.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[1].meaning`
  - `content/library.json:$.articles[5].evidenceLabels[1].meaning`
  - `content/library.json:$.articles[6].evidenceLabels[1].meaning`
  - `content/library.json:$.articles[7].evidenceLabels[1].meaning`
  - `content/library.json:$.articles[8].evidenceLabels[1].meaning`
  - `content/library.json:$.articles[9].evidenceLabels[1].meaning`
  - `library/correlation-causation-relative-risk.html:65`
  - `library/gut-health-101.html:65`
  - `library/gut-testing-biomarkers.html:65`
  - `library/how-to-read-a-health-study.html:65`
  - `library/performance-nutrition-basics.html:65`
  - `library/recovery-after-training.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evidence supports the idea, but interpretation depends on context.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceLabels[1].meaning`
  - `library/omega-3-what-the-numbers-mean.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Evidence supports the use, but interpretation depends on context and method.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[1].meaning`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “FDA allows certain nutrient-content, health, and structure/function claims under different rules.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[4].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “FTC guidance is used to evaluate whether the express and implied message of a health claim is adequately supported.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].evidenceNotes[2]`
  - `library/how-to-read-a-supplement-label.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “FTC guidance says objective health claims should be truthful, not misleading and supported by competent and reliable scientific evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[4].blocks[1].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Fix chronic sleep, fueling or load problems before adding a specialized tool.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].evidenceLabels[3].items[1]`
  - `library/recovery-after-training.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Fluid, carbohydrate, protein and sleep contribute to restoration through different mechanisms.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].evidenceLabels[0].items[1]`
  - `library/recovery-after-training.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Food and supplements can both provide omega-3 fats, but they are not interchangeable shortcuts.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].dek`
  - `library/food-vs-omega-3-supplements.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Food provides energy, amino acids, carbohydrate, fat, micronutrients and fluid needed for training and health.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].evidenceLabels[0].items[0]`
  - `library/performance-nutrition-basics.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “For certain qualified health claims about combined EPA and DHA consumption and the risk of hypertension and coronary heart disease, FDA determined that the evidence met the “credible evidence” standard for a qualified health claim but did not meet the “significant scientific agreement” standard required for an authorized health claim.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[5].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “For exposures that cannot be randomized, causal reasoning draws on temporality, replication, magnitude, dose-response, negative controls, natural experiments, mechanistic evidence and methods designed to reduce confounding.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].bodySections[3].blocks[1].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “For the broader foundation, begin with what omega-3 is, what can be measured, and how common numbers differ.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].relatedReadingIntro`
  - `library/should-you-test-your-omega-3-levels.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Good interpretation keeps the denominator, the alternative explanations and the study design visible at the same time.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].evidenceSummary.statement`
  - `library/correlation-causation-relative-risk.html:67`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Greater dietary variety and fiber-rich plant foods can support microbial functions in many people.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[1].items[0]`
  - `library/gut-health-101.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Gut Health 101: The Microbiome—and What We Actually Know”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].title`
  - `library.html:101`
  - `library/gut-health-101.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Gut Health 101: The Microbiome—and What We Actually Know →”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/gut-testing-biomarkers.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Gut Health 101: What We Actually Know | The Mindful Matrix”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].seoTitle`
  - `library/gut-health-101.html:6`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Gut Testing: What Biomarkers Can and Can’t Tell You | The Mindful Matrix”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].seoTitle`
  - `library/gut-testing-biomarkers.html:6`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Gut Testing: What Biomarkers Can—and Can’t—Tell You”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].title`
  - `library.html:108`
  - `library/gut-testing-biomarkers.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Gut Testing: What Biomarkers Can—and Can’t—Tell You →”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/correlation-causation-relative-risk.html:71`
  - `library/gut-health-101.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “High Variability in Erythrocyte, Plasma and Whole Blood EPA and DHA Levels in Response to Supplementation”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].sources[5].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “High Variability in Erythrocyte, Plasma and Whole Blood EPA and DHA Levels in Response to Supplementation ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Higher protein intake than the general adult minimum can support many training programs.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].evidenceLabels[1].items[0]`
  - `library/performance-nutrition-basics.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How one result should translate into clinical decisions or predicted health outcomes.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[2].items[2]`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How the result is expressed—for example, as a percentage of total fatty acids in the selected blood fraction.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[1].blocks[2].items[2].definition`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How to Read a Health Study Without Getting Fooled”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].title`
  - `library.html:129`
  - `library/how-to-read-a-health-study.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How to Read a Health Study Without Getting Fooled | The Mindful Matrix”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].seoTitle`
  - `library/how-to-read-a-health-study.html:6`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How to Read a Health Study Without Getting Fooled →”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/correlation-causation-relative-risk.html:71`
  - `library/gut-testing-biomarkers.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How to Read a Supplement Label Without Overreading It”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].title`
  - `library.html:73`
  - `library/how-to-read-a-supplement-label.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How to Read a Supplement Label Without Overreading It →”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/food-vs-omega-3-supplements.html:69`
  - `library/gut-health-101.html:71`
  - `library/how-to-read-a-health-study.html:71`
  - `library/performance-nutrition-basics.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “How to Read a Supplement Label | The Mindful Matrix”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].seoTitle`
  - `library/how-to-read-a-supplement-label.html:6`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If considering a supplement, compare EPA and DHA per serving, serving size, other ingredients and relevant cautions.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[6].blocks[0].items[3]`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If considering a supplement, compare the listed EPA and DHA per serving and discuss meaningful changes when medical context matters.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[3].items[2]`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If no possible result would change a sensible action, the test may add data without adding value.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[0].blocks[2].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If supplement users have better outcomes, the supplement may help—or users may also differ in income, diet, health behavior, access to care, baseline risk or reasons for taking it.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].bodySections[1].blocks[1].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If symptoms are persistent, severe, associated with bleeding, fever, dehydration, weight loss or significant pain, skip the wellness interpretation and seek appropriate care.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[4].blocks[1].text`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If testing is one of your questions, this companion guide explains what a blood result can—and can’t—tell you.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].relatedReadingIntro`
  - `library/omega-3-what-the-numbers-mean.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If the amount of a key ingredient is not disclosed, be careful about matching the product to research that used a defined dose.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[3].blocks[2].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If you are comparing gut tools”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].optionalAction.heading`
  - `library/gut-health-101.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If you have identified a clear format or fueling need, compare the available tools without treating them as a substitute for sleep, food or training design.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].optionalAction.copy`
  - `library/recovery-after-training.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “If you test, the useful question isn't simply whether a number is good or bad.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[8].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “In one randomized dose-response study, baseline Omega-3 Index, EPA and DHA dose relative to body weight, age, sex, and physical activity helped explain differences in response.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Individual conditions, immune status and medications can change the risk-benefit discussion.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[3].blocks[1].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Instead of estimating omega-3 intake from diet alone, laboratories can measure fatty acids in biological samples.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[0].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Interlaboratory Assessment of Dried Blood Spot Fatty Acid Compositions”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].sources[6].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Interlaboratory Assessment of Dried Blood Spot Fatty Acid Compositions ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “International Society of Sports Nutrition Position Stand: protein and exercise”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].sources[1].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “International Society of Sports Nutrition Position Stand: protein and exercise ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/performance-nutrition-basics.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Intervention studies also show that these biomarkers can change after intake changes, although the size of the response varies between people.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Inventoried for catalog completeness; its research-compound ingredients require elevated compliance review.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[41].whyItsHere`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Inventoried for catalog completeness; multiple research-compound ingredients require elevated compliance review.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/catalog.json:$.products[40].whyItsHere`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Is the comparison range a laboratory reference, a research proposal, or a clinical guideline?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[7].blocks[0].items[3]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It cannot guarantee that a particular dietary or supplement change will produce a specific result.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].blocks[1].items[3]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It cannot prove that changing the biomarker will produce a particular health outcome.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].blocks[1].items[4]`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It cannot remove every uncertainty about health.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It cannot replace evidence, product-specific quality verification or appropriate medical context.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].evidenceSummary.statement`
  - `library/how-to-read-a-supplement-label.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It does not automatically explain why that relationship exists—or what it means for your health.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[4].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It does not prove that every dose or product produces a particular health outcome.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[4].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It does not rank commercial products or endorse a universal blood target.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].limitations[3]`
  - `library/food-vs-omega-3-supplements.html:67`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It does not, by itself, show that overall health improved.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It is not a rule that everyone must test, change something, or retest.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[6].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It is not a verdict on effectiveness, safety for a particular person, manufacturing quality beyond what is verified, or whether a marketing claim matches the total evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[0].blocks[1].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It is part of using a biomarker responsibly.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[8].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It is studied as a biomarker or index.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[5].blocks[1].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It is which omega-3 fatty acid a source provides, what amount reaches the diet, and what decision that information is meant to support.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[0].blocks[0].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It means the test can provide another piece of information.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[2].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “It should not be expanded into conclusions the test did not measure.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[4].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Knowing where the evidence ends is part of being informed.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceSummary.statement`
  - `library/omega-3-what-the-numbers-mean.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Laboratories can analyze fatty acids in plasma, serum, plasma phospholipids, erythrocytes, or whole blood.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[1].blocks[0].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Laboratory sample channel, biomarker bands and microbial signals in a dark diagnostic interface”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].hero.alt`
  - `library.html:106`
  - `library/gut-testing-biomarkers.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Layered research paper, study groups and evidence signals under a focused reading beam”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].hero.alt`
  - `index.html:990`
  - `library.html:127`
  - `library/how-to-read-a-health-study.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Learn a practical framework for reading health studies, spotting bias and judging whether results apply to you.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Learn what a Supplement Facts panel can establish, what claims and disclaimers do not prove, and how to compare serving size, amounts, ingredients and quality signals.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].summary`
  - `library.html:73`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Learn what gut biomarkers and consumer microbiome tests measure, where they can help, and where interpretation stops.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Learn what omega-3 blood tests measure, how the Omega-3 Index is calculated, what can affect a result, and why a number is information—not a diagnosis.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Learn what omega-3 blood tests measure, what can affect a result, and why a number is information—not a diagnosis.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].summary`
  - `library.html:94`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Learn what the result directly measures, what can be inferred, and where the evidence stops.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[6].blocks[0].items[1].definition`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Look for evidence in a population and outcome relevant to you.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[4].blocks[1].items[1]`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Making informed decisions about your health doesn't mean obsessing over every number on a report.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[0].blocks[0].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Many studies compare microbiomes in people with and without a condition.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[2].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Massage, compression, cold-water immersion, active recovery and other modalities may change soreness or perceived fatigue in some settings.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].bodySections[3].blocks[0].text`
  - `library/recovery-after-training.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Measurement method and sample type matter, and there isn't universal agreement about one single best PUFA biomarker for every purpose.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[3].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Mechanistic experiments, repeated findings, prospective studies and intervention trials can increase confidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[2].blocks[1].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Metabolic indices of polyunsaturated fatty acids: current evidence, research controversies, and clinical utility”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].sources[3].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Metabolic indices of polyunsaturated fatty acids: current evidence, research controversies, and clinical utility ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/omega-3-what-the-numbers-mean.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Microbiome research changes quickly and uses varied sampling, sequencing and analysis methods.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].limitations[0]`
  - `library/gut-health-101.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Most performance-nutrition decisions are not about finding a secret ingredient.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].dek`
  - `library/performance-nutrition-basics.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “NIH notes that omega-3 supplements can interact with medications, including anticoagulants, and that higher doses deserve additional care.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[5].blocks[0].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “National Center for Complementary and Integrative Health”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].sources[4].organization`
  - `content/library.json:$.articles[8].sources[1].organization`
  - `content/library.json:$.articles[9].sources[4].organization`
  - `library/correlation-causation-relative-risk.html:70`
  - `library/gut-health-101.html:70`
  - `library/how-to-read-a-health-study.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “National Heart, Lung, and Blood Institute”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].sources[2].organization`
  - `content/library.json:$.articles[9].sources[2].organization`
  - `library/correlation-causation-relative-risk.html:70`
  - `library/how-to-read-a-health-study.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “National Institute of Environmental Health Sciences”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].sources[0].organization`
  - `library/gut-health-101.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Needs differ by sport, body size, climate, health status and training history.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].limitations[0]`
  - `library/recovery-after-training.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Next, learn why an association is not automatically a cause—and why relative risk needs an absolute baseline.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].relatedReadingIntro`
  - `library/how-to-read-a-health-study.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Next, see what consumer gut tests can measure—and where interpretation can overreach.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].relatedReadingIntro`
  - `library/gut-health-101.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Not all gut tests are the same”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[1].heading`
  - `library/gut-testing-biomarkers.html:62`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Observational studies identify associations but generally cannot establish causation alone.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].evidenceLabels[0].items[2]`
  - `library/how-to-read-a-health-study.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Omega-3 fatty acids for the primary and secondary prevention of cardiovascular disease”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].sources[5].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Omega-3 fatty acids for the primary and secondary prevention of cardiovascular disease ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/food-vs-omega-3-supplements.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Omega-3 gets talked about everywhere—from fish and supplements to blood tests and ratios.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].dek`
  - `library/omega-3-what-the-numbers-mean.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Omega-3 lipid molecules and blood-status signals in a dark biological matrix”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].hero.alt`
  - `library.html:78`
  - `library/omega-3-what-the-numbers-mean.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Omega-3: What It Is, What You Can Measure, and What the Numbers Actually Mean”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].title`
  - `library.html:80`
  - `library/omega-3-what-the-numbers-mean.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Omega-3: What It Is, What You Can Measure, and What the Numbers Actually Mean →”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/food-vs-omega-3-supplements.html:69`
  - `library/how-to-read-a-supplement-label.html:69`
  - `library/should-you-test-your-omega-3-levels.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Omega-6 and omega-3 fatty acids are both families of polyunsaturated fats, and comparing them as a ratio has attracted considerable research interest.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[4].blocks[0].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “One macro split, meal frequency or supplement stack for all athletes.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].evidenceLabels[2].items[0]`
  - `library/performance-nutrition-basics.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “One study rarely settles a broad health question.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].keyTakeaways[3]`
  - `library/how-to-read-a-health-study.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Organize energy, protein, carbohydrate, hydration and meal timing before deciding whether a supplement solves anything.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].summary`
  - `library.html:122`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Our editorial system is designed to keep evidence, opinion, uncertainty, and partnerships visible.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library.html:146`
  - `templates/library.html:33`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Outcome evidence is summarized conservatively because effects vary by population, dose, intervention and outcome.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceNotes[2]`
  - `library/food-vs-omega-3-supplements.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “People do not all produce the same biomarker response to the same intake.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[3].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Performance Nutrition Basics Before Supplements | The Mindful Matrix”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].seoTitle`
  - `library/performance-nutrition-basics.html:6`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Performance Nutrition: The Basics Before Supplements”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].title`
  - `library.html:122`
  - `library/performance-nutrition-basics.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Performance Nutrition: The Basics Before Supplements →”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/recovery-after-training.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Performance nutrition is a matching problem: align enough food and fluid with the training demand, then evaluate optional tools narrowly.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].evidenceSummary.statement`
  - `library/performance-nutrition-basics.html:67`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Performance nutrition starts with enough energy to support training, recovery and ordinary biological function.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[0].blocks[0].text`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Personalized food or supplement prescriptions based on a single commercial microbiome profile.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[2].items[1]`
  - `library/gut-health-101.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Personalized supplement plans derived from a single taxonomic profile.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[2].items[1]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Position statements synthesize broad evidence but still require individual application.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].evidenceNotes[0]`
  - `library/performance-nutrition-basics.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Practical wellness education built around credible sources, useful context, and clearer next steps.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library.html:55`
  - `templates/library.html:12`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Pre-analytic and analytic methods affect test results.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[0].items[1]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Prefer independent quality certification when contamination carries sport or health consequences.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].bodySections[4].blocks[1].items[3]`
  - `library/performance-nutrition-basics.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Probiotic evidence is strain-, dose-, population- and outcome-specific.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceNotes[1]`
  - `library/gut-health-101.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Randomization can balance known and unknown confounders on average, making a well-conducted trial a strong design for many intervention questions.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].bodySections[3].blocks[0].text`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Randomization can reduce confounding in intervention studies.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].evidenceLabels[0].items[0]`
  - `library/how-to-read-a-health-study.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Randomized controlled trial: can support causal inference when allocation, adherence, follow-up and measurement are sound.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[1].blocks[0].items[0]`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Randomized trials support that supplemental EPA and DHA can change measured fatty-acid status, but biomarker response is not treated as proof of a guaranteed clinical benefit.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceNotes[1]`
  - `library/food-vs-omega-3-supplements.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Recovery research often uses short-term biomarkers or soreness, which may not predict long-term performance or adaptation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].evidenceNotes[1]`
  - `library/recovery-after-training.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Red-blood-cell measures can be useful markers of longer-term EPA and DHA exposure.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[3].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Research does not support one universal answer for every person or outcome.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[2].meaning`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Research exists, but important uncertainty or disagreement remains.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceLabels[2].meaning`
  - `content/library.json:$.articles[1].evidenceLabels[2].meaning`
  - `library/omega-3-what-the-numbers-mean.html:63`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Results are often reported as a percentage of the fatty acids in the analyzed fraction rather than as the total amount of omega-3 in the body.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[1].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Return to the study-reading guide and apply the risk and causation questions to a complete paper.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].relatedReadingIntro`
  - `library/correlation-causation-relative-risk.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Seek professional context when a result may influence medical care or substantial supplement changes.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[3].items[2]`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Selected fatty acids can be measured in plasma, serum, erythrocytes, and whole blood.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[0].items[0]`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Should You Test Your Omega-3 Levels?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].seoTitle`
  - `content/library.json:$.articles[1].title`
  - `library.html:94`
  - `library/omega-3-what-the-numbers-mean.html:69`
  - `library/should-you-test-your-omega-3-levels.html:56`
  - `library/should-you-test-your-omega-3-levels.html:6`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Sleep, adequate energy, protein distribution, carbohydrate needs and fluid replacement deserve attention before specialized tools.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].keyTakeaways[1]`
  - `library/recovery-after-training.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Sleep: protect adequate opportunity, consistency and quality.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].bodySections[1].blocks[0].items[1]`
  - `library/recovery-after-training.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Some specialized tests have narrower evidence bases than can be covered here.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].limitations[2]`
  - `library/gut-testing-biomarkers.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Some specific probiotic strains have evidence for specific uses; effects cannot be generalized to every product or condition.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[1].items[1]`
  - `library/gut-health-101.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Soreness is not a complete measure of recovery or workout quality.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].keyTakeaways[3]`
  - `library/recovery-after-training.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Source forms can appear in parentheses—for example, a mineral followed by the compound that supplies it.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[2].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Sports-supplement evidence can be affected by small studies, trained-vs-untrained differences, product formulation and industry funding.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].evidenceNotes[1]`
  - `library/performance-nutrition-basics.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Start with the question and the evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].optionalAction.copy`
  - `library/gut-health-101.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Start with the research question and study design, not the conclusion paragraph.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].keyTakeaways[0]`
  - `library/how-to-read-a-health-study.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Step 5: Put one result into the evidence map”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[4].heading`
  - `library/how-to-read-a-health-study.html:62`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Supplement label under an evidence-reading scanner with ingredient and dose fields”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].hero.alt`
  - `library.html:71`
  - `library/how-to-read-a-supplement-label.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Supplements are optional tools with product-specific evidence, quality and safety questions.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].keyTakeaways[3]`
  - `library/performance-nutrition-basics.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Supported by authoritative nutrition guidance and established fatty-acid biology.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[0].meaning`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Supported by established measurement and biomarker evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[0].meaning`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Supported by established nutrition and physiology evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceLabels[0].meaning`
  - `library/omega-3-what-the-numbers-mean.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Supported by established physiology, nutrition, or research-method evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[0].meaning`
  - `content/library.json:$.articles[5].evidenceLabels[0].meaning`
  - `content/library.json:$.articles[6].evidenceLabels[0].meaning`
  - `content/library.json:$.articles[7].evidenceLabels[0].meaning`
  - `content/library.json:$.articles[8].evidenceLabels[0].meaning`
  - `content/library.json:$.articles[9].evidenceLabels[0].meaning`
  - `library/correlation-causation-relative-risk.html:65`
  - `library/gut-health-101.html:65`
  - `library/gut-testing-biomarkers.html:65`
  - `library/how-to-read-a-health-study.html:65`
  - `library/performance-nutrition-basics.html:65`
  - `library/recovery-after-training.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Systematic review or meta-analysis: structured synthesis whose strength depends on search, selection, bias assessment and study comparability.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[1].blocks[0].items[4]`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Systematic reviews can improve the evidence picture when methods are rigorous and included studies are sufficiently comparable.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].evidenceLabels[1].items[0]`
  - `library/how-to-read-a-health-study.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Take one recent health claim and identify the population, design, comparator, measured outcome, absolute effect and largest uncertainty before deciding what it means.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].optionalAction.copy`
  - `library/how-to-read-a-health-study.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Targeted clinical test: a specific analyte tied to a clinical question.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[1].blocks[2].items[0]`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Temporality, consistency, dose-response patterns, plausible mechanisms and intervention evidence can strengthen causal inference when considered together.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].evidenceLabels[1].items[0]`
  - `library/correlation-causation-relative-risk.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Test offerings and laboratory methods can change faster than consensus guidance.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].limitations[0]`
  - `library/gut-testing-biomarkers.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “That does not mean every microbe has a simple meaning—or that one food, probiotic, or score can define a healthy gut.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].dek`
  - `library/gut-health-101.html:58`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “That doesn't mean one blood test tells you everything about your health.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[2].blocks[2].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “That is why change over time is easiest to interpret when the specimen type, reported metric or units, method where available, and relevant pre-test conditions are comparable.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[6].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “That supports a biomarker effect.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[4].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The American Heart Association recommends eating two servings of fish per week, particularly fatty fish.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[1].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The Facts About Health News Stories”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].sources[4].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The Facts About Health News Stories ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/correlation-causation-relative-risk.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The Microbiome in Health and Disease”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].sources[2].title`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The Microbiome in Health and Disease ↗”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/gut-health-101.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The Omega-3 Index is used in omega-3 research.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceLabels[1].items[1]`
  - `library/omega-3-what-the-numbers-mean.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The Omega-3 Index provides information about erythrocyte EPA and DHA status and is a biomarker used in omega-3 research.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[3].blocks[2].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The Omega-3 Index: a new risk factor for death from coronary heart disease?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].sources[1].title`
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The absence of a caution statement does not prove that a supplement has no risks.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[6].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The amount listed in Supplement Facts is usually the amount per serving, not necessarily per capsule, scoop, gummy or bottle.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[1].blocks[0].text`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The basics—adequate nutrition, fiber from varied foods when tolerated, sleep and appropriate medical care—matter more than chasing a perfect score.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].keyTakeaways[3]`
  - `library/gut-health-101.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The best PUFA biomarker for every context.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceLabels[2].items[1]`
  - `library/omega-3-what-the-numbers-mean.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The best specimen and biomarker for every population or purpose.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].evidenceLabels[2].items[1]`
  - `library/should-you-test-your-omega-3-levels.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The consensus literature distinguishes research potential from current routine clinical utility.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].evidenceNotes[1]`
  - `library/gut-testing-biomarkers.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The essential move is to compare the claim with what the study was actually capable of showing.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].evidenceSummary.statement`
  - `library/how-to-read-a-health-study.html:67`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The evidence does not support treating either one as a universal prescription.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceSummary.statement`
  - `library/food-vs-omega-3-supplements.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The gut microbiome is an ecosystem of microorganisms and their genes—not a single organ with one ideal setting.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].keyTakeaways[0]`
  - `library/gut-health-101.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The intake or blood target that should apply to every population.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[2].items[1]`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The material analyzed, such as plasma, serum, erythrocytes, or whole blood.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[1].blocks[2].items[0].definition`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The next guide explains how study design and bias affect the confidence you should place in any health claim.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].relatedReadingIntro`
  - `library/gut-testing-biomarkers.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The next step may be adding a food, reading a label, asking a professional a better question, choosing an algae-derived option, or deciding that no supplement is needed right now.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[6].blocks[1].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The numerical examples are hypothetical and illustrate interpretation; they are not estimates of a real health outcome.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].evidenceNotes[0]`
  - `library/correlation-causation-relative-risk.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The nutrient, botanical, amino acid or other dietary substance declared in Supplement Facts.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[2].blocks[1].items[0].definition`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The performance-nutrition guide puts protein, carbohydrate, hydration and supplements into one practical order.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].relatedReadingIntro`
  - `library/recovery-after-training.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The practical lesson is not that EPA and DHA do nothing; it is that changing intake, changing a biomarker and changing a clinical outcome are three different claims.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].bodySections[4].blocks[2].text`
  - `library/food-vs-omega-3-supplements.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The product does not determine the evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[0].blocks[5].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The recent NIST-associated comparison assessed analytical performance, not whether every possible microbiome test is useless.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].evidenceNotes[0]`
  - `library/gut-testing-biomarkers.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The scientific support for a claim should match the ingredient, dose, population and outcome being advertised.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].evidenceLabels[1].items[2]`
  - `library/how-to-read-a-supplement-label.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The time between an intake change and a blood draw also matters because blood fractions turn over at different rates.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[5].blocks[1].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “The useful question is not whether everyone should test.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[0].blocks[2].text`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “These organisms interact with food components, medications, the immune system and each other.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[0].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “This guide cannot cover specialized statistical methods or every study design.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].limitations[0]`
  - `library/how-to-read-a-health-study.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “This guide does not calculate individualized energy, carbohydrate, protein, electrolyte or fluid targets.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].limitations[0]`
  - `library/performance-nutrition-basics.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “This guide does not certify or rank any supplement manufacturer.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].limitations[0]`
  - `library/how-to-read-a-supplement-label.html:67`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “This guide does not provide an individualized hydration or nutrition prescription.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].limitations[1]`
  - `library/recovery-after-training.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Those steps support overall health even when the microbiome mechanism is not the main reason.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[3].blocks[0].text`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Treat a supplement as optional, product-specific and evidence-specific.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[4].blocks[0].items[4]`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Treating diversity as a stand-alone health grade.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceLabels[2].items[2]`
  - `library/gut-health-101.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Understand ALA, EPA, DHA, the Omega-3 Index, fatty-acid ratios and what blood measurements can—and cannot—tell you.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].seoDescription`
  - `content/library.json:$.articles[0].summary`
  - `library.html:80`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Understand correlation, causation, confounding, relative risk and absolute risk in everyday health research.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Understand the difference between ALA, EPA and DHA, where food fits, when supplements may be useful, and why changing a biomarker is not the same as guaranteeing a health outcome.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].summary`
  - `library.html:87`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Understand the difference between clinically ordered stool or blood markers and consumer microbiome profiles before acting on a result.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].summary`
  - `library.html:108`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Understand the gut microbiome, what shapes it, and where current gut-health evidence remains uncertain.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].seoDescription`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Understand the method and the decision it could support before following a commercial route.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].optionalAction.copy`
  - `library/gut-testing-biomarkers.html:71`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Understand what a test measures before acting on the number.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].evidenceLabels[3].items[2]`
  - `library/omega-3-what-the-numbers-mean.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Use a comparable measurement to evaluate whether the biomarker—not an assumed health outcome—actually changed.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].bodySections[6].blocks[0].items[3].definition`
  - `library/should-you-test-your-omega-3-levels.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Use a test only when you understand what it measures and what decision could follow.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].bodySections[4].blocks[0].items[3]`
  - `library/gut-health-101.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Use the evidence, your circumstances and reasonable next steps.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[7].blocks[1].items[2].definition`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for PUFA biomarkers, metabolic indices, research controversies, and clinical utility.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].sources[3].detail`
  - `library/omega-3-what-the-numbers-mean.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for available blood specimens, recent-meal effects on plasma and serum, the longer erythrocyte measurement window, the Omega-3 Index definition, and the absence of established normal ranges.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].sources[0].detail`
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for biomarker response to intake changes and for baseline status, dose relative to body weight, age, sex, and physical activity as response variables in the study population.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].sources[4].detail`
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for definitions of ALA, EPA and DHA; food and supplement sources; ALA conversion; intake and status context; medication interactions; and safety considerations.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].sources[0].detail`
  - `library/food-vs-omega-3-supplements.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for definitions of risk ratio and measures of association.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].sources[0].detail`
  - `library/correlation-causation-relative-risk.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for evaluating express and implied health claims, relevant scientific substantiation and the need to communicate important limitations clearly.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].sources[6].detail`
  - `library/how-to-read-a-supplement-label.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for evidence of variability across seven consumer services using standardized material.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].sources[1].detail`
  - `library/gut-testing-biomarkers.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for evidence on soreness and perceived-fatigue outcomes across recovery modalities.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].sources[3].detail`
  - `library/recovery-after-training.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for internal validity and risk-of-bias principles across study designs.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].sources[3].detail`
  - `library/how-to-read-a-health-study.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for laboratory comparability, reporting variation, and the value of standardized reporting for dried blood spot fatty-acid profiles.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].sources[6].detail`
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for nutrient definitions, metabolism, blood measurement, Omega-3 Index context, and biomarker limitations.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].sources[0].detail`
  - `library/omega-3-what-the-numbers-mean.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for practical evidence and safety context around probiotic products.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].sources[4].detail`
  - `library/gut-health-101.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for practical questions about study type, magnitude, uncertainty and reporting.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].sources[4].detail`
  - `library/correlation-causation-relative-risk.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for protein intake, distribution and exercise-context evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].sources[1].detail`
  - `library/performance-nutrition-basics.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for supplement evidence, safety, labeling and quality context.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].sources[2].detail`
  - `library/performance-nutrition-basics.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the current limits of standardization and individual health interpretation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].sources[2].detail`
  - `library/gut-testing-biomarkers.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the distinction between research associations, diagnostic development and clinical translation.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].sources[3].detail`
  - `library/gut-testing-biomarkers.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the dose-responsive increase in erythrocyte EPA plus DHA and the influence of baseline and individual response variables in the study population.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].sources[4].detail`
  - `library/food-vs-omega-3-supplements.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the fact that FDA does not approve dietary supplements for safety and effectiveness before sale and for required Supplement Facts information.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].sources[3].detail`
  - `library/how-to-read-a-supplement-label.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the finding that individual EPA and DHA biomarker responses can vary across erythrocyte, plasma, and whole-blood measurements.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].sources[5].detail`
  - `library/should-you-test-your-omega-3-levels.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the integrated energy, carbohydrate, protein, fat, fluid and timing framework.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[7].sources[0].detail`
  - `library/performance-nutrition-basics.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the limited role, evidence variation and safety considerations of performance supplements.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].sources[4].detail`
  - `library/recovery-after-training.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the role of adequate energy, carbohydrate, protein, fluid and individualized planning.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[6].sources[1].detail`
  - `library/recovery-after-training.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used for the strengths and limits of randomized and observational study designs.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].sources[0].detail`
  - `library/how-to-read-a-health-study.html:70`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Used to show the distinction between credible evidence and the stronger significant-scientific-agreement standard for certain cardiovascular claims.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].sources[2].detail`
  - `library/omega-3-what-the-numbers-mean.html:68`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Was the study long enough to observe a meaningful outcome?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[8].bodySections[2].blocks[1].items[5]`
  - `library/how-to-read-a-health-study.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Was the study observational or experimental?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[9].bodySections[4].blocks[0].items[0]`
  - `library/correlation-causation-relative-risk.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “We've collected testing and omega-3 tools on The Shelf.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].optionalAction.copy`
  - `library/omega-3-what-the-numbers-mean.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “What a Blood Test Can—and Can’t—Tell You”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[1].title`
  - `library.html:94`
  - `library/should-you-test-your-omega-3-levels.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “What a Blood Test Can—and Can’t—Tell You →”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `library/omega-3-what-the-numbers-mean.html:69`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “What does the evidence actually support?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[6].blocks[9].items[4]`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “What exact claim is being made, and does the cited evidence match the ingredient, dose, population and outcome?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[7].blocks[0].items[4]`
  - `library/how-to-read-a-supplement-label.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “What exact question is the test designed to answer?”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].bodySections[0].blocks[1].items[0]`
  - `library/gut-testing-biomarkers.html:66`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “What the evidence supports”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[4].evidenceSummary.heading`
  - `content/library.json:$.articles[5].evidenceSummary.heading`
  - `content/library.json:$.articles[6].evidenceSummary.heading`
  - `content/library.json:$.articles[7].evidenceSummary.heading`
  - `content/library.json:$.articles[8].evidenceSummary.heading`
  - `content/library.json:$.articles[9].evidenceSummary.heading`
  - `library/correlation-causation-relative-risk.html:67`
  - `library/gut-health-101.html:67`
  - `library/gut-testing-biomarkers.html:67`
  - `library/how-to-read-a-health-study.html:67`
  - `library/performance-nutrition-basics.html:67`
  - `library/recovery-after-training.html:67`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Whenever possible, education should link back to credible evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/site.json:$.homepage.standards.principles[1].copy`
  - `index.html:1009`
  - `library.html:147`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Whether a supplement improves a specific long-term outcome in a particular person.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[2].items[0]`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Whether one supplement form is meaningfully superior across all real-world uses.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].evidenceLabels[2].items[2]`
  - `library/food-vs-omega-3-supplements.html:63`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Whole-food omega sources balanced against a neutral supplement form”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[2].hero.alt`
  - `library.html:85`
  - `library/food-vs-omega-3-supplements.html:56`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “Write down the question before ordering a test.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[5].evidenceLabels[3].items[0]`
  - `library/gut-testing-biomarkers.html:65`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “You don't need every answer before making informed health-related choices.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[7].blocks[0].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “You might hear about EPA, DHA, ALA, the Omega-3 Index, omega-6:omega-3 balance, AA/EPA ratios, fish oil and blood testing as though they're interchangeable.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[0].bodySections[0].blocks[2].text`
  - `library/omega-3-what-the-numbers-mean.html:64`

### LOW_RISK — RESEARCH_INTERPRETATION

- Exact text: “‘Supports’ is not automatically established evidence.”
- Risk: `GREEN`
- Reason: Likely editorial claim; retain source, scope, limitations, and uncertainty.
- Source/rule: `HEURISTIC_CLAIM_BEARING_TEXT`
- Recommended next action: `EDITORIAL_SOURCE_REVIEW`
- Locations:
  - `content/library.json:$.articles[3].bodySections[4].blocks[2].items[0]`
  - `library/how-to-read-a-supplement-label.html:64`

## Interpretation

A RED result is a machine hard-stop for the stated commercial context. A YELLOW result is not approval; it requires evidence, qualification, disclosure, or human review. Exact registry matches preserve the currently reviewed wording and scope only. Duplicate public/template findings are retained in the JSON report so every location remains auditable.

The absence of a machine-detected hard violation must be described only as: **No hard-rule violations detected by Compliance Engine v1.** It must not be described as legal compliance.
