# Unit of Work

## Conceito

O Unit of Work coordena a persistência de múltiplas operações em uma única transação. No EF Core, o `DbContext` já implementa este padrão internamente.

---

## Interface (em Domain)

```csharp
// Domain/Interfaces/IUnitOfWork.cs
using Microsoft.EntityFrameworkCore.Storage;

namespace Domain.Interfaces;

public interface IUnitOfWork : IDisposable
{
    /// <summary>
    /// Persiste todas as alterações pendentes no banco de dados.
    /// </summary>
    Task<int> SaveChangesAsync(CancellationToken ct = default);
    
    /// <summary>
    /// Inicia uma transação explícita.
    /// </summary>
    Task<IDbContextTransaction> BeginTransactionAsync(CancellationToken ct = default);
}
```

---

## Implementação (DbContext já implementa)

```csharp
// Infrastructure/Persistence/ApplicationDbContext.cs
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;

namespace Infrastructure.Persistence;

public class ApplicationDbContext : DbContext, IUnitOfWork
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) 
        : base(options)
    {
    }
    
    // IUnitOfWork implementation
    public override async Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        return await base.SaveChangesAsync(ct);
    }
    
    public async Task<IDbContextTransaction> BeginTransactionAsync(CancellationToken ct = default)
    {
        return await Database.BeginTransactionAsync(ct);
    }
    
    // Dispose já é implementado pelo DbContext
}
```

---

## Uso nos Handlers

### Uso Básico (Sem Transação Explícita)

```csharp
public class CreateProductCommandHandler : IRequestHandler<CreateProductCommand, Result<Guid>>
{
    private readonly IProductRepository _productRepository;
    private readonly IUnitOfWork _unitOfWork;

    public CreateProductCommandHandler(
        IProductRepository productRepository,
        IUnitOfWork unitOfWork)
    {
        _productRepository = productRepository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<Guid>> Handle(CreateProductCommand request, CancellationToken ct)
    {
        var product = Product.Create(request.Name, request.Price);
        
        await _productRepository.AddAsync(product, ct);
        
        // Persiste todas as alterações de uma vez
        await _unitOfWork.SaveChangesAsync(ct);
        
        return Result.Created(product.Id);
    }
}
```

### Uso com Múltiplos Repositórios

```csharp
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<Guid>>
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly ICustomerRepository _customerRepository;
    private readonly IUnitOfWork _unitOfWork;

    public CreateOrderCommandHandler(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        ICustomerRepository customerRepository,
        IUnitOfWork unitOfWork)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _customerRepository = customerRepository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<Guid>> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        // Validar customer
        var customer = await _customerRepository.GetByIdAsync(request.CustomerId, ct);
        if (customer is null)
            return Result.NotFound("Cliente não encontrado");
        
        // Criar order
        var order = Order.Create(request.CustomerId, request.ShippingAddress);
        
        // Adicionar items e atualizar estoque
        foreach (var item in request.Items)
        {
            var product = await _productRepository.GetByIdAsync(item.ProductId, ct);
            if (product is null)
                return Result.NotFound($"Produto {item.ProductId} não encontrado");
            
            // Adicionar item ao pedido
            order.AddItem(product.Id, product.Name, product.Price, item.Quantity);
            
            // Decrementar estoque (entidade tracked)
            product.DecreaseStock(item.Quantity);
        }
        
        await _orderRepository.AddAsync(order, ct);
        
        // Um único SaveChanges persiste:
        // - O novo Order
        // - Os OrderItems
        // - As atualizações de estoque dos Products
        await _unitOfWork.SaveChangesAsync(ct);
        
        return Result.Created(order.Id);
    }
}
```

### Uso com Transação Explícita

```csharp
public class TransferFundsCommandHandler : IRequestHandler<TransferFundsCommand, Result>
{
    private readonly IAccountRepository _accountRepository;
    private readonly ITransactionRepository _transactionRepository;
    private readonly IUnitOfWork _unitOfWork;

    public async Task<r> Handle(TransferFundsCommand request, CancellationToken ct)
    {
        // Iniciar transação explícita
        await using var transaction = await _unitOfWork.BeginTransactionAsync(ct);
        
        try
        {
            var sourceAccount = await _accountRepository.GetByIdAsync(request.SourceAccountId, ct);
            var targetAccount = await _accountRepository.GetByIdAsync(request.TargetAccountId, ct);
            
            if (sourceAccount is null || targetAccount is null)
                return Result.NotFound("Conta não encontrada");
            
            // Operações de domínio
            sourceAccount.Withdraw(request.Amount);
            targetAccount.Deposit(request.Amount);
            
            // Registrar transação
            var txn = FinancialTransaction.Create(
                sourceAccount.Id, 
                targetAccount.Id, 
                request.Amount);
            
            await _transactionRepository.AddAsync(txn, ct);
            
            // Persistir
            await _unitOfWork.SaveChangesAsync(ct);
            
            // Commit da transação
            await transaction.CommitAsync(ct);
            
            return Result.Success();
        }
        catch (Exception)
        {
            // Rollback automático se não commitado
            await transaction.RollbackAsync(ct);
            throw;
        }
    }
}
```

