---
name: discovery-vision
description: Conduz a construção da visão do projeto durante o discovery. Use esta skill sempre que o usuário mencionar "visão do projeto", "definir visão", "qual o problema que resolvemos", "proposta de valor", "público-alvo", "para quem é esse sistema", "qual o objetivo do projeto" ou qualquer variação que indique a necessidade de definir o propósito central do projeto. Deve ser usada após a discovery-init. Use proativamente sempre que o usuário quiser entender ou documentar o "porquê" do projeto.
---

# Discovery Vision

Skill responsável por conduzir a conversa de visão do projeto e gerar o documento `vision.md`.

---

## Pré-requisito

Antes de iniciar, verifique se o arquivo `docs/{nome-do-projeto}/project.md` existe.

- **Se não existir**: informe o usuário que é necessário iniciar o projeto primeiro e sugira usar a skill `discovery-init`.
- **Se existir**: leia o arquivo para usar o nome do projeto e contexto já registrado.

---

## Fluxo de execução

Conduza a conversa em blocos temáticos, de forma natural e progressiva. Não faça todas as perguntas de uma vez — espere a resposta de cada uma antes de avançar.

---

### Bloco 1 — O Problema

> "Vamos começar pelo problema que esse projeto resolve. Me conta: qual é a dor principal que esse sistema vai endereçar?"

Perguntas de aprofundamento (use conforme necessário):
- "Quem sente essa dor hoje? Com que frequência isso acontece?"
- "O que acontece quando esse problema não é resolvido?"
- "Existe alguma solução atual, mesmo que manual ou improvisada?"

---

### Bloco 2 — O Público-Alvo

> "Quem são as pessoas ou organizações que vão se beneficiar diretamente desse sistema?"

Perguntas de aprofundamento:
- "Existe mais de um tipo de usuário? (ex: administrador, operador, cliente final)"
- "Qual o contexto em que esse usuário vai usar o sistema? (rotina, emergência, decisão estratégica...)"

---

### Bloco 3 — Proposta de Valor

> "Se esse projeto der certo, qual a transformação que ele entrega? O que muda na vida ou no trabalho do usuário?"

Perguntas de aprofundamento:
- "O que esse sistema faz que nenhuma outra solução existente faz hoje?"
- "Se você tivesse que explicar o valor desse projeto em uma frase para um executivo, o que diria?"

---

### Bloco 4 — Contexto e Motivação

> "Por que esse projeto está sendo feito agora? Existe alguma pressão de prazo, regulação, oportunidade de mercado ou demanda interna?"

---

### Bloco 5 — Restrições Conhecidas *(opcional)*

> "Já existe alguma restrição importante que devemos considerar desde já? (tecnologia obrigatória, orçamento, prazo, integrações necessárias...)"

---

## Gerar o documento `vision.md`

Após coletar as informações, gere o arquivo em:
```
docs/{nome-do-projeto}/discovery/vision.md
```

Use o template abaixo:

```markdown
# Visão do Projeto — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}

---

## O Problema

{Descrição clara do problema central identificado}

**Quem sente essa dor:** {público afetado}
**Frequência/Impacto:** {como e com que frequência o problema ocorre}
**Situação atual:** {como está sendo resolvido hoje, se houver}

---

## Público-Alvo

{Descrição dos perfis de usuário}

| Perfil | Descrição | Principal necessidade |
|---|---|---|
| {perfil 1} | {descrição} | {necessidade} |
| {perfil 2} | {descrição} | {necessidade} |

---

## Proposta de Valor

{Declaração clara do valor entregue pelo sistema}

**Transformação esperada:** {o que muda para o usuário}
**Diferencial:** {o que esse sistema faz que outros não fazem}

---

## Motivação e Contexto

{Por que esse projeto está acontecendo agora}

---

## Restrições Conhecidas

{Liste restrições já identificadas, ou "Nenhuma identificada neste momento"}

---

## Declaração de Visão

> "{Frase de visão — síntese do propósito do projeto em 1-2 linhas}"
```

---

## Após gerar o documento

Informe o usuário:
> "O documento `vision.md` foi salvo em `docs/{nome-do-projeto}/discovery/`. Quer continuar o discovery? As próximas etapas disponíveis são:
> - **Oportunidades** — mapear dores e jobs to be done
> - **Hipóteses** — levantar premissas que precisam ser validadas
> - **Stakeholders** — identificar os envolvidos
> - **Métricas** — definir como vamos medir o sucesso"

Atualize o `project.md` marcando o item Discovery como em andamento, se ainda não estiver.

---

## Regras importantes

- Adapte o tom conforme o perfil do usuário: mais técnico para devs/techlead, mais conceitual para PMs e analistas.
- Se o usuário já trouxer as respostas de forma proativa, não repita as perguntas — apenas confirme e organize.
- Se um bloco ficar vago, sinalize: "Esse ponto pode ser importante para as próximas fases — quer detalhar mais ou deixamos como rascunho por enquanto?"
- Nunca invente informações — se o usuário não souber responder algo, registre como `"a definir"` no documento.
