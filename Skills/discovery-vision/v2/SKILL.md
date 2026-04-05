---
name: discovery-vision
description: Conduz a construção da visão do projeto durante o discovery, gerando o documento vision.md. Use quando o usuário mencionar "visão do projeto", "definir visão", "qual o problema", "proposta de valor", "público-alvo", "para quem é esse sistema", "objetivo do projeto", "por que estamos fazendo isso", "qual dor resolvemos", "quem vai usar", "valor entregue", "contexto do projeto", "restrições do projeto". Requer que discovery-init tenha sido executado antes (verifica existência de project.md). NÃO use para oportunidades/dores (use discovery-opportunity), hipóteses (use discovery-assumptions), stakeholders (use discovery-stakeholders) ou métricas (use discovery-metrics).
metadata:
  author: Equipe de Discovery
  version: 1.1.0
  category: discovery
  depends-on: discovery-init
  output: docs/{projeto}/discovery/vision.md
---

# Discovery Vision

Skill responsável por conduzir a conversa de visão do projeto e gerar o documento `vision.md`.

---

## Pré-requisito

Antes de iniciar, verifique se o arquivo `docs/{nome-do-projeto}/project.md` existe.

- **Se não existir**: informe o usuário que é necessário iniciar o projeto primeiro e pergunte: "Quer que eu inicie o projeto agora usando a skill discovery-init?"
- **Se existir**: leia o arquivo para extrair o nome do projeto e contexto já registrado. Use essas informações para personalizar as perguntas.

---

## Fluxo de Execução

Conduza a conversa em blocos temáticos, de forma natural e progressiva. Não faça todas as perguntas de uma vez — espere a resposta de cada uma antes de avançar.

### Bloco 1 — O Problema

> "Vamos começar pelo problema que esse projeto resolve. Me conta: qual é a dor principal que esse sistema vai endereçar?"

Perguntas de aprofundamento (use conforme necessário):
- "Quem sente essa dor hoje? Com que frequência isso acontece?"
- "O que acontece quando esse problema não é resolvido?"
- "Existe alguma solução atual, mesmo que manual ou improvisada?"

**Validação:** Se a resposta for vaga (ex: "melhorar processos"), peça um exemplo concreto antes de avançar.

---

### Bloco 2 — O Público-Alvo

> "Quem são as pessoas ou organizações que vão se beneficiar diretamente desse sistema?"

Perguntas de aprofundamento:
- "Existe mais de um tipo de usuário? (ex: administrador, operador, cliente final)"
- "Qual o contexto em que esse usuário vai usar o sistema? (rotina, emergência, decisão estratégica...)"
- "Qual o nível de familiaridade desses usuários com tecnologia?"

**Validação:** Garanta que pelo menos um perfil de usuário esteja claramente definido.

---

### Bloco 3 — Proposta de Valor

> "Se esse projeto der certo, qual a transformação que ele entrega? O que muda na vida ou no trabalho do usuário?"

Perguntas de aprofundamento:
- "O que esse sistema faz que nenhuma outra solução existente faz hoje?"
- "Se você tivesse que explicar o valor desse projeto em uma frase para um executivo, o que diria?"
- "Qual seria o 'antes e depois' mais visível para o usuário?"

**Validação:** A proposta de valor deve ser específica e mensurável quando possível.

---

### Bloco 4 — Contexto e Motivação

> "Por que esse projeto está sendo feito agora? Existe alguma pressão de prazo, regulação, oportunidade de mercado ou demanda interna?"

Perguntas de aprofundamento:
- "O que mudou recentemente que tornou esse projeto prioritário?"
- "Existe algum evento ou deadline externo que influencia o timing?"

---

### Bloco 5 — Restrições Conhecidas *(opcional)*

> "Já existe alguma restrição importante que devemos considerar desde já? (tecnologia obrigatória, orçamento, prazo, integrações necessárias...)"

Perguntas de aprofundamento:
- "Existe algum sistema legado com o qual precisamos integrar?"
- "Há limitações de orçamento ou equipe que devemos considerar?"
- "Existe alguma tecnologia que obrigatoriamente deve ou não deve ser usada?"

**Nota:** Se o usuário não souber responder, registre como "a definir" e siga em frente.

---

## Gerar o Documento

Após coletar as informações, gere o arquivo em:

```
docs/{nome-do-projeto}/discovery/vision.md
```

