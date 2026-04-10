# Task Breakdown

## Decomposição por Camada

A decomposição segue a ordem obrigatória das camadas Clean Architecture.

---

## 1. Domain Layer (Primeira)

### Tarefas Típicas

| Tarefa | Skill | Artefatos Gerados | Estimativa |
|--------|-------|-------------------|------------|
| Criar Value Object | `dotnet-domain-entity` | `Domain/ValueObjects/{Name}.cs` | 1-2h |
| Criar Enum | `dotnet-domain-entity` | `Domain/Enums/{Name}.cs` | 0.5-1h |
| Criar Entity simples | `dotnet-domain-entity` | `Domain/Entities/{Name}.cs` | 2-3h |
| Criar Entity com regras | `dotnet-domain-entity` | `Domain/Entities/{Name}.cs` | 3-5h |
| Criar Aggregate Root | `dotnet-domain-entity` | `Domain/Aggregates/{Name}.cs` + Entities | 4-8h |
| Criar Domain Event | `dotnet-domain-entity` | `Domain/Events/{Name}Event.cs` | 0.5-1h |
| Criar Domain Exception | `dotnet-domain-entity` | `Domain/Exceptions/{Name}Exception.cs` | 0.5h |
| Criar Interface Repository | `dotnet-domain-entity` | `Domain/Interfaces/I{Name}Repository.cs` | 1-2h |

### Ordem de Dependência (Domain)

```
1. Value Objects (sem dependência)
   └── Money, Email, Address, etc.

2. Enums
   └── Status, Types, Categories

3. Entities Base (dependem de VOs e Enums)
   └── Entities simples sem relacionamentos

4. Entities com Relacionamentos
   └── Entities que referenciam outras

5. Aggregate Roots (dependem de Entities)
   └── Raízes com suas entidades filhas

6. Domain Events
   └── Eventos emitidos pelas entidades

7. Interfaces de Repository
   └── Contratos para cada Aggregate Root
```

### Exemplo de Decomposição Domain

```markdown
#### Domain Layer - Módulo Produtos

| ID | Tarefa | Tipo | Skill | Dependência | Est. |
|----|--------|------|-------|-------------|------|
| D1 | Criar VO `Money` | ValueObject | `dotnet-domain-entity` | - | 1h |
| D2 | Criar VO `Sku` | ValueObject | `dotnet-domain-entity` | - | 1h |
| D3 | Criar Enum `ProductStatus` | Enum | `dotnet-domain-entity` | - | 0.5h |
| D4 | Criar Entity `Category` | Entity | `dotnet-domain-entity` | - | 2h |
| D5 | Criar Entity `Product` | Entity | `dotnet-domain-entity` | D1,D2,D3,D4 | 3h |
| D6 | Criar Event `ProductCreatedEvent` | Event | `dotnet-domain-entity` | D5 | 0.5h |
| D7 | Criar Interface `IProductRepository` | Interface | `dotnet-domain-entity` | D5 | 1h |
| D8 | Criar Interface `ICategoryRepository` | Interface | `dotnet-domain-entity` | D4 | 0.5h |
```

---

## 2. Infrastructure Layer (Segunda)

### Tarefas Típicas

| Tarefa | Skill | Artefatos Gerados | Estimativa |
|--------|-------|-------------------|------------|
| Criar EF Configuration | - | `Infrastructure/Persistence/Configurations/{Name}Configuration.cs` | 1-2h |
| Criar Repository simples | `dotnet-infrastructure-repository` | `Infrastructure/Persistence/Repositories/{Name}Repository.cs` | 1-2h |
| Criar Repository com queries | `dotnet-infrastructure-repository` | `Infrastructure/Persistence/Repositories/{Name}Repository.cs` | 2-4h |
| Criar Migration | - | `Infrastructure/Persistence/Migrations/` | 0.5h |
| Criar Integração Externa | `dotnet-external-service` | `Infrastructure/ExternalServices/{Provider}/` | 4-8h |

### Ordem de Dependência (Infrastructure)

```
1. RepositoryBase (se não existir)
   └── Classe base para todos os repositórios

2. DbContext (adicionar DbSets)
   └── Registrar novas entidades

3. Entity Configurations
   └── Configurações EF Core por entidade

4. Repositories
   └── Implementações dos contratos de Domain

5. Migrations
   └── Após todas as configurações

6. External Services (se necessário)
   └── Integrações com APIs externas
```

