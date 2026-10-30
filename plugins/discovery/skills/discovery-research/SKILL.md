---
name: discovery-research
description: Conduz pesquisa de mercado e de concorrentes com fontes citadas durante o discovery, gerando docs/{projeto}/discovery/pesquisa/mercado-{tema}.md (tamanho, segmentos, tendências, regulação, sinais de demanda) e docs/{projeto}/discovery/pesquisa/concorrentes.md (concorrentes diretos, indiretos e substitutos, fichas dos concorrentes fortes, matriz comparativa, posicionamento e lacunas de diferenciação). Toda afirmação com fonte (link e data de acesso) ou marcada como estimativa. Use quando o usuário mencionar "pesquisa de mercado", "tamanho do mercado", "TAM SAM SOM", "concorrentes", "concorrência", "análise competitiva", "benchmark", "quem já faz isso", "concorrentes fortes", "comparar com o mercado", "existe mercado para isso", "como os outros cobram". Requer discovery-init. NÃO use para visão (use discovery-vision), dores e jobs to be done (use discovery-opportunity), hipóteses (use discovery-assumptions) ou pesquisa técnica de bibliotecas e frameworks.
metadata:
  version: 1.0.0
  category: discovery
  depends-on: discovery-init
  output: docs/{projeto}/discovery/pesquisa/mercado-{tema}.md, docs/{projeto}/discovery/pesquisa/concorrentes.md
---

# Discovery Research

Pesquisa de **mercado** e de **concorrentes** com busca na web e fontes citadas, para que visão, oportunidades e hipóteses partam de evidência externa e não só da percepção do time. Inspirada na pesquisa de mercado/domínio do BMAD v6 e no `bmad-deep-recon` da v7 (pesquisa com citações).

Leia antes de executar:
- `references/guia-fontes.md` — citação, qualidade das fontes, divergência e limites.
- `references/template-mercado.md` e `references/template-concorrentes.md` — os documentos.

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

Leia também, se existirem, `discovery/vision.md` e `discovery/opportunity.md` (público e problema orientam a busca) e a pasta `discovery/pesquisa/` (pesquisa anterior: modo atualização).

## Customização (por projeto)

Depois de identificar o projeto, resolva a customização desta skill:

```
uv run _sdd/scripts/customize.py --skill-dir "${CLAUDE_SKILL_DIR}" --project docs/{projeto}
```

Sem o script (ou sem `uv`/`python`): leia `${CLAUDE_SKILL_DIR}/customize.toml` e, se existir, `docs/{projeto}/_custom/discovery-research.toml`, e mescle pelas regras de `sdd-setup/references/customizacao.md`. Sem override, valem os padrões da skill.

1. Execute os `workflow.activation_steps_prepend`, na ordem.
2. Leia os arquivos de `facts` (e os textos literais): são fatos válidos durante toda a skill e vencem os padrões dela quando conflitarem.
3. Use os valores de `resolved.workflow` onde esta skill os cita: `default_region` (Passo 1), `known_competitors` (Passo 4), `strong_competitor_criteria` e `min_criteria` (critério de concorrente forte, Passo 4) e `max_strong_competitors` (quantas fichas, Passo 4).
4. Ao terminar, execute os `workflow.activation_steps_append` e o `workflow.on_complete`.

Mostre os `warnings` ao usuário uma vez (ex.: chave que não é customizável, override que repete a base).

## Script

```
uv run _sdd/scripts/research.py check docs/{projeto}/discovery/pesquisa/{arquivo}.md
```

Confere citações: número sem `[n]` nem marca de estimativa, `[n]` sem fonte, fonte sem link ou sem data. Sem o script: faça a mesma conferência lendo o documento (regras em `guia-fontes.md`).

---

## Fluxo

### Passo 1 — Enquadrar

Pergunte o que faltar, uma pergunta por vez:
1. **Modo:** mercado, concorrentes ou os dois (padrão: os dois, concorrentes primeiro se o mercado já é conhecido).
2. **Pergunta de pesquisa:** que decisão a pesquisa vai apoiar (ex.: "vale entrar nesse segmento?", "como nos diferenciar?").
3. **Recorte:** região (padrão `default_region`), segmento/público, horizonte de tempo.
4. **O que o time já sabe:** concorrentes conhecidos, números que já circulam (vão ser checados, não aceitos).

