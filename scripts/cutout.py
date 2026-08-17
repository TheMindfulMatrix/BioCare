#!/usr/bin/env python3
"""Create normalized product cutouts without altering source assets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

DEFAULT_CANVAS = 560
DEFAULT_MARGIN = 0.06
MODEL = "isnet-general-use"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

MATTING = {
    "alpha_matting": True,
    "alpha_matting_foreground_threshold": 248,
    "alpha_matting_background_threshold": 12,
    "alpha_matting_erode_size": 9,
}


def trim_to_subject(image: Image.Image) -> Image.Image:
    """Crop transparent excess while retaining every non-transparent pixel."""
    bbox = image.getchannel("A").getbbox()
    return image.crop(bbox) if bbox else image


def fit_square(image: Image.Image, canvas: int, margin: float) -> Image.Image:
    """Fit an RGBA image proportionally on a centered transparent square."""
    usable = int(canvas * (1 - margin * 2))
    width, height = image.size
    scale = min(usable / width, usable / height)
    resized = image.resize(
        (max(1, round(width * scale)), max(1, round(height * scale))),
        Image.Resampling.LANCZOS,
    )
    output = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    output.paste(
        resized,
        ((canvas - resized.width) // 2, (canvas - resized.height) // 2),
        resized,
    )
    return output


def has_transparency(image: Image.Image) -> bool:
    """Return whether the source includes any transparent or partial pixels."""
    return "A" in image.getbands() and image.getchannel("A").getextrema()[0] < 255


def remove_background(image: Image.Image, session: object) -> Image.Image:
    """Remove a source background with the approved model and matting values."""
    from rembg import remove

    detection_input = Image.new("RGB", image.size, "white")
    detection_input.paste(image, mask=image.getchannel("A"))
    result = remove(detection_input, session=session, **MATTING)
    return result.convert("RGBA")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize product photos as centered transparent PNG cutouts."
    )
    parser.add_argument("input_folder", type=Path, help="Folder containing source images")
    parser.add_argument("output_folder", type=Path, help="Separate folder for generated PNG cutouts")
    parser.add_argument(
        "--canvas-size",
        type=int,
        default=DEFAULT_CANVAS,
        help=f"Square output size in pixels (default: {DEFAULT_CANVAS})",
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=DEFAULT_MARGIN,
        help=f"Transparent margin on each side as a fraction (default: {DEFAULT_MARGIN})",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--force-rembg",
        action="store_true",
        help="Remove a residual background even when the source already has an alpha channel",
    )
    mode.add_argument(
        "--skip-rembg",
        action="store_true",
        help="Require useful source transparency and only trim/fit the image",
    )
    parser.add_argument(
        "--output-name",
        help="Filename for a single input image (must end in .png)",
    )
    return parser


def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not args.input_folder.is_dir():
        parser.error(f"Input folder does not exist: {args.input_folder}")
    if args.canvas_size < 1:
        parser.error("--canvas-size must be at least 1")
    if not 0 <= args.margin < 0.5:
        parser.error("--margin must be at least 0 and less than 0.5")
    if args.input_folder.resolve() == args.output_folder.resolve():
        parser.error("Input and output folders must be different; source assets are immutable")
    if args.output_name and Path(args.output_name).suffix.lower() != ".png":
        parser.error("--output-name must end in .png")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args, parser)

    sources = sorted(
        path
        for path in args.input_folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not sources:
        parser.error(f"No supported images found in {args.input_folder}")
    if args.output_name and len(sources) != 1:
        parser.error("--output-name can only be used when the input folder contains one image")

    args.output_folder.mkdir(parents=True, exist_ok=True)
    session = None

    for source in sources:
        with Image.open(source) as opened:
            source_size = opened.size
            source_has_alpha = has_transparency(opened)
            image = opened.convert("RGBA")

        use_rembg = args.force_rembg or not source_has_alpha
        if args.skip_rembg and not source_has_alpha:
            parser.error(f"{source.name} is opaque; background removal is required")

        if use_rembg:
            try:
                from rembg import new_session
            except ImportError:
                parser.error(
                    'Background removal requires: pip install "rembg[cpu]" pillow'
                )
            if session is None:
                session = new_session(MODEL)
            image = remove_background(image, session)
            method = f"rembg:{MODEL}"
        else:
            method = "existing-alpha"

        trimmed = trim_to_subject(image)
        output = fit_square(trimmed, args.canvas_size, args.margin)
        filename = args.output_name or f"{source.stem}.png"
        destination = args.output_folder / filename
        if destination.resolve() == source.resolve():
            parser.error(f"Refusing to overwrite source asset: {source}")
        output.save(destination, format="PNG", optimize=True)
        print(
            f"{source.name} -> {destination} | method={method} | "
            f"source={source_size[0]}x{source_size[1]} | "
            f"trimmed={trimmed.width}x{trimmed.height} | "
            f"output={output.width}x{output.height}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
