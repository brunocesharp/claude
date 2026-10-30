"""Funções comuns aos scripts do sdd: raiz do workspace e leitura/gravação da configuração.

Sem dependências fora da biblioteca padrão (Python >= 3.11, por causa do tomllib).
Os arquivos de configuração usam só chaves pontuadas na raiz (ex.: ``user.name = "Ana"``),
sem cabeçalhos de tabela, para que acrescentar uma chave no fim do arquivo seja sempre válido.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

SDD_DIR = "_sdd"
TEAM_FILE = "config.toml"
USER_FILE = "config.user.toml"
VERSION_FILE = "version.toml"

TEAM_HEADER = (
    "# Configuração do workspace (equipe, versionada). Criada pelo sdd-setup.\n"
    "# Edite os valores à vontade: o setup só acrescenta chaves novas e nunca altera um valor existente.\n"
    "# Os valores de config.user.toml vencem os deste arquivo.\n"
)
USER_HEADER = (
    "# Configuração pessoal (não vai para o Git). Criada pelo sdd-setup.\n"
    "# Vence o config.toml. O setup só acrescenta chaves novas e nunca altera um valor existente.\n"
)


class SddError(Exception):
    """Erro esperado: o script imprime 'error: <mensagem>' e sai com código 1."""


def find_workspace_root(start: Path) -> Path | None:
    """Pasta mais próxima, de ``start`` para cima, que contém ``_sdd/``."""
    current = start.resolve()
    for folder in (current, *current.parents):
        if (folder / SDD_DIR).is_dir():
            return folder
    return None


def flatten(table: dict, prefix: str = "") -> dict[str, object]:
    flat: dict[str, object] = {}
    for key, value in table.items():
        dotted = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(flatten(value, f"{dotted}."))
        else:
            flat[dotted] = value
    return flat


def read_toml(path: Path) -> dict[str, object]:
    """Lê um TOML e devolve as chaves achatadas (``a.b``). Arquivo ausente = vazio."""
    if not path.is_file():
        return {}
    try:
        with path.open("rb") as handle:
            return flatten(tomllib.load(handle))
    except tomllib.TOMLDecodeError as exc:
        raise SddError(f"{path} não é um TOML válido: {exc}") from exc


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def append_values(path: Path, values: dict[str, str], header: str) -> list[str]:
    """Acrescenta ao arquivo as chaves que ainda não existem. Devolve as chaves gravadas."""
    existing = read_toml(path)
    new = {key: value for key, value in values.items() if key not in existing}
    if not new:
        return []
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.is_file() else header
    if text and not text.endswith("\n"):
        text += "\n"
    for key, value in new.items():
        text += f"{key} = {toml_string(value)}\n"
    path.write_text(text, encoding="utf-8")
    return list(new)


def resolve_config(root: Path) -> dict[str, object]:
    """Configuração final: o pessoal (config.user.toml) vence o da equipe (config.toml)."""
    sdd = root / SDD_DIR
    merged = read_toml(sdd / TEAM_FILE)
    merged.update(read_toml(sdd / USER_FILE))
    return merged


def emit(value: object) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(value, ensure_ascii=False, indent=2))


def fail(message: str) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"error: {message}")
    sys.exit(1)
