# V8 Released and Verified

V8 is released, deployed, and independently verified at `https://themindfulmatrix.github.io/BioCare/`.

## Release identity

- V7 production baseline: `db2c82b36f356c92e37d983844fea0fdb0297ae5`
- Approved final V8 candidate: `7afe8289ccfe28832080b1ce31009d72383861ac`
- Candidate validation: run `32434521277`, success on the exact candidate SHA
- V8 PR: [#8](https://github.com/TheMindfulMatrix/BioCare/pull/8), merged normally with a merge commit at `2026-08-21T00:57:57Z`
- Functional merge commit: `f08a5e6a40a7347a8bbbe46b87626278a578f9de`
- Final disclosure fix candidate: `de6b67b5ce8fdefe57c0c856c906afd7b35f321c`
- Fix-forward PR: [#9](https://github.com/TheMindfulMatrix/BioCare/pull/9), merged normally with a merge commit at `2026-08-21T01:14:20Z`
- Final public-output release SHA: `8677222b5628a866ed5790ab05f88dd69be4bb96`
- Final main validation: run `32435593010`, success on the exact final public-output SHA
- Final Pages deployment: run `32435592732`, success on the exact final public-output SHA at `2026-08-21T01:15:04Z`
- Production verification completed at `2026-08-21T01:15:33Z`, followed by final browser interaction and responsive rechecks

The release-record publication branch contains only this Markdown file and its JSON counterpart. Its later report-only merge changes no generated page, asset, content model, template, script, or test; `8677222…` remains the authoritative V8 public-output tree.

## Release decision

- Definition of Done: **80 MET / 0 NOT MET / 0 DEFERRED**
- Visual acceptance: **20 MET / 0 NOT MET / 0 DEFERRED**
- Public pages: **22**
- Search inventory: **62 records** — 45 products, 10 guides, six departments, one journey
- Departments: **6**
- Products: **45 active / 8 deferred**
- Active product-image payload: **1,103,598 bytes**
- Compliance fixtures: **8/8 passed**
- Complete test suite: **15/15 passed**
- Compliance hard gate: **passed**
- Review/strict reconciliation: **91 review warnings / 98 strict dry-run advisory items**, unchanged

## Functional verification

Universal search passed empty, exact/partial/mixed-case/multi-term, product, guide, topic, department, journey, verified-ingredient and no-match cases; Everything, Products and Learn modes; clear, Escape, Enter, live announcements, URL state, reload, back/forward consistency and stale-state checks. Representative final-production results included omega `15 / 10 / 5` across Everything / Products / Learn, exact Balance Test Basic Kit `1`, mixed-case Balance Test `2`, omega food `7`, exact guide `1`, testing journey `1`, magnesium `6`, and no-match `0`.

Explore passed 12-product initial rendering and `12 → 24 → 36 → 45` reachability; both manufacturers; all six departments; all nine canonical product kinds; canonical/name/manufacturer sorting; chips, URL state, reset, empty state and no-JavaScript Products fallback. Department counts remained `7 / 10 / 3 / 15 / 8 / 2`.

Product Universe exercised all 45 unique active records with valid artwork, one selected state, correct sponsored link relations and no failures. Both manufacturers, six intents, 18 categories, filtered intent availability, previous/next confinement, accessory cross-intent behavior, empty state and full reset passed. Deferred products remained absent.

The Balance Test Basic Kit remained visible in the compact opening with a loaded official cutout, dated `$127` start-kit and `$47/mo` subscription presentation, a distinct internal testing-guide action and a distinct sponsored Zinzino source containing partner ID `2021428066`.

Know Your Number, Library, all ten Library guides, Start Here, Learn Before You Choose, Information → Education → Action, TEST. DON’T GUESS., and TEST → MEASURE → ACT → RETEST remained present and reachable.

## Live production evidence

- All 22 production pages returned successfully and matched the released repository output byte-for-byte.
- All 60 checked product images, Library artworks, CSS, JavaScript, search-index, sitemap and robots assets were available.
- The Google Fonts stylesheet and all eight referenced font files were available.
- Desktop `1440×900`, tablet `768×1024`, mobile `390×844`, and mobile `375×812` sweeps each covered all 22 pages with zero overflow, broken images, duplicate IDs, missing H1s, hidden featured imagery, sub-12px non-decorative text, or interactive targets below 44×44.
- Mobile navigation open/close, Escape close, focus return and visible focus passed.
- Production-origin console errors and warnings: zero.
- Product and search state remained current; no stale filter, result, inspector or empty-state content was observed.

## Disclosure fix-forward

The first live audit found that Explore and the six department grids referenced `shop-affiliate-disclosure` from sponsored price links without rendering that ID on those pages. The isolated fix-forward reused the exact approved Zinzino commission and BioLimitless compensation copy, placed applicable disclosures before each grid, bound every described action to an existing disclosure container, and added deterministic checks for future public pages. It changed no claims, catalog facts, prices, destinations, styling, JavaScript, imagery, education, navigation, or visual behavior. All nine affected routes passed at all four target viewports, and final production contains zero missing `aria-describedby` targets.

## Performance and assets

- Homepage HTML: **183,165 B**
- Explore HTML: **131,273 B**
- Products HTML: **137,176 B**
- CSS: **207,204 B**
- JavaScript: **46,562 B**
- Search index: **41,482 B**
- Homepage DOM after stabilization: **1,110 elements**
- Fresh Explore DOM: **1,058 elements**
- Homepage images: **22 elements** — 4 explicitly eager, 7 default-loading, 11 lazy, 3 high-priority
- Initial non-lazy candidates: **11 elements / 5 unique URLs**
- High-priority Balance Kit cutout transfer size: **18,460 B**; cinematic shelf artwork: **232,526 B**
- Observed browser-control upper bounds: search median **23 ms**, maximum **36 ms**; filter median **18 ms**, maximum **20 ms**. These include control-transport overhead and are not page-runtime-only benchmarks.
- LCP candidates remain the homepage H1 and cached featured Balance Kit imagery; no reliable lab LCP value was available.
- No layout shift was observed in stabilized captures, but no synthetic CLS score is claimed.
- No new runtime dependency, background video, image-payload regression, stale asset path, or heavy reduced-motion asset was introduced.

## Compliance, rights and links

The compliance hard gate and 8/8 fixtures passed. No diagnostic, disease, treatment, prevention, efficacy, dosage, guarantee, return, availability or outcome claim was added. Truthful Organization, WebSite, CollectionPage, ItemList, BreadcrumbList and Article data remained; no aggregate ratings, fake reviews, fake availability or unsupported Product/Offer data were introduced.

Commercial validation passed **90 records / 56 unique URLs / 56 reachable / 0 failed**. Partner/referral attribution, product-specific accessible names, sponsored relations, dated price sources, manufacturer-checkout separation, Independent Partner identification, commission/compensation disclosures, New York notice and applicable FDA disclaimer remain in place.

Non-commercial validation passed **49 unique references / 49 verified / 0 failed**: 46 directly reachable and three bot-protected destinations verified in a real browser. Two obsolete NCCIH references were replaced with their current authoritative pages.

Restricted R3G recordings, recorded third-party social interfaces, creator handles as assets, educational-only product-connected resources, recruiting, opportunity/income/lifestyle claims and resource 69315 remain unpublished. Public media/reference scanning found zero restricted media links. The explicit educational boundary statement is retained.

## Rollback and observations

- Historical tag `v5.1` remains unchanged at `b5d35772e98580e253c08f6319aa8e412fa20aea`.
- V7 rollback target remains `db2c82b36f356c92e37d983844fea0fdb0297ae5`.
- Repository-safe rollback process: create `agent/v8-rollback` from current `main`; revert merge commit `8677222b…` with mainline parent 1, then revert merge commit `f08a5e6a…` with mainline parent 1; regenerate and validate; open and merge a normal rollback PR; monitor Pages; verify the V7 production identity and all public routes. Never reset, rewrite history, move `v5.1`, or patch production directly.
- No rollback was required. No fix-forward remains pending.
- Non-blocking workflow observation: GitHub annotates Actions using Node 20-based action packages because its runner currently forces those actions onto Node 24. All validation and Pages jobs completed successfully.

## Final status

**V8 RELEASED AND VERIFIED.**

