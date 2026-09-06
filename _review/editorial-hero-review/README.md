# Editorial and desktop hero review candidate

Prepared September 6, 2026 on `agent/editorial-hero-review`, from production baseline `02727eaa7e47f250b91ffef115fc1bb742b60422`.

**Not released. No push, PR, merge or deployment is part of this local review handoff.** The existing V12 draft and its worktree are untouched. No external reviewer or manufacturer has been contacted.

## Review decisions

| Requested action | Candidate result | Remaining decision |
| --- | --- | --- |
| Review Xtend+ substantiation first | [Source-review packet](XTEND_SUBSTANTIATION_REVIEW.md), including the linked US PDF's dated label, differing caution coverage and a prepared information request | Obtain current formulation/label reconciliation and finished-product evidence; keep HUMAN_REVIEW_REQUIRED until qualified human review. |
| Test sharper official desktop hero | Native 650px official source, optimized to 28,414 bytes, used only at 1200px+ | Review desktop screenshot; this is a modest improvement, not a retina-resolution master. |
| Prepare education one guide at a time | [K2 reader draft and review checklist](VITAMIN_K2_DRAFT.md) | Editorial/medical review and fuller literature check before any publication; zinc/copper and magnesium remain [queued](EDUCATION_QUEUE.md). |

The **70 review warnings / 77 strict advisory items**, seven inherited P1 human-review items, source classifications, claims, qualifications, disclosure requirements and review dates are preserved. A passing gate does not approve the unpublished draft or establish efficacy.

## Visual review

Local screenshots (excluded from commits and website publication):

- [Desktop candidate](../../_preview/editorial-hero-review/candidate-1440.png) and [exact-baseline desktop](../../_preview/editorial-hero-review/baseline-1440.png).
- [Tablet 768px](../../_preview/editorial-hero-review/candidate-768.png), [phone 390px](../../_preview/editorial-hero-review/candidate-390.png), [phone 375px](../../_preview/editorial-hero-review/candidate-375.png).
- [Image provenance, dimensions and transfer tradeoff](HERO_SOURCE.md).

The desktop source retains the original photograph's alpha/shadow and framing; the legacy normalized cutout remains below 1200px. The surrounding layout is unchanged, but visible product placement within the original photograph is not pixel-identical to the legacy cutout. Do not describe this as a lossless enlargement of the old image.

## Scope and verification

- 69 public pages and 10 published guides; 45 active / 8 deferred products.
- Only the homepage's hero picture markup changes among generated pages. The other **68 HTML pages**, search index, sitemap and robots output match baseline bytes after Git's newline normalization.
- CSS, JavaScript, templates, existing images, product descriptions, pricing, destinations, contact details, metadata, disclosures, compliance registries and Library records are unchanged.
- The new desktop asset is 28,414 bytes. Hero-selected-image difference: +9,954 bytes; whole-runtime inventory difference: +28,414 bytes because the original remains used elsewhere. No new-image request occurs below 1200px.
- Build deterministic; **88/88 unit tests pass** (84 inherited + 4 desktop-hero regression tests).
- Hard gate passes, **70/77** reconciliation retained; public safety scan: **0 findings**.
- **32 source-selection cases pass:** widths 375, 390, 768, 896, 1024, 1199, 1200, 1440; DPR 1 and 2; reduced motion and normal motion.
- **16 exact-baseline geometry comparisons pass.** Frozen screenshots at 375/390/768 are byte-identical to their baseline captures.
- Local served-build audit: **69 pages / 165 assets**, all HTTP 200 and byte parity, zero coverage/page/asset failures. The local server normalizes Windows CRLF text to the LF representation used by GitHub's Linux artifact; binaries remain untouched.
- Full permanent browser audit: **276 page/viewport states pass**, plus **8 Library viewport/motion cases**. Zero recorded overflow, broken images, bad page statuses, duplicate IDs, unnamed controls, console errors/warnings, failed requests, coverage failures or functional failures. See [QA_SUMMARY.json](QA_SUMMARY.json); detailed local output is `_preview/editorial-hero-review/browser/browser-audit.json`.

## Reproduce

Run from the repository root (normal build and tests need only Python's standard library):

```text
python scripts/build.py
python scripts/validate.py
python scripts/validate.py --compliance-strict --compliance-dry-run
python -m unittest discover -s tests -v
python scripts/scan_v10_public_safety.py
```

Optional asset regeneration requires Pillow: `python scripts/prepare_desktop_hero.py`. Its source-identity guard must not be removed to accept a changed official image without review. Visual QA requires Playwright and Chrome: `python _review/editorial-hero-review/verify_candidate.py`. It starts and stops its own loopback-only server, compares against the exact baseline, and runs the permanent all-pages browser audit. It never contacts production or changes website sources. Generated local evidence lives under `_preview/editorial-hero-review/`.

Review notes and drafts are under `_review/`, outside the canonical build and GitHub Pages' default Jekyll publication boundary. "Non-public" here means not published on the website, not confidential storage; no personal or restricted account information belongs here. Preview files are ignored by Git.

## Next authorized gate

Review the desktop visual and the K2 draft separately. A future approved hero release must not implicitly publish the draft or clear any advisory. Before any push/release, recheck current main, inspect the complete diff, rerun required checks on the exact candidate SHA, and follow the normal PR review/merge/deployment process only when authorized.
