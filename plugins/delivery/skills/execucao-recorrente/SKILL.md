---
name: execucao-recorrente
description: Executa, sem supervisão e de forma recorrente (ex.: a cada 5 minutos, por uma tarefa agendada), as stories prontas dos repositórios listados num arquivo de configuração, classificados como prioritários e sem prioridade — uma tarefa por vez; se não há tarefa em andamento, retoma a que ela mesma deixou in-progress ou inicia uma nova, primeiro dos repositórios prioritários e, só se nenhum tiver tarefa, dos sem prioridade. Roda o dev-story num contexto limpo e, quando não consegue concluir, registra o motivo na story, no log e, se for o caso, move a story para blocked. Use quando o usuário disser "execucao-recorrente", "execução recorrente", "executar as stories automaticamente", "rodar as tarefas pendentes dos projetos", "agendar a execução das stories", "processar a fila de stories", "adicionar repositório na execução recorrente". NÃO use para implementar uma story específica acompanhando (use dev-story), preparar stories (use create-story), revisar (use story-review), ver ou mudar o quadro (use sprint-planning) ou mudar requisito (use correct-course).
metadata:
  version: 1.0.0
  category: implementation
  depends-on: dev-story
  output: código nos repositórios das stories (via dev-story); Registro do desenvolvimento e Histórico das stories; {workspace}/_sdd/execucao-recorrente/ (estado.json, log/AAAA-MM.md); trava global ao lado do arquivo de configuração
---

# Execução Recorrente

Processa a fila de stories de vários repositórios **sem ninguém olhando**, **uma tarefa por vez**. Cada rodada faz no máximo uma story, do começo ao fim, e termina. Pensada para rodar a cada poucos minutos por uma tarefa agendada (`references/agendamento.md`): enquanto uma tarefa está em andamento, as rodadas seguintes veem a trava e terminam sem iniciar nada.

**Só trabalha com o quadro de stories**: entram apenas os projetos com `docs/{projeto}/implementacao/sprint-status.yaml` (fluxo `plan-epics` → `sprint-planning` → `create-story`). Projeto sem quadro, inclusive o que só tem `plan-execution`, fica fora da fila com uma nota no `scan`; para incluí-lo, gere o quadro.

Ela não implementa nada por conta própria: escolhe a story, prepara o terreno e entrega a story ao `dev-story` (ou à `story-review`/`create-story`, se o projeto liberar) num contexto limpo, com as regras do modo não supervisionado. O que não puder ser feito sem uma pessoa vira **motivo registrado**, nunca suposição.

Leia antes de executar: `sdd-setup/references/sprint-status.md` (plugin `sdd`; estados e transições) e a SKILL.md do `dev-story`.

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
lock_expira_min = 90    # validade da trava; maior que a tarefa mais longa
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

O resultado traz `em_andamento` (trava global ativa), `escolhida`, `motivo`, a `fila` completa em ordem, os `grupos` (prioritário e sem prioridade) com cada repositório, projeto e as stories `puladas` com o motivo, mais `erros` e `avisos`.

**Ordem de escolha:**

1. **Tarefa em andamento** (`em_andamento: true`) → não inicia nada. Responda `tarefa em andamento: {motivo}` e termine.
2. **Retomar**: story `in-progress` que a própria execução recorrente começou e não terminou (a rodada anterior morreu, estourou o contexto ou falhou por erro técnico) — vem antes de qualquer tarefa nova, de qualquer grupo.
3. **Nova tarefa dos repositórios prioritários**, na ordem da lista; dentro de cada projeto, a ordem do `status.py next`: `review` (se `story-review` estiver em `acoes`) → `ready-for-dev` na ordem de build → primeira `backlog` (se `create-story` estiver em `acoes`).
4. **Só se nenhum prioritário tiver tarefa**, nova tarefa dos repositórios **sem prioridade**, na mesma regra.

Ficam **fora** da fila, com o motivo em `puladas`:
- `in-progress` que a execução recorrente não começou (alguém pode estar nela);
- story com `checkpoint: true` (precisa de acompanhamento humano);
- `depends_on` com story que ainda não está em `review` ou `done`;
- story que já falhou `max_tentativas` vezes na mesma ação;
- projeto com `habilitado = false`.

`escolhida` nula: não registre nada, responda o `motivo` (ex.: `sem tarefas nos repositórios prioritários nem nos sem prioridade`) e termine.

## Customização (por projeto)

Para o projeto da story escolhida, resolva a customização desta skill a partir da raiz do workspace dele:

