"""Reproduce the codec-only desktop hero derivative from its immutable source.

Pillow is needed only for this optional asset-maintenance command, not build.py.
No resampling, sharpening, background removal, or generated pixels are applied.
"""

from pathlib import Path
import hashlib


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/source-products/zinzino/balance-test-basic-kit/balance-test-basic-kit-910465-main.png"
DESTINATION = ROOT / "assets/product-cutouts/hero/balance-test-basic-kit-650.webp"
SOURCE_SHA256 = "b0cf5653d294e964b849076667f554bab71e01a64733ec1ab6544e0f381cb5e1"


def main():
    from PIL import Image

    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("Source changed: re-review the official product identity before generating.")
    with Image.open(SOURCE) as image:
        if image.size != (650, 650):
            raise SystemExit("Unexpected native resolution; refusing to resize.")
        DESTINATION.parent.mkdir(parents=True, exist_ok=True)
        image.save(DESTINATION, "WEBP", quality=90, method=6, exact=True)
    print(f"{DESTINATION.relative_to(ROOT)}: {DESTINATION.stat().st_size} bytes; native 650 x 650")


if __name__ == "__main__":
    main()
