# RxJS — Operadores de Transformação e Filtragem

## Os 4 operadores de Higher-Order Mapping (os mais importantes)

### Guia de escolha

```
Usuário clica BUSCAR com nova query:
  → switchMap ✅  (cancela busca anterior — a mais recente vence)

Usuário clica UPLOAD de vários arquivos:
  → mergeMap ✅   (todos em paralelo, sem cancelar)

Usuário clica SALVAR (não pode duplicar):
  → concatMap ✅  (fila — garante ordem, processa um de cada vez)
  → exhaustMap ✅ (ignora cliques extras enquanto salva)
```

---

## `switchMap` — cancela o anterior, ativa o novo

```typescript
import { switchMap, catchError } from 'rxjs/operators';
import { of } from 'rxjs';

// ── Caso 1: Search input com cancelamento ────────────────
// Quando o usuário digita nova letra, a requisição anterior é cancelada
@Injectable({ providedIn: 'root' })
export class SearchService {
  search(term$: Observable<string>): Observable<SearchResult[]> {
    return term$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      filter(term => term.length >= 2),
      switchMap(term =>             // ← cancela HTTP anterior
        this.api.search(term).pipe(
          catchError(() => of([]))  // ← erro não cancela o stream pai
        )
      )
    );
  }
}

// ── Caso 2: NgRx Effect de listagem ─────────────────────
loadUsers$ = createEffect(() =>
  this.actions$.pipe(
    ofType(UsersActions.loadAll),
    switchMap(() =>                 // ← se 2 dispatches chegam rápido, cancela o primeiro
      this.api.getAll().pipe(
        map(users => UsersActions.loadAllSuccess({ users })),
        catchError(err => of(UsersActions.loadAllFailure({ error: err.message })))
      )
    )
  )
);

// ── Caso 3: Route param → load detail ───────────────────
// Quando muda o ID na URL, cancela requisição anterior e carrega novo
this.route.paramMap.pipe(
  map(params => params.get('id')!),
  distinctUntilChanged(),
  switchMap(id => this.api.getById(id)),
  takeUntilDestroyed()
).subscribe(user => this.user.set(user));
```

---

## `mergeMap` — paralelo, não cancela

```typescript
import { mergeMap } from 'rxjs/operators';

// ── Caso 1: Upload de múltiplos arquivos em paralelo ─────
uploadAll(files: File[]): Observable<UploadResult> {
  return from(files).pipe(
    mergeMap(file => this.api.upload(file)), // ← todos em paralelo
    toArray()                                // ← aguarda todos completarem
  );
}

// ── Caso 2: NgRx Effect de notificações SignalR ──────────
// Cada notificação é processada independentemente
receiveNotification$ = createEffect(() =>
  this.hub.notification$.pipe(
    mergeMap(notification =>        // ← paralelo: cada notificação processa ao mesmo tempo
      this.api.markAsSeen(notification.id).pipe(
        map(() => NotificationsActions.received({ notification })),
        catchError(() => of(NotificationsActions.received({ notification })))
      )
    )
  )
);

// ── Caso 3: Deletar selecionados em paralelo ─────────────
deleteSelected(ids: string[]): Observable<void> {
  return from(ids).pipe(
    mergeMap(id => this.api.delete(id), 3), // ← no máximo 3 em paralelo (concurrency)
    toArray(),
    map(() => undefined)
  );
}
```

---

## `concatMap` — fila, ordem garantida

```typescript
import { concatMap } from 'rxjs/operators';

// ── Caso 1: Salvar itens de form em sequência ────────────
saveAll(items: Item[]): Observable<Item> {
  return from(items).pipe(
    concatMap(item => this.api.save(item))  // ← salva um por vez, na ordem
  );
}

// ── Caso 2: Ações que dependem da anterior ───────────────
// Criar usuário → criar perfil → enviar e-mail de boas-vindas
createUserFlow(dto: CreateUserDto): Observable<void> {
  return this.api.createUser(dto).pipe(
    concatMap(user => this.api.createProfile(user.id)),
    concatMap(profile => this.api.sendWelcomeEmail(profile.userId)),
    map(() => undefined)
  );
}

// ── Caso 3: NgRx Effect com ordem garantida ──────────────
// Útil quando a ordem das ações importa (ex: audit log)
logAction$ = createEffect(() =>
  this.actions$.pipe(
    ofType(AuditActions.log),
    concatMap(action =>             // ← garante que logs chegam ao servidor em ordem
      this.auditApi.log(action.entry).pipe(
        map(() => AuditActions.logSuccess()),
        catchError(() => of(AuditActions.logFailure()))
      )
    )
  )
);
```

