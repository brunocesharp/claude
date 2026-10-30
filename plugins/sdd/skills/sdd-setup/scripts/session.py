#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Monta (e, com --launch, executa) o comando que abre uma sessão nova do Claude Code numa janela de terminal.

O Claude não limpa a própria sessão; o jeito de começar com contexto limpo é outra janela.

Uso:
  uv run _sdd/scripts/session.py --cwd <repositório> [--add-dir <pasta> ...] [--prompt "dev-story 1-2 do projeto loja"]
  ... --launch          abre a janela (só depois da confirmação do usuário)

Imprime JSON: {platform, command, display, launched}.
"""

from __future__ import annotations

import argparse
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from sddlib import SddError, emit, fail

# Sem aspas, &, |, <, >, ^, %, ; ou $: o prompt atravessa cmd, wt, osascript e bash sem interpretação.
SAFE_PROMPT = re.compile(r"^[\w\s.,:/\\()-]*$")


def detect_platform() -> str:
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def claude_args(add_dirs: list[str], prompt: str) -> list[str]:
    args = ["claude"]
    for folder in add_dirs:
        args += ["--add-dir", folder]
    if prompt:
        args.append(prompt)
    return args


def build(platform: str, cwd: str, add_dirs: list[str], prompt: str, which=shutil.which) -> list[str]:
    inner = claude_args(add_dirs, prompt)
    if platform == "windows":
        # cmd /k resolve claude.exe e claude.cmd (instalação via npm) e mantém a janela aberta no fim.
        if which("wt"):
            return ["wt", "-w", "new", "-d", cwd, "cmd", "/k", *inner]
        return ["cmd", "/c", "start", "", "/D", cwd, "cmd", "/k", *inner]
    shell_line = f"cd {shlex.quote(cwd)} && {shlex.join(inner)}"
    if platform == "macos":
        script = shell_line.replace("\\", "\\\\").replace('"', '\\"')
        return ["osascript", "-e", f'tell application "Terminal" to do script "{script}"',
                "-e", 'tell application "Terminal" to activate']
    for terminal in ("gnome-terminal", "konsole", "x-terminal-emulator"):
        if which(terminal):
            if terminal == "gnome-terminal":
                return ["gnome-terminal", f"--working-directory={cwd}", "--", *inner]
            if terminal == "konsole":
                return ["konsole", "--workdir", cwd, "-e", *inner]
            return ["x-terminal-emulator", "-e", "bash", "-lc", f"{shell_line}; exec bash"]
    raise SddError("nenhum terminal encontrado (gnome-terminal, konsole, x-terminal-emulator): "
                   "abra um terminal e rode o comando de 'display'")


def display(platform: str, cwd: str, add_dirs: list[str], prompt: str) -> str:
    """Comando para a pessoa colar num terminal, caso prefira abrir à mão."""
    inner = claude_args(add_dirs, prompt)
    if platform == "windows":
        quoted = " ".join(f'"{a}"' if (" " in a or not a) else a for a in inner)
        return f'cd /d "{cwd}" && {quoted}'
    return f"cd {shlex.quote(cwd)} && {shlex.join(inner)}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cwd", required=True, help="pasta onde a sessão abre (o repositório principal da story)")
    parser.add_argument("--add-dir", action="append", default=[], help="pasta extra acessível na sessão; pode repetir")
    parser.add_argument("--prompt", default="", help="primeira mensagem da sessão")
    parser.add_argument("--platform", choices=("windows", "macos", "linux"), help="padrão: o sistema atual")
    parser.add_argument("--launch", action="store_true", help="abre a janela (só com confirmação do usuário)")
    args = parser.parse_args()

    try:
        cwd = Path(args.cwd)
        if not cwd.is_dir():
            raise SddError(f"a pasta {cwd} não existe")
        missing = [d for d in args.add_dir if not Path(d).is_dir()]
        if missing:
            raise SddError(f"pastas inexistentes em --add-dir: {', '.join(missing)}")
        if not SAFE_PROMPT.match(args.prompt):
            raise SddError("o prompt só pode ter letras, números, espaço e . , : / \\ ( ) -")
        platform = args.platform or detect_platform()
        cwd_text = str(cwd.resolve())
        add_dirs = [str(Path(d).resolve()) for d in args.add_dir]
        try:
            command, note = build(platform, cwd_text, add_dirs, args.prompt), None
        except SddError as exc:
            if args.launch:
                raise
            command, note = None, str(exc)
        result = {"platform": platform, "command": command,
                  "display": display(platform, cwd_text, add_dirs, args.prompt), "launched": False}
        if note:
            result["note"] = note
        if args.launch:
            if platform != detect_platform():
                raise SddError("--launch só funciona na plataforma atual")
            subprocess.Popen(command, cwd=cwd_text, stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            result["launched"] = True
        emit(result)
    except (SddError, OSError) as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
