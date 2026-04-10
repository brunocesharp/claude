# Repository Implementation

## Estrutura

```csharp
public class {Entity}Repository : RepositoryBase<{Entity}, {TId}>, I{Entity}Repository
{
    public {Entity}Repository(ApplicationDbContext context) : base(context) { }
    
    // Implementar métodos específicos da interface
}
```

---

## Exemplos Completos

### Repository Simples

```csharp
// Infrastructure/Persistence/Repositories/CategoryRepository.cs
using Domain.Entities;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public class CategoryRepository : RepositoryBase<Category, Guid>, ICategoryRepository
{
    public CategoryRepository(ApplicationDbContext context) : base(context) { }
    
    public async Task<Category?> GetByNameAsync(string name, CancellationToken ct = default)
    {
        return await DbSet
            .FirstOrDefaultAsync(c => c.Name == name, ct);
    }
    
    public async Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default)
    {
        return await DbSet
            .AnyAsync(c => c.Name == name, ct);
    }
    
    public async Task<bool> ExistsByNameAsync(string name, Guid excludeId, CancellationToken ct = default)
    {
        return await DbSet
            .AnyAsync(c => c.Name == name && c.Id != excludeId, ct);
    }
    
    public async Task<IEnumerable<Category>> GetActiveAsync(CancellationToken ct = default)
    {
        return await DbSet
            .Where(c => c.IsActive)
            .OrderBy(c => c.Name)
            .ToListAsync(ct);
    }
    
    public async Task<IEnumerable<Category>> GetWithProductCountAsync(CancellationToken ct = default)
    {
        return await DbSet
            .Include(c => c.Products)
            .OrderBy(c => c.Name)
            .ToListAsync(ct);
    }
}
```

### Repository com Queries Complexas

