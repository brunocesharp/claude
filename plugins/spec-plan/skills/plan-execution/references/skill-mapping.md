# Skill Mapping

## Mapeamento Completo: Tarefa → Skill

Este documento mapeia cada tipo de tarefa para a skill apropriada do ecossistema fullstack (.NET Clean Architecture + Angular).

---

## Skills Disponíveis

### Backend (.NET)

| Skill | Camada | Propósito |
|-------|--------|-----------|
| `architecture-entities` | Domain | Entidades, Value Objects, Aggregates, Interfaces |
| `architecture-repository` | Infrastructure | Repositórios, DbContext, Unit of Work |
| `architecture-feature` | Application | Commands, Queries, Handlers, DTOs |
| `architecture-controller` | Presentation | Controllers, Endpoints, Validators |
| `architecture-external-service` | Infrastructure | Integrações com APIs externas |
| `deploy-dotnet-homolog` | DevOps | Deploy em homologação |
| `deploy-dotnet-prod` | DevOps | Deploy em produção |

### Frontend (Angular)

> Tarefas Angular não possuem skill dedicada — seguem os padrões definidos em `references/angular-patterns.md`.

| Tipo de Tarefa | Camada Angular | Quando Criar |
|----------------|----------------|--------------|
| Interface / Model TypeScript | Core / Shared | Sempre — uma por DTO do backend |
| Service com HttpClient | Core / Shared | Sempre — um por recurso da API |
| State Service (BehaviorSubject) | Core / Shared | Estado compartilhado entre 2-3 componentes |
| NgRx (Store + Effects) | Core / Shared | Estado global complexo, 4+ features |
| HTTP Interceptor | Core / Shared | Auth JWT, loading global, tratamento de erros |
| Route Guard (CanActivate) | Core / Shared | Rotas protegidas por autenticação/perfil |
| Smart Component | Feature Module | Containers que injetam services |
| Presentational Component | Feature Module | Componentes puros com @Input/@Output + OnPush |
| Reactive Form | Feature Module | Formulários de criação e edição |
| Feature Routing (lazy) | Feature Module | Sempre — um por Feature Module |
| Pipe customizado | Shared | Transformações de exibição reutilizáveis |
| Diretiva customizada | Shared | Comportamentos de DOM reutilizáveis |

---

## Mapeamento por Tipo de Tarefa

### Domain Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar Entity | `architecture-entities` | `references/entity-template.md` |
| Criar Aggregate Root | `architecture-entities` | `references/entity-template.md` |
| Criar Value Object | `architecture-entities` | `references/value-objects.md` |
| Criar Enum | `architecture-entities` | `references/entity-template.md` |
| Criar Domain Event | `architecture-entities` | `references/entity-template.md` |
| Criar Domain Exception | `architecture-entities` | `references/entity-template.md` |
| Criar Interface Repository | `architecture-entities` | `references/repository-interface.md` |

### Infrastructure Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar RepositoryBase | `architecture-repository` | `references/repository-base.md` |
| Criar Repository | `architecture-repository` | `references/repository-implementation.md` |
| Configurar DbContext | `architecture-repository` | `references/repository-base.md` |
| Implementar Unit of Work | `architecture-repository` | `references/unit-of-work.md` |
| Criar Entity Configuration | Manual / EF Core | - |
| Criar Migration | Manual / `dotnet ef` | - |
| Criar Integração Externa | `architecture-external-service` | `references/adapter-gateway.md` |
| Configurar HttpClient (.NET) | `architecture-external-service` | `references/http-client-base.md` |
| Configurar Polly | `architecture-external-service` | `references/resilience.md` |
| Configurar OAuth2 | `architecture-external-service` | `references/authentication.md` |