---

## Transaction Behavior (Pipeline)

Para aplicar transações automaticamente em Commands:

```csharp
// Application/Common/Behaviors/TransactionBehavior.cs
using Domain.Interfaces;
using MediatR;

namespace Application.Common.Behaviors;

public class TransactionBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IUnitOfWork _unitOfWork;

    public TransactionBehavior(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        var requestName = typeof(TRequest).Name;
        
        // Apenas para Commands
        if (!requestName.EndsWith("Command"))
            return await next();
        
        await using var transaction = await _unitOfWork.BeginTransactionAsync(ct);
        
        try
        {
            var response = await next();
            
            // Commit se sucesso
            await transaction.CommitAsync(ct);
            
            return response;
        }
        catch
        {
            // Rollback em caso de erro
            await transaction.RollbackAsync(ct);
            throw;
        }
    }
}
```

### Registro do Behavior

```csharp
// Application/DependencyInjection.cs
services.AddTransient(typeof(IPipelineBehavior<,>), typeof(TransactionBehavior<,>));
```

---

## Registro no DI

```csharp
// Infrastructure/DependencyInjection.cs
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration configuration)
{
    // DbContext
    services.AddDbContext<ApplicationDbContext>(options =>
        options.UseNpgsql(configuration.GetConnectionString("DefaultConnection")));
    
    // Unit of Work - Registrar o DbContext como IUnitOfWork
    services.AddScoped<IUnitOfWork>(sp => 
        sp.GetRequiredService<ApplicationDbContext>());
    
    // Repositories...
    
    return services;
}
```

---

## Quando Usar Transação Explícita

| Cenário | Transação Implícita | Transação Explícita |
|---------|---------------------|---------------------|
| CRUD simples | ✅ | ❌ |
| Múltiplas entidades relacionadas | ✅ | ❌ |
| Operações que podem falhar parcialmente | ❌ | ✅ |
| Chamadas a serviços externos | ❌ | ✅ |
| Operações financeiras | ❌ | ✅ |
| Saga / Compensação | ❌ | ✅ |

### Exemplo: Quando NÃO precisa de transação explícita

```csharp
// EF Core já envolve SaveChangesAsync em uma transação
public async Task<Result<Guid>> Handle(CreateOrderCommand request, CancellationToken ct)
{
    var order = Order.Create(...);
    
    foreach (var item in request.Items)
    {
        order.AddItem(...);
    }
    
    await _orderRepository.AddAsync(order, ct);
    
    // Tudo isso é persistido atomicamente
    await _unitOfWork.SaveChangesAsync(ct);
    
    return Result.Created(order.Id);
}
```

### Exemplo: Quando PRECISA de transação explícita

```csharp
// Quando há operações que podem falhar entre múltiplos SaveChanges
// ou chamadas externas que precisam de compensação
public async Task<Result> Handle(ProcessPaymentCommand request, CancellationToken ct)
{
    await using var transaction = await _unitOfWork.BeginTransactionAsync(ct);
    
    try
    {
        // 1. Reservar estoque
        await _inventoryService.ReserveAsync(request.Items, ct);
        await _unitOfWork.SaveChangesAsync(ct);
        
        // 2. Processar pagamento (serviço externo)
        var paymentResult = await _paymentGateway.ChargeAsync(request.PaymentInfo, ct);
        
        if (!paymentResult.Success)
        {
            // Rollback - liberar estoque
            await transaction.RollbackAsync(ct);
            return Result.Error("Pagamento falhou");
        }
        
        // 3. Confirmar pedido
        order.Confirm(paymentResult.TransactionId);
        await _unitOfWork.SaveChangesAsync(ct);
        
        await transaction.CommitAsync(ct);
        
        return Result.Success();
    }
    catch (Exception)
    {
        await transaction.RollbackAsync(ct);
        throw;
    }
}
```
