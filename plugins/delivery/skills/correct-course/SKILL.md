---
name: correct-course
description: Mudança de rumo no meio da entrega — quando surge algo que muda o plano (requisito novo ou errado, story ambígua que parou o dev-story, decisão da revisão que muda o prometido, limitação técnica, story que não cabe), analisa o impacto em especificação, escopo, arquitetura, épicos, stories e contratos (stories afetadas agrupadas por estado), classifica (menor, moderado, maior), propõe opções com recomendação e as edições antes → depois, grava a proposta em docs/{projeto}/implementacao/mudancas/{data}-{slug}.md e, só após aprovação, aplica — mudanças maiores são encaminhadas às skills donas. Use quando o usuário disser "correct course", "mudança de rumo", "mudou o requisito", "a story não dá", "replanejar", "o cliente pediu outra coisa", "essa story precisa mudar", "cancelar stories", "dividir uma story em andamento". NÃO use para planejar o escopo do zero ou acrescentar épicos antes da implementação (use plan-epics), só mudar o estado de uma story (use sprint-planning) ou corrigir achados da revisão que cabem na story (use dev-story).
metadata:
  version: 1.0.0
  category: plan
  depends-on: plan-epics
  output: docs/{projeto}/implementacao/mudancas/{data}-{slug}.md
---

# Correct Course

Quando o plano encontra a realidade: analisa o impacto de uma mudança, propõe o caminho e só aplica depois da aprovação, deixando o histórico em todos os artefatos tocados. Inspirado no `correct-course` do BMAD v6 (*Sprint Change Proposal*). Mudanças de regra de negócio, escopo ou arquitetura são **encaminhadas** às skills donas, não editadas por fora.

Leia antes de executar: `references/template-proposta.md` (proposta e tabela de classificação) e `sdd-setup/references/sprint-status.md` (plugin `sdd`; transições).

---

## Passo 0 — Identificar o projeto

A raiz de trabalho é uma pasta de documentação com vários projetos, cada um em `docs/{projeto}/`.

1. Se o usuário citou o projeto, use a pasta dele.
2. Senão, leia `docs/workspace.md`: com um único projeto, use-o e avise; com vários, liste e pergunte qual.
3. Sem `docs/workspace.md`, procure `docs/*/project.md`.
4. Se o projeto não existir, ofereça iniciá-lo com `discovery-init`.
5. Leia `docs/{projeto}/project-config.json` (nome, stack, repositório; ver o schema em `discovery-init/references/project-config-schema.md`). Se não existir, use o `project.md` e ofereça criar o config a partir dele.
6. Leia a configuração do workspace, se existir: `_sdd/config.toml` e `_sdd/config.user.toml` na raiz (o pessoal vence; chaves em `sdd-setup/references/config-schema.md`). Converse em `language.conversation`, escreva os documentos em `language.documents`, chame o usuário por `user.name` e ajuste as explicações a `user.skill_level`; se `paths.docs_root` não for `docs`, use-o no lugar de `docs/` em todos os caminhos. Sem `_sdd/`, use os padrões (pt-BR, nível intermediário, `docs/`) e sugira uma vez rodar o `sdd-setup`, sem bloquear.

`{projeto}` é a pasta escolhida; todos os caminhos abaixo são relativos à raiz de trabalho. Chamada a partir do `dev-story` ou do `story-review` (no repositório de código), localize o workspace como eles fazem.

## Customização (por projeto)

Depois de identificar o projeto, resolva a customização desta skill:

```
uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto}
```

Sem o script (ou sem `uv`/`python`): leia `${CLAUDE_SKILL_DIR}/customize.toml` e, se existir, `docs/{projeto}/_custom/correct-course.toml`, e mescle pelas regras de `sdd-setup/references/customizacao.md`. Sem override, valem os padrões da skill.

1. Execute os `workflow.activation_steps_prepend`, na ordem.
2. Leia os arquivos de `facts` (e os textos literais): são fatos válidos durante toda a skill e vencem os padrões dela quando conflitarem.
3. Use os valores de `resolved.workflow` onde esta skill os cita: `approvers` (quem aprova cada escopo, na proposta).
4. Ao terminar, execute os `workflow.activation_steps_append` e o `workflow.on_complete`.

Mostre os `warnings` ao usuário uma vez (ex.: chave que não é customizável, override que repete a base).

## Scripts

```
uv run _sdd/scripts/status.py --project docs/{projeto} show
uv run _sdd/scripts/epics.py  --project docs/{projeto} impact [--escopo {escopo}] {ids da spec que mudaram}
uv run _sdd/scripts/epics.py  --project docs/{projeto} validate | coverage --escopo {escopo}
uv run _sdd/scripts/status.py --project docs/{projeto} set {id} {estado}
uv run _sdd/scripts/status.py --project docs/{projeto} sync [--dry-run]
```

Sem `uv`: `python` 3.11+ com `pyyaml`; sem nenhum, procure as stories afetadas pelo `covers` no frontmatter dos épicos e edite o `sprint-status.yaml` como em `sprint-status.md` ("Sem `uv`").

---

## Fluxo

### Passo 1 — Gatilho

Registre o que aconteceu, quem levantou e a evidência (story e seção, bloco de revisão, cenário da spec, mensagem). Chamada pelo `dev-story` ou `story-review`: leia o Registro/Revisão da story que parou. Se a "mudança" for só um achado que cabe na story (o prometido não muda), diga isso e devolva para `dev-story`/`story-review` — não é mudança de rumo.

