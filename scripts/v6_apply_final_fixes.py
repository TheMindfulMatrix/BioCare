#!/usr/bin/env python3
"""Apply the final V6 review-candidate fixes before the gated build."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Expected {label} block not found")
    return text.replace(old, new, 1)


def patch_finalize() -> None:
    path = ROOT / "scripts" / "v6_finalize_candidate.py"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '''        if not original_path.exists():
            original_path = source_path
            original_rel = source_rel

        with Image.open(original_path) as opened:
''',
        '''        if not original_path.exists():
            original_path = source_path
            original_rel = source_rel
        if not original_rel:
            original_rel = source_rel

        with Image.open(original_path) as opened:
''',
        "original image fallback",
    )
    text = replace_once(
        text,
        '        output_path = output_dir / f"{Path(original_rel).stem}.webp"\n',
        '        output_path = output_dir / f"{Path(original_rel or source_rel).stem}.webp"\n',
        "idempotent output path",
    )

    helper = '''

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
'''
    marker = '\n\ndef fetch_link(product: dict[str, Any]) -> LinkResult:\n'
    if "def attributed_source_url(product:" not in text:
        if marker not in text:
            raise SystemExit("fetch_link marker not found")
        text = text.replace(marker, helper + marker, 1)

    text = replace_once(
        text,
        '    attributed = str(price.get("affiliate_price_source") or original)\n',
        '    attributed = attributed_source_url(product)\n',
        "commerce attributed URL",
    )
    text = replace_once(
        text,
        '        record["verificationStatus"] = status\n',
        '        record["verificationStatus"] = status\n        record["status"] = "approved" if publish else "pending"\n',
        "public label status",
    )

    old_consolidate = '''        browser_result = browser_item.get("classification")
        item["browser_result"] = browser_result
        passed = item.get("classification") == "pass" or browser_result == "pass"
        if not passed:
            product = products.get(item.get("product_id"))
            if product:
                price = product.get("price") or {}
                original = item.get("original_url")
                if original:
                    price["affiliate_price_source"] = original
                    item["reverted"] = True
                    item["classification"] = "reverted_unverified"
                    reverted.append(item.get("product_name") or item.get("product_id"))
        else:
            item["classification"] = "pass"
'''
    new_consolidate = '''        browser_result = browser_item.get("classification")
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
'''
    text = replace_once(text, old_consolidate, new_consolidate, "commerce consolidation")
    path.write_text(text, encoding="utf-8")


def patch_build() -> None:
    path = ROOT / "scripts" / "build.py"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '    source = product["price"]["official_price_source"]\n',
        '    source = product["price"].get("affiliate_price_source") or product["price"]["official_price_source"]\n',
        "builder affiliate override",
    )
    path.write_text(text, encoding="utf-8")


def patch_validator() -> None:
    path = ROOT / "scripts" / "validate.py"
    text = path.read_text(encoding="utf-8")

    dimensions_anchor = '''def image_dimensions(path: Path) -> tuple[int, int] | None:
    if path.suffix.lower() == ".png":
        return png_dimensions(path)
    if path.suffix.lower() == ".webp":
        return webp_dimensions(path)
    return None
'''
    alpha_helper = '''def webp_has_alpha(path: Path) -> bool:
    """Return whether a WebP container declares or carries an alpha channel."""
    data = path.read_bytes()
    if len(data) < 21 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return False
    offset = 12
    while offset + 8 <= len(data):
        chunk = data[offset:offset + 4]
        size = int.from_bytes(data[offset + 4:offset + 8], "little")
        payload = offset + 8
        if chunk == b"VP8X" and payload < len(data):
            return bool(data[payload] & 0x10)
        if chunk == b"ALPH":
            return True
        if chunk == b"VP8L" and payload + 5 <= len(data) and data[payload] == 0x2F:
            bits = int.from_bytes(data[payload + 1:payload + 5], "little")
            return bool((bits >> 28) & 1)
        offset = payload + size + (size % 2)
    return False


'''
    if "def webp_has_alpha" not in text:
        if dimensions_anchor not in text:
            raise SystemExit("image_dimensions anchor not found")
        text = text.replace(dimensions_anchor, alpha_helper + dimensions_anchor, 1)

    old_provenance = '''                    production_filename = provenance.get("production_filename")
                    if production_filename:
                        check(production_filename == cutout.get("src"), f"{label}: provenance production filename mismatch")
                        if cutout_path.is_file() and "byte-for-byte copy" in provenance.get("alteration", ""):
                            check(sha256(cutout_path) == sha256(source_path), f"{label}: declared untouched production copy differs from official source")
'''
    new_provenance = '''                    production_filename = provenance.get("production_filename")
                    optimization = cutout.get("v6Optimization") or {}
                    if optimization:
                        original_rel = optimization.get("originalSrc")
                        original_path = ROOT / (original_rel or "missing")
                        check(product.get("manufacturer") == "Zinzino", f"{label}: V6 product-image derivatives are limited to Zinzino assets")
                        check(optimization.get("status") == "approved", f"{label}: V6 product-image derivative requires approved status")
                        check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(optimization.get("checkedDate", "")))), f"{label}: V6 product-image derivative requires a checked date")
                        check(bool(original_rel) and original_path.is_file(), f"{label}: V6 product-image derivative requires its original production asset")
                        check(cutout.get("src", "").startswith("assets/product-cutouts/zinzino-v6/"), f"{label}: approved V6 cutout must remain in the dedicated derivative directory")
                        check(cutout_path.suffix.lower() == ".webp", f"{label}: approved V6 product-image derivative must be WebP")
                        check("no upscale" in str(optimization.get("method", "")).lower(), f"{label}: V6 product-image method must declare no-upscale processing")
                        if cutout_path.is_file():
                            check(webp_has_alpha(cutout_path), f"{label}: approved V6 WebP must preserve alpha transparency")
                        if original_path.is_file() and cutout_path.is_file():
                            original_dimensions = image_dimensions(original_path)
                            derivative_dimensions = image_dimensions(cutout_path)
                            check(original_dimensions is not None, f"{label}: original production image dimensions could not be read")
                            check(derivative_dimensions is not None, f"{label}: V6 derivative dimensions could not be read")
                            if original_dimensions and derivative_dimensions:
                                check(derivative_dimensions[0] <= original_dimensions[0] and derivative_dimensions[1] <= original_dimensions[1], f"{label}: V6 product-image derivative must not upscale its original production asset")
                        if production_filename:
                            check(production_filename == original_rel, f"{label}: provenance original production filename mismatch")
                            if original_path.is_file() and "byte-for-byte copy" in provenance.get("alteration", ""):
                                check(sha256(original_path) == sha256(source_path), f"{label}: declared untouched original production copy differs from official source")
                    elif production_filename:
                        check(production_filename == cutout.get("src"), f"{label}: provenance production filename mismatch")
                        if cutout_path.is_file() and "byte-for-byte copy" in provenance.get("alteration", ""):
                            check(sha256(cutout_path) == sha256(source_path), f"{label}: declared untouched production copy differs from official source")
'''
    text = replace_once(text, old_provenance, new_provenance, "V6 derivative provenance")
    text = replace_once(
        text,
        '    check(\'assets/product-cutouts/zinzino/balance-test-basic-kit-910465.png\' in home, "Verified Balance cutout must remain the rendered foreground")\n',
        '    featured_cutout_src = featured.get("cutout", {}).get("src", "")\n    check(bool(featured_cutout_src) and featured_cutout_src in home, "The canonical featured Balance cutout must remain the rendered foreground")\n',
        "featured cutout assertion",
    )
    text = replace_once(
        text,
        '    source = product["price"]["official_price_source"]\n',
        '    source = product["price"].get("affiliate_price_source") or product["price"]["official_price_source"]\n',
        "validator affiliate override",
    )
    path.write_text(text, encoding="utf-8")


def populate_approved_sample_labels() -> None:
    path = ROOT / "content" / "product-labels.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("records", [])
    by_id = {record.get("product_id"): record for record in records}
    checked = "2026-08-19"
    samples = {
        "balanceoil-plus-300ml": {
            "serving_size": "2.5 tsp (12.5 mL) for 175 lb reference body weight",
            "servings_per_container": 24,
            "source_url": "https://zinzinowebstorage.blob.core.windows.net/product-sheets/BalanceOil-plus-en-US.pdf",
            "source_title": "BalanceOil+ US Product Sheet",
            "source_version": "en-US 2024-11-27",
            "ingredients": [("Calories",110,"cal"),("Total Fat",12,"g"),("Polyunsaturated Fat",3,"g"),("Monounsaturated Fat",5,"g"),("Vitamin D",20,"mcg"),("Omega-3 Fatty Acids",2500,"mg"),("EPA",1336,"mg"),("DHA",711,"mg"),("Olive Oil",4262,"mg"),("Oleic Acid (Omega-9)",3197,"mg"),("Olive Polyphenols",3.7,"mg")],
        },
        "zinobiotic-plus": {
            "serving_size": "1 scoop (6 g)", "servings_per_container": 30,
            "source_url": "https://zinzinowebstorage.blob.core.windows.net/product-sheets/ZinoBiotic-plus-en-US.pdf",
            "source_title": "ZinoBiotic+ US Product Sheet", "source_version": "en-US 2025-12-04",
            "ingredients": [("Calories",21,"cal"),("Total Carbohydrate",6,"g"),("Dietary Fiber",5,"g"),("Resistant Starch",2.5,"g"),("Beta Glucans",0.5,"g"),("Inulin",0.9,"g"),("Fructo-oligosaccharides",0.1,"g"),("Psyllium Seed Husk",0.3,"g"),("Guar Gum Fiber",0.12,"g")],
        },
        "xtend-plus": {
            "serving_size": "4 capsules", "servings_per_container": 15,
            "source_url": "https://zinzinowebstorage.blob.core.windows.net/product-sheets/Xtend-plus-en-US.pdf",
            "source_title": "Xtend+ US Product Sheet", "source_version": "en-US 2024-05-02",
            "ingredients": [("Vitamin C",80,"mg"),("Vitamin D3",20,"mcg"),("Vitamin E",3,"mg"),("Thiamin",0.27,"mg"),("Riboflavin",0.39,"mg"),("Niacin",4.94,"mg"),("Vitamin B6",0.25,"mg"),("Folate",57,"mcg"),("Vitamin B12",0.6,"mcg"),("Biotin",18,"mcg"),("Pantothenic Acid",1.84,"mg"),("Iron",4.2,"mg"),("Iodine",150,"mcg"),("Magnesium",180,"mg"),("Zinc",10,"mg"),("Selenium",82.5,"mcg"),("Copper",1,"mg"),("Manganese",2,"mg"),("Chromium",80,"mcg"),("Molybdenum",50,"mcg"),("Boron",3,"mg"),("Beta Glucans",200,"mg"),("Menaquinone",60,"mcg"),("Turmeric Root Extract",100,"mg"),("Coenzyme Q10",15,"mg"),("Tomato Fruit Extract",40,"mg"),("Olive Leaf Extract",500,"mg"),("Lutein",6,"mg"),("Zeaxanthin",6,"mg"),("Broccoli Aerial-parts Extract",50,"mg"),("Mixed Tocopherols and Tocotrienols",14.4,"mg"),("Seaweed Extract",200,"mg")],
        },
    }
    for product_id, sample in samples.items():
        record = by_id.get(product_id)
        if not record:
            raise SystemExit(f"Label record not found: {product_id}")
        record.update({"status":"verified_pending_approval","serving_size":sample["serving_size"],"servings_per_container":sample["servings_per_container"],"source_url":sample["source_url"],"source_title":sample["source_title"],"source_version":sample["source_version"],"checked_date":checked,"ingredients":[{"ingredient":name,"amount":amount,"unit":unit,"disclosed":True} for name,amount,unit in sample["ingredients"]],"notes":"Verified from the cited official manufacturer product sheet; approved continuation sample."})
    cell = by_id.get("biolimitless-cell-signals")
    if not cell:
        raise SystemExit("Cell Signals label record not found")
    cell.update({"status":"partial_verified_pending_approval","serving_size":None,"servings_per_container":None,"source_url":"https://biolimitless.com/shop/formulas/cell-signals/","source_title":"BioLimitless Cell Signals Official Product Page","source_version":None,"checked_date":checked,"ingredients":[{"ingredient":name,"amount":None,"unit":None,"disclosed":False,"note":"Amount not disclosed by manufacturer."} for name in ("Beta-Hydroxybutyrate","L-Carnosine","Methylcobalamin (Vitamin B12)","L-5-MTHF","Glycine","Phosphatidylserine","L-Tyrosine")],"notes":"Named ingredients are present on the official product page. Serving information and per-serving amounts remain unavailable and are not inferred."})
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    patch_finalize()
    patch_build()
    patch_validator()
    populate_approved_sample_labels()


if __name__ == "__main__":
    main()
