---
name: scope-generate
description: Gera um novo escopo de projeto consolidando os documentos de discovery existentes. Use esta skill sempre que o usuário mencionar "gerar escopo", "criar escopo", "montar escopo", "definir escopo", "escopo do projeto", "escopo da feature", "escopo do módulo", "quero escopar", "vamos escopar" ou qualquer variação que indique a necessidade de formalizar o que será desenvolvido. Um escopo pode cobrir o projeto inteiro ou apenas uma parte (módulo, feature, fase). Use proativamente sempre que o discovery de um projeto ou parte dele parecer concluído e o time estiver pronto para formalizar o que vai ser construído.
---

# Scope Generate

Skill responsável por gerar um escopo formal a partir dos documentos de discovery existentes, evitando duplicidade com escopos já criados.

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.
- **Se não existir**: informe o usuário que é necessário iniciar o projeto com `discovery-init` antes de gerar um escopo.
- **Se existir**: leia o arquivo para obter o nome do projeto e contexto geral.

---

## Fluxo de execução

### Passo 1 — Identificar o projeto

Pergunte ao usuário:
> "Para qual projeto vamos gerar o escopo?"

Leia o `project.md` do projeto informado para carregar o contexto.

---

### Passo 2 — Ler os documentos de discovery

Leia todos os arquivos disponíveis em `docs/{nome-do-projeto}/discovery/`:

- `vision.md` — visão, problema, público-alvo, proposta de valor
- `opportunity.md` — dores, jobs to be done, oportunidades
- `assumptions.md` — hipóteses críticas e premissas
- `stakeholders.md` — envolvidos, interesses, influências
- `success-metrics.md` — métricas, critérios de sucesso, OKRs

Se algum arquivo não existir, registre como ausente e siga — não bloqueie o fluxo.

---

### Passo 3 — Ler escopos já existentes

Leia todos os arquivos `escopo.md` dentro de `docs/{nome-do-projeto}/escopo/*/`:

Para cada escopo encontrado, extraia:
- **Título do escopo**
- **Situação** (Rascunho / Em revisão / Aprovado / Em execução / Concluído)
- **O que já foi coberto** (funcionalidades, módulos, integrações descritas)

Liste os escopos encontrados para o usuário:
> "Encontrei os seguintes escopos já existentes para esse projeto:
> - `{título}` — Situação: {situação}
> - ...
>
> Vou considerar esses escopos para evitar repetição no novo escopo."

Se não existir nenhum escopo ainda, informe:
> "Nenhum escopo encontrado para esse projeto. Este será o primeiro."

---

### Passo 4 — Definir o título e abrangência do novo escopo

Pergunte:
> "Qual será o título desse escopo?"
> *(Ex: 'Escopo Geral do Projeto', 'Módulo de Autenticação', 'Integração com ERP', 'Fase 1 — MVP')*

Em seguida:
> "Esse escopo cobre o projeto inteiro ou uma parte específica? Se for parcial, me descreva o que ele deve cobrir."

Use a resposta para filtrar quais informações do discovery são relevantes para esse escopo específico.

---

### Passo 5 — Confirmar arquivos de discovery relevantes

Com base no título e abrangência, identifique quais arquivos de discovery são relevantes para este escopo e informe o usuário:

> "Para o escopo '{título}', vou utilizar os seguintes documentos de discovery como base:
> - vision.md ✓
> - opportunity.md ✓
> - assumptions.md ✓
> - stakeholders.md ✓
> - success-metrics.md ✓
>
> Algum desses não deve ser incluído, ou há algum contexto adicional que devo considerar?"

Aguarde confirmação antes de gerar.

---

### Passo 6 — Gerar a estrutura de pastas do escopo

Gere o nome da pasta em kebab-case a partir do título:
- "Módulo de Autenticação" → `modulo-de-autenticacao`
- "Fase 1 — MVP" → `fase-1-mvp`

Crie a estrutura:
```
docs/{nome-do-projeto}/escopo/{titulo-kebab-case}/
├── escopo.md
└── discovery/
    ├── vision.md          (cópia do discovery, se relevante)
    ├── opportunity.md     (cópia do discovery, se relevante)
    ├── assumptions.md     (cópia do discovery, se relevante)
    ├── stakeholders.md    (cópia do discovery, se relevante)
    └── success-metrics.md (cópia do discovery, se relevante)
```

Copie apenas os arquivos de discovery marcados como relevantes para a subpasta `discovery/` dentro do escopo.

---

### Passo 7 — Gerar o `escopo.md`