```
uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto}
```

Sem o script (ou sem `uv`/`python`): leia `${CLAUDE_SKILL_DIR}/customize.toml` e, se existir, `docs/{projeto}/_custom/execucao-recorrente.toml`, e mescle pelas regras de `sdd-setup/references/customizacao.md`. Sem override, valem os padrões da skill.

1. Execute os `workflow.activation_steps_prepend`, na ordem.
2. Leia os arquivos de `facts` (e os textos literais): são fatos válidos durante toda a skill e vencem os padrões dela quando conflitarem.
3. Use os valores de `resolved.workflow` onde esta skill os cita: `habilitado` e `acoes` (filtram a fila no `scan`), `max_tentativas` (Passo 4) e `commit_ao_concluir` (Passo 3). O `recorrente.py` já lê esses quatro campos do override do projeto.
4. Ao terminar, execute os `workflow.activation_steps_append` e o `workflow.on_complete`.

Mostre os `warnings` uma vez no resumo final.

## Scripts

```
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" init-config [--config {arquivo}]   # cria o modelo; nunca sobrescreve
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" config      [--config {arquivo}]   # valida e mostra as listas
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" scan        [--config {arquivo}]
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" lock adquirir|liberar [--config {arquivo}] [--dono "{texto}"]
uv run "${CLAUDE_SKILL_DIR}/scripts/recorrente.py" registrar {workspace} --projeto {projeto} --id {id} --acao {acao} --resultado iniciada|concluida|falhou|bloqueada|pulada [--motivo "{motivo}"]
```

E, a partir da raiz de cada workspace, os scripts do fluxo: `_sdd/scripts/status.py` e `_sdd/scripts/story.py` (`sprint-status.md`).

Sem `uv`: `python` 3.11+ com `pyyaml`. Sem nenhum dos dois, **não rode sem supervisão**: sem a trava e o estado, duas rodadas podem pegar tarefas ao mesmo tempo. Responda `sem python 3.11+: execução recorrente desativada` e termine.

Onde o script grava:

| Arquivo | Conteúdo |
|---------|----------|
| `{config}.lock.json`, ao lado do arquivo de configuração (ex.: `~/.claude/execucao-recorrente.lock.json`) | Trava global: `ativo` com início, validade e dono, ou `livre`. Nunca é apagado, só regravado |
| `{workspace}/_sdd/execucao-recorrente/estado.json` | Por story: ação, tentativas, último resultado e motivo, histórico das últimas 20 execuções e o motivo atual de `pulada` (com a data desde quando) |
| `{workspace}/_sdd/execucao-recorrente/log/AAAA-MM.md` | Uma linha por execução: data, projeto, story, ação, resultado, tentativa e motivo. `pulada` só quando o motivo muda |

---

## Passo 1 — Travar

1. `lock adquirir [--config {arquivo}] --dono "{origem da rodada e hora}"`.
   - `adquirido: false`: outra rodada começou uma tarefa entre o `scan` e a trava. Termine com `tarefa em andamento`.
   - `assumiu_expirado: true`: a rodada anterior morreu sem liberar. Se ela deixou uma story `in-progress`, a fila já a traz como retomada.
2. A validade (`execucao.lock_expira_min`, padrão 90 min) precisa ser maior que a story mais longa: uma tarefa que estoura a validade pode ser alcançada por outra rodada.
3. **Daqui em diante, toda saída passa pelo Passo 5** (liberar a trava), inclusive em erro.

## Passo 2 — Pré-condições, sem perguntar

Faça as conferências do Passo 2 do `dev-story`, trocando cada pergunta por uma decisão registrada:

| Situação | O que fazer | Resultado |
|----------|-------------|-----------|
| `story.py check {id}` com `problems` | Não começa | `falhou` — "story incompleta: {problems}" |
| Repositório de código da story não existe no caminho local | Não começa | `falhou` — "repositório {r} não encontrado em {caminho}" |
| Repositório de código com alterações pendentes de **outra** story ou branch diferente com trabalho em aberto | Não mexe | `pulada` — "aguardando commit/limpeza em {r} ({branch atual})". Não conta tentativa |
| Branch `feat/{id}` não existe | Cria a partir da branch principal (o modo não supervisionado vale como `auto_mode = sim` só para isso) | segue |
| `status.py` recusa a transição | Não força | `falhou` — mensagem do script |

