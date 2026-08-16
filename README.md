# The Mindful Matrix / BioCare

This repository is a dependency-free static site published under the GitHub Pages project path `/BioCare/`.

## Content model

- `content/site.json` is the source of truth for site copy, disclosures, product metadata, images, and verified destinations.
- Each product's `artwork` object reserves a stable Shelf background slot. Keep `src` null until approved original editorial artwork, dimensions, and crops are supplied; the existing product image remains the foreground fallback.
- `content/library.json` establishes the article collection and schema. An empty collection renders the visitor-facing coming-soon state; valid article records automatically replace it with the article grid.
- `templates/index.html` contains document structure only.
- `scripts/build.py` produces the deployable root `index.html` using only Python's standard library.
- `img/responsive/` contains optimized WebP derivatives; the original `img/` files remain fallbacks and source assets.

Do not edit generated product content in `index.html`. Change the content model or template, then regenerate it.

## Local validation

```text
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --directory ..
```

Open `http://localhost:8000/BioCare/` to test the same subpath shape used by GitHub Pages.

Pull requests run the same generator and validation checks and provide a downloadable static preview artifact. GitHub Pages remains compatible with its current branch-root configuration because the generated `index.html` is committed.

## Design system

- `assets/css/tokens.css` defines contrast-safe dark, light, and warm environments; display, body, and data typography; layout; spacing; shape; focus; and motion roles.
- `assets/brand/` contains replaceable SVG lockups, standalone mark variants, a single-color gold mark, and the favicon.
- `assets/css/site.css` contains reusable navigation, button, journey, data, product, Library, pathway, and destination patterns.
- The generated page is the production homepage. Library articles remain intentionally empty until reviewed content is approved.
