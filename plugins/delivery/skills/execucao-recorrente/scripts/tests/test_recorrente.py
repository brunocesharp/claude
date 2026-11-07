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
    set_status(env["prio"], "loja", "1-2-listar", "done")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque" and out["escolhida"]["prioridade"] == "sem-prioridade"
    assert "sem-prioridade" in out["motivo"]


def test_sem_tarefas_em_nenhum_grupo(env):
    set_status(env["prio"], "loja", "1-2-listar", "done")
    set_status(env["sem"], "estoque", "1-2-listar", "done")
    out = scan(env)
    assert out["escolhida"] is None and "sem tarefas" in out["motivo"]
    assert out["espera_sugerida_s"] == 1800
    # o checkpoint de 1-3-editar precisa de uma pessoa: vai para a lista de atenção
    assert {(a["projeto"], a["id"]) for a in out["atencao"]} >= {("loja", "1-3-editar"), ("estoque", "1-3-editar")}


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
    (custom / "execucao-recorrente.toml").write_text('[workflow]\nacoes = ["create-story", "deploy"]\n',
                                                     encoding="utf-8")
    out = scan(env)
    # só criação na loja, e ela já tem 2 stories prontas (max_prontas): a vez é do estoque
    assert out["escolhida"]["projeto"] == "estoque"
    assert any("deploy" in a for a in out["avisos"])
    (custom / "execucao-recorrente.toml").write_text("[workflow]\nhabilitado = false\n", encoding="utf-8")
    assert scan(env)["escolhida"]["projeto"] == "estoque"


def story_file(workspace: Path, projeto: str, story_id: str) -> Path:
    return workspace / "docs" / projeto / "implementacao" / "stories" / f"{story_id}.md"


def historico(workspace: Path, projeto: str, story_id: str, *linhas: str) -> None:
    path = story_file(workspace, projeto, story_id)
    text = path.read_text(encoding="utf-8")
    if "## Histórico" not in text:
        text += "\n## Histórico\n\n| Data | De → para | Por | Observação |\n|------|-----------|-----|------------|\n"
    path.write_text(text + "".join(f"{linha}\n" for linha in linhas), encoding="utf-8")


def reg(workspace: Path, projeto: str, story_id: str, resultado: str, *extra: str, acao: str = "dev-story"):
    return run("registrar", str(workspace), "--projeto", projeto, "--id", story_id, "--acao", acao,
               "--resultado", resultado, *extra)


def acoes(workspace: Path, projeto: str, lista: str) -> None:
    custom = workspace / "docs" / projeto / "_custom"
    custom.mkdir(exist_ok=True)
    (custom / "execucao-recorrente.toml").write_text(f"[workflow]\nacoes = {lista}\n", encoding="utf-8")


def test_review_vem_antes_de_ready_for_dev(env):
    set_status(env["prio"], "loja", "1-3-editar", "review")
    out = scan(env)
    assert out["escolhida"]["id"] == "1-3-editar" and out["escolhida"]["acao"] == "story-review"
    assert [i["acao"] for i in out["fila"][:2]] == ["story-review", "dev-story"]
    assert out["espera_sugerida_s"] == 60


def test_story_devolvida_pela_revisao_e_retomada(env):
    # bug: depois da story-review devolver para in-progress, a story ficava parada como "de outra pessoa"
    reg(env["prio"], "loja", "1-2-listar", "concluida", "--motivo", "2 correções R1, R2", acao="story-review")
    set_status(env["prio"], "loja", "1-2-listar", "in-progress")
    out = scan(env)
    escolhida = out["escolhida"]
    assert escolhida["id"] == "1-2-listar" and escolhida["acao"] == "dev-story" and escolhida["retomada"] is True
    assert escolhida["correcoes_revisao"] is True and escolhida["tentativas"] == 0
    assert "correções da revisão" in out["motivo"]


def test_devolvida_por_revisao_manual_e_retomada_pelo_historico(env):
    reg(env["prio"], "loja", "1-2-listar", "concluida")
    set_status(env["prio"], "loja", "1-2-listar", "in-progress")
    puladas = {p["id"]: p["motivo"] for p in scan(env)["grupos"][0]["repositorios"][0]["projetos"][0]["puladas"]}
    assert "sem ter sido iniciada" in puladas["1-2-listar"]
    historico(env["prio"], "loja", "1-2-listar", "| 01/11/2026 | review → in-progress | story-review | R1 aberta |")
    assert scan(env)["escolhida"]["correcoes_revisao"] is True


