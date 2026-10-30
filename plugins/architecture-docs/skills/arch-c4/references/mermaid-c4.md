# Mermaid C4

Sintaxe conferida na documentação do Mermaid (v11). O suporte a C4 no Mermaid é **experimental**: a sintaxe é compatível com o C4-PlantUML, mas o layout é simples e alguns recursos não existem.

## Limitações que afetam a skill

| Limitação | Como contornar |
|-----------|----------------|
| Sem legenda (`SHOW_LEGEND`, `tags`, `sprite`, `link` não suportados) | Tabela de legenda em Markdown logo abaixo do diagrama |
| Layout não é automático: elementos soltos vêm **antes** de todos os limites (`*_Boundary`), e dentro de cada grupo vale a ordem das declarações | Siga o padrão de layout abaixo; ajuste com `UpdateLayoutConfig` |
| `Lay_U`, `Lay_D`, `Lay_L`, `Lay_R` não existem | Use `Rel_U`/`Rel_D`/`Rel_L`/`Rel_R` para sugerir a direção da seta |
| Rótulos de relação se sobrepõem | `UpdateRelStyle(de, para, $offsetX="...", $offsetY="...")` |
| `RelIndex` ignora o número | No diagrama dinâmico, a numeração segue a ordem dos `Rel` |

## Padrão de layout

Para ficar como o livro recomenda (pessoas em cima, sistema no centro, dependências embaixo) e igual em todos os diagramas:

1. **Pessoas** soltas, declaradas primeiro: ficam em cima.
2. **Sistema em escopo** (ou o contêiner detalhado) dentro do seu limite.
3. **Sistemas externos** dentro de `Boundary(externos, "Sistemas externos", "externo") { }`, declarado por último: ficam embaixo. Sem esse limite, o Mermaid os coloca soltos em cima, junto com as pessoas.
4. `UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")` para diagramas de contêineres e componentes; `"3"` no contexto.
5. Rótulo sobreposto: `UpdateRelStyle` com `$offsetX`/`$offsetY`.

## Regras de escrita

- **Alias** (primeiro parâmetro): só letras, números e `_`, sem acento nem hífen (`api`, `banco_pedidos`, `spa`).
- **Textos** sempre entre aspas: `"Sistema de Pedidos"`. Acentos são aceitos dentro das aspas.
- Quebra de linha numa descrição: `<br/>`.
- Um elemento por linha; limites (`*_Boundary`) com `{ }`.
- Bloco de código com a linguagem `mermaid`.

## Elementos

| Nível | Elementos |
|-------|-----------|
| Contexto | `Person(alias, "Nome", "Descrição")`, `Person_Ext`, `System(alias, "Nome", "Descrição")`, `System_Ext`, `SystemDb`, `SystemDb_Ext`, `SystemQueue`, `SystemQueue_Ext`, `Enterprise_Boundary(alias, "Nome") { }`, `System_Boundary`, `Boundary(alias, "Nome", "tipo")` |
| Contêineres | `Container(alias, "Nome", "Tecnologia", "Descrição")`, `ContainerDb`, `ContainerQueue`, `Container_Ext`, `ContainerDb_Ext`, `ContainerQueue_Ext`, `Container_Boundary(alias, "Nome") { }` |
| Componentes | `Component(alias, "Nome", "Tecnologia", "Descrição")`, `ComponentDb`, `ComponentQueue`, `Component_Ext`, `ComponentDb_Ext`, `ComponentQueue_Ext` |
| Deployment | `Deployment_Node(alias, "Nome", "Tipo", "Descrição") { }` (atalhos `Node`, `Node_L`, `Node_R`) |
| Relações | `Rel(de, para, "Rótulo", "Tecnologia")`, `BiRel`, `Rel_U`, `Rel_D`, `Rel_L`, `Rel_R`, `Rel_Back`, `RelIndex(n, de, para, "Rótulo")` |
| Estilo | `UpdateElementStyle(alias, $bgColor="...", $fontColor="...", $borderColor="...")`, `UpdateRelStyle(de, para, $textColor="...", $lineColor="...", $offsetX="...", $offsetY="...")`, `UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")` |

