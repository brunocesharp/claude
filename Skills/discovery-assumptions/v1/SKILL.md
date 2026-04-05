---
name: discovery-assumptions
description: Conduz o levantamento de hipóteses e premissas durante o discovery de um projeto. Use esta skill sempre que o usuário mencionar "hipóteses do projeto", "premissas", "o que ainda não sabemos", "riscos de descoberta", "validações necessárias", "o que precisamos confirmar", "suposições do projeto" ou qualquer variação que indique a necessidade de mapear incertezas antes de investir em desenvolvimento. Use proativamente sempre que o time parecer estar operando com muitas suposições não validadas sobre usuários, tecnologia ou mercado.
---

# Discovery Assumptions

Skill responsável por conduzir o levantamento de hipóteses e premissas e gerar o documento `assumptions.md`.

Baseada no framework **Assumption Mapping** (David Bland & Alex Osterwalder) e nas práticas de **Lean Startup** (Eric Ries).

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.
- **Se não existir**: sugira iniciar com `discovery-init`.
- **Se existir**: leia também `vision.md` e `opportunity.md` se disponíveis — eles são a melhor fonte para identificar hipóteses implícitas.

---

## Conceito rápido (use se o usuário não for familiarizado)

> "Toda decisão de produto carrega suposições embutidas — sobre o que os usuários querem, sobre o que é tecnicamente possível, sobre o que o mercado aceita. O objetivo aqui é tornar essas suposições explícitas para que possamos priorizá-las e validá-las antes de construir a coisa errada."

---

## Fluxo de execução

### Bloco 1 — Hipóteses sobre Usuários

> "Quais são as suposições que estamos fazendo sobre os usuários desse sistema?"

Perguntas de apoio:
- "Estamos assumindo que o usuário vai querer usar isso — qual é a evidência disso?"
- "Estamos assumindo que o usuário consegue usar — ele tem o nível de acesso, conhecimento técnico e tempo necessário?"
- "Existe alguma suposição sobre o comportamento do usuário que, se estiver errada, inviabiliza o projeto?"

---

### Bloco 2 — Hipóteses sobre o Negócio

> "Quais são as suposições sobre o impacto no negócio?"

Perguntas de apoio:
- "Estamos assumindo que esse sistema vai gerar algum resultado mensurável — qual?"
- "Existe alguma premissa financeira ou de prazo que precisa ser verdade para o projeto fazer sentido?"
- "O que o negócio está assumindo que vai acontecer após o lançamento?"

---

### Bloco 3 — Hipóteses Técnicas

> "Quais são as suposições técnicas que precisam ser validadas?"

Perguntas de apoio:
- "Existe alguma integração com sistema externo que assumimos que vai funcionar?"
- "Estamos assumindo disponibilidade de alguma API, dado ou infraestrutura?"
- "Existe alguma dependência técnica que ainda não foi confirmada?"

---

### Bloco 4 — Priorização das Hipóteses

Após listar as hipóteses, ajude o usuário a priorizá-las por dois eixos:

> "Agora vamos classificar cada hipótese por dois critérios: **o quanto ela é crítica para o sucesso do projeto** e **o quanto temos certeza de que ela é verdade**."

Use a matriz:
```
                ALTA CERTEZA
                     |
    Monitorar        |      Confirmar e seguir
                     |
BAIXO IMPACTO -------+------- ALTO IMPACTO
                     |
    Ignorar          |      VALIDAR PRIMEIRO ⚠️
                     |
                BAIXA CERTEZA
```

As hipóteses no quadrante **alto impacto + baixa certeza** são as mais críticas e devem ser validadas antes de qualquer desenvolvimento.

---

## Gerar o documento `assumptions.md`

Salve em:
```
docs/{nome-do-projeto}/discovery/assumptions.md
```

Template:

```markdown
# Hipóteses e Premissas — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}

---

## Hipóteses sobre Usuários

| Hipótese | Impacto se falsa | Certeza atual | Prioridade de validação |
|---|---|---|---|
| {hipótese} | {alto/médio/baixo} | {alta/média/baixa} | {crítica/importante/monitorar} |

---

## Hipóteses sobre o Negócio

| Hipótese | Impacto se falsa | Certeza atual | Prioridade de validação |
|---|---|---|---|
| {hipótese} | {alto/médio/baixo} | {alta/média/baixa} | {crítica/importante/monitorar} |

---

## Hipóteses Técnicas

| Hipótese | Impacto se falsa | Certeza atual | Prioridade de validação |
|---|---|---|---|
| {hipótese} | {alto/médio/baixo} | {alta/média/baixa} | {crítica/importante/monitorar} |

---

## Hipóteses Críticas ⚠️

> Estas hipóteses têm alto impacto e baixa certeza — devem ser validadas antes do desenvolvimento.

1. {hipótese crítica 1} — **Como validar:** {sugestão de experimento ou pesquisa}
2. {hipótese crítica 2} — **Como validar:** {sugestão de experimento ou pesquisa}

---

## Premissas Assumidas como Verdade

> Estas premissas foram aceitas pela equipe sem necessidade de validação adicional.

- {premissa 1}
- {premissa 2}
```

---

## Após gerar o documento

> "O `assumptions.md` foi salvo em `docs/{nome-do-projeto}/discovery/`. Com as hipóteses mapeadas, fica mais claro o que precisamos validar antes de investir em desenvolvimento. Quer continuar com:
> - **Stakeholders** — mapear quem pode ajudar a validar essas hipóteses
> - **Métricas** — definir como medir se as hipóteses críticas foram confirmadas"

---

## Regras importantes

- Não julgue hipóteses como certas ou erradas — o objetivo é torná-las explícitas e priorizadas.
- Se o usuário disser "isso é óbvio" ou "todo mundo sabe", questione gentilmente: "Temos evidência disso ou é uma suposição forte que ainda não foi testada?"
- Sugira formas concretas de validar hipóteses críticas: entrevistas, protótipos, análise de dados, spike técnico, etc.
- Nunca deixe o documento vazio — se o usuário não conseguir listar hipóteses, ajude com exemplos baseados no que foi discutido em `vision.md` e `opportunity.md`.
