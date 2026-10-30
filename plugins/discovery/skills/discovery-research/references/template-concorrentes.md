# Template: `docs/{projeto}/discovery/pesquisa/concorrentes.md`

````markdown
---
tipo: concorrentes
regiao: {região}
segmento: {segmento}
atualizado_em: {AAAA-MM-DD}
---

# Concorrentes

## Pergunta de pesquisa

{Ex.: "Quem já resolve a gestão de estoque de pequenas lojas, como, por quanto, e onde há espaço para diferenciação?"}

## Resumo

- {3 a 5 conclusões com [n]}

## Panorama

| Concorrente | Tipo | Proposta em uma frase | Público | Modelo / preço | Forte? | Fonte |
|-------------|------|-----------------------|---------|----------------|--------|-------|
| {nome} | direto | {...} | {...} | {R$ X/mês — plano Y} | sim | [n] |
| {nome} | indireto | | | | não | [n] |
| {planilha, processo manual} | substituto | | | | — | [n] |

- **Direto:** resolve o mesmo problema para o mesmo público.
- **Indireto:** resolve o mesmo problema para outro público, ou parte dele.
- **Substituto:** o que as pessoas usam hoje no lugar (planilha, ERP genérico, papel, não fazer).

**Critério de "forte"** usado: {critérios do customize / combinados com o usuário}.

## Matriz comparativa (concorrentes fortes)

| Critério | {Concorrente A} | {Concorrente B} | {Nós — proposta} |
|----------|-----------------|-----------------|------------------|
| Preço de entrada | {R$ ...} [n] | | {a definir} |
| {funcionalidade-chave 1} | sim [n] | não [n] | |
| {funcionalidade-chave 2} | | | |
| Integrações | | | |
| Avaliação média dos usuários | {4,2/5 — N avaliações} [n] | | — |

## Fichas dos concorrentes fortes

### {Concorrente A}

- **Proposta de valor:** {...} [n]
- **Público:** {...} [n]
- **Modelo e preço:** {planos e valores, data de acesso} [n]
- **Funcionalidades-chave:** {...} [n]
- **Pontos fortes:** {com evidência} [n]
- **Pontos fracos:** {temas recorrentes nas avaliações, limitações declaradas} [n]
- **Movimentos recentes:** {lançamentos, rodadas, aquisições, últimos 12–24 meses} [n]
- **Tamanho e tração:** {clientes, funcionários, receita — "declarado" quando vier do próprio concorrente} [n]

## Posicionamento

```mermaid
quadrantChart
    title {Eixo de valor x eixo de preço, por exemplo}
    x-axis {Baixo} --> {Alto}
    y-axis {Baixo} --> {Alto}
    quadrant-1 {rótulo}
    quadrant-2 {rótulo}
    quadrant-3 {rótulo}
    quadrant-4 {rótulo}
    {Concorrente A}: [0.7, 0.8]
    {Concorrente B}: [0.3, 0.6]
```

{Explique os eixos e de onde vem a posição de cada um — as posições são uma leitura qualitativa das fichas, não medidas.}

## Lacunas e oportunidades de diferenciação

- {dor que nenhum concorrente forte resolve bem} — evidência: {avaliações [n], ausência na matriz}
- {público mal atendido} — evidência: {...}

## Implicações para o projeto

- **Visão (diferenciação):** {...}
- **Oportunidades (dores não atendidas):** {...}
- **Hipóteses a validar:** {...}

## Limites da pesquisa

- {...}

## Revisões

| Data | O que mudou |
|------|-------------|
| {AAAA-MM-DD} | Primeira versão |

## Fontes

- [1] {título} — {URL} — acessado em {AAAA-MM-DD}
````

## Atualização

Rodando de novo, **não apague fichas**: atualize os dados com a nova data e as novas fontes, marque o que mudou (ex.: "preço subiu de R$ 79 para R$ 99 [7]; antes: [2]") e registre em Revisões. Concorrente que saiu do mercado fica com "(encerrado em {data}) [n]".
