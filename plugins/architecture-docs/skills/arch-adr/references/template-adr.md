# Template — ADR

Baseado no formato de Michael Nygard (contexto, decisão, consequências), com as opções consideradas explícitas.

````markdown
# ADR-{NNN}: {Título curto da decisão}

| Campo | Valor |
|-------|-------|
| Situação | {Proposta / Aceita / Rejeitada / Obsoleta / Substituída por ADR-NNN} |
| Data | {DD/MM/AAAA} |
| Decisores | {nomes ou papéis} |
| Substitui | {ADR-NNN ou "—"} |
| Contêineres afetados | {nomes, conforme o diagrama de contêineres} |

## Contexto

{O problema, a necessidade e as forças em jogo: requisitos, restrições (prazo, equipe, custo, infraestrutura), atributos de qualidade. Escrito de forma neutra, sem antecipar a decisão.}

## Opções consideradas

### Opção 1 — {nome}
- Prós: {...}
- Contras: {...}

### Opção 2 — {nome}
- Prós: {...}
- Contras: {...}

## Decisão

{A opção escolhida, na voz ativa: "Vamos usar X para Y." E o motivo principal em relação às outras opções.}

## Consequências

- Positivas: {o que fica mais fácil}
- Negativas: {o que fica mais difícil, custos, riscos aceitos}
- Ações decorrentes: {migração, atualização do C4, mudança no deploy, treinamento}

## Referências

- {links para escopo, especificação, issues, documentação de fornecedor}
````

---

## Template — decisoes/README.md

````markdown
# Decisões de Arquitetura — {Nome do Projeto}

| ADR | Título | Situação | Data |
|-----|--------|----------|------|
| [ADR-001](ADR-001-{titulo}.md) | {título} | Aceita | {DD/MM/AAAA} |
````
