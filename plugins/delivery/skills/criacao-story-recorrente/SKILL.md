---
name: criacao-story-recorrente
description: Cria stories com o create-story sem supervisão e de forma recorrente (ex.: a cada 15 minutos, por uma tarefa agendada), nos repositórios listados num arquivo de configuração, classificados como prioritários e sem prioridade — uma tarefa por vez; se não há criação em andamento, retoma a que ela mesma deixou pela metade ou cria a próxima story do backlog (dependências prontas, abaixo do limite de stories ready-for-dev), primeiro dos repositórios prioritários e, só se nenhum tiver story a criar, dos sem prioridade. Roda o create-story num contexto limpo, move a story para ready-for-dev quando o story.py check passa e, quando não consegue concluir, registra o motivo no log e, se precisa de uma pessoa, move a story para blocked. Use quando o usuário disser "criacao-story-recorrente", "criar stories automaticamente", "criação recorrente de stories", "agendar o create-story", "manter stories prontas", "adicionar repositório na criação de stories". NÃO use para criar uma story específica acompanhando (use create-story), implementar stories sem supervisão (use execucao-recorrente), planejar épicos (use plan-epics), ver o quadro (use sprint-planning) ou mudar requisito (use correct-course).
metadata:
  version: 1.0.0
  category: plan
  depends-on: create-story
  output: docs/{projeto}/implementacao/stories/{id}.md (via create-story); {workspace}/_sdd/criacao-story-recorrente/ (estado.json, log/AAAA-MM.md); trava global ao lado do arquivo de configuração
---

# Criação Recorrente de Stories

Mantém o backlog dos projetos **convertido em stories prontas**, sem ninguém olhando, **uma criação por vez**. Cada rodada cria no máximo uma story e termina. Pensada para rodar periodicamente por uma tarefa agendada (`references/agendamento.md`), ao lado da `execucao-recorrente`: esta prepara as stories (`backlog → ready-for-dev`), aquela as implementa.

Ela não escreve a story por conta própria: escolhe qual criar e entrega ao `create-story` num contexto limpo, com as regras do modo não supervisionado. O que exigiria uma pergunta ao usuário vira **motivo registrado** e story `blocked`, nunca requisito inventado.

Leia antes de executar: a SKILL.md do `create-story` e `sdd-setup/references/sprint-status.md` (plugin `sdd`; estados e transições). A lógica de configuração, trava e registro é a mesma da `execucao-recorrente`; o script é compartilhado com ela.

---

## Arquivo de configuração

Os repositórios verificados ficam num arquivo TOML fora do plugin:

1. `--config {arquivo}` no pedido (`/criacao-story-recorrente --config D:\repos\criacao-story-recorrente.toml`);
2. senão, a variável de ambiente `CRIACAO_STORY_RECORRENTE_CONFIG`;
3. senão, `~/.claude/criacao-story-recorrente.toml` (no Windows, `C:\Users\{usuário}\.claude\criacao-story-recorrente.toml`).

```toml
[repositorios]
prioritarios = [
  'D:\repos\docs-loja',
]
sem_prioridade = [
  'D:\repos\docs-estoque',
]

[execucao]
lock_expira_min = 60    # validade da trava; maior que a criação mais longa
```

O formato e as regras são os da `execucao-recorrente`: cada caminho é a raiz de um workspace (todos os projetos com `sprint-status.yaml`), a pasta de um projeto ou uma pasta dentro de um workspace; aspas simples; a ordem de cada lista é a ordem de verificação; caminho nas duas listas vale como prioritário; caminho inexistente vai para `erros` sem impedir os demais.

**A mesma lista das duas skills:** passe às duas o mesmo `--config` (ou aponte as duas variáveis para o mesmo arquivo). Elas passam a usar as mesmas listas **e a mesma trava**: no total, uma tarefa por vez entre criação e implementação. Com arquivos separados (o padrão), cada skill tem a sua trava e as duas podem rodar ao mesmo tempo — a criação só escreve no workspace de documentação e só lê os repositórios de código.

**Sem o arquivo** (`scan` devolve erro): numa conversa, crie o modelo com `init-config`, mostre o caminho e pergunte quais repositórios entram em cada lista; grave com a ferramenta Edit. Em execução agendada, termine com `sem arquivo de configuração: {caminho}` — nunca adivinhe repositórios.

**Pedidos para mudar a lista** — edite só o arquivo de configuração, rode `config` para validar e mostre as duas listas como ficaram.

## Passo 0 — Ler a configuração e montar a fila

