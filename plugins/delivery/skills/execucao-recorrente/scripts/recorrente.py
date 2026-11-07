#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Apoio das skills execucao-recorrente (perfil execucao: o agente de entrega, que cria, implementa, revisa e
desbloqueia stories) e criacao-story-recorrente (perfil criacao: só create-story): lê o arquivo de configuração
(repositórios prioritários e sem prioridade), monta a fila da próxima tarefa possível, controla a trava global
do perfil (uma tarefa por vez), registra o resultado de cada execução e prepara a worktree da story.
Imprime JSON; em erro, 'error: <msg>' e código 1.

Uso (de qualquer pasta; --perfil vem antes do comando, padrão execucao):
  uv run scripts/recorrente.py [--perfil execucao|criacao] config [--config ARQ]       # mostra/valida
  uv run scripts/recorrente.py [--perfil ...] init-config [--config ARQ]               # cria o modelo
  uv run scripts/recorrente.py [--perfil ...] scan [--config ARQ]                      # fila em ordem
  uv run scripts/recorrente.py [--perfil ...] lock adquirir|renovar|liberar [--config ARQ] [--expira-min 90] [--dono "..."]
  uv run scripts/recorrente.py [--perfil ...] registrar {workspace} --projeto loja --id 1-2-listar-produtos \\
      --acao dev-story --resultado iniciada|concluida|falhou|bloqueada|pulada|aguardando|desbloqueada \\
      [--motivo "..."] [--causa ambiente|tecnica|decisao] [--verificar caminho:D:\\x] [--repo D:\\repos\\api]
  uv run scripts/recorrente.py worktree {repositório} --id 1-2-listar-produtos [--base main]

Configuração: --config, senão a variável do perfil (EXECUCAO_RECORRENTE_CONFIG / CRIACAO_STORY_RECORRENTE_CONFIG),
senão ~/.claude/{skill}.toml. A trava global fica ao lado dela ({nome}.lock.json). Estado e log de cada
workspace ficam em {workspace}/_sdd/{skill}/ (o create-story sempre em criacao-story-recorrente/, nos dois perfis).
Regras na SKILL.md de cada skill.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timedelta
from pathlib import Path

import yaml

SKILLS_ROOT = Path(__file__).resolve().parents[2]   # plugins/delivery/skills
STATUS_FILE = Path("implementacao") / "sprint-status.yaml"
ACOES = ("dev-story", "story-review", "create-story")
RESULTADOS = ("iniciada", "concluida", "falhou", "bloqueada", "pulada", "aguardando", "desbloqueada")
CAUSAS = ("ambiente", "tecnica", "decisao")
VERIFICACOES = ("caminho", "comando")
ISOLAMENTOS = ("worktree", "checkout")
GRUPOS = (("prioritarios", "prioritario"), ("sem_prioridade", "sem-prioridade"))
PERFIS = {
    "execucao": {"skill": "execucao-recorrente", "env": "EXECUCAO_RECORRENTE_CONFIG",
                 "acoes": ("dev-story", "story-review", "create-story"), "titulo": "Execução recorrente"},
    "criacao": {"skill": "criacao-story-recorrente", "env": "CRIACAO_STORY_RECORRENTE_CONFIG",
                "acoes": ("create-story",), "titulo": "Criação recorrente de stories"},
}
PERFIL = PERFIS["execucao"]
# espera sugerida até a próxima rodada (segundos), para o /loop sem intervalo
ESPERA_COM_FILA, ESPERA_EM_ANDAMENTO, ESPERA_OCIOSA = 60, 600, 1800
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
# Minutos de validade da trava; precisa ser maior que a tarefa mais longa (a rodada a renova entre os passos).
lock_expira_min = 90
# Modo contínuo: tarefas seguidas numa mesma rodada antes de parar e agendar a próxima.
max_tarefas_por_rodada = 5
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


def perfil_da_acao(acao: str) -> dict:
    """O estado do create-story fica sempre na pasta da criacao-story-recorrente, para as duas skills o verem."""
    return PERFIS["criacao"] if acao == "create-story" else PERFIS["execucao"]


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
    max_tarefas = int(execucao.get("max_tarefas_por_rodada", 5))
    if max_tarefas < 1:
        raise RecError(f"{path}: execucao.max_tarefas_por_rodada precisa ser positivo")
    avisos = [f"chave desconhecida em [repositorios]: {k} (use prioritarios ou sem_prioridade)" for k in desconhecidas]
    repetidos = set(grupos["prioritarios"]) & set(grupos["sem_prioridade"])
    avisos += [f"{r} está nas duas listas; vale prioritarios" for r in sorted(repetidos)]
    grupos["sem_prioridade"] = [r for r in grupos["sem_prioridade"] if r not in repetidos]
    return {"path": str(path), "prioritarios": grupos["prioritarios"], "sem_prioridade": grupos["sem_prioridade"],
            "lock_expira_min": expira, "max_tarefas_por_rodada": max_tarefas, "avisos": avisos}


