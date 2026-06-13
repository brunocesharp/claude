# Repository Interfaces

## Conceito

Interfaces de repositório são definidas na camada **Domain**, mas implementadas na camada **Infrastructure**. Isso mantém o domínio agnóstico de persistência.

## Estrutura de Arquivos

```
Domain/
└── Interfaces/
    ├── IRepository.cs           # Interface base genérica
    ├── IProductRepository.cs    # Interface específica
    ├── IOrderRepository.cs
    └── IUnitOfWork.cs
    
Infrastructure/
└── Persistence/
    └── Repositories/
        ├── Repository.cs        # Implementação base
        ├── ProductRepository.cs
        └── OrderRepository.cs
```

---

## Interface Base Genérica

```csharp
// Domain/Interfaces/IRepository.cs
using Domain.Common;

namespace Domain.Interfaces;

public interface IRepository<TEntity, TId>
    where TEntity : AggregateRoot<TId>
    where TId : notnull
{
    // Queries básicas
    Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct = default);
    Task<IEnumerable<TEntity>> GetAllAsync(CancellationToken ct = default);
    Task<bool> ExistsAsync(TId id, CancellationToken ct = default);
    
    // Commands básicos
    Task AddAsync(TEntity entity, CancellationToken ct = default);
    void Update(TEntity entity);
    void Remove(TEntity entity);
}
```

### Com Specification Pattern

```csharp
// Domain/Interfaces/IRepository.cs
using Domain.Common;
using Domain.Specifications;

namespace Domain.Interfaces;

public interface IRepository<TEntity, TId>
    where TEntity : AggregateRoot<TId>
    where TId : notnull
{
    // Queries básicas
    Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct = default);
    Task<IEnumerable<TEntity>> GetAllAsync(CancellationToken ct = default);
    Task<bool> ExistsAsync(TId id, CancellationToken ct = default);
    
    // Queries com Specification
    Task<TEntity?> FirstOrDefaultAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default);
    
    Task<IEnumerable<TEntity>> ListAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default);
    
    Task<int> CountAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default);
    
    Task<bool> AnyAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default);
    
    // Commands básicos
    Task AddAsync(TEntity entity, CancellationToken ct = default);
    void Update(TEntity entity);
    void Remove(TEntity entity);
}
```

---

## Unit of Work

```csharp
// Domain/Interfaces/IUnitOfWork.cs
namespace Domain.Interfaces;

public interface IUnitOfWork : IDisposable
{
    Task<int> SaveChangesAsync(CancellationToken ct = default);
}

// Versão com transação explícita
public interface IUnitOfWork : IDisposable
{
    Task<int> SaveChangesAsync(CancellationToken ct = default);
    Task<IDbContextTransaction> BeginTransactionAsync(CancellationToken ct = default);
}
```

---

## Interfaces Específicas

### Repository Simples

```csharp
// Domain/Interfaces/ICategoryRepository.cs
using Domain.Entities;

namespace Domain.Interfaces;

public interface ICategoryRepository : IRepository<Category, Guid>
{
    Task<Category?> GetByNameAsync(string name, CancellationToken ct = default);
    Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default);
    Task<IEnumerable<Category>> GetActiveAsync(CancellationToken ct = default);
}
```

### Repository com Queries Complexas

```csharp
// Domain/Interfaces/IProductRepository.cs
using Domain.Entities;

namespace Domain.Interfaces;

public interface IProductRepository : IRepository<Product, Guid>
{
    // Queries por campo
    Task<Product?> GetBySkuAsync(string sku, CancellationToken ct = default);
    Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default);
    Task<bool> ExistsByNameAsync(string name, Guid excludeId, CancellationToken ct = default);
    
    // Queries com relacionamento
    Task<Product?> GetByIdWithCategoryAsync(Guid id, CancellationToken ct = default);
    Task<IEnumerable<Product>> GetByCategoryAsync(Guid categoryId, CancellationToken ct = default);
    
    // Queries com filtro
    Task<IEnumerable<Product>> GetActiveAsync(CancellationToken ct = default);
    Task<IEnumerable<Product>> GetLowStockAsync(int threshold, CancellationToken ct = default);
    
    // Queries paginadas
    Task<(IEnumerable<Product> Items, int TotalCount)> GetPagedAsync(
        int pageNumber,
        int pageSize,
        string? searchTerm = null,
        Guid? categoryId = null,
        decimal? minPrice = null,
        decimal? maxPrice = null,
        bool? isActive = null,
        string? sortBy = null,
        bool sortDescending = false,
        CancellationToken ct = default);
    
    // Full-text search
    Task<(IEnumerable<Product> Items, int TotalCount)> SearchAsync(
        string searchTerm,
        int pageNumber,
        int pageSize,
        CancellationToken ct = default);
}
```

### Repository de Aggregate Root

