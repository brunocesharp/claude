# Repository Base

## Estrutura de Arquivos

```
Infrastructure/
└── Persistence/
    ├── ApplicationDbContext.cs
    └── Repositories/
        └── RepositoryBase.cs
```

---

## ApplicationDbContext

```csharp
// Infrastructure/Persistence/ApplicationDbContext.cs
using Domain.Common;
using Domain.Entities;
using Domain.Aggregates;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;
using System.Reflection;

namespace Infrastructure.Persistence;

public class ApplicationDbContext : DbContext, IUnitOfWork
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) 
        : base(options)
    {
    }
    
    // DbSets
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public DbSet<Customer> Customers => Set<Customer>();
    
    // IUnitOfWork
    public override async Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        return await base.SaveChangesAsync(ct);
    }
    
    public async Task<IDbContextTransaction> BeginTransactionAsync(CancellationToken ct = default)
    {
        return await Database.BeginTransactionAsync(ct);
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Aplicar todas as configurações do assembly
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        
        base.OnModelCreating(modelBuilder);
    }
}
```

### DbContext com Auditoria Automática

```csharp
// Infrastructure/Persistence/ApplicationDbContext.cs
using Domain.Common;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;
using Microsoft.EntityFrameworkCore.Storage;
using System.Reflection;

namespace Infrastructure.Persistence;

public class ApplicationDbContext : DbContext, IUnitOfWork
{
    private readonly ICurrentUserService? _currentUserService;
    
    public ApplicationDbContext(
        DbContextOptions<ApplicationDbContext> options,
        ICurrentUserService? currentUserService = null) 
        : base(options)
    {
        _currentUserService = currentUserService;
    }
    
    // DbSets...
    
    public override async Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        ApplyAuditInfo();
        DispatchDomainEvents();
        
        return await base.SaveChangesAsync(ct);
    }
    
    public async Task<IDbContextTransaction> BeginTransactionAsync(CancellationToken ct = default)
    {
        return await Database.BeginTransactionAsync(ct);
    }
    
    private void ApplyAuditInfo()
    {
        var entries = ChangeTracker.Entries<IAuditable>();
        var now = DateTime.UtcNow;
        var userId = _currentUserService?.UserId;
        
        foreach (var entry in entries)
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    entry.Entity.SetCreated(now, userId);
                    break;
                    
                case EntityState.Modified:
                    entry.Entity.SetModified(now, userId);
                    break;
            }
        }
    }
    
    private void DispatchDomainEvents()
    {
        var aggregateRoots = ChangeTracker
            .Entries<IAggregateRoot>()
            .Where(e => e.Entity.DomainEvents.Any())
            .Select(e => e.Entity)
            .ToList();
        
        var domainEvents = aggregateRoots
            .SelectMany(ar => ar.DomainEvents)
            .ToList();
        
        // Limpar eventos
        aggregateRoots.ForEach(ar => ar.ClearDomainEvents());
        
        // TODO: Dispatch events via MediatR ou outro mecanismo
        // foreach (var domainEvent in domainEvents)
        // {
        //     await _mediator.Publish(domainEvent);
        // }
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        
        // Global query filter para soft delete
        foreach (var entityType in modelBuilder.Model.GetEntityTypes())
        {
            if (typeof(ISoftDeletable).IsAssignableFrom(entityType.ClrType))
            {
                modelBuilder.Entity(entityType.ClrType)
                    .AddQueryFilter<ISoftDeletable>(e => !e.IsDeleted);
            }
        }
        
        base.OnModelCreating(modelBuilder);
    }
}

// Extension para query filter
public static class ModelBuilderExtensions
{
    public static void AddQueryFilter<TInterface>(
        this EntityTypeBuilder entityTypeBuilder, 
        Expression<Func<TInterface, bool>> filter)
    {
        var param = Expression.Parameter(entityTypeBuilder.Metadata.ClrType, "e");
        var body = ReplacingExpressionVisitor.Replace(
            filter.Parameters[0], 
            param, 
            filter.Body);
        
        var lambda = Expression.Lambda(body, param);
        entityTypeBuilder.HasQueryFilter(lambda);
    }
}
```

---

## RepositoryBase

