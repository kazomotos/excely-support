#!/usr/bin/env python3
"""Validate the static Tablivio website without third-party dependencies."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
PAGES = (ROOT / "index.html", ROOT / "datenschutz.html")


class SiteParser(HTMLParser):
    """Collect structural data needed for lightweight static-site checks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.title_depth = 0
        self.title = ""
        self.h1_count = 0
        self.lang = ""
        self.meta_description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "html":
            self.lang = attributes.get("lang", "")
        if element_id := attributes.get("id"):
            if element_id in self.ids:
                raise AssertionError(f"Doppelte ID: {element_id}")
            self.ids.add(element_id)
        if tag == "a" and (href := attributes.get("href")):
            self.links.append(href)
        if tag == "title":
            self.title_depth += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and attributes.get("name") == "description":
            self.meta_description = attributes.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data


def parse_page(path: Path) -> SiteParser:
    """Parse one HTML page and assert its baseline document metadata."""
    parser = SiteParser()
    parser.feed(path.read_text(encoding="utf-8"))
    assert parser.lang == "de", f"{path.name}: lang muss de sein"
    assert parser.title.strip(), f"{path.name}: title fehlt"
    assert parser.meta_description.strip(), f"{path.name}: Meta-Beschreibung fehlt"
    assert parser.h1_count == 1, f"{path.name}: genau eine h1 erwartet"
    return parser


def validate_links(path: Path, parser: SiteParser, parsed_pages: dict[Path, SiteParser]) -> None:
    """Ensure that local documents and fragment targets resolve."""
    for href in parser.links:
        if href.startswith(("mailto:", "https://")):
            continue
        parsed = urlparse(href)
        target_path = path if not parsed.path else (ROOT / parsed.path).resolve()
        if target_path.is_dir():
            target_path /= "index.html"
        assert target_path.exists(), f"{path.name}: Linkziel fehlt: {href}"
        if parsed.fragment:
            target_parser = parsed_pages.get(target_path)
            if target_parser is None:
                target_parser = parse_page(target_path)
                parsed_pages[target_path] = target_parser
            assert parsed.fragment in target_parser.ids, (
                f"{path.name}: Sprungziel fehlt: {href}"
            )


def main() -> None:
    """Run all deterministic website checks."""
    parsed_pages = {path.resolve(): parse_page(path) for path in PAGES}
    for page in PAGES:
        validate_links(page.resolve(), parsed_pages[page.resolve()], parsed_pages)

    privacy_text = (ROOT / "datenschutz.html").read_text(encoding="utf-8")
    required_privacy_terms = (
        "Eichenstraße 1",
        "GitHub Pages",
        "Microsoft Graph",
        "macOS und iOS",
        "Apple-Schlüsselbund",
        "Bayerische Landesamt für Datenschutzaufsicht",
    )
    for term in required_privacy_terms:
        assert term in privacy_text, f"Datenschutzangabe fehlt: {term}"

    support_text = (ROOT / "index.html").read_text(encoding="utf-8")
    required_support_terms = (
        'id="hilfe"',
        'id="funktionen"',
        'id="faq"',
        "Microsoft-365-Geschäfts- und Schulkonten",
        "Keine sensiblen Dateien senden",
        "Supportanfrage öffnen",
        "https://kazomotos.github.io/tablivio-support/",
        "assets/tablivio-support-social.png",
    )
    for term in required_support_terms:
        assert term in support_text, f"Supportangabe fehlt: {term}"

    for page in PAGES:
        page_text = page.read_text(encoding="utf-8")
        assert ">Excely<" not in page_text, (
            f"{page.name}: sichtbarer alter Produktname gefunden"
        )

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert "@media (max-width: 660px)" in css, "Mobile Breakpoint fehlt"
    assert ":focus-visible" in css, "Sichtbarer Tastaturfokus fehlt"
    assert "prefers-reduced-motion" in css, "Reduced-Motion-Regel fehlt"
    brand_rule = css.split(".brand {", maxsplit=1)[1].split("}", maxsplit=1)[0]
    assert "font-weight: bold;" in brand_rule, (
        "Tablivio-Wortmarke muss fett gesetzt sein"
    )

    required_assets = (
        ROOT / "assets" / "tablivio-mark.png",
        ROOT / "assets" / "tablivio-support-social.png",
        ROOT / "assets" / "screenshots" / "timer-macos.webp",
        ROOT / "assets" / "screenshots" / "microsoft-365-macos.webp",
        ROOT / "assets" / "screenshots" / "filter-macos.webp",
        ROOT / "assets" / "screenshots" / "smart-fill-macos.webp",
        ROOT / "assets" / "screenshots" / "entry-ios.webp",
        ROOT / "favicon.png",
    )
    for asset in required_assets:
        assert asset.is_file() and asset.stat().st_size > 0, (
            f"Bilddatei fehlt oder ist leer: {asset.relative_to(ROOT)}"
        )

    print(f"OK: {len(PAGES)} Seiten, lokale Links und Pflichtangaben geprüft.")


if __name__ == "__main__":
    main()
