# RxJS — Tratamento de Erros

## Regra fundamental

> **Um erro não tratado em um Observable encerra o stream permanentemente.**
> Use `catchError` para recuperar e manter o stream vivo.

---

## `catchError` — captura e recupera

```typescript
import { catchError, throwError, of, EMPTY } from 'rxjs';

// ── Padrão 1: Retornar valor default ─────────────────────
this.api.getUsers().pipe(
  catchError(() => of([]))          // ← em caso de erro, retorna lista vazia
)

// ── Padrão 2: Re-propagar com contexto ───────────────────
this.api.getUser(id).pipe(
  catchError(err => throwError(() => ({
    ...err,
    context: `Falha ao carregar usuário ${id}`,
    timestamp: new Date()
  })))
)

// ── Padrão 3: Cancelar silenciosamente ───────────────────
this.api.getOptionalData().pipe(
  catchError(() => EMPTY)           // ← ignora o erro, stream completa
)

// ── Padrão 4: Lógica condicional por tipo de erro ────────
this.api.getData().pipe(
  catchError((err: HttpErrorResponse) => {
    switch (err.status) {
      case 404: return of(null);                        // recurso não existe — ok
      case 401: this.router.navigate(['/login']);        // não autenticado — redireciona
               return EMPTY;
      case 503: return throwError(() => err);           // servidor down — propaga
      default:  return throwError(() => err);
    }
  })
)

// ── Padrão 5: Em NgRx Effect — CRÍTICO ──────────────────
// O catchError DEVE ficar DENTRO do switchMap/mergeMap
// Se ficar fora, o Effect morre após o primeiro erro

// ❌ ERRADO — catchError fora do operador de mapping
loadUsers$ = createEffect(() =>
  this.actions$.pipe(
    ofType(UsersActions.loadAll),
    switchMap(() => this.api.getAll()),
    map(users => UsersActions.loadAllSuccess({ users })),
    catchError(err => of(UsersActions.loadAllFailure({ error: err.message })))
    // ↑ Quando erro ocorre, o Effect para de funcionar para sempre
  )
);

// ✅ CORRETO — catchError dentro do switchMap
loadUsers$ = createEffect(() =>
  this.actions$.pipe(
    ofType(UsersActions.loadAll),
    switchMap(() =>
      this.api.getAll().pipe(                           // ← pipe interno
        map(users => UsersActions.loadAllSuccess({ users })),
        catchError(err => of(UsersActions.loadAllFailure({ error: err.message })))
        // ↑ Erro tratado aqui: o stream do switchMap continua funcionando
      )
    )
  )
);
```

---

## `retry` e `retryWhen` — nova tentativa automática

```typescript
import { retry, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';

// ── retry simples ─────────────────────────────────────────
this.api.getData().pipe(
  retry(3)                    // ← retenta 3x imediatamente
)

// ── retry com delay fixo ──────────────────────────────────
this.api.getData().pipe(
  retry({
    count: 3,
    delay: 1000              // ← aguarda 1s entre tentativas
  })
)

// ── retry com backoff exponencial ────────────────────────
// 1ª tentativa: 1s, 2ª: 2s, 3ª: 4s, 4ª: 8s
this.api.getData().pipe(
  retry({
    count: 4,
    delay: (error, retryCount) => {
      // Só retenta em erros de rede ou servidor
      if (error instanceof HttpErrorResponse && error.status < 500 && error.status !== 0) {
        throw error;            // ← não retenta em 4xx
      }
      const delayMs = Math.pow(2, retryCount - 1) * 1000;
      console.log(`[Retry] tentativa ${retryCount}, aguardando ${delayMs}ms`);
      return timer(delayMs);
    }
  }),
  catchError(err => {
    console.error('[Final] Todas as tentativas esgotadas:', err);
    return throwError(() => err);
  })
)

// ── retry em Interceptor ──────────────────────────────────
export const retryInterceptor: HttpInterceptorFn = (req, next) => {
  // Não retenta mutações
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
    return next(req);
  }

  return next(req).pipe(
    retry({
      count: 2,
      delay: (err: HttpErrorResponse, count) => {
        if (err.status >= 400 && err.status < 500) throw err; // não retenta 4xx
        return timer(count * 1000);
      }
    })
  );
};
```

