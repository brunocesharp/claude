---
name: sprint-planning
description: Gera e mantém o quadro de entrega do projeto, docs/{projeto}/implementacao/sprint-status.yaml, a partir dos arquivos de épico; mostra o quadro por épico (backlog, ready-for-dev, in-progress, review, done, blocked, dropped), a próxima story e muda o estado de uma story ou épico a pedido. Use quando o usuário mencionar "sprint planning", "planejar o sprint", "gerar o sprint-status", "atualizar o sprint-status", "sincronizar os épicos", "quadro do sprint", "status do sprint", "como está o sprint", "qual a próxima story", "marcar story como", "bloquear story", "cancelar story". NÃO use para criar épicos e stories a partir da especificação (use plan-epics), gerar o arquivo de uma story (use create-story), implementar (use dev-story) ou mudar o plano por causa de uma mudança de requisito (use correct-course).
metadata:
  version: 1.0.0
  category: plan
  depends-on: plan-epics
  output: docs/{projeto}/implementacao/sprint-status.yaml
---

# Sprint Planning

Mantém o `sprint-status.yaml` do projeto: a **fonte única** do andamento de épicos e stories. Inspirado no `sprint-planning` do BMAD v6.

Leia antes de executar: `sdd-setup/references/sprint-status.md` (no plugin `sdd`) — formato, estados, transições, frontmatter dos épicos e o comando `status.py`.

Três modos, pela frase do usuário:

| Modo | Exemplo | Grava? |
|------|---------|--------|
| **Sincronizar** | "gerar o sprint-status", "atualizar com os épicos novos" | Sim, após confirmação |
| **Quadro** | "como está o sprint", "qual a próxima story" | Não |
| **Mudar estado** | "bloqueia a 1-3", "cancela a 2-1", "marca a 1-2 como done" | Sim, após confirmação |

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

## Como chamar o script

```
uv run _sdd/scripts/status.py --project docs/{projeto} <comando>
```

Rode a partir da raiz do workspace. Sem `_sdd/scripts/status.py`: ofereça rodar o `sdd-setup` (ele copia os scripts). Sem `uv`: `python _sdd/scripts/status.py ...` funciona se o Python 3.11+ tiver o pacote `pyyaml`; senão, siga **Sem `uv`** no fim. Em erro, o script imprime `error: <mensagem>`: mostre a mensagem e não contorne editando o arquivo à mão.

---

## Modo Sincronizar

1. **Épicos.** Liste `docs/{projeto}/implementacao/epicos/epic-*.md`. Sem nenhum: explique que o quadro nasce dos épicos e ofereça a skill `plan-epics`. Se ela não estiver instalada, mostre o frontmatter de épico da referência e ofereça criar os arquivos com o usuário.
2. **Prévia.** Rode `sync --dry-run` e mostre, de forma resumida:
   - se o arquivo será **criado**;
   - épicos e stories **novos** (entram em `backlog`);
   - **atualizados** (título, escopo, repositórios) e épicos **reordenados**;
   - **órfãos**: stories ou épicos que estão no `sprint-status.yaml` e sumiram dos arquivos de épico;
   - o quadro resultante (`board`).
   Se `changed` for `false` e não houver órfãos, diga que já está sincronizado e pule para o passo 5.
3. **Órfãos.** O sync nunca remove. Para cada órfão, pergunte o que fazer: cancelar (`set <id> dropped`), devolver ao arquivo do épico (a story foi apagada por engano) ou deixar como está. Story órfã em `in-progress` ou `review` indica mudança de plano no meio da entrega: sugira `correct-course`.
4. **Gravar.** Com a confirmação, rode `sync` (sem `--dry-run`) e depois os `set` decididos no passo 3.
5. **Vários repositórios.** Se existir `docs/{projeto}/repositorios.md`, confira se cada nome em `repositories` está cadastrado lá; nome desconhecido: avise e sugira corrigir no arquivo do épico ou cadastrar com `multi-repo`.
6. **Resumos para pessoas.** Rode `show` e atualize:
   - `docs/{projeto}/project.md`: marque `[x] Plano de Execução` (se ainda não estiver);
   - linha do projeto em `docs/workspace.md`: coluna Situação = campo `situacao` do `show` (só essa célula; nunca reescreva o arquivo inteiro).
