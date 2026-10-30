# 09 — Implementação: uma sessão nova por story, spec como única fonte

- **Pedido:** "Implementação quero seguir Uma sessão nova por story, com a spec como única fonte de verdade" (linha 9)
- **Tamanho:** G
- **Depende de:** 06, 08 (e 13 para vários repositórios)
- **Situação:** [ ] a fazer

## Contexto

### Como o BMAD faz
- v6: `dev-story` roda **em contexto limpo** (chat novo), lê só o story file, implementa tarefa por tarefa (testes primeiro), marca `[x]` só com testes passando, preenche Dev Agent Record e File List, roda a suíte inteira e move a story para `review`. Recomenda-se rodar o `code-review` em outra sessão (de preferência outro modelo).
- v7: `bmad-build` uma vez por story; `bmad-build-auto` para rodar sem supervisão, uma story por execução; o build termina em `built` e a revisão/triagem já vem embutida.

### Como está hoje
- As skills de código (`architecture-entities`, `-feature`, `-repository`, `-controller`, `angular-*`) geram peças isoladas; nada orquestra a implementação de uma tarefa nem registra o que foi feito.

## Objetivo

Skill `dev-story` que implementa **uma** story a partir do story file, numa sessão limpa, usando as skills de código, e deixa o registro para a revisão.

## Proposta

1. **Skill `dev-story`**. Entrada: caminho ou ID da story (sem ID: a primeira `ready-for-dev`, ou a `in-progress` existente para retomar).
2. **Sessão nova**:
   - A skill **não consegue** limpar o contexto sozinha. Ela orienta: ao final de `create-story` (08) e de `code-review` (10), mostrar o comando para a próxima sessão — `/clear` e depois `dev-story 1-2`, ou abrir uma sessão nova no repositório certo (`claude --add-dir <workspace>`).
   - Ao iniciar, se detectar que já trabalhou em outra story nesta sessão (conversa com outro story file aberto), avisa e recomenda `/clear` antes de seguir.
3. **Spec como única fonte de verdade**:
   - Lê **apenas** o story file e os arquivos de código. Não abre escopo, spec funcional, arquitetura, a não ser por referência explícita do story file (caminho#seção).
   - Se o story file estiver incompleto, ambíguo ou contradizer o código: **para**, registra a dúvida em "Registro do desenvolvimento" e sugere `correct-course` (12) ou ajuste do story file — não inventa requisito.
4. **Execução**:
   1. Pré-condições: status `ready-for-dev` ou `in-progress`; repositórios clonados; branch da story (13) — cria só com confirmação.
   2. Muda para `in-progress`.
   3. Para cada tarefa, na ordem: teste que falha → implementação (usando a skill de código indicada no story file) → teste passa → marca `[x]`. Respeita checkpoints marcados no épico (pausa para o humano).
   4. Roda build + suíte completa (comandos por stack, customizáveis — 04).
   5. Preenche "Registro do desenvolvimento" (decisões, desvios, pendências) e "Arquivos alterados" por repositório.
   6. Todos os critérios atendidos e testes verdes → `review`. Caso contrário, fica `in-progress` com o motivo.
   7. Nunca faz commit/push sem pedido; ao final oferece a mensagem de commit pronta.
5. **Retomada**: story `in-progress` é retomada pelas tarefas ainda `[ ]` e pelo registro.
6. **Modo sem supervisão** (opcional, `delivery.auto_mode`, 02): só para stories sem checkpoint; ainda para em ambiguidade.

## Decisões em aberto

- Onde abrir a sessão: no workspace com `--add-dir` dos repositórios, ou no repositório com `--add-dir` do workspace. Recomendação: no repositório (valem o `CLAUDE.md` e as configs dele), lendo o story file pelo caminho absoluto. fazer o recomendado
- TDD obrigatório ou recomendado (configurável). recomendado
- Rodar `code-review` automaticamente ao final (em subagente, contexto separado) ou sempre em sessão nova pelo usuário. Recomendação: sugerir sessão nova; opção de subagente via customização.fzer o recomendado, verificar se é possivel abrir uma nova sessão usando script

## Critérios de aceite

- [ ] Skill com fluxo acima, `references/` com regras de "fonte única" e comandos por stack (.NET, Angular, Java).
- [ ] Teste num repositório de exemplo: story do 08 implementada, tarefas marcadas, registro preenchido, status `review`.
- [ ] Story ambígua faz a skill parar com a dúvida registrada (teste com story propositalmente incompleta).
- [ ] Nenhum commit/push feito pela skill.

## Arquivos impactados

`plugins/<delivery>/skills/dev-story/**` (novo); `plan-execution/references/skill-mapping.md` (reaproveitar o mapeamento tarefa → skill de código); `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.
