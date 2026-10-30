#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Visão do workspace: projetos, fase, situação, repositórios e quadro do sprint. Imprime JSON.

Uso:
  uv run _sdd/scripts/workspace.py [--workspace-root <pasta>] [--project <slug>]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from sddlib import SddError, emit, fail, find_workspace_root, resolve_config
from status import STATUS_FILE, load, next_action, summary, validate

CHECKBOX = re.compile(r"^\s*-\s*\[( |x|X)\]\s*(.+?)\s*$")


def phases(project_md: Path) -> dict[str, object]:
    """Lê a seção 'Status das Fases' do project.md: fases concluídas e a atual (primeira em aberto)."""
    if not project_md.is_file():
        return {"done": [], "current": None}
    done, pending, inside = [], [], False
    for line in project_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = "status das fases" in line.lower()
            continue
        match = CHECKBOX.match(line) if inside else None
        if match:
            (pending if match.group(1) == " " else done).append(match.group(2))
    return {"done": done, "current": pending[0] if pending else None}


def workspace_rows(workspace_md: Path) -> dict[str, dict[str, str]]:
    """Linhas da tabela de projetos do workspace.md, indexadas pelo slug da coluna Pasta."""
    if not workspace_md.is_file():
        return {}
    rows: dict[str, dict[str, str]] = {}
    header: list[str] | None = None
    for line in workspace_md.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            header = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = [cell.lower() for cell in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        row = dict(zip(header, cells))
        slug = re.search(r"/([^/`]+)/?`?\s*$", row.get("pasta", ""))
        if slug:
            rows[slug.group(1)] = row
    return rows


def project_info(root: Path, docs: Path, slug: str, rows: dict[str, dict[str, str]]) -> dict[str, object]:
    folder = docs / slug
    config_path = folder / "project-config.json"
    config: dict = {}
    if config_path.is_file():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            config = {}
    info: dict[str, object] = {
        "slug": slug,
        "name": config.get("name", slug),
        "folder": str(folder.relative_to(root)).replace("\\", "/"),
        "has_config": config_path.is_file(),
        "repositories": "varios" if (folder / "repositorios.md").is_file() else config.get("repositories", "um"),
        "phases": phases(folder / "project.md"),
        "situacao": rows.get(slug, {}).get("situação") or rows.get(slug, {}).get("situacao"),
        "sprint": None,
    }
    status_file = folder / STATUS_FILE
    if status_file.is_file():
        try:
            data = load(status_file)
            errors = validate(data)
            if errors:
                info["sprint"] = {"valid": False, "problems": errors}
            else:
                board = summary(data)
                info["sprint"] = {
                    "valid": True,
                    "epics": [{k: e[k] for k in ("id", "title", "status", "done", "total", "counts")} for e in board["epics"]],
                    "next": next_action(data),
                }
        except SddError as exc:
            info["sprint"] = {"valid": False, "problems": [str(exc)]}
    return info


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace-root", type=Path)
    parser.add_argument("--project", help="slug de um projeto")
    args = parser.parse_args()

    root = (args.workspace_root or find_workspace_root(Path.cwd()) or Path.cwd()).resolve()
    try:
        config = resolve_config(root) if (root / "_sdd").is_dir() else {}
    except SddError as exc:
        fail(str(exc))
    docs = root / str(config.get("paths.docs_root", "docs"))
    rows = workspace_rows(docs / "workspace.md")
    slugs = sorted({p.parent.name for p in docs.glob("*/project.md")} | {p.parent.name for p in docs.glob("*/project-config.json")})
    if args.project:
        if args.project not in slugs:
            fail(f"projeto {args.project} não encontrado em {docs}")
        slugs = [args.project]
    emit({
        "workspace_root": str(root),
        "docs_root": str(docs.relative_to(root)).replace("\\", "/"),
        "has_workspace_md": (docs / "workspace.md").is_file(),
        "projects": [project_info(root, docs, slug, rows) for slug in slugs],
    })


if __name__ == "__main__":
    main()
