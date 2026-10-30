---
name: retrospective
description: Retrospectiva de um épico com base em evidências — inventário das stories (estados, rodadas de revisão, achados, correções, desvios, pendências), checagem do "Pronto quando", seguimento dos itens da retrospectiva anterior, reconciliação com especificação e arquitetura, preparação do próximo épico, veredito (accepted, accepted-with-open-items, rejected) e itens de ação; grava docs/{projeto}/implementacao/retrospectivas/epic-{n}-{data}.md e, com confirmação, fecha o épico. Opcional. Use quando o usuário disser "retrospectiva", "retro do épico", "fechar o épico", "encerrar o épico", "lições do épico", "o que aprendemos". NÃO use para ver o quadro (use sprint-planning), revisar uma story (use story-review) ou mudar o plano no meio do épico (use correct-course).
metadata:
  version: 1.0.0
  category: implementation
  depends-on: story-review
  output: docs/{projeto}/implementacao/retrospectivas/epic-{n}-{data}.md
---

# Retrospective

Fecha um épico olhando para o que aconteceu, **a partir de evidências** — os arquivos das stories, os blocos de revisão, as mudanças de rumo e, se disponível, o histórico do git. Não inventa achado. É **opcional**: um épico pode ser fechado sem retrospectiva. Inspirado no `retrospective` do BMAD v6 e no `bmad-retrospective` da v7 (veredito e evidências).

Leia antes de executar: `references/template-retrospectiva.md` (documento e critérios do veredito).

---

## Passo 0 — Identificar o projeto

A raiz de trabalho é uma pasta de documentação com vários projetos, cada um em `docs/{projeto}/`.

1. Se o usuário citou o projeto, use a pasta dele.
2. Senão, leia `docs/workspace.md`: com um único projeto, use-o e avise; com vários, liste e pergunte qual.
3. Sem `docs/workspace.md`, procure `docs/*/project.md`.
4. Se o projeto não existir, ofereça iniciá-lo com `discovery-init`.
5. Leia `docs/{projeto}/project-config.json` (nome, stack, repositório; ver o schema em `discovery-init/references/project-config-schema.md`). Se não existir, use o `project.md` e ofereça criar o config a partir dele.
6. Leia a configuração do workspace, se existir: `_sdd/config.toml` e `_sdd/config.user.toml` na raiz (o pessoal vence; chaves em `sdd-setup/references/config-schema.md`). Converse em `language.conversation`, escreva os documentos em `language.documents`, chame o usuário por `user.name` e ajuste as explicações a `user.skill_level`; se `paths.docs_root` não for `docs`, use-o no lugar de `docs/` em todos os caminhos. Sem `_sdd/`, use os padrões (pt-BR, nível intermediário, `docs/`) e sugira uma vez rodar o `sdd-setup`, sem bloquear.

`{projeto}` é a pasta escolhida; todos os caminhos abaixo são relativos à raiz de trabalho.

## Scripts

```
uv run _sdd/scripts/retro.py  --project docs/{projeto} evidence epic-{n} [--repo {nome}={caminho} ...] [--base main]
uv run _sdd/scripts/status.py --project docs/{projeto} set epic-{n}-retrospective done
uv run _sdd/scripts/status.py --project docs/{projeto} set epic-{n} done
```

Sem `uv`: `python` 3.11+ com `pyyaml`; sem nenhum, monte o inventário lendo o `sprint-status.yaml` e cada arquivo de story (seções Tarefas, Registro do desenvolvimento e Revisão).

---

## Fluxo

### Passo 1 — Escolher o épico

Com o épico citado, use-o. Sem: `status.py next` (ação `retrospective` ou `close-epic`) ou pergunte. Rode `retro.py evidence`. Se `all_finished` for `false`, mostre as `open_stories` e pergunte se segue mesmo assim (o veredito tende a `rejected`) ou se prefere terminar as stories antes.

### Passo 2 — Histórico do git (opcional)

