---
name: discovery-metrics
description: Conduz a definição de métricas de sucesso durante o discovery, gerando o documento success-metrics.md. Baseada em OKR, North Star Metric e HEART. Use quando o usuário mencionar "métricas", "KPIs", "OKRs", "critérios de sucesso", "como medir", "indicadores", "metas", "ROI", "impacto do projeto", "dashboard de acompanhamento", "baseline", "como saber se deu certo", "definir sucesso", "o que significa dar certo", "North Star". Requer discovery-init. NÃO use para visão geral (use discovery-vision), dores e oportunidades (use discovery-opportunity), hipóteses (use discovery-assumptions) ou stakeholders (use discovery-stakeholders). Esta skill foca em COMO MEDIR sucesso, não em definir o que construir.
metadata:
  author: Equipe de Discovery
  version: 1.1.0
  category: discovery
  depends-on: discovery-init
  recommended-after: discovery-stakeholders
  output: docs/{projeto}/discovery/success-metrics.md
  frameworks: OKR, North Star Metric, HEART, AARRR
---

# Discovery Metrics

Conduz a definição de métricas de sucesso e gera o documento `success-metrics.md`.

Para detalhes sobre os frameworks (OKR, North Star, HEART, AARRR), consulte `references/frameworks.md`.

Para exemplos de métricas por tipo de projeto, consulte `references/metrics-catalog.md`.

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.

- **Se não existir**: pergunte "Quer que eu inicie o projeto agora usando a skill discovery-init?"
- **Se existir**: leia também `vision.md`, `opportunity.md` e `assumptions.md` — eles definem o problema e hipóteses que as métricas devem validar.

---

## Conceito Rápido

Use se o usuário não for familiarizado:

> "Definir métricas antes de construir nos protege de dois erros: construir a coisa certa e não saber medir, ou construir a coisa errada e só descobrir depois. O objetivo é ter indicadores que digam claramente se o projeto está gerando impacto."

---

## Fluxo de Execução

Conduza a conversa em blocos temáticos. Espere a resposta de cada bloco antes de avançar.

### Bloco 1 — Objetivo Central

> "Se esse projeto der certo, qual é a principal mudança que queremos ver? Pense em resultado, não em funcionalidades."

Perguntas:
- "Como seria o sucesso daqui a 6 meses?"
- "O que mudaria no dia a dia dos usuários ou da empresa?"
- "Existe algum número que hoje está ruim e queremos melhorar?"

**Validação:**
- O objetivo deve ser um RESULTADO, não uma entrega
- Se usuário falar em funcionalidades, redirecione: "Isso é o que vamos construir. O que muda quando isso existir?"

---

### Bloco 2 — North Star Metric

> "Existe UMA métrica principal que captura o valor central desse sistema?"

Perguntas:
- "Se pudesse acompanhar apenas um número, qual seria?"
- "Essa métrica reflete valor para o usuário ou só para o negócio?"

**Validação:**
- Deve haver UMA métrica, não várias
- Se houver mais de uma "principal", force priorização
- Deve refletir valor para USUÁRIO, não só atividade

Para exemplos de North Star por tipo de projeto, consulte `references/metrics-catalog.md`.

---

### Bloco 3 — Métricas de Negócio

> "Quais indicadores de negócio esse projeto deve mover?"

Exemplos para inspirar:
- Redução de custo operacional
- Aumento de receita ou conversão
- Redução de tempo de processo
- Aumento de capacidade/volume
- Redução de erros ou retrabalho

**Validação:**
- Pelo menos 2-3 métricas de negócio
- Devem ser mensuráveis, não "melhorar eficiência"
- Pergunte: "Como vamos medir isso? Temos os dados?"

---

### Bloco 4 — Métricas de Produto/Usuário

> "Como vamos medir se os usuários estão adotando e se beneficiando?"

Use o framework HEART:
- **Happiness** — satisfação (NPS, CSAT)
- **Engagement** — uso ativo (frequência, sessões)
- **Adoption** — novos usuários/expansão
- **Retention** — usuários que continuam usando
- **Task Success** — conclusão das tarefas principais

**Validação:**
- Pelo menos 2-3 métricas de usuário
- Evite métricas de vaidade (cadastros sem ativação)
- Pergunte: "Isso reflete valor real ou só atividade?"

---

### Bloco 5 — Critérios de Aceitação

> "Quais são os critérios mínimos para considerar o lançamento bem-sucedido?"

Perguntas:
- "O que precisa funcionar no go-live?"
- "Existe requisito de desempenho, disponibilidade ou segurança?"
- "Quais critérios os stakeholders vão exigir?"

**Validação:**
- Critérios devem ser verificáveis (sim/não)
- Não confundir com métricas contínuas

---

### Bloco 6 — Baseline e Metas

> "Para as métricas mais importantes, temos valor atual para comparar?"

Perguntas:
- "Sabemos como está hoje o indicador que queremos melhorar?"
- "Qual seria uma meta realista para 3 meses após o lançamento?"
- "Quem vai acompanhar essas métricas?"

Para técnicas de definição de baseline e metas, consulte `references/baseline-and-goals.md`.

**Validação:**
- Se não houver baseline, registre "a medir" mas sinalize como ação
- Metas devem ser específicas e com prazo

---

## Gerar o Documento

Após coletar as informações, gere `docs/{nome-do-projeto}/discovery/success-metrics.md` usando o template em `references/template-metrics.md`.

---

## Após Gerar o Documento

1. **Salve o arquivo** em `docs/{nome-do-projeto}/discovery/success-metrics.md`

2. **Informe o usuário:**

> "O `success-metrics.md` foi salvo. Com as métricas definidas, o discovery está fundamentado. Próximos passos:
>
> - **Gerar o escopo** — consolidar todos os documentos em um escopo formal
> - **Iniciar a especificação** — detalhar regras de negócio
>
> Qual faz mais sentido agora?"

---

## Regras Importantes

### Comportamento Obrigatório

- **Empurre para mensurável** — "aumentar satisfação" → "aumentar NPS de 32 para 50"
- **Questione métricas de vaidade** — "Isso reflete valor real ou só atividade?"
- **Registre baseline ausente** — marque "a medir" mas sinalize como ação prioritária
- **Alinhe negócio e usuário** — se uma sobe e outra cai, algo está errado

### O Que NÃO Fazer

- Não aceite métricas vagas ("melhorar a experiência")
- Não permita múltiplas North Star Metrics
- Não ignore a conexão com hipóteses do `assumptions.md`
- Não defina metas sem considerar baseline
- Não esqueça de definir QUEM vai acompanhar

### Adaptação de Tom

- **Para PMs:** Foque em métricas de produto e usuário
- **Para devs/tech leads:** Destaque métricas técnicas (performance, disponibilidade)
- **Para founders/executivos:** Enfatize métricas de negócio e ROI

---

## Troubleshooting

Para problemas comuns, consulte `references/troubleshooting.md`.

Resumo dos mais frequentes:
- **Usuário quer várias North Star** → force priorização: "Se só pudesse uma?"
- **Todas são métricas de vaidade** → "Essa métrica indica valor real para o usuário?"
- **Não existe baseline** → registre como ação prioritária pós-lançamento
- **Métricas impossíveis de medir** → discuta instrumentação ou proxies

---

## Exemplos

Para exemplos detalhados de uso, consulte `references/examples.md`.
