"""Testes do session.py (só montagem do comando; nunca abre janela).
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import session  # noqa: E402


def run(*args: str):
    result = subprocess.run([sys.executable, str(SCRIPTS / "session.py"), *args],
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


def test_windows_com_wt_abre_janela_nova_via_cmd():
    command = session.build("windows", r"D:\repos\api", [r"D:\docs"], "dev-story 1-2 do projeto loja",
                            which=lambda name: name == "wt")
    assert command == ["wt", "-w", "new", "-d", r"D:\repos\api", "cmd", "/k", "claude", "--add-dir", r"D:\docs",
                       "dev-story 1-2 do projeto loja"]


def test_windows_sem_wt_usa_start():
    command = session.build("windows", r"D:\repos\api", [], "", which=lambda name: None)
    assert command[:6] == ["cmd", "/c", "start", "", "/D", r"D:\repos\api"]
    assert command[-1] == "claude"


def test_macos_e_linux():
    mac = session.build("macos", "/Users/a/api repo", ["/docs"], "dev-story 1-2", which=lambda n: None)
    assert mac[0] == "osascript" and "cd '/Users/a/api repo' && claude --add-dir /docs 'dev-story 1-2'" in mac[2]
    linux = session.build("linux", "/home/a/api", [], "dev-story 1-2", which=lambda n: n == "gnome-terminal")
    assert linux == ["gnome-terminal", "--working-directory=/home/a/api", "--", "claude", "dev-story 1-2"]


def test_cli_mostra_sem_abrir(tmp_path):
    code, result = run("--cwd", str(tmp_path), "--add-dir", str(tmp_path), "--prompt", "dev-story 1-2", "--platform", "linux")
    assert code == 0 and result["launched"] is False
    assert result["display"].startswith("cd ") and result["display"].endswith(" 'dev-story 1-2'")
    assert "claude --add-dir" in result["display"]


def test_cli_recusa_prompt_perigoso_e_pasta_inexistente(tmp_path):
    code, message = run("--cwd", str(tmp_path), "--prompt", "dev-story 1-2 & del *")
    assert code == 1 and "prompt" in message
    code, message = run("--cwd", str(tmp_path / "nao-existe"))
    assert code == 1 and "não existe" in message