7. **Fechamento.** Mostre o quadro (Modo Quadro) e a próxima ação.

## Modo Quadro

Rode `show` e `next`. Mostre uma tabela por épico e a próxima ação:

> **epic-1 — Cadastro de produtos** (in-progress, 1/3 done)
>
> | Story | Estado | Repositórios |
> |-------|--------|--------------|
> | 1-1-criar-produto | done | loja-api, loja-web |
> | 1-2-listar-produtos | ready-for-dev | loja-api, loja-web |
> | 1-3-importar-planilha | backlog | loja-api |
>
> **Próxima:** implementar `1-2-listar-produtos` com `dev-story`, numa sessão nova.

Traduza a ação do `next`: `dev-story` (retomar ou implementar), `story-review` (revisar), `create-story` (gerar o arquivo da story), `retrospective` (opcional) ou `close-epic` (confirmar o épico como done), `unblock` (só restam bloqueadas: pergunte o que destrava). Se a skill indicada ainda não estiver instalada, diga qual é a story e o que fazer com ela. Rode também `check` e mostre os `problems`, se houver (ex.: frontmatter da story diferente do quadro).

## Modo Mudar estado

1. Identifique o id (story `N-M-slug`, épico `epic-N` ou retrospectiva `epic-N-retrospective`) e o estado pedido.
2. Mostre a mudança (de → para) e peça confirmação. `blocked`: peça o motivo e registre na seção Histórico do arquivo da story, se ele existir.
3. Rode `set <id> <estado>`. Se o script recusar a transição, mostre a mensagem com os estados permitidos. Use `--force` **só** se o usuário pedir explicitamente, depois de ver a recusa.
4. Épico para `done`: só com todas as stories `done`/`dropped`, e sempre com confirmação. Sugira a retrospectiva (opcional) antes.
5. Atualize a Situação do `workspace.md` com o `situacao` do `show`.

As transições do dia a dia são feitas pelas próprias skills do fluxo (`create-story`, `dev-story`, `story-review`); este modo é para ajustes da pessoa.

---

## Sem `uv`

Faça à mão, seguindo `sdd-setup/references/sprint-status.md`:
- **Sincronizar:** leia o frontmatter de cada épico e edite o `sprint-status.yaml` com as mesmas regras do `sync` (acrescentar em `backlog`, atualizar título/escopo/repositórios/ordem, nunca mudar `status`/`file`, nunca remover). Mostre a prévia antes de gravar.
- **Mudar estado:** confira a transição na tabela da referência antes de editar; atualize `updated_at` e o `status:` do frontmatter da story.

## Regras importantes

- O `sprint-status.yaml` é a fonte única do andamento: o `project.md` e o `workspace.md` só recebem o resumo.
- Nunca rebaixe nem apague estado por conta própria: o sync não faz isso, e mudanças manuais pedem confirmação.
- A ordem das stories no arquivo é a ordem de build; ela vem dos arquivos de épico.
- Nada desta skill é gravado nos repositórios de código. Nunca faça commit nem push.

## Troubleshooting

**`error: sprint-status.yaml inválido`** — alguém editou à mão. Mostre os erros e proponha a correção; depois rode o `sync` de novo.

**Story mudou de épico** — o id carrega o número do épico (`2-1-...`). Mover é trocar o id: crie a story nova no épico de destino e cancele a antiga (`dropped`), registrando no Histórico de ambas. Se já houver arquivo de story, use `correct-course`.

**Dois escopos no mesmo projeto** — um `sprint-status.yaml` só; os épicos dos dois escopos convivem, cada um com o seu `escopo`. A numeração dos épicos é global no projeto.
