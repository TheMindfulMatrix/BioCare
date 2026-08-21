#!/usr/bin/env python3
"""Audit the generated BioCare site and its live GitHub Pages deployment.

The script is intentionally read-only with respect to the repository and live
site. It writes machine-readable and human-readable evidence only to the
explicit output directory supplied by the caller.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRODUCTION_BASE = "https://themindfulmatrix.github.io/BioCare/"
USER_AGENT = "TheMindfulMatrix-BioCare-Daily-Audit/1.0"
PROTECTED_EXTERNAL_STATUSES = {401, 403, 405, 418, 429}
RETRYABLE_STATUSES = {408, 425, 429, 500, 502, 503, 504}


@dataclasses.dataclass(frozen=True)
class FetchResult:
    requested_url: str
    final_url: str
    status: int | None
    content_type: str
    body: bytes
    error: str | None = None


@dataclasses.dataclass(frozen=True)
class AuditCheck:
    category: str
    target: str
    status: str
    detail: str
    http_status: int | None = None
    expected_sha256: str | None = None
    actual_sha256: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {key: value for key, value in dataclasses.asdict(self).items() if value is not None}


class ReferenceParser(HTMLParser):
    """Collect navigational and resource references from generated HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "link" and {part.lower() for part in str(values.get("rel", "")).split()} & {"preconnect", "dns-prefetch"}:
            return
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.references.append(str(values[attribute]))
        if values.get("srcset"):
            for candidate in str(values["srcset"]).split(","):
                reference = candidate.strip().split()[0]
                if reference:
                    self.references.append(reference)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def committed_or_worktree_bytes(path: Path, repository_root: Path) -> bytes:
    """Read tracked bytes from Git, avoiding platform checkout conversions."""
    try:
        relative = path.resolve().relative_to(repository_root.resolve()).as_posix()
    except ValueError:
        return path.read_bytes()
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=repository_root,
        check=False,
        capture_output=True,
    )
    return result.stdout if result.returncode == 0 else path.read_bytes()


def normalize_base(raw: str) -> str:
    parsed = urllib.parse.urlsplit(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Production base must be an absolute HTTP(S) URL: {raw}")
    if parsed.scheme != "https" and parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise ValueError("Production auditing requires HTTPS except for local tests")
    if parsed.query or parsed.fragment:
        raise ValueError("Production base must not contain a query string or fragment")
    path = parsed.path if parsed.path.endswith("/") else parsed.path + "/"
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def url_without_fragment(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))


def url_without_query_or_fragment(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def url_to_local_path(url: str, production_base: str, repository_root: Path) -> Path:
    base = urllib.parse.urlsplit(production_base)
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc):
        raise ValueError(f"URL is outside the production origin: {url}")
    if not parsed.path.startswith(base.path):
        raise ValueError(f"URL is outside the production base path: {url}")

    relative_raw = urllib.parse.unquote(parsed.path[len(base.path):])
    relative = PurePosixPath(relative_raw or "index.html")
    if relative_raw.endswith("/"):
        relative = relative / "index.html"
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Unsafe production path: {url}")

    root = repository_root.resolve()
    target = (root / Path(*relative.parts)).resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"Resolved path escapes repository root: {url}")
    return target


def load_public_pages(repository_root: Path, production_base: str) -> list[tuple[str, Path]]:
    sitemap_path = repository_root / "sitemap.xml"
    tree = ET.parse(sitemap_path)
    locations = [str(node.text).strip() for node in tree.findall(".//{*}loc") if node.text and node.text.strip()]
    if not locations:
        raise ValueError("sitemap.xml contains no public page locations")
    if len(locations) != len(set(locations)):
        raise ValueError("sitemap.xml contains duplicate public page locations")

    pages: list[tuple[str, Path]] = []
    for location in locations:
        canonical = url_without_query_or_fragment(location)
        path = url_to_local_path(canonical, production_base, repository_root)
        if path.suffix.lower() != ".html":
            raise ValueError(f"Sitemap entry is not an HTML page: {location}")
        if not path.is_file():
            raise ValueError(f"Sitemap entry has no generated file: {path.relative_to(repository_root)}")
        pages.append((canonical, path))
    return pages


