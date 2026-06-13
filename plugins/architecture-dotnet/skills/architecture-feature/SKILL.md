---
name: dotnet-application-feature
description: Gera Commands e Queries na camada Application seguindo CQRS e Clean Architecture. Use quando o usuário mencionar "criar command", "novo command", "criar query", "nova query", "feature application", "caso de uso", "use case", "handler", "criar handler", "command handler", "query handler", "adicionar command", "adicionar query", "operação de escrita", "operação de leitura", "CQRS". Também dispara quando pedir para criar funcionalidades que envolvam orquestração de casos de uso, busca de dados ou alteração de estado. NÃO use para lógica de domínio pura (use domain-layer) ou endpoints HTTP (use dotnet-endpoint-generator).
---

# .NET Application Feature Generator

Gera Commands (escrita) e Queries (leitura) na camada Application seguindo CQRS, MediatR e Clean Architecture.

## Instruções

### ANTES de gerar código, consulte as referências:

1. **Leia `references/command-template.md`** para estrutura de Commands
2. **Leia `references/query-template.md`** para estrutura de Queries
3. **Leia `references/behaviors.md`** para pipeline behaviors

### Passo 1: Identificar Tipo de Operação

| Tipo | Quando Usar | Retorno |
|------|-------------|---------|
| **Command** | Altera estado (Create, Update, Delete) | `Result<T>` ou `Result` |
| **Query** | Apenas leitura (Get, List, Search) | `Result<TDto>` ou `Result<PagedResult<TDto>>` |

### Passo 2: Coletar Informações

Para **Command**:
- Nome da ação (Create, Update, Delete, Approve, Cancel, etc.)
- Nome da entidade
- Campos necessários
- Validações de negócio
- Retorno esperado (Id, void, DTO)

Para **Query**:
- Tipo (ById, List, Search, Filter)
- Nome da entidade
- Filtros necessários
- Se precisa paginação
- Campos do DTO de retorno

### Passo 3: Gerar Artefatos

#### Para Command (na ordem):

```
Application/
└── {Feature}/
    └── Commands/
        └── {Action}{Entity}/
            ├── {Action}{Entity}Command.cs
            ├── {Action}{Entity}CommandHandler.cs
            └── {Action}{Entity}CommandValidator.cs
```

#### Para Query (na ordem):

```
Application/
└── {Feature}/
    └── Queries/
        └── Get{Entity}{Suffix}/
            ├── Get{Entity}{Suffix}Query.cs
            └── Get{Entity}{Suffix}QueryHandler.cs
    └── DTOs/
        └── {Entity}Dto.cs
```

### Passo 4: Validar Checklist

- [ ] Command/Query é um `record` imutável
- [ ] Implementa `IRequest<Result<T>>` (não `IRequest<T>`)
- [ ] Handler injeta apenas interfaces (não implementações)
- [ ] `CancellationToken` propagado em todos os métodos async
- [ ] Validações de negócio retornam `Result.Invalid()` ou `Result.NotFound()`
- [ ] Validator usa FluentValidation (apenas para Commands)
- [ ] DTO é `record` com todos os campos necessários

## Padrões Obrigatórios

### Nomenclatura

| Artefato | Padrão | Exemplo |
|----------|--------|---------|
| Command | `{Action}{Entity}Command` | `CreateProductCommand` |
| Command Handler | `{Action}{Entity}CommandHandler` | `CreateProductCommandHandler` |
| Command Validator | `{Action}{Entity}CommandValidator` | `CreateProductCommandValidator` |
| Query | `Get{Entity}{Suffix}Query` | `GetProductByIdQuery`, `GetProductListQuery` |
| Query Handler | `Get{Entity}{Suffix}QueryHandler` | `GetProductByIdQueryHandler` |
| DTO | `{Entity}Dto` | `ProductDto` |

### Result Pattern (Obrigatório)

```csharp
// CORRETO - Usar Result<T>
public record CreateProductCommand(...) : IRequest<Result<Guid>>;

// INCORRETO - Não usar tipo direto
public record CreateProductCommand(...) : IRequest<Guid>;
```

### Injeção de Dependências

```csharp
// CORRETO - Injetar interfaces
public class Handler(IProductRepository repository, IUnitOfWork unitOfWork)

// INCORRETO - Não injetar implementações
public class Handler(ProductRepository repository, ApplicationDbContext context)
```

## Fluxo de Decisão

```
Usuário quer criar feature
         │
         ▼
    Altera estado?
    ┌────┴────┐
   Sim       Não
    │         │
    ▼         ▼
 COMMAND    QUERY
    │         │
    ▼         ▼
 Precisa    Retorna
validação?  lista?
    │         │
   Sim       Sim
    │         │
    ▼         ▼
Validator  Paginação
```

## Troubleshooting

### Erro: Handler não encontrado pelo MediatR
**Causa**: Assembly não registrado ou handler não público
**Solução**: Verificar `AddMediatR(cfg => cfg.RegisterServicesFromAssembly(...))`

### Erro: Validator não executa
**Causa**: `ValidationBehavior` não registrado
**Solução**: Adicionar `services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>))`

### Erro: Dependência não resolvida no Handler
**Causa**: Interface não registrada no DI
**Solução**: Verificar registro em `Infrastructure/DependencyInjection.cs`