Tipos de diagrama: `C4Context`, `C4Container`, `C4Component`, `C4Dynamic`, `C4Deployment`.

---

## Exemplo — Contexto

```mermaid
C4Context
  title [Contexto] Sistema de Pedidos

  Person(cliente, "Cliente", "Compra produtos pela loja on-line.")
  Person(atendente, "Atendente", "Acompanha pedidos e resolve problemas de entrega.")

  System_Boundary(escopo, "Em escopo") {
    System(pedidos, "Sistema de Pedidos", "Permite montar o carrinho, pagar e acompanhar a entrega.")
  }

  Boundary(externos, "Sistemas externos", "externo") {
    System_Ext(pagamento, "Gateway de Pagamento", "Processa cartão e Pix. Mantido pelo fornecedor.")
    System_Ext(email, "Serviço de E-mail", "Envia e-mails transacionais.")
    System_Ext(erp, "ERP", "Controla estoque e faturamento. Mantido pela TI corporativa.")
  }

  Rel(cliente, pedidos, "Faz pedidos e acompanha entregas usando")
  Rel(atendente, pedidos, "Consulta e ajusta pedidos em")
  Rel(pedidos, pagamento, "Cobra o pedido usando")
  Rel(pedidos, email, "Envia confirmações usando")
  Rel(pedidos, erp, "Reserva estoque e emite nota em")

  UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

| Legenda | Significado |
|---------|-------------|
| Pessoa | Usuário do sistema |
| Caixa azul | Sistema em escopo (construído pelo time) |
| Caixa cinza | Sistema externo (outro dono) |
| Seta | Dependência, do iniciador para o receptor |

---

## Exemplo — Contêineres

```mermaid
C4Container
  title [Contêineres] Sistema de Pedidos

  Person(cliente, "Cliente", "Compra produtos pela loja on-line.")

  System_Boundary(sistema, "Sistema de Pedidos") {
    Container(spa, "Loja Web", "Angular 20, TypeScript", "Catálogo, carrinho e acompanhamento do pedido no navegador.")
    Container(api, "API de Pedidos", "ASP.NET Core 9 Web API", "Regras de pedido, pagamento e entrega. Expõe JSON/HTTPS.")
    ContainerDb(banco, "Banco de Pedidos", "Schema PostgreSQL 16", "Pedidos, itens, clientes e histórico de situação.")
    ContainerQueue(fila, "Fila de Eventos", "RabbitMQ", "Eventos de pedido para processamento assíncrono.")
    Container(worker, "Processador de Pedidos", "Worker .NET 9", "Reserva estoque e envia e-mails a partir dos eventos.")
  }

  Boundary(externos, "Sistemas externos", "externo") {
    System_Ext(pagamento, "Gateway de Pagamento", "Processa cartão e Pix.")
    System_Ext(erp, "ERP", "Estoque e faturamento.")
  }

  Rel(cliente, spa, "Usa", "HTTPS")
  Rel(spa, api, "Chama", "JSON/HTTPS, síncrono")
  Rel(api, banco, "Lê e grava em", "EF Core, TCP 5432")
  Rel(api, pagamento, "Cobra o pedido usando", "JSON/HTTPS, síncrono")
  Rel(api, fila, "Publica eventos de pedido em", "AMQP, assíncrono")
  Rel(worker, fila, "Consome eventos de", "AMQP")
  Rel(worker, erp, "Reserva estoque em", "SOAP/HTTPS")

  UpdateRelStyle(spa, api, $offsetY="-40", $offsetX="-20")
  UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

---

## Exemplo — Componentes

