---
name: angular-core-layer
description: Gera todos os elementos da camada Core de uma solução Angular com SignalR, RxJS e NgRx. Use sempre que o usuário mencionar "criar core Angular", "camada core", "core service", "core hub", "SignalR Angular", "interceptor Angular", "guard Angular", "resolver Angular", "http service Angular", "error handler Angular", "model Angular", "interface Angular", "criar estrutura core", "core module", "base service", "base hub". Também dispara quando o usuário pedir para criar qualquer um destes itens: CoreService, CoreHubService, HttpService, Interceptor, Guard, Resolver, ErrorHandler, Model ou Interface em contexto Angular. NÃO use para camadas de Feature ou Shared — apenas para a camada Core.
compatibility: Angular 17+, TypeScript 5+, @microsoft/signalr, @ngrx/store, RxJS 7+
metadata:
  author: angular-architecture
  version: 1.0.0
  category: angular
  tags: [angular, core, signalr, rxjs, ngrx, interceptor, guard, resolver]
---

# Angular Core Layer

Skill para geração da **camada Core** de uma solução Angular seguindo Clean Architecture, com SignalR, RxJS e NgRx integrados.

## Visão geral da camada Core

A camada Core contém tudo que é **singleton e inicializado uma vez** na aplicação. Todos os serviços são providos com `providedIn: 'root'` ou no `CoreModule`.

```
core/
├── services/          → Core Services (lógica de negócio singleton)
├── hubs/              → SignalR Hubs (tempo real)
├── http/              → HTTP Services (chamadas REST)
├── interceptors/      → Interceptors (auth, error, logging)
├── guards/            → Guards (proteção de rotas)
├── resolvers/         → Resolvers (pré-carregamento de dados)
├── models/            → Models e Interfaces (contratos TypeScript)
└── error-handler/     → Error Handler global
```

## Itens disponíveis

Antes de gerar, identifique qual item o usuário quer criar. Consulte o arquivo de referência correspondente:

| Item | Arquivo de referência | Quando usar |
|---|---|---|
| Core Service | `references/core-service.md` | Lógica de negócio, estado com BehaviorSubject |
| Core Hub (SignalR) | `references/core-hub.md` | Comunicação tempo real com .NET SignalR |
| HTTP Service | `references/core-http.md` | Chamadas REST com HttpClient + RxJS |
| Interceptor | `references/core-interceptor.md` | Auth token, error handling, logging |
| Guard / Resolver | `references/core-guard-resolver.md` | Proteção de rotas e pré-carregamento |
| Model / Interface | `references/core-model.md` | Contratos TypeScript, DTOs, enums |
| Error Handler | `references/core-error-handler.md` | Tratamento global de erros |

## Fluxo de geração

### Passo 1 — Identificar o item
Pergunte ao usuário qual item da camada Core deseja criar, caso não esteja claro na solicitação.

### Passo 2 — Coletar informações
Colete os dados necessários para o item:
- **Nome** da entidade ou serviço (ex: `User`, `Notification`, `Auth`)
- **Contexto** de uso (o que o serviço deve fazer)
- **Dependências** (quais outros serviços ou hubs são necessários)

### Passo 3 — Ler referência e gerar
Leia o arquivo de referência do item solicitado e gere o código TypeScript completo seguindo os padrões documentados.

### Passo 4 — Entregar
Entregue:
1. O arquivo `.ts` gerado com path correto (`src/app/core/...`)
2. O registro no módulo ou `app.config.ts` se necessário
3. Exemplo de uso em um componente ou effect

## Convenções obrigatórias

- **Nomenclatura de arquivos**: `kebab-case.tipo.ts` (ex: `auth.service.ts`, `notification.hub.ts`)
- **Nomenclatura de classes**: PascalCase com sufixo (ex: `AuthService`, `NotificationHub`)
- **Injeção de dependências**: sempre via `inject()` (Angular 17+), não via constructor
- **Imports RxJS**: sempre de `rxjs` e `rxjs/operators` separados
- **Signals**: usar `signal()` e `computed()` do `@angular/core` quando o estado for local
- **`takeUntilDestroyed`**: sempre usar em subscriptions de componentes
- **`providedIn: 'root'`**: padrão para todos os Core Services

## Troubleshooting comum

**SignalR não conecta**
- Verificar CORS no backend .NET
- Confirmar que o Hub está mapeado em `Program.cs`
- Testar com `withUrl(url, { transport: HttpTransportType.WebSockets })`

**Interceptor não intercepta**
- Confirmar que está registrado em `app.config.ts` via `withInterceptors([...])`
- Para interceptors baseados em classe, usar `withInterceptorsFromDi()`

**Guard retorna sempre false**
- Verificar se `AuthService` está injetado corretamente
- Confirmar que o token está no `localStorage` ou `sessionStorage`
