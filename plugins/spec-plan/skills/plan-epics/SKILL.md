---
name: plan-epics
description: Transforma escopo, especificação funcional e arquitetura de um projeto em épicos fatiados em stories verticais (cada story cabe numa sessão de implementação), com ordem de build, checkpoints, tamanho relativo (P/M/G) e matriz de cobertura cenário BDD → story; grava um arquivo por épico em docs/{projeto}/implementacao/epicos/ e alimenta o sprint-status.yaml. Também converte um execution-plan.md antigo em épicos. Use quando o usuário disser "planejar épicos", "criar épicos", "quebrar em stories", "fatiar em stories", "épicos e stories", "user stories do escopo", "backlog do escopo", "plano por stories", "converter o plano de execução em épicos". NÃO use para plano por entregas e tarefas por camada (use plan-execution), especificação (use spec-functional), gerar o arquivo detalhado de uma story (use create-story) ou só ver/mudar o quadro (use sprint-planning).
metadata:
  version: 1.0.0
  category: plan
  depends-on: spec-functional
  recommended-after: arch-c4
  output: docs/{projeto}/implementacao/epicos/epic-{n}-{slug}.md, docs/{projeto}/implementacao/sprint-status.yaml
---

# Plan Epics

Planeja a entrega de um escopo em **épicos** (resultados para o usuário) fatiados em **stories verticais** (um comportamento testável de ponta a ponta, que cabe numa sessão). Inspirado no `create-epics-and-stories` do BMAD v6 e no refinamento/incepção da PO do BMAD v7.

Não cria os arquivos de story: isso é o `create-story`, uma por vez, na hora de implementar.

Leia antes de executar:
- `references/checklist-prontidao.md` — o que conferir antes de fatiar.
- `references/fatiamento-vertical.md` — épico x story, como fatiar, tamanho, tipos, ordem e checkpoint (com exemplos bons e ruins).
- `references/template-epico.md` — o arquivo de épico (frontmatter lido por scripts + corpo).
- `sdd-setup/references/sprint-status.md` (plugin `sdd`) — o `sprint-status.yaml` que o plano alimenta.
- `../plan-execution/references/skill-mapping.md` — tipo de tarefa → skill de código, para a linha "Camadas tocadas".

Modos:

| Modo | Quando |
|------|--------|
| **Planejar** | Escopo com especificação e sem épicos |
| **Atualizar** | Épicos novos ou mudanças num escopo já planejado (antes de começar a implementar o que muda; durante a implementação, use `correct-course`) |
| **Migrar** | Existe `plano-execucao/{escopo}/execution-plan.md` e o usuário quer passar para épicos e stories |

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

**Escopo.** Liste `docs/{projeto}/especificacao/*/` e pergunte qual escopo planejar (um só: use e avise). Sem especificação: ofereça `spec-functional` (ou aceite uma especificação colada na conversa, avisando que a cobertura não poderá ser verificada por script).

## Customização (por projeto)

Depois de identificar o projeto, resolva a customização desta skill:

```
uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto}
```

Sem o script (ou sem `uv`/`python`): leia `${CLAUDE_SKILL_DIR}/customize.toml` e, se existir, `docs/{projeto}/_custom/plan-epics.toml`, e mescle pelas regras de `sdd-setup/references/customizacao.md`. Sem override, valem os padrões da skill.

1. Execute os `workflow.activation_steps_prepend`, na ordem.
2. Leia os arquivos de `facts` (e os textos literais): são fatos válidos durante toda a skill e vencem os padrões dela quando conflitarem.
3. Use os valores de `resolved.workflow` onde esta skill os cita: `max_stories_per_epic` (Passo 3), `max_size` (maior tamanho aceito no Passo 5), `checkpoint_rules` (Passo 6) e `title_prefixes` (prefixos no corpo do épico).
4. Ao terminar, execute os `workflow.activation_steps_append` e o `workflow.on_complete`.

Mostre os `warnings` ao usuário uma vez (ex.: chave que não é customizável, override que repete a base).

## Scripts

Rode a partir da raiz do workspace:

```
uv run _sdd/scripts/epics.py  --project docs/{projeto} validate
uv run _sdd/scripts/epics.py  --project docs/{projeto} coverage --escopo {escopo}
uv run _sdd/scripts/status.py --project docs/{projeto} sync [--dry-run]
```