### Passo 2 — Impacto

1. **Quadro:** `status.py show`.
2. **Stories afetadas:** se a mudança toca cenários ou regras da spec, rode `epics.py impact` com esses ids — a saída agrupa por estado (`done`, `in-progress`, `review`, `ready-for-dev`, `backlog`). Senão, identifique pelas descrições, repositórios e contratos. `not_covered`: id sem story (cenário novo) → story nova.
3. **Artefatos:** spec, escopo, arquitetura/ADRs, épicos e, com vários repositórios, contratos e o que já foi mergeado/publicado (`repositorios.md`, `mudanca-multi-repo.md` da story).
4. Mostre a tabela de impacto.

### Passo 3 — Classificar e propor

Classifique pela tabela do template (**menor**, **moderado**, **maior**). Proponha 2–3 opções com prós, contras e esforço, e recomende uma. Regras para as stories:
- `done`: **nunca reabra**; crie uma story de ajuste (próximo `m` livre no épico em andamento, ou no épico da story se ele ainda estiver aberto).
- `in-progress` / `review` com critério que muda: volta para `backlog` (de `review`: passe por `in-progress`) e o arquivo é regenerado pelo `create-story`; o código já feito na branch é avaliado no próprio `create-story` (reaproveitar ou descartar — descartar só com o usuário).
- `ready-for-dev`: volta para `backlog` e é regenerada.
- `backlog`: ajuste no épico.
- Cancelada: `dropped` (nunca apague do épico nem do quadro).

### Passo 4 — Proposta

Escreva `implementacao/mudancas/{AAAA-MM-DD}-{slug}.md` pelo template, com `status: proposta`, as edições **antes → depois** por arquivo e o efeito no quadro. Mostre um resumo e peça a aprovação (ou ajustes, ou rejeição — `status: rejeitada`, com o motivo).

### Passo 5 — Aplicar (só com `status: aprovada`)

Marque `aprovada` (data e quem, na tabela de aprovação) e aplique conforme o escopo:

- **Menor:** edite o arquivo da story (critério esclarecido, Decisões em aberto resolvidas) e acrescente no Histórico `correct-course: {resumo} — mudancas/{arquivo}`. Rode `story.py check`. A story continua no estado em que estava.
- **Moderado:**
  1. edite os arquivos de épico (story nova, divisão, reordenação; cancelada marcada `(cancelada)` no corpo) sem mudar ids existentes; rode `epics.py validate` e, se a spec é a mesma, `coverage`;
  2. `status.py sync --dry-run` → mostre → `sync`;
  3. aplique as transições do efeito no quadro com `status.py set` (uma por uma, mostrando cada uma);
  4. Histórico em cada story afetada.
- **Maior:** marque `status: encaminhada` e encaminhe, nesta ordem, às skills donas: `spec-functional` (regra/cenário — sem renumerar), `discovery-scoped` (escopo), `arch-c4`/`arch-adr` (arquitetura, decisão). Depois que elas rodarem, volte aqui e aplique a parte moderada (épicos, stories, quadro) pelo `plan-epics` (modo Atualizar) ou pelos passos acima.

Vários repositórios: contrato incompatível precisa da estratégia (expandir e depois contrair, versão nova, feature flag) registrada na proposta e nas stories; o que já foi publicado no provedor não pode ser removido antes de os consumidores migrarem.

### Passo 6 — Fechar

Marque `status: aplicada` (ou `encaminhada` enquanto faltar a skill dona), atualize a Situação do `workspace.md` com o `situacao` de `status.py show` e diga o próximo passo (`status.py next`): normalmente `create-story` para regenerar ou criar as stories afetadas, ou retomar o `dev-story` se a mudança era menor.

---

## Vários repositórios

No impacto, leia os `implementacao/multi-repo/{id}.md` das stories afetadas: o que já foi mergeado e publicado em cada repositório e ambiente. Contrato já publicado não pode ser removido nem mudado de forma incompatível sem estratégia (expandir e depois contrair, versão nova, feature flag) e sem os consumidores migrarem — registre a estratégia na proposta e crie as stories de expansão e de contração. Mudança que exige repositório novo ou troca de responsabilidade entre repositórios é **maior**: encaminhe para `multi-repo` (Cadastrar) e `arch-adr`.

## Regras importantes

- Nada muda antes da aprovação; a proposta fica registrada mesmo quando rejeitada.
- Story `done` nunca é reaberta; ids nunca são reaproveitados; nada é apagado do quadro (`dropped` é o histórico).
- Spec, escopo, arquitetura e ADRs mudam pelas skills donas — esta skill encaminha.
- Toda story afetada ganha uma linha no Histórico apontando a proposta.
- Nada é alterado nos repositórios de código (código já feito é avaliado pelo `create-story`/`dev-story`).

## Troubleshooting

**Mudança descoberta na revisão de uma story quase pronta** — se o comportamento prometido não muda, não é correct-course: é correção da revisão. Se muda, classifique normalmente; a story volta para `backlog` (via `in-progress`) e o que já está implementado é aproveitado ao regenerar.

**Várias mudanças pequenas seguidas** — uma proposta por gatilho; se elas se repetem num épico, traga para a retrospectiva (sinal de spec ou fatiamento fraco).

**Contrato já publicado em produção** — a proposta precisa de plano de compatibilidade com data de remoção do contrato antigo; sem ele, classifique como maior e envolva o `arch-adr`.