def test_cria_story_quando_nao_ha_o_que_implementar(env):
    for sid in ("1-2-listar", "1-3-editar", "1-4-importar"):
        set_status(env["prio"], "loja", sid, "done")
    out = scan(env)
    # o prioritário cria antes de o sem prioridade implementar
    assert out["escolhida"]["projeto"] == "loja" and out["escolhida"]["acao"] == "create-story"
    assert out["escolhida"]["id"] == "1-5-exportar"
    code, r = reg(env["prio"], "loja", "1-5-exportar", "iniciada", acao="create-story")
    assert code == 0 and "criacao-story-recorrente" in r["log"]
    # a criação interrompida é retomada antes de tudo (estado compartilhado com a criacao-story-recorrente)
    out = scan(env)
    assert out["escolhida"]["acao"] == "create-story" and out["escolhida"]["retomada"] is True
    acoes(env["prio"], "loja", '["dev-story"]')
    assert scan(env)["escolhida"]["projeto"] == "estoque"


def bloquear(env, story_id: str, *extra: str, por: str = "execucao-recorrente"):
    code, out = reg(env["prio"], "loja", story_id, "bloqueada", "--motivo", "sem o repositório api", *extra)
    set_status(env["prio"], "loja", story_id, "blocked")
    historico(env["prio"], "loja", story_id, f"| 02/11/2026 | ready-for-dev → blocked | {por} | x |")
    return code, out


def projeto_loja(out: dict) -> dict:
    return out["grupos"][0]["repositorios"][0]["projetos"][0]


def test_bloqueio_de_ambiente_volta_quando_resolvido(env, tmp_path):
    falta = tmp_path / "repos" / "api"
    code, out = bloquear(env, "1-2-listar", "--causa", "ambiente", "--verificar", f"caminho:{falta}")
    assert code == 0 and out["bloqueio"]["voltar_para"] == "ready-for-dev"
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque"
    assert any(a["id"] == "1-2-listar" and "ainda falta" in a["motivo"] for a in out["atencao"])
    falta.mkdir(parents=True)
    out = scan(env)
    escolhida = out["escolhida"]
    assert escolhida["acao"] == "desbloquear" and escolhida["acao_origem"] == "dev-story"
    assert escolhida["voltar_para"] == "ready-for-dev" and escolhida["causa"] == "ambiente"
    assert "desbloquear" in out["motivo"]
    code, done = reg(env["prio"], "loja", "1-2-listar", "desbloqueada", "--motivo", "repositório clonado")
    assert code == 0 and done["tentativas"] == 0 and done["voltar_para"] == "ready-for-dev"
    set_status(env["prio"], "loja", "1-2-listar", "ready-for-dev")
    assert scan(env)["escolhida"]["id"] == "1-2-listar"


def test_ambiente_sem_verificacao_e_recusado(env):
    code, out = reg(env["prio"], "loja", "1-2-listar", "bloqueada", "--causa", "ambiente", "--motivo", "x")
    assert code == 1 and "--verificar" in out
    code, out = reg(env["prio"], "loja", "1-2-listar", "bloqueada", "--causa", "ambiente", "--verificar", "url:x")
    assert code == 1 and "inválido" in out


