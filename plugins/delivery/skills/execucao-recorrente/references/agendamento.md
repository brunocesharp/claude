# Agendar a execução recorrente

A skill tem duas formas: a **rodada única** faz uma tarefa e termina; o **modo contínuo** (`--continuo`) faz uma tarefa atrás da outra até a fila esvaziar (ou `max_tarefas_por_rodada`) e escolhe quando acordar de novo. Em qualquer forma, a trava global (ao lado do arquivo de configuração) garante uma tarefa por vez: enquanto uma tarefa está em andamento, outra rodada que dispare termina na hora, sem iniciar nada.

Antes de agendar, crie o arquivo de configuração e preencha as listas `prioritarios` e `sem_prioridade` (veja a SKILL.md). Pedir `/execucao-recorrente` numa conversa sem o arquivo cria o modelo e pergunta os repositórios.

Incluir, tirar ou mudar a prioridade de um repositório é só editar o arquivo: o agendamento não muda.

## Opções

| Opção | Roda onde | Precisa de sessão aberta | Ritmo | Quando usar |
|-------|-----------|--------------------------|-------|-------------|
| **`/loop /execucao-recorrente --continuo`** (sem intervalo) | No seu computador | Sim; o loop expira em 7 dias e não volta com `--resume` | A própria skill escolhe: 1 min com fila, 30 min sem tarefas | Recomendada para o dia a dia: não fica parada entre tarefas e quase não gasta quando não há o que fazer |
| **Tarefa agendada do Claude Desktop** | No seu computador | Não (o app precisa estar aberto e o computador ligado) | Intervalo fixo, mínimo 1 min | Rodar todo dia sem deixar um terminal aberto |
| **`claude --agent` / `claude -p` + Agendador de Tarefas do Windows / cron** | No seu computador | Não | O do agendador | Controle total por linha de comando |
| Rotina na nuvem | Nuvem (clone novo do repositório) | Não | Mínimo 1 hora | Não serve aqui: não vê as pastas locais |

Fonte: documentação do Claude Code, "Run prompts on a schedule" (code.claude.com/docs/en/scheduled-tasks), "Create custom subagents" (code.claude.com/docs/en/sub-agents) e "Run Claude Code programmatically" (code.claude.com/docs/en/headless).

## 1. `/loop` sem intervalo (modo contínuo)

```
/loop /execucao-recorrente --continuo
```

ou, com o arquivo em outro lugar, `/loop /execucao-recorrente --continuo --config D:\repos\execucao-recorrente.toml`.

Sem intervalo, o `/loop` deixa o Claude decidir quando voltar (de 1 minuto a 1 hora). A skill faz até `max_tarefas_por_rodada` tarefas seguidas e agenda o próximo despertar com a `espera_sugerida_s` do `scan`: 60 s quando há fila, 10 min quando outra rodada está com a trava, 30 min quando não há nada a fazer. Assim ela não fica parada entre tarefas e quase não gasta quando não há o que fazer.

- Para parar: `Esc` durante a espera.
- O loop roda só enquanto a sessão está aberta e ociosa. Ele expira em 7 dias e não é restaurado por `--resume`: rode `/loop` de novo.
- Cada tarefa roda num subagente; o contexto da sessão guarda só as linhas de resumo. Mesmo assim, num loop de vários dias, faça `/clear` de vez em quando e reinicie o loop.
- Para a sessão não parar pedindo permissão, libere antes os comandos da seção "Permissões".

## 2. Tarefa agendada do Claude Desktop

1. Instale o plugin `delivery` no Claude Code / Claude Desktop (`/plugin install delivery@claude`).
2. No Claude Desktop, crie uma tarefa agendada com o prompt `/execucao-recorrente --continuo` (a rodada esvazia a fila e termina), intervalo de 15–30 minutos, e a pasta de trabalho num dos workspaces (ou numa pasta que contenha todos).
3. Libere para a tarefa as pastas dos workspaces, dos repositórios de código **e a pasta-mãe deles** (as worktrees ficam em `{repositório}.worktrees/`, ao lado de cada repositório): sem acesso, a story fica `blocked` por ambiente ou `falhou`.
4. Permissões: as da seção "Permissões".

## 3. Agente `agente-entrega` com o Agendador de Tarefas do Windows

O plugin traz o agente `delivery:agente-entrega`: a sessão inteira roda como o agente de entrega, já com a skill carregada e as regras do modo não supervisionado.

Script `D:\repos\execucao-recorrente.cmd`:

```bat
@echo off
cd /d D:\repos
claude --agent delivery:agente-entrega -p "rode a fila --config D:\repos\execucao-recorrente.toml" ^
  --permission-mode acceptEdits ^
  --permission-prompts none ^
  --allowedTools "Bash(uv *),Bash(python *),Bash(git status *),Bash(git branch *),Bash(git switch *),Bash(git diff *),Bash(git worktree *),Bash(git rev-parse *),Bash(git show-ref *),Bash(git symbolic-ref *),Bash(dotnet *),Bash(npx *),Bash(npm *),Bash(mvn *)" ^
  >> D:\repos\execucao-recorrente.out.log 2>&1
```

Agendar a cada 30 minutos:

```bat
schtasks /create /tn "Execucao recorrente" /sc minute /mo 30 /tr "D:\repos\execucao-recorrente.cmd"
```

No Linux/macOS, uma linha no `crontab -e`: `*/30 * * * * cd ~/repos && claude --agent delivery:agente-entrega -p "rode a fila --config ~/repos/execucao-recorrente.toml" --permission-mode acceptEdits --permission-prompts none --allowedTools "..." >> ~/repos/execucao-recorrente.out.log 2>&1`.

Notas:
- A documentação mostra `--agent` para a sessão interativa e `--agents` com `-p`. **Teste uma vez à mão** antes de agendar: se a sua versão não aceitar `--agent` com `-p`, troque a linha por `claude -p "/execucao-recorrente --continuo --config ..."` — o efeito é o mesmo.
- Cada disparo esvazia a fila (até `max_tarefas_por_rodada`) e termina; a espera entre disparos é a do agendador. A trava impede que dois disparos trabalhem ao mesmo tempo.
- Num agente de plugin, `permissionMode` e `hooks` são ignorados: as permissões vêm das opções da linha de comando.
- `--permission-prompts none` nega o que pediria aprovação em vez de esperar; o Claude é avisado e a story termina `falhou` com o motivo. Requer Claude Code v2.1.259 ou mais novo.
- `acceptEdits` libera a edição de arquivos; comandos de shell precisam estar em `--allowedTools` (`Bash(git diff *)` libera tudo que começa com `git diff`). Inclua `Bash(git commit *)` só se usar `commit_ao_concluir = true`. Nunca libere `git push`.
- Não use `--bare`: ele não carrega os plugins instalados, e o agente e a skill vêm do plugin `delivery`.
- Os subagentes podem chamar subagentes até 3 níveis abaixo da sessão. Com o agente como sessão, a `story-review` (que usa subagentes para as lentes) fica no limite — não chame o `agente-entrega` como subagente de outra sessão.

## Permissões

A rodada precisa ler e editar arquivos e rodar:
- `uv` / `python`, para os scripts;
- `git status`, `branch`, `switch`, `diff`, `worktree`, `rev-parse`, `show-ref`, `symbolic-ref`, e `commit` só com `commit_ao_concluir = true`;
- os comandos de build e teste das stacks (`dotnet`, `npx ng`, `npm`, `mvn`).

Sem uma permissão, a tarefa termina `falhou` ou `blocked` (ambiente) com o motivo: confira o log nos primeiros dias.

## Custo

Cada disparo de um agendador fixo abre uma sessão do Claude, mesmo quando não há nada a fazer; uma rodada sem tarefas ou com a trava ativa termina logo e gasta pouco, mas não zero. Por isso o modo contínuo é mais barato: faz várias tarefas por disparo e, sem tarefas, dorme 30 minutos. Com agendador fixo, 15–30 minutos costuma bastar; restrinja o horário (dias úteis, horário comercial) se ninguém vai acompanhar os resultados fora dele.

## Acompanhar

- `scan` do `recorrente.py`: a fila na ordem de execução, a lista de `atencao` (o que precisa de uma pessoa) e o motivo de cada story pulada.
- `_sdd/execucao-recorrente/log/AAAA-MM.md` (implementação e revisão) e `_sdd/criacao-story-recorrente/log/AAAA-MM.md` (criação) de cada workspace: uma linha por tarefa, com resultado e motivo. Story pulada aparece uma vez por motivo, não a cada rodada; rodada sem tarefa ou com a trava ativa não escreve no log.
- Stories em `blocked` no quadro (`sprint-planning`) e no dashboard (`sdd-dashboard`): o motivo está no Histórico e no Registro do desenvolvimento da story.
- `_sdd/execucao-recorrente/estado.json`: tentativas, bloqueios e histórico por story.
- `git worktree list` em cada repositório: as pastas de trabalho das stories.
