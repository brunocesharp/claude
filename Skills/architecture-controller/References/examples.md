# Exemplos Completos de Endpoints

## Exemplo 1: CRUD Completo com Controller

### Entidade: Product

#### 1. Request Models

```csharp
// Presentation/Models/Requests/CreateProductRequest.cs
namespace Presentation.Models.Requests;

public record CreateProductRequest(
    string Name,
    string? Description,
    decimal Price,
    int StockQuantity,
    Guid CategoryId);

// Presentation/Models/Requests/UpdateProductRequest.cs
namespace Presentation.Models.Requests;

public record UpdateProductRequest(
    string Name,
    string? Description,
    decimal Price,
    int StockQuantity);

// Presentation/Models/Requests/ProductFilterRequest.cs
namespace Presentation.Models.Requests;

public record ProductFilterRequest(
    int PageNumber = 1,
    int PageSize = 10,
    string? SearchTerm = null,
    Guid? CategoryId = null,
    decimal? MinPrice = null,
    decimal? MaxPrice = null,
    string? SortBy = null,
    bool SortDescending = false);
```

#### 2. Validators

```csharp
// Presentation/Validators/CreateProductRequestValidator.cs
using FluentValidation;
using Presentation.Models.Requests;

namespace Presentation.Validators;

public class CreateProductRequestValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(200).WithMessage("Nome deve ter no máximo 200 caracteres");

        RuleFor(x => x.Description)
            .MaximumLength(1000).WithMessage("Descrição deve ter no máximo 1000 caracteres");

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Preço deve ser maior que zero")
            .LessThanOrEqualTo(999999.99m).WithMessage("Preço máximo excedido");

        RuleFor(x => x.StockQuantity)
            .GreaterThanOrEqualTo(0).WithMessage("Quantidade não pode ser negativa");

        RuleFor(x => x.CategoryId)
            .NotEmpty().WithMessage("Categoria é obrigatória");
    }
}

// Presentation/Validators/UpdateProductRequestValidator.cs
using FluentValidation;
using Presentation.Models.Requests;

namespace Presentation.Validators;

public class UpdateProductRequestValidator : AbstractValidator<UpdateProductRequest>
{
    public UpdateProductRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(200);

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Preço deve ser maior que zero");

        RuleFor(x => x.StockQuantity)
            .GreaterThanOrEqualTo(0);
    }
}
```

#### 3. Commands e Queries (Application Layer)

