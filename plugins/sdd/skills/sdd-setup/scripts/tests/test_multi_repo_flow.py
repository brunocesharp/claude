"""Fluxo de ponta a ponta com dois repositórios (api provedor, web consumidor), só nos scripts:
épico → sync → story → attach/ready-for-dev → branches feat/{id} → integridade da revisão → retrospectiva.
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_epics import write_epic  # noqa: E402

STORY_ID = "1-1-listar-eventos"

STORY = f"""---
id: {STORY_ID}
epic: epic-1
status: backlog
title: Listar eventos
size: M
kind: story
covers: ["1.1"]
repositories: [loja-api, loja-web]
branch: feat/{STORY_ID}
---

# Story 1.1: Listar eventos

## História

**Como** visitante, **quero** ver os eventos, **para** escolher um.

## Critérios de aceite

- **CA-1** — Lista de eventos. Origem: cenário 1.1.

## Tarefas

- [x] **T1** — Endpoint GET /api/eventos na api (CA-1)
- [x] **T2** — Tela de eventos na web consumindo o endpoint (CA-1)

## Repositórios

| Repositório | Caminho local | Branch | O que muda |
|---|---|---|---|
| loja-api | (teste) | feat/{STORY_ID} | endpoint |
| loja-web | (teste) | feat/{STORY_ID} | tela |

**Ordem:** loja-api antes de loja-web.

### Contratos

| Contrato | Provedor → consumidor | Mudança | Compatível? | Estratégia |
|---|---|---|---|---|
| GET /api/eventos | api → web | novo | sim | — |

## Contexto para o desenvolvimento

## Fora desta story

## Registro do desenvolvimento

## Arquivos alterados

### loja-api (`feat/{STORY_ID}`)
- `A` src/EventosController.cs

### loja-web (`feat/{STORY_ID}`)
- `A` src/eventos.component.ts

## Revisão

## Histórico
"""

MULTI = f"""---
story: {STORY_ID}
branch: feat/{STORY_ID}
situacao: em-homologacao
---
# Mudança em vários repositórios — Story {STORY_ID}

## Checklist

- [x] Branch `feat/{STORY_ID}` criada em todos os repositórios da story
- [x] Provedor mergeado e publicado antes do consumidor, em cada ambiente
- [ ] PRs com link cruzado (cada PR cita os outros e a story)
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def make_repo(root: Path, name: str, new_file: str) -> Path:
    repo = root / name
    (repo / "src").mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@t")
    git(repo, "config", "user.name", "t")
    (repo / "README.md").write_text(name, encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "switch", "-q", "-c", f"feat/{STORY_ID}")
    (repo / "src" / new_file).write_text("x\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", f"feat: {new_file} ({STORY_ID})")
    return repo


def run(script: str, project: Path, *args: str):
    result = subprocess.run([sys.executable, str(SCRIPTS / script), "--project", str(project), *args],
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    assert not text.startswith("error:"), text
    return json.loads(text)


def test_story_em_dois_repositorios_do_plano_a_retrospectiva(tmp_path):
    project = tmp_path / "docs" / "loja"
    spec = project / "especificacao" / "eventos"
    spec.mkdir(parents=True)
    (spec / "spec-functional.md").write_text("#### Cenário 1.1: Listar eventos\n\nEntão vejo os eventos\n", encoding="utf-8")
    write_epic(project, "epic-1-eventos.md", {"id": "epic-1", "title": "Eventos", "escopo": "eventos", "stories": [
        {"id": STORY_ID, "title": "Listar eventos", "size": "M", "repositories": ["loja-api", "loja-web"],
         "covers": ["1.1"], "checkpoint": True}]})

    assert run("epics.py", project, "validate")["valid"]
    assert run("epics.py", project, "coverage", "--escopo", "eventos")["complete"]
    assert run("status.py", project, "sync")["added_stories"] == [STORY_ID]

    stories = project / "implementacao" / "stories"
    stories.mkdir()
    (stories / f"{STORY_ID}.md").write_text(STORY, encoding="utf-8")
    check = run("story.py", project, "check", STORY_ID)
    assert check["valid"], check["problems"]
    run("status.py", project, "attach", STORY_ID, f"stories/{STORY_ID}.md")
    for state in ("ready-for-dev", "in-progress", "review"):
        run("status.py", project, "set", STORY_ID, state)

    api = make_repo(tmp_path, "loja-api", "EventosController.cs")
    web = make_repo(tmp_path, "loja-web", "eventos.component.ts")
    repos = ["--repo", f"loja-api={api}", "--repo", f"loja-web={web}"]
    integrity = run("review.py", project, "integrity", STORY_ID, *repos)
    assert integrity["consistent"], integrity
    assert [r["branch"] for r in integrity["repos"]] == [f"feat/{STORY_ID}"] * 2

    run("status.py", project, "set", STORY_ID, "done")
    multi = project / "implementacao" / "multi-repo"
    multi.mkdir()
    (multi / f"{STORY_ID}.md").write_text(MULTI, encoding="utf-8")

    evidence = run("retro.py", project, "evidence", "epic-1", *repos)
    story = evidence["stories"][0]
    assert evidence["all_finished"] is True
    assert story["commits"] == {"loja-api": 1, "loja-web": 1}
    assert story["multi_repo"] == {
        "file": f"multi-repo/{STORY_ID}.md", "situacao": "em-homologacao",
        "checklist_open": ["PRs com link cruzado (cada PR cita os outros e a story)"], "checklist_done": 2}

    board = yaml.safe_load((project / "implementacao" / "sprint-status.yaml").read_text(encoding="utf-8"))
    assert board["epics"]["epic-1"]["stories"][STORY_ID]["repositories"] == ["loja-api", "loja-web"]
