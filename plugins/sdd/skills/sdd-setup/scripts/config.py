#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Resolve a configuração do workspace e imprime JSON.

Uso:
  uv run _sdd/scripts/config.py [--workspace-root <pasta>] [--key user.name --key language.documents]

Sem --key, imprime todas as chaves. Com --key, imprime só as pedidas (ausente = null).
Precedência: _sdd/config.user.toml > _sdd/config.toml.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from sddlib import SddError, emit, fail, find_workspace_root, resolve_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace-root", type=Path, help="raiz do workspace (padrão: pasta mais próxima com _sdd/)")
    parser.add_argument("--key", action="append", default=[], help="chave pontuada; pode repetir")
    args = parser.parse_args()

    root = args.workspace_root or find_workspace_root(Path.cwd())
    if root is None or not (root / "_sdd").is_dir():
        fail("workspace sem _sdd/: rode o sdd-setup primeiro")
    try:
        config = resolve_config(root)
    except SddError as exc:
        fail(str(exc))
    if args.key:
        config = {key: config.get(key) for key in args.key}
    emit(config)


if __name__ == "__main__":
    main()