### Application Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar DTO | `architecture-feature` | `references/query-template.md` |
| Criar Command | `architecture-feature` | `references/command-template.md` |
| Criar Command Handler | `architecture-feature` | `references/command-template.md` |
| Criar Command Validator | `architecture-feature` | `references/command-template.md` |
| Criar Query | `architecture-feature` | `references/query-template.md` |
| Criar Query Handler | `architecture-feature` | `references/query-template.md` |
| Criar Behavior | `architecture-feature` | `references/behaviors.md` |
| Criar Mapping Profile | `architecture-feature` | - |

### Presentation Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar Controller | `architecture-controller` | `references/examples.md` |
| Criar Minimal API Endpoint | `architecture-controller` | `references/examples.md` |
| Criar Request Model | `architecture-controller` | `references/structure.md` |
| Criar Request Validator | `architecture-controller` | `references/patterns.md` |
| Criar Response Model | `architecture-controller` | `references/structure.md` |
| Configurar OpenAPI | `architecture-controller` | `references/patterns.md` |

### Frontend — Core / Shared

| Tarefa | Referência |
|--------|------------|
| Criar Interface/Model TypeScript | `references/angular-patterns.md#models` |
| Criar Service com HttpClient | `references/angular-patterns.md#services` |
| Criar State Service (BehaviorSubject) | `references/angular-patterns.md#state` |
| Criar NgRx Actions | `references/angular-patterns.md#ngrx` |
| Criar NgRx Reducer | `references/angular-patterns.md#ngrx` |
| Criar NgRx Selectors | `references/angular-patterns.md#ngrx` |
| Criar NgRx Effects | `references/angular-patterns.md#ngrx` |
| Criar HTTP Interceptor | `references/angular-patterns.md#interceptors` |
| Criar Route Guard | `references/angular-patterns.md#guards` |

### Frontend — Feature Module

| Tarefa | Referência |
|--------|------------|
| Criar Feature Module + Routing lazy | `references/angular-patterns.md#routing` |
| Criar Smart Component (Container) | `references/angular-patterns.md#components` |
| Criar Presentational Component (OnPush) | `references/angular-patterns.md#components` |
| Criar Reactive Form | `references/angular-patterns.md#forms` |
| Criar Pipe customizado | `references/angular-patterns.md#pipes` |
| Criar Diretiva customizada | `references/angular-patterns.md#directives` |

### DevOps

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Deploy Homologação | `deploy-dotnet-homolog` | `references/pipeline-steps.md` |
| Health Check Homolog | `deploy-dotnet-homolog` | `references/health-check.md` |
| Deploy Produção | `deploy-dotnet-prod` | `references/pipeline-steps.md` |
| Rollback Produção | `deploy-dotnet-prod` | `references/rollback.md` |

---

## Fluxo de Decisão: Qual Skill / Camada Usar?

```
┌──────────────────────────────────────────────────────────────┐
│                       NOVA TAREFA                            │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │  É backend ou    │
                   │   frontend?      │
                   └──────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
         BACKEND                       FRONTEND
              │                             │
              ▼                             ▼
   ┌──────────────────┐        ┌────────────────────┐
   │  Em qual camada? │        │  É Core/Shared ou  │
   └──────────────────┘        │  Feature Module?   │
              │                └────────────────────┘
    ┌────┬────┼────┬────┐               │
    ▼    ▼    ▼    ▼    ▼      ┌────────┴────────┐
  Dom  Inf  App  Pre  DevOps   ▼                 ▼
    │    │    │    │    │   CORE/SHARED    FEATURE MODULE
    ▼    │    ▼    ▼    ▼       │                 │
dotnet   │  dotnet  dotnet  dotnet   ┌────────────┐    ┌─────────────────┐
-domain  │  -appl  -endpt  -deploy  │ Model TS?  │    │ Component?      │
-entity  │  -feat  -gen    -hom/*   │ Service?   │    │ Form?           │
         │                         │ State?     │    │ Routing?        │
         ▼                         │ Guard?     │    └─────────────────┘
   É API externa?                  │ Interceptor│     → angular-patterns.md
         │                         └────────────┘       #components / #forms
    ┌────┴────┐                    → angular-patterns.md
    ▼         ▼                      #models / #services
   Sim       Não                     #state / #guards
    │         │                      #interceptors
    ▼         ▼
dotnet-   dotnet-
external  infrastr
-service  -reposit
```

