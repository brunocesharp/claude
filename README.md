# Skills de Discovery para Claude Code

Um conjunto de skills conversacionais para guiar equipes de desenvolvimento através do ciclo completo de um projeto de software — da ideação à produção.

## O que é isso?

Este repositório contém **skills modulares** para o Claude Code que ajudam a construir documentação de projeto de forma estruturada e conversacional. Cada skill conduz uma conversa focada em um aspecto específico do projeto e gera documentos `.md` padronizados.

**Por que usar?**
- Garante que nenhum aspecto importante seja esquecido
- Cria documentação consistente entre projetos
- Funciona como um facilitador de discovery e escopo
- Permite usar apenas as peças que você precisa

## Quick Start

### 1. Copie as skills para seu projeto

```bash
# Clone este repositório
git clone <url-do-repositorio> claude-skills

# Copie a versão mais recente de cada skill para seu projeto
cp -r claude-skills/Skills/discovery-init/v2/SKILL.md seu-projeto/.claude/skills/discovery-init/SKILL.md
# Repita para cada skill que quiser usar
```

### 2. Inicie um novo projeto

No Claude Code, dentro do seu projeto:

```
> iniciar projeto
```

O Claude vai guiar você pelo setup inicial.

### 3. Siga o fluxo de discovery

Após o init, siga as skills de discovery na ordem que fizer sentido:

```
> definir visão do projeto
> mapear oportunidades
> levantar hipóteses
> identificar stakeholders
> definir métricas de sucesso
```

### 4. Gere o escopo

Com o discovery completo (ou parcialmente completo):

```
> gerar escopo
```

## Skills Disponíveis

### Fase: Discovery

| Skill | Gatilho | Frameworks | Saída |
|-------|---------|------------|-------|
| `discovery-init` | "iniciar projeto", "novo projeto" | — | `project.md` |
| `discovery-vision` | "visão do projeto", "proposta de valor" | Lean Canvas, Value Proposition Canvas | `vision.md` |
| `discovery-opportunity` | "mapear oportunidades", "jobs to be done" | Opportunity Solution Tree, JTBD | `opportunity.md` |
| `discovery-assumptions` | "hipóteses", "premissas" | Assumption Mapping, Lean Startup | `assumptions.md` |
| `discovery-stakeholders` | "stakeholders", "partes interessadas" | Power-Interest Matrix | `stakeholders.md` |
| `discovery-metrics` | "métricas", "KPIs", "como medir sucesso" | OKR, North Star Metric, HEART, AARRR | `success-metrics.md` |

### Fase: Escopo

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `discovery-scoped` | "gerar escopo", "criar escopo" | `escopo.md` + cópia do discovery |

## Estrutura do Repositório

As skills são versionadas. A versão mais recente é sempre a que deve ser usada em projetos novos.

```
Skills/
├── discovery-init/
│   ├── v1/
│   │   └── SKILL.md
│   └── v2/
│       └── SKILL.md
├── discovery-vision/
│   ├── v1/
│   │   └── SKILL.md
│   └── v2/
│       └── SKILL.md
├── discovery-opportunity/
│   ├── v1/
│   │   └── SKILL.md
│   └── v2/
│       ├── SKILL.md
│       └── references/
│           ├── frameworks.md
│           ├── template-opportunity.md
│           ├── troubleshooting.md
│           └── examples.md
├── discovery-assumptions/
│   ├── v1/
│   │   └── SKILL.md
│   └── v2/
│       ├── SKILL.md
│       └── references/
│           ├── frameworks.md
│           ├── prioritization.md
│           ├── validation-methods.md
│           ├── template-assumptions.md
│           ├── troubleshooting.md
│           └── examples.md
├── discovery-stakeholders/
│   ├── v1/
│   │   └── SKILL.md
│   └── v2/
│       ├── SKILL.md
│       └── references/
│           ├── frameworks.md
│           ├── classification.md
│           ├── engagement-strategies.md
│           ├── template-stakeholders.md
│           ├── troubleshooting.md
│           └── examples.md
├── discovery-metrics/
│   ├── v1/
│   │   └── SKILL.md
│   └── v2/
│       ├── SKILL.md
│       └── references/
│           ├── frameworks.md
│           ├── metrics-catalog.md
│           ├── baseline-and-goals.md
│           ├── template-metrics.md
│           ├── troubleshooting.md
│           └── examples.md
└── discovery-scoped/
    ├── v1/
    │   └── SKILL.md
    └── v2/
        ├── SKILL.md
        └── references/
            ├── template-escopo.md
            ├── checklist.md
            ├── situation-management.md
            ├── troubleshooting.md
            └── examples.md
```

## Estrutura de Pastas Gerada no Projeto

Após usar as skills, seu projeto terá esta estrutura:

