---
name: sdd-customize
description: Customiza uma skill para um projeto do workspace sem editar o plugin — mostra os campos customizáveis (customize.toml da skill), pergunta o que mudar, grava um override esparso em docs/{projeto}/_custom/{skill}.toml e mostra o resultado resolvido. Skills customizáveis: spec-functional, plan-epics, sprint-planning, create-story, dev-story, story-review, retrospective, correct-course. Use quando o usuário disser "customizar a skill", "personalizar a skill", "mudar o padrão da skill", "configurar a revisão do projeto", "desligar uma lente", "acrescentar uma lente", "comandos de teste do projeto", "Definição de Pronto do projeto", "padrões do time na skill", "fatos fixos", "o que dá para customizar". NÃO use para a configuração do workspace (idioma, nome, nível — use sdd-setup) nem para mudar a skill para todo mundo (isso é mudança no plugin).
metadata:
  version: 1.0.0
  category: workspace
  output: docs/{projeto}/_custom/{skill}.toml
---

# SDD Customize

Grava e confere a customização de uma skill **para um projeto**. Leia antes: `sdd-setup/references/customizacao.md` (arquivos, regras de merge, override esparso, exemplos).

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

## Fluxo

### Passo 1 — Qual skill

Pergunte qual skill customizar (ou use a citada). Só as da tabela de `customizacao.md` têm `customize.toml`.

### Passo 2 — O que existe hoje

Rode `uv run _sdd/scripts/customize.py --skill <skill> --project docs/{projeto}`. O script localiza a skill instalada (plugins pelo `installed_plugins.json`, Skills CLI em `.claude/skills/`) e lê o `customize.toml` dela (caminho em `base`). Skill não encontrada: diga que ela não é customizável ou não está instalada. Mostre:
- os campos customizáveis, com o padrão e o comentário do `customize.toml`;
- o override atual (`docs/{projeto}/_custom/<skill>.toml`), se houver, e os `warnings`.

### Passo 3 — O que mudar

Pergunte o que o usuário quer mudar e traduza para os campos. Exemplos: "a revisão não precisa de segurança neste projeto" → `lenses` com `id = "seguranca"` e `enabled = false`; "sempre leia nossos padrões" → `persistent_facts = ["file:docs/padroes/*.md"]`; "nosso teste é `make test`" → `commands` com o `code` da stack e só `suite`. Pedido que nenhum campo atende: diga isso — não invente campo (ele seria ignorado). Se for um ajuste que só faz sentido para uma execução, sugira dizer isso na conversa em vez de gravar.

### Passo 4 — Gravar esparso

Monte o override só com o que muda (nunca copie a base). Mostre o arquivo antes → depois e, com a confirmação, grave `docs/{projeto}/_custom/<skill>.toml`. Arquivo existente: edite só as chaves em questão, preservando o resto.

### Passo 5 — Conferir

Rode o `customize.py --skill <skill>` de novo e mostre o `resolved` dos campos alterados (`--key`) e os `warnings`. Aviso de chave ignorada ou de tipo errado: corrija. Aviso de override não esparso: proponha remover os valores iguais à base.

## Regras importantes

- Nunca edite o `customize.toml` de uma skill nem arquivos do plugin.
- O override é por projeto e fica na documentação do projeto; nada vai para `_sdd/` nem para os repositórios de código.
- Só o que muda vai para o override.
- Para desfazer: apagar o `docs/{projeto}/_custom/<skill>.toml` (com confirmação) devolve a skill aos padrões.
