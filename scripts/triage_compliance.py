#!/usr/bin/env python3
"""Create a deterministic, non-approving triage of the compliance backlog."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from validate_compliance import validate_compliance

ROOT = Path(__file__).resolve().parents[1]


def category(message: str) -> str:
    lowered = message.casefold()
    if "lacks evidence" in lowered or "evidence" in lowered and "missing" in lowered:
        return "evidence/context gap"
    if "expired" in lowered or "date" in lowered and "invalid" in lowered:
        return "objective tooling or stale-record review"
    if "unresolved yellow commercial claim" in lowered or "human review" in lowered:
        return "human review required"
    if "unresolved strict-mode yellow claim" in lowered or "unregistered" in lowered:
        return "registered wording candidate"
    if "deferred" in lowered or "non-public" in lowered:
        return "deferred or non-public content"
    return "human review required"


def _catalog() -> dict:
    return json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))


def _product_for_claim(claim_id: str, catalog: dict) -> dict | None:
    marker = "CLAIM_PRODUCT_"
    suffix = "_DESCRIPTION"
    if not claim_id.startswith(marker) or not claim_id.endswith(suffix):
        return None
    normalized = claim_id[len(marker) : -len(suffix)].casefold().replace("_", "-")
    return next((product for product in catalog.get("products", []) if product.get("id", "").casefold() == normalized), None)


def triage_item(message: str, queue_position: int, catalog: dict) -> dict:
    path_match = re.match(r"^(?P<file>[^:]+):(?P<locator>\$[^:]*): (?P<reason>.*?): (?P<wording>.*)$", message)
    claim_match = re.match(r"^(?P<claim>CLAIM_PRODUCT_[A-Z0-9_]+_DESCRIPTION): (?P<reason>.*)$", message)
    source_file = "compliance claim registry"
    locator = claim_match.group("claim") if claim_match else "unparsed"
    wording = None
    reason = message
    priority = "Priority 3"
    visibility = "internal policy or metadata review"
    evidence = "Confirm context before registering or revising wording."
    next_action = "Retain in the human-review queue; do not suppress automatically."
    meaning_change = "No automatic wording change proposed."
    tags = [category(message)]
    if path_match:
        source_file = path_match.group("file")
        locator = path_match.group("locator")
        wording = path_match.group("wording")
        reason = path_match.group("reason")
        if any(token in locator for token in (".description", ".whyItsHere")):
            priority = "Priority 2"
            visibility = "public product, discovery, or campaign copy"
            evidence = "Verify canonical label/manufacturer facts and independent evidence boundaries."
            next_action = "Human-review the public wording and preserve meaning before any later copy-only change."
            meaning_change = "Possible; editorial and compliance approval required."
        elif ".cutout.alt" in locator:
            visibility = "public accessibility metadata"
            tags.append("metadata or alt text")
        elif ".contentPolicy" in locator:
            tags.append("accepted or registered legacy wording")
    elif claim_match:
        product = _product_for_claim(claim_match.group("claim"), catalog)
        source_file = "content/catalog.json"
        locator = f"$.products[id={product.get('id') if product else 'unresolved'}].description"
        wording = product.get("description") if product else None
        reason = claim_match.group("reason")
        priority = "Priority 1"
        visibility = "public commercial product description"
        evidence = "Requires product-specific manufacturer verification; ingredient evidence cannot validate the finished product."
        next_action = "Review against the current official product source before proposing any narrow copy change."
        meaning_change = "Likely if rewritten; manufacturer and compliance review required."
        tags.extend(["requires manufacturer verification", "requires evidence review"])
    return {
        "queue_position": queue_position,
        "priority": priority,
        "category": category(message),
        "source_file": source_file,
        "locator": locator,
        "existing_wording": wording,
        "reason_flagged": reason,
        "public_visibility": visibility,
        "evidence_relationship": evidence,
        "recommended_next_action": next_action,
        "wording_change_would_alter_meaning": meaning_change,
        "tags": sorted(set(tags)),
        "raw_message": message,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()
    normal = validate_compliance(strict=False)
    strict = validate_compliance(strict=True)
    strict_only = sorted(set(strict["errors"]) - set(normal["errors"]))
    catalog = _catalog()
    items = [triage_item(message, index, catalog) for index, message in enumerate(strict_only, start=1)]
    counts = Counter(item["category"] for item in items)
    result = {
        "schema_version": "1.0.0",
        "normal_hard_gate_errors": len(normal["errors"]),
        "normal_review_warnings": len(normal["warnings"]),
        "strict_unresolved_items": len(strict_only),
        "category_counts": dict(sorted(counts.items())),
        "items": items,
        "policy": "Triage only. No warning is approved, waived, or reclassified as compliant by this report.",
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "# V11.3 compliance triage",
        "",
        "This is a prioritization aid, not an approval or weakening of the compliance gate.",
        "",
        f"- Normal hard-gate errors: **{len(normal['errors'])}**",
        f"- Review warnings: **{len(normal['warnings'])}**",
        f"- Strict unresolved items: **{len(strict_only)}**",
        "",
        "## Categories",
        "",
    ]
    lines.extend(f"- {name}: **{count}**" for name, count in sorted(counts.items()))
    lines.extend(["", "## Priority 1 and 2 human-review queue", ""])
    for item in items:
        if item["priority"] not in {"Priority 1", "Priority 2"}:
            continue
        lines.extend([
            f"### {item['queue_position']}. {item['priority']} — {item['source_file']} {item['locator']}",
            "",
            f"- Existing wording: {json.dumps(item['existing_wording'])}",
            f"- Reason flagged: {item['reason_flagged']}",
            f"- Public visibility: {item['public_visibility']}",
            f"- Evidence relationship: {item['evidence_relationship']}",
            f"- Recommended next action: {item['recommended_next_action']}",
            f"- Meaning impact: {item['wording_change_would_alter_meaning']}",
            "",
        ])
    lines.extend(["## Priority 3 queue", ""])
    lines.extend(f"{item['queue_position']}. **{item['category']}** — {item['raw_message']}" for item in items if item["priority"] == "Priority 3")
    args.markdown_output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("normal_hard_gate_errors", "normal_review_warnings", "strict_unresolved_items", "category_counts")}, indent=2))


if __name__ == "__main__":
    main()
