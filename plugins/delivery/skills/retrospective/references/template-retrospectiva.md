# Template: `implementacao/retrospectivas/epic-{n}-{AAAA-MM-DD}.md`

Todo achado cita a fonte: story (`{id}`, seção), bloco de revisão (data, rodada), commit (repositório, hash) ou proposta de mudança. Sem fonte, não entra.

```markdown
---
epic: epic-{n}
date: {AAAA-MM-DD}
verdict: accepted | accepted-with-open-items | rejected
stories: {done}/{total} done, {dropped} dropped
---

# Retrospectiva — Épico {n}: {título}

## Evidências

| Story | Estado | Rodadas de revisão | Achados (h/m/l) | Correções abertas | Desvios | Commits |
|-------|--------|--------------------|-----------------|-------------------|---------|---------|
| {id} | done | 2 | 1/1/1 | 1 | sim | api: 4 |

Mudanças de rumo no período: {mudancas/... ou "nenhuma"}.
Fontes não lidas: {ex.: git (repositório não disponível), ou "nenhuma"}.

## Pronto quando

| Verificação do épico | Situação | Evidência |
|----------------------|----------|-----------|
| {item do "Pronto quando"} | atendida / não atendida / sem evidência | {story/teste/revisão} |

## O que funcionou

- {achado} — fonte: {story 1-1, Registro 19/10}

## O que não funcionou

- {achado} — fonte: {story 1-1, revisão rodada 1: A1 high}

## Surpresas

- {o que ninguém previu no plano} — fonte: {...}

## Itens da retrospectiva anterior

| Item | Situação | Evidência |
|------|----------|-----------|
| {texto} | feito / não feito / não se aplica | {...} |

{Primeira retrospectiva do projeto: "Não há retrospectiva anterior."}

## Reconciliação com a especificação e a arquitetura

| O que foi implementado diferente | Onde está documentado hoje | Proposta | Aprovada? |
|----------------------------------|----------------------------|----------|-----------|
| {validação no domínio, não na API} | spec 1.2 / arquitetura | {atualizar spec-functional / ADR via arch-adr} | {sim/não/pendente} |

## Preparação do próximo épico

- **Dependências:** {o que o próximo épico precisa deste}
- **Riscos:** {...}
- **Ajustes nas stories em backlog:** {story: o que muda — via plan-epics (Atualizar) ou correct-course}

## Veredito

**{accepted | accepted-with-open-items | rejected}** — {justificativa em 2–3 frases, citando o "Pronto quando"}.

## Itens de ação

- [ ] {ação} — tipo: {story nova | ajuste no épico {n+1} | processo} — responsável: {quem ou "a definir"}
```

## Veredito

| Veredito | Quando |
|----------|--------|
| `accepted` | Todas as stories `done`/`dropped`, todo "Pronto quando" atendido com evidência, sem correção `high`/`medium` aberta |
| `accepted-with-open-items` | O resultado do épico foi entregue, mas há itens que não bloqueiam (correção `low` aberta, adiados, reconciliação pendente) |
| `rejected` | Story aberta, "Pronto quando" não atendido ou sem evidência, ou correção `high`/`medium` aberta. O usuário pode sobrescrever; registre o motivo |
