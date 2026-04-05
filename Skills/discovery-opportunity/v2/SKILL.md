---
name: discovery-opportunity
description: Conduz o mapeamento de oportunidades durante o discovery, gerando o documento opportunity.md. Baseada em Opportunity Solution Tree e Jobs to Be Done. Use quando o usuário mencionar "oportunidades", "mapear dores", "jobs to be done", "JTBD", "o que o usuário quer fazer", "necessidades dos usuários", "fricções", "ganhos esperados", "contexto de uso", "tentativas anteriores", "por que soluções anteriores falharam", "entender o problema antes de resolver". Requer discovery-init. NÃO use para visão geral do projeto (use discovery-vision), hipóteses a validar (use discovery-assumptions), stakeholders (use discovery-stakeholders) ou métricas (use discovery-metrics). Esta skill foca no PROBLEMA, não em soluções.
metadata:
  author: Equipe de Discovery
  version: 1.1.0
  category: discovery
  depends-on: discovery-init
  recommended-after: discovery-vision
  output: docs/{projeto}/discovery/opportunity.md
  frameworks: Opportunity Solution Tree, Jobs to Be Done
---

# Discovery Opportunity

Conduz o mapeamento de oportunidades e gera o documento `opportunity.md`.

Para detalhes sobre os frameworks utilizados (Opportunity Solution Tree, Jobs to Be Done), consulte `references/frameworks.md`.

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.

- **Se não existir**: pergunte "Quer que eu inicie o projeto agora usando a skill discovery-init?"
- **Se existir**: leia o arquivo. Se `vision.md` também existir, use-o para contextualizar as perguntas.

---

## Fluxo de Execução

Conduza a conversa em blocos temáticos. Espere a resposta de cada bloco antes de avançar.

### Bloco 1 — Jobs to Be Done

> "Vamos pensar no que os usuários estão tentando realizar — não o que o sistema vai fazer, mas o **objetivo real** por trás do uso."

Perguntas:
- "Quando um usuário vai usar esse sistema, qual tarefa ou objetivo ele está tentando completar?"
- "Existe mais de um tipo de objetivo dependendo do perfil do usuário?"
- "O que define 'missão cumprida' para esse usuário?"

**Validação:** 
- Pelo menos um job principal deve estar definido
- O critério de sucesso deve ser observável
- Se vago, use a fórmula JTBD: "Quando [situação], eu quero [motivação], para que [resultado]"

---

### Bloco 2 — Dores e Fricções

> "O que atrapalha o usuário hoje? O que torna essa tarefa difícil, demorada, frustrante ou sujeita a erro?"

Perguntas:
- "Qual é a dor mais crítica — a que mais impacta o usuário?"
- "Existem dores secundárias que também valem resolver?"
- "Essas dores são universais ou variam por perfil?"

**Validação:**
- Distinguir dores críticas de secundárias
- Se usuário falar de funcionalidades, redirecione: "Qual dor essa funcionalidade resolveria?"

---

### Bloco 3 — Desejos e Ganhos

> "Além de resolver dores, o que o usuário gostaria de ganhar? Que resultado positivo ele espera além do básico?"

Perguntas:
- "O que faria o usuário dizer 'esse sistema é incrível'?"
- "Existe algo que o usuário já pediu ou sonha em ter?"

**Validação:**
- Dor = algo negativo que acontece HOJE
- Desejo = algo positivo que NÃO acontece hoje
- Pergunte: "Isso atrapalha hoje ou seria um bônus?"

---

### Bloco 4 — Contexto de Uso

> "Em que contexto o usuário vai usar esse sistema?"

Perguntas:
- "O uso é rotineiro (diário/semanal) ou pontual?"
- "Ambiente controlado (escritório) ou em campo (celular, sem internet)?"
- "Existe urgência ou pressão de tempo durante o uso?"

**Validação:**
- Se não claro, peça para descrever um dia típico do usuário
- Identifique o momento exato de uso

---

### Bloco 5 — Tentativas Anteriores

> "O que já foi tentado para resolver esse problema?"

Perguntas:
- "Por que essas tentativas não funcionaram?"
- "O que podemos aprender com o que já foi tentado?"

**Validação:**
- Se não houver tentativas, pergunte sobre workarounds improvisados
- Investigue soluções de mercado rejeitadas

---

## Gerar o Documento

Após coletar as informações, gere `docs/{nome-do-projeto}/discovery/opportunity.md` usando o template em `references/template-opportunity.md`.

---

## Após Gerar o Documento

1. **Salve o arquivo** em `docs/{nome-do-projeto}/discovery/opportunity.md`

2. **Informe o usuário:**

> "O `opportunity.md` foi salvo. Com as oportunidades mapeadas, as próximas etapas recomendadas são:
> 
> - **Hipóteses** — transformar oportunidades em hipóteses a validar
> - **Stakeholders** — identificar quem influencia essas oportunidades
> - **Métricas** — definir como medir se estamos no caminho certo
> 
> Qual faz mais sentido agora?"

---

## Regras Importantes

### Comportamento Obrigatório

- **Nunca sugira soluções** — o objetivo é entender o problema, não resolvê-lo
- **Nunca invente informações** — se não souber, registre como "a investigar"
- **Redirecione funcionalidades**: "Ótimo — qual dor essa funcionalidade resolveria?"
- **Sugira validação**: "Esse seria um bom ponto para validar com usuários reais"

### O Que NÃO Fazer

- Não sugira soluções ou funcionalidades
- Não priorize por esforço técnico — aqui importa impacto no usuário
- Não ignore tentativas anteriores — elas têm lições valiosas
- Não misture com visão — visão é o "porquê geral", oportunidades são dores específicas

### Adaptação de Tom

- **Para PMs/designers:** Foque em jobs, dores, ganhos
- **Para devs/tech leads:** Conecte com restrições técnicas do contexto
- **Para stakeholders:** Destaque impacto de negócio das dores

---

## Troubleshooting

Para problemas comuns, consulte `references/troubleshooting.md`.

Resumo dos mais frequentes:
- **Usuário confunde dores com funcionalidades** → pergunte "qual dor isso resolve?"
- **Jobs muito genéricos** → use a fórmula JTBD com situação específica
- **Dores e desejos misturados** → "isso atrapalha hoje ou seria um bônus?"
- **Sem acesso a usuários reais** → marque como "a investigar"

---

## Exemplos

Para exemplos detalhados de uso, consulte `references/examples.md`.
