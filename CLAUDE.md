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

Plugins: `sdd` (hub `sdd-setup`: setup, status e próximo passo), `workspace` (multi-repo), `discovery`, `spec-plan`, `architecture-docs` (C4 e ADR), `architecture-dotnet`, `architecture-angular`, `architecture-java`, `business-docs`, `art-direction` (direção de arte). Para adicionar uma skill, crie a pasta em `plugins/<plugin>/skills/<nome-da-skill>/`.

## Frontmatter obrigatório no SKILL.md

```yaml
---
name: nome-da-skill            # IGUAL ao nome da pasta
description: >
  Quando usar (gatilhos em linguagem natural).
  Quando NÃO usar (citando o nome real de outras skills).
metadata:
  version: 1.0.0
  category: workspace | discovery | scope | spec | architecture-docs | architecture | plan | deploy
  depends-on: skill-anterior     # opcional
  output: docs/{projeto}/pasta/arquivo.md
---
```

O `name` é o identificador usado para invocar a skill e citado nas outras skills: mantenha igual ao nome da pasta. Ao renomear uma skill, procure o nome antigo em todo o repositório.

## Workspace com vários projetos

As skills de documentação rodam numa **pasta só de documentação** (workspace) que reúne vários projetos. O código de cada projeto fica no próprio repositório; o caminho local fica no `project.md`.

```
_sdd/                                 # sdd-setup: config.toml (time), config.user.toml (pessoal), version.toml, scripts/
docs/
├── workspace.md                      # projetos: pasta, repositório, código local, situação (discovery-init)
├── arquitetura/landscape.md          # visão de todos os sistemas (arch-c4, opcional)
└── {projeto}/
    ├── project-config.json           # discovery-init: configuração lida pelas skills (schema em discovery-init/references)
    ├── project.md                    # discovery-init: resumo para pessoas
    ├── repositorios.md               # multi-repo (só com código em vários repositórios)
    ├── discovery/                    # discovery-vision / opportunity / assumptions / stakeholders / metrics
    ├── escopo/{titulo}/escopo.md     # discovery-scoped (+ discovery/ com o snapshot usado)
    ├── especificacao/{escopo}/spec-functional.md   # spec-functional
    ├── arquitetura/                  # arch-c4 (arquitetura.md, componentes/, dinamicos/) e arch-adr (decisoes/)
    ├── plano-execucao/{escopo}/execution-plan.md   # plan-execution
    ├── implementacao/sprint-status.yaml            # estado de épicos e stories (status.py; formato em sdd-setup/references/sprint-status.md)
    └── business/                     # business-docs (areas.md + {area}.md)
```

**Toda skill de documentação começa com o "Passo 0 — Identificar o projeto"** (mesmo texto em todas):
1. Projeto citado na conversa → usa a pasta dele.
2. Senão, lê `docs/workspace.md`: um projeto → usa e avisa; vários → lista e pergunta.
3. Sem `workspace.md` → procura `docs/*/project.md`.
4. Projeto inexistente → oferece `discovery-init`.
5. Lê `docs/{projeto}/project-config.json` (nome, stack, repositório); sem ele, usa o `project.md` e oferece criar o config.
6. Lê a configuração do workspace em `_sdd/config.toml` + `_sdd/config.user.toml` (o pessoal vence): idioma da conversa e dos documentos, nome e nível do usuário, `paths.docs_root`. Sem `_sdd/`, usa os padrões e sugere o `sdd-setup` uma vez.

Ao mudar esse passo, mude em todas as skills. Skills que avançam de fase atualizam o `project.md` e a coluna Situação do `workspace.md`.

**Onde está o código:** projeto de um repositório usa `repository_url` e `code_path` do `project-config.json` (espelhados no `project.md`); com dois ou mais, a fonte única é `docs/{projeto}/repositorios.md` (skill `multi-repo`: papel, caminho, contêineres C4 e contratos de cada repositório). Skills que leem código (`arch-c4`, `business-docs`, `plan-execution`) consultam os dois. Nenhuma skill faz commit, push ou merge nos repositórios de código sem pedido explícito.

Nada fica guardado nos arquivos da skill por projeto: configuração específica de um projeto (ex.: mapa de áreas do `business-docs`) vai para `docs/{projeto}/`.

## Configuração do workspace e scripts (`sdd-setup`)

