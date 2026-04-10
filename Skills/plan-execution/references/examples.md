# Execution Plan Examples

## Exemplo 1: E-Commerce - Módulo de Produtos

### Especificação Resumida

```
Funcionalidades:
- CRUD de produtos
- Categorização
- Controle de estoque
- Busca e filtros
- Ativação/desativação

Regras:
- Produto deve ter categoria
- SKU único
- Preço não pode ser negativo
- Estoque não pode ficar negativo
```

### Plano de Execução

```markdown
# Plano de Execução: Módulo de Produtos

## Visão Geral das Entregas

| # | Entrega | Descrição | Est. | Dep. |
|---|---------|-----------|------|------|
| 1 | CRUD Básico | Create, Read, Update de produtos | 3d | - |
| 2 | Categorias | CRUD de categorias + vínculo | 2d | 1 |
| 3 | Listagem | Paginação, busca, filtros | 1.5d | 1 |
| 4 | Estoque | Entrada/saída de estoque | 1.5d | 1 |

**Total: 8 dias**

---

## Entrega 1: CRUD Básico de Produtos

### Objetivo
Permitir criar, visualizar e atualizar produtos.

### Tarefas

#### Domain Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.1 | Criar VO `Money` | `dotnet-domain-entity` | 1h |
| 1.2 | Criar VO `Sku` | `dotnet-domain-entity` | 1h |
| 1.3 | Criar Enum `ProductStatus` | `dotnet-domain-entity` | 0.5h |
| 1.4 | Criar Entity `Product` | `dotnet-domain-entity` | 3h |
| 1.5 | Criar Interface `IProductRepository` | `dotnet-domain-entity` | 1h |

#### Infrastructure Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.6 | Criar `ProductConfiguration` | - | 1h |
| 1.7 | Criar `ProductRepository` | `dotnet-infrastructure-repository` | 2h |
| 1.8 | Criar Migration | - | 0.5h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.9 | Criar `ProductDto` | `dotnet-application-feature` | 0.5h |
| 1.10 | Criar `CreateProductCommand` | `dotnet-application-feature` | 2.5h |
| 1.11 | Criar `UpdateProductCommand` | `dotnet-application-feature` | 2h |
| 1.12 | Criar `GetProductByIdQuery` | `dotnet-application-feature` | 1.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.13 | Criar Request Models | `dotnet-endpoint-generator` | 1h |
| 1.14 | Criar Validators | `dotnet-endpoint-generator` | 1h |
| 1.15 | Criar `ProductsController` | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 1.16 | Testes unitários Domain | 2h |
| 1.17 | Testes unitários Application | 3h |
| 1.18 | Testes integração API | 2h |

**Subtotal: 24h (3 dias)**

### Critérios de Aceite
- [ ] POST /api/products cria produto
- [ ] GET /api/products/{id} retorna produto
- [ ] PUT /api/products/{id} atualiza produto
- [ ] Validações funcionando (SKU único, preço positivo)

---

## Entrega 2: Categorias

### Objetivo
Permitir categorizar produtos.

### Tarefas

#### Domain Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.1 | Criar Entity `Category` | `dotnet-domain-entity` | 2h |
| 2.2 | Criar Interface `ICategoryRepository` | `dotnet-domain-entity` | 0.5h |
| 2.3 | Adicionar `CategoryId` em `Product` | `dotnet-domain-entity` | 1h |

#### Infrastructure Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.4 | Criar `CategoryConfiguration` | - | 1h |
| 2.5 | Criar `CategoryRepository` | `dotnet-infrastructure-repository` | 1.5h |
| 2.6 | Atualizar `ProductConfiguration` | - | 0.5h |
| 2.7 | Criar Migration | - | 0.5h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.8 | Criar `CategoryDto` | `dotnet-application-feature` | 0.5h |
| 2.9 | Criar `CreateCategoryCommand` | `dotnet-application-feature` | 2h |
| 2.10 | Criar `GetCategoryListQuery` | `dotnet-application-feature` | 1.5h |
| 2.11 | Atualizar `CreateProductCommand` (categoria obrigatória) | `dotnet-application-feature` | 1h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.12 | Criar `CategoriesController` | `dotnet-endpoint-generator` | 1.5h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 2.13 | Testes Category | 2h |

**Subtotal: 16h (2 dias)**

---

## Entrega 3: Listagem e Filtros

### Objetivo
Permitir listar produtos com paginação e filtros.

### Tarefas

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.1 | Criar `ProductListItemDto` | `dotnet-application-feature` | 0.5h |
| 3.2 | Criar `GetProductListQuery` (paginado) | `dotnet-application-feature` | 3h |
| 3.3 | Criar `SearchProductsQuery` | `dotnet-application-feature` | 2h |

#### Infrastructure Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.4 | Adicionar queries paginadas no Repository | `dotnet-infrastructure-repository` | 2h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.5 | Adicionar endpoints de listagem | `dotnet-endpoint-generator` | 1.5h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 3.6 | Testes de paginação e filtros | 2h |

**Subtotal: 11h (1.5 dias)**

---

## Entrega 4: Controle de Estoque

### Objetivo
Permitir entrada e saída de estoque.

### Tarefas

#### Domain Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.1 | Adicionar métodos `IncreaseStock`/`DecreaseStock` em `Product` | `dotnet-domain-entity` | 2h |
| 4.2 | Criar Event `StockChangedEvent` | `dotnet-domain-entity` | 0.5h |
| 4.3 | Criar Exception `InsufficientStockException` | `dotnet-domain-entity` | 0.5h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.4 | Criar `IncreaseStockCommand` | `dotnet-application-feature` | 2h |
| 4.5 | Criar `DecreaseStockCommand` | `dotnet-application-feature` | 2h |
| 4.6 | Criar `GetLowStockProductsQuery` | `dotnet-application-feature` | 1.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.7 | Adicionar endpoints de estoque | `dotnet-endpoint-generator` | 1.5h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 4.8 | Testes de estoque | 2h |

**Subtotal: 12h (1.5 dias)**

---

## Cronograma

```
Semana 1:
├── Dia 1-2: Entrega 1 (Domain + Infrastructure)
├── Dia 3-4: Entrega 1 (Application + Presentation)
└── Dia 5: Entrega 1 (Testes) + Entrega 2 (início)

