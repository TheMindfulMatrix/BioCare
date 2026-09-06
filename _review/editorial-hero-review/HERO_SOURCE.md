# Desktop hero source review

Reviewed September 6, 2026. **Candidate only; not deployed.**

- Identity: Balance Test Basic Kit, US SKU **910465**, standard BalanceTest box and BalanceOil+ Orange Lemon Mint bottle. Not the Premium variant.
- [Official product page](https://www.zinzino.com/shop/site/US/en-US/products/premier-kits/910465) uses its `/large/910465.png` display derivative; the recorded full-size [official original](https://zinzinowebstorage.blob.core.windows.net/productimages/910465.png) was fetched again and is byte-identical to the archived 650 x 650 source.
- Source SHA-256: `b0cf5653d294e964b849076667f554bab71e01a64733ec1ab6544e0f381cb5e1`.
- Current cutout: 560 x 560, **18,460 bytes**. Native original: 650 x 650, **184,469 bytes**. Proposed WebP: 650 x 650, **28,414 bytes**, quality 90/method 6, alpha retained. Pixel dimensions and original composition are retained; no sharpening, AI reconstruction, background removal, resampling or upscaling was performed.
- Candidate SHA-256: `22f1181bf5af365233e63b0232b18023efe9a4b2f4f0c9e4d4e7e041d20c7b33`. Reproduction: `python scripts/prepare_desktop_hero.py` with Pillow; normal site build remains standard-library only.
- Encoder used: Pillow **12.3.0**, libwebp **1.6.0**. Other encoder versions may produce different bytes; review any regenerated asset rather than changing its pinned test hash blindly.

## Decision

Visual desktop comparison shows more legible packaging lettering and smoother bottle edges. The original photograph retains its own shadow/alpha treatment and differs slightly in visible subject placement from the normalized legacy cutout. It is not an identical-pixel enlargement. Review the screenshot before release.

Only the homepage hero at **75rem / 1200px and wider** selects the new source. The fallback img, intrinsic aspect ratio, dimensions, alt text, link, loading priority, CSS and JavaScript remain unchanged. All phone/tablet widths below that threshold retain the old source, including high-DPI devices. Catalog, search, social images and product-page source selections are unchanged. The picture wrapper uses display:contents so it does not become a new grid/flex box.

Net image-transfer difference for a cold desktop hero selection: **+9,954 bytes** compared with the old hero source. Both assets may be fetched elsewhere on the homepage because catalog cards still use the original; the additional unique runtime asset is therefore **28,414 bytes**, not just the difference. No additional image transfer is needed below the desktop threshold.

At 1440px viewport the existing image box is about 742.4 CSS pixels wide, so even 650px is below a 1:1 source-to-display ratio. This is a modest source-quality improvement, not a claim of retina-ready artwork. A larger licensed transparent manufacturer master would be needed for a further substantial improvement without synthesizing package details.

The experiment and screenshots live only under `_preview/editorial-hero-review/`; no review document is linked from public output.
