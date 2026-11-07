---
name: execucao-recorrente
description: Agente de entrega sem supervisão — busca sempre a próxima tarefa possível nos repositórios listados num arquivo de configuração (prioritários e sem prioridade) e a executa num contexto limpo, uma por vez — retoma o que ele mesmo deixou pela metade (inclusive stories que a story-review devolveu com correções), desbloqueia stories que ele bloqueou por causa de ambiente ou técnica quando a causa mudou, revisa as stories em review, implementa as ready-for-dev e, sem nada disso, cria a próxima story do backlog. Cada story trabalha numa worktree própria, para um repositório nunca esperar commit de outra story. Roda uma rodada (agendada a cada poucos minutos) ou em modo contínuo, esvaziando a fila e agendando o próprio próximo despertar (/loop sem intervalo). O que precisa de uma pessoa vira motivo registrado e entra na lista de atenção. Use quando o usuário disser "execucao-recorrente", "execução recorrente", "agente de entrega", "executar as stories automaticamente", "rodar as tarefas pendentes dos projetos", "agendar a execução das stories", "processar a fila de stories", "deixar rodando em loop", "adicionar repositório na execução recorrente". NÃO use para implementar uma story específica acompanhando (use dev-story), preparar uma story acompanhando (use create-story), só criar stories sem supervisão (use criacao-story-recorrente), revisar acompanhando (use story-review), ver ou mudar o quadro (use sprint-planning) ou mudar requisito (use correct-course).
metadata:
  version: 1.1.0
  category: implementation
  depends-on: dev-story
  output: código nos repositórios das stories, em worktrees {repositório}.worktrees/{id} (via dev-story); arquivos das stories (via create-story, dev-story e story-review); {workspace}/_sdd/execucao-recorrente/ e _sdd/criacao-story-recorrente/ (estado.json, log/AAAA-MM.md); trava global ao lado do arquivo de configuração
---

# Execução Recorrente — agente de entrega

Mantém o fluxo de stories andando **sem ninguém olhando**, **uma tarefa por vez**, buscando sempre a **próxima tarefa possível** para não ficar parado: retomar, desbloquear, revisar, implementar ou criar. Cada tarefa é feita do começo ao fim num contexto limpo. Duas formas de rodar:

- **Rodada única** (padrão): faz uma tarefa e termina. Pensada para uma tarefa agendada a cada poucos minutos (`references/agendamento.md`); enquanto uma tarefa está em andamento, as rodadas seguintes veem a trava e terminam sem iniciar nada.
- **Modo contínuo** (`--continuo`): faz uma tarefa atrás da outra até a fila esvaziar ou chegar a `max_tarefas_por_rodada`, e agenda o próprio próximo despertar. Para `/loop` sem intervalo ou para o agente `agente-entrega` (seção "Modo contínuo").

**Só trabalha com o quadro de stories**: entram apenas os projetos com `docs/{projeto}/implementacao/sprint-status.yaml` (fluxo `plan-epics` → `sprint-planning` → `create-story`). Projeto sem quadro, inclusive o que só tem `plan-execution`, fica fora da fila com uma nota no `scan`; para incluí-lo, gere o quadro.

Ela não implementa nada por conta própria: escolhe a tarefa, prepara o terreno e a entrega ao `create-story`, ao `dev-story` ou à `story-review` num contexto limpo, com as regras do modo não supervisionado. O que não puder ser feito sem uma pessoa vira **motivo registrado**, nunca suposição.

Leia antes de executar: `sdd-setup/references/sprint-status.md` (plugin `sdd`; estados e transições) e a SKILL.md da skill da tarefa escolhida (`create-story`, `dev-story` ou `story-review`).

A criação de stories faz parte da fila desta skill (ação `create-story`). A `criacao-story-recorrente` continua existindo para quem quer **só** criar; não agende as duas com arquivos de configuração diferentes (veja "Criação de stories").

---

## Arquivo de configuração

Os repositórios verificados ficam num arquivo TOML, fora do plugin (atualizar o plugin nunca o toca):

