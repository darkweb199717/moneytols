#!/usr/bin/env python3
"""MoneyTols daily site audit. Reports issues; never edits website or ad code."""
from __future__ import annotations
import os
import re
import ssl
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://moneytols.com/"
REPORT = ROOT / "audit" / "daily-findings.md"

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.in_title = False
        self.description = ""
        self.canonical = ""
        self.ids = set()
        self.duplicate_ids = set()
        self.links = []
        self.images = []
        self.scripts = []
        self.structured = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicate_ids.add(a["id"])
            self.ids.add(a["id"])
        if tag == "meta" and a.get("name", "").lower() == "description":
            self.description = a.get("content", "")
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonical = a.get("href", "")
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images.append(a)
        if tag == "script":
            self.scripts.append(a)
            if a.get("type") == "application/ld+json":
                self.structured += 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

def fetch_status(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "MoneyTolsMaintenanceAudit/1.0 (+https://moneytols.com/)"})
    try:
        with urllib.request.urlopen(request, timeout=14) as response:
            return response.status, ""
    except urllib.error.HTTPError as exc:
        return exc.code, "HTTP error"
    except Exception as exc:
        return None, type(exc).__name__

def main():
    findings = []
    def flag(level, issue):
        findings.append((level, issue))
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(source)

    if not page.title.strip():
        flag("High", "Homepage is missing a `<title>`.")
    if not page.description.strip():
        flag("High", "Homepage is missing a meta description.")
    if page.canonical.rstrip("/") != SITE.rstrip("/"):
        flag("High", "Homepage canonical URL differs from https://moneytols.com/.")
    if page.duplicate_ids:
        flag("Medium", "Duplicate element IDs: " + ", ".join(sorted(page.duplicate_ids)[:12]))
    if not page.structured:
        flag("Medium", "No JSON-LD structured data found.")

    # Test only same-page fragments; the SPA may intentionally use hashes for navigation.
    targets = {x[1:] for x in page.links if x.startswith("#") and len(x) > 1}
    missing = sorted(targets - page.ids)
    # JavaScript routing hashes are legitimate and not treated as broken HTML anchors.
    if missing and len(missing) <= 5:
        flag("Info", "Review JavaScript-routed hash links: " + ", ".join("#" + x for x in missing))

    # Images are verified only where a static local path was declared.
    for img in page.images:
        src = img.get("src", "")
        if src.startswith("/") and not src.startswith("//"):
            if not (ROOT / src.lstrip("/")).is_file():
                flag("Medium", "Local image referenced but absent from repository: `" + src + "`")
        if not img.get("alt", "").strip():
            flag("Low", "At least one image is missing alternative text.")
            break

    for resource in ("robots.txt", "sitemap.xml"):
        if not (ROOT / resource).is_file():
            flag("High", "Missing repository file: `" + resource + "`")

    # Network probes do not modify the website.
    for path in ("", "robots.txt", "sitemap.xml"):
        url = urljoin(SITE, path)
        status, err = fetch_status(url)
        if status is None:
            flag("Medium", "Could not verify " + url + " (" + err + "); investigate connectivity.")
        elif status >= 400:
            flag("High", url + " returned HTTP " + str(status) + ".")

    # Preserve all ad / sponsored / tracking code. The job only writes its report.
    lines = [
        "# MoneyTols daily audit findings",
        "",
        "Automated static checks and basic live-URL checks. No website code, advertisements, sponsored links, or calculator calculations are changed by this job.",
        "",
    ]
    if findings:
        severity = {"High": 0, "Medium": 1, "Low": 2, "Info": 3}
        for level, issue in sorted(set(findings), key=lambda x: (severity[x[0]], x[1])):
            lines.append("- **" + level + ":** " + issue)
    else:
        lines.append("No issues detected by these limited checks.")
    lines += [
        "",
        "## Manual review still required",
        "",
        "Calculator accuracy, real mobile rendering, browser interactions, ad delivery, and Core Web Vitals are not verified by these checks.",
        "",
        "Do not merge an audit report as a replacement for testing or approval of code fixes.",
        "",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    # Do not fail CI just because a report contains findings: the review PR communicates them.

if __name__ == "__main__":
    main()
