---
name: dev-story
description: Implementa uma story a partir do arquivo dela (docs/{projeto}/implementacao/stories/{id}.md), numa sessão nova, tendo a story como única fonte de verdade — cria a branch, executa as tarefas na ordem (teste antes do código), usa as skills de código indicadas, roda build e testes, preenche o Registro do desenvolvimento e os Arquivos alterados e move a story de ready-for-dev para in-progress e para review. Retoma uma story in-progress. Também abre, com confirmação, uma janela nova do terminal já com o Claude no repositório da story. Use quando o usuário disser "dev-story", "implementar a story", "desenvolver a story", "começar a story", "retomar a story", "continuar a implementação", "abrir sessão nova para a story". NÃO use para preparar a story (use create-story), revisar a implementação (use story-review), mudar requisito ou plano (use correct-course) ou gerar código avulso sem story (use as skills architecture-* e angular-*).
metadata:
  version: 1.0.0
  category: implementation
  depends-on: create-story
  output: código nos repositórios da story; seções Tarefas, Registro do desenvolvimento, Arquivos alterados e Histórico do arquivo da story
---

# Dev Story

Implementa **uma** story, numa sessão com contexto limpo, seguindo **só** o arquivo da story. Inspirado no `dev-story` do BMAD v6: a story foi preparada com todo o contexto (`create-story`); aqui não se reabre escopo, especificação nem arquitetura, e não se inventa requisito.

Leia antes de executar: `references/comandos-por-stack.md` (build e testes) e `sdd-setup/references/sprint-status.md` (plugin `sdd`; estados e scripts).

---

## Passo 0 — Localizar a story e o workspace

Esta skill normalmente roda **dentro do repositório de código**, com o workspace de documentação acessível por `--add-dir`. Por isso o Passo 0 é diferente das skills de documentação:

1. **Story**: o usuário passa o id (`1-2-listar-produtos`) ou o caminho do arquivo. Com caminho: `{P}` = a pasta três níveis acima (`docs/{projeto}`) e `{workspace}` = a pasta que contém `docs/` (e `_sdd/`). Só com id: procure `_sdd/` no diretório atual, nos pais e nos diretórios adicionados à sessão; depois `docs/*/implementacao/stories/{id}.md`. Mais de um projeto com esse id: pergunte. Não achou: peça o caminho do workspace (e explique o `--add-dir`).
2. **Configuração**: leia `{workspace}/_sdd/config.toml` e `config.user.toml` (o pessoal vence): `language.*`, `user.*`, `delivery.tdd` (`recomendado`), `delivery.auto_mode` (`nao`), `delivery.review_mode` (`sessao-nova`). Sem `_sdd/`: use os padrões.
3. Sem id nem caminho: rode `status.py next` e use a story indicada, se a ação for `dev-story`.

## Scripts

Rode a partir de `{workspace}` (`{P}` = `docs/{projeto}`):

```
uv run _sdd/scripts/story.py   --project {P} check {id}
uv run _sdd/scripts/status.py  --project {P} set {id} in-progress | review
uv run _sdd/scripts/session.py --cwd {repo} --add-dir {workspace} [--add-dir {outro repo}] --prompt "dev-story {id}" [--launch]
```

Sem `uv`: `python` 3.11+ com `pyyaml`; sem nenhum, edite o `sprint-status.yaml` e o frontmatter como em `sprint-status.md` ("Sem `uv`").

---

## Passo 1 — Sessão nova

A story precisa ser a primeira coisa desta sessão. Se a conversa já tem outra story, outro escopo ou uma implementação anterior:

> "Esta sessão já tem outro contexto ({o quê}). Para implementar a **{id}** só com a story como referência, o melhor é uma sessão nova. Posso:
> 1. **Abrir uma janela nova** do terminal com o Claude no repositório **{repo}**, já pedindo `dev-story {id}`;
> 2. Você roda `/clear` aqui e pede `dev-story {id}` de novo;
> 3. Seguir aqui mesmo (não recomendado)."