```csharp
// Domain/Interfaces/IOrderRepository.cs
using Domain.Aggregates;
using Domain.Enums;

namespace Domain.Interfaces;

public interface IOrderRepository : IRepository<Order, Guid>
{
    // Queries com Include
    Task<Order?> GetByIdWithItemsAsync(Guid id, CancellationToken ct = default);
    Task<Order?> GetByIdWithItemsAndCustomerAsync(Guid id, CancellationToken ct = default);
    
    // Queries por relacionamento
    Task<IEnumerable<Order>> GetByCustomerAsync(Guid customerId, CancellationToken ct = default);
    
    // Queries por status
    Task<IEnumerable<Order>> GetByStatusAsync(OrderStatus status, CancellationToken ct = default);
    Task<IEnumerable<Order>> GetPendingApprovalAsync(CancellationToken ct = default);
    
    // Queries por período
    Task<IEnumerable<Order>> GetByDateRangeAsync(
        DateTime startDate, 
        DateTime endDate, 
        CancellationToken ct = default);
    
    // Queries paginadas
    Task<(IEnumerable<Order> Items, int TotalCount)> GetPagedAsync(
        int pageNumber,
        int pageSize,
        Guid? customerId = null,
        OrderStatus? status = null,
        DateTime? fromDate = null,
        DateTime? toDate = null,
        string? sortBy = null,
        bool sortDescending = false,
        CancellationToken ct = default);
    
    // Agregações
    Task<int> CountByStatusAsync(OrderStatus status, CancellationToken ct = default);
    Task<decimal> GetTotalRevenueAsync(DateTime? fromDate = null, DateTime? toDate = null, CancellationToken ct = default);
}
```

---

## Read-Only Repository (para Queries)

```csharp
// Domain/Interfaces/IReadRepository.cs
using Domain.Common;

namespace Domain.Interfaces;

public interface IReadRepository<TEntity, TId>
    where TEntity : Entity<TId>
    where TId : notnull
{
    Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct = default);
    Task<IEnumerable<TEntity>> GetAllAsync(CancellationToken ct = default);
    Task<bool> ExistsAsync(TId id, CancellationToken ct = default);
    Task<int> CountAsync(CancellationToken ct = default);
}
```

---

## Specification Pattern (Opcional)

```csharp
// Domain/Specifications/ISpecification.cs
using System.Linq.Expressions;

namespace Domain.Specifications;

public interface ISpecification<T>
{
    Expression<Func<T, bool>> Criteria { get; }
    List<Expression<Func<T, object>>> Includes { get; }
    List<string> IncludeStrings { get; }
    Expression<Func<T, object>>? OrderBy { get; }
    Expression<Func<T, object>>? OrderByDescending { get; }
    int? Take { get; }
    int? Skip { get; }
    bool IsPagingEnabled { get; }
}

// Domain/Specifications/BaseSpecification.cs
namespace Domain.Specifications;

public abstract class BaseSpecification<T> : ISpecification<T>
{
    public Expression<Func<T, bool>> Criteria { get; private set; } = _ => true;
    public List<Expression<Func<T, object>>> Includes { get; } = new();
    public List<string> IncludeStrings { get; } = new();
    public Expression<Func<T, object>>? OrderBy { get; private set; }
    public Expression<Func<T, object>>? OrderByDescending { get; private set; }
    public int? Take { get; private set; }
    public int? Skip { get; private set; }
    public bool IsPagingEnabled { get; private set; }
    
    protected void AddCriteria(Expression<Func<T, bool>> criteria)
    {
        Criteria = criteria;
    }
    
    protected void AddInclude(Expression<Func<T, object>> includeExpression)
    {
        Includes.Add(includeExpression);
    }
    
    protected void AddInclude(string includeString)
    {
        IncludeStrings.Add(includeString);
    }
    
    protected void ApplyOrderBy(Expression<Func<T, object>> orderByExpression)
    {
        OrderBy = orderByExpression;
    }
    
    protected void ApplyOrderByDescending(Expression<Func<T, object>> orderByDescExpression)
    {
        OrderByDescending = orderByDescExpression;
    }
    
    protected void ApplyPaging(int skip, int take)
    {
        Skip = skip;
        Take = take;
        IsPagingEnabled = true;
    }
}

// Exemplo de uso
// Domain/Specifications/ProductsByCategory.cs
namespace Domain.Specifications;

public class ProductsByCategorySpec : BaseSpecification<Product>
{
    public ProductsByCategorySpec(Guid categoryId, bool onlyActive = true)
    {
        AddCriteria(p => p.CategoryId == categoryId && (!onlyActive || p.IsActive));
        AddInclude(p => p.Category);
        ApplyOrderBy(p => p.Name);
    }
}

public class ProductsPagedSpec : BaseSpecification<Product>
{
    public ProductsPagedSpec(int pageNumber, int pageSize, string? searchTerm = null)
    {
        if (!string.IsNullOrWhiteSpace(searchTerm))
        {
            AddCriteria(p => p.Name.Contains(searchTerm) || 
                            (p.Description != null && p.Description.Contains(searchTerm)));
        }
        
        ApplyOrderByDescending(p => p.CreatedAt);
        ApplyPaging((pageNumber - 1) * pageSize, pageSize);
    }
}
```