```csharp
// Infrastructure/Persistence/Repositories/RepositoryBase.cs
using Domain.Common;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public abstract class RepositoryBase<TEntity, TId> : IRepository<TEntity, TId>
    where TEntity : AggregateRoot<TId>
    where TId : notnull
{
    protected readonly ApplicationDbContext Context;
    protected readonly DbSet<TEntity> DbSet;
    
    protected RepositoryBase(ApplicationDbContext context)
    {
        Context = context;
        DbSet = context.Set<TEntity>();
    }
    
    // Queries básicas
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
    
    public virtual async Task<int> CountAsync(CancellationToken ct = default)
    {
        return await DbSet.CountAsync(ct);
    }
    
    // Commands básicos
    public virtual async Task AddAsync(TEntity entity, CancellationToken ct = default)
    {
        await DbSet.AddAsync(entity, ct);
    }
    
    public virtual async Task AddRangeAsync(IEnumerable<TEntity> entities, CancellationToken ct = default)
    {
        await DbSet.AddRangeAsync(entities, ct);
    }
    
    public virtual void Update(TEntity entity)
    {
        DbSet.Update(entity);
    }
    
    public virtual void UpdateRange(IEnumerable<TEntity> entities)
    {
        DbSet.UpdateRange(entities);
    }
    
    public virtual void Remove(TEntity entity)
    {
        DbSet.Remove(entity);
    }
    
    public virtual void RemoveRange(IEnumerable<TEntity> entities)
    {
        DbSet.RemoveRange(entities);
    }
}
```

### RepositoryBase com Specification Pattern

```csharp
// Infrastructure/Persistence/Repositories/RepositoryBase.cs
using Domain.Common;
using Domain.Interfaces;
using Domain.Specifications;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public abstract class RepositoryBase<TEntity, TId> : IRepository<TEntity, TId>
    where TEntity : AggregateRoot<TId>
    where TId : notnull
{
    protected readonly ApplicationDbContext Context;
    protected readonly DbSet<TEntity> DbSet;
    
    protected RepositoryBase(ApplicationDbContext context)
    {
        Context = context;
        DbSet = context.Set<TEntity>();
    }
    
    // Queries básicas
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
    
    public virtual async Task<int> CountAsync(CancellationToken ct = default)
    {
        return await DbSet.CountAsync(ct);
    }
    
    // Queries com Specification
    public virtual async Task<TEntity?> FirstOrDefaultAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default)
    {
        return await ApplySpecification(specification).FirstOrDefaultAsync(ct);
    }
    
    public virtual async Task<IEnumerable<TEntity>> ListAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default)
    {
        return await ApplySpecification(specification).ToListAsync(ct);
    }
    
    public virtual async Task<int> CountAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default)
    {
        return await ApplySpecification(specification, evaluateCriteriaOnly: true).CountAsync(ct);
    }
    
    public virtual async Task<bool> AnyAsync(
        ISpecification<TEntity> specification, 
        CancellationToken ct = default)
    {
        return await ApplySpecification(specification, evaluateCriteriaOnly: true).AnyAsync(ct);
    }
    
    // Commands básicos
    public virtual async Task AddAsync(TEntity entity, CancellationToken ct = default)
    {
        await DbSet.AddAsync(entity, ct);
    }
    
    public virtual async Task AddRangeAsync(IEnumerable<TEntity> entities, CancellationToken ct = default)
    {
        await DbSet.AddRangeAsync(entities, ct);
    }
    
    public virtual void Update(TEntity entity)
    {
        DbSet.Update(entity);
    }
    
    public virtual void Remove(TEntity entity)
    {
        DbSet.Remove(entity);
    }
    
    // Specification helpers
    protected IQueryable<TEntity> ApplySpecification(
        ISpecification<TEntity> specification,
        bool evaluateCriteriaOnly = false)
    {
        return SpecificationEvaluator<TEntity>.GetQuery(
            DbSet.AsQueryable(), 
            specification, 
            evaluateCriteriaOnly);
    }
}

// Infrastructure/Persistence/SpecificationEvaluator.cs
namespace Infrastructure.Persistence;

public static class SpecificationEvaluator<TEntity> where TEntity : class
{
    public static IQueryable<TEntity> GetQuery(
        IQueryable<TEntity> query,
        ISpecification<TEntity> specification,
        bool evaluateCriteriaOnly = false)
    {
        // Aplicar critério (Where)
        if (specification.Criteria is not null)
        {
            query = query.Where(specification.Criteria);
        }
        
        if (evaluateCriteriaOnly)
            return query;
        
        // Aplicar Includes
        query = specification.Includes
            .Aggregate(query, (current, include) => current.Include(include));
        
        query = specification.IncludeStrings
            .Aggregate(query, (current, include) => current.Include(include));
        
        // Aplicar ordenação
        if (specification.OrderBy is not null)
        {
            query = query.OrderBy(specification.OrderBy);
        }
        else if (specification.OrderByDescending is not null)
        {
            query = query.OrderByDescending(specification.OrderByDescending);
        }
        
        // Aplicar paginação
        if (specification.IsPagingEnabled)
        {
            if (specification.Skip.HasValue)
                query = query.Skip(specification.Skip.Value);
            
            if (specification.Take.HasValue)
                query = query.Take(specification.Take.Value);
        }
        
        return query;
    }
}
```