1. `--config {arquivo}` no pedido (`/execucao-recorrente --config D:\repos\execucao-recorrente.toml`);
2. senão, a variável de ambiente `EXECUCAO_RECORRENTE_CONFIG`;
3. senão, `~/.claude/execucao-recorrente.toml` (no Windows, `C:\Users\{usuário}\.claude\execucao-recorrente.toml`).

```toml
[repositorios]
prioritarios = [
  'D:\repos\docs-loja',
  'D:\repos\docs-financeiro\docs\pagamentos',
]
sem_prioridade = [
  'D:\repos\docs-estoque',
]

[execucao]
lock_expira_min = 90          # validade da trava; a rodada a renova entre os passos
max_tarefas_por_rodada = 5    # modo contínuo: tarefas seguidas antes de parar e agendar a próxima
```

Cada caminho pode ser:

| Caminho | O que a skill verifica |
|---------|------------------------|
| Raiz de um workspace (tem `_sdd/` ou `docs/`) | Todos os projetos com `docs/{projeto}/implementacao/sprint-status.yaml` (`paths.docs_root` do `_sdd/config.toml`, se houver) |
| Pasta de um projeto (`docs/{projeto}`) | Só esse projeto, se tiver `sprint-status.yaml` |
| Pasta qualquer dentro de um workspace | O workspace que a contém |

Regras do arquivo: caminhos entre **aspas simples** (no Windows, a barra invertida não precisa ser dobrada); a ordem dentro de cada lista é a ordem de verificação; um caminho nas duas listas vale como prioritário (o script avisa); caminho inexistente vai para `erros` e não impede os demais. Para incluir ou tirar um repositório, edite o arquivo — a próxima rodada já usa a lista nova.

**Sem o arquivo** (`scan` devolve erro): numa conversa com o usuário, crie o modelo com `init-config`, mostre o caminho e pergunte quais repositórios entram em cada lista; grave com a ferramenta Edit. Em execução agendada (ninguém para responder), termine com `sem arquivo de configuração: {caminho}` — nunca adivinhe repositórios.

**Pedidos para mudar a lista** ("adicione D:\repos\docs-rh como prioritário", "tire o estoque") — edite só o arquivo de configuração, rode `config` para validar e mostre as duas listas como ficaram.

## Passo 0 — Ler a configuração e montar a fila

```
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" scan [--config {arquivo}]
```

O resultado traz `em_andamento` (trava global ativa), `escolhida`, `motivo`, a `fila` completa em ordem, a lista de `atencao` (o que precisa de uma pessoa), `espera_sugerida_s` (modo contínuo), os `grupos` (prioritário e sem prioridade) com cada repositório, projeto e as stories `puladas` com o motivo, mais `erros` e `avisos`.

**Ordem da fila — a próxima tarefa possível:**

1. **Tarefa em andamento** (`em_andamento: true`) → não inicia nada. Responda `tarefa em andamento: {motivo}` e termine.
2. **Retomar**, de qualquer grupo, antes de tudo:
   - story `in-progress` que a própria automação começou e não terminou (a rodada anterior morreu, estourou o contexto ou falhou por erro técnico);
   - story `in-progress` que a `story-review` **devolveu com correções** (`correcoes_revisao: true`) — pelo registro da revisão automática ou pela última linha do Histórico (`review → in-progress`, `story-review`);
   - criação de story (`create-story`) que ficou pela metade.
3. **Repositórios prioritários**, na ordem da lista; em cada grupo:
   1. **desbloquear** (`acao: desbloquear`): story que a automação bloqueou por causa de **ambiente** ou **técnica** e cuja causa mudou (seção "Stories bloqueadas") — é rápido e devolve a story à fila;
   2. **revisar** (`story-review`) as stories em `review` — fecha trabalho e libera quem depende delas;
   3. **implementar** (`dev-story`) as `ready-for-dev`, na ordem de build;
   4. **criar** (`create-story`) a próxima story do `backlog`, se o projeto tiver menos de `max_prontas` stories prontas.
