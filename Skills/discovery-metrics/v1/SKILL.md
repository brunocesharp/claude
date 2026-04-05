---
name: discovery-metrics
description: Conduz a definição de métricas de sucesso durante o discovery de um projeto. Use esta skill sempre que o usuário mencionar "métricas do projeto", "como vamos medir o sucesso", "KPIs", "OKRs", "critérios de sucesso", "como saber se deu certo", "indicadores de resultado", "metas do projeto" ou qualquer variação que indique a necessidade de definir o que significa sucesso antes de construir. Use proativamente sempre que o time estiver prestes a entrar em desenvolvimento sem ter definido como vai medir o impacto do projeto.
---

# Discovery Metrics

Skill responsável por conduzir a definição de métricas de sucesso e gerar o documento `success-metrics.md`.

Baseada no framework **OKR** (Objectives and Key Results) e nas práticas de **North Star Metric** (produto) e **HEART** (Google, para métricas de UX).

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.
- **Se não existir**: sugira iniciar com `discovery-init`.
- **Se existir**: leia também `vision.md` e `opportunity.md` se disponíveis — eles definem o problema que as métricas devem refletir.

---

## Conceito rápido (use se necessário)

> "Definir métricas agora, antes de construir, nos protege de dois erros comuns: construir a coisa certa e não saber medir, ou construir a coisa errada e só descobrir depois. O objetivo é chegar em indicadores que nos digam claramente se o projeto está gerando o impacto esperado."

---

## Fluxo de execução

### Bloco 1 — Objetivo Central

> "Se esse projeto der certo, qual é a principal mudança que queremos ver? Pense em termos de resultado para o usuário ou para o negócio, não em funcionalidades entregues."

Perguntas de aprofundamento:
- "Como seria o sucesso desse projeto daqui a 6 meses?"
- "O que mudaria no dia a dia dos usuários ou da empresa se esse sistema funcionar bem?"
- "Existe algum número ou indicador que hoje está ruim e queremos melhorar?"

---

### Bloco 2 — North Star Metric

> "Existe uma métrica principal — a mais importante de todas — que captura o valor central que esse sistema entrega?"

Perguntas de apoio:
- "Se você pudesse acompanhar apenas um número para saber se o projeto está indo bem, qual seria?"
- "Essa métrica reflete valor real para o usuário ou só para o negócio?"

---

### Bloco 3 — Métricas de Negócio

> "Quais indicadores de negócio esse projeto deve mover?"

Exemplos para inspirar (adapte ao contexto):
- Redução de custo operacional
- Aumento de receita ou conversão
- Redução de tempo de processo
- Aumento de capacidade ou volume
- Redução de erros ou retrabalho

---

### Bloco 4 — Métricas de Produto/Usuário

> "Como vamos medir se os usuários estão adotando e se beneficiando do sistema?"

Use o framework HEART como guia:
- **Happiness** — satisfação do usuário (NPS, CSAT)
- **Engagement** — uso ativo (frequência, sessões, features usadas)
- **Adoption** — novos usuários ou expansão
- **Retention** — usuários que continuam usando
- **Task Success** — taxa de conclusão das tarefas principais

---

### Bloco 5 — Critérios de Aceitação do Projeto

> "Independente de métricas contínuas, quais são os critérios mínimos para considerar o projeto bem-sucedido no lançamento?"

Perguntas:
- "O que precisaria estar funcionando no dia do go-live para considerar o lançamento um sucesso?"
- "Existe algum requisito não negociável de desempenho, disponibilidade ou segurança?"
- "Quais são os critérios de homologação que os stakeholders vão exigir?"

---

### Bloco 6 — Linha de Base e Metas

> "Para as métricas mais importantes, temos algum valor atual (baseline) para comparar?"

Perguntas:
- "Sabemos como está hoje o indicador que queremos melhorar?"
- "Qual seria uma meta realista para os primeiros 3 meses após o lançamento?"
- "Quem vai acompanhar essas métricas após o lançamento?"

---

## Gerar o documento `success-metrics.md`

Salve em:
```
docs/{nome-do-projeto}/discovery/success-metrics.md
```

Template:

```markdown
# Métricas de Sucesso — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}

---

## Objetivo Central

{Declaração clara do resultado esperado com o projeto}

---

## North Star Metric

> A métrica mais importante — aquela que melhor representa o valor entregue.

**Métrica:** {nome da métrica}
**Definição:** {como é calculada}
**Responsável:** {quem acompanha}

---

## Métricas de Negócio

| Métrica | Baseline atual | Meta (3 meses) | Meta (6 meses) | Responsável |
|---|---|---|---|---|
| {métrica} | {valor atual ou "a medir"} | {meta} | {meta} | {responsável} |

---

## Métricas de Produto e Usuário

| Categoria (HEART) | Métrica | Baseline | Meta | Como medir |
|---|---|---|---|---|
| {Happiness/Engagement/...} | {métrica} | {valor} | {meta} | {ferramenta/método} |

---

## Critérios de Aceitação do Lançamento

> O que precisa ser verdade no go-live para considerar o lançamento bem-sucedido.

- [ ] {critério 1}
- [ ] {critério 2}
- [ ] {critério 3}

---

## Critérios de Sucesso do Projeto (longo prazo)

> O que define sucesso depois de 6 meses em produção.

- {critério 1}
- {critério 2}

---

## Riscos de Medição

{O que pode dificultar o acompanhamento das métricas — falta de dados, sistemas legados, etc.}
```

---

## Após gerar o documento

> "O `success-metrics.md` foi salvo em `docs/{nome-do-projeto}/discovery/`. Com as métricas definidas, o discovery está bem fundamentado. Os próximos passos são:
> - **Gerar o escopo** — consolidar todos os documentos de discovery em um escopo formal
> - **Iniciar a especificação** — detalhar as regras de negócio"

---

## Regras importantes

- Métricas vagas como "aumentar a satisfação" não são úteis — sempre empurre para algo mensurável: "aumentar o NPS de 32 para 50 em 6 meses".
- Se o usuário não tiver baseline, registre "a medir" — mas sinalize que estabelecer o baseline deve ser uma das primeiras ações pós-lançamento.
- Evite métricas de vaidade (ex: número de cadastros sem considerar ativação). Questione: "Essa métrica reflete valor real ou apenas atividade?"
- Lembre que métricas de negócio e métricas de usuário devem estar alinhadas — se uma sobe enquanto a outra cai, algo está errado.
