#!/usr/bin/env python3
"""Deterministic claim classification and repository audit engine.

The engine is deliberately conservative. It combines exact registry matches,
context-aware rules, protective-negation handling, and product-level implied-claim
checks. It reports; it does not rewrite source content.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
COMPLIANCE = ROOT / "content" / "compliance"
REPORTS = ROOT / "reports"
STATE_WEIGHT = {"GREEN": 1, "YELLOW": 2, "RED": 3}

CLAIM_TYPES = {
    "FACTUAL_PRODUCT_FACT",
    "PRICE_CLAIM",
    "INGREDIENT_CLAIM",
    "NUTRIENT_CONTENT_CLAIM",
    "STRUCTURE_FUNCTION_CLAIM",
    "GENERAL_WELLBEING_CLAIM",
    "AUTHORIZED_HEALTH_CLAIM",
    "QUALIFIED_HEALTH_CLAIM",
    "DISEASE_CLAIM",
    "DIAGNOSTIC_CLAIM",
    "SAFETY_CLAIM",
    "EFFICACY_CLAIM",
    "COMPARATIVE_CLAIM",
    "SUPERIORITY_CLAIM",
    "TESTIMONIAL_CLAIM",
    "BEFORE_AFTER_CLAIM",
    "ENDORSEMENT_CLAIM",
    "PROFESSIONAL_AUTHORITY_CLAIM",
    "SCIENTIFIC_EVIDENCE_CLAIM",
    "RESEARCH_INTERPRETATION",
    "MLM_EARNINGS_CLAIM",
    "MLM_LIFESTYLE_CLAIM",
    "MLM_RECRUITMENT_CLAIM",
    "AFFILIATE_RELATIONSHIP_CLAIM",
    "PRICE_SAVINGS_CLAIM",
    "AVAILABILITY_URGENCY_CLAIM",
    "IMPLIED_CLAIM_REVIEW",
}

LIKELY_CLAIM = re.compile(
    r"(?:\$\s?\d|\b(?:support|supports|may|can|evidence|research|stud(?:y|ies)|safe|effective|"
    r"test|testing|measure|measurement|biomarker|blood|health|wellness|nutrition|supplement|"
    r"ingredient|contains|capsules?|servings?|price|retail|premier|subscription|commission|"
    r"affiliate|partner|recommend|diagnos|treat|cure|prevent|recover|metabol|immune|gut|sleep|"
    r"energy|cardiovascular|cognit|body composition|professional|doctor|fda|results?|risk)\b)",
    re.I,
)
HEALTH_SIGNAL = re.compile(
    r"\b(?:health|wellness|supplement|support|immune|gut|digestion|sleep|energy|metabol|recovery|"
    r"cognit|brain|heart|cardiovascular|joint|muscle|skin|cellular|test|blood|biomarker|nutrition|"
    r"vitamin|mineral|omega|peptide|body composition|safe|effective|benefit)\b",
    re.I,
)
RESEARCH_SIGNAL = re.compile(r"\b(?:research|evidence|study|studies|trial|association|suggests?|uncertain|limitations?)\b", re.I)
PRICE_SIGNAL = re.compile(r"\$\s?\d+(?:[,.]\d+)?|\b(?:retail|premier|one[- ]time|monthly subscription|autoship)\b", re.I)
DISCLOSURE_SIGNAL = re.compile(r"\b(?:commission|compensation|affiliate|independent .* partner|material connection)\b", re.I)
JSON_NON_COPY_KEYS = {
    "id", "slug", "sku", "src", "srcsmall", "sourceasset", "sourceurl", "provenance", "href", "url", "destination",
    "officialproductpage", "intent", "environment", "variantgroup", "variantlabel", "visuallabel", "cta", "referralslug",
    "referralquerykey", "mechanism", "sourcemediaid", "sourcewidth", "sourceheight", "width", "height", "smallwidth", "smallheight",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).casefold()
    value = re.sub(r"[^a-z0-9$%]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    value = compact_text(re.sub(r"\{\{[^}]+\}\}", " ", text))
    if not value:
        return []
    parts = re.split(r"(?<=[.!?])\s+|\s*[\r\n]+\s*", value)
    return [part.strip(" \t\r\n") for part in parts if len(part.strip()) >= 3]


def protective_negation(text: str) -> bool:
    normalized = normalize(text)
    phrases = (
        "not intended to diagnose treat cure or prevent",
        "not a diagnostic",
        "does not diagnose",
        "doesn t diagnose",
        "cannot diagnose",
        "do not diagnose",
        "must not diagnose",
        "do not imply",
        "does not replace professional",
        "not a replacement for professional",
        "not medical advice",
    )
    return any(phrase in normalized for phrase in phrases)


def path_context(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix().casefold()
    if "recruit" in relative or "opportunity" in relative:
        return "MLM_RECRUITMENT"
    if relative.startswith(("social/", "content/social/")) or "caption" in relative:
        return "SOCIAL_COMMERCIAL"
    if relative == "content/catalog.json" or relative in {"shop.html", "templates/shop.html"}:
        return "COMMERCIAL_PRODUCT"
    if relative == "content/library.json" or relative.startswith("library/") or relative in {"library.html", "templates/library.html", "templates/article.html"}:
        return "EDITORIAL"
    return "MIXED_PUBLIC"


@dataclass(frozen=True)
class Finding:
    location: str
    exact_text: str
    context: str
    claim_type: str
    risk: str
    classification: str
    reason: str
    matched_rules: list[str]
    registry_claim_id: str | None
    registry_claim_ids: list[str]
    evidence_status: str
    supporting_evidence: list[str]
    required_disclosure: list[str]
    required_action: str
    implied_claim_review: bool
    strict_failure: bool


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.entries: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "svg", "noscript"}:
            self.skip_depth += 1
        values = dict(attrs)
        for attribute in ("alt", "aria-label", "title"):
            value = values.get(attribute)
            if value and not self.skip_depth:
                self.entries.append((self.getpos()[0], str(value)))

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg", "noscript"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and compact_text(data):
            self.entries.append((self.getpos()[0], data))


class ComplianceEngine:
    def __init__(self) -> None:
        self.version = load_json(COMPLIANCE / "version.json")
        self.rules_payload = load_json(COMPLIANCE / "rules.json")
        self.claims_payload = load_json(COMPLIANCE / "claims.json")
        self.evidence_payload = load_json(COMPLIANCE / "evidence.json")
        self.products_payload = load_json(COMPLIANCE / "products.json")
        self.rules = sorted(self.rules_payload["rules"], key=lambda item: (-int(item["priority"]), item["rule_id"]))
        self.claims = self.claims_payload["claims"]
        self.claim_by_normalized: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for claim in self.claims:
            self.claim_by_normalized[claim["normalized_text"]].append(claim)
        self.evidence_by_id = {item["evidence_id"]: item for item in self.evidence_payload["evidence"]}

    def _context_allowed(self, rule: dict[str, Any], context: str) -> bool:
        return context in rule.get("contexts", [])

    def _matches(self, rule: dict[str, Any], text: str) -> bool:
        match = rule["match"]
        mode = match["mode"]
        if mode == "always":
            return True
        if mode == "regex_any":
            return any(re.search(pattern, text, re.I) for pattern in match.get("patterns", []))
        if mode == "cooccurrence":
            return all(any(re.search(pattern, text, re.I) for pattern in group) for group in match.get("groups", []))
        raise ValueError(f"Unsupported match mode: {mode}")

    def _rule_matches(self, text: str, context: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        protected = protective_negation(text)
        for rule in self.rules:
            if not self._context_allowed(rule, context) or not self._matches(rule, text):
                continue
            if protected and rule["risk"] == "RED" and rule["rule_id"] in {
                "CE_RED_DISEASE_COMMERCIAL",
                "CE_RED_DISEASE_ACTION",
                "CE_RED_TEST_DIAGNOSIS",
                "CE_RED_MEDICAL_ADVICE",
            }:
                continue
            results.append(rule)
        return results

    def _classification(self, risk: str, action: str, registered: bool) -> str:
        if risk == "RED":
            return "LAUNCH_BLOCKER_COMPLIANCE"
        if risk == "YELLOW" and ("HUMAN_REVIEW" in action or action in {"IMPLIED_CLAIM_REVIEW", "DEFERRED_COMPLIANCE_REVIEW"}):
            return "HIGH_PRIORITY_REVIEW"
        if risk == "YELLOW":
            return "YELLOW_REVIEW"
        return "PASS" if registered else "LOW_RISK"

    def analyze_text(
        self,
        text: str,
        *,
        context: str,
        location: str = "inline",
        product_id: str | None = None,
    ) -> Finding | None:
        exact = compact_text(text)
        if not exact or exact.startswith(("http://", "https://")):
            return None
        registered = list(self.claim_by_normalized.get(normalize(exact), []))
        if product_id:
            product_matches = [claim for claim in registered if claim.get("product_id") == product_id]
            if product_matches:
                registered = product_matches
        if registered:
            allowed = [
                claim
                for claim in registered
                if context in claim.get("allowed_contexts", []) and context not in claim.get("prohibited_contexts", [])
            ]
            candidates = allowed or registered
            selected = max(
                candidates,
                key=lambda claim: (
                    STATE_WEIGHT[claim["compliance_state"]],
                    claim["review_status"] in {"BLOCKED", "DEFERRED_COMPLIANCE_REVIEW"},
                    claim["claim_id"],
                ),
            )
            risk = selected["compliance_state"]
            action = selected["review_status"]
            reason = selected["review_reason"]
            if not allowed:
                internal_deferred_record = product_id is not None and action == "DEFERRED_COMPLIANCE_REVIEW"
                risk = "RED" if risk == "RED" or (context in selected.get("prohibited_contexts", []) and not internal_deferred_record) else "YELLOW"
                if action not in {"BLOCKED", "DEFERRED_COMPLIANCE_REVIEW"}:
                    action = "HUMAN_REVIEW_REQUIRED_CONTEXT_MISMATCH"
                reason = f"Exact registered wording is not approved for the {context} context."
            supporting_evidence = sorted({source for claim in candidates for source in claim["supporting_sources"]})
            required_disclosure = sorted({item for claim in candidates for item in claim["required_disclosure"]})
            claim_ids = sorted(claim["claim_id"] for claim in candidates)
            evidence_status = "MISSING" if not supporting_evidence else ("REGISTERED" if len(claim_ids) == 1 else "REGISTERED_MULTIPLE_MATCHES")
            return Finding(
                location=location,
                exact_text=exact,
                context=context,
                claim_type=selected["claim_type"],
                risk=risk,
                classification=self._classification(risk, action, True),
                reason=reason,
                matched_rules=["CLAIM_REGISTRY_EXACT_MATCH"],
                registry_claim_id=selected["claim_id"],
                registry_claim_ids=claim_ids,
                evidence_status=evidence_status,
                supporting_evidence=supporting_evidence,
                required_disclosure=required_disclosure,
                required_action=action,
                implied_claim_review=selected["claim_type"] == "IMPLIED_CLAIM_REVIEW",
                strict_failure=risk == "RED" or (risk == "YELLOW" and action not in {"PASS", "PASS_WITH_QUALIFICATION"}),
            )

        matches = self._rule_matches(exact, context)
        if matches:
            highest = max(matches, key=lambda rule: (STATE_WEIGHT[rule["risk"]], int(rule["priority"])))
            risk = highest["risk"]
            action = highest["action"]
            claim_type = highest["claim_types"][0]
            implied = any(rule["rule_id"] == "CE_YELLOW_IMPLIED_CLAIM" for rule in matches)
            strict_failure = risk == "RED" or (risk == "YELLOW" and context in {"COMMERCIAL_PRODUCT", "SOCIAL_COMMERCIAL", "MLM_RECRUITMENT"})
            return Finding(
                location=location,
                exact_text=exact,
                context=context,
                claim_type=claim_type,
                risk=risk,
                classification=self._classification(risk, action, False),
                reason=highest["notes"],
                matched_rules=[rule["rule_id"] for rule in matches],
                registry_claim_id=None,
                registry_claim_ids=[],
                evidence_status="UNREGISTERED",
                supporting_evidence=[],
                required_disclosure=[highest["required_disclosure"]] if highest.get("required_disclosure") else [],
                required_action=action,
                implied_claim_review=implied,
                strict_failure=strict_failure,
            )

        word_count = len(re.findall(r"\b[\w’'-]+\b", exact))
        if word_count <= 5 and not PRICE_SIGNAL.search(exact) and not DISCLOSURE_SIGNAL.search(exact) and not re.search(
            r"\b(?:supports?|improves?|boosts?|prevents?|treats?|cures?|diagnoses?|guaranteed?|safe|proven|suggests?|contains?|includes?)\b",
            exact,
            re.I,
        ):
            return None
        if not LIKELY_CLAIM.search(exact):
            return None
        if PRICE_SIGNAL.search(exact):
            claim_type, risk, action, reason = "PRICE_CLAIM", "GREEN", "VERIFY_CURRENT_OFFICIAL_PRICE_SOURCE", "Price-like language requires current manufacturer source and verification metadata."
        elif DISCLOSURE_SIGNAL.search(exact):
            claim_type, risk, action, reason = "AFFILIATE_RELATIONSHIP_CLAIM", "YELLOW", "VERIFY_DISCLOSURE_AND_PLACEMENT", "Material-connection language requires exact approved disclosure wording and clear, conspicuous placement."
        elif context in {"COMMERCIAL_PRODUCT", "SOCIAL_COMMERCIAL", "MLM_RECRUITMENT", "MIXED_PUBLIC"} and HEALTH_SIGNAL.search(exact):
            claim_type, risk, action, reason = "EFFICACY_CLAIM", "YELLOW", "REGISTER_CLAIM_OR_HUMAN_REVIEW", "Unregistered commercial or mixed-context health language requires claim classification and evidence review."
        elif RESEARCH_SIGNAL.search(exact) or HEALTH_SIGNAL.search(exact):
            claim_type, risk, action, reason = "RESEARCH_INTERPRETATION", "GREEN", "EDITORIAL_SOURCE_REVIEW", "Likely editorial claim; retain source, scope, limitations, and uncertainty."
        else:
            claim_type, risk, action, reason = "FACTUAL_PRODUCT_FACT", "GREEN", "VERIFY_SOURCE", "Likely factual claim; verify the underlying source and current scope."
        strict_failure = risk == "YELLOW" and context in {"COMMERCIAL_PRODUCT", "SOCIAL_COMMERCIAL", "MLM_RECRUITMENT"}
        return Finding(
            location=location,
            exact_text=exact,
            context=context,
            claim_type=claim_type,
            risk=risk,
            classification=self._classification(risk, action, False),
            reason=reason,
            matched_rules=["HEURISTIC_CLAIM_BEARING_TEXT"],
            registry_claim_id=None,
            registry_claim_ids=[],
            evidence_status="UNREGISTERED",
            supporting_evidence=[],
            required_disclosure=[],
            required_action=action,
            implied_claim_review=False,
            strict_failure=strict_failure,
        )

    def _json_strings(self, value: Any, path: str = "$") -> Iterable[tuple[str, str]]:
        if isinstance(value, dict):
            for key in sorted(value):
                yield from self._json_strings(value[key], f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                yield from self._json_strings(item, f"{path}[{index}]")
        elif isinstance(value, str):
            yield path, value

    def scan_json(self, path: Path) -> list[Finding]:
        payload = load_json(path)
        context = path_context(path)
        relative = path.relative_to(ROOT).as_posix()
        findings: list[Finding] = []
        seen: set[tuple[str, str]] = set()
        for json_path, value in self._json_strings(payload):
            last_key_match = re.search(r"\.([A-Za-z0-9_]+)$", json_path)
            last_key = last_key_match.group(1).casefold() if last_key_match else ""
            if last_key in JSON_NON_COPY_KEYS or value.startswith(("http://", "https://", "assets/", "library/", "index.html", "shop.html", "start.html")):
                continue
            registered = self.claim_by_normalized.get(normalize(value))
            product_id = None
            if relative == "content/catalog.json":
                product_match = re.match(r"\$\.products\[(\d+)\]", json_path)
                if product_match:
                    product_index = int(product_match.group(1))
                    product_id = payload["products"][product_index].get("id")
            if registered:
                finding = self.analyze_text(value, context=context, location=f"{relative}:{json_path}", product_id=product_id)
                if finding:
                    findings.append(finding)
                continue
            for sentence in split_sentences(value):
                key = (json_path, sentence)
                if key in seen:
                    continue
                seen.add(key)
                finding = self.analyze_text(sentence, context=context, location=f"{relative}:{json_path}", product_id=product_id)
                if finding:
                    findings.append(finding)
        if relative == "content/catalog.json":
            for index, product in enumerate(payload.get("products", [])):
                aggregate = " | ".join(
                    compact_text(str(product.get(key, "")))
                    for key in ("name", "category", "productKind", "whyItsHere", "description", "visualLabel")
                    if product.get(key)
                )
                implied_rules = [rule for rule in self._rule_matches(aggregate, "COMMERCIAL_PRODUCT") if rule["rule_id"] == "CE_YELLOW_IMPLIED_CLAIM"]
                if implied_rules:
                    rule = implied_rules[0]
                    findings.append(
                        Finding(
                            location=f"{relative}:$.products[{index}]",
                            exact_text=aggregate,
                            context="COMMERCIAL_PRODUCT",
                            claim_type="IMPLIED_CLAIM_REVIEW",
                            risk="YELLOW",
                            classification="HIGH_PRIORITY_REVIEW",
                            reason=rule["notes"],
                            matched_rules=[rule["rule_id"]],
                            registry_claim_id=None,
                            registry_claim_ids=[],
                            evidence_status="UNREGISTERED_NET_IMPRESSION",
                            supporting_evidence=[],
                            required_disclosure=[],
                            required_action="IMPLIED_CLAIM_REVIEW",
                            implied_claim_review=True,
                            strict_failure=True,
                        )
                    )
        return findings

    def scan_html(self, path: Path) -> list[Finding]:
        parser = VisibleTextParser()
        parser.feed(path.read_text(encoding="utf-8"))
        context = path_context(path)
        relative = path.relative_to(ROOT).as_posix()
        findings: list[Finding] = []
        seen: set[tuple[int, str]] = set()
        for line, value in parser.entries:
            registered = self.claim_by_normalized.get(normalize(compact_text(value)))
            if registered:
                finding = self.analyze_text(value, context=context, location=f"{relative}:{line}")
                if finding:
                    findings.append(finding)
                continue
            for sentence in split_sentences(value):
                key = (line, sentence)
                if key in seen:
                    continue
                seen.add(key)
                finding = self.analyze_text(sentence, context=context, location=f"{relative}:{line}")
                if finding:
                    findings.append(finding)
        return findings

    def audit_paths(self) -> list[Path]:
        paths = [ROOT / "content" / name for name in ("catalog.json", "library.json", "site.json")]
        paths.extend(sorted((ROOT / "templates").glob("**/*.html")))
        paths.extend(ROOT / name for name in ("index.html", "shop.html", "library.html", "start.html"))
        paths.extend(sorted((ROOT / "library").glob("*.html")))
        for folder in (ROOT / "content" / "social", ROOT / "social"):
            if folder.is_dir():
                paths.extend(sorted(path for path in folder.rglob("*") if path.suffix.lower() in {".txt", ".md", ".json", ".html"}))
        return [path for path in paths if path.is_file()]

    def audit_repository(self) -> dict[str, Any]:
        findings: list[Finding] = []
        paths = self.audit_paths()
        for path in paths:
            findings.extend(self.scan_json(path) if path.suffix.lower() == ".json" else self.scan_html(path))
        findings.sort(key=lambda item: (item.location, item.exact_text, item.claim_type))
        state_counts = Counter(item.risk for item in findings)
        classification_counts = Counter(item.classification for item in findings)
        claim_type_counts = Counter(item.claim_type for item in findings)
        registered = sum(1 for item in findings if item.registry_claim_id)
        return {
            "schema_version": "1.0.0",
            "engine_version": self.version["engine_version"],
            "ruleset_version": self.version["ruleset_version"],
            "audit_date": self.version["last_policy_review"],
            "jurisdiction": self.version["primary_jurisdiction"],
            "legal_notice": self.version["legal_notice"],
            "scope": {
                "files_scanned": len(paths),
                "paths": [path.relative_to(ROOT).as_posix() for path in paths],
            },
            "summary": {
                "total_claims_scanned": len(findings),
                "GREEN": state_counts["GREEN"],
                "YELLOW": state_counts["YELLOW"],
                "RED": state_counts["RED"],
                "ambiguous_or_implied": sum(1 for item in findings if item.implied_claim_review),
                "registered_exact_matches": registered,
                "classification_counts": dict(sorted(classification_counts.items())),
                "claim_type_counts": dict(sorted(claim_type_counts.items())),
            },
            "findings": [asdict(item) for item in findings],
        }


def markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# The Mindful Matrix — Compliance Audit v1",
        "",
        f"Audit date: `{report['audit_date']}`",
        "",
        f"Engine/ruleset: `{report['engine_version']}` / `{report['ruleset_version']}`",
        "",
        f"Scope: `{report['scope']['files_scanned']}` source, template, and generated-public files",
        "",
        "> This is a machine-assisted risk-control audit. It is not legal advice, regulatory approval, or a guarantee of compliance.",
        "",
        "## Summary",
        "",
        f"- Total claim-bearing records: **{summary['total_claims_scanned']}**",
        f"- GREEN: **{summary['GREEN']}**",
        f"- YELLOW: **{summary['YELLOW']}**",
        f"- RED: **{summary['RED']}**",
        f"- Ambiguous/implied: **{summary['ambiguous_or_implied']}**",
        f"- Exact registry matches: **{summary['registered_exact_matches']}**",
        "",
        "## Finding classification",
        "",
    ]
    for classification, count in summary["classification_counts"].items():
        lines.append(f"- {classification}: **{count}**")

    grouped: dict[tuple[str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for finding in report["findings"]:
        if finding["classification"] == "PASS":
            continue
        key = (finding["classification"], finding["risk"], finding["claim_type"], finding["exact_text"], finding["reason"])
        grouped[key].append(finding)

    order = {"LAUNCH_BLOCKER_COMPLIANCE": 0, "HIGH_PRIORITY_REVIEW": 1, "YELLOW_REVIEW": 2, "LOW_RISK": 3}
    lines.extend(["", "## Non-PASS findings", ""])
    if not grouped:
        lines.append("No non-PASS findings were detected.")
    for (classification, risk, claim_type, exact_text, reason), items in sorted(grouped.items(), key=lambda item: (order[item[0][0]], item[0][2], item[0][3])):
        actions = sorted({item["required_action"] for item in items})
        rules = sorted({rule for item in items for rule in item["matched_rules"]})
        lines.extend(
            [
                f"### {classification} — {claim_type}",
                "",
                f"- Exact text: “{exact_text}”",
                f"- Risk: `{risk}`",
                f"- Reason: {reason}",
                f"- Source/rule: `{', '.join(rules)}`",
                f"- Recommended next action: `{', '.join(actions)}`",
                "- Locations:",
            ]
        )
        for item in items:
            lines.append(f"  - `{item['location']}`")
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "A RED result is a machine hard-stop for the stated commercial context. A YELLOW result is not approval; it requires evidence, qualification, disclosure, or human review. Exact registry matches preserve the currently reviewed wording and scope only. Duplicate public/template findings are retained in the JSON report so every location remains auditable.",
            "",
            "The absence of a machine-detected hard violation must be described only as: **No hard-rule violations detected by Compliance Engine v1.** It must not be described as legal compliance.",
            "",
        ]
    )
    return "\n".join(lines)


def write_audit(report: dict[str, Any], *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(markdown_report(report), encoding="utf-8")


if __name__ == "__main__":
    engine = ComplianceEngine()
    audit = engine.audit_repository()
    write_audit(audit, json_path=REPORTS / "compliance-audit-v1.json", markdown_path=REPORTS / "compliance-audit-v1.md")
    summary = audit["summary"]
    print(
        f"Compliance audit: {summary['total_claims_scanned']} claims; "
        f"GREEN={summary['GREEN']} YELLOW={summary['YELLOW']} RED={summary['RED']} "
        f"implied={summary['ambiguous_or_implied']}"
    )
