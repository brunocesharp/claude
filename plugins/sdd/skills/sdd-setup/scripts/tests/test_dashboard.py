"""Testes do dashboard.py.

Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests/test_dashboard.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

SCRIPT = Path(__file__).parents[1] / "dashboard.py"


def run(root: Path, *args: str) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--workspace-root", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = result.stdout if result.returncode == 0 else result.stderr or result.stdout
    return result.returncode, json.loads(output) if result.returncode == 0 else {"error": output.strip()}


def make_workspace(root: Path) -> Path:
    (root / "_sdd").mkdir()
    (root / "_sdd" / "config.toml").write_text('paths.docs_root = "docs"\n', encoding="utf-8")
    project = root / "docs" / "loja"
    (project / "implementacao").mkdir(parents=True)
    (project / "project-config.json").write_text(json.dumps({"name": "Loja", "repositories": "um"}), encoding="utf-8")
    (project / "project.md").write_text("# Loja\n\n## Status das Fases\n- [x] Discovery\n- [ ] Desenvolvimento\n", encoding="utf-8")
    board = {
        "version": 1,
        "project": "loja",
        "updated_at": "2026-11-05",
        "epics": {
            "epic-1": {
                "title": "Comprar produtos",
                "escopo": "compras",
                "status": "in-progress",
                "retrospective": "optional",
                "stories": {
                    "1-1-carrinho": {"title": "Adicionar ao carrinho", "status": "done", "repositories": ["web"], "file": "stories/1-1-carrinho.md"},
                    "1-2-pagamento": {"title": "Pagar pedido", "status": "review", "repositories": ["api", "web"], "file": "stories/1-2-pagamento.md"},
                    "1-3-cupom": {"title": "Aplicar cupom", "status": "blocked", "repositories": ["api"], "file": "stories/1-3-cupom.md"},
                },
            }
        },
    }
    (project / "implementacao" / "sprint-status.yaml").write_text(yaml.safe_dump(board, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return project


def test_show_consolida_portfolio_e_fila_de_atencao(tmp_path: Path):
    make_workspace(tmp_path)
    code, data = run(tmp_path, "show")
    assert code == 0
    assert data["workspace"] == tmp_path.name
    assert data["totals"]["done"] == 1
    assert data["totals"]["review"] == 1
    assert data["totals"]["blocked"] == 1
    assert data["projects"][0]["next"]["action"] == "story-review"
    assert {(item["kind"], item.get("story")) for item in data["attention"]} == {
        ("review", "1-2-pagamento"),
        ("blocked", "1-3-cupom"),
    }


def test_build_grava_json_e_html_autocontido(tmp_path: Path):
    make_workspace(tmp_path)
    code, result = run(tmp_path, "build")
    assert code == 0
    html_path = Path(result["html"])
    json_path = Path(result["json"])
    assert html_path == tmp_path / "_sdd" / "dashboard" / "index.html"
    assert html_path.is_file() and json_path.is_file()
    content = html_path.read_text(encoding="utf-8")
    assert "SDD Dashboard" in content
    assert "Adicionar ao carrinho" in content
    assert "__DATA__" not in content
    assert json.loads(json_path.read_text(encoding="utf-8"))["projects"][0]["slug"] == "loja"


def test_automacao_com_falha_entra_na_fila_de_atencao(tmp_path: Path):
    make_workspace(tmp_path)
    state = tmp_path / "_sdd" / "execucao-recorrente"
    state.mkdir()
    state.joinpath("estado.json").write_text(json.dumps({"stories": {"loja/1-3-cupom": {
        "acao": "dev-story", "ultimo_resultado": "falhou", "tentativas": 2,
        "ultima_execucao": "2026-11-05T10:00:00-03:00", "motivo": "testes falharam"
    }}}), encoding="utf-8")
    code, data = run(tmp_path, "show")
    assert code == 0
    assert data["automations"][1]["records"][0]["attempts"] == 2
    assert any(item["kind"] == "automation" and item["story"] == "1-3-cupom" for item in data["attention"])


def test_project_limita_o_snapshot(tmp_path: Path):
    make_workspace(tmp_path)
    other = tmp_path / "docs" / "site"
    other.mkdir()
    (other / "project.md").write_text("# Site\n", encoding="utf-8")
    code, data = run(tmp_path, "--project", "loja", "show")
    assert code == 0
    assert [project["slug"] for project in data["projects"]] == ["loja"]


def test_project_inexistente_falha_sem_gravar(tmp_path: Path):
    make_workspace(tmp_path)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--workspace-root", str(tmp_path), "--project", "x", "show"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 1
    assert "projeto x não encontrado" in result.stdout
    assert not (tmp_path / "_sdd" / "dashboard").exists()
