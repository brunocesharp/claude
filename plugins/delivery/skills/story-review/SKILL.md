---
name: story-review
description: Revisão adversarial da implementação de uma story contra o arquivo dela (docs/{projeto}/implementacao/stories/{id}.md) — lentes em paralelo (aderência aos critérios de aceite, integridade do registro, correção e casos de borda, segurança, testes, arquitetura, contratos entre repositórios), triagem de cada achado (verificar, severidade, descartar com motivo, encaminhar para corrigir, adiar ou decisão), bloco datado na seção Revisão da story e decisão do estado (review → done ou de volta a in-progress). Use quando o usuário disser "story-review", "revisar a story", "revisão da story", "code review da story", "revisar a implementação", "a story está pronta?". NÃO use para revisar um diff ou PR sem story (use o /code-review do Claude Code), implementar as correções (use dev-story) ou mudar o que a story promete (use correct-course).
metadata:
  version: 1.0.0
  category: implementation
  depends-on: dev-story
  output: seção Revisão (e correções R{n} em Tarefas) do arquivo da story; sprint-status.yaml
---

# Story Review

Revisa uma story em `review` **contra o arquivo da story**, de forma adversarial: parte do princípio de que há defeitos e procura ativamente — sem inventar achado. Inspirado no `code-review` do BMAD v6 (adversarial) e no `bmad-code-review` da v7 (lentes em paralelo e triagem). Não altera código sem confirmação e não faz commit.

Leia antes de executar:
- `references/lentes.md` — o que cada lente procura e o formato de retorno.
- `references/triagem.md` — verificar, severidade, descartar, encaminhar e o resultado.
- `references/template-revisao.md` — o bloco que vai para a story.
- `../dev-story/references/comandos-por-stack.md` — como rodar build e testes.

---

## Passo 0 — Localizar a story e o workspace

Igual ao `dev-story`: id ou caminho da story; `{P}` = `docs/{projeto}`, `{workspace}` = a pasta com `docs/` e `_sdd/` (procure no diretório atual, nos pais e nos diretórios adicionados à sessão). Leia `{workspace}/_sdd/config.toml` e `config.user.toml`: `language.*`, `user.*`, `delivery.review_depth` (`completa`). Sem id: `status.py next` com ação `story-review`.

## Customização (por projeto)

Depois de identificar o projeto, resolva a customização desta skill:

```
uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto}
```

Sem o script (ou sem `uv`/`python`): leia `${CLAUDE_SKILL_DIR}/customize.toml` e, se existir, `docs/{projeto}/_custom/story-review.toml`, e mescle pelas regras de `sdd-setup/references/customizacao.md`. Sem override, valem os padrões da skill.

1. Execute os `workflow.activation_steps_prepend`, na ordem.
2. Leia os arquivos de `facts` (e os textos literais): são fatos válidos durante toda a skill e vencem os padrões dela quando conflitarem.
3. Use os valores de `resolved.workflow` onde esta skill os cita: `lenses` (só as `enabled = true`; lente nova roda como as demais, com o `focus` dela e a Postura de `lentes.md`) e `block_on` (severidades que impedem o `done`).
4. Ao terminar, execute os `workflow.activation_steps_append` e o `workflow.on_complete`.

Mostre os `warnings` ao usuário uma vez (ex.: chave que não é customizável, override que repete a base).

## Scripts

A partir de `{workspace}`:

```
uv run _sdd/scripts/story.py   --project {P} check {id}
uv run _sdd/scripts/review.py  --project {P} integrity {id} --repo {nome}={caminho} [--repo ...] [--base main]
uv run _sdd/scripts/review.py  --project {P} diff {id} --repo {nome}={caminho} [...] --out {arquivo}
uv run _sdd/scripts/status.py  --project {P} set {id} done | in-progress
```

`{arquivo}` do diff: na pasta temporária da sessão (scratchpad), nunca no workspace nem no repositório. Sem `uv`: `python` 3.11+ com `pyyaml`; sem nenhum, faça a lente 2 com `git diff --name-status {base}...HEAD` e `git status --porcelain` à mão.

---

## Passo 1 — Sessão separada

A revisão não pode rodar na mesma conversa em que a story foi implementada (o revisor herdaria as justificativas do autor). Se esta conversa tem o `dev-story` da mesma story: ofereça abrir uma janela nova (`session.py --prompt "story-review {id}"`, `--launch` só com confirmação), `/clear`, ou rodar a revisão inteira num subagente com contexto separado.

## Passo 2 — Preparar

