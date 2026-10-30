# `sprint-status.yaml` — formato, estados e transições

Fonte única do andamento da entrega de um projeto. Um arquivo por projeto, cobrindo todos os escopos:

```
docs/{projeto}/implementacao/
├── sprint-status.yaml
├── epicos/epic-{n}-{slug}.md        # plan-epics
└── stories/{n}-{m}-{slug}.md        # create-story (o campo file aponta para cá)
```

Adaptado do `sprint-status.yaml` do BMAD v6, em formato aninhado (épico → stories) e com `blocked` e `dropped`.

## Formato

```yaml
# (cabeçalho de comentário gravado pelo status.py)
version: 1
project: gestao-de-estoque          # slug da pasta em docs/
updated_at: '2026-10-30'           # o status.py atualiza a cada mudança
epics:
  epic-1:
    title: Cadastro de produtos
    escopo: gestao-de-produtos      # pasta em docs/{projeto}/escopo/
    status: in-progress
    retrospective: optional         # optional | done
    stories:
      1-1-criar-produto:
        title: Criar produto
        status: done
        repositories: [estoque-api, estoque-web]
        file: stories/1-1-criar-produto.md      # relativo a implementacao/
      1-2-listar-produtos:
        title: Listar produtos
        status: ready-for-dev
        repositories: [estoque-api, estoque-web]
        file: stories/1-2-listar-produtos.md
      1-3-importar-planilha:
        title: Importar planilha
        status: backlog
        repositories: [estoque-api]
```

| Campo | Regra |
|-------|-------|
| id do épico | `epic-N`, numeração global no projeto (não reinicia por escopo) |
| id da story | `N-M-slug`: N = número do épico, M = ordem no épico, slug em kebab-case |
| ordem | a ordem das chaves é a **ordem de build** — o `next` segue essa ordem |
| `repositories` | nomes do `repositorios.md` (vários repositórios) ou o repositório único; lista vazia se não se aplica |
| `file` | obrigatório a partir de `ready-for-dev` |

## Estados

**Story:** `backlog` → `ready-for-dev` → `in-progress` → `review` → `done`, mais `blocked` e `dropped`.

| Estado | Significa | Quem coloca |
|--------|-----------|-------------|
| `backlog` | Planejada, sem arquivo de story | `sprint-planning` / `plan-epics` |
| `ready-for-dev` | Arquivo da story pronto, com contexto completo | `create-story` |
| `in-progress` | Em implementação | `dev-story` ao começar |
| `review` | Implementada, testes passando, aguardando revisão | `dev-story` ao terminar |
| `done` | Revisada e aceita | `story-review` ou a pessoa |
| `blocked` | Parada por impedimento externo (registre o motivo na story) | qualquer skill ou a pessoa |
| `dropped` | Cancelada; fica no arquivo como histórico | `correct-course` ou a pessoa |

**Épico:** `backlog`, `in-progress`, `done`, `dropped`. Vai sozinho para `in-progress` quando a primeira story sai do backlog. Só vai para `done` com todas as stories `done`/`dropped`, e só após confirmação do usuário.

**Retrospectiva** (`retrospective` do épico): `optional` → `done`. É opcional.

## Transições permitidas

| De | Para |
|----|------|
| `backlog` | `ready-for-dev`, `blocked`, `dropped` |
| `ready-for-dev` | `in-progress`, `backlog`, `blocked`, `dropped` |
| `in-progress` | `review`, `ready-for-dev`, `backlog`, `blocked`, `dropped` |
| `review` | `done`, `in-progress`, `blocked`, `dropped` |
| `blocked` | `backlog`, `ready-for-dev`, `in-progress`, `review`, `dropped` |
| `dropped` | `backlog` |
| `done` | nenhuma — mudança depois de pronto vira story de ajuste (`correct-course`) |

Épico: `backlog` → `in-progress`/`dropped`; `in-progress` → `done`/`backlog`/`dropped`; `done` → `in-progress`; `dropped` → `backlog`.

Fora da tabela, só com `--force` e **só quando o usuário pedir** explicitamente.

## Entrada: frontmatter dos épicos

O `sprint-status.yaml` nasce e é atualizado a partir dos arquivos de épico (`plan-epics` escreve; `sprint-planning` sincroniza). Cada `implementacao/epicos/epic-N-slug.md` começa com:

```yaml
---
id: epic-1
title: Cadastro de produtos
escopo: gestao-de-produtos
stories:                       # na ordem de build
  - id: 1-1-criar-produto
    title: Criar produto
    repositories: [estoque-api, estoque-web]
    size: M                    # P | M | G (tamanho relativo; G = no limite de uma sessão)
    kind: story                # story | spike | enabler
    covers: ["1.1", "1.2", "RN-1.1"]   # cenários (N.M) e regras (RN-N.M) da spec-functional
    checkpoint: true           # pede atenção humana antes de seguir
  - id: 1-2-listar-produtos
    title: Listar produtos
    repositories: [estoque-api, estoque-web]
    size: M
    covers: ["1.3"]
    depends_on: [1-1-criar-produto]     # só stories que vêm antes na ordem de build
---
```

O `sync` usa só `id`, `title`, `escopo` e `repositories`. Os demais campos são do planejamento (`plan-epics`) e são conferidos pelo `epics.py`:

```
uv run _sdd/scripts/epics.py --project docs/{projeto} validate                       # formato, tamanhos, dependências
uv run _sdd/scripts/epics.py --project docs/{projeto} coverage --escopo {escopo}     # cenário da spec → stories
```

`coverage` lê os cabeçalhos `#### Cenário N.M` e as regras `**RN-N.M**` da `especificacao/{escopo}/spec-functional.md`. Itens com `(removido)` no título não precisam de cobertura.

`status.py sync` mescla todos os épicos no `sprint-status.yaml`:
- cria o arquivo se não existir;
- acrescenta épicos e stories novos em `backlog`;
- atualiza `title`, `escopo`, `repositories` e a **ordem** das stories conforme os épicos;
- **nunca** muda `status` nem `file` do que já existe e **nunca** remove: o que sumiu dos épicos fica no arquivo e volta em `orphans` (decidir com o usuário: `dropped`, mover para outro épico ou devolver ao arquivo do épico);
- `--dry-run` mostra o resultado sem gravar.

## Script (`_sdd/scripts/status.py`)

Rode a partir da raiz do workspace (onde está `_sdd/`):

```
uv run _sdd/scripts/status.py --project docs/{projeto} sync [--dry-run]   # mescla os épicos
uv run _sdd/scripts/status.py --project docs/{projeto} show          # quadro por épico (+ texto da Situação)
uv run _sdd/scripts/status.py --project docs/{projeto} next          # próxima ação
uv run _sdd/scripts/status.py --project docs/{projeto} set <id> <estado> [--force]
uv run _sdd/scripts/status.py --project docs/{projeto} check         # coerência com os arquivos de story
```

- `set` valida a transição e a coerência, grava o arquivo e, para story, atualiza o `status:` no frontmatter do arquivo da story. Para a retrospectiva, use o id `epic-N-retrospective`.
- `next` devolve a ação, nesta prioridade: retomar `in-progress` (`dev-story`) → revisar `review` (`story-review`) → implementar `ready-for-dev` (`dev-story`) → fechar o épico com todas as stories finalizadas (`retrospective`, opcional, ou `close-epic`) → criar o arquivo do primeiro `backlog` (`create-story`) → desbloquear (`unblock`).
- `check` aponta: arquivo de story ausente, frontmatter diferente do sprint-status (vale o sprint-status) e erros de formato.
- O hook do plugin `sdd` valida o arquivo sempre que o Claude o grava ou edita; erro volta para o Claude corrigir.

## Sem `uv`

Edite o arquivo com a ferramenta Edit seguindo este documento:
1. Confira a transição na tabela antes de mudar um `status`.
2. Story saindo do backlog com o épico em `backlog`: mude o épico para `in-progress` também.
3. Atualize `updated_at` com a data de hoje e o `status:` do frontmatter do arquivo da story.
4. Nunca mude a ordem das stories sem o usuário pedir (é a ordem de build).

## Resumo para pessoas

Ao mudar estados, a skill atualiza também:
- `docs/{projeto}/project.md`: marca a fase **Plano de Execução** quando o sprint-status nasce; durante a entrega, a fase atual é Desenvolvimento.
- Coluna **Situação** do `docs/workspace.md`: o campo `situacao` do `show`, ex.: `Desenvolvimento — epic-1: 3/5 done` (épico em andamento, ou o próximo, e stories `done` sobre as não canceladas).