4. **Só se nenhum prioritário tiver tarefa**, os repositórios **sem prioridade**, na mesma regra.

Ficam **fora** da fila, com o motivo em `puladas` (e em `atencao` quando precisa de uma pessoa):
- `in-progress` que a automação não começou nem foi devolvido pela revisão (alguém pode estar nele);
- story com `checkpoint: true` (precisa de acompanhamento humano) — atenção;
- `depends_on` com story que ainda não está em `review` ou `done`;
- story que já falhou `max_tentativas` vezes na mesma ação;
- `blocked` por decisão, por uma pessoa, ou cuja causa não mudou — atenção;
- criação aguardando confirmação (`exige_confirmacao = true`) — atenção;
- ação fora de `acoes` no projeto; projeto com `habilitado = false`.

`escolhida` nula: não registre nada, responda o `motivo` e a lista de atenção, e termine (no modo contínuo, agende o próximo despertar).

## Customização (por projeto)

Para o projeto da story escolhida, resolva a customização desta skill a partir da raiz do workspace dele:

```
uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto}
```

Sem o script (ou sem `uv`/`python`): leia `${CLAUDE_SKILL_DIR}/customize.toml` e, se existir, `docs/{projeto}/_custom/execucao-recorrente.toml`, e mescle pelas regras de `sdd-setup/references/customizacao.md`. Sem override, valem os padrões da skill.

1. Execute os `workflow.activation_steps_prepend`, na ordem.
2. Leia os arquivos de `facts` (e os textos literais): são fatos válidos durante toda a skill e vencem os padrões dela quando conflitarem.
3. Use os valores de `resolved.workflow` onde esta skill os cita: `habilitado` e `acoes` (filtram a fila no `scan`), `max_tentativas` (Passo 4), `commit_ao_concluir` (Passo 3) e `isolamento` (Passo 2). O `recorrente.py` já lê esses campos do override do projeto. Para `create-story`, valem os campos de `_custom/criacao-story-recorrente.toml` (`max_prontas`, `dependencias_em`, `exige_confirmacao`, `max_tentativas`), que o script também lê.
4. Ao terminar, execute os `workflow.activation_steps_append` e o `workflow.on_complete`.

Mostre os `warnings` uma vez no resumo final.

## Scripts

```
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" init-config [--config {arquivo}]   # cria o modelo; nunca sobrescreve
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" config      [--config {arquivo}]   # valida e mostra as listas
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" scan        [--config {arquivo}]
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" lock adquirir|renovar|liberar [--config {arquivo}] [--dono "{texto}"]
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" worktree {repositório} --id {id} [--base {branch}]
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" registrar {workspace} --projeto {projeto} --id {id} --acao {acao} \
    --resultado iniciada|concluida|falhou|bloqueada|pulada|aguardando|desbloqueada [--motivo "{motivo}"] \
    [--causa ambiente|tecnica|decisao] [--verificar caminho:{pasta}|comando:{executável}] [--repo {repositório}]
```

E, a partir da raiz de cada workspace, os scripts do fluxo: `_sdd/scripts/status.py`, `_sdd/scripts/story.py` e `_sdd/scripts/epics.py` (`sprint-status.md`).

Sem `uv`: `python` 3.11+ com `pyyaml`. Sem nenhum dos dois, **não rode sem supervisão**: sem a trava e o estado, duas rodadas podem pegar tarefas ao mesmo tempo. Responda `sem python 3.11+: execução recorrente desativada` e termine.

Onde o script grava:

