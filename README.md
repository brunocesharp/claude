# Skills para Claude Code — Do Discovery ao Deploy

Um conjunto de skills conversacionais e de geração de código para guiar equipes de desenvolvimento através do ciclo completo de um projeto de software — da ideação ao deploy em produção.

## O que é isso?

Este repositório contém **skills modulares** para o Claude Code que cobrem todo o ciclo de vida de desenvolvimento:

- **Discovery** — entender o problema antes de codar
- **Escopo** — formalizar o que será construído
- **Especificação** — detalhar regras de negócio com BDD
- **Arquitetura (documentação)** — descrever o sistema no modelo C4 e registrar decisões (ADR)
- **Direção de arte** — definir a identidade visual do produto
- **Plano de Execução** — decompor features em tarefas ordenadas
- **Arquitetura (código)** — gerar código .NET, Angular e testes Java seguindo Clean Architecture e CQRS
- **Deploy** — publicar em homologação e produção

**Por que usar?**
- Garante que nenhum aspecto importante seja esquecido
- Cria documentação consistente entre projetos
- Gera código seguindo padrões estabelecidos (Clean Architecture, DDD, CQRS, Result Pattern)
- Permite usar apenas as peças que você precisa

---

## Quick Start

### 1. Instale os plugins

As skills são distribuídas como **plugins** do Claude Code. A instalação tem duas etapas, nesta ordem:

1. **Conectar o Claude Code a este repositório** (registrar o marketplace). Sem isso, o Claude Code não conhece os plugins e o `/plugin install` responde que o plugin não foi encontrado.
2. **Instalar os plugins** que você quer usar.

Os comandos que começam com `/` são digitados **no prompt do Claude Code**, numa sessão aberta no seu computador (o `/plugin` não funciona por Remote Control). Se preferir o terminal do sistema, veja "Alternativa: pelo terminal" mais abaixo.

#### Etapa 1 — Conectar ao repositório

```
/plugin marketplace add brunocesharp/claude
```

O Claude Code baixa o catálogo (`.claude-plugin/marketplace.json`) do GitHub e registra o marketplace com o nome **`claude`**. A resposta esperada é `Successfully added marketplace: claude`. Isso é feito uma vez por máquina.

#### Etapa 2 — Instalar os plugins

Cada plugin é instalado com `/plugin install <plugin>@claude` (o `@claude` é o nome do marketplace registrado na etapa 1). Instale só os que fazem sentido para você:

```
/plugin install sdd@claude
/plugin install workspace@claude
/plugin install discovery@claude
/plugin install spec-plan@claude
/plugin install architecture-docs@claude
/plugin install architecture-dotnet@claude
/plugin install architecture-angular@claude
/plugin install architecture-java@claude
/plugin install business-docs@claude
/plugin install art-direction@claude
```

Cada comando responde `Installed <plugin>. Plugin is now active.` Também dá para instalar pelo menu: digite `/plugin` e escolha os plugins do marketplace `claude`.

#### Etapa 3 — Recarregar e conferir

```
/reload-plugins
/plugin list
```

O `/reload-plugins` ativa as skills na sessão atual (ou abra uma sessão nova). O `/plugin list` mostra os plugins instalados, cada um como `<plugin>@claude ... enabled`.

#### Atualizar quando sair versão nova

O Claude Code guarda uma cópia do catálogo. Para buscar plugins e versões novas deste repositório:

```
/plugin marketplace update claude
/reload-plugins
```

#### Alternativa: pelo terminal

As mesmas etapas, sem abrir uma sessão (útil em script de configuração da máquina):

```bash
claude plugin marketplace add brunocesharp/claude
claude plugin install discovery@claude
claude plugin install architecture-docs@claude
# ... um comando por plugin
claude plugin marketplace update claude   # para atualizar depois
```

Por padrão a instalação vale para o seu usuário em qualquer pasta (`--scope user`). Com `--scope project`, ela fica registrada no `.claude/settings.json` do projeto.