### Passo 2 — Plano de busca

Mostre o plano antes de buscar: perguntas específicas, termos de busca (em português e, se o mercado for global, em inglês), tipos de fonte (ver a tabela de qualidade) e o que conta como "concorrente forte" (critérios do customize, que o usuário pode ajustar para esta pesquisa). Peça ok.

### Passo 3 — Mercado (se no modo)

Busque com a ferramenta de busca na web disponível e abra as páginas (não cite resultado de busca sem ler a página). Para dados de mercado, preços e números recentes, use o modo de busca mais completo, se a ferramenta oferecer. Levante: tamanho (TAM/SAM/SOM quando houver dado; senão, os indicadores disponíveis), segmentos, tendências, sinais de demanda, regulação. Calcule SAM/SOM só com premissas explícitas e marque como estimativa.

### Passo 4 — Concorrentes (se no modo)

1. **Panorama:** liste diretos, indiretos e substitutos (inclua os `known_competitors` e os que o usuário citou), com proposta, público, modelo/preço e fonte.
2. **Fortes:** aplique os `strong_competitor_criteria` (forte = atende a pelo menos `min_criteria`), mostre a classificação com o motivo e confirme com o usuário. Aprofunde no máximo `max_strong_competitors`.
3. **Fichas:** para cada forte — proposta de valor, público, preço e planos, funcionalidades-chave, pontos fortes e fracos (temas recorrentes em avaliações públicas), movimentos recentes, tamanho e tração (marcando o que é "declarado" pelo próprio concorrente).
4. **Matriz** comparativa e **posicionamento** (`quadrantChart`, com os eixos escolhidos com o usuário e a explicação de que as posições são qualitativas).
5. **Lacunas:** dores e públicos que nenhum concorrente forte atende bem, com a evidência.

### Passo 5 — Escrever e conferir

Grave pelo template em `discovery/pesquisa/` (crie a pasta). Rode `research.py check` em cada arquivo e corrija todos os `problems` (citar, marcar como estimativa ou remover a afirmação). Mostre um resumo: conclusões, concorrentes fortes, lacunas, limites da pesquisa.

### Passo 6 — Encaminhar

> "Pesquisa salva em `docs/{projeto}/discovery/pesquisa/`. Ela alimenta:
> - **Visão** (`discovery-vision`): diferenciação e público;
> - **Oportunidades** (`discovery-opportunity`): dores não atendidas pelos concorrentes;
> - **Hipóteses** (`discovery-assumptions`): {N} premissas de mercado que a pesquisa não confirmou.
> Por onde quer seguir?"

Atualize `docs/{projeto}/project.md` só se a fase Discovery ainda não estiver marcada como em andamento.

---

## Modo atualização

Com pesquisa anterior em `discovery/pesquisa/`: pergunte o que atualizar (preços, novo concorrente, números do ano). Não apague fichas nem fontes antigas: atualize com a nova data e a nova fonte, registre o antes e o depois e acrescente uma linha em **Revisões**. Concorrente encerrado fica com "(encerrado em {data}) [n]".

## Regras importantes

- Toda afirmação de fato externo tem fonte `[n]` com link e data de acesso, ou é marcada como estimativa com o cálculo. Nunca cite o que não leu.
- Números que o time trouxe são checados como qualquer outro; sem fonte, viram estimativa ou hipótese.
- Percepção não é dado: avaliações de usuários servem para temas recorrentes, não para números.
- Escreva "Limites da pesquisa" sempre: o que não foi possível saber vira hipótese.
- Só grava em `docs/{projeto}/discovery/pesquisa/`. Não altere os outros documentos de discovery: eles leem a pesquisa quando forem rodados.

## Troubleshooting

**Mercado sem dado público** (nicho, B2B fechado) — diga isso, use indicadores indiretos (número de empresas do segmento, vagas, buscas) marcados como estimativa e proponha pesquisa primária (entrevistas) como hipótese a validar.

**Concorrente sem preço público** — registre "preço sob consulta" com a fonte da página; se houver preço em fonte secundária, cite-a como tal.

**Busca na web indisponível** — não invente: ofereça montar o plano de busca e o template para o time preencher, ou trabalhar com fontes que o usuário enviar (links ou arquivos).
