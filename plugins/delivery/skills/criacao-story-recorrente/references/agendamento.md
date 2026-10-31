# Agendar a criação recorrente de stories

Funciona como a `execucao-recorrente` (detalhes das opções em `execucao-recorrente/references/agendamento.md`): a skill faz uma rodada e termina, e algo precisa chamá-la periodicamente. A trava ao lado do arquivo de configuração garante uma criação por vez.

Antes de agendar, crie o arquivo de configuração (`~/.claude/criacao-story-recorrente.toml`) e preencha `prioritarios` e `sem_prioridade`. Pedir `/criacao-story-recorrente` numa conversa sem o arquivo cria o modelo e pergunta os repositórios.

O prompt agendado é só:

```
/criacao-story-recorrente
```

ou, com o arquivo em outro lugar:

```
/criacao-story-recorrente --config D:\repos\criacao-story-recorrente.toml
```

## Intervalo

Criar uma story é mais lento que decidir que não há o que fazer, e o `max_prontas` (padrão 2 por projeto) limita quantas ficam esperando. Por isso a criação não precisa rodar tão seguido quanto a implementação: **a cada 15–30 minutos** costuma bastar. Uma rodada sem story a criar termina logo, mas cada disparo abre uma sessão e gasta um pouco.

## Opções

| Opção | Como |
|-------|------|
| **Tarefa agendada do Claude Desktop** (recomendada) | Prompt acima, intervalo de 15 minutos, pasta de trabalho num dos workspaces. Libere as pastas dos workspaces e, para o `create-story` ler o código e citar caminhos reais, as dos repositórios de código (só leitura) |
| **`/loop`** numa sessão aberta | `/loop 15m /criacao-story-recorrente` — para testar; expira em 7 dias |
| **`claude -p` + Agendador de Tarefas do Windows** | Script abaixo + `schtasks /create /tn "Criacao de stories" /sc minute /mo 15 /tr "D:\repos\criacao-story-recorrente.cmd"` |

Script `D:\repos\criacao-story-recorrente.cmd`:

```bat
@echo off
cd /d D:\repos
claude -p "/criacao-story-recorrente --config D:\repos\criacao-story-recorrente.toml" ^
  --permission-mode acceptEdits ^
  --permission-prompts none ^
  --allowedTools "Bash(uv *),Bash(python *)" ^
  >> D:\repos\criacao-story-recorrente.out.log 2>&1
```

Permissões menores que as da execução: a criação só lê e escreve arquivos de documentação e roda os scripts (`uv`/`python`). Não precisa de `git` nem de build e testes. Sem uma permissão, a story termina `falhou` com o motivo no log.

## Junto com a execucao-recorrente

As duas se completam: a criação mantém até `max_prontas` stories em `ready-for-dev` por projeto; a execução as implementa e as leva a `review`, o que libera a criação da próxima (dependências em `review` ou `done`).

| Arranjo | Como | Efeito |
|---------|------|--------|
| **Independentes** (padrão) | Cada skill com o seu arquivo de configuração | Cada uma com a sua trava: criação e implementação podem rodar ao mesmo tempo. As listas podem ser diferentes (ex.: criar stories de um projeto que ainda não vai ser implementado sozinho) |
| **Uma tarefa por vez no total** | As duas com o mesmo `--config` | Mesmas listas e a mesma trava: enquanto uma cria, a outra não implementa, e vice-versa |

Rodando ao mesmo tempo, as duas atualizam o `sprint-status.yaml` do projeto (via `status.py`), cada uma numa story diferente. As gravações são rápidas; se preferir eliminar qualquer chance de uma sobrescrever a outra, use o mesmo arquivo de configuração.

## Acompanhar

- `scan` do `story_recorrente.py`: a fila, quantas stories prontas cada projeto tem e o motivo de cada story pulada.
- `_sdd/criacao-story-recorrente/log/AAAA-MM.md` de cada workspace: uma linha por rodada com resultado e motivo.
- Stories em `blocked` no quadro (`sprint-planning`): o motivo está no Histórico da story, ou só no log quando a criação parou antes de escrever o arquivo.