def project_config(project: Path, perfil: dict | None = None) -> dict:
    """Campos próprios da skill do perfil: padrão do customize.toml + override do projeto (o override substitui)."""
    perfil = perfil or PERFIL
    skill = perfil["skill"]
    base = dict(read_toml(SKILLS_ROOT / skill / "customize.toml").get("workflow", {}))
    override = read_toml(project / "_custom" / f"{skill}.toml").get("workflow", {})
    base.update(override)
    cfg = {"habilitado": bool(base.get("habilitado", True)), "max_tentativas": int(base.get("max_tentativas", 3)),
           "avisos": []}
    if perfil is PERFIS["criacao"]:
        deps = base.get("dependencias_em", ["review", "done"])
        cfg.update({"acoes": ["create-story"], "max_prontas": int(base.get("max_prontas", 2)),
                    "dependencias_em": [str(d) for d in deps] if isinstance(deps, list) else ["review", "done"],
                    "exige_confirmacao": bool(base.get("exige_confirmacao", False)), "commit_ao_concluir": False,
                    "isolamento": "checkout"})
        return cfg
    pedidas = base.get("acoes", ["dev-story", "story-review", "create-story"])
    if not isinstance(pedidas, list):
        pedidas = []
    cfg["acoes"] = [a for a in pedidas if a in perfil["acoes"]]
    cfg["avisos"] += [f"ação desconhecida em acoes: {a} (use {', '.join(perfil['acoes'])})"
                      for a in pedidas if a not in perfil["acoes"]]
    cfg["commit_ao_concluir"] = bool(base.get("commit_ao_concluir", False))
    isolamento = str(base.get("isolamento", "worktree"))
    if isolamento not in ISOLAMENTOS:
        cfg["avisos"].append(f"isolamento = {isolamento} inválido; usando worktree")
        isolamento = "worktree"
    cfg["isolamento"] = isolamento
    if "create-story" in cfg["acoes"]:
        # a criação usa os campos da criacao-story-recorrente do projeto (max_prontas, dependencias_em...)
        cfg["criacao"] = project_config(project, PERFIS["criacao"])
    return cfg


def docs_root(workspace: Path) -> Path:
    root = "docs"
    for name in ("config.toml", "config.user.toml"):
        paths = read_toml(workspace / "_sdd" / name).get("paths", {})
        if isinstance(paths, dict) and paths.get("docs_root"):
            root = str(paths["docs_root"])
    return workspace / root


def code_path(project: Path) -> str | None:
    """code_path do project-config.json, quando é um diretório local (projeto de um repositório)."""
    path = project / "project-config.json"
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8")).get("code_path")
    except (json.JSONDecodeError, AttributeError):
        return None
    return value if isinstance(value, str) and Path(value).expanduser().is_dir() else None


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


def state_dir(workspace: Path, perfil: dict | None = None) -> Path:
    return workspace / "_sdd" / (perfil or PERFIL)["skill"]


