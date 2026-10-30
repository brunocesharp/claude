"""Testes do review.py com um repositório Git temporário.
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent

STORY = """---
id: 1-2-listar
epic: epic-1
status: review
---
# Story

## Arquivos alterados

### loja-api (`feat/1-2-listar`)
- `A` src/Listar.cs
- `M` src/Controller.cs
- `A` src/Fantasma.cs

## Revisão
"""


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def setup(tmp_path: Path):
    repo = tmp_path / "loja-api"
    (repo / "src").mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@t")
    git(repo, "config", "user.name", "t")
    (repo / "src" / "Controller.cs").write_text("class C {}\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "switch", "-q", "-c", "feat/1-2-listar")
    (repo / "src" / "Listar.cs").write_text("class L {}\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "listar")
    (repo / "src" / "Controller.cs").write_text("class C { int x; }\n", encoding="utf-8")  # não commitado
    (repo / "src" / "Extra.cs").write_text("class E {}\n", encoding="utf-8")  # não rastreado e não declarado
    project = tmp_path / "docs" / "loja"
    (project / "implementacao" / "stories").mkdir(parents=True)
    (project / "implementacao" / "stories" / "1-2-listar.md").write_text(STORY, encoding="utf-8")
    return project, repo


def run(project: Path, *args: str):
    result = subprocess.run([sys.executable, str(SCRIPTS / "review.py"), "--project", str(project), *args],
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


def test_integrity_compara_declarado_e_real(setup):
    project, repo = setup
    code, result = run(project, "integrity", "1-2-listar", "--repo", f"loja-api={repo}")
    assert code == 0, result
    row = result["repos"][0]
    assert row["base"] == "main" and row["branch"] == "feat/1-2-listar"
    assert row["undeclared"] == ["src/Extra.cs"]
    assert row["declared_not_changed"] == ["src/Fantasma.cs"]
    assert row["uncommitted"] is True
    assert result["consistent"] is False


def test_diff_inclui_commits_trabalho_e_nao_rastreados(setup, tmp_path):
    project, repo = setup
    out = tmp_path / "revisao" / "diff.txt"
    code, result = run(project, "diff", "1-2-listar", "--repo", f"loja-api={repo}", "--out", str(out))
    assert code == 0, result
    text = out.read_text(encoding="utf-8")
    assert "src/Listar.cs" in text and "int x;" in text and "src/Extra.cs" in text
    assert result["repos"][0]["untracked"] == ["src/Extra.cs"]


def test_repo_invalido(setup, tmp_path):
    project, _ = setup
    code, message = run(project, "integrity", "1-2-listar", "--repo", f"x={tmp_path}")
    assert code == 1 and "não é um repositório Git" in message
