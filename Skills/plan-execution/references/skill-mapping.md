# Skill Mapping

## Mapeamento Completo: Tarefa → Skill

Este documento mapeia cada tipo de tarefa para a skill apropriada do ecossistema .NET Clean Architecture.

---

## Skills Disponíveis

| Skill | Camada | Propósito |
|-------|--------|-----------|
| `dotnet-domain-entity` | Domain | Entidades, Value Objects, Aggregates, Interfaces |
| `dotnet-infrastructure-repository` | Infrastructure | Repositórios, DbContext, Unit of Work |
| `dotnet-application-feature` | Application | Commands, Queries, Handlers, DTOs |
| `dotnet-endpoint-generator` | Presentation | Controllers, Endpoints, Validators |
| `dotnet-external-service` | Infrastructure | Integrações com APIs externas |
| `dotnet-deploy-homolog` | DevOps | Deploy em homologação |
| `dotnet-deploy-prod` | DevOps | Deploy em produção |

---

## Mapeamento por Tipo de Tarefa

### Domain Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar Entity | `dotnet-domain-entity` | `references/entity-template.md` |
| Criar Aggregate Root | `dotnet-domain-entity` | `references/entity-template.md` |
| Criar Value Object | `dotnet-domain-entity` | `references/value-objects.md` |
| Criar Enum | `dotnet-domain-entity` | `references/entity-template.md` |
| Criar Domain Event | `dotnet-domain-entity` | `references/entity-template.md` |
| Criar Domain Exception | `dotnet-domain-entity` | `references/entity-template.md` |
| Criar Interface Repository | `dotnet-domain-entity` | `references/repository-interface.md` |

### Infrastructure Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar RepositoryBase | `dotnet-infrastructure-repository` | `references/repository-base.md` |
| Criar Repository | `dotnet-infrastructure-repository` | `references/repository-implementation.md` |
| Configurar DbContext | `dotnet-infrastructure-repository` | `references/repository-base.md` |
| Implementar Unit of Work | `dotnet-infrastructure-repository` | `references/unit-of-work.md` |
| Criar Entity Configuration | Manual / EF Core | - |
| Criar Migration | Manual / `dotnet ef` | - |
| Criar Integração Externa | `dotnet-external-service` | `references/adapter-gateway.md` |
| Configurar HttpClient | `dotnet-external-service` | `references/http-client-base.md` |
| Configurar Polly | `dotnet-external-service` | `references/resilience.md` |
| Configurar OAuth2 | `dotnet-external-service` | `references/authentication.md` |

### Application Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar DTO | `dotnet-application-feature` | `references/query-template.md` |
| Criar Command | `dotnet-application-feature` | `references/command-template.md` |
| Criar Command Handler | `dotnet-application-feature` | `references/command-template.md` |
| Criar Command Validator | `dotnet-application-feature` | `references/command-template.md` |
| Criar Query | `dotnet-application-feature` | `references/query-template.md` |
| Criar Query Handler | `dotnet-application-feature` | `references/query-template.md` |
| Criar Behavior | `dotnet-application-feature` | `references/behaviors.md` |
| Criar Mapping Profile | `dotnet-application-feature` | - |

### Presentation Layer

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Criar Controller | `dotnet-endpoint-generator` | `references/examples.md` |
| Criar Minimal API Endpoint | `dotnet-endpoint-generator` | `references/examples.md` |
| Criar Request Model | `dotnet-endpoint-generator` | `references/structure.md` |
| Criar Request Validator | `dotnet-endpoint-generator` | `references/patterns.md` |
| Criar Response Model | `dotnet-endpoint-generator` | `references/structure.md` |
| Configurar OpenAPI | `dotnet-endpoint-generator` | `references/patterns.md` |

### DevOps

| Tarefa | Skill | Referência na Skill |
|--------|-------|---------------------|
| Deploy Homologação | `dotnet-deploy-homolog` | `references/pipeline-steps.md` |
| Health Check Homolog | `dotnet-deploy-homolog` | `references/health-check.md` |
| Deploy Produção | `dotnet-deploy-prod` | `references/pipeline-steps.md` |
| Rollback Produção | `dotnet-deploy-prod` | `references/rollback.md` |

---

## Fluxo de Decisão: Qual Skill Usar?

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOVA TAREFA                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  É sobre qual   │
                    │    camada?      │
                    └─────────────────┘
                              │
        ┌─────────┬───────────┼───────────┬─────────┐
        ▼         ▼           ▼           ▼         ▼
    ┌───────┐ ┌───────┐ ┌───────────┐ ┌───────┐ ┌───────┐
    │Domain │ │Infra  │ │Application│ │Present│ │DevOps │
    └───────┘ └───────┘ └───────────┘ └───────┘ └───────┘
        │         │           │           │         │
        ▼         ▼           ▼           ▼         ▼
┌─────────────┐   │     ┌───────────┐     │    ┌─────────┐
│dotnet-domain│   │     │dotnet-    │     │    │dotnet-  │
│-entity      │   │     │application│     │    │deploy-* │
└─────────────┘   │     │-feature   │     │    └─────────┘
                  │     └───────────┘     │
                  ▼                       ▼
          ┌─────────────┐         ┌─────────────┐
          │ É API       │         │dotnet-      │
          │ externa?    │         │endpoint-    │
          └─────────────┘         │generator    │
                │                 └─────────────┘
        ┌───────┴───────┐
        ▼               ▼
    ┌───────┐       ┌───────┐
    │  Sim  │       │  Não  │
    └───────┘       └───────┘
        │               │
        ▼               ▼