---

## Regras de Uso das Skills

### Sempre Consultar Referências

Ao usar qualquer skill backend, **SEMPRE** ler as referências antes de gerar código:

```markdown
### Ao usar `architecture-entities`:
1. Ler `references/entity-template.md`
2. Ler `references/value-objects.md` (se criar VO)
3. Ler `references/repository-interface.md` (se criar interface)

### Ao usar `architecture-repository`:
1. Ler `references/repository-base.md`
2. Ler `references/repository-implementation.md`
3. Ler `references/unit-of-work.md`

### Ao usar `architecture-feature`:
1. Ler `references/command-template.md` (se Command)
2. Ler `references/query-template.md` (se Query)
3. Ler `references/behaviors.md`

### Ao usar `architecture-controller`:
1. Ler `references/patterns.md`
2. Ler `references/structure.md`
3. Ler `references/examples.md`

### Ao usar `architecture-external-service`:
1. Ler `references/http-client-base.md`
2. Ler `references/adapter-gateway.md`
3. Ler `references/resilience.md`
4. Ler `references/authentication.md`

### Ao usar `deploy-dotnet-homolog`:
1. Ler `references/pipeline-steps.md`
2. Ler `references/health-check.md`
3. Ler `references/troubleshooting.md`

### Ao usar `deploy-dotnet-prod`:
1. Ler `references/pre-deploy-checklist.md`
2. Ler `references/pipeline-steps.md`
3. Ler `references/rollback.md`

### Para qualquer tarefa Angular (Core/Shared ou Feature Module):
1. Ler `references/angular-patterns.md` — seção correspondente ao tipo de tarefa
```

---

## Exemplos de Mapeamento

### Exemplo 1: Feature CRUD Completa (Fullstack)

```markdown
## Feature: Gestão de Clientes

### Backend
| Tarefa | Skill |
|--------|-------|
| Criar VO `Email` | `architecture-entities` |
| Criar VO `PhoneNumber` | `architecture-entities` |
| Criar Entity `Customer` | `architecture-entities` |
| Criar Interface `ICustomerRepository` | `architecture-entities` |
| Criar `CustomerRepository` | `architecture-repository` |
| Criar `CustomerDto` | `architecture-feature` |
| Criar `CreateCustomerCommand` | `architecture-feature` |
| Criar `UpdateCustomerCommand` | `architecture-feature` |
| Criar `GetCustomerByIdQuery` | `architecture-feature` |
| Criar `GetCustomerListQuery` | `architecture-feature` |
| Criar `CustomersController` | `architecture-controller` |
| Deploy Homologação | `deploy-dotnet-homolog` |

### Frontend
| Tarefa | Referência |
|--------|------------|
| Criar model `Customer` (espelha `CustomerDto`) | `angular-patterns.md#models` |
| Criar `CustomerService` (HttpClient) | `angular-patterns.md#services` |
| Criar `CustomerStateService` (BehaviorSubject) | `angular-patterns.md#state` |
| Criar `customers.module.ts` + rota lazy `/customers` | `angular-patterns.md#routing` |
| Criar `CustomerListComponent` (Smart) | `angular-patterns.md#components` |
| Criar `CustomerCardComponent` (Presentational + OnPush) | `angular-patterns.md#components` |
| Criar `CustomerFormComponent` (Reactive Form) | `angular-patterns.md#forms` |
```

### Exemplo 2: Feature com Integração Externa (Fullstack)

```markdown
## Feature: Processamento de Pagamentos

