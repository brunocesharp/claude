"""Testes do status.py, workspace.py, migrate.py e do hook.
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
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sprint-status.yaml"


def run(script: str, *args: str, stdin: str | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True,
                          encoding="utf-8", input=stdin, cwd=cwd)


def out(result: subprocess.CompletedProcess):
    text = result.stdout.strip()
    return text if text.startswith("error:") else json.loads(text)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    folder = tmp_path / "docs" / "loja"
    impl = folder / "implementacao"
    (impl / "stories").mkdir(parents=True)
    shutil.copy(FIXTURE, impl / "sprint-status.yaml")
    (impl / "stories" / "1-1-criar-produto.md").write_text("---\nid: 1-1-criar-produto\nstatus: done\n---\n# 1.1\n", encoding="utf-8")
    (impl / "stories" / "1-2-listar-produtos.md").write_text(
        "---\nid: 1-2-listar-produtos\nstatus: ready-for-dev\n---\n# 1.2\n\nstatus: não mexer aqui\n", encoding="utf-8")
    return folder


def status(project: Path, *args: str):
    result = run("status.py", "--project", str(project), *args)
    return result.returncode, out(result)


def current(project: Path) -> dict:
    return yaml.safe_load((project / "implementacao" / "sprint-status.yaml").read_text(encoding="utf-8"))


def test_show_conta_por_epico(project):
    code, board = status(project, "show")
    assert code == 0
    epic1 = board["epics"][0]
    assert (epic1["done"], epic1["total"]) == (1, 3)
    assert board["totals"]["backlog"] == 2


def test_next_segue_prioridade(project):
    _, action = status(project, "next")
    assert action == {"action": "dev-story", "id": "1-2-listar-produtos", "epic": "epic-1",
                      "reason": "implementar em uma sessão nova"}
    status(project, "set", "1-2-listar-produtos", "in-progress")
    status(project, "set", "1-2-listar-produtos", "review")
    _, action = status(project, "next")
    assert action["action"] == "story-review"


def test_set_valido_grava_e_sincroniza_frontmatter(project):
    code, result = status(project, "set", "1-2-listar-produtos", "in-progress")
    assert code == 0 and result["changed"] and result["story_file"] == "updated"
    assert current(project)["epics"]["epic-1"]["stories"]["1-2-listar-produtos"]["status"] == "in-progress"
    text = (project / "implementacao" / "stories" / "1-2-listar-produtos.md").read_text(encoding="utf-8")
    assert "status: in-progress" in text
    assert "status: não mexer aqui" in text, "só o frontmatter muda"
    assert (project / "implementacao" / "sprint-status.yaml").read_text(encoding="utf-8").startswith("# Estado")


def test_transicao_invalida_recusada_com_mensagem(project):
    code, message = status(project, "set", "1-2-listar-produtos", "done")
    assert code == 1
    assert "ready-for-dev → done não permitida" in message
    assert "in-progress" in message
    assert current(project)["epics"]["epic-1"]["stories"]["1-2-listar-produtos"]["status"] == "ready-for-dev"


def test_done_e_final_mas_force_passa(project):
    code, message = status(project, "set", "1-1-criar-produto", "in-progress")
    assert code == 1 and "correct-course" in message
    code, result = status(project, "set", "1-1-criar-produto", "in-progress", "--force")
    assert code == 0 and result["forced"] is True


def test_story_sem_arquivo_nao_sai_do_backlog(project):
    code, message = status(project, "set", "1-3-importar-planilha", "ready-for-dev")
    assert code == 1 and "file" in message


def test_epico_vai_para_in_progress_com_a_primeira_story(project):
    data = current(project)
    data["epics"]["epic-2"]["stories"]["2-1-movimentar-estoque"]["file"] = "stories/2-1-movimentar-estoque.md"
    (project / "implementacao" / "sprint-status.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    code, result = status(project, "set", "2-1-movimentar-estoque", "ready-for-dev")
    assert code == 0 and result["epic_status"] == "in-progress" and result["story_file"] == "missing"


def test_epico_done_exige_stories_finalizadas_e_retrospectiva(project):
    code, message = status(project, "set", "epic-1", "done")
    assert code == 1 and "1-2-listar-produtos" in message
    status(project, "set", "1-3-importar-planilha", "dropped")
    for state in ("in-progress", "review", "done"):
        status(project, "set", "1-2-listar-produtos", state)
    _, action = status(project, "next")
    assert action["action"] == "retrospective" and action["id"] == "epic-1"
    code, result = status(project, "set", "epic-1-retrospective", "done")
    assert code == 0 and result["to"] == "done"
    _, action = status(project, "next")
    assert action["action"] == "close-epic"
    code, _ = status(project, "set", "epic-1", "done")
    assert code == 0
    _, action = status(project, "next")
    assert action == {"action": "create-story", "id": "2-1-movimentar-estoque", "epic": "epic-2",
                      "reason": "gerar o arquivo da story"}


def test_validacao_aponta_erros(project):
    path = project / "implementacao" / "sprint-status.yaml"
    data = current(project)
    data["epics"]["epic-2"]["stories"]["1-9-errada"] = {"title": "x", "status": "talvez"}
    data["epics"]["epic-2"]["status"] = "done"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    code, message = status(project, "show")
    assert code == 1
    assert "1-9-errada: está no epic-2" in message
    assert "'talvez' inválido" in message
    assert "epic-2: done com stories ainda abertas" in message


def test_check_acusa_frontmatter_divergente(project):
    story = project / "implementacao" / "stories" / "1-1-criar-produto.md"
    story.write_text(story.read_text(encoding="utf-8").replace("status: done", "status: review"), encoding="utf-8")
    code, result = status(project, "check")
    assert code == 0 and result["valid"] is False
    assert "1-1-criar-produto: frontmatter diz review" in result["problems"][0]


def test_arquivo_inexistente(tmp_path):
    code, message = status(tmp_path, "show")
    assert code == 1 and "sprint-planning" in message


def hook(payload: dict) -> subprocess.CompletedProcess:
    return run("hook_sprint_status.py", stdin=json.dumps(payload))


def test_hook_ignora_outros_arquivos_e_aceita_valido(project):
    assert hook({"tool_input": {"file_path": str(project / "project.md")}}).returncode == 0
    path = project / "implementacao" / "sprint-status.yaml"
    assert hook({"tool_input": {"file_path": str(path)}}).returncode == 0


def test_hook_bloqueia_arquivo_invalido(project):
    path = project / "implementacao" / "sprint-status.yaml"
    path.write_text(path.read_text(encoding="utf-8").replace("status: done", "status: pronto", 1), encoding="utf-8")
    result = hook({"tool_name": "Edit", "tool_input": {"file_path": str(path)}})
    assert result.returncode == 2
    assert "'pronto' inválido" in result.stderr


def test_workspace_resume_projetos(project):
    root = project.parent.parent
    (project / "project.md").write_text(
        "# Loja\n\n## Status das Fases\n- [x] Discovery\n- [x] Escopo\n- [ ] Especificação\n", encoding="utf-8")
    (project / "project-config.json").write_text(json.dumps({"name": "Loja", "repositories": "um"}), encoding="utf-8")
    (root / "docs" / "workspace.md").write_text(
        "# W\n\n## Projetos\n\n| Projeto | Pasta | Repositório | Código local | Situação |\n"
        "|---|---|---|---|---|\n| Loja | `docs/loja/` | x | y | Desenvolvimento |\n", encoding="utf-8")
    (project / "repositorios.md").write_text("# Repos", encoding="utf-8")
    result = run("workspace.py", "--workspace-root", str(root))
    assert result.returncode == 0, result.stdout
    info = out(result)["projects"][0]
    assert info["name"] == "Loja" and info["repositories"] == "varios"
    assert info["phases"] == {"done": ["Discovery", "Escopo"], "current": "Especificação"}
    assert info["situacao"] == "Desenvolvimento"
    assert info["sprint"]["valid"] and info["sprint"]["next"]["id"] == "1-2-listar-produtos"


def test_migrate_sem_migracoes_declaradas(tmp_path):
    result = run("migrate.py", "--workspace-root", str(tmp_path), "--all")
    assert result.returncode == 0 and out(result) == []
    result = run("migrate.py", "--workspace-root", str(tmp_path), "--mark-applied", "nao-existe")
    assert result.returncode == 1


def test_migrate_versao(tmp_path):
    sys.path.insert(0, str(SCRIPTS))
    import migrate

    migrations = [{"id": "x", "title": "t", "kind": "upgrade", "to": "1.2.0", "guide": "SKILL.md", "module": "sdd"},
                  {"id": "y", "title": "t", "kind": "optional", "to": "1.0.0", "guide": "SKILL.md", "module": "sdd"}]
    sdd = tmp_path / "_sdd"
    sdd.mkdir()
    (sdd / "version.toml").write_text('modules.sdd = "1.1.0"\n', encoding="utf-8")
    assert [m["id"] for m in migrate.listing(tmp_path, migrations, False)] == ["x"]
    assert [m["id"] for m in migrate.listing(tmp_path, migrations, True)] == ["x", "y"]
    assert migrate.mark_applied(tmp_path, migrations, "x")["changed"] is True
    assert [m["id"] for m in migrate.listing(tmp_path, migrations, True)] == ["y"]
    (sdd / "version.toml").write_text('modules.sdd = "1.2.0"\n', encoding="utf-8")
    assert migrate.listing(tmp_path, migrations, False) == []