---

## `exhaustMap` — ignora novos enquanto ocupado

```typescript
import { exhaustMap } from 'rxjs/operators';

// ── Caso 1: Submit de formulário — evita duplo clique ────
submitForm$ = createEffect(() =>
  this.actions$.pipe(
    ofType(UsersActions.create),
    exhaustMap(({ dto }) =>         // ← ignora cliques extras enquanto POST está em andamento
      this.api.create(dto).pipe(
        map(user => UsersActions.createSuccess({ user })),
        catchError(err => of(UsersActions.createFailure({ error: err.message })))
      )
    )
  )
);

// ── Caso 2: Refresh manual — ignora cliques rápidos ──────
refresh$ = createEffect(() =>
  this.actions$.pipe(
    ofType(DashboardActions.refresh),
    exhaustMap(() =>                // ← só inicia novo refresh quando o atual terminar
      this.api.getDashboard().pipe(
        map(data => DashboardActions.refreshSuccess({ data })),
        catchError(err => of(DashboardActions.refreshFailure({ error: err.message })))
      )
    )
  )
);
```

---

## Operadores de filtragem

```typescript
import {
  filter, debounceTime, throttleTime,
  distinctUntilChanged, take, first,
  skip, skipUntil, takeWhile, auditTime
} from 'rxjs/operators';

// filter — condicional
this.store.select(selectUser).pipe(
  filter(user => user !== null),   // ← só passa se user não é null
  map(user => user!)               // ← TypeScript sabe que não é null aqui
)

// debounceTime — aguarda parar de emitir (search, resize)
searchControl.valueChanges.pipe(
  debounceTime(300),               // ← aguarda 300ms de silêncio
  distinctUntilChanged()           // ← não re-dispara se valor não mudou
)

// throttleTime — limita frequência (scroll, mouse move)
fromEvent(window, 'scroll').pipe(
  throttleTime(100)               // ← no máximo 1x a cada 100ms
)

// auditTime — pega o último valor de uma janela de tempo
fromEvent(window, 'resize').pipe(
  auditTime(200)                  // ← pega o valor após 200ms de silêncio
)

// take — completa após N emissões
this.api.getData().pipe(
  take(1)                         // ← garante que o Observable completa após 1 emissão
)

// first — completa na primeira emissão que satisfaz condição
this.store.select(selectUser).pipe(
  first(user => user?.id === targetId)
)

// takeWhile — completa quando condição falha
interval(1000).pipe(
  takeWhile(() => this.isActive)  // ← para quando isActive = false
)

// skip — ignora as primeiras N emissões
someStream$.pipe(
  skip(1)                         // ← ignora o valor inicial do BehaviorSubject
)
```

---

## Operadores de transformação

```typescript
import { map, pluck, tap, scan, reduce, bufferTime, pairwise } from 'rxjs/operators';

// map — transformação síncrona (o mais usado)
this.store.select(selectUsers).pipe(
  map(users => users.filter(u => u.status === 'Active')),
  map(users => users.map(toUserViewModel))
)

// tap — efeito colateral sem modificar o valor (debugging, logging)
this.api.getUsers().pipe(
  tap(users => console.log('[DEBUG] users loaded:', users.length)),
  tap({ error: err => console.error('[ERROR]', err) })
)

// scan — acumula valores como um reduce, mas emite a cada passo
// Uso: lista de notificações que cresce
this.hub.notification$.pipe(
  scan((acc, notification) => [notification, ...acc].slice(0, 50), [] as Notification[])
)

// pairwise — emite [valorAnterior, valorAtual]
// Uso: detectar direção do scroll
fromEvent(window, 'scroll').pipe(
  map(() => window.scrollY),
  pairwise(),                     // ← [[prevY, currY], ...]
  map(([prev, curr]) => curr > prev ? 'down' : 'up')
)

// bufferTime — agrupa emissões por janela de tempo
// Uso: batch de eventos para enviar ao backend
this.analyticsEvents$.pipe(
  bufferTime(5000),               // ← agrupa eventos dos últimos 5s
  filter(events => events.length > 0),
  switchMap(events => this.api.sendBatch(events))
)
```