```csharp
// Infrastructure/Persistence/Repositories/ProductRepository.cs
using Domain.Entities;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public class ProductRepository : RepositoryBase<Product, Guid>, IProductRepository
{
    public ProductRepository(ApplicationDbContext context) : base(context) { }
    
    // Query por campo único
    public async Task<Product?> GetBySkuAsync(string sku, CancellationToken ct = default)
    {
        return await DbSet
            .FirstOrDefaultAsync(p => p.Sku == sku, ct);
    }
    
    // Query com Include
    public async Task<Product?> GetByIdWithCategoryAsync(Guid id, CancellationToken ct = default)
    {
        return await DbSet
            .Include(p => p.Category)
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }
    
    // Query com múltiplos Includes
    public async Task<Product?> GetByIdWithDetailsAsync(Guid id, CancellationToken ct = default)
    {
        return await DbSet
            .Include(p => p.Category)
            .Include(p => p.Images)
            .Include(p => p.Reviews)
                .ThenInclude(r => r.Customer)
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }
    
    // Verificação de existência
    public async Task<bool> ExistsByNameAsync(string name, CancellationToken ct = default)
    {
        return await DbSet.AnyAsync(p => p.Name == name, ct);
    }
    
    public async Task<bool> ExistsByNameAsync(string name, Guid excludeId, CancellationToken ct = default)
    {
        return await DbSet.AnyAsync(p => p.Name == name && p.Id != excludeId, ct);
    }
    
    public async Task<bool> ExistsBySkuAsync(string sku, CancellationToken ct = default)
    {
        return await DbSet.AnyAsync(p => p.Sku == sku, ct);
    }
    
    // Query por relacionamento
    public async Task<IEnumerable<Product>> GetByCategoryAsync(
        Guid categoryId, 
        CancellationToken ct = default)
    {
        return await DbSet
            .Where(p => p.CategoryId == categoryId)
            .OrderBy(p => p.Name)
            .ToListAsync(ct);
    }
    
    public async Task<IEnumerable<Product>> GetByCategoryAsync(
        Guid categoryId, 
        bool? isActive, 
        CancellationToken ct = default)
    {
        var query = DbSet.Where(p => p.CategoryId == categoryId);
        
        if (isActive.HasValue)
            query = query.Where(p => p.IsActive == isActive.Value);
        
        return await query
            .OrderBy(p => p.Name)
            .ToListAsync(ct);
    }
    
    // Query com filtros múltiplos
    public async Task<IEnumerable<Product>> GetActiveAsync(CancellationToken ct = default)
    {
        return await DbSet
            .Where(p => p.IsActive)
            .OrderBy(p => p.Name)
            .ToListAsync(ct);
    }
    
    public async Task<IEnumerable<Product>> GetLowStockAsync(
        int threshold, 
        CancellationToken ct = default)
    {
        return await DbSet
            .Where(p => p.IsActive && p.StockQuantity <= threshold)
            .OrderBy(p => p.StockQuantity)
            .ToListAsync(ct);
    }
    
    // Query paginada
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
        
        // Aplicar filtros
        if (!string.IsNullOrWhiteSpace(searchTerm))
        {
            var term = searchTerm.ToLower();
            query = query.Where(p => 
                p.Name.ToLower().Contains(term) || 
                (p.Description != null && p.Description.ToLower().Contains(term)) ||
                (p.Sku != null && p.Sku.ToLower().Contains(term)));
        }
        
        if (categoryId.HasValue)
            query = query.Where(p => p.CategoryId == categoryId.Value);
        
        if (minPrice.HasValue)
            query = query.Where(p => p.Price.Amount >= minPrice.Value);
        
        if (maxPrice.HasValue)
            query = query.Where(p => p.Price.Amount <= maxPrice.Value);
        
        if (isActive.HasValue)
            query = query.Where(p => p.IsActive == isActive.Value);
        
        // Contar total (antes de paginar)
        var totalCount = await query.CountAsync(ct);
        
        // Aplicar ordenação
        query = ApplySorting(query, sortBy, sortDescending);
        
        // Aplicar paginação
        var items = await query
            .Skip((pageNumber - 1) * pageSize)
            .Take(pageSize)
            .Include(p => p.Category)
            .AsNoTracking()
            .ToListAsync(ct);
        
        return (items, totalCount);
    }
    
    // Full-text search
    public async Task<(IEnumerable<Product> Items, int TotalCount)> SearchAsync(
        string searchTerm,
        int pageNumber,
        int pageSize,
        CancellationToken ct = default)
    {
        var term = searchTerm.ToLower();
        
        var query = DbSet
            .Where(p => p.IsActive)
            .Where(p => 
                EF.Functions.ILike(p.Name, $"%{term}%") ||
                (p.Description != null && EF.Functions.ILike(p.Description, $"%{term}%")));
        
        var totalCount = await query.CountAsync(ct);
        
        var items = await query
            .OrderByDescending(p => EF.Functions.ILike(p.Name, $"{term}%")) // Prioriza início
            .ThenBy(p => p.Name)
            .Skip((pageNumber - 1) * pageSize)
            .Take(pageSize)
            .Include(p => p.Category)
            .AsNoTracking()
            .ToListAsync(ct);
        
        return (items, totalCount);
    }
    
    // Helper para ordenação
    private static IQueryable<Product> ApplySorting(
        IQueryable<Product> query, 
        string? sortBy, 
        bool sortDescending)
    {
        return sortBy?.ToLowerInvariant() switch
        {
            "name" => sortDescending 
                ? query.OrderByDescending(p => p.Name) 
                : query.OrderBy(p => p.Name),
            "price" => sortDescending 
                ? query.OrderByDescending(p => p.Price.Amount) 
                : query.OrderBy(p => p.Price.Amount),
            "stock" => sortDescending 
                ? query.OrderByDescending(p => p.StockQuantity) 
                : query.OrderBy(p => p.StockQuantity),
            "createdat" => sortDescending 
                ? query.OrderByDescending(p => p.CreatedAt) 
                : query.OrderBy(p => p.CreatedAt),
            "category" => sortDescending 
                ? query.OrderByDescending(p => p.Category.Name) 
                : query.OrderBy(p => p.Category.Name),
            _ => query.OrderByDescending(p => p.CreatedAt) // Default
        };
    }
}
```

### Repository de Aggregate Root

