# 07 — Plano em épicos fatiados em stories

- **Pedido:** "Planos quero seguir Épicos fatiados em stories, uma spec por story e um arquivo de status" (linha 8)
- **Tamanho:** G
- **Depende de:** 06 (formato do status). A "spec por story" é a tarefa 08.
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Como o BMAD faz
- v6: `create-epics-and-stories` a partir do PRD + arquitetura (+ UX) → `epics.md` com épicos, stories (user story + critérios de aceite em BDD) e cobertura dos requisitos. `check-implementation-readiness` confere PRD × arquitetura × épicos antes de implementar. `sprint-planning` gera o status.
- v7: a PO **refina** o épico (o que já está definido; cada ponto em aberto vira "resolver agora", "spike" ou "deixar para a story"), faz a **incepção** (proposta de stories em ordem de build, com cobertura de requisitos, dependências e verificação) e o humano **revisa a ordem e define checkpoints**. Stories pequenas sem épico vão para `backlog/`.
- Regra de tamanho: uma story cabe numa sessão de implementação.

### Como está hoje
- `plan-execution` (plugin `spec-plan`): um `execution-plan.md` por escopo com **Entregas** (1–3 dias) e tabelas de tarefas **por camada** (Domain, Infra, Application, Presentation, Angular, testes), com estimativas em horas e nomenclatura `[TASK]/[HT]/[FEATURE]`.
- A unidade é a camada técnica, não o incremento de valor; não há critério de aceite por tarefa nem rastreio para os cenários BDD da `spec-functional`.

## Objetivo

Transformar escopo + especificação + arquitetura em **épicos** e **stories verticais** (cada story entrega comportamento testável de ponta a ponta), em ordem de build, alimentando o `sprint-status.yaml`.

## Proposta

1. **Skill `plan-epics`** (plugin `spec-plan`), entradas: `escopo.md`, `spec-functional.md`, `arquitetura.md` + ADRs, `repositorios.md`, `project-config.json`.
2. **Fluxo**:
   1. **Prontidão** (equivalente ao `check-implementation-readiness`): todo cenário BDD tem dono? A arquitetura cobre os contêineres tocados? Há pontos em aberto? Mostra lacunas e pergunta se segue.
   2. **Épicos**: um por resultado coerente para o usuário (não por camada). Cada épico: objetivo, limites (entra/não entra), "pronto quando" verificável, cenários BDD cobertos.
   3. **Refinamento dos pontos em aberto** (da v7): cada um vira *resolver agora*, *spike* (story própria) ou *decidir na story*.
   4. **Stories**: fatias verticais, cada uma cabendo numa sessão; formato "Como / quero / para", critérios de aceite apontando para os cenários da spec (IDs), dependências, repositórios (13), tamanho (P/M/G) e, opcionalmente, as camadas tocadas (mantém o vínculo com as skills `architecture-*`/`angular-*`).
   5. **Ordem de build e checkpoints**: mostra a sequência; o usuário ajusta e marca checkpoints (stories fundacionais/arriscadas que pedem atenção humana antes de seguir).
   6. **Matriz de cobertura**: cenário BDD → story. Cenário sem story = alerta.
3. **Saídas**:
   - `docs/{projeto}/implementacao/epicos/epic-{n}-{slug}.md` — um arquivo por épico (objetivo, limites, pronto quando, lista de stories em ordem, cobertura).
   - Atualiza o `sprint-status.yaml` (06) com épicos e stories em `backlog` — via `sprint-planning`.
   - **Não** cria os arquivos de story (isso é o `create-story`, 08, uma por vez, na hora certa).
4. **`plan-execution` atual**: manter como modo alternativo ("plano por entregas e camadas", útil para Redmine). Opções: (a) skill separada continua existindo; (b) `plan-epics` gera, no fim, a visão por camadas a partir das stories. Recomendação: (a) agora, avaliar (b) depois.
5. **Nomenclatura** `[FEATURE]/[TASK]/[HT]`: épico ↔ `[FEATURE]`, story ↔ `[TASK]`, spike ↔ `[TASK] Analisar e especificar`, habilitador ↔ `[HT]` — configurável (02/04).

## Decisões em aberto

- Nome: `plan-epics`, `plan-stories` ou `epics-and-stories`. plan-epics
- Numeração: `epic-1`, `1-1-slug` (igual ao v6) ou incluir o escopo no ID quando o projeto tem vários escopos (ex.: `prod-1-1-slug`). Recomendação: numeração global no projeto (épicos não reiniciam por escopo). fazer o recomendado
- Estimativa em horas (como hoje) ou só tamanho relativo. estimativa com tamanho relativo
- O que acontece com planos `execution-plan.md` já existentes (migração opcional pelo `migrate.py`, 03). migracao opcional

## Critérios de aceite

- [ ] Skill com Passo 0, `references/` com template de épico, guia de fatiamento vertical (com exemplos bons e ruins) e checklist de prontidão.
- [ ] Testada com o exemplo "Gestão de Produtos" do `plan-execution`: gera épicos e stories verticais e a matriz de cobertura sem cenário órfão.
- [ ] `sprint-status.yaml` criado/atualizado com todas as stories em `backlog`.
- [ ] README (fluxo e tabelas), `CLAUDE.md` (dependências entre skills) e `0.0 - contexto-projeto-skills.md` atualizados.

## Arquivos impactados

`plugins/spec-plan/skills/plan-epics/**` (novo), `plugins/spec-plan/skills/plan-execution/SKILL.md` (descrição "quando NÃO usar"), `spec-functional` (IDs estáveis nos cenários, se ainda não tiver), `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.

## Resultado (30/10/2026)

- **Skill `plan-epics`** (plugin `spec-plan`, que subiu para a 1.1.0), com três modos: Planejar, Atualizar e Migrar.
  - O fluxo segue a proposta: prontidão → épicos → pontos em aberto → stories → ordem e checkpoints → gravar → quadro.
  - Referências: `template-epico.md`, `fatiamento-vertical.md` (exemplos bons e ruins, tamanho P/M/G, tipos `story`/`spike`/`enabler`, ordem com vários repositórios) e `checklist-prontidao.md`.
- **Cobertura determinística:** `_sdd/scripts/epics.py`.
  - `validate`: ids, tamanho, tipo, `covers`, `depends_on` só para trás, e o próximo número de épico.
  - `coverage --escopo`: cruza os cabeçalhos `#### Cenário N.M` e as regras `**RN-N.M**` da spec com os `covers` das stories. Ignora itens `(removido)` e acusa referências que não existem.
- **`spec-functional`:** ganhou a regra de numeração estável (não renumerar; item que deixou de valer fica marcado `(removido)`).
- **Migração opcional:** `execution-plan-para-epicos`, declarada em `modules/spec-plan.toml`, com guia em `sdd-setup/references/migracoes/`. O `migrate.py --all` a lista.
- **`plan-execution`:** continua existindo; a descrição agora aponta o `plan-epics` como caminho padrão.

**Decisões aplicadas:**
- Nome `plan-epics`.
- Numeração global no projeto.
- Tamanho relativo P/M/G em vez de horas.
- Migração opcional.

**Critérios de aceite:**
- Referências e Passo 0: feitos.
- O exemplo "Gestão de Produtos" virou fixture (spec + 2 épicos): `validate` sem problemas, cobertura completa, `sync` gerando o quadro (37 testes).
- O fluxo conversacional da skill ainda não foi rodado numa sessão real: fazer isso no primeiro uso.
- README, `CLAUDE.md` e contexto atualizados.
