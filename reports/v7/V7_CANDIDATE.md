# The Mindful Matrix V7 candidate

## Complete candidate finish

The finished candidate adds canonical homepage discovery (search, manufacturer, category and six-intent filters; canonical/name/manufacturer sorts; live derived counts; reset and empty states), removes non-comparable price sorting, and adds the generated `know-your-number.html` education route with metadata, canonical URL, sitemap entry, evidence links, limitations and clearly separated official product-source actions. The Balance Kit foreground is forced out of reveal-animation dependency; served-asset inspection at 375px and 390px confirmed the 560 × 560 source loaded, rendered at 350.8 × 350.8 and 367.0 × 367.0 CSS pixels respectively, opacity 1, visible display, and zero horizontal overflow. Resource 69315 and restricted recordings remain withheld.

# BASELINE RECONCILIATION

See `V7_BASELINE_RECONCILIATION.md`. V7 uses the persisted V6 tree, removes only obsolete execution machinery, resets payload/warning metrics to deterministic values, and does not rewrite V6 history.

## Candidate outcome

- Product-first homepage retains the canonical Balance Test Basic Kit as the above-the-fold featured starting point, with current canonical manufacturer, pricing, disclosure, imagery, and destination logic.
- Product Universe remains immediately below the hero and exposes all 45 active canonical products by six intents.
- Shop discovery adds accessible free-text search, manufacturer filtering, canonical/name/manufacturer sorting, a derived live result count, and one-step reset. Non-comparable price sorting was removed. Search spans product name, manufacturer, category, kind, format, and description.
- A new Matrix-native “Know your number” section connects TEST → MEASURE → ACT → RETEST to the two existing evidence-reviewed Omega guides and canonical testing tools. It explicitly limits the measurement and makes action optional.
- Restricted third-party recordings and resource 69315 are not published because current public-sharing eligibility and rights were not established from repository evidence.
- No new Product/Offer schema is published. The existing CollectionPage/ItemList remains the accurate model for a collection that sends visitors to external manufacturers; no seller, availability, review, or unsupported offer facts are inferred.

## Validation evidence

- Final responsive matrix: 1440×900, 768×1024, 390×844 and 375×812; zero horizontal overflow, zero duplicate IDs, featured foreground loaded at opacity 1, and all six intents/canonical 45-product payload present at every viewport.
- Discovery matrix: empty, exact, partial, mixed-case, multi-term, no-match, repeated and whitespace-normalized queries; all 18 active categories; all six intents; all three manufacturers states; canonical/name/manufacturer sorts; reset; 45/45 exact-product selections. No stale inspector failures.
- Mobile accessibility: 108 visible interactive controls audited; important hero/Product Universe text meets the 11px floor and in-scope actions meet the 44×44 target after release cache-busting.
- Commercial audit: 45 active products, 90 destination/source records, 56 unique live URLs, 56 reachable, 0 protected, 0 failed.

- Deterministic build: passed.
- Static validation: passed; 4 core pages, 10 articles, 45 active products, 8 deferred products, `/BioCare/` safe.
- Compliance hard gate: passed with 91 review warnings.
- Compliance fixtures: 8/8 passed.
- Strict dry run: 98 advisory items, reconciled to the persisted baseline.
- Browser QA: desktop, tablet, 390px and 375px mobile; 0 horizontal overflow; 45 product cards; search `omega` derived 8 results; mobile search `Balance Test` + Zinzino derived 2 results; no console errors or warnings.
- Responsive evidence: `v7-home-desktop.png`, `v7-home-mobile-375.png`, `v7-shop-desktop.png`, `v7-shop-mobile-375.png` (review deliverables generated outside the deployed tree).
- Active product-image payload: 1,103,598 B across 45 unique active cutouts, reduced 301,610 B (21.46%) from the persisted 1,405,208 B baseline. Zinzino: 855,408 B; BioLimitless: 248,190 B. A four-setting WebP study selected quality 74/method 6 after contact-sheet review; dimensions, alpha, aspect ratios and provenance are unchanged. The approximately 800 KB target was not reached without a more aggressive quality tradeoff.

## Definition of Done (46 lines)

1. MET — verified persisted baseline used.  
2. MET — work isolated to `agent/v7-product-first`.  
3. MET — product-first hierarchy shipped.  
4. MET — Balance Kit is the featured above-fold product.  
5. MET — canonical product identity and data preserved.  
6. MET — 45 active products remain available.  
7. MET — 8 deferred products remain non-public.  
8. MET — search implemented.  
9. MET — manufacturer filtering implemented.  
10. MET — useful sorting implemented.  
11. MET — result count is derived and live.  
12. MET — controls are labeled and keyboard-operable.  
13. MET — mobile-first layout verified at 375px.  
14. MET — no horizontal overflow at tested widths.  
15. MET — Product Universe remains canonical-data driven.  
16. MET — Library stays one clear navigation action away.  
17. MET — Start Here is preserved.  
18. MET — Information → Education → Action is preserved.  
19. MET — TEST. DON’T GUESS. methodology is preserved.  
20. MET — TEST → MEASURE → ACT → RETEST is integrated.  
21. MET — Omega is framed as the first journey, not the whole brand.  
22. MET — existing Omega education is connected.  
23. MET — measurement limitations are explicit.  
24. MET — action remains optional.  
25. MET — no unverified imported funnel claims were copied.  
26. MET — restricted third-party recordings were not published.  
27. DEFERRED — resource 69315 omitted pending rights/current-copy verification.  
28. MET — commercial disclosures remain proximate.  
29. MET — partner link safety/attribution remains generated.  
30. MET — canonical pricing logic remains unchanged.  
31. MET — accessibility names on product links remain product-specific.  
32. MET — conservative Collection/ItemList schema retained.  
33. MET — no unsupported seller/offer/review/availability facts added.  
34. MET — metadata and sitemap regenerate deterministically.  
35. MET — compliance hard gate passes.  
36. MET — compliance tests pass 8/8.  
37. MET — review and strict warning totals reconciled.  
38. MET — browser discovery interactions verified.  
39. MET — desktop/mobile screenshots produced.  
40. MET — no merge or deployment performed.  
41. MET — persisted V6 discrepancy documented honestly.  
42. MET — no missing V6 release evidence fabricated.  
43. MET — obsolete one-time V6 workflows removed safely.  
44. MET — obsolete V6 patch/transfer artifacts removed safely.  
45. MET — permanent validation preserved and extended to V7 branch.  
46. MET — performance comparison uses actual 1,405,208 B baseline.

## Review boundary

Candidate completed the approved visual review. The approximately 800 KB image goal remains aspirational; the final defensible study result is 1,103,598 B. Live Rich Results testing remains a post-deployment verification where applicable.
