"""Testes do story.py, epics.py spec e status.py attach.
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

STORY = """---
id: 1-2-listar-produtos
epic: epic-1
status: backlog
title: Listar produtos
size: M
kind: story
covers: ["1.3"]
repositories: [loja-api, loja-web]
branch: feat/1-2-listar-produtos
depends_on: [1-1-criar-produto]
---

# Story 1.2: [TASK] Desenvolver - [PRODUTO] - Listar produtos

## História

**Como** gestor, **quero** ver a lista de produtos, **para** encontrar o que preciso.

## Critérios de aceite

- **CA-1** — Lista paginada de 20 em 20. Origem: cenário 1.3.

## Tarefas

- [ ] **T1** — Query paginada na API (CA-1)
- [x] **T2** — Testes da query e da tela (CA-1)

## Repositórios

| Repositório | Caminho local | Branch | O que muda |
|---|---|---|---|
| loja-api | a definir | feat/1-2-listar-produtos | endpoint |

## Contexto para o desenvolvimento

### Referências

- `docs/loja/especificacao/gestao-de-produtos/spec-functional.md#feature-1` — feature

## Fora desta story

- Filtros.

## Registro do desenvolvimento

## Arquivos alterados

## Revisão

## Histórico
"""


def run(script: str, project: Path, *args: str):
    result = subprocess.run([sys.executable, str(SCRIPTS / script), "--project", str(project), *args],
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


@pytest.fixture
def project(tmp_path: Path) -> Path:
    folder = tmp_path / "docs" / "loja"
    spec = folder / "especificacao" / "gestao-de-produtos"
    spec.mkdir(parents=True)
    shutil.copy(FIXTURES / "spec-functional.md", spec / "spec-functional.md")
    impl = folder / "implementacao"
    (impl / "stories").mkdir(parents=True)
    shutil.copy(FIXTURES / "sprint-status.yaml", impl / "sprint-status.yaml")
    data = yaml.safe_load((impl / "sprint-status.yaml").read_text(encoding="utf-8"))
    data["epics"]["epic-1"]["stories"]["1-2-listar-produtos"]["status"] = "backlog"
    del data["epics"]["epic-1"]["stories"]["1-2-listar-produtos"]["file"]
    (impl / "sprint-status.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    (impl / "stories" / "1-2-listar-produtos.md").write_text(STORY, encoding="utf-8")
    return folder


def test_story_valida(project):
    code, result = run("story.py", project, "check", "1-2-listar-produtos")
    assert code == 0 and result["valid"], result["problems"]
    assert result["criteria"] == ["CA-1"]
    assert result["tasks"] == {"total": 2, "done": 1}


def test_story_com_problemas(project):
    path = project / "implementacao" / "stories" / "1-2-listar-produtos.md"
    text = STORY.replace('covers: ["1.3"]', 'covers: ["1.3", "RN-1.1"]')
    text = text.replace("(CA-1)\n- [x]", "\n- [x]").replace("Testes da query e da tela (CA-1)", "Testes (CA-2)")
    text = text.replace("## Fora desta story\n\n- Filtros.\n\n", "")
    text = text.replace("spec-functional.md#feature-1", "nao-existe.md")
    path.write_text(text, encoding="utf-8")
    code, result = run("story.py", project, "check", "1-2-listar-produtos")
    assert code == 0 and not result["valid"]
    joined = "\n".join(result["problems"])
    assert "CA-1 não tem tarefa" in joined
    assert "tarefa cita CA-2" in joined
    assert "covers RN-1.1 não aparece" in joined
    assert "falta a seção '## Fora desta story'" in joined
    assert "referência inexistente: docs/loja/especificacao/gestao-de-produtos/nao-existe.md" in joined


def test_extract_copia_texto_literal(project):
    code, result = run("epics.py", project, "spec", "--escopo", "gestao-de-produtos", "1.2", "RN-1.1", "9.9")
    assert code == 0
    blocks = {b["id"]: b["text"] for b in result["blocks"]}
    assert blocks["1.2"].startswith("#### Cenário 1.2: Recusar produto com nome repetido")
    assert 'Então vejo "Já existe um produto com esse nome"' in blocks["1.2"]
    assert "Cenário 1.3" not in blocks["1.2"]
    assert blocks["RN-1.1"] == "- **RN-1.1** — O nome do produto é obrigatório e único"
    assert result["missing"] == ["9.9"]


def test_attach_e_ready_for_dev(project):
    code, message = run("status.py", project, "set", "1-2-listar-produtos", "ready-for-dev")
    assert code == 1 and "file" in message
    code, result = run("status.py", project, "attach", "1-2-listar-produtos", "stories/1-2-listar-produtos.md")
    assert code == 0 and result["changed"]
    code, result = run("status.py", project, "set", "1-2-listar-produtos", "ready-for-dev")
    assert code == 0 and result["story_file"] == "updated"
    code, result = run("story.py", project, "check", "1-2-listar-produtos")
    assert result["valid"] and not any("diferente do sprint-status" in w for w in result["warnings"])


def test_attach_recusa_arquivo_inexistente_e_story_em_andamento(project):
    code, message = run("status.py", project, "attach", "1-2-listar-produtos", "stories/x.md")
    assert code == 1 and "não existe" in message
    code, message = run("status.py", project, "attach", "1-1-criar-produto", "stories/1-2-listar-produtos.md")
    assert code == 1 and "não pode mais ser trocado" in message
