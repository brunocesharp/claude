# Domain Layer

## Visão Geral

Camada central da arquitetura. Contém regras de negócio invariantes e não possui dependências externas.

## Estrutura

```
Domain/
├── Entities/
│   └── {Entidade}.cs
├── ValueObjects/
│   └── {ValueObject}.cs
├── Aggregates/
│   └── {AggregateRoot}.cs
├── Enums/
│   └── {Enum}.cs
├── Events/
│   └── {DomainEvent}.cs
├── Exceptions/
│   └── {DomainException}.cs
├── Interfaces/
│   ├── Repositories/
│   │   └── I{Entidade}Repository.cs
│   └── Services/
│       └── I{DomainService}.cs
└── Services/
    └── {DomainService}.cs
```

## Entidade Base

```csharp
public abstract class Entity<TId> : IEquatable<Entity<TId>>
{
    public TId Id { get; protected set; }
    
    protected Entity(TId id)
    {
        Id = id;
    }
    
    protected Entity() { }
    
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
}
```

## Value Object Base

```csharp
public abstract class ValueObject
{
    protected abstract IEnumerable<object> GetEqualityComponents();
    
    public override bool Equals(object? obj)
    {
        if (obj is null || obj.GetType() != GetType())
            return false;
            
        var other = (ValueObject)obj;
        return GetEqualityComponents()
            .SequenceEqual(other.GetEqualityComponents());
    }
    
    public override int GetHashCode()
    {
        return GetEqualityComponents()
            .Select(x => x?.GetHashCode() ?? 0)
            .Aggregate((x, y) => x ^ y);
    }
}
```

## Aggregate Root

```csharp
public abstract class AggregateRoot<TId> : Entity<TId>
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

## Domain Event

```csharp
public interface IDomainEvent
{
    DateTime OccurredOn { get; }
}

public abstract record DomainEvent : IDomainEvent
{
    public DateTime OccurredOn { get; } = DateTime.UtcNow;
}
```

## Repository Interface

```csharp
public interface IRepository<TEntity, TId> 
    where TEntity : AggregateRoot<TId>
{
    Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct = default);
    Task<IEnumerable<TEntity>> GetAllAsync(CancellationToken ct = default);
    Task AddAsync(TEntity entity, CancellationToken ct = default);
    void Update(TEntity entity);
    void Remove(TEntity entity);
}
```

## Domain Exception

```csharp
public abstract class DomainException : Exception
{
    protected DomainException(string message) : base(message) { }
}

public class EntityNotFoundException : DomainException
{
    public EntityNotFoundException(string entityName, object id)
        : base($"{entityName} com id '{id}' não encontrado.") { }
}
```

## Regras

1. **Sem dependências externas** - apenas System.*
2. **Entidades com comportamento** - métodos que encapsulam regras
3. **Value Objects imutáveis** - init-only ou readonly
4. **Validações no construtor** - estado sempre válido
5. **Factory methods** - para criação complexa
6. **Private setters** - alteração apenas por métodos de domínio