Sem `_sdd/scripts/`: ofereça o `sdd-setup`. Sem `uv`: `python` com Python 3.11+ e `pyyaml`; sem nenhum, faça as mesmas verificações lendo os arquivos (seção **Sem `uv`**).

---

## Fluxo — modo Planejar

### Passo 1 — Ler as entradas

Na ordem, o que existir: `especificacao/{escopo}/spec-functional.md` (inteira), `escopo/{escopo}/escopo.md`, `arquitetura/arquitetura.md` e os ADRs aceitos em `arquitetura/decisoes/`, `repositorios.md`, `business/` (regras já documentadas do domínio), `implementacao/epicos/` (épicos de outros escopos). Rode `epics.py validate` para saber o próximo número de épico (`next_epic`).

### Passo 2 — Prontidão

Percorra `references/checklist-prontidao.md` e mostre o resultado em uma tabela curta (item, ok/lacuna, observação). Lacunas viram pontos em aberto no Passo 4. Pergunte se segue.

### Passo 3 — Propor os épicos

Proponha os épicos (só título, objetivo em uma frase, cenários cobertos), seguindo `fatiamento-vertical.md`: um por resultado para o usuário, nunca por camada; de 2 a ~8 stories cada. Em sistema novo, considere um primeiro épico com o esqueleto andante. Peça ajustes antes de seguir.

### Passo 4 — Pontos em aberto

Para cada lacuna da prontidão e cada ponto em aberto da especificação, proponha uma decisão e confirme com o usuário:
- **resolver agora** — pergunte e registre a resposta no épico (ou sugira `arch-adr` se for decisão de arquitetura);
- **spike** — vira story `kind: spike` antes das que dependem dela;
- **decidir na story** — fica anotado na story que vai precisar da decisão.

### Passo 5 — Fatiar em stories

Para cada épico, proponha as stories em ordem de build, numa tabela (como a do template): título, tamanho, tipo, cenários cobertos, dependências, repositórios, checkpoint. Para cada story, a frase **Como / quero / para** e as camadas tocadas com as skills de código. Regras:
- fatia vertical, cabe numa sessão (`G` é o limite; maior que isso, divida);
- `covers` com os ids da especificação (`N.M`, `RN-N.M`);
- vários repositórios: provedor antes do consumidor; contrato incompatível vira story própria com estratégia ou ponto em aberto;
- checkpoint nas fundacionais e arriscadas.

Mostre épico por épico e ajuste com o usuário antes do próximo.

### Passo 6 — Ordem de build e checkpoints

Mostre a sequência completa (todas as stories, na ordem) com as dependências e os checkpoints. O usuário pode reordenar e marcar ou desmarcar checkpoints. `depends_on` só aponta para stories anteriores.

### Passo 7 — Gravar os épicos

Mostre a lista de arquivos e grave `implementacao/epicos/epic-{n}-{slug}.md` pelo template (nunca sobrescreva um arquivo existente sem mostrar a diferença e confirmar). Depois rode:
1. `epics.py validate` — corrija os `problems` e mostre os `warnings`;
2. `epics.py coverage --escopo {escopo}` — preencha a seção Cobertura de cada épico com a matriz. Cenário sem story (`uncovered_scenarios`) ou referência inexistente (`unknown_refs`): volte ao Passo 5 para aquele item e só siga com o usuário de acordo. Regras sem cobertura direta (`uncovered_rules`): mostre e pergunte se estão implícitas em algum cenário.

### Passo 8 — Quadro

Rode `status.py sync --dry-run`, mostre o resultado (épicos e stories novos em `backlog`) e, com a confirmação, `sync`. Atualize `docs/{projeto}/project.md` (`[x] Plano de Execução`) e a Situação da linha do projeto em `docs/workspace.md` com o `situacao` de `status.py show`.

### Passo 9 — Fechamento

> "Planejei **{E} épicos** e **{S} stories** para o escopo **{escopo}**, com todos os {C} cenários cobertos. {K} stories têm checkpoint.
> A primeira é **{id}** — {título}. O próximo passo é gerar o arquivo dela com contexto completo (`create-story`) e implementá-la numa sessão nova."

Se o `create-story` não estiver instalado, diga isso e mostre a story no épico como ponto de partida.

---

## Modo Atualizar

