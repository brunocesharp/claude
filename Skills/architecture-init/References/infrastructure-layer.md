# Infrastructure Layer

## Visão Geral

Implementa interfaces definidas em Domain e Application. Contém detalhes técnicos de persistência, integrações e serviços externos.

## Estrutura

```
Infrastructure/
├── Persistence/
│   ├── ApplicationDbContext.cs
│   ├── UnitOfWork.cs
│   ├── Configurations/
│   │   └── {Entity}Configuration.cs
│   ├── Repositories/
│   │   └── {Entity}Repository.cs
│   ├── Migrations/
│   └── Interceptors/
│       └── AuditableEntityInterceptor.cs
├── Services/
│   ├── DateTimeService.cs
│   ├── EmailService.cs
│   └── FileStorageService.cs
├── Identity/
│   ├── IdentityService.cs
│   └── JwtTokenGenerator.cs
├── External/
│   └── {ExternalApi}Client.cs
└── DependencyInjection.cs
```

## DbContext

```csharp
public class ApplicationDbContext : DbContext, IUnitOfWork
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options) { }
    
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Order> Orders => Set<Order>();
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(ApplicationDbContext).Assembly);
            
        base.OnModelCreating(modelBuilder);
    }
    
    public override async Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        // Dispatch domain events before saving
        await DispatchDomainEventsAsync();
        return await base.SaveChangesAsync(ct);
    }
    
    private async Task DispatchDomainEventsAsync()
    {
        var entities = ChangeTracker
            .Entries<AggregateRoot<Guid>>()
            .Where(e => e.Entity.DomainEvents.Any())
            .Select(e => e.Entity)
            .ToList();
            
        var events = entities
            .SelectMany(e => e.DomainEvents)
            .ToList();
            
        entities.ForEach(e => e.ClearDomainEvents());
        
        // Publish events via MediatR or similar
    }
}
```

## Entity Configuration

```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("Products");
        
        builder.HasKey(p => p.Id);
        
        builder.Property(p => p.Name)
            .HasMaxLength(200)
            .IsRequired();
            
        builder.Property(p => p.Description)
            .HasMaxLength(1000);
            
        // Value Object mapping
        builder.OwnsOne(p => p.Price, priceBuilder =>
        {
            priceBuilder.Property(m => m.Amount)
                .HasColumnName("Price")
                .HasPrecision(18, 2);
                
            priceBuilder.Property(m => m.Currency)
                .HasColumnName("Currency")
                .HasMaxLength(3);
        });
        
        builder.HasIndex(p => p.Name);
    }
}
```

## Repository Implementation

```csharp
public class ProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context;
    
    public ProductRepository(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task<Product?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        return await _context.Products
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }
    
    public async Task<IEnumerable<Product>> GetAllAsync(CancellationToken ct = default)
    {
        return await _context.Products.ToListAsync(ct);
    }
    
    public async Task AddAsync(Product product, CancellationToken ct = default)
    {
        await _context.Products.AddAsync(product, ct);
    }
    
    public void Update(Product product)
    {
        _context.Products.Update(product);
    }
    
    public void Remove(Product product)
    {
        _context.Products.Remove(product);
    }
}
```

## Auditable Interceptor

```csharp
public class AuditableEntityInterceptor : SaveChangesInterceptor
{
    private readonly ICurrentUserService _currentUser;
    private readonly IDateTimeService _dateTime;
    
    public AuditableEntityInterceptor(
        ICurrentUserService currentUser,
        IDateTimeService dateTime)
    {
        _currentUser = currentUser;
        _dateTime = dateTime;
    }
    
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken ct = default)
    {
        var context = eventData.Context;
        if (context is null) return base.SavingChangesAsync(eventData, result, ct);
        
        foreach (var entry in context.ChangeTracker.Entries<IAuditableEntity>())
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.CreatedBy = _currentUser.UserId;
                entry.Entity.CreatedAt = _dateTime.UtcNow;
            }
            
            if (entry.State == EntityState.Modified)
            {
                entry.Entity.ModifiedBy = _currentUser.UserId;
                entry.Entity.ModifiedAt = _dateTime.UtcNow;
            }
        }
        
        return base.SavingChangesAsync(eventData, result, ct);
    }
}
```

## External Service

```csharp
public class EmailService : IEmailService
{
    private readonly IOptions<EmailSettings> _settings;
    
    public EmailService(IOptions<EmailSettings> settings)
    {
        _settings = settings;
    }
    
    public async Task SendAsync(EmailMessage message, CancellationToken ct = default)
    {
        // Implementation using SMTP, SendGrid, etc.
    }
}
```

## Dependency Injection

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // DbContext
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(
                configuration.GetConnectionString("DefaultConnection"),
                b => b.MigrationsAssembly(typeof(ApplicationDbContext).Assembly.FullName)));
        
        // Unit of Work
        services.AddScoped<IUnitOfWork>(sp => 
            sp.GetRequiredService<ApplicationDbContext>());
        
        // Repositories
        services.AddScoped<IProductRepository, ProductRepository>();
        services.AddScoped<IOrderRepository, OrderRepository>();
        
        // Services
        services.AddTransient<IDateTimeService, DateTimeService>();
        services.AddTransient<IEmailService, EmailService>();
        
        // Interceptors
        services.AddScoped<AuditableEntityInterceptor>();
        
        // Options
        services.Configure<EmailSettings>(
            configuration.GetSection("Email"));
        
        return services;
    }
}
```

## Regras

1. **Implementa interfaces de Domain/Application**
2. **DbContext como Unit of Work**
3. **Configurations separadas** - uma por entidade
4. **Repositories genéricos + específicos**
5. **Interceptors para cross-cutting concerns**
6. **Options pattern para configurações**
7. **Dependency Injection centralizado**
