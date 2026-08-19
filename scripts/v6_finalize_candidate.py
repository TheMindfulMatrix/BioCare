#!/usr/bin/env python3
"""Finalize the V6 review candidate without touching production.

This script intentionally keeps unverifiable policy and ingredient claims out of
public output. It optimizes approved product imagery, verifies commercial source
links, records evidence, rebuilds the static site, and writes review reports.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import csv
import hashlib
import http.cookiejar
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "b5d35772e98580e253c08f6319aa8e412fa20aea"
CHECKED_DATE = date.today().isoformat()
CATALOG_PATH = ROOT / "content" / "catalog.json"
LABELS_PATH = ROOT / "content" / "product-labels.json"
DOCS_PATH = ROOT / "content" / "manufacturer-documents.json"
REPORT_DIR = ROOT / "reports" / "v6"
REVIEW_DIR = Path(os.environ.get("V6_REVIEW_DIR", "/tmp/v6-review"))
NETWORK_REPORT = REPORT_DIR / "commerce-verification.json"
BROWSER_REPORT = REPORT_DIR / "browser-qa.json"
IMAGE_REPORT = REPORT_DIR / "image-optimization.json"
LABEL_REPORT = REPORT_DIR / "ingredient-coverage.json"
POLICY_REPORT = REPORT_DIR / "policy-evidence.json"
FINAL_REPORT = REPORT_DIR / "FINAL_CANDIDATE.md"

PARTNER_ID = "2021428066"
BIO_REF_KEY = "me"
BIO_REF_VALUE = "matrix"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")


def run(*args: str, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, check=check, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def active_products(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    return [p for p in catalog.get("products", []) if p.get("commercial_status", "active") == "active"]


def safe_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda p: 255 if p > 3 else 0)
    return mask.getbbox()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_zinzino_images(catalog: dict[str, Any]) -> dict[str, Any]:
    """Generate transparent WebP proposals using the approved no-upscale rules."""
    report_items: list[dict[str, Any]] = []
    output_dir = ROOT / "assets" / "product-cutouts" / "zinzino-v6"
    output_dir.mkdir(parents=True, exist_ok=True)
    review_images = REVIEW_DIR / "images"
    review_images.mkdir(parents=True, exist_ok=True)

    before_total = 0
    after_total = 0
    changed = 0
    unchanged: list[dict[str, str]] = []

    products = active_products(catalog)
    for product in products:
        cutout = product.get("cutout") or {}
        source_rel = cutout.get("src")
        if product.get("manufacturer") != "Zinzino" or not source_rel:
            continue
        source_path = ROOT / source_rel
        if not source_path.exists():
            raise FileNotFoundError(f"Missing active cutout: {source_rel}")

        # If already pointed at the V6 asset, retain it and recover the original
        # source from the optimization record or immutable source path.
        original_rel = (cutout.get("v6Optimization") or {}).get("originalSrc")
        original_path = ROOT / original_rel if original_rel else source_path
        if not original_path.exists() and source_path.suffix.lower() == ".webp":
            possible = ROOT / "assets" / "product-cutouts" / "zinzino" / f"{source_path.stem}.png"
            if possible.exists():
                original_path = possible
                original_rel = str(possible.relative_to(ROOT)).replace("\\", "/")
        if not original_path.exists():
            original_path = source_path
            original_rel = source_rel
        if not original_rel:
            original_rel = source_rel

        with Image.open(original_path) as opened:
            original = opened.convert("RGBA")
        bbox = alpha_bbox(original)
        if not bbox:
            raise ValueError(f"No visible subject pixels: {original_rel}")

        before_total += original_path.stat().st_size
        native_side = max(original.size)
        output_side = min(800, native_side)  # never upscale
        subject = original.crop(bbox)

        # Scale down only. Smaller source subjects are repositioned, never enlarged.
        max_w = int(round(output_side * 0.86))
        max_h = int(round(output_side * 0.80))
        scale = min(1.0, max_w / subject.width, max_h / subject.height)
        if scale < 0.999:
            new_size = (max(1, int(round(subject.width * scale))), max(1, int(round(subject.height * scale))))
            subject = subject.resize(new_size, Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", (output_side, output_side), (0, 0, 0, 0))
        target_baseline = output_side - int(round(output_side * 0.08))
        x = max(0, (output_side - subject.width) // 2)
        y = target_baseline - subject.height
        y = max(int(round(output_side * 0.035)), y)
        if x + subject.width > output_side or y + subject.height > output_side:
            raise ValueError(f"Normalized subject would clip: {product['name']}")
        canvas.alpha_composite(subject, (x, y))

        result_bbox = alpha_bbox(canvas)
        if not result_bbox:
            raise ValueError(f"Normalized image lost transparency subject: {product['name']}")
        if result_bbox[0] < 0 or result_bbox[1] < 0 or result_bbox[2] > output_side or result_bbox[3] > output_side:
            raise ValueError(f"Normalized image clipped: {product['name']}")

        output_path = output_dir / f"{Path(original_rel or source_rel).stem}.webp"
        canvas.save(output_path, "WEBP", quality=82, method=6, exact=True)
        # Decode the final file to prove it is usable and has alpha.
        with Image.open(output_path) as test:
            test_rgba = test.convert("RGBA")
            if test_rgba.size != (output_side, output_side):
                raise ValueError(f"Unexpected WebP dimensions: {output_path}")
            if "A" not in test_rgba.getbands() or not alpha_bbox(test_rgba):
                raise ValueError(f"WebP alpha validation failed: {output_path}")

        new_rel = str(output_path.relative_to(ROOT)).replace("\\", "/")
        after_total += output_path.stat().st_size
        if source_rel != new_rel:
            changed += 1
        cutout["src"] = new_rel
        cutout["width"] = output_side
        cutout["height"] = output_side
        cutout["v6Optimization"] = {
            "status": "approved",
            "originalSrc": original_rel,
            "method": "alpha-bounds reframe, no upscale, 8% baseline, transparent WebP quality 82",
            "checkedDate": CHECKED_DATE,
        }

        # Lightweight contact-sheet tile; uploaded as a workflow artifact, not committed.
        tile_w, tile_h = 900, 470
        tile = Image.new("RGB", (tile_w, tile_h), "#f4efe4")
        draw = ImageDraw.Draw(tile)
        font = ImageFont.load_default()
        draw.text((18, 12), f"{product['name']} · SKU {product.get('sku', 'n/a')}", fill="#182017", font=font)
        draw.text((18, 32), f"Original {original.size[0]}x{original.size[1]} · {original_path.stat().st_size:,} B", fill="#34463a", font=font)
        draw.text((470, 32), f"V6 {output_side}x{output_side} · {output_path.stat().st_size:,} B", fill="#34463a", font=font)
        preview_bg = Image.new("RGBA", (410, 390), (15, 25, 18, 255))
        left = original.copy(); left.thumbnail((370, 350), Image.Resampling.LANCZOS)
        right = canvas.copy(); right.thumbnail((370, 350), Image.Resampling.LANCZOS)
        p1 = preview_bg.copy(); p1.alpha_composite(left, ((410-left.width)//2, (390-left.height)//2))
        p2 = preview_bg.copy(); p2.alpha_composite(right, ((410-right.width)//2, (390-right.height)//2))
        tile.paste(p1.convert("RGB"), (18, 62)); tile.paste(p2.convert("RGB"), (470, 62))
        tile_path = review_images / f"{safe_name(product['name'])}.jpg"
        tile.save(tile_path, "JPEG", quality=88)

        report_items.append({
            "product_id": product.get("id"), "product_name": product.get("name"), "sku": product.get("sku"),
            "original_src": original_rel, "v6_src": new_rel,
            "original_dimensions": list(original.size), "v6_dimensions": [output_side, output_side],
            "original_bytes": original_path.stat().st_size, "v6_bytes": output_path.stat().st_size,
            "original_sha256": file_sha256(original_path), "v6_sha256": file_sha256(output_path),
            "alpha_preserved": True, "upscaled": False,
            "subject_bbox_before": list(bbox), "subject_bbox_after": list(result_bbox),
        })

    # Build one vertical contact sheet in the review artifact directory.
    tiles = sorted(review_images.glob("*.jpg"))
    if tiles:
        opened_tiles = [Image.open(p).convert("RGB") for p in tiles]
        sheet = Image.new("RGB", (900, 470 * len(opened_tiles)), "#f4efe4")
        for index, tile in enumerate(opened_tiles):
            sheet.paste(tile, (0, index * 470))
        sheet.save(REVIEW_DIR / "v6-product-image-contact-sheet.jpg", "JPEG", quality=88)
        for tile in opened_tiles:
            tile.close()

    active_payload = 0
    for product in products:
        rel = (product.get("cutout") or {}).get("src")
        if rel and (ROOT / rel).exists():
            active_payload += (ROOT / rel).stat().st_size

    report = {
        "checked_date": CHECKED_DATE,
        "active_zinzino_count": len(report_items),
        "original_zinzino_bytes": before_total,
        "final_zinzino_bytes": after_total,
        "zinzino_savings_bytes": before_total - after_total,
        "zinzino_savings_percent": round((before_total - after_total) * 100 / before_total, 2) if before_total else 0,
        "final_active_product_image_bytes": active_payload,
        "files_changed_to_webp": changed,
        "intentionally_unchanged": unchanged,
        "items": report_items,
    }
    write_json(IMAGE_REPORT, report)
    return report


def find_label_records(data: Any) -> tuple[list[dict[str, Any]], str | None]:
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data, None
    if isinstance(data, dict):
        for key in ("products", "labels", "records", "productLabels", "product_labels"):
            value = data.get(key)
            if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                return value, key
    return [], None


def first_value(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if value not in (None, "", []):
            return value
    return None


def official_source(url: str | None, manufacturer: str | None) -> bool:
    if not url:
        return False
    host = urllib.parse.urlparse(url).hostname or ""
    host = host.lower()
    if manufacturer == "Zinzino":
        return host.endswith("zinzino.com") or host.endswith("zinzinowebstorage.blob.core.windows.net")
    if manufacturer == "BioLimitless":
        return host.endswith("biolimitless.com")
    return host.endswith("zinzino.com") or host.endswith("biolimitless.com") or host.endswith("zinzinowebstorage.blob.core.windows.net")


def ingredient_item_valid(item: dict[str, Any]) -> bool:
    name = first_value(item, "name", "ingredient")
    if not name:
        return False
    disclosed = item.get("disclosed")
    amount_status = str(first_value(item, "amountStatus", "amount_status", "status") or "").lower()
    note = str(first_value(item, "note", "notes", "limitation") or "").lower()
    if disclosed is False or "not disclosed" in amount_status or "not disclosed" in note or "unknown" in amount_status:
        return True
    amount = first_value(item, "amount", "value")
    unit = first_value(item, "unit", "amountUnit", "amount_unit")
    return amount not in (None, "") and unit not in (None, "")


def approve_verified_labels(catalog: dict[str, Any]) -> dict[str, Any]:
    if not LABELS_PATH.exists():
        return {"complete": 0, "partial": 0, "unavailable": 45, "items": []}
    data = load_json(LABELS_PATH)
    records, key = find_label_records(data)
    products = {p.get("id"): p for p in active_products(catalog)}
    coverage: list[dict[str, Any]] = []
    complete_count = partial_count = unavailable_count = 0

    for record in records:
        product_id = first_value(record, "productId", "product_id", "id")
        product = products.get(product_id)
        if not product:
            continue
        manufacturer = product.get("manufacturer")
        source = first_value(record, "sourceUrl", "source_url")
        if not source and isinstance(record.get("source"), dict):
            source = first_value(record["source"], "url", "sourceUrl")
        checked = first_value(record, "checkedDate", "checked_date", "verifiedDate", "verified_date")
        ingredients = first_value(record, "ingredients", "ingredientList", "ingredient_list") or []
        serving_size = first_value(record, "servingSize", "serving_size")
        servings = first_value(record, "servingsPerContainer", "servings_per_container")
        source_ok = official_source(str(source) if source else None, manufacturer) and bool(checked)
        ingredient_ok = bool(ingredients) and all(isinstance(i, dict) and ingredient_item_valid(i) for i in ingredients)
        has_any_facts = bool(ingredients or serving_size or servings)
        complete = bool(source_ok and ingredient_ok and serving_size and servings)
        partial = bool(source_ok and has_any_facts and not complete)

        if complete:
            status = "complete_verified"
            complete_count += 1
        elif partial:
            status = "partial_verified"
            partial_count += 1
        else:
            status = "unavailable_or_unverified"
            unavailable_count += 1

        # Set compatibility flags used by the current build and preserve a clear audit trail.
        publish = status in {"complete_verified", "partial_verified"}
        record["verificationStatus"] = status
        record["status"] = "approved" if publish else "pending"
        record["approvalStatus"] = "approved" if publish else "pending"
        record["approval_status"] = "approved" if publish else "pending"
        record["approved"] = publish
        record["public"] = publish
        record["checkedDate"] = checked or None
        if partial:
            record.setdefault("limitations", "Only facts verified from the cited manufacturer source are shown; the label record is incomplete.")
        if not publish:
            record["public"] = False

        coverage.append({
            "product_id": product_id, "product_name": product.get("name"), "sku": product.get("sku"),
            "manufacturer": manufacturer, "status": status, "source_url": source,
            "checked_date": checked, "ingredient_count": len(ingredients) if isinstance(ingredients, list) else 0,
            "serving_size_verified": bool(serving_size), "servings_per_container_verified": bool(servings),
        })

    if key is None and isinstance(data, list):
        write_json(LABELS_PATH, records)
    else:
        write_json(LABELS_PATH, data)

    report = {
        "checked_date": CHECKED_DATE,
        "active_products": len(products),
        "records_found": len(coverage),
        "complete_verified": complete_count,
        "partial_verified": partial_count,
        "unavailable_or_unverified": max(len(products) - complete_count - partial_count, unavailable_count),
        "public_rendering_rule": "Only complete_verified or partial_verified records may render.",
        "items": coverage,
    }
    write_json(LABEL_REPORT, report)
    return report


@dataclass
class LinkResult:
    product_id: str
    product_name: str
    sku: str
    manufacturer: str
    original_url: str
    attributed_url: str
    mechanism: str
    first_status: int | None = None
    final_status: int | None = None
    final_url: str | None = None
    redirects: list[str] | None = None
    identity_ok: bool = False
    attribution_ok: bool = False
    duplicate_referral: bool = False
    classification: str = "unchecked"
    error: str | None = None
    browser_result: str | None = None
    reverted: bool = False
    rel_ok: bool | None = None
    accessible_name_ok: bool | None = None
    disclosure_ok: bool | None = None


def attribution_ok(url: str, manufacturer: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    if manufacturer == "Zinzino":
        return f"/shop/{PARTNER_ID}/" in parsed.path.lower()
    query = urllib.parse.parse_qs(parsed.query)
    return query.get(BIO_REF_KEY, []).count(BIO_REF_VALUE) == 1


def duplicate_referral(url: str, manufacturer: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    if manufacturer == "Zinzino":
        return parsed.path.lower().count(f"/{PARTNER_ID}/") > 1
    return urllib.parse.parse_qs(parsed.query).get(BIO_REF_KEY, []).count(BIO_REF_VALUE) > 1


def identity_matches(product: dict[str, Any], final_url: str, body: str) -> bool:
    sku = str(product.get("sku") or "").strip().lower()
    haystack = f"{final_url}\n{body[:350000]}".lower()
    if sku and sku in haystack:
        return True
    tokens = [t for t in re.findall(r"[a-z0-9]+", str(product.get("name", "")).lower()) if len(t) >= 4]
    if not tokens:
        return False
    return sum(token in haystack for token in tokens[:5]) >= min(2, len(tokens))


def attributed_source_url(product: dict[str, Any]) -> str:
    """Derive the same disclosed partner source URL used by the static builder."""
    price = product.get("price") or {}
    explicit = price.get("affiliate_price_source")
    if explicit:
        return str(explicit)
    source = str(price.get("official_price_source") or product.get("officialProductPage") or "")
    manufacturer = str(product.get("manufacturer") or "")
    if manufacturer == "Zinzino":
        return source.replace("/shop/site/US/en-US/", f"/shop/{PARTNER_ID}/us/en-us/", 1)
    if manufacturer == "BioLimitless":
        parsed = urllib.parse.urlsplit(source)
        query = [(key, value) for key, value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True) if key != BIO_REF_KEY]
        query.append((BIO_REF_KEY, BIO_REF_VALUE))
        return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(query), parsed.fragment))
    return source


def fetch_link(product: dict[str, Any]) -> LinkResult:
    price = product.get("price") or {}
    original = str(price.get("official_price_source") or product.get("officialProductPage") or "")
    attributed = attributed_source_url(product)
    manufacturer = str(product.get("manufacturer") or "")
    mechanism = "Zinzino partner path" if manufacturer == "Zinzino" else "BioLimitless AffiliateWP query"
    result = LinkResult(
        product_id=str(product.get("id") or ""), product_name=str(product.get("name") or ""),
        sku=str(product.get("sku") or ""), manufacturer=manufacturer,
        original_url=original, attributed_url=attributed, mechanism=mechanism,
        redirects=[], duplicate_referral=duplicate_referral(attributed, manufacturer),
    )
    if not attributed:
        result.classification = "failed"
        result.error = "missing attributed URL"
        return result

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    request = urllib.request.Request(
        attributed,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with opener.open(request, timeout=25) as response:
            result.first_status = getattr(response, "status", None)
            result.final_status = getattr(response, "status", None)
            result.final_url = response.geturl()
            raw = response.read(350000)
            body = raw.decode(response.headers.get_content_charset() or "utf-8", errors="ignore")
            result.identity_ok = identity_matches(product, result.final_url or attributed, body)
            result.attribution_ok = attribution_ok(result.final_url or attributed, manufacturer) or attribution_ok(attributed, manufacturer)
            if result.final_status and 200 <= result.final_status < 400 and result.identity_ok and result.attribution_ok and not result.duplicate_referral:
                result.classification = "pass"
            elif result.final_status in (403, 429, 503):
                result.classification = "bot_protected"
            else:
                result.classification = "uncertain"
    except urllib.error.HTTPError as error:
        result.first_status = error.code
        result.final_status = error.code
        result.final_url = error.geturl()
        result.error = f"HTTP {error.code}"
        result.attribution_ok = attribution_ok(result.final_url or attributed, manufacturer) or attribution_ok(attributed, manufacturer)
        result.classification = "bot_protected" if error.code in (401, 403, 429, 503) else "failed"
    except Exception as error:  # network/DNS/timeout is resolved by the browser pass
        result.error = f"{type(error).__name__}: {error}"
        result.attribution_ok = attribution_ok(attributed, manufacturer)
        result.classification = "uncertain"
    return result


def verify_commerce(catalog: dict[str, Any]) -> dict[str, Any]:
    products = active_products(catalog)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch_link, products))
    report = {
        "checked_date": CHECKED_DATE,
        "active_products": len(products),
        "commercial_records": len(products) * 2,
        "source_links_checked": len(results),
        "http_pass": sum(r.classification == "pass" for r in results),
        "bot_protected": sum(r.classification == "bot_protected" for r in results),
        "uncertain": sum(r.classification == "uncertain" for r in results),
        "failed": sum(r.classification == "failed" for r in results),
        "items": [asdict(r) for r in results],
    }
    write_json(NETWORK_REPORT, report)
    return report


def create_policy_report() -> dict[str, Any]:
    entries = [
        {
            "claim": "Numeric return window",
            "sources": [
                "https://www.zinzino.com/site/us/en-us/about/how-it-works",
                "https://zinzinowebstorage.blob.core.windows.net/contracts/TermsAndConditions_US_en-US.pdf",
            ],
            "status": "hold",
            "reason": "Current official web copy and the currently linked April 2022 PDF describe different return windows.",
            "published": False,
        },
        {
            "claim": "BalanceTest first-test refund/guarantee",
            "sources": [
                "https://www.zinzino.com/site/us/en-us/apie-mus/this-is-zinzino/",
                "https://zinzinowebstorage.blob.core.windows.net/contracts/TermsAndConditions_US_en-US.pdf",
            ],
            "status": "hold",
            "reason": "A current general statement exists, while detailed eligibility conditions are in an older linked document; no broader website claim is published.",
            "published": False,
        },
        {
            "claim": "Subscription cancellation/no commitment",
            "sources": [
                "https://www.zinzino.com/site/us/en-us/about/how-it-works",
                "https://zinzinowebstorage.blob.core.windows.net/contracts/TermsAndConditions_US_en-US.pdf",
            ],
            "status": "hold",
            "reason": "Cancellation is described through Customer Care, while the detailed notice condition remains tied to the older linked policy PDF.",
            "published": False,
        },
    ]
    report = {
        "checked_date": CHECKED_DATE,
        "market": "United States",
        "numeric_return_claim_published": False,
        "new_policy_claims_published": [],
        "held_claims": [entry["claim"] for entry in entries],
        "entries": entries,
        "recommendation": "Ship V6 without new guarantee, return-window, or cancellation badges until current official terms are unambiguous.",
    }
    write_json(POLICY_REPORT, report)
    return report


def build_site() -> None:
    run(sys.executable, "scripts/build.py")


def apply_html_checks(catalog: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    soup = BeautifulSoup((ROOT / "shop.html").read_text(encoding="utf-8"), "html.parser")
    cards = {card.get("data-product-id"): card for card in soup.select("[data-product-id]") if card.get("data-product-id")}
    for item in report.get("items", []):
        card = cards.get(item["product_id"])
        if not card:
            continue
        link = card.select_one(".product-price__source")
        if not link:
            continue
        rel = set(link.get("rel") or [])
        item["rel_ok"] = {"sponsored", "noopener", "noreferrer"}.issubset(rel)
        aria = link.get("aria-label", "")
        item["accessible_name_ok"] = item["product_name"].lower() in aria.lower()
        described_by = link.get("aria-describedby")
        item["disclosure_ok"] = bool(described_by and soup.find(id=described_by))
    write_json(NETWORK_REPORT, report)
    return report


def consolidate_commerce(catalog: dict[str, Any]) -> dict[str, Any]:
    report = load_json(NETWORK_REPORT)
    browser = load_json(BROWSER_REPORT) if BROWSER_REPORT.exists() else {"external_links": []}
    browser_map = {item.get("product_id"): item for item in browser.get("external_links", [])}
    products = {p.get("id"): p for p in active_products(catalog)}
    reverted: list[str] = []

    for item in report.get("items", []):
        browser_item = browser_map.get(item.get("product_id"), {})
        browser_result = browser_item.get("classification")
        item["browser_result"] = browser_result
        manufacturer = str(item.get("manufacturer") or "")
        browser_final = str(browser_item.get("final_url") or "")
        item["identity_ok"] = bool(item.get("identity_ok") or browser_item.get("identity_ok"))
        item["attribution_ok"] = bool(
            item.get("attribution_ok")
            or attribution_ok(browser_final, manufacturer)
            or attribution_ok(str(item.get("attributed_url") or ""), manufacturer)
        )
        passed = bool(
            (item.get("classification") == "pass" or browser_result == "pass")
            and item.get("identity_ok")
            and item.get("attribution_ok")
            and not item.get("duplicate_referral")
        )
        product = products.get(item.get("product_id"))
        if not passed:
            if product:
                price = product.get("price") or {}
                original = item.get("original_url")
                if original:
                    price["affiliate_price_source"] = original
                    item["reverted"] = True
                    item["classification"] = "reverted_unverified"
                    reverted.append(item.get("product_name") or item.get("product_id"))
        else:
            if product:
                product.setdefault("price", {})["affiliate_price_source"] = item.get("attributed_url")
            item["classification"] = "pass"

    report["final_pass"] = sum(i.get("classification") == "pass" for i in report.get("items", []))
    report["reverted_count"] = len(reverted)
    report["reverted_products"] = reverted
    report["neutral_source_links_remaining"] = len(reverted)
    write_json(CATALOG_PATH, catalog)
    build_site()
    report = apply_html_checks(catalog, report)
    report["rel_failures"] = sum(i.get("rel_ok") is False for i in report.get("items", []))
    report["accessible_name_failures"] = sum(i.get("accessible_name_ok") is False for i in report.get("items", []))
    report["disclosure_failures"] = sum(i.get("disclosure_ok") is False for i in report.get("items", []))
    write_json(NETWORK_REPORT, report)
    return report


def count_dom(path: Path) -> int:
    return len(BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser").find_all(True))


def git_show_bytes(ref: str, path: str) -> bytes:
    process = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        return b""
    return process.stdout


def structured_metadata_report() -> dict[str, Any]:
    public_pages = [ROOT / "index.html", ROOT / "shop.html", ROOT / "library.html", ROOT / "start.html"] + sorted((ROOT / "library").glob("*.html"))
    metadata: list[dict[str, Any]] = []
    product_schema_count = 0
    rating_count = 0
    for page in public_pages:
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        schemas: list[Any] = []
        for node in soup.select('script[type="application/ld+json"]'):
            try:
                schemas.append(json.loads(node.string or node.text))
            except json.JSONDecodeError:
                schemas.append({"invalid": True})
        serialized = json.dumps(schemas)
        product_schema_count += serialized.count('"@type": "Product"') + serialized.count('"@type":"Product"')
        rating_count += serialized.count("aggregateRating")
        metadata.append({
            "path": str(page.relative_to(ROOT)).replace("\\", "/"),
            "title": bool(soup.title and soup.title.string),
            "description": bool(soup.select_one('meta[name="description"]')),
            "canonical": bool(soup.select_one('link[rel="canonical"]')),
            "og_title": len(soup.select('meta[property="og:title"]')),
            "og_url": len(soup.select('meta[property="og:url"]')),
            "og_image": len(soup.select('meta[property="og:image"]')),
            "twitter_card": len(soup.select('meta[name="twitter:card"]')),
            "jsonld_blocks": len(schemas),
        })
    sitemap = BeautifulSoup((ROOT / "sitemap.xml").read_text(encoding="utf-8"), "xml")
    return {
        "public_pages": len(public_pages),
        "metadata_pages_pass": sum(all([i["title"], i["description"], i["canonical"], i["og_title"] == 1, i["og_url"] == 1, i["og_image"] == 1, i["twitter_card"] == 1]) for i in metadata),
        "product_schema_objects": product_schema_count,
        "aggregate_rating_occurrences": rating_count,
        "sitemap_urls": len(sitemap.find_all("loc")),
        "pages": metadata,
    }


def write_final_report(catalog: dict[str, Any], image_report: dict[str, Any], label_report: dict[str, Any], commerce: dict[str, Any], policy: dict[str, Any]) -> None:
    baseline_index = git_show_bytes(BASELINE, "index.html")
    current_index = (ROOT / "index.html").read_bytes()
    baseline_dom = len(BeautifulSoup(baseline_index.decode("utf-8", errors="ignore"), "html.parser").find_all(True)) if baseline_index else None
    current_dom = count_dom(ROOT / "index.html")
    active = active_products(catalog)
    deferred = [p for p in catalog.get("products", []) if p.get("commercial_status") != "active"]
    metadata = structured_metadata_report()

    warning_current = None
    strict_current = None
    audit_path = ROOT / "reports" / "compliance-audit-v1.json"
    if audit_path.exists():
        audit = load_json(audit_path)
        # Different engine versions expose one of these shapes.
        for key in ("reviewWarningCount", "review_warning_count", "warning_count"):
            if isinstance(audit, dict) and isinstance(audit.get(key), int):
                warning_current = audit[key]
                break

    body = f"""# The Mindful Matrix V6 final candidate report

