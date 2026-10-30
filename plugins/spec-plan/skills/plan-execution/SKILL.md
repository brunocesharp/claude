---
name: plan-execution
description: Gera plano de execução técnico fullstack (.NET + Angular) para implementação de features, dividindo em entregas incrementais com tarefas por camada. Use quando o usuário disser "plano de execução", "execution plan", "planejar implementação", "dividir em tarefas", "quebrar feature", "como implementar essa spec", "etapas de desenvolvimento", "decomposição técnica", "quero um plano para implementar". NÃO use para especificação funcional (use spec-functional), arquitetura (use arch-c4) ou discovery (use discovery-*).
metadata:
  version: 2.1.0
  category: planning
  depends-on: spec-functional
  recommended-after: arch-c4
  output: docs/{projeto}/plano-execucao/{escopo}/execution-plan.md
  tags: [dotnet, angular, clean-architecture, execution-plan, fullstack]
---

# .NET + Angular Execution Plan Generator

Gera planos de execução técnicos para features fullstack, com tarefas ordenadas por camada (backend Clean Architecture + frontend Angular) e estimativas de esforço.

## Instruções

### CRÍTICO: Leia as referências antes de gerar qualquer plano

1. Leia `references/plan-structure.md` — estrutura e template do documento
2. Leia `references/task-breakdown.md` — decomposição de tarefas por camada
3. Leia `references/skill-mapping.md` — mapeamento de skills por tipo de tarefa

### Passo 0: Identificar o projeto e as entradas

A raiz de trabalho é uma pasta de documentação com vários projetos, cada um em `docs/{projeto}/`. Se o usuário citou o projeto, use-o; senão, leia `docs/workspace.md` (um projeto: use e avise; vários: pergunte). Se o projeto não existir, ofereça `discovery-init`.

Leia, nesta ordem:
1. `docs/{projeto}/especificacao/{escopo}/spec-functional.md` — o que construir (obrigatório; sem ele, ofereça `spec-functional` ou aceite uma especificação enviada na conversa).
2. `docs/{projeto}/arquitetura/arquitetura.md` — contêineres, tecnologias e componentes (C4). Use para:
   - saber **quais contêineres** a entrega toca (API, SPA, banco, worker...) e escolher as skills de código pela tecnologia de cada um;
   - respeitar as decisões registradas em `docs/{projeto}/arquitetura/decisoes/` (ADRs aceitas);
   - prever tarefa de atualização do C4 quando a entrega cria contêiner, sistema externo ou componente novo.
   Se não existir, avise que o plano vai supor a arquitetura e sugira `arch-c4`.
3. `docs/{projeto}/project.md` — repositório e código local.
4. `docs/{projeto}/repositorios.md` — se existir (código em vários repositórios): qual repositório implementa cada contêiner. Nesse caso, acrescente a coluna **Repositório** nas tabelas de tarefas, ordene as entregas com o provedor antes do consumidor (backend antes do frontend que usa o endpoint novo) e, ao final, sugira a skill `multi-repo` (Mudança coordenada) para criar as branches e registrar a ordem de merge e de deploy.

### Passo 1: Analisar a Especificação

Identifique na especificação fornecida:

**Backend:**
- Entidades de domínio e Value Objects
- Casos de uso (Commands e Queries)
- Endpoints necessários
- Integrações externas

**Frontend:**
- Telas e componentes Angular necessários
- Fluxos de navegação e rotas
- Estratégia de estado (local, BehaviorSubject ou NgRx)

**Regras de negócio** que impactam ambas as camadas

### Passo 2: Definir Entregas (Releases)

Cada entrega deve:
- Entregar valor isoladamente (backend + frontend funcionando juntos)
- Ser deployável de forma independente
- Ter dependências claras com outras entregas
- Permitir validação parcial (ex.: testar API via Swagger antes do frontend)

### Passo 3: Decompor em Tarefas

Ordem obrigatória dentro de cada entrega:

**Backend (.NET):**
1. Domain → Value Objects, Entidades, Interfaces
2. Infrastructure → Repositórios, EF Config, Migrations
3. Application → DTOs, Commands, Queries, Handlers
4. Presentation → Endpoints, Validators de Request

**Frontend (Angular):**
5. Core/Shared → Models TypeScript, Services HttpClient, Interceptors, Guards
6. Feature Module → Routing (lazy), Smart Components, Presentational Components, Forms
7. State → BehaviorSubject ou NgRx (somente se necessário)

### Passo 4: Gerar o Documento

Salve em `docs/{projeto}/plano-execucao/{escopo}/execution-plan.md` seguindo o template em `references/plan-structure.md`. Atualize `docs/{projeto}/project.md` (Plano de Execução em andamento) e a coluna Situação em `docs/workspace.md`.

---

## Template de Entrega

```markdown
### Entrega N: {Nome}
- **Objetivo**: {valor entregue de forma independente}
- **Estimativa**: {X} dias
- **Dependências**: Nenhuma | Entrega N

#### Backend
| ID | Tarefa | Camada | Skill | Est. |
|----|--------|--------|-------|------|
| N.1 | Criar entidade `X` | Domain | architecture-entities | 2h |
| N.2 | Criar repositório `X` | Infrastructure | architecture-repository | 2h |
| N.3 | Criar `CreateXCommand` | Application | architecture-feature | 3h |
| N.4 | Criar `XController` | Presentation | architecture-controller | 2h |

#### Frontend (Angular)
| ID | Tarefa | Camada | Tipo | Est. |
|----|--------|--------|------|------|
| N.5 | Criar model `X` | Core/Models | Interface | 0.5h |
| N.6 | Criar `XService` (HttpClient) | Core/Services | Service | 2h |
| N.7 | Criar `XListComponent` | Feature | Smart Component | 3h |
| N.8 | Criar rota `/x` com lazy loading | Feature | Routing | 1h |

#### Testes
| ID | Tarefa | Tipo | Est. |
|----|--------|------|------|
| N.9 | Testes unitários Domain | Unit (.NET) | 2h |
| N.10 | Testes unitários Handlers | Unit (.NET) | 2h |
| N.11 | Testes unitários Service Angular | Unit (Angular) | 1h |
| N.12 | Testes integração API | Integration | 2h |

#### Critérios de Aceite
- [ ] Endpoint POST /api/x funcional e testado via Swagger
- [ ] Lista Angular exibindo dados reais da API
- [ ] Formulário Angular criando registros com feedback ao usuário
- [ ] Cobertura de testes maior que 80%
```

---

## Mapeamento de Skills

### Backend (.NET Clean Architecture)

| Tipo de Tarefa | Skill |
|----------------|-------|
| Entidade, Value Object, Aggregate | `architecture-entities` |
| Command, Query, Handler | `architecture-feature` |
| Repositório, DbContext | `architecture-repository` |
| Controller, Endpoint | `architecture-controller` |
| API Externa, Integração | `architecture-external-service` |
| Deploy Homologação | `deploy-dotnet-homolog` |
| Deploy Produção | `deploy-dotnet-prod` |

### Frontend (Angular)

| Tipo de Tarefa | Quando Usar |
|----------------|-------------|
| Interface/Model TypeScript | Sempre — espelha DTOs do backend |
| Service com HttpClient | Sempre — uma por recurso da API |
| Service de estado (BehaviorSubject) | Estado local/médio (até 3 features) |
| NgRx (Store + Effects) | Estado complexo compartilhado entre 4+ features |
| Smart Component | Containers que injetam services |
| Presentational Component | Componentes puros com @Input/@Output + OnPush |
| Routing com Lazy Loading | Sempre para Feature Modules |
| Route Guard (CanActivate) | Rotas protegidas por autenticação/autorização |
| HTTP Interceptor | Autenticação JWT, loading global, tratamento de erros |
| Reactive Form | Formulários de criação e edição |
| Signals (Angular 16+) | Estado local dentro de um único componente |

