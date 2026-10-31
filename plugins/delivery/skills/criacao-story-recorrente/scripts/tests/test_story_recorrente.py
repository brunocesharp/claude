"""Testes do story_recorrente.py (skill criacao-story-recorrente; perfil criacao do recorrente.py).
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/delivery/skills/criacao-story-recorrente/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "story_recorrente.py"

SPRINT = """version: 1
project: {projeto}
updated_at: '2026-10-31'
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
        status: backlog
        repositories: [api]
      1-3-editar:
        title: Editar
        status: backlog
        repositories: [api]
      1-4-importar:
        title: Importar
        status: backlog
        repositories: [api]
"""

EPIC = """---
id: epic-1
title: Cadastro
escopo: produtos
stories:
  - id: 1-1-criar
    title: Criar
    repositories: [api]
  - id: 1-2-listar
    title: Listar
    repositories: [api]
    depends_on: [1-1-criar]
  - id: 1-3-editar
    title: Editar
    repositories: [api]
    depends_on: [1-2-listar]
  - id: 1-4-importar
    title: Importar
    repositories: [api]
---
# Épico 1
"""


def make_workspace(root: Path, projeto: str) -> Path:
    (root / "_sdd").mkdir(parents=True)
    impl = root / "docs" / projeto / "implementacao"
    (impl / "stories").mkdir(parents=True)
    (impl / "epicos").mkdir()
    (impl / "sprint-status.yaml").write_text(SPRINT.format(projeto=projeto), encoding="utf-8")
    (impl / "epicos" / "epic-1-cadastro.md").write_text(EPIC, encoding="utf-8")
    return root


@pytest.fixture
def env(tmp_path: Path) -> dict:
    prio = make_workspace(tmp_path / "ws-prio", "loja")
    sem = make_workspace(tmp_path / "ws-sem", "estoque")
    config = tmp_path / "cfg" / "criacao-story-recorrente.toml"
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


def registrar(workspace: Path, projeto: str, story_id: str, resultado: str, motivo: str = "", acao: str = "create-story"):
    return run("registrar", str(workspace), "--projeto", projeto, "--id", story_id, "--acao", acao,
               "--resultado", resultado, "--motivo", motivo)


def puladas(out: dict, grupo: int = 0) -> dict:
    return {p["id"]: p["motivo"] for p in out["grupos"][grupo]["repositorios"][0]["projetos"][0]["puladas"]}


def test_cria_a_primeira_do_backlog_do_prioritario(env):
    out = scan(env)
    assert out["perfil"] == "criacao-story-recorrente"
    assert (out["escolhida"]["projeto"], out["escolhida"]["id"], out["escolhida"]["acao"]) == \
        ("loja", "1-2-listar", "create-story")
    # uma story nova por projeto: o sem prioridade entra na fila, mas só depois
    assert [(i["projeto"], i["id"]) for i in out["fila"]] == [("loja", "1-2-listar"), ("estoque", "1-2-listar")]


def test_dependencia_pendente_pula_para_a_proxima_sem_dependencia(env):
    set_status(env["prio"], "loja", "1-1-criar", "in-progress")
    out = scan(env)
    assert out["escolhida"]["id"] == "1-4-importar"
    motivos = puladas(out)
    assert "1-1-criar (in-progress)" in motivos["1-2-listar"] and "1-2-listar" in motivos["1-3-editar"]


def test_dependencia_em_review_vale_por_padrao_e_override_exige_done(env):
    set_status(env["prio"], "loja", "1-1-criar", "review")
    assert scan(env)["escolhida"]["id"] == "1-2-listar"
    custom = env["prio"] / "docs" / "loja" / "_custom"
    custom.mkdir()
    (custom / "criacao-story-recorrente.toml").write_text('[workflow]\ndependencias_em = ["done"]\n', encoding="utf-8")
    assert scan(env)["escolhida"]["id"] == "1-4-importar"


def test_limite_de_prontas_passa_para_o_sem_prioridade(env):
    set_status(env["prio"], "loja", "1-2-listar", "ready-for-dev")
    set_status(env["prio"], "loja", "1-4-importar", "ready-for-dev")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque" and out["escolhida"]["prioridade"] == "sem-prioridade"
    assert "max_prontas = 2" in puladas(out)[None]


def test_sem_tarefas_quando_tudo_esta_pronto(env):
    for ws, proj in ((env["prio"], "loja"), (env["sem"], "estoque")):
        for sid in ("1-2-listar", "1-3-editar", "1-4-importar"):
            set_status(ws, proj, sid, "ready-for-dev")
    out = scan(env)
    assert out["escolhida"] is None and "sem tarefas" in out["motivo"]


def test_retomada_vem_antes_do_prioritario(env):
    registrar(env["sem"], "estoque", "1-2-listar", "iniciada")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque" and out["escolhida"]["retomada"] is True
    assert "retomar" in out["motivo"]


def test_aguardando_confirmacao_nao_e_recriada(env):
    code, _ = registrar(env["prio"], "loja", "1-2-listar", "aguardando", "arquivo pronto")
    assert code == 0
    out = scan(env)
    assert "aguardando confirmação" in puladas(out)["1-2-listar"]
    assert out["escolhida"]["id"] == "1-4-importar"   # 1-3 depende da 1-2, que ainda está em backlog


def test_falhas_param_no_limite(env):
    for _ in range(3):
        _, reg = registrar(env["prio"], "loja", "1-2-listar", "falhou", "cenário 1.3 não existe mais na spec")
    assert reg["limite_atingido"] is True
    out = scan(env)
    assert "limite de 3" in puladas(out)["1-2-listar"] and out["escolhida"]["id"] == "1-4-importar"
    assert "_sdd" in reg["log"] and "criacao-story-recorrente" in reg["log"]
    assert "Criação recorrente de stories" in Path(reg["log"]).read_text(encoding="utf-8")


def test_acao_de_outra_skill_e_recusada(env):
    code, out = registrar(env["prio"], "loja", "1-2-listar", "iniciada", acao="dev-story")
    assert code == 1 and "criacao-story-recorrente" in out


def test_trava_propria_impede_segunda_rodada(env):
    code, lock = run("lock", "adquirir", "--config", str(env["config"]))
    assert code == 0 and lock["adquirido"] is True and lock["lock"]["dono"] == "criacao-story-recorrente"
    assert Path(lock["lock_file"]).name == "criacao-story-recorrente.lock.json"
    out = scan(env)
    assert out["em_andamento"] is True and out["escolhida"] is None
    run("lock", "liberar", "--config", str(env["config"]))
    assert scan(env)["escolhida"] is not None


def test_init_config_usa_o_nome_da_skill(tmp_path):
    config = tmp_path / "criacao-story-recorrente.toml"
    code, out = run("init-config", "--config", str(config))
    assert code == 0 and out["criado"] is True
    assert "criacao-story-recorrente" in config.read_text(encoding="utf-8")
    code, cfg = run("config", "--config", str(config))
    assert code == 0 and cfg["prioritarios"] == [] and cfg["sem_prioridade"] == []