### Template do Documento

```markdown
# Visão do Projeto — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}
> Versão: 1.0

---

## O Problema

{Descrição clara do problema central identificado}

| Aspecto | Descrição |
|---------|-----------|
| **Quem sente essa dor** | {público afetado} |
| **Frequência/Impacto** | {como e com que frequência o problema ocorre} |
| **Situação atual** | {como está sendo resolvido hoje, se houver} |

---

## Público-Alvo

{Descrição geral dos perfis de usuário}

| Perfil | Descrição | Principal Necessidade | Contexto de Uso |
|--------|-----------|----------------------|-----------------|
| {perfil 1} | {descrição} | {necessidade} | {contexto} |
| {perfil 2} | {descrição} | {necessidade} | {contexto} |

---

## Proposta de Valor

{Declaração clara do valor entregue pelo sistema}

| Aspecto | Descrição |
|---------|-----------|
| **Transformação esperada** | {o que muda para o usuário} |
| **Diferencial** | {o que esse sistema faz que outros não fazem} |
| **Frase de elevador** | {proposta de valor em uma frase} |

---

## Motivação e Contexto

{Por que esse projeto está acontecendo agora}

**Gatilhos identificados:**
- {gatilho 1}
- {gatilho 2}

---

## Restrições Conhecidas

{Liste restrições já identificadas, ou "Nenhuma identificada neste momento"}

| Tipo | Restrição | Impacto |
|------|-----------|---------|
| {Tecnologia/Prazo/Orçamento/Integração} | {descrição} | {como afeta o projeto} |

---

## Declaração de Visão

> "{Frase de visão — síntese do propósito do projeto em 1-2 linhas}"

---

## Pontos a Refinar

{Liste aqui itens marcados como "a definir" ou que precisam de mais investigação}

- [ ] {ponto 1}
- [ ] {ponto 2}

---

## Próximos Passos Sugeridos

Com base nesta visão, as próximas etapas recomendadas de discovery são:
- **Oportunidades** — mapear dores e jobs to be done em profundidade
- **Hipóteses** — identificar premissas que precisam ser validadas
- **Stakeholders** — mapear os envolvidos e suas expectativas
- **Métricas** — definir como medir o sucesso
```

---

## Após Gerar o Documento

1. **Salve o arquivo** em `docs/{nome-do-projeto}/discovery/vision.md`

2. **Atualize o `project.md`** marcando o item Discovery como "em andamento"

3. **Informe o usuário:**

> "O documento `vision.md` foi salvo em `docs/{nome-do-projeto}/discovery/`.
> 
> Com base no que conversamos, as próximas etapas mais relevantes parecem ser:
> 
> - **Oportunidades** — se você quer explorar mais as dores e necessidades dos usuários
> - **Hipóteses** — se existem premissas críticas que precisam ser validadas antes de investir
> - **Stakeholders** — se há múltiplos envolvidos com interesses ou expectativas diferentes
> - **Métricas** — se você precisa definir critérios claros de sucesso
> 
> Qual faz mais sentido para o momento do seu projeto?"

---

## Exemplos de Uso

### Exemplo 1: Projeto novo, usuário ainda organizando ideias

**Usuário diz:** "Quero definir a visão do projeto, mas ainda estou organizando as ideias"

**Ações:**
1. Confirmar que `project.md` existe
2. Conduzir cada bloco com perguntas de aprofundamento
3. Usar perguntas adicionais para ajudar o usuário a clarear o pensamento
4. Registrar respostas vagas como "a definir" na seção "Pontos a Refinar"
5. Gerar `vision.md` com lacunas claramente identificadas

**Resultado:** Documento de visão com pontos a refinar marcados, permitindo evolução iterativa

---

### Exemplo 2: Usuário já tem tudo estruturado

**Usuário diz:** "O problema é que vendedores perdem 2h por dia preenchendo relatórios manualmente. O público são vendedores de campo de empresas B2B. O valor é reduzir esse tempo para 15 minutos com preenchimento automático via voz. Precisamos entregar até março por causa de uma meta de produtividade da diretoria."

**Ações:**
1. Não repetir perguntas — apenas confirmar e organizar
2. Fazer 1-2 perguntas de refinamento se necessário (ex: "Existe alguma restrição técnica?")
3. Preencher todos os campos do template com as informações fornecidas
4. Gerar `vision.md` completo

