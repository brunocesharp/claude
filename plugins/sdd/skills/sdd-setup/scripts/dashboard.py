#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Consolida o estado do workspace e gera o dashboard SDD.

Uso:
  uv run _sdd/scripts/dashboard.py [--workspace-root <pasta>] [--project <slug>] show
  uv run _sdd/scripts/dashboard.py [--workspace-root <pasta>] [--project <slug>] build
  uv run _sdd/scripts/dashboard.py [--workspace-root <pasta>] [--project <slug>] serve [--port 8765]

``show`` não grava nada. ``build`` grava um snapshot JSON e um HTML autocontido em
``_sdd/dashboard/``. ``serve`` regenera os arquivos e os publica apenas em localhost,
para uso no Simple Browser do VS Code.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from sddlib import SddError, emit, fail, find_workspace_root, resolve_config
from status import STATUS_FILE, load, next_action, summary, validate
from workspace import phases, workspace_rows

DASHBOARD_DIR = Path("_sdd") / "dashboard"
AUTOMATIONS = (
    ("criacao-story-recorrente", "Criação de stories"),
    ("execucao-recorrente", "Execução de stories"),
)
VISIBLE_STATES = ("backlog", "ready-for-dev", "in-progress", "review", "blocked", "done", "dropped")


def read_json(path: Path) -> tuple[dict, str | None]:
    if not path.is_file():
        return {}, None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, str(exc)
    return (value if isinstance(value, dict) else {}), None


def read_config(root: Path) -> dict:
    if not (root / "_sdd").is_dir():
        return {}
    return resolve_config(root)