### Exemplo de Decomposição Infrastructure

```markdown
#### Infrastructure Layer - Módulo Produtos

| ID | Tarefa | Tipo | Skill | Dependência | Est. |
|----|--------|------|-------|-------------|------|
| I1 | Criar `CategoryConfiguration` | EF Config | - | D4 | 1h |
| I2 | Criar `ProductConfiguration` | EF Config | - | D5 | 1.5h |
| I3 | Adicionar DbSets no Context | DbContext | - | I1,I2 | 0.5h |
| I4 | Criar `CategoryRepository` | Repository | `dotnet-infrastructure-repository` | D8,I1 | 1.5h |
| I5 | Criar `ProductRepository` | Repository | `dotnet-infrastructure-repository` | D7,I2 | 2.5h |
| I6 | Criar Migration | Migration | - | I1,I2,I3 | 0.5h |
```

---

## 3. Application Layer (Terceira)

### Tarefas Típicas

| Tarefa | Skill | Artefatos Gerados | Estimativa |
|--------|-------|-------------------|------------|
| Criar DTO | `dotnet-application-feature` | `Application/{Feature}/DTOs/{Name}Dto.cs` | 0.5-1h |
| Criar Command simples | `dotnet-application-feature` | `Command.cs` + `Handler.cs` + `Validator.cs` | 2-3h |
| Criar Command complexo | `dotnet-application-feature` | `Command.cs` + `Handler.cs` + `Validator.cs` | 3-5h |
| Criar Query GetById | `dotnet-application-feature` | `Query.cs` + `Handler.cs` | 1-2h |
| Criar Query List/Paged | `dotnet-application-feature` | `Query.cs` + `Handler.cs` | 2-3h |
| Criar Query com filtros | `dotnet-application-feature` | `Query.cs` + `Handler.cs` | 2-4h |
| Criar Mapping Profile | `dotnet-application-feature` | `Application/Mappings/{Name}Profile.cs` | 0.5-1h |

### Ordem de Dependência (Application)

```
1. DTOs
   └── Modelos de transferência de dados

2. Mapping Profiles
   └── Conversão Entity <-> DTO

3. Queries simples (GetById)
   └── Operações de leitura básicas

4. Queries de listagem
   └── Operações com paginação/filtros

5. Commands de criação
   └── Create{Entity}Command

6. Commands de atualização
   └── Update{Entity}Command

7. Commands de ação
   └── Approve, Cancel, etc.

8. Commands de deleção
   └── Delete{Entity}Command
```

### Exemplo de Decomposição Application

```markdown
#### Application Layer - Módulo Produtos

| ID | Tarefa | Tipo | Skill | Dependência | Est. |
|----|--------|------|-------|-------------|------|
| A1 | Criar `ProductDto` | DTO | `dotnet-application-feature` | D5 | 0.5h |
| A2 | Criar `ProductListItemDto` | DTO | `dotnet-application-feature` | D5 | 0.5h |
| A3 | Criar `CategoryDto` | DTO | `dotnet-application-feature` | D4 | 0.5h |
| A4 | Criar `ProductMappingProfile` | Mapping | `dotnet-application-feature` | A1,A2 | 0.5h |
| A5 | Criar `GetProductByIdQuery` | Query | `dotnet-application-feature` | A1,I5 | 1.5h |
| A6 | Criar `GetProductListQuery` | Query | `dotnet-application-feature` | A2,I5 | 2.5h |
| A7 | Criar `CreateProductCommand` | Command | `dotnet-application-feature` | I5 | 3h |
| A8 | Criar `UpdateProductCommand` | Command | `dotnet-application-feature` | I5,A5 | 2.5h |
| A9 | Criar `DeleteProductCommand` | Command | `dotnet-application-feature` | I5 | 1.5h |
| A10 | Criar `ActivateProductCommand` | Command | `dotnet-application-feature` | I5 | 1.5h |
| A11 | Criar `DeactivateProductCommand` | Command | `dotnet-application-feature` | I5 | 1.5h |
```

---

## 4. Presentation Layer (Última)

