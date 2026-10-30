# Template: `implementacao/mudancas/{AAAA-MM-DD}-{slug}.md`

Proposta de mudança de rumo (*Sprint Change Proposal* do BMAD v6). Nada é aplicado antes de `status: aprovada`.

```markdown
---
date: {AAAA-MM-DD}
slug: {slug}
scope: menor | moderado | maior
status: proposta | aprovada | aplicada | encaminhada | rejeitada
trigger: {dev-story | story-review | retrospective | usuário}
epics: [epic-{n}]
stories: [{id}, {id}]
---

# Mudança de rumo: {título curto}

## Gatilho

{O que aconteceu, quando, quem levantou. Ex.: "Na story 1-2, o dev-story parou: a spec pede paginação de 20 itens, o ADR-003 exige cursor para listas grandes e a story não diz qual vale."}

**Evidência:** {story e seção, bloco de revisão, cenário da spec, mensagem do usuário}

## Impacto

| Artefato | Afetado? | Como |
|----------|----------|------|
| Especificação (`especificacao/{escopo}/spec-functional.md`) | sim/não | {cenário 1.3 muda o "Então"} |
| Escopo | sim/não | |
| Arquitetura / ADRs | sim/não | |
| Épicos | sim/não | {epic-1: story nova, reordenar} |
| Contratos entre repositórios | sim/não | {GET /api/produtos muda o DTO — incompatível} |

### Stories

| Story | Estado | Efeito | Ação proposta |
|-------|--------|--------|---------------|
| {id} | done | já entregue com o comportamento antigo | story de ajuste {novo id} |
| {id} | in-progress | critério CA-1 muda | voltar a backlog e regenerar com create-story |
| {id} | ready-for-dev | critério muda | voltar a backlog e regenerar |
| {id} | backlog | covers muda | ajustar no épico |

## Classificação

**{menor | moderado | maior}** — {por quê, pela tabela de classificação}.

## Opções

1. **{opção}** — {o que muda; prós; contras; esforço P/M/G}
2. **{opção}** — ...

**Recomendação:** opção {n}, porque {...}.

## Edições propostas

### {arquivo}
**Antes:**
> {trecho}

**Depois:**
> {trecho}

{Uma subseção por arquivo. Para documentos de skill dona (spec, arquitetura, ADR), descreva a mudança e indique a skill: as edições são feitas por ela.}

## Efeito no quadro (`sprint-status.yaml`)

| Story | De → para | Comando |
|-------|-----------|---------|
| {id} | in-progress → backlog | `status.py set {id} backlog` |
| {id} | backlog → dropped | `status.py set {id} dropped` |
| {novo id} | (nova) → backlog | épico + `status.py sync` |

## Riscos

- {para o que já está done, para contratos já publicados, para o prazo}

## Aprovação e aplicação

| Data | Evento | Por |
|------|--------|-----|
| {data} | Proposta criada | correct-course |
```

## Tabela de classificação

| Escopo | Exemplos | Quem decide | O que muda |
|--------|----------|-------------|------------|
| **menor** | Esclarecer ou corrigir um critério sem mudar o comportamento prometido; detalhe técnico que a story não previu | Dev (o usuário confirma) | Arquivo da story (Histórico + Decisões) |
| **moderado** | Story nova, divisão, junção, reordenação, cancelamento; critério diferente numa story ainda não `done`; mudança de contrato compatível | Responsável pelo backlog | Épicos, stories, `sprint-status.yaml` |
| **maior** | Regra de negócio nova ou diferente, cenário novo/removido, contêiner ou sistema externo novo, mudança de escopo, contrato incompatível sem estratégia | PO / arquiteto | Spec, escopo, arquitetura/ADR — **encaminhado** às skills donas — e depois épicos e stories |