def story_path(root: Path, project: Path, story: dict) -> str | None:
    file = story.get("file")
    if not file:
        return None
    try:
        return str((project / "implementacao" / str(file)).relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(project / "implementacao" / str(file))


def automation_state(root: Path) -> list[dict]:
    output = []
    for code, title in AUTOMATIONS:
        path = root / "_sdd" / code / "estado.json"
        data, error = read_json(path)
        records = []
        for key, item in (data.get("stories") or {}).items():
            if not isinstance(item, dict):
                continue
            project, _, story_id = str(key).partition("/")
            records.append({
                "project": project,
                "story": story_id,
                "action": item.get("acao"),
                "result": item.get("ultimo_resultado"),
                "attempts": item.get("tentativas", 0),
                "last_run": item.get("ultima_execucao"),
                "reason": item.get("motivo") or (item.get("pulada") or {}).get("motivo"),
            })
        records.sort(key=lambda row: row.get("last_run") or "", reverse=True)
        output.append({
            "code": code,
            "title": title,
            "configured": path.is_file(),
            "error": error,
            "records": records[:20],
        })
    return output


def project_snapshot(root: Path, docs: Path, project: Path, rows: dict[str, dict[str, str]]) -> dict:
    slug = project.name
    config, config_error = read_json(project / "project-config.json")
    item = {
        "slug": slug,
        "name": config.get("name", slug),
        "folder": str(project.relative_to(root)).replace("\\", "/"),
        "phase": phases(project / "project.md"),
        "situation": rows.get(slug, {}).get("situação") or rows.get(slug, {}).get("situacao"),
        "repositories": "varios" if (project / "repositorios.md").is_file() else config.get("repositories", "um"),
        "config_error": config_error,
        "updated_at": None,
        "valid": True,
        "problems": [],
        "epics": [],
        "stories": [],
        "totals": {state: 0 for state in VISIBLE_STATES},
        "next": None,
    }
    status_file = project / STATUS_FILE
    if not status_file.is_file():
        return item
    try:
        data = load(status_file)
        problems = validate(data)
        item["valid"] = not problems
        item["problems"] = problems
        item["updated_at"] = str(data.get("updated_at") or "")
        if problems:
            return item
        board = summary(data)
        item["next"] = next_action(data)
        item["totals"].update({state: int(board["totals"].get(state, 0)) for state in VISIBLE_STATES})
        for epic in board["epics"]:
            item["epics"].append({key: epic[key] for key in ("id", "title", "status", "done", "total", "counts")})
            for story in epic["stories"]:
                item["stories"].append({
                    **story,
                    "epic": epic["id"],
                    "epic_title": epic["title"],
                    "path": story_path(root, project, story),
                })
    except SddError as exc:
        item["valid"] = False
        item["problems"] = [str(exc)]
    return item


def build_snapshot(root: Path, project_filter: str | None = None) -> dict:
    config = read_config(root)
    docs = root / str(config.get("paths.docs_root", "docs"))
    rows = workspace_rows(docs / "workspace.md")
    slugs = sorted({p.parent.name for p in docs.glob("*/project.md")} | {p.parent.name for p in docs.glob("*/project-config.json")})
    if project_filter:
        if project_filter not in slugs:
            raise SddError(f"projeto {project_filter} não encontrado em {docs}")
        slugs = [project_filter]
    projects = [project_snapshot(root, docs, docs / slug, rows) for slug in slugs]
    automations = automation_state(root)
    attention = []
    for project in projects:
        if not project["valid"]:
            attention.append({"kind": "invalid", "project": project["slug"], "title": "Quadro inválido", "detail": "; ".join(project["problems"])})
        for story in project["stories"]:
            if story["status"] == "blocked":
                attention.append({"kind": "blocked", "project": project["slug"], "story": story["id"], "title": story["title"], "detail": "Story bloqueada"})
            elif story["status"] == "review":
                attention.append({"kind": "review", "project": project["slug"], "story": story["id"], "title": story["title"], "detail": "Aguardando revisão"})
    for automation in automations:
        if automation["error"]:
            attention.append({"kind": "automation", "project": "workspace", "title": automation["title"], "detail": automation["error"]})
        for record in automation["records"]:
            if record["result"] in ("falhou", "bloqueada", "aguardando"):
                attention.append({
                    "kind": "automation",
                    "project": record["project"],
                    "story": record["story"],
                    "title": f"{automation['title']}: {record['story']}",
                    "detail": record["reason"] or record["result"],
                })
    totals = Counter()
    for project in projects:
        totals.update(project["totals"])
    return {
        "version": 1,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "workspace": root.name,
        "workspace_root": str(root),
        "docs_root": str(docs.relative_to(root)).replace("\\", "/") if docs.is_relative_to(root) else str(docs),
        "projects": projects,
        "totals": {state: totals[state] for state in VISIBLE_STATES},
        "attention": attention,
        "automations": automations,
    }


HTML_TEMPLATE = r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>SDD Dashboard</title>
  <style>
    :root{color-scheme:light dark;--bg:#f5f7fb;--panel:#fff;--text:#172033;--muted:#64748b;--line:#dce3ee;--accent:#2563eb;--accent-soft:#dbeafe;--danger:#b42318;--danger-soft:#fee4e2;--warn:#b54708;--warn-soft:#fef0c7;--ok:#067647;--ok-soft:#d1fadf;--shadow:0 8px 28px rgba(15,23,42,.08)}
    @media(prefers-color-scheme:dark){:root{--bg:#0d1117;--panel:#161b22;--text:#e6edf3;--muted:#8b949e;--line:#30363d;--accent:#58a6ff;--accent-soft:#132f4c;--danger:#ff7b72;--danger-soft:#3d191d;--warn:#e3b341;--warn-soft:#352b13;--ok:#3fb950;--ok-soft:#14321f;--shadow:none}}
    *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}button,input,select{font:inherit}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid color-mix(in srgb,var(--accent) 45%,transparent);outline-offset:2px}.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
    .shell{display:grid;grid-template-columns:230px minmax(0,1fr);min-height:100vh}.sidebar{background:var(--panel);border-right:1px solid var(--line);padding:24px 16px;position:sticky;top:0;height:100vh}.brand{font-size:18px;font-weight:700;margin:0 8px 4px}.workspace{color:var(--muted);margin:0 8px 24px;overflow-wrap:anywhere}.nav{display:grid;gap:6px}.nav button{border:0;background:transparent;color:var(--muted);text-align:left;padding:10px 12px;border-radius:8px;cursor:pointer}.nav button.active{background:var(--accent-soft);color:var(--accent);font-weight:650}.main{min-width:0;padding:28px}.top{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:22px}.top h1{font-size:24px;margin:0 0 4px}.subtitle{color:var(--muted);margin:0}.updated{color:var(--muted);font-size:12px;white-space:nowrap}
    .metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:24px}.metric,.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow)}.metric{padding:16px}.metric b{display:block;font-size:25px}.metric span{color:var(--muted)}.panel{padding:18px;margin-bottom:18px}.panel h2{font-size:16px;margin:0 0 14px}.filters{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px}.filters input,.filters select{background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:8px;padding:8px 10px;min-width:180px}
    .project-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}.project-card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px}.project-card h3{margin:0 0 3px;font-size:16px}.meta{color:var(--muted);font-size:12px}.progress{height:8px;background:var(--line);border-radius:999px;overflow:hidden;margin:14px 0 7px}.progress>i{display:block;height:100%;background:var(--accent)}.next{margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}.badge{display:inline-flex;align-items:center;border-radius:999px;padding:3px 8px;font-size:12px;background:var(--accent-soft);color:var(--accent)}.badge.blocked,.badge.invalid{background:var(--danger-soft);color:var(--danger)}.badge.review,.badge.automation{background:var(--warn-soft);color:var(--warn)}.badge.done{background:var(--ok-soft);color:var(--ok)}
    .board{display:grid;grid-template-columns:repeat(7,minmax(210px,1fr));gap:12px;overflow-x:auto;padding-bottom:8px}.column{min-height:180px}.column h3{font-size:13px;color:var(--muted);margin:0 0 10px;text-transform:uppercase;letter-spacing:.04em}.story{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:9px;padding:12px;margin-bottom:9px}.story[data-status="blocked"]{border-left-color:var(--danger)}.story[data-status="review"]{border-left-color:var(--warn)}.story[data-status="done"]{border-left-color:var(--ok)}.story b{display:block;margin-bottom:4px}.story small{color:var(--muted)}.story a{color:var(--accent);text-decoration:none}.story a:hover{text-decoration:underline}
    .attention{display:grid;gap:9px}.attention-item{display:grid;grid-template-columns:auto 1fr;gap:10px;padding:11px 0;border-bottom:1px solid var(--line)}.attention-item:last-child{border:0}.attention-item p{margin:2px 0 0;color:var(--muted)}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:12px;color:var(--muted)}.empty{color:var(--muted);padding:24px 0;text-align:center}.view[hidden]{display:none}
    @media(max-width:900px){.shell{grid-template-columns:1fr}.sidebar{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line);padding:14px}.nav{grid-template-columns:repeat(3,1fr)}.nav button{text-align:center}.main{padding:18px}.metrics{grid-template-columns:repeat(2,1fr)}.updated{white-space:normal}}
    @media(max-width:520px){.metrics{grid-template-columns:1fr}.top{display:block}.updated{margin-top:8px}.nav{grid-template-columns:1fr}.filters input,.filters select{width:100%}}
  </style>
