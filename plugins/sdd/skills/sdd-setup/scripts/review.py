#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Apoio à revisão de uma story: diff dos repositórios e integridade do registro. Imprime JSON.

Uso (a partir da raiz do workspace):
  uv run _sdd/scripts/review.py --project docs/{projeto} integrity {id} --repo api=D:/repos/api [--repo web=...] [--base main]
  uv run _sdd/scripts/review.py --project docs/{projeto} diff {id} --repo api=D:/repos/api [...] --out {arquivo}

integrity compara a seção "Arquivos alterados" da story com o que mudou de fato em cada repositório
(commits da branch desde a base + alterações ainda não commitadas). Só lê os repositórios.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from sddlib import SddError, emit, fail
from story import sections

REPO_HEADING = re.compile(r"^###\s+([^\s(]+)")
FILE_LINE = re.compile(r"^\s*-\s*`?([AMDRC])`?\s+`?([^`\s]+)`?")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise SddError(f"git {' '.join(args)} em {repo}: {result.stderr.strip()}")
    return result.stdout


def base_branch(repo: Path, base: str | None) -> str:
    if base:
        return base
    try:
        ref = git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").strip()
        return ref.removeprefix("refs/remotes/")
    except SddError:
        pass
    for candidate in ("main", "master", "develop"):
        if subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", candidate],
                          capture_output=True).returncode == 0:
            return candidate
    raise SddError(f"não achei a branch base em {repo}: informe --base")


def changed_files(repo: Path, base: str) -> dict[str, str]:
    """{caminho: status} — commits desde o merge-base com a base + árvore de trabalho (inclui não rastreados)."""
    files: dict[str, str] = {}
    for line in git(repo, "diff", "--name-status", f"{base}...HEAD").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            files[parts[-1]] = parts[0][0]
    for line in git(repo, "status", "--porcelain", "--untracked-files=all").splitlines():
        code, path = line[:2], line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files[path.strip('"')] = "A" if code == "??" else (code.strip()[:1] or "M")
    return files


def declared_files(project: Path, story_id: str) -> dict[str, dict[str, str]]:
    path = project / "implementacao" / "stories" / f"{story_id}.md"
    if not path.is_file():
        raise SddError(f"{path} não existe")
    section = sections(path.read_text(encoding="utf-8")).get("Arquivos alterados", "")
    declared: dict[str, dict[str, str]] = {}
    current = None
    for line in section.splitlines():
        heading = REPO_HEADING.match(line)
        if heading:
            current = heading.group(1)
            declared.setdefault(current, {})
            continue
        match = FILE_LINE.match(line)
        if match and current:
            declared[current][match.group(2)] = match.group(1)
    return declared


def parse_repos(values: list[str]) -> dict[str, Path]:
    repos: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise SddError(f"--repo deve ser nome=caminho: {value}")
        name, path = value.split("=", 1)
        repo = Path(path)
        if not (repo / ".git").exists():
            raise SddError(f"{repo} não é um repositório Git")
        repos[name] = repo
    if not repos:
        raise SddError("informe ao menos um --repo nome=caminho")
    return repos


def integrity(project: Path, story_id: str, repos: dict[str, Path], base: str | None) -> dict:
    declared = declared_files(project, story_id)
    result = {"id": story_id, "repos": [], "consistent": True}
    for name, repo in repos.items():
        used_base = base_branch(repo, base)
        actual = changed_files(repo, used_base)
        listed = declared.get(name, {})
        undeclared = sorted(p for p in actual if p not in listed)
        not_changed = sorted(p for p in listed if p not in actual)
        row = {"repo": name, "base": used_base, "branch": git(repo, "branch", "--show-current").strip(),
               "changed": len(actual), "declared": len(listed),
               "undeclared": undeclared, "declared_not_changed": not_changed,
               "uncommitted": bool(git(repo, "status", "--porcelain").strip())}
        if undeclared or not_changed:
            result["consistent"] = False
        result["repos"].append(row)
    unknown = sorted(set(declared) - set(repos))
    if unknown:
        result["declared_repos_not_checked"] = unknown
    return result


def write_diff(repos: dict[str, Path], base: str | None, out: Path) -> dict:
    chunks = []
    summary = []
    for name, repo in repos.items():
        used_base = base_branch(repo, base)
        committed = git(repo, "diff", f"{used_base}...HEAD")
        working = git(repo, "diff", "HEAD")
        untracked = [l[3:] for l in git(repo, "status", "--porcelain", "--untracked-files=all").splitlines()
                     if l.startswith("??")]
        chunks.append(f"# ===== {name} ({repo}) — base {used_base} =====\n")
        chunks.append(committed)
        if working:
            chunks.append(f"\n# ----- {name}: alterações não commitadas -----\n")
            chunks.append(working)
        if untracked:
            chunks.append(f"\n# ----- {name}: arquivos novos não rastreados (leia direto do repositório) -----\n")
            chunks.append("\n".join(untracked) + "\n")
        summary.append({"repo": name, "base": used_base, "untracked": untracked,
                        "lines": committed.count("\n") + working.count("\n")})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(chunks), encoding="utf-8")
    return {"out": str(out), "repos": summary}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("integrity", "diff"):
        cmd = sub.add_parser(name)
        cmd.add_argument("id")
        cmd.add_argument("--repo", action="append", default=[], help="nome=caminho; pode repetir")
        cmd.add_argument("--base", help="branch base (padrão: origin/HEAD, main, master ou develop)")
        if name == "diff":
            cmd.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        repos = parse_repos(args.repo)
        if args.command == "integrity":
            emit(integrity(args.project.resolve(), args.id, repos, args.base))
        else:
            emit(write_diff(repos, args.base, args.out))
    except SddError as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
