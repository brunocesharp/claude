---
name: spec-functional
description: Conduz a especificação funcional de um escopo usando BDD (Behavior-Driven Development), gerando o documento spec-functional.md. Use quando o usuário mencionar "especificação funcional", "regras de negócio", "critérios de aceitação", "cenários BDD", "Given When Then", "comportamento esperado", "especificar funcionalidades", "detalhar regras" ou "escrever acceptance criteria". NÃO use para casos de uso com múltiplos atores (use spec-usecases), requisitos não-funcionais (use spec-nonfunctional) ou refinamento técnico (use refinement-*).
metadata:
  author: Equipe de Especificação
  version: 1.1.0
  category: specification
  depends-on: scope-generate
  output: "{docs_root}/especificacao/{escopo}/spec-functional.md"
---

# Spec Functional

Skill que conduz a especificação funcional usando BDD e gera o `spec-functional.md`.

Antes de iniciar qualquer especificação, consulte os arquivos de referência:
- `references/bdd-teoria.md` — hierarquia BDD, Feature Injection e fundamentos
- `references/cenarios-given-when-then.md` — regras e anti-padrões de escrita de cenários
- `references/extracao-de-exemplos.md` — técnica de conversa e extração de exemplos
- `references/template-spec-functional.md` — template com exemplo preenchido

---

## Pré-requisito

Leia `docs/project-config.json` e extraia `docs_root` (padrão: `"docs"`).

Verifique se existe `{docs_root}/escopo/{nome-do-escopo}/escopo.md`.

- **Não existe:** informe o usuário e ofereça executar `scope-generate` agora.
- **Existe:** leia o arquivo completamente e extraia: título, funcionalidades listadas, usuários afetados, hipóteses críticas e restrições. Não repita perguntas já respondidas.

---

## Fluxo de Execução

### Passo 1 — Abertura

Após ler o escopo, apresente as features identificadas e confirme a ordem:

> "Li o escopo **{título}**. Vou especificar estas funcionalidades:
>
> 1. {funcionalidade 1}
> 2. {funcionalidade 2}
>
> Trabalharemos uma por vez. Começamos pela **{funcionalidade 1}**?"

Se houver mais de 5 funcionalidades, pergunte quais são prioritárias.

---

### Passo 2 — Para cada Feature: Narrativa

Apresente e confirme a narrativa no formato Feature Injection:

> "A narrativa desta feature:
>
> **Feature:** {nome}
> **In order to** {objetivo de negócio mensurável}
> **As** {ator principal}
> **I want** {o que o sistema faz}
>
> Correto?"

Nunca aceite "melhorar o sistema" como objetivo. Peça impacto real e mensurável.
Consulte `references/bdd-teoria.md` para exemplos de bons objetivos de negócio.

---

### Passo 3 — Para cada Feature: Cenário Principal (Happy Path)

> "Me dê um exemplo concreto do caso mais comum: quem usa, em que situação, o que espera."

Perguntas de aprofundamento:
- "Quais dados de entrada seriam usados?"
- "Qual o resultado exato — com valores concretos?"

Formalize e confirme imediatamente. Consulte `references/cenarios-given-when-then.md`
para as regras de qualidade do cenário antes de apresentá-lo ao usuário.

---

### Passo 4 — Para cada Feature: Cenários Alternativos e de Exceção

> "O que acontece quando as coisas saem do esperado?"

Perguntas-guia:
- "O que acontece se {dado inválido ou ausente}?"
- "E se o usuário não tiver permissão?"
- "Quais são os limites — mínimos, máximos, casos vazios?"
- "O que acontece se uma dependência externa falhar?"

Consulte `references/extracao-de-exemplos.md` para os tipos de exemplos a levantar
(variações válidas, limites, casos inválidos, exceções).

---

### Passo 5 — Para cada Feature: Regras de Negócio e Tabelas

> "Existe alguma regra que se aplica a múltiplos cenários? Cálculos, faixas, elegibilidade?"

