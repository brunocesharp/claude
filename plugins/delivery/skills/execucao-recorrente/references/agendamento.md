# Agendar a execução recorrente

A skill faz uma rodada e termina. Para virar um agent que roda a cada 5 minutos, algo precisa chamá-la nesse intervalo. A trava global (ao lado do arquivo de configuração) garante uma tarefa por vez: enquanto uma tarefa está em andamento, a rodada que dispara termina na hora, sem iniciar outra.

Antes de agendar, crie o arquivo de configuração e preencha as listas `prioritarios` e `sem_prioridade` (veja a SKILL.md). Pedir `/execucao-recorrente` numa conversa sem o arquivo cria o modelo e pergunta os repositórios.

O prompt agendado é só:

```
/execucao-recorrente
```

com o arquivo no lugar padrão (`~/.claude/execucao-recorrente.toml`), ou, em outro lugar:

```
/execucao-recorrente --config D:\repos\execucao-recorrente.toml
```

Incluir, tirar ou mudar a prioridade de um repositório é só editar o arquivo: o agendamento não muda.

## Opções

| Opção | Roda onde | Precisa de sessão aberta | Intervalo mínimo | Quando usar |
|-------|-----------|--------------------------|------------------|-------------|
| **Tarefa agendada do Claude Desktop** | No seu computador | Não (o app precisa estar aberto e o computador ligado) | 1 minuto | Recomendada: acessa as pastas locais e tem permissões por tarefa |
| **`/loop` numa sessão do Claude Code** | No seu computador | Sim; tarefas recorrentes expiram em 7 dias | 1 minuto | Teste rápido ou um dia de trabalho |
| **`claude -p` + Agendador de Tarefas do Windows / cron** | No seu computador | Não | O do agendador | Controle total por linha de comando |
| Rotina na nuvem | Nuvem (clone novo do repositório) | Não | 1 hora | Não serve aqui: não vê as pastas locais nem roda a cada 5 minutos |

Fonte: documentação do Claude Code, "Run prompts on a schedule" (code.claude.com/docs/en/scheduled-tasks) e "Run Claude Code programmatically" (code.claude.com/docs/en/headless).

## 1. Tarefa agendada do Claude Desktop (recomendada)

1. Instale o plugin `delivery` no Claude Code / Claude Desktop (`/plugin install delivery@claude`).
2. No Claude Desktop, crie uma tarefa agendada com o prompt acima, intervalo de 5 minutos, e a pasta de trabalho num dos workspaces (ou numa pasta que contenha todos).
3. Libere para a tarefa as pastas dos workspaces **e** dos repositórios de código das stories: sem acesso a um repositório, a story falha com "repositório não encontrado".
4. Permissões: a rodada precisa ler e editar arquivos, rodar `uv`/`python`, `git` (status, switch, diff, e `commit` se `commit_ao_concluir = true`) e os comandos de build e teste das stacks (`dotnet`, `npx ng`, `npm`, `mvn`). Sem uma permissão, a story termina `falhou` com o motivo — confira o log nos primeiros dias.

## 2. `/loop` numa sessão aberta

```
/loop 5m /execucao-recorrente
```

Roda enquanto a sessão estiver aberta e ociosa; fechar o terminal para o loop. Tarefas recorrentes de sessão expiram em 7 dias. Bom para testar a configuração antes de agendar de verdade.

## 3. `claude -p` com o Agendador de Tarefas do Windows

Script `D:\repos\execucao-recorrente.cmd`:

```bat
@echo off
cd /d D:\repos
claude -p "/execucao-recorrente --config D:\repos\execucao-recorrente.toml" ^
  --permission-mode acceptEdits ^
  --permission-prompts none ^
  --allowedTools "Bash(uv *),Bash(python *),Bash(git status *),Bash(git branch *),Bash(git switch *),Bash(git diff *),Bash(dotnet *),Bash(npx *),Bash(npm *),Bash(mvn *)" ^
  >> D:\repos\execucao-recorrente.out.log 2>&1
```

Agendar a cada 5 minutos:

```bat
schtasks /create /tn "Execucao recorrente" /sc minute /mo 5 /tr "D:\repos\execucao-recorrente.cmd"
```

No Linux/macOS, uma linha no `crontab -e`: `*/5 * * * * cd ~/repos && claude -p "/execucao-recorrente --config ~/repos/execucao-recorrente.toml" --permission-mode acceptEdits --permission-prompts none --allowedTools "..." >> ~/repos/execucao-recorrente.out.log 2>&1`.

Notas:
- `-p` roda sem interface; uma skill vai no texto do prompt como `/nome-da-skill`.
- `--permission-prompts none` nega o que pediria aprovação em vez de esperar; o Claude é avisado e a story termina `falhou` com o motivo. Requer Claude Code v2.1.259 ou mais novo.
- `acceptEdits` libera a edição de arquivos; comandos de shell precisam estar em `--allowedTools` (sintaxe de regra de permissão: `Bash(git diff *)` libera tudo que começa com `git diff`). Inclua `Bash(git commit *)` só se usar `commit_ao_concluir = true`. Nunca libere `git push`.
- Não use `--bare`: ele não carrega os plugins instalados, e a skill vem do plugin `delivery`.
- Confira as opções da sua versão com `claude --help`.

## Custo

Cada disparo abre uma sessão do Claude, mesmo quando não há nada a fazer. A cada 5 minutos são 288 disparos por dia; uma rodada sem tarefas ou com a trava ativa termina logo e gasta pouco, mas não zero. Se as stories ficam prontas poucas vezes por dia, um intervalo de 15–30 minutos costuma bastar. Restrinja o horário do agendamento (ex.: dias úteis, horário comercial) se ninguém vai acompanhar os resultados fora dele.

## Acompanhar

- `scan` do `recorrente.py`: a fila na ordem de execução e o motivo de cada story pulada.
- `_sdd/execucao-recorrente/log/AAAA-MM.md` de cada workspace: uma linha por story executada, com resultado e motivo. Story pulada aparece uma vez por motivo, não a cada rodada; rodada sem tarefa ou com a trava ativa não escreve no log (veja o histórico do agendador).
- Stories em `blocked` no quadro (`sprint-planning`): o motivo está no Histórico e no Registro do desenvolvimento da story.
- `_sdd/execucao-recorrente/estado.json`: tentativas e histórico por story.
