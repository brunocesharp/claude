# 12 — Correct course (mudança de rumo)

- **Pedido:** "Verificação e fechamento quero seguir ... correct course" (linha 10)
- **Tamanho:** M
- **Depende de:** 06, 07, 08
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Como o BMAD faz
- v6 (`correct-course`): usado quando, no meio do sprint, surge algo que muda o plano (requisito novo ou errado, limitação técnica, story que não cabe, descoberta na revisão). Passos: identificar o gatilho → analisar impacto em épicos, stories, PRD, arquitetura, UX → avaliar caminhos (ajuste direto, rollback, revisão do MVP) → gerar **Sprint Change Proposal** com as edições propostas em cada artefato → classificar o escopo (**menor**: o dev resolve; **moderado**: reorganizar backlog; **maior**: replanejamento com PM/arquiteto) → aplicar após aprovação e atualizar o status.
- v7: não há skill própria; o usuário avisa a PO, que atualiza os requisitos e refatia as stories restantes, registrando linhas `Decision:` datadas nas notas.

### Como está hoje
- Nada equivalente. Mudança no meio da execução = editar o plano à mão.

## Objetivo

Skill `correct-course` que analisa o impacto de uma mudança, propõe as alterações em todos os artefatos afetados e só aplica após aprovação, mantendo o histórico.

## Proposta

1. **Gatilhos**: chamada direta ("mudou o requisito X", "essa story não dá") ou sugerida por `dev-story` (09, story ambígua/contraditória), `code-review` (10, decisão necessária com impacto) e `retrospective` (11).
2. **Análise de impacto** (lê o que existir): stories `in-progress`/`ready-for-dev`/`backlog` afetadas, épicos, `spec-functional`, `escopo.md`, `arquitetura.md` + ADRs, `repositorios.md`/contratos (13), código já entregue (`done`).
3. **Classificação**:
   | Escopo | Exemplo | Quem decide | O que muda |
   |--------|---------|-------------|------------|
   | Menor | Detalhe de critério de uma story | Dev | Story file |
   | Moderado | Story nova, divisão, reordenação, cancelamento | Responsável pelo backlog | Épico, stories, status |
   | Maior | Regra de negócio, contêiner novo, escopo | PO / arquiteto | Spec, escopo, arquitetura/ADR, épicos |
4. **Proposta** (`docs/{projeto}/implementacao/mudancas/{data}-{slug}.md`): gatilho, evidência, impacto por artefato, opções com recomendação, edições propostas (antes → depois) por arquivo, efeito no `sprint-status.yaml` (stories novas, `dropped`, voltando para `backlog`), riscos para o que já está `done`.
5. **Aplicação**: só após aprovação; edita os artefatos, atualiza status via `status.py`, registra no "Histórico" de cada story afetada e, para mudanças maiores, encaminha para a skill dona (`spec-functional`, `arch-adr`, `arch-c4`, `plan-epics`) em vez de editar por fora.
6. Stories já `done` afetadas: não reabre; cria story de ajuste.

## Decisões em aberto

- Nome em português (`mudanca-de-rumo`) ou manter `correct-course` (reconhecível para quem conhece o BMAD). manter
- Mudanças maiores: a skill aplica ou só encaminha para a skill dona. Recomendação: só encaminha. recomendado

## Critérios de aceite

- [ ] Skill com template da proposta e tabela de classificação em `references/`.
- [ ] Teste: mudar um cenário BDD que afeta uma story `done`, uma `ready-for-dev` e uma `backlog` — proposta cobre as três corretamente.
- [ ] Nada é alterado antes da aprovação.

## Arquivos impactados

`plugins/<delivery>/skills/correct-course/**` (novo), `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.

## Resultado (30/10/2026)

**Skill `correct-course`** (plugin `delivery`). Etapas:
1. **Gatilho:** se o prometido não muda, devolve para `dev-story`/`story-review`.
2. **Impacto:** quadro, `epics.py impact`, artefatos e contratos/merges.
3. **Classificar e propor:** opções com recomendação.
4. **Proposta** em `mudancas/`, com `status: proposta`.
5. **Aplicar só com `aprovada`:**
   - **menor:** edita a story;
   - **moderado:** épicos, `validate`/`coverage`, `sync`, transições e Histórico;
   - **maior:** `encaminhada` às skills donas e depois a parte moderada.
6. **Fechar:** `aplicada` e próximo passo.

**Regras das stories:**
- `done` nunca reabre; vira uma story de ajuste.
- `in-progress`, `review` e `ready-for-dev` voltam para `backlog` e são regeneradas pelo `create-story`.
- Canceladas viram `dropped`, sem apagar nada.

**Script `epics.py impact`:** recebe os ids de cenários ou regras que mudaram e devolve as stories afetadas agrupadas por estado, mais os ids sem story (cenário novo). A `retrospective` lê as propostas de `mudancas/` pelo frontmatter (`scope`, `status`).

**Template:** `references/template-proposta.md`, com proposta e tabela de classificação (menor, moderado ou maior; quem decide; o que muda).

**Decisões aplicadas:** nome `correct-course`; mudanças maiores só encaminhadas às skills donas.

**Critérios de aceite:**
- Template e tabela de classificação: feitos.
- O impacto de um cenário que afeta stories `done`, `in-progress` e `backlog` é coberto por teste no script (54 testes).
- A redação da proposta é do modelo: verificar no primeiro uso.
- Nada é alterado antes da aprovação: regra explícita, com o passo 5 condicionado a `status: aprovada`.
