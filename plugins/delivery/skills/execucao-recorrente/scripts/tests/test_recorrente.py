"""Testes do recorrente.py (skill execucao-recorrente).
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/delivery/skills/execucao-recorrente/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "recorrente.py"

SPRINT = """version: 1
project: {projeto}
updated_at: '2026-10-30'
epics:
  epic-1:
    title: Cadastro
    escopo: produtos
    status: in-progress
    retrospective: optional
    stories:
      1-1-criar:
        title: Criar
        status: done
        repositories: [api]
        file: stories/1-1-criar.md
      1-2-listar:
        title: Listar
        status: ready-for-dev
        repositories: [api]
        file: stories/1-2-listar.md
      1-3-editar:
        title: Editar
        status: ready-for-dev
        repositories: [api]
        file: stories/1-3-editar.md
      1-4-importar:
        title: Importar
        status: ready-for-dev
        repositories: [api]
        file: stories/1-4-importar.md
      1-5-exportar:
        title: Exportar
        status: backlog
        repositories: [api]
"""


def story(status: str, extra: str = "") -> str:
    return f"---\nid: x\nstatus: {status}\n{extra}---\n# story\n"


def make_workspace(root: Path, projeto: str) -> Path:
    (root / "_sdd").mkdir(parents=True)
    project = root / "docs" / projeto
    stories = project / "implementacao" / "stories"
    stories.mkdir(parents=True)
    (project / "implementacao" / "sprint-status.yaml").write_text(SPRINT.format(projeto=projeto), encoding="utf-8")
    (stories / "1-1-criar.md").write_text(story("done"), encoding="utf-8")
    (stories / "1-2-listar.md").write_text(story("ready-for-dev", "depends_on: [1-1-criar]\n"), encoding="utf-8")
    (stories / "1-3-editar.md").write_text(story("ready-for-dev", "checkpoint: true\n"), encoding="utf-8")
    (stories / "1-4-importar.md").write_text(story("ready-for-dev", "depends_on: [1-3-editar]\n"), encoding="utf-8")
    return root


@pytest.fixture
def env(tmp_path: Path) -> dict:
    prio = make_workspace(tmp_path / "ws-prio", "loja")
    sem = make_workspace(tmp_path / "ws-sem", "estoque")
    config = tmp_path / "cfg" / "execucao-recorrente.toml"
    config.parent.mkdir()
    config.write_text(f"[repositorios]\nprioritarios = ['{prio}']\nsem_prioridade = ['{sem}']\n", encoding="utf-8")
    return {"prio": prio, "sem": sem, "config": config}


def run(*args: str):
    result = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


def scan(env: dict) -> dict:
    code, out = run("scan", "--config", str(env["config"]))
    assert code == 0, out
    return out


def set_status(workspace: Path, projeto: str, story_id: str, status: str) -> None:
    path = workspace / "docs" / projeto / "implementacao" / "sprint-status.yaml"
    head, tail = path.read_text(encoding="utf-8").split(f"      {story_id}:\n", 1)
    lines = tail.split("\n")
    lines[1] = f"        status: {status}"
    path.write_text(head + f"      {story_id}:\n" + "\n".join(lines), encoding="utf-8")


def registrar(workspace: Path, projeto: str, story_id: str, resultado: str, motivo: str = ""):
    return run("registrar", str(workspace), "--projeto", projeto, "--id", story_id, "--acao", "dev-story",
               "--resultado", resultado, "--motivo", motivo)


def test_prioritario_vem_antes_do_sem_prioridade(env):
    out = scan(env)
    assert out["escolhida"]["projeto"] == "loja" and out["escolhida"]["prioridade"] == "prioritario"
    assert out["escolhida"]["id"] == "1-2-listar"
    assert [(i["projeto"], i["id"]) for i in out["fila"]] == [("loja", "1-2-listar"), ("estoque", "1-2-listar")]
    puladas = {p["id"]: p["motivo"] for p in out["grupos"][0]["repositorios"][0]["projetos"][0]["puladas"]}
    assert "checkpoint" in puladas["1-3-editar"] and "1-3-editar" in puladas["1-4-importar"]


def test_sem_tarefa_no_prioritario_usa_o_sem_prioridade(env):
    set_status(env["prio"], "loja", "1-2-listar", "review")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque" and out["escolhida"]["prioridade"] == "sem-prioridade"
    assert "sem-prioridade" in out["motivo"]


def test_sem_tarefas_em_nenhum_grupo(env):
    set_status(env["prio"], "loja", "1-2-listar", "review")
    set_status(env["sem"], "estoque", "1-2-listar", "done")
    out = scan(env)
    assert out["escolhida"] is None and "sem tarefas" in out["motivo"]


def test_tarefa_em_andamento_impede_iniciar_outra(env):
    code, lock = run("lock", "adquirir", "--config", str(env["config"]), "--dono", "rodada 19:05")
    assert code == 0 and lock["adquirido"] is True
    assert Path(lock["lock_file"]).name == "execucao-recorrente.lock.json"
    out = scan(env)
    assert out["em_andamento"] is True and out["escolhida"] is None and "em andamento" in out["motivo"]
    _, second = run("lock", "adquirir", "--config", str(env["config"]))
    assert second["adquirido"] is False


def test_trava_expirada_e_assumida_e_liberar_funciona(env):
    run("lock", "adquirir", "--config", str(env["config"]))
    lock_file = env["config"].with_name("execucao-recorrente.lock.json")
    data = json.loads(lock_file.read_text(encoding="utf-8"))
    data["expira_em"] = (datetime.now().astimezone() - timedelta(minutes=1)).isoformat()
    lock_file.write_text(json.dumps(data), encoding="utf-8")
    assert scan(env)["em_andamento"] is False
    _, again = run("lock", "adquirir", "--config", str(env["config"]))
    assert again["adquirido"] is True and again["assumiu_expirado"] is True
    _, freed = run("lock", "liberar", "--config", str(env["config"]))
    assert freed["liberado"] is True and scan(env)["em_andamento"] is False


def test_retomada_vem_antes_de_tudo_mesmo_sem_prioridade(env):
    registrar(env["sem"], "estoque", "1-2-listar", "iniciada")
    set_status(env["sem"], "estoque", "1-2-listar", "in-progress")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque" and out["escolhida"]["retomada"] is True
    assert "retomar" in out["motivo"]


def test_in_progress_de_outra_pessoa_e_pulada(env):
    set_status(env["prio"], "loja", "1-2-listar", "in-progress")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque"
    puladas = {p["id"]: p["motivo"] for p in out["grupos"][0]["repositorios"][0]["projetos"][0]["puladas"]}
    assert "sem ter sido iniciada" in puladas["1-2-listar"]


def test_falhas_contam_e_param_no_limite(env):
    for _ in range(3):
        code, reg = registrar(env["prio"], "loja", "1-2-listar", "falhou", "build quebrou")
        assert code == 0
    assert reg["tentativas"] == 3 and reg["limite_atingido"] is True
    assert scan(env)["escolhida"]["projeto"] == "estoque"
    log = Path(reg["log"]).read_text(encoding="utf-8")
    assert log.count("build quebrou") == 3 and "| 3/3 |" in log


def test_pulada_vai_para_o_log_so_quando_o_motivo_muda(env):
    code, reg = registrar(env["prio"], "loja", "1-2-listar", "pulada", "aguardando commit da 1-1")
    assert code == 0 and reg["registrado"] is True and reg["tentativas"] == 0
    log_file = Path(reg["log"])
    _, again = registrar(env["prio"], "loja", "1-2-listar", "pulada", "aguardando commit da 1-1")
    assert again["registrado"] is False and again["repetida"] is True
    assert log_file.read_text(encoding="utf-8").count("aguardando commit") == 1
    _, other = registrar(env["prio"], "loja", "1-2-listar", "pulada", "branch feat/1-1 em aberto")
    assert other["registrado"] is True
    # depois de executar, o mesmo motivo de antes volta a ser registrado
    registrar(env["prio"], "loja", "1-2-listar", "falhou", "build quebrou")
    _, back = registrar(env["prio"], "loja", "1-2-listar", "pulada", "branch feat/1-1 em aberto")
    assert back["registrado"] is True and back["tentativas"] == 1
    assert log_file.read_text(encoding="utf-8").count("branch feat/1-1 em aberto") == 2
    assert scan(env)["escolhida"]["id"] == "1-2-listar"


def test_projeto_sem_sprint_status_fica_fora(env, tmp_path):
    projeto = tmp_path / "ws-novo" / "docs" / "rh"
    projeto.mkdir(parents=True)
    (tmp_path / "ws-novo" / "_sdd").mkdir()
    (projeto / "project.md").write_text("# rh\n", encoding="utf-8")
    env["config"].write_text(f"[repositorios]\nprioritarios = ['{projeto}', '{tmp_path / 'ws-novo'}']\n"
                             f"sem_prioridade = ['{env['sem']}']\n", encoding="utf-8")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque" and not out["erros"]
    notas = [r.get("nota", "") for r in out["grupos"][0]["repositorios"]]
    assert all("sprint-status.yaml" in n for n in notas)


def test_override_do_projeto(env):
    custom = env["prio"] / "docs" / "loja" / "_custom"
    custom.mkdir()
    (custom / "execucao-recorrente.toml").write_text('[workflow]\nacoes = ["create-story"]\n', encoding="utf-8")
    out = scan(env)
    # create-story é da skill criacao-story-recorrente: aqui o projeto fica sem ações e o scan avisa
    assert out["escolhida"]["projeto"] == "estoque"
    assert any("criacao-story-recorrente" in a for a in out["avisos"])
    (custom / "execucao-recorrente.toml").write_text("[workflow]\nhabilitado = false\n", encoding="utf-8")
    assert scan(env)["escolhida"]["projeto"] == "estoque"


def test_config_aceita_pasta_do_projeto_e_aponta_erros(env):
    env["config"].write_text(
        f"[repositorios]\nprioritarios = ['{env['prio'] / 'docs' / 'loja'}', '{env['prio'] / 'nao-existe'}']\n"
        f"sem_prioridade = ['{env['prio'] / 'docs' / 'loja'}']\nfoo = []\n", encoding="utf-8")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "loja" and out["erros"]
    assert any("duas listas" in a for a in out["avisos"]) and any("foo" in a for a in out["avisos"])
    assert [i["projeto"] for i in out["fila"]] == ["loja"]


def test_init_config_nao_sobrescreve(tmp_path):
    config = tmp_path / "novo" / "execucao-recorrente.toml"
    code, out = run("init-config", "--config", str(config))
    assert code == 0 and out["criado"] is True
    code, cfg = run("config", "--config", str(config))
    assert code == 0 and cfg["prioritarios"] == [] and cfg["sem_prioridade"] == [] and cfg["lock_expira_min"] == 90
    _, again = run("init-config", "--config", str(config))
    assert again["criado"] is False


def test_config_ausente_e_erro(tmp_path):
    code, out = run("scan", "--config", str(tmp_path / "x.toml"))
    assert code == 1 and "init-config" in out
