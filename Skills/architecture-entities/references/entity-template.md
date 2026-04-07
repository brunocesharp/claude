# Entity Template

## Estrutura de Arquivos

```
Domain/
├── Entities/
│   └── {Entity}.cs
├── Aggregates/
│   └── {AggregateRoot}.cs
├── Events/
│   └── {Entity}{Action}Event.cs
└── Exceptions/
    └── {Entity}Exception.cs
```

---

## Classes Base

### Entity Base

```csharp
// Domain/Common/Entity.cs
namespace Domain.Common;

public abstract class Entity<TId> : IEquatable<Entity<TId>>
    where TId : notnull
{
    public TId Id { get; protected set; } = default!;
    
    protected Entity(TId id)
    {
        Id = id;
    }
    
    protected Entity() { } // Para EF Core
    
    public override bool Equals(object? obj)
    {
        return obj is Entity<TId> entity && Id.Equals(entity.Id);
    }
    
    public bool Equals(Entity<TId>? other)
    {
        return Equals((object?)other);
    }
    
    public override int GetHashCode()
    {
        return Id.GetHashCode();
    }
    
    public static bool operator ==(Entity<TId>? left, Entity<TId>? right)
    {
        return Equals(left, right);
    }
    
    public static bool operator !=(Entity<TId>? left, Entity<TId>? right)
    {
        return !Equals(left, right);
    }
}
```

### Aggregate Root Base

```csharp
// Domain/Common/AggregateRoot.cs
namespace Domain.Common;

public abstract class AggregateRoot<TId> : Entity<TId>
    where TId : notnull
{
    private readonly List<IDomainEvent> _domainEvents = new();
    
    public IReadOnlyCollection<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();
    
    protected void AddDomainEvent(IDomainEvent domainEvent)
    {
        _domainEvents.Add(domainEvent);
    }
    
    public void ClearDomainEvents()
    {
        _domainEvents.Clear();
    }
    
    protected AggregateRoot(TId id) : base(id) { }
    
    protected AggregateRoot() { }
}
```

### Auditable Entity

```csharp
// Domain/Common/AuditableEntity.cs
namespace Domain.Common;

public abstract class AuditableEntity<TId> : Entity<TId>
    where TId : notnull
{
    public DateTime CreatedAt { get; private set; }
    public Guid? CreatedBy { get; private set; }
    public DateTime? ModifiedAt { get; private set; }
    public Guid? ModifiedBy { get; private set; }
    
    protected void SetCreated(Guid? userId = null)
    {
        CreatedAt = DateTime.UtcNow;
        CreatedBy = userId;
    }
    
    protected void SetModified(Guid? userId = null)
    {
        ModifiedAt = DateTime.UtcNow;
        ModifiedBy = userId;
    }
    
    protected AuditableEntity(TId id) : base(id) { }
    
    protected AuditableEntity() { }
}
```

### Soft Delete

```csharp
// Domain/Common/ISoftDeletable.cs
namespace Domain.Common;

public interface ISoftDeletable
{
    bool IsDeleted { get; }
    DateTime? DeletedAt { get; }
    Guid? DeletedBy { get; }
    void Delete(Guid? userId = null);
    void Restore();
}

// Implementação na entidade
public class Product : AuditableEntity<Guid>, ISoftDeletable
{
    public bool IsDeleted { get; private set; }
    public DateTime? DeletedAt { get; private set; }
    public Guid? DeletedBy { get; private set; }
    
    public void Delete(Guid? userId = null)
    {
        IsDeleted = true;
        DeletedAt = DateTime.UtcNow;
        DeletedBy = userId;
    }
    
    public void Restore()
    {
        IsDeleted = false;
        DeletedAt = null;
        DeletedBy = null;
    }
}
```

---

## Exemplos Completos

### Entity Simples

```csharp
// Domain/Entities/Category.cs
using Domain.Common;

namespace Domain.Entities;

public class Category : AuditableEntity<Guid>
{
    public string Name { get; private set; } = string.Empty;
    public string? Description { get; private set; }
    public bool IsActive { get; private set; }
    
    // Navegação (somente leitura)
    private readonly List<Product> _products = new();
    public IReadOnlyCollection<Product> Products => _products.AsReadOnly();
    
    // Construtor privado
    private Category(string name, string? description) : base(Guid.NewGuid())
    {
        Name = name;
        Description = description;
        IsActive = true;
        SetCreated();
    }
    
    private Category() { } // EF Core
    
    // Factory method
    public static Category Create(string name, string? description = null)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Nome da categoria é obrigatório", nameof(name));
        
        if (name.Length > 100)
            throw new ArgumentException("Nome deve ter no máximo 100 caracteres", nameof(name));
        
        return new Category(name, description);
    }
    
    // Métodos de domínio
    public void Update(string name, string? description)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Nome da categoria é obrigatório", nameof(name));
        
        Name = name;
        Description = description;
        SetModified();
    }
    
    public void Activate()
    {
        IsActive = true;
        SetModified();
    }
    
    public void Deactivate()
    {
        IsActive = false;
        SetModified();
    }
}
```