```
uv run "${CLAUDE_SKILL_DIR}/scripts/story_recorrente.py" scan [--config {arquivo}]
```

O resultado traz `em_andamento` (trava ativa), `escolhida`, `motivo`, a `fila` em ordem e os `grupos` com cada repositório, projeto (`prontas` = stories `ready-for-dev`) e as `puladas` com o motivo, mais `erros` e `avisos`.

**Ordem de escolha:**

1. **Criação em andamento** (`em_andamento: true`) → não inicia nada. Responda `criação em andamento: {motivo}` e termine.
2. **Retomar**: story que esta skill começou a criar e não terminou (a rodada morreu ou estourou o contexto) — antes de qualquer story nova, de qualquer grupo.
3. **Nova story dos repositórios prioritários**, na ordem da lista: em cada projeto, a **primeira** story em `backlog` na ordem de build cujas dependências estão prontas.
4. **Só se nenhum prioritário tiver story a criar**, a dos repositórios **sem prioridade**, na mesma regra.

Cada projeto oferece no máximo uma story nova por rodada (o `create-story` cria uma por vez, para cada uma levar os aprendizados da anterior). Ficam **fora** da fila, com o motivo em `puladas`:
- projeto que já tem `max_prontas` stories em `ready-for-dev` (padrão 2): não há pressa em escrever a próxima;
- story cujas `depends_on` (frontmatter do épico) não estão num estado de `dependencias_em` (padrão `review` ou `done`) — a skill passa para a próxima story do backlog sem dependência pendente;
- story com o arquivo pronto aguardando confirmação de uma pessoa (`exige_confirmacao = true`);
- story que já falhou `max_tentativas` vezes;
- story `blocked`, épico `done` ou `dropped`, projeto com `habilitado = false`.

`escolhida` nula: não registre nada, responda o `motivo` e termine.

## Customização (por projeto)

Para o projeto da story escolhida, resolva a customização desta skill a partir da raiz do workspace dele:

```
uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto}
```

Sem o script (ou sem `uv`/`python`): leia `${CLAUDE_SKILL_DIR}/customize.toml` e, se existir, `docs/{projeto}/_custom/criacao-story-recorrente.toml`, e mescle pelas regras de `sdd-setup/references/customizacao.md`. Sem override, valem os padrões da skill.

1. Execute os `workflow.activation_steps_prepend`, na ordem.
2. Leia os arquivos de `facts` (e os textos literais): são fatos válidos durante toda a skill e vencem os padrões dela quando conflitarem.
3. Use os valores de `resolved.workflow` onde esta skill os cita: `habilitado`, `max_prontas` e `dependencias_em` (filtram a fila no `scan`), `exige_confirmacao` (Passo 3) e `max_tentativas` (Passo 4). O script já lê esses campos do override do projeto.
4. Ao terminar, execute os `workflow.activation_steps_append` e o `workflow.on_complete`.

A customização do próprio `create-story` no projeto (`_custom/create-story.toml`: template, padrão de branch, seções extras) continua valendo: é o `create-story` que a aplica.

## Scripts

```
uv run "${CLAUDE_SKILL_DIR}/scripts/story_recorrente.py" init-config [--config {arquivo}]
uv run "${CLAUDE_SKILL_DIR}/scripts/story_recorrente.py" config      [--config {arquivo}]
uv run "${CLAUDE_SKILL_DIR}/scripts/story_recorrente.py" scan        [--config {arquivo}]
uv run "${CLAUDE_SKILL_DIR}/scripts/story_recorrente.py" lock adquirir|liberar [--config {arquivo}] [--dono "{texto}"]
uv run "${CLAUDE_SKILL_DIR}/scripts/story_recorrente.py" registrar {workspace} --projeto {projeto} --id {id} --acao create-story --resultado iniciada|concluida|aguardando|bloqueada|falhou|pulada [--motivo "{motivo}"]
```

`story_recorrente.py` chama o `recorrente.py` da `execucao-recorrente` (mesmo plugin) no perfil `criacao`; se ele não for encontrado, reinstale o plugin `delivery`. A partir da raiz de cada workspace, os scripts do fluxo: `_sdd/scripts/status.py`, `epics.py` e `story.py`.

Sem `uv`: `python` 3.11+ com `pyyaml`. Sem nenhum dos dois, **não rode sem supervisão**: responda `sem python 3.11+: criação recorrente desativada` e termine.