```mermaid
C4Component
  title [Componentes] Sistema de Pedidos — API de Pedidos

  Container(spa, "Loja Web", "Angular 20", "Interface do cliente.")

  Container_Boundary(api, "API de Pedidos") {
    Component(ctrl, "PedidosController", "Controller ASP.NET Core", "Endpoints de criação e consulta de pedidos.")
    Component(servico, "Serviço de Pedidos", "Serviço C#", "Regras de criação, cancelamento e mudança de situação.")
    Component(repo, "Repositório de Pedidos", "EF Core", "Persistência de pedidos e itens.")
    Component(gateway, "Adaptador de Pagamento", "HttpClient + Polly", "Traduz a cobrança para a API do gateway.")
  }

  Boundary(dependencias, "Dependências", "vizinhos") {
    ContainerDb(banco, "Banco de Pedidos", "Schema PostgreSQL 16", "Pedidos e itens.")
    System_Ext(pagamento, "Gateway de Pagamento", "Processa cartão e Pix.")
  }

  Rel(spa, ctrl, "Chama", "JSON/HTTPS")
  Rel(ctrl, servico, "Usa")
  Rel(servico, repo, "Persiste pedidos usando")
  Rel(servico, gateway, "Cobra usando")
  Rel(repo, banco, "Lê e grava em", "SQL")
  Rel(gateway, pagamento, "Chama", "JSON/HTTPS")

  UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

| Componente | Código |
|------------|--------|
| PedidosController | `src/Pedidos.API/Controllers/PedidosController.cs` |
| Serviço de Pedidos | `src/Pedidos.Application/Pedidos/` |
| Repositório de Pedidos | `src/Pedidos.Infrastructure/Repositories/PedidoRepository.cs` |
| Adaptador de Pagamento | `src/Pedidos.Infrastructure/ExternalServices/Pagamento/` |

---

## Exemplo — Deployment

```mermaid
C4Deployment
  title [Deployment] Sistema de Pedidos — Produção

  Deployment_Node(navegador, "Navegador do cliente", "Chrome, Edge, Safari") {
    Container(spa, "Loja Web", "Angular 20", "Interface do cliente.")
  }

  Deployment_Node(vps, "Servidor de produção", "Ubuntu 24.04, Docker Compose") {
    Deployment_Node(nginx, "nginx", "Proxy reverso e TLS") {
      Container(estatico, "Arquivos da Loja Web", "Build estático do Angular", "Servidos pelo nginx.")
    }
    Deployment_Node(c_api, "api", "Container Docker") {
      Container(api, "API de Pedidos", "ASP.NET Core 9", "Regras de pedido.")
    }
    Deployment_Node(c_db, "postgres", "Container Docker, PostgreSQL 16") {
      ContainerDb(banco, "Banco de Pedidos", "Schema PostgreSQL", "Pedidos e itens.")
    }
  }

  Rel(spa, api, "Chama", "JSON/HTTPS via nginx")
  Rel(api, banco, "Lê e grava em", "TCP 5432")
```

---

## Exemplo — Dinâmico

```mermaid
C4Dynamic
  title [Dinâmico] Sistema de Pedidos — Pagamento de um pedido

  Container(spa, "Loja Web", "Angular 20")
  Container(api, "API de Pedidos", "ASP.NET Core 9")
  ContainerDb(banco, "Banco de Pedidos", "PostgreSQL")
  System_Ext(pagamento, "Gateway de Pagamento")
  ContainerQueue(fila, "Fila de Eventos", "RabbitMQ")

  Rel(spa, api, "Envia o pedido para pagamento", "JSON/HTTPS")
  Rel(api, pagamento, "Solicita a cobrança a", "JSON/HTTPS")
  Rel(api, banco, "Grava a situação Pago em", "SQL")
  Rel(api, fila, "Publica PedidoPago em", "AMQP")
```

A numeração (1, 2, 3, 4) sai da ordem dos `Rel`.

---

## Problemas comuns

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| Diagrama não renderiza | Alias com hífen, acento ou espaço; aspas faltando | Alias só com letras, números e `_`; textos entre aspas |
| Erro em descrição com vírgula | Texto sem aspas | Coloque o texto entre aspas |
| Elementos em uma linha só, muito largo | Muitos elementos por linha | `UpdateLayoutConfig($c4ShapeInRow="3")` |
| Rótulos em cima de outros | Relações paralelas | `UpdateRelStyle` com `$offsetX`/`$offsetY`, ou mude a ordem das declarações |
| Diagrama ilegível | Elementos demais | Divida em diagramas menores (ver "Escopo do diagrama" em `notacao.md`) |
