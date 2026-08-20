# The Mindful Matrix V7 candidate

# BASELINE RECONCILIATION

See `V7_BASELINE_RECONCILIATION.md`. V7 uses the persisted V6 tree, removes only obsolete execution machinery, resets payload/warning metrics to deterministic values, and does not rewrite V6 history.

## Candidate outcome

- Product-first homepage retains the canonical Balance Test Basic Kit as the above-the-fold featured starting point, with current canonical manufacturer, pricing, disclosure, imagery, and destination logic.
- Product Universe remains immediately below the hero and exposes all 45 active canonical products by six intents.
- Shop discovery adds accessible free-text search, manufacturer filtering, curated/name/price sorting, a derived live result count, and one-step reset. Search spans product name, manufacturer, category, kind, format, and description.
- A new Matrix-native “Know your number” section connects TEST → MEASURE → ACT → RETEST to the two existing evidence-reviewed Omega guides and canonical testing tools. It explicitly limits the measurement and makes action optional.
- Restricted third-party recordings and resource 69315 are not published because current public-sharing eligibility and rights were not established from repository evidence.
- No new Product/Offer schema is published. The existing CollectionPage/ItemList remains the accurate model for a collection that sends visitors to external manufacturers; no seller, availability, review, or unsupported offer facts are inferred.

## Validation evidence

- Deterministic build: passed.
- Static validation: passed; 4 core pages, 10 articles, 45 active products, 8 deferred products, `/BioCare/` safe.
- Compliance hard gate: passed with 91 review warnings.
- Compliance fixtures: 8/8 passed.
- Strict dry run: 98 advisory items, reconciled to the persisted baseline.
- Browser QA: desktop and 375px mobile; 0 horizontal overflow; 45 product cards; search `omega` derived 8 results; mobile search `Balance Test` + Zinzino derived 2 results; no console errors or warnings.
- Responsive evidence: `v7-home-desktop.png`, `v7-home-mobile-375.png`, `v7-shop-desktop.png`, `v7-shop-mobile-375.png` (review deliverables generated outside the deployed tree).
- Active product-image payload: 1,405,208 B across 45 unique active cutouts.

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

Candidate is ready for visual and editorial review only. Do not merge or deploy before approval. The approximately 800 KB image goal and live Rich Results Test remain future work that requires a deliberate visual-compression study and a deployed URL, respectively.