1. Leia a story inteira. Ela precisa estar em `review` (outra situação: diga qual e pare; `in-progress` com o usuário insistindo: revise, mas avise que o resultado não muda o estado).
2. `story.py check {id}` — `problems` viram achados da lente 1.
3. Repositórios da seção Repositórios, com o caminho local. Para cada um, a branch da story precisa existir.
4. `review.py diff` (um arquivo para todas as lentes) e `review.py integrity` (lente 2).
5. Profundidade: `delivery.review_depth` = `completa` (padrão) ou `rapida`; o usuário pode pedir a outra nesta rodada.

## Passo 3 — Lentes

**Completa:** dispare **em paralelo** um subagente por lente — 1 Aderência, 3 Correção, 4 Segurança, 5 Testes, 6 Arquitetura e, se houver mais de um repositório ou contratos na story, 7 Contratos. Cada subagente recebe só: o caminho do arquivo da story, o caminho do diff, os caminhos locais dos repositórios, o texto da sua lente em `references/lentes.md` (incluindo a Postura) e o formato de retorno. Não passe a conversa nem a sua opinião sobre a story.

**Rápida:** um revisor (você ou um subagente) cobre as lentes 1, 3 e 5, com a mesma Postura.

A lente 5 **roda a suíte** de cada repositório. A lente 2 é o resultado do `integrity`.

## Passo 4 — Triagem

Junte os retornos e siga `references/triagem.md` para cada achado: verificar no código → severidade → descartar com motivo → encaminhar (**corrigir**, **adiar**, **decisão**). Problema causado pela story nunca é adiado. Decida o **resultado**: aprovada, correções ou decisão pendente.

## Passo 5 — Registrar na story

Acrescente o bloco em `## Revisão` pelo `references/template-revisao.md` (rodada `n` = blocos anteriores + 1), com achados, descartados e o "verificado sem achados" de cada lente. Para cada achado **corrigir**, acrescente a tarefa `R{n}` em `### Correções da revisão {n}` no fim de `## Tarefas`.

## Passo 6 — Decidir com o usuário

Mostre o resumo (achados por severidade, encaminhamento, resultado) e:

- **Aprovada:** proponha `status.py set {id} done`. Com o sim: transição, linha no Histórico (`review → done`, `story-review`) e Situação do `workspace.md` com o `situacao` do `show`.
- **Correções:** ofereça duas saídas:
  1. **Devolver ao dev** (padrão): `status.py set {id} in-progress`, linha no Histórico; o `dev-story {id}` retoma pelas tarefas `R{n}` abertas, numa sessão nova.
  2. **Aplicar agora** (só correções pequenas e claras, com confirmação explícita): aplique, rode os testes do alvo e a suíte, marque os `R{n}`, registre "Aplicado nesta rodada" no bloco e atualize "Arquivos alterados". A story fica em `review`; ofereça uma nova rodada rápida antes do `done`.
- **Decisão pendente:** mostre as opções com a recomendação. Decidido: se cabe no que a story promete, vira `R{n}` (siga como Correções); se muda o prometido, sugira `correct-course`.
- **Adiados:** para cada um, pergunte se vira story nova. Com o sim: acrescente-a no arquivo do épico (próximo `m` livre, `kind: story` ou `enabler`, sem mudar ids existentes) e rode `status.py sync` (entra em `backlog`). Registre o id no bloco.

## Passo 7 — Próximo passo

Use `status.py next`: próxima story (`create-story`), retomar correções (`dev-story`) ou, com o épico todo finalizado, a retrospectiva (opcional) e o fechamento do épico.

---

## Vários repositórios

O `review.py diff` e o `integrity` recebem um `--repo` por repositório da story. A lente 7 (Contratos) roda sempre que a story tiver mais de um repositório ou contrato: provedor e consumidor batem, estratégia aplicada para incompatíveis, ordem de merge e deploy registrada em `implementacao/multi-repo/{id}.md`. A suíte é rodada em cada repositório. A story não vai para `done` com contrato quebrado entre os repositórios.

## Regras importantes

- Adversarial, não inventiva: todo achado tem local e consequência verificados; lente sem achados registra o que checou.
- A revisão descreve; só altera código com confirmação explícita. Nunca commit, push ou merge.
- Testes são rodados na revisão, não lidos do Registro.
- Nada vai para `done` sem a confirmação do usuário e sem `high`/`medium` em aberto.
- O bloco de revisão é histórico: nunca apague rodadas anteriores.

## Troubleshooting

**Suíte não roda localmente** (depende de serviço externo) — registre na lente 5 o que não foi executado e por quê; o resultado não pode ser "aprovada" se um CA só é verificado por esse teste, a menos que o usuário aceite explicitamente (registre).

**Diff enorme** — a story provavelmente era grande demais; revise mesmo assim por lente e registre para a retrospectiva.

**Terceira rodada com achados não triviais** — pare e procure a causa com o usuário (critério ambíguo, padrão faltando, story mal fatiada) antes de outra rodada.
