# 10 — Revisão adversarial

- **Pedido:** "Verificação e fechamento quero seguir revisão adversarial" (linha 10)
- **Tamanho:** M
- **Depende de:** 06, 08, 09
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Como o BMAD faz
- v6 (`code-review`): revisão **adversarial** — o revisor parte do princípio de que há problemas e precisa encontrar achados concretos (não aceita "parece bom"). Confere: cada critério de aceite implementado; cada tarefa marcada `[x]` realmente feita; File List × `git diff` real; qualidade, segurança, testes. Recomenda rodar em sessão nova, de preferência com outro modelo. Resultado: corrige ou cria itens de acompanhamento na story; status vai para `done` ou volta para `in-progress`.
- v7 (`bmad-code-review`): várias camadas/lentes revisam o mesmo diff em paralelo (`quick` = 1 revisor, `thorough` = várias lentes). **Triagem**: verificar a consequência no código → severidade (`low`/`medium`/`high`) → descartar ruído com motivo → encaminhar como **patch** (uma correção clara), **defer** (problema real anterior à mudança; problemas causados pela mudança nunca são adiados) ou **decision needed** (mais de uma correção razoável; lista opções e recomenda). Anexa bloco datado `## Code Review` ao plano. Não muda status.

### Como está hoje
- Não existe skill de revisão no marketplace (só o `/code-review` do próprio Claude Code, sem vínculo com a story).

## Objetivo

Skill `code-review` (nome a definir para não confundir com o comando do Claude Code) que revisa a implementação **contra o story file**, de forma adversarial, com triagem, e decide o próximo estado.

## Proposta

1. **Entrada**: ID da story em `review` (sem ID: a primeira em `review`). Lê o story file, o diff de cada repositório (branch da story × branch principal) e a lista de arquivos alterados.
2. **Postura adversarial** (regras explícitas no SKILL.md):
   - Assumir que há defeitos; procurar ativamente. Mínimo configurável de achados verificados por lente — se não achar, justificar por lente o que foi checado (sem "LGTM" vazio).
   - Rodar em **sessão nova** (ou subagente), nunca na mesma conversa do `dev-story`.
3. **Lentes** (em paralelo via subagentes no modo completo; uma só no rápido — `delivery.review_depth`, 02; customizáveis, 04):
   - Aderência à story: cada critério de aceite e cada tarefa `[x]` com evidência no código/teste.
   - Integridade do registro: arquivos alterados × diff real (arquivo não declarado ou declarado e não alterado).
   - Correção e casos de borda; segurança; testes (cobrem os critérios? passam?); arquitetura (ADRs, camadas, padrões das skills `architecture-*`).
   - Contratos entre repositórios (13).
4. **Triagem** (da v7): verificar → severidade → descartar com motivo → **corrigir** / **adiar** (só pré-existente) / **decisão necessária**.
5. **Saída**: bloco datado em "Revisão" no story file (achados, severidade, encaminhamento, o que foi descartado e por quê). Opcional: arquivo `implementacao/revisoes/{story}-{data}.md` se ficar grande.
6. **Estado**:
   - Sem achados `medium`/`high` abertos e sem decisão pendente → `done`.
   - Com correções → oferece aplicar (com confirmação) e volta para `in-progress`, ou fica em `review` aguardando decisão.
   - Itens adiados viram stories novas em `backlog` (com confirmação) ou itens no épico.
7. Ao final, mostra o próximo passo: próxima story (`create-story`) ou retrospectiva se o épico acabou.

## Decisões em aberto

- Nome da skill (`story-review`? `review-story`?) — evitar conflito com `/code-review`. `story-review`
- A revisão aplica as correções ou só as descreve. Recomendação: descreve; aplica só com confirmação. recomendado
- Usar outro modelo para revisar (subagente com `model` diferente) como padrão. Nao

## Critérios de aceite

- [ ] Skill com `references/` de lentes, triagem e template do bloco de revisão.
- [ ] Teste com story implementada contendo um defeito plantado, uma tarefa marcada sem implementação e um arquivo fora da lista: os três aparecem como achados.
- [ ] Transições `review → done` / `review → in-progress` via `status.py`.

## Arquivos impactados

`plugins/<delivery>/skills/<nome>/**` (novo), `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.

## Resultado (30/10/2026)

**Skill `story-review`** (plugin `delivery`). Etapas:
1. Sessão separada da implementação: janela nova, `/clear` ou subagente.
2. Preparar: `story.py check`, diff e integridade.
3. Lentes.
4. Triagem.
5. Registrar na story.
6. Decidir com o usuário.
7. Próximo passo.

**Lentes** (`references/lentes.md`):
1. Aderência aos critérios e às tarefas `[x]`.
2. Integridade do registro, feita por script.
3. Correção e casos de borda.
4. Segurança.
5. Testes. A revisão **roda** a suíte, em vez de confiar no registro.
6. Arquitetura e padrões.
7. Contratos, quando há vários repositórios.

No modo completo, cada lente roda num subagente, em paralelo, que recebe só a story, o diff e a lente. No modo rápido, um revisor cobre as lentes 1, 3 e 5.

**Triagem** (`references/triagem.md`, do BMAD v7):
- Verificar no código, dar severidade `high`/`medium`/`low` e descartar com motivo.
- Encaminhar para corrigir (tarefa `R{n}`), adiar (só problema pré-existente; vira story nova via `sync`) ou decisão.
- Resultado: aprovada, correções ou decisão pendente.

**Script `review.py`:**
- `diff` grava num arquivo o diff de todos os repositórios: commits desde a base, alterações não commitadas e arquivos novos não rastreados.
- `integrity` compara "Arquivos alterados" com o git: arquivos não declarados, declarados sem mudança, alterações não commitadas e branch.
- A base é detectada pelo `origin/HEAD` ou por `main`/`master`/`develop`.

**Pergunta do setup:** `delivery.review_depth` (completa).

**Desvio do plano: sem "mínimo de achados".** Em vez de uma cota (o BMAD v6 pede de 3 a 10), cada lente que não acha nada registra o que verificou. Uma cota incentiva achado inventado, e achado inventado é descartado na triagem e desacredita a revisão.

**Decisões aplicadas:**
- Nome `story-review`.
- A revisão descreve e só aplica com confirmação. "Aplicar agora" é opcional e vale só para correções pequenas; o padrão é devolver ao `dev-story`.
- Sem troca de modelo por padrão.

**Critérios de aceite:**
- Skill com lentes, triagem e template: feita.
- O teste com um defeito plantado é coberto pelo script: o arquivo fora da lista e o arquivo declarado sem mudança aparecem (50 testes).
- O defeito de lógica plantado e a tarefa marcada sem implementação dependem das lentes, ou seja, do modelo. Fazer no primeiro uso.
- As transições de estado usam o `status.py`.
