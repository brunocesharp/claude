"""Testes do epics.py. Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

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

EPIC_1 = {"id": "epic-1", "title": "Cadastro de produtos", "escopo": "gestao-de-produtos", "stories": [
    {"id": "1-1-criar-produto", "title": "Criar produto", "size": "M", "kind": "story",
     "repositories": ["loja-api", "loja-web"], "covers": ["1.1", "1.2", "RN-1.1", "RN-1.2"], "checkpoint": True},
    {"id": "1-2-listar-produtos", "title": "Listar produtos", "size": "M",
     "repositories": ["loja-api", "loja-web"], "covers": ["1.3"], "depends_on": ["1-1-criar-produto"]},
]}
EPIC_2 = {"id": "epic-2", "title": "Estoque", "escopo": "gestao-de-produtos", "stories": [
    {"id": "2-1-spike-concorrencia", "title": "Spike: concorrência no estoque", "size": "P", "kind": "spike"},
    {"id": "2-2-registrar-entrada", "title": "Registrar entrada", "size": "G", "repositories": ["loja-api"],
     "covers": ["2.1", "RN-2.1"], "depends_on": ["1-1-criar-produto", "2-1-spike-concorrencia"]},
]}


def write_epic(project: Path, name: str, front: dict) -> None:
    folder = project / "implementacao" / "epicos"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text("---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False) + "---\n# x\n",
                               encoding="utf-8")


@pytest.fixture
def project(tmp_path: Path) -> Path:
    folder = tmp_path / "docs" / "loja"
    spec = folder / "especificacao" / "gestao-de-produtos"
    spec.mkdir(parents=True)
    shutil.copy(FIXTURES / "spec-functional.md", spec / "spec-functional.md")
    write_epic(folder, "epic-1-cadastro.md", EPIC_1)
    write_epic(folder, "epic-2-estoque.md", EPIC_2)
    return folder


def epics(project: Path, *args: str):
    result = subprocess.run([sys.executable, str(SCRIPTS / "epics.py"), "--project", str(project), *args],
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


def test_validate_ok(project):
    code, result = epics(project, "validate")
    assert code == 0 and result["valid"], result["problems"]
    assert result["next_epic"] == 3 and result["stories"] == 4
    assert result["warnings"] == []


def test_validate_aponta_problemas(project):
    bad = json.loads(json.dumps(EPIC_2))
    bad["stories"][1]["depends_on"] = ["3-1-futura"]
    bad["stories"][1]["size"] = "GG"
    bad["stories"][0]["covers"] = ["Cenário 1.1"]
    bad["stories"].append({"id": "2-3-sem-cobertura", "title": "x", "size": "P"})
    write_epic(project, "epic-2-estoque.md", bad)
    code, result = epics(project, "validate")
    assert code == 0 and not result["valid"]
    text = "\n".join(result["problems"])
    assert "depends_on 3-1-futura não vem antes" in text
    assert "size deve ser P, M ou G" in text
    assert "covers deve ser uma lista" in text
    assert any("2-3-sem-cobertura: story sem covers" in w for w in result["warnings"])


def test_coverage_completa_ignora_removido(project):
    code, result = epics(project, "coverage", "--escopo", "gestao-de-produtos")
    assert code == 0 and result["complete"], result
    rows = {row["id"]: row for row in result["scenarios"]}
    assert rows["1.1"]["stories"] == ["1-1-criar-produto"]
    assert rows["1.4"]["removed"] is True
    assert result["uncovered_rules"] == []


def test_coverage_aponta_lacunas_e_referencias_erradas(project):
    partial = json.loads(json.dumps(EPIC_1))
    partial["stories"][1]["covers"] = ["1.9", "1.4"]
    write_epic(project, "epic-1-cadastro.md", partial)
    code, result = epics(project, "coverage", "--escopo", "gestao-de-produtos")
    assert code == 0 and result["complete"] is False
    assert result["uncovered_scenarios"] == ["1.3"]
    assert result["unknown_refs"] == ["1.9"]
    assert result["covering_removed"] == ["1.4"]


def test_coverage_sem_spec(project):
    code, message = epics(project, "coverage", "--escopo", "outro")
    assert code == 1 and "não existe" in message


def test_sync_aceita_campos_extras_dos_epicos(project):
    result = subprocess.run([sys.executable, str(SCRIPTS / "status.py"), "--project", str(project), "sync"],
                            capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stdout
    data = yaml.safe_load((project / "implementacao" / "sprint-status.yaml").read_text(encoding="utf-8"))
    assert list(data["epics"]["epic-2"]["stories"]) == ["2-1-spike-concorrencia", "2-2-registrar-entrada"]
    assert data["epics"]["epic-2"]["stories"]["2-1-spike-concorrencia"]["repositories"] == []
