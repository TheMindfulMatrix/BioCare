# External integration decisions — 2026-09-06

No account created, trial started, service purchased, DNS record changed or marketing message sent.

| Capability | Observed state | Next action / owner |
| --- | --- | --- |
| Website analytics | No existing runtime integration found. New measurement core is not included in HTML. | Owner approves provider and spend; implement a privacy-reviewed adapter and test actual reporting before activation. |
| Search Console | Available browser signed out; property status unknown. No account selection or credentials entered. | Owner signs in to the intended business Google account; verify the domain or URL-prefix property and submit the existing sitemap. DNS changes require separate approval. |
| Newsletter | No verified mailing-service account, address or sending authorization available. | Confirm provider permits this education-plus-partner business, approve terms/cost, and verify sender, double opt-in, unsubscribe, suppression and postal-address fields. |
| Affiliate sales reporting | Not accessed; no order/commission export supplied. | Owner supplies approved aggregate totals or scoped reporting access. Do not infer purchases from clicks. |
| Email authentication | Public SPF record present; DMARC requests quarantine; both Microsoft DKIM selectors resolve to public keys. | Do not change these records. A future mailing provider may require separate authentication; validate a real received test message's Authentication-Results after authorized setup. DNS records alone do not prove delivered-mail alignment. |
| Correspondence retention | Actual mailbox retention settings not inspected. | Owner/qualified adviser confirms retention and request handling before any stronger privacy promise. |

## Analytics option, not a purchase recommendation without review

[Plausible](https://plausible.io/) is a candidate for aggregate measurement. Its displayed 10k-pageview tier on 2026-09-06 listed Starter at $9/month and Business at $19/month; custom properties are listed under Business. Billing interval, limits, tax and final checkout price must be confirmed before approval. Do not budget a custom-properties implementation at the cheaper Starter price without checking feature compatibility.

The proposed fields are broad section/source/action/merchant, not health-topic URLs or product IDs. A vendor's ordinary automatic pageview/outbound tracker is not a drop-in implementation of this privacy contract. It can send full URLs and referrers. An adapter must explicitly map only the approved fields, avoid implicit URL/referrer leakage at the HTTP layer, document IP/connection processing and retention, and pass an actual network-payload review. If that cannot be achieved, choose a more suitable architecture or leave measurement off. Vendor privacy marketing is not legal clearance.

Sources: [Events API](https://plausible.io/docs/events-api), [Google Search Console reports](https://support.google.com/webmasters/answer/9133276?hl=en), [sitemap submission](https://support.google.com/webmasters/answer/7451001?hl=en). No API token was requested or embedded.

## Mailing-provider fit is a real gate

[MailerLite's content policy](https://www.mailerlite.com/help/is-there-any-content-that-mailerlite-doesn-t-allow) explicitly lists affiliate marketing and multi-level marketing among prohibited categories. Its [terms](https://www.mailerlite.com/legal/terms-of-service) must be considered for this partner-funded website. It is **not selected**; a low advertised price is not enough to establish eligibility. Do not disguise the business or remove disclosures to gain approval. Obtain a suitable provider's written eligibility determination before signup/activation.

No alternative provider is represented as approved. A business mailbox is not a substitute for consent records, subscriber suppression, and unsubscribe management.

Commercial messages need appropriate sender/advertising identification, a valid postal address and opt-out handling under the [FTC's business guidance](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business). Explicit consent is the proposed site standard; do not imply that this alone resolves every applicable law. A legitimate business mailing address or eligible registered mailbox can be considered rather than publishing a home address. Actual address not supplied and not invented.

## Activation acceptance criteria

1. Provider/account/terms/cost and business eligibility approved by the owner.
2. Data flow, retention, disclosure and applicable consent reviewed; public notice updated to match.
3. Authentication checked without replacing existing working email records blindly.
4. Double opt-in and unsubscribe tested with separately authorized controlled addresses; provider confirms subscription only after confirmation.
5. No unnecessary health details, raw query text, public subscriber records or client-side credentials.
6. Actual service logs/reporting verified; mocks explicitly distinguished.
7. Exact-SHA review candidate approved for deployment. Current candidate cannot activate services through a flag change.
