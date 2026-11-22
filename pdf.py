#!/usr/bin/env python3
"""Genera un PDF de lectura, en una columna, con los capítulos 1–13."""

from html import escape
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
CHAPTERS = [
    "1 triunfador.md", "2 fallo.md", "3 colapso.md", "4 fondo.md",
    "5 vecinos.md", "6 calma.md", "7 cena.md", "8 agravamiento.md",
    "9 panico.md", "10 caos.md", "11 inaplazable.md", "12 cambio.md",
    "13 comienzo.md",
]


def markdown_to_html(text: str) -> str:
    """Convierte el Markdown sencillo del manuscrito a HTML sin dependencias."""
    out = []
    paragraph = []

    def flush():
        if paragraph:
            out.append("<p>" + " ".join(paragraph) + "</p>")
            paragraph.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
        elif stripped == "***":
            flush()
            out.append('<hr class="scene">')
        elif stripped.startswith("### "):
            flush()
            out.append("<h1>" + escape(stripped[4:]) + "</h1>")
        elif stripped.startswith("## "):
            flush()
            out.append("<h2>" + escape(stripped[3:]) + "</h2>")
        elif stripped.startswith("# "):
            flush()
            out.append("<h1>" + escape(stripped[2:]) + "</h1>")
        else:
            paragraph.append(escape(stripped))
    flush()
    return "\n".join(out)


def main():
    missing = [name for name in CHAPTERS if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit("Faltan capítulos: " + ", ".join(missing))
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        raise SystemExit("No encuentro Google Chrome/Chromium para exportar el PDF.")

    sections = []
    for name in CHAPTERS:
        body = markdown_to_html((ROOT / name).read_text(encoding="utf-8"))
        sections.append(f'<section class="chapter">{body}</section>')

    html = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Entre tontos</title><style>
@page { size: A5; margin: 15mm 14mm 16mm; }
html { font-family: "Liberation Serif", "DejaVu Serif", serif; color: #171717; }
body { margin: 0; font-size: 10.5pt; line-height: 1.38; }
.chapter { column-count: 1; }
.chapter + .chapter { break-before: page; }
h1 { text-align: center; font-size: 17pt; font-weight: normal;
     margin: 0 0 9mm; break-after: avoid; }
h2 { font-size: 13pt; break-after: avoid; }
p { margin: 0 0 0.65em; orphans: 2; widows: 2; }
hr.scene { border: 0; text-align: center; margin: 1.2em 0; break-inside: avoid; }
hr.scene:after { content: "* * *"; color: #777; letter-spacing: .3em; }
</style></head><body>""" + "\n".join(sections) + "</body></html>"

    with tempfile.TemporaryDirectory(prefix="cuentos-pdf-") as temp:
        html_path = Path(temp) / "manuscrito.html"
        html_path.write_text(html, encoding="utf-8")
        output = ROOT / "Entre tontos.pdf"
        subprocess.run([
            chrome, "--headless", "--no-sandbox", "--disable-gpu",
            f"--user-data-dir={Path(temp).resolve() / 'profile'}", "--no-pdf-header-footer", f"--print-to-pdf={output}", html_path.as_uri(),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"PDF generado: {output}")


if __name__ == "__main__":
    main()
