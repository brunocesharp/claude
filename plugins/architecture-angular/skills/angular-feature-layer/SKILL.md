---
name: angular-feature-layer
description: Gera todos os elementos da camada Feature de uma solução Angular com NgRx, RxJS, Signals e Reactive Forms. Use sempre que o usuário mencionar "criar feature Angular", "camada feature", "smart component", "dumb component", "feature component", "feature page", "feature store", "NgRx feature", "actions Angular", "reducers Angular", "effects Angular", "selectors Angular", "reactive form Angular", "feature service", "feature routing", "lazy load Angular", "rota feature", "criar módulo feature". Também dispara quando o usuário pedir para criar qualquer um destes itens: SmartComponent, DumbComponent, FeaturePage, NgRxStore, Actions, Reducers, Effects, Selectors, ReactiveForm, FeatureService, FeatureRouting em contexto Angular. NÃO use para a camada Core (use angular-core-layer) ou Shared — apenas para Features isoladas e lazy loaded.
compatibility: Angular 17+, TypeScript 5+, @ngrx/store, @ngrx/effects, @ngrx/entity, RxJS 7+
metadata:
  author: angular-architecture
  version: 1.0.0
  category: angular
  tags: [angular, feature, ngrx, rxjs, signals, reactive-forms, lazy-loading, routing]
---

# Angular Feature Layer

Skill para geração da **camada Feature** de uma solução Angular seguindo Clean Architecture, com NgRx, RxJS, Signals e Reactive Forms integrados.

## Visão geral da camada Feature

Cada Feature é um **módulo isolado, carregado sob demanda (lazy loaded)**. Contém tudo que pertence exclusivamente àquela funcionalidade.

```
features/
└── [nome-feature]/
    ├── components/        → Smart Components (consomem Store, serviços)
    │   └── [nome]/
    │       ├── [nome].component.ts
    │       ├── [nome].component.html
    │       └── [nome].component.scss
    ├── pages/             → Pages (componentes roteados, orquestram layout)
    │   └── [nome]-page/
    ├── store/             → NgRx (Actions, Reducers, Effects, Selectors, State)
    │   ├── [nome].actions.ts
    │   ├── [nome].reducer.ts
    │   ├── [nome].effects.ts
    │   ├── [nome].selectors.ts
    │   └── [nome].state.ts
    ├── forms/             → Reactive Forms (builders, validators)
    │   └── [nome].form.ts
    ├── services/          → Feature Services (lógica local da feature)
    │   └── [nome].service.ts
    └── [nome].routes.ts   → Routing (lazy routes desta feature)
```

## Itens disponíveis

Identifique qual item o usuário quer criar e leia o arquivo de referência correspondente:

| Item | Arquivo de referência | Quando usar |
|---|---|---|
| Smart / Dumb Component | `references/feature-components.md` | Componentes que consomem Store ou recebem @Input |
| Pages | `references/feature-pages.md` | Componentes roteados que orquestram layout |
| Store NgRx | `references/feature-store.md` | Actions, Reducers, Effects, Selectors, State |
| Forms | `references/feature-forms.md` | Reactive Forms, FormBuilder, validators customizados |
| Feature Services | `references/feature-services.md` | Lógica local, estado temporário da feature |
| Routing | `references/feature-routing.md` | Rotas lazy loaded, guards, resolvers por feature |

## Fluxo de geração

### Passo 1 — Identificar o item e a feature
Pergunte ao usuário:
- Qual **item** da camada Feature deseja criar
- Qual o **nome da feature** (ex: `users`, `orders`, `dashboard`)
- Qual a **entidade principal** envolvida (ex: `User`, `Order`)

### Passo 2 — Verificar dependências
Confirme com o usuário:
- Se existe a **camada Core** já criada (models, HTTP service)
- Se a **Store** já existe (para components que consomem NgRx)
- Se o **Routing** principal já tem a feature registrada

### Passo 3 — Ler referência e gerar
Leia o arquivo de referência do item solicitado e gere os arquivos TypeScript completos.

### Passo 4 — Entregar
Entregue:
1. Todos os arquivos `.ts` com paths corretos (`src/app/features/[feature]/...`)
2. O registro no routing principal se for uma nova feature
3. Exemplo de integração entre os itens gerados

## Convenções obrigatórias

- **Standalone components**: sempre `standalone: true` (Angular 17+)
- **inject()**: sempre via `inject()`, não via constructor
- **OnPush**: sempre `ChangeDetectionStrategy.OnPush` em Smart Components
- **takeUntilDestroyed**: sempre em subscriptions de componentes
- **NgRx Entity**: usar `createEntityAdapter` para coleções de entidades
- **createFeature**: usar `createFeature()` do NgRx para registrar a store da feature
- **Signals + NgRx**: combinar `toSignal()` com selectors para interop
- **Reactive Forms**: sempre `FormBuilder` com `nonNullable` para evitar `| null`

## Padrão de nomenclatura

| Tipo | Padrão | Exemplo |
|---|---|---|
| Feature folder | `kebab-case` | `users/`, `order-management/` |
| Actions | `[Feature]Actions.verb` | `UsersActions.loadAll` |
| Reducer | `[feature]Reducer` | `usersReducer` |
| Effects class | `[Feature]Effects` | `UsersEffects` |
| Selectors | `select[Feature][Campo]` | `selectUsersAll`, `selectUsersLoading` |
| Feature state | `[Feature]State` | `UsersState` |
| Form class | `[Feature]Form` | `UserForm` |

## Troubleshooting comum

**Effect não dispara**
- Verificar se `EffectsModule.forFeature([XEffects])` ou `provideEffects([XEffects])` está registrado
- Confirmar que a Action está sendo despachada via `store.dispatch()`

**Selector retorna undefined**
- Confirmar que `provideState(featureName, reducer)` está no routing da feature
- Verificar se o `featureName` do `createFeature` bate com o registrado

**Reactive Form não valida**
- Usar `nonNullable: true` no FormBuilder para evitar valores `null`
- Confirmar que `ReactiveFormsModule` está nos `imports` do componente standalone

**Lazy loading não funciona**
- Verificar se a feature usa `loadComponent` ou `loadChildren` corretamente
- Confirmar que não há import direto do componente no routing principal
