#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Valida os arquivos de épico e calcula a cobertura dos cenários da especificação. Imprime JSON.

Uso (a partir da raiz do workspace):
  uv run _sdd/scripts/epics.py --project docs/{projeto} validate
  uv run _sdd/scripts/epics.py --project docs/{projeto} coverage --escopo {escopo}

Formato do frontmatter: sdd-setup/references/sprint-status.md (seção "Entrada: frontmatter dos épicos").
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from sddlib import SddError, emit, fail
from status import STORY_ID, read_epic_files

SIZES = ("P", "M", "G")
KINDS = ("story", "spike", "enabler")
COVER = re.compile(r"^(RN-)?\d+\.\d+$")
SCENARIO = re.compile(r"^#{2,6}\s*Cen[aá]rio\s+(\d+\.\d+)\s*:?\s*(.*?)\s*$", re.IGNORECASE)
RULE = re.compile(r"\*\*RN-(\d+\.\d+)\*\*\s*[—–-]?\s*(.*)")


def validate(project: Path) -> dict:
    epics = read_epic_files(project)
    problems: list[str] = []
    warnings: list[str] = []
    order: list[str] = []  # ordem de build global: épicos por número, stories na ordem do arquivo
    for epic in epics:
        number = str(epic["number"])
        if not epic.get("title"):
            problems.append(f"{epic['id']}: falta title")
        if not epic.get("escopo"):
            warnings.append(f"{epic['id']}: sem escopo (a cobertura por escopo não o considera)")
        for story in epic.get("stories") or []:
            sid = str(story["id"])
            where = f"{epic['id']}/{sid}"
            match = STORY_ID.match(sid)
            if not match:
                problems.append(f"{where}: id deve ser N-M-slug (kebab-case)")
                continue
            if match.group(1) != number:
                problems.append(f"{where}: o número do épico no id é {match.group(1)}")
            if sid in order:
                problems.append(f"{where}: id repetido")
            if not story.get("title"):
                problems.append(f"{where}: falta title")
            if story.get("size") not in SIZES:
                problems.append(f"{where}: size deve ser P, M ou G")
            if story.get("kind", "story") not in KINDS:
                problems.append(f"{where}: kind deve ser story, spike ou enabler")
            covers = story.get("covers") or []
            if not isinstance(covers, list) or not all(isinstance(c, str) and COVER.match(c) for c in covers):
                problems.append(f"{where}: covers deve ser uma lista como [\"1.1\", \"RN-1.2\"]")
            elif not covers and story.get("kind", "story") == "story":
                warnings.append(f"{where}: story sem covers (não cobre nenhum cenário da especificação)")
            for dep in story.get("depends_on") or []:
                if dep not in order:
                    problems.append(f"{where}: depends_on {dep} não vem antes na ordem de build")
            order.append(sid)
    next_epic = max((e["number"] for e in epics), default=0) + 1
    return {"valid": not problems, "problems": problems, "warnings": warnings,
            "epics": [e["id"] for e in epics], "stories": len(order), "next_epic": next_epic}


def parse_spec(spec: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    scenarios: dict[str, dict] = {}
    rules: dict[str, dict] = {}
    for line in spec.read_text(encoding="utf-8").splitlines():
        match = SCENARIO.match(line.strip())
        if match:
            title = match.group(2)
            scenarios[match.group(1)] = {"title": title, "removed": "(removido)" in title.lower()}
            continue
        match = RULE.search(line)
        if match and f"RN-{match.group(1)}" not in rules:
            text = match.group(2).strip()
            rules[f"RN-{match.group(1)}"] = {"title": text, "removed": "(removido)" in text.lower()}
    return scenarios, rules


def coverage(project: Path, escopo: str) -> dict:
    spec = project / "especificacao" / escopo / "spec-functional.md"
    if not spec.is_file():
        raise SddError(f"{spec} não existe: a cobertura precisa da especificação do escopo")
    scenarios, rules = parse_spec(spec)
    if not scenarios:
        raise SddError(f"{spec.name}: nenhum cabeçalho '#### Cenário N.M' encontrado")
    covered: dict[str, list[str]] = {}
    for epic in read_epic_files(project):
        if epic.get("escopo") != escopo:
            continue
        for story in epic.get("stories") or []:
            for ref in story.get("covers") or []:
                covered.setdefault(str(ref), []).append(str(story["id"]))

    matrix = [{"id": sid, "title": s["title"], "stories": covered.get(sid, []), "removed": s["removed"]}
              for sid, s in scenarios.items()]
    uncovered = [row["id"] for row in matrix if not row["stories"] and not row["removed"]]
    rules_uncovered = [rid for rid, r in rules.items() if not r["removed"] and rid not in covered]
    known = set(scenarios) | set(rules)
    unknown = sorted({ref for ref in covered if ref not in known})
    covering_removed = sorted({ref for ref in covered if ref in known
                               and (scenarios.get(ref) or rules.get(ref))["removed"]})
    return {
        "escopo": escopo,
        "spec": str(spec),
        "complete": not uncovered and not unknown,
        "scenarios": matrix,
        "uncovered_scenarios": uncovered,
        "uncovered_rules": rules_uncovered,
        "unknown_refs": unknown,
        "covering_removed": covering_removed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, required=True, help="pasta do projeto (docs/{projeto})")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    cov = sub.add_parser("coverage")
    cov.add_argument("--escopo", required=True)
    args = parser.parse_args()

    project = args.project.resolve()
    try:
        if args.command == "validate":
            emit(validate(project))
        else:
            emit(coverage(project, args.escopo))
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
