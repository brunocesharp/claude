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
# Plano de Execução: [FEATURE] [E-COMMERCE - PRODUTO] - Módulo de Produtos

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
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.1 | [TASK] Desenvolver - [PRODUTO] - Criar VO `Money` | `dotnet-domain-entity` | 1h |
| 1.2 | [TASK] Desenvolver - [PRODUTO] - Criar VO `Sku` | `dotnet-domain-entity` | 1h |
| 1.3 | [TASK] Desenvolver - [PRODUTO] - Criar Enum `ProductStatus` | `dotnet-domain-entity` | 0.5h |
| 1.4 | [TASK] Desenvolver - [PRODUTO] - Criar Entity `Product` | `dotnet-domain-entity` | 3h |
| 1.5 | [TASK] Desenvolver - [PRODUTO] - Criar Interface `IProductRepository` | `dotnet-domain-entity` | 1h |

#### Infrastructure Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.6 | [HT] [PRODUTO] - Criar `ProductConfiguration` (EF Core) | - | 1h |
| 1.7 | [TASK] Desenvolver - [PRODUTO] - Criar `ProductRepository` | `dotnet-infrastructure-repository` | 2h |
| 1.8 | [HT] [PRODUTO] - Criar Migration inicial | - | 0.5h |

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.9 | [TASK] Desenvolver - [PRODUTO] - Criar `ProductDto` | `dotnet-application-feature` | 0.5h |
| 1.10 | [TASK] Desenvolver - [PRODUTO] - Criar `CreateProductCommand` | `dotnet-application-feature` | 2.5h |
| 1.11 | [TASK] Desenvolver - [PRODUTO] - Criar `UpdateProductCommand` | `dotnet-application-feature` | 2h |
| 1.12 | [TASK] Desenvolver - [PRODUTO] - Criar `GetProductByIdQuery` | `dotnet-application-feature` | 1.5h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.13 | [TASK] Desenvolver - [PRODUTO] - Criar Request Models | `dotnet-endpoint-generator` | 1h |
| 1.14 | [TASK] Desenvolver - [PRODUTO] - Criar Validators | `dotnet-endpoint-generator` | 1h |
| 1.15 | [TASK] Desenvolver - [PRODUTO] - Criar `ProductsController` | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 1.16 | [TASK] Testar - [PRODUTO] - Testes unitários Domain | 2h |
| 1.17 | [TASK] Testar - [PRODUTO] - Testes unitários Application | 3h |
| 1.18 | [TASK] Testar - [PRODUTO] - Testes de integração API | 2h |

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
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 2.1 | [TASK] Desenvolver - [PRODUTO] - Criar Entity `Category` | `dotnet-domain-entity` | 2h |
| 2.2 | [TASK] Desenvolver - [PRODUTO] - Criar Interface `ICategoryRepository` | `dotnet-domain-entity` | 0.5h |
| 2.3 | [TASK] Desenvolver - [PRODUTO] - Adicionar `CategoryId` em `Product` | `dotnet-domain-entity` | 1h |

#### Infrastructure Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 2.4 | [HT] [PRODUTO] - Criar `CategoryConfiguration` (EF Core) | - | 1h |
| 2.5 | [TASK] Desenvolver - [PRODUTO] - Criar `CategoryRepository` | `dotnet-infrastructure-repository` | 1.5h |
| 2.6 | [HT] [PRODUTO] - Atualizar `ProductConfiguration` (FK Categoria) | - | 0.5h |
| 2.7 | [HT] [PRODUTO] - Criar Migration (vínculo categoria) | - | 0.5h |

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 2.8 | [TASK] Desenvolver - [PRODUTO] - Criar `CategoryDto` | `dotnet-application-feature` | 0.5h |
| 2.9 | [TASK] Desenvolver - [PRODUTO] - Criar `CreateCategoryCommand` | `dotnet-application-feature` | 2h |
| 2.10 | [TASK] Desenvolver - [PRODUTO] - Criar `GetCategoryListQuery` | `dotnet-application-feature` | 1.5h |
| 2.11 | [TASK] Desenvolver - [PRODUTO] - Atualizar `CreateProductCommand` (categoria obrigatória) | `dotnet-application-feature` | 1h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 2.12 | [TASK] Desenvolver - [PRODUTO] - Criar `CategoriesController` | `dotnet-endpoint-generator` | 1.5h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 2.13 | [TASK] Testar - [PRODUTO] - Testes Category | 2h |

**Subtotal: 16h (2 dias)**

---

## Entrega 3: Listagem e Filtros

### Objetivo
Permitir listar produtos com paginação e filtros.

### Tarefas

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 3.1 | [TASK] Desenvolver - [PRODUTO] - Criar `ProductListItemDto` | `dotnet-application-feature` | 0.5h |
| 3.2 | [TASK] Desenvolver - [PRODUTO] - Criar `GetProductListQuery` (paginado) | `dotnet-application-feature` | 3h |
| 3.3 | [TASK] Desenvolver - [PRODUTO] - Criar `SearchProductsQuery` | `dotnet-application-feature` | 2h |

