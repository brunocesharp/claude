# Padrões de Código para Endpoints

## Result Pattern

### Retornos Padronizados

```csharp
// Sucesso com dados
return Result.Success(data);

// Sucesso sem dados
return Result.Success();

// Criado
return Result.Created(data);

// Não encontrado
return Result.NotFound("Mensagem descritiva");

// Validação inválida
return Result.Invalid(new ValidationError("Campo", "Mensagem"));

// Não autorizado
return Result.Unauthorized();

// Proibido
return Result.Forbidden();

// Conflito
return Result.Conflict("Recurso já existe");

// Erro interno
return Result.Error("Erro inesperado");
```

### Conversão para ActionResult

```csharp
// Em ApiControllerBase
protected ActionResult<T> ToActionResult<T>(Result<T> result)
{
    return result.Status switch
    {
        ResultStatus.Ok => Ok(result.Value),
        ResultStatus.Created => CreatedAtAction(null, result.Value),
        ResultStatus.NotFound => NotFound(ToProblemDetails(result)),
        ResultStatus.Invalid => BadRequest(ToValidationProblemDetails(result)),
        ResultStatus.Unauthorized => Unauthorized(),
        ResultStatus.Forbidden => Forbid(),
        ResultStatus.Conflict => Conflict(ToProblemDetails(result)),
        _ => StatusCode(500, ToProblemDetails(result))
    };
}
```

## FluentValidation

### Validator Padrão

```csharp
public class CreateEntityRequestValidator : AbstractValidator<CreateEntityRequest>
{
    public CreateEntityRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(200).WithMessage("Nome deve ter no máximo 200 caracteres");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email é obrigatório")
            .EmailAddress().WithMessage("Email inválido");

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Preço deve ser maior que zero");

        RuleFor(x => x.Quantity)
            .InclusiveBetween(1, 1000).WithMessage("Quantidade deve estar entre 1 e 1000");
    }
}
```

### Validação Async (com dependência)

```csharp
public class CreateEntityRequestValidator : AbstractValidator<CreateEntityRequest>
{
    public CreateEntityRequestValidator(IEntityRepository repository)
    {
        RuleFor(x => x.Code)
            .NotEmpty()
            .MustAsync(async (code, ct) => !await repository.ExistsAsync(code, ct))
            .WithMessage("Código já existe");
    }
}
```

## MediatR

### Command (Escrita)

```csharp
public record CreateEntityCommand(
    string Name,
    string Description,
    decimal Price) : IRequest<Result<Guid>>;

public class CreateEntityCommandHandler : IRequestHandler<CreateEntityCommand, Result<Guid>>
{
    private readonly IEntityRepository _repository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;

    public CreateEntityCommandHandler(
        IEntityRepository repository,
        IUnitOfWork unitOfWork,
        IMapper mapper)
    {
        _repository = repository;
        _unitOfWork = unitOfWork;
        _mapper = mapper;
    }

    public async Task<Result<Guid>> Handle(
        CreateEntityCommand request, 
        CancellationToken ct)
    {
        if (await _repository.ExistsByNameAsync(request.Name, ct))
            return Result.Conflict($"Entidade com nome '{request.Name}' já existe");

        var entity = Entity.Create(request.Name, request.Description, request.Price);

        await _repository.AddAsync(entity, ct);
        await _unitOfWork.SaveChangesAsync(ct);

        return Result.Created(entity.Id);
    }
}
```

### Query (Leitura)

```csharp
public record GetEntityByIdQuery(Guid Id) : IRequest<Result<EntityDto>>;

public class GetEntityByIdQueryHandler : IRequestHandler<GetEntityByIdQuery, Result<EntityDto>>
{
    private readonly IEntityRepository _repository;
    private readonly IMapper _mapper;

    public GetEntityByIdQueryHandler(IEntityRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<Result<EntityDto>> Handle(
        GetEntityByIdQuery request, 
        CancellationToken ct)
    {
        var entity = await _repository.GetByIdAsync(request.Id, ct);

        if (entity is null)
            return Result.NotFound($"Entidade com id '{request.Id}' não encontrada");

        return Result.Success(_mapper.Map<EntityDto>(entity));
    }
}
```

### Query Paginada

```csharp
public record GetEntitiesQuery(
    int PageNumber = 1,
    int PageSize = 10,
    string? SearchTerm = null,
    string? SortBy = null,
    bool SortDescending = false) : IRequest<Result<PagedResult<EntityDto>>>;

public class GetEntitiesQueryHandler 
    : IRequestHandler<GetEntitiesQuery, Result<PagedResult<EntityDto>>>
{
    private readonly IEntityRepository _repository;
    private readonly IMapper _mapper;

    public async Task<Result<PagedResult<EntityDto>>> Handle(
        GetEntitiesQuery request, 
        CancellationToken ct)
    {
        var (items, totalCount) = await _repository.GetPagedAsync(
            request.PageNumber,
            request.PageSize,
            request.SearchTerm,
            request.SortBy,
            request.SortDescending,
            ct);

        var dtos = _mapper.Map<IEnumerable<EntityDto>>(items);

        return Result.Success(new PagedResult<EntityDto>(
            dtos,
            request.PageNumber,
            request.PageSize,
            totalCount));
    }
}
```

## Documentação OpenAPI

### Atributos de Controller

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType(typeof(EntityDto), StatusCodes.Status200OK)]
[ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
public async Task<ActionResult<EntityDto>> GetById(Guid id, CancellationToken ct)
```

### Atributos de Minimal API

```csharp
group.MapGet("/{id:guid}", GetById)
    .WithName("GetEntityById")
    .WithSummary("Obtém entidade por ID")
    .WithDescription("Retorna os detalhes completos de uma entidade específica")
    .Produces<EntityDto>(StatusCodes.Status200OK)
    .ProducesProblem(StatusCodes.Status404NotFound);
```

## Cancellation Token

**SEMPRE** propague `CancellationToken`:

```csharp
// Controller - binding automático
public async Task<ActionResult<EntityDto>> GetById(Guid id, CancellationToken ct)
{
    var result = await Mediator.Send(new GetEntityByIdQuery(id), ct);
    return ToActionResult(result);
}

// Minimal API - via parâmetro
app.MapGet("/{id:guid}", async (Guid id, ISender mediator, CancellationToken ct) =>
{
    var result = await mediator.Send(new GetEntityByIdQuery(id), ct);
    return result.ToMinimalApiResult();
});
```