### Aggregate Root com Itens

```csharp
// Domain/Aggregates/Order.cs
using Domain.Common;
using Domain.Entities;
using Domain.Enums;
using Domain.Events;
using Domain.Exceptions;
using Domain.ValueObjects;

namespace Domain.Aggregates;

public class Order : AggregateRoot<Guid>
{
    public Guid CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; } = Money.Zero();
    public Address ShippingAddress { get; private set; } = null!;
    public DateTime OrderDate { get; private set; }
    public DateTime? ShippedDate { get; private set; }
    public string? Notes { get; private set; }
    
    // Coleção de itens (parte do agregado)
    private readonly List<OrderItem> _items = new();
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();
    
    // Construtor privado
    private Order(Guid customerId, Address shippingAddress, string? notes) 
        : base(Guid.NewGuid())
    {
        CustomerId = customerId;
        ShippingAddress = shippingAddress;
        Notes = notes;
        Status = OrderStatus.Draft;
        OrderDate = DateTime.UtcNow;
    }
    
    private Order() { } // EF Core
    
    // Factory method
    public static Order Create(Guid customerId, Address shippingAddress, string? notes = null)
    {
        if (customerId == Guid.Empty)
            throw new ArgumentException("Cliente é obrigatório", nameof(customerId));
        
        ArgumentNullException.ThrowIfNull(shippingAddress);
        
        var order = new Order(customerId, shippingAddress, notes);
        order.AddDomainEvent(new OrderCreatedEvent(order.Id, customerId));
        
        return order;
    }
    
    // Métodos de domínio
    public void AddItem(Guid productId, string productName, Money unitPrice, int quantity)
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOrderStateException("Itens só podem ser adicionados em pedidos em rascunho");
        
        if (quantity <= 0)
            throw new ArgumentException("Quantidade deve ser maior que zero", nameof(quantity));
        
        var existingItem = _items.FirstOrDefault(i => i.ProductId == productId);
        
        if (existingItem is not null)
        {
            existingItem.IncreaseQuantity(quantity);
        }
        else
        {
            var item = OrderItem.Create(Id, productId, productName, unitPrice, quantity);
            _items.Add(item);
        }
        
        RecalculateTotal();
    }
    
    public void RemoveItem(Guid productId)
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOrderStateException("Itens só podem ser removidos de pedidos em rascunho");
        
        var item = _items.FirstOrDefault(i => i.ProductId == productId);
        
        if (item is null)
            throw new OrderItemNotFoundException(productId);
        
        _items.Remove(item);
        RecalculateTotal();
    }
    
    public void Submit()
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOrderStateException("Apenas pedidos em rascunho podem ser submetidos");
        
        if (!_items.Any())
            throw new InvalidOrderStateException("Pedido deve ter pelo menos um item");
        
        Status = OrderStatus.Pending;
        AddDomainEvent(new OrderSubmittedEvent(Id, CustomerId, TotalAmount.Amount));
    }
    
    public void Approve(Guid approvedBy)
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOrderStateException("Apenas pedidos pendentes podem ser aprovados");
        
        Status = OrderStatus.Approved;
        AddDomainEvent(new OrderApprovedEvent(Id, approvedBy));
    }
    
    public void Ship(string trackingNumber)
    {
        if (Status != OrderStatus.Approved)
            throw new InvalidOrderStateException("Apenas pedidos aprovados podem ser enviados");
        
        Status = OrderStatus.Shipped;
        ShippedDate = DateTime.UtcNow;
        AddDomainEvent(new OrderShippedEvent(Id, trackingNumber));
    }
    
    public void Cancel(string reason)
    {
        if (Status == OrderStatus.Shipped || Status == OrderStatus.Delivered)
            throw new InvalidOrderStateException("Pedidos enviados ou entregues não podem ser cancelados");
        
        Status = OrderStatus.Cancelled;
        AddDomainEvent(new OrderCancelledEvent(Id, reason));
    }
    
    public void UpdateShippingAddress(Address newAddress)
    {
        if (Status == OrderStatus.Shipped || Status == OrderStatus.Delivered)
            throw new InvalidOrderStateException("Endereço não pode ser alterado após envio");
        
        ShippingAddress = newAddress ?? throw new ArgumentNullException(nameof(newAddress));
    }
    
    private void RecalculateTotal()
    {
        var total = _items.Sum(i => i.TotalPrice.Amount);
        TotalAmount = Money.Create(total, TotalAmount.Currency);
    }
}

// Domain/Entities/OrderItem.cs (parte do agregado Order)
namespace Domain.Entities;

public class OrderItem : Entity<Guid>
{
    public Guid OrderId { get; private set; }
    public Guid ProductId { get; private set; }
    public string ProductName { get; private set; } = string.Empty;
    public Money UnitPrice { get; private set; } = null!;
    public int Quantity { get; private set; }
    public Money TotalPrice => Money.Create(UnitPrice.Amount * Quantity, UnitPrice.Currency);
    
    private OrderItem(Guid orderId, Guid productId, string productName, Money unitPrice, int quantity)
        : base(Guid.NewGuid())
    {
        OrderId = orderId;
        ProductId = productId;
        ProductName = productName;
        UnitPrice = unitPrice;
        Quantity = quantity;
    }
    
    private OrderItem() { }
    
    internal static OrderItem Create(
        Guid orderId, 
        Guid productId, 
        string productName, 
        Money unitPrice, 
        int quantity)
    {
        return new OrderItem(orderId, productId, productName, unitPrice, quantity);
    }
    
    internal void IncreaseQuantity(int amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Quantidade deve ser positiva", nameof(amount));
        
        Quantity += amount;
    }
    
    internal void DecreaseQuantity(int amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Quantidade deve ser positiva", nameof(amount));
        
        if (Quantity - amount < 1)
            throw new InvalidOperationException("Quantidade não pode ser menor que 1");
        
        Quantity -= amount;
    }
}
```

