"""Testes do retro.py evidence e do epics.py impact.
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_epics import EPIC_1, EPIC_2, write_epic  # noqa: E402

STORY_1 = """---
id: 1-1-criar-produto
epic: epic-1
status: done
checkpoint: true
---
# Story 1.1

## Tarefas

- [x] **T1** — Criar (CA-1)

### Correções da revisão 1 (2026-10-20)

- [x] **R1** — Página de 20 (CA-1)
- [ ] **R2** — Nome de arquivo

## Registro do desenvolvimento

### 2026-10-19 — modelo
- **Decisões:** usar cursor
- **Desvios:** validação movida para o domínio
- **Testes:** ok
- **Pendências:** nenhuma

## Revisão

### 2026-10-20 — revisão completa — rodada 1

**Resultado:** correções

| # | Sev. | Lente | Onde | Achado | Encaminhamento |
|---|------|-------|------|--------|----------------|
| A1 | high | Aderência | api | x | corrigir → R1 |
| A2 | low | Registro | api | y | corrigir → R2 |
| A3 | medium | Testes | api | z | adiar → story 1-3-x |

### 2026-10-21 — revisão rápida — rodada 2

**Resultado:** aprovada

## Histórico
"""

RETRO_1 = """---
epic: epic-1
verdict: accepted-with-open-items
---
# Retrospectiva

## Itens de ação

- [x] Documentar padrão de paginação
- [ ] Criar fixture de produtos
"""


def run(script: str, project: Path, *args: str):
    result = subprocess.run([sys.executable, str(SCRIPTS / script), "--project", str(project), *args],
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


def set_state(project: Path, story: str, *states: str) -> None:
    for state in states:
        code, out = run("status.py", project, "set", story, state)
        assert code == 0, out


@pytest.fixture
def project(tmp_path: Path) -> Path:
    folder = tmp_path / "docs" / "loja"
    write_epic(folder, "epic-1-cadastro.md", EPIC_1)
    write_epic(folder, "epic-2-estoque.md", EPIC_2)
    assert run("status.py", folder, "sync")[0] == 0
    stories = folder / "implementacao" / "stories"
    stories.mkdir(parents=True)
    (stories / "1-1-criar-produto.md").write_text(STORY_1, encoding="utf-8")
    (stories / "1-2-listar-produtos.md").write_text("---\nid: 1-2-listar-produtos\nstatus: backlog\n---\n# 1.2\n",
                                                    encoding="utf-8")
    run("status.py", folder, "attach", "1-1-criar-produto", "stories/1-1-criar-produto.md")
    run("status.py", folder, "attach", "1-2-listar-produtos", "stories/1-2-listar-produtos.md")
    set_state(folder, "1-1-criar-produto", "ready-for-dev", "in-progress", "review", "done")
    set_state(folder, "1-2-listar-produtos", "ready-for-dev", "in-progress")
    return folder


def test_evidence_inventaria_o_epico(project):
    code, ev = run("retro.py", project, "evidence", "epic-1")
    assert code == 0, ev
    assert ev["all_finished"] is False and ev["open_stories"] == ["1-2-listar-produtos"]
    s1 = next(s for s in ev["stories"] if s["id"] == "1-1-criar-produto")
    assert s1["review_rounds"] == 2
    assert s1["review_results"] == ["correções", "aprovada"]
    assert s1["findings"] == {"high": 1, "medium": 1, "low": 1}
    assert s1["routes"] == {"corrigir": 2, "adiar": 1, "decisão": 0}
    assert s1["fix_tasks"] == {"total": 2, "open": 1}
    assert s1["desvios"] == ["validação movida para o domínio"] and s1["pendencias"] == []
    assert s1["checkpoint"] is True
    assert ev["totals"]["findings_high"] == 1 and ev["totals"]["deferred"] == 1
    assert ev["previous_retrospective"] is None


def test_evidence_le_retro_anterior_e_mudancas(project):
    retros = project / "implementacao" / "retrospectivas"
    retros.mkdir()
    (retros / "epic-1-2026-10-25.md").write_text(RETRO_1, encoding="utf-8")
    changes = project / "implementacao" / "mudancas"
    changes.mkdir()
    (changes / "2026-10-26-estoque.md").write_text("---\nscope: moderado\nstatus: aplicada\n---\nAfeta 2-2-registrar-entrada\n",
                                                   encoding="utf-8")
    code, ev = run("retro.py", project, "evidence", "epic-2")
    assert code == 0, ev
    prev = ev["previous_retrospective"]
    assert prev["file"] == "retrospectivas/epic-1-2026-10-25.md"
    assert prev["verdict"] == "accepted-with-open-items"
    assert prev["action_items"] == [{"done": True, "text": "Documentar padrão de paginação"},
                                    {"done": False, "text": "Criar fixture de produtos"}]
    assert ev["course_changes"] == [{"file": "mudancas/2026-10-26-estoque.md", "scope": "moderado", "status": "aplicada"}]


def test_evidence_recusa_story(project):
    code, message = run("retro.py", project, "evidence", "1-1-criar-produto")
    assert code == 1 and "não é um épico" in message


def test_impact_agrupa_por_estado(project):
    code, result = run("epics.py", project, "impact", "1.1", "1.3", "2.1", "9.9")
    assert code == 0, result
    assert result["by_status"] == {"done": ["1-1-criar-produto"], "in-progress": ["1-2-listar-produtos"],
                                   "backlog": ["2-2-registrar-entrada"]}
    assert result["not_covered"] == ["9.9"]
    code, result = run("epics.py", project, "impact", "--escopo", "outro", "1.1")
    assert result["affected"] == []
