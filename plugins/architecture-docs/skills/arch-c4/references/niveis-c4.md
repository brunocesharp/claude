# Níveis do C4

Fonte: Simon Brown, *The C4 model for visualising software architecture*, cap. 5 a 9.

O C4 é um conjunto de **mapas** do sistema em níveis de zoom. Não é um processo de design: é uma coleção de diagramas para descrever a estrutura estática. Siga o mantra de Shneiderman: **visão geral primeiro, depois zoom e filtro, e detalhes sob demanda**.

| Nível | Diagrama | Zoom | Obrigatório? | Público |
|-------|----------|------|--------------|---------|
| 1 | Contexto do sistema | O sistema e o mundo ao redor | **Sim**, todo sistema | Técnicos e não técnicos, de dentro e de fora do time |
| 2 | Contêineres | Dentro do sistema | **Sim**, todo sistema | Técnicos de dentro e de fora do time (dev, operação, suporte) |
| 3 | Componentes | Dentro de um contêiner | Opcional | Técnicos do time |
| 4 | Código | Dentro de um componente | Opcional, geralmente não recomendado | Desenvolvedores |

Recomendação do livro: todo time cria Contexto e Contêineres, e pensa bem se Componentes e Código compensam o custo de criar **e manter atualizados**.

---

## Nível 1 — Contexto do sistema

**Intenção** — responder:
1. Que sistema estamos construindo (ou construímos)?
2. Quem usa?
3. Como ele se encaixa no ambiente existente?

**Estrutura** — o sistema em escopo como uma caixa no centro, cercado pelos usuários e pelos outros sistemas com que interage. Detalhe não importa; o foco é em pessoas e sistemas, não em tecnologias, protocolos ou detalhes de baixo nível.

**Elementos**
- **Pessoas**: nome e descrição (papel, responsabilidades). Modele como usuários, papéis, atores ou personas.
- **Sistemas de software**: nome e descrição. Normalmente fora do escopo e da responsabilidade do time; aparecem para mostrar que são **dependências**, não algo que o time constrói.
- **Limite da organização** (opcional): linha tracejada separando o que é interno do que é externo (`Enterprise_Boundary`).

**Interações** — anote o propósito de toda interação, em alto nível, sem protocolos ou formatos.

**Motivação** — torna explícitos o contexto e o escopo; mostra o que está sendo acrescentado ao ambiente; serve de ponto de partida para conversas com qualquer público; mostra com quem conversar sobre interfaces entre sistemas. Pode ser desenhado em workshop de levantamento de requisitos.

---

## Nível 2 — Contêineres

**Intenção** — responder:
1. Qual a forma geral do sistema?
2. Quais as decisões de tecnologia de alto nível?
3. Como as responsabilidades estão distribuídas?
4. Como os contêineres se comunicam?
5. Como desenvolvedor, onde preciso escrever código para implementar uma funcionalidade?

**Estrutura** — os blocos técnicos de alto nível do sistema, dentro de um limite (`System_Boundary`) que corresponde à caixa do diagrama de contexto. Não mostra quantidade de instâncias, cluster ou failover: isso vai no diagrama de deployment.

**Quanto detalhe** — em design antecipado, ponha o que se sabe. Documentando sistema existente, dá para incluir protocolos e portas.

**Elementos**
- **Contêiner**: nome, **tecnologia** (ex.: "ASP.NET Core 9 Web API", "Angular 20 SPA", "Schema PostgreSQL") e descrição curta ou lista de responsabilidades/entidades guardadas.
  - Tecnologia ainda indefinida: liste as opções ou o tipo genérico ("Schema de banco relacional").
  - Banco padrão sem recursos proprietários: a tecnologia pode ir só no deployment. Se usa recursos específicos (procedures, extensões), indique a tecnologia.
- **Sistema de arquivos**: só quando guarda dados críticos de negócio; arquivos de log ficam de fora.
- **Armazenamento como serviço** (S3, R2, RDS): normalmente aparece, porque o time é dono dos buckets/schemas.
- **Pessoas e sistemas**: os mesmos do contexto, para dar continuidade à história.

**Interações** — normalmente fora do processo. Anote: propósito ("lê e grava em"), mecanismo (REST, gRPC, fila, SignalR), estilo (síncrono, assíncrono, batch) e protocolo/porta (HTTPS, SMTP, AMQP).

**Motivação** — torna explícitas as escolhas de tecnologia e as relações entre contêineres. É o diagrama intermediário entre a caixa preta do contexto e o excesso de detalhe dos componentes.

---

## Nível 3 — Componentes

**Intenção** — responder:
1. De quais componentes cada contêiner é feito?
2. Todo componente tem um lugar (está em algum contêiner)?
3. Dá para entender como o software funciona em alto nível?

**Estrutura** — os componentes de **um** contêiner por vez, dentro de um `Container_Boundary`, com os contêineres, pessoas e sistemas vizinhos para dar contexto. Pode mostrar só parte dos componentes, se for isso que conta a história.

**Elementos**
- **Componente**: nome, tecnologia (ex.: "Controller ASP.NET Core", "Serviço C#", "Repositório EF Core", "Componente Angular standalone") e descrição curta da responsabilidade.
- O diagrama deve refletir o estilo arquitetural em uso (camadas, hexagonal...).

**Componentes de infraestrutura e transversais** (log, autenticação, cache):
1. Omitir, se não ajudam a contar a história;
2. Escrever uma nota ("todos os componentes registram log pelo Componente de Log");
3. Incluir sem as linhas e marcar quem usa com cor/símbolo explicado na legenda.

**Componentes compartilhados e bibliotecas** — inclua se ajudar a contar a história; marque como compartilhado na legenda.

**Várias implementações de um componente** (ex.: armazenamento local ou em nuvem escolhido por configuração):
1. Desenhar como se houvesse uma só;
2. Dizer na descrição que a implementação varia por configuração;
3. Um diagrama por implementação, se forem poucas combinações.

**Interações** — propósito ("usa", "persiste dados usando", "delega para") e estilo (síncrono, assíncrono).

**Quando fazer** — não para bancos, armazenamentos ou contêineres muito simples (um microsserviço pequeno). Para monólitos e APIs grandes, vale considerar, especialmente em design antecipado. Para documentação de longa duração, muitos times acham opcional pelo custo de manutenção.

**Mapeamento para o código** — se cada componente do diagrama corresponde a algo no código (pasta, namespace, classe), o diagrama vira um ótimo guia do código. Inclua uma tabela componente → caminho.

---

## Nível 4 — Código

**Intenção** — mostrar como um componente é implementado.

**Estrutura** — diagrama de classes UML (no Mermaid, `classDiagram`) limitado ao interior de **um** componente, só com atributos e métodos relevantes para a narrativa.

**Quando fazer** — raramente. Esse detalhe está no código e a IDE mostra sob demanda. Só para componentes muito complexos ou para documentar um padrão que se repete no código (ex.: como todo command/handler é montado).
