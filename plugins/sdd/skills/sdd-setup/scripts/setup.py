#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Setup do workspace sdd. Cada chamada imprime um JSON; em erro imprime 'error: <msg>' e sai com 1.

Modos:
  --status                    Verifica e não grava nada.
  --list-config-questions     Perguntas ainda sem resposta: [{module, key, prompt, default, scope}].
  (sem modo)                  Cria/atualiza _sdd/: grava respostas (--answers), copia os scripts e a versão.
  --gitignore                 Acrescenta _sdd/*.user.toml ao .gitignore do workspace.

Opções comuns:
  --workspace-root <pasta>    Raiz do workspace (obrigatória).
  --modules sdd,spec-plan     Módulos instalados (padrão: todos os registros em modules/).
  --answers <arquivo.json>    {"chave": "valor"}; o arquivo é apagado depois de lido.
"""

from __future__ import annotations

import argparse
import getpass
import json
import shutil
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from sddlib import (
    SDD_DIR,
    TEAM_FILE,
    TEAM_HEADER,
    USER_FILE,
    USER_HEADER,
    VERSION_FILE,
    SddError,
    append_values,
    emit,
    fail,
    read_toml,
)

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
MODULES_DIR = SKILL_DIR / "modules"
SCOPES = ("team", "user")
GITIGNORE_LINE = "_sdd/*.user.toml"


@dataclass(frozen=True)
class Question:
    module: str
    key: str
    prompt: str
    default: str
    scope: str


@dataclass(frozen=True)
class Module:
    code: str
    plugin: str
    version: str
    skills: tuple[str, ...]
    questions: tuple[Question, ...]


def load_modules(selected: list[str] | None) -> list[Module]:
    modules: list[Module] = []
    for path in sorted(MODULES_DIR.glob("*.toml")):
        with path.open("rb") as handle:
            data = tomllib.load(handle).get("module")
        if not isinstance(data, dict):
            raise SddError(f"{path.name}: falta a tabela [module]")
        for field in ("code", "plugin", "version"):
            if not isinstance(data.get(field), str) or not data[field]:
                raise SddError(f"{path.name}: module.{field} deve ser texto não vazio")
        code = data["code"]
        questions = []
        for index, raw in enumerate(data.get("config_questions", [])):
            where = f"{path.name}: config_questions[{index}]"
            for field in ("key", "prompt", "default"):
                if not isinstance(raw.get(field), str):
                    raise SddError(f"{where}.{field} deve ser texto")
            scope = raw.get("scope", "team")
            if scope not in SCOPES:
                raise SddError(f'{where}.scope deve ser "team" ou "user"')
            questions.append(Question(code, raw["key"], raw["prompt"], raw["default"], scope))
        modules.append(Module(code, data["plugin"], data["version"], tuple(data.get("skills", [])), tuple(questions)))

    keys: dict[str, str] = {}
    for module in modules:
        for question in module.questions:
            if question.key in keys:
                raise SddError(f"chave {question.key} declarada em {keys[question.key]} e {module.code}")
            keys[question.key] = module.code

    if selected is None:
        return modules
    known = {module.code for module in modules}
    unknown = [code for code in selected if code not in known]
    if unknown:
        raise SddError(f"módulo desconhecido: {', '.join(unknown)} (conhecidos: {', '.join(sorted(known))})")
    return [module for module in modules if module.code in selected]


def expand_default(default: str, root: Path) -> str:
    try:
        os_user = getpass.getuser()
    except Exception:  # sem usuário no ambiente (ex.: container)
        os_user = ""
    return default.replace("{directory_name}", root.name).replace("{os_user}", os_user)


def config_file(root: Path, scope: str) -> Path:
    return root / SDD_DIR / (USER_FILE if scope == "user" else TEAM_FILE)


def pending_questions(root: Path, modules: list[Module]) -> list[Question]:
    answered = {scope: read_toml(config_file(root, scope)) for scope in SCOPES}
    return [q for m in modules for q in m.questions if q.key not in answered[q.scope]]


def runtime_scripts() -> list[Path]:
    """Scripts copiados para _sdd/scripts/. O setup.py fica de fora: depende de modules/ da skill."""
    return [path for path in sorted(SCRIPTS_DIR.glob("*.py")) if path.name != "setup.py"]


def scripts_state(root: Path) -> dict[str, str]:
    """Para cada script de runtime: missing, stale ou current na cópia em _sdd/scripts/."""
    target = root / SDD_DIR / "scripts"
    state = {}
    for source in runtime_scripts():
        copy = target / source.name
        if not copy.is_file():
            state[source.name] = "missing"
        elif copy.read_bytes() != source.read_bytes():
            state[source.name] = "stale"
        else:
            state[source.name] = "current"
    return state


def gitignore_state(root: Path) -> str:
    gitignore = root / ".gitignore"
    if not (root / ".git").exists() and not gitignore.is_file():
        return "not-git"
    if not gitignore.is_file():
        return "unprotected"
    lines = {line.strip() for line in gitignore.read_text(encoding="utf-8").splitlines()}
    protected = {GITIGNORE_LINE, "_sdd/config.user.toml", "*.user.toml", "_sdd/", "_sdd"}
    return "protected" if lines & protected else "unprotected"


def list_projects(root: Path, docs_root: str) -> list[dict[str, object]]:
    projects = []
    for config in sorted((root / docs_root).glob("*/project-config.json")):
        try:
            data = json.loads(config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
        projects.append({"slug": config.parent.name, "name": data.get("name", config.parent.name), "has_config": True})
    for project in sorted((root / docs_root).glob("*/project.md")):
        if not (project.parent / "project-config.json").is_file():
            projects.append({"slug": project.parent.name, "name": project.parent.name, "has_config": False})
    return projects


def status(root: Path, modules: list[Module]) -> dict[str, object]:
    sdd = root / SDD_DIR
    installed = read_toml(sdd / VERSION_FILE)
    module_rows = []
    for module in modules:
        recorded = installed.get(f"modules.{module.code}")
        if recorded is None:
            state = "new"
        elif recorded == module.version:
            state = "current"
        else:
            state = "updated"
        module_rows.append({
            "code": module.code,
            "plugin": module.plugin,
            "skills": list(module.skills),
            "version": module.version,
            "recorded_version": recorded,
            "state": state,
            "install": f"/plugin install {module.plugin}@claude",
        })

    team = read_toml(sdd / TEAM_FILE)
    docs_root = str(team.get("paths.docs_root", "docs"))
    pending = pending_questions(root, modules)
    scripts = scripts_state(root)
    projects = list_projects(root, docs_root)
    sdd_exists = sdd.is_dir()

    if not sdd_exists:
        next_step = "setup"
    elif pending or any(s != "current" for s in scripts.values()) or any(m["state"] != "current" for m in module_rows):
        next_step = "update"
    elif not projects:
        next_step = "discovery-init"
    else:
        next_step = None

    return {
        "workspace_root": str(root),
        "sdd_exists": sdd_exists,
        "current": sdd_exists and next_step != "update",
        "python": sys.version.split()[0],
        "uv": shutil.which("uv") is not None,
        "modules": module_rows,
        "pending_questions": len(pending),
        "scripts": scripts,
        "gitignore": gitignore_state(root),
        "docs_root": docs_root,
        "has_workspace_md": (root / docs_root / "workspace.md").is_file(),
        "projects": projects,
        "next": next_step,
    }


def apply(root: Path, modules: list[Module], answers: dict[str, str]) -> dict[str, object]:
    sdd = root / SDD_DIR
    created = not sdd.is_dir()
    sdd.mkdir(parents=True, exist_ok=True)

    by_key = {q.key: q for m in modules for q in m.questions}
    unknown = [key for key in answers if key not in by_key]
    if unknown:
        raise SddError(f"respostas para chaves que nenhum módulo declara: {', '.join(unknown)}")
    grouped: dict[str, dict[str, str]] = {scope: {} for scope in SCOPES}
    for key, value in answers.items():
        if not isinstance(value, str):
            raise SddError(f"a resposta de {key} deve ser texto")
        grouped[by_key[key].scope][key] = value
    written = {
        "team": append_values(sdd / TEAM_FILE, grouped["team"], TEAM_HEADER),
        "user": append_values(sdd / USER_FILE, grouped["user"], USER_HEADER),
    }

    before = scripts_state(root)
    target = sdd / "scripts"
    target.mkdir(exist_ok=True)
    for source in runtime_scripts():
        shutil.copy2(source, target / source.name)
    scripts = {
        name: {"missing": "created", "stale": "updated", "current": "unchanged"}[state]
        for name, state in before.items()
    }

    lines = [
        "# Versões gravadas pelo último sdd-setup. Arquivo gerado: não edite.",
        f'updated_at = "{date.today().isoformat()}"',
    ]
    previous = read_toml(sdd / VERSION_FILE)
    versions = {key: value for key, value in previous.items() if key.startswith("modules.")}
    versions.update({f"modules.{m.code}": m.version for m in modules})
    lines += [f'{key} = "{value}"' for key, value in sorted(versions.items())]
    (sdd / VERSION_FILE).write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "sdd": "created" if created else "updated",
        "written": written,
        "scripts": scripts,
        "versions": {key.removeprefix("modules."): value for key, value in versions.items()},
        "pending_questions": len(pending_questions(root, modules)),
        "gitignore": gitignore_state(root),
        "answers": {
            "team": read_toml(sdd / TEAM_FILE),
            "user": read_toml(sdd / USER_FILE),
        },
    }