</head>
<body>
<div class="shell">
  <aside class="sidebar"><div class="brand">SDD Dashboard</div><p class="workspace" id="workspace-name"></p><nav class="nav" aria-label="Navegação"><button class="active" data-view="portfolio">Portfólio</button><button data-view="kanban">Kanban</button><button data-view="attention">Atenção</button><button data-view="automations">Automações</button></nav></aside>
  <main class="main">
    <header class="top"><div><h1 id="page-title">Situação dos projetos</h1><p class="subtitle" id="page-subtitle"></p></div><div class="updated" id="updated"></div></header>
    <section class="view" id="portfolio-view"><div class="metrics" id="metrics"></div><div class="panel"><h2>Projetos</h2><div class="project-grid" id="projects"></div></div></section>
    <section class="view" id="kanban-view" hidden><div class="filters"><label><span class="sr">Projeto</span><select id="project-filter"></select></label><label><span class="sr">Buscar</span><input id="search" type="search" placeholder="Buscar story"></label></div><div class="board" id="board"></div></section>
    <section class="view" id="attention-view" hidden><div class="panel"><h2>Fila de atenção</h2><div class="attention" id="attention"></div></div></section>
    <section class="view" id="automations-view" hidden><div id="automations"></div></section>
  </main>
</div>
<script id="dashboard-data" type="application/json">__DATA__</script>
<script>
const DATA=JSON.parse(document.getElementById('dashboard-data').textContent);const states=['backlog','ready-for-dev','in-progress','review','blocked','done','dropped'];const labels={'backlog':'Backlog','ready-for-dev':'Pronta','in-progress':'Em desenvolvimento','review':'Revisão','blocked':'Bloqueada','done':'Concluída','dropped':'Cancelada'};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const plural=(n,a,b)=>`${n} ${n===1?a:b}`;document.getElementById('workspace-name').textContent=DATA.workspace;document.getElementById('page-subtitle').textContent=plural(DATA.projects.length,'projeto acompanhado','projetos acompanhados');document.getElementById('updated').textContent=`Atualizado em ${new Date(DATA.generated_at).toLocaleString('pt-BR')}`;
function metric(label,value){return `<div class="metric"><b>${value}</b><span>${label}</span></div>`}const active=states.filter(s=>!['done','dropped'].includes(s)).reduce((n,s)=>n+(DATA.totals[s]||0),0);document.getElementById('metrics').innerHTML=metric('Projetos',DATA.projects.length)+metric('Stories ativas',active)+metric('Em revisão',DATA.totals.review||0)+metric('Bloqueios',DATA.totals.blocked||0);
function projectCard(p){const total=states.filter(s=>s!=='dropped').reduce((n,s)=>n+(p.totals[s]||0),0),done=p.totals.done||0,pct=total?Math.round(done*100/total):0,phase=p.phase.current||'Fluxo concluído ou não iniciado',next=p.next?.action?`${p.next.action}${p.next.id?' · '+p.next.id:''}`:'Nenhuma ação pendente';return `<article class="project-card"><h3>${esc(p.name)}</h3><div class="meta">${esc(p.slug)} · ${esc(phase)}</div><div class="progress" role="progressbar" aria-label="Progresso de ${esc(p.name)}" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100"><i style="width:${pct}%"></i></div><div class="meta">${done}/${total} concluídas · ${pct}%</div>${p.valid?'':`<p><span class="badge invalid">Quadro inválido</span></p>`}<div class="next"><span class="meta">Próxima ação</span><br><b>${esc(next)}</b></div></article>`}document.getElementById('projects').innerHTML=DATA.projects.length?DATA.projects.map(projectCard).join(''):'<div class="empty">Nenhum projeto encontrado.</div>';
const select=document.getElementById('project-filter');select.innerHTML=DATA.projects.map(p=>`<option value="${esc(p.slug)}">${esc(p.name)}</option>`).join('');function renderBoard(){const p=DATA.projects.find(x=>x.slug===select.value)||DATA.projects[0],q=document.getElementById('search').value.trim().toLowerCase();document.getElementById('board').innerHTML=states.map(state=>{const stories=(p?.stories||[]).filter(s=>s.status===state&&(!q||`${s.id} ${s.title} ${s.epic}`.toLowerCase().includes(q)));return `<section class="column"><h3>${labels[state]} · ${stories.length}</h3>${stories.map(s=>`<article class="story" data-status="${state}"><b>${s.path?`<a href="../../${esc(s.path)}">${esc(s.id)}</a>`:esc(s.id)}</b><div>${esc(s.title)}</div><small>${esc(s.epic)}${s.repositories?.length?' · '+esc(s.repositories.join(', ')):''}</small></article>`).join('')}</section>`}).join('')}select.addEventListener('change',renderBoard);document.getElementById('search').addEventListener('input',renderBoard);renderBoard();
document.getElementById('attention').innerHTML=DATA.attention.length?DATA.attention.map(a=>`<article class="attention-item"><span class="badge ${esc(a.kind)}">${esc(a.kind)}</span><div><b>${esc(a.project)}${a.story?' · '+esc(a.story):''} — ${esc(a.title)}</b><p>${esc(a.detail)}</p></div></article>`).join(''):'<div class="empty">Nada exige atenção agora.</div>';
document.getElementById('automations').innerHTML=DATA.automations.map(a=>`<section class="panel"><h2>${esc(a.title)} ${a.configured?'':'<span class="badge">não configurada</span>'}</h2>${a.error?`<p class="badge invalid">${esc(a.error)}</p>`:''}<div class="table-wrap"><table><thead><tr><th>Projeto / story</th><th>Resultado</th><th>Tentativas</th><th>Última execução</th><th>Motivo</th></tr></thead><tbody>${a.records.length?a.records.map(r=>`<tr><td>${esc(r.project)} / ${esc(r.story)}</td><td>${esc(r.result||'—')}</td><td>${esc(r.attempts)}</td><td>${r.last_run?new Date(r.last_run).toLocaleString('pt-BR'):'—'}</td><td>${esc(r.reason||'—')}</td></tr>`).join(''):'<tr><td colspan="5" class="empty">Sem execuções registradas.</td></tr>'}</tbody></table></div></section>`).join('');
document.querySelectorAll('.nav button').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.nav button').forEach(b=>b.classList.toggle('active',b===btn));document.querySelectorAll('.view').forEach(v=>v.hidden=v.id!==`${btn.dataset.view}-view`);const titles={portfolio:'Situação dos projetos',kanban:'Quadro de stories',attention:'Fila de atenção',automations:'Execuções automáticas'};document.getElementById('page-title').textContent=titles[btn.dataset.view]}));
</script>
</body></html>'''


def render_html(snapshot: dict) -> str:
    payload = json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")).replace("</script", "<\\/script")
    return HTML_TEMPLATE.replace("__DATA__", payload)


def write_dashboard(root: Path, snapshot: dict) -> dict:
    folder = root / DASHBOARD_DIR
    folder.mkdir(parents=True, exist_ok=True)
    json_path = folder / "project-status.json"
    html_path = folder / "index.html"
    json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path.write_text(render_html(snapshot), encoding="utf-8")
    return {"generated": True, "html": str(html_path), "json": str(json_path), "projects": len(snapshot["projects"]), "attention": len(snapshot["attention"])}


def serve(root: Path, snapshot: dict, port: int) -> None:
    result = write_dashboard(root, snapshot)
    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(root), **kwargs)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    except OSError as exc:
        raise SddError(f"não foi possível abrir a porta {port}: {exc}") from exc
    result["url"] = f"http://127.0.0.1:{server.server_port}/_sdd/dashboard/"
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace-root", type=Path)
    parser.add_argument("--project", help="limita o snapshot a um projeto")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("show", help="imprime o snapshot JSON; não grava")
    sub.add_parser("build", help="gera _sdd/dashboard/index.html e project-status.json")
    serve_parser = sub.add_parser("serve", help="gera e serve o dashboard somente em localhost")
    serve_parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    root = (args.workspace_root or find_workspace_root(Path.cwd()) or Path.cwd()).resolve()
    try:
        snapshot = build_snapshot(root, args.project)
        if args.command == "show":
            emit(snapshot)
        elif args.command == "build":
            emit(write_dashboard(root, snapshot))
        else:
            serve(root, snapshot, args.port)
    except (SddError, OSError) as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
