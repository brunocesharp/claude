# Template: `implementacao/stories/{id}.md`

O arquivo da story é a **única fonte de verdade** da implementação: o `dev-story` lê só ele (e os arquivos de código). Tudo o que o desenvolvimento precisa saber está aqui, copiado ou referenciado com caminho e seção.

Os títulos `## ...` são **fixos e em português**, em qualquer `language.documents`: são lidos pelo `story.py` e pelas skills do fluxo. O conteúdo segue o idioma configurado.

```markdown
---
id: {n}-{m}-{slug}
epic: epic-{n}
status: ready-for-dev
title: {título curto, sem prefixo}
size: M
kind: story
covers: ["1.3", "RN-1.2"]
repositories: [{repo-api}, {repo-web}]
branch: feat/{n}-{m}-{slug}
depends_on: [{n}-{m-1}-{slug}]
checkpoint: false
created_at: {AAAA-MM-DD}
---

# Story {n}.{m}: {[TASK] Desenvolver - [{Módulo}] - }{Título}

## História

**Como** {ator}, **quero** {ação}, **para** {benefício}.

## Critérios de aceite

- **CA-1** — {o que precisa ser verdade, em uma frase}. Origem: cenário {1.3}.

  ```gherkin
  {texto literal do cenário, copiado com epics.py spec}
  ```

- **CA-2** — {regra}. Origem: {RN-1.2} — "{texto literal da regra}".

## Tarefas

- [ ] **T1** — {tarefa, na ordem de execução} (CA-1)
  - [ ] {subtarefa}
- [ ] **T2** — Testes: {o que testar e em que nível} (CA-1, CA-2)

## Repositórios

| Repositório | Caminho local | Branch | O que muda |
|-------------|---------------|--------|------------|
| {repo-api} | {D:\repos\repo-api ou "a definir"} | feat/{n}-{m}-{slug} | {endpoint GET /x paginado} |
| {repo-web} | {...} | feat/{n}-{m}-{slug} | {tela de lista} |

**Ordem:** {repo-api} antes de {repo-web} (provedor antes do consumidor).

### Contratos

| Contrato | Provedor → consumidor | Mudança | Compatível? | Estratégia |
|----------|-----------------------|---------|-------------|------------|
| GET /api/x | api → web | novo endpoint | sim (só acrescenta) | — |

{Um repositório só e sem contrato: "Um repositório ({nome}); sem contratos alterados." e apague a tabela.}

## Contexto para o desenvolvimento

### Arquitetura e decisões

- Contêineres: {API (.NET), SPA (Angular)} — `docs/{projeto}/arquitetura/arquitetura.md#{seção}`
- {ADR-003 — Paginação por cursor: resumo da decisão em uma frase} — `docs/{projeto}/arquitetura/decisoes/ADR-003-paginacao.md`

### Arquivos a criar ou alterar

| Repositório | Arquivo | Ação | Por quê |
|-------------|---------|------|---------|
| {repo-api} | `src/X.Application/Produtos/Queries/...` | criar | {query paginada} |
| {repo-api} | `src/X.Presentation/Controllers/ProdutosController.cs` | alterar | {novo endpoint} |

### Padrões e skills de código

- {Query paginada: `architecture-feature` (query-template, seção Paginação). Seguir o padrão já usado em `ListarClientesQuery`.}
- {Lista Angular: `angular-feature-layer` (feature-pages).}

### Regras de negócio

{Regras do domínio que valem aqui e não estão nos critérios (de `docs/{projeto}/business/`), ou "Nenhuma além dos critérios".}

### Aprendizados da story anterior

{Da story {id anterior}: decisões do Registro do desenvolvimento e achados da Revisão que afetam esta. Primeira story: "Primeira story do épico."}

### Referências

- `docs/{projeto}/especificacao/{escopo}/spec-functional.md#feature-1` — feature completa
- `docs/{projeto}/implementacao/epicos/epic-{n}-{slug}.md` — épico

### Decisões em aberto

{Pontos "decidir na story" do épico, com as opções. Ou "Nenhuma".}

## Fora desta story

- {o que parece fazer parte mas fica para outra story: qual}

## Registro do desenvolvimento

_Preenchido pelo `dev-story`: modelo usado, decisões tomadas, desvios do plano, dúvidas e pendências._

## Arquivos alterados

_Preenchido pelo `dev-story`, agrupado por repositório._

## Revisão

_Blocos datados do `story-review`._

## Histórico

| Data | De → para | Por | Observação |
|------|-----------|-----|------------|
| {DD/MM/AAAA} | backlog → ready-for-dev | create-story | Story criada |
```

## Regras

- **Critérios de aceite:** um `**CA-N**` por cenário ou regra coberta (pode agrupar regras do mesmo cenário). Todo id de `covers` aparece no texto dos critérios. O texto do cenário/regra é **copiado literalmente** (`epics.py spec`), nunca reescrito.
- **Tarefas:** checklist na ordem de execução; toda tarefa cita os CA que atende `(CA-1, CA-2)`; todo CA tem ao menos uma tarefa; testes são tarefas, não um anexo. Com vários repositórios, as tarefas do provedor vêm antes.
- **Copiar x referenciar:** copie critérios, cenários, regras e decisões (o que o dev não pode interpretar errado); referencie o resto com caminho e seção. Toda referência a `docs/...` precisa existir.
- **Branch:** `feat/{id}` — o mesmo nome em todos os repositórios da story (siga a convenção do repositório se houver outra).
- **Spike** (`kind: spike`): a História é a pergunta a responder; os CA são o que conta como resposta (decisão registrada, ADR, protótipo descartável); `covers` pode ficar vazio.
- **Nada de "a definir" nos critérios:** se um critério depende de decisão, ela vai em Decisões em aberto e o critério diz o que vale em cada opção — ou a story volta para o `plan-epics`/`correct-course`.