### Tarefas Típicas

| Tarefa | Skill | Artefatos Gerados | Estimativa |
|--------|-------|-------------------|------------|
| Criar Controller CRUD | `dotnet-endpoint-generator` | `Presentation/Controllers/{Name}Controller.cs` | 2-4h |
| Criar Endpoint Minimal API | `dotnet-endpoint-generator` | `Presentation/Endpoints/{Name}Endpoints.cs` | 2-3h |
| Criar Request Model | `dotnet-endpoint-generator` | `Presentation/Models/Requests/{Action}Request.cs` | 0.5h |
| Criar Request Validator | `dotnet-endpoint-generator` | `Presentation/Validators/{Name}Validator.cs` | 1-2h |
| Criar Response Model | `dotnet-endpoint-generator` | `Presentation/Models/Responses/{Name}Response.cs` | 0.5h |

### Ordem de Dependência (Presentation)

```
1. Request Models
   └── Modelos de entrada da API

2. Response Models (se diferentes dos DTOs)
   └── Modelos de saída customizados

3. Request Validators
   └── Validações de entrada

4. Controllers/Endpoints
   └── Exposição HTTP dos Commands/Queries
```

### Exemplo de Decomposição Presentation

```markdown
#### Presentation Layer - Módulo Produtos

| ID | Tarefa | Tipo | Skill | Dependência | Est. |
|----|--------|------|-------|-------------|------|
| P1 | Criar `CreateProductRequest` | Request | `dotnet-endpoint-generator` | A7 | 0.5h |
| P2 | Criar `UpdateProductRequest` | Request | `dotnet-endpoint-generator` | A8 | 0.5h |
| P3 | Criar `CreateProductRequestValidator` | Validator | `dotnet-endpoint-generator` | P1 | 1h |
| P4 | Criar `UpdateProductRequestValidator` | Validator | `dotnet-endpoint-generator` | P2 | 1h |
| P5 | Criar `ProductsController` | Controller | `dotnet-endpoint-generator` | A5-A11,P1-P4 | 3h |
```

---

## 5. Testes

### Tarefas Típicas

| Tarefa | Estimativa Base | Cálculo |
|--------|-----------------|---------|
| Testes Unitários Domain | 1-2h por entidade | ~50% do tempo da entidade |
| Testes Unitários Application | 1-2h por handler | ~50% do tempo do handler |
| Testes Integração Repository | 1-2h por repositório | ~50% do tempo do repositório |
| Testes Integração API | 2-4h por controller | ~30% do tempo do controller |

### Exemplo de Decomposição Testes

```markdown
#### Testes - Módulo Produtos

| ID | Tarefa | Tipo | Dependência | Est. |
|----|--------|------|-------------|------|
| T1 | Testes unitários `Product` | Unit | D5 | 1.5h |
| T2 | Testes unitários `Money` | Unit | D1 | 0.5h |
| T3 | Testes `CreateProductCommandHandler` | Unit | A7 | 1.5h |
| T4 | Testes `UpdateProductCommandHandler` | Unit | A8 | 1h |
| T5 | Testes `GetProductByIdQueryHandler` | Unit | A5 | 1h |
| T6 | Testes integração `ProductRepository` | Integration | I5 | 2h |
| T7 | Testes integração `ProductsController` | Integration | P5 | 2.5h |
```

---

## Matriz de Estimativas

### Por Complexidade

| Complexidade | Domain | Infra | Application | Presentation | Testes | Total |
|--------------|--------|-------|-------------|--------------|--------|-------|
| **Simples** (CRUD básico) | 4h | 3h | 8h | 4h | 6h | **25h** (~3d) |
| **Média** (validações, queries) | 8h | 5h | 16h | 6h | 12h | **47h** (~6d) |
| **Complexa** (regras, integrações) | 16h | 10h | 24h | 8h | 20h | **78h** (~10d) |

### Fatores de Ajuste

| Fator | Multiplicador |
|-------|---------------|
| Primeira feature do projeto | 1.5x (setup inicial) |
| Integração externa | +4-8h por integração |
| Regras de negócio complexas | +50% no Domain |
| Muitos relacionamentos | +30% em todas as camadas |
| Requisitos de performance | +20% em Infra e Testes |
