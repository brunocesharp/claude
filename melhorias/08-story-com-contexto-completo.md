# 08 — Um arquivo por story, com contexto completo

- **Pedido:** "uma spec por story" (linha 8) e "Um arquivo por tarefa com contexto completo" (linha 12)
- **Tamanho:** G
- **Depende de:** 06, 07
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Como o BMAD v6 faz
- `create-story` pega a próxima story do `sprint-status.yaml` e gera o **story file** com tudo o que o dev precisa: user story, critérios de aceite, tarefas/subtarefas mapeadas para os critérios, **Dev Notes** (trechos relevantes da arquitetura, padrões, arquivos a criar/alterar, aprendizados da story anterior, referências com caminho e seção), e seções que o dev preenche (Dev Agent Record: modelo usado, log de debug, notas de conclusão, **File List**, Change Log).
- A story vai para `ready-for-dev`. O dev **não precisa ler** PRD nem arquitetura: o story file é autossuficiente.
- O story file é gerado na hora (just-in-time), depois que a story anterior terminou, para incorporar o que se aprendeu.

### Como está hoje
- Não há arquivo por tarefa. As tarefas são linhas de tabela no `execution-plan.md`, sem critérios de aceite próprios nem contexto técnico.

## Objetivo

Skill `create-story` que gera, para a próxima story, um arquivo autossuficiente — a **única fonte de verdade** para a implementação (09).

## Proposta

1. **Skill `create-story`** (plugin de entrega). Entrada: projeto + (opcional) ID da story; sem ID, pega a primeira `backlog` cujo pré-requisito está `done` (via `status.py next`).
2. **Coleta de contexto** (o trabalho pesado fica aqui, não no dev):
   - épico e story (07); cenários BDD citados (texto copiado, não só o link);
   - arquitetura: contêineres/componentes tocados, ADRs aplicáveis (resumo + link);
   - repositório(s) e caminhos (13); stack e convenções (skills `architecture-*`/`angular-*` que se aplicam, com o que cada uma vai gerar);
   - código existente: arquivos a alterar e padrões já usados no repositório (lê o código quando o caminho local existir);
   - **aprendizados da story anterior** (Dev Notes, achados da revisão) e regras de negócio do `business-docs`, se houver.
3. **Template** (`docs/{projeto}/implementacao/stories/{n}-{m}-{slug}.md`):
   ```markdown
   ---
   id: 1-2-cadastro-de-conta
   epic: epic-1
   status: ready-for-dev
   repositories: [x-api, x-web]
   branch: feat/1-2-cadastro-de-conta
   ---
   # Story 1.2: Cadastro de conta
   ## História            (Como / quero / para)
   ## Critérios de aceite  (numerados; cada um com o cenário BDD de origem, texto incluído)
   ## Tarefas              (- [ ] tarefa (CA 1, 2) / subtarefas; inclui testes)
   ## Contexto para o desenvolvimento
   ### Arquitetura e decisões   ### Arquivos a criar/alterar   ### Padrões e skills de código
   ### Aprendizados da story anterior   ### Referências (caminho#seção)
   ## Fora desta story
   ## Registro do desenvolvimento   (preenchido no 09: modelo, decisões, log, notas)
   ## Arquivos alterados            (preenchido no 09: por repositório)
   ## Revisão                       (preenchido no 10: blocos datados)
   ## Histórico                     (data, de → para, quem)
   ```
4. **Validação antes de marcar `ready-for-dev`**: todo critério de aceite tem ao menos uma tarefa; toda referência existe; nada contradiz ADR aceito; tamanho cabe numa sessão (senão propõe dividir — e atualiza o épico e o status).
5. **Estado**: `backlog → ready-for-dev` no `sprint-status.yaml` e no frontmatter.
6. **Just-in-time**: por padrão gera uma story por vez; opção de gerar as N próximas, avisando que perdem os aprendizados das anteriores.

## Decisões em aberto

- O que o pedido chama de "tarefa" é a **story** (recomendado — evita dois níveis de arquivo) ou cada tarefa dentro da story também vira arquivo? Recomendação: um arquivo por story; tarefas são checklist dentro dele. Fazer o recomendado
- Copiar trechos (autossuficiente, mas duplica) ou só referenciar (enxuto, mas o dev precisa abrir outros arquivos). Recomendação: copiar critérios/cenários e decisões; referenciar o resto com caminho e seção. fazer o recomendado
- Nomenclatura `[TASK]` no título da story. Sim

## Critérios de aceite

- [ ] Skill com `references/template-story.md` e checklist de validação.
- [ ] Story gerada para o exemplo do 07 é implementável lendo **só** ela (teste: abrir sessão nova e pedir um resumo do que fazer sem outros arquivos).
- [ ] Transição de status feita via `status.py` (ou edição manual descrita).

## Arquivos impactados

`plugins/<delivery>/skills/create-story/**` (novo), `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.

## Resultado (30/10/2026)

- **Skill `create-story`** (plugin `delivery`), com sete passos:
  1. Escolher a story (`next`, dependências, uma por vez).
  2. Juntar o contexto em 8 fontes: épico, spec literal, arquitetura/ADRs, `business/`, repositórios/contratos, código (só leitura), skills de código e story anterior.
  3. Escrever o arquivo.
  4. Validar.
  5. Confirmar com o usuário.
  6. Passar para `ready-for-dev`.
  7. Orientar a sessão nova para o `dev-story`.
- **Template** em `create-story/references/template-story.md`.
  - As seções `##` têm títulos fixos em português, porque são lidas por script.
  - Os critérios seguem o formato `**CA-N**` e as tarefas citam `(CA-N)`.
  - Há uma seção Repositórios, com contratos e ordem (tarefa 13), e branch `feat/{id}`.
- **Scripts novos:**
  - `epics.py spec`: texto literal de cenários e regras, para copiar sem reescrever.
  - `story.py check`: seções, frontmatter, CA ↔ tarefas, `covers` nos critérios, referências `docs/...` existentes, coerência com o `sprint-status`; também conta as tarefas feitas.
  - `status.py attach`: liga o arquivo à story; `ready-for-dev` exige `file`.

**Decisões aplicadas:**
- Um arquivo por story, com as tarefas como checklist.
- Copiar critérios, cenários e decisões; referenciar o resto.
- `[TASK]` no título quando `backlog.prefixes` = `sim`.

**Critérios de aceite:**
- Skill e checklist de validação feitos.
- Transição de status via script, coberta por 42 testes.
- O teste "abrir sessão nova e implementar lendo só a story" depende do `dev-story` (tarefa 09).
