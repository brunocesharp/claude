# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este repositório

**Marketplace de plugins** do Claude Code que cobre o ciclo completo de desenvolvimento de software — do discovery ao deploy. Cada plugin agrupa um conjunto de skills relacionadas e é instalado via `/plugin marketplace add` + `/plugin install`, guiando equipes através de fases estruturadas de descoberta, especificação, arquitetura e publicação.

## Estrutura do repositório

```
.claude-plugin/
└── marketplace.json          # catálogo dos plugins deste repositório

plugins/
└── nome-do-plugin/
    ├── .claude-plugin/
    │   └── plugin.json        # metadados do plugin
    └── skills/
        └── nome-da-skill/
            ├── SKILL.md        # frontmatter + fluxo de execução
            └── references/
```

Cada plugin reúne as skills de uma fase/stack (discovery, spec-plan, architecture-dotnet, architecture-angular, business-docs). Para adicionar uma skill, crie a pasta em `plugins/<plugin>/skills/<nome-da-skill>/`.

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
  output: "{docs_root}/pasta/arquivo.md"
---
```

## Arquivo de configuração do projeto

Toda skill lê `docs/project-config.json` na raiz do projeto para resolver caminhos e obter contexto. O arquivo é criado por `discovery-init` e nunca precisa ser duplicado em outras skills.

```json
{
  "name": "Nome do Projeto",
  "slug": "nome-do-projeto",
  "version": "1.0.0",
  "setup": "git",
  "docs_root": "docs",
  "repository_url": "https://github.com/org/repo",
  "project_type": "web-api",
  "tech_stack": "dotnet",
  "responsible": "a definir",
  "created_at": "15/04/2026"
}
```

| Campo | Descrição |
|-------|-----------|
| `setup` | `"git"` — repositório existe; `"local"` — sem repositório ainda |
| `docs_root` | Pasta raiz dos documentos (padrão `"docs"`). Todas as skills prefixam caminhos com esse valor |
| `tech_stack` | Tecnologia principal — permite que skills de arquitetura carreguem padrões corretos |

> **Regra de execução:** as skills devem ser sempre executadas a partir da pasta que contém `docs/` (raiz do repositório para setup git; pasta `{slug}/` para setup local).

Schema completo em `Skills/discovery-init/v2/references/project-config-schema.md`.

## Fluxo de saída dos documentos

Quando as skills são executadas num projeto real, os artefatos são salvos relativos ao `docs_root` do `project-config.json`:

```
{docs_root}/
├── project-config.json               # gerado por discovery-init — lido por todas as skills
├── project.md                        # gerado por discovery-init
├── discovery/
│   ├── vision.md                     # discovery-vision
│   ├── opportunity.md                # discovery-opportunity
│   ├── assumptions.md                # discovery-assumptions
│   ├── stakeholders.md               # discovery-stakeholders
│   └── success-metrics.md            # discovery-metrics
├── escopo/
│   └── {titulo-kebab-case}/
│       ├── escopo.md                 # discovery-scoped
│       └── discovery/               # snapshot dos docs de discovery usados
└── especificacao/
    └── {titulo-kebab-case}/
        └── spec-functional.md        # spec-functional
```

**Com repositório Git**: `docs_root = "docs"` na raiz do repo clonado.

**Sem repositório Git**: cria-se `{slug}/docs/` localmente — execute as skills de dentro de `{slug}/`.

A skill `discovery-init` é sempre o ponto de entrada — ela cria `project-config.json`, `project.md` e a estrutura de pastas. Todas as outras skills leem `docs/project-config.json` antes de executar.

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

1. Escolher o plugin correto em `plugins/<plugin>/skills/` (ou criar um novo plugin com `.claude-plugin/plugin.json` e registrá-lo em `.claude-plugin/marketplace.json`)
2. Criar a pasta `plugins/<plugin>/skills/nome-da-skill/`
3. Criar `SKILL.md` com frontmatter válido e fluxo de execução detalhado
4. Adicionar arquivos de referência em `references/` (templates, exemplos, frameworks teóricos)
5. Atualizar o `README.md` com a nova skill nas tabelas e no diagrama de fluxo