`falhou` ou `pulada` **antes de começar** a story: registre (`registrar …`) e passe para a próxima da `fila`. `pulada` não conta tentativa e só entra no log quando o motivo muda (o `registrar` devolve `repetida: true` e não grava nada se o motivo é o mesmo da rodada anterior); mantenha o texto do motivo estável entre rodadas — sem horário nem contagem — para isso funcionar. Siga para a próxima, mantendo a ordem (retomadas → prioritários → sem prioridade). Assim um repositório prioritário travado não impede o trabalho nos outros. Sem próxima, vá para o Passo 5.

Começando de verdade: `registrar … --resultado iniciada` **antes** de chamar o `dev-story` — é isso que permite retomar a story se esta rodada morrer.

## Passo 3 — Executar em contexto limpo

Rode a ação num **subagente** (ferramenta Agent), para a story ser a primeira coisa do contexto, como o `dev-story` exige. Sem ferramenta de subagente, execute aqui mesmo: numa tarefa agendada cada rodada já é uma sessão nova. Nunca abra janela de terminal (`session.py`): não há ninguém para usá-la.

Prompt do subagente (preencha as chaves):

```
Execute a skill {acao} para a story {id} do projeto {projeto}.
Story: {project_path}/implementacao/{file}. Workspace: {workspace}. {Retomada: continue de onde o Registro do desenvolvimento parou.}

MODO NÃO SUPERVISIONADO — ninguém vai responder perguntas:
- Siga a skill {acao} à risca, com a story como única fonte de verdade.
- Pode criar a branch feat/{id}. Não abra janela de terminal nem sessão nova.
- Onde a skill mandaria perguntar ou parar (ambiguidade, decisão em aberto, contrato além do previsto,
  algo de "Fora desta story", teste que já falhava antes, ação destrutiva), NÃO pergunte e NÃO invente:
  registre no Registro do desenvolvimento o que, onde e as opções, e termine.
- {commit_ao_concluir = true: "Ao mover para review, faça commit local em cada repositório tocado com a commit_message do dev-story. Nunca push, merge, rebase, reset ou stash." | false: "Nunca faça commit, push, merge, rebase, reset, stash nem descarte."}
- Nunca apague arquivos, nunca use --force no status.py, nunca altere outra story.

Termine com exatamente estas linhas:
RESULTADO: concluida | bloqueada | falhou
STATUS_FINAL: {status da story no sprint-status.yaml ao terminar}
MOTIVO: {uma frase; vazio se concluida}
RESUMO: {o que foi feito, arquivos e testes}
```

Para `story-review`: acrescente que a revisão aplica correções só se a própria skill permitir sem confirmação; achado de **decisão** = `bloqueada`. Para `create-story`: a story só vai para `ready-for-dev` se o `story.py check` passar.

## Passo 4 — Registrar o resultado

Confira o que o subagente disse contra o `sprint-status.yaml` (`status.py show`) e o arquivo da story — vale o que está nos arquivos. Depois:

| Resultado | Quando | Na story | No estado/log |
|-----------|--------|----------|---------------|
| `concluida` | Story em `review` (dev-story), `done`/`in-progress` com correções (story-review) ou `ready-for-dev` (create-story) | O que a skill já escreveu | `registrar … --resultado concluida --motivo "{resumo curto}"` |
| `bloqueada` | Precisa de decisão humana (regra da fonte única, checkpoint descoberto, decisão da revisão) | `status.py set {id} blocked` + linha no Histórico: `\| {data} \| {de} → blocked \| execucao-recorrente \| {motivo} \|` | `registrar … --resultado bloqueada --motivo "{motivo}"` |
| `falhou` | Erro técnico: build/teste que não conseguiu corrigir, ferramenta ou repositório ausente, subagente interrompido, contexto estourado | Bloco no Registro do desenvolvimento (abaixo); a story fica onde está (`in-progress` é retomada na próxima rodada) | `registrar … --resultado falhou --motivo "{motivo}"` |

Bloco de falha no **Registro do desenvolvimento** da story (acrescente, nunca apague):

```markdown
### {AAAA-MM-DD HH:MM} — Execução recorrente: falhou (tentativa {n}/{max})
- **Motivo:** {o que impediu, concreto: comando, erro, arquivo}
- **Onde parou:** {tarefa Tn / passo}
- **Para destravar:** {o que uma pessoa precisa fazer}
```

Se o `registrar` devolver `limite_atingido: true`: `status.py set {id} blocked` com a linha no Histórico "falhou {max} vezes: {último motivo}". A story sai da fila até alguém mudar o estado, e a próxima rodada passa para a próxima tarefa.

