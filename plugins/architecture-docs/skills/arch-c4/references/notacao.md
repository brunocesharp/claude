# Notação

Fonte: Simon Brown, *The C4 model for visualising software architecture*, cap. 10 ("Notation") e 11 ("Diagrams must reflect reality").

O C4 é independente de notação. Estas regras valem para qualquer ferramenta; a forma de aplicá-las no Mermaid está em `mermaid-c4.md`.

---

## Título

- Todo diagrama tem um título curto e claro, **com o tipo do diagrama**.
- Se houver ordem de leitura, numere.
- Formato adotado nesta skill: `[Contexto] Nome do Sistema`, `[Contêineres] Nome do Sistema`, `[Componentes] Nome do Sistema — Nome do Contêiner`, `[Deployment] Nome do Sistema — Produção`, `[Dinâmico] Nome do Sistema — Cenário`.

## Legenda

Mesmo quando a notação parece óbvia, inclua uma legenda: pessoas com experiências diferentes interpretam cores e formas de jeitos diferentes ("as caixas cinza parecem ser os sistemas existentes..."). A legenda explica:
- formas;
- estilos de linha;
- cores;
- bordas;
- siglas.

O Mermaid C4 não desenha legenda: escreva uma **tabela de legenda logo abaixo de cada diagrama**.

## Elementos

Informação mínima de cada elemento:

| Elemento | Informação |
|----------|------------|
| Pessoa | Nome e descrição |
| Sistema de software | Nome e descrição |
| Contêiner | Nome, tecnologia e descrição |
| Componente | Nome, tecnologia e descrição |

- **Descrição/responsabilidades**: não deixe caixas só com nome. Uma frase curta ou uma lista curta (7 ± 2 itens) remove ambiguidade.
- **Tipo do elemento** explícito (pessoa, sistema, contêiner, componente).
- **Cor** é ótima para complementar um diagrama que já faz sentido. Pode codificar: existente × novo; produto pronto × construído; tecnologia; risco; dono (do time × de outros); interno × externo; o que muda na próxima entrega. Sempre na legenda, e funcionando para daltônicos e em impressão preto e branco (não dependa só da cor).
- **Formas**: comece com caixas; formas (pessoa, cilindro para banco, fila) só reforçam o que o texto já diz. Ponha na legenda.
- **Bordas** (dupla, tracejada, colorida): para ênfase ou agrupamento, sempre rotuladas ou na legenda.
- **Tamanho**: desenhe os elementos do mesmo tamanho, a menos que queira dizer algo sobre tamanho ou importância.

## Linhas

- **Direção**: mesmo que a relação seja bidirecional, escolha a direção mais significativa e desenhe uma seta só. Padrão desta skill: **dependência, do iniciador para o receptor**. Seja consistente.
- **Descrição**: escreva para que a frase faça sentido lida em voz alta, terminando com preposição quando ajudar:
  - "API — lê e grava em → Banco" (e não "lê e grava")
  - "Sistema — obtém perfis e posts de → Instagram" (e não "obtém perfis e posts")
- **Estilo de linha** (tracejada para assíncrono, cor para HTTP × HTTPS): só como complemento, sempre na legenda.
- **Uma linha ou várias**: se houver duas APIs diferentes entre os mesmos elementos, pode usar duas linhas para ser preciso.

## Layout e orientação

- Ponha o elemento mais importante no centro e trabalhe ao redor.
- Mantenha a posição consistente entre diagramas (ex.: pessoas em cima, sistemas externos embaixo).
- Não existe orientação "correta", mas inverter o comum (banco em cima) confunde.

## Siglas

Evite siglas; se usar, explique no glossário ou na legenda. Siglas de tecnologia muito conhecidas (REST, JSON, SQL) podem ficar, mas na dúvida explique. Siglas do domínio (do negócio) sempre vão para o glossário.

## Atributos de qualidade

Dá para acrescentar texto (número de usuários, latência alvo, volume de dados) a elementos e linhas. Mas não force tudo no diagrama: preocupações transversais como segurança ficam melhor em texto curto no documento. Réplicas e clusters (escalabilidade, disponibilidade) vão no deployment.

## Escopo do diagrama

Diagramas grandes têm carga cognitiva alta e ninguém lê. Aumentar a página só aumenta a bagunça. Em vez de um diagrama gigante (comum em componentes), divida em vários diagramas menores, cada um focado numa área de negócio, área funcional, contexto delimitado, caso de uso ou conjunto de funcionalidades — **cada um contando uma parte da mesma história, no mesmo nível de abstração**. Referência prática: acima de ~12 elementos, considere dividir.

## Escute as perguntas

Se, ao apresentar, você precisar dizer "só para deixar claro, essas setas são fluxo de dados", essa informação deve ir para a legenda.

---

## Diagramas refletem a realidade

- **Distância entre modelo e código** (George Fairbanks): pensamos em componentes, camadas e serviços, mas a linguagem só tem classes e pacotes. Reduza essa distância com um **estilo de código que evidencia a arquitetura**: convenções de nome, organização por pasta/namespace e, se útil, metadados (atributos/anotações).
- Se há uma caixa "Componente de Log" no diagrama, deve existir um Componente de Log no código.
- **Tecnologia nos diagramas**: incluir as escolhas de tecnologia evita a "arquitetura de torre de marfim" e força as perguntas certas ("como esse componente fala com aquele se estão em processos diferentes?"). Documentando depois de construído, não há motivo para omitir. Em design, se a escolha está em aberto, escreva as opções ("PostgreSQL ou SQL Server"): fica explícito que há uma decisão a tomar.
- **"Vocês codificariam assim?"** — antes de fechar um diagrama, pergunte se ele mostra o que vai ser (ou foi) construído:
  - Componente de log compartilhado por duas aplicações, entregue como DLL dentro de cada uma: desenhe dentro de **cada** contêiner, marcado como compartilhado — não como um contêiner central, que pareceria um servidor de log.
  - Camadas com CQRS em que a leitura pula a camada de serviço: desenhe as linhas como serão codificadas, anotando a intenção.
