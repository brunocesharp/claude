# Análise — melhorias do sdd-full inspiradas no BMAD

Origem: `melhorias.md` (raiz do repositório). Data da análise: 30/10/2026.

## 1. O que o pedido mistura (ler antes de executar)

O `melhorias.md` cita conceitos de **duas versões diferentes do BMAD**:

| Tema | Versão do BMAD | Como está na documentação atual |
|------|----------------|---------------------------------|
| Instalação, `bmad setup`, `_bmad/`, `_bmad/scripts/`, `_bmad/custom/*.toml` | **v7** (preview alpha) | `npx skills add bmad-code-org/BMAD-METHOD`, hub `bmad` com `setup`/`status`, scripts Python com `uv run` |
| `sprint-status.yaml` com `backlog → ready-for-dev → in-progress → review → done` | **v6** (estável, 6.12) | Na v7 foi substituído por `tickets.toml` + plano por story com `built`/`done`/`dropped` |
| Story file com contexto completo, sessão nova por story (`create-story` / `dev-story`) | **v6** | Na v7 o story file é opcional e o build gera um `story-<slug>-plan.md` |
| Revisão adversarial, `correct-course`, retrospectiva | **v6** (as três) / v7 (retrospectiva e code review com triagem patch/defer/decision) | v7 não tem `correct-course`; o replanejamento é pedido à PO (Sofia) |

**Recomendação:** usar a v7 como modelo para **instalação, setup, estado/scripts e customização** (infraestrutura), e a v6 como modelo para o **fluxo de entrega** (sprint-status, story file, dev-story, revisão adversarial, correct-course), que é exatamente o que o pedido descreve. Da v7, aproveitar duas ideias boas no fluxo de entrega: a **triagem patch/defer/decision** na revisão e o **veredito** (`accepted` / `accepted-with-open-items` / `rejected`) na retrospectiva.

## 2. Situação atual do repositório (o que já existe)

- Marketplace de plugins (`.claude-plugin/marketplace.json`) com 9 plugins; instalação por `/plugin marketplace add` + `/plugin install`.
- Configuração **por projeto** em `docs/{projeto}/project-config.json` (criado pelo `discovery-init`). Não existe configuração **do workspace** (idioma, nome do usuário, nível, pastas de saída).
- Nenhum script: todo estado é lido e escrito pelo modelo, editando Markdown.
- Nenhum mecanismo de customização: para mudar uma skill é preciso editar o `SKILL.md` (perde-se na atualização do plugin).
- Discovery não tem pesquisa (mercado, concorrentes, domínio). `discovery-opportunity` e `discovery-assumptions` falam de dores e hipóteses, sem fontes externas.
- `plan-execution` gera **um único** `execution-plan.md` por escopo, organizado em *Entregas* com tabelas de tarefas por camada. Não há épicos, stories nem arquivo por tarefa.
- **Situação** só existe em três lugares, todos de granularidade grossa: checkbox de fase no `project.md`, coluna Situação no `workspace.md` e campo Status (Rascunho/Aprovado/Em Execução/Concluído) no `execution-plan.md`.
- Não há skills de implementação orientada por story, revisão, retrospectiva ou mudança de rumo. As skills de código (`architecture-*`, `angular-*`) são geradores independentes.
- `multi-repo` já resolve cadastro, panorama, mudança coordenada e "onde fica"; `plan-execution` já acrescenta a coluna Repositório quando há vários.

## 3. Tarefas identificadas

| # | Arquivo | Tarefa | Linha do pedido | Tamanho |
|---|---------|--------|-----------------|---------|
| 01 | [01-instalacao-hub-sdd.md](01-instalacao-hub-sdd.md) | Hub `sdd` + instalação no estilo v7 | 3 | M |
| 02 | [02-configuracao-setup.md](02-configuracao-setup.md) | Perguntas do setup e config do workspace | 4 | M |
| 03 | [03-estado-e-scripts.md](03-estado-e-scripts.md) | Pasta `_sdd/` e scripts de estado | 5 | G |
| 04 | [04-customizacao.md](04-customizacao.md) | Overrides por skill (equipe e pessoal) | 6 | G |
| 05 | [05-pesquisa-mercado-concorrentes.md](05-pesquisa-mercado-concorrentes.md) | Skill de pesquisa de mercado e concorrentes | 7 | M |
| 06 | [06-sprint-status.md](06-sprint-status.md) | `sprint-status.yaml` e máquina de estados | 11 | M |
| 07 | [07-epicos-e-stories.md](07-epicos-e-stories.md) | Plano em épicos fatiados em stories | 8 | G |
| 08 | [08-story-com-contexto-completo.md](08-story-com-contexto-completo.md) | Um arquivo por story com contexto completo | 8, 12 | G |
| 09 | [09-implementacao-sessao-por-story.md](09-implementacao-sessao-por-story.md) | `dev-story`: sessão nova, spec como única fonte | 9 | G |
| 10 | [10-revisao-adversarial.md](10-revisao-adversarial.md) | Revisão adversarial da story | 10 | M |
| 11 | [11-retrospectiva.md](11-retrospectiva.md) | Retrospectiva de épico | 10 | M |
| 12 | [12-correct-course.md](12-correct-course.md) | Mudança de rumo no meio do sprint | 10 | M |
| 13 | [13-multi-repo-no-fluxo.md](13-multi-repo-no-fluxo.md) | Vários repositórios no fluxo de stories | 13 | M |