Onde o script grava: a trava em `{config}.lock.json` ao lado do arquivo de configuração; em cada workspace, `_sdd/criacao-story-recorrente/estado.json` (tentativas e último resultado por story) e `_sdd/criacao-story-recorrente/log/AAAA-MM.md` (uma linha por rodada, com o motivo).

---

## Passo 1 — Travar

1. `lock adquirir [--config {arquivo}] --dono "{origem da rodada e hora}"`.
   - `adquirido: false`: outra rodada começou entre o `scan` e a trava. Termine com `criação em andamento`.
   - `assumiu_expirado: true`: a rodada anterior morreu; se ela deixou uma story pela metade, a fila já a traz como retomada.
2. **Daqui em diante, toda saída passa pelo Passo 5** (liberar a trava), inclusive em erro.

## Passo 2 — Pré-condições, sem perguntar

| Situação | O que fazer | Resultado |
|----------|-------------|-----------|
| Story não está mais em `backlog` (alguém mexeu entre o `scan` e agora) | Não cria | `pulada` — "story em {estado}". Não conta tentativa |
| Workspace sem `_sdd/scripts/` (sem `epics.py`/`story.py`) | Não cria: o `create-story` precisa deles para copiar a spec e validar | `falhou` — "workspace sem _sdd/scripts: rode o sdd-setup" |
| Arquivo do épico da story não encontrado | Não cria | `bloqueada` — "épico {epic} sem arquivo em implementacao/epicos/" |

Com `pulada` ou `falhou` antes de começar: registre (`registrar …`) e passe para a próxima da `fila`, mantendo a ordem (retomadas → prioritários → sem prioridade). Sem próxima, vá para o Passo 5.

Começando de verdade: `registrar … --resultado iniciada` **antes** de chamar o `create-story` — é isso que permite retomar se esta rodada morrer.

## Passo 3 — Criar em contexto limpo

Rode o `create-story` num **subagente** (ferramenta Agent), para a story ser preparada só com o contexto que ela mesma junta. Sem ferramenta de subagente, execute aqui mesmo: numa tarefa agendada cada rodada já é uma sessão nova. Nunca abra janela de terminal nem ofereça sessão nova (Passo 7 do `create-story`): não há ninguém para usá-la.

Prompt do subagente (preencha as chaves):

```
Execute a skill create-story para a story {id} do projeto {projeto}.
Workspace: {workspace}. Projeto: {project_path}. Épico: {epic}. {Retomada: o arquivo pode existir pela metade; refaça-o a partir do Passo 2.}

MODO NÃO SUPERVISIONADO — ninguém vai responder perguntas:
- Siga a skill create-story à risca: Passos 0 a 4 (escolher a story {id}, juntar o contexto, escrever, validar com story.py check).
- Nos repositórios de código, só leitura: nada de branch, commit ou arquivo novo.
- Onde a skill mandaria perguntar ou parar — dúvida que só o usuário responde, cenário citado que não existe mais na spec
  (missing no epics.py spec), contrato incompatível sem estratégia, story que não cabe numa sessão, dependência ainda não pronta —
  NÃO pergunte e NÃO invente: termine com RESULTADO bloqueada e o motivo. Se o arquivo da story já foi gravado, registre
  a dúvida em Decisões em aberto.
- Passo 5 (confirmação): {exige_confirmacao = false: "não há confirmação humana: se o story.py check não tiver problems, faça o Passo 6 (attach, set ready-for-dev, Histórico com 'criacao-story-recorrente (confirmação automática)', Situação do workspace.md)." | true: "não confirme: rode só o status.py attach e deixe a story em backlog, com a linha no Histórico 'arquivo pronto, aguardando confirmação'. Termine com RESULTADO aguardando."}
- Não faça o Passo 7. Nunca use --force no status.py, nunca altere outra story, nunca apague arquivos.

Termine com exatamente estas linhas:
RESULTADO: concluida | aguardando | bloqueada | falhou
STATUS_FINAL: {status da story no sprint-status.yaml ao terminar}
MOTIVO: {uma frase; vazio se concluida}
RESUMO: {critérios, tarefas, repositórios, warnings do story.py check}
```

## Passo 4 — Registrar o resultado

Confira o que o subagente disse contra o `sprint-status.yaml` (`status.py show`), o arquivo da story e o `story.py check {id}` — vale o que está nos arquivos. Uma story que diz `concluida` mas tem `problems` no check é `falhou`.

