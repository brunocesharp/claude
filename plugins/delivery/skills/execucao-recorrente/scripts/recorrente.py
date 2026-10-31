#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Apoio das skills execucao-recorrente (perfil execucao: dev-story/story-review) e criacao-story-recorrente
(perfil criacao: create-story): lê o arquivo de configuração (repositórios prioritários e sem prioridade),
acha a próxima story, controla a trava global do perfil (uma tarefa por vez) e registra o resultado de cada
execução. Imprime JSON; em erro, 'error: <msg>' e código 1.

Uso (de qualquer pasta; --perfil vem antes do comando, padrão execucao):
  uv run scripts/recorrente.py [--perfil execucao|criacao] config [--config ARQ]       # mostra/valida
  uv run scripts/recorrente.py [--perfil ...] init-config [--config ARQ]               # cria o modelo
  uv run scripts/recorrente.py [--perfil ...] scan [--config ARQ]                      # fila em ordem
  uv run scripts/recorrente.py [--perfil ...] lock adquirir|liberar [--config ARQ] [--expira-min 90] [--dono "..."]
  uv run scripts/recorrente.py [--perfil ...] registrar {workspace} --projeto loja --id 1-2-listar-produtos \\
      --acao dev-story --resultado iniciada|concluida|falhou|bloqueada|pulada|aguardando [--motivo "..."]

Configuração: --config, senão a variável do perfil (EXECUCAO_RECORRENTE_CONFIG / CRIACAO_STORY_RECORRENTE_CONFIG),
senão ~/.claude/{skill}.toml. A trava global fica ao lado dela ({nome}.lock.json). Estado e log de cada
workspace ficam em {workspace}/_sdd/{skill}/. Regras na SKILL.md de cada skill.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tomllib
from datetime import datetime, timedelta
from pathlib import Path

import yaml

SKILLS_ROOT = Path(__file__).resolve().parents[2]   # plugins/delivery/skills
STATUS_FILE = Path("implementacao") / "sprint-status.yaml"
ACOES = ("dev-story", "story-review", "create-story")
RESULTADOS = ("iniciada", "concluida", "falhou", "bloqueada", "pulada", "aguardando")
GRUPOS = (("prioritarios", "prioritario"), ("sem_prioridade", "sem-prioridade"))
PERFIS = {
    "execucao": {"skill": "execucao-recorrente", "env": "EXECUCAO_RECORRENTE_CONFIG",
                 "acoes": ("dev-story", "story-review"), "titulo": "Execução recorrente"},
    "criacao": {"skill": "criacao-story-recorrente", "env": "CRIACAO_STORY_RECORRENTE_CONFIG",
                "acoes": ("create-story",), "titulo": "Criação recorrente de stories"},
}
PERFIL = PERFIS["execucao"]
LOG_HEADER = ("# {titulo} — log de {mes}\n\n"
              "| Data | Projeto | Story | Ação | Resultado | Tentativa | Motivo |\n"
              "|------|---------|-------|------|-----------|-----------|--------|\n")
CONFIG_TEMPLATE = """# Configuração da skill {skill}.
# Cada caminho pode ser a raiz de um workspace (tem _sdd/ ou docs/), a pasta de um projeto
# (docs/{{projeto}}) ou qualquer pasta dentro de um workspace. Use aspas simples para caminhos do Windows.
#
# Ordem: 1) retoma a tarefa que esta skill começou e não terminou;
# 2) a próxima tarefa dos repositórios prioritários, na ordem da lista;
# 3) só se nenhum prioritário tiver tarefa, a próxima dos repositórios sem prioridade.
# Uma tarefa por vez: enquanto uma rodada está em andamento, as outras não iniciam nada.

[repositorios]
prioritarios = [
  # 'D:\\repos\\docs-loja',
]
sem_prioridade = [
  # 'D:\\repos\\docs-estoque',
]

[execucao]
# Minutos de validade da trava; precisa ser maior que a tarefa mais longa.
lock_expira_min = 90
"""


class RecError(Exception):
    """Erro esperado: o script imprime 'error: <mensagem>' e sai com código 1."""


def emit(value: object) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(value, ensure_ascii=False, indent=2))


def fail(message: str) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"error: {message}")
    sys.exit(1)


def agora() -> datetime:
    return datetime.now().astimezone().replace(microsecond=0)


# ---------------------------------------------------------------- arquivos de configuração


