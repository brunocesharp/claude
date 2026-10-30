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
| 1.1 | Criar VO `Money` | `architecture-entities` | 1h |
| 1.2 | Criar VO `Sku` | `architecture-entities` | 1h |
| 1.3 | Criar Enum `ProductStatus` | `architecture-entities` | 0.5h |
| 1.4 | Criar Entity `Product` | `architecture-entities` | 3h |
| 1.5 | Criar Interface `IProductRepository` | `architecture-entities` | 1h |

#### Infrastructure Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.6 | Criar `ProductConfiguration` | - | 1h |
| 1.7 | Criar `ProductRepository` | `architecture-repository` | 2h |
| 1.8 | Criar Migration | - | 0.5h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.9 | Criar `ProductDto` | `architecture-feature` | 0.5h |
| 1.10 | Criar `CreateProductCommand` | `architecture-feature` | 2.5h |
| 1.11 | Criar `UpdateProductCommand` | `architecture-feature` | 2h |
| 1.12 | Criar `GetProductByIdQuery` | `architecture-feature` | 1.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.13 | Criar Request Models | `architecture-controller` | 1h |
| 1.14 | Criar Validators | `architecture-controller` | 1h |
| 1.15 | Criar `ProductsController` | `architecture-controller` | 2h |

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
| 2.1 | Criar Entity `Category` | `architecture-entities` | 2h |
| 2.2 | Criar Interface `ICategoryRepository` | `architecture-entities` | 0.5h |
| 2.3 | Adicionar `CategoryId` em `Product` | `architecture-entities` | 1h |

#### Infrastructure Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.4 | Criar `CategoryConfiguration` | - | 1h |
| 2.5 | Criar `CategoryRepository` | `architecture-repository` | 1.5h |
| 2.6 | Atualizar `ProductConfiguration` | - | 0.5h |
| 2.7 | Criar Migration | - | 0.5h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.8 | Criar `CategoryDto` | `architecture-feature` | 0.5h |
| 2.9 | Criar `CreateCategoryCommand` | `architecture-feature` | 2h |
| 2.10 | Criar `GetCategoryListQuery` | `architecture-feature` | 1.5h |
| 2.11 | Atualizar `CreateProductCommand` (categoria obrigatória) | `architecture-feature` | 1h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.12 | Criar `CategoriesController` | `architecture-controller` | 1.5h |

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
| 3.1 | Criar `ProductListItemDto` | `architecture-feature` | 0.5h |
| 3.2 | Criar `GetProductListQuery` (paginado) | `architecture-feature` | 3h |
| 3.3 | Criar `SearchProductsQuery` | `architecture-feature` | 2h |

#### Infrastructure Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.4 | Adicionar queries paginadas no Repository | `architecture-repository` | 2h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.5 | Adicionar endpoints de listagem | `architecture-controller` | 1.5h |

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
| 4.1 | Adicionar métodos `IncreaseStock`/`DecreaseStock` em `Product` | `architecture-entities` | 2h |
| 4.2 | Criar Event `StockChangedEvent` | `architecture-entities` | 0.5h |
| 4.3 | Criar Exception `InsufficientStockException` | `architecture-entities` | 0.5h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.4 | Criar `IncreaseStockCommand` | `architecture-feature` | 2h |
| 4.5 | Criar `DecreaseStockCommand` | `architecture-feature` | 2h |
| 4.6 | Criar `GetLowStockProductsQuery` | `architecture-feature` | 1.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.7 | Adicionar endpoints de estoque | `architecture-controller` | 1.5h |

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
| 1.1 | Criar VO `Money` | `architecture-entities` | 1h |
| 1.2 | Criar Enum `PaymentStatus` | `architecture-entities` | 0.5h |
| 1.3 | Criar Enum `PaymentMethod` | `architecture-entities` | 0.5h |
| 1.4 | Criar Aggregate `Payment` | `architecture-entities` | 4h |
| 1.5 | Criar Events (Created, Processed, Failed, Refunded) | `architecture-entities` | 1h |
| 1.6 | Criar Interface `IPaymentRepository` | `architecture-entities` | 1h |

#### Infrastructure - Persistence
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.7 | Criar `PaymentConfiguration` | - | 1.5h |
| 1.8 | Criar `PaymentRepository` | `architecture-repository` | 2h |
| 1.9 | Criar Migration | - | 0.5h |

#### Infrastructure - External Service
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.10 | Criar `IStripeGateway` | `architecture-external-service` | 1h |
| 1.11 | Criar `StripeSettings` | `architecture-external-service` | 0.5h |
| 1.12 | Criar `StripeAdapter` | `architecture-external-service` | 4h |
| 1.13 | Criar Models Request/Response | `architecture-external-service` | 2h |
| 1.14 | Configurar Polly + HttpClient | `architecture-external-service` | 1h |

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
| 2.1 | Criar `PaymentDto` | `architecture-feature` | 0.5h |
| 2.2 | Criar `CreatePaymentCommand` | `architecture-feature` | 3h |
| 2.3 | Criar `ProcessPaymentCommand` | `architecture-feature` | 3h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 2.4 | Criar Request Models | `architecture-controller` | 1h |
| 2.5 | Criar Validators | `architecture-controller` | 1h |
| 2.6 | Criar `PaymentsController` (POST) | `architecture-controller` | 2h |

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
| 3.1 | Criar `GetPaymentByIdQuery` | `architecture-feature` | 1.5h |
| 3.2 | Criar `GetPaymentsByCustomerQuery` | `architecture-feature` | 2h |
| 3.3 | Criar `UpdatePaymentStatusCommand` | `architecture-feature` | 2h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 3.4 | Adicionar GET endpoints | `architecture-controller` | 1h |
| 3.5 | Criar `WebhookController` | `architecture-controller` | 2h |

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
| 4.1 | Adicionar método `Refund` em `Payment` | `architecture-entities` | 1h |

#### Application Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.2 | Criar `RefundPaymentCommand` | `architecture-feature` | 2.5h |

#### Infrastructure
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.3 | Adicionar `RefundAsync` no StripeAdapter | `architecture-external-service` | 1.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 4.4 | Adicionar endpoint POST /payments/{id}/refund | `architecture-controller` | 1h |

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
| 1.1 | Criar `SalesSummaryDto` | `architecture-feature` | 0.5h |
| 1.2 | Criar `TopProductDto` | `architecture-feature` | 0.5h |
| 1.3 | Criar `SalesByPeriodDto` | `architecture-feature` | 0.5h |
| 1.4 | Criar `GetSalesSummaryQuery` | `architecture-feature` | 2h |
| 1.5 | Criar `GetTopProductsQuery` | `architecture-feature` | 2h |
| 1.6 | Criar `GetSalesByPeriodQuery` | `architecture-feature` | 2.5h |

#### Presentation Layer
| ID | Tarefa | Skill | Est. |
|----|--------|-------|------|
| 1.7 | Criar `DashboardController` | `architecture-controller` | 2h |

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