**Resultado:** Documento de visão consolidado em uma única interação

---

### Exemplo 3: Usuário quer pular etapas

**Usuário diz:** "Não sei quem é o público ainda, vamos pular essa parte"

**Ações:**
1. Informar a importância do ponto: "O público-alvo vai influenciar várias decisões depois, mas podemos marcar como 'a definir' e seguir."
2. Registrar na seção "Pontos a Refinar"
3. Continuar com os próximos blocos
4. Ao final, destacar os pontos pendentes

**Resultado:** Documento gerado com pendências claramente sinalizadas

---

## Troubleshooting

### Erro: `project.md` não encontrado

**Causa:** O usuário não executou `discovery-init` antes.

**Solução:** 
- Informe: "Para criar a visão, preciso primeiro das informações básicas do projeto."
- Pergunte: "Quer que eu inicie o projeto agora usando a skill discovery-init?"
- Se sim, execute o fluxo de init primeiro, depois retome a visão

---

### Problema: Respostas muito vagas do usuário

**Causa:** Usuário não tem clareza sobre o projeto ou está em fase muito inicial.

**Solução:** 
- Ofereça exemplos genéricos: "Por exemplo, o problema poderia ser algo como 'clientes esperam muito tempo para ser atendidos' ou 'equipe gasta horas em tarefas repetitivas'. Algo nessa linha?"
- Se ainda assim for vago, registre como "a definir" e sinalize: "Esse ponto pode ser importante para as próximas fases — quer detalhar mais ou deixamos como rascunho por enquanto?"
- Continue o fluxo para não travar a conversa

---

### Problema: Usuário mistura visão com outras etapas

**Causa:** Usuário começa a falar de hipóteses, métricas ou detalhes técnicos durante a visão.

**Solução:**
- Anote as informações relevantes para as outras skills
- Gentilmente redirecione: "Ótimo ponto sobre métricas! Vou guardar isso para quando fizermos o discovery de métricas. Por agora, vamos focar em..."
- Ao final, mencione que já há insumos para as próximas etapas

---

### Problema: Conflito de informações

**Causa:** Usuário dá informações contraditórias em diferentes momentos.

**Solução:**
- Sinalize a inconsistência: "Antes você mencionou que o público eram gerentes, agora parece que são analistas. Qual dos dois é o foco principal?"
- Registre ambos os perfis se forem válidos
- Documente a ambiguidade se não for resolvida

---

### Problema: Usuário quer gerar documento incompleto

**Causa:** Pressa ou falta de informação disponível.

**Solução:**
- Permita gerar, mas informe: "Posso gerar o documento agora, mas ele ficará incompleto nos pontos X, Y e Z. Você poderá complementar depois. Quer seguir assim?"
- Marque claramente os pontos incompletos na seção "Pontos a Refinar"
- Sugira revisitar o documento quando houver mais informações

---

## Regras Importantes

### Adaptação de Tom
- **Para devs/tech leads:** Use termos técnicos, seja direto, foque em restrições técnicas
- **Para PMs/analistas:** Foque em valor de negócio, usuários, métricas
- **Para stakeholders executivos:** Seja conciso, destaque impacto e timing

### Comportamentos Obrigatórios
- **Nunca invente informações** — se o usuário não souber, registre como "a definir"
- **Não repita perguntas** — se o usuário já trouxe a resposta, apenas confirme e organize
- **Sinalize lacunas** — pontos vagos devem ser destacados para revisão futura
- **Mantenha o foco** — visão é sobre o "porquê" e "para quem", não sobre "como"

### O Que NÃO Fazer Nesta Skill
- Não sugira soluções técnicas (isso é para refinamento)
- Não detalhe funcionalidades (isso é para escopo)
- Não defina métricas específicas (isso é para discovery-metrics)
- Não mapeie stakeholders em profundidade (isso é para discovery-stakeholders)
- Não liste hipóteses a validar (isso é para discovery-assumptions)

---

## Referências

Para aprofundamento nos conceitos utilizados nesta skill:
- **Lean Canvas** — estrutura para capturar modelo de negócio enxuto
- **Value Proposition Canvas** — framework para proposta de valor
- **Jobs to Be Done** — abordagem para entender necessidades do usuário

*Nota: Materiais de referência detalhados podem ser adicionados em `references/` conforme necessário.*
