#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Confere as citações de um documento de pesquisa (discovery-research). Imprime JSON.

Uso:
  uv run _sdd/scripts/research.py check docs/{projeto}/discovery/pesquisa/concorrentes.md

Regras:
- Cada frase ou célula de tabela com afirmação quantitativa (%, moeda, mil/milhões/bilhões) cita a
  própria fonte [n] ou está marcada como estimativa ("(estimativa" ou "(est.").
- Todo [n] citado existe na seção "## Fontes", com link http(s) e data de acesso (AAAA-MM-DD ou DD/MM/AAAA).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from sddlib import SddError, emit, fail

QUANT = re.compile(
    r"\d[\d.,]*\s*%"
    r"|(?:R\$|US\$|USD|BRL|EUR|€|\$)\s?\d"
    r"|\d[\d.,]*\s*(?:mil\b|milh(?:ão|ões|oes)|bilh(?:ão|ões|oes)|trilh(?:ão|ões|oes)|mi\b|bi\b|tri\b|[kKMB]\b)",
    re.IGNORECASE,
)
CITE = re.compile(r"\[(\d+)\]")
ESTIMATE = re.compile(r"\((?:estimativa|est\.)", re.IGNORECASE)
SOURCE = re.compile(r"^\s*(?:-\s*)?\[(\d+)\]\s*(.+)$")
URL = re.compile(r"https?://\S+")
SEGMENT = re.compile(r"(?<=[.;!?])\s+|\|")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{2}/\d{2}/\d{4}\b")


def check(path: Path) -> dict:
    if not path.is_file():
        raise SddError(f"{path} não existe")
    lines = path.read_text(encoding="utf-8").splitlines()
    problems: list[str] = []
    warnings: list[str] = []
    cited: set[str] = set()
    sources: dict[str, str] = {}
    section = ""
    in_code = in_front = False
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if number == 1 and stripped == "---":
            in_front = True
            continue
        if in_front:
            in_front = stripped != "---"
            continue
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith("#"):
            section = stripped.lstrip("#").strip().lower()
            continue
        if section == "fontes":
            match = SOURCE.match(stripped)
            if match:
                n, text = match.groups()
                if n in sources:
                    problems.append(f"fonte [{n}] declarada duas vezes")
                sources[n] = text
                if not URL.search(text):
                    problems.append(f"fonte [{n}] sem link http(s)")
                if not DATE.search(text):
                    problems.append(f"fonte [{n}] sem data de acesso")
            continue
        refs = CITE.findall(line)
        cited.update(refs)
        if section.startswith("limites") or section.startswith("revis"):
            continue
        # Cada frase (ou célula de tabela) com número precisa da própria citação ou marca de estimativa.
        for segment in SEGMENT.split(line):
            if QUANT.search(segment) and not CITE.search(segment) and not ESTIMATE.search(segment):
                problems.append(f"linha {number}: número sem fonte [n] nem marca de estimativa: {segment.strip()[:100]}")
    for n in sorted(cited - set(sources), key=int):
        problems.append(f"[{n}] citado, mas não está em '## Fontes'")
    for n in sorted(set(sources) - cited, key=int):
        warnings.append(f"fonte [{n}] declarada e não citada")
    if not sources:
        warnings.append("documento sem seção '## Fontes'")
    return {"file": str(path), "valid": not problems, "problems": problems, "warnings": warnings,
            "sources": len(sources), "citations": len(cited)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    chk = sub.add_parser("check")
    chk.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        emit(check(args.file))
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