def load_estado(workspace: Path, perfil: dict | None = None) -> dict:
    path = state_dir(workspace, perfil) / "estado.json"
    if not path.is_file():
        return {"stories": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RecError(f"{path} corrompido: {exc}") from exc
    data.setdefault("stories", {})
    return data


def save_estado(workspace: Path, data: dict, perfil: dict | None = None) -> None:
    folder = state_dir(workspace, perfil)
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


def append_log(workspace: Path, now: datetime, row: list[str], perfil: dict | None = None) -> Path:
    perfil = perfil or PERFIL
    folder = state_dir(workspace, perfil) / "log"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{now:%Y-%m}.md"
    text = (path.read_text(encoding="utf-8") if path.is_file()
            else LOG_HEADER.format(titulo=perfil["titulo"], mes=f"{now:%m/%Y}"))
    cells = [c.replace("|", "\\|").replace("\n", " ").strip() for c in row]
    text += "| " + " | ".join(cells) + " |\n"
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------- git


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError as exc:
        raise RecError("git não encontrado no PATH") from exc
    if check and result.returncode != 0:
        raise RecError(f"git {' '.join(args)} em {repo}: {(result.stderr or result.stdout).strip()}")
    return result


def git_ref(repo: str, ref: str) -> str:
    try:
        result = git(Path(repo), "rev-parse", "--verify", "--quiet", ref, check=False)
    except RecError:
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def branch_principal(top: Path) -> str:
    head = git(top, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD", check=False)
    nomes = [head.stdout.strip().split("/", 1)[-1]] if head.returncode == 0 and head.stdout.strip() else []
    for nome in nomes + ["main", "master"]:
        if git(top, "show-ref", "--verify", "--quiet", f"refs/heads/{nome}", check=False).returncode == 0:
            return nome
    raise RecError(f"branch principal não encontrada em {top} (nem main nem master): passe --base")


def cmd_worktree(repo_raw: str, story_id: str, base: str | None) -> dict:
    """Pasta de trabalho da story: a worktree da branch feat/{id}, criada ao lado do repositório se não existir.
    Se a branch já está no checkout principal (story começada antes), usa o checkout. Nunca apaga nada."""
    repo = Path(repo_raw).expanduser()
    if not repo.is_dir():
        raise RecError(f"repositório não encontrado: {repo_raw}")
    top = Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    branch = f"feat/{story_id}"
    listing = git(top, "worktree", "list", "--porcelain").stdout
    for block in listing.strip().split("\n\n"):
        fields = dict(line.split(" ", 1) for line in block.splitlines() if " " in line)
        if fields.get("branch") == f"refs/heads/{branch}":
            path = Path(fields["worktree"]).resolve()
            return {"caminho": str(path), "repositorio": str(top), "branch": branch,
                    "modo": "checkout" if path == top else "worktree", "criado": False}
    dest = top.parent / f"{top.name}.worktrees" / story_id
    if dest.exists():
        raise RecError(f"{dest} já existe e não é a worktree de {branch}: confira à mão (nada foi alterado)")
    dest.parent.mkdir(parents=True, exist_ok=True)
    existe = git(top, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}", check=False).returncode == 0
    base_usada = None
    if existe:
        git(top, "worktree", "add", str(dest), branch)
    else:
        base_usada = base or branch_principal(top)
        git(top, "worktree", "add", "-b", branch, str(dest), base_usada)
    return {"caminho": str(dest), "repositorio": str(top), "branch": branch, "modo": "worktree", "criado": True,
            "base": base_usada}


# ---------------------------------------------------------------- leitura das stories


def story_path(project: Path, story: dict) -> Path | None:
    file = story.get("file")
    path = project / "implementacao" / file if file else None
    return path if path and path.is_file() else None


def story_frontmatter(project: Path, story: dict) -> dict:
    path = story_path(project, story)
    if path is None:
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


def ultima_transicao(path: Path | None) -> tuple[str, str] | None:
    """(de → para, por) da última linha do Histórico da story; None sem arquivo ou sem linhas."""
    if path is None:
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^## Histórico[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        return None
    rows = [line for line in match.group(1).splitlines() if line.strip().startswith("|")]
    rows = [r for r in rows if not re.match(r"^\|[\s\-|:]+\|?\s*$", r)]
    if len(rows) < 2:   # só o cabeçalho
        return None
    cells = [c.strip() for c in rows[-1].strip().strip("|").split("|")]
    if len(cells) < 3:
        return None
    transicao = re.sub(r"\s*(→|->)\s*", " → ", cells[1])
    return transicao, cells[2]


def assinatura(path: Path | None, repos: list[str], story_id: str) -> str:
    """Muda quando a story ou o código mudam: hash do arquivo da story + HEAD e feat/{id} de cada repositório."""
    digest = hashlib.sha1()
    if path is not None:
        digest.update(path.read_bytes())
    for repo in sorted(set(repos)):
        digest.update(repo.encode())
        digest.update(git_ref(repo, "HEAD").encode())
        digest.update(git_ref(repo, f"refs/heads/feat/{story_id}").encode())
    return digest.hexdigest()[:16]


def conferir(verificar: list[str]) -> list[str]:
    """Verificações de ambiente que ainda falham (vazia = tudo resolvido)."""
    falhas = []
    for item in verificar:
        tipo, _, alvo = item.partition(":")
        ok = Path(alvo).expanduser().exists() if tipo == "caminho" else shutil.which(alvo) is not None
        if not ok:
            falhas.append(item)
    return falhas


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


# ---------------------------------------------------------------- escolha da story


class Contexto:
    """Um projeto visto por um perfil: configuração, estado e a saída onde vão as stories puladas."""

    def __init__(self, workspace: Path, project: Path, prioridade: str, cfg: dict, perfil: dict, out: dict):
        self.workspace, self.project, self.prioridade, self.cfg, self.out = workspace, project, prioridade, cfg, out
        self.nome = project.name
        self.estado = load_estado(workspace, perfil)

    def reg(self, story_id: str) -> dict:
        return self.estado["stories"].get(f"{self.nome}/{story_id}", {})

    def item(self, epic_id: str, story_id: str, story: dict, acao: str, retomada: bool = False, **extra) -> dict:
        reg = self.reg(story_id)
        tentativas = reg.get("tentativas", 0) if reg.get("acao") == acao else 0
        base = {"workspace": str(self.workspace), "projeto": self.nome, "project_path": str(self.project),
                "prioridade": self.prioridade, "id": story_id, "epic": epic_id, "title": story.get("title"),
                "status": story.get("status"), "acao": acao, "file": story.get("file"),
                "repositories": story.get("repositories", []), "retomada": retomada, "tentativas": tentativas,
                "commit_ao_concluir": self.cfg["commit_ao_concluir"], "isolamento": self.cfg["isolamento"]}
        base.update(extra)
        return base

    def esgotada(self, story_id: str, acao: str) -> bool:
        reg = self.reg(story_id)
        return reg.get("acao") == acao and reg.get("tentativas", 0) >= self.cfg["max_tentativas"]

    def limite(self) -> str:
        return f"limite de {self.cfg['max_tentativas']} tentativas atingido"

    def pular(self, story_id: str | None, motivo: str, atencao: bool = False) -> None:
        self.out["puladas"].append({"id": story_id, "motivo": motivo})
        if atencao:
            self.out["atencao"].append({"projeto": self.nome, "id": story_id, "motivo": motivo})


def candidates(workspace: Path, project: Path, prioridade: str) -> dict:
    """Stories executáveis de um projeto: retomadas, desbloqueios, novas (review/ready-for-dev) e criação."""
    cfg = project_config(project)
    out = {"projeto": project.name, "path": str(project), "prioridade": prioridade, "config": cfg,
           "retomadas": [], "desbloqueios": [], "novas": [], "criacao": [], "puladas": [], "atencao": []}
    avisos = list(cfg["avisos"])
    if not cfg["habilitado"]:
        out["puladas"].append({"id": None, "motivo": f"{PERFIL['skill']} desligada no projeto (habilitado = false)"})
        return out
    try:
        data = yaml.safe_load((project / STATUS_FILE).read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        out["erro"] = f"sprint-status.yaml inválido: {exc}"
        return out
    epics = data.get("epics") or {}
    order = [(epic_id, story_id, story) for epic_id, epic in epics.items()
             if epic.get("status") not in ("dropped", "done")
             for story_id, story in (epic.get("stories") or {}).items()]
    status_of = {sid: s.get("status") for epic in epics.values() for sid, s in (epic.get("stories") or {}).items()}

    if PERFIL is PERFIS["criacao"]:
        ctx = Contexto(workspace, project, prioridade, cfg, PERFIL, out)
        retomadas, nova = _criacao(ctx, project, order, status_of)
        out["retomadas"] = retomadas
        out["novas"] = [nova] if nova else []
        return out

    ctx = Contexto(workspace, project, prioridade, cfg, PERFIL, out)
    ctx_cria = None
    if "create-story" in cfg["acoes"]:
        ccfg = dict(cfg["criacao"], commit_ao_concluir=False, isolamento="checkout")
        avisos += ccfg["avisos"]
        if ccfg["habilitado"]:
            ctx_cria = Contexto(workspace, project, prioridade, ccfg, PERFIS["criacao"], out)
        else:
            out["puladas"].append({"id": None, "motivo": "criação desligada no projeto "
                                   "(_custom/criacao-story-recorrente.toml: habilitado = false)"})
    _execucao(ctx, ctx_cria, project, order, status_of)
    if ctx_cria is not None:
        retomadas, nova = _criacao(ctx_cria, project, order, status_of)
        out["retomadas"] += retomadas
        out["criacao"] = [nova] if nova else []
    cfg["avisos"] = avisos
    return out


def _devolvida_pela_revisao(reg: dict, path: Path | None) -> bool:
    """Story em in-progress porque a story-review a devolveu com correções (tarefas R{n})."""
    if reg.get("acao") == "story-review" and reg.get("ultimo_resultado") == "concluida":
        return True
    ultima = ultima_transicao(path)
    return (reg.get("acao") == "dev-story" and reg.get("ultimo_resultado") == "concluida" and ultima is not None
            and ultima[0] == "review → in-progress" and "story-review" in ultima[1])


def _execucao(ctx: Contexto, ctx_cria: Contexto | None, project: Path, order, status_of) -> None:
    review, ready = [], []
    acoes = ctx.cfg["acoes"]
    for epic_id, story_id, story in order:
        st = story.get("status")
        reg = ctx.reg(story_id)
        if st == "in-progress":
            propria = reg.get("acao") == "dev-story" and reg.get("ultimo_resultado") in (
                "em-andamento", "falhou", "desbloqueada")
            devolvida = not propria and _devolvida_pela_revisao(reg, story_path(project, story))
            if not (propria or devolvida):
                ctx.pular(story_id, "in-progress sem ter sido iniciada pela execução recorrente "
                                    "(alguém pode estar trabalhando nela)")
            elif "dev-story" not in acoes:
                ctx.pular(story_id, "devolvida pela revisão, mas dev-story não está em acoes", atencao=True)
            elif ctx.esgotada(story_id, "dev-story"):
                ctx.pular(story_id, ctx.limite())
            else:
                ctx.out["retomadas"].append(ctx.item(epic_id, story_id, story, "dev-story", retomada=True,
                                                     correcoes_revisao=devolvida))
        elif st == "blocked":
            _avaliar_bloqueio(ctx, ctx_cria, project, epic_id, story_id, story)
        elif st == "review" and "story-review" in acoes:
            if ctx.esgotada(story_id, "story-review"):
                ctx.pular(story_id, ctx.limite())
            else:
                review.append(ctx.item(epic_id, story_id, story, "story-review"))
        elif st == "ready-for-dev" and "dev-story" in acoes:
            front = story_frontmatter(project, story)
            pendentes = [d for d in (front.get("depends_on") or []) if status_of.get(d) not in ("done", "review")]
            if front.get("checkpoint") is True:
                ctx.pular(story_id, "checkpoint: precisa de acompanhamento humano", atencao=True)
            elif pendentes:
                ctx.pular(story_id, "depende de " + ", ".join(pendentes))
            elif ctx.esgotada(story_id, "dev-story"):
                ctx.pular(story_id, ctx.limite())
            else:
                ready.append(ctx.item(epic_id, story_id, story, "dev-story"))
    # review primeiro: fecha trabalho e libera quem depende dela; depois a ordem de build
    ctx.out["novas"] = review + ready


def _avaliar_bloqueio(ctx: Contexto, ctx_cria: Contexto | None, project: Path, epic_id: str, story_id: str,
                      story: dict) -> None:
    """Story blocked: volta à fila só se foi bloqueada pela automação por causa de ambiente ou técnica e a causa
    mudou. Bloqueio de decisão ou feito por uma pessoa vai para a lista de atenção."""
    achados = [(c, c.reg(story_id)) for c in (ctx, ctx_cria) if c is not None]
    achados = [(c, r) for c, r in achados if r.get("ultimo_resultado") == "bloqueada" and r.get("bloqueio")]
    if not achados:
        ctx.pular(story_id, "blocked sem bloqueio automático registrado: precisa de uma pessoa", atencao=True)
        return
    dono, reg = max(achados, key=lambda cr: cr[1]["bloqueio"].get("desde", ""))
    bloqueio = reg["bloqueio"]
    path = story_path(project, story)
    ultima = ultima_transicao(path)
    if path is not None and (ultima is None or not ultima[0].endswith("→ blocked") or "recorrente" not in ultima[1]):
        ctx.pular(story_id, "blocked: o Histórico mostra mudança de uma pessoa depois do bloqueio automático",
                  atencao=True)
        return
    acao = reg.get("acao")
    causa = bloqueio.get("causa", "decisao")
    if acao not in ctx.cfg["acoes"]:
        ctx.pular(story_id, f"blocked ({causa}): {bloqueio.get('motivo')} — {acao} não está em acoes", atencao=True)
        return
    if causa == "decisao":
        ctx.pular(story_id, f"blocked, precisa de decisão: {bloqueio.get('motivo')}", atencao=True)
        return
    if causa == "ambiente" and bloqueio.get("verificar"):
        falhas = conferir(bloqueio["verificar"])
        if falhas:
            ctx.pular(story_id, f"blocked (ambiente), ainda falta: {', '.join(falhas)}", atencao=True)
            return
        condicao = "ambiente resolvido: " + ", ".join(bloqueio["verificar"])
    else:
        if assinatura(path, bloqueio.get("repos", []), story_id) == bloqueio.get("assinatura"):
            ctx.pular(story_id, f"blocked ({causa}), nada mudou na story nem no código desde o bloqueio: "
                                f"{bloqueio.get('motivo')}", atencao=True)
            return
        condicao = "story ou código mudou desde o bloqueio"
    ctx.out["desbloqueios"].append(dono.item(epic_id, story_id, story, "desbloquear", acao_origem=acao,
                                             causa=causa, voltar_para=bloqueio.get("voltar_para"),
                                             condicao=condicao, motivo_bloqueio=bloqueio.get("motivo")))


def _criacao(ctx: Contexto, project: Path, order, status_of) -> tuple[list[dict], dict | None]:
    """Uma story nova por projeto: a primeira do backlog, na ordem de build, com as dependências prontas."""
    meta = epic_meta(project)
    prontas = sum(1 for _e, _sid, s in order if s.get("status") == "ready-for-dev")
    ctx.out["prontas"] = prontas
    retomadas, nova = [], None
    for epic_id, story_id, story in order:
        if story.get("status") != "backlog":
            continue
        reg = ctx.reg(story_id)
        criando = reg.get("acao") == "create-story"
        if criando and reg.get("ultimo_resultado") == "em-andamento":
            if ctx.esgotada(story_id, "create-story"):
                ctx.pular(story_id, ctx.limite())
            else:
                retomadas.append(ctx.item(epic_id, story_id, story, "create-story", retomada=True))
            continue
        if criando and reg.get("ultimo_resultado") == "aguardando":
            ctx.pular(story_id, "arquivo da story pronto, aguardando confirmação de uma pessoa para ready-for-dev",
                      atencao=True)
            continue
        if nova is not None:
            continue
        pendentes = [d for d in (meta.get(story_id, {}).get("depends_on") or [])
                     if status_of.get(d) not in ctx.cfg["dependencias_em"]]
        if pendentes:
            ctx.pular(story_id, "depende de " + ", ".join(f"{d} ({status_of.get(d, 'inexistente')})"
                                                          for d in pendentes))
        elif ctx.esgotada(story_id, "create-story"):
            ctx.pular(story_id, ctx.limite())
        else:
            nova = ctx.item(epic_id, story_id, story, "create-story")
    if retomadas:
        return retomadas, None
    if prontas >= ctx.cfg["max_prontas"]:
        ctx.pular(None, f"já há {prontas} stories ready-for-dev (limite max_prontas = {ctx.cfg['max_prontas']})")
        return [], None
    return [], nova


def scan(cfg: dict, lock: dict) -> dict:
    now = agora()
    em_andamento = lock_ativo(lock, now)
    result = {"perfil": PERFIL["skill"], "agora": now.isoformat(), "config": cfg["path"],
              "em_andamento": em_andamento, "lock": lock, "max_tarefas_por_rodada": cfg["max_tarefas_por_rodada"],
              "grupos": [], "fila": [], "atencao": [], "erros": [], "avisos": list(cfg["avisos"])}
    retomadas: list[dict] = []
    por_grupo: dict[str, list[dict]] = {}
    vistos: set[Path] = set()
    for key, nome in GRUPOS:
        grupo = {"prioridade": nome, "repositorios": []}
        desbloqueios, novas, criacao = [], [], []
        for raw in cfg[key]:
            entry = {"caminho": raw, "projetos": []}
            grupo["repositorios"].append(entry)
            try:
                workspace, project = resolve_dir(raw)
                projects = [project] if project is not None else projects_of(workspace)
                # só entram projetos com quadro: sem sprint-status.yaml não há stories para executar
                projects = [p for p in projects if (p / STATUS_FILE).is_file()]
                entry["workspace"] = str(workspace)
                if not projects:
                    entry["nota"] = ("nenhum projeto com implementacao/sprint-status.yaml "
                                     "(gere o quadro com plan-epics e sprint-planning)")
                for proj in projects:
                    if proj in vistos:
                        continue
                    vistos.add(proj)
                    info = candidates(workspace, proj, nome)
                    entry["projetos"].append(info)
                    result["avisos"] += [f"{info['projeto']}: {a}" for a in info["config"]["avisos"]]
                    result["atencao"] += info["atencao"]
                    retomadas.extend(info["retomadas"])
                    desbloqueios.extend(info["desbloqueios"])
                    novas.extend(info["novas"])
                    criacao.extend(info["criacao"])
            except RecError as exc:
                entry["erro"] = str(exc)
                result["erros"].append(str(exc))
        # dentro do grupo: desbloquear (rápido, devolve a story à fila) → revisar e implementar → criar
        por_grupo[nome] = desbloqueios + novas + criacao
        result["grupos"].append(grupo)
    # 1) retomar o que a automação começou e não terminou; 2) prioritários; 3) sem prioridade
    result["fila"] = retomadas + por_grupo["prioritario"] + por_grupo["sem-prioridade"]
    if em_andamento:
        result["escolhida"] = None
        result["motivo"] = f"tarefa em andamento desde {lock.get('desde')} ({lock.get('dono')}): nada a iniciar"
        result["espera_sugerida_s"] = ESPERA_EM_ANDAMENTO
    elif result["fila"]:
        escolhida = result["escolhida"] = result["fila"][0]
        if escolhida["retomada"]:
            result["motivo"] = ("retomar correções da revisão" if escolhida.get("correcoes_revisao")
                                else "retomar tarefa interrompida")
        elif escolhida["acao"] == "desbloquear":
            result["motivo"] = f"desbloquear ({escolhida['causa']}, {escolhida['prioridade']})"
        else:
            result["motivo"] = f"nova tarefa ({escolhida['prioridade']})"
        result["espera_sugerida_s"] = ESPERA_COM_FILA
    else:
        result["escolhida"] = None
        result["motivo"] = "sem tarefas nos repositórios prioritários nem nos sem prioridade"
        result["espera_sugerida_s"] = ESPERA_OCIOSA
    return result


# ---------------------------------------------------------------- comandos de escrita


def cmd_lock(path: Path, acao: str, expira_min: int, dono: str) -> dict:
    now = agora()
    lock = read_lock(path)
    if acao == "liberar":
        write_lock(path, {"estado": "livre", "liberado_em": now.isoformat(), "anterior": lock.get("dono")})
        return {"liberado": True, "lock_file": str(path)}
    if acao == "renovar":
        if not lock_ativo(lock, now):
            return {"renovado": False, "lock": lock, "motivo": "a trava não está ativa (expirou ou foi liberada)"}
        lock.update({"expira_em": (now + timedelta(minutes=expira_min)).isoformat(), "renovado_em": now.isoformat()})
        write_lock(path, lock)
        return {"renovado": True, "lock": lock, "lock_file": str(path)}
    if lock_ativo(lock, now):
        return {"adquirido": False, "lock": lock, "motivo": "outra execução está em andamento"}
    novo = {"estado": "ativo", "desde": now.isoformat(), "expira_em": (now + timedelta(minutes=expira_min)).isoformat(),
            "dono": dono}
    write_lock(path, novo)
    return {"adquirido": True, "lock": novo, "lock_file": str(path), "assumiu_expirado": lock.get("estado") == "ativo"}


def _voltar_para(acao: str, reg: dict) -> str:
    if acao == "create-story":
        return "backlog"
    if acao == "story-review":
        return "review"
    return "in-progress" if reg.get("iniciada_em") else "ready-for-dev"


def _story_file(project: Path, story_id: str) -> Path | None:
    try:
        data = yaml.safe_load((project / STATUS_FILE).read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return None
    for epic in (data.get("epics") or {}).values():
        story = (epic.get("stories") or {}).get(story_id)
        if story:
            return story_path(project, story)
    return None


def cmd_registrar(workspace: Path, projeto: str, story_id: str, acao: str, resultado: str, motivo: str,
                  causa: str | None = None, verificar: list[str] | None = None, repos: list[str] | None = None,
                  voltar_para: str | None = None) -> dict:
    if acao not in PERFIL["acoes"]:
        raise RecError(f"a ação {acao} não pertence à skill {PERFIL['skill']} (use {', '.join(PERFIL['acoes'])})")
    perfil = perfil_da_acao(acao)
    now = agora()
    project = docs_root(workspace) / projeto
    cfg = project_config(project, perfil) if project.is_dir() else {"max_tentativas": 3}
    estado = load_estado(workspace, perfil)
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
        save_estado(workspace, estado, perfil)
        log = append_log(workspace, now, [f"{now:%d/%m/%Y %H:%M}", projeto, story_id, acao, resultado, "",
                                          motivo or "—"], perfil)
        return {"registrado": True, "repetida": False, "tentativas": tentativas,
                "max_tentativas": cfg["max_tentativas"], "limite_atingido": False, "log": str(log)}
    if resultado == "desbloqueada" and not (reg.get("acao") == acao and reg.get("bloqueio")):
        raise RecError(f"{key} não tem bloqueio automático registrado para {acao}: só uma pessoa a desbloqueia")
    reg.pop("pulada", None)
    if reg.get("acao") != acao:
        reg = {"acao": acao, "tentativas": 0, "historico": reg.get("historico", [])}
    extra: dict = {}
    if resultado == "iniciada":
        reg["ultimo_resultado"] = "em-andamento"
        reg["iniciada_em"] = now.isoformat()
    elif resultado == "falhou":
        reg["tentativas"] = reg.get("tentativas", 0) + 1
        reg["ultimo_resultado"] = "falhou"
    elif resultado == "bloqueada":
        causa = causa or "decisao"   # sem causa, nunca desbloqueia sozinha
        verificar = verificar or []
        if causa == "ambiente" and not verificar:
            raise RecError("causa ambiente precisa de --verificar (caminho:{pasta} ou comando:{executável}) para "
                           "a automação saber quando foi resolvido; sem isso, use --causa tecnica")
        invalidas = [v for v in verificar if v.partition(":")[0] not in VERIFICACOES or not v.partition(":")[2]]
        if invalidas:
            raise RecError(f"--verificar inválido: {', '.join(invalidas)} "
                           "(use caminho:{pasta} ou comando:{executável})")
        todos_repos = list(dict.fromkeys([*(repos or []), *([code_path(project)] if code_path(project) else [])]))
        reg["ultimo_resultado"] = "bloqueada"
        reg["bloqueio"] = {"causa": causa, "motivo": motivo, "desde": now.isoformat(),
                           "voltar_para": voltar_para or _voltar_para(acao, reg), "verificar": verificar,
                           "repos": todos_repos,
                           "assinatura": assinatura(_story_file(project, story_id), todos_repos, story_id)}
        extra["bloqueio"] = reg["bloqueio"]
    elif resultado == "desbloqueada":
        bloqueio = reg.pop("bloqueio")
        # ambiente resolvido recomeça as tentativas; falha técnica ganha só mais uma
        reg["tentativas"] = 0 if bloqueio.get("causa") == "ambiente" else min(
            reg.get("tentativas", 0), max(cfg["max_tentativas"] - 1, 0))
        reg["ultimo_resultado"] = "desbloqueada"
        extra["voltar_para"] = bloqueio.get("voltar_para")
    elif resultado in ("concluida", "aguardando"):
        reg["ultimo_resultado"] = resultado
    if resultado != "bloqueada":
        reg.pop("bloqueio", None)
    reg["ultima_execucao"] = now.isoformat()
    reg["motivo"] = motivo
    reg.setdefault("historico", []).append({"em": now.isoformat(), "resultado": resultado, "motivo": motivo})
    reg["historico"] = reg["historico"][-20:]
    estado["stories"][key] = reg
    save_estado(workspace, estado, perfil)
    tentativas = reg.get("tentativas", 0)
    tentativa_txt = f"{tentativas}/{cfg['max_tentativas']}" if resultado == "falhou" else ""
    texto = f"{motivo or '—'} ({causa})" if resultado == "bloqueada" else (motivo or "—")
    log = append_log(workspace, now, [f"{now:%d/%m/%Y %H:%M}", projeto, story_id, acao, resultado, tentativa_txt,
                                      texto], perfil)
    limite = resultado == "falhou" and tentativas >= cfg["max_tentativas"]
    out = {"registrado": True, "tentativas": tentativas, "max_tentativas": cfg["max_tentativas"],
           "limite_atingido": limite, "log": str(log), **extra}
    if limite:
        out["proximo"] = ("status.py set blocked com a linha no Histórico e, por último, registrar "
                          "--resultado bloqueada --causa tecnica")
    return out


def main() -> None:
    global PERFIL
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--perfil", choices=tuple(PERFIS), default="execucao",
                        help="execucao (agente de entrega) ou criacao (create-story)")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, text in (("config", "mostra e valida a configuração"),
                       ("init-config", "cria o arquivo de configuração modelo (nunca sobrescreve)"),
                       ("scan", "fila de stories na ordem de execução")):
        p = sub.add_parser(name, help=text)
        p.add_argument("--config")
    lockp = sub.add_parser("lock", help="adquire, renova ou libera a trava global (uma tarefa por vez)")
    lockp.add_argument("acao", choices=("adquirir", "renovar", "liberar"))
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
    regp.add_argument("--causa", choices=CAUSAS, help="bloqueada: ambiente | tecnica | decisao (padrão)")
    regp.add_argument("--verificar", action="append", default=[],
                      help="bloqueada por ambiente: caminho:{pasta} ou comando:{executável} (repetível)")
    regp.add_argument("--repo", action="append", default=[], help="bloqueada: repositório de código da story")
    regp.add_argument("--voltar-para", help="bloqueada: estado ao desbloquear (padrão pela ação)")
    wtp = sub.add_parser("worktree", help="pasta de trabalho da story (worktree da branch feat/{id})")
    wtp.add_argument("repositorio")
    wtp.add_argument("--id", required=True)
    wtp.add_argument("--base", help="branch de origem quando feat/{id} não existe (padrão: a principal)")
    args = parser.parse_args()
    PERFIL = PERFIS[args.perfil]
    try:
        if args.command == "registrar":
            workspace, _project = resolve_dir(args.workspace)
            emit(cmd_registrar(workspace, args.projeto, args.id, args.acao, args.resultado, args.motivo,
                               args.causa, args.verificar, args.repo, args.voltar_para))
            return
        if args.command == "worktree":
            emit(cmd_worktree(args.repositorio, args.id, args.base))
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