### Backend
| Tarefa | Skill |
|--------|-------|
| Criar VO `Money` | `architecture-entities` |
| Criar Enum `PaymentStatus` | `architecture-entities` |
| Criar Aggregate `Payment` | `architecture-entities` |
| Criar Event `PaymentProcessedEvent` | `architecture-entities` |
| Criar Interface `IPaymentRepository` | `architecture-entities` |
| Criar `PaymentRepository` | `architecture-repository` |
| Criar `IStripeGateway` | `architecture-external-service` |
| Criar `StripeAdapter` | `architecture-external-service` |
| Criar `ProcessPaymentCommand` | `architecture-feature` |
| Criar `GetPaymentByIdQuery` | `architecture-feature` |
| Criar `PaymentsController` | `architecture-controller` |
| Deploy Homologação | `deploy-dotnet-homolog` |
| Validar em Homolog | Manual |
| Deploy Produção | `deploy-dotnet-prod` |

### Frontend
| Tarefa | Referência |
|--------|------------|
| Criar model `Payment` (espelha DTO) | `angular-patterns.md#models` |
| Criar `PaymentService` (HttpClient) | `angular-patterns.md#services` |
| Criar `AuthInterceptor` (JWT Bearer) | `angular-patterns.md#interceptors` |
| Criar `payments.module.ts` + rota lazy `/payments` | `angular-patterns.md#routing` |
| Criar `PaymentCheckoutComponent` (Smart + Form) | `angular-patterns.md#forms` |
| Criar `PaymentStatusComponent` (Presentational) | `angular-patterns.md#components` |
```

### Exemplo 3: Feature Somente Leitura — Dashboard (Fullstack)

```markdown
## Feature: Dashboard de Vendas

### Backend
| Tarefa | Skill |
|--------|-------|
| Criar `SalesSummaryDto` | `architecture-feature` |
| Criar `TopProductDto` | `architecture-feature` |
| Criar `GetSalesSummaryQuery` | `architecture-feature` |
| Criar `GetTopProductsQuery` | `architecture-feature` |
| Criar `GetSalesByPeriodQuery` | `architecture-feature` |
| Criar `DashboardController` | `architecture-controller` |

### Frontend
| Tarefa | Referência |
|--------|------------|
| Criar models `SalesSummary`, `TopProduct` | `angular-patterns.md#models` |
| Criar `DashboardService` (HttpClient — somente GET) | `angular-patterns.md#services` |
| Criar `dashboard.module.ts` + rota lazy `/dashboard` | `angular-patterns.md#routing` |
| Criar `DashboardComponent` (Smart — carrega dados no init) | `angular-patterns.md#components` |
| Criar `SalesChartComponent` (Presentational + OnPush) | `angular-patterns.md#components` |
| Criar `TopProductsTableComponent` (Presentational + OnPush) | `angular-patterns.md#components` |
```

---

## Combinação de Skills por Entrega

### Entrega Mínima — Backend + Frontend básico (MVP)

```
Backend:
architecture-entities → architecture-repository →
architecture-feature → architecture-controller

Frontend:
Model TS → Service HttpClient → State Service →
Feature Module (lazy) → Smart Component → Presentational Component

Deploy:
→ deploy-dotnet-homolog
```

### Entrega com Integração Externa

```
Backend:
architecture-entities → architecture-repository →
architecture-external-service → architecture-feature →
architecture-controller

Frontend:
Model TS → Service HttpClient → HTTP Interceptor →
Feature Module (lazy) → Smart Component → Form Component

Deploy:
→ deploy-dotnet-homolog
```

### Entrega com Estado Global (NgRx)

```
Backend:
[skills normais da feature]

Frontend:
Model TS → Service HttpClient →
NgRx (Actions → Reducer → Selectors → Effects) →
Feature Module (lazy) → Smart Component (usa Store) →
Presentational Component

Deploy:
→ deploy-dotnet-homolog
```

### Entrega de Produção

```
[Todas as skills do backend] +
[Todas as tarefas Angular da feature] →
deploy-dotnet-homolog → [Validação manual + E2E] →
deploy-dotnet-prod
```