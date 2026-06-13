---
name: dotnet-domain-entity
description: Gera entidades de domínio seguindo DDD e Clean Architecture. Use quando o usuário mencionar "criar entidade", "nova entidade", "entity", "aggregate", "aggregate root", "value object", "domain model", "modelo de domínio", "classe de domínio", "tabela", "criar tabela", "nova tabela", "definir entidade", "modelar entidade". Também dispara quando pedir para criar modelos que representam conceitos de negócio, objetos persistidos ou agregados. NÃO use para DTOs (use application-feature), endpoints (use endpoint-generator) ou configurações de banco (use infrastructure).
---

# .NET Domain Entity Generator

Gera entidades de domínio, Value Objects, Aggregates e interfaces de repositório seguindo DDD e Clean Architecture.

## Instruções

### ANTES de gerar código, consulte as referências:

1. **Leia `references/entity-template.md`** para estrutura de entidades
2. **Leia `references/value-objects.md`** para Value Objects
3. **Leia `references/repository-interface.md`** para interfaces de repositório

### Passo 1: Identificar Tipo de Objeto

| Tipo | Quando Usar | Características |
|------|-------------|-----------------|
| **Entity** | Tem identidade única | `Id`, ciclo de vida próprio |
| **Aggregate Root** | Entidade raiz de um agregado | Controla consistência do agregado |
| **Value Object** | Definido por atributos, não identidade | Imutável, comparado por valor |
| **Enum de Domínio** | Estados, tipos, categorias | Strongly-typed, com comportamento |

### Passo 2: Coletar Informações

Para **Entity/Aggregate**:
- Nome da entidade
- Propriedades e tipos
- Relacionamentos (1:1, 1:N, N:N)
- Regras de negócio/invariantes
- Eventos de domínio (se aplicável)

Para **Value Object**:
- Nome e propósito
- Propriedades que compõem o valor
- Validações no construtor
- Operações/comportamentos

### Passo 3: Gerar Artefatos

```
Domain/
├── Entities/
│   └── {Entity}.cs
├── Aggregates/
│   └── {AggregateRoot}.cs
├── ValueObjects/
│   └── {ValueObject}.cs
├── Enums/
│   └── {Enum}.cs
├── Events/
│   └── {Entity}{Action}Event.cs
├── Exceptions/
│   └── {Entity}Exception.cs
└── Interfaces/
    └── I{Entity}Repository.cs
```

### Passo 4: Validar Checklist

- [ ] Entidade tem construtor privado/protected
- [ ] Factory method `Create()` para instanciação
- [ ] Setters são `private` ou `init`
- [ ] Métodos de domínio para alteração de estado
- [ ] Validações no construtor/factory
- [ ] Value Objects são `record` ou classe imutável
- [ ] Interface de repositório em Domain (não Infrastructure)
- [ ] Sem dependências de infraestrutura (EF, Dapper, etc.)

## Padrões Obrigatórios

### Entidade com Comportamento (Rich Domain Model)

```csharp
// ✅ CORRETO - Entidade rica
public class Order : Entity<Guid>
{
    public OrderStatus Status { get; private set; }
    
    public void Approve(Guid approvedBy)
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOrderStateException("Apenas pedidos pendentes podem ser aprovados");
        
        Status = OrderStatus.Approved;
        AddDomainEvent(new OrderApprovedEvent(Id, approvedBy));
    }
}

// ❌ INCORRETO - Entidade anêmica
public class Order : Entity<Guid>
{
    public OrderStatus Status { get; set; } // Setter público!
}
```

### Factory Method

```csharp
// ✅ CORRETO - Factory method com validação
public static Product Create(string name, Money price)
{
    if (string.IsNullOrWhiteSpace(name))
        throw new ArgumentException("Nome é obrigatório", nameof(name));
    
    return new Product(name, price);
}

// ❌ INCORRETO - Construtor público
public Product(string name, Money price) // Construtor público!
{
    Name = name;
    Price = price;
}
```

### Nomenclatura

| Artefato | Padrão | Exemplo |
|----------|--------|---------|
| Entity | `{Nome}` | `Product`, `Order` |
| Aggregate Root | `{Nome}` | `Order` (com `OrderItem` interno) |
| Value Object | `{Nome}` | `Money`, `Address`, `Email` |
| Domain Event | `{Entity}{Action}Event` | `OrderCreatedEvent` |
| Repository Interface | `I{Entity}Repository` | `IProductRepository` |
| Domain Exception | `{Context}Exception` | `InvalidOrderStateException` |

## Fluxo de Decisão

```
Novo conceito de domínio
         │
         ▼
    Tem identidade?
    ┌────┴────┐
   Sim       Não
    │         │
    ▼         ▼
 ENTITY    VALUE OBJECT
    │
    ▼
Controla outros
  objetos?
    │
   Sim
    │
    ▼
AGGREGATE ROOT
```

## Relacionamentos

### One-to-Many (Aggregate)

```csharp
public class Order : AggregateRoot<Guid>
{
    private readonly List<OrderItem> _items = new();
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();
    
    public void AddItem(Product product, int quantity)
    {
        var item = new OrderItem(product.Id, product.Price, quantity);
        _items.Add(item);
    }
}
```

### Many-to-Many (via Entity intermediária)

```csharp
// Não usar coleção direta - criar entidade de relacionamento
public class ProductCategory : Entity<Guid>
{
    public Guid ProductId { get; private set; }
    public Guid CategoryId { get; private set; }
}
```

## Troubleshooting

### Erro: Dependência circular entre entidades
**Causa**: Entidades referenciando umas às outras diretamente
**Solução**: Usar apenas IDs para referências entre agregados diferentes

### Erro: EF não mapeia propriedade
**Causa**: Propriedade sem setter acessível
**Solução**: Usar `private set` (não `readonly`) para EF Core

### Erro: Value Object não persiste
**Causa**: Falta configuração `OwnsOne` no EF Core
**Solução**: Configurar em `Infrastructure/Persistence/Configurations`
