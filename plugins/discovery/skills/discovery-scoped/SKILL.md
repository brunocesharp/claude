---
name: scope-generate
description: Gera um documento de escopo consolidando os documentos de discovery existentes, criando a pasta escopo/{titulo}/escopo.md com cópias dos arquivos de discovery relevantes. Use quando o usuário mencionar "gerar escopo", "criar escopo", "montar escopo", "definir escopo", "escopo do projeto", "escopo da feature", "PRD", "documento de requisitos", "o que vamos construir", "formalizar o que será feito", "consolidar discovery", "fechar escopo", "escopo do módulo", "escopo da fase". Requer discovery-init e preferencialmente os documentos de discovery completos. NÃO use para conduzir discovery (use as skills discovery-*), especificação técnica (use spec-*) ou plano de execução (use plan-*). Esta skill CONSOLIDA o discovery em um documento formal, não coleta novas informações.
metadata:
  author: Equipe de Discovery
  version: 1.1.0
  category: scope
  depends-on: discovery-init
  recommended-after: discovery-metrics
  output: "{docs_root}/escopo/{titulo}/escopo.md"
  consolidates: vision, opportunity, assumptions, stakeholders, success-metrics
---

# Scope Generate

Gera um escopo formal a partir dos documentos de discovery existentes, evitando duplicidade com escopos já criados.

Para o template completo do escopo, consulte `references/template-escopo.md`.

Para o fluxo de aprovação e estados, consulte `references/situation-management.md`.

---

## Pré-requisito

Leia `docs/project-config.json` para obter a configuração do projeto.

- **Se não existir**: informe que é necessário executar `discovery-init` e ofereça criar agora.
- **Se existir**: extraia `docs_root` (padrão: `"docs"`). Use esse valor como prefixo em todos os caminhos desta skill. Leia `{docs_root}/project.md` para obter nome e contexto geral.

> Execute sempre as skills a partir da raiz do projeto (pasta que contém `docs/`).

---

## Fluxo de Execução

### Passo 1 — Identificar o projeto

> "Para qual projeto vamos gerar o escopo?"

Leia `{docs_root}/project.md` para confirmar o projeto.

**Validação:**
- Se não existir, ofereça criar com `discovery-init`

---

### Passo 2 — Ler os documentos de discovery

Leia todos os arquivos em `{docs_root}/discovery/`:

- `vision.md` — visão, problema, público-alvo
- `opportunity.md` — dores, jobs to be done
- `assumptions.md` — hipóteses críticas
- `stakeholders.md` — envolvidos, interesses
- `success-metrics.md` — métricas, critérios de sucesso

**Validação:**
- Pelo menos `vision.md` OU `opportunity.md` deve existir
- Se < 3 arquivos: avise "Discovery incompleto — escopo pode ficar superficial"
- Se nenhum arquivo: ofereça conduzir discovery primeiro ou prossiga com aviso

---

### Passo 3 — Ler escopos já existentes

Leia todos os `escopo.md` em `{docs_root}/escopo/*/escopo.md`:

Para cada escopo, extraia:
- Título
- Situação (Rascunho / Em revisão / Aprovado / Em execução / Concluído)
- Funcionalidades cobertas

> "Encontrei os seguintes escopos existentes:
> - `{título}` — Situação: {situação}
> 
> Vou considerar para evitar repetição."

Se nenhum escopo existir:
> "Este será o primeiro escopo do projeto."

**Validação:**
- Se houver sobreposição potencial, sinalize ANTES de gerar

---

### Passo 4 — Definir título e abrangência

> "Qual será o título desse escopo?"
> *(Ex: 'Escopo Geral do Projeto', 'Módulo de Autenticação', 'Fase 1 — MVP')*

> "Esse escopo cobre o projeto inteiro ou uma parte específica?"

**Validação:**
- Título deve ser descritivo (não apenas "Escopo 1")
- Se cobrir tudo, confirme: "Então este é o escopo geral do projeto?"
- Se for parcial, pergunte exatamente o que inclui e exclui

---

### Passo 5 — Confirmar arquivos relevantes

Com base no título e abrangência:

> "Para o escopo '{título}', vou utilizar:
> - vision.md ✓
> - opportunity.md ✓
> - assumptions.md ✓
> - stakeholders.md ✓
> - success-metrics.md ✓
>
> Algum não deve ser incluído, ou há contexto adicional?"

**Validação:**
- Aguarde confirmação antes de gerar
- Se usuário adicionar contexto, incorpore

---

### Passo 6 — Gerar estrutura de pastas

Converta título para kebab-case:
- "Módulo de Autenticação" → `modulo-de-autenticacao`
- "Fase 1 — MVP" → `fase-1-mvp`

Crie a estrutura em `{docs_root}/escopo/{titulo-kebab}/`:

```
{docs_root}/escopo/{titulo-kebab}/
├── escopo.md
└── discovery/
    ├── vision.md          (cópia, se relevante)
    ├── opportunity.md     (cópia, se relevante)
    ├── assumptions.md     (cópia, se relevante)
    ├── stakeholders.md    (cópia, se relevante)
    └── success-metrics.md (cópia, se relevante)
```

**Validação:**
- Nunca modifique os originais em `discovery/`
- Apenas copie arquivos marcados como relevantes

---

### Passo 7 — Gerar o escopo.md

Use o template em `references/template-escopo.md`.

Preencha com base nos documentos de discovery lidos.

Para checklist de qualidade, consulte `references/checklist.md`.

**Validação:**
- Todas as seções obrigatórias preenchidas
- Funcionalidades conectadas a oportunidades
- Métricas com baseline e meta

---

### Passo 8 — Confirmar e informar

> "Escopo **'{título}'** criado com sucesso!
>
> 📄 `{docs_root}/escopo/{titulo-kebab}/escopo.md`
> 📁 Discovery copiado para `{docs_root}/escopo/{titulo-kebab}/discovery/`
>
> **Situação:** Rascunho
>
> Próximos passos:
> - Revise e atualize para **Em revisão** quando pronto
> - Inicie a **Especificação** para detalhar regras de negócio"

Atualize `project.md` marcando Escopo como iniciado.

---

## Regras Importantes

### Comportamento Obrigatório

- **Nunca repita** funcionalidades de escopos `Aprovado` ou `Em execução`
- **Sinalize sobreposição** com escopos em `Rascunho` ou `Em revisão`, mas não bloqueie
- **Sempre crie como Rascunho** — situação só muda manualmente
- **Nunca modifique** arquivos originais de discovery
- **Mantenha sincronizado** nome da pasta e título no arquivo

### O Que NÃO Fazer

- Não gere escopo sem pelo menos 1 documento de discovery (ou aviso explícito)
- Não repita funcionalidades já cobertas em escopos aprovados
- Não deixe seções obrigatórias vazias
- Não liste funcionalidades sem oportunidade correspondente
- Não ignore hipóteses críticas pendentes de validação

### Adaptação de Tom

- **Para PMs:** Foque em funcionalidades e métricas
- **Para devs/tech leads:** Destaque restrições técnicas e dependências
- **Para stakeholders:** Enfatize abrangência e critérios de aprovação

---

## Troubleshooting

Para problemas comuns, consulte `references/troubleshooting.md`.

Resumo dos mais frequentes:
- **Discovery incompleto** → gere com aviso ou conduza discovery primeiro
- **Sobreposição com escopo existente** → consolide ou delimite claramente
- **Escopo muito grande** → sugira dividir em fases ou módulos
- **Funcionalidades sem oportunidade** → questione se realmente são necessárias

---

## Exemplos

Para exemplos detalhados de uso, consulte `references/examples.md`.
