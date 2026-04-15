# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este repositório

Coleção de **skills modulares** para o Claude Code que cobrem o ciclo completo de desenvolvimento de software — do discovery ao deploy. As skills são instaladas em `.claude/skills/` de projetos externos e guiam equipes através de fases estruturadas de descoberta, especificação, arquitetura e publicação.

## Estrutura de uma skill

```
Skills/
└── nome-da-skill/
    ├── v1/            # versões antigas (apenas skills de discovery)
    ├── v2/            # versão atual (apenas skills de discovery)
    │   ├── SKILL.md   # frontmatter + fluxo de execução
    │   └── references/
    └── SKILL.md       # skills sem versionamento ficam na raiz da pasta
```

Skills de discovery (`discovery-*`, `discovery-scoped`) usam versionamento `v1/`/`v2/`. Skills de arquitetura, spec, plan e deploy não têm versionamento — apenas a versão atual existe na raiz da pasta.

## Frontmatter obrigatório no SKILL.md

```yaml
---
name: nome-da-skill
description: >
  Quando usar (gatilhos em linguagem natural).
  Quando NÃO usar.
metadata:
  version: 1.0.0
  category: discovery | scope | spec | architecture | plan | deploy
  depends-on: skill-anterior     # opcional
  output: docs/{projeto}/pasta/arquivo.md
---
```

## Fluxo de saída dos documentos

Quando as skills são executadas num projeto real, os artefatos são salvos em:

**Com repositório Git** (o repositório já é exclusivo do projeto):
```
docs/
├── project.md                        # gerado por discovery-init
├── discovery/
│   ├── vision.md                     # discovery-vision
│   ├── opportunity.md                # discovery-opportunity
│   ├── assumptions.md                # discovery-assumptions
│   ├── stakeholders.md               # discovery-stakeholders
│   └── success-metrics.md            # discovery-metrics
└── escopo/
    └── {titulo-kebab-case}/
        ├── escopo.md                 # discovery-scoped
        └── discovery/               # snapshot dos docs de discovery usados
```

**Sem repositório Git** (criado localmente):
```
{nome-do-projeto}/
└── docs/
    ├── project.md
    ├── discovery/
    └── escopo/
```

A skill `discovery-init` é sempre o ponto de entrada — ela cria o `project.md` e a estrutura de pastas. Todas as outras skills verificam se `project.md` existe antes de executar.

## Dependências entre skills

```
discovery-init
  └── discovery-vision / opportunity / assumptions / stakeholders / metrics
        └── discovery-scoped
              └── spec-functional
                    └── plan-execution
                          └── architecture-entities / feature / repository / controller
                                └── deploy-dotnet-homolog
                                      └── deploy-dotnet-prod
```

Skills de arquitetura (`architecture-*`) são independentes entre si e podem ser usadas sem discovery prévio.

## Padrões de design das skills

- **Interação conversacional por blocos**: cada skill conduz perguntas temáticas e ao final gera o(s) arquivo(s) `.md`
- **Nunca sobrescrever sem confirmação**: verificar existência do arquivo antes de criar
- **Nomes de pasta em kebab-case**: confirmar com o usuário antes de criar
- **Registrar como "a definir"**: quando o usuário não souber uma informação, seguir normalmente
- **Result Pattern**: skills de arquitetura geram código com `Result<T>` em vez de exceções
- **CQRS com MediatR**: commands (escrita) e queries (leitura) separados, handlers retornam `Result<T>`

## Skills de arquitetura .NET

Geram código seguindo Clean Architecture + DDD + CQRS + Result Pattern:

| Camada | Skill | O que gera |
|--------|-------|------------|
| Domain | `architecture-entities` | Entidade com `Create()` factory, Value Objects imutáveis, interface de repositório |
| Application | `architecture-feature` | Command/Query + Handler + Validator (FluentValidation) |
| Infrastructure | `architecture-repository` | Implementação com `RepositoryBase<TEntity, TId>`, EF Core |
| Infrastructure | `architecture-external-service` | Adapter/Gateway com Polly (retry, circuit breaker, timeout) |
| Presentation | `architecture-controller` | Controller ou Minimal API com OpenAPI e tratamento via Result Pattern |

## Como adicionar ou modificar uma skill

1. Criar a pasta em `Skills/nome-da-skill/` (com versão se for skill de discovery, sem versão para as demais)
2. Criar `SKILL.md` com frontmatter válido e fluxo de execução detalhado
3. Adicionar arquivos de referência em `references/` (templates, exemplos, frameworks teóricos)
4. Atualizar o `README.md` com a nova skill nas tabelas e no diagrama de fluxo