- Cada plugin que precisa de configuração declara as perguntas em `plugins/sdd/skills/sdd-setup/modules/<plugin>.toml` (`key`, `prompt`, `default`, `scope` team|user). A `version` do registro é igual à do `plugin.json`: ao subir uma, suba a outra (há teste). Chaves e uso em `sdd-setup/references/config-schema.md`.
- Scripts em Python ≥ 3.11, executados com `uv run` (fallback `python`), só biblioteca padrão ou dependências inline (PEP 723). Imprimem JSON; em erro, `error: <mensagem>` e código 1. Os de runtime são copiados pelo setup para `_sdd/scripts/`, de onde as skills de qualquer plugin os chamam (`${CLAUDE_PLUGIN_ROOT}` só vale dentro do próprio plugin). Toda skill que usa script descreve o caminho sem `uv`.
- Runtime em `_sdd/scripts/`: `config.py` (configuração), `workspace.py` (projetos, fase, quadro do sprint) e `status.py` (estados do `sprint-status.yaml`, com as transições de `sdd-setup/references/sprint-status.md`). `setup.py` e `migrate.py` rodam da pasta da skill. O hook do plugin (`plugins/sdd/hooks/hooks.json`) valida o `sprint-status.yaml` a cada Write/Edit.
- Testes: `uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests`.

## Dependências entre skills

```
sdd-setup (uma vez por workspace; recomendado, não obrigatório)
discovery-init
  └── discovery-vision / opportunity / assumptions / stakeholders / metrics
        └── discovery-scoped
              └── spec-functional
                    └── arch-c4  <->  arch-adr
                          └── plan-execution  ->  multi-repo (mudança coordenada, se houver vários repositórios)
                                └── architecture-entities / feature / repository / controller, angular-*
                                      └── deploy-dotnet-homolog
                                            └── deploy-dotnet-prod
```

Skills de código (`architecture-*`, `angular-*`) são independentes entre si e podem ser usadas sem discovery prévio. A `arch-c4` também roda sem discovery, no modo Levantamento (lê o código do projeto).

## Padrões de design das skills

- **Interação conversacional por blocos**: cada skill conduz perguntas temáticas e ao final gera o(s) arquivo(s) `.md`
- **Nunca sobrescrever sem confirmação**: verificar existência do arquivo antes de criar
- **Nomes de pasta em kebab-case**: confirmar com o usuário antes de criar
- **Registrar como "a definir"**: quando o usuário não souber uma informação, seguir normalmente
- **Result Pattern**: skills de código .NET geram código com `Result<T>` em vez de exceções
- **CQRS com MediatR**: commands (escrita) e queries (leitura) separados, handlers retornam `Result<T>`

## Skills de documentação de arquitetura (C4)

Baseadas em *The C4 model for visualising software architecture* (Simon Brown). Diagramas em **Mermaid C4** dentro do Markdown.

| Skill | O que gera |
|-------|------------|
| `arch-c4` | `arquitetura.md` com contexto e contêineres (obrigatórios), componentes por contêiner (opcional), deployment por ambiente, dinâmicos e landscape (opcionais), glossário e pontos em aberto. Modos Design, Levantamento (código) e Atualização |
| `arch-adr` | Um ADR por decisão (`decisoes/ADR-NNN-titulo.md`) + índice; decisão aceita é substituída, não editada |

O Mermaid C4 é experimental: não desenha legenda (cada diagrama tem tabela de legenda abaixo) e o layout segue a ordem das declarações. Detalhes em `plugins/architecture-docs/skills/arch-c4/references/mermaid-c4.md`.

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
3. Criar `SKILL.md` com frontmatter válido (`name` = nome da pasta) e fluxo de execução detalhado; skill de documentação começa com o Passo 0 e salva em `docs/{projeto}/`
4. Adicionar arquivos de referência em `references/` (templates, exemplos, frameworks teóricos)
5. Atualizar o `README.md` com a nova skill nas tabelas e no diagrama de fluxo, e o `0.0 - contexto-projeto-skills.md`

## Arquivos que não vão para o Git

Livros e PDFs de referência (ex.: o livro do C4) ficam só na máquina local: são material com direitos autorais e o repositório é público. O conteúdo necessário vai resumido nas `references/` das skills, citando a fonte.