| Arquivo | Conteúdo |
|---------|----------|
| `{config}.lock.json`, ao lado do arquivo de configuração (ex.: `~/.claude/execucao-recorrente.lock.json`) | Trava global: `ativo` com início, validade e dono, ou `livre`. Nunca é apagado, só regravado |
| `{workspace}/_sdd/execucao-recorrente/estado.json` | Por story (`dev-story`, `story-review`): ação, tentativas, último resultado e motivo, o `bloqueio` (causa, verificações, assinatura, estado de volta), histórico das últimas 20 execuções e o motivo atual de `pulada` |
| `{workspace}/_sdd/criacao-story-recorrente/estado.json` | O mesmo para `create-story` — compartilhado com a `criacao-story-recorrente` |
| `{workspace}/_sdd/{skill}/log/AAAA-MM.md` | Uma linha por execução: data, projeto, story, ação, resultado, tentativa e motivo. `pulada` só quando o motivo muda |
| `{repositório}.worktrees/{id}/`, ao lado de cada repositório de código | A worktree da branch `feat/{id}` (só com `isolamento = "worktree"`) |

---

## Passo 1 — Travar

1. `lock adquirir [--config {arquivo}] --dono "{origem da rodada e hora}"`.
   - `adquirido: false`: outra rodada começou uma tarefa entre o `scan` e a trava. Termine com `tarefa em andamento`.
   - `assumiu_expirado: true`: a rodada anterior morreu sem liberar. Se ela deixou uma story `in-progress`, a fila já a traz como retomada.
2. A validade (`execucao.lock_expira_min`, padrão 90 min) precisa ser maior que o trecho mais longo sem renovar. Rode `lock renovar` antes de chamar o subagente e logo depois que ele terminar; `renovado: false` quer dizer que a trava expirou e outra rodada pode ter assumido — registre o que já aconteceu, não comece nada novo e vá para o Passo 5.
3. **Daqui em diante, toda saída passa pelo Passo 5** (liberar a trava), inclusive em erro.

## Passo 2 — Pré-condições, sem perguntar

**Desbloquear** (`acao: desbloquear`) não tem pré-condição de código — vá direto para o Passo 3.

Para as outras ações, faça as conferências do Passo 2 da skill da tarefa, trocando cada pergunta por uma decisão registrada:

| Situação | O que fazer | Resultado |
|----------|-------------|-----------|
| `dev-story`/`story-review`: `story.py check {id}` com `problems` | Não começa | `falhou` — "story incompleta: {problems}" |
| Repositório de código da story não existe no caminho local | Não começa | `bloqueada`, causa **ambiente**, `--verificar caminho:{caminho}` — "repositório {r} não encontrado em {caminho}" |
| Ferramenta de build/teste da stack ausente (`dotnet`, `npx`, `mvn`) | Não começa | `bloqueada`, causa **ambiente**, `--verificar comando:{executável}` |
| `create-story`: story não está mais em `backlog`; workspace sem `_sdd/scripts/`; épico sem arquivo | Como no Passo 2 da `criacao-story-recorrente` | `pulada` / `falhou` / `bloqueada` (decisão) |
| `status.py` recusa a transição | Não força | `falhou` — mensagem do script |

**Pasta de trabalho** (`dev-story` e `story-review`), em cada repositório de código da story, na ordem da seção Repositórios:

- `isolamento = "worktree"` (padrão): `worktree {repositório} --id {id}`. Ele devolve `caminho` — a worktree da branch `feat/{id}` em `{repositório}.worktrees/{id}`, criada a partir da branch principal se não existir — ou, se a branch já está no checkout principal (story começada antes), o próprio checkout (`modo: checkout`). O checkout principal **não é tocado**: alterações pendentes de outra story nele não impedem nada. Erro do script → `falhou` com a mensagem.
- `isolamento = "checkout"`: o comportamento antigo — `git status --porcelain` e `git branch --show-current` no repositório; alterações de **outra** story ou branch diferente com trabalho em aberto → `pulada` "aguardando commit/limpeza em {r} ({branch atual})" (não conta tentativa); branch `feat/{id}` inexistente → crie a partir da branch principal (o modo não supervisionado vale como `auto_mode = sim` só para isso).

