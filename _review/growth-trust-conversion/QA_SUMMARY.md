# Growth / trust candidate — review evidence

Date: 2026-09-06. Status: validated review candidate; integrations inactive and editorial review still open.
No merge, deployment, service activation or editorial publication authorized by this report.

Baseline / rollback: `0a8ddc194b8ccea71c173ec6196d0e8a94d388a4` (PR #30). The exact candidate commit and CI result will be recorded by the draft PR. This report is not a release record.

## Validation

| Check | Result |
| --- | --- |
| Canonical build / structure | 71 public pages; 10 published articles; 45 active / 8 deferred products |
| Python tests | 105/105 pass (88 inherited + 17 new) |
| Node measurement tests | 9/9 pass; mocked adapters, not provider verification |
| Compliance hard gate | PASS; zero hard-gate errors |
| Advisory reconciliation | 70 review warnings / 77 unresolved strict items, unchanged |
| P1 priorities | All seven remain inherited HUMAN_REVIEW_REQUIRED |
| Safety scan | Zero public-source safety findings |
| Final full browser sweep | PASS: 568 states = 71 pages × 1440/768/390/375px × both motion settings; zero recorded failures |
| Final hero / zoom / prototype checks | 32 exact hero geometry/source comparisons; 16 200%-text cases without overflow; eight dummy-only signup simulations; mocked browser measurement deduplication/payload checks |
| Targeted accessibility | 12 page/viewport cases; 308 text contrast checks pass; keyboard skip/focus, forced-color focus, 44px primary buttons; four no-JS static routes and four comparison/product round trips |
| Production read-only parity | HEALTHY: existing 69 pages and 165 assets match the released baseline |
| Local candidate parity | HEALTHY: all 71 pages and 166 referenced assets; deterministic rebuild |
| CI public-preview packaging | Downloaded preview from run 34059787709: all 71 pages match the candidate; `_review` absent |

Strict dry-run **would fail** with the same 77 advisory items; it is not a clean strict-mode pass. All 10 inherited compliance files, catalog, Library source, site configuration, core styles, and existing enhancement script remain byte-identical to the baseline. No finding was reclassified, removed or suppressed. Xtend+ remains the first editorial priority.

Coverage expands to the new canonical growth copy and generated trust/journey pages. The daily workflow retains one existing schedule and its read-only behavior, while the permanent browser audit now covers all public pages with both motion preferences.

## Visual review

[Before/after image index](screenshots/README.md). Machine evidence: [review cases](evidence/review-qa.json), [local parity](evidence/local-parity.json), [accessibility and navigation](evidence/accessibility.json).

[Complete 568-state browser report](evidence/browser-audit.json): zero overflow, broken images, invalid page/H1 counts, duplicate IDs, unnamed controls, console errors/warnings, failed requests, HTTP errors or functional failures. The website source is commit `14372b3e99e27f11c61956809797d1d7dc0dd1d7`; the final follow-up commit adds only review evidence and documentation, with no website-source changes. Exact final head/CI status is recorded on draft PR #31.

The approved homepage artwork, responsive layout, header geometry and phone/tablet positioning are preserved. The additions use the existing visual system. PR #26 supplied a limited card-rounding idea only; its obsolete hero/header transformations were not imported.

Before/after journey captures show the added two-format comparison and non-purchase next step. New About/Contact and Privacy pages have no previous-page equivalent. Product-page changes add a comparison backlink only for the individual BalanceTest and Balance Test Basic Kit, alongside shared footer/accessibility styling.

Visual review caught faint dark-theme price supporting text on the new light comparison cards. The candidate now uses scoped, 14px supporting text with a measured 6.45:1 contrast ratio; a regression test protects the override. The repeated comparison disclosure was removed while retaining one adjacent disclosure and its accessibility association.

The new stylesheet is 5,443 bytes (uncompressed, LF-normalized); the 5,119-byte measurement module is not loaded by the site. No new fonts, runtime library or image asset is requested by public pages. Review PNGs are repository-only evidence outside the public artifact, not added website payload.

Screenshot pixel differences are diagnostic, not proof of a layout change: Chrome's composited decorative background varied between captures. The harness checks exact hero element geometry and image source separately. Section-only crops hide fixed header/dock/skip overlays during capture; full-page and first-screen captures preserve the actual interface. No image was retouched.

## What works and what does not

Public candidate: existing education → purchase-format comparison → canonical product details → established official manufacturer link. About/contact, corrections route, FAQs, privacy notice, navigation, search/filter behavior and disclosures remain usable without requiring signup. Opening the contact link is not proof of email delivery. No purchase was placed.

Analytics: inert allowlisted event core and tests only. No public script loads it; no network adapter, provider or dashboard is active. Clicks are not sales, pageviews are not unique visitors, and source labels do not establish session-level affiliate attribution.

Newsletter: non-public dummy-address prototype only. No real addresses, messages, subscriptions or lists were sent or stored. Actual delivery, double opt-in, unsubscribe and suppression remain unverified until an eligible provider is selected and activated under separate authorization.

Search Console: signed-out browser; property/indexing status unknown. Mailing-provider eligibility, account access, approved cost, private business postal address, sender setup and matching privacy review remain external dependencies. Existing email DNS was inspected read-only, not altered. See [integration status](INTEGRATION_STATUS.md).

Editorial: Xtend+ substantiation remains open; K2 literature addendum and existing draft remain non-public, awaiting full literature and qualified clinical/compliance review. Zinc/copper and magnesium have sourced research briefs, not published guides. The label checklist and welcome emails are also unapproved drafts.

## Review and later evaluation

Review the screenshots, commercial clarity and trust copy first. Approve a merge/deployment separately if this candidate is satisfactory. No paid service, DNS update, email sending or health-draft publication is bundled into that decision.

After separate measurement activation, collect a baseline using the [reporting worksheet](MEASUREMENT_PLAN.md): broad traffic source/section → useful actions → manufacturer clicks → separately confirmed orders/commissions → actual costs. Keep aggregates private, distinguish unknown values from zero and avoid unsupported revenue attribution.
