# Command Template

## Estrutura de Arquivos

```
Application/
└── {Feature}/
    └── Commands/
        └── {Action}{Entity}/
            ├── {Action}{Entity}Command.cs
            ├── {Action}{Entity}CommandHandler.cs
            └── {Action}{Entity}CommandValidator.cs
```

## Command Record

```csharp
using Ardalis.Result;
using MediatR;

namespace Application.{Feature}.Commands.{Action}{Entity};

/// <summary>
/// {Descrição da operação}
/// </summary>
public record {Action}{Entity}Command(
    // Parâmetros como propriedades do record
    string Name,
    string? Description,
    decimal Price) : IRequest<Result<Guid>>;  // ou Result para void
```

### Tipos de Retorno

| Cenário | Tipo de Retorno |
|---------|-----------------|
| Create (retorna ID) | `IRequest<Result<Guid>>` |
| Update (sem retorno) | `IRequest<Result>` |
| Delete (sem retorno) | `IRequest<Result>` |
| Ação com DTO | `IRequest<Result<EntityDto>>` |

## Command Handler

```csharp
using Ardalis.Result;
using Domain.Entities;
using Domain.Interfaces;
using MediatR;

namespace Application.{Feature}.Commands.{Action}{Entity};

public class {Action}{Entity}CommandHandler 
    : IRequestHandler<{Action}{Entity}Command, Result<Guid>>
{
    private readonly I{Entity}Repository _repository;
    private readonly IUnitOfWork _unitOfWork;

    public {Action}{Entity}CommandHandler(
        I{Entity}Repository repository,
        IUnitOfWork unitOfWork)
    {
        _repository = repository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<Guid>> Handle(
        {Action}{Entity}Command request, 
        CancellationToken ct)
    {
        // 1. Validações de negócio
        // (validações que dependem de estado/banco)
        
        // 2. Criar/Modificar entidade
        
        // 3. Persistir
        
        // 4. Retornar resultado
    }
}
```

## Command Validator

```csharp
using FluentValidation;

namespace Application.{Feature}.Commands.{Action}{Entity};

public class {Action}{Entity}CommandValidator 
    : AbstractValidator<{Action}{Entity}Command>
{
    public {Action}{Entity}CommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(200).WithMessage("Nome deve ter no máximo 200 caracteres");

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Preço deve ser maior que zero");
    }
}
```

---

## Exemplos Completos

### CREATE Command

```csharp
// CreateProductCommand.cs
using Ardalis.Result;
using MediatR;

namespace Application.Products.Commands.CreateProduct;

public record CreateProductCommand(
    string Name,
    string? Description,
    decimal Price,
    int StockQuantity,
    Guid CategoryId) : IRequest<Result<Guid>>;

// CreateProductCommandHandler.cs
using Ardalis.Result;
using Domain.Entities;
using Domain.Interfaces;
using Domain.ValueObjects;
using MediatR;

namespace Application.Products.Commands.CreateProduct;

public class CreateProductCommandHandler 
    : IRequestHandler<CreateProductCommand, Result<Guid>>
{
    private readonly IProductRepository _productRepository;
    private readonly ICategoryRepository _categoryRepository;
    private readonly IUnitOfWork _unitOfWork;

    public CreateProductCommandHandler(
        IProductRepository productRepository,
        ICategoryRepository categoryRepository,
        IUnitOfWork unitOfWork)
    {
        _productRepository = productRepository;
        _categoryRepository = categoryRepository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<Guid>> Handle(
        CreateProductCommand request, 
        CancellationToken ct)
    {
        // Validação: Categoria existe?
        var categoryExists = await _categoryRepository.ExistsAsync(request.CategoryId, ct);
        if (!categoryExists)
            return Result.NotFound($"Categoria '{request.CategoryId}' não encontrada");

        // Validação: Nome duplicado?
        var nameExists = await _productRepository.ExistsByNameAsync(request.Name, ct);
        if (nameExists)
            return Result.Conflict($"Produto '{request.Name}' já existe");

        // Criar entidade via factory method
        var product = Product.Create(
            request.Name,
            request.Description,
            Money.Create(request.Price, "BRL"),
            request.StockQuantity,
            request.CategoryId);

        // Persistir
        await _productRepository.AddAsync(product, ct);
        await _unitOfWork.SaveChangesAsync(ct);

        return Result.Created(product.Id);
    }
}

// CreateProductCommandValidator.cs
using FluentValidation;

namespace Application.Products.Commands.CreateProduct;

public class CreateProductCommandValidator 
    : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(200).WithMessage("Nome deve ter no máximo 200 caracteres");

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Preço deve ser maior que zero")
            .LessThanOrEqualTo(999999.99m).WithMessage("Preço excede o limite");

        RuleFor(x => x.StockQuantity)
            .GreaterThanOrEqualTo(0).WithMessage("Quantidade não pode ser negativa");

        RuleFor(x => x.CategoryId)
            .NotEmpty().WithMessage("Categoria é obrigatória");
    }
}
```

### UPDATE Command

