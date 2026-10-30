#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Confere o arquivo de uma story (implementacao/stories/{id}.md). Imprime JSON.

Uso (a partir da raiz do workspace):
  uv run _sdd/scripts/story.py --project docs/{projeto} check {id}

Template e regras: create-story/references/template-story.md (plugin delivery).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from sddlib import SddError, emit, fail
from status import EPIC_ID, STATUS_FILE, STORY_ID, find, load, read_frontmatter

# Títulos fixos (lidos por scripts e pelas skills do fluxo), em qualquer idioma de documento.
SECTIONS = (
    "História",
    "Critérios de aceite",
    "Tarefas",
    "Repositórios",
    "Contexto para o desenvolvimento",
    "Fora desta story",
    "Registro do desenvolvimento",
    "Arquivos alterados",
    "Revisão",
    "Histórico",
)
REQUIRED_FIELDS = ("id", "epic", "status", "title", "kind", "covers", "repositories", "branch")
CA = re.compile(r"\*\*(CA-\d+)\*\*")
CA_REF = re.compile(r"\bCA-\d+\b")
CHECKBOX = re.compile(r"^\s*-\s*\[( |x|X)\]", re.MULTILINE)
DOC_PATH = re.compile(r"`((?:docs|[\w.-]+)/[^`\s]+?\.(?:md|ya?ml|json))(?:#[^`]*)?`")


def sections(text: str) -> dict[str, str]:
    """Conteúdo de cada seção '## Título' (sem o título)."""
    found: dict[str, str] = {}
    current = None
    buffer: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                found[current] = "\n".join(buffer)
            current, buffer = line[3:].strip(), []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        found[current] = "\n".join(buffer)
    return found


def check(project: Path, story_id: str) -> dict:
    path = project / "implementacao" / "stories" / f"{story_id}.md"
    if not path.is_file():
        raise SddError(f"{path} não existe")
    problems: list[str] = []
    warnings: list[str] = []
    front = read_frontmatter(path)
    text = path.read_text(encoding="utf-8")

    for field in REQUIRED_FIELDS:
        if field not in front:
            problems.append(f"frontmatter sem {field}")
    if front.get("id") != story_id:
        problems.append(f"frontmatter id {front.get('id')!r} diferente do nome do arquivo ({story_id})")
    match = STORY_ID.match(story_id)
    epic_match = EPIC_ID.match(str(front.get("epic", "")))
    if not match:
        problems.append("id deve ser N-M-slug")
    elif not epic_match or epic_match.group(1) != match.group(1):
        problems.append(f"epic {front.get('epic')!r} não corresponde ao número no id")
    covers = front.get("covers") or []
    repos = front.get("repositories") or []
    if not isinstance(covers, list) or not isinstance(repos, list):
        problems.append("covers e repositories devem ser listas")
        covers, repos = [], []
    if front.get("kind", "story") == "story" and not covers:
        problems.append("story sem covers")

    body = sections(text)
    for name in SECTIONS:
        if name not in body:
            problems.append(f"falta a seção '## {name}'")

    criteria = body.get("Critérios de aceite", "")
    tasks = body.get("Tarefas", "")
    ca_ids = list(dict.fromkeys(CA.findall(criteria)))
    if not ca_ids:
        problems.append("nenhum critério de aceite no formato **CA-N**")
    referenced = set(CA_REF.findall(tasks))
    for ca in ca_ids:
        if ca not in referenced:
            problems.append(f"{ca} não tem tarefa (cite '({ca})' em alguma tarefa)")
    for ref in sorted(referenced - set(ca_ids)):
        problems.append(f"tarefa cita {ref}, que não existe nos critérios")
    for ref in covers:
        if not re.search(rf"(?<![\d.]){re.escape(str(ref))}(?![\d])", criteria):
            problems.append(f"covers {ref} não aparece nos critérios de aceite")
    boxes = CHECKBOX.findall(tasks)
    if not boxes:
        problems.append("Tarefas sem checklist (- [ ] ...)")

    root = project.parent.parent
    context = body.get("Contexto para o desenvolvimento", "")
    for ref in sorted(set(DOC_PATH.findall(context))):
        if ref.startswith(("docs/", f"{project.parent.name}/")) and not (root / ref).exists():
            problems.append(f"referência inexistente: {ref}")

    if front.get("size") == "G":
        warnings.append("story G: no limite de uma sessão; confirme que não dá para dividir")
    if "a definir" in criteria.lower():
        warnings.append("critério de aceite 'a definir': a implementação vai parar nele")

    status_path = project / STATUS_FILE
    if status_path.is_file():
        try:
            kind, node, _ = find(load(status_path), story_id)
            if kind == "story":
                if node.get("status") != front.get("status"):
                    warnings.append(f"status no frontmatter ({front.get('status')}) diferente do sprint-status "
                                    f"({node.get('status')}); vale o sprint-status")
                if sorted(node.get("repositories") or []) != sorted(repos):
                    warnings.append("repositories diferente do sprint-status")
        except SddError as exc:
            warnings.append(str(exc))
    else:
        warnings.append("projeto sem sprint-status.yaml")

    return {
        "id": story_id,
        "file": str(path),
        "valid": not problems,
        "problems": problems,
        "warnings": warnings,
        "criteria": ca_ids,
        "tasks": {"total": len(boxes), "done": sum(1 for b in boxes if b.lower() == "x")},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, required=True, help="pasta do projeto (docs/{projeto})")
    sub = parser.add_subparsers(dest="command", required=True)
    chk = sub.add_parser("check")
    chk.add_argument("id")
    args = parser.parse_args()
    try:
        emit(check(args.project.resolve(), args.id))
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