#### Alternativa: pelo Skills CLI

Também dá para instalar as skills, sem o sistema de plugins, com o [Skills CLI](https://skills.sh) (precisa de Node.js e Git). Rode na pasta do workspace:

```bash
npx skills add brunocesharp/claude --skill '*'          # todas as skills
npx skills add brunocesharp/claude                      # escolher as skills numa lista
npx skills add brunocesharp/claude --skill sdd-setup --skill discovery-init
npx skills update                                       # para atualizar depois
```

Use um caminho só (plugins **ou** Skills CLI) para a mesma skill: com as duas cópias, o Claude pode usar a antiga. Inclua sempre a `sdd-setup`.

#### Problemas comuns

- **Plugin não encontrado** no `/plugin install`: a etapa 1 não foi feita, ou o nome está sem o marketplace (use `<plugin>@claude`).
- **`/plugin isn't available`**: a sessão está em Remote Control. Rode os comandos no Claude Code aberto no computador ou use a alternativa pelo terminal.
- **A skill não aparece**: rode `/reload-plugins` ou abra uma sessão nova.
- **Skill duplicada ou com comportamento antigo**: se você tinha copiado skills à mão para `~/.claude/skills/` (ou subido como skill no claude.ai), remova essas cópias. Com as duas versões, o Claude pode escolher a antiga.

| Plugin | Skills |
|--------|--------|
| `sdd` | `sdd-setup` |
| `workspace` | `multi-repo` |
| `discovery` | `discovery-init`, `discovery-vision`, `discovery-opportunity`, `discovery-assumptions`, `discovery-stakeholders`, `discovery-metrics`, `discovery-scoped` |
| `spec-plan` | `spec-functional`, `plan-execution` |
| `architecture-docs` | `arch-c4`, `arch-adr` |
| `architecture-dotnet` | `architecture-init`, `architecture-entities`, `architecture-feature`, `architecture-repository`, `architecture-external-service`, `architecture-controller`, `deploy-dotnet-homolog`, `deploy-dotnet-prod` |
| `architecture-angular` | `angular-core-layer`, `angular-feature-layer`, `angular-shared-layer`, `angular-rxjs-transversal` |
| `architecture-java` | `architecture-unit-test` |
| `business-docs` | `business-docs` |
| `art-direction` | `direcao-arte-fundacao` |

#### Para o time: instalação pelo projeto

Para que cada pessoa não precise digitar os comandos, declare o marketplace e os plugins no `.claude/settings.json` do repositório do time (o workspace de documentação, por exemplo). Quando a pessoa abre o Claude Code nessa pasta e aceita a pergunta de confiança da pasta, o Claude Code registra o marketplace e ativa os plugins listados (em pasta não confiável a configuração é ignorada):

```json
{
  "extraKnownMarketplaces": {
    "claude": {
      "source": { "source": "github", "repo": "brunocesharp/claude" }
    }
  },
  "enabledPlugins": {
    "workspace@claude": true,
    "discovery@claude": true,
    "spec-plan@claude": true,
    "architecture-docs@claude": true,
    "architecture-dotnet@claude": true
  }
}
```

### 2. Prepare a pasta de documentação (workspace)

As skills de documentação trabalham numa **pasta só de documentação que reúne vários projetos**. Cada projeto fica em `docs/{projeto}/`, e o código de cada um continua no próprio repositório (o caminho fica registrado no `project.md`). Abra o Claude Code nessa pasta:

```
meu-workspace/            # ex.: um repositório "docs" do time
└── docs/
    ├── workspace.md      # lista dos projetos
    ├── projeto-a/
    └── projeto-b/
```

Na primeira vez, configure o workspace:

```
> sdd setup
```

A `sdd-setup` pergunta o nome do workspace, como te chamar, seu nível de experiência, o idioma da conversa e dos documentos e a pasta de documentação, e grava em `_sdd/` na raiz do workspace:

```
meu-workspace/
├── _sdd/
│   ├── config.toml        # do time (vai para o Git)
│   ├── config.user.toml   # pessoal (fica no .gitignore)
│   ├── version.toml       # versões do último setup
│   └── scripts/           # scripts usados pelas skills
└── docs/
```

Os scripts rodam com o [uv](https://docs.astral.sh/uv/) (ou Python 3.11+). Rode o `sdd setup` de novo depois de atualizar os plugins: ele só pergunta o que é novo e nunca altera uma resposta já gravada. Para saber o que está instalado, use `sdd status`. Para saber o próximo passo, pergunte "o que faço agora?".

### 3. Inicie um projeto

```
> iniciar projeto
```

O `discovery-init` cria `docs/{projeto}/project-config.json` e `docs/{projeto}/project.md` e registra o projeto em `docs/workspace.md`. Nas demais skills, cite o projeto ("visão do projeto-a") ou escolha na lista que a skill mostra.

Se o código do projeto estiver em vários repositórios (ex.: backend e frontend separados), cadastre-os:

```
> cadastrar os repositórios do projeto-a
```

A `multi-repo` cria `docs/{projeto}/repositorios.md`, que as skills usam para saber onde está cada parte do código.

### 4. Siga o fluxo

```
> definir visão do projeto
> mapear oportunidades
> levantar hipóteses
> identificar stakeholders
> definir métricas de sucesso
> gerar escopo
> especificação funcional
> documentar a arquitetura (C4)
> registrar decisão de arquitetura
> definir a direção de arte
> plano de execução
> criar entidade Pedido
> criar command ProcessarPedido
> criar endpoint POST /pedidos
> deploy homologação
```

---

## Skills Disponíveis

### Workspace

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `sdd-setup` | "sdd setup", "configurar o workspace", "sdd status", "o que faço agora", "por onde começo" | `_sdd/config.toml`, `_sdd/config.user.toml`, `_sdd/version.toml`, `_sdd/scripts/` |
| `multi-repo` | "vários repositórios", "cadastrar repositório", "status dos repositórios", "criar branch em todos", "feature em mais de um repositório" | `repositorios.md`, `plano-execucao/{escopo}/mudanca-multi-repo.md` |

### Fase: Discovery

| Skill | Gatilho | Frameworks | Saída |
|-------|---------|------------|-------|
| `discovery-init` | "iniciar projeto", "novo projeto" | — | `project.md` + linha em `docs/workspace.md` |
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

### Fase: Arquitetura (documentação)

Descreve a estrutura do sistema em níveis de abstração, seguindo *The C4 model for visualising software architecture* (Simon Brown). Diagramas em Mermaid C4, dentro do Markdown. Funciona para sistema novo (a partir do escopo e da especificação) e para sistema existente (lendo o código).

| Skill | Gatilho | Frameworks | Saída |
|-------|---------|------------|-------|
| `arch-c4` | "arquitetura", "modelo C4", "diagrama de contexto/contêineres/componentes/deployment" | C4 model, Mermaid C4 | `arquitetura/arquitetura.md` (+ `componentes/`, `dinamicos/`) |
| `arch-adr` | "ADR", "decisão de arquitetura", "por que escolhemos" | Architecture Decision Records (Nygard) | `arquitetura/decisoes/ADR-NNN-titulo.md` |

### Fase: Direção de Arte

Baseada nas obras de Richard Poulin (*Layout*, *Type*, *The Language of Graphic Design*): a arquitetura funcional vem antes de qualquer escolha estética.

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `direcao-arte-fundacao` | "direção de arte", "identidade visual", "style guide", "paleta de cores do projeto", "tipografia do projeto", "design system" | `direcao-arte/fundacao.md` |

### Fase: Arquitetura Angular

Skills para gerar a solução Angular por camada, com Signals, RxJS e NgRx.

| Skill | Gatilho | Camada | Saída |
|-------|---------|--------|-------|
| `angular-core-layer` | "camada core", "interceptor", "guard", "SignalR Angular", "error handler" | Core | Services, hubs, HTTP, interceptors, guards, resolvers, models |
| `angular-feature-layer` | "criar feature Angular", "smart/dumb component", "NgRx feature", "reactive form" | Feature | Páginas, componentes, store NgRx, formulários, rotas lazy |
| `angular-shared-layer` | "componente compartilhado", "pipe", "directive", "PrimeNG", "Angular Material" | Shared | Dumb components, pipes, directives, integração com biblioteca de UI |
| `angular-rxjs-transversal` | "RxJS", "switchMap", "combineLatest", "unsubscribe", "toSignal" | Todas | Guia de operadores e padrões RxJS por camada |

### Fase: Arquitetura Java

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `architecture-unit-test` | "teste unitário", "TDD Java", "JUnit", "gerar testes do BDD" | Testes JUnit 5 (Given-When-Then) a partir dos cenários BDD |

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

### Fase: Documentação de Negócio

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `business-docs` | "documentar regras de negócio", "gerar docs de negócio", "business docs", "documentar domínio" | `business/{area}.md` |

Todas as saídas de documentação ficam dentro de `docs/{projeto}/` (ver "Estrutura de pastas do workspace").

---

## Estrutura do Repositório

Este repositório é um **marketplace de plugins** do Claude Code. Cada plugin agrupa as skills de uma fase ou stack:

```
.claude-plugin/
└── marketplace.json              # catálogo dos plugins

plugins/
├── sdd/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       └── sdd-setup/
│           ├── SKILL.md
│           ├── modules/              # registro de cada plugin: versão, skills e perguntas do setup
│           ├── references/
│           │   ├── config-schema.md
│           │   └── proximos-passos.md
│           └── scripts/              # setup.py, config.py, sddlib.py (+ tests/)
│
├── workspace/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       └── multi-repo/
│           ├── SKILL.md
│           └── references/
│               ├── template-repositorios.md
│               ├── comandos-git.md
│               └── coordenacao-mudancas.md
│
├── discovery/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       ├── discovery-init/
│       ├── discovery-vision/
│       ├── discovery-opportunity/   # com references/
│       ├── discovery-assumptions/   # com references/
│       ├── discovery-stakeholders/  # com references/
│       ├── discovery-metrics/       # com references/
│       └── discovery-scoped/        # com references/
│
├── spec-plan/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       ├── spec-functional/
│       │   ├── SKILL.md
│       │   └── References/
│       │       ├── bdd-teoria.md
│       │       ├── cenarios-given-when-then.md
│       │       ├── extracao-de-exemplos.md
│       │       └── template-spec-functional.md
│       └── plan-execution/
│           ├── SKILL.md
│           └── references/
│               ├── plan-structure.md
│               ├── task-breakdown.md
│               ├── skill-mapping.md
│               └── examples.md
│
├── architecture-docs/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       ├── arch-c4/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── vocabulario-c4.md
│       │       ├── niveis-c4.md
│       │       ├── notacao.md
│       │       ├── mermaid-c4.md
│       │       ├── diagramas-complementares.md
│       │       ├── levantamento-codigo.md
│       │       ├── template-arquitetura.md
│       │       └── checklist.md
│       └── arch-adr/
│           ├── SKILL.md
│           └── references/
│               └── template-adr.md
│
├── architecture-dotnet/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       ├── architecture-init/
│       │   ├── SKILL.md
│       │   └── References/
│       │       ├── domain-layer.md
│       │       ├── application-layer.md
│       │       ├── infrastructure-layer.md
│       │       └── presentation-layer.md
│       ├── architecture-entities/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── entity-template.md
│       │       ├── value-objects.md
│       │       └── repository-interface.md
│       ├── architecture-feature/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── command-template.md
│       │       ├── query-template.md
│       │       └── behaviors.md
│       ├── architecture-repository/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── repository-base.md
│       │       ├── repository-implementation.md
│       │       └── unit-of-work.md
│       ├── architecture-external-service/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── http-client-base.md
│       │       ├── adapter-gateway.md
│       │       ├── resilience.md
│       │       └── authentication.md
│       ├── architecture-controller/
│       │   ├── SKILL.md
│       │   └── References/
│       │       ├── patterns.md
│       │       ├── structure.md
│       │       └── examples.md
│       ├── deploy-dotnet-homolog/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── pipeline-steps.md
│       │       ├── health-check.md
│       │       └── troubleshooting.md
│       └── deploy-dotnet-prod/
│           ├── SKILL.md
│           └── references/
│               ├── pre-deploy-checklist.md
│               ├── pipeline-steps.md
│               └── rollback.md
│
├── architecture-angular/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       ├── angular-core-layer/       # com assets/ e references/
│       ├── angular-feature-layer/    # com assets/ e references/
│       ├── angular-shared-layer/     # com assets/ e references/
│       └── angular-rxjs-transversal/ # com assets/ e references/
│
├── architecture-java/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       └── architecture-unit-test/   # com References/
│
├── business-docs/
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       └── business-docs/
│           ├── SKILL.md
│           └── references/
│               ├── areas.md
│               └── template-business-rule.md
│
└── art-direction/
    ├── .claude-plugin/plugin.json
    └── skills/
        └── direcao-arte-fundacao/
            ├── SKILL.md
            └── references/
                ├── guia-processo.md
                ├── template-mestre.md
                └── fontes.md
```

---

## Estrutura de pastas do workspace

A pasta de documentação reúne vários projetos. Após usar as skills:

```
_sdd/                                 # configuração do workspace (sdd-setup)
docs/
├── workspace.md                      # projetos: pasta, repositório, código local, situação
├── arquitetura/
│   └── landscape.md                  # visão de todos os sistemas (arch-c4, opcional)
├── projeto-a/
│   ├── project-config.json           # configuração lida pelas skills
│   ├── project.md
│   ├── repositorios.md               # só com código em vários repositórios (multi-repo)
│   ├── discovery/
│   │   ├── vision.md
│   │   ├── opportunity.md
│   │   ├── assumptions.md
│   │   ├── stakeholders.md
│   │   └── success-metrics.md
│   ├── escopo/
│   │   └── titulo-do-escopo/
│   │       ├── escopo.md
│   │       └── discovery/            # snapshot do discovery usado
│   ├── especificacao/
│   │   └── titulo-do-escopo/
│   │       └── spec-functional.md
│   ├── arquitetura/
│   │   ├── arquitetura.md            # contexto, contêineres, deployment, glossário
│   │   ├── componentes/{conteiner}.md
│   │   ├── dinamicos/{cenario}.md
│   │   └── decisoes/
│   │       ├── README.md             # índice dos ADRs
│   │       └── ADR-001-titulo.md
│   ├── direcao-arte/
│   │   └── fundacao.md               # identidade visual (direcao-arte-fundacao)
│   ├── plano-execucao/
│   │   └── titulo-do-escopo/
│   │       ├── execution-plan.md
│   │       └── mudanca-multi-repo.md # branches, contratos e ordem de merge/deploy (multi-repo)
│   └── business/
│       ├── areas.md                  # mapa de áreas do código
│       └── {area}.md
└── projeto-b/
    └── ...
```

Toda skill de documentação começa identificando o projeto: usa o que foi citado na conversa; senão lê `docs/workspace.md` (um projeto: usa esse; vários: pergunta). Em seguida lê a configuração do workspace em `_sdd/` (idioma, nível de detalhe, pasta de documentação).

E seu projeto .NET (no repositório de código) terá a estrutura Clean Architecture:

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

### sdd-setup

Hub do workspace, no papel do `bmad setup` do BMAD. No **setup**, faz só as perguntas ainda sem resposta (cada plugin declara as suas em `sdd-setup/modules/<plugin>.toml`) e grava em `_sdd/config.toml` (time) e `_sdd/config.user.toml` (pessoal), sem nunca alterar um valor existente. Também copia os scripts para `_sdd/scripts/` e registra as versões. O **status** mostra plugins e versões, perguntas pendentes, scripts desatualizados, proteção do `.gitignore` e os projetos. A **ajuda** lê o estado do projeto e recomenda a próxima skill. Não instala plugins nem faz commit.

### discovery-init

Ponto de entrada. Coleta nome, descrição, URL do repositório, caminho local do código e tipo do projeto. Gera `docs/{projeto}/project.md`, cria a estrutura de pastas e registra o projeto em `docs/workspace.md`.

### multi-repo

Para projetos com o código em vários repositórios. Cadastra os repositórios em `docs/{projeto}/repositorios.md` (URL, caminho local, papel, stack, contêineres C4 que implementa, contratos entre eles e deploy), detectando o que dá pelo Git. Mostra o panorama de todos (branch, alterações, atrás/à frente), clona os que faltam e coordena entregas que atravessam repositórios: repositórios afetados, contratos compatíveis ou não (expandir e contrair, versão nova, feature flag), ordem provedor antes do consumidor, mesma branch em todos. Nada que altere um repositório é feito sem confirmação, e commit, push e merge só a pedido.

### discovery-vision / opportunity / assumptions / stakeholders / metrics

Cada skill conduz uma conversa em blocos temáticos e gera um documento `.md` estruturado. Requerem que `project.md` exista. Podem ser usadas em qualquer ordem — use só as que fazem sentido para o seu contexto.

### discovery-scoped

Lê todos os arquivos de `discovery/`, verifica escopos já existentes (evita repetição com escopos `Aprovado` ou `Em execução`) e gera `escopo.md` com estado inicial `Rascunho`. Suporta escopos parciais (módulo, feature, fase).

### spec-functional

Baseada em **BDD** e **Feature Injection**. Para cada funcionalidade do escopo, define narrativa (`In order to / As / I want`) e levanta cenários `Given / When / Then`. Usa Esquema do Cenário para múltiplas combinações de dados. Requer que `escopo.md` exista.

### arch-c4

Baseada no **modelo C4** de Simon Brown. Conduz em blocos: vocabulário, contexto (obrigatório), contêineres (obrigatório), componentes (opcional, por contêiner, com mapeamento para o código), deployment por ambiente e complementares (dinâmico, landscape). Tem três modos: **Design** (sistema novo, a partir de discovery/escopo/spec), **Levantamento** (sistema existente, lendo `docker-compose`, `csproj`, `angular.json`, configs) e **Atualização** (altera só o que mudou). Cada diagrama tem título com o tipo e tabela de legenda (o Mermaid C4 não desenha legenda) e passa por um checklist antes de salvar.

### arch-adr

Registra uma decisão de arquitetura por arquivo (contexto, opções, decisão, consequências), numerada (`ADR-001`), com índice em `decisoes/README.md`. Decisão aceita não é editada: é substituída por outro ADR. Resolve os pontos em aberto do `arquitetura.md`.

### direcao-arte-fundacao

Conduz a fundação da identidade visual em blocos, cada um confirmado antes do próximo: fundamentos do projeto, auditoria e arquitetura visual, conceito e direção de arte, sistema visual (cores, tipografia, grid, iconografia) e fechamento com validação. Gera `direcao-arte/fundacao.md`, que serve de base para as telas e para as skills Angular. Se o documento já existe, continua de onde parou ou revisa, sem repetir perguntas já respondidas.

### business-docs

Lê o código implementado (.NET e Angular) e documenta as regras de negócio por área em `business/{area}.md`, numeradas (`RN-001`) e com arquivo e linha de cada regra. O mapa de áreas do código fica em `business/areas.md`. Com vários repositórios, prioriza os de backend.

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

### angular-core-layer / feature-layer / shared-layer / rxjs-transversal

Geram a solução Angular por camada: Core (serviços, HTTP, SignalR, interceptors, guards, tratamento de erro), Feature (páginas, smart e dumb components, store NgRx, formulários reativos, rotas lazy) e Shared (componentes reutilizáveis, pipes, directives, biblioteca de UI). A `angular-rxjs-transversal` complementa as três com os operadores e padrões RxJS de cada camada.

### architecture-unit-test

Gera testes unitários Java (JUnit 5) a partir dos cenários BDD da especificação, mantendo a estrutura Given-When-Then e os padrões de cada camada.

### plan-execution

Analisa a especificação funcional (e a arquitetura C4, se existir) e decompõe em entregas incrementais com tarefas ordenadas por camada (Domain → Infrastructure → Application → Presentation). Usa os contêineres e tecnologias do C4 para escolher a skill correta para cada tarefa e respeita os ADRs aceitos. Inclui estimativas de esforço.

### deploy-dotnet-homolog

Executa pipeline sequencial: Restore → Build → Test → Docker Build → Deploy → Health Check. Interrompe imediatamente em caso de falha. Gera relatório com artefatos e status de cada etapa.

### deploy-dotnet-prod

Igual ao homolog, com etapas extras: confirmação explícita do usuário, validação prévia (branch, commits pendentes, variáveis de ambiente) e procedimento de rollback documentado no relatório.

---

## Para quem é isso?

- **Product Managers** — para conduzir discovery estruturado e gerar escopos
- **Tech Leads** — para garantir alinhamento antes de codar e definir arquitetura
- **Designers e diretores de arte** — para definir e documentar a identidade visual do produto
- **Desenvolvedores .NET, Angular e Java** — para gerar código e testes seguindo os padrões do time
- **Analistas de Sistemas** — para especificação funcional com BDD

---

## Fluxo Completo

```
sdd-setup (uma vez por workspace)
     │
     ▼
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
                arch-c4 ◄──► arch-adr
                          │
                          ▼
              direcao-arte-fundacao (opcional)
                          │
                          ▼
                  plan-execution ──► multi-repo (vários repositórios)
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
As de código (`architecture-*`, `angular-*`) podem ser usadas sem ter feito discovery — basta saber o que construir. A `arch-c4` também: num sistema existente, ela levanta a arquitetura a partir do código.

**Vários projetos**
Cite o projeto no pedido ("gerar escopo do projeto-b") para pular a pergunta de qual projeto usar.

**Vários repositórios**
Do workspace, dê acesso ao código com `/add-dir {caminho}` (ou `claude --add-dir`). Para gerar muito código num repositório, abra o Claude Code dentro dele: o `CLAUDE.md` daquele repositório passa a valer.

---

## Roadmap

| Fase | Status | Skills |
|------|--------|--------|
| Discovery | Implementado (v2) | 6 skills |
| Escopo | Implementado (v2) | 1 skill |
| Especificação Funcional | Implementado | `spec-functional` |
| Arquitetura (documentação C4 + ADR) | Implementado | `arch-c4`, `arch-adr` |
| Workspace com vários projetos | Implementado | todas as skills de documentação |
| Vários repositórios por projeto | Implementado | `multi-repo` |
| Direção de Arte (fundação) | Implementado | `direcao-arte-fundacao` |
| Direção de Arte (validação) | Planejado | `direcao-arte-validacao` |
| Arquitetura .NET | Implementado | 6 skills |
| Arquitetura Angular | Implementado | 4 skills |
| Testes Java | Implementado | `architecture-unit-test` |
| Plano de Execução | Implementado | `plan-execution` |
| Deploy .NET | Implementado | `deploy-dotnet-homolog`, `deploy-dotnet-prod` |
| Documentação de Negócio | Implementado | `business-docs` |
| Especificação Não-Funcional | Planejado | `spec-nonfunctional` |
| Refinamento | Planejado | `refinement-screens`, `refinement-api`, `refinement-data-model` |

---

## Estrutura de uma skill

```
plugins/<plugin>/skills/nome-da-skill/
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