Semana 2:
├── Dia 1: Entrega 2 (conclusão)
├── Dia 2-3: Entrega 3
├── Dia 4: Entrega 4
└── Dia 5: Deploy Homolog + Validação
```
```

---

## Exemplo 2: Sistema de Pagamentos com Integração

### Especificação Resumida

```
Funcionalidades:
- Criar pagamento
- Processar via Stripe
- Consultar status
- Webhook de atualização
- Reembolso

Integrações:
- Stripe API
```

### Plano de Execução

```markdown
# Plano de Execução: Sistema de Pagamentos

## Visão Geral das Entregas

| # | Entrega | Descrição | Est. | Dep. |
|---|---------|-----------|------|------|
| 1 | Domínio + Integração | Entidades + Gateway Stripe | 3d | - |
| 2 | Criar Pagamento | Flow completo de criação | 2d | 1 |
| 3 | Consultas + Webhook | Status e atualizações | 1.5d | 2 |
| 4 | Reembolso | Flow de reembolso | 1d | 2 |

**Total: 7.5 dias**

---

## Entrega 1: Domínio e Integração Stripe

### Tarefas

#### Domain Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.1 | Criar VO `Money` | `dotnet-domain-entity` | 1h |
| 1.2 | Criar Enum `PaymentStatus` | `dotnet-domain-entity` | 0.5h |
| 1.3 | Criar Enum `PaymentMethod` | `dotnet-domain-entity` | 0.5h |
| 1.4 | Criar Aggregate `Payment` | `dotnet-domain-entity` | 4h |
| 1.5 | Criar Events (Created, Processed, Failed, Refunded) | `dotnet-domain-entity` | 1h |
| 1.6 | Criar Interface `IPaymentRepository` | `dotnet-domain-entity` | 1h |

#### Infrastructure - Persistence
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.7 | Criar `PaymentConfiguration` | - | 1.5h |
| 1.8 | Criar `PaymentRepository` | `dotnet-infrastructure-repository` | 2h |
| 1.9 | Criar Migration | - | 0.5h |

#### Infrastructure - External Service
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.10 | Criar `IStripeGateway` | `dotnet-external-service` | 1h |
| 1.11 | Criar `StripeSettings` | `dotnet-external-service` | 0.5h |
| 1.12 | Criar `StripeAdapter` | `dotnet-external-service` | 4h |
| 1.13 | Criar Models Request/Response | `dotnet-external-service` | 2h |
| 1.14 | Configurar Polly + HttpClient | `dotnet-external-service` | 1h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 1.15 | Testes Domain | 2h |
| 1.16 | Testes StripeAdapter (mock) | 2h |

**Subtotal: 24.5h (3 dias)**

---

## Entrega 2: Criar Pagamento

### Tarefas

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.1 | Criar `PaymentDto` | `dotnet-application-feature` | 0.5h |
| 2.2 | Criar `CreatePaymentCommand` | `dotnet-application-feature` | 3h |
| 2.3 | Criar `ProcessPaymentCommand` | `dotnet-application-feature` | 3h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.4 | Criar Request Models | `dotnet-endpoint-generator` | 1h |
| 2.5 | Criar Validators | `dotnet-endpoint-generator` | 1h |
| 2.6 | Criar `PaymentsController` (POST) | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 2.7 | Testes Handlers | 3h |
| 2.8 | Testes Integração | 2h |

**Subtotal: 15.5h (2 dias)**

---

## Entrega 3: Consultas e Webhook

### Tarefas

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.1 | Criar `GetPaymentByIdQuery` | `dotnet-application-feature` | 1.5h |
| 3.2 | Criar `GetPaymentsByCustomerQuery` | `dotnet-application-feature` | 2h |
| 3.3 | Criar `UpdatePaymentStatusCommand` | `dotnet-application-feature` | 2h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.4 | Adicionar GET endpoints | `dotnet-endpoint-generator` | 1h |
| 3.5 | Criar `WebhookController` | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 3.6 | Testes Queries | 1.5h |
| 3.7 | Testes Webhook | 2h |

**Subtotal: 12h (1.5 dias)**

---

## Entrega 4: Reembolso

### Tarefas

#### Domain Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.1 | Adicionar método `Refund` em `Payment` | `dotnet-domain-entity` | 1h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.2 | Criar `RefundPaymentCommand` | `dotnet-application-feature` | 2.5h |

#### Infrastructure
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.3 | Adicionar `RefundAsync` no StripeAdapter | `dotnet-external-service` | 1.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.4 | Adicionar endpoint POST /payments/{id}/refund | `dotnet-endpoint-generator` | 1h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 4.5 | Testes Refund | 2h |

**Subtotal: 8h (1 dia)**
```