┌─────────────┐  ┌─────────────┐
│dotnet-      │  │dotnet-infra-│
│external-    │  │structure-   │
│service      │  │repository   │
└─────────────┘  └─────────────┘
```

---

## Exemplos de Mapeamento

### Exemplo 1: Feature CRUD Completa

```markdown
## Feature: Gestão de Clientes

### Tarefas e Skills

| Tarefa | Skill |
|--------|-------|
| Criar VO `Email` | `dotnet-domain-entity` |
| Criar VO `PhoneNumber` | `dotnet-domain-entity` |
| Criar Entity `Customer` | `dotnet-domain-entity` |
| Criar Interface `ICustomerRepository` | `dotnet-domain-entity` |
| Criar `CustomerRepository` | `dotnet-infrastructure-repository` |
| Criar `CustomerDto` | `dotnet-application-feature` |
| Criar `CreateCustomerCommand` | `dotnet-application-feature` |
| Criar `UpdateCustomerCommand` | `dotnet-application-feature` |
| Criar `GetCustomerByIdQuery` | `dotnet-application-feature` |
| Criar `GetCustomerListQuery` | `dotnet-application-feature` |
| Criar `CustomersController` | `dotnet-endpoint-generator` |
| Deploy Homologação | `dotnet-deploy-homolog` |
```

### Exemplo 2: Feature com Integração Externa

```markdown
## Feature: Processamento de Pagamentos

### Tarefas e Skills

| Tarefa | Skill |
|--------|-------|
| Criar VO `Money` | `dotnet-domain-entity` |
| Criar Enum `PaymentStatus` | `dotnet-domain-entity` |
| Criar Aggregate `Payment` | `dotnet-domain-entity` |
| Criar Event `PaymentProcessedEvent` | `dotnet-domain-entity` |
| Criar Interface `IPaymentRepository` | `dotnet-domain-entity` |
| Criar `PaymentRepository` | `dotnet-infrastructure-repository` |
| Criar `IStripeGateway` | `dotnet-external-service` |
| Criar `StripeAdapter` | `dotnet-external-service` |
| Criar `ProcessPaymentCommand` | `dotnet-application-feature` |
| Criar `GetPaymentByIdQuery` | `dotnet-application-feature` |
| Criar `PaymentsController` | `dotnet-endpoint-generator` |
| Deploy Homologação | `dotnet-deploy-homolog` |
| Validar em Homolog | Manual |
| Deploy Produção | `dotnet-deploy-prod` |
```

### Exemplo 3: Feature Somente Leitura (Dashboard)

```markdown
## Feature: Dashboard de Vendas

### Tarefas e Skills

| Tarefa | Skill |
|--------|-------|
| Criar `SalesSummaryDto` | `dotnet-application-feature` |
| Criar `TopProductDto` | `dotnet-application-feature` |
| Criar `GetSalesSummaryQuery` | `dotnet-application-feature` |
| Criar `GetTopProductsQuery` | `dotnet-application-feature` |
| Criar `GetSalesByPeriodQuery` | `dotnet-application-feature` |
| Criar `DashboardController` | `dotnet-endpoint-generator` |
```

---

## Regras de Uso das Skills

### Sempre Consultar Referências

Ao usar qualquer skill, **SEMPRE** ler as referências antes de gerar código:

```markdown
### Ao usar `dotnet-domain-entity`:
1. Ler `references/entity-template.md`
2. Ler `references/value-objects.md` (se criar VO)
3. Ler `references/repository-interface.md` (se criar interface)

### Ao usar `dotnet-infrastructure-repository`:
1. Ler `references/repository-base.md`
2. Ler `references/repository-implementation.md`
3. Ler `references/unit-of-work.md`

### Ao usar `dotnet-application-feature`:
1. Ler `references/command-template.md` (se Command)
2. Ler `references/query-template.md` (se Query)
3. Ler `references/behaviors.md`

### Ao usar `dotnet-endpoint-generator`:
1. Ler `references/patterns.md`
2. Ler `references/structure.md`
3. Ler `references/examples.md`

### Ao usar `dotnet-external-service`:
1. Ler `references/http-client-base.md`
2. Ler `references/adapter-gateway.md`
3. Ler `references/resilience.md`
4. Ler `references/authentication.md`

### Ao usar `dotnet-deploy-homolog`:
1. Ler `references/pipeline-steps.md`
2. Ler `references/health-check.md`
3. Ler `references/troubleshooting.md`

### Ao usar `dotnet-deploy-prod`:
1. Ler `references/pre-deploy-checklist.md`
2. Ler `references/pipeline-steps.md`
3. Ler `references/rollback.md`
```

---

## Combinação de Skills por Entrega

### Entrega Mínima (MVP)

```
dotnet-domain-entity → dotnet-infrastructure-repository → 
dotnet-application-feature → dotnet-endpoint-generator → 
dotnet-deploy-homolog
```

### Entrega com Integração

```
dotnet-domain-entity → dotnet-infrastructure-repository → 
dotnet-external-service → dotnet-application-feature → 
dotnet-endpoint-generator → dotnet-deploy-homolog
```

### Entrega Produção

```
[Todas as skills da feature] → dotnet-deploy-homolog → 
[Validação] → dotnet-deploy-prod
```
