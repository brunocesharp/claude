---
name: create-story
description: Gera o arquivo de uma story com contexto completo (docs/{projeto}/implementacao/stories/{id}.md) — história, critérios de aceite com os cenários BDD copiados literalmente, tarefas ligadas aos critérios, repositórios e contratos, arquitetura e decisões, arquivos a criar ou alterar, skills de código e aprendizados da story anterior — e move a story de backlog para ready-for-dev. É a única fonte de verdade para a implementação. Use quando o usuário disser "criar story", "gerar a story", "preparar a próxima story", "detalhar a story", "story file", "próxima story", "deixar a story pronta para desenvolvimento", "ready for dev". NÃO use para planejar épicos e stories (use plan-epics), ver o quadro (use sprint-planning), implementar (use dev-story) ou mudar uma story já em andamento (use correct-course).
metadata:
  version: 1.0.0
  category: plan
  depends-on: plan-epics
  output: docs/{projeto}/implementacao/stories/{id}.md
---

# Create Story

Gera, para **uma** story do quadro, o arquivo que o `dev-story` vai seguir como **única fonte de verdade**. O trabalho pesado de juntar contexto fica aqui, para que a implementação, numa sessão nova, não precise abrir escopo, spec nem arquitetura. Inspirado no `create-story` do BMAD v6.

Leia antes de executar:
- `references/template-story.md` — o arquivo da story e as regras de preenchimento.
- `sdd-setup/references/sprint-status.md` (plugin `sdd`) — estados e scripts.
- `plan-epics/references/template-epico.md` (plugin `spec-plan`) — de onde vêm história, camadas e decisões da story.

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

A partir da raiz do workspace (`{P}` = `docs/{projeto}`):

```
uv run _sdd/scripts/status.py --project {P} next | show
uv run _sdd/scripts/epics.py  --project {P} spec --escopo {escopo} 1.3 RN-1.2
uv run _sdd/scripts/story.py  --project {P} check {id}
uv run _sdd/scripts/status.py --project {P} attach {id} stories/{id}.md
uv run _sdd/scripts/status.py --project {P} set {id} ready-for-dev
```

Sem `_sdd/scripts/`: ofereça o `sdd-setup`. Sem `uv`: `python` 3.11+ com `pyyaml`; sem nenhum, siga **Sem `uv`**.

---

## Fluxo

### Passo 1 — Escolher a story

- Com id citado: use-a. Ela precisa estar em `backlog` (ou `blocked` com o impedimento resolvido). Em `ready-for-dev`: o arquivo já existe — ofereça revisar/regenerar (mostrando a diferença) em vez de criar. Em `in-progress` ou além: pare e sugira `correct-course`.
- Sem id: rode `status.py next`. Se a ação for `create-story`, use essa story. Se for outra (há story em andamento, em revisão ou pronta para desenvolver), mostre e pergunte se quer mesmo preparar uma nova agora.
- **Dependências:** confira no `show` as stories de `depends_on` (frontmatter do épico). Alguma ainda não `done`: avise — os aprendizados dela ainda não existem — e pergunte se segue.
- **Uma por vez:** se o usuário pedir várias, avise que as seguintes não vão ter os aprendizados das anteriores; gere em sequência só com a confirmação.

### Passo 2 — Juntar o contexto

Leia, nesta ordem, e anote o que vai para cada seção do template:

1. **Épico** (`implementacao/epicos/epic-{n}-*.md`): a story no frontmatter (`covers`, `repositories`, `size`, `kind`, `depends_on`, `checkpoint`) e no corpo (história, camadas tocadas, decisões a tomar na story), além dos Limites do épico (para "Fora desta story").
2. **Especificação**: rode `epics.py spec --escopo {escopo}` com os ids de `covers` e copie os blocos **literalmente** nos critérios. `missing` não vazio: a spec mudou depois do plano — pare e sugira `correct-course`.
3. **Arquitetura**: `arquitetura/arquitetura.md` (contêineres e componentes tocados) e os ADRs aceitos que se aplicam (resumo de uma frase + caminho).
4. **Regras de negócio** já documentadas em `business/` para as áreas tocadas.
5. **Repositórios**: um só (`project-config.json`: `repository_url`, `code_path`) ou vários (`repositorios.md`: papel, caminho local, contêineres, contratos). Branch `feat/{id}` em todos os repositórios da story. Liste os contratos que mudam e se são compatíveis (ver `workspace/multi-repo/references/coordenacao-mudancas.md`).
6. **Código**: se o caminho local existir, leia o necessário para preencher "Arquivos a criar ou alterar" com caminhos reais e para citar o padrão já usado (um arquivo parecido existente). Só leitura: não altere nada nos repositórios. Sem código local: registre os caminhos esperados pela arquitetura e marque "conferir no código".
7. **Skills de código**: pela tecnologia de cada contêiner e o tipo de tarefa (`plan-execution/references/skill-mapping.md`), diga qual skill e qual referência dela o dev deve usar.
8. **Story anterior**: a última `done` do mesmo épico (ou a dependência direta). Do arquivo dela, leve para "Aprendizados" as decisões do Registro do desenvolvimento e os achados da Revisão que afetam esta story.

Dúvida que só o usuário responde (ex.: comportamento não coberto pela spec): pergunte agora. Não invente requisito.

