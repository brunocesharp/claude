#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Hook PostToolUse (Write|Edit) do plugin sdd: valida o sprint-status.yaml depois que o Claude o grava.

Lê o JSON do hook na entrada padrão. Se o arquivo gravado não for um sprint-status.yaml, sai com 0.
Se for e estiver inválido, escreve os erros na saída de erro e sai com 2 (o Claude recebe a mensagem e corrige).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path") or ""
    if Path(file_path).name != "sprint-status.yaml" or not Path(file_path).is_file():
        return 0

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from sddlib import SddError
    from status import load, validate

    try:
        errors = validate(load(Path(file_path)))
    except SddError as exc:
        errors = [str(exc)]
    if not errors:
        return 0
    sys.stderr.reconfigure(encoding="utf-8")
    print(f"{file_path} ficou inválido:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    print("Corrija o arquivo (formato em sdd-setup/references/sprint-status.md). "
          "Para mudar estados, prefira _sdd/scripts/status.py set, que valida as transições.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
