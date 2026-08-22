#!/usr/bin/env python3
"""Generate canonical V11.2 inventory and relationship reports."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/v11.2"
SHA = "56347ababaea5af5e088d26d52f61df807ae4f70"

catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
library = json.loads((ROOT / "content/library.json").read_text(encoding="utf-8"))
discovery = json.loads((ROOT / "content/discovery.json").read_text(encoding="utf-8"))
sources = json.loads((ROOT / "content/resources/public-sources.json").read_text(encoding="utf-8"))["records"]
active = [p for p in catalog["products"] if p.get("commercial_status") == "active"]
departments = {d["intentId"]: d for d in discovery["departments"]}
published = {a["slug"] for a in library["articles"] if a.get("status") == "published"}

products = []
relationships = []
for product in active:
    department = departments[product["intent"]]
    articles = [slug for slug in department["articleSlugs"] if slug in published]
    exact = [s["id"] for s in sources if s.get("status") == "published" and product["id"] in s.get("product_ids", [])]
    context = [s["id"] for s in sources if s.get("status") == "published" and product["intent"] in s.get("department_ids", []) and s["id"] not in exact]
    products.append({"id": product["id"], "name": product["name"], "route": f'products/{product["id"]}.html', "department": department["slug"], "generated": True})
    relationships.append({"productId": product["id"], "departmentId": product["intent"], "articleSlugs": articles, "productSpecificSourceIds": exact, "departmentContextSourceIds": context, "boundary": "department context is not product-specific evidence"})

(OUT / "V11_2_PRODUCT_PAGES.json").write_text(json.dumps({"candidateSha": SHA, "count": len(products), "records": products}, indent=2) + "\n", encoding="utf-8", newline="\n")
(OUT / "V11_2_RELATIONSHIP_MAP.json").write_text(json.dumps({"candidateSha": SHA, "schemaVersion": "1.0", "count": len(relationships), "records": relationships}, indent=2) + "\n", encoding="utf-8", newline="\n")