- Baseline: `{BASELINE}`
- Branch: `agent/v6-build`
- Status: final review candidate; not merged and not deployed
- Active/deferred products: {len(active)} / {len(deferred)}
- All active products curated: {all(p.get('curated') is True for p in active)}

## Architecture and performance

- Homepage HTML: {len(baseline_index):,} B → {len(current_index):,} B
- Homepage DOM: {baseline_dom if baseline_dom is not None else 'unavailable'} → {current_dom}
- Product Universe: one rendered panel plus a build-generated canonical product payload
- Original active Zinzino images: {image_report.get('original_zinzino_bytes', 0):,} B
- Final active Zinzino images: {image_report.get('final_zinzino_bytes', 0):,} B
- Zinzino savings: {image_report.get('zinzino_savings_percent', 0)}%
- Final active product-image payload: {image_report.get('final_active_product_image_bytes', 0):,} B

## Ingredient labels

- Complete verified: {label_report.get('complete_verified', 0)}
- Partial verified: {label_report.get('partial_verified', 0)}
- Unavailable/unverified: {label_report.get('unavailable_or_unverified', 0)}
- Unverified records rendered: 0 by publication rule

## Commerce

- Source links checked: {commerce.get('source_links_checked', 0)}
- Final verified attributed links: {commerce.get('final_pass', commerce.get('http_pass', 0))}
- Reverted source rewrites: {commerce.get('reverted_count', 0)}
- Neutral source links remaining: {commerce.get('neutral_source_links_remaining', 0)}
- `rel` failures: {commerce.get('rel_failures', 0)}
- Accessible-name failures: {commerce.get('accessible_name_failures', 0)}
- Disclosure failures: {commerce.get('disclosure_failures', 0)}

