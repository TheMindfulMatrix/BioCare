# V8 Final Candidate Report

Branch: `agent/v8-unified-discovery`. Candidate identity: exact pushed branch HEAD recorded by the draft PR and permanent validation run.

V8 adds a generated universal search spanning 45 active products, 10 published guides, six departments, and Know Your Number. Search fields derive from canonical catalog, Library, approved label records, and ID-only discovery mappings. It provides Everything, Products, and Learn modes with URL state.

The homepage preserves the Balance Test Basic Kit, distinct Learn and Official Product Source paths, commercial disclosure, Product Universe, Know Your Number, Library, and Information → Education → Action. A compact platform search and six derived-count department tiles precede the catalog.

`explore.html` provides search, 12-product progressive presentation, manufacturer/department/kind filters, canonical/name/manufacturer sorting, derived counts, reset, empty state, URL persistence, and no-JavaScript link to Products. Six generated department hubs connect canonical products, explicitly mapped guides, eligible journeys, transparency, and disclosures.

Validation: 22 public pages; deterministic build; core validator passed; 13/13 unit tests passed; compliance hard gate passed; 91 review warnings and 98 strict dry-run items exactly preserve the reconciled V7 baseline. No new unsupported claims were introduced. Responsive browser QA passed at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken rendered images, duplicate IDs, console errors, or console warnings.

Performance: homepage 172,225 B; Explore 113,286 B; Products 137,119 B; JavaScript 43,491 B; generated search index 31,142 B; active product imagery 1,103,598 B (no regression). Explore initially exposes 12 of 45 product cards and uses lazy images.

## Biological-tech visual integration

The visual pass corrects the flat utility presentation while retaining the approved V8 platform structure. Reusable CSS/SVG components now provide biological fields, signal paths, node clusters, scan frames, product stages, six department biomes, data captions, and evidence frames. Homepage search is integrated with the featured Balance Kit opening; typed search results visually separate product cutouts, article artwork, journeys, and departments. Know Your Number, Library, Start Here, Product Universe, header, and footer share the same restrained pathway language.

Motion is transform/opacity/SVG based, pauses offscreen and when the document is hidden, and resolves to a complete static design under reduced motion. Decorative layers are `aria-hidden`, ignore pointer events, and introduce no claims or fake measurements.

Final performance: homepage 183,104 B; Explore 130,822 B; Products 137,115 B; CSS 206,317 B; JavaScript 45,614 B; generated search index 41,482 B; active product imagery remains 1,103,598 B. JavaScript growth is 6.33%. Explore/search-index growth is the measured cost of richer typed-result imagery and derived department metadata.

Evidence screenshots are in `outputs/v8/before/` and `outputs/v8/after/` outside the repository. No merge or deployment occurred.
