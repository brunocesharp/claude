# Skills para Claude Code — Do Discovery ao Deploy

Um conjunto de skills conversacionais e de geração de código para guiar equipes de desenvolvimento através do ciclo completo de um projeto de software — da ideação ao deploy em produção.

## O que é isso?

Este repositório contém **skills modulares** para o Claude Code que cobrem todo o ciclo de vida de desenvolvimento:

- **Discovery** — entender o problema antes de codar
- **Escopo** — formalizar o que será construído
- **Especificação** — detalhar regras de negócio com BDD
- **Arquitetura** — gerar código .NET seguindo Clean Architecture e CQRS
- **Plano de Execução** — decompor features em tarefas ordenadas
- **Deploy** — publicar em homologação e produção

**Por que usar?**
- Garante que nenhum aspecto importante seja esquecido
- Cria documentação consistente entre projetos
- Gera código seguindo padrões estabelecidos (Clean Architecture, DDD, CQRS, Result Pattern)
- Permite usar apenas as peças que você precisa

---

## Quick Start

### 1. Copie as skills para seu projeto

```bash
# Clone este repositório
git clone <url-do-repositorio> claude-skills

# Copie as skills desejadas para seu projeto
cp -r claude-skills/Skills/discovery-init/v2/* seu-projeto/.claude/skills/discovery-init/
# Repita para cada skill que quiser usar
```

### 2. Inicie um novo projeto

No Claude Code, dentro do seu projeto:

```
> iniciar projeto
```

### 3. Siga o fluxo

```
> definir visão do projeto
> mapear oportunidades
> levantar hipóteses
> identificar stakeholders
> definir métricas de sucesso
> gerar escopo
> especificação funcional
> criar entidade Pedido
> criar command ProcessarPedido
> criar endpoint POST /pedidos
> deploy homologação
```

---

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

### Fase: Especificação

| Skill | Gatilho | Frameworks | Saída |
|-------|---------|------------|-------|
| `spec-functional` | "especificação funcional", "regras de negócio", "cenários BDD" | BDD, Given-When-Then, Feature Injection | `spec-functional.md` |

### Fase: Arquitetura .NET

Skills para geração de código seguindo Clean Architecture, DDD, CQRS e Result Pattern.

| Skill | Gatilho | Camada | Saída |
|-------|---------|--------|-------|
| `architecture-init` | "clean architecture", "estrutura de projeto .NET" | Todas | Estrutura de solução |
| `architecture-entities` | "criar entidade", "aggregate root", "value object" | Domain | `{Entity}.cs`, `I{Entity}Repository.cs` |
| `architecture-feature` | "criar command", "criar query", "use case", "CQRS" | Application | `{Action}{Entity}Command/Query.cs` + Handler + Validator |
| `architecture-repository` | "criar repositório", "repository", "persistência" | Infrastructure | `{Entity}Repository.cs` |
| `architecture-external-service` | "integração com API", "API externa", "adapter", "gateway" | Infrastructure | `{Provider}Adapter.cs` + Gateway + Settings |
| `architecture-controller` | "criar endpoint", "controller", "rota HTTP" | Presentation | Controller/Minimal API + Request/Response models |

### Fase: Plano de Execução

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `plan-execution` | "plano de execução", "dividir em tarefas", "como implementar" | `execution-plan.md` |

### Fase: Deploy .NET

| Skill | Gatilho | Ambiente | Saída |
|-------|---------|----------|-------|
| `deploy-dotnet-homolog` | "deploy homologação", "deploy homolog", "subir para homolog" | Staging | Relatório de deploy |
| `deploy-dotnet-prod` | "deploy produção", "deploy prod", "go live" | Production | Relatório de deploy + info de rollback |

---

## Estrutura do Repositório

