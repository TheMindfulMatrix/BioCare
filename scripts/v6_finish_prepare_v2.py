#!/usr/bin/env python3
"""Idempotent V6 finish-pass product-image and hero optimization."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "content" / "catalog.json"
REPORT = ROOT / "reports" / "v6" / "image-finish-pass.json"
CHECKED = "2026-08-20"
PREVIOUS_TOTAL = 1_405_208
ORIGINAL_V5_1_TOTAL = 4_643_596
TARGET_TOTAL = 800_000
AGGRESSIVE = {
    "balanceoil-plus-premium",
    "balanceoil-tutti-frutti",
    "balanceoil-plus-100ml-6pcs",
    "x-gold-plus",
    "phycosci-plus-x20",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def active_products(data: dict) -> list[dict]:
    return [
        product
        for product in data["products"]
        if product.get("commercial_status", "active") == "active"
    ]


def original_source(product: dict, current_path: Path) -> tuple[str, Path]:
    cutout = product["cutout"]
    if product["manufacturer"] == "Zinzino":
        rel = (cutout.get("v6Optimization") or {}).get("originalSrc")
    else:
        rel = (cutout.get("finishImageOptimization") or {}).get("originalSrc")
    path = ROOT / rel if rel else current_path
    if not path.exists():
        return cutout["src"], current_path
    return str(rel), path


def encode_product(product: dict) -> dict:
    cutout = product["cutout"]
    current_path = ROOT / cutout["src"]
    manufacturer = product["manufacturer"]
    original_rel, source_path = original_source(product, current_path)

    if manufacturer == "Zinzino":
        output_path = current_path
        cap = 480 if product["id"] in AGGRESSIVE else 520
        quality = 30 if product["id"] in AGGRESSIVE else 40
        mode = "RGBA"
    else:
        output_dir = ROOT / "assets" / "product-cutouts" / "biolimitless-v6"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{source_path.stem}.webp"
        cap = 540
        quality = 50
        mode = "RGB"

    with Image.open(source_path) as opened:
        source = opened.convert(mode)
        native = source.size
        scale = min(1.0, cap / max(native))
        target = (max(1, round(native[0] * scale)), max(1, round(native[1] * scale)))
        rendered = source.resize(target, Image.Resampling.LANCZOS) if target != native else source.copy()
        rendered.save(output_path, "WEBP", quality=quality, method=4, exact=True)

    with Image.open(output_path) as final:
        final.load()
        final_size = final.size
        if manufacturer == "Zinzino":
            if "A" not in final.getbands() or final.getchannel("A").getextrema() == (255, 255):
                raise ValueError(f"Transparency validation failed: {output_path}")

    new_rel = str(output_path.relative_to(ROOT)).replace("\\", "/")
    cutout["src"] = new_rel
    cutout["width"], cutout["height"] = final_size
    if manufacturer == "Zinzino":
        meta = cutout.setdefault("v6Optimization", {})
        meta.update(
            {
                "status": "approved",
                "originalSrc": original_rel,
                "method": "approved alpha-bounds normalization followed by ratio-preserving WebP downscale/recompression; no upscale",
                "finishPassCheckedDate": CHECKED,
                "finishPassBytes": output_path.stat().st_size,
                "finishPassDimensions": list(final_size),
                "finishPassQuality": quality,
            }
        )
    else:
        cutout["finishImageOptimization"] = {
            "status": "approved",
            "checkedDate": CHECKED,
            "originalSrc": original_rel,
            "method": "ratio-preserving WebP downscale/recompression; no upscale",
            "quality": quality,
            "dimensions": list(final_size),
            "bytes": output_path.stat().st_size,
        }

    return {
        "product_id": product["id"],
        "name": product["name"],
        "manufacturer": manufacturer,
        "original_src": original_rel,
        "src": new_rel,
        "native_dimensions": list(native),
        "before_bytes": source_path.stat().st_size,
        "bytes": output_path.stat().st_size,
        "dimensions": list(final_size),
        "quality": quality,
        "sha256": sha256(output_path),
        "alpha_preserved": manufacturer == "Zinzino",
        "upscaled": final_size[0] > native[0] or final_size[1] > native[1],
        "aggressive": product["id"] in AGGRESSIVE,
    }


def optimize_hero(data: dict) -> dict:
    product = next(p for p in active_products(data) if p["id"] == "balance-basic-kit")
    source = ROOT / "assets" / "artwork" / "shelf" / "balance-test-basic-kit-cinematic.webp"
    output = ROOT / "assets" / "artwork" / "shelf" / "balance-test-basic-kit-cinematic-v6.webp"
    with Image.open(source) as opened:
        image = opened.convert("RGB")
        width, height = image.size
        crop_height = round(width * 5 / 4)
        center_y = round(height * 0.53)
        top = max(0, min(height - crop_height, center_y - crop_height // 2))
        image.crop((0, top, width, top + crop_height)).resize(
            (800, 1000), Image.Resampling.LANCZOS
        ).save(output, "WEBP", quality=68, method=4)
    rel = str(output.relative_to(ROOT)).replace("\\", "/")
    product.setdefault("artwork", {}).update(
        {
            "src": rel,
            "width": 800,
            "height": 1000,
            "status": "approved Mindful Matrix cinematic background",
            "v6Optimization": {
                "status": "approved-finish-pass",
                "originalSrc": str(source.relative_to(ROOT)).replace("\\", "/"),
                "method": "crop to rendered 4:5 ratio using approved 50% / 53% focal position; resize to 800x1000 WebP",
                "checkedDate": CHECKED,
                "bytes": output.stat().st_size,
            },
        }
    )
    return {
        "original_src": str(source.relative_to(ROOT)).replace("\\", "/"),
        "original_dimensions": [1024, 1536],
        "original_bytes": source.stat().st_size,
        "final_src": rel,
        "final_dimensions": [800, 1000],
        "final_bytes": output.stat().st_size,
        "source_ratio": round(1024 / 1536, 6),
        "final_ratio": 0.8,
        "crop_focal_position": "50% 53%",
    }


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    items = [encode_product(product) for product in active_products(data)]
    hero = optimize_hero(data)
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if any(item["upscaled"] for item in items):
        raise ValueError("Finish pass attempted to upscale an active product image")
    zinzino = [item for item in items if item["manufacturer"] == "Zinzino"]
    biolimitless = [item for item in items if item["manufacturer"] == "BioLimitless"]
    total = sum(item["bytes"] for item in items)
    report = {
        "checked_date": CHECKED,
        "previous_candidate_total_bytes": PREVIOUS_TOTAL,
        "original_v5_1_total_bytes": ORIGINAL_V5_1_TOTAL,
        "zinzino_bytes": sum(item["bytes"] for item in zinzino),
        "biolimitless_bytes": sum(item["bytes"] for item in biolimitless),
        "total_active_bytes": total,
        "target_bytes": TARGET_TOTAL,
        "target_met": total <= TARGET_TOTAL,
        "reduction_from_original_percent": round((ORIGINAL_V5_1_TOTAL - total) * 100 / ORIGINAL_V5_1_TOTAL, 2),
        "reduction_from_previous_candidate_percent": round((PREVIOUS_TOTAL - total) * 100 / PREVIOUS_TOTAL, 2),
        "hero": hero,
        "aggressive_five": [item for item in items if item["aggressive"]],
        "largest_remaining": sorted(items, key=lambda item: item["bytes"], reverse=True)[:12],
        "items": items,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("zinzino_bytes", "biolimitless_bytes", "total_active_bytes", "target_met")}, indent=2))
    if not report["target_met"]:
        raise SystemExit(f"Active product-image payload is {total:,} bytes; target is {TARGET_TOTAL:,}")


if __name__ == "__main__":
    main()