def test_bloqueio_tecnico_volta_so_quando_algo_muda_e_com_uma_tentativa(env):
    reg(env["prio"], "loja", "1-2-listar", "iniciada")
    for _ in range(3):
        _, last = reg(env["prio"], "loja", "1-2-listar", "falhou", "--motivo", "dotnet test falha")
    assert last["limite_atingido"] is True and "bloqueada --causa tecnica" in last["proximo"]
    set_status(env["prio"], "loja", "1-2-listar", "blocked")
    historico(env["prio"], "loja", "1-2-listar", "| 02/11/2026 | in-progress → blocked | execucao-recorrente | x |")
    code, out = reg(env["prio"], "loja", "1-2-listar", "bloqueada", "--causa", "tecnica", "--motivo", "falhou 3 vezes")
    assert code == 0 and out["bloqueio"]["voltar_para"] == "in-progress"
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque"
    assert any("nada mudou" in a["motivo"] for a in out["atencao"] if a["id"] == "1-2-listar")
    # uma pessoa anota a correção na story: a assinatura muda e a story volta com mais uma tentativa
    path = story_file(env["prio"], "loja", "1-2-listar")
    path.write_text(path.read_text(encoding="utf-8").replace("# story", "# story\nCorrigido o teste.\n"),
                    encoding="utf-8")
    assert scan(env)["escolhida"]["acao"] == "desbloquear"
    _, done = reg(env["prio"], "loja", "1-2-listar", "desbloqueada")
    assert done["tentativas"] == 2 and done["voltar_para"] == "in-progress"
    set_status(env["prio"], "loja", "1-2-listar", "in-progress")
    escolhida = scan(env)["escolhida"]
    assert escolhida["retomada"] is True and escolhida["tentativas"] == 2


def test_bloqueio_de_decisao_nunca_volta_sozinho(env):
    bloquear(env, "1-2-listar")   # sem --causa = decisão
    path = story_file(env["prio"], "loja", "1-2-listar")
    path.write_text(path.read_text(encoding="utf-8") + "mudou\n", encoding="utf-8")
    out = scan(env)
    assert out["escolhida"]["projeto"] == "estoque"
    assert any("precisa de decisão" in a["motivo"] for a in out["atencao"] if a["id"] == "1-2-listar")
    code, err = reg(env["prio"], "loja", "1-3-editar", "desbloqueada")
    assert code == 1 and "uma pessoa" in err


def test_bloqueio_de_pessoa_fica_na_atencao(env, tmp_path):
    set_status(env["prio"], "loja", "1-2-listar", "blocked")
    out = scan(env)
    assert any("sem bloqueio automático" in a["motivo"] for a in out["atencao"] if a["id"] == "1-2-listar")
    # bloqueio automático, mas uma pessoa mexeu depois: o Histórico manda
    tmp_path.joinpath("ok").mkdir()
    bloquear(env, "1-3-editar", "--causa", "ambiente", "--verificar", f"caminho:{tmp_path / 'ok'}", por="Ana")
    puladas = {p["id"]: p["motivo"] for p in projeto_loja(scan(env))["puladas"]}
    assert "mudança de uma pessoa" in puladas["1-3-editar"]


def test_lock_renovar(env):
    _, out = run("lock", "renovar", "--config", str(env["config"]))
    assert out["renovado"] is False
    run("lock", "adquirir", "--config", str(env["config"]), "--expira-min", "1")
    _, out = run("lock", "renovar", "--config", str(env["config"]), "--expira-min", "60")
    assert out["renovado"] is True
    expira = datetime.fromisoformat(out["lock"]["expira_em"])
    assert expira > datetime.now().astimezone() + timedelta(minutes=50)
    assert scan(env)["espera_sugerida_s"] == 600


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t", *args],
                            capture_output=True, text=True, encoding="utf-8", check=True)
    return result.stdout.strip()


def test_worktree_da_story(tmp_path):
    repo = tmp_path / "api"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    (repo / "a.txt").write_text("a", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "inicial")
    (repo / "a.txt").write_text("alteração de outra story", encoding="utf-8")   # checkout principal sujo
    code, out = run("worktree", str(repo), "--id", "1-2-listar")
    assert code == 0 and out["criado"] is True and out["modo"] == "worktree" and out["base"] == "main"
    wt = Path(out["caminho"])
    assert wt == (tmp_path / "api.worktrees" / "1-2-listar").resolve() and (wt / "a.txt").read_text() == "a"
    assert git(wt, "branch", "--show-current") == "feat/1-2-listar"
    _, again = run("worktree", str(repo), "--id", "1-2-listar")
    assert again["criado"] is False and Path(again["caminho"]) == wt
    # story começada no checkout principal (antes das worktrees): usa o checkout
    git(repo, "stash", "-q")
    git(repo, "switch", "-q", "-c", "feat/1-3-editar")
    _, main = run("worktree", str(repo), "--id", "1-3-editar")
    assert main["modo"] == "checkout" and Path(main["caminho"]) == repo.resolve()
    code, err = run("worktree", str(tmp_path / "nao-existe"), "--id", "x")
    assert code == 1 and "não encontrado" in err


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