def fetch_url(url: str, *, timeout: float, retries: int, max_bytes: int | None = None) -> FetchResult:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json,text/css,image/avif,image/webp,image/*,*/*;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
        method="GET",
    )
    last_error: str | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read() if max_bytes is None else response.read(max_bytes)
                return FetchResult(
                    requested_url=url,
                    final_url=response.geturl(),
                    status=int(response.status),
                    content_type=response.headers.get_content_type() or "",
                    body=body,
                )
        except urllib.error.HTTPError as error:
            last_error = f"HTTP {error.code}: {error.reason}"
            if error.code not in RETRYABLE_STATUSES or attempt == retries:
                return FetchResult(
                    requested_url=url,
                    final_url=error.geturl() or url,
                    status=int(error.code),
                    content_type=error.headers.get_content_type() if error.headers else "",
                    body=b"",
                    error=last_error,
                )
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = str(getattr(error, "reason", error))
            if attempt == retries:
                break
        if attempt < retries:
            time.sleep(1.0 + attempt)
    return FetchResult(url, url, None, "", b"", last_error or "unknown network failure")


def classify_reference(reference: str, page_url: str, production_base: str) -> tuple[str, str] | None:
    cleaned = html.unescape(reference.strip())
    if not cleaned or cleaned.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return None
    resolved = url_without_fragment(urllib.parse.urljoin(page_url, cleaned))
    parsed = urllib.parse.urlsplit(resolved)
    if parsed.scheme not in {"http", "https"}:
        return None
    base = urllib.parse.urlsplit(production_base)
    is_internal = (parsed.scheme, parsed.netloc) == (base.scheme, base.netloc) and parsed.path.startswith(base.path)
    return ("internal" if is_internal else "external", resolved)


def collect_references(
    pages: Iterable[tuple[str, Path]], production_base: str, repository_root: Path
) -> tuple[set[str], set[str]]:
    internal: set[str] = set()
    external: set[str] = set()
    page_urls = {url_without_query_or_fragment(url) for url, _path in pages}

    for page_url, path in pages:
        parser = ReferenceParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for reference in parser.references:
            classified = classify_reference(reference, page_url, production_base)
            if classified is None:
                continue
            kind, resolved = classified
            if kind == "internal":
                if url_without_query_or_fragment(resolved) not in page_urls:
                    internal.add(resolved)
            else:
                external.add(resolved)

    # Include resources referenced from local CSS without executing any code.
    pending = list(sorted(internal))
    visited: set[str] = set()
    css_pattern = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", flags=re.IGNORECASE)
    while pending:
        resource_url = pending.pop()
        canonical = url_without_query_or_fragment(resource_url)
        if canonical in visited:
            continue
        visited.add(canonical)
        try:
            path = url_to_local_path(resource_url, production_base, repository_root)
        except ValueError:
            continue
        if path.suffix.lower() != ".css" or not path.is_file():
            continue
        for _quote, reference in css_pattern.findall(path.read_text(encoding="utf-8")):
            classified = classify_reference(reference, resource_url, production_base)
            if classified is None:
                continue
            kind, resolved = classified
            if kind == "internal":
                if resolved not in internal:
                    internal.add(resolved)
                    pending.append(resolved)
            else:
                external.add(resolved)
    return internal, external


def page_check(url: str, path: Path, fetcher: Callable[..., FetchResult], timeout: float) -> AuditCheck:
    expected = path.read_bytes()
    result = fetcher(url, timeout=timeout, retries=2)
    expected_hash = sha256_bytes(expected)
    actual_hash = sha256_bytes(result.body) if result.body else None
    if result.status != 200:
        return AuditCheck("public_page", url, "fail", result.error or f"unexpected HTTP {result.status}", result.status, expected_hash, actual_hash)
    if url_without_query_or_fragment(result.final_url) != url_without_query_or_fragment(url):
        return AuditCheck("public_page", url, "fail", f"redirected to unexpected URL {result.final_url}", result.status, expected_hash, actual_hash)
    if result.content_type not in {"text/html", "application/xhtml+xml"}:
        return AuditCheck("public_page", url, "fail", f"unexpected content type {result.content_type or 'missing'}", result.status, expected_hash, actual_hash)
    if result.body != expected:
        return AuditCheck("public_page", url, "fail", f"live bytes differ from {path.name}", result.status, expected_hash, actual_hash)
    return AuditCheck("public_page", url, "pass", f"HTTP 200 and byte-exact ({len(expected)} bytes)", result.status, expected_hash, actual_hash)