```
seu-projeto/
├── .claude/
│   └── skills/           # Skills copiadas para cá
│       ├── discovery-init/
│       │   └── SKILL.md
│       ├── discovery-vision/
│       │   └── SKILL.md
│       ├── discovery-opportunity/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── discovery-assumptions/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── discovery-stakeholders/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── discovery-metrics/
│       │   ├── SKILL.md
│       │   └── references/
│       └── discovery-scoped/
│           ├── SKILL.md
│           └── references/
│
└── docs/
    └── nome-do-projeto/
        ├── project.md              # Metadados do projeto
        ├── discovery/
        │   ├── vision.md
        │   ├── opportunity.md
        │   ├── assumptions.md
        │   ├── stakeholders.md
        │   └── success-metrics.md
        └── escopo/
            └── titulo-do-escopo/
                ├── escopo.md       # Documento consolidado
                └── discovery/      # Snapshot do discovery usado
```

## Para quem é isso?

- **Product Managers** — para conduzir discovery estruturado
- **Tech Leads** — para garantir alinhamento antes de codar
- **Desenvolvedores** — para entender o contexto completo
- **Analistas de Sistemas** — para documentação consistente

## Como funciona cada skill

### discovery-init

Ponto de entrada. Coleta informações básicas:
- Nome do projeto
- Descrição resumida
- URL do repositório Git
- Tipo de projeto

Gera `project.md` e cria a estrutura de pastas `discovery/` e `escopo/`.

### discovery-vision

Baseada em **Lean Canvas** e **Value Proposition Canvas**. Explora:
- Qual problema estamos resolvendo?
- Para quem?
- Qual a proposta de valor?
- Quais as restrições?

### discovery-opportunity

Baseada em **Opportunity Solution Tree** (Teresa Torres) e **Jobs to Be Done**. Mapeia:
- Jobs que o usuário quer realizar
- Dores atuais
- Desejos e expectativas
- Tentativas anteriores de resolver

Nunca sugere soluções durante essa etapa — foco total no problema.

### discovery-assumptions

Baseada em **Assumption Mapping** (Bland & Osterwalder) e **Lean Startup**. Identifica:
- Hipóteses sobre usuários
- Hipóteses de negócio
- Hipóteses técnicas
- Priorização por impacto × certeza

Hipóteses com **alto impacto + baixa certeza** são priorizadas para validação imediata.

### discovery-stakeholders

Baseada na **Power-Interest Matrix**. Mapeia:
- Quem aprova?
- Quem é afetado?
- Classificação por influência × interesse
- Estratégia de comunicação por perfil

### discovery-metrics

Baseada em **OKRs**, **North Star Metric**, **HEART Framework** e **AARRR**. Define:
- Métrica principal (North Star — uma única)
- KPIs de negócio
- KPIs de produto/usuário
- Critérios de aceitação
- Baseline e metas com prazo

### discovery-scoped

Consolida todo o discovery em um documento de escopo formal:
- Lê todos os arquivos de `discovery/` existentes
- Verifica escopos já criados (evita duplicidade com escopos `Aprovado` ou `Em execução`)
- Define título, abrangência (inclui/não inclui) e situação inicial (`Rascunho`)
- Gera `escopo.md` com funcionalidades, métricas, hipóteses críticas e stakeholders
- Copia snapshot do discovery usado

## Roadmap

| Fase | Status | Skills |
|------|--------|--------|
| Discovery | Implementado | 6 skills (v2) |
| Escopo | Implementado | 1 skill (v2) |
| Especificação | Planejado | `spec-business-rules`, `spec-functional`, `spec-nonfunctional` |
| Refinamento | Planejado | `refinement-screens`, `refinement-api`, `refinement-data-model` |
| Plano de Execução | Planejado | `plan-tasks`, `plan-estimation` |
| Homologação | Planejado | `deploy-homolog` |
| Produção | Planejado | `deploy-production` |

## Dicas de Uso

**Não precisa fazer tudo**
Use só as skills que fazem sentido para seu contexto. Um projeto pequeno pode precisar só de `discovery-vision` e `discovery-scoped`.

**Itere**
Os documentos são vivos. Rode as skills novamente quando tiver novas informações.

**Escopo parcial**
Um escopo pode cobrir só uma feature ou módulo, não precisa ser o projeto inteiro.

**Múltiplos escopos**
Projetos grandes podem ter vários escopos, cada um com seu ciclo de vida independente.

## Contribuindo

1. Fork este repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-skill`)
3. Commit suas mudanças (`git commit -m 'Adiciona skill X'`)
4. Push para a branch (`git push origin feature/nova-skill`)
5. Abra um Pull Request

### Estrutura de uma skill (v2)

```
nome-da-skill/
└── v2/
    ├── SKILL.md          # Instruções principais para o Claude
    └── references/       # Arquivos de referência (frameworks, templates, exemplos)
        ├── frameworks.md
        ├── template-*.md
        ├── troubleshooting.md
        └── examples.md
```

O `SKILL.md` deve conter no frontmatter:
- `name` — identificador da skill
- `description` — texto completo com gatilhos e quando NÃO usar
- `metadata` — versão, categoria, dependências, output

O corpo do `SKILL.md` deve conter:
- Pré-requisitos
- Fluxo conversacional por blocos temáticos
- Regras obrigatórias e o que NÃO fazer
- Adaptação de tom por perfil de usuário
- Referências para arquivos em `references/`

## Licença

MIT

---

**Feito para times que querem parar de começar projetos no escuro.**
