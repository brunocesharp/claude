"""Testes do customize.py: uma regra de merge por teste, mais os customize.toml reais das skills.
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent
PLUGINS = SCRIPTS.parents[3]
sys.path.insert(0, str(SCRIPTS))

from customize import merge  # noqa: E402

BASE = """
[workflow]
persistent_facts = []
activation_steps_prepend = []
on_complete = ""
max_stories = 8
mode = "completa"

[workflow.prefixes]
epic = "[FEATURE]"
story = "[TASK]"

[[workflow.lenses]]
id = "aderencia"
enabled = true
focus = "critérios"

[[workflow.lenses]]
id = "seguranca"
enabled = true
focus = "auth"
"""


def m(base: dict, over: dict):
    warnings: list[str] = []
    return merge(base, over, "", warnings), warnings


def test_escalar_substitui():
    result, warnings = m({"a": 1, "b": "x"}, {"a": 2})
    assert result == {"a": 2, "b": "x"} and warnings == []


def test_tabela_merge_profundo():
    result, _ = m({"p": {"epic": "[FEATURE]", "story": "[TASK]"}}, {"p": {"story": "[US]"}})
    assert result == {"p": {"epic": "[FEATURE]", "story": "[US]"}}


def test_lista_de_tabelas_com_id_mescla_no_lugar_e_acrescenta():
    base = {"l": [{"id": "a", "on": True, "f": "x"}, {"id": "b", "on": True, "f": "y"}]}
    result, _ = m(base, {"l": [{"id": "b", "on": False}, {"id": "c", "on": True, "f": "z"}]})
    assert result["l"] == [{"id": "a", "on": True, "f": "x"}, {"id": "b", "on": False, "f": "y"},
                           {"id": "c", "on": True, "f": "z"}]


def test_lista_de_tabelas_com_code():
    result, _ = m({"c": [{"code": "dotnet", "suite": "dotnet test"}]}, {"c": [{"code": "dotnet", "suite": "make test"}]})
    assert result["c"] == [{"code": "dotnet", "suite": "make test"}]


def test_outras_listas_acumulam_e_nao_removem():
    result, _ = m({"facts": ["a"]}, {"facts": ["b"]})
    assert result["facts"] == ["a", "b"]


def test_chave_desconhecida_e_tipo_errado_sao_ignorados_com_aviso():
    result, warnings = m({"a": 1, "t": {"x": 1}}, {"z": 1, "a": "texto", "t": [1]})
    assert result == {"a": 1, "t": {"x": 1}}
    assert any("z: não é customizável" in w for w in warnings)
    assert any("a: tipo diferente" in w for w in warnings)
    assert any("t: esperava uma tabela" in w for w in warnings)


def run(skill_dir: Path, project: Path, *args: str):
    result = subprocess.run([sys.executable, str(SCRIPTS / "customize.py"), "--skill-dir", str(skill_dir),
                             "--project", str(project), *args], capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


@pytest.fixture
def env(tmp_path: Path):
    skill = tmp_path / "plugin" / "skills" / "minha-skill"
    skill.mkdir(parents=True)
    (skill / "customize.toml").write_text(BASE, encoding="utf-8")
    project = tmp_path / "ws" / "docs" / "loja"
    (project / "_custom").mkdir(parents=True)
    (tmp_path / "ws" / "docs" / "padroes").mkdir()
    (tmp_path / "ws" / "docs" / "padroes" / "api.md").write_text("# padrão", encoding="utf-8")
    return skill, project


def test_sem_override_devolve_a_base(env):
    skill, project = env
    code, result = run(skill, project)
    assert code == 0 and result["override"] is None
    assert result["resolved"]["workflow"]["max_stories"] == 8


def test_override_do_projeto_e_fatos(env):
    skill, project = env
    (project / "_custom" / "minha-skill.toml").write_text(
        '[workflow]\nmax_stories = 5\npersistent_facts = ["file:docs/padroes/*.md", "Sempre em inglês nos nomes"]\n'
        '[[workflow.lenses]]\nid = "seguranca"\nenabled = false\n', encoding="utf-8")
    code, result = run(skill, project, "--key", "workflow.max_stories", "--key", "workflow.lenses")
    assert code == 0, result
    assert result["resolved"]["workflow.max_stories"] == 5
    assert result["resolved"]["workflow.lenses"][1] == {"id": "seguranca", "enabled": False, "focus": "auth"}
    assert result["facts"] == [{"source": "file:docs/padroes/*.md", "files": ["docs/padroes/api.md"]},
                               {"source": "texto", "text": "Sempre em inglês nos nomes"}]
    assert result["warnings"] == []


def test_avisa_override_nao_esparso(env):
    skill, project = env
    (project / "_custom" / "minha-skill.toml").write_text(
        '[workflow]\nmax_stories = 8\nmode = "completa"\non_complete = ""\n', encoding="utf-8")
    _, result = run(skill, project)
    assert any("não esparso" in w for w in result["warnings"])


def test_skill_sem_customize(tmp_path):
    code, message = run(tmp_path, tmp_path)
    assert code == 1 and "não é customizável" in message


CUSTOMIZABLE = ["spec-plan/skills/spec-functional", "spec-plan/skills/plan-epics", "delivery/skills/sprint-planning",
                "delivery/skills/create-story", "delivery/skills/dev-story", "delivery/skills/story-review",
                "delivery/skills/retrospective", "delivery/skills/correct-course"]


@pytest.mark.parametrize("skill", CUSTOMIZABLE)
def test_customize_toml_das_skills(skill):
    folder = PLUGINS / skill
    data = tomllib.loads((folder / "customize.toml").read_text(encoding="utf-8"))
    workflow = data["workflow"]
    for key in ("persistent_facts", "activation_steps_prepend", "activation_steps_append", "on_complete"):
        assert key in workflow, f"{skill}: falta workflow.{key}"
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    assert "## Customização" in text and "customize.py" in text, f"{skill}: falta o bloco de ativação"


def test_localiza_skill_pelo_installed_plugins(env, tmp_path, monkeypatch):
    skill, project = env
    config = tmp_path / "config"
    (config / "plugins").mkdir(parents=True)
    install = skill.parent.parent  # .../plugin
    (config / "plugins" / "installed_plugins.json").write_text(json.dumps(
        {"version": 2, "plugins": {"x@claude": [{"scope": "user", "installPath": str(install)}]}}), encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPTS / "customize.py"), "--skill", "minha-skill",
                             "--project", str(project)], capture_output=True, text=True, encoding="utf-8",
                            env={**__import__("os").environ, "CLAUDE_CONFIG_DIR": str(config)})
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["base"] == str(skill / "customize.toml")


def test_localiza_skill_no_repositorio_e_falha_com_nome_desconhecido(env, tmp_path):
    _, project = env
    env_vars = {**__import__("os").environ, "CLAUDE_CONFIG_DIR": str(tmp_path / "vazio")}
    ok = subprocess.run([sys.executable, str(SCRIPTS / "customize.py"), "--skill", "story-review", "--project",
                         str(project)], capture_output=True, text=True, encoding="utf-8", env=env_vars)
    assert ok.returncode == 0, ok.stdout
    assert json.loads(ok.stdout)["base"].replace("\\", "/").endswith("delivery/skills/story-review/customize.toml")
    bad = subprocess.run([sys.executable, str(SCRIPTS / "customize.py"), "--skill", "nao-existe", "--project",
                          str(project)], capture_output=True, text=True, encoding="utf-8", env=env_vars)
    assert bad.returncode == 1 and "não encontrada" in bad.stdout
