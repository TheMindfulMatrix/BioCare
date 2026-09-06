# Trust, design and measurable growth — candidate review

Baseline and rollback: `0a8ddc194b8ccea71c173ec6196d0e8a94d388a4` (PR #30), verified on 2026-09-06. Main and Pages matched that SHA before work. Baseline: 69 pages, 88 Python tests, 45 active / 8 deferred products, hard gate PASS, 70 review / 77 strict advisory findings.

Branch: `agent/growth-trust-conversion`. This directory is non-public review material, not a website section. Candidate lifecycle and exact SHA are recorded in the draft PR; do not interpret this snapshot as release authorization.

## Public candidate scope

- `about.html`: business identity, contact, editorial role, commercial relationships and keyboard-operable FAQ.
- `privacy.html`: the actual current static-site data flows, including Google Fonts, GitHub Pages and email; analytics/signup explicitly off.
- Existing testing journey: two canonical purchase formats, current price references, recurring-charge/eligibility/checkout checklist and manufacturer support. The two relevant product records link back to the comparison.
- Footer access from every page. Scoped supporting-text/card/focus polish; approved homepage hero and header geometry preserved.
- No new published health article, price value, claim, testimonial, social profile or affiliate destination.

## Not operational or not cleared

- Analytics: contract implementation and mocked tests only; no service, transport, script inclusion, telemetry or dashboard activated.
- Email: review-only prototype, draft checklist and welcome messages. No public signup, real addresses, subscriber import, email sending or automation activation.
- Search Console: the available browser reached a signed-out account chooser. Account/property/indexing status could not be verified. Public DNS absence of a Google verification TXT record is not proof that the property is unverified by another method.
- K2 and later education: still non-public and awaiting qualified review. The K2 addendum identifies additional primary studies, including a 2026 trial; it is not publication clearance.
- Xtend+: inherited HUMAN_REVIEW_REQUIRED wording and sources retained. No manufacturer or clinician was contacted.

See `INTEGRATION_STATUS.md`, `MEASUREMENT_PLAN.md`, `EMAIL_WELCOME_DRAFT.md`, `LABEL_CHECKLIST.md`, `EDITORIAL_REVIEW.md`, and `K2_REVIEW_ADDENDUM.md`.

## Design decision

Reviewed PR #26 at `6cb7e029fcea1cdd414e5e15f0f1ad2cb791b586`. Adapted modest card/control rounding in scoped additions. Did not import its hero dimensions, image transforms, label opacity, header geometry, global spacing/token changes or obsolete generated HTML. Existing approved imagery is reused; no AI artwork, extra fonts or animation libraries added.

The Sites-building skill guided readable type, focused scope, consistent states and reuse of the existing stack. Its hosting flow is intentionally not used because the user requires a draft PR and prohibits deployment.

## Boundaries and review questions

Owner: choose/authorize suitable analytics and mailing providers and supply an approved business postal address privately. Provider eligibility and actual settings must be confirmed before integration. Qualified reviewer: assess health/editorial wording and privacy/legal fit before the respective activation/publication. Coding agent: implement and verify the approved service in a separate candidate. Nobody should enable services by merely flipping the two booleans: the build deliberately refuses that shortcut.

The public privacy notice describes observed technical behavior, not certified legal compliance. Email retention settings and legal applicability remain review questions. No home address is published.

Production must remain unchanged until the user separately approves merge and deployment.

## Publication boundary

The existing Pages branch build uses Jekyll, with no `.nojekyll` or root config overriding its [leading-underscore directory exclusion](https://jekyllrb.com/docs/structure/). Review files, screenshots, research and the email simulation remain under `_review/`; the CI public-preview artifact also excludes that directory. Regression coverage blocks a silent change to this assumption. A future hosting/pipeline migration must explicitly preserve the exclusion. Repository collaborators can read this review material: this is not a place for secrets or personal data. The local review server intentionally serves these files for QA; it is not a production packaging model.
