---
name: sdd-dashboard
description: Consolida a situação dos projetos do workspace e gera um dashboard HTML com portfólio, Kanban, fila de atenção e execuções automáticas. Use quando o usuário pedir "dashboard", "painel do projeto", "visualizar as tarefas", "acompanhar o projeto", "situação dos projetos", "Kanban no VS Code", "abrir o dashboard" ou "atualizar o dashboard". NÃO use para mudar o estado de uma story (use sprint-planning/status.py) nem para explicar o fluxo das skills.
metadata:
  version: 1.0.0
  category: workspace
  output: _sdd/dashboard/index.html, _sdd/dashboard/project-status.json
---

# SDD Dashboard

Gera uma visão somente leitura do workspace. O dashboard não edita stories nem o `sprint-status.yaml`; mudanças de estado continuam passando pelo `status.py`.

## Pré-condição

Localize a raiz do workspace pela pasta `_sdd/`. Se `_sdd/scripts/dashboard.py` não existir ou estiver desatualizado, rode a atualização da skill `sdd-setup` antes de continuar. Não execute o dashboard no repositório dos plugins nem em um repositório de código.

## Modos

| Pedido | Comando | Grava? |
|---|---|---|
| Ver situação no terminal ou obter dados | `show` | Não |
| Gerar ou atualizar o painel | `build` | Sim, somente em `_sdd/dashboard/` |
| Usar dentro do VS Code | `serve` | Atualiza o painel e abre um servidor apenas em localhost |

### Snapshot no terminal

```text
uv run _sdd/scripts/dashboard.py --workspace-root "{workspace}" [--project {slug}] show
```

Resuma projetos, stories por estado, próxima ação e itens da fila de atenção. Não despeje o JSON inteiro na conversa.

### Gerar HTML estático

```text
uv run _sdd/scripts/dashboard.py --workspace-root "{workspace}" [--project {slug}] build
```

Informe os caminhos `html` e `json` devolvidos pelo script. O HTML é autocontido; `project-status.json` é o contrato estável para futuras interfaces.

### Visualizar no VS Code

Inicie em um terminal do VS Code:

```text
uv run _sdd/scripts/dashboard.py --workspace-root "{workspace}" [--project {slug}] serve --port 8765
```

O processo imprime a URL `http://127.0.0.1:8765/` e permanece ativo. Oriente a abrir `Simple Browser: Show` na paleta de comandos do VS Code e colar a URL. Use outra porta se 8765 estiver ocupada. Interromper o terminal encerra o servidor; nada fica exposto fora de localhost.

## Dados consolidados

- `project.md`, `project-config.json` e `workspace.md`: nome, fase e situação.
- `implementacao/sprint-status.yaml`: épicos, stories, progresso e próxima ação.
- `_sdd/criacao-story-recorrente/estado.json` e `_sdd/execucao-recorrente/estado.json`: últimas execuções e falhas.

O painel mostra portfólio, Kanban filtrável, fila de atenção e histórico recente das automações. Story em `review`, `blocked`, quadro inválido ou automação com falha/bloqueio/espera entra na fila de atenção.

## Regras

- Regere o dashboard para refletir mudanças nos arquivos; não há gravação automática em segundo plano.
- Não altere o HTML gerado manualmente: ele será substituído no próximo `build`.
- Não adicione comandos de mudança de estado ao painel. Use `sprint-planning` ou `_sdd/scripts/status.py`.
- Nunca publique o servidor fora de `127.0.0.1`.
- Fale no idioma de `language.conversation`, quando configurado.
