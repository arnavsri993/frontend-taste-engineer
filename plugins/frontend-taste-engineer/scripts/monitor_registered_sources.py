#!/usr/bin/env python3
"""Monitor registered public sources without changing stable knowledge.

The monitor reads the reviewed source registry, resolves GitHub repository heads and
license metadata, fingerprints bounded visible text for other public pages, compares
the observations with the registry and an optional prior report, and writes reviewable
JSON/Markdown reports. It never executes source code or promotes knowledge.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from html.parser import HTMLParser
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import sys
from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = PLUGIN_ROOT / "research" / "source-registry.yml"
USER_AGENT = "FrontendTasteEngineer-SourceMonitor/0.1 (+bounded-public-metadata)"
TEXT_CONTENT_TYPES = {
    "text/html",
    "application/xhtml+xml",
    "text/plain",
    "application/json",
    "application/ld+json",
    "text/markdown",
}
AUTH_PATH_RE = re.compile(
    r"/(?:login|log-in|signin|sign-in|account|billing|checkout|admin|private|members?)(?:/|$)",
    re.IGNORECASE,
)
IMMUTABLE_REVISION_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{7,40}(?![0-9a-f])", re.I)


class MonitorError(ValueError):
    """Expected, user-actionable monitor failure."""


@dataclass(frozen=True)
class Response:
    status: int
    final_url: str
    content_type: str
    headers: Mapping[str, str]
    body: bytes


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_registry(path: Path) -> list[dict[str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise MonitorError(f"Cannot read source registry {path}: {exc}") from exc
    entries: list[dict[str, str]] = []
    for raw in re.split(r"(?m)^  - id: ", text)[1:]:
        entry = {"id": _unquote(raw.splitlines()[0])}
        for field in (
            "canonical_url",
            "classification",
            "license",
            "last_checked_revision",
            "maintenance_status",
        ):
            match = re.search(rf"(?m)^    {re.escape(field)}:\s*(.*)$", raw)
            if match:
                entry[field] = _unquote(match.group(1))
        missing = [field for field in ("id", "canonical_url", "classification", "last_checked_revision") if not entry.get(field)]
        if missing:
            raise MonitorError(f"Registry source {entry.get('id') or '<unknown>'} lacks: {', '.join(missing)}")
        entries.append(entry)
    if not entries:
        raise MonitorError("No registered sources were found")
    return entries


def normalize_url(raw: str) -> str:
    parsed = urlsplit(raw.strip())
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise MonitorError(f"Only absolute public HTTP(S) URLs are supported: {raw!r}")
    if parsed.username or parsed.password:
        raise MonitorError("URLs containing credentials are prohibited")
    host = parsed.hostname.lower().rstrip(".")
    port = f":{parsed.port}" if parsed.port else ""
    path = re.sub(r"/+", "/", parsed.path or "")
    return urlunsplit((parsed.scheme.lower(), host + port, path, parsed.query, ""))


def public_url(raw: str) -> str:
    normalized = normalize_url(raw)
    parsed = urlsplit(normalized)
    host = parsed.hostname or ""
    if host in {"localhost", "localhost.localdomain"} or host.endswith((".local", ".internal", ".localhost")):
        raise MonitorError("Local and private hostnames are prohibited")
    if AUTH_PATH_RE.search(parsed.path):
        raise MonitorError("Authenticated/account paths are outside monitor scope")
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        literal = None
    if literal is not None and not literal.is_global:
        raise MonitorError("Private, reserved, loopback, or link-local addresses are prohibited")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or 443, type=socket.SOCK_STREAM)}
    except socket.gaierror as exc:
        raise MonitorError(f"Hostname resolution failed for {host}: {exc}") from exc
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise MonitorError(f"Hostname {host} resolves to a non-public address")
    return normalized


class SafeRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Request | None:
        target = public_url(urljoin(req.full_url, newurl))
        return super().redirect_request(req, fp, code, msg, headers, target)


class HttpClient:
    def __init__(self, *, timeout: float, max_bytes: int, github_token: str = "") -> None:
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.github_token = github_token
        self.opener = build_opener(SafeRedirectHandler())

    def fetch(self, url: str, *, github_api: bool = False) -> Response:
        target = public_url(url)
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json" if github_api else "text/html,application/xhtml+xml,text/plain,application/json,text/markdown;q=0.8",
            "Accept-Encoding": "identity",
        }
        if github_api and self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
            headers["X-GitHub-Api-Version"] = "2022-11-28"
        request = Request(target, headers=headers, method="GET")
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                final_url = public_url(response.geturl())
                content_type = response.headers.get_content_type().lower()
                if content_type not in TEXT_CONTENT_TYPES:
                    raise MonitorError(f"Unsupported content type {content_type}")
                declared = response.headers.get("Content-Length")
                if declared and int(declared) > self.max_bytes:
                    raise MonitorError(f"Response exceeds {self.max_bytes} bytes")
                body = response.read(self.max_bytes + 1)
                if len(body) > self.max_bytes:
                    raise MonitorError(f"Response exceeds {self.max_bytes} bytes")
                selected_headers = {
                    key.lower(): value
                    for key, value in response.headers.items()
                    if key.lower() in {"etag", "last-modified", "content-type"}
                }
                return Response(int(response.status), final_url, content_type, selected_headers, body)
        except HTTPError as exc:
            raise MonitorError(f"HTTP {exc.code} from {urlsplit(target).hostname}") from exc
        except (URLError, TimeoutError, OSError, ValueError) as exc:
            raise MonitorError(f"Request failed for {urlsplit(target).hostname}: {exc}") from exc


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            clean = " ".join(data.split())
            if clean:
                self.parts.append(clean)


def visible_fingerprint(response: Response) -> str:
    text = response.body.decode("utf-8", errors="replace")
    if response.content_type in {"text/html", "application/xhtml+xml"}:
        parser = VisibleTextParser()
        parser.feed(text)
        text = " ".join(parser.parts)
    normalized = " ".join(text.split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def github_repo(url: str) -> tuple[str, str] | None:
    parsed = urlsplit(normalize_url(url))
    if parsed.hostname not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    return parts[0], re.sub(r"\.git$", "", parts[1])


def immutable_registry_revision(value: str) -> str | None:
    match = IMMUTABLE_REVISION_RE.search(value)
    return match.group(0).lower() if match else None


def prior_sources(value: Mapping[str, Any] | None) -> dict[str, Mapping[str, Any]]:
    if not value:
        return {}
    sources = value.get("sources") or []
    if not isinstance(sources, list):
        return {}
    return {str(item.get("id")): item for item in sources if isinstance(item, Mapping) and item.get("id")}


def _json_response(response: Response, source_id: str) -> Mapping[str, Any]:
    try:
        value = json.loads(response.body.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise MonitorError(f"GitHub metadata for {source_id} was not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise MonitorError(f"GitHub metadata for {source_id} was not an object")
    return value


def monitor_github_source(source: Mapping[str, str], client: HttpClient, previous: Mapping[str, Any] | None) -> dict[str, Any]:
    owner_repo = github_repo(source["canonical_url"])
    if not owner_repo:
        raise MonitorError(f"{source['id']} is not a GitHub repository URL")
    owner, repo = owner_repo
    repo_response = client.fetch(f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}", github_api=True)
    metadata = _json_response(repo_response, source["id"])
    default_branch = str(metadata.get("default_branch") or "main")
    commit_response = client.fetch(
        f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}/commits/{quote(default_branch)}",
        github_api=True,
    )
    commit = _json_response(commit_response, source["id"])
    latest_revision = str(commit.get("sha") or "").lower()
    if not re.fullmatch(r"[0-9a-f]{40}", latest_revision):
        raise MonitorError(f"GitHub did not return an immutable revision for {source['id']}")
    commit_data = commit.get("commit") if isinstance(commit.get("commit"), Mapping) else {}
    committer = commit_data.get("committer") if isinstance(commit_data.get("committer"), Mapping) else {}
    observed_license = ""
    if isinstance(metadata.get("license"), Mapping):
        observed_license = str(metadata["license"].get("spdx_id") or "")
    registry_revision = immutable_registry_revision(source["last_checked_revision"])
    reasons: list[str] = []
    revision_changed: bool | None
    if registry_revision:
        revision_changed = not latest_revision.startswith(registry_revision)
        if revision_changed:
            reasons.append("upstream-revision-changed")
    else:
        revision_changed = None
        reasons.append("registry-revision-not-immutable")
    registry_license = source.get("license", "").lower()
    license_changed = bool(observed_license and observed_license not in {"NOASSERTION", "OTHER"} and observed_license.lower() not in registry_license)
    if license_changed:
        reasons.append("license-metadata-needs-review")
    archived = bool(metadata.get("archived") or metadata.get("disabled"))
    if archived:
        reasons.append("repository-archived-or-disabled")
    previous_revision = str((previous or {}).get("observed_revision") or "")
    changed_since_prior = bool(previous_revision and previous_revision != latest_revision)
    return {
        "id": source["id"],
        "canonical_url": source["canonical_url"],
        "classification": source["classification"],
        "kind": "github-repository",
        "status": "reachable",
        "registry_revision": source["last_checked_revision"],
        "observed_revision": latest_revision,
        "observed_at": committer.get("date") or metadata.get("pushed_at"),
        "revision_changed": revision_changed,
        "changed_since_prior_monitor": changed_since_prior,
        "default_branch": default_branch,
        "observed_license": observed_license or "unknown",
        "license_changed": license_changed,
        "archived_or_disabled": archived,
        "content_sha256": None,
        "content_changed_since_prior": None,
        "review_reasons": reasons,
    }


def monitor_page_source(source: Mapping[str, str], client: HttpClient, previous: Mapping[str, Any] | None) -> dict[str, Any]:
    response = client.fetch(source["canonical_url"])
    fingerprint = visible_fingerprint(response)
    previous_hash = str((previous or {}).get("content_sha256") or "")
    content_changed = bool(previous_hash and previous_hash != fingerprint)
    reasons: list[str] = []
    if content_changed:
        reasons.append("public-content-changed")
    if source["classification"] in {"inaccessible", "rejected"}:
        reasons.append("previously-blocked-source-became-reachable")
    canonical = normalize_url(source["canonical_url"])
    final_url = normalize_url(response.final_url)
    if (urlsplit(canonical).hostname, urlsplit(canonical).path.rstrip("/")) != (urlsplit(final_url).hostname, urlsplit(final_url).path.rstrip("/")):
        reasons.append("canonical-redirect-changed")
    return {
        "id": source["id"],
        "canonical_url": source["canonical_url"],
        "classification": source["classification"],
        "kind": "public-text",
        "status": "reachable",
        "registry_revision": source["last_checked_revision"],
        "observed_revision": None,
        "observed_at": response.headers.get("last-modified"),
        "revision_changed": None,
        "changed_since_prior_monitor": None,
        "final_url": response.final_url,
        "etag": response.headers.get("etag"),
        "content_sha256": fingerprint,
        "content_changed_since_prior": content_changed,
        "review_reasons": reasons,
    }


def monitor_sources(
    sources: Sequence[Mapping[str, str]],
    client: HttpClient,
    *,
    baseline: Mapping[str, Any] | None = None,
    as_of: str,
) -> dict[str, Any]:
    previous_by_id = prior_sources(baseline)
    results: list[dict[str, Any]] = []
    for source in sources:
        previous = previous_by_id.get(source["id"])
        try:
            if github_repo(source["canonical_url"]):
                result = monitor_github_source(source, client, previous)
            else:
                result = monitor_page_source(source, client, previous)
        except MonitorError as exc:
            reasons = [] if source["classification"] in {"inaccessible", "rejected"} else ["source-unreachable"]
            result = {
                "id": source["id"],
                "canonical_url": source["canonical_url"],
                "classification": source["classification"],
                "kind": "github-repository" if github_repo(source["canonical_url"]) else "public-text",
                "status": "unreachable",
                "registry_revision": source["last_checked_revision"],
                "observed_revision": None,
                "observed_at": None,
                "content_sha256": None,
                "review_reasons": reasons,
                "error": str(exc)[:300],
            }
        results.append(result)
    review_count = sum(bool(item["review_reasons"]) for item in results)
    return {
        "schema_version": 1,
        "generated_on": as_of,
        "network_used": True,
        "stable_knowledge_modified": False,
        "baseline_used": bool(baseline),
        "review_required": review_count > 0,
        "summary": {
            "registered_sources": len(results),
            "reachable": sum(item["status"] == "reachable" for item in results),
            "unreachable": sum(item["status"] == "unreachable" for item in results),
            "sources_requiring_review": review_count,
        },
        "sources": results,
        "collection_policy": {
            "stored": ["canonical URLs", "public revision and license metadata", "bounded visible-text fingerprints", "reachability and redirect metadata"],
            "not_stored": ["page dumps", "binaries", "cookies", "credentials", "browser profiles", "private or paid content"],
            "automatic_promotion": False,
        },
    }


def markdown_report(report: Mapping[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Registered source monitor",
        "",
        f"Generated: {report['generated_on']}  ",
        f"Registered sources checked: {summary['registered_sources']}  ",
        f"Sources requiring review: {summary['sources_requiring_review']}  ",
        "Stable knowledge modified: no",
        "",
        "## Review queue",
        "",
    ]
    review_items = [item for item in report["sources"] if item["review_reasons"]]
    if not review_items:
        lines.append("No registered source change requires review.")
    else:
        lines.extend(["| Source | Observation | Reasons |", "|---|---|---|"])
        for item in review_items:
            observation = item.get("observed_revision") or item.get("status") or "unknown"
            reasons = ", ".join(item["review_reasons"])
            lines.append(f"| `{item['id']}` | `{observation}` | {reasons} |")
    lines.extend([
        "",
        "## All registered sources",
        "",
        "| Source | Kind | Status | Review |",
        "|---|---|---|---|",
    ])
    for item in report["sources"]:
        lines.append(f"| `{item['id']}` | {item['kind']} | {item['status']} | {'yes' if item['review_reasons'] else 'no'} |")
    lines.extend([
        "",
        "## Boundary",
        "",
        "This is a report-only monitor. A changed revision, page fingerprint, license signal, redirect, or availability state is evidence for review—not permission to copy, execute, install, or promote source material. Stable knowledge changes still require provenance, license review, evaluation, and a reviewed candidate pull request.",
        "",
    ])
    return "\n".join(lines)


def load_baseline(path: Path | None) -> Mapping[str, Any] | None:
    if not path or not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise MonitorError(f"Cannot read baseline report {path}: {exc}") from exc
    if not isinstance(value, Mapping):
        raise MonitorError("Baseline report must be a JSON object")
    return value


def safe_output(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    knowledge = (PLUGIN_ROOT / "knowledge").resolve()
    if resolved == knowledge or knowledge in resolved.parents:
        raise MonitorError("Monitor reports may never be written into canonical knowledge/")
    return resolved


def write_report(path: Path, content: str) -> None:
    destination = safe_output(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    result.add_argument("--baseline-json", type=Path)
    result.add_argument("--json-out", type=Path)
    result.add_argument("--md-out", type=Path)
    result.add_argument("--source-id", action="append", default=[], help="Limit monitoring to one or more registered source IDs.")
    result.add_argument("--as-of", default=dt.date.today().isoformat())
    result.add_argument("--timeout", type=float, default=12.0)
    result.add_argument("--max-bytes", type=int, default=400_000)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        dt.date.fromisoformat(args.as_of)
        if args.timeout <= 0 or args.timeout > 60:
            raise MonitorError("--timeout must be greater than 0 and at most 60 seconds")
        if args.max_bytes < 10_000 or args.max_bytes > 2_000_000:
            raise MonitorError("--max-bytes must be between 10000 and 2000000")
        sources = parse_registry(args.registry)
        if args.source_id:
            selected = set(args.source_id)
            sources = [source for source in sources if source["id"] in selected]
            missing = sorted(selected - {source["id"] for source in sources})
            if missing:
                raise MonitorError(f"Unknown source IDs: {', '.join(missing)}")
        report = monitor_sources(
            sources,
            HttpClient(timeout=args.timeout, max_bytes=args.max_bytes, github_token=os.environ.get("GITHUB_TOKEN", "")),
            baseline=load_baseline(args.baseline_json),
            as_of=args.as_of,
        )
        json_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
        markdown = markdown_report(report)
        if args.json_out:
            write_report(args.json_out, json_text)
        if args.md_out:
            write_report(args.md_out, markdown)
        print(json.dumps({
            "network_used": True,
            "stable_knowledge_modified": False,
            "review_required": report["review_required"],
            "summary": report["summary"],
            "json_out": str(args.json_out) if args.json_out else None,
            "md_out": str(args.md_out) if args.md_out else None,
        }, indent=2, sort_keys=True))
        return 0
    except (MonitorError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "stable_knowledge_modified": False}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