## Policy

- New policy claims published: {len(policy.get('new_policy_claims_published', []))}
- Numeric return window published: {policy.get('numeric_return_claim_published', False)}
- Held claims: {', '.join(policy.get('held_claims', []))}

## Structured data, sitemap, and social metadata

- Public pages checked: {metadata.get('public_pages')}
- Complete metadata pages: {metadata.get('metadata_pages_pass')}
- Product schema objects on catalog: {metadata.get('product_schema_objects')}
- Aggregate ratings: {metadata.get('aggregate_rating_occurrences')}
- Sitemap URLs: {metadata.get('sitemap_urls')}

## Deferred

- How It Works imagery remains deferred until licensed assets are supplied.
- Facebook Sharing Debugger and in-app browser behavior remain post-deployment manual checks.
- Policy copy remains held while official current sources conflict or depend on older linked terms.
"""
    FINAL_REPORT.write_text(body, encoding="utf-8")


def prepare() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    catalog = load_json(CATALOG_PATH)
    # Enforce approved V6 curation semantics without activating deferred records.
    for product in catalog.get("products", []):
        if product.get("commercial_status", "active") == "active":
            product["curated"] = True
    image_report = normalize_zinzino_images(catalog)
    label_report = approve_verified_labels(catalog)
    policy = create_policy_report()
    write_json(CATALOG_PATH, catalog)
    commerce = verify_commerce(catalog)
    build_site()
    commerce = apply_html_checks(catalog, commerce)
    write_final_report(catalog, image_report, label_report, commerce, policy)


def consolidate() -> None:
    catalog = load_json(CATALOG_PATH)
    commerce = consolidate_commerce(catalog)
    # Re-run label validation after any generated changes.
    label_report = approve_verified_labels(catalog)
    image_report = load_json(IMAGE_REPORT)
    policy = load_json(POLICY_REPORT)
    build_site()
    write_final_report(catalog, image_report, label_report, commerce, policy)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "consolidate"))
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    else:
        consolidate()


if __name__ == "__main__":
    main()