1. Leia os épicos do escopo e o `sprint-status.yaml` (`status.py show`).
2. Pergunte o que mudou (cenários novos na spec, épico novo, divisão de story). Rode `epics.py coverage` para achar cenários novos sem story.
3. Aplique o fluxo dos Passos 4 a 7 só ao que muda. Regras: ids existentes não mudam; story nova recebe o próximo `m` livre do épico (a posição na lista define a ordem); story que sai do plano **não** é apagada do arquivo do épico se já estiver no quadro — marque-a com `(cancelada)` no corpo e, no Passo 8, trate como órfã (`dropped`).
4. Story já em `ready-for-dev` ou além que precisaria mudar: não edite aqui; sugira `correct-course`.
5. Registre a mudança no Histórico de cada épico alterado e rode o Passo 8 (o `sync` mostra o que muda).

## Modo Migrar (de `execution-plan.md`)

Migração opcional, oferecida também pelo `sdd-setup` (guia `sdd-setup/references/migracoes/execution-plan-para-epicos.md`).

1. Leia o `plano-execucao/{escopo}/execution-plan.md` e a especificação do escopo.
2. Cada **Entrega** do plano vira um ou mais **stories** (a entrega já é vertical, mas costuma levar mais de uma sessão: divida por cenário ou operação). Um conjunto coerente de entregas vira um **épico**; plano pequeno = um épico.
3. As tarefas por camada da entrega viram a linha "Camadas tocadas" da story. Estimativas em horas são descartadas (tamanho P/M/G). Critérios de aceite da entrega viram o `covers` (procure o cenário correspondente na spec) e o "Pronto quando" do épico.
4. Entregas já concluídas: pergunte; elas entram como stories e, depois do `sync`, vão para `done` com `status.py set ... --force` (a pedido do usuário, porque não passaram pelo fluxo de story).
5. Siga os Passos 6 a 9. No topo do `execution-plan.md`, acrescente uma linha `> Migrado para épicos em {data}: implementacao/epicos/` — nunca apague o plano antigo.

---

## Sem `uv`

- **validate:** confira à mão as regras de `references/template-epico.md` (ids, tamanhos, `depends_on` só para trás).
- **coverage:** liste os cabeçalhos `#### Cenário N.M` da spec (ignorando os `(removido)`) e cruze com os `covers` de todas as stories do escopo.
- **sync:** edite o `sprint-status.yaml` como descrito em `sdd-setup/references/sprint-status.md`.

## Vários repositórios

Com `docs/{projeto}/repositorios.md`:
- cada story declara em `repositories` os repositórios que toca (nomes do cadastro); prefira stories de um repositório quando o fatiamento vertical permitir;
- dentro da story, provedor antes do consumidor; entre stories, o contrato novo vem antes de quem o consome (`depends_on`);
- contrato incompatível vira story própria com a estratégia (expandir e depois contrair, versão nova, feature flag) — a contração também vira story — ou ponto em aberto para `arch-adr`;
- a prontidão confere se cada contêiner tocado tem um repositório responsável.

## Regras importantes

- Épico = resultado para o usuário; story = fatia vertical que cabe numa sessão. Nunca fatie por camada.
- Todo cenário vigente da especificação é coberto por alguma story antes de fechar o plano.
- Ids de épico e de story nunca são reaproveitados nem renumerados depois de irem para o quadro.
- Nunca altere status no `sprint-status.yaml` além do que o `sync` faz (stories novas em `backlog`).
- Nada é gravado nos repositórios de código. Nunca faça commit nem push.
- Se o usuário não souber algo, registre "a definir" no ponto em aberto e siga.

## Troubleshooting

**Story não cabe numa sessão mas não dá para dividir** — normalmente há uma decisão escondida. Crie um spike antes, ou separe a parte de regra de exceção.

**Escopo sem arquitetura** — siga supondo a arquitetura informada pelo usuário, registre como ponto em aberto e sugira `arch-c4` antes da primeira story.

**Spec sem cenários numerados** (documento antigo ou colado) — proponha numerar os cenários na spec (`#### Cenário N.M`) com a `spec-functional` antes de fatiar; sem isso a cobertura não pode ser verificada.

**Muitos épicos de uma vez** — planeje os 2–3 primeiros em detalhe e deixe os demais só com título e objetivo (sem stories); eles entram no quadro quando forem fatiados.