| Resultado | Quando | No quadro e na story | No estado/log |
|-----------|--------|----------------------|---------------|
| `concluida` | Story em `ready-for-dev`, check sem problemas | O que o `create-story` já fez (Passo 6) | `registrar … --resultado concluida --motivo "{n} CA, {n} tarefas"` |
| `aguardando` | `exige_confirmacao = true`, arquivo pronto e ligado (`attach`), story em `backlog` | Linha no Histórico: aguardando confirmação | `registrar … --resultado aguardando` — a story sai da fila até uma pessoa confirmar (`create-story {id}` para revisar, ou `status.py set {id} ready-for-dev`) |
| `bloqueada` | Precisa de uma pessoa: dúvida de requisito, spec mudou (`correct-course`), contrato sem estratégia, story grande demais (`plan-epics`) | `status.py set {id} blocked`; se o arquivo da story existe, linha no Histórico: `\| {data} \| backlog → blocked \| criacao-story-recorrente \| {motivo} \|` | `registrar … --resultado bloqueada --motivo "{motivo e skill sugerida}"` |
| `falhou` | Erro técnico: script falhou, subagente interrompido, contexto estourado, check com problemas que ele não corrigiu | A story fica em `backlog`; arquivo pela metade é refeito na próxima tentativa | `registrar … --resultado falhou --motivo "{motivo}"` |

Se o `registrar` devolver `limite_atingido: true`: `status.py set {id} blocked` com a linha no Histórico "falhou {max} vezes: {último motivo}" (se houver arquivo). A story sai da fila; a próxima rodada passa para a próxima story do backlog.

**O motivo é obrigatório** em `bloqueada`, `falhou` e `pulada`, concreto o bastante para uma pessoa agir sem reabrir a rodada ("cenário 1.4 citado em covers não existe mais na spec-functional do escopo produtos: rodar correct-course", não "erro na spec"). Story bloqueada **sem arquivo** (parou antes de escrever) tem o motivo só no log e no `estado.json`: diga isso na resposta.

## Passo 5 — Liberar e responder

1. `lock liberar [--config {arquivo}]` — sempre, mesmo depois de erro.
2. Responda em poucas linhas, que é o que aparece no histórico da tarefa agendada:
   ```
   {projeto}/{id} (create-story, {prioritario|sem-prioridade}): {resultado} — {resumo ou motivo}
   puladas: {n} ({motivos agrupados}) | fila restante: {n} | erros de configuração: {n}
   ```
   Sem nada a fazer: só o `motivo` do `scan`.

---

## Agendar

`references/agendamento.md`: como agendar (tarefa agendada do Claude Desktop, `/loop` ou `claude -p` com o Agendador de Tarefas do Windows), as permissões — menores que as da `execucao-recorrente`, porque a criação não compila nem testa — e como combinar as duas skills.

## Regras importantes

- **Uma criação por vez**, com a trava. Nunca rode sem o script.
- **Retomar antes de iniciar**; story nova dos sem prioridade só quando nenhum prioritário tiver story a criar.
- **Uma story nova por projeto por rodada**, na ordem de build, e só abaixo de `max_prontas`.
- **Nunca invente requisito**: o que exigiria pergunta vira `bloqueada` com o motivo; critérios e cenários continuam copiados literalmente pelo `create-story`.
- `ready-for-dev` só com `story.py check` sem problemas.
- Repositórios de código: só leitura.
- Nunca `--force` no `status.py`. Nunca edite story que não é a da rodada.
- Esta skill só edita: o arquivo da story, o `sprint-status.yaml` (via script), o `project.md`, o `workspace.md`, `_sdd/criacao-story-recorrente/` e — só a pedido do usuário — o arquivo de configuração.

## Troubleshooting

**Nenhuma story é criada e o motivo é `max_prontas`** — o projeto já tem stories prontas esperando implementação. É o esperado; aumente `max_prontas` no `_custom/criacao-story-recorrente.toml` do projeto se quiser mais folga.

**Story pulada por dependência o tempo todo** — a anterior ainda não chegou a `review`. Com a `execucao-recorrente` rodando, ela chega sozinha; sem ela, implemente a anterior ou mude `dependencias_em`.

**Stories bloqueadas com "spec mudou"** — rode `correct-course` no projeto; depois devolva a story ao backlog (`sprint-planning`) e a próxima rodada a cria de novo.

**Toda rodada responde "criação em andamento"** — uma rodada morreu com a trava ativa. Ela expira sozinha após `lock_expira_min`; para liberar antes, `lock liberar` (só se tiver certeza de que nada está rodando).

**`script compartilhado não encontrado`** — a skill depende do `recorrente.py` da `execucao-recorrente`, no mesmo plugin `delivery`. Reinstale ou atualize o plugin.