Pergunte se quer incluir o histórico do git. Com o sim, use os caminhos locais dos repositórios (`project-config.json` ou `repositorios.md`) e rode `evidence` de novo com `--repo` (e `--base`, se a branch principal não for `main`). Repositório que não está nesta máquina: siga sem ele e registre em "Fontes não lidas". Para entender um ponto específico, leia `git log --oneline {base}..feat/{id}` daquela story.

### Passo 3 — Ler as evidências

A partir do inventário, leia o que importa (não tudo):
- o arquivo do épico (Objetivo, **Pronto quando**, Pontos em aberto);
- nas stories com sinais (`review_rounds` > 1, achados `high`/`medium`, `desvios`, `pendencias`, `fix_tasks.open` > 0, `checkpoint`), as seções Registro do desenvolvimento e Revisão;
- as propostas de mudança listadas em `course_changes`;
- a retrospectiva anterior (`previous_retrospective`): os itens de ação e se foram feitos, procurando a evidência nas stories deste épico.

### Passo 4 — Conversa com o time (opcional)

Pergunte se quer acrescentar percepções do time (o que foi bom, o que atrapalhou). Elas entram nos achados com a fonte "conversa em {data} — {quem}". Não substitua evidência por opinião: percepção que contradiz o registro aparece como tal.

### Passo 5 — Escrever

Monte o documento pelo template: Evidências, Pronto quando (item a item, com evidência), O que funcionou / não funcionou / Surpresas (cada um com fonte), Itens da retrospectiva anterior, Reconciliação, Preparação do próximo épico, **Veredito** (pelos critérios do template) e Itens de ação. Mostre um resumo e o veredito antes de gravar; com a confirmação, grave `implementacao/retrospectivas/epic-{n}-{AAAA-MM-DD}.md` (nunca sobrescreva uma retrospectiva existente: outra no mesmo dia ganha sufixo `-2`).

### Passo 6 — Encaminhar, com confirmação de cada um

- **Reconciliações aprovadas:** encaminhe à skill dona — `spec-functional` (atualizar a spec, sem renumerar), `arch-c4` (arquitetura) ou `arch-adr` (decisão). Não edite esses documentos por fora.
- **Itens de ação "story nova":** acrescente a story no épico seguinte (ou no atual, se ele continuar aberto) pelo `plan-epics` (modo Atualizar) e rode `status.py sync`.
- **Ajustes em stories do backlog:** `plan-epics` (Atualizar); se a story já está em `ready-for-dev` ou além, `correct-course`.
- **Itens de processo:** ficam só na retrospectiva (a próxima confere).

### Passo 7 — Fechar

1. `status.py set epic-{n}-retrospective done`.
2. Pergunte se o épico pode ser fechado. Com o sim e todas as stories `done`/`dropped`: `status.py set epic-{n} done`. Veredito `rejected`: não feche sem o usuário pedir explicitamente; registre o motivo na retrospectiva.
3. Atualize a Situação do projeto no `docs/workspace.md` com o `situacao` de `status.py show`; se todos os épicos estiverem `done`, marque a fase correspondente no `project.md`.
4. Próximo passo: `status.py next` (normalmente `create-story` do próximo épico).

---

## Regras importantes

- Evidência, não opinião: todo achado cita a fonte; percepção do time é registrada como tal.
- A skill grava só a retrospectiva (e, via script, o estado). Spec, arquitetura, ADRs e épicos mudam pelas skills donas, com aprovação.
- O épico só vai para `done` com a confirmação do usuário.
- Nada é alterado nos repositórios de código; o git é só lido, e só se o usuário quiser.

## Troubleshooting

**Stories sem Registro ou sem Revisão** (feitas fora do fluxo) — registre como "sem evidência" no inventário; o veredito não pode ser `accepted` para um "Pronto quando" sem evidência.

**Épico fechado sem retrospectiva e o usuário quer fazer depois** — pode: a skill roda com o épico em `done`; no Passo 7 só marca a retrospectiva.

**Muitas rodadas de revisão no épico** — é o principal sinal de story mal fatiada ou critério ambíguo: traga como achado e como item de ação para o `plan-epics`.
