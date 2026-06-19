# Application Layer

## Visão Geral

Orquestra casos de uso. Coordena fluxos entre Domain e Infrastructure através de interfaces.

## Estrutura

```
Application/
├── Common/
│   ├── Interfaces/
│   │   ├── IUnitOfWork.cs
│   │   └── ICurrentUserService.cs
│   ├── Behaviors/
│   │   ├── ValidationBehavior.cs
│   │   └── LoggingBehavior.cs
│   └── Exceptions/
│       └── ApplicationException.cs
├── {Feature}/
│   ├── Commands/
│   │   ├── Create{Entity}/
│   │   │   ├── Create{Entity}Command.cs
│   │   │   ├── Create{Entity}CommandHandler.cs
│   │   │   └── Create{Entity}CommandValidator.cs
│   │   └── Update{Entity}/
│   │       └── ...
│   ├── Queries/
│   │   ├── Get{Entity}ById/
│   │   │   ├── Get{Entity}ByIdQuery.cs
│   │   │   └── Get{Entity}ByIdQueryHandler.cs
│   │   └── Get{Entity}List/
│   │       └── ...
│   └── DTOs/
│       └── {Entity}Dto.cs
├── Mappings/
│   └── MappingProfile.cs
└── DependencyInjection.cs
```

## Command (CQRS)

```csharp
public record CreateProductCommand(
    string Name,
    string Description,
    decimal Price) : IRequest<Guid>;

public class CreateProductCommandHandler 
    : IRequestHandler<CreateProductCommand, Guid>
{
    private readonly IProductRepository _repository;
    private readonly IUnitOfWork _unitOfWork;
    
    public CreateProductCommandHandler(
        IProductRepository repository,
        IUnitOfWork unitOfWork)
    {
        _repository = repository;
        _unitOfWork = unitOfWork;
    }
    
    public async Task<Guid> Handle(
        CreateProductCommand request, 
        CancellationToken ct)
    {
        var product = Product.Create(
            request.Name,
            request.Description,
            Money.Create(request.Price));
            
        await _repository.AddAsync(product, ct);
        await _unitOfWork.SaveChangesAsync(ct);
        
        return product.Id;
    }
}
```

## Query (CQRS)

```csharp
public record GetProductByIdQuery(Guid Id) : IRequest<ProductDto?>;

public class GetProductByIdQueryHandler 
    : IRequestHandler<GetProductByIdQuery, ProductDto?>
{
    private readonly IProductRepository _repository;
    private readonly IMapper _mapper;
    
    public GetProductByIdQueryHandler(
        IProductRepository repository,
        IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }
    
    public async Task<ProductDto?> Handle(
        GetProductByIdQuery request, 
        CancellationToken ct)
    {
        var product = await _repository.GetByIdAsync(request.Id, ct);
        return product is null ? null : _mapper.Map<ProductDto>(product);
    }
}
```

## Validator (FluentValidation)

```csharp
public class CreateProductCommandValidator 
    : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(200);
            
        RuleFor(x => x.Price)
            .GreaterThan(0);
    }
}
```

## Validation Behavior (Pipeline)

```csharp
public class ValidationBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;
    
    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }
    
    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        if (!_validators.Any())
            return await next();
            
        var context = new ValidationContext<TRequest>(request);
        
        var failures = _validators
            .Select(v => v.Validate(context))
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();
            
        if (failures.Any())
            throw new ValidationException(failures);
            
        return await next();
    }
}
```

## Unit of Work Interface

```csharp
public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken ct = default);
}
```

## DTO

```csharp
public record ProductDto(
    Guid Id,
    string Name,
    string Description,
    decimal Price,
    DateTime CreatedAt);
```

## Mapping Profile

```csharp
public class MappingProfile : Profile
{
    public MappingProfile()
    {
        CreateMap<Product, ProductDto>()
            .ForMember(d => d.Price, opt => opt.MapFrom(s => s.Price.Amount));
    }
}
```

## Dependency Injection

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(cfg => 
            cfg.RegisterServicesFromAssembly(typeof(DependencyInjection).Assembly));
            
        services.AddValidatorsFromAssembly(typeof(DependencyInjection).Assembly);
        
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        
        services.AddAutoMapper(typeof(DependencyInjection).Assembly);
        
        return services;
    }
}
```

## Regras

1. **Depende apenas de Domain**
2. **Commands alteram estado** - retornam Id ou void
3. **Queries apenas leem** - retornam DTOs
4. **Handlers são classes** - um handler por command/query
5. **Validators separados** - FluentValidation
6. **DTOs são records** - imutáveis
7. **Sem lógica de infraestrutura** - apenas interfaces