---

## `finalize` — executa sempre (sucesso ou erro)

```typescript
import { finalize } from 'rxjs/operators';

// Uso típico: esconder loading independente do resultado
@Injectable({ providedIn: 'root' })
export class LoadingService {
  private count = 0;
  private readonly _loading$ = new BehaviorSubject(false);
  readonly loading$ = this._loading$.asObservable();

  wrap<T>(source$: Observable<T>): Observable<T> {
    return new Observable(observer => {
      this.count++;
      this._loading$.next(true);

      return source$.pipe(
        finalize(() => {            // ← executa em complete() E em error()
          this.count--;
          if (this.count === 0) this._loading$.next(false);
        })
      ).subscribe(observer);
    });
  }
}

// Em interceptor de loading
export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loading = inject(LoadingService);
  loading.show();

  return next(req).pipe(
    finalize(() => loading.hide()) // ← esconde loader em qualquer caso
  );
};
```

---

## Erros em streams longos (SignalR, polling)

```typescript
// ── Problema: erro em stream de longa duração mata tudo ──

// ❌ ERRADO — qualquer erro do SignalR encerra o stream
this.hub.notification$.pipe(
  map(n => processNotification(n))  // ← se lançar erro, stream para
).subscribe(...)

// ✅ CORRETO — isola erro por emissão, stream continua
this.hub.notification$.pipe(
  switchMap(n =>
    of(n).pipe(
      map(n => processNotification(n)),
      catchError(err => {
        console.error('[Notification error]', err);
        return EMPTY;             // ← descarta esta emissão com erro
      })
    )
  )
).subscribe(...)

// ── Polling com reconexão automática ─────────────────────
const polling$ = interval(30_000).pipe(
  switchMap(() =>
    this.api.getStatus().pipe(
      catchError(err => {
        console.warn('[Polling] Falha temporária:', err.message);
        return of(null);          // ← retorna null, polling continua
      })
    )
  ),
  filter(Boolean),
  takeUntilDestroyed()
);
```

---

## Padrão: `onErrorResumeNext` e `iif`

```typescript
import { iif, onErrorResumeNext, of } from 'rxjs';

// iif — Observable condicional (lazy evaluation)
const data$ = iif(
  () => this.auth.isAuthenticated(),  // ← condição avaliada na subscrição
  this.api.getPrivateData(),           // ← Observable se true
  of(publicDefaultData)               // ← Observable se false
);

// onErrorResumeNext — continua com próximo Observable mesmo em erro
// Útil para fallback em sequências
onErrorResumeNext(
  this.api.getPrimary(),    // ← tenta primeiro
  this.api.getSecondary(),  // ← se erro, tenta este
  of(defaultData)           // ← se tudo falhar, usa default
).subscribe(data => console.log('Conseguiu de algum lugar:', data));
```

---

## Notificação de erros ao usuário

```typescript
// Padrão: tap no erro + catchError para UI
@Injectable({ providedIn: 'root' })
export class UserApiService extends BaseApiService {
  private readonly notification = inject(NotificationService);

  create(dto: CreateUserDto): Observable<User> {
    return this.post<User>('users', dto).pipe(
      tap({ error: (err: HttpErrorResponse) => {
        // Notifica o usuário de erros de validação (422)
        if (err.status === 422 && err.error?.errors) {
          const messages = Object.values(err.error.errors).flat() as string[];
          messages.forEach(msg => this.notification.error(msg));
        }
      }}),
      // Deixa o erro propagar para o Effect tratar
    );
  }
}
```