def internal_resource_check(
    url: str,
    production_base: str,
    repository_root: Path,
    fetcher: Callable[..., FetchResult],
    timeout: float,
) -> AuditCheck:
    try:
        path = url_to_local_path(url, production_base, repository_root)
    except ValueError as error:
        return AuditCheck("internal_resource", url, "fail", str(error))
    if not path.is_file():
        return AuditCheck("internal_resource", url, "fail", "referenced repository file is missing")
    expected = committed_or_worktree_bytes(path, repository_root)
    result = fetcher(url, timeout=timeout, retries=2)
    expected_hash = sha256_bytes(expected)
    actual_hash = sha256_bytes(result.body) if result.body else None
    if result.status != 200:
        return AuditCheck("internal_resource", url, "fail", result.error or f"unexpected HTTP {result.status}", result.status, expected_hash, actual_hash)
    if result.body != expected:
        return AuditCheck("internal_resource", url, "fail", f"live bytes differ from {path.relative_to(repository_root)}", result.status, expected_hash, actual_hash)
    return AuditCheck("internal_resource", url, "pass", f"HTTP 200 and byte-exact ({len(expected)} bytes)", result.status, expected_hash, actual_hash)


def external_link_check(url: str, fetcher: Callable[..., FetchResult], timeout: float) -> AuditCheck:
    result = fetcher(url, timeout=timeout, retries=1, max_bytes=64 * 1024)
    if result.status is not None and 200 <= result.status < 400:
        return AuditCheck("external_link", url, "pass", f"reachable at {result.final_url}", result.status)
    if result.status in PROTECTED_EXTERNAL_STATUSES:
        return AuditCheck("external_link", url, "warning", "destination blocks or rate-limits automated checks", result.status)
    return AuditCheck("external_link", url, "fail", result.error or f"unexpected HTTP {result.status}", result.status)


def parse_component_status(values: Iterable[str]) -> dict[str, int]:
    statuses: dict[str, int] = {}
    for value in values:
        name, separator, raw_status = value.partition("=")
        if not separator or not name or not raw_status.isdigit():
            raise ValueError(f"Invalid component status {value!r}; expected NAME=EXIT_CODE")
        statuses[name] = int(raw_status)
    return statuses


def repository_sha(repository_root: Path) -> str:
    if os.environ.get("GITHUB_SHA"):
        return os.environ["GITHUB_SHA"]
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def summarize(checks: list[AuditCheck], category: str) -> dict[str, int]:
    relevant = [check for check in checks if check.category == category]
    return {
        "checked": len(relevant),
        "passed": sum(check.status == "pass" for check in relevant),
        "warnings": sum(check.status == "warning" for check in relevant),
        "failed": sum(check.status == "fail" for check in relevant),
    }


def run_audit(
    *,
    repository_root: Path,
    production_base: str,
    component_statuses: dict[str, int],
    timeout: float,
    workers: int,
    check_external: bool,
    fetcher: Callable[..., FetchResult] = fetch_url,
) -> dict[str, object]:
    checks: list[AuditCheck] = [
        AuditCheck(
            "repository_suite",
            name,
            "pass" if status == 0 else "fail",
            f"exit code {status}",
        )
        for name, status in sorted(component_statuses.items())
    ]

    pages = load_public_pages(repository_root, production_base)
    for url, path in pages:
        checks.append(page_check(url, path, fetcher, timeout))

    internal_urls, external_urls = collect_references(pages, production_base, repository_root)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(internal_resource_check, url, production_base, repository_root, fetcher, timeout): url
            for url in sorted(internal_urls)
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                checks.append(future.result())
            except Exception as error:  # pragma: no cover - defensive workflow evidence
                checks.append(AuditCheck("internal_resource", futures[future], "fail", f"unhandled check error: {error}"))

    if check_external:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(external_link_check, url, fetcher, timeout): url for url in sorted(external_urls)}
            for future in concurrent.futures.as_completed(futures):
                try:
                    checks.append(future.result())
                except Exception as error:  # pragma: no cover - defensive workflow evidence
                    checks.append(AuditCheck("external_link", futures[future], "fail", f"unhandled check error: {error}"))

    checks.sort(key=lambda check: (check.category, check.target))
    failures = [check for check in checks if check.status == "fail"]
    warnings = [check for check in checks if check.status == "warning"]
    repository_name = os.environ.get("GITHUB_REPOSITORY", "TheMindfulMatrix/BioCare")
    run_id = os.environ.get("GITHUB_RUN_ID")
    run_url = f"https://github.com/{repository_name}/actions/runs/{run_id}" if run_id else None
    return {
        "schemaVersion": 1,
        "status": "fail" if failures else "pass",
        "generatedAtUtc": utc_now(),
        "repository": repository_name,
        "repositorySha": repository_sha(repository_root),
        "productionBase": production_base,
        "trigger": os.environ.get("GITHUB_EVENT_NAME", "local"),
        "runUrl": run_url,
        "componentStatuses": component_statuses,
        "publicPages": summarize(checks, "public_page"),
        "internalResources": summarize(checks, "internal_resource"),
        "externalLinks": {
            **summarize(checks, "external_link"),
            "discovered": len(external_urls),
            "enabled": check_external,
        },
        "totals": {
            "checks": len(checks),
            "failures": len(failures),
            "warnings": len(warnings),
        },
        "checks": [check.as_dict() for check in checks],
    }