```csharp
// Infrastructure/Persistence/Repositories/OrderRepository.cs
using Domain.Aggregates;
using Domain.Enums;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public class OrderRepository : RepositoryBase<Order, Guid>, IOrderRepository
{
    public OrderRepository(ApplicationDbContext context) : base(context) { }
    
    // Override GetById para incluir Items por padrão
    public override async Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        return await DbSet
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }
    
    // Query com Includes específicos
    public async Task<Order?> GetByIdWithItemsAsync(Guid id, CancellationToken ct = default)
    {
        return await DbSet
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }
    
    public async Task<Order?> GetByIdWithDetailsAsync(Guid id, CancellationToken ct = default)
    {
        return await DbSet
            .Include(o => o.Items)
            .Include(o => o.Customer)
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }
    
    // Queries por relacionamento
    public async Task<IEnumerable<Order>> GetByCustomerAsync(
        Guid customerId, 
        CancellationToken ct = default)
    {
        return await DbSet
            .Where(o => o.CustomerId == customerId)
            .Include(o => o.Items)
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync(ct);
    }
    
    // Queries por status
    public async Task<IEnumerable<Order>> GetByStatusAsync(
        OrderStatus status, 
        CancellationToken ct = default)
    {
        return await DbSet
            .Where(o => o.Status == status)
            .Include(o => o.Items)
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync(ct);
    }
    
    public async Task<IEnumerable<Order>> GetPendingApprovalAsync(CancellationToken ct = default)
    {
        return await DbSet
            .Where(o => o.Status == OrderStatus.Pending)
            .Include(o => o.Items)
            .Include(o => o.Customer)
            .OrderBy(o => o.OrderDate)
            .ToListAsync(ct);
    }
    
    // Queries por período
    public async Task<IEnumerable<Order>> GetByDateRangeAsync(
        DateTime startDate, 
        DateTime endDate, 
        CancellationToken ct = default)
    {
        return await DbSet
            .Where(o => o.OrderDate >= startDate && o.OrderDate <= endDate)
            .Include(o => o.Items)
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync(ct);
    }
    
    // Query paginada
    public async Task<(IEnumerable<Order> Items, int TotalCount)> GetPagedAsync(
        int pageNumber,
        int pageSize,
        Guid? customerId = null,
        OrderStatus? status = null,
        DateTime? fromDate = null,
        DateTime? toDate = null,
        string? sortBy = null,
        bool sortDescending = false,
        CancellationToken ct = default)
    {
        var query = DbSet.AsQueryable();
        
        // Filtros
        if (customerId.HasValue)
            query = query.Where(o => o.CustomerId == customerId.Value);
        
        if (status.HasValue)
            query = query.Where(o => o.Status == status.Value);
        
        if (fromDate.HasValue)
            query = query.Where(o => o.OrderDate >= fromDate.Value);
        
        if (toDate.HasValue)
            query = query.Where(o => o.OrderDate <= toDate.Value);
        
        // Total
        var totalCount = await query.CountAsync(ct);
        
        // Ordenação
        query = sortBy?.ToLowerInvariant() switch
        {
            "date" => sortDescending 
                ? query.OrderByDescending(o => o.OrderDate) 
                : query.OrderBy(o => o.OrderDate),
            "total" => sortDescending 
                ? query.OrderByDescending(o => o.TotalAmount.Amount) 
                : query.OrderBy(o => o.TotalAmount.Amount),
            "status" => sortDescending 
                ? query.OrderByDescending(o => o.Status) 
                : query.OrderBy(o => o.Status),
            _ => query.OrderByDescending(o => o.OrderDate)
        };
        
        // Paginação
        var items = await query
            .Skip((pageNumber - 1) * pageSize)
            .Take(pageSize)
            .Include(o => o.Items)
            .Include(o => o.Customer)
            .AsNoTracking()
            .ToListAsync(ct);
        
        return (items, totalCount);
    }
    
    // Agregações
    public async Task<int> CountByStatusAsync(
        OrderStatus status, 
        CancellationToken ct = default)
    {
        return await DbSet.CountAsync(o => o.Status == status, ct);
    }
    
    public async Task<decimal> GetTotalRevenueAsync(
        DateTime? fromDate = null, 
        DateTime? toDate = null, 
        CancellationToken ct = default)
    {
        var query = DbSet.Where(o => 
            o.Status == OrderStatus.Delivered || 
            o.Status == OrderStatus.Shipped);
        
        if (fromDate.HasValue)
            query = query.Where(o => o.OrderDate >= fromDate.Value);
        
        if (toDate.HasValue)
            query = query.Where(o => o.OrderDate <= toDate.Value);
        
        return await query.SumAsync(o => o.TotalAmount.Amount, ct);
    }
    
    public async Task<Dictionary<OrderStatus, int>> GetCountByStatusAsync(
        CancellationToken ct = default)
    {
        return await DbSet
            .GroupBy(o => o.Status)
            .Select(g => new { Status = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.Status, x => x.Count, ct);
    }
}
```

---

## Boas Práticas

### AsNoTracking para Queries de Leitura

```csharp
// ✅ Para queries que não serão modificadas
public async Task<IEnumerable<Product>> GetForDisplayAsync(CancellationToken ct)
{
    return await DbSet
        .AsNoTracking()  // Melhor performance
        .ToListAsync(ct);
}

// ❌ Não usar AsNoTracking se for modificar
public async Task<Product?> GetForUpdateAsync(Guid id, CancellationToken ct)
{
    return await DbSet
        .FirstOrDefaultAsync(p => p.Id == id, ct); // Tracked
}
```

### Projeção Direta (Melhor Performance)

```csharp
// ✅ Projetar para DTO no banco (SQL otimizado)
public async Task<IEnumerable<ProductListDto>> GetListDtoAsync(CancellationToken ct)
{
    return await DbSet
        .Select(p => new ProductListDto(
            p.Id,
            p.Name,
            p.Price.Amount,
            p.Category.Name))
        .AsNoTracking()
        .ToListAsync(ct);
}
```

### Split Query para Múltiplos Includes

```csharp
// ✅ Para evitar explosão cartesiana
public async Task<Order?> GetWithAllDetailsAsync(Guid id, CancellationToken ct)
{
    return await DbSet
        .Include(o => o.Items)
        .Include(o => o.Customer)
        .Include(o => o.Payments)
        .AsSplitQuery()  // Queries separadas
        .FirstOrDefaultAsync(o => o.Id == id, ct);
}
```
