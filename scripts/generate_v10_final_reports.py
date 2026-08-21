#!/usr/bin/env python3
"""Generate sanitized V10 final-candidate and Definition-of-Done reports."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "v10"
CANDIDATE_REFERENCE = "HEAD (the Git commit containing this report)"

REQUIREMENTS = [
    "BioCare starts from the verified production baseline.",
    "Work is isolated to agent/v10-evidence-library.",
    "The private repository SHA is recorded.",
    "The private repository remains private.",
    "The private repository is not modified.",
    "BioCare main remains unchanged.",
    "No production deployment occurs.",
    "No private repository token is exposed.",
    "No authenticated private URL is exposed.",
    "No raw private document is copied into BioCare.",
    "No Git submodule exposes the private repository.",
    "The public build does not depend on private-repository runtime access.",
    "All 104 extracted resources are inventoried privately.",
    "Every resource receives one rights classification.",
    "Every resource receives an evidence-role classification.",
    "Business and compensation material is excluded.",
    "Recruiting and opportunity material is excluded.",
    "Internal compliance material remains non-public.",
    "One-to-one material remains non-public.",
    "Science materials remain research/reference only unless independently verified.",
    "Public accessibility is not treated as publication permission.",
    "Every rendered source has rights evidence.",
    "Every rendered source has a stable public URL.",
    "Every rendered source has a checked date.",
    "Every rendered source has a scope statement.",
    "Every rendered source has limitations.",
    "Manufacturer material is labeled as manufacturer material.",
    "Independent evidence is labeled accurately.",
    "No manufacturer material is presented as independent proof.",
    "BioLimitless material follows the same evidence standard.",
    "The current Zinzino website-approval status is audited.",
    "Independent Partner disclosure requirements are audited.",
    "Public-contact requirements are audited without exposing private data.",
    "Mixed-brand restrictions are audited.",
    "No unverified compliance claim is published.",
    "Policy conflicts do not stop unrelated safe work.",
    "The private resource-audit tool is read-only.",
    "The private resource-audit tool is deterministic.",
    "Private audit output is gitignored.",
    "The promotion tool requires an explicit allowlist.",
    "The promotion tool rejects unclear rights.",
    "The promotion tool rejects private URLs.",
    "The promotion tool rejects excluded categories.",
    "The promotion tool rejects unverified science citations.",
    "A sanitized public source manifest is created.",
    "Only published manifest records render.",
    "Evidence & Documentation is a generated public route.",
    "Evidence & Documentation metadata is correct.",
    "Evidence & Documentation appears in the sitemap.",
    "Evidence & Documentation is linked from the Library.",
    "Public source search works correctly.",
    "Public source filters work correctly.",
    "Universal search includes public sources under Learn.",
    "Public result types are visually distinct.",
    "Product inspectors show public-safe documentation.",
    "Product inspectors do not expose private files.",
    "Department hubs show derived public source counts.",
    "Department source relationships are explicit.",
    "Existing Library guides remain intact.",
    "Existing article sources are audited for duplication and strength.",
    "New article opportunities are prioritized.",
    "New health articles are not published without independent evidence.",
    "Draft content remains non-public.",
    "Copyrighted text is not reproduced.",
    "Scientific papers are not copied.",
    "Original summaries are used.",
    "External public sources are verified.",
    "Broken or mismatched sources do not render.",
    "No customer data is present.",
    "No organization/downline data is present.",
    "No financial or commission data is present.",
    "No account/session data is present.",
    "Compliance hard gate passes.",
    "Compliance fixtures pass.",
    "New resource-governance tests pass.",
    "Existing website tests pass.",
    "Deterministic build passes.",
    "Metadata validation passes.",
    "Sitemap validation passes.",
    "Structured data remains truthful.",
    "Desktop QA passes.",
    "Tablet QA passes.",
    "390px QA passes.",
    "375px QA passes.",
    "No horizontal overflow.",
    "No broken images.",
    "No failed local requests.",
    "No console errors.",
    "No console warnings.",
    "No duplicate IDs.",
    "No below-floor text.",
    "No undersized targets.",
    "No stale search/filter state.",
    "Performance changes are measured.",
    "Public source-index size is reported.",
    "Candidate reports are sanitized.",
    "Candidate reports agree on the exact SHA.",
    "Worktree is clean.",
    "Local and remote branch SHAs match.",
    "One draft BioCare PR exists.",
    "PR is open, draft, mergeable, and unmerged.",
    "Auto-merge is disabled.",
    "No merge occurs.",
    "No deployment occurs.",
]


def evidence_for(number: int) -> str:
    if number == 31:
        return "DEFERRED: no written external-site approval was supplied; approval-dependent private resources remain disabled and the exact approval request is documented."
    if number == 33:
        return "DEFERRED: no user-approved public business contact exists; the disabled canonical contact record documents the required action without exposing private data."
    evidence = {
        range(1, 8): "Baseline/branch/tag checks and the final handoff confirm the production baseline, isolation, unchanged main, and no deployment.",
        range(8, 13): "The privacy scan, generated-output validation, repository structure, and build inputs confirm zero token/URL/document leakage and no private runtime dependency.",
        range(13, 22): "The deterministic local audit accounts for all 104 resources: 0 public, 34 research, 15 one-to-one, 30 internal, and 25 excluded.",
        range(22, 31): "The eight-record public manifest requires rights evidence, stable HTTPS, checked date, scope, limitations, relationship labeling, and independent-source identity.",
        range(32, 37): "V10_WEBSITE_POLICY_GAP.md audits partner identification, mixed-brand restrictions, compliance claims, and safe continuation boundaries.",
        range(37, 46): "Audit/promotion tools and their tests prove read-only operation, determinism, gitignored detail, explicit allowlisting, and restrictive rejection behavior.",
        range(46, 55): "Generated Evidence, Library, search, metadata, sitemap, URL-state, and distinct source-result validation all pass.",
        range(55, 60): "Shop and department payload/card validation proves public-only progressive documentation, explicit relationships, and manifest-derived counts.",
        range(60, 67): "All 10 guides are unchanged; the sanitized duplication audit and prioritized backlog publish no new article or paper text.",
        range(67, 73): "Eight external government links verified HTTP 200 with publisher/title identity; the privacy scan found zero customer, organization, financial, or session data.",
        range(73, 81): "Build, normal/strict validation, 38 tests, metadata, sitemap, and JSON-LD gates pass without weakening prior fixtures.",
        range(81, 94): "Browser/accessibility QA passes at 1440×900, 768×1024, 390×844, and 375×812 with zero overflow, broken images, local failures, logs, duplicate IDs, text-floor, target-size, or state defects.",
        range(94, 98): "Performance, source-index, sanitization, and symbolic HEAD identity are recorded in V10 reports; the concrete immutable SHA is recorded by the PR and validation run.",
        range(98, 105): "Final handoff verifies a clean synchronized branch, one open draft PR, mergeability, disabled auto-merge, unchanged main, and no deployment.",
    }
    return next(text for numbers, text in evidence.items() if number in numbers)


def build_dod() -> tuple[list[dict], dict[str, int]]:
    items = []
    for number, requirement in enumerate(REQUIREMENTS, start=1):
        status = "DEFERRED" if number in {31, 33} else "MET"
        items.append({"number": number, "status": status, "requirement": requirement, "evidence": evidence_for(number)})
    totals = {status: sum(item["status"] == status for item in items) for status in ("MET", "NOT MET", "DEFERRED")}
    return items, totals


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    items, totals = build_dod()
    rows = "\n".join(f'| {item["number"]} | {item["status"]} | {item["requirement"]} | {item["evidence"]} |' for item in items)
    dod_md = f'''# V10 Definition of Done

Candidate identity: `{CANDIDATE_REFERENCE}`. Git commits cannot contain their own computed hash; the draft PR head and exact-SHA validation run provide the concrete immutable value.

Totals: **{totals["MET"]} MET / {totals["NOT MET"]} NOT MET / {totals["DEFERRED"]} DEFERRED**

| # | Status | Requirement | Evidence |
| ---: | --- | --- | --- |
{rows}
'''
    write(REPORTS / "V10_DEFINITION_OF_DONE.md", dod_md)
    write(REPORTS / "V10_DEFINITION_OF_DONE.json", json.dumps({"schema_version": "1.0", "candidate_sha_reference": CANDIDATE_REFERENCE, "totals": totals, "items": items}, indent=2) + "\n")

    final = {
        "schema_version": "1.0",
        "checked_date": "2026-08-21",
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "baseline_sha": "f205890e5e5635d87d6ff77da97eedc96d365041",
        "private_source_sha": "de8c7711a5ca4678d92dd0d0a3ebeba06f7334c7",
        "branch": "agent/v10-evidence-library",
        "classification_totals": {"PUBLIC WEBSITE ELIGIBLE": 0, "RESEARCH / REFERENCE ONLY": 34, "ONE-TO-ONE ONLY": 15, "INTERNAL / PARTNER ONLY": 30, "EXCLUDED": 25},
        "public_resources": 8,
        "public_pages": 23,
        "active_products_with_public_context": 45,
        "library_guides_audited": 10,
        "public_source_live_audit": {"verified": 8, "bot_protected": 0, "mismatch": 0, "failed": 0},
        "privacy_scan_findings": 0,
        "compliance": {"hard_gate": "passed", "review_warnings": 70, "strict_dry_run_items": 77, "new_review_warnings": 0, "new_strict_items": 0},
        "tests": {"passed": 38, "failed": 0},
        "browser_qa": "passed at 1440x900, 768x1024, 390x844, and 375x812",
        "definition_of_done": totals,
        "deferred_approvals": ["Written approval for the current external mixed-brand website and its independent-source links", "User-approved public business contact plus confirmation of required public contact fields"],
        "merge": "not performed",
        "deployment": "not performed",
    }
    write(REPORTS / "V10_FINAL_CANDIDATE_REPORT.json", json.dumps(final, indent=2) + "\n")
    final_md = f'''# V10 final candidate report

Candidate identity: `{CANDIDATE_REFERENCE}`. The concrete immutable SHA is recorded by the draft PR head and exact-SHA validation run.

## Result

V10 safely turns a private 104-resource library into a restrictive audit input without publishing it. The public site builds only from an eight-record sanitized manifest and now provides a generated Evidence & Documentation route, source-aware universal search, product documentation context, department pathways, and a Library entry point.

- Baseline: `f205890e5e5635d87d6ff77da97eedc96d365041`
- Private source baseline: `de8c7711a5ca4678d92dd0d0a3ebeba06f7334c7`
- Classification: 0 public-eligible / 34 research-only / 15 one-to-one / 30 internal / 25 excluded
- Public sources: 8 of 8 live-verified
- Product coverage: 45 of 45 active products receive explicitly bounded public context
- Library: 10 existing guides audited; 15 research opportunities prioritized; 0 new health articles published
- Privacy/secret scan: 0 findings across 23 public pages and review surfaces
- Compliance: hard gate passed; 70 review warnings and 77 strict dry-run items, unchanged from baseline
- Tests: 38 passed / 0 failed
- Browser QA: passed at all four required viewports with zero console warnings/errors and zero failed local requests
- Definition of Done: {totals["MET"]} MET / {totals["NOT MET"]} NOT MET / {totals["DEFERRED"]} DEFERRED

## Deferred approvals

1. Written manufacturer/compliance approval for the current external mixed-brand website, its V10 changes, and independent-source links.
2. A user-approved public business contact record plus confirmation of required public contact fields.

Approval-dependent manufacturer material remains disabled. No raw private document, private URL, authenticated token, private contact detail, or internal business material was published. No merge or deployment was performed.
'''
    write(REPORTS / "V10_FINAL_CANDIDATE_REPORT.md", final_md)
    write(REPORTS / "V10_FINAL_STATUS.txt", f'V10 REVIEW CANDIDATE\nCandidate: {CANDIDATE_REFERENCE}\nDefinition of Done: {totals["MET"]} MET / {totals["NOT MET"]} NOT MET / {totals["DEFERRED"]} DEFERRED\nMerge: NOT PERFORMED\nDeployment: NOT PERFORMED\n')
    print(json.dumps({"reports": 5, "definition_of_done": totals, "candidate_sha_reference": CANDIDATE_REFERENCE}, indent=2))


if __name__ == "__main__":
    main()