---

## RepositoryBase para Entities (não Aggregate)

```csharp
// Para entidades que não são Aggregate Root
// Infrastructure/Persistence/Repositories/ReadRepositoryBase.cs
using Domain.Common;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Persistence.Repositories;

public abstract class ReadRepositoryBase<TEntity, TId>
    where TEntity : Entity<TId>
    where TId : notnull
{
    protected readonly ApplicationDbContext Context;
    protected readonly DbSet<TEntity> DbSet;
    
    protected ReadRepositoryBase(ApplicationDbContext context)
    {
        Context = context;
        DbSet = context.Set<TEntity>();
    }
    
    public virtual async Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct = default)
    {
        return await DbSet.AsNoTracking().FirstOrDefaultAsync(e => e.Id.Equals(id), ct);
    }
    
    public virtual async Task<IEnumerable<TEntity>> GetAllAsync(CancellationToken ct = default)
    {
        return await DbSet.AsNoTracking().ToListAsync(ct);
    }
    
    public virtual async Task<bool> ExistsAsync(TId id, CancellationToken ct = default)
    {
        return await DbSet.AnyAsync(e => e.Id.Equals(id), ct);
    }
}
```

---

## Interfaces de Suporte

```csharp
// Domain/Common/IAuditable.cs
namespace Domain.Common;

public interface IAuditable
{
    DateTime CreatedAt { get; }
    Guid? CreatedBy { get; }
    DateTime? ModifiedAt { get; }
    Guid? ModifiedBy { get; }
    
    void SetCreated(DateTime timestamp, Guid? userId);
    void SetModified(DateTime timestamp, Guid? userId);
}

// Domain/Common/IAggregateRoot.cs
namespace Domain.Common;

public interface IAggregateRoot
{
    IReadOnlyCollection<IDomainEvent> DomainEvents { get; }
    void ClearDomainEvents();
}

// Domain/Common/ISoftDeletable.cs
namespace Domain.Common;

public interface ISoftDeletable
{
    bool IsDeleted { get; }
    DateTime? DeletedAt { get; }
    Guid? DeletedBy { get; }
}

// Domain/Interfaces/IUnitOfWork.cs
namespace Domain.Interfaces;

public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken ct = default);
    Task<IDbContextTransaction> BeginTransactionAsync(CancellationToken ct = default);
}
```

---

## Registro no DI

```csharp
// Infrastructure/DependencyInjection.cs
using Domain.Interfaces;
using Infrastructure.Persistence;
using Infrastructure.Persistence.Repositories;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // DbContext
        services.AddDbContext<ApplicationDbContext>(options =>
        {
            options.UseNpgsql(
                configuration.GetConnectionString("DefaultConnection"),
                npgsqlOptions =>
                {
                    npgsqlOptions.MigrationsAssembly(typeof(ApplicationDbContext).Assembly.FullName);
                    npgsqlOptions.EnableRetryOnFailure(3);
                });
        });
        
        // Unit of Work
        services.AddScoped<IUnitOfWork>(sp => 
            sp.GetRequiredService<ApplicationDbContext>());
        
        // Repositories
        services.AddScoped<IProductRepository, ProductRepository>();
        services.AddScoped<ICategoryRepository, CategoryRepository>();
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<ICustomerRepository, CustomerRepository>();
        
        return services;
    }
}
```