`falhou`, `bloqueada` ou `pulada` **antes de começar** a tarefa: registre (`registrar …`; `bloqueada` com o Histórico do Passo 4) e passe para a próxima da `fila`, mantendo a ordem. `pulada` não conta tentativa e só entra no log quando o motivo muda (o `registrar` devolve `repetida: true` e não grava nada se o motivo é o mesmo da rodada anterior); mantenha o texto do motivo estável entre rodadas — sem horário nem contagem. Assim um repositório travado não impede o trabalho nos outros. Sem próxima, vá para o Passo 5.

Começando de verdade: `registrar … --resultado iniciada` **antes** de chamar o subagente — é isso que permite retomar a tarefa se esta rodada morrer.

## Passo 3 — Executar em contexto limpo

### Desbloquear

Sem subagente. A story está em `blocked` e o `scan` já confirmou que a causa mudou (`condicao`):

1. `status.py set {id} {voltar_para}` (nunca `--force`). Se recusar, `pulada` com a mensagem e siga.
2. Se a story tem arquivo, linha no Histórico: `| {data} | blocked → {voltar_para} | execucao-recorrente | desbloqueio automático: {condicao} |`.
3. `registrar … --acao {acao_origem} --resultado desbloqueada --motivo "{condicao}"` — causa ambiente recomeça as tentativas; causa técnica ganha **uma** tentativa a mais.
4. Siga para a próxima tarefa: no modo contínuo, a próxima iteração já encontra a story na fila; na rodada única, termine (Passo 5).

### Criar, implementar ou revisar

Rode a ação num **subagente** (ferramenta Agent), para a story ser a primeira coisa do contexto, como as skills exigem. Sem ferramenta de subagente, execute aqui mesmo só na rodada única (cada rodada agendada já é uma sessão nova); no modo contínuo, sem subagente, faça uma tarefa e termine. Nunca abra janela de terminal (`session.py`): não há ninguém para usá-la.

**`create-story`**: use o prompt do Passo 3 da `criacao-story-recorrente` (mesmas regras: só leitura nos repositórios de código, `exige_confirmacao`, linhas de resultado) e, no Passo 4, a tabela de resultados dela — com `aguardando` incluído.

**`dev-story` e `story-review`** — prompt do subagente (preencha as chaves):

```
Execute a skill {acao} para a story {id} do projeto {projeto}.
Story: {project_path}/implementacao/{file}. Workspace: {workspace}.
{Retomada: continue de onde o Registro do desenvolvimento parou.}
{correcoes_revisao: a story-review devolveu esta story com correções: faça as tarefas R{n} abertas da seção Revisão.}

PASTA DE TRABALHO — use estas pastas no lugar do caminho do project-config.json / repositorios.md:
{para cada repositório: "- {nome}: {caminho} (branch feat/{id}, já preparada; não troque de branch)"}

MODO NÃO SUPERVISIONADO — ninguém vai responder perguntas:
- Siga a skill {acao} à risca, com a story como única fonte de verdade.
- A branch e a pasta de trabalho já estão prontas: não crie outra branch, não use git switch nem worktree.
  Não abra janela de terminal nem sessão nova.
- Onde a skill mandaria perguntar ou parar (ambiguidade, decisão em aberto, contrato além do previsto,
  algo de "Fora desta story", teste que já falhava antes, ação destrutiva), NÃO pergunte e NÃO invente:
  registre no Registro do desenvolvimento o que, onde e as opções, e termine.
- {commit_ao_concluir = true: "Ao mover para review, faça commit local em cada pasta de trabalho tocada com a commit_message do dev-story. Nunca push, merge, rebase, reset ou stash." | false: "Nunca faça commit, push, merge, rebase, reset, stash nem descarte."}
- Nunca apague arquivos, nunca use --force no status.py, nunca altere outra story.

Termine com exatamente estas linhas:
RESULTADO: concluida | bloqueada | falhou
CAUSA: decisao | ambiente | tecnica   (só se bloqueada ou falhou: ambiente = falta repositório, ferramenta, permissão ou serviço local; tecnica = erro de build/teste/código; decisao = precisa de uma pessoa decidir)
VERIFICAR: {só se CAUSA ambiente: caminho:{pasta} ou comando:{executável} que mostra que foi resolvido}
STATUS_FINAL: {status da story no sprint-status.yaml ao terminar}
MOTIVO: {uma frase; vazio se concluida}
RESUMO: {o que foi feito, arquivos e testes}
```