```csharp
// Application/Products/Commands/CreateProduct/CreateProductCommand.cs
using Ardalis.Result;
using MediatR;

namespace Application.Products.Commands.CreateProduct;

public record CreateProductCommand(
    string Name,
    string? Description,
    decimal Price,
    int StockQuantity,
    Guid CategoryId) : IRequest<Result<Guid>>;

// Application/Products/Commands/CreateProduct/CreateProductCommandHandler.cs
using Ardalis.Result;
using Domain.Entities;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Commands.CreateProduct;

public class CreateProductCommandHandler : IRequestHandler<CreateProductCommand, Result<Guid>>
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

    public async Task<Result<Guid>> Handle(CreateProductCommand request, CancellationToken ct)
    {
        // Verificar se categoria existe
        var categoryExists = await _categoryRepository.ExistsAsync(request.CategoryId, ct);
        if (!categoryExists)
            return Result.NotFound($"Categoria com id '{request.CategoryId}' não encontrada");

        // Verificar duplicidade
        var nameExists = await _productRepository.ExistsByNameAsync(request.Name, ct);
        if (nameExists)
            return Result.Conflict($"Produto com nome '{request.Name}' já existe");

        // Criar produto
        var product = Product.Create(
            request.Name,
            request.Description,
            Money.Create(request.Price),
            request.StockQuantity,
            request.CategoryId);

        await _productRepository.AddAsync(product, ct);
        await _unitOfWork.SaveChangesAsync(ct);

        return Result.Created(product.Id);
    }
}

// Application/Products/Queries/GetProductById/GetProductByIdQuery.cs
using Ardalis.Result;
using Application.Products.DTOs;
using MediatR;

namespace Application.Products.Queries.GetProductById;

public record GetProductByIdQuery(Guid Id) : IRequest<Result<ProductDto>>;

// Application/Products/Queries/GetProductById/GetProductByIdQueryHandler.cs
using Ardalis.Result;
using Application.Products.DTOs;
using AutoMapper;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Queries.GetProductById;

public class GetProductByIdQueryHandler : IRequestHandler<GetProductByIdQuery, Result<ProductDto>>
{
    private readonly IProductRepository _repository;
    private readonly IMapper _mapper;

    public GetProductByIdQueryHandler(IProductRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<Result<ProductDto>> Handle(GetProductByIdQuery request, CancellationToken ct)
    {
        var product = await _repository.GetByIdWithCategoryAsync(request.Id, ct);

        if (product is null)
            return Result.NotFound($"Produto com id '{request.Id}' não encontrado");

        return Result.Success(_mapper.Map<ProductDto>(product));
    }
}

// Application/Products/Queries/GetProductList/GetProductListQuery.cs
using Ardalis.Result;
using Application.Common;
using Application.Products.DTOs;
using MediatR;

namespace Application.Products.Queries.GetProductList;

public record GetProductListQuery(
    int PageNumber = 1,
    int PageSize = 10,
    string? SearchTerm = null,
    Guid? CategoryId = null,
    decimal? MinPrice = null,
    decimal? MaxPrice = null,
    string? SortBy = null,
    bool SortDescending = false) : IRequest<Result<PagedResult<ProductDto>>>;

// Application/Products/Queries/GetProductList/GetProductListQueryHandler.cs
using Ardalis.Result;
using Application.Common;
using Application.Products.DTOs;
using AutoMapper;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Queries.GetProductList;

public class GetProductListQueryHandler 
    : IRequestHandler<GetProductListQuery, Result<PagedResult<ProductDto>>>
{
    private readonly IProductRepository _repository;
    private readonly IMapper _mapper;

    public GetProductListQueryHandler(IProductRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<Result<PagedResult<ProductDto>>> Handle(
        GetProductListQuery request, 
        CancellationToken ct)
    {
        var (products, totalCount) = await _repository.GetPagedAsync(
            request.PageNumber,
            request.PageSize,
            request.SearchTerm,
            request.CategoryId,
            request.MinPrice,
            request.MaxPrice,
            request.SortBy,
            request.SortDescending,
            ct);

        var dtos = _mapper.Map<IEnumerable<ProductDto>>(products);

        return Result.Success(PagedResult<ProductDto>.Create(
            dtos,
            request.PageNumber,
            request.PageSize,
            totalCount));
    }
}
```

#### 4. DTO

```csharp
// Application/Products/DTOs/ProductDto.cs
namespace Application.Products.DTOs;

public record ProductDto(
    Guid Id,
    string Name,
    string? Description,
    decimal Price,
    string Currency,
    int StockQuantity,
    Guid CategoryId,
    string CategoryName,
    bool IsActive,
    DateTime CreatedAt,
    DateTime? ModifiedAt);
```

#### 5. Controller

