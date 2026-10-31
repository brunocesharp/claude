#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Apoio da skill criacao-story-recorrente: o mesmo script da execucao-recorrente, no perfil criacao
(create-story). Aceita os mesmos comandos: config, init-config, scan, lock, registrar.

Uso (de qualquer pasta):
  uv run scripts/story_recorrente.py scan [--config ARQ]
  uv run scripts/story_recorrente.py lock adquirir|liberar [--config ARQ]
  uv run scripts/story_recorrente.py registrar {workspace} --projeto loja --id 1-3-editar \\
      --acao create-story --resultado iniciada|concluida|falhou|bloqueada|pulada|aguardando [--motivo "..."]

Configuração: --config, senão CRIACAO_STORY_RECORRENTE_CONFIG, senão ~/.claude/criacao-story-recorrente.toml.
"""

import runpy
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "execucao-recorrente" / "scripts" / "recorrente.py"

if __name__ == "__main__":
    if not SHARED.is_file():
        sys.stdout.reconfigure(encoding="utf-8")
        print(f"error: script compartilhado não encontrado: {SHARED} (a skill execucao-recorrente faz parte do "
              "mesmo plugin delivery; reinstale o plugin)")
        sys.exit(1)
    sys.argv[1:1] = ["--perfil", "criacao"]
    runpy.run_path(str(SHARED), run_name="__main__")
