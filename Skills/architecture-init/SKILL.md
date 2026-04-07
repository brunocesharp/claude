---
name: dotnet-clean-architecture
description: Define a estrutura de camadas para aplicações .NET seguindo Clean Architecture. Use quando o usuário mencionar 'clean architecture', 'arquitetura limpa', 'camadas .NET', 'estrutura de projeto .NET', 'DDD layers', 'domain-driven design .NET', 'separação de responsabilidades', 'modularização .NET', 'criar projeto .NET estruturado', 'organização de solução .NET'. Também use quando for criar novos projetos .NET que precisem de arquitetura bem definida.
---

# Clean Architecture para .NET

## Estrutura de Camadas

```
Solution/
├── src/
│   ├── Domain/                    # Camada de Domínio (núcleo)
│   ├── Application/               # Camada de Aplicação
│   ├── Infrastructure/            # Camada de Infraestrutura
│   └── Presentation/              # Camada de Apresentação
├── tests/
│   ├── Domain.Tests/
│   ├── Application.Tests/
│   ├── Infrastructure.Tests/
│   └── Presentation.Tests/
└── Solution.sln
```

## Camadas e Responsabilidades

### 1. Domain (Núcleo)
**Projeto:** `{SolutionName}.Domain`

**Dependências:** Nenhuma (camada mais interna)

**Conteúdo:**
```
Domain/
├── Entities/           # Entidades de domínio
├── ValueObjects/       # Objetos de valor
├── Aggregates/         # Raízes de agregados
├── Enums/              # Enumerações de domínio
├── Events/             # Eventos de domínio
├── Exceptions/         # Exceções de domínio
├── Interfaces/         # Contratos (repositories, services)
└── Services/           # Serviços de domínio (lógica pura)
```

**Regras:**
- Zero dependências externas (exceto primitivos .NET)
- Contém toda lógica de negócio invariante
- Entidades com comportamento, não anêmicas
- Value Objects imutáveis
- Interfaces de repositórios (não implementações)

---

### 2. Application (Orquestração)
**Projeto:** `{SolutionName}.Application`

**Dependências:** Domain

**Conteúdo:**
```
Application/
├── Commands/           # Comandos (write operations)
│   └── {Feature}/
│       ├── {Command}Command.cs
│       └── {Command}CommandHandler.cs
├── Queries/            # Consultas (read operations)
│   └── {Feature}/
│       ├── {Query}Query.cs
│       └── {Query}QueryHandler.cs
├── DTOs/               # Data Transfer Objects
├── Interfaces/         # Contratos de serviços externos
├── Mappings/           # Configurações AutoMapper
├── Behaviors/          # Pipeline behaviors (validation, logging)
├── Exceptions/         # Exceções de aplicação
└── Common/             # Classes compartilhadas
```

**Regras:**
- Implementa casos de uso
- Orquestra fluxos de trabalho
- Define DTOs de entrada/saída
- Não conhece detalhes de infraestrutura
- Usa CQRS (Commands/Queries separados)

---

### 3. Infrastructure (Implementações)
**Projeto:** `{SolutionName}.Infrastructure`

**Dependências:** Domain, Application

**Conteúdo:**
```
Infrastructure/
├── Persistence/
│   ├── Configurations/     # Entity configurations (EF Core)
│   ├── Repositories/       # Implementações de repositórios
│   ├── Migrations/         # Migrations do banco
│   └── ApplicationDbContext.cs
├── Services/
│   ├── Email/              # Serviço de email
│   ├── Storage/            # Serviço de arquivos
│   └── External/           # Integrações externas
├── Identity/               # Autenticação/Autorização
└── DependencyInjection.cs  # Registro de serviços
```

**Regras:**
- Implementa interfaces definidas em Domain/Application
- Contém detalhes de persistência (EF Core, Dapper)
- Integrações com serviços externos
- Configurações de infraestrutura

---

### 4. Presentation (Gateway)
**Projeto:** `{SolutionName}.Presentation` ou `{SolutionName}.API`

**Dependências:** Application, Infrastructure (apenas para DI)

**Conteúdo:**
```
Presentation/
├── Controllers/        # Endpoints da API
├── Middleware/         # Middlewares customizados
├── Filters/            # Action filters
├── Models/             # View models / Request models
├── Extensions/         # Extension methods
├── Program.cs          # Entry point
└── appsettings.json    # Configurações
```

**Regras:**
- Recebe requisições externas
- Valida input básico
- Roteia para Application layer
- Formata responses
- Não contém lógica de negócio

---

## Fluxo de Dependências

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION                          │
│              (Controllers, Endpoints)                    │
└─────────────────────────┬───────────────────────────────┘
                          │ usa
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    APPLICATION                           │
│           (Commands, Queries, Handlers)                  │
└─────────────────────────┬───────────────────────────────┘
                          │ usa
                          ▼
┌─────────────────────────────────────────────────────────┐
│                      DOMAIN                              │
│        (Entities, Value Objects, Interfaces)             │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │ implementa
┌─────────────────────────┴───────────────────────────────┐
│                   INFRASTRUCTURE                         │
│         (Repositories, DbContext, Services)              │
└─────────────────────────────────────────────────────────┘
```

**Regra de Dependência:** Dependências apontam apenas para dentro (camadas internas).

---

## Convenções de Nomenclatura

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Entidade | `{Nome}` | `Product`, `Order` |
| Value Object | `{Nome}` | `Money`, `Address` |
| Repository Interface | `I{Entidade}Repository` | `IProductRepository` |
| Repository Impl | `{Entidade}Repository` | `ProductRepository` |
| Command | `{Ação}{Entidade}Command` | `CreateProductCommand` |
| Query | `Get{Entidade}Query` | `GetProductByIdQuery` |
| Handler | `{Command/Query}Handler` | `CreateProductCommandHandler` |
| DTO | `{Entidade}Dto` | `ProductDto` |
| Controller | `{Entidade}Controller` | `ProductsController` |

---

## Referências

Para detalhes de implementação de cada camada, consulte:
- `references/domain-layer.md` - Detalhes da camada Domain
- `references/application-layer.md` - Detalhes da camada Application
- `references/infrastructure-layer.md` - Detalhes da camada Infrastructure
- `references/presentation-layer.md` - Detalhes da camada Presentation
