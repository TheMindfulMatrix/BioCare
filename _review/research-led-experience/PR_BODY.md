# Research-led Matrix experience — review candidate

**Draft only. Do not merge or deploy without the owner's approval.**

Built from verified main `e0a668a10ddd6cafdf3f27ee4e6261f7e9caf27e` on `agent/research-led-experience`. The earlier V12 draft PR #26 is untouched; this is a separate, current-main candidate.

## What changed

- Original mineral-green / cream visual language across homepage, catalog, Library, Evidence, guides, Core Four and product records.
- A more composed opening with larger official Balance-kit imagery and responsive spacing.
- Keyboard-operable Learn / Measure / Explore navigation; useful static content remains without JavaScript.
- Three-guide home preview, with all ten guides preserved and the Library's search/filter controls moved earlier.
- Corrected inherited catalog initial scrolling that skipped the keyboard entry point.
- No product facts, prices, partner destinations, canonical domain, email, published guide text, claims registries or inherited review classifications changed.
- No tracking, paid services, framework migration, generated packaging, new health claims, merge or deployment.

## Research and visual review

[100-site research report](https://github.com/TheMindfulMatrix/BioCare/blob/agent/research-led-experience/_review/research-led-experience/RESEARCH_REPORT.md)

[QA report and artifact identity](https://github.com/TheMindfulMatrix/BioCare/blob/agent/research-led-experience/_review/research-led-experience/QA_REPORT.md)

[Actual before/after screenshots](https://github.com/TheMindfulMatrix/BioCare/tree/agent/research-led-experience/_review/research-led-experience/screenshots)

Local review gallery: `http://127.0.0.1:8772/_review/research-led-experience/` while the review server is running. The gallery is not part of the public build.

The research includes 85 bounded HTML observations, 15 primary-page fallbacks, and 12 desktop visual deep dives. It does not claim that all 100 sites received full mobile/functional audits or that visual polish establishes revenue, conversion or business failure.

![New desktop opening](https://github.com/TheMindfulMatrix/BioCare/blob/agent/research-led-experience/_review/research-led-experience/screenshots/home-desktop.jpg?raw=true)

## Validation

- 71 canonical pages; 45 active / 8 deferred products; 10 published guides.
- 112/112 Python tests; 9/9 JavaScript tests.
- Deterministic build; normal validation and compliance hard gate passed; zero RED.
- 568 browser states: zero recorded overflow, broken images, bad status, duplicate IDs, unnamed controls, console errors/warnings, non-navigation-abort failed requests or tested functional failures.
- 40 targeted usability cases; 8 deeper interaction suites; five no-JavaScript routes.
- Production-style **local** parity: 71 pages + 168 referenced assets passed. The documented first raw-Windows parity attempt differed only on CRLF text bytes; the audit was not weakened.
- Public safety scan: 114 files / 71 public pages, zero findings.
- Exact canonical public digest: `04870e4119b3ec3c2e5b2bbecbf3af471398954d986d32a853d7afba9e4d8e12`.

## Compliance and performance caveats

Advisory occurrence accounting is **69 / 76**, versus 70 / 77 before, solely because one duplicate homepage product description is no longer rendered. The claim itself, all unique human-review wording, all seven inherited P1 classifications and their sources/disclosures remain unchanged. Xtend+ remains the first future editorial-review priority. Strict mode still **would fail**; no claim was cleared or suppressed.

The visual layer adds about 18.2 KB (1.9%) in the measured first-viewport decoded loopback sample, despite a smaller homepage HTML document. No real-user performance or conversion uplift is claimed. The accessibility checks are useful basics, not a WCAG certification.

## Release boundary

This PR is for design review. Normal protected release approval, exact-head checks, merge commit and deployment/production verification would be a separate authorized step.
