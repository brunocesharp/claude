#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Resolve a customização de uma skill para um projeto e imprime JSON.

Uso (a partir da raiz do workspace):
  uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto} [--key workflow.lenses]
  uv run _sdd/scripts/customize.py --skill story-review --project docs/{projeto}      (localiza a skill instalada)

Base: {skill-dir}/customize.toml (instalada com o plugin; não editar).
Override: docs/{projeto}/_custom/{skill}.toml (esparso; o plugin nunca toca).
Regras de merge: sdd-setup/references/customizacao.md.
"""

from __future__ import annotations

import argparse
import json
import os
import tomllib
from pathlib import Path

from sddlib import SddError, emit, fail

KEYS = ("id", "code")


def load(path: Path) -> dict:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise SddError(f"{path} não é um TOML válido: {exc}") from exc


def item_key(items: list) -> str | None:
    """'id' ou 'code' se TODOS os itens forem tabelas com essa chave; senão None."""
    if not items or not all(isinstance(i, dict) for i in items):
        return None
    for key in KEYS:
        if all(key in i for i in items):
            return key
    return None


def merge(base: object, over: object, path: str, warnings: list[str]) -> object:
    if isinstance(base, dict):
        if not isinstance(over, dict):
            warnings.append(f"{path}: esperava uma tabela; override ignorado")
            return base
        result = dict(base)
        for key, value in over.items():
            child = f"{path}.{key}" if path else key
            if key not in base:
                warnings.append(f"{child}: não é customizável nesta skill (ignorado)")
                continue
            result[key] = merge(base[key], value, child, warnings)
        return result
    if isinstance(base, list):
        if not isinstance(over, list):
            warnings.append(f"{path}: esperava uma lista; override ignorado")
            return base
        key = item_key(base) if base else item_key(over)
        if key and item_key(over) == key:
            merged = [dict(i) for i in base]
            index = {i[key]: n for n, i in enumerate(merged)}
            for item in over:
                if item[key] in index:
                    n = index[item[key]]
                    merged[n] = merge(merged[n], item, f"{path}[{key}={item[key]}]", warnings)
                else:
                    merged.append(item)
            return merged
        return [*base, *over]
    if isinstance(over, (dict, list)):
        warnings.append(f"{path}: esperava um valor simples; override ignorado")
        return base
    if base is not None and type(base) is not type(over) and not (isinstance(base, (int, float)) and isinstance(over, (int, float))):
        warnings.append(f"{path}: tipo diferente da base ({type(base).__name__}); override ignorado")
        return base
    return over


def same_as_base(base: object, over: object) -> tuple[int, int]:
    """(folhas do override iguais à base, total de folhas do override) — para avisar override não esparso."""
    if isinstance(over, dict) and isinstance(base, dict):
        equal = total = 0
        for key, value in over.items():
            e, t = same_as_base(base.get(key), value)
            equal, total = equal + e, total + t
        return equal, total
    return (1 if over == base else 0), 1


def facts(values: list, root: Path, warnings: list[str]) -> list[dict]:
    out = []
    for value in values:
        if not isinstance(value, str):
            warnings.append(f"persistent_facts: {value!r} ignorado (use texto ou 'file:glob')")
            continue
        if value.startswith("file:"):
            pattern = value[5:].strip()
            files = sorted(str(p.relative_to(root)).replace("\\", "/") for p in root.glob(pattern) if p.is_file())
            if not files:
                warnings.append(f"persistent_facts: '{pattern}' não encontrou arquivos")
            out.append({"source": value, "files": files})
        else:
            out.append({"source": "texto", "text": value})
    return out


def resolve(skill_dir: Path, project: Path) -> dict:
    base_path = skill_dir / "customize.toml"
    if not base_path.is_file():
        raise SddError(f"{skill_dir.name} não tem customize.toml: a skill não é customizável")
    skill = skill_dir.name
    base = load(base_path)
    override_path = project / "_custom" / f"{skill}.toml"
    warnings: list[str] = []
    resolved = base
    override = None
    if override_path.is_file():
        override = load(override_path)
        resolved = merge(base, override, "", warnings)
        equal, total = same_as_base(base, override)
        if total >= 3 and equal * 2 > total:
            warnings.append(f"override não esparso: {equal} de {total} valores são iguais à base; "
                            "deixe só o que muda (o resto é herdado e recebe as melhorias do plugin)")
    root = project.parent.parent
    workflow = resolved.get("workflow", {})
    return {
        "skill": skill,
        "base": str(base_path),
        "override": str(override_path) if override is not None else None,
        "resolved": resolved,
        "facts": facts(workflow.get("persistent_facts", []), root, warnings),
        "warnings": warnings,
    }


def find_skill_dir(name: str, workspace: Path, own_dir: Path = Path(__file__).resolve().parent) -> Path:
    """Pasta instalada da skill: plugins (installed_plugins.json), Skills CLI (.claude/skills) ou repositório local."""
    config_dir = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    candidates: list[Path] = []
    installed = config_dir / "plugins" / "installed_plugins.json"
    if installed.is_file():
        try:
            data = json.loads(installed.read_text(encoding="utf-8"))
            for entries in (data.get("plugins") or {}).values():
                for entry in entries if isinstance(entries, list) else [entries]:
                    if isinstance(entry, dict) and entry.get("installPath"):
                        candidates.append(Path(entry["installPath"]) / "skills" / name)
        except (OSError, json.JSONDecodeError):
            pass
    candidates += [workspace / ".claude" / "skills" / name, config_dir / "skills" / name]
    # Repositório do marketplace (desenvolvimento): plugins/<plugin>/skills/<skill>, a partir deste script.
    if len(own_dir.parents) > 3 and own_dir.parent.name == "sdd-setup":
        candidates += sorted(own_dir.parents[3].glob(f"*/skills/{name}"))
    found = [c for c in candidates if (c / "customize.toml").is_file()]
    if not found:
        raise SddError(f"skill {name} não encontrada com customize.toml (é uma das customizáveis? está instalada?)")
    return found[0]


def pick(data: dict, dotted: str):
    node = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    where = parser.add_mutually_exclusive_group(required=True)
    where.add_argument("--skill-dir", type=Path, help="pasta da skill (${CLAUDE_SKILL_DIR}, dentro da própria skill)")
    where.add_argument("--skill", help="nome da skill; o script localiza a pasta instalada")
    parser.add_argument("--project", type=Path, required=True, help="pasta do projeto (docs/{projeto})")
    parser.add_argument("--key", action="append", default=[], help="chave pontuada de resolved; pode repetir")
    args = parser.parse_args()
    try:
        project = args.project.resolve()
        skill_dir = args.skill_dir.resolve() if args.skill_dir else find_skill_dir(args.skill, project.parent.parent)
        result = resolve(skill_dir, project)
        if args.key:
            result["resolved"] = {key: pick(result["resolved"], key) for key in args.key}
        emit(result)
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
