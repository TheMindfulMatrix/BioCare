#!/usr/bin/env python3
"""Live, read-only audit of active commercial destinations and price sources."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import ssl
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "content" / "catalog.json"
TIMEOUT_SECONDS = 20
USER_AGENT = "Mozilla/5.0 (compatible; MindfulMatrixReleaseAudit/3.1)"


def probe(url: str) -> dict:
    request = Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS, context=ssl.create_default_context()) as response:
            return {"url": url, "status": response.status, "final_url": response.geturl(), "result": "reachable"}
    except HTTPError as error:
        if error.code in {401, 403}:
            return {"url": url, "status": error.code, "final_url": error.geturl(), "result": "protected"}
        if error.code == 405:
            fallback = Request(url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"}, method="GET")
            try:
                with urlopen(fallback, timeout=TIMEOUT_SECONDS, context=ssl.create_default_context()) as response:
                    return {"url": url, "status": response.status, "final_url": response.geturl(), "result": "reachable"}
            except (HTTPError, URLError, TimeoutError) as fallback_error:
                return {"url": url, "status": getattr(fallback_error, "code", None), "error": str(fallback_error), "result": "failed"}
        return {"url": url, "status": error.code, "final_url": error.geturl(), "error": str(error), "result": "failed"}
    except (URLError, TimeoutError) as error:
        return {"url": url, "status": None, "error": str(error), "result": "failed"}


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    active = [product for product in catalog["products"] if product["commercial_status"] == "active"]
    records = []
    for product in active:
        expected_host = "www.zinzino.com" if product["manufacturer"] == "Zinzino" else "biolimitless.com"
        for role, url in (
            ("destination", product["destination"]),
            ("price_source", product["price"]["official_price_source"]),
        ):
            records.append({"product": product["id"], "role": role, "url": url, "expected_host": expected_host})

    unique_urls = sorted({record["url"] for record in records})
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(probe, url): url for url in unique_urls}
        for future in as_completed(futures):
            result = future.result()
            results[result["url"]] = result

    failures = []
    for record in records:
        result = results[record["url"]]
        final_host = urlparse(result.get("final_url", record["url"])).hostname
        if result["result"] == "failed" or final_host != record["expected_host"]:
            failures.append({**record, **result, "final_host": final_host})

    summary = {
        "active_products": len(active),
        "commercial_records": len(records),
        "unique_urls": len(unique_urls),
        "reachable": sum(result["result"] == "reachable" for result in results.values()),
        "protected": sum(result["result"] == "protected" for result in results.values()),
        "failed": len(failures),
        "failures": failures,
    }
    print(json.dumps(summary, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