Para `story-review`: acrescente que a revisão aplica correções só se a própria skill permitir sem confirmação; achado de **decisão** = `bloqueada` com causa `decisao`; devolver ao dev (`in-progress` com tarefas `R{n}`) = `concluida` — a próxima rodada retoma a story no `dev-story`.

## Passo 4 — Registrar o resultado

Confira o que o subagente disse contra o `sprint-status.yaml` (`status.py show`) e o arquivo da story — vale o que está nos arquivos. Depois:

| Resultado | Quando | Na story | No estado/log |
|-----------|--------|----------|---------------|
| `concluida` | Story em `review` (dev-story); `done` ou devolvida a `in-progress` com tarefas `R{n}` (story-review); `ready-for-dev` (create-story) | O que a skill já escreveu | `registrar … --resultado concluida --motivo "{resumo curto}"` |
| `bloqueada` | Precisa de uma pessoa ou de uma mudança no ambiente | `status.py set {id} blocked` + linha no Histórico: `\| {data} \| {de} → blocked \| execucao-recorrente \| {motivo} \|` | **Por último** (depois de toda escrita na story): `registrar … --resultado bloqueada --causa {causa} --motivo "{motivo}" [--verificar …] [--repo {pasta de cada repositório}]` |
| `falhou` | Erro técnico: build/teste que não conseguiu corrigir, subagente interrompido, contexto estourado | Bloco no Registro do desenvolvimento (abaixo); a story fica onde está (`in-progress` é retomada na próxima rodada) | `registrar … --resultado falhou --motivo "{motivo}"` |

**Causa do bloqueio** — decide se a story volta sozinha (seção "Stories bloqueadas"):

| Causa | Quando | `--verificar` |
|-------|--------|---------------|
| `ambiente` | Falta repositório, ferramenta, permissão ou serviço local | Obrigatório: `caminho:{pasta}` e/ou `comando:{executável}` que provam que foi resolvido |
| `tecnica` | Falhou `max_tentativas` vezes por erro técnico | — (vale a assinatura: story + código) |
| `decisao` | Ambiguidade, decisão em aberto, checkpoint descoberto, achado de decisão da revisão, spec mudou. **Padrão** quando em dúvida | — |

Bloco de falha no **Registro do desenvolvimento** da story (acrescente, nunca apague):

```markdown
### {AAAA-MM-DD HH:MM} — Execução recorrente: falhou (tentativa {n}/{max})
- **Motivo:** {o que impediu, concreto: comando, erro, arquivo}
- **Onde parou:** {tarefa Tn / passo}
- **Para destravar:** {o que uma pessoa precisa fazer}
```

Se o `registrar` devolver `limite_atingido: true`: `status.py set {id} blocked` com a linha no Histórico "falhou {max} vezes: {último motivo}" e, por último, `registrar … --resultado bloqueada --causa tecnica --repo {pastas}`. A story sai da fila até a story ou o código mudarem (ou alguém mudar o estado), e a fila passa para a próxima tarefa.

**O motivo é obrigatório** em `bloqueada`, `falhou` e `pulada`: uma frase que permita a uma pessoa agir sem reabrir a execução ("`dotnet test` falha em ProdutoTests.Listar: NullReferenceException em ListarProdutosHandler.cs:42", não "erro nos testes").

Atualize também o `project.md` e a coluna Situação do `workspace.md` como a skill da tarefa faria (campo `situacao` do `status.py show`).

## Passo 5 — Liberar e responder

