---
name: arch-adr
description: Registra uma decisão de arquitetura (ADR — Architecture Decision Record) de um projeto em docs/{projeto}/arquitetura/decisoes/ADR-{NNN}-{titulo}.md, com contexto, opções consideradas, decisão e consequências, e mantém o índice de decisões. Use quando o usuário mencionar "ADR", "decisão de arquitetura", "registrar decisão", "por que escolhemos", "escolher entre tecnologias", "trocar de banco/framework/fila", "substituir decisão", "decisões técnicas do projeto". NÃO use para desenhar a arquitetura (use arch-c4), para regras de negócio (use business-docs) ou para especificação funcional (use spec-functional).
metadata:
  author: Equipe de Arquitetura
  version: 1.0.0
  category: architecture-docs
  depends-on: discovery-init
  recommended-after: arch-c4
  output: docs/{projeto}/arquitetura/decisoes/ADR-{NNN}-{titulo}.md
---

# Registro de Decisão de Arquitetura (ADR)

Registra **uma** decisão significativa por arquivo: o que foi decidido, por quê, quais opções foram descartadas e o que muda depois. Complementa a skill `arch-c4`: os diagramas mostram **o que** é a arquitetura; os ADRs explicam **por que** ela é assim.

Template: `references/template-adr.md`.

---

## Pré-requisito

### Passo 0 — Identificar o projeto

A raiz de trabalho é uma pasta de documentação com vários projetos, cada um em `docs/{projeto}/`.

1. Se o usuário citou o projeto, use a pasta dele.
2. Senão, leia `docs/workspace.md`: com um único projeto, use-o e avise; com vários, liste e pergunte qual.
3. Sem `docs/workspace.md`, procure `docs/*/project.md`.
4. Se o projeto não existir, ofereça iniciá-lo com `discovery-init`.

`{projeto}` é a pasta escolhida; todos os caminhos abaixo são relativos à raiz de trabalho.

---

## O que merece um ADR

Decisões **difíceis de reverter** ou que **afetam vários contêineres/times**:
- tecnologia de um contêiner (banco, framework, mensageria, provedor de nuvem);
- estilo de arquitetura (monólito modular, microsserviços, CQRS, eventos);
- forma de integração com um sistema externo;
- autenticação/autorização, multi-tenant, estratégia de cache, armazenamento de arquivos;
- padrões que todo o código deve seguir.

Não merece ADR: escolha local e fácil de trocar (nome de variável, biblioteca de utilitário isolada).

---

## Fluxo de Execução

### Passo 1 — Ler o contexto

- Liste `docs/{projeto}/arquitetura/decisoes/ADR-*.md` e leia o índice `decisoes/README.md`, se existir. Próximo número = maior + 1, com três dígitos (`ADR-007`).
- Verifique se já existe ADR sobre o mesmo assunto. Se existir e estiver **Aceita**, a nova decisão a **substitui** (ver Passo 5).
- Leia `docs/{projeto}/arquitetura/arquitetura.md` (contêineres afetados, pontos em aberto) e, se relevante, o escopo e a especificação.

### Passo 2 — Conduzir a decisão

Uma pergunta por vez:

1. **Contexto**: "Qual problema ou necessidade força essa decisão agora? Quais restrições existem (prazo, equipe, custo, infraestrutura atual, requisitos de qualidade)?"
2. **Opções**: "Quais alternativas foram consideradas?" — pelo menos duas; "não fazer nada" ou "manter como está" conta como opção. Para cada uma: prós, contras e riscos.
3. **Decisão**: "Qual foi escolhida e por quê?" — se ainda não foi decidida, a situação é **Proposta**.
4. **Consequências**: "O que fica mais fácil e o que fica mais difícil? O que precisa ser feito por causa dela (migração, treinamento, mudança no deploy)?"
5. **Envolvidos**: quem decidiu ou precisa aprovar.

**Validação:**
- O contexto explica a força que leva à decisão, não só o resultado.
- Consequências negativas estão registradas (toda decisão tem custo).
- Opções descartadas têm o motivo.

### Passo 3 — Gerar o arquivo

Nome: `docs/{projeto}/arquitetura/decisoes/ADR-{NNN}-{titulo-kebab}.md` (ex.: `ADR-003-armazenamento-de-arquivos-no-r2.md`), com o template de `references/template-adr.md`.

### Passo 4 — Atualizar os índices

1. `docs/{projeto}/arquitetura/decisoes/README.md`: crie se não existir; acrescente a linha (número, título, situação, data).
2. Seção **Decisões de arquitetura** de `docs/{projeto}/arquitetura/arquitetura.md`, se o arquivo existir.
3. Se a decisão resolve um item de **Pontos em aberto** do `arquitetura.md`, marque o item e aponte para o ADR.
4. Se a decisão muda um diagrama (tecnologia de contêiner, nova integração), avise e ofereça atualizar com `arch-c4`.

### Passo 5 — Substituição

ADR aceito **não é editado** no conteúdo da decisão: é substituído.
- No novo ADR: "Substitui: ADR-00X".
- No antigo: situação muda para **Substituída por ADR-00Y** (única alteração permitida, além de correções de digitação).
- Atualize os dois índices.

---

## Situações

| Situação | Quando |
|----------|--------|
| Proposta | Em discussão, ainda não decidida |
| Aceita | Decidida e válida |
| Rejeitada | Discutida e descartada (fica registrada para não ser rediscutida sem fato novo) |
| Obsoleta | Deixou de valer sem substituta (ex.: contêiner removido) |
| Substituída por ADR-NNN | Trocada por outra decisão |

---

## Regras Importantes

- Um ADR = uma decisão.
- Nunca apague um ADR; decisões antigas são histórico.
- Nunca invente motivos ou opções: o que o usuário não souber fica "a definir" e a situação fica **Proposta**.
- Linguagem direta; o ADR deve ser lido em 5 minutos.
- Datas no formato DD/MM/AAAA.

## Exemplos de Uso

**"Registra a decisão de usar PostgreSQL"** — lê `arquitetura.md` (contêiner "Banco" com "PostgreSQL ou SQL Server"), conduz contexto e opções, gera `ADR-001-banco-de-dados-postgresql.md` como Aceita, atualiza o índice, marca o ponto em aberto e oferece atualizar o diagrama de contêineres para "PostgreSQL 16".

**"Vamos trocar o Redis pelo Garnet"** — encontra `ADR-004` (Redis, Aceita), gera `ADR-009` que a substitui, muda a situação da `ADR-004` e atualiza os índices.

## Troubleshooting

**Usuário quer registrar várias decisões de uma vez** — faça uma por vez, cada uma com o seu arquivo.

**Decisão já implementada sem registro** — registre mesmo assim (ADR retroativo), com a data em que foi tomada se o usuário souber, e a data do registro.

**Numeração com buracos ou repetida** — não renumere ADRs existentes (links quebrariam); siga do maior número.