**O motivo é obrigatório** em `bloqueada`, `falhou` e `pulada`: uma frase que permita a uma pessoa agir sem reabrir a execução ("`dotnet test` falha em ProdutoTests.Listar: NullReferenceException em ListarProdutosHandler.cs:42", não "erro nos testes").

Atualize também o `project.md` e a coluna Situação do `workspace.md` como o `dev-story` faria (campo `situacao` do `status.py show`).

## Passo 5 — Liberar e responder

1. `lock liberar [--config {arquivo}]` — sempre, mesmo depois de erro.
2. Responda em poucas linhas, que é o que aparece no histórico da tarefa agendada:
   ```
   {projeto}/{id} ({acao}, {prioritario|sem-prioridade}): {resultado} — {resumo ou motivo}
   puladas: {n} ({motivos agrupados}) | fila restante: {n} | erros de configuração: {n}
   ```
   Sem nada a fazer: só o `motivo` do `scan`.

---

## Agendar

`references/agendamento.md` mostra como rodar a skill a cada 5 minutos: pela tarefa agendada do Claude Desktop (com o computador ligado) ou pelo Claude Code em modo não interativo com o Agendador de Tarefas do Windows / cron. Lá também estão as permissões que a rodada precisa e o custo de disparar com frequência.

## Vários repositórios de código

- O Passo 2 confere **todos** os repositórios de código da story; qualquer um com trabalho de outra story → `pulada`.
- A branch `feat/{id}` é criada em todos, na ordem da seção Repositórios; se falhar num, `falhou` com o que já foi feito.
- O subagente segue a seção "Vários repositórios" do `dev-story` (provedor antes do consumidor, `implementacao/multi-repo/{id}.md`).
- Com `commit_ao_concluir = true`, commit em cada repositório tocado; nunca merge (a ordem de merge fica para a pessoa).

## Regras importantes

- **Uma tarefa por vez**, com a trava global. Nunca rode sem o `recorrente.py`.
- **Retomar antes de iniciar**; tarefa nova só do grupo sem prioridade quando nenhum prioritário tiver tarefa.
- **Nunca invente requisito nem decisão**: sem pessoa para perguntar, o que exigiria pergunta vira `bloqueada` com o motivo.
- Story `in-progress` que a execução recorrente não começou é de alguém: nunca a pegue.
- Checkpoints são sempre de uma pessoa: stories com `checkpoint: true` nunca entram na fila.
- Nos repositórios de código: branch sim; commit só com `commit_ao_concluir = true`; **nunca** push, merge, rebase, reset, stash, descarte ou exclusão.
- Nunca `--force` no `status.py`. Nunca edite story que não é a da rodada.
- Esta skill só edita: o arquivo da story, o `sprint-status.yaml` (via script), o `project.md`, o `workspace.md`, `_sdd/execucao-recorrente/` e — só a pedido do usuário — o arquivo de configuração.

## Troubleshooting

**Toda rodada responde "tarefa em andamento"** — uma rodada morreu com a trava ativa. Ela expira sozinha após `lock_expira_min`; para liberar antes, rode `lock liberar` (só se tiver certeza de que nada está rodando).

**Os repositórios sem prioridade nunca rodam** — é o esperado enquanto algum prioritário tiver tarefa. Confira a `fila` do `scan`; para alternar, mova o repositório de lista no arquivo de configuração.

**Story parada como `pulada`** — normalmente "aguardando commit": faça o commit (ou ligue `commit_ao_concluir`) no repositório indicado. O log tem uma linha só, da primeira vez que o motivo apareceu; `estado.json` (campo `pulada.desde`) e o `scan` mostram que ela continua parada.

**Projeto não aparece na fila** — sem `implementacao/sprint-status.yaml` ele é ignorado (nota no `scan`). Gere o quadro com `plan-epics` e `sprint-planning`.

**Story parada em `in-progress` e ninguém retoma** — confira em `estado.json` se ela foi iniciada pela execução recorrente. Se foi uma pessoa, a fila a ignora de propósito; mova para `ready-for-dev` (`sprint-planning`) se quiser que a execução assuma.

**Story voltou para a fila depois de `blocked`** — alguém mudou o estado; as tentativas recomeçam quando a ação muda. Para zerar sem mudar a ação, rode `registrar … --resultado concluida`.

**Contexto estourou no meio da story** — é `falhou`; o Registro diz onde parou e a próxima rodada retoma. Se acontece sempre, a story é grande demais para uma sessão: anote para a retrospectiva.
