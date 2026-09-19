"""One-time image export; never required by the canonical site build."""
import argparse
from pathlib import Path
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    destination = Path(__file__).resolve().parents[1] / "assets/images/academy"
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("everyday-matrix", "partner-practice"):
        with Image.open(args.source / f"{name}-editorial.png") as original:
            for width in (640, 1280):
                image = original.convert("RGB")
                image = image.resize((width, round(width * original.height / original.width)), Image.Resampling.LANCZOS)
                path = destination / f"{name}-{width}.webp"
                image.save(path, "WEBP", quality=82, method=6)
                print(f"{path.name}: {image.size}; {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
