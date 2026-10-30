#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Migrações declaradas pelos módulos (modules/<plugin>.toml, [[module.migrations]]). Imprime JSON.

Uso:
  uv run "${CLAUDE_SKILL_DIR}/scripts/migrate.py" --workspace-root <pasta> [--modules a,b]            pendentes
  uv run "${CLAUDE_SKILL_DIR}/scripts/migrate.py" --workspace-root <pasta> --all                     inclui opcionais
  uv run "${CLAUDE_SKILL_DIR}/scripts/migrate.py" --workspace-root <pasta> --mark-applied <id>       registra

O script só lista e registra. Os passos de cada migração estão no guia (campo guide) e são feitos
pela skill, com confirmação do usuário. Migração registrada fica em _sdd/version.toml (migrations.<id>).

Campos de uma migração:
  id      identificador único (kebab-case)
  title   o que muda, em uma frase
  kind    "upgrade": pendente quando a versão gravada do módulo é menor que 'to';
          "optional": oferecida só com --all ou a pedido (ex.: converter um formato antigo)
  to      versão do módulo que introduz a migração
  guide   caminho do guia, relativo à pasta da skill sdd-setup
"""

from __future__ import annotations

import argparse
import tomllib
from datetime import date
from pathlib import Path

from sddlib import SDD_DIR, VERSION_FILE, SddError, emit, fail, read_toml
from setup import MODULES_DIR, SKILL_DIR

KINDS = ("upgrade", "optional")


def version_tuple(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in value.split("-")[0].split("."))
    except ValueError as exc:
        raise SddError(f"versão inválida: {value!r}") from exc


def load_migrations(selected: list[str] | None) -> list[dict]:
    migrations = []
    for path in sorted(MODULES_DIR.glob("*.toml")):
        with path.open("rb") as handle:
            module = tomllib.load(handle).get("module", {})
        if selected is not None and module.get("code") not in selected:
            continue
        for index, raw in enumerate(module.get("migrations", [])):
            where = f"{path.name}: migrations[{index}]"
            for field in ("id", "title", "kind", "to", "guide"):
                if not isinstance(raw.get(field), str) or not raw[field]:
                    raise SddError(f"{where}.{field} deve ser texto não vazio")
            if raw["kind"] not in KINDS:
                raise SddError(f'{where}.kind deve ser "upgrade" ou "optional"')
            if not (SKILL_DIR / raw["guide"]).is_file():
                raise SddError(f"{where}: guia {raw['guide']} não existe")
            migrations.append({**raw, "module": module["code"]})
    ids = [m["id"] for m in migrations]
    duplicated = {i for i in ids if ids.count(i) > 1}
    if duplicated:
        raise SddError(f"migração com id repetido: {', '.join(sorted(duplicated))}")
    return migrations


def listing(root: Path, migrations: list[dict], include_optional: bool) -> list[dict]:
    recorded = read_toml(root / SDD_DIR / VERSION_FILE)
    out = []
    for migration in migrations:
        applied = recorded.get(f"migrations.{migration['id']}")
        if applied:
            continue
        version = recorded.get(f"modules.{migration['module']}")
        if migration["kind"] == "upgrade":
            # Workspace novo (sem versão gravada) não tem nada antigo para migrar.
            if version is None or version_tuple(str(version)) >= version_tuple(migration["to"]):
                continue
        elif not include_optional:
            continue
        out.append({**migration, "guide": str((SKILL_DIR / migration["guide"]).resolve()), "recorded_version": version})
    return out


def mark_applied(root: Path, migrations: list[dict], migration_id: str) -> dict:
    if migration_id not in {m["id"] for m in migrations}:
        raise SddError(f"migração {migration_id} não declarada")
    path = root / SDD_DIR / VERSION_FILE
    if not path.is_file():
        raise SddError("workspace sem _sdd/version.toml: rode o setup primeiro")
    key = f"migrations.{migration_id}"
    if key in read_toml(path):
        return {"id": migration_id, "changed": False}
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + f'{key} = "{date.today().isoformat()}"\n', encoding="utf-8")
    return {"id": migration_id, "changed": True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--modules")
    parser.add_argument("--all", action="store_true", help="inclui migrações opcionais")
    parser.add_argument("--mark-applied", metavar="ID")
    args = parser.parse_args()

    root = args.workspace_root.resolve()
    selected = [c.strip() for c in args.modules.split(",") if c.strip()] if args.modules else None
    try:
        migrations = load_migrations(selected)
        if args.mark_applied:
            emit(mark_applied(root, migrations, args.mark_applied))
        else:
            emit(listing(root, migrations, args.all))
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