Quando houver múltiplas combinações entrada/saída para a mesma regra, sugira
Esquema do Cenário com tabela. Consulte `references/cenarios-given-when-then.md`
para o formato correto e exemplos de quando usar.

---

### Passo 6 — Para cada Feature: Revisão de Cobertura

Liste os cenários levantados e pergunte:

> "Cenários desta feature:
> ✅ {cenário 1}
> ✅ {cenário 2}
>
> Algum caso ficou de fora?"

Cheques adicionais:
- "E se dois usuários fizerem a mesma ação simultaneamente?"
- "Há dependência com sistema externo que pode falhar?"
- "Alguma regra sazonal, por horário ou por período?"

---

### Passo 7 — Fechamento

Ao concluir todas as features:

> "Cobrimos todas as funcionalidades. Antes de gerar:
> 1. Há features não abordadas?
> 2. Algum cenário levantou dúvidas para stakeholders?
> 3. Existe regra importante ainda não capturada?"

---

## Gerar o Documento

Use o template em `references/template-spec-functional.md` como base.

Salve em `{docs_root}/especificacao/{nome-do-escopo}/spec-functional.md`.

---

## Após Gerar o Documento

> "Documento salvo em `{docs_root}/especificacao/{escopo}/spec-functional.md`.
> {N} features especificadas, {M} cenários no total.
> {Se houver pontos em aberto}: {X} pontos precisam de resposta dos stakeholders."

Sugira os próximos passos com base no que foi levantado.

---

## Exemplos de Uso

### Exemplo 1: Regras de negócio claras

**Usuário:** "Vamos especificar o módulo de cálculo de frete"

**Ações:**
1. Ler escopo e identificar features (cálculo por peso, por região, descontos)
2. Para cada feature, executar passos 2 a 6
3. Usar Esquema do Cenário para combinações peso × região × desconto

**Resultado:** Documento com cenários executáveis prontos para automação de testes

---

### Exemplo 2: Regras pouco claras

**Usuário:** "Quero especificar o processo de aprovação de crédito"

**Ações:**
1. Identificar que os critérios de aprovação não estão definidos no escopo
2. Extrair exemplos concretos via Passo 3 e técnica do `references/extracao-de-exemplos.md`
3. Revelar regras implícitas através dos exemplos
4. Marcar lacunas como "Ponto em Aberto" com responsável identificado

**Resultado:** Documento com cenários conhecidos e pontos em aberto rastreáveis

---

### Exemplo 3: Múltiplas combinações de dados

**Usuário:** "A comissão varia por produto, vendedor e faixa de valor"

**Ações:**
1. Identificar variáveis (produto, perfil, faixa, percentual)
2. Pedir 3–4 casos reais: "Quais exemplos você usaria para testar?"
3. Organizar em Esquema do Cenário com tabela
4. Verificar casos extremos (mínimo, máximo, zero)

**Resultado:** Um cenário parametrizado cobrindo todas as combinações

---

## Troubleshooting

**Usuário não consegue dar exemplos concretos**
Ofereça um hipotético para desbloqueá-lo: "Seria algo como: Dado que João tem
R$500, quando solicita transferência de R$200, então o saldo deve ser R$300?"
Ver também: técnica "Popping the Why Stack" em `references/extracao-de-exemplos.md`

**Usuário quer especificar a tela**
Redirecione: "Ótimo ponto para o refinement-screens. Por agora, independente da
tela, o que o sistema deve fazer quando o usuário realiza essa ação?"

**Cenário ficou longo demais**
Identifique a ação principal (When) e o resultado principal (Then). Remova
passos de navegação e ações intermediárias. Ver anti-padrões em
`references/cenarios-given-when-then.md`

**Muitos cenários quase idênticos**
Use Esquema do Cenário. Regra de ouro: se dois cenários diferem apenas nos
dados, devem ser um único cenário parametrizado.