```csharp
// Presentation/Controllers/ProductsController.cs
using Application.Products.Commands.CreateProduct;
using Application.Products.Commands.UpdateProduct;
using Application.Products.Commands.DeleteProduct;
using Application.Products.DTOs;
using Application.Products.Queries.GetProductById;
using Application.Products.Queries.GetProductList;
using Application.Common;
using Microsoft.AspNetCore.Mvc;
using Presentation.Models.Requests;

namespace Presentation.Controllers;

[Route("api/[controller]")]
public class ProductsController : ApiControllerBase
{
    /// <summary>
    /// Lista produtos com paginação e filtros
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<ProductDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<PagedResult<ProductDto>>> GetAll(
        [FromQuery] ProductFilterRequest filter,
        CancellationToken ct)
    {
        var query = new GetProductListQuery(
            filter.PageNumber,
            filter.PageSize,
            filter.SearchTerm,
            filter.CategoryId,
            filter.MinPrice,
            filter.MaxPrice,
            filter.SortBy,
            filter.SortDescending);

        var result = await Mediator.Send(query, ct);
        return ToActionResult(result);
    }

    /// <summary>
    /// Obtém produto por ID
    /// </summary>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductDto>> GetById(Guid id, CancellationToken ct)
    {
        var result = await Mediator.Send(new GetProductByIdQuery(id), ct);
        return ToActionResult(result);
    }

    /// <summary>
    /// Cria novo produto
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof(Guid), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status409Conflict)]
    public async Task<ActionResult<Guid>> Create(
        [FromBody] CreateProductRequest request,
        CancellationToken ct)
    {
        var command = new CreateProductCommand(
            request.Name,
            request.Description,
            request.Price,
            request.StockQuantity,
            request.CategoryId);

        var result = await Mediator.Send(command, ct);
        
        return CreatedAtActionResult(result, nameof(GetById), new { id = result.Value });
    }

    /// <summary>
    /// Atualiza produto existente
    /// </summary>
    [HttpPut("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult> Update(
        Guid id,
        [FromBody] UpdateProductRequest request,
        CancellationToken ct)
    {
        var command = new UpdateProductCommand(
            id,
            request.Name,
            request.Description,
            request.Price,
            request.StockQuantity);

        var result = await Mediator.Send(command, ct);
        return ToActionResult(result);
    }

    /// <summary>
    /// Remove produto
    /// </summary>
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult> Delete(Guid id, CancellationToken ct)
    {
        var result = await Mediator.Send(new DeleteProductCommand(id), ct);
        return ToActionResult(result);
    }
}
```

---

## Exemplo 2: CRUD com Minimal API

```csharp
// Presentation/Endpoints/ProductEndpoints.cs
using Application.Common;
using Application.Products.Commands.CreateProduct;
using Application.Products.Commands.UpdateProduct;
using Application.Products.Commands.DeleteProduct;
using Application.Products.DTOs;
using Application.Products.Queries.GetProductById;
using Application.Products.Queries.GetProductList;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Presentation.Models.Requests;

namespace Presentation.Endpoints;

public static class ProductEndpoints
{
    public static IEndpointRouteBuilder MapProductEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/products")
            .WithTags("Products")
            .WithOpenApi();

        group.MapGet("/", GetAll)
            .WithName("GetAllProducts")
            .WithSummary("Lista produtos com paginação")
            .Produces<PagedResult<ProductDto>>();

        group.MapGet("/{id:guid}", GetById)
            .WithName("GetProductById")
            .WithSummary("Obtém produto por ID")
            .Produces<ProductDto>()
            .ProducesProblem(StatusCodes.Status404NotFound);

        group.MapPost("/", Create)
            .WithName("CreateProduct")
            .WithSummary("Cria novo produto")
            .Produces<Guid>(StatusCodes.Status201Created)
            .ProducesValidationProblem()
            .ProducesProblem(StatusCodes.Status409Conflict);

        group.MapPut("/{id:guid}", Update)
            .WithName("UpdateProduct")
            .WithSummary("Atualiza produto")
            .Produces(StatusCodes.Status204NoContent)
            .ProducesValidationProblem()
            .ProducesProblem(StatusCodes.Status404NotFound);

        group.MapDelete("/{id:guid}", Delete)
            .WithName("DeleteProduct")
            .WithSummary("Remove produto")
            .Produces(StatusCodes.Status204NoContent)
            .ProducesProblem(StatusCodes.Status404NotFound);

        return app;
    }

    private static async Task<IResult> GetAll(
        [AsParameters] ProductFilterRequest filter,
        ISender mediator,
        CancellationToken ct)
    {
        var query = new GetProductListQuery(
            filter.PageNumber,
            filter.PageSize,
            filter.SearchTerm,
            filter.CategoryId,
            filter.MinPrice,
            filter.MaxPrice,
            filter.SortBy,
            filter.SortDescending);

        var result = await mediator.Send(query, ct);
        return result.ToMinimalApiResult();
    }

    private static async Task<IResult> GetById(
        Guid id,
        ISender mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetProductByIdQuery(id), ct);
        return result.ToMinimalApiResult();
    }

    private static async Task<IResult> Create(
        CreateProductRequest request,
        ISender mediator,
        CancellationToken ct)
    {
        var command = new CreateProductCommand(
            request.Name,
            request.Description,
            request.Price,
            request.StockQuantity,
            request.CategoryId);

        var result = await mediator.Send(command, ct);

        return result.IsSuccess
            ? Results.CreatedAtRoute("GetProductById", new { id = result.Value }, result.Value)
            : result.ToMinimalApiResult();
    }

    private static async Task<IResult> Update(
        Guid id,
        UpdateProductRequest request,
        ISender mediator,
        CancellationToken ct)
    {
        var command = new UpdateProductCommand(
            id,
            request.Name,
            request.Description,
            request.Price,
            request.StockQuantity);

        var result = await mediator.Send(command, ct);
        return result.ToMinimalApiResult();
    }

    private static async Task<IResult> Delete(
        Guid id,
        ISender mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new DeleteProductCommand(id), ct);
        return result.ToMinimalApiResult();
    }
}
```

