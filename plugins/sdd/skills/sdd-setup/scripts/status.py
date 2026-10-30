#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Lê, valida e atualiza o sprint-status.yaml de um projeto. Imprime JSON; em erro, 'error: <msg>' e código 1.

Uso (a partir da raiz do workspace):
  uv run _sdd/scripts/status.py --project docs/{projeto} show
  uv run _sdd/scripts/status.py --project docs/{projeto} next
  uv run _sdd/scripts/status.py --project docs/{projeto} set 1-2-cadastro in-progress [--force]
  uv run _sdd/scripts/status.py --project docs/{projeto} set epic-1 done
  uv run _sdd/scripts/status.py --project docs/{projeto} set epic-1-retrospective done
  uv run _sdd/scripts/status.py --project docs/{projeto} check
  uv run _sdd/scripts/status.py --project docs/{projeto} attach 1-2-cadastro stories/1-2-cadastro.md
  uv run _sdd/scripts/status.py --project docs/{projeto} sync [--dry-run]

Formato, estados e transições: sdd-setup/references/sprint-status.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

from sddlib import SddError, emit, fail

STATUS_FILE = Path("implementacao") / "sprint-status.yaml"

STORY_STATES = ("backlog", "ready-for-dev", "in-progress", "review", "done", "blocked", "dropped")
EPIC_STATES = ("backlog", "in-progress", "done", "dropped")
RETRO_STATES = ("optional", "done")
FINISHED = ("done", "dropped")

# De → para permitidos sem --force.
STORY_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "backlog": ("ready-for-dev", "blocked", "dropped"),
    "ready-for-dev": ("in-progress", "backlog", "blocked", "dropped"),
    "in-progress": ("review", "ready-for-dev", "backlog", "blocked", "dropped"),
    "review": ("done", "in-progress", "blocked", "dropped"),
    "blocked": ("backlog", "ready-for-dev", "in-progress", "review", "dropped"),
    "dropped": ("backlog",),
    "done": (),
}
EPIC_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "backlog": ("in-progress", "dropped"),
    "in-progress": ("done", "backlog", "dropped"),
    "done": ("in-progress",),
    "dropped": ("backlog",),
}

EPIC_ID = re.compile(r"^epic-(\d+)$")
STORY_ID = re.compile(r"^(\d+)-(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*$")
RETRO_ID = re.compile(r"^(epic-\d+)-retrospective$")

HEADER = (
    "# Estado de entrega do projeto. Fonte única do andamento de épicos e stories.\n"
    "# Formato e transições: sdd-setup/references/sprint-status.md.\n"
    "# Prefira mudar estados com _sdd/scripts/status.py (valida as transições).\n"
)


# ---------------------------------------------------------------- leitura e validação


def status_path(project: Path) -> Path:
    return project / STATUS_FILE


def load(path: Path) -> dict:
    if not path.is_file():
        raise SddError(f"{path} não existe: gere com a skill sprint-planning")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SddError(f"{path} não é um YAML válido: {exc}") from exc
    return data if isinstance(data, dict) else {}


