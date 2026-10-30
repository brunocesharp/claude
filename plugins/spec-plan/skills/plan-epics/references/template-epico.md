# Template: `implementacao/epicos/epic-{n}-{slug}.md`

O frontmatter é lido por scripts (`status.py sync`, `epics.py`): siga os nomes de campo exatamente. O corpo é para pessoas e para o `create-story`, que copia dele o contexto de cada story.

```markdown
---
id: epic-{n}
title: {Resultado para o usuário, sem prefixo}
escopo: {pasta do escopo em docs/{projeto}/escopo/}
stories:
  - id: {n}-1-{slug}
    title: {Título curto}
    size: M
    kind: story
    repositories: [{repo}]
    covers: ["{N.M}", "RN-{N.M}"]
    checkpoint: true
  - id: {n}-2-{slug}
    title: {Título curto}
    size: P
    kind: story
    repositories: [{repo}]
    covers: ["{N.M}"]
    depends_on: [{n}-1-{slug}]
---

# Épico {n}: {[FEATURE] [{Módulo}] - }{Título}

## Objetivo

{O que o usuário consegue fazer quando o épico termina, em 2–3 frases. Resultado, não camada.}

## Limites

**Entra:**
- {comportamento}

**Não entra:**
- {comportamento, e onde ele fica: outro épico, outro escopo, fora}

## Pronto quando

- [ ] {verificação objetiva, observável pelo usuário ou por teste}
- [ ] Todos os cenários cobertos abaixo passam em teste automatizado

## Stories (ordem de build)

| # | Story | Tam. | Tipo | Cobre | Depende de | Repositórios | Checkpoint |
|---|-------|------|------|-------|------------|--------------|------------|
| {n}.1 | {[TASK] Desenvolver - [{Módulo}] - }{título} | M | story | 1.1, 1.2, RN-1.1 | — | api, web | sim |
| {n}.2 | {título} | P | story | 1.3 | {n}.1 | api, web | — |

### {n}.1 — {Título}

**Como** {ator}, **quero** {ação}, **para** {benefício}.

- **Critérios de aceite:** cenários {1.1}, {1.2} da especificação; regra {RN-1.1}. {Algo além dos cenários, se houver.}
- **Camadas tocadas:** {Domain (entidade X), Application (command Y), Presentation (endpoint Z), Angular (lista)} — skills: `architecture-entities`, `architecture-feature`, `architecture-controller`.
- **Decisões a tomar na story:** {ponto em aberto marcado "decidir na story", ou "nenhuma"}.
- **Por que checkpoint:** {fundacional/arriscada: define o padrão que as próximas seguem}.

### {n}.2 — {Título}

{mesma estrutura}

## Pontos em aberto

| Ponto | Decisão | Onde fica |
|-------|---------|-----------|
| {pergunta} | resolver agora | {resposta registrada aqui ou no ADR-NNN} |
| {pergunta} | spike | story {n}.x |
| {pergunta} | decidir na story | story {n}.y |

## Cobertura

Gerada por `epics.py coverage --escopo {escopo}` (cenário → stories). Cenário sem story é lacuna.

| Cenário | Título | Stories |
|---------|--------|---------|
| 1.1 | {título} | {n}-1-{slug} |

## Histórico

| Data | Mudança | Motivo |
|------|---------|--------|
| {DD/MM/YYYY} | Criado pelo plan-epics | — |
```

## Regras de preenchimento

- **id e número:** numeração global no projeto. O próximo número vem de `epics.py validate` (`next_epic`). Nunca reaproveite o número de um épico apagado.
- **Ids de story:** `{n}-{m}-{slug}`; `m` segue a ordem de build. Depois que a story existe no `sprint-status.yaml`, o id não muda, mesmo que a ordem mude (reordenar = mudar a posição na lista, não o id).
- **`title` no frontmatter** sem prefixo de backlog; no corpo, com prefixo quando `backlog.prefixes` = `sim` (épico `[FEATURE]`, story `[TASK] Desenvolver`, spike `[TASK] Analisar e especificar`, habilitador `[HT]`).
- **`repositories`:** nomes do `repositorios.md`; com um repositório só, o nome dele (última parte da URL); lista vazia para spike sem código.
- **`size`:** P, M ou G — ver `fatiamento-vertical.md`. Nada maior que G.
- **`covers`:** só ids que existem na spec do escopo (`N.M` e `RN-N.M`). Spike e habilitador podem ficar sem `covers`.
- **`depends_on`:** só stories que vêm antes na ordem de build (de qualquer épico).
- **`checkpoint: true`** nas stories fundacionais ou arriscadas; omita nas demais.
