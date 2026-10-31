# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Testes do setup.py e do config.py. Rodar: uv run --with pytest pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
SKILL = SCRIPTS.parent
REPO_PLUGINS = SKILL.parent.parent.parent


def run(script: Path, *args: str, cwd: Path | None = None) -> tuple[int, object]:
    result = subprocess.run(
        [sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8", cwd=cwd
    )
    out = result.stdout.strip()
    if out.startswith("error:"):
        return result.returncode, out
    return result.returncode, json.loads(out)


def setup(ws: Path, *args: str) -> tuple[int, object]:
    return run(SCRIPTS / "setup.py", "--workspace-root", str(ws), *args)


def answer_all(ws: Path, **overrides: str) -> dict:
    _, questions = setup(ws, "--list-config-questions")
    answers = {q["key"]: q["default"] for q in questions}
    answers.update(overrides)
    path = ws / "answers.json"
    path.write_text(json.dumps(answers), encoding="utf-8")
    code, result = setup(ws, "--answers", str(path))
    assert code == 0, result
    assert not path.exists(), "o arquivo de respostas deve ser apagado"
    return result


def test_status_em_workspace_vazio_pede_setup(tmp_path):
    code, status = setup(tmp_path, "--status")
    assert code == 0
    assert status["sdd_exists"] is False
    assert status["next"] == "setup"
    assert not (tmp_path / "_sdd").exists(), "status não grava nada"


def test_defaults_expandem_placeholders(tmp_path):
    _, questions = setup(tmp_path, "--list-config-questions")
    by_key = {q["key"]: q for q in questions}
    assert by_key["workspace.name"]["default"] == tmp_path.name
    assert by_key["user.name"]["scope"] == "user"
    assert by_key["language.documents"]["scope"] == "team"


def test_primeiro_setup_grava_config_scripts_e_versao(tmp_path):
    result = answer_all(tmp_path, **{"user.name": "Ana"})
    assert result["sdd"] == "created"
    assert result["pending_questions"] == 0
    assert result["answers"]["user"]["user.name"] == "Ana"
    assert (tmp_path / "_sdd" / "scripts" / "config.py").is_file()
    assert not (tmp_path / "_sdd" / "scripts" / "setup.py").exists()
    versions = tomllib.loads((tmp_path / "_sdd" / "version.toml").read_text(encoding="utf-8"))
    assert versions["modules"]["sdd"] == "1.0.2"
    _, status = setup(tmp_path, "--status")
    assert status["current"] is True
    assert status["next"] == "discovery-init"


def test_setup_nunca_altera_valor_existente(tmp_path):
    answer_all(tmp_path)
    team = tmp_path / "_sdd" / "config.toml"
    team.write_text(team.read_text(encoding="utf-8").replace('"pt-BR"', '"en-US"'), encoding="utf-8")
    path = tmp_path / "a.json"
    path.write_text(json.dumps({"language.documents": "pt-BR"}), encoding="utf-8")
    code, result = setup(tmp_path, "--answers", str(path))
    assert code == 0
    assert result["written"]["team"] == []
    assert result["answers"]["team"]["language.documents"] == "en-US"


def test_so_pergunta_chaves_novas(tmp_path):
    answer_all(tmp_path, **{"backlog.prefixes": "nao"})
    _, questions = setup(tmp_path, "--list-config-questions")
    assert questions == []
    (tmp_path / "_sdd" / "config.toml").write_text('workspace.name = "x"\n', encoding="utf-8")
    _, questions = setup(tmp_path, "--list-config-questions")
    assert "language.documents" in {q["key"] for q in questions}
    assert "workspace.name" not in {q["key"] for q in questions}


def test_modulos_filtrados_e_desconhecido(tmp_path):
    _, questions = setup(tmp_path, "--list-config-questions", "--modules", "sdd")
    assert "backlog.prefixes" not in {q["key"] for q in questions}
    code, out = setup(tmp_path, "--status", "--modules", "nao-existe")
    assert code == 1 and out.startswith("error:")


def test_resposta_para_chave_desconhecida_falha(tmp_path):
    path = tmp_path / "a.json"
    path.write_text(json.dumps({"nada.disso": "x"}), encoding="utf-8")
    code, out = setup(tmp_path, "--answers", str(path))
    assert code == 1 and "nada.disso" in out


def test_scripts_desatualizados_pedem_update(tmp_path):
    answer_all(tmp_path)
    (tmp_path / "_sdd" / "scripts" / "config.py").write_text("# velho\n", encoding="utf-8")
    _, status = setup(tmp_path, "--status")
    assert status["scripts"]["config.py"] == "stale"
    assert status["next"] == "update"


def test_gitignore(tmp_path):
    (tmp_path / ".git").mkdir()
    _, status = setup(tmp_path, "--status")
    assert status["gitignore"] == "unprotected"
    code, result = setup(tmp_path, "--gitignore")
    assert code == 0 and result["changed"] is True
    _, status = setup(tmp_path, "--status")
    assert status["gitignore"] == "protected"


def test_config_resolve_com_precedencia_do_pessoal(tmp_path):
    answer_all(tmp_path, **{"language.conversation": "en-US"})
    (tmp_path / "_sdd" / "config.user.toml").write_text(
        'user.name = "Bia"\nlanguage.conversation = "es"\n', encoding="utf-8"
    )
    sub = tmp_path / "docs" / "projeto"
    sub.mkdir(parents=True)
    code, config = run(tmp_path / "_sdd" / "scripts" / "config.py", "--key", "language.conversation", "--key", "x.y", cwd=sub)
    assert code == 0
    assert config == {"language.conversation": "es", "x.y": None}


def test_projetos_listados(tmp_path):
    answer_all(tmp_path)
    project = tmp_path / "docs" / "loja"
    project.mkdir(parents=True)
    (project / "project-config.json").write_text(json.dumps({"name": "Loja"}), encoding="utf-8")
    (tmp_path / "docs" / "antigo").mkdir()
    (tmp_path / "docs" / "antigo" / "project.md").write_text("# Antigo", encoding="utf-8")
    _, status = setup(tmp_path, "--status")
    assert {p["slug"]: p["has_config"] for p in status["projects"]} == {"loja": True, "antigo": False}
    assert status["next"] is None


def test_versao_dos_registros_igual_ao_plugin_json():
    for record in sorted((SKILL / "modules").glob("*.toml")):
        module = tomllib.loads(record.read_text(encoding="utf-8"))["module"]
        manifest = REPO_PLUGINS / module["plugin"] / ".claude-plugin" / "plugin.json"
        assert manifest.is_file(), f"{record.name}: plugin {module['plugin']} não existe"
        plugin = json.loads(manifest.read_text(encoding="utf-8"))
        assert module["version"] == plugin["version"], f"{record.name}: versão diferente do plugin.json"
        for skill in module["skills"]:
            assert (REPO_PLUGINS / module["plugin"] / "skills" / skill / "SKILL.md").is_file(), skill