1. `lock liberar [--config {arquivo}]` — sempre, mesmo depois de erro.
2. Responda em poucas linhas, que é o que aparece no histórico da tarefa agendada:
   ```
   {projeto}/{id} ({acao}, {prioritario|sem-prioridade}): {resultado} — {resumo ou motivo}
   puladas: {n} ({motivos agrupados}) | fila restante: {n} | atenção: {n} | erros de configuração: {n}
   ```
   Sem nada a fazer: o `motivo` do `scan` e a lista de `atencao` (projeto/id: motivo), uma por linha.

---

## Modo contínuo

Pedido com `--continuo` (ou pelo agente `agente-entrega`): repita **Passo 0 → Passo 5** em sequência, uma tarefa por vez, sem esperar o próximo disparo:

1. A cada iteração, rode o `scan` de novo — a tarefa anterior muda o quadro (uma story revisada libera a dependente; uma desbloqueada volta à fila).
2. Pare quando: `escolhida` nula; `max_tarefas_por_rodada` tarefas feitas (`desbloquear` não conta); trava ocupada por outra rodada; ou duas falhas seguidas em projetos diferentes (provável problema de ambiente geral — ex.: sem rede, sem permissão).
3. Cada tarefa num subagente: o contexto principal guarda só a linha de resumo de cada uma. Nunca carregue o código ou a story aqui.
4. Ao parar, responda o resumo da rodada (uma linha por tarefa, a lista de atenção) e **agende o próximo despertar**:
   - num `/loop` sem intervalo: chame o `ScheduleWakeup` com `delaySeconds = espera_sugerida_s` do último `scan` (60 s com fila, 600 s com trava de outra rodada, 1800 s sem tarefas; parou pelo limite de tarefas → 60 s), o mesmo prompt do loop e um `reason` curto ("3 stories na fila", "nada a fazer: 2 bloqueadas aguardando decisão");
   - fora de um loop (`claude -p` agendado, rodada pedida numa conversa): só termine.

## Stories bloqueadas

Uma story `blocked` volta sozinha à fila **só se** foi bloqueada pela automação (registro com `bloqueio` e última linha do Histórico `→ blocked` por `execucao-recorrente`/`criacao-story-recorrente`) **e**:

| Causa | Volta quando | Tentativas ao voltar |
|-------|--------------|----------------------|
| `ambiente` | Todas as verificações passam (`caminho:` existe, `comando:` está no PATH) | Recomeçam |
| `tecnica` | A **assinatura** mudou: o arquivo da story, o `HEAD` ou a branch `feat/{id}` de algum repositório da story (uma pessoa corrigiu, anotou na story ou fez commit) | Uma a mais |
| `decisao` | Nunca sozinha | — |

Volta para `voltar_para`: `backlog` (create-story), `review` (story-review), `in-progress` se a implementação começou, senão `ready-for-dev`. Bloqueio feito por uma pessoa, de decisão ou cuja causa não mudou fica na lista de `atencao`: para destravar, uma pessoa resolve e move a story (`sprint-planning`).

## Criação de stories

- A ação `create-story` segue a `criacao-story-recorrente` (Passos 2 a 4 dela) e grava o estado em `_sdd/criacao-story-recorrente/`, o mesmo arquivo da skill de criação: as duas veem as criações uma da outra.
- Só cria quando o projeto tem menos de `max_prontas` stories `ready-for-dev` e na ordem de build — então só cria quando falta o que implementar.
- **Não agende as duas skills com arquivos de configuração diferentes**: cada arquivo tem a sua trava, e as duas poderiam criar a mesma story. Use só esta (com `create-story` em `acoes`) ou, se quiser a `criacao-story-recorrente` à parte, tire `create-story` de `acoes` ou passe às duas o mesmo `--config` (mesma trava).

## Agendar

`references/agendamento.md`: o `/loop` sem intervalo (modo contínuo), a tarefa agendada do Claude Desktop, o agente `agente-entrega` com `claude --agent` e o Agendador de Tarefas do Windows / cron. Lá também estão as permissões que a rodada precisa e o custo de disparar com frequência.

## Vários repositórios de código

