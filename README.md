# The Mindful Matrix / BioCare

This repository is a dependency-free static site published under the GitHub Pages project path `/BioCare/`.

## Content model

- `content/site.json` is the source of truth for site copy, disclosures, product metadata, images, and verified destinations.
- Each product's `artwork` object reserves a stable Shelf background slot. Its `environment` selects a low-cost decorative treatment, while a verified `cutout` remains a separate foreground image. Keep `artwork.src` null until approved original editorial artwork, dimensions, and crops are supplied.
- `content/library.json` is the single source of truth for Library categories, the article schema, publication status, and article records. An empty collection renders the visitor-facing coming-soon state.
- `templates/index.html`, `templates/library.html`, `templates/start.html`, and `templates/article.html` contain page structure only. Shared navigation, footer, and metadata markup are generated centrally.
- `scripts/build.py` produces `index.html`, `library.html`, `start.html`, published-only `library/<slug>.html` files, `robots.txt`, and `sitemap.xml` using only Python's standard library. Draft records are never emitted as public pages or included in the sitemap.
- `img/responsive/` contains optimized WebP derivatives; the original `img/` files remain fallbacks and source assets.

Do not edit generated page content in root HTML files. Change the content model or templates, then regenerate the site.

## Library publishing

Add reviewed article records to the `articles` array in `content/library.json`. A record must use a configured category and a URL-safe unique slug. Keep work in progress set to `"status": "draft"`; only records explicitly set to `"status": "published"` generate `library/<slug>.html`.

The article model supports body sections, plain paragraphs, subheadings, lists, quotations, callouts, key takeaways, evidence notes, limitations, HTTPS sources, related published articles, and explicitly approved product connections. Article hero images are optional, but any configured hero must include dimensions and deliberate alt behavior. Categories with published content link to their generated group; empty categories remain visible, non-interactive, and labeled “Coming soon.”

A local fixture can be rendered without adding it to public content:

```text
python scripts/build.py --preview-article <path-to-non-public-fixture.json>
python scripts/validate.py --preview _preview/article-preview.html
```

The preview receives `noindex, nofollow`, no canonical URL, and a visible non-public banner. Keep fixture files and `_preview/` output out of commits and deployment artifacts.

## Local validation

```text
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --directory ..
```

Open `http://localhost:8000/BioCare/` to test the same subpath shape used by GitHub Pages.

Pull requests run the same generator and validation checks and provide a downloadable static preview artifact. GitHub Pages remains compatible with its current branch-root configuration because the generated `index.html` is committed.

Generated public pages include unique canonical URLs, Open Graph and Twitter metadata, conservative schema.org records, and the shared 1200 × 630 brand preview in `assets/brand/social-preview.png`. The canonical base remains `https://themindfulmatrix.github.io/BioCare/`; no custom domain is assumed.

## Official product cutouts

Immutable manufacturer downloads belong in `assets/source-products/`. Normalized transparent foregrounds belong in `assets/product-cutouts/`; never write processed files back into the source folder.

The reusable cutout tool accepts separate input and output folders and defaults to a 560 × 560 transparent PNG with a 6% margin:

```text
pip install "rembg[cpu]" pillow
python scripts/cutout.py assets/source-products/manufacturer/product assets/product-cutouts/manufacturer
```

The tool keeps an existing alpha channel by default and only trims, proportionally resizes, and centers those pixels. Inspect transparent sources before processing: use `--skip-rembg` when the alpha is already clean, or `--force-rembg` when an otherwise transparent file still contains a background surface. Opaque sources automatically use `isnet-general-use` with the approved alpha-matting settings. Use `--canvas-size` for another square size and `--output-name` to name a single generated PNG explicitly.

Example for the verified Balance Test Basic Kit source, whose transparent file still contains a presentation background:

```text
python scripts/cutout.py assets/source-products/zinzino/balance-test-basic-kit assets/product-cutouts/zinzino --force-rembg --output-name balance-test-basic-kit-910465.png
```

## Design system

- `assets/css/tokens.css` defines contrast-safe dark, light, and warm environments; display, body, and data typography; layout; spacing; shape; focus; and motion roles.
- `assets/brand/` contains replaceable SVG lockups, standalone mark variants, a single-color gold mark, and the favicon.
- `assets/css/site.css` contains reusable navigation, button, journey, data, product, Library, pathway, and destination patterns.
- The generated root pages are the homepage, Library landing page, and Start Here orientation. Published Library records are generated as evidence-forward guides; draft records remain private to the content model and preview workflow.
