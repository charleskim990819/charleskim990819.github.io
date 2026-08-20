#!/usr/bin/env python3
"""Render _data/cv.yml to assets/pdf/Chansoo_Kim_CV.pdf.

The web CV and the downloadable PDF are generated from the same YAML, so
editing _data/cv.yml keeps both in sync. Run from the repository root:

    python scripts/build_cv_pdf.py

Requires a Chrome or Edge binary for the HTML -> PDF step (headless).
"""

import html
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CV_YAML = os.path.join(REPO, "_data", "cv.yml")
OUT_PDF = os.path.join(REPO, "assets", "pdf", "Chansoo_Kim_CV.pdf")

BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "google-chrome",
    "chromium",
]

CSS = """
@page { size: A4; margin: 16mm 15mm 14mm; }
* { box-sizing: border-box; }
body { font-family: "Inter","Segoe UI","Malgun Gothic",sans-serif; font-size: 9.4pt;
       line-height: 1.45; color:#16161d; margin:0; }
header { border-bottom: 1.6pt solid #16161d; padding-bottom: 7pt; margin-bottom: 12pt; }
h1 { font-size: 21pt; font-weight: 700; letter-spacing:-0.02em; margin:0 0 2pt; }
.label { font-size: 10pt; color:#4a4a58; margin-bottom:5pt; }
.contact { font-size: 8.1pt; color:#5c5c6a; }
h2 { font-size: 8.4pt; font-weight:700; letter-spacing:0.13em; text-transform:uppercase;
     color:#3a3aa0; border-bottom:0.5pt solid #c9c9d4; padding-bottom:3pt; margin:13pt 0 7pt; }
.entry { display:grid; grid-template-columns: 72pt 1fr; gap:9pt; margin-bottom:8pt;
         break-inside: avoid; }
.date { font-size:8.1pt; color:#6a6a78; padding-top:1pt; white-space:nowrap; }
.t { font-weight:600; font-size:9.8pt; }
.o { font-size:8.7pt; color:#55555f; margin-bottom:2pt; }
.body p { margin:2pt 0 0; text-align:justify; }
.body ul { margin:2pt 0 0; padding-left:12pt; }
.body li { margin-bottom:1pt; }
.summary { margin:0; text-align:justify; }
.ra { margin-bottom:6pt; break-inside:avoid; }
.ra .t { font-weight:600; }
.ra p { margin:1pt 0 0; }
.sk { display:grid; grid-template-columns:96pt 1fr; gap:9pt; margin-bottom:3.5pt;
      break-inside:avoid; }
.cat { font-weight:600; }
.items { color:#3c3c48; }
"""


def esc(value):
    return html.escape(str(value)) if value else ""


def md(value):
    """Minimal markdown: *emphasis* only, which is all cv.yml uses."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", esc(value))


def date_range(start, end=None):
    return f"{start} – {end}" if end else str(start)


def entry_block(date, title, org, body_html):
    return (
        f'<div class="entry"><div class="date">{esc(date)}</div>'
        f'<div class="body"><div class="t">{title}</div>'
        f'<div class="o">{esc(org)}</div>{body_html}</div></div>'
    )


def build_html(cv):
    sections = cv["sections"]
    out = []

    contact = " &nbsp;·&nbsp; ".join(
        [
            esc(cv["email"]),
            f"{esc(cv['address']['street'])}, {esc(cv['address']['region'])}, "
            f"{esc(cv['address']['city'])}",
            "github.com/charleskim990819",
            "linkedin.com/in/charleskim99",
            "charleskim99.com",
        ]
    )
    out.append(
        f'<header><h1>{esc(cv["name"])}</h1>'
        f'<div class="label">{esc(cv["label"])}</div>'
        f'<div class="contact">{contact}</div></header>'
        f'<section><h2>Summary</h2>'
        f'<p class="summary">{esc(cv["summary"].strip())}</p></section>'
    )

    rows = []
    for e in sections["Education"]:
        bullets = "".join(f"<li>{md(h)}</li>" for h in e.get("highlights", []))
        rows.append(
            entry_block(
                date_range(e["start_date"], e["end_date"]),
                f'{esc(e["studyType"])}, {esc(e["area"])}',
                f'{esc(e["institution"])} · {esc(e["location"])}',
                f"<ul>{bullets}</ul>",
            )
        )
    out.append("<section><h2>Education</h2>" + "".join(rows) + "</section>")

    rows = []
    for e in sections["Experience"]:
        rows.append(
            entry_block(
                date_range(e["start_date"], e["end_date"]),
                esc(e["position"]),
                f'{esc(e["company"])} · {esc(e["location"])}',
                f'<p>{md(e["summary"].strip())}</p>',
            )
        )
    out.append("<section><h2>Experience</h2>" + "".join(rows) + "</section>")

    # Any remaining title/organization/date/description section renders generically,
    # in the order it appears in cv.yml.
    generic = [
        k
        for k in sections
        if k
        not in (
            "Education",
            "Experience",
            "Research Areas",
            "Skills",
            "Languages",
            "Interests",
        )
    ]
    for name in generic:
        rows = []
        for e in sections[name]:
            rows.append(
                entry_block(
                    e.get("date", ""),
                    esc(e.get("title", "")),
                    e.get("organization", ""),
                    f'<p>{md(e.get("description", "").strip())}</p>',
                )
            )
        out.append(f"<section><h2>{esc(name)}</h2>" + "".join(rows) + "</section>")

    rows = [
        f'<div class="ra"><div class="t">{esc(e["title"])}</div>'
        f'<p>{md(e["summary"].strip())}</p></div>'
        for e in sections["Research Areas"]
    ]
    out.append("<section><h2>Research Areas</h2>" + "".join(rows) + "</section>")

    rows = [
        f'<div class="sk"><span class="cat">{esc(e["category"])}</span>'
        f'<span class="items">{esc(", ".join(e["items"]))}</span></div>'
        for e in sections["Skills"]
    ]
    out.append("<section><h2>Technical Skills</h2>" + "".join(rows) + "</section>")

    rows = [
        f'<div class="sk"><span class="cat">{esc(e["language"])}</span>'
        f'<span class="items">{esc(e["fluency"])}</span></div>'
        for e in sections["Languages"]
    ]
    out.append("<section><h2>Languages</h2>" + "".join(rows) + "</section>")

    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        f'<title>{esc(cv["name"])} — CV</title><style>{CSS}</style></head>'
        f'<body>{"".join(out)}</body></html>'
    )


def find_browser():
    for candidate in BROWSERS:
        if os.path.exists(candidate):
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    return None


def main():
    with io.open(CV_YAML, encoding="utf-8") as fh:
        cv = yaml.safe_load(fh)["cv"]

    browser = find_browser()
    if not browser:
        sys.exit("No Chrome/Edge binary found; cannot render the PDF.")

    tmp_dir = tempfile.mkdtemp()
    tmp_html = os.path.join(tmp_dir, "cv.html")
    with io.open(tmp_html, "w", encoding="utf-8") as fh:
        fh.write(build_html(cv))

    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    subprocess.run(
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            f"--print-to-pdf={OUT_PDF}",
            "file:///" + tmp_html.replace("\\", "/"),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"wrote {OUT_PDF} ({os.path.getsize(OUT_PDF) // 1024} KB)")


if __name__ == "__main__":
    main()