- O Passo 2 prepara a pasta de trabalho de **todos** os repositórios da story, na ordem da seção Repositórios; se falhar num, `falhou` com o que já foi feito.
- O subagente recebe a lista de pastas e segue a seção "Vários repositórios" do `dev-story` (provedor antes do consumidor, `implementacao/multi-repo/{id}.md`).
- Com `commit_ao_concluir = true`, commit em cada pasta de trabalho tocada; nunca merge (a ordem de merge fica para a pessoa).
- No bloqueio, passe `--repo` com a pasta de cada repositório, para a assinatura acompanhar o código.

## Regras importantes

- **Uma tarefa por vez**, com a trava global, renovada entre os passos. Nunca rode sem o `recorrente.py`.
- **Sempre a próxima tarefa possível**: retomar → desbloquear → revisar → implementar → criar; tarefa dos sem prioridade só quando nenhum prioritário tiver tarefa. Story travada nunca para a fila: registre e passe para a próxima.
- **Nunca invente requisito nem decisão**: sem pessoa para perguntar, o que exigiria pergunta vira `bloqueada` com causa `decisao`. Na dúvida sobre a causa, é `decisao`.
- Desbloqueio automático só de causa `ambiente` ou `tecnica` e só do que a própria automação bloqueou.
- Story `in-progress` que a automação não começou nem foi devolvida pela revisão é de alguém: nunca a pegue.
- Checkpoints são sempre de uma pessoa: stories com `checkpoint: true` nunca entram na fila.
- Nos repositórios de código: worktree e branch `feat/{id}` sim; commit só com `commit_ao_concluir = true`; **nunca** push, merge, rebase, reset, stash, descarte, exclusão nem `git worktree remove`.
- Nunca `--force` no `status.py`. Nunca edite story que não é a da tarefa.
- Esta skill só edita: o arquivo da story, o `sprint-status.yaml` (via script), o `project.md`, o `workspace.md`, `_sdd/execucao-recorrente/`, `_sdd/criacao-story-recorrente/`, as worktrees `{repositório}.worktrees/` (via script e subagente) e — só a pedido do usuário — o arquivo de configuração.

## Troubleshooting

**Toda rodada responde "tarefa em andamento"** — uma rodada morreu com a trava ativa. Ela expira sozinha após `lock_expira_min`; para liberar antes, rode `lock liberar` (só se tiver certeza de que nada está rodando).

**Os repositórios sem prioridade nunca rodam** — é o esperado enquanto algum prioritário tiver tarefa (inclusive criar story). Confira a `fila` do `scan`; para alternar, mova o repositório de lista no arquivo de configuração.

**Story parada em `blocked`** — veja a `atencao` do `scan`: "precisa de decisão" é de uma pessoa; "ainda falta" diz o que instalar ou clonar; "nada mudou" pede uma correção no código ou uma anotação na story. Depois de resolver uma decisão, mova a story com `sprint-planning`.

**Projeto não aparece na fila** — sem `implementacao/sprint-status.yaml` ele é ignorado (nota no `scan`). Gere o quadro com `plan-epics` e `sprint-planning`.

**Story parada em `in-progress` e ninguém retoma** — confira em `estado.json` se ela foi iniciada pela automação, e no Histórico se a última linha é a devolução da `story-review`. Se foi uma pessoa, a fila a ignora de propósito; mova para `ready-for-dev` (`sprint-planning`) se quiser que a automação assuma.

**Muitas worktrees em `{repositório}.worktrees/`** — a skill nunca as apaga. Depois do merge de uma story, rode `git worktree remove {pasta}` no repositório (recusa se houver alteração sem commit) e, se quiser, apague a branch.

**`... já existe e não é a worktree de feat/{id}`** — sobrou uma pasta de uma worktree removida à mão. Confira o conteúdo, apague a pasta (ou `git worktree prune`) e a próxima rodada cria de novo.

**Contexto estourou no meio da story** — é `falhou`; o Registro diz onde parou e a próxima rodada retoma. Se acontece sempre, a story é grande demais para uma sessão: anote para a retrospectiva.
