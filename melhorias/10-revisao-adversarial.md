# 10 — Revisão adversarial

- **Pedido:** "Verificação e fechamento quero seguir revisão adversarial" (linha 10)
- **Tamanho:** M
- **Depende de:** 06, 08, 09
- **Situação:** [ ] a fazer

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