---

## Ordem de Dependências por Camada

### Backend

```
Domain (primeiro — sem dependências externas)
  └── Value Objects → Enums → Entidades → Aggregates → Interfaces → Events

Infrastructure (segundo — depende de Domain)
  └── EF Configurations → Repositories → Migrations → External Services

Application (terceiro — depende de Domain + Infrastructure)
  └── DTOs → Queries simples → Queries paginadas → Commands criação → Commands atualização → Commands ação

Presentation (último — depende de Application)
  └── Request Models → Validators → Controllers/Endpoints
```

### Frontend Angular

```
Core/Shared (fundação — sem dependências de feature)
  └── Models/Interfaces → Services HTTP → Services de estado → Interceptors → Guards

Feature Module (depende de Core/Shared)
  └── Routing (lazy) → Components presentacionais → Smart Components → Forms

State opcional (depende de Feature)
  └── NgRx Actions → Reducers → Selectors → Effects
```

---

## Estimativas de Referência

### Backend

| Tarefa | Estimativa |
|--------|------------|
| Value Object | 1-2h |
| Entidade simples | 2-3h |
| Entidade com regras de negócio | 3-5h |
| Aggregate Root | 4-8h |
| Repositório simples | 1-2h |
| Repositório com queries complexas | 2-4h |
| Command simples | 2-3h |
| Command com validações complexas | 3-5h |
| Query simples (GetById) | 1-2h |
| Query paginada com filtros | 2-3h |
| Endpoint CRUD completo | 2-4h |
| Integração externa (adapter) | 4-8h |

### Frontend Angular

| Tarefa | Estimativa |
|--------|------------|
| Model/Interface TypeScript | 0.5-1h |
| Service com HttpClient (CRUD) | 2-4h |
| Service de estado (BehaviorSubject) | 2-3h |
| NgRx por entidade (actions + reducer + selectors + effect) | 4-8h |
| Presentational Component simples | 1-2h |
| Smart Component com lista e filtros | 2-4h |
| Componente de formulário reativo | 3-5h |
| Rota + Lazy Loading de Feature Module | 1-2h |
| Route Guard | 1-2h |
| HTTP Interceptor | 2-3h |

### Testes (adicionar sobre o tempo base)

| Tipo | Fator |
|------|-------|
| Testes unitários Domain (.NET) | +50% do tempo da entidade |
| Testes unitários Handlers (.NET) | +50% do tempo do handler |
| Testes unitários Service Angular | +30% do tempo do service |
| Testes unitários Component Angular | +40% do tempo do componente |
| Testes de integração API | +30% do tempo do endpoint |
| Testes E2E (Cypress/Playwright) | 2-4h por fluxo principal |

---

## Decisão: BehaviorSubject vs NgRx

Use **BehaviorSubject** quando:
- Estado é usado por 1-3 features
- Time não conhece padrão Redux
- Prazo curto

Use **NgRx** quando:
- Estado é compartilhado por 4+ features
- Time precisa de DevTools / time-travel debug
- Aplicação tem fluxos assíncronos complexos (Effects)

**Regra prática:** comece sempre com BehaviorSubject. Migre para NgRx em refactoring planejado, nunca no meio de uma entrega.

---

## Troubleshooting

**Feature muito grande para uma entrega**
Divida em entregas menores onde cada uma entregue backend + frontend básico funcionando. Uma entrega deve caber em 1-3 dias de trabalho.

**Estimativa muito incerta para integração Angular + backend**
Crie uma "Entrega 0" de spike: montar o esqueleto do Feature Module Angular chamando um endpoint mock (json-server) antes de implementar o backend real.

**Estado complexo surgindo durante o desenvolvimento**
Não migre para NgRx no meio de uma entrega. Registre como dívida técnica e planeje entrega de refactoring separada.

**Dependência circular entre entregas**
Isole modelos e interfaces compartilhados em uma entrega 0 ou na camada `shared` do Angular e `Domain` do backend.