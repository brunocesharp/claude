# Query Template

## Estrutura de Arquivos

```
Application/
└── {Feature}/
    ├── Queries/
    │   ├── Get{Entity}ById/
    │   │   ├── Get{Entity}ByIdQuery.cs
    │   │   └── Get{Entity}ByIdQueryHandler.cs
    │   └── Get{Entity}List/
    │       ├── Get{Entity}ListQuery.cs
    │       └── Get{Entity}ListQueryHandler.cs
    └── DTOs/
        └── {Entity}Dto.cs
```

## Query Record

```csharp
using Ardalis.Result;
using Application.{Feature}.DTOs;
using MediatR;

namespace Application.{Feature}.Queries.Get{Entity}{Suffix};

/// <summary>
/// {Descrição da consulta}
/// </summary>
public record Get{Entity}{Suffix}Query(
    // Parâmetros de filtro/identificação
    Guid Id) : IRequest<Result<{Entity}Dto>>;
```

### Tipos de Query

| Tipo | Sufixo | Retorno | Exemplo |
|------|--------|---------|---------|
| Por ID | `ById` | `Result<EntityDto>` | `GetProductByIdQuery` |
| Lista simples | `List` | `Result<IEnumerable<EntityDto>>` | `GetProductListQuery` |
| Lista paginada | `List` | `Result<PagedResult<EntityDto>>` | `GetProductListQuery` |
| Filtro específico | `By{Filtro}` | `Result<IEnumerable<EntityDto>>` | `GetProductsByCategoryQuery` |
| Busca | `Search` | `Result<PagedResult<EntityDto>>` | `SearchProductsQuery` |

## Query Handler

```csharp
using Ardalis.Result;
using Application.{Feature}.DTOs;
using AutoMapper;
using Domain.Interfaces;
using MediatR;

namespace Application.{Feature}.Queries.Get{Entity}{Suffix};

public class Get{Entity}{Suffix}QueryHandler 
    : IRequestHandler<Get{Entity}{Suffix}Query, Result<{Entity}Dto>>
{
    private readonly I{Entity}Repository _repository;
    private readonly IMapper _mapper;

    public Get{Entity}{Suffix}QueryHandler(
        I{Entity}Repository repository,
        IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<Result<{Entity}Dto>> Handle(
        Get{Entity}{Suffix}Query request, 
        CancellationToken ct)
    {
        // 1. Buscar dados
        
        // 2. Verificar existência (se aplicável)
        
        // 3. Mapear para DTO
        
        // 4. Retornar resultado
    }
}
```

## DTO Record

```csharp
namespace Application.{Feature}.DTOs;

public record {Entity}Dto(
    Guid Id,
    string Name,
    string? Description,
    decimal Price,
    DateTime CreatedAt,
    DateTime? ModifiedAt);
```

---

## Exemplos Completos

### GET BY ID Query

```csharp
// GetProductByIdQuery.cs
using Ardalis.Result;
using Application.Products.DTOs;
using MediatR;

namespace Application.Products.Queries.GetProductById;

public record GetProductByIdQuery(Guid Id) : IRequest<Result<ProductDto>>;

// GetProductByIdQueryHandler.cs
using Ardalis.Result;
using Application.Products.DTOs;
using AutoMapper;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Queries.GetProductById;

public class GetProductByIdQueryHandler 
    : IRequestHandler<GetProductByIdQuery, Result<ProductDto>>
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

    public async Task<Result<ProductDto>> Handle(
        GetProductByIdQuery request, 
        CancellationToken ct)
    {
        var product = await _repository.GetByIdWithCategoryAsync(request.Id, ct);

        if (product is null)
            return Result.NotFound($"Produto '{request.Id}' não encontrado");

        var dto = _mapper.Map<ProductDto>(product);
        
        return Result.Success(dto);
    }
}

// ProductDto.cs
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

### GET LIST (Paginada) Query

```csharp
// GetProductListQuery.cs
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
    bool? IsActive = null,
    string? SortBy = null,
    bool SortDescending = false) : IRequest<Result<PagedResult<ProductDto>>>;