---

## Exemplo 3: Feature Simples (Relatório)

### Especificação Resumida

```
Funcionalidades:
- Dashboard com resumo de vendas
- Top 10 produtos mais vendidos
- Vendas por período
```

### Plano de Execução

```markdown
# Plano de Execução: Dashboard de Vendas

## Visão Geral

**Entrega única** - Feature somente leitura, sem Domain novo.

| # | Entrega | Descrição | Est. |
|---|---------|-----------|------|
| 1 | Dashboard | Queries + Endpoints | 2d |

---

## Entrega 1: Dashboard

### Tarefas

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.1 | Criar `SalesSummaryDto` | `dotnet-application-feature` | 0.5h |
| 1.2 | Criar `TopProductDto` | `dotnet-application-feature` | 0.5h |
| 1.3 | Criar `SalesByPeriodDto` | `dotnet-application-feature` | 0.5h |
| 1.4 | Criar `GetSalesSummaryQuery` | `dotnet-application-feature` | 2h |
| 1.5 | Criar `GetTopProductsQuery` | `dotnet-application-feature` | 2h |
| 1.6 | Criar `GetSalesByPeriodQuery` | `dotnet-application-feature` | 2.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.7 | Criar `DashboardController` | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Tarefa | Est. |
|----|--------|------|
| 1.8 | Testes Queries | 3h |
| 1.9 | Testes Integração | 2h |

**Subtotal: 15h (2 dias)**

### Endpoints

- GET /api/dashboard/summary
- GET /api/dashboard/top-products?limit=10
- GET /api/dashboard/sales?from=2025-01-01&to=2025-01-31
```