```csharp
// UpdateProductCommand.cs
using Ardalis.Result;
using MediatR;

namespace Application.Products.Commands.UpdateProduct;

public record UpdateProductCommand(
    Guid Id,
    string Name,
    string? Description,
    decimal Price,
    int StockQuantity) : IRequest<Result>;

// UpdateProductCommandHandler.cs
using Ardalis.Result;
using Domain.Interfaces;
using Domain.ValueObjects;
using MediatR;

namespace Application.Products.Commands.UpdateProduct;

public class UpdateProductCommandHandler 
    : IRequestHandler<UpdateProductCommand, Result>
{
    private readonly IProductRepository _repository;
    private readonly IUnitOfWork _unitOfWork;

    public UpdateProductCommandHandler(
        IProductRepository repository,
        IUnitOfWork unitOfWork)
    {
        _repository = repository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result> Handle(
        UpdateProductCommand request, 
        CancellationToken ct)
    {
        var product = await _repository.GetByIdAsync(request.Id, ct);
        
        if (product is null)
            return Result.NotFound($"Produto '{request.Id}' não encontrado");

        // Validação: Nome duplicado (exceto ele mesmo)?
        var nameExists = await _repository.ExistsByNameAsync(request.Name, request.Id, ct);
        if (nameExists)
            return Result.Conflict($"Produto '{request.Name}' já existe");

        // Atualizar via método de domínio
        product.Update(
            request.Name,
            request.Description,
            Money.Create(request.Price, "BRL"),
            request.StockQuantity);

        // Persistir (EF Core tracked)
        await _unitOfWork.SaveChangesAsync(ct);

        return Result.Success();
    }
}
```

### DELETE Command

```csharp
// DeleteProductCommand.cs
using Ardalis.Result;
using MediatR;

namespace Application.Products.Commands.DeleteProduct;

public record DeleteProductCommand(Guid Id) : IRequest<Result>;

// DeleteProductCommandHandler.cs
using Ardalis.Result;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Commands.DeleteProduct;

public class DeleteProductCommandHandler 
    : IRequestHandler<DeleteProductCommand, Result>
{
    private readonly IProductRepository _repository;
    private readonly IUnitOfWork _unitOfWork;

    public DeleteProductCommandHandler(
        IProductRepository repository,
        IUnitOfWork unitOfWork)
    {
        _repository = repository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result> Handle(
        DeleteProductCommand request, 
        CancellationToken ct)
    {
        var product = await _repository.GetByIdAsync(request.Id, ct);
        
        if (product is null)
            return Result.NotFound($"Produto '{request.Id}' não encontrado");

        // Validação: Pode deletar?
        if (product.HasActiveOrders)
            return Result.Invalid(new ValidationError(
                "Id", 
                "Produto possui pedidos ativos e não pode ser removido"));

        // Soft delete ou hard delete
        product.Deactivate(); // ou _repository.Remove(product);
        
        await _unitOfWork.SaveChangesAsync(ct);

        return Result.Success();
    }
}
```

### ACTION Command (Não-CRUD)

```csharp
// ApproveOrderCommand.cs
using Ardalis.Result;
using MediatR;

namespace Application.Orders.Commands.ApproveOrder;

public record ApproveOrderCommand(
    Guid OrderId,
    Guid ApprovedBy,
    string? Notes) : IRequest<Result>;

// ApproveOrderCommandHandler.cs
using Ardalis.Result;
using Domain.Entities;
using Domain.Interfaces;
using MediatR;

namespace Application.Orders.Commands.ApproveOrder;

public class ApproveOrderCommandHandler 
    : IRequestHandler<ApproveOrderCommand, Result>
{
    private readonly IOrderRepository _orderRepository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly INotificationService _notificationService;

    public ApproveOrderCommandHandler(
        IOrderRepository orderRepository,
        IUnitOfWork unitOfWork,
        INotificationService notificationService)
    {
        _orderRepository = orderRepository;
        _unitOfWork = unitOfWork;
        _notificationService = notificationService;
    }

    public async Task<Result> Handle(
        ApproveOrderCommand request, 
        CancellationToken ct)
    {
        var order = await _orderRepository.GetByIdAsync(request.OrderId, ct);
        
        if (order is null)
            return Result.NotFound($"Pedido '{request.OrderId}' não encontrado");

        // Validação de estado
        if (order.Status != OrderStatus.PendingApproval)
            return Result.Invalid(new ValidationError(
                "Status", 
                $"Pedido não pode ser aprovado. Status atual: {order.Status}"));

        // Executar ação de domínio
        order.Approve(request.ApprovedBy, request.Notes);

        await _unitOfWork.SaveChangesAsync(ct);

        // Side effect (pode ser via Domain Event também)
        await _notificationService.NotifyOrderApprovedAsync(order, ct);

        return Result.Success();
    }
}
```

---

## Validações: Validator vs Handler

| Tipo | Onde Colocar | Exemplo |
|------|--------------|---------|
| Formato/Estrutura | **Validator** | Campo obrigatório, tamanho máximo, formato email |
| Regra de Negócio Simples | **Validator** | Preço > 0, Data futura |
| Regra que depende de BD | **Handler** | Nome único, entidade existe |
| Regra de Estado | **Handler** | Status permite ação, permissão do usuário |

```csharp
// Validator - regras estruturais (síncronas, sem I/O)
public class CreateProductCommandValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Price).GreaterThan(0);
    }
}

// Handler - regras de negócio (assíncronas, com I/O)
public async Task<Result<Guid>> Handle(CreateProductCommand request, CancellationToken ct)
{
    // Regra que depende do banco
    if (await _repository.ExistsByNameAsync(request.Name, ct))
        return Result.Conflict("Nome já existe");
    
    // Regra de relacionamento
    if (!await _categoryRepository.ExistsAsync(request.CategoryId, ct))
        return Result.NotFound("Categoria não encontrada");
    
    // ... resto do handler
}
```