// GetProductListQueryHandler.cs
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

    public GetProductListQueryHandler(
        IProductRepository repository,
        IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<Result<PagedResult<ProductDto>>> Handle(
        GetProductListQuery request, 
        CancellationToken ct)
    {
        var (products, totalCount) = await _repository.GetPagedAsync(
            pageNumber: request.PageNumber,
            pageSize: request.PageSize,
            searchTerm: request.SearchTerm,
            categoryId: request.CategoryId,
            minPrice: request.MinPrice,
            maxPrice: request.MaxPrice,
            isActive: request.IsActive,
            sortBy: request.SortBy,
            sortDescending: request.SortDescending,
            cancellationToken: ct);

        var dtos = _mapper.Map<IEnumerable<ProductDto>>(products);

        var pagedResult = PagedResult<ProductDto>.Create(
            dtos,
            request.PageNumber,
            request.PageSize,
            totalCount);

        return Result.Success(pagedResult);
    }
}
```

### GET BY FILTER Query

```csharp
// GetProductsByCategoryQuery.cs
using Ardalis.Result;
using Application.Products.DTOs;
using MediatR;

namespace Application.Products.Queries.GetProductsByCategory;

public record GetProductsByCategoryQuery(
    Guid CategoryId,
    bool? IsActive = true) : IRequest<Result<IEnumerable<ProductDto>>>;

// GetProductsByCategoryQueryHandler.cs
using Ardalis.Result;
using Application.Products.DTOs;
using AutoMapper;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Queries.GetProductsByCategory;

public class GetProductsByCategoryQueryHandler 
    : IRequestHandler<GetProductsByCategoryQuery, Result<IEnumerable<ProductDto>>>
{
    private readonly IProductRepository _repository;
    private readonly ICategoryRepository _categoryRepository;
    private readonly IMapper _mapper;

    public GetProductsByCategoryQueryHandler(
        IProductRepository repository,
        ICategoryRepository categoryRepository,
        IMapper mapper)
    {
        _repository = repository;
        _categoryRepository = categoryRepository;
        _mapper = mapper;
    }

    public async Task<Result<IEnumerable<ProductDto>>> Handle(
        GetProductsByCategoryQuery request, 
        CancellationToken ct)
    {
        // Validar categoria existe
        var categoryExists = await _categoryRepository.ExistsAsync(request.CategoryId, ct);
        if (!categoryExists)
            return Result.NotFound($"Categoria '{request.CategoryId}' não encontrada");

        var products = await _repository.GetByCategoryAsync(
            request.CategoryId, 
            request.IsActive, 
            ct);

        var dtos = _mapper.Map<IEnumerable<ProductDto>>(products);

        return Result.Success(dtos);
    }
}
```

### SEARCH Query (Full-text)

```csharp
// SearchProductsQuery.cs
using Ardalis.Result;
using Application.Common;
using Application.Products.DTOs;
using MediatR;

namespace Application.Products.Queries.SearchProducts;

public record SearchProductsQuery(
    string SearchTerm,
    int PageNumber = 1,
    int PageSize = 10) : IRequest<Result<PagedResult<ProductSearchResultDto>>>;

// SearchProductsQueryHandler.cs
using Ardalis.Result;
using Application.Common;
using Application.Products.DTOs;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Queries.SearchProducts;