def validate(data: dict) -> list[str]:
    """Erros de estrutura e de coerência. Lista vazia = válido."""
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version deve ser 1")
    if not isinstance(data.get("project"), str) or not data.get("project"):
        errors.append("project deve ser o slug do projeto")
    epics = data.get("epics")
    if epics is None:
        epics = {}
    if not isinstance(epics, dict):
        return errors + ["epics deve ser um mapa epic-N: {...}"]

    seen_stories: set[str] = set()
    for epic_id, epic in epics.items():
        match = EPIC_ID.match(str(epic_id))
        if not match:
            errors.append(f"{epic_id}: id de épico deve ser epic-N")
            continue
        if not isinstance(epic, dict):
            errors.append(f"{epic_id}: deve ser um mapa")
            continue
        number = match.group(1)
        if not epic.get("title"):
            errors.append(f"{epic_id}: falta title")
        if epic.get("status") not in EPIC_STATES:
            errors.append(f"{epic_id}: status {epic.get('status')!r} inválido (use {', '.join(EPIC_STATES)})")
        if epic.get("retrospective", "optional") not in RETRO_STATES:
            errors.append(f"{epic_id}: retrospective deve ser optional ou done")
        stories = epic.get("stories") or {}
        if not isinstance(stories, dict):
            errors.append(f"{epic_id}: stories deve ser um mapa")
            continue
        for story_id, story in stories.items():
            story_match = STORY_ID.match(str(story_id))
            if not story_match:
                errors.append(f"{story_id}: id de story deve ser N-M-slug (kebab-case)")
                continue
            if story_match.group(1) != number:
                errors.append(f"{story_id}: está no {epic_id}, mas o número do épico no id é {story_match.group(1)}")
            if story_id in seen_stories:
                errors.append(f"{story_id}: id repetido")
            seen_stories.add(story_id)
            if not isinstance(story, dict):
                errors.append(f"{story_id}: deve ser um mapa")
                continue
            if story.get("status") not in STORY_STATES:
                errors.append(f"{story_id}: status {story.get('status')!r} inválido (use {', '.join(STORY_STATES)})")
            repos = story.get("repositories", [])
            if not isinstance(repos, list) or not all(isinstance(r, str) for r in repos):
                errors.append(f"{story_id}: repositories deve ser uma lista de nomes")
            if story.get("status") not in ("backlog", "dropped", None) and not story.get("file"):
                errors.append(f"{story_id}: status {story['status']} exige file (o arquivo da story)")

        states = [s.get("status") for s in stories.values() if isinstance(s, dict)]
        if epic.get("status") == "done" and any(state not in FINISHED for state in states):
            errors.append(f"{epic_id}: done com stories ainda abertas")
        if epic.get("status") == "backlog" and any(state not in ("backlog", "dropped") for state in states):
            errors.append(f"{epic_id}: backlog com stories já iniciadas (deveria ser in-progress)")
    return errors


def find(data: dict, item_id: str) -> tuple[str, dict, dict | None]:
    """Devolve (tipo, nó, épico) para epic-N, N-M-slug ou epic-N-retrospective."""
    epics = data.get("epics") or {}
    retro = RETRO_ID.match(item_id)
    if retro:
        epic = epics.get(retro.group(1))
        if epic is None:
            raise SddError(f"{retro.group(1)} não existe")
        return "retrospective", epic, epic
    if item_id in epics:
        return "epic", epics[item_id], None
    for epic in epics.values():
        stories = epic.get("stories") or {}
        if item_id in stories:
            return "story", stories[item_id], epic
    raise SddError(f"{item_id} não existe no sprint-status.yaml")


# ---------------------------------------------------------------- gravação


def save(path: Path, data: dict) -> None:
    data["updated_at"] = date.today().isoformat()
    body = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=None, width=120)
    path.write_text(HEADER + body, encoding="utf-8")


FRONTMATTER_STATUS = re.compile(r"^(status:\s*)(\S+)\s*$", re.MULTILINE)


def story_file(project: Path, story: dict) -> Path | None:
    file = story.get("file")
    return (project / "implementacao" / file) if file else None


def frontmatter_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    match = FRONTMATTER_STATUS.search(text[:end])
    return match.group(2) if match else None


