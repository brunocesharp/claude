---
name: angular-rxjs-transversal
description: Guia completo de RxJS aplicado em todas as camadas de uma solução Angular. Use sempre que o usuário mencionar "RxJS", "Observable", "Subject", "BehaviorSubject", "ReplaySubject", "operadores RxJS", "pipe RxJS", "switchMap", "mergeMap", "concatMap", "exhaustMap", "combineLatest", "forkJoin", "withLatestFrom", "debounceTime", "distinctUntilChanged", "takeUntilDestroyed", "shareReplay", "catchError", "retry", "scan", "reduce", "zip", "race", "fromEvent", "interval", "timer", "of", "from", "EMPTY", "NEVER", "stream reativo", "programação reativa Angular", "rxjs Angular", "cancelar requisição", "requisições paralelas", "encadear observables", "erro em observable", "memory leak Angular", "unsubscribe Angular", "toSignal", "interop signal observable". Também dispara quando o usuário tiver dúvidas sobre qual operador usar para um cenário específico, como "como cancelar requisição anterior", "como combinar dois observables", "como lidar com erro sem cancelar stream", "como fazer debounce de input". NÃO substitui as skills de camada (core, feature, shared) — complementa mostrando como RxJS funciona em cada uma delas.
compatibility: Angular 17+, RxJS 7+, TypeScript 5+
metadata:
  author: angular-architecture
  version: 1.0.0
  category: angular
  tags: [rxjs, angular, reactive, observable, operators, signals, interop]
---

# RxJS Transversal — Angular

RxJS é o **sistema nervoso reativo** da solução Angular. Não tem uma pasta própria — atravessa todas as camadas. Esta skill mapeia quais operadores e padrões usar em cada contexto.

## Mapa de uso por camada

| Camada | Onde o RxJS vive | Operadores mais usados |
|---|---|---|
| **Core / Services** | `BehaviorSubject`, `ReplaySubject` para estado | `shareReplay`, `distinctUntilChanged` |
| **Core / HTTP** | `HttpClient` retorna Observables | `switchMap`, `catchError`, `retry`, `timeout` |
| **Core / Hubs** | `Subject` para eventos SignalR | `fromEvent`, `share`, `takeUntil` |
| **Core / Interceptors** | Middleware de Observables HTTP | `switchMap`, `catchError`, `throwError`, `finalize` |
| **Feature / Effects** | NgRx side-effects assíncronos | `ofType`, `switchMap`, `mergeMap`, `exhaustMap`, `concatMap` |
| **Feature / Selectors** | Combinar fatias do estado | `combineLatest`, `withLatestFrom`, `map` |
| **Feature / Components** | Consumir Store no template | `async pipe`, `toSignal`, `takeUntilDestroyed` |
| **Feature / Forms** | Reagir a mudanças de valor | `debounceTime`, `distinctUntilChanged`, `switchMap` |
| **Shared / Directives** | Eventos do DOM | `fromEvent`, `throttleTime`, `debounceTime` |

## Referências disponíveis

Identifique o cenário do usuário e leia o arquivo correspondente:

| Cenário | Arquivo de referência |
|---|---|
| Criação de streams (fontes) | `references/rxjs-creation.md` |
| Transformação e filtragem | `references/rxjs-operators.md` |
| Combinação de streams | `references/rxjs-combination.md` |
| Tratamento de erros | `references/rxjs-error-handling.md` |
| Gerenciamento de subscriptions | `references/rxjs-subscription.md` |
| Padrões por camada Angular | `references/rxjs-patterns.md` |
| Interop com Signals | `references/rxjs-signals.md` |

## Fluxo de decisão — qual operador usar?

```
Preciso transformar cada valor de um stream?
  └─ map() — transformação síncrona simples
  └─ switchMap() — transforma em outro Observable, CANCELA o anterior
  └─ mergeMap() — transforma em Observable, executa EM PARALELO
  └─ concatMap() — transforma em Observable, executa em FILA (ordem garantida)
  └─ exhaustMap() — transforma em Observable, IGNORA novos enquanto ocupado

Preciso combinar múltiplos streams?
  └─ combineLatest([a$, b$]) — emite quando QUALQUER um emite (precisa de valor inicial em todos)
  └─ forkJoin([a$, b$])     — espera TODOS completarem (ex: requisições paralelas)
  └─ withLatestFrom(b$)     — combina com valor mais recente de b$ sem re-disparar
  └─ zip([a$, b$])          — combina por índice (sincroniza emissões)

Preciso filtrar emissões?
  └─ filter() — só deixa passar se condição for verdadeira
  └─ debounceTime(ms) — aguarda parar de emitir por X ms (ex: search input)
  └─ throttleTime(ms) — emite no máximo 1x por X ms (ex: scroll, resize)
  └─ distinctUntilChanged() — só emite se valor mudou
  └─ take(n) — completa após N emissões
  └─ first() — completa após primeira emissão

Preciso tratar erros?
  └─ catchError() — captura e retorna Observable alternativo
  └─ retry(n) — retenta N vezes antes de propagar o erro
  └─ retryWhen() — retenta com lógica customizada (backoff exponencial)

Preciso compartilhar um stream entre múltiplos subscribers?
  └─ shareReplay(1) — cacheia o último valor e compartilha (HTTP requests)
  └─ share() — multicasta sem cache (eventos, cliques)
```

## Regras de ouro no contexto Angular

1. **SEMPRE** use `takeUntilDestroyed()` em subscriptions de componentes
2. **NUNCA** faça subscribe dentro de subscribe — use `switchMap`/`mergeMap`
3. **PREFIRA** `async pipe` no template ao invés de subscribe manual
4. **PREFIRA** `toSignal()` para integrar Observables com o sistema de Signals
5. **EVITE** `tap()` para lógica — use para logging e debug apenas
6. **USE** `shareReplay(1)` em HTTP requests que podem ter múltiplos subscribers
7. **NUNCA** use `share()` sozinho para HTTP — o request seria refeito por cada subscriber

## Troubleshooting rápido

**Memory leak / subscription não cancela**
→ Leia `references/rxjs-subscription.md`

**Múltiplas requisições HTTP disparadas**
→ Usar `exhaustMap` em vez de `switchMap` nos Effects de submit

**Valor chega undefined no combineLatest**
→ Todos os streams precisam emitir pelo menos um valor; usar `startWith()`

**switchMap cancela requisição que não deveria**
→ Avaliar `mergeMap` (paralelo) ou `concatMap` (fila)

**toSignal dá erro de injection context**
→ Deve ser chamado no construtor ou com `runInInjectionContext`