### Passo 3 — Escrever o arquivo

Grave `implementacao/stories/{id}.md` pelo template, com `status: backlog` no frontmatter (o script troca na transição). Título com prefixo de backlog se `backlog.prefixes` = `sim` (`[TASK] Desenvolver - [{Módulo}] - ...`; spike: `[TASK] Analisar e especificar - ...`; habilitador: `[HT] [{Módulo}] - ...`).

Regras do conteúdo: cada `covers` vira `**CA-N**` com o texto copiado; toda tarefa cita seus CA e todo CA tem tarefa; testes são tarefas; provedor antes do consumidor; nada de "a definir" nos critérios.

### Passo 4 — Validar

Rode `story.py check {id}`. Corrija todos os `problems` e mostre os `warnings`. Confira também, à mão:
- dá para implementar lendo **só** este arquivo? (releia como se fosse o dev, numa sessão sem histórico);
- nada contradiz um ADR aceito;
- cabe numa sessão. Se não couber, proponha dividir: a divisão é feita no épico (`plan-epics`, modo Atualizar) e esta story volta ao passo 1.

### Passo 5 — Mostrar e confirmar

Mostre um resumo: história, critérios (CA e origem), tarefas, repositórios e ordem, arquivos principais, decisões em aberto. Peça confirmação ou ajustes.

### Passo 6 — Pronta para desenvolvimento

Com a confirmação:
1. `status.py attach {id} stories/{id}.md`
2. `status.py set {id} ready-for-dev` (atualiza o frontmatter e, se for a primeira do épico, o épico para `in-progress`)
3. Acrescente a linha no Histórico da story (`backlog → ready-for-dev`, `create-story`).
4. Atualize a Situação do projeto em `docs/workspace.md` com o `situacao` de `status.py show`.

### Passo 7 — Próximo passo: sessão nova

> "A story **{id}** está pronta para desenvolvimento em `docs/{projeto}/implementacao/stories/{id}.md`.
> Implemente numa **sessão nova**, para começar só com a story como contexto: abra o Claude Code no repositório **{repositório principal}** (com `--add-dir` do workspace e dos outros repositórios da story) e peça `dev-story {id}`. Posso abrir essa janela para você. Ou, aqui: `/clear` e depois `dev-story {id}`.
> {checkpoint: true} Esta story é um **checkpoint**: acompanhe a implementação de perto e revise antes de seguir para a próxima."

Para abrir a janela: `session.py` sem `--launch` (mostre o `display`) e, com a confirmação, com `--launch` — `--cwd` = repositório principal, `--add-dir` = workspace e demais repositórios, `--prompt "dev-story {id}"`.

Se o `dev-story` não estiver instalado, diga que a story pode ser implementada à mão seguindo as Tarefas, marcando-as e preenchendo o Registro do desenvolvimento.

---

## Sem `uv`

- **Story:** escolha pelo `sprint-status.yaml` (ordem do arquivo, primeira em `backlog`).
- **Cenários:** copie da spec o bloco inteiro do `#### Cenário N.M` até o próximo título; a regra, a linha inteira do `**RN-N.M**`.
- **Validação:** confira as regras de `references/template-story.md` (seções, CA ↔ tarefas, covers nos critérios, referências existentes).
- **Transição:** edite o `sprint-status.yaml` (`file` e `status: ready-for-dev`, épico para `in-progress` se estava em `backlog`, `updated_at`) e o frontmatter da story.

## Vários repositórios

A seção **Repositórios** da story é o plano da mudança coordenada: caminho local de cada repositório, branch `feat/{id}` (a mesma em todos), o que muda em cada um, a **ordem** (provedor antes do consumidor) e a tabela **Contratos** (compatível ou não, e a estratégia). Tarefas do provedor vêm antes das do consumidor. Contrato incompatível sem estratégia: não marque `ready-for-dev` — decida com o usuário (ou `arch-adr`). Ao fechar, diga em qual repositório abrir a sessão do `dev-story` (o primeiro da ordem) e quais entram com `--add-dir`.

## Regras importantes

- Uma story por vez, na ordem do quadro, salvo pedido explícito.
- Critérios e cenários são copiados, nunca reescritos; o resto é referenciado com caminho e seção existentes.
- A story não sai de `backlog` sem `story.py check` sem problemas e sem a confirmação do usuário.
- Só leitura nos repositórios de código: nada de branch, commit ou arquivo novo lá. A branch é criada pelo `dev-story` (ou pelo `multi-repo`).
- Se a spec ou o épico não bastam para escrever um critério sem ambiguidade, pergunte ou devolva para `plan-epics`/`correct-course` — não invente.

## Troubleshooting

**Cenário citado não existe mais na spec** (`missing` no `epics.py spec`) — a especificação mudou depois do plano. Não crie a story; sugira `correct-course`.

**Story de vários repositórios com contrato incompatível sem estratégia** — não siga: registre em Decisões em aberto as opções (expandir e depois contrair, versão nova, feature flag) e decida com o usuário; se a decisão vale para o projeto, sugira `arch-adr`.

**Código local indisponível** — gere com os caminhos esperados e avise no Contexto que precisam ser conferidos; o `dev-story` confere ao abrir o repositório.