def read_toml(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise RecError(f"{path} não é um TOML válido: {exc}") from exc


def config_path(arg: str | None) -> Path:
    raw = arg or os.environ.get(PERFIL["env"]) or f"~/.claude/{PERFIL['skill']}.toml"
    return Path(raw).expanduser()


def load_config(path: Path) -> dict:
    """Configuração da skill: listas de repositórios por prioridade e opções da execução."""
    if not path.is_file():
        raise RecError(f"arquivo de configuração não encontrado: {path} (crie com init-config)")
    data = read_toml(path)
    repos = data.get("repositorios", {})
    if not isinstance(repos, dict):
        raise RecError(f"{path}: [repositorios] precisa ser uma tabela")
    grupos = {}
    for key, _nome in GRUPOS:
        value = repos.get(key, [])
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            raise RecError(f"{path}: repositorios.{key} precisa ser uma lista de caminhos")
        grupos[key] = [v for v in value if v.strip()]
    desconhecidas = sorted(set(repos) - {k for k, _ in GRUPOS})
    execucao = data.get("execucao", {})
    expira = int(execucao.get("lock_expira_min", 90))
    if expira < 1:
        raise RecError(f"{path}: execucao.lock_expira_min precisa ser positivo")
    avisos = [f"chave desconhecida em [repositorios]: {k} (use prioritarios ou sem_prioridade)" for k in desconhecidas]
    repetidos = set(grupos["prioritarios"]) & set(grupos["sem_prioridade"])
    avisos += [f"{r} está nas duas listas; vale prioritarios" for r in sorted(repetidos)]
    grupos["sem_prioridade"] = [r for r in grupos["sem_prioridade"] if r not in repetidos]
    return {"path": str(path), "prioritarios": grupos["prioritarios"], "sem_prioridade": grupos["sem_prioridade"],
            "lock_expira_min": expira, "avisos": avisos}


def project_config(project: Path) -> dict:
    """Campos próprios da skill do perfil: padrão do customize.toml + override do projeto (o override substitui)."""
    skill = PERFIL["skill"]
    base = dict(read_toml(SKILLS_ROOT / skill / "customize.toml").get("workflow", {}))
    override = read_toml(project / "_custom" / f"{skill}.toml").get("workflow", {})
    base.update(override)
    cfg = {"habilitado": bool(base.get("habilitado", True)), "max_tentativas": int(base.get("max_tentativas", 3)),
           "avisos": []}
    if PERFIL is PERFIS["criacao"]:
        deps = base.get("dependencias_em", ["review", "done"])
        cfg.update({"acoes": ["create-story"], "max_prontas": int(base.get("max_prontas", 2)),
                    "dependencias_em": [str(d) for d in deps] if isinstance(deps, list) else ["review", "done"],
                    "exige_confirmacao": bool(base.get("exige_confirmacao", False)), "commit_ao_concluir": False})
        return cfg
    pedidas = base.get("acoes", ["dev-story"])
    cfg["acoes"] = [a for a in pedidas if a in PERFIL["acoes"]]
    if "create-story" in pedidas:
        cfg["avisos"].append("acoes = create-story não vale mais na execucao-recorrente: use a skill "
                             "criacao-story-recorrente")
    cfg["commit_ao_concluir"] = bool(base.get("commit_ao_concluir", False))
    return cfg


def docs_root(workspace: Path) -> Path:
    root = "docs"
    for name in ("config.toml", "config.user.toml"):
        paths = read_toml(workspace / "_sdd" / name).get("paths", {})
        if isinstance(paths, dict) and paths.get("docs_root"):
            root = str(paths["docs_root"])
    return workspace / root


# ---------------------------------------------------------------- diretórios → workspaces e projetos


def resolve_dir(raw: str) -> tuple[Path, Path | None]:
    """Devolve (workspace, projeto) — projeto None quando o diretório é o workspace inteiro."""
    path = Path(raw).expanduser()
    if not path.is_dir():
        raise RecError(f"diretório não encontrado: {raw}")
    path = path.resolve()
    if (path / STATUS_FILE).is_file() or (path / "project.md").is_file():
        for folder in path.parents:
            if (folder / "_sdd").is_dir():
                return folder, path
        return path.parent.parent, path
    if (path / "_sdd").is_dir() or (path / "docs").is_dir():
        return path, None
    for folder in path.parents:
        if (folder / "_sdd").is_dir():
            return folder, None
    raise RecError(f"{raw} não é um workspace (sem _sdd/ nem docs/) nem a pasta de um projeto")


def projects_of(workspace: Path) -> list[Path]:
    root = docs_root(workspace)
    if not root.is_dir():
        return []
    return sorted(p.parent.parent for p in root.glob(f"*/{STATUS_FILE.as_posix()}"))


# ---------------------------------------------------------------- estado, trava e log


def state_dir(workspace: Path) -> Path:
    return workspace / "_sdd" / PERFIL["skill"]


def load_estado(workspace: Path) -> dict:
    path = state_dir(workspace) / "estado.json"
    if not path.is_file():
        return {"stories": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RecError(f"{path} corrompido: {exc}") from exc
    data.setdefault("stories", {})
    return data


def save_estado(workspace: Path, data: dict) -> None:
    folder = state_dir(workspace)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "estado.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def lock_path(config: Path) -> Path:
    return config.with_name(config.stem + ".lock.json")


def read_lock(path: Path) -> dict:
    if not path.is_file():
        return {"estado": "livre"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"estado": "livre", "nota": "trava ilegível; tratada como livre"}


def lock_ativo(lock: dict, now: datetime) -> bool:
    if lock.get("estado") != "ativo":
        return False
    try:
        return datetime.fromisoformat(lock["expira_em"]) > now
    except (KeyError, ValueError):
        return False


def write_lock(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_log(workspace: Path, now: datetime, row: list[str]) -> Path:
    folder = state_dir(workspace) / "log"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{now:%Y-%m}.md"
    text = (path.read_text(encoding="utf-8") if path.is_file()
            else LOG_HEADER.format(titulo=PERFIL["titulo"], mes=f"{now:%m/%Y}"))
    cells = [c.replace("|", "\\|").replace("\n", " ").strip() for c in row]
    text += "| " + " | ".join(cells) + " |\n"
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------- escolha da story


def story_frontmatter(project: Path, story: dict) -> dict:
    file = story.get("file")
    if not file:
        return {}
    path = project / "implementacao" / file
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        data = yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def epic_meta(project: Path) -> dict[str, dict]:
    """depends_on/checkpoint de cada story, do frontmatter dos épicos (a story em backlog ainda não tem arquivo)."""
    meta: dict[str, dict] = {}
    for path in sorted((project / "implementacao" / "epicos").glob("epic-*.md")):
        text = path.read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        if not text.startswith("---") or end == -1:
            continue
        try:
            data = yaml.safe_load(text[3:end]) or {}
        except yaml.YAMLError:
            continue
        for story in data.get("stories") or []:
            if isinstance(story, dict) and story.get("id"):
                meta[str(story["id"])] = story
    return meta


def candidates(workspace: Path, project: Path, estado: dict, prioridade: str) -> dict:
    """Stories executáveis de um projeto: retomadas (começadas por esta skill e não terminadas) e novas."""
    cfg = project_config(project)
    nome = project.name
    out = {"projeto": nome, "path": str(project), "prioridade": prioridade, "config": cfg,
           "retomadas": [], "novas": [], "puladas": []}
    if not cfg["habilitado"]:
        out["puladas"].append({"id": None, "motivo": f"{PERFIL['skill']} desligada no projeto (habilitado = false)"})
        return out
    try:
        data = yaml.safe_load((project / STATUS_FILE).read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        out["erro"] = f"sprint-status.yaml inválido: {exc}"
        return out
    order = [(epic_id, story_id, story) for epic_id, epic in (data.get("epics") or {}).items()
             if epic.get("status") not in ("dropped", "done")
             for story_id, story in (epic.get("stories") or {}).items()]
    status_of = {sid: s.get("status") for epic in (data.get("epics") or {}).values()
                 for sid, s in (epic.get("stories") or {}).items()}

    def item(epic_id: str, story_id: str, story: dict, acao: str, retomada: bool = False) -> dict:
        reg = estado["stories"].get(f"{nome}/{story_id}", {})
        tentativas = reg.get("tentativas", 0) if reg.get("acao") == acao else 0
        return {"workspace": str(workspace), "projeto": nome, "project_path": str(project), "prioridade": prioridade,
                "id": story_id, "epic": epic_id, "title": story.get("title"), "status": story.get("status"),
                "acao": acao, "file": story.get("file"), "repositories": story.get("repositories", []),
                "retomada": retomada, "tentativas": tentativas, "commit_ao_concluir": cfg["commit_ao_concluir"]}

    def esgotada(story_id: str, acao: str) -> bool:
        reg = estado["stories"].get(f"{nome}/{story_id}", {})
        return reg.get("acao") == acao and reg.get("tentativas", 0) >= cfg["max_tentativas"]

    def pular(story_id: str | None, motivo: str) -> None:
        out["puladas"].append({"id": story_id, "motivo": motivo})

    limite = f"limite de {cfg['max_tentativas']} tentativas atingido"
    if PERFIL is PERFIS["criacao"]:
        _criacao(project, order, status_of, estado, nome, cfg, out, item, esgotada, pular, limite)
    else:
        _execucao(project, order, status_of, estado, nome, cfg, out, item, esgotada, pular, limite)
    return out


def _execucao(project, order, status_of, estado, nome, cfg, out, item, esgotada, pular, limite) -> None:
    buckets: dict[str, list[dict]] = {"review": [], "ready-for-dev": []}
    for epic_id, story_id, story in order:
        st = story.get("status")
        reg = estado["stories"].get(f"{nome}/{story_id}", {})
        if st == "in-progress":
            if reg.get("acao") != "dev-story" or reg.get("ultimo_resultado") not in ("em-andamento", "falhou"):
                pular(story_id, "in-progress sem ter sido iniciada pela execução recorrente "
                                "(alguém pode estar trabalhando nela)")
            elif esgotada(story_id, "dev-story"):
                pular(story_id, limite)
            else:
                out["retomadas"].append(item(epic_id, story_id, story, "dev-story", retomada=True))
        elif st == "review" and "story-review" in cfg["acoes"]:
            if esgotada(story_id, "story-review"):
                pular(story_id, limite)
            else:
                buckets["review"].append(item(epic_id, story_id, story, "story-review"))
        elif st == "ready-for-dev" and "dev-story" in cfg["acoes"]:
            front = story_frontmatter(project, story)
            pendentes = [d for d in (front.get("depends_on") or []) if status_of.get(d) not in ("done", "review")]
            if front.get("checkpoint") is True:
                pular(story_id, "checkpoint: precisa de acompanhamento humano")
            elif pendentes:
                pular(story_id, "depende de " + ", ".join(pendentes))
            elif esgotada(story_id, "dev-story"):
                pular(story_id, limite)
            else:
                buckets["ready-for-dev"].append(item(epic_id, story_id, story, "dev-story"))
    out["novas"] = buckets["review"] + buckets["ready-for-dev"]


def _criacao(project, order, status_of, estado, nome, cfg, out, item, esgotada, pular, limite) -> None:
    """Uma story nova por projeto: a primeira do backlog, na ordem de build, com as dependências prontas."""
    meta = epic_meta(project)
    prontas = sum(1 for _e, _sid, s in order if s.get("status") == "ready-for-dev")
    out["prontas"] = prontas
    nova = None
    for epic_id, story_id, story in order:
        if story.get("status") != "backlog":
            continue
        reg = estado["stories"].get(f"{nome}/{story_id}", {})
        criando = reg.get("acao") == "create-story"
        if criando and reg.get("ultimo_resultado") == "em-andamento":
            if esgotada(story_id, "create-story"):
                pular(story_id, limite)
            else:
                out["retomadas"].append(item(epic_id, story_id, story, "create-story", retomada=True))
            continue
        if criando and reg.get("ultimo_resultado") == "aguardando":
            pular(story_id, "arquivo da story pronto, aguardando confirmação de uma pessoa para ready-for-dev")
            continue
        if nova is not None:
            continue
        pendentes = [d for d in (meta.get(story_id, {}).get("depends_on") or [])
                     if status_of.get(d) not in cfg["dependencias_em"]]
        if pendentes:
            pular(story_id, "depende de " + ", ".join(f"{d} ({status_of.get(d, 'inexistente')})" for d in pendentes))
        elif esgotada(story_id, "create-story"):
            pular(story_id, limite)
        else:
            nova = item(epic_id, story_id, story, "create-story")
    if out["retomadas"]:
        return
    if prontas >= cfg["max_prontas"]:
        pular(None, f"já há {prontas} stories ready-for-dev (limite max_prontas = {cfg['max_prontas']})")
    elif nova is not None:
        out["novas"].append(nova)


def scan(cfg: dict, lock: dict) -> dict:
    now = agora()
    em_andamento = lock_ativo(lock, now)
    result = {"perfil": PERFIL["skill"], "agora": now.isoformat(), "config": cfg["path"],
              "em_andamento": em_andamento, "lock": lock, "grupos": [], "fila": [], "erros": [],
              "avisos": list(cfg["avisos"])}
    retomadas: list[dict] = []
    novas: dict[str, list[dict]] = {}
    vistos: set[Path] = set()
    for key, nome in GRUPOS:
        grupo = {"prioridade": nome, "repositorios": []}
        novas[nome] = []
        for raw in cfg[key]:
            entry = {"caminho": raw, "projetos": []}
            grupo["repositorios"].append(entry)
            try:
                workspace, project = resolve_dir(raw)
                estado = load_estado(workspace)
            except RecError as exc:
                entry["erro"] = str(exc)
                result["erros"].append(str(exc))
                continue
            entry["workspace"] = str(workspace)
            projects = [project] if project is not None else projects_of(workspace)
            # só entram projetos com quadro: sem sprint-status.yaml não há stories para executar
            projects = [p for p in projects if (p / STATUS_FILE).is_file()]
            if not projects:
                entry["nota"] = ("nenhum projeto com implementacao/sprint-status.yaml "
                                 "(gere o quadro com plan-epics e sprint-planning)")
            for proj in projects:
                if proj in vistos:
                    continue
                vistos.add(proj)
                info = candidates(workspace, proj, estado, nome)
                entry["projetos"].append(info)
                result["avisos"] += [f"{info['projeto']}: {a}" for a in info["config"]["avisos"]]
                retomadas.extend(info["retomadas"])
                novas[nome].extend(info["novas"])
        result["grupos"].append(grupo)
    # 1) retomar o que esta skill começou e não terminou; 2) prioritários; 3) sem prioridade
    result["fila"] = retomadas + novas["prioritario"] + novas["sem-prioridade"]
    if em_andamento:
        result["escolhida"] = None
        result["motivo"] = f"tarefa em andamento desde {lock.get('desde')} ({lock.get('dono')}): nada a iniciar"
    elif result["fila"]:
        result["escolhida"] = result["fila"][0]
        escolhida = result["escolhida"]
        result["motivo"] = ("retomar tarefa interrompida" if escolhida["retomada"]
                            else f"nova tarefa ({escolhida['prioridade']})")
    else:
        result["escolhida"] = None
        result["motivo"] = "sem tarefas nos repositórios prioritários nem nos sem prioridade"
    return result


# ---------------------------------------------------------------- comandos de escrita


def cmd_lock(path: Path, acao: str, expira_min: int, dono: str) -> dict:
    now = agora()
    lock = read_lock(path)
    if acao == "liberar":
        write_lock(path, {"estado": "livre", "liberado_em": now.isoformat(), "anterior": lock.get("dono")})
        return {"liberado": True, "lock_file": str(path)}
    if lock_ativo(lock, now):
        return {"adquirido": False, "lock": lock, "motivo": "outra execução está em andamento"}
    novo = {"estado": "ativo", "desde": now.isoformat(), "expira_em": (now + timedelta(minutes=expira_min)).isoformat(),
            "dono": dono}
    write_lock(path, novo)
    return {"adquirido": True, "lock": novo, "lock_file": str(path), "assumiu_expirado": lock.get("estado") == "ativo"}


def cmd_registrar(workspace: Path, projeto: str, story_id: str, acao: str, resultado: str, motivo: str) -> dict:
    if acao not in PERFIL["acoes"]:
        raise RecError(f"a ação {acao} não pertence à skill {PERFIL['skill']} (use {', '.join(PERFIL['acoes'])})")
    now = agora()
    project = docs_root(workspace) / projeto
    cfg = project_config(project) if project.is_dir() else {"max_tentativas": 3}
    estado = load_estado(workspace)
    key = f"{projeto}/{story_id}"
    reg = estado["stories"].get(key, {})
    if resultado == "pulada":
        # pulada não conta tentativa; só vai para o log quando o motivo muda (senão seria uma linha por rodada)
        anterior = reg.get("pulada", {})
        tentativas = reg.get("tentativas", 0) if reg.get("acao") == acao else 0
        if anterior.get("motivo") == motivo:
            return {"registrado": False, "repetida": True, "desde": anterior.get("desde"), "tentativas": tentativas,
                    "max_tentativas": cfg["max_tentativas"], "limite_atingido": False, "log": None}
        reg["pulada"] = {"motivo": motivo, "desde": now.isoformat()}
        estado["stories"][key] = reg
        save_estado(workspace, estado)
        log = append_log(workspace, now, [f"{now:%d/%m/%Y %H:%M}", projeto, story_id, acao, resultado, "",
                                          motivo or "—"])
        return {"registrado": True, "repetida": False, "tentativas": tentativas,
                "max_tentativas": cfg["max_tentativas"], "limite_atingido": False, "log": str(log)}
    reg.pop("pulada", None)
    if reg.get("acao") != acao:
        reg = {"acao": acao, "tentativas": 0, "historico": reg.get("historico", [])}
    if resultado == "iniciada":
        reg["ultimo_resultado"] = "em-andamento"
        reg["iniciada_em"] = now.isoformat()
    elif resultado == "falhou":
        reg["tentativas"] = reg.get("tentativas", 0) + 1
        reg["ultimo_resultado"] = "falhou"
    elif resultado in ("concluida", "bloqueada", "aguardando"):
        reg["ultimo_resultado"] = resultado
    reg["ultima_execucao"] = now.isoformat()
    reg["motivo"] = motivo
    reg.setdefault("historico", []).append({"em": now.isoformat(), "resultado": resultado, "motivo": motivo})
    reg["historico"] = reg["historico"][-20:]
    estado["stories"][key] = reg
    save_estado(workspace, estado)
    tentativas = reg.get("tentativas", 0)
    tentativa_txt = f"{tentativas}/{cfg['max_tentativas']}" if resultado == "falhou" else ""
    log = append_log(workspace, now, [f"{now:%d/%m/%Y %H:%M}", projeto, story_id, acao, resultado, tentativa_txt,
                                      motivo or "—"])
    return {"registrado": True, "tentativas": tentativas, "max_tentativas": cfg["max_tentativas"],
            "limite_atingido": resultado == "falhou" and tentativas >= cfg["max_tentativas"], "log": str(log)}


def main() -> None:
    global PERFIL
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--perfil", choices=tuple(PERFIS), default="execucao",
                        help="execucao (dev-story/story-review) ou criacao (create-story)")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, text in (("config", "mostra e valida a configuração"),
                       ("init-config", "cria o arquivo de configuração modelo (nunca sobrescreve)"),
                       ("scan", "fila de stories na ordem de execução")):
        p = sub.add_parser(name, help=text)
        p.add_argument("--config")
    lockp = sub.add_parser("lock", help="adquire ou libera a trava global (uma tarefa por vez)")
    lockp.add_argument("acao", choices=("adquirir", "liberar"))
    lockp.add_argument("--config")
    lockp.add_argument("--expira-min", type=int, help="padrão: execucao.lock_expira_min da configuração (90)")
    lockp.add_argument("--dono")
    regp = sub.add_parser("registrar", help="registra o resultado de uma execução no estado e no log do workspace")
    regp.add_argument("workspace")
    regp.add_argument("--projeto", required=True)
    regp.add_argument("--id", required=True)
    regp.add_argument("--acao", required=True, choices=ACOES)
    regp.add_argument("--resultado", required=True, choices=RESULTADOS)
    regp.add_argument("--motivo", default="")
    args = parser.parse_args()
    PERFIL = PERFIS[args.perfil]
    try:
        if args.command == "registrar":
            workspace, _project = resolve_dir(args.workspace)
            emit(cmd_registrar(workspace, args.projeto, args.id, args.acao, args.resultado, args.motivo))
            return
        path = config_path(args.config)
        if args.command == "init-config":
            if path.exists():
                emit({"criado": False, "config": str(path), "motivo": "já existe; nada foi alterado"})
                return
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(CONFIG_TEMPLATE.format(skill=PERFIL["skill"]), encoding="utf-8")
            emit({"criado": True, "config": str(path)})
            return
        if args.command == "lock":
            expira = args.expira_min
            if expira is None:
                expira = load_config(path)["lock_expira_min"] if path.is_file() else 90
            emit(cmd_lock(lock_path(path), args.acao, expira, args.dono or PERFIL["skill"]))
            return
        cfg = load_config(path)
        if args.command == "config":
            cfg["lock_file"] = str(lock_path(path))
            emit(cfg)
        else:
            emit(scan(cfg, read_lock(lock_path(path))))
    except RecError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
