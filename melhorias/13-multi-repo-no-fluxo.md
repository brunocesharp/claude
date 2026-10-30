# 13 — Vários repositórios por projeto no novo fluxo

- **Pedido:** "Manter a possibilidade de varios repositorios para um projeto" (linha 13)
- **Tamanho:** M
- **Depende de:** atravessa 03 e 06–12 — usar como checklist em cada uma
- **Situação:** [ ] a fazer

## Contexto

### Como o BMAD faz
- v7: para vários repositórios, o setup é feito na **raiz do workspace**; épicos independentes podem rodar em paralelo com fronteiras explícitas e dono por stream. Não há um cadastro de repositórios como o nosso.

### Como está hoje (já resolvido e a preservar)
- `multi-repo` mantém `docs/{projeto}/repositorios.md` (papel, caminho, contêineres C4, contratos, deploy), panorama do Git, clone, **mudança coordenada** (mesma branch, provedor antes do consumidor, compatibilidade de contratos, `mudanca-multi-repo.md`) e "onde fica".
- `plan-execution` acrescenta a coluna Repositório e ordena provedor → consumidor quando há vários repositórios.
- Regra: só leitura por padrão; clone/branch com confirmação; commit/push/merge só a pedido.

## Objetivo

Garantir que o fluxo épico → story → implementação → revisão funcione com o código espalhado em vários repositórios, sem duplicar o que o `multi-repo` já faz.

## Proposta (checklist por tarefa)

- **03 estado/scripts**: `_sdd/` fica na raiz do workspace de documentação (nunca nos repositórios de código); `workspace.py` lê `repositorios.md`; caminhos locais variam por máquina (aceitar override em `config.user.toml`).
- **06 sprint-status**: campo `repositories` por story; `sdd status` mostra o panorama do `multi-repo` para a story em andamento.
- **07 épicos/stories**: cada story declara os repositórios que toca; a ordem de build respeita provedor → consumidor; contrato incompatível vira story própria com estratégia (expandir/contrair, versão, flag) ou ponto em aberto para `arch-adr`. Preferir stories que tocam **um** repositório quando o fatiamento vertical permitir; quando tocar vários, é uma "story coordenada".
- **08 story file**: seção "Repositórios" com caminho, branch e o que muda em cada um; contratos que mudam, com compatibilidade.
- **09 dev-story**: abre a sessão no repositório principal da story com `--add-dir` dos demais (ou no workspace com `--add-dir` de todos); implementa provedor antes do consumidor; "Arquivos alterados" agrupado por repositório; branch criada pelo `multi-repo` (Mudança coordenada) — o `mudanca-multi-repo.md` passa a poder ser **por story** ou **por épico**.
- **10 revisão**: diff por repositório; lente de contratos (provedor e consumidor compatíveis, ordem de merge registrada).
- **11 retrospectiva**: `git log` de todos os repositórios do épico; ordem de merge/deploy cumprida?
- **12 correct-course**: impacto em contratos e em repositórios já mergeados.

## Decisões em aberto

- Branch por story (`feat/1-2-slug`) ou por épico (`feat/epic-1-slug`) — por repositório. Recomendação: por story, com o mesmo nome em todos os repositórios tocados. recomendado
- `mudanca-multi-repo.md` por story ou por épico. por story
- Atualizar o `multi-repo` (Operação 4) para aceitar uma story como entrada, além de escopo e item do plano. Sim

## Critérios de aceite

- [ ] `multi-repo` aceita story/épico como entrada da Mudança coordenada.
- [ ] Cada skill nova (06–12) tem uma seção "Vários repositórios" coerente com este checklist.
- [ ] Teste de ponta a ponta num projeto de exemplo com `api` + `web`: story que muda um endpoint e a tela que o consome — ordem, branches, revisão de contrato e retrospectiva corretas.

## Arquivos impactados

`plugins/workspace/skills/multi-repo/SKILL.md` e `references/coordenacao-mudancas.md`, `references/template-repositorios.md`; todas as skills novas das tarefas 06–12.
