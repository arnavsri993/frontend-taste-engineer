#!/usr/bin/env python3
"""Discover public frontend-source candidates without executing third-party code.

YAML inputs use the JSON-compatible subset of YAML so this script remains
standard-library only. Dry-run mode is offline, seed-backed, deterministic, and
write-free. Network mode searches public pages and writes candidate artifacts;
it never promotes stable knowledge.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import socket
import sys
from typing import Any, Iterable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote_plus, unquote, urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_ROOT = PLUGIN_ROOT / "research" / "source-discovery"
DEFAULT_QUERY_FILE = DISCOVERY_ROOT / "discovery-queries.json"
DEFAULT_SEED_FILE = DISCOVERY_ROOT / "seed-catalog.json"
REGISTRY_FILE = PLUGIN_ROOT / "research" / "source-registry.json"
USER_AGENT = "FrontendTasteEngineer-SourceDiscovery/0.3 (+public-text-only; no-code-execution)"

REQUIRED_SOURCE_FIELDS = (
    "id", "name", "author_or_organization", "canonical_url", "supplied_url",
    "source_type", "classification", "license", "accessible_revision",
    "last_checked_revision", "topics_contributed", "files_or_sections_consulted",
    "reliability_assessment", "maintenance_status",
    "copying_or_adaptation_restrictions", "related_sources", "notes",
)
CLASSIFICATIONS = {
    "core", "specialized", "experimental", "inspiration-only",
    "inaccessible", "unresolved", "rejected",
}
TEXT_CONTENT_TYPES = {
    "text/html", "application/xhtml+xml", "text/plain", "application/json",
    "application/ld+json", "text/markdown",
}
AUTH_PATH_RE = re.compile(
    r"/(?:login|log-in|signin|sign-in|account|billing|checkout|admin|private|members?)(?:/|$)",
    re.IGNORECASE,
)
PROMPT_INJECTION_PATTERNS = {
    "ignore-instructions": re.compile(r"ignore (?:all |any )?(?:previous|prior|system) instructions", re.I),
    "agent-role-override": re.compile(r"(?:you are now|act as) (?:a |an )?(?:different|new|unrestricted) (?:agent|assistant|model)", re.I),
    "system-prompt-request": re.compile(r"(?:reveal|print|return|show).{0,40}(?:system prompt|hidden instructions)", re.I),
    "secret-exfiltration": re.compile(r"(?:send|upload|exfiltrate|reveal).{0,50}(?:secret|token|credential|api key|private key)", re.I),
}
CREDENTIAL_PATTERNS = {
    "seed-phrase-request": re.compile(r"(?:enter|submit|verify).{0,30}(?:seed phrase|recovery phrase)", re.I),
    "private-key-request": re.compile(r"(?:enter|submit|paste).{0,30}private key", re.I),
    "credential-capture": re.compile(r"(?:enter|submit|paste).{0,30}(?:password|api key|access token).{0,30}(?:continue|verify|unlock)", re.I),
}
INSTALL_PATTERNS = {
    "shell-pipe-install": re.compile(r"(?:curl|wget)[^\n|]{0,200}\|\s*(?:sh|bash|zsh)", re.I),
    "package-install-command": re.compile(r"\b(?:npm|pnpm|yarn|bun|pipx?|uvx|npx)\s+(?:add|install|i|exec)\b", re.I),
}
INSPIRATION_TERMS = {
    "inspiration", "gallery", "examples", "landing page", "portfolio", "screen flow",
    "pricing page", "web design", "mobile app screen",
}
REUSABLE_TERMS = {
    "component", "components", "template", "templates", "documentation", "docs",
    "source", "repository", "package", "registry", "api", "sdk", "license",
}


class DiscoveryError(ValueError):
    """Expected, user-actionable discovery failure."""


def load_json_yaml(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise DiscoveryError(f"Cannot parse JSON-compatible YAML {path}: {exc}") from exc


def normalize_url(raw: str) -> str:
    value = html.unescape(str(raw).strip())
    if value.startswith("//"):
        value = "https:" + value
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise DiscoveryError(f"Only absolute public HTTP(S) URLs are supported: {raw!r}")
    if parsed.username or parsed.password:
        raise DiscoveryError("URLs containing credentials are prohibited")
    host = parsed.hostname.lower().rstrip(".")
    port = f":{parsed.port}" if parsed.port else ""
    path = re.sub(r"/+", "/", parsed.path or "")
    if path != "/":
        path = path.rstrip("/")
    if path == "/":
        path = ""
    query_parts = []
    for part in parsed.query.split("&") if parsed.query else []:
        key = part.split("=", 1)[0].lower()
        if key and not key.startswith("utm_") and key not in {"ref", "source", "s", "fbclid", "gclid"}:
            query_parts.append(part)
    return urlunsplit((parsed.scheme.lower(), host + port, path, "&".join(sorted(query_parts)), ""))


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "candidate"


def source_id(url: str) -> str:
    parsed = urlsplit(url)
    host = re.sub(r"^www\.", "", parsed.hostname or "source")
    path = "-".join(part for part in parsed.path.split("/") if part)
    return slug(f"{host}-{path}" if path else host)


def public_url(url: str) -> str:
    normalized = normalize_url(url)
    parsed = urlsplit(normalized)
    host = parsed.hostname or ""
    if host in {"localhost", "localhost.localdomain"} or host.endswith((".local", ".internal", ".localhost")):
        raise DiscoveryError("Local and private hostnames are prohibited")
    if AUTH_PATH_RE.search(parsed.path):
        raise DiscoveryError("Authenticated/account paths are outside discovery scope")
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        literal = None
    if literal is not None and not literal.is_global:
        raise DiscoveryError("Private, reserved, loopback, or link-local addresses are prohibited")
    try:
        resolved = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or 443, type=socket.SOCK_STREAM)}
    except socket.gaierror as exc:
        raise DiscoveryError(f"Hostname resolution failed: {exc}") from exc
    if not resolved or any(not ipaddress.ip_address(address).is_global for address in resolved):
        raise DiscoveryError("Hostname resolves to a non-public address")
    return normalized


class SafeRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Request | None:
        target = public_url(urljoin(req.full_url, newurl))
        return super().redirect_request(req, fp, code, msg, headers, target)


def fetch_public_text(url: str, *, timeout: float, max_bytes: int) -> tuple[str, str, str]:
    target = public_url(url)
    request = Request(
        target,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,text/plain,application/json,text/markdown;q=0.8",
            "Accept-Encoding": "identity",
        },
        method="GET",
    )
    opener = build_opener(SafeRedirectHandler())
    try:
        with opener.open(request, timeout=timeout) as response:
            final_url = public_url(response.geturl())
            content_type = response.headers.get_content_type().lower()
            if content_type not in TEXT_CONTENT_TYPES:
                raise DiscoveryError(f"Binary or unsupported content type blocked: {content_type}")
            declared = response.headers.get("Content-Length")
            if declared and int(declared) > max_bytes:
                raise DiscoveryError(f"Text response exceeds {max_bytes} bytes")
            payload = response.read(max_bytes + 1)
            if len(payload) > max_bytes:
                raise DiscoveryError(f"Text response exceeds {max_bytes} bytes")
            charset = response.headers.get_content_charset() or "utf-8"
            return final_url, payload.decode(charset, errors="replace"), content_type
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
        raise DiscoveryError(str(exc)) from exc


class PageTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.meta_description = ""
        self._title = False
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"}:
            self._ignored_depth += 1
        if tag == "title":
            self._title = True
        if tag == "meta":
            values = {key.lower(): value or "" for key, value in attrs}
            if values.get("name", "").lower() == "description" or values.get("property", "").lower() == "og:description":
                self.meta_description = values.get("content", "")[:500]

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == "title":
            self._title = False

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if not clean or self._ignored_depth:
            return
        if self._title:
            self.title_parts.append(clean)
        self.text_parts.append(clean)

    @property
    def title(self) -> str:
        return " ".join(self.title_parts)[:180]

    @property
    def text(self) -> str:
        return " ".join(self.text_parts)


class SearchResultParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        values = {key.lower(): value or "" for key, value in attrs}
        href = values.get("href", "")
        classes = values.get("class", "")
        if href and ("result" in classes or "uddg=" in href):
            self.links.append(href)


def result_target(raw: str) -> str | None:
    value = html.unescape(raw)
    if value.startswith("//"):
        value = "https:" + value
    parsed = urlsplit(value)
    if parsed.hostname and parsed.hostname.endswith("duckduckgo.com"):
        target = parse_qs(parsed.query).get("uddg", [""])[0]
        value = unquote(target)
    try:
        return normalize_url(value)
    except DiscoveryError:
        return None


def search_public_web(query: str, *, timeout: float, max_bytes: int) -> list[str]:
    search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    _, raw, _ = fetch_public_text(search_url, timeout=timeout, max_bytes=max_bytes)
    parser = SearchResultParser()
    parser.feed(raw)
    results = []
    for href in parser.links:
        target = result_target(href)
        if target and target not in results:
            results.append(target)
    return results


def registry_urls(path: Path) -> dict[str, str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    for entry in value.get("sources") or []:
        if not isinstance(entry, Mapping) or not entry.get("id") or not entry.get("canonical_url"):
            continue
        try:
            result[normalize_url(str(entry["canonical_url"]))] = str(entry["id"])
        except DiscoveryError:
            continue
    return result


def effective_seed_sources(value: Mapping[str, Any]) -> list[dict[str, Any]]:
    defaults = dict(value.get("entry_defaults") or {})
    result = []
    for category in value.get("categories") or []:
        if not isinstance(category, Mapping):
            continue
        category_defaults = dict(category.get("defaults") or {})
        for source in category.get("sources") or []:
            if not isinstance(source, Mapping):
                continue
            merged = {**defaults, **category_defaults, **source, "category": category.get("id")}
            missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in merged]
            if missing:
                raise DiscoveryError(f"Seed {source.get('id')} lacks effective fields: {', '.join(missing)}")
            if merged["classification"] not in CLASSIFICATIONS:
                raise DiscoveryError(f"Seed {source.get('id')} has invalid classification")
            merged["canonical_url"] = normalize_url(str(merged["canonical_url"]))
            result.append(merged)
    return sorted(result, key=lambda item: (str(item["id"]), str(item["canonical_url"])))


def scan_safety(text: str, url: str) -> dict[str, list[str]]:
    injection = sorted(name for name, pattern in PROMPT_INJECTION_PATTERNS.items() if pattern.search(text))
    credentials = sorted(name for name, pattern in CREDENTIAL_PATTERNS.items() if pattern.search(text))
    installs = sorted(name for name, pattern in INSTALL_PATTERNS.items() if pattern.search(text))
    prohibited = []
    lowered = f"{url} {text[:10000]}".lower()
    if "openai build week" in lowered or "openai-build-week" in lowered:
        prohibited.append("prohibited-corporate-event-marketing")
    return {
        "prompt_injection_signals": injection,
        "credential_or_payment_signals": credentials,
        "install_or_execution_signals": installs,
        "prohibited_source_signals": prohibited,
    }


def score_candidate(*, text: str, query: str, category: str, accessible: bool, safety: Mapping[str, list[str]], seed: bool) -> dict[str, int]:
    lowered = f"{query} {category} {text[:50000]}".lower()
    relevance_terms = {"frontend", "react", "ui", "component", "template", "design", "tailwind", "dashboard", "accessibility", "motion"}
    relevance = min(20, (16 if seed else 8) + sum(term in lowered for term in relevance_terms))
    license_clarity = 0
    if re.search(r"\b(?:mit license|apache(?: license)? 2\.0|bsd-[23]-clause)\b", lowered):
        license_clarity = 6  # signal only; item-level scope is still unverified
    quality = 2 if seed else (7 if accessible and len(text) > 300 else 3 if accessible else 0)
    accessibility = min(15, 3 * sum(term in lowered for term in ("accessibility", "keyboard", "focus", "aria", "screen reader")))
    implementation = min(10, 2 * sum(term in lowered for term in ("component", "code", "api", "docs", "example")))
    inspiration = 10 if any(term in lowered for term in INSPIRATION_TERMS) else 4 if "design" in lowered else 0
    dependency = 2 if seed else (1 if safety["install_or_execution_signals"] else 4)
    security = 0 if safety["prompt_injection_signals"] or safety["credential_or_payment_signals"] else (2 if seed else 5)
    values = {
        "relevance": relevance,
        "license_clarity": license_clarity,
        "quality_maintainability": quality,
        "accessibility_usefulness": accessibility,
        "implementation_usefulness": implementation,
        "inspiration_value": inspiration,
        "dependency_safety": dependency,
        "prompt_injection_security_safety": security,
    }
    values["total"] = min(69 if license_clarity < 20 else 100, sum(values.values()))
    return values


def classify(score: int, *, accessible: bool, safety: Mapping[str, list[str]], inspiration: bool, reusable: bool) -> str:
    if safety["prompt_injection_signals"] or safety["credential_or_payment_signals"] or safety["prohibited_source_signals"]:
        return "rejected"
    if not accessible:
        return "inaccessible"
    if inspiration and not reusable:
        return "inspiration-only"
    if score < 25:
        return "rejected"
    if score < 70:
        return "unresolved"
    return "experimental"  # automated discovery never assigns core/specialized


def seed_candidate(source: Mapping[str, Any], *, as_of: str) -> dict[str, Any]:
    safety = {
        "prompt_injection_signals": [], "credential_or_payment_signals": [],
        "install_or_execution_signals": [], "prohibited_source_signals": [],
    }
    category = str(source.get("category") or "")
    score = score_candidate(text="", query="request-supplied seed", category=category, accessible=False, safety=safety, seed=True)
    candidate = dict(source)
    candidate.update({
        "classification": source["classification"],
        "discovery": {"query": "request-supplied seed", "discovered_on": as_of, "network_used": False, "registry_duplicate": bool(source.get("registry_id"))},
        "score": score,
        "safety_review": {**safety, "binary_or_install_payloads_downloaded": False, "third_party_code_executed": False},
        "promotion": {"status": "candidate-only", "required_reviews": ["license", "security", "product-fit", "accessibility", "performance", "originality", "evaluation"]},
    })
    return candidate


def network_candidate(url: str, query: str, *, as_of: str, timeout: float, max_bytes: int) -> dict[str, Any]:
    try:
        final_url, raw, content_type = fetch_public_text(url, timeout=timeout, max_bytes=max_bytes)
        accessible = True
        if content_type in {"text/html", "application/xhtml+xml"}:
            parser = PageTextParser()
            parser.feed(raw)
            title = parser.title or (urlsplit(final_url).hostname or final_url)
            page_text = f"{parser.title} {parser.meta_description} {parser.text}"
        else:
            title = urlsplit(final_url).hostname or final_url
            page_text = raw
        failure = ""
    except DiscoveryError as exc:
        final_url = normalize_url(url)
        accessible = False
        title = urlsplit(final_url).hostname or final_url
        page_text = ""
        failure = str(exc)[:300]
    safety = scan_safety(page_text, final_url)
    display_title = title if not safety["prompt_injection_signals"] else (urlsplit(final_url).hostname or "rejected candidate")
    lowered = f"{query} {title} {page_text[:30000]}".lower()
    inspiration = any(term in lowered for term in INSPIRATION_TERMS)
    reusable = any(term in lowered for term in REUSABLE_TERMS)
    score = score_candidate(text=page_text, query=query, category="network-discovery", accessible=accessible, safety=safety, seed=False)
    classification = classify(score["total"], accessible=accessible, safety=safety, inspiration=inspiration, reusable=reusable)
    license_text = "Unverified; do not copy or adapt until the exact license and asset scope are reviewed."
    if score["license_clarity"]:
        license_text = "Possible public license signal observed; exact item scope and obligations remain unverified."
    return {
        "id": source_id(final_url),
        "name": " ".join(display_title.split())[:180],
        "author_or_organization": "Unverified; public page metadata is not accepted as authorship proof.",
        "canonical_url": final_url,
        "supplied_url": url,
        "source_type": "public-web discovery candidate",
        "classification": classification,
        "license": license_text,
        "accessible_revision": f"live-public-text@{as_of}" if accessible else "Public content not inspected reliably.",
        "last_checked_revision": f"live-page@{as_of}" if accessible else f"inaccessible@{as_of}",
        "topics_contributed": sorted(term for term in ("components", "templates", "accessibility", "motion", "dashboards", "inspiration") if term.rstrip("s") in lowered or term in lowered),
        "files_or_sections_consulted": [f"public text surface: {final_url}"] if accessible else [],
        "reliability_assessment": "Candidate metadata only; substantive claims require manual source and provenance review." if accessible else "Insufficient accessible evidence for assessment.",
        "maintenance_status": "Unknown until release history or maintained documentation is reviewed.",
        "copying_or_adaptation_restrictions": "Discovery/linking only. No copying, adaptation, installation, or execution until license, source-selection, and safety gates pass.",
        "related_sources": [],
        "notes": "Candidate report only; stable knowledge was not modified." + (f" Access failure: {failure}" if failure else ""),
        "discovery": {"query": query, "discovered_on": as_of, "network_used": True, "registry_duplicate": False},
        "score": score,
        "safety_review": {**safety, "binary_or_install_payloads_downloaded": False, "third_party_code_executed": False},
        "promotion": {"status": "candidate-only", "required_reviews": ["license", "security", "product-fit", "accessibility", "performance", "originality", "evaluation"]},
    }


def markdown_report(candidates: Sequence[Mapping[str, Any]], *, as_of: str, mode: str, query_errors: Sequence[Mapping[str, str]]) -> str:
    counts = {classification: sum(item.get("classification") == classification for item in candidates) for classification in sorted(CLASSIFICATIONS)}
    lines = [
        "# External source discovery report", "",
        f"Generated: {as_of}  ", f"Mode: {mode}  ",
        f"Candidates: {len(candidates)}  ", "Stable knowledge modified: no", "",
        "## Classification", "",
        "| Classification | Count |", "|---|---:|",
    ]
    lines.extend(f"| {name} | {count} |" for name, count in counts.items() if count)
    lines.extend(["", "## Candidates", "", "| ID | Classification | Score | Source |", "|---|---|---:|---|"])
    for item in candidates:
        safe_name = re.sub(r"[\[\]()<>`#]", " ", str(item.get("name") or item.get("id"))).replace("|", "\\|")
        lines.append(f"| `{item['id']}` | {item['classification']} | {item['score']['total']} | [{safe_name}]({item['canonical_url']}) |")
    if query_errors:
        lines.extend(["", "## Query/access errors", ""])
        for error in query_errors:
            lines.append(f"- `{error['query']}` — {error['error']}")
    lines.extend([
        "", "## Promotion boundary", "",
        "This report is candidate-only. Numeric scores do not grant license permission or stable status. Review ownership, license, safety, accessibility, performance, originality, and evaluation evidence before preparing a candidate branch/PR.", "",
    ])
    return "\n".join(lines)


def candidate_markdown(item: Mapping[str, Any]) -> str:
    score = item["score"]
    safety = item["safety_review"]
    safe_name = re.sub(r"[\[\]()<>`#]", " ", str(item["name"]))
    return "\n".join([
        f"# {safe_name}", "",
        f"- ID: `{item['id']}`",
        f"- URL: <{item['canonical_url']}>",
        f"- Classification: `{item['classification']}`",
        f"- Score: {score['total']}/100",
        f"- License: {item['license']}",
        f"- Revision: {item['last_checked_revision']}", "",
        "## Safety signals", "",
        f"- Prompt injection: {', '.join(safety['prompt_injection_signals']) or 'none observed on the bounded surface'}",
        f"- Credential/payment: {', '.join(safety['credential_or_payment_signals']) or 'none observed on the bounded surface'}",
        f"- Install/execution: {', '.join(safety['install_or_execution_signals']) or 'none observed on the bounded surface'}",
        f"- Prohibited-source: {', '.join(safety['prohibited_source_signals']) or 'none observed on the bounded surface'}", "",
        "## Restrictions", "", str(item["copying_or_adaptation_restrictions"]), "",
        "Stable knowledge was not modified. Promotion requires the recorded reviews and a reviewed candidate branch/PR.", "",
    ])


def render_outputs(candidates: Sequence[Mapping[str, Any]], *, as_of: str, mode: str, query_errors: Sequence[Mapping[str, str]]) -> tuple[str, str, dict[str, str]]:
    yaml_text = json.dumps({
        "schema_version": 1,
        "generated_on": as_of,
        "mode": mode,
        "stable_knowledge_modified": False,
        "candidate_count": len(candidates),
        "candidates": list(candidates),
        "query_errors": list(query_errors),
    }, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    report = markdown_report(candidates, as_of=as_of, mode=mode, query_errors=query_errors)
    items = {f"items/{item['id']}.md": candidate_markdown(item) for item in candidates}
    return yaml_text, report, items


def safe_output_dir(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    knowledge = (PLUGIN_ROOT / "knowledge").resolve()
    if resolved == knowledge or knowledge in resolved.parents:
        raise DiscoveryError("Candidate reports may never be written into canonical knowledge/")
    candidate_root = (DISCOVERY_ROOT / "candidates").resolve()
    if PLUGIN_ROOT.resolve() in resolved.parents and not (resolved == candidate_root or candidate_root in resolved.parents):
        raise DiscoveryError("Repository-local reports must be under research/source-discovery/candidates/")
    return resolved


def write_reports(out_dir: Path, yaml_text: str, report: str, items: Mapping[str, str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "candidates.yml").write_text(yaml_text, encoding="utf-8")
    (out_dir / "source-discovery-report.md").write_text(report, encoding="utf-8")
    for relative, content in sorted(items.items()):
        path = out_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def build_candidates(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    query_data = load_json_yaml(Path(args.query_file))
    seed_data = load_json_yaml(Path(args.seed_file))
    seeds = effective_seed_sources(seed_data)
    registered = registry_urls(REGISTRY_FILE)
    limit = max(1, int(args.max_results))
    if args.dry_run:
        return [seed_candidate(source, as_of=args.as_of) for source in seeds[:limit]], []

    known = set(registered) | {source["canonical_url"] for source in seeds}
    discovered: dict[str, str] = {}
    errors: list[dict[str, str]] = []
    queries = [str(query) for query in query_data.get("query_templates") or []]
    for query in queries:
        if len(discovered) >= limit:
            break
        try:
            results = search_public_web(query, timeout=args.timeout, max_bytes=args.max_bytes)
        except DiscoveryError as exc:
            errors.append({"query": query, "error": str(exc)[:300]})
            continue
        for url in results:
            if url in known or url in discovered:
                continue
            discovered[url] = query
            if len(discovered) >= limit:
                break
    candidates = [
        network_candidate(url, query, as_of=args.as_of, timeout=args.timeout, max_bytes=args.max_bytes)
        for url, query in sorted(discovered.items())
    ]
    candidates.sort(key=lambda item: (-int(item["score"]["total"]), str(item["id"])))
    return candidates, errors


def parser() -> argparse.ArgumentParser:
    today = dt.date.today().isoformat()
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--query-file", type=Path, default=DEFAULT_QUERY_FILE)
    result.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    result.add_argument("--out-dir", type=Path)
    result.add_argument("--max-results", type=int, default=50)
    result.add_argument("--dry-run", action="store_true", help="Use seeds only; perform no network access and no writes.")
    result.add_argument("--as-of", default=today, help="ISO date used for deterministic report metadata.")
    result.add_argument("--timeout", type=float, default=12.0)
    result.add_argument("--max-bytes", type=int, default=300_000)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        dt.date.fromisoformat(args.as_of)
        if args.max_results < 1 or args.max_results > 500:
            raise DiscoveryError("--max-results must be between 1 and 500")
        if args.max_bytes < 10_000 or args.max_bytes > 2_000_000:
            raise DiscoveryError("--max-bytes must be between 10000 and 2000000")
        out_dir = safe_output_dir(Path(args.out_dir) if args.out_dir else DISCOVERY_ROOT / "candidates" / args.as_of[:7])
        candidates, errors = build_candidates(args)
        yaml_text, report, items = render_outputs(candidates, as_of=args.as_of, mode="offline-seed-dry-run" if args.dry_run else "public-web-candidate-discovery", query_errors=errors)
        hashes = {
            "candidates_yml": hashlib.sha256(yaml_text.encode()).hexdigest(),
            "report_md": hashlib.sha256(report.encode()).hexdigest(),
            "items": hashlib.sha256("".join(items[key] for key in sorted(items)).encode()).hexdigest(),
        }
        if not args.dry_run:
            write_reports(out_dir, yaml_text, report, items)
        print(json.dumps({
            "schema_version": 1,
            "dry_run": bool(args.dry_run),
            "network_used": not args.dry_run,
            "stable_knowledge_modified": False,
            "candidate_count": len(candidates),
            "classification_counts": {name: sum(item["classification"] == name for item in candidates) for name in sorted(CLASSIFICATIONS) if any(item["classification"] == name for item in candidates)},
            "query_error_count": len(errors),
            "out_dir": str(out_dir),
            "would_write": ["candidates.yml", "source-discovery-report.md", *sorted(items)] if args.dry_run else [],
            "written": [] if args.dry_run else ["candidates.yml", "source-discovery-report.md", *sorted(items)],
            "content_sha256": hashes,
        }, indent=2, sort_keys=True))
        return 0
    except (DiscoveryError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "stable_knowledge_modified": False}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