def add_gitignore(root: Path) -> dict[str, object]:
    if gitignore_state(root) == "protected":
        return {"gitignore": "protected", "changed": False}
    gitignore = root / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    if text and not text.endswith("\n"):
        text += "\n"
    text += f"# Configuração pessoal do sdd\n{GITIGNORE_LINE}\n"
    gitignore.write_text(text, encoding="utf-8")
    return {"gitignore": "protected", "changed": True}


def read_answers(path: Path) -> dict[str, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SddError(f"não consegui ler as respostas em {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SddError("o arquivo de respostas deve ser um objeto JSON {\"chave\": \"valor\"}")
    path.unlink()
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--modules", help="códigos separados por vírgula")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--status", action="store_true")
    mode.add_argument("--list-config-questions", action="store_true")
    mode.add_argument("--gitignore", action="store_true")
    parser.add_argument("--answers", type=Path)
    args = parser.parse_args()

    root = args.workspace_root.resolve()
    if not root.is_dir():
        fail(f"a pasta {root} não existe")
    selected = [code.strip() for code in args.modules.split(",") if code.strip()] if args.modules else None

    try:
        modules = load_modules(selected)
        if args.status:
            emit(status(root, modules))
        elif args.list_config_questions:
            emit([
                {"module": q.module, "key": q.key, "prompt": q.prompt,
                 "default": expand_default(q.default, root), "scope": q.scope}
                for q in pending_questions(root, modules)
            ])
        elif args.gitignore:
            emit(add_gitignore(root))
        else:
            answers = read_answers(args.answers) if args.answers else {}
            emit(apply(root, modules, answers))
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