```
Skills/
├── discovery-init/          # v1/ e v2/
├── discovery-vision/        # v1/ e v2/
├── discovery-opportunity/   # v1/ e v2/ (com references/)
├── discovery-assumptions/   # v1/ e v2/ (com references/)
├── discovery-stakeholders/  # v1/ e v2/ (com references/)
├── discovery-metrics/       # v1/ e v2/ (com references/)
├── discovery-scoped/        # v1/ e v2/ (com references/)
│
├── spec-functional/
│   ├── SKILL.md
│   └── References/
│       ├── bdd-teoria.md
│       ├── cenarios-given-when-then.md
│       ├── extracao-de-exemplos.md
│       └── template-spec-functional.md
│
├── architecture-init/
│   ├── SKILL.md
│   └── References/
│       ├── domain-layer.md
│       ├── application-layer.md
│       ├── infrastructure-layer.md
│       └── presentation-layer.md
│
├── architecture-entities/
│   ├── SKILL.md
│   └── references/
│       ├── entity-template.md
│       ├── value-objects.md
│       └── repository-interface.md
│
├── architecture-feature/
│   ├── SKILL.md
│   └── references/
│       ├── command-template.md
│       ├── query-template.md
│       └── behaviors.md
│
├── architecture-repository/
│   ├── SKILL.md
│   └── references/
│       ├── repository-base.md
│       ├── repository-implementation.md
│       └── unit-of-work.md
│
├── architecture-external-service/
│   ├── SKILL.md
│   └── references/
│       ├── http-client-base.md
│       ├── adapter-gateway.md
│       ├── resilience.md
│       └── authentication.md
│
├── architecture-controller/
│   ├── SKILL.md
│   └── References/
│       ├── patterns.md
│       ├── structure.md
│       └── examples.md
│
├── plan-execution/
│   ├── SKILL.md
│   └── references/
│       ├── plan-structure.md
│       ├── task-breakdown.md
│       ├── skill-mapping.md
│       └── examples.md
│
├── deploy-dotnet-homolog/
│   ├── SKILL.md
│   └── references/
│       ├── pipeline-steps.md
│       ├── health-check.md
│       └── troubleshooting.md
│
└── deploy-dotnet-prod/
    ├── SKILL.md
    └── references/
        ├── pre-deploy-checklist.md
        ├── pipeline-steps.md
        └── rollback.md
```

> Skills de discovery usam versionamento (`v1/`, `v2/`). Skills de arquitetura e deploy não são versionadas — apenas a versão atual existe na raiz da pasta.

---

## Estrutura de Pastas Gerada no Projeto

Após usar as skills, seu projeto de documentação terá:

```
docs/
└── nome-do-projeto/
    ├── project.md
    ├── discovery/
    │   ├── vision.md
    │   ├── opportunity.md
    │   ├── assumptions.md
    │   ├── stakeholders.md
    │   └── success-metrics.md
    ├── escopo/
    │   └── titulo-do-escopo/
    │       ├── escopo.md
    │       └── discovery/        # snapshot do discovery usado
    └── especificacao/
        └── titulo-do-escopo/
            └── spec-functional.md
```

E seu projeto .NET terá a estrutura Clean Architecture:

```
src/
├── {Solution}.Domain/
│   ├── Entities/
│   ├── ValueObjects/
│   ├── Aggregates/
│   ├── Events/
│   ├── Exceptions/
│   └── Interfaces/
├── {Solution}.Application/
│   ├── {Feature}/
│   │   ├── Commands/
│   │   └── Queries/
│   ├── DTOs/
│   └── Behaviors/
├── {Solution}.Infrastructure/
│   ├── Persistence/
│   │   ├── Repositories/
│   │   └── Configurations/
│   └── ExternalServices/
│       └── {Provider}/
└── {Solution}.Presentation/
    └── Controllers/
```

---

## Como funciona cada skill

### discovery-init

Ponto de entrada. Coleta nome, descrição, URL do repositório e tipo do projeto. Gera `project.md` e cria a estrutura de pastas `discovery/` e `escopo/`.

### discovery-vision / opportunity / assumptions / stakeholders / metrics

Cada skill conduz uma conversa em blocos temáticos e gera um documento `.md` estruturado. Requerem que `project.md` exista. Podem ser usadas em qualquer ordem — use só as que fazem sentido para o seu contexto.

### discovery-scoped

Lê todos os arquivos de `discovery/`, verifica escopos já existentes (evita repetição com escopos `Aprovado` ou `Em execução`) e gera `escopo.md` com estado inicial `Rascunho`. Suporta escopos parciais (módulo, feature, fase).

### spec-functional

Baseada em **BDD** e **Feature Injection**. Para cada funcionalidade do escopo, define narrativa (`In order to / As / I want`) e levanta cenários `Given / When / Then`. Usa Esquema do Cenário para múltiplas combinações de dados. Requer que `escopo.md` exista.

### architecture-init

Define e documenta a estrutura de camadas Clean Architecture para a solução .NET. Serve como referência para todas as outras skills de arquitetura.

### architecture-entities

Gera entidades de domínio ricas (Rich Domain Model), Value Objects imutáveis, Aggregates e interfaces de repositório. Entidades com construtor privado e factory method `Create()`. Sem dependências de infraestrutura.

### architecture-feature

