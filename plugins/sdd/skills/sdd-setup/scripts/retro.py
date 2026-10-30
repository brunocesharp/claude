#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Inventário de evidências para a retrospectiva de um épico. Imprime JSON. Só lê.

Uso (a partir da raiz do workspace):
  uv run _sdd/scripts/retro.py --project docs/{projeto} evidence epic-1 [--repo api=D:/repos/api ...] [--base main]

Com --repo (opcional), acrescenta os commits de cada story (branch feat/{id} contra a base).
"""

from __future__ import annotations

import re
import argparse
import subprocess
from pathlib import Path

from sddlib import SddError, emit, fail
from status import FINISHED, STATUS_FILE, find, load, read_epic_files, read_frontmatter
from story import sections

ROUND = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})\s+—\s+revisão\s+(\S+)\s+—\s+rodada\s+(\d+)", re.MULTILINE)
RESULT = re.compile(r"\*\*Resultado:\*\*\s*([^\n]+)")
FINDING = re.compile(r"^\|\s*A\d+\s*\|\s*(high|medium|low|—|-)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|\s*$", re.MULTILINE)
R_TASK = re.compile(r"^\s*-\s*\[( |x|X)\]\s*\*\*R\d+\*\*", re.MULTILINE)
ACTION_ITEM = re.compile(r"^\s*-\s*\[( |x|X)\]\s*(.+)$", re.MULTILINE)


def multi_repo_evidence(project: Path, story_id: str) -> dict | None:
    """Registro da mudança coordenada da story (skill multi-repo), se existir."""
    path = project / "implementacao" / "multi-repo" / f"{story_id}.md"
    if not path.is_file():
        return None
    boxes = ACTION_ITEM.findall(sections(path.read_text(encoding="utf-8")).get("Checklist", ""))
    return {"file": f"multi-repo/{story_id}.md", "situacao": read_frontmatter(path).get("situacao"),
            "checklist_open": [text.strip() for box, text in boxes if box == " "],
            "checklist_done": sum(1 for box, _ in boxes if box.lower() == "x")}


def story_evidence(project: Path, story_id: str, node: dict) -> dict:
    row: dict = {"id": story_id, "title": node.get("title"), "status": node["status"], "file": node.get("file")}
    coordinated = multi_repo_evidence(project, story_id)
    if coordinated:
        row["multi_repo"] = coordinated
    if not node.get("file"):
        return row
    path = project / "implementacao" / node["file"]
    if not path.is_file():
        row["missing_file"] = True
        return row
    text = path.read_text(encoding="utf-8")
    body = sections(text)
    review = body.get("Revisão", "")
    rounds = ROUND.findall(review)
    severities = {"high": 0, "medium": 0, "low": 0}
    routes = {"corrigir": 0, "adiar": 0, "decisão": 0}
    for severity, route in FINDING.findall(review):
        if severity in severities:
            severities[severity] += 1
        for key in routes:
            if route.lower().startswith(key):
                routes[key] += 1
    r_tasks = R_TASK.findall(body.get("Tarefas", ""))
    registro = body.get("Registro do desenvolvimento", "")
    desvios = re.findall(r"\*\*Desvios:\*\*\s*(.+)", registro)
    pendencias = re.findall(r"\*\*Pendências:\*\*\s*(.+)", registro)
    row.update({
        "review_rounds": len(rounds),
        "review_results": RESULT.findall(review),
        "findings": severities,
        "routes": routes,
        "fix_tasks": {"total": len(r_tasks), "open": sum(1 for b in r_tasks if b == " ")},
        "desvios": [d.strip() for d in desvios if d.strip().lower() not in ("nenhum", "nenhum.")],
        "pendencias": [p.strip() for p in pendencias if p.strip().lower() not in ("nenhuma", "nenhuma.")],
        "decisoes_no_registro": registro.count("**Decisões:**"),
        "checkpoint": bool(read_frontmatter(path).get("checkpoint")),
    })
    return row


def previous_retro(project: Path, epic_number: int) -> dict | None:
    folder = project / "implementacao" / "retrospectivas"
    candidates = []
    for path in folder.glob("epic-*.md"):
        match = re.match(r"epic-(\d+)-", path.name)
        if match and int(match.group(1)) < epic_number:
            candidates.append((int(match.group(1)), path.name, path))
    if not candidates:
        return None
    _, name, path = max(candidates)
    items_section = sections(path.read_text(encoding="utf-8")).get("Itens de ação", "")
    items = [{"done": box.lower() == "x", "text": text.strip()} for box, text in ACTION_ITEM.findall(items_section)]
    return {"file": f"retrospectivas/{name}", "verdict": read_frontmatter(path).get("verdict"), "action_items": items}


def course_changes(project: Path, epic_id: str, story_ids: list[str]) -> list[dict]:
    found = []
    for path in sorted((project / "implementacao" / "mudancas").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if epic_id in text or any(sid in text for sid in story_ids):
            front = read_frontmatter(path) if text.startswith("---") else {}
            found.append({"file": f"mudancas/{path.name}", "scope": front.get("scope"), "status": front.get("status")})
    return found


def commits(repo: Path, branch: str, base: str) -> int | None:
    result = subprocess.run(["git", "-C", str(repo), "rev-list", "--count", f"{base}..{branch}"],
                            capture_output=True, text=True)
    return int(result.stdout.strip()) if result.returncode == 0 else None


def evidence(project: Path, epic_id: str, repos: dict[str, Path], base: str) -> dict:
    data = load(project / STATUS_FILE)
    kind, epic, _ = find(data, epic_id)
    if kind != "epic":
        raise SddError(f"{epic_id} não é um épico")
    epic_file = next((e for e in read_epic_files(project) if e["id"] == epic_id), None)
    stories = [story_evidence(project, sid, node) for sid, node in (epic.get("stories") or {}).items()]
    if repos:
        for row in stories:
            row["commits"] = {name: commits(path, f"feat/{row['id']}", base) for name, path in repos.items()}
    open_stories = [s["id"] for s in stories if s["status"] not in FINISHED]
    number = int(epic_id.split("-")[1])
    return {
        "epic": epic_id,
        "title": epic.get("title"),
        "status": epic["status"],
        "retrospective": epic.get("retrospective", "optional"),
        "epic_file": epic_file["source"] if epic_file else None,
        "all_finished": not open_stories,
        "open_stories": open_stories,
        "stories": stories,
        "totals": {
            "stories": len(stories),
            "done": sum(1 for s in stories if s["status"] == "done"),
            "dropped": sum(1 for s in stories if s["status"] == "dropped"),
            "review_rounds": sum(s.get("review_rounds", 0) for s in stories),
            "findings_high": sum(s.get("findings", {}).get("high", 0) for s in stories),
            "findings_medium": sum(s.get("findings", {}).get("medium", 0) for s in stories),
            "deferred": sum(s.get("routes", {}).get("adiar", 0) for s in stories),
            "stories_with_desvios": sum(1 for s in stories if s.get("desvios")),
        },
        "previous_retrospective": previous_retro(project, number),
        "course_changes": course_changes(project, epic_id, [s["id"] for s in stories]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    ev = sub.add_parser("evidence")
    ev.add_argument("epic")
    ev.add_argument("--repo", action="append", default=[], help="nome=caminho (opcional, para contar commits)")
    ev.add_argument("--base", default="main")
    args = parser.parse_args()
    try:
        repos = {}
        for value in args.repo:
            name, _, path = value.partition("=")
            if not path:
                raise SddError(f"--repo deve ser nome=caminho: {value}")
            repos[name] = Path(path)
        emit(evidence(args.project.resolve(), args.epic, repos, args.base))
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