---

## Exemplo 3: Endpoint Específico (Não-CRUD)

### Cenário: Aprovar Pedido

```csharp
// Presentation/Models/Requests/ApproveOrderRequest.cs
namespace Presentation.Models.Requests;

public record ApproveOrderRequest(
    string? ApprovalNotes,
    bool SendNotification = true);

// Application/Orders/Commands/ApproveOrder/ApproveOrderCommand.cs
using Ardalis.Result;
using MediatR;

namespace Application.Orders.Commands.ApproveOrder;

public record ApproveOrderCommand(
    Guid OrderId,
    Guid ApprovedBy,
    string? ApprovalNotes,
    bool SendNotification) : IRequest<Result>;

// Application/Orders/Commands/ApproveOrder/ApproveOrderCommandHandler.cs
using Ardalis.Result;
using Domain.Entities;
using Domain.Interfaces;
using MediatR;

namespace Application.Orders.Commands.ApproveOrder;

public class ApproveOrderCommandHandler : IRequestHandler<ApproveOrderCommand, Result>
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

    public async Task<Result> Handle(ApproveOrderCommand request, CancellationToken ct)
    {
        var order = await _orderRepository.GetByIdAsync(request.OrderId, ct);

        if (order is null)
            return Result.NotFound($"Pedido '{request.OrderId}' não encontrado");

        if (order.Status != OrderStatus.PendingApproval)
            return Result.Invalid(new ValidationError(
                "Status", 
                $"Pedido não pode ser aprovado. Status atual: {order.Status}"));

        // Aprovar pedido (método de domínio)
        order.Approve(request.ApprovedBy, request.ApprovalNotes);

        await _unitOfWork.SaveChangesAsync(ct);

        // Enviar notificação
        if (request.SendNotification)
        {
            await _notificationService.SendOrderApprovedAsync(order, ct);
        }

        return Result.Success();
    }
}

// Controller endpoint
[HttpPost("{id:guid}/approve")]
[ProducesResponseType(StatusCodes.Status204NoContent)]
[ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
[ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
public async Task<ActionResult> Approve(
    Guid id,
    [FromBody] ApproveOrderRequest request,
    CancellationToken ct)
{
    var userId = User.GetUserId(); // Extension method
    
    var command = new ApproveOrderCommand(
        id,
        userId,
        request.ApprovalNotes,
        request.SendNotification);

    var result = await Mediator.Send(command, ct);
    return ToActionResult(result);
}
```