Gera Commands (escrita) e Queries (leitura) seguindo **CQRS** com MediatR. Todos os handlers retornam `Result<T>` (Result Pattern). Commands incluem Validator com FluentValidation. Queries de lista incluem paginação.

### architecture-repository

Gera implementações de repositório na camada Infrastructure herdando de `RepositoryBase<TEntity, TId>`. Usa EF Core com `AsNoTracking()` para queries de leitura. Registra no DI em `DependencyInjection.cs`.

### architecture-external-service

Gera integrações com APIs externas usando padrão **Adapter/Gateway**. Herda de `HttpClientBase`, configura Polly (retry, circuit breaker, timeout), define interface em Application e implementação em Infrastructure.

### architecture-controller

Gera endpoints ASP.NET Core (Controller ou Minimal API) com Request/Response models, validators FluentValidation, documentação OpenAPI e tratamento de erros via Result Pattern. Usa `ISender` do MediatR.

### plan-execution

Analisa a especificação funcional e decompõe em entregas incrementais com tarefas ordenadas por camada (Domain → Infrastructure → Application → Presentation). Referencia a skill correta para cada tipo de tarefa. Inclui estimativas de esforço.

### deploy-dotnet-homolog

Executa pipeline sequencial: Restore → Build → Test → Docker Build → Deploy → Health Check. Interrompe imediatamente em caso de falha. Gera relatório com artefatos e status de cada etapa.

### deploy-dotnet-prod

Igual ao homolog, com etapas extras: confirmação explícita do usuário, validação prévia (branch, commits pendentes, variáveis de ambiente) e procedimento de rollback documentado no relatório.

---

## Para quem é isso?

- **Product Managers** — para conduzir discovery estruturado e gerar escopos
- **Tech Leads** — para garantir alinhamento antes de codar e definir arquitetura
- **Desenvolvedores .NET** — para gerar código seguindo padrões Clean Architecture
- **Analistas de Sistemas** — para especificação funcional com BDD

---

## Fluxo Completo

```
discovery-init
     │
     ▼
discovery-vision ──► discovery-opportunity ──► discovery-assumptions
     │                                               │
     └──────────────────────────────────────────────┘
                          │
                          ▼
              discovery-stakeholders ──► discovery-metrics
                          │
                          ▼
                  discovery-scoped
                          │
                          ▼
                  spec-functional
                          │
                          ▼
                  plan-execution
                          │
                          ▼
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
 architecture-      architecture-    architecture-
   entities           feature         repository
                          │
                          ▼
              architecture-controller
              architecture-external-service
                          │
                          ▼
               deploy-dotnet-homolog
                          │
                          ▼
                deploy-dotnet-prod
```

---

## Dicas de Uso

**Não precisa fazer tudo**
Um projeto pequeno pode precisar só de `discovery-vision` + `discovery-scoped` + skills de arquitetura.

**Itere**
Os documentos são vivos. Rode as skills novamente quando tiver novas informações.

**Escopo parcial**
Um escopo pode cobrir só uma feature ou módulo. O plano de execução divide em entregas incrementais.

**Skills de arquitetura são independentes**
Podem ser usadas sem ter feito discovery — basta saber o que construir.

---

## Roadmap

| Fase | Status | Skills |
|------|--------|--------|
| Discovery | Implementado (v2) | 6 skills |
| Escopo | Implementado (v2) | 1 skill |
| Especificação Funcional | Implementado | `spec-functional` |
| Arquitetura .NET | Implementado | 6 skills |
| Plano de Execução | Implementado | `plan-execution` |
| Deploy .NET | Implementado | `deploy-dotnet-homolog`, `deploy-dotnet-prod` |
| Especificação Não-Funcional | Planejado | `spec-nonfunctional` |
| Refinamento | Planejado | `refinement-screens`, `refinement-api`, `refinement-data-model` |

---

## Estrutura de uma skill

```
nome-da-skill/
├── SKILL.md          # Frontmatter com name/description/metadata + fluxo de execução
└── references/       # Arquivos de referência consultados durante a execução
    ├── template-*.md
    ├── frameworks.md
    ├── troubleshooting.md
    └── examples.md
```

O frontmatter do `SKILL.md` deve ter:
- `name` — identificador
- `description` — gatilhos e quando NÃO usar
- `metadata` — versão, categoria, `depends-on`, `output`

---

## Contribuindo

1. Fork este repositório
2. Crie uma branch (`git checkout -b feature/nova-skill`)
3. Commit suas mudanças
4. Abra um Pull Request

---

## Licença

MIT

---

**Feito para times que querem parar de começar projetos no escuro — e terminar deploys no escuro também.**
