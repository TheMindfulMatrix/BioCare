# Measurement contract and baseline worksheet

Status: **INERT FOUNDATION / NO PROVIDER CONNECTED**. `assets/js/growth-measurement.js` is deliberately not loaded by public HTML. Its transport is injected in tests; it has no network or storage implementation. Node and browser tests prove the contract, not a working analytics account.

## Allowlisted events

| Event | Meaning | Fields | Does not mean |
| --- | --- | --- | --- |
| page_view | A loaded document emitted an event | action, broad section, broad source | A unique person, qualified lead, or consent |
| manufacturer_click | A sponsored link to a recognized manufacturer was clicked | action, section, source, merchant | A completed order or earned commission |
| education_click | A local Library-article link was clicked | action, section, source | The guide was read or understood |
| contact_click | An email link was clicked | action, section, source | An email was sent or a subscription created |

Sections: home, products, library, evidence, journeys, explore, business, other. Sources: explicit allowlisted source labels or coarse referrer domain groups; unknown values are discarded. No full URL, query, title, product ID, health topic, raw referrer, user/email identifier, test data or arbitrary custom property is serialized. Source grouping is per document and does not stitch sessions. Internal navigation cannot be reliably credited back to its initial acquisition channel without a separately reviewed design.

Rapid duplicate events within one second are suppressed; pageview is emitted at most once per binding. Handler installation is idempotent. Exceptions/rejected transport promises are contained; navigation is never delayed or prevented. Blocking/ad blockers and unknown referrers reduce coverage; do not bypass user privacy controls to improve totals.

Confirmed subscribers come from mailing-provider double-opt-in records. Orders/commissions come from manufacturer affiliate reports. Keep those aggregates in a restricted workspace or approved account, never a public dashboard or this Git repository.

## Weekly aggregate worksheet — no live business data

| Field | Current baseline | Source / caveat |
| --- | --- | --- |
| Reporting period and attribution window | Not established | Set before collecting a baseline |
| Google impressions and clicks | Unavailable | Search Console access required |
| Recorded pageviews by broad source/section | Unavailable | Provider inactive; not unique visitors |
| Manufacturer-link clicks | Unavailable | Interest only; state filtering/deduplication |
| Confirmed newsletter subscribers | Unavailable | Provider inactive |
| Confirmed orders, reversals and earned commissions | Unavailable | Manufacturer report; attribution coverage may differ |
| Approved recurring service costs | Unavailable | Use actual invoices, not estimated vendor prices |
| Commission less recorded operating costs | Not calculable | Not full accounting profit; exclude unknown costs explicitly |

Do not divide incompatible totals into a purported sales-conversion rate. Report a click rate only when its numerator/denominator and time window are compatible. Do not claim user-level conversion attribution from aggregate reports.

## Evaluation plan

Capture baseline data after authorized activation, retaining the same definitions in the comparison period. Inspect sufficient traffic and variation before declaring a winner; no arbitrary guaranteed improvement or revenue target. Change one journey element at a time where practical. Include usability feedback when traffic is too small for a meaningful experiment. Review costs and commission reversals, not just activity. Keep daily technical audits and business reporting separate.

Suggested social destination: the existing `/know-your-number.html` journey for testing-related posts. Use simple approved source labels only, without personal/health information, and do not rewrite existing manufacturer referral URLs.
