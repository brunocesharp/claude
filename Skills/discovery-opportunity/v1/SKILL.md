---
name: discovery-opportunity
description: Conduz o mapeamento de oportunidades durante o discovery de um projeto. Use esta skill sempre que o usuário mencionar "oportunidades do projeto", "mapear dores", "jobs to be done", "o que o usuário quer fazer", "dores dos usuários", "explorar oportunidades", "mapa de oportunidades" ou qualquer variação que indique a necessidade de entender profundamente as necessidades e motivações dos usuários antes de definir soluções. Use proativamente sempre que a conversa indicar que o time quer entender melhor o problema antes de partir para soluções.
---

# Discovery Opportunity

Skill responsável por conduzir o mapeamento de oportunidades e gerar o documento `opportunity.md`.

Baseada no framework **Opportunity Solution Tree** (Teresa Torres) e na teoria de **Jobs to Be Done** (Christensen/Ulwick).

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.
- **Se não existir**: sugira iniciar com `discovery-init`.
- **Se existir**: leia o arquivo. Se `vision.md` também existir, leia-o para contextualizar melhor as perguntas.

---

## Fluxo de execução

### Bloco 1 — Jobs to Be Done

Explique brevemente o conceito antes de perguntar, se o usuário não for técnico em produto:

> "Vamos pensar no que os usuários estão tentando realizar — não o que o sistema vai fazer, mas o **objetivo real** por trás do uso. Isso nos ajuda a não resolver o problema errado."

Perguntas:
- "Quando um usuário vai usar esse sistema, qual tarefa ou objetivo ele está tentando completar?"
- "Existe mais de um tipo de objetivo dependendo do perfil do usuário?"
- "O que define 'missão cumprida' para esse usuário ao usar o sistema?"

---

### Bloco 2 — Dores e Fricções

> "Agora vamos mapear o que atrapalha o usuário hoje. O que torna essa tarefa difícil, demorada, frustrante ou sujeita a erro?"

Perguntas de aprofundamento:
- "Qual é a dor mais crítica — a que mais impacta o usuário?"
- "Existem dores secundárias que também valem a pena resolver?"
- "Essas dores são universais para todos os usuários ou variam por perfil?"

---

### Bloco 3 — Desejos e Ganhos

> "Além de resolver dores, o que o usuário gostaria de ganhar com esse sistema? Que resultado positivo ele espera além do básico?"

Perguntas:
- "O que faria o usuário dizer 'esse sistema é incrível'?"
- "Existe alguma funcionalidade ou experiência que o usuário já pediu ou sonha em ter?"

---

### Bloco 4 — Contexto de Uso

> "Em que contexto o usuário vai usar esse sistema? Isso afeta muito o que precisamos priorizar."

Perguntas:
- "O uso é rotineiro (diário/semanal) ou pontual (em situações específicas)?"
- "O usuário estará em um ambiente controlado (escritório) ou em campo (celular, sem internet)?"
- "Existe urgência ou pressão de tempo durante o uso?"

---

### Bloco 5 — Tentativas Anteriores

> "O que já foi tentado para resolver esse problema? Seja internamente ou por soluções de mercado?"

Perguntas:
- "Por que essas tentativas não funcionaram ou foram insuficientes?"
- "O que podemos aprender com o que já foi tentado?"

---

## Gerar o documento `opportunity.md`

Salve em:
```
docs/{nome-do-projeto}/discovery/opportunity.md
```

Template:

```markdown
# Mapeamento de Oportunidades — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}

---

## Jobs to Be Done

> O que os usuários estão tentando realizar ao usar esse sistema?

| Perfil | Job principal | Critério de sucesso |
|---|---|---|
| {perfil} | {job} | {como sabe que completou} |

---

## Dores e Fricções

### Dores críticas
{Liste as dores de maior impacto}

### Dores secundárias
{Liste dores menores mas relevantes}

---

## Desejos e Ganhos Esperados

{O que o usuário espera ganhar além da resolução das dores}

---

## Contexto de Uso

- **Frequência:** {rotineiro / pontual / variável}
- **Ambiente:** {escritório / campo / ambos}
- **Pressão de tempo:** {sim / não / depende do contexto}
- **Observações:** {outros aspectos relevantes do contexto}

---

## Tentativas Anteriores

| Solução tentada | Por que não funcionou | Aprendizado |
|---|---|---|
| {solução} | {motivo} | {lição} |

---

## Mapa de Oportunidades

> Oportunidades são lacunas entre o que o usuário precisa e o que existe hoje.

- **Oportunidade 1:** {descrição}
- **Oportunidade 2:** {descrição}
- **Oportunidade 3:** {descrição}
```

---

## Após gerar o documento

> "O `opportunity.md` foi salvo em `docs/{nome-do-projeto}/discovery/`. Com as oportunidades mapeadas, as próximas etapas recomendadas são:
> - **Hipóteses** — transformar oportunidades em hipóteses a validar
> - **Stakeholders** — identificar quem influencia ou é afetado por essas oportunidades
> - **Métricas** — definir como medir se estamos endereçando as oportunidades certas"

---

## Regras importantes

- Nunca sugira soluções durante essa etapa — o objetivo é entender o problema, não resolvê-lo.
- Se o usuário começar a falar em funcionalidades, redirecione: "Ótimo ponto — vamos registrar isso como uma ideia de solução para depois. Mas primeiro, qual é a dor que essa funcionalidade estaria resolvendo?"
- Se o usuário não souber responder algum bloco, sugira: "Isso pode ser um bom ponto para uma entrevista com usuários reais. Vamos registrar como 'a investigar'?"
