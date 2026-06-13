# Estrutura de Arquivos para Endpoints

## Organização por Camada

```
src/
├── Presentation/
│   ├── Controllers/
│   │   ├── ApiControllerBase.cs
│   │   └── {Entity}Controller.cs
│   ├── Endpoints/
│   │   └── {Entity}Endpoints.cs
│   ├── Models/
│   │   ├── Requests/
│   │   │   ├── Create{Entity}Request.cs
│   │   │   ├── Update{Entity}Request.cs
│   │   │   └── {Entity}FilterRequest.cs
│   │   └── Responses/
│   │       └── {Entity}Response.cs
│   └── Validators/
│       ├── Create{Entity}RequestValidator.cs
│       └── Update{Entity}RequestValidator.cs
│
├── Application/
│   └── {Entity}/
│       ├── Commands/
│       │   ├── Create{Entity}/
│       │   │   ├── Create{Entity}Command.cs
│       │   │   └── Create{Entity}CommandHandler.cs
│       │   ├── Update{Entity}/
│       │   │   ├── Update{Entity}Command.cs
│       │   │   └── Update{Entity}CommandHandler.cs
│       │   └── Delete{Entity}/
│       │       ├── Delete{Entity}Command.cs
│       │       └── Delete{Entity}CommandHandler.cs
│       ├── Queries/
│       │   ├── Get{Entity}ById/
│       │   │   ├── Get{Entity}ByIdQuery.cs
│       │   │   └── Get{Entity}ByIdQueryHandler.cs
│       │   └── Get{Entity}List/
│       │       ├── Get{Entity}ListQuery.cs
│       │       └── Get{Entity}ListQueryHandler.cs
│       └── DTOs/
│           └── {Entity}Dto.cs
│
├── Domain/
│   ├── Entities/
│   │   └── {Entity}.cs
│   └── Interfaces/
│       └── I{Entity}Repository.cs
│
└── Infrastructure/
    └── Persistence/
        └── Repositories/
            └── {Entity}Repository.cs
```

## Arquivos Necessários por Operação

### CREATE (POST)

| Camada | Arquivo | Conteúdo |
|--------|---------|----------|
| Presentation | `Models/Requests/Create{Entity}Request.cs` | Record com campos de entrada |
| Presentation | `Validators/Create{Entity}RequestValidator.cs` | Validação FluentValidation |
| Application | `Commands/Create{Entity}/Create{Entity}Command.cs` | Command MediatR |
| Application | `Commands/Create{Entity}/Create{Entity}CommandHandler.cs` | Handler com lógica |
| Domain | `Entities/{Entity}.cs` | Método `Create()` factory |

### READ (GET by ID)

| Camada | Arquivo | Conteúdo |
|--------|---------|----------|
| Application | `Queries/Get{Entity}ById/Get{Entity}ByIdQuery.cs` | Query MediatR |
| Application | `Queries/Get{Entity}ById/Get{Entity}ByIdQueryHandler.cs` | Handler |
| Application | `DTOs/{Entity}Dto.cs` | DTO de retorno |

### READ (GET List/Paged)

| Camada | Arquivo | Conteúdo |
|--------|---------|----------|
| Presentation | `Models/Requests/{Entity}FilterRequest.cs` | Filtros e paginação |
| Application | `Queries/Get{Entity}List/Get{Entity}ListQuery.cs` | Query com filtros |
| Application | `Queries/Get{Entity}List/Get{Entity}ListQueryHandler.cs` | Handler paginado |

### UPDATE (PUT)

| Camada | Arquivo | Conteúdo |
|--------|---------|----------|
| Presentation | `Models/Requests/Update{Entity}Request.cs` | Record com campos |
| Presentation | `Validators/Update{Entity}RequestValidator.cs` | Validação |
| Application | `Commands/Update{Entity}/Update{Entity}Command.cs` | Command |
| Application | `Commands/Update{Entity}/Update{Entity}CommandHandler.cs` | Handler |
| Domain | `Entities/{Entity}.cs` | Método `Update()` |

### DELETE (DELETE)

| Camada | Arquivo | Conteúdo |
|--------|---------|----------|
| Application | `Commands/Delete{Entity}/Delete{Entity}Command.cs` | Command |
| Application | `Commands/Delete{Entity}/Delete{Entity}CommandHandler.cs` | Handler |

## Templates de Arquivo

### Request Model

```csharp
namespace Presentation.Models.Requests;

public record Create{Entity}Request(
    string Name,
    string? Description,
    decimal Price);
```

### Validator

```csharp
using FluentValidation;
using Presentation.Models.Requests;

namespace Presentation.Validators;

public class Create{Entity}RequestValidator : AbstractValidator<Create{Entity}Request>
{
    public Create{Entity}RequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(200);

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Preço deve ser maior que zero");
    }
}
```

### Command

```csharp
using Ardalis.Result;
using MediatR;

namespace Application.{Entity}.Commands.Create{Entity};

public record Create{Entity}Command(
    string Name,
    string? Description,
    decimal Price) : IRequest<Result<Guid>>;
```

### Handler

```csharp
using Ardalis.Result;
using MediatR;

namespace Application.{Entity}.Commands.Create{Entity};

public class Create{Entity}CommandHandler 
    : IRequestHandler<Create{Entity}Command, Result<Guid>>
{
    private readonly I{Entity}Repository _repository;
    private readonly IUnitOfWork _unitOfWork;

    public Create{Entity}CommandHandler(
        I{Entity}Repository repository,
        IUnitOfWork unitOfWork)
    {
        _repository = repository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<Guid>> Handle(
        Create{Entity}Command request,
        CancellationToken ct)
    {
        var entity = Domain.Entities.{Entity}.Create(
            request.Name,
            request.Description,
            request.Price);

        await _repository.AddAsync(entity, ct);
        await _unitOfWork.SaveChangesAsync(ct);

        return Result.Created(entity.Id);
    }
}
```

### DTO

```csharp
namespace Application.{Entity}.DTOs;

public record {Entity}Dto(
    Guid Id,
    string Name,
    string? Description,
    decimal Price,
    DateTime CreatedAt,
    DateTime? ModifiedAt);
```

## Registro de Dependências

### Presentation (Program.cs ou Extension)

```csharp
// Validators são registrados automaticamente
services.AddValidatorsFromAssemblyContaining<Create{Entity}RequestValidator>();
```

### Application (DependencyInjection.cs)

```csharp
public static IServiceCollection AddApplication(this IServiceCollection services)
{
    services.AddMediatR(cfg => 
        cfg.RegisterServicesFromAssembly(typeof(DependencyInjection).Assembly));
    
    services.AddAutoMapper(typeof(DependencyInjection).Assembly);
    
    return services;
}
```
