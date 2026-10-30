# Template: `docs/{projeto}/discovery/pesquisa/mercado-{tema}.md`

```markdown
---
tipo: mercado
tema: {tema}
regiao: {região}
segmento: {segmento}
atualizado_em: {AAAA-MM-DD}
---

# Pesquisa de mercado — {tema}

## Pergunta de pesquisa

{O que queremos saber e para qual decisão. Ex.: "O mercado de gestão de estoque para pequenas lojas no Brasil é grande e crescente o bastante para um produto por assinatura?"}

## Resumo

- {3 a 5 conclusões, cada uma com [n] ou marca de estimativa}

## Tamanho do mercado

| Medida | Valor | Ano | Como | Fonte |
|--------|-------|-----|------|-------|
| TAM — mercado total | {valor} | {ano} | {de cima para baixo / de baixo para cima} | [n] |
| SAM — alcançável pelo nosso modelo | {valor} | | {recorte aplicado} | [n] ou (estimativa: ...) |
| SOM — fatia realista em {N} anos | {valor} | | {premissa} | (estimativa: ...) |

{Sem dado para TAM/SAM/SOM: diga isso e use os indicadores disponíveis (número de empresas do segmento, gasto médio). Não invente.}

## Segmentos

| Segmento | Tamanho | Características | O que valorizam | Fonte |
|----------|---------|-----------------|-----------------|-------|

## Tendências e sinais de demanda

- {tendência} — {evidência} [n]
- {sinal de demanda: buscas, vagas, investimentos, crescimento de categoria} [n]

## Regulação e restrições

- {norma, exigência, mudança prevista} [n] — {impacto no produto}

## Implicações para o projeto

- **Para a visão (público e proposta de valor):** {...}
- **Oportunidades:** {...}
- **Hipóteses a validar** (vão para o `discovery-assumptions`): {premissa de mercado que esta pesquisa não confirmou}

## Limites da pesquisa

- {o que não foi possível saber e por quê}

## Revisões

| Data | O que mudou |
|------|-------------|
| {AAAA-MM-DD} | Primeira versão |

## Fontes

- [1] {título} — {URL} — acessado em {AAAA-MM-DD}
```
