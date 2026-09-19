# Site and Academy review candidate — September 18, 2026

Draft only. No public merge, deployment, paid enrollment or account activation.

## This increment

- Product-first homepage and approved artwork preserved; a quiet Academy entry follows the Library.
- Shared native mobile navigation works without deferred JavaScript. Keyboard Escape closes the enhanced menu.
- Academy previews explain audience, module count, format, enrollment status and where to find the free sample, curriculum and access details.
- Saving disclosures distinguish visit-only public samples, account-synced self-review marks in the private candidate, and written answers that must be downloaded before closing their page.
- Library search has explicit result counts, reset and empty states; Enter no longer reloads the page.
- Evidence reset removes its hidden Core Four collection restriction; history restores collection filtering.

Product records, prices, destinations, images, editorial classifications and paid-course materials were not changed by this increment. No private hosting links, credentials, course manuscripts, learner information or operational exports are included.

## Verification

- Canonical build: 88 pages, 45 active / 8 deferred products; 91 generated outputs unchanged on a repeated build.
- 143 Python tests and 26 JavaScript tests passed, including both motion preferences in functional regression fixtures.
- All 88 pages, 175 referenced assets, robots.txt and sitemap.xml returned HTTP 200 and matched exact candidate bytes in local Windows serving.
- The existing audit's LF-normalized comparison reported 19 unchanged CRLF text-asset mismatches. The raw failing result was retained privately; separate exact-byte verification passed. The audit was not weakened.
- Actual local browser: eight representative routes at 1440, 768, 390 and 375 px, 32 states; no captured overflow, duplicate IDs or broken loaded images. No captured warning/error logs during that route pass. This is not physical-device, screen-reader, exhaustive WCAG or human-learner evidence.
- Mobile navigation/Escape, Library empty search/Enter/reset and Evidence Core Four reset were exercised. Broader reduced-motion behavior is covered by local fixtures, not newly claimed as browser-emulated evidence.
- Public safety scan: 143 files / 88 pages, zero findings. No paid/account routes in the public sitemap.
- Shared CSS/JavaScript increased by 3,873 uncompressed bytes; no new media. These are asset-size measurements, not field performance results.

## Compliance and scope reconciliation

Previous PR head `aa1d643df091ef69d36fcf356bfd9feaef1529de`: 379 review warnings / 386 strict advisory items. This candidate: **407 / 414**, zero RED or hard errors. All 28 added occurrences arise in the Partner page's `MLM_RECRUITMENT` context: 24 new text/context groups and four repeated existing occurrences. No findings were removed or rules suppressed. The seven inherited priorities and Xtend+ editorial priority remain open human-review work.

The live main baseline remains `ef36a71ecc3365fa1a03db18083ac75349c54574`, with 71 routes. This PR already contains three testing/learning routes and 14 additional Library guides, giving 88. They are not newly published by this pass. The K2, magnesium and zinc/copper guides are included in that inherited draft scope and need their publication review reconciled with separate maintenance PR #34 before any merge. PR #34 was not modified or incorporated.

## Release gate

This public candidate is not proof of a working purchaser journey. Keep enrollment closed until processor eligibility and credentials, real TEST purchase/access/progress/receipt/refund checks, qualified content review, consenting adult learner testing, approved seller/terms/support, production isolation/recovery and final release approval are complete. Public-site approval does not authorize private payment activation or social publication.