public class SearchProductsQueryHandler 
    : IRequestHandler<SearchProductsQuery, Result<PagedResult<ProductSearchResultDto>>>
{
    private readonly IProductRepository _repository;

    public SearchProductsQueryHandler(IProductRepository repository)
    {
        _repository = repository;
    }

    public async Task<Result<PagedResult<ProductSearchResultDto>>> Handle(
        SearchProductsQuery request, 
        CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(request.SearchTerm))
            return Result.Invalid(new ValidationError("SearchTerm", "Termo de busca é obrigatório"));

        if (request.SearchTerm.Length < 3)
            return Result.Invalid(new ValidationError("SearchTerm", "Termo deve ter no mínimo 3 caracteres"));

        var (results, totalCount) = await _repository.SearchAsync(
            request.SearchTerm,
            request.PageNumber,
            request.PageSize,
            ct);

        // Projeção direta (sem AutoMapper para performance)
        var dtos = results.Select(p => new ProductSearchResultDto(
            p.Id,
            p.Name,
            p.Description,
            p.Price.Amount,
            p.Category.Name));

        var pagedResult = PagedResult<ProductSearchResultDto>.Create(
            dtos,
            request.PageNumber,
            request.PageSize,
            totalCount);

        return Result.Success(pagedResult);
    }
}

// ProductSearchResultDto.cs (DTO específico para search)
namespace Application.Products.DTOs;

public record ProductSearchResultDto(
    Guid Id,
    string Name,
    string? Description,
    decimal Price,
    string CategoryName);
```

---

## PagedResult Helper

```csharp
// Application/Common/PagedResult.cs
namespace Application.Common;

public record PagedResult<T>
{
    public IEnumerable<T> Items { get; init; } = [];
    public int PageNumber { get; init; }
    public int PageSize { get; init; }
    public int TotalCount { get; init; }
    public int TotalPages { get; init; }
    public bool HasPreviousPage => PageNumber > 1;
    public bool HasNextPage => PageNumber < TotalPages;

    public static PagedResult<T> Create(
        IEnumerable<T> items,
        int pageNumber,
        int pageSize,
        int totalCount)
    {
        return new PagedResult<T>
        {
            Items = items,
            PageNumber = pageNumber,
            PageSize = pageSize,
            TotalCount = totalCount,
            TotalPages = (int)Math.Ceiling(totalCount / (double)pageSize)
        };
    }

    public static PagedResult<T> Empty(int pageNumber = 1, int pageSize = 10)
    {
        return new PagedResult<T>
        {
            Items = [],
            PageNumber = pageNumber,
            PageSize = pageSize,
            TotalCount = 0,
            TotalPages = 0
        };
    }
}
```

---

## AutoMapper Profile

```csharp
// Application/Products/MappingProfile.cs
using Application.Products.DTOs;
using AutoMapper;
using Domain.Entities;

namespace Application.Products;

public class ProductMappingProfile : Profile
{
    public ProductMappingProfile()
    {
        CreateMap<Product, ProductDto>()
            .ForMember(d => d.Price, opt => opt.MapFrom(s => s.Price.Amount))
            .ForMember(d => d.Currency, opt => opt.MapFrom(s => s.Price.Currency))
            .ForMember(d => d.CategoryName, opt => opt.MapFrom(s => s.Category.Name));

        // Projeção para lista (sem Category carregada)
        CreateMap<Product, ProductListItemDto>()
            .ForMember(d => d.Price, opt => opt.MapFrom(s => s.Price.Amount));
    }
}
```

---

## Queries NÃO devem ter Validators

Queries são operações de leitura e não precisam de FluentValidation:

```csharp
// ❌ INCORRETO - Não criar validator para Query
public class GetProductByIdQueryValidator : AbstractValidator<GetProductByIdQuery>
{
    // Não fazer isso!
}

// ✅ CORRETO - Validar no Handler se necessário
public async Task<Result<ProductDto>> Handle(GetProductByIdQuery request, CancellationToken ct)
{
    if (request.Id == Guid.Empty)
        return Result.Invalid(new ValidationError("Id", "Id inválido"));
    
    // ... resto do handler
}
```

**Exceção**: Queries com parâmetros complexos de busca podem ter validação básica no handler.
