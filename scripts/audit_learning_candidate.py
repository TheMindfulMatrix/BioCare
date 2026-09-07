"""Build a reproducible review packet without changing production or source content."""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit

from daily_audit import audit_site, build_bytes, fetch
from site_paths import audited_page_paths
from compliance_engine import ComplianceEngine
from validate_compliance import validate_compliance

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "ef36a71ecc3365fa1a03db18083ac75349c54574"
OUTPUT = ROOT / "_review/testing-library-partner-learning"


def read(name):
    return json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", "-c", "safe.directory=" + ROOT.as_posix(), *args], cwd=ROOT)


def baseline_checks():
    # Export only public text inputs needed by the baseline's own validator.
    paths = ["content", "templates", "library", "index.html", "shop.html", "library.html",
             "start.html", "about.html", "privacy.html", "know-your-number.html",
             "scripts/compliance_engine.py", "scripts/validate_compliance.py"]
    archive = git("archive", "--format=tar", BASELINE, *paths)
    with tempfile.TemporaryDirectory(prefix="matrix-baseline-") as directory:
        target_root = Path(directory).resolve()
        with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
            for item in stream:
                if not item.isfile():
                    continue
                target = (target_root / item.name).resolve()
                if target_root not in target.parents:
                    raise ValueError("Archive path escaped baseline validation directory")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(stream.extractfile(item).read())
        code = "import json,sys;sys.path.insert(0,'scripts');from validate_compliance import validate_compliance;from compliance_engine import ComplianceEngine;print(json.dumps({'normal':validate_compliance(),'strict':validate_compliance(strict=True),'audit':ComplianceEngine().audit_repository()}))"
        output = subprocess.check_output([sys.executable, "-c", code], cwd=target_root)
        return json.loads(output)


def save(name, data):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-url", default="http://127.0.0.1:8775/")
    args = parser.parse_args()
    if urlsplit(args.local_url).hostname not in {"127.0.0.1", "localhost"}:
        raise SystemExit("This candidate check accepts loopback previews only.")
    baseline = baseline_checks()
    normal = validate_compliance()
    strict = validate_compliance(strict=True)
    audit = ComplianceEngine().audit_repository()
    inherited = {(f["exact_text"], f["context"], f["required_action"]) for f in baseline["audit"]["findings"] if f["strict_failure"]}
    added = [f for f in audit["findings"] if f["strict_failure"] and (f["exact_text"], f["context"], f["required_action"]) not in inherited]
    changes = []
    for name in ["content/catalog.json", "content/site.json", "content/product-labels.json", "content/manufacturer-documents.json"] + [p.relative_to(ROOT).as_posix() for p in (ROOT / "content/compliance").glob("*") if p.is_file()]:
        if git("show", BASELINE + ":" + name).replace(b"\r\n", b"\n") != build_bytes(ROOT / name):
            changes.append(name)
    summary = {
        "baseline_sha": BASELINE,
        "baseline_review_warnings": len(baseline["normal"]["warnings"]),
        "baseline_strict_items": len(baseline["strict"]["errors"]),
        "candidate_review_warnings": len(normal["warnings"]),
        "candidate_strict_items": len(strict["errors"]),
        "candidate_hard_errors": normal["errors"],
        "candidate_red": audit["summary"]["RED"],
        "protected_canonical_files_changed": changes,
        "new_strict_finding_locations": len(added),
        "new_strict_findings_by_file": dict(Counter(f["location"].split(":")[0] for f in added)),
        "interpretation": "Machine advisories are not clinical or legal approval. New business/education surfaces and the source manifest are now audited. Existing registry classifications, qualifications, sources and disclosures remain unchanged.",
    }
    save("compliance-reconciliation.json", summary)
    save("new-review-advisories.json", {"findings": added})
    sources = read("resources/public-sources.json")["records"]
    articles = read("library.json")["articles"]
    departments = read("discovery.json")["departments"]
    coverage = []
    for product in read("catalog.json")["products"]:
        if product["commercial_status"] != "active":
            continue
        contextual = [s["id"] for s in sources if product["id"] in s["product_ids"]]
        explicit = [a["slug"] for a in articles if product["id"] in a.get("relatedProducts", [])]
        dept = next(d for d in departments if d["intentId"] == product["intent"])
        coverage.append({"product_id": product["id"], "name": product["name"],
                         "topic_source_ids": contextual, "specific_navigation_guides": explicit,
                         "department_guides": dept["articleSlugs"],
                         "finished_product_effectiveness_established_here": False,
                         "remaining_gap": "No finished-product efficacy claim established. Topic sources and catalog connections are educational navigation only."})
    save("product-evidence-coverage.json", {"active_products": len(coverage), "covered_with_topic_context": sum(bool(p["topic_source_ids"]) for p in coverage), "products": coverage})
    # Python's Windows preview serves checkout CRLF bytes; Linux Pages serves LF.
    # Normalize only text line endings for this explicitly local parity check.
    # The permanent live-production audit remains strict and unchanged.
    def local_fetch(url):
        result = fetch(url)
        if Path(urlsplit(url).path).suffix in {".html", ".css", ".js", ".json", ".svg", ".xml", ".txt"}:
            result["body"] = result["body"].replace(b"\r\n", b"\n")
        return result
    parity = audit_site(ROOT, args.local_url, "unreleased-candidate", fetcher=local_fetch)
    parity["comparison_note"] = "Loopback only; CRLF normalized to LF for text. Not a live-production or browser QA result."
    save("local-parity.json", parity)
    hashes_before = {p: hashlib.sha256(build_bytes(ROOT / (p or "index.html"))).hexdigest() for p in audited_page_paths(ROOT)}
    subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, check=True)
    hashes_after = {p: hashlib.sha256(build_bytes(ROOT / (p or "index.html"))).hexdigest() for p in audited_page_paths(ROOT)}
    result = {"pages": len(hashes_after), "deterministic": hashes_before == hashes_after,
              "local_page_failures": len(parity["page_regressions"]), "local_asset_failures": len(parity["broken_live_assets"]),
              "assets": parity["referenced_live_assets"], "compliance": summary}
    save("validation-summary.json", result)
    print(json.dumps(result, indent=2))
    if normal["errors"] or changes or hashes_before != hashes_after or parity["overall_status"] != "HEALTHY":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