def sync_frontmatter(path: Path, status: str) -> bool:
    """Atualiza 'status:' no frontmatter da story. Devolve True se mudou."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    head, rest = text[:end], text[end:]
    new_head, count = FRONTMATTER_STATUS.subn(lambda m: f"{m.group(1)}{status}", head, count=1)
    if count == 0 or new_head == head:
        return False
    path.write_text(new_head + rest, encoding="utf-8")
    return True


# ---------------------------------------------------------------- comandos


def summary(data: dict) -> dict:
    epics_out = []
    totals = {state: 0 for state in STORY_STATES}
    for epic_id, epic in (data.get("epics") or {}).items():
        counts = {state: 0 for state in STORY_STATES}
        stories = []
        for story_id, story in (epic.get("stories") or {}).items():
            counts[story["status"]] += 1
            totals[story["status"]] += 1
            stories.append({"id": story_id, "title": story.get("title"), "status": story["status"],
                            "repositories": story.get("repositories", []), "file": story.get("file")})
        active = sum(n for state, n in counts.items() if state != "dropped")
        epics_out.append({
            "id": epic_id, "title": epic.get("title"), "escopo": epic.get("escopo"), "status": epic["status"],
            "retrospective": epic.get("retrospective", "optional"),
            "done": counts["done"], "total": active, "counts": counts, "stories": stories,
        })
    return {"project": data.get("project"), "updated_at": str(data.get("updated_at")), "epics": epics_out,
            "totals": totals, "situacao": situacao(epics_out)}


def situacao(epics_out: list[dict]) -> str:
    """Texto para a coluna Situação do workspace.md: o épico em andamento (ou o próximo) e as stories done."""
    open_epics = [e for e in epics_out if e["status"] not in FINISHED]
    if not epics_out:
        return "Plano de Execução"
    if not open_epics:
        return "Desenvolvimento — épicos concluídos"
    current = next((e for e in open_epics if e["status"] == "in-progress"), open_epics[0])
    return f"Desenvolvimento — {current['id']}: {current['done']}/{current['total']} done"


# ---------------------------------------------------------------- sync a partir dos épicos


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SddError(f"{path.name}: falta o frontmatter (--- ... ---) com id, title e stories")
    end = text.find("\n---", 3)
    if end == -1:
        raise SddError(f"{path.name}: frontmatter sem o --- de fechamento")
    try:
        data = yaml.safe_load(text[3:end])
    except yaml.YAMLError as exc:
        raise SddError(f"{path.name}: frontmatter não é YAML válido: {exc}") from exc
    return data if isinstance(data, dict) else {}


def read_epic_files(project: Path) -> list[dict]:
    """Lê implementacao/epicos/epic-*.md, na ordem do número do épico."""
    folder = project / "implementacao" / "epicos"
    epics = []
    for path in folder.glob("epic-*.md"):
        front = read_frontmatter(path)
        epic_id = str(front.get("id", ""))
        match = EPIC_ID.match(epic_id)
        if not match:
            raise SddError(f"{path.name}: id deve ser epic-N")
        if not path.name.startswith(f"{epic_id}-") and path.name != f"{epic_id}.md":
            raise SddError(f"{path.name}: o nome do arquivo deve começar com {epic_id}-")
        stories = front.get("stories") or []
        if not isinstance(stories, list) or not all(isinstance(s, dict) and s.get("id") for s in stories):
            raise SddError(f"{path.name}: stories deve ser uma lista de {{id, title, repositories}}")
        epics.append({**front, "number": int(match.group(1)), "source": f"epicos/{path.name}"})
    numbers = [e["number"] for e in epics]
    if len(numbers) != len(set(numbers)):
        raise SddError("há dois arquivos de épico com o mesmo número")
    return sorted(epics, key=lambda e: e["number"])


def sync(project: Path, data: dict | None, epics_in: list[dict]) -> tuple[dict, dict]:
    """Mescla os épicos no sprint-status. Acrescenta e atualiza títulos, escopo, repositórios e ordem;
    nunca muda status nem file de algo que já existe, e nunca remove (o que sumiu vira 'orphans')."""
    created = data is None
    data = data or {"version": 1, "project": project.name, "updated_at": date.today().isoformat(), "epics": {}}
    data.setdefault("epics", {})
    old_epics = data["epics"] or {}
    report: dict = {"created": created, "added_epics": [], "added_stories": [], "updated": [], "reordered": [],
                    "orphans": []}

    new_epics: dict = {}
    for epic_in in epics_in:
        epic_id = epic_in["id"]
        old = old_epics.get(epic_id)
        if old is None:
            report["added_epics"].append(epic_id)
            epic = {"title": epic_in.get("title"), "escopo": epic_in.get("escopo"), "status": "backlog",
                    "retrospective": "optional", "stories": {}}
        else:
            epic = dict(old)
            for field in ("title", "escopo"):
                if epic_in.get(field) and epic.get(field) != epic_in[field]:
                    report["updated"].append(f"{epic_id}.{field}")
                    epic[field] = epic_in[field]
        old_stories = epic.get("stories") or {}
        stories: dict = {}
        for story_in in epic_in.get("stories") or []:
            story_id = str(story_in["id"])
            repos = story_in.get("repositories") or []
            story = dict(old_stories.get(story_id) or {})
            if not story:
                report["added_stories"].append(story_id)
                story = {"title": story_in.get("title"), "status": "backlog", "repositories": repos}
            else:
                if story_in.get("title") and story.get("title") != story_in["title"]:
                    report["updated"].append(f"{story_id}.title")
                    story["title"] = story_in["title"]
                if "repositories" in story_in and story.get("repositories") != repos:
                    report["updated"].append(f"{story_id}.repositories")
                    story["repositories"] = repos
            stories[story_id] = story
        for story_id, story in old_stories.items():
            if story_id not in stories:
                report["orphans"].append(story_id)
                stories[story_id] = story
        if old is not None and list(old_stories) != [s for s in stories if s in old_stories]:
            report["reordered"].append(epic_id)
        epic["stories"] = stories
        new_epics[epic_id] = epic
    for epic_id, epic in old_epics.items():
        if epic_id not in new_epics:
            report["orphans"].append(epic_id)
            new_epics[epic_id] = epic
    data["epics"] = new_epics
    return data, report


def next_action(data: dict) -> dict:
    """Próxima ação, na ordem: retomar in-progress, revisar review, implementar ready-for-dev,
    fechar épico com tudo finalizado (retrospectiva opcional), criar a story do próximo backlog, desbloquear."""
    epics = data.get("epics") or {}
    order = [(epic_id, epic, story_id, story) for epic_id, epic in epics.items() if epic["status"] != "dropped"
             for story_id, story in (epic.get("stories") or {}).items()]

    def first(state: str, skill: str, why: str) -> dict | None:
        for epic_id, _epic, story_id, story in order:
            if story["status"] == state:
                return {"action": skill, "id": story_id, "epic": epic_id, "reason": why}
        return None

    for state, skill, why in (("in-progress", "dev-story", "retomar a implementação"),
                              ("review", "story-review", "revisar a implementação"),
                              ("ready-for-dev", "dev-story", "implementar em uma sessão nova")):
        found = first(state, skill, why)
        if found:
            return found
    closing = close_epic_action(epics)
    if closing:
        return closing
    found = first("backlog", "create-story", "gerar o arquivo da story")
    if found:
        return found
    blocked = [sid for _e, _ep, sid, s in order if s["status"] == "blocked"]
    if blocked:
        return {"action": "unblock", "id": blocked[0], "blocked": blocked, "reason": "só restam stories bloqueadas"}
    return {"action": None, "reason": "nada pendente: planeje novos épicos (plan-epics)"}


def close_epic_action(epics: dict) -> dict | None:
    for epic_id, epic in epics.items():
        stories = (epic.get("stories") or {}).values()
        if epic["status"] not in FINISHED and stories and all(s["status"] in FINISHED for s in stories):
            if epic.get("retrospective", "optional") != "done":
                return {"action": "retrospective", "id": epic_id, "epic": epic_id,
                        "reason": "todas as stories finalizadas: retrospectiva (opcional) e fechar o épico"}
            return {"action": "close-epic", "id": epic_id, "epic": epic_id,
                    "reason": "retrospectiva feita: confirmar o épico como done"}
    return None


def set_state(project: Path, data: dict, item_id: str, new: str, force: bool) -> dict:
    kind, node, epic = find(data, item_id)
    if kind == "retrospective":
        if new not in RETRO_STATES:
            raise SddError(f"retrospectiva aceita {', '.join(RETRO_STATES)}")
        old = node.get("retrospective", "optional")
        node["retrospective"] = new
        return {"id": item_id, "kind": kind, "from": old, "to": new}

    states, transitions = (STORY_STATES, STORY_TRANSITIONS) if kind == "story" else (EPIC_STATES, EPIC_TRANSITIONS)
    if new not in states:
        raise SddError(f"estado {new!r} inválido para {kind} (use {', '.join(states)})")
    old = node["status"]
    if old == new:
        return {"id": item_id, "kind": kind, "from": old, "to": new, "changed": False}
    if new not in transitions[old] and not force:
        allowed = ", ".join(transitions[old]) or "nenhum (estado final; use correct-course para criar uma story de ajuste)"
        raise SddError(f"{item_id}: transição {old} → {new} não permitida. A partir de {old}: {allowed}")

    if kind == "epic" and new == "done":
        open_stories = [sid for sid, s in (node.get("stories") or {}).items() if s["status"] not in FINISHED]
        if open_stories:
            raise SddError(f"{item_id}: não pode ir para done com stories abertas: {', '.join(open_stories)}")
    if kind == "story" and new not in ("backlog", "dropped") and not node.get("file"):
        raise SddError(f"{item_id}: defina file (arquivo da story) antes de mover para {new}")

    node["status"] = new
    result: dict = {"id": item_id, "kind": kind, "from": old, "to": new, "changed": True, "forced": force and new not in transitions[old]}

    if kind == "story":
        if epic["status"] == "backlog" and new not in ("backlog", "dropped"):
            epic["status"] = "in-progress"
            result["epic_status"] = "in-progress"
    return result


def attach(project: Path, data: dict, story_id: str, file: str) -> dict:
    """Liga o arquivo da story (relativo a implementacao/) à story. Só antes da implementação começar."""
    kind, story, _ = find(data, story_id)
    if kind != "story":
        raise SddError(f"{story_id} não é uma story")
    if story["status"] not in ("backlog", "ready-for-dev", "blocked"):
        raise SddError(f"{story_id} está em {story['status']}: o arquivo não pode mais ser trocado")
    file = file.replace("\\", "/")
    if not (project / "implementacao" / file).is_file():
        raise SddError(f"implementacao/{file} não existe")
    old = story.get("file")
    story["file"] = file
    return {"id": story_id, "file": file, "previous": old, "changed": old != file}


def sync_story_file(project: Path, data: dict, result: dict) -> None:
    """Depois de salvar o sprint-status: leva o novo estado ao frontmatter do arquivo da story."""
    if result["kind"] != "story":
        return
    _, story, _ = find(data, result["id"])
    path = story_file(project, story)
    if path is None:
        return
    if not path.is_file():
        result["story_file"] = "missing"
    else:
        result["story_file"] = "updated" if sync_frontmatter(path, result["to"]) else "unchanged"


def check(project: Path, data: dict) -> dict:
    problems = validate(data)
    warnings = []
    for epic in (data.get("epics") or {}).values():
        for story_id, story in (epic.get("stories") or {}).items():
            path = story_file(project, story)
            if not path:
                continue
            if not path.is_file():
                if story["status"] not in ("backlog", "dropped"):
                    problems.append(f"{story_id}: arquivo {story['file']} não existe")
                continue
            front = frontmatter_status(path)
            if front is None:
                warnings.append(f"{story_id}: {story['file']} sem 'status:' no frontmatter")
            elif front != story["status"]:
                problems.append(f"{story_id}: frontmatter diz {front}, sprint-status diz {story['status']} "
                                f"(vale o sprint-status; rode set para sincronizar)")
    return {"valid": not problems, "problems": problems, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, required=True, help="pasta do projeto (docs/{projeto})")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("show")
    sub.add_parser("next")
    sub.add_parser("check")
    syncp = sub.add_parser("sync", help="mescla implementacao/epicos/*.md no sprint-status.yaml")
    syncp.add_argument("--dry-run", action="store_true", help="mostra o que mudaria sem gravar")
    attp = sub.add_parser("attach", help="liga o arquivo da story (relativo a implementacao/)")
    attp.add_argument("id")
    attp.add_argument("file")
    setp = sub.add_parser("set")
    setp.add_argument("id")
    setp.add_argument("state")
    setp.add_argument("--force", action="store_true", help="aceita transição fora da tabela (só a pedido do usuário)")
    args = parser.parse_args()

    project = args.project.resolve()
    path = status_path(project)
    try:
        if args.command == "sync":
            epics_in = read_epic_files(project)
            if not epics_in:
                raise SddError("nenhum épico em implementacao/epicos/: gere com a skill plan-epics")
            existing = load(path) if path.is_file() else None
            if existing is not None:
                errors = validate(existing)
                if errors:
                    raise SddError("sprint-status.yaml inválido; corrija antes do sync:\n- " + "\n- ".join(errors))
            data, report = sync(project, existing, epics_in)
            errors = validate(data)
            if errors:
                raise SddError("o resultado do sync ficaria inválido:\n- " + "\n- ".join(errors))
            changed = any(report[k] for k in ("created", "added_epics", "added_stories", "updated", "reordered"))
            if changed and not args.dry_run:
                path.parent.mkdir(parents=True, exist_ok=True)
                save(path, data)
            emit({**report, "changed": changed, "dry_run": args.dry_run, "board": summary(data)})
            return
        data = load(path)
        if args.command == "check":
            emit(check(project, data))
            return
        errors = validate(data)
        if errors:
            raise SddError("sprint-status.yaml inválido:\n- " + "\n- ".join(errors))
        if args.command == "attach":
            result = attach(project, data, args.id, args.file)
            if result["changed"]:
                save(path, data)
            emit(result)
        elif args.command == "show":
            emit(summary(data))
        elif args.command == "next":
            emit(next_action(data))
        else:
            result = set_state(project, data, args.id, args.state, args.force)
            errors = validate(data)
            if errors:
                raise SddError("a mudança deixaria o arquivo inválido:\n- " + "\n- ".join(errors))
            if result.get("changed", True):
                save(path, data)
            sync_story_file(project, data, result)
            emit(result)
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
