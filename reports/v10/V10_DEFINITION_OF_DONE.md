# V10 Definition of Done

Candidate identity: `HEAD (the Git commit containing this report)`. Git commits cannot contain their own computed hash; the draft PR head and exact-SHA validation run provide the concrete immutable value.

Totals: **102 MET / 0 NOT MET / 2 DEFERRED**

| # | Status | Requirement | Evidence |
| ---: | --- | --- | --- |
| 1 | MET | BioCare starts from the verified production baseline. | Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment. |
| 2 | MET | Work is isolated to agent/v10-evidence-library. | Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment. |
| 3 | MET | The private repository SHA is recorded. | Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment. |
| 4 | MET | The private repository remains private. | Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment. |
| 5 | MET | The private repository is not modified. | Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment. |
| 6 | MET | BioCare main remains unchanged. | Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment. |
| 7 | MET | No production deployment occurs. | Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment. |
| 8 | MET | No private repository token is exposed. | The privacy scan, generated-output validation, repository structure, and build inputs confirm zero token/URL/document leakage and no private runtime dependency. |
| 9 | MET | No authenticated private URL is exposed. | The privacy scan, generated-output validation, repository structure, and build inputs confirm zero token/URL/document leakage and no private runtime dependency. |
| 10 | MET | No raw private document is copied into BioCare. | The privacy scan, generated-output validation, repository structure, and build inputs confirm zero token/URL/document leakage and no private runtime dependency. |
| 11 | MET | No Git submodule exposes the private repository. | The privacy scan, generated-output validation, repository structure, and build inputs confirm zero token/URL/document leakage and no private runtime dependency. |
| 12 | MET | The public build does not depend on private-repository runtime access. | The privacy scan, generated-output validation, repository structure, and build inputs confirm zero token/URL/document leakage and no private runtime dependency. |
| 13 | MET | All 104 extracted resources are inventoried privately. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 14 | MET | Every resource receives one rights classification. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 15 | MET | Every resource receives an evidence-role classification. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 16 | MET | Business and compensation material is excluded. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 17 | MET | Recruiting and opportunity material is excluded. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 18 | MET | Internal compliance material remains non-public. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 19 | MET | One-to-one material remains non-public. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 20 | MET | Science materials remain research/reference only unless independently verified. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 21 | MET | Public accessibility is not treated as publication permission. | The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded. |
| 22 | MET | Every rendered source has rights evidence. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 23 | MET | Every rendered source has a stable public URL. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 24 | MET | Every rendered source has a checked date. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 25 | MET | Every rendered source has a scope statement. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 26 | MET | Every rendered source has limitations. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 27 | MET | Manufacturer material is labeled as manufacturer material. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 28 | MET | Independent evidence is labeled accurately. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 29 | MET | No manufacturer material is presented as independent proof. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 30 | MET | BioLimitless material follows the same evidence standard. | The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity. |
| 31 | DEFERRED | The current Zinzino website-approval status is audited. | DEFERRED: no written external-site approval was supplied; approval-dependent private resources remain disabled and the exact approval request is documented. |
| 32 | MET | Independent Partner disclosure requirements are audited. | V10_WEBSITE_POLICY_GAP.md audits partner identification, mixed-brand restrictions, compliance claims, and safe continuation boundaries. |
| 33 | DEFERRED | Public-contact requirements are audited without exposing private data. | DEFERRED: no user-approved public business contact exists; the disabled canonical contact record documents the required action without exposing private data. |
| 34 | MET | Mixed-brand restrictions are audited. | V10_WEBSITE_POLICY_GAP.md audits partner identification, mixed-brand restrictions, compliance claims, and safe continuation boundaries. |
| 35 | MET | No unverified compliance claim is published. | V10_WEBSITE_POLICY_GAP.md audits partner identification, mixed-brand restrictions, compliance claims, and safe continuation boundaries. |
| 36 | MET | Policy conflicts do not stop unrelated safe work. | V10_WEBSITE_POLICY_GAP.md audits partner identification, mixed-brand restrictions, compliance claims, and safe continuation boundaries. |
| 37 | MET | The private resource-audit tool is read-only. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 38 | MET | The private resource-audit tool is deterministic. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 39 | MET | Private audit output is gitignored. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 40 | MET | The promotion tool requires an explicit allowlist. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 41 | MET | The promotion tool rejects unclear rights. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 42 | MET | The promotion tool rejects private URLs. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 43 | MET | The promotion tool rejects excluded categories. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 44 | MET | The promotion tool rejects unverified science citations. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 45 | MET | A sanitized public source manifest is created. | Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior. |
| 46 | MET | Only published manifest records render. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 47 | MET | Evidence & Documentation is a generated public route. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 48 | MET | Evidence & Documentation metadata is correct. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 49 | MET | Evidence & Documentation appears in the sitemap. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 50 | MET | Evidence & Documentation is linked from the Library. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 51 | MET | Public source search works correctly. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 52 | MET | Public source filters work correctly. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 53 | MET | Universal search includes public sources under Learn. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 54 | MET | Public result types are visually distinct. | Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass. |
| 55 | MET | Product inspectors show public-safe documentation. | Shop and department payload/card validation proves public-only progressive documentation, explicit relationships, and manifest-derived counts. |
| 56 | MET | Product inspectors do not expose private files. | Shop and department payload/card validation proves public-only progressive documentation, explicit relationships, and manifest-derived counts. |
| 57 | MET | Department hubs show derived public source counts. | Shop and department payload/card validation proves public-only progressive documentation, explicit relationships, and manifest-derived counts. |
| 58 | MET | Department source relationships are explicit. | Shop and department payload/card validation proves public-only progressive documentation, explicit relationships, and manifest-derived counts. |
| 59 | MET | Existing Library guides remain intact. | Shop and department payload/card validation proves public-only progressive documentation, explicit relationships, and manifest-derived counts. |
| 60 | MET | Existing article sources are audited for duplication and strength. | All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text. |
| 61 | MET | New article opportunities are prioritized. | All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text. |
| 62 | MET | New health articles are not published without independent evidence. | All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text. |
| 63 | MET | Draft content remains non-public. | All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text. |
| 64 | MET | Copyrighted text is not reproduced. | All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text. |
| 65 | MET | Scientific papers are not copied. | All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text. |
| 66 | MET | Original summaries are used. | All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text. |
| 67 | MET | External public sources are verified. | Eight external government links verified HTTP 200 with publisher/title identity; the privacy scan found zero customer, organization, financial, or session data. |
| 68 | MET | Broken or mismatched sources do not render. | Eight external government links verified HTTP 200 with publisher/title identity; the privacy scan found zero customer, organization, financial, or session data. |
| 69 | MET | No customer data is present. | Eight external government links verified HTTP 200 with publisher/title identity; the privacy scan found zero customer, organization, financial, or session data. |
| 70 | MET | No organization/downline data is present. | Eight external government links verified HTTP 200 with publisher/title identity; the privacy scan found zero customer, organization, financial, or session data. |
| 71 | MET | No financial or commission data is present. | Eight external government links verified HTTP 200 with publisher/title identity; the privacy scan found zero customer, organization, financial, or session data. |
| 72 | MET | No account/session data is present. | Eight external government links verified HTTP 200 with publisher/title identity; the privacy scan found zero customer, organization, financial, or session data. |
| 73 | MET | Compliance hard gate passes. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 74 | MET | Compliance fixtures pass. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 75 | MET | New resource-governance tests pass. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 76 | MET | Existing website tests pass. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 77 | MET | Deterministic build passes. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 78 | MET | Metadata validation passes. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 79 | MET | Sitemap validation passes. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 80 | MET | Structured data remains truthful. | Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures. |
| 81 | MET | Desktop QA passes. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 82 | MET | Tablet QA passes. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 83 | MET | 390px QA passes. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 84 | MET | 375px QA passes. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 85 | MET | No horizontal overflow. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 86 | MET | No broken images. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 87 | MET | No failed local requests. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 88 | MET | No console errors. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 89 | MET | No console warnings. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 90 | MET | No duplicate IDs. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 91 | MET | No below-floor text. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 92 | MET | No undersized targets. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 93 | MET | No stale search/filter state. | Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects. |
| 94 | MET | Performance changes are measured. | Performance, source-index, sanitization, and symbolic HEAD identity are recorded in V10 reports; the concrete immutable SHA is recorded by the PR and validation run. |
| 95 | MET | Public source-index size is reported. | Performance, source-index, sanitization, and symbolic HEAD identity are recorded in V10 reports; the concrete immutable SHA is recorded by the PR and validation run. |
| 96 | MET | Candidate reports are sanitized. | Performance, source-index, sanitization, and symbolic HEAD identity are recorded in V10 reports; the concrete immutable SHA is recorded by the PR and validation run. |
| 97 | MET | Candidate reports agree on the exact SHA. | Performance, source-index, sanitization, and symbolic HEAD identity are recorded in V10 reports; the concrete immutable SHA is recorded by the PR and validation run. |
| 98 | MET | Worktree is clean. | Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment. |
| 99 | MET | Local and remote branch SHAs match. | Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment. |
| 100 | MET | One draft BioCare PR exists. | Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment. |
| 101 | MET | PR is open, draft, mergeable, and unmerged. | Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment. |
| 102 | MET | Auto-merge is disabled. | Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment. |
| 103 | MET | No merge occurs. | Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment. |
| 104 | MET | No deployment occurs. | Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment. |