#### Infrastructure Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 3.4 | [TASK] Desenvolver - [PRODUTO] - Adicionar queries paginadas no Repository | `dotnet-infrastructure-repository` | 2h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 3.5 | [TASK] Desenvolver - [PRODUTO] - Adicionar endpoints de listagem | `dotnet-endpoint-generator` | 1.5h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 3.6 | [TASK] Testar - [PRODUTO] - Testes de paginação e filtros | 2h |

**Subtotal: 11h (1.5 dias)**

---

## Entrega 4: Controle de Estoque

### Objetivo
Permitir entrada e saída de estoque.

### Tarefas

#### Domain Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 4.1 | [TASK] Desenvolver - [PRODUTO] - Adicionar métodos `IncreaseStock`/`DecreaseStock` em `Product` | `dotnet-domain-entity` | 2h |
| 4.2 | [TASK] Desenvolver - [PRODUTO] - Criar Event `StockChangedEvent` | `dotnet-domain-entity` | 0.5h |
| 4.3 | [TASK] Desenvolver - [PRODUTO] - Criar Exception `InsufficientStockException` | `dotnet-domain-entity` | 0.5h |

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 4.4 | [TASK] Desenvolver - [PRODUTO] - Criar `IncreaseStockCommand` | `dotnet-application-feature` | 2h |
| 4.5 | [TASK] Desenvolver - [PRODUTO] - Criar `DecreaseStockCommand` | `dotnet-application-feature` | 2h |
| 4.6 | [TASK] Desenvolver - [PRODUTO] - Criar `GetLowStockProductsQuery` | `dotnet-application-feature` | 1.5h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 4.7 | [TASK] Desenvolver - [PRODUTO] - Adicionar endpoints de estoque | `dotnet-endpoint-generator` | 1.5h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 4.8 | [TASK] Testar - [PRODUTO] - Testes de estoque | 2h |

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
# Plano de Execução: [FEATURE] [FINANCEIRO - PAGAMENTO] - Sistema de Pagamentos

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
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.1 | [TASK] Desenvolver - [PAGAMENTO] - Criar VO `Money` | `dotnet-domain-entity` | 1h |
| 1.2 | [TASK] Desenvolver - [PAGAMENTO] - Criar Enum `PaymentStatus` | `dotnet-domain-entity` | 0.5h |
| 1.3 | [TASK] Desenvolver - [PAGAMENTO] - Criar Enum `PaymentMethod` | `dotnet-domain-entity` | 0.5h |
| 1.4 | [TASK] Desenvolver - [PAGAMENTO] - Criar Aggregate `Payment` | `dotnet-domain-entity` | 4h |
| 1.5 | [TASK] Desenvolver - [PAGAMENTO] - Criar Events (Created, Processed, Failed, Refunded) | `dotnet-domain-entity` | 1h |
| 1.6 | [TASK] Desenvolver - [PAGAMENTO] - Criar Interface `IPaymentRepository` | `dotnet-domain-entity` | 1h |

#### Infrastructure - Persistência
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.7 | [HT] [PAGAMENTO] - Criar `PaymentConfiguration` (EF Core) | - | 1.5h |
| 1.8 | [TASK] Desenvolver - [PAGAMENTO] - Criar `PaymentRepository` | `dotnet-infrastructure-repository` | 2h |
| 1.9 | [HT] [PAGAMENTO] - Criar Migration inicial | - | 0.5h |

#### Infrastructure - Serviço Externo
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.10 | [TASK] Desenvolver - [PAGAMENTO] - Criar `IStripeGateway` | `dotnet-external-service` | 1h |
| 1.11 | [HT] [PAGAMENTO] - Criar `StripeSettings` (configuração) | `dotnet-external-service` | 0.5h |
| 1.12 | [TASK] Desenvolver - [PAGAMENTO] - Criar `StripeAdapter` | `dotnet-external-service` | 4h |
| 1.13 | [TASK] Desenvolver - [PAGAMENTO] - Criar Models Request/Response Stripe | `dotnet-external-service` | 2h |
| 1.14 | [HT] [PAGAMENTO] - Configurar Polly + HttpClient (resiliência) | `dotnet-external-service` | 1h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 1.15 | [TASK] Testar - [PAGAMENTO] - Testes unitários Domain | 2h |
| 1.16 | [TASK] Testar - [PAGAMENTO] - Testes StripeAdapter (mock) | 2h |

**Subtotal: 24.5h (3 dias)**

---

## Entrega 2: Criar Pagamento