---

## Domain Events

```csharp
// Domain/Common/IDomainEvent.cs
namespace Domain.Common;

public interface IDomainEvent
{
    Guid EventId { get; }
    DateTime OccurredOn { get; }
}

// Domain/Common/DomainEvent.cs
namespace Domain.Common;

public abstract record DomainEvent : IDomainEvent
{
    public Guid EventId { get; } = Guid.NewGuid();
    public DateTime OccurredOn { get; } = DateTime.UtcNow;
}

// Domain/Events/OrderCreatedEvent.cs
namespace Domain.Events;

public record OrderCreatedEvent(
    Guid OrderId,
    Guid CustomerId) : DomainEvent;

// Domain/Events/OrderApprovedEvent.cs
namespace Domain.Events;

public record OrderApprovedEvent(
    Guid OrderId,
    Guid ApprovedBy) : DomainEvent;

// Domain/Events/OrderShippedEvent.cs
namespace Domain.Events;

public record OrderShippedEvent(
    Guid OrderId,
    string TrackingNumber) : DomainEvent;
```

---

## Domain Exceptions

```csharp
// Domain/Exceptions/DomainException.cs
namespace Domain.Exceptions;

public abstract class DomainException : Exception
{
    protected DomainException(string message) : base(message) { }
    
    protected DomainException(string message, Exception innerException) 
        : base(message, innerException) { }
}

// Domain/Exceptions/InvalidOrderStateException.cs
namespace Domain.Exceptions;

public class InvalidOrderStateException : DomainException
{
    public InvalidOrderStateException(string message) : base(message) { }
}

// Domain/Exceptions/OrderItemNotFoundException.cs
namespace Domain.Exceptions;

public class OrderItemNotFoundException : DomainException
{
    public Guid ProductId { get; }
    
    public OrderItemNotFoundException(Guid productId) 
        : base($"Item com produto '{productId}' não encontrado no pedido")
    {
        ProductId = productId;
    }
}

// Domain/Exceptions/EntityNotFoundException.cs
namespace Domain.Exceptions;

public class EntityNotFoundException : DomainException
{
    public string EntityName { get; }
    public object EntityId { get; }
    
    public EntityNotFoundException(string entityName, object entityId) 
        : base($"{entityName} com id '{entityId}' não encontrado")
    {
        EntityName = entityName;
        EntityId = entityId;
    }
}
```

---

## Domain Enums (Strongly Typed)

```csharp
// Domain/Enums/OrderStatus.cs
namespace Domain.Enums;

public enum OrderStatus
{
    Draft = 0,
    Pending = 1,
    Approved = 2,
    Shipped = 3,
    Delivered = 4,
    Cancelled = 5
}

// Extensões para enum
public static class OrderStatusExtensions
{
    public static bool CanTransitionTo(this OrderStatus current, OrderStatus target)
    {
        return (current, target) switch
        {
            (OrderStatus.Draft, OrderStatus.Pending) => true,
            (OrderStatus.Draft, OrderStatus.Cancelled) => true,
            (OrderStatus.Pending, OrderStatus.Approved) => true,
            (OrderStatus.Pending, OrderStatus.Cancelled) => true,
            (OrderStatus.Approved, OrderStatus.Shipped) => true,
            (OrderStatus.Approved, OrderStatus.Cancelled) => true,
            (OrderStatus.Shipped, OrderStatus.Delivered) => true,
            _ => false
        };
    }
    
    public static string GetDisplayName(this OrderStatus status)
    {
        return status switch
        {
            OrderStatus.Draft => "Rascunho",
            OrderStatus.Pending => "Pendente",
            OrderStatus.Approved => "Aprovado",
            OrderStatus.Shipped => "Enviado",
            OrderStatus.Delivered => "Entregue",
            OrderStatus.Cancelled => "Cancelado",
            _ => status.ToString()
        };
    }
}
```
