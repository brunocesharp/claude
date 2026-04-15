---
name: discovery-assumptions
description: Conduz o levantamento de hipóteses e premissas durante o discovery, gerando o documento assumptions.md. Baseada em Assumption Mapping e Lean Startup. Use quando o usuário mencionar "hipóteses", "premissas", "suposições", "o que não sabemos", "riscos de descoberta", "validações necessárias", "incertezas", "apostas do projeto", "o que precisamos confirmar", "isso é um chute", "estamos assumindo que", "precisamos testar antes", "como saber se funciona". Requer discovery-init. NÃO use para visão geral (use discovery-vision), dores e oportunidades (use discovery-opportunity), stakeholders (use discovery-stakeholders) ou métricas (use discovery-metrics). Esta skill foca em INCERTEZAS que precisam ser validadas antes de investir.
metadata:
  author: Equipe de Discovery
  version: 1.1.0
  category: discovery
  depends-on: discovery-init
  recommended-after: discovery-opportunity
  output: docs/discovery/assumptions.md
  frameworks: Assumption Mapping, Lean Startup
---

# Discovery Assumptions

Conduz o levantamento de hipóteses e premissas e gera o documento `assumptions.md`.

Para detalhes sobre os frameworks (Assumption Mapping, Lean Startup), consulte `references/frameworks.md`.

---

## Pré-requisito

Verifique a existência do `project.md` no caminho correto:

| Situação | Caminho |
|---|---|
| Com repositório clonado | `docs/project.md` |
| Sem repositório (local) | `{nome-do-projeto}/docs/project.md` |

- **Se não existir**: pergunte "Quer que eu inicie o projeto agora usando a skill discovery-init?"
- **Se existir**: leia também `vision.md` e `opportunity.md` — eles são a melhor fonte para identificar hipóteses implícitas.

---

## Conceito Rápido

Use se o usuário não for familiarizado com o conceito:

> "Toda decisão de produto carrega suposições embutidas — sobre o que os usuários querem, sobre o que é tecnicamente possível, sobre o que o mercado aceita. O objetivo aqui é tornar essas suposições explícitas para validá-las antes de construir a coisa errada."

---

## Fluxo de Execução

Conduza a conversa em blocos temáticos. Espere a resposta de cada bloco antes de avançar.

### Bloco 1 — Hipóteses sobre Usuários

> "Quais suposições estamos fazendo sobre os usuários desse sistema?"

Perguntas:
- "Estamos assumindo que o usuário vai querer usar isso — qual é a evidência?"
- "Estamos assumindo que ele consegue usar — tem acesso, conhecimento, tempo?"
- "Existe suposição sobre comportamento que, se errada, inviabiliza o projeto?"

**Validação:**
- Pelo menos 2-3 hipóteses devem ser identificadas
- Se usuário disser "não temos", extraia do `vision.md` e `opportunity.md`
- Se disser "é óbvio", questione: "Temos evidência ou é suposição forte?"

---

### Bloco 2 — Hipóteses sobre o Negócio

> "Quais suposições estamos fazendo sobre o impacto no negócio?"

Perguntas:
- "Estamos assumindo que vai gerar algum resultado mensurável — qual?"
- "Existe premissa financeira ou de prazo que precisa ser verdade?"
- "O que o negócio assume que vai acontecer após o lançamento?"

**Validação:**
- Conecte com métricas de sucesso se `success-metrics.md` existir
- Hipóteses de ROI ou payback são sempre críticas

---

### Bloco 3 — Hipóteses Técnicas

> "Quais suposições técnicas precisam ser validadas?"

Perguntas:
- "Existe integração com sistema externo que assumimos que vai funcionar?"
- "Estamos assumindo disponibilidade de API, dado ou infraestrutura?"
- "Existe dependência técnica ainda não confirmada?"

**Validação:**
- Se não houver hipóteses técnicas, pergunte sobre integrações e performance
- Hipóteses de "já fizemos algo parecido" merecem questionamento

---

### Bloco 4 — Priorização das Hipóteses

Após listar, classifique por dois eixos:

> "Vamos classificar cada hipótese por: **impacto se estiver errada** e **certeza que temos hoje**."

Para detalhes da matriz de priorização, consulte `references/prioritization.md`.

Resumo rápido:
- **Alto impacto + Baixa certeza** = VALIDAR PRIMEIRO ⚠️
- **Alto impacto + Alta certeza** = Confirmar e seguir
- **Baixo impacto + Baixa certeza** = Monitorar
- **Baixo impacto + Alta certeza** = Ignorar

---

## Gerar o Documento

Após coletar as informações, gere o arquivo usando o template em `references/template-assumptions.md` no caminho correto:

| Situação | Caminho do arquivo |
|---|---|
| Com repositório clonado | `docs/discovery/assumptions.md` |
| Sem repositório (local) | `{nome-do-projeto}/docs/discovery/assumptions.md` |

Para técnicas de validação, consulte `references/validation-methods.md`.

---

## Após Gerar o Documento

1. **Salve o arquivo** no caminho correto (com repositório: `docs/discovery/assumptions.md` / sem repositório: `{nome-do-projeto}/docs/discovery/assumptions.md`)

2. **Informe o usuário:**

> "O `assumptions.md` foi salvo. Com as hipóteses mapeadas e priorizadas, os próximos passos podem ser:
>
> - **Planejar validações** — definir experimentos para hipóteses críticas
> - **Stakeholders** — mapear quem pode ajudar a validar
> - **Métricas** — definir como medir se as hipóteses foram confirmadas
>
> Qual faz mais sentido agora?"

---

## Regras Importantes

### Comportamento Obrigatório

- **Não julgue hipóteses** — o objetivo é torná-las explícitas, não certas ou erradas
- **Questione o "óbvio"** — "Temos evidência ou é suposição forte não testada?"
- **Sugira validações concretas** — entrevistas, protótipos, spikes, análise de dados
- **Nunca deixe vazio** — se usuário não listar, extraia de `vision.md` e `opportunity.md`

### O Que NÃO Fazer

- Não valide hipóteses durante o mapeamento — isso é uma etapa posterior
- Não descarte hipóteses por parecerem "óbvias"
- Não misture hipóteses com fatos confirmados
- Não sugira soluções — foco em incertezas, não em funcionalidades
- Não priorize por facilidade de validação — priorize por impacto

### Adaptação de Tom

- **Para PMs/analistas:** Foque em hipóteses de usuário e negócio
- **Para devs/tech leads:** Aprofunde em hipóteses técnicas e integrações
- **Para founders/executivos:** Destaque hipóteses de mercado e modelo de negócio

---

## Troubleshooting

Para problemas comuns, consulte `references/troubleshooting.md`.

Resumo dos mais frequentes:
- **Usuário confunde hipótese com fato** → "Qual foi a última evidência disso?"
- **Todas parecem óbvias** → "Se errada, o que acontece com o projeto?"
- **Não consegue pensar em hipóteses técnicas** → pergunte sobre integrações e performance
- **Hipóteses muito vagas** → peça para reformular como afirmação testável

---

## Exemplos

Para exemplos detalhados de uso, consulte `references/examples.md`.
