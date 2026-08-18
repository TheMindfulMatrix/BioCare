#!/usr/bin/env python3
"""Check draft copy or the catalog against Compliance Engine v1."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from compliance_engine import ComplianceEngine, ROOT, split_sentences


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to classify")
    source.add_argument("--file", type=Path, help="Draft text, JSON, or HTML file to scan")
    source.add_argument("--catalog", action="store_true", help="Scan content/catalog.json")
    parser.add_argument(
        "--context",
        choices=["COMMERCIAL_PRODUCT", "EDITORIAL", "SOCIAL_COMMERCIAL", "MLM_RECRUITMENT", "MIXED_PUBLIC"],
        default="SOCIAL_COMMERCIAL",
        help="Review context for --text and plain-text --file inputs",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    engine = ComplianceEngine()
    if args.catalog:
        findings = engine.scan_json(ROOT / "content" / "catalog.json")
    elif args.file:
        path = args.file.resolve()
        if path.suffix.lower() == ".json":
            findings = engine.scan_json(path)
        elif path.suffix.lower() == ".html":
            findings = engine.scan_html(path)
        else:
            findings = [
                finding
                for index, sentence in enumerate(split_sentences(path.read_text(encoding="utf-8")), 1)
                if (finding := engine.analyze_text(sentence, context=args.context, location=f"{path}:{index}"))
            ]
    else:
        findings = [
            finding
            for index, sentence in enumerate(split_sentences(args.text), 1)
            if (finding := engine.analyze_text(sentence, context=args.context, location=f"inline:{index}"))
        ]

    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2, ensure_ascii=False))
        return
    if not findings:
        print("No claim-bearing text detected by Compliance Engine v1.")
        return
    for index, finding in enumerate(findings, 1):
        print(f"CLAIM {index}: {finding.exact_text}")
        print(f"TYPE: {finding.claim_type}")
        print(f"RISK: {finding.risk} / {finding.classification}")
        print(f"MATCHED RULE: {', '.join(finding.matched_rules)}")
        print(f"EVIDENCE STATUS: {finding.evidence_status}")
        print(f"REQUIRED DISCLOSURE: {', '.join(finding.required_disclosure) if finding.required_disclosure else 'NONE IDENTIFIED'}")
        print(f"RECOMMENDATION: {finding.required_action}")
        if finding.registry_claim_ids:
            print(f"REGISTERED CLAIM ID(S): {', '.join(finding.registry_claim_ids)}")
        print()


if __name__ == "__main__":
    main()