Opção 1: rode `session.py` **sem** `--launch`, mostre o comando (`display`) e, com a confirmação, rode com `--launch`. `--cwd` = repositório principal da story (o primeiro em `repositories`); `--add-dir` = o workspace e os outros repositórios. Depois de abrir, pare aqui: a implementação continua na janela nova. Se `--launch` falhar ou não houver terminal (`note`), mostre o `display` para a pessoa colar.

## Passo 2 — Pré-condições

1. Leia o arquivo da story **inteiro**. Ele é a fonte única: só abra outro documento quando a story o referenciar (caminho#seção), e só a seção citada.
2. `status` precisa ser `ready-for-dev` (começar) ou `in-progress` (retomar). `backlog`: sugira `create-story`. `review`/`done`: pergunte se é revisão (`story-review`) ou mudança (`correct-course`). `blocked`: mostre o motivo no Histórico e pergunte se foi resolvido.
3. `story.py check {id}`: com `problems`, pare e sugira corrigir com `create-story`.
4. **Repositórios** (seção Repositórios): cada um precisa existir no caminho local. Em cada um, rode `git status --porcelain` e `git branch --show-current`:
   - alterações pendentes que não são desta story: pare naquele repositório e pergunte (nunca faça stash, commit ou descarte);
   - branch `feat/{id}` (ou a da story) já existe: use-a;
   - não existe: mostre `git switch -c feat/{id}` (a partir da branch principal atualizada) e crie **após confirmação** — em `auto_mode` = `sim`, crie sem perguntar. Vários repositórios: o mesmo nome em todos, na ordem da seção Repositórios; se falhar em um, pare e mostre o que já foi feito.
5. Começando: `status.py set {id} in-progress` e linha no Histórico (`ready-for-dev → in-progress`, `dev-story`).

## Passo 3 — Implementar, tarefa por tarefa

Na ordem da seção Tarefas, começando pela primeira `[ ]` (retomada: confira no Registro do desenvolvimento onde parou):

1. **Teste primeiro** (`delivery.tdd`): escreva o teste que expressa o critério (CA) da tarefa e veja-o falhar. `recomendado`: pode inverter quando o teste antes não fizer sentido (ex.: configuração), registrando o porquê; `obrigatorio`: sempre.
2. **Código**: use a skill e a referência indicadas em "Padrões e skills de código" (ex.: `architecture-feature`, `angular-feature-layer`) e siga o padrão do arquivo de exemplo citado. Crie/altere os arquivos de "Arquivos a criar ou alterar"; arquivo novo fora da lista é permitido quando necessário, e vai para o Registro.
3. **Teste passa**: rode o teste do alvo (`comandos-por-stack.md`).
4. **Marque** a tarefa `[x]` no arquivo da story (e as subtarefas) só com o teste passando.
5. Vários repositórios: provedor antes do consumidor, como na seção Repositórios; confira o contrato (rota, DTO, evento) contra a tabela de Contratos antes de usar no consumidor.

**Regra da fonte única — pare quando:**
- um critério ou tarefa estiver ambíguo, incompleto ou contradizer o código existente;
- for preciso decidir algo listado em "Decisões em aberto" ou algo que a story não cobre;
- a implementação exigir mudar um contrato além do previsto ou mexer em algo de "Fora desta story".

Nesses casos: registre a dúvida no Registro do desenvolvimento (o que, onde, opções) e pergunte. Se o usuário responder, registre a resposta como **Decisão** (data, quem) e siga. Se a resposta muda o que a story promete (critério novo, critério diferente, outro repositório), não siga: sugira `correct-course` e, se a story ficar parada, `status.py set {id} blocked` com o motivo no Histórico. Nunca invente o requisito.

**Checkpoint** (`checkpoint: true` no frontmatter): pare ao fim da primeira tarefa que define o padrão (normalmente a T1) e ao fim da story, mostre o que foi feito e espere o "pode seguir". Vale mesmo em `auto_mode`.

**`auto_mode` = `sim`** (story sem checkpoint): sem pausas de confirmação entre tarefas; continua parando nas situações da regra da fonte única e antes de qualquer ação destrutiva.

## Passo 4 — Fechar a implementação

1. **Suíte completa e build** de cada repositório tocado (`comandos-por-stack.md`), mais lint se houver. Falhou: corrija e rode de novo; falha que não é desta story (já falhava na branch principal): registre e pergunte.
2. **Critérios**: para cada `CA-N`, confira que há teste que o verifica e que passa.
3. **Registro do desenvolvimento** — acrescente, sem apagar o que já existe:
   ```markdown
   ### {AAAA-MM-DD} — {modelo usado na sessão}
   - **Decisões:** {o que foi decidido e por quê; decisões do usuário com "(confirmado por {nome})"}
   - **Desvios:** {o que saiu diferente do planejado na story, e por quê; ou "nenhum"}
   - **Testes:** {suíte de cada repositório: N passaram / falharam / não executados (motivo)}
   - **Pendências:** {o que ficou para depois, ou "nenhuma"}
   ```
4. **Arquivos alterados** — por repositório, a partir de `git status --porcelain` e `git diff --name-status {branch principal}...HEAD` (inclua o que ainda não foi commitado):
   ```markdown
   ### {repositório} (`feat/{id}`)
   - `A` src/.../ListarProdutosQuery.cs
   - `M` src/.../ProdutosController.cs
   ```
5. **Estado**:
   - todas as tarefas `[x]`, todos os CA com teste passando e suíte verde → `status.py set {id} review` e linha no Histórico (`in-progress → review`);
   - senão, fica `in-progress` e o Registro diz o que falta.
6. **Commit**: nunca faça commit nem push sem o usuário pedir. Ofereça, por repositório, a mensagem pronta: `feat({módulo}): {título da story} ({id})`.

## Passo 5 — Próximo passo: revisão

- `delivery.review_mode` = `sessao-nova` (padrão): a revisão deve começar sem o contexto desta implementação. Ofereça abrir uma janela nova com `session.py` (`--prompt "story-review {id}"`) ou `/clear` e `story-review {id}`.
- `subagente`: ofereça rodar o `story-review` num subagente desta sessão (contexto separado), passando só o id e o caminho da story.
- Se o `story-review` não estiver instalado, diga que a story está em `review` e pode ser revisada à mão (critérios × testes × arquivos alterados) e movida para `done` com o `sprint-planning`.

---

## Regras importantes

- **Fonte única:** o arquivo da story. Nada de reabrir spec, escopo ou arquitetura por conta própria, nem completar requisito por suposição.
- Uma story por sessão.
- Tarefa marcada `[x]` só com teste passando; story em `review` só com tudo verde. Nunca registre teste como passando sem ter rodado.
- Nos repositórios de código: branch só com confirmação (ou `auto_mode`); **nunca** commit, push, merge, rebase, reset, stash ou descarte sem pedido explícito.
- No workspace de documentação, esta skill só edita o arquivo da story e, via script, o `sprint-status.yaml`.

## Troubleshooting

**A janela nova não abriu** — rode o `display` do `session.py` num terminal. No Windows sem Windows Terminal, o script usa `start`; no Linux sem terminal conhecido, só o `display` funciona.

**Story longa demais para a sessão** (contexto enchendo) — termine a tarefa atual, registre no Registro onde parou, deixe `in-progress` e continue numa sessão nova (`dev-story {id}` retoma pelas tarefas abertas). Se isso acontecer sempre, a story devia ter sido dividida: anote para a retrospectiva.

**Testes que já falhavam antes** — não conserte o que não é da story sem perguntar; registre como pendência e informe na revisão.

**Repositório não clonado** — sugira a `multi-repo` (Preparar) ou o `git clone` com confirmação; sem ele, a parte da story naquele repositório não pode ser feita.
