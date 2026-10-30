# 05 — Pesquisa de mercado e concorrentes

- **Pedido:** "para Ideia / pesquisa quero implementar no meu pesquisa de mercado, concorrentes fortes" (linha 7)
- **Tamanho:** M
- **Depende de:** `discovery-init` (já existe). Independente das demais tarefas.
- **Situação:** [ ] a fazer

## Contexto

### Como o BMAD faz
- v6: workflow de pesquisa com três tipos — **mercado** (tamanho, segmentos, tendências), **domínio** (regras, regulação, terminologia) e **técnica** (opções de tecnologia) — conduzido pela analista, com busca na web.
- v7: `bmad-deep-recon` gera `research-<tema>.md` **com citações**; `bmad-forge-idea` e `bmad-brainstorming` para lapidar a ideia; `bmad-product-brief` consolida.

### Como está hoje
- Discovery: `vision`, `opportunity`, `assumptions`, `stakeholders`, `metrics`, `scoped`. Nenhuma skill busca fontes externas; concorrência e mercado não aparecem em nenhum template.

## Objetivo

Skill `discovery-research` que faz pesquisa de **mercado** e de **concorrentes** com fontes citadas, e alimenta as skills de discovery seguintes.

## Proposta

1. **Skill `discovery-research`** (plugin `discovery`), com modos:
   - **Mercado**: tamanho e crescimento (TAM/SAM/SOM quando houver dado), segmentos, tendências, regulação relevante, sinais de demanda.
   - **Concorrentes**: identificar concorrentes diretos, indiretos e substitutos; para os **fortes** (critério explícito: participação, financiamento, base de clientes, presença no segmento-alvo) aprofundar: proposta de valor, público, preço/modelo, funcionalidades-chave, pontos fortes e fracos, avaliações públicas de usuários, movimentos recentes.
   - **Domínio** e **técnica** (opcionais, mesmo formato) — avaliar se entram já ou depois.
2. **Fluxo**: perguntas de enquadramento (pergunta de pesquisa, região, segmento, horizonte, concorrentes já conhecidos) → plano de busca mostrado ao usuário → busca (WebSearch/WebFetch; `extended` para dados de mercado e preços) → síntese → arquivo.
3. **Saídas** em `docs/{projeto}/discovery/pesquisa/`:
   - `mercado-{tema}.md`
   - `concorrentes.md` — matriz comparativa (concorrente × critérios) + ficha de cada concorrente forte + posicionamento (mapa 2×2 em Mermaid `quadrantChart`) + lacunas/oportunidades de diferenciação.
   - Cada afirmação com fonte (link + data de acesso); dado sem fonte marcado como estimativa; seção "Limites da pesquisa".
4. **Integração**: `discovery-vision` (proposta de valor e diferenciação), `discovery-opportunity` (dores não atendidas pelos concorrentes), `discovery-assumptions` (premissas de mercado viram hipóteses a validar) e `discovery-scoped` (snapshot da pesquisa no escopo) passam a ler a pasta `pesquisa/` quando existir.
5. **Atualização**: rodar de novo atualiza o arquivo com seção "Revisões" (data e o que mudou), sem apagar a versão anterior das fichas.

## Decisões em aberto

- Incluir já os modos domínio e técnica, ou só mercado + concorrentes. Só mercado + concorrentes
- Usar `anthropic-skills:deep-research` (se disponível) como motor, ou a skill faz a busca diretamente. Recomendação: a skill faz a busca diretamente (não depender de skill externa ao marketplace). fazer o recomendado
- Critério de "concorrente forte" configurável via customização (04). sim

## Critérios de aceite

- [ ] `plugins/discovery/skills/discovery-research/SKILL.md` com Passo 0 e frontmatter válido; `references/` com templates de mercado e de concorrentes e o guia de fontes/citação.
- [ ] Nenhuma afirmação quantitativa sem fonte ou sem marca de estimativa.
- [ ] Skills de discovery citadas no item 4 leem a pesquisa quando existir.
- [ ] README (tabela do discovery + fluxo) e `0.0 - contexto-projeto-skills.md` atualizados.

## Arquivos impactados

`plugins/discovery/skills/discovery-research/**` (novo), `discovery-vision`, `discovery-opportunity`, `discovery-assumptions`, `discovery-scoped`, `README.md`, `0.0 - contexto-projeto-skills.md`, `CLAUDE.md` (estrutura `docs/{projeto}/discovery/pesquisa/`).
