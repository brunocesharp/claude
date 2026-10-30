# Vocabulário C4

Fonte: Simon Brown, *The C4 model for visualising software architecture*, cap. 4 ("A shared vocabulary").

O problema que o C4 resolve não é a notação, e sim a falta de um **vocabulário comum**. "Componente" pode ser "a aplicação web é um componente do sistema" ou "a aplicação web é feita de componentes" — dois níveis de abstração com a mesma palavra. Antes de desenhar, o time precisa concordar sobre os termos; a notação pode evoluir depois.

Assim como dois mapas da mesma cidade usam cores e símbolos diferentes mas mostram as mesmas coisas (ruas, rios, bairros), dois diagramas C4 podem usar notações diferentes desde que mostrem as mesmas **abstrações** e tenham uma **legenda**.

---

## A hierarquia

> Um **sistema de software** é formado por um ou mais **contêineres** (aplicações web, apps mobile, aplicações desktop, bancos de dados, sistemas de arquivos...), cada um com um ou mais **componentes**, que por sua vez são implementados por um ou mais **elementos de código** (classes, interfaces, objetos, funções...). E **pessoas** usam os sistemas de software.

| Nível | Elemento | Definição |
|-------|----------|-----------|
| 1 | Sistema de software | O nível mais alto: algo que entrega valor aos usuários, humanos ou não |
| 2 | Contêiner | Algo que hospeda código ou dados e precisa estar rodando para o sistema funcionar |
| 3 | Componente | Agrupamento de funcionalidades relacionadas atrás de uma interface bem definida, dentro de um contêiner |
| 4 | Código | Classes, interfaces, enums, funções, objetos que implementam um componente |
| — | Pessoa | Usuário, papel, ator ou persona que usa o sistema |

---

## Contêiner

Exemplos:
- Aplicação web no servidor (ASP.NET Core, Spring, Node.js, Rails)
- Aplicação web no cliente (SPA Angular/React rodando no navegador)
- Aplicação desktop, app mobile
- Aplicação de console, processo batch, worker
- Microsserviço (do próprio time)
- Função serverless (cada uma é um contêiner, pois é implantável separadamente)
- Banco de dados (um schema em um SGBD, um banco de documentos, grafo...)
- Armazenamento de blobs ou conteúdo (S3, R2, Azure Blob, CDN)
- Sistema de arquivos (quando guarda dados de negócio; arquivos de log não entram)
- Script de shell

Regras:
- **Implantável separadamente.** Em tese, cada contêiner pode rodar numa infraestrutura própria; a comunicação entre contêineres é fora do processo (rede ou outro processo).
- Duas aplicações web empacotadas separadamente são **dois** contêineres, mesmo que fiquem no mesmo servidor (isso é otimização de deployment).
- Duas aplicações "logicamente separadas" mas empacotadas juntas são **um** contêiner.
- Dois schemas de banco são **dois** contêineres, mesmo no mesmo servidor de banco.
- Bibliotecas e módulos (DLL, JAR, assembly .NET, pacote npm) **não** são contêineres, a não ser que rodem sozinhos (ex.: JAR executável).
- O nome "contêiner" não tem relação com Docker. Se confundir o time, use "unidade implantável" ou "contexto de execução" e registre no glossário.

---

## Componente

- Não é implantável separadamente: todos os componentes de um contêiner rodam, em geral, no mesmo processo.
- Como o componente é empacotado (uma DLL ou várias) é uma questão ortogonal.
- É um passo acima do código:
  - Linguagens OO (C#, Java): um conjunto de classes e interfaces (ex.: um controller; um serviço com a interface e a implementação; um repositório).
  - JavaScript/TypeScript: um módulo com seus objetos e funções.
  - Banco relacional: um agrupamento lógico de tabelas, views, procedures.
- Vale para qualquer forma de organizar o código (por camada, por feature, por componente) e qualquer estilo (camadas, hexagonal, portas e adaptadores).
- **Componentes devem ser coisas reais, visíveis no código**, e não construções lógicas que só existem nas discussões de arquitetura.
- Código compartilhado (classes base, utilitários) usado por muitos componentes é inevitável; não precisa virar componente.

---

## Casos frequentes

| Caso | Como modelar |
|------|--------------|
| Microsserviços de outro time, fora do controle do time | Sistemas de software externos (caixa preta) |
| Microsserviços do próprio time | Contêineres, e o armazenamento de cada um é outro contêiner |
| Funções serverless | Contêineres (implantáveis separadamente) |
| Frameworks, plataformas e bibliotecas | Tecnologia de um componente, não componente (ex.: Entity Framework, logging, driver de banco) |
| Serviço gerenciado em que o time controla os dados (bucket, banco RDS) | Contêiner (é parte da arquitetura, mesmo hospedado fora) |
| Serviço de terceiro apenas consumido (gateway de pagamento, e-mail SaaS) | Sistema externo |
| "Módulo" e "subsistema" | O C4 evita esses termos por serem difíceis de mapear no código; se forem úteis ao time, defina-os no glossário |

---

## Crie o vocabulário do time

Não há regra universal. Se a organização já usa outros termos (ex.: "componente" para o executável e "módulo" para as partes), mantenha-os, desde que estejam **definidos explicitamente** e todos entendam. O importante é haver uma hierarquia que descreva o sistema em vários níveis de abstração. Registre as equivalências no glossário do `arquitetura.md`.
