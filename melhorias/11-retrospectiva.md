# 11 — Retrospectiva de épico

- **Pedido:** "Verificação e fechamento quero seguir ... retrospectiva" (linha 10)
- **Tamanho:** M
- **Depende de:** 06, 08, 10
- **Situação:** [ ] a fazer

## Contexto

### Como o BMAD faz
- v6 (`retrospective`): ao fim do épico, lê todas as stories (registros e revisões), levanta o que foi bem, o que não foi, lições, confere se os itens da retrospectiva anterior foram feitos, prepara o próximo épico (dependências, ajustes de arquitetura) e marca `epic-N-retrospective: done` no status.
- v7 (`bmad-retrospective`): roda quando todos os tickets estão finalizados (`built`/`done`/`dropped`); lê `tickets.toml`, o "pronto quando" do épico, requisitos cobertos (`covers`), planos e revisões, **histórico do git** desde a linha de base de cada story e a retrospectiva anterior. Gera `epic-<slug>-retrospective.md` com inventário de evidências, achados com fonte, **veredito** (`accepted` / `accepted-with-open-items` / `rejected`) e itens de ação propostos. ADRs só após aprovação. "Lê evidências, não as inventa." Não marca o épico como concluído — o humano confirma.

### Como está hoje
- Nada equivalente. O `execution-plan.md` tem DoD por entrega, sem fechamento formal.

## Objetivo

Skill `retrospective` que fecha um épico com base em evidências, decide se o próximo pode começar e alimenta o ciclo com itens de ação.

## Proposta

1. **Entrada**: ID do épico (sem ID: o épico com todas as stories `done`/`dropped` e retrospectiva `optional`). Se houver story pendente, lista e pergunta se segue (veredito tende a `rejected`).
2. **Evidências**: épico (pronto quando, cenários cobertos), cada story (critérios, registro, revisões, itens adiados), `git log`/diff de cada repositório desde o início do épico, retrospectiva anterior, mudanças de rumo (12) do período.
3. **Conteúdo** (`docs/{projeto}/implementacao/retrospectivas/epic-{n}-{data}.md`):
   - Inventário de evidências; checagem do "pronto quando" item a item.
   - O que funcionou / o que não funcionou / surpresas, cada um com a fonte (story, revisão, commit).
   - Seguimento dos itens da retrospectiva anterior.
   - Reconciliação com a especificação: o que foi implementado diferente da spec/arquitetura (propõe atualizar `spec-functional`, `arch-c4` ou um ADR via `arch-adr` — só com aprovação).
   - Preparação do próximo épico: dependências, riscos, ajustes nas stories ainda em `backlog`.
   - **Veredito** no frontmatter: `accepted` / `accepted-with-open-items` / `rejected`.
   - Itens de ação: cada um vira story nova, ajuste no próximo épico ou tarefa de processo (com confirmação).
4. **Modo conversa** (opcional): perguntas ao time antes de fechar (o pedido não exige; vem do v6).
5. **Estado**: `epic-N.retrospective: done`; o épico vai para `done` **só após confirmação** do usuário; atualiza `project.md`/`workspace.md`.

## Decisões em aberto

- Retrospectiva obrigatória para fechar o épico ou opcional (v6: opcional). opicional
- Ler histórico do git exige caminho local dos repositórios — sem ele, segue só com os arquivos e avisa. Ler historico do git opicional

## Critérios de aceite

- [ ] Skill com template e regras de evidência (nenhum achado sem fonte).
- [ ] Teste com épico de exemplo de 3 stories: veredito coerente, itens de ação, seguimento da retrospectiva anterior.
- [ ] Nenhum artefato (spec, ADR, épico) alterado sem confirmação.

## Arquivos impactados

`plugins/<delivery>/skills/retrospective/**` (novo), `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.