---

## Implementação na Infrastructure

```csharp
// Infrastructure/Persistence/Repositories/Repository.cs
using Domain.Common;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public class Repository<TEntity, TId> : IRepository<TEntity, TId>
    where TEntity : AggregateRoot<TId>
    where TId : notnull
{
    protected readonly ApplicationDbContext Context;
    protected readonly DbSet<TEntity> DbSet;
    
    public Repository(ApplicationDbContext context)
    {
        Context = context;
        DbSet = context.Set<TEntity>();
    }
    
    public virtual async Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct = default)
    {
        return await DbSet.FindAsync(new object[] { id }, ct);
    }
    
    public virtual async Task<IEnumerable<TEntity>> GetAllAsync(CancellationToken ct = default)
    {
        return await DbSet.ToListAsync(ct);
    }
    
    public virtual async Task<bool> ExistsAsync(TId id, CancellationToken ct = default)
    {
        return await DbSet.AnyAsync(e => e.Id.Equals(id), ct);
    }
    
    public virtual async Task AddAsync(TEntity entity, CancellationToken ct = default)
    {
        await DbSet.AddAsync(entity, ct);
    }
    
    public virtual void Update(TEntity entity)
    {
        DbSet.Update(entity);
    }
    
    public virtual void Remove(TEntity entity)
    {
        DbSet.Remove(entity);
    }
}

// Infrastructure/Persistence/Repositories/ProductRepository.cs
using Domain.Entities;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public class ProductRepository : Repository<Product, Guid>, IProductRepository
{
    public ProductRepository(ApplicationDbContext context) : base(context) { }
    
    public async Task<Product?> GetByIdWithCategoryAsync(Guid id, CancellationToken ct = default)
    {
        return await DbSet
            .Include(p => p.Category)
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }
    
    public async Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default)
    {
        return await DbSet.AnyAsync(p => p.Name == name, ct);
    }
    
    public async Task<bool> ExistsByNameAsync(string name, Guid excludeId, CancellationToken ct = default)
    {
        return await DbSet.AnyAsync(p => p.Name == name && p.Id != excludeId, ct);
    }
    
    public async Task<(IEnumerable<Product> Items, int TotalCount)> GetPagedAsync(
        int pageNumber,
        int pageSize,
        string? searchTerm = null,
        Guid? categoryId = null,
        decimal? minPrice = null,
        decimal? maxPrice = null,
        bool? isActive = null,
        string? sortBy = null,
        bool sortDescending = false,
        CancellationToken ct = default)
    {
        var query = DbSet.AsQueryable();
        
        // Filtros
        if (!string.IsNullOrWhiteSpace(searchTerm))
            query = query.Where(p => p.Name.Contains(searchTerm) || 
                                    (p.Description != null && p.Description.Contains(searchTerm)));
        
        if (categoryId.HasValue)
            query = query.Where(p => p.CategoryId == categoryId.Value);
        
        if (minPrice.HasValue)
            query = query.Where(p => p.Price.Amount >= minPrice.Value);
        
        if (maxPrice.HasValue)
            query = query.Where(p => p.Price.Amount <= maxPrice.Value);
        
        if (isActive.HasValue)
            query = query.Where(p => p.IsActive == isActive.Value);
        
        // Contagem total
        var totalCount = await query.CountAsync(ct);
        
        // Ordenação
        query = sortBy?.ToLowerInvariant() switch
        {
            "name" => sortDescending ? query.OrderByDescending(p => p.Name) : query.OrderBy(p => p.Name),
            "price" => sortDescending ? query.OrderByDescending(p => p.Price.Amount) : query.OrderBy(p => p.Price.Amount),
            "createdat" => sortDescending ? query.OrderByDescending(p => p.CreatedAt) : query.OrderBy(p => p.CreatedAt),
            _ => query.OrderByDescending(p => p.CreatedAt)
        };
        
        // Paginação
        var items = await query
            .Skip((pageNumber - 1) * pageSize)
            .Take(pageSize)
            .Include(p => p.Category)
            .ToListAsync(ct);
        
        return (items, totalCount);
    }
}
```

---

## Registro no DI

```csharp
// Infrastructure/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // DbContext
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseNpgsql(configuration.GetConnectionString("DefaultConnection")));
        
        // Unit of Work
        services.AddScoped<IUnitOfWork>(sp => 
            sp.GetRequiredService<ApplicationDbContext>());
        
        // Repositories
        services.AddScoped(typeof(IRepository<,>), typeof(Repository<,>));
        services.AddScoped<IProductRepository, ProductRepository>();
        services.AddScoped<ICategoryRepository, CategoryRepository>();
        services.AddScoped<IOrderRepository, OrderRepository>();
        
        return services;
    }
}
```