### Tarefas

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 2.1 | [TASK] Desenvolver - [PAGAMENTO] - Criar `PaymentDto` | `dotnet-application-feature` | 0.5h |
| 2.2 | [TASK] Desenvolver - [PAGAMENTO] - Criar `CreatePaymentCommand` | `dotnet-application-feature` | 3h |
| 2.3 | [TASK] Desenvolver - [PAGAMENTO] - Criar `ProcessPaymentCommand` | `dotnet-application-feature` | 3h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 2.4 | [TASK] Desenvolver - [PAGAMENTO] - Criar Request Models | `dotnet-endpoint-generator` | 1h |
| 2.5 | [TASK] Desenvolver - [PAGAMENTO] - Criar Validators | `dotnet-endpoint-generator` | 1h |
| 2.6 | [TASK] Desenvolver - [PAGAMENTO] - Criar `PaymentsController` (POST) | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 2.7 | [TASK] Testar - [PAGAMENTO] - Testes unitários Handlers | 3h |
| 2.8 | [TASK] Testar - [PAGAMENTO] - Testes de integração | 2h |

**Subtotal: 15.5h (2 dias)**

---

## Entrega 3: Consultas e Webhook

### Tarefas

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 3.1 | [TASK] Desenvolver - [PAGAMENTO] - Criar `GetPaymentByIdQuery` | `dotnet-application-feature` | 1.5h |
| 3.2 | [TASK] Desenvolver - [PAGAMENTO] - Criar `GetPaymentsByCustomerQuery` | `dotnet-application-feature` | 2h |
| 3.3 | [TASK] Desenvolver - [PAGAMENTO] - Criar `UpdatePaymentStatusCommand` | `dotnet-application-feature` | 2h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 3.4 | [TASK] Desenvolver - [PAGAMENTO] - Adicionar GET endpoints | `dotnet-endpoint-generator` | 1h |
| 3.5 | [TASK] Desenvolver - [PAGAMENTO] - Criar `WebhookController` | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 3.6 | [TASK] Testar - [PAGAMENTO] - Testes unitários Queries | 1.5h |
| 3.7 | [TASK] Testar - [PAGAMENTO] - Testes Webhook | 2h |

**Subtotal: 12h (1.5 dias)**

---

## Entrega 4: Reembolso

### Tarefas

#### Domain Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 4.1 | [TASK] Desenvolver - [PAGAMENTO] - Adicionar método `Refund` em `Payment` | `dotnet-domain-entity` | 1h |

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 4.2 | [TASK] Desenvolver - [PAGAMENTO] - Criar `RefundPaymentCommand` | `dotnet-application-feature` | 2.5h |

#### Infrastructure
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 4.3 | [TASK] Desenvolver - [PAGAMENTO] - Adicionar `RefundAsync` no StripeAdapter | `dotnet-external-service` | 1.5h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 4.4 | [TASK] Desenvolver - [PAGAMENTO] - Adicionar endpoint POST /payments/{id}/refund | `dotnet-endpoint-generator` | 1h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 4.5 | [TASK] Testar - [PAGAMENTO] - Testes de reembolso | 2h |

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
# Plano de Execução: [FEATURE] [VENDAS - DASHBOARD] - Dashboard de Vendas

## Visão Geral

**Entrega única** - Feature somente leitura, sem Domain novo.

| # | Entrega | Descrição | Est. |
|---|---------|-----------|------|
| 1 | Dashboard | Queries + Endpoints | 2d |

---

## Entrega 1: Dashboard

### Tarefas

#### Application Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.1 | [TASK] Desenvolver - [DASHBOARD] - Criar `SalesSummaryDto` | `dotnet-application-feature` | 0.5h |
| 1.2 | [TASK] Desenvolver - [DASHBOARD] - Criar `TopProductDto` | `dotnet-application-feature` | 0.5h |
| 1.3 | [TASK] Desenvolver - [DASHBOARD] - Criar `SalesByPeriodDto` | `dotnet-application-feature` | 0.5h |
| 1.4 | [TASK] Desenvolver - [DASHBOARD] - Criar `GetSalesSummaryQuery` | `dotnet-application-feature` | 2h |
| 1.5 | [TASK] Desenvolver - [DASHBOARD] - Criar `GetTopProductsQuery` | `dotnet-application-feature` | 2h |
| 1.6 | [TASK] Desenvolver - [DASHBOARD] - Criar `GetSalesByPeriodQuery` | `dotnet-application-feature` | 2.5h |

#### Presentation Layer
| ID | Título do Item | Skill | Est. |
|----|----------------|-------|------|
| 1.7 | [TASK] Desenvolver - [DASHBOARD] - Criar `DashboardController` | `dotnet-endpoint-generator` | 2h |

#### Testes
| ID | Título do Item | Est. |
|----|----------------|------|
| 1.8 | [TASK] Testar - [DASHBOARD] - Testes unitários Queries | 3h |
| 1.9 | [TASK] Testar - [DASHBOARD] - Testes de integração | 2h |

**Subtotal: 15h (2 dias)**

### Endpoints

- GET /api/dashboard/summary
- GET /api/dashboard/top-products?limit=10
- GET /api/dashboard/sales?from=2025-01-01&to=2025-01-31
```
