#!/usr/bin/env python3
"""Generate the public-safe V10 product documentation coverage report."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "v10" / "V10_PRODUCT_DOCUMENTATION_COVERAGE.json"


def main() -> None:
    shop = (ROOT / "shop.html").read_text(encoding="utf-8")
    match = re.search(r'<script type="application/json" data-shop-catalog>(.*?)</script>', shop, flags=re.S)
    if not match:
        raise SystemExit("Shop catalog payload missing")
    payload = json.loads(match.group(1))
    products = payload["products"]
    records = [
        {
            "product_id": product["id"],
            "manufacturer": product["manufacturer"],
            "department": product["intent"],
            "label_state": product["label"]["state"],
            "related_guide": (product.get("relatedEducation") or {}).get("href"),
            "public_source_count": len(product.get("documentation", [])),
            "public_source_ids": [source["id"] for source in product.get("documentation", [])],
            "relationship_states": sorted({source["relationship"] for source in product.get("documentation", [])}),
        }
        for product in products
    ]
    report = {
        "schema_version": "1.0",
        "checked_date": "2026-08-21",
        "active_product_count": len(products),
        "products_with_public_context": sum(bool(record["public_source_count"]) for record in records),
        "products_without_public_context": sum(not record["public_source_count"] for record in records),
        "label_state_totals": dict(sorted(Counter(record["label_state"] for record in records).items())),
        "manufacturer_totals": dict(sorted(Counter(record["manufacturer"] for record in records).items())),
        "boundary": "Public sources provide product-specific or department context; department context is not product evidence.",
        "records": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in report.items() if key != "records"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
