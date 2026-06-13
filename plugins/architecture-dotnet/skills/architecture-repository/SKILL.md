---
name: dotnet-infrastructure-repository
description: Gera repositórios na camada Infrastructure seguindo Clean Architecture. Use quando o usuário mencionar "criar repositório", "novo repositório", "repository", "implementar repositório", "repositório de", "persistência", "acesso a dados", "data access", "criar repository", "implementação do repositório". Também dispara quando pedir para criar implementações de IRepository, acesso ao banco de dados ou operações CRUD de persistência. NÃO use para interfaces de repositório (use dotnet-domain-entity) ou configurações de entidade EF Core (use dotnet-ef-configuration).
---

# .NET Infrastructure Repository Generator

Gera implementações de repositórios na camada Infrastructure usando EF Core, herdando de RepositoryBase.

## Instruções

### ANTES de gerar código, consulte as referências:

1. **Leia `references/repository-base.md`** para a classe base e DbContext
2. **Leia `references/repository-implementation.md`** para implementações específicas
3. **Leia `references/unit-of-work.md`** para padrão Unit of Work

### Passo 1: Verificar Pré-requisitos

Antes de criar o repositório, confirme que existe:
- [ ] Interface `I{Entity}Repository` em `Domain/Interfaces/`
- [ ] Entidade `{Entity}` em `Domain/Entities/` ou `Domain/Aggregates/`
- [ ] `ApplicationDbContext` configurado
- [ ] `RepositoryBase<TEntity, TId>` implementado

### Passo 2: Identificar Métodos Necessários

A interface define os métodos. O repositório implementa:

| Método Interface | Implementação |
|------------------|---------------|
| Herdados de `IRepository<T,TId>` | Já implementados em `RepositoryBase` |
| Queries específicas | Implementar com LINQ/EF Core |
| Queries paginadas | Implementar com Skip/Take |
| Queries com Include | Implementar com Include/ThenInclude |

### Passo 3: Gerar Artefatos

```
Infrastructure/
└── Persistence/
    └── Repositories/
        ├── RepositoryBase.cs        # Classe base (se não existir)
        └── {Entity}Repository.cs    # Implementação específica
```

### Passo 4: Validar Checklist

- [ ] Herda de `RepositoryBase<TEntity, TId>`
- [ ] Implementa `I{Entity}Repository`
- [ ] Construtor apenas chama `base(context)`
- [ ] Métodos usam `DbSet` ou `Context` protegidos da base
- [ ] `CancellationToken` propagado em todos os métodos async
- [ ] Queries usam `AsNoTracking()` quando apropriado
- [ ] Registrado no DI em `Infrastructure/DependencyInjection.cs`

## Padrões Obrigatórios

### Herança da Base

```csharp
// ✅ CORRETO - Herdar de RepositoryBase
public class ProductRepository : RepositoryBase<Product, Guid>, IProductRepository
{
    public ProductRepository(ApplicationDbContext context) : base(context) { }
}

// ❌ INCORRETO - Injetar DbContext diretamente
public class ProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context; // NÃO FAZER
}
```

### Usar Membros Protegidos da Base

```csharp
public class ProductRepository : RepositoryBase<Product, Guid>, IProductRepository
{
    public async Task<Product?> GetBySkuAsync(string sku, CancellationToken ct)
    {
        // ✅ Usar DbSet da base
        return await DbSet.FirstOrDefaultAsync(p => p.Sku == sku, ct);
    }
    
    public async Task<IEnumerable<Product>> GetWithOrdersAsync(CancellationToken ct)
    {
        // ✅ Usar Context da base para queries complexas
        return await Context.Products
            .Include(p => p.OrderItems)
            .ToListAsync(ct);
    }
}
```

### Nomenclatura

| Artefato | Padrão | Exemplo |
|----------|--------|---------|
| Repository | `{Entity}Repository` | `ProductRepository` |
| Localização | `Infrastructure/Persistence/Repositories/` | |
| Registro DI | `services.AddScoped<I{Entity}Repository, {Entity}Repository>()` | |

## Fluxo de Decisão

```
Novo repositório
       │
       ▼
Interface existe em Domain?
       │
      Não ──► Criar interface primeiro (use dotnet-domain-entity)
       │
      Sim
       │
       ▼
RepositoryBase existe?
       │
      Não ──► Criar RepositoryBase (ver references/repository-base.md)
       │
      Sim
       │
       ▼
Criar {Entity}Repository
herdando de RepositoryBase
```

## Troubleshooting

### Erro: DbSet não encontrado
**Causa**: Entidade não configurada no DbContext
**Solução**: Adicionar `DbSet<Entity>` no ApplicationDbContext

### Erro: Tipo não pode ser usado como parâmetro de tipo
**Causa**: Entidade não herda de `Entity<TId>` ou `AggregateRoot<TId>`
**Solução**: Verificar herança da entidade em Domain

### Erro: Dependência circular
**Causa**: Repositório referenciando outro repositório
**Solução**: Usar apenas o Context para queries entre agregados
