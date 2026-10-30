# 06 — `sprint-status.yaml` e máquina de estados

- **Pedido:** "quero implementar sprint-status.yaml, em que cada story passa por backlog, ready-for-dev, in-progress, review e done. Nas suas skills, a situação só existe no nível do escopo e como checkbox no project.md." (linha 11)
- **Tamanho:** M
- **Depende de:** 03 (scripts) — mas o formato pode ser fechado antes
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Como o BMAD v6 faz
Um `sprint-status.yaml` por projeto, gerado pelo `sprint-planning` a partir dos épicos, e atualizado por cada workflow:
```yaml
generated: 2026-10-30
project: Nome
tracking_system: file-system
story_location: ...
development_status:
  epic-1: in-progress
  1-1-autenticacao: done
  1-2-cadastro-de-conta: review
  1-3-recuperar-senha: ready-for-dev
  epic-1-retrospective: optional
```
- Épico: `backlog → in-progress → done`
- Story: `backlog → ready-for-dev → in-progress → review → done`
- Retrospectiva: `optional ↔ done`

### Como está hoje (confirmado)
- `project.md`: checkbox por fase (Discovery, Escopo, ..., Produção).
- `workspace.md`: coluna Situação por projeto.
- `execution-plan.md`: campo Status do plano inteiro.
- Nenhum estado por tarefa.

## Objetivo

Um arquivo de estado por projeto, legível por pessoa e por script, que é a **fonte única** do andamento da entrega.

## Proposta

1. **Local:** `docs/{projeto}/implementacao/sprint-status.yaml` (um por projeto, cobrindo todos os escopos).
2. **Formato** (compatível com o v6, com campos a mais para o nosso contexto):
   ```yaml
   version: 1
   project: gestao-de-estoque
   updated_at: 2026-10-30
   tracking_system: file-system        # ou redmine / jira (espelho)
   epics:
     epic-1:
       title: Cadastro de produtos
       escopo: gestao-de-produtos      # pasta em docs/{projeto}/escopo/
       status: in-progress
       retrospective: optional
       stories:
         1-1-criar-produto:
           status: review
           repositories: [estoque-api, estoque-web]   # 13
           file: stories/1-1-criar-produto.md
           external_id: "#4321"         # opcional (Redmine/Jira)
   ```
   Decidir entre esse formato aninhado (mais legível) e o plano do v6 (`development_status` chave → valor, mais fácil de editar à mão). Recomendação: aninhado, com o script validando.
3. **Transições permitidas** (validadas pelo `status.py`, 03):
   | De | Para | Quem move |
   |----|------|-----------|
   | `backlog` | `ready-for-dev` | `create-story` (08) |
   | `ready-for-dev` | `in-progress` | `dev-story` (09), ao começar |
   | `in-progress` | `review` | `dev-story`, ao terminar com testes passando |
   | `review` | `done` | `code-review` (10), sem achados bloqueantes — ou pessoa |
   | `review` | `in-progress` | `code-review`, com achados a corrigir |
   | qualquer | `backlog` / `dropped` | `correct-course` (12) ou pessoa |
   Épico: `backlog → in-progress` quando a primeira story sai do backlog; `in-progress → done` só quando todas as stories estão `done`/`dropped` (sugerido pela retrospectiva, 11).
   Avaliar acrescentar `dropped` (vem da v7) para stories canceladas sem apagar o histórico.
4. **Status também no frontmatter da story** (`status:`), mantido em sincronia; `status.py check` acusa divergência e o `sprint-status.yaml` vence.
5. **Derivados**: ao mudar estado, as skills atualizam o `project.md` (fase Desenvolvimento) e a coluna Situação do `workspace.md` com um resumo (ex.: "Desenvolvimento — épico 1: 3/5 done").
6. **Skill `sprint-planning`** (ou modo do `plan-epics`, 07): gera/atualiza o arquivo a partir dos épicos, **sem rebaixar** estados existentes; mostra o quadro (por épico, quantas stories em cada estado) e a próxima story.

## Decisões em aberto

- Formato aninhado ou chave → valor (v6). aninhado, com o script validando.
- Incluir `dropped` e `blocked`. Sim
- Um arquivo por projeto (recomendado) ou um por escopo. Fazer o recomendado
- Espelhamento com Redmine (já existe a skill `execution-plan-to-redmine` fora do marketplace): fora do escopo agora, mas reservar `external_id`. Nao

## Critérios de aceite

- [ ] `references/sprint-status.md` com formato, estados, transições e exemplo — referenciado por todas as skills do fluxo.
- [ ] `status.py` (03) valida e aplica as transições.
- [ ] `sprint-planning` gera o arquivo a partir de épicos de exemplo e é idempotente.
- [ ] `sdd status` (01) mostra o quadro por épico.

## Arquivos impactados

`plugins/<delivery>/skills/sprint-planning/**` (novo), `plugins/sdd/scripts/status.py`, `CLAUDE.md` e `0.0 - contexto-projeto-skills.md` (estrutura `docs/{projeto}/implementacao/`).

## Resultado (30/10/2026)

- **Plugin `delivery`** criado e registrado no marketplace e em `sdd-setup/modules/delivery.toml`. Por enquanto o registro não tem perguntas: `review_depth` e `auto_mode` entram com as skills 09 e 10.
- **Skill `sprint-planning`**, com três modos:
  - **Sincronizar**: prévia com `--dry-run`, decisão sobre órfãos, gravação, conferência dos nomes de repositório com o `repositorios.md`, atualização do `project.md` e da Situação do `workspace.md`.
  - **Quadro**: tabela por épico e próxima ação.
  - **Mudar estado**: com confirmação; `--force` só a pedido explícito.
  - Tem caminho sem `uv`.
- **`status.py sync`** lê o frontmatter de `implementacao/epicos/epic-N-slug.md`, com `id`, `title`, `escopo` e `stories: [{id, title, repositories}]`. A tarefa 07 (`plan-epics`) precisa gravar esse formato, descrito em `sdd-setup/references/sprint-status.md`.
  - Acrescenta itens novos em `backlog` e atualiza título, escopo, repositórios e ordem.
  - Nunca mexe em `status`/`file` do que já existe e nunca remove: o que sumiu dos épicos vira `orphans`.
  - Rodar de novo sem mudanças devolve `changed: false`.
- **`show`** ganhou o campo `situacao` (ex.: `Desenvolvimento — epic-1: 0/2 done`), usado na coluna Situação do `workspace.md`.
- **Decisões aplicadas:** formato aninhado validado pelo script, `blocked` e `dropped` incluídos, um arquivo por projeto, sem `tracking_system`/`external_id`.

**Critérios de aceite:**
- A referência existe.
- O `status.py` valida e aplica as transições.
- O `sync` é idempotente (31 testes).
- O quadro por épico aparece no `sdd-setup` pelo `workspace.py`.
