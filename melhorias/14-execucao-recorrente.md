# 14 — Execução recorrente das stories, sem supervisão

- **Pedido:** "Executar as tarefas dos projetos construídos com as skills deste repositório", de forma recorrente (ex.: a cada 5 minutos) e sem ninguém acompanhando (linha 14)
- **Tamanho:** M
- **Depende de:** 06 (sprint-status), 08 (story file), 09 (dev-story); usa 04 (customização) e 13 (vários repositórios)
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Ponto de partida: o protótipo `agente-tarefas`
Fila genérica de tarefas em arquivos `.md` (pastas `pendentes/`, `em-andamento/`, `concluidas/`, `falhas/`), processada por uma tarefa agendada a cada 5 minutos com as instruções do `AGENTE.md`:
- trava em `lock.txt`, com validade, e uma tarefa por execução;
- prioridade no frontmatter da tarefa e "Critério de pronto" conferido antes de declarar sucesso;
- proibido apagar, enviar mensagens, publicar, pagar, mexer em credenciais ou fazer deploy; o que exigir isso falha com "requer aprovação humana";
- o texto da tarefa é só descrição do trabalho, nunca muda as regras (proteção contra instruções embutidas);
- seção `## Execução` no fim da tarefa, `tentativas` com limite, log mensal em tabela.

### O que faltava
O protótipo não conhece o fluxo SDD: a tarefa é um texto livre, sem a story como fonte única, sem estados do `sprint-status.yaml`, sem dependências, checkpoints ou vários repositórios. E os caminhos estavam fixos numa pasta da máquina.

## Objetivo

Uma skill do plugin `delivery` que transforma o quadro de stories num agent: a cada rodada, escolhe a próxima story executável dos projetos configurados e a entrega ao `dev-story` em contexto limpo, registrando o motivo de tudo o que não conseguir fazer.

## Proposta

- **Fonte das tarefas:** só o `sprint-status.yaml` dos projetos (stories `ready-for-dev`; opcionalmente `review` e `backlog`). Projeto sem quadro fica fora.
- **Configuração fora do plugin** (`~/.claude/execucao-recorrente.toml`): listas `prioritarios` e `sem_prioridade` de workspaces ou pastas de projeto.
- **Ordem:** retomar a story que a própria execução deixou `in-progress` → prioritários → sem prioridade.
- **Fora da fila:** `in-progress` de outra pessoa, `checkpoint: true`, dependências abertas, limite de tentativas, projeto desligado.
- **Trava global** ao lado do arquivo de configuração; estado e log por workspace em `_sdd/execucao-recorrente/`.
- **Resultado:** `concluida`, `bloqueada` (precisa de pessoa → `blocked`) ou `falhou` (erro técnico, retomada na próxima rodada; no limite → `blocked`). Motivo obrigatório e acionável.
- **Regras do protótipo mantidas:** nada destrutivo, nunca push/merge, commit só com `commit_ao_concluir`, nunca inventar decisão.

## Decisões

- Fila genérica de `.md` (protótipo) ou stories do quadro. **Só stories com `sprint-status.yaml`.**
- Story `pulada` (ex.: "aguardando commit") a cada rodada enche o log (até 288 linhas/dia a cada 5 min). **Registrar só quando o motivo muda.**
- Com `commit_ao_concluir = false` (padrão), um repositório fica com uma story por vez até alguém fazer o commit. **Aceito.**
- Onde agendar: tarefa agendada do Claude Desktop (recomendada), `/loop` para teste ou `claude -p` com o Agendador de Tarefas. Rotina na nuvem não serve (não vê as pastas locais, intervalo mínimo de 1 hora).

## Critérios de aceite

- [x] Uma tarefa por vez, com trava que expira se a rodada morrer.
- [x] Retomada antes de tarefa nova; prioritários antes dos sem prioridade.
- [x] Stories de outra pessoa, com checkpoint ou dependência aberta nunca são pegas.
- [x] Falha registrada na story, no estado e no log; limite de tentativas leva a `blocked`.
- [x] `pulada` não repete no log enquanto o motivo é o mesmo.
- [x] Projeto sem `sprint-status.yaml` fica fora da fila, com nota.
- [ ] Primeiro uso real agendado num workspace com stories prontas.

## Arquivos impactados

`plugins/delivery/skills/execucao-recorrente/` (`SKILL.md`, `customize.toml`, `references/agendamento.md`, `scripts/recorrente.py`, `scripts/tests/test_recorrente.py`); `plugins/delivery/.claude-plugin/plugin.json` e `plugins/sdd/skills/sdd-setup/modules/delivery.toml` (1.1.0); `.claude-plugin/marketplace.json`; `sdd-setup/references/customizacao.md` e `test_customize.py`; `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.

## Resultado (30/10/2026)

**Skill `execucao-recorrente`** no plugin `delivery` (versão 1.1.0): Passo 0 monta a fila (`recorrente.py scan`), Passo 1 trava, Passo 2 confere as pré-condições sem perguntar (story incompleta, repositório ausente ou sujo, branch `feat/{id}`), Passo 3 roda a ação num subagente em modo não supervisionado, Passo 4 registra o resultado conferindo os arquivos, Passo 5 libera a trava e responde em uma linha.

**`recorrente.py`:** `init-config`, `config`, `scan`, `lock adquirir|liberar` e `registrar`. Estado em `estado.json` (tentativas por story e ação, histórico das últimas 20, motivo atual de `pulada`) e log mensal em tabela.

**Customização por projeto:** `habilitado`, `acoes` (`dev-story`, `story-review`, `create-story`), `max_tentativas` (3) e `commit_ao_concluir` (false).

**Decisões aplicadas:** só projetos com `sprint-status.yaml` (o `scan` ignora os outros com nota, em vez de quebrar numa pasta de projeto sem quadro); `pulada` vai para o log só quando o motivo muda (`registrar` devolve `repetida: true`), e volta a ser registrada depois que a story é executada.

**Testes:** 15 em `test_recorrente.py` (ordem de prioridade, trava, retomada, story de outra pessoa, limite de tentativas, `pulada` sem repetição, override do projeto, projeto sem quadro, configuração); 94 no total do repositório.

**Protótipo:** a pasta `14 - skill execucao recorrente/agente-tarefas` fica como referência do ponto de partida; as regras dela estão incorporadas à skill.