def failure_report(error: Exception, repository_root: Path, production_base: str, component_statuses: dict[str, int]) -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "status": "fail",
        "generatedAtUtc": utc_now(),
        "repository": os.environ.get("GITHUB_REPOSITORY", "TheMindfulMatrix/BioCare"),
        "repositorySha": repository_sha(repository_root),
        "productionBase": production_base,
        "trigger": os.environ.get("GITHUB_EVENT_NAME", "local"),
        "runUrl": None,
        "componentStatuses": component_statuses,
        "publicPages": {"checked": 0, "passed": 0, "warnings": 0, "failed": 1},
        "internalResources": {"checked": 0, "passed": 0, "warnings": 0, "failed": 0},
        "externalLinks": {"checked": 0, "passed": 0, "warnings": 0, "failed": 0, "discovered": 0, "enabled": True},
        "totals": {"checks": 1, "failures": 1, "warnings": 0},
        "checks": [AuditCheck("audit_runtime", "daily_site_audit.py", "fail", str(error)).as_dict()],
    }


def markdown_report(report: dict[str, object]) -> str:
    status = str(report["status"]).upper()
    run_url = report.get("runUrl")
    lines = [
        "<!-- biocare-daily-audit -->",
        "# BioCare daily site audit",
        "",
        f"**Status: {status}**",
        "",
        f"- Generated: `{report['generatedAtUtc']}`",
        f"- Repository SHA: `{report['repositorySha']}`",
        f"- Production: `{report['productionBase']}`",
        f"- Trigger: `{report['trigger']}`",
    ]
    if run_url:
        lines.append(f"- Workflow run: {run_url}")

    lines.extend(["", "## Repository suite", "", "| Component | Exit code |", "|---|---:|"])
    for name, status_code in sorted(dict(report.get("componentStatuses", {})).items()):
        lines.append(f"| `{name}` | {status_code} |")

    lines.extend(["", "## Live production", ""])
    for label, key in (
        ("Public pages", "publicPages"),
        ("Internal resources", "internalResources"),
        ("External links", "externalLinks"),
    ):
        summary = dict(report[key])
        lines.append(
            f"- {label}: {summary.get('checked', 0)} checked / {summary.get('passed', 0)} passed / "
            f"{summary.get('warnings', 0)} warnings / {summary.get('failed', 0)} failed"
        )

    checks = list(report.get("checks", []))
    failures = [check for check in checks if check.get("status") == "fail"]
    warnings = [check for check in checks if check.get("status") == "warning"]
    lines.extend(["", "## Failures", ""])
    if failures:
        for check in failures[:50]:
            lines.append(f"- **{check['category']}** — `{check['target']}`: {check['detail']}")
        if len(failures) > 50:
            lines.append(f"- {len(failures) - 50} additional failures are recorded in the JSON artifact.")
    else:
        lines.append("- None.")

    lines.extend(["", "## Warnings", ""])
    if warnings:
        for check in warnings[:50]:
            lines.append(f"- **{check['category']}** — `{check['target']}`: {check['detail']}")
        if len(warnings) > 50:
            lines.append(f"- {len(warnings) - 50} additional warnings are recorded in the JSON artifact.")
    else:
        lines.append("- None.")
    lines.extend(["", "The workflow is read-only and made no website, branch, deployment, or pull-request changes.", ""])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--production-base", default=DEFAULT_PRODUCTION_BASE)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--component-status", action="append", default=[], metavar="NAME=EXIT_CODE")
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--skip-external", action="store_true", help="Skip external destinations (intended for isolated local tests only)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repository_root = args.repository_root.resolve()
    production_base = normalize_base(args.production_base)
    component_statuses = parse_component_status(args.component_status)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    try:
        report = run_audit(
            repository_root=repository_root,
            production_base=production_base,
            component_statuses=component_statuses,
            timeout=args.timeout,
            workers=max(1, args.workers),
            check_external=not args.skip_external,
        )
    except Exception as error:  # Always leave actionable workflow evidence.
        report = failure_report(error, repository_root, production_base, component_statuses)

    json_path = args.output_dir / "daily-site-audit.json"
    markdown_path = args.output_dir / "daily-site-audit.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    markdown_path.write_text(markdown_report(report), encoding="utf-8", newline="\n")
    print(markdown_report(report))
    print(f"Evidence: {json_path} and {markdown_path}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