Tamanho: P = até meio dia, M = 1 a 2 dias, G = 3 dias ou mais (escrita de skill + referências + teste num workspace real).

## 4. Dependências e ordem sugerida

```
02 configuração ──┐
                  ├──> 03 estado/scripts ──> 06 sprint-status ──> 07 épicos/stories ──> 08 story file ──> 09 dev-story ──> 10 revisão
01 hub sdd ───────┘            │                                                                                    │
                               └──> 04 customização                                          11 retrospectiva <─────┤
                                                                                              12 correct-course <────┘
05 pesquisa (independente)            13 multi-repo: atravessa 06–12 (aplicar junto ou logo depois de cada uma)
```

Ordem de execução recomendada:

1. **02 → 01 → 03**: a fundação (onde a configuração mora, quem faz o setup, onde ficam os scripts). O 01 e o 02 andam juntos: o setup do hub faz as perguntas do 02.
2. **06**: o modelo de estados, que todas as skills do fluxo de entrega leem e escrevem.
3. **07 → 08 → 09 → 10**: o caminho feliz de uma story, do plano ao `done`.
4. **11, 12**: fechamento e desvio.
5. **13**: revisar 06–12 para vários repositórios (ou incluir em cada uma, usando o 13 como checklist).
6. **04 e 05** podem entrar em qualquer momento depois do 03 (04) ou já (05). O 04 fica melhor quando já houver skills novas para customizar.

Um MVP útil do fluxo de entrega é **06 + 07 + 08 + 09** com estado editado pelo modelo; scripts (03) e customização (04) podem vir depois sem mudar os formatos de arquivo, desde que os formatos sejam fechados no 06.

## 5. Decisões que valem para todas as tarefas

Propostas para confirmar antes de começar (cada arquivo repete as que lhe dizem respeito):

1. **Nome do plugin novo**: `sdd` (hub + scripts + revisão + retrospectiva + correct-course) ou distribuir nos plugins atuais (`workspace`, `spec-plan`). Recomendação: plugin `sdd` para a infraestrutura (hub, setup, scripts, customização) e plugin novo `delivery` para o ciclo da story (sprint-planning, create-story, dev-story, code-review, retrospective, correct-course). `spec-plan` fica com `spec-functional` e o planejamento de épicos.
2. **Onde ficam os artefatos de entrega**: `docs/{projeto}/implementacao/` (sprint-status, épicos, stories, revisões, retrospectivas, propostas de mudança). Mantém o padrão "tudo do projeto em `docs/{projeto}/`".
3. **Linguagem dos scripts**: Python executado com `uv run` (igual ao BMAD), com dependências declaradas inline no script (PEP 723). Toda skill precisa funcionar também **sem** `uv`, com o modelo lendo e editando os arquivos (degradação explícita).
4. **Formatos**: TOML para configuração e customização (igual à v7, lido com `tomllib`); YAML para o `sprint-status.yaml` (pedido explícito); Markdown com frontmatter YAML para épicos e stories.
5. **`plan-execution` atual**: não apagar. Vira o modo "plano por entregas" (equipes que trabalham com tarefas por camada e Redmine) e o novo planejamento por épicos/stories vira o caminho padrão. Decidir no 07.
6. **Regra de sempre**: nenhuma skill faz commit, push ou merge sem pedido explícito; nada é sobrescrito sem confirmação; toda skill de documentação começa com o Passo 0; README e `0.0 - contexto-projeto-skills.md` atualizados a cada skill nova.
