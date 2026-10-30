# Guia de fontes e citação

## Citação

- Toda afirmação de fato externo (número, preço, participação, data de lançamento, funcionalidade de concorrente) cita a fonte: `[n]` no fim da frase ou da célula da tabela.
- Na seção `## Fontes`, uma linha por fonte: `- [n] {título ou descrição} — {URL} — acessado em {AAAA-MM-DD}`.
- Número sem fonte só entra marcado: `(estimativa: {como foi calculada})`. Ex.: "cerca de 40 mil clientes (estimativa: 2 mil revendas × 20 clientes, a partir de [3] e [4])".
- Use o texto da fonte, não a sua lembrança. Se a página não abriu, a fonte não serve — não cite o que não leu.
- O `research.py check` confere: número sem `[n]` nem estimativa, `[n]` sem fonte, fonte sem link ou sem data.

## Qualidade das fontes (da mais à menos confiável)

| Tipo | Exemplos | Cuidado |
|------|----------|---------|
| Dado oficial e regulatório | IBGE, Banco Central, agências reguladoras, diários oficiais, relatórios anuais auditados | Confira o ano de referência |
| Pesquisa setorial | Associações do setor, consultorias com metodologia publicada | Vieses do patrocinador; prefira a que publica a metodologia |
| Fonte primária do concorrente | Site, página de preços, documentação, notas de versão, vagas abertas, relatório a investidores | É o que o concorrente diz de si: marque como "declarado" |
| Imprensa especializada | Veículos de negócios e tecnologia | Confira se cita a fonte original; prefira a original |
| Avaliações de usuários | Lojas de apps, sites de avaliação de software, Reclame Aqui | Amostra enviesada: use para temas recorrentes, não para números |
| Blogs, posts, fóruns | — | Só como pista para achar a fonte melhor |

## Divergência e atualidade

- Duas fontes com números diferentes: mostre as duas e explique a diferença (ano, recorte, metodologia). Não tire a média sem dizer.
- Dado com mais de 3 anos: diga o ano e trate como contexto, não como tamanho atual.
- Preços e planos mudam rápido: registre a data de acesso e, se possível, o plano exato.

## Limites da pesquisa (seção obrigatória)

Registre o que não foi possível saber e por quê (dado pago, empresa fechada, mercado informal, idioma), as buscas que não deram resultado e o que precisaria de pesquisa primária (entrevista, survey) — isso alimenta o `discovery-assumptions`.