Salve em:
```
docs/{nome-do-projeto}/escopo/{titulo-kebab-case}/escopo.md
```

Use o template abaixo, preenchido com base nos documentos de discovery lidos:

```markdown
# {Título do Escopo}

**Situação:** Rascunho
**Data de criação:** {DD/MM/YYYY}
**Projeto:** {Nome do Projeto}
**Repositório:** {URL do repositório ou "a definir"}

---

## Contexto

{Resumo do problema e motivação para este escopo, extraído do vision.md}

---

## Abrangência

> O que este escopo cobre e o que está explicitamente fora.

### Inclui
- {item 1}
- {item 2}

### Não inclui (out of scope)
- {item 1}
- {item 2}

---

## Usuários Afetados

{Perfis de usuário impactados por este escopo, extraído de vision.md e stakeholders.md}

| Perfil | Como é afetado |
|---|---|
| {perfil} | {descrição} |

---

## Oportunidades Endereçadas

{Dores e jobs to be done que este escopo resolve, extraído de opportunity.md}

- {oportunidade 1}
- {oportunidade 2}

---

## Funcionalidades e Comportamentos Esperados

{Descrição do que o sistema deve fazer dentro deste escopo — baseado nas oportunidades e na visão}

### {Agrupamento 1}
- {comportamento esperado}
- {comportamento esperado}

### {Agrupamento 2}
- {comportamento esperado}

---

## Hipóteses Críticas Associadas

{Hipóteses de alto impacto relacionadas a este escopo, extraídas de assumptions.md}

| Hipótese | Situação | Como validar |
|---|---|---|
| {hipótese} | {validada / a validar / invalidada} | {método} |

---

## Stakeholders Envolvidos

{Stakeholders relevantes para este escopo, extraídos de stakeholders.md}

| Stakeholder | Papel no escopo | Precisa aprovar? |
|---|---|---|
| {nome} | {papel} | {sim/não} |

---

## Métricas de Sucesso

{Indicadores que definem o sucesso deste escopo, extraídos de success-metrics.md}

| Métrica | Baseline | Meta | Prazo |
|---|---|---|---|
| {métrica} | {valor} | {meta} | {prazo} |

---

## Restrições e Dependências

{Restrições técnicas, organizacionais ou de prazo conhecidas para este escopo}

- {restrição/dependência 1}
- {restrição/dependência 2}

---

## Escopos Relacionados

{Liste escopos existentes do mesmo projeto que têm relação com este}

- [{título do escopo relacionado}](../{pasta-do-escopo}/escopo.md) — {como se relaciona}

---

## Histórico de Situação

| Data | Situação | Observação |
|---|---|---|
| {DD/MM/YYYY} | Rascunho | Criação inicial |
```

---

### Passo 8 — Confirmar e informar

Após gerar tudo, informe o usuário:

> "Escopo **'{título}'** criado com sucesso!
>
> 📄 `docs/{nome-do-projeto}/escopo/{titulo-kebab}/escopo.md`
> 📁 Arquivos de discovery copiados para `docs/{nome-do-projeto}/escopo/{titulo-kebab}/discovery/`
>
> **Situação atual:** Rascunho
>
> Próximos passos sugeridos:
> - Revise o escopo e atualize a situação para **Em revisão** quando estiver pronto para aprovação
> - Inicie a **Especificação** para detalhar as regras de negócio deste escopo"

Atualize o `project.md` marcando a fase de Escopo como iniciada, se ainda não estiver.

---

## Regras importantes

- **Nunca repita** funcionalidades ou comportamentos já cobertos em escopos com situação `Aprovado` ou `Em execução` — sinalize ao usuário se houver sobreposição.
- Se houver sobreposição com um escopo em `Rascunho` ou `Em revisão`, informe mas não bloqueie: "Atenção: o escopo '{outro}' também cobre '{área}'. Deseja consolidar ou manter separados?"
- O campo **Situação** só deve ser alterado manualmente pelo usuário — a skill sempre cria novos escopos como `Rascunho`.
- Se nenhum arquivo de discovery existir, ainda é possível gerar o escopo — mas avise: "Nenhum documento de discovery encontrado. O escopo será gerado com base nas informações que você fornecer agora. Recomendo executar o discovery antes para ter um escopo mais fundamentado."
- O nome da pasta e o título no `escopo.md` devem sempre estar sincronizados.
- Ao copiar arquivos de discovery para a pasta do escopo, **nunca modifique os originais** em `docs/{nome-do-projeto}/discovery/`.
