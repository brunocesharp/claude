# Lentes da revisão

Cada lente olha o **mesmo diff** com uma pergunta diferente. No modo **completo** cada lente roda num subagente próprio, em paralelo. No modo **rápido**, um revisor só cobre as lentes 1, 3 e 5. A lente 2 é sempre o script (`review.py integrity`).

## Postura (vale para todas)

- Parta do princípio de que **há defeitos** e procure ativamente. "Parece bom" não é resultado.
- Todo achado aponta **onde** (repositório, arquivo, linha ou trecho), **o quê** e **qual a consequência** concreta (o que quebra, para quem, em que situação). Sem consequência, não é achado.
- Leia além do trecho do diff quando precisar: quem chama, o teste, a configuração.
- **Não invente defeito para preencher cota.** Se a lente não achar nada, diga o que foi verificado (lista de checagens) — isso vai para o bloco de revisão como "verificado sem achados". Achado inventado custa mais que achado perdido: ele será descartado na triagem e desacredita a revisão.
- Não sugira refatoração por gosto. Estilo só é achado quando contradiz um padrão citado na story ou no repositório.

## 1. Aderência à story

- Para cada `**CA-N**`: onde está implementado e qual teste o verifica? O teste verifica de fato o que o cenário diz (o "Então"), com os dados do cenário?
- Cada tarefa marcada `[x]`: o que ela diz foi feito? Tarefa marcada sem implementação é achado `high`.
- Algo de "Fora desta story" foi implementado? Algo que a story não pede foi acrescentado?
- Decisões registradas no Registro do desenvolvimento contradizem algum critério?

## 2. Integridade do registro (script)

`review.py integrity`: arquivo alterado e não declarado em "Arquivos alterados" (`undeclared`), declarado e não alterado (`declared_not_changed`), alterações não commitadas, branch diferente de `feat/{id}`. Cada divergência vira achado `low` (registro incompleto), salvo se esconder mudança relevante (aí, a lente correspondente avalia).

## 3. Correção e casos de borda

Valores nulos/vazios, limites (0, 1, máximo, paginação na última página), concorrência, ordenação, fuso/data, arredondamento, mensagens de erro, tratamento de falha (Result Pattern: erro retornado e tratado, não exceção engolida), transação e consistência, performance óbvia (N+1, consulta sem índice em lista grande).

## 4. Segurança

Autorização (o endpoint novo exige o perfil certo?), validação de entrada, injeção (SQL, comando, HTML), dados sensíveis em log ou resposta, segredo no código ou na configuração versionada, CORS/CSRF quando há tela, dependência nova com vulnerabilidade conhecida.

## 5. Testes

- Os testes passam? **Rode** a suíte de cada repositório (`dev-story/references/comandos-por-stack.md`); não confie no Registro.
- Cada CA tem teste; os testes falhariam se o comportamento quebrasse (asserção real, não só "não lançou exceção").
- Testes frágeis (dependem de ordem, horário, rede) e mocks que escondem o comportamento testado.

## 6. Arquitetura e padrões

ADRs citados na story respeitados; camadas (Domain sem dependência de infraestrutura, Application sem detalhe de HTTP...); padrão das skills de código (`architecture-*`, `angular-*`) e o arquivo de exemplo citado na story; nomes e pastas no padrão do repositório.

## 7. Contratos (só com mais de um repositório ou contrato na story)

Provedor e consumidor batem (rota, verbo, DTO, nomes e tipos de campos, códigos de erro)? Mudança incompatível tem a estratégia da tabela de Contratos (expandir/contrair, versão, flag)? A ordem de merge e deploy (provedor antes) está registrada?

## Formato de retorno de cada lente

```
LENTE: {nome}
ACHADOS:
- [{severidade proposta}] {repo}:{arquivo}:{linha} — {o quê}. Consequência: {o que acontece}. Sugestão: {correção, se houver uma clara}
VERIFICADO SEM ACHADOS:
- {checagem feita}
```
