#!/usr/bin/env python3
"""Create a deterministic, non-approving triage of the compliance backlog."""

from __future__ import annotations

import argparse
import json
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()
    normal = validate_compliance(strict=False)
    strict = validate_compliance(strict=True)
    strict_only = sorted(set(strict["errors"]) - set(normal["errors"]))
    items = [{"priority": index, "category": category(message), "message": message} for index, message in enumerate(strict_only, start=1)]
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
        "# V10.2 compliance triage",
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
    lines.extend(["", "## Prioritized human-review queue", ""])
    lines.extend(f"{item['priority']}. **{item['category']}** — {item['message']}" for item in items)
    args.markdown_output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("normal_hard_gate_errors", "normal_review_warnings", "strict_unresolved_items", "category_counts")}, indent=2))


if __name__ == "__main__":
    main()
