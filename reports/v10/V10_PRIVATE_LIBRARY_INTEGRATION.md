# V10 private-library integration

## Architecture

V10 uses two deliberately separate layers:

1. A local, gitignored audit artifact contains the detailed 104-resource inventory and rights/evidence-role classification. It is generated from a read-only source checkout and is not required to build or run BioCare.
2. The committed public manifest contains only reviewed public URLs, original summaries, scope, limitations, rights evidence, and public relationship metadata. The static builder reads only this committed manifest.

The public site has no submodule, remote fetch, token, runtime call, or build-time dependency on the private source. Promotion from the private audit requires a source-SHA-pinned explicit allowlist and affirmative public rights; the current private audit yields zero automatically public-eligible resources.

## Private audit result

| Classification | Count |
| --- | ---: |
| Public Website Eligible | 0 |
| Research / Reference Only | 34 |
| One-to-One Only | 15 |
| Internal / Partner Only | 30 |
| Excluded | 25 |
| Total | 104 |

Two content-level duplicate groups were detected. No secret-pattern matches were detected. The source manifest contained 135 entries and the canonical document set contained 104 extracted resources. The source checkout SHA and clean status were identical before and after both deterministic audit runs.

## Public integration result

Eight independently hosted public-government resources are published from the sanitized manifest. V10 adds a generated `evidence.html` route, Library pathway, department counts and source cards, universal-search `source` records, and progressive-disclosure links in every active product inspector. Manufacturer-specific private material remains disabled.

No raw source extract, private filename, authenticated URL, temporary signed URL, internal policy text, private contact detail, compensation material, or private audit record is present in generated public output.
