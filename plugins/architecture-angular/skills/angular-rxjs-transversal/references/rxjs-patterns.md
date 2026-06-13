# RxJS — Padrões por Camada Angular

## Core / Services — Estado reativo com BehaviorSubject

```typescript
// src/app/core/services/theme.service.ts
import { Injectable, signal, computed } from '@angular/core';
import { BehaviorSubject, distinctUntilChanged, map } from 'rxjs';

type Theme = 'light' | 'dark' | 'system';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly _theme$ = new BehaviorSubject<Theme>(
    (localStorage.getItem('theme') as Theme) ?? 'system'
  );

  // Observable público — para quem precisa de stream
  readonly theme$        = this._theme$.asObservable();
  readonly isDark$       = this._theme$.pipe(
    map(t => t === 'dark' || (t === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)),
    distinctUntilChanged()
  );

  // Getter síncrono — para leitura pontual
  get currentTheme(): Theme { return this._theme$.value; }

  setTheme(theme: Theme): void {
    this._theme$.next(theme);
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
  }
}
```

---

## Core / HTTP — Fluxos de requisição

```typescript
// src/app/core/http/user-api.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {
  Observable, throwError, timer
} from 'rxjs';
import {
  map, catchError, retry, timeout,
  shareReplay, tap
} from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class UserApiService {
  private readonly http = inject(HttpClient);

  // shareReplay(1): se múltiplos componentes assinarem, só 1 request
  private readonly roles$: Observable<Role[]> = this.http
    .get<Role[]>('/api/roles')
    .pipe(shareReplay(1));         // ← cacheia, não refaz o request

  getAll(params: Record<string, string> = {}): Observable<PagedResult<User>> {
    return this.http.get<PagedResult<User>>('/api/users', { params }).pipe(
      timeout(10_000),             // ← erro se não responder em 10s
      retry({                      // ← retenta 2x com backoff
        count: 2,
        delay: (_, i) => timer(i * 1000)
      }),
      map(result => ({
        ...result,
        items: result.items.map(toUserViewModel)
      })),
      catchError(err => throwError(() => err))
    );
  }

  getRoles(): Observable<Role[]> {
    return this.roles$;            // ← retorna o Observable cacheado
  }
}
```

---

## Core / Interceptors — Middleware de Observables

```typescript
// src/app/core/interceptors/auth.interceptor.ts
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, take, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth  = inject(AuthService);
  const token = localStorage.getItem('token');

  const authReq = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(authReq).pipe(
    catchError((err: HttpErrorResponse) => {
      // Token expirado: tenta refresh e retenta a requisição original
      if (err.status === 401 && !req.url.includes('/auth')) {
        return auth.refreshToken().pipe(
          take(1),
          switchMap(newToken => {
            const retried = req.clone({
              setHeaders: { Authorization: `Bearer ${newToken}` }
            });
            return next(retried);
          }),
          catchError(() => {
            auth.logout();
            return throwError(() => err);
          })
        );
      }
      return throwError(() => err);
    })
  );
};
```

---

## Core / Hubs (SignalR) — Eventos em tempo real

```typescript
// src/app/core/hubs/notification.hub.ts
import { Injectable, inject } from '@angular/core';
import { Subject, Observable, share, retry, timer } from 'rxjs';
import { BaseHubService } from './base-hub.service';

@Injectable({ providedIn: 'root' })
export class NotificationHub extends BaseHubService {
  private readonly _events$ = new Subject<HubEvent>();

  // share(): multicast sem replay — múltiplos subscribers, 1 conexão
  readonly events$: Observable<HubEvent> = this._events$.pipe(
    share()
  );

  // Streams filtradas por tipo de evento
  readonly notification$ = this.events$.pipe(
    filter((e): e is NotificationEvent => e.type === 'Notification')
  );

  readonly userOnline$ = this.events$.pipe(
    filter((e): e is UserOnlineEvent => e.type === 'UserOnline')
  );

  private registerHandlers(): void {
    this.connection.on('HubEvent', (event: HubEvent) => {
      this._events$.next(event);
    });
  }
}
```

---

## Feature / NgRx Effects — Side-effects completos

```typescript
// src/app/features/users/store/users.effects.ts
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import {
  switchMap, mergeMap, exhaustMap, concatMap,
  map, catchError, withLatestFrom, tap, filter
} from 'rxjs/operators';
import { of, from } from 'rxjs';

@Injectable()
export class UsersEffects {
  private readonly actions$ = inject(Actions);
  private readonly store    = inject(Store);
  private readonly api      = inject(UserApiService);
  private readonly router   = inject(Router);
  private readonly hub      = inject(NotificationHub);

  // switchMap — cancelamento: nova busca cancela a anterior
  search$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.search),
      switchMap(({ term }) =>
        this.api.search(term).pipe(
          map(users => UsersActions.searchSuccess({ users })),
          catchError(err => of(UsersActions.searchFailure({ error: err.message })))
        )
      )
    )
  );

  // exhaustMap — submit: ignora cliques extras enquanto salva
  create$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.create),
      exhaustMap(({ dto }) =>
        this.api.create(dto).pipe(
          map(user => UsersActions.createSuccess({ user })),
          catchError(err => of(UsersActions.createFailure({ error: err.message })))
        )
      )
    )
  );

  // concatMap — audit log: garante ordem dos logs
  auditLog$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.createSuccess, UsersActions.updateSuccess, UsersActions.removeSuccess),
      concatMap(action =>
        this.api.log({ action: action.type, timestamp: new Date() }).pipe(
          map(() => AuditActions.logged()),
          catchError(() => of(AuditActions.logFailed()))
        )
      )
    )
  );

  // withLatestFrom — contexto do estado sem re-disparar
  loadWithContext$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.loadAll),
      withLatestFrom(
        this.store.select(selectUsersFilters),
        this.store.select(selectCurrentUser)
      ),
      switchMap(([, filters, currentUser]) =>
        this.api.getAll({ ...filters, tenantId: currentUser!.tenantId }).pipe(
          map(result => UsersActions.loadAllSuccess({
            users: result.items,
            totalCount: result.totalCount
          })),
          catchError(err => of(UsersActions.loadAllFailure({ error: err.message })))
        )
      )
    )
  );

  // SignalR → Store: sem dispatch de Action intermediária
  syncFromHub$ = createEffect(() =>
    this.hub.notification$.pipe(
      filter(e => e.entityType === 'User'),
      mergeMap(event =>
        this.api.getById(event.entityId).pipe(
          map(user => UsersActions.syncedFromHub({ user })),
          catchError(() => of(UsersActions.syncFailed()))
        )
      )
    )
  );

  // Navegação — sem dispatch (dispatch: false)
  navigateAfterCreate$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.createSuccess),
      tap(({ user }) => this.router.navigate(['/users', user.id]))
    ),
    { dispatch: false }
  );
}
```

---

## Feature / Forms — Reactive Forms com RxJS

```typescript
// src/app/features/users/components/user-search/user-search.component.ts
import {
  Component, inject, ChangeDetectionStrategy, OnInit
} from '@angular/core';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { Store } from '@ngrx/store';
import { toSignal } from '@angular/core/rxjs-interop';
import {
  debounceTime, distinctUntilChanged, filter,
  switchMap, startWith, catchError
} from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ReactiveFormsModule],
  template: `
    <input [formControl]="searchControl" placeholder="Buscar..." />
    <div>{{ results().length }} resultados</div>
  `
})
export class UserSearchComponent {
  private readonly fb  = inject(FormBuilder);
  private readonly api = inject(UserApiService);

  readonly searchControl = this.fb.nonNullable.control('');

  // Pipeline completo: input → debounce → HTTP → Signal
  readonly results = toSignal(
    this.searchControl.valueChanges.pipe(
      startWith(''),                    // ← emite imediatamente com valor atual
      debounceTime(300),                // ← aguarda parar de digitar
      distinctUntilChanged(),           // ← só se mudou
      filter(term => term.length >= 2 || term.length === 0),
      switchMap(term =>                 // ← cancela request anterior
        term
          ? this.api.search(term).pipe(catchError(() => of([])))
          : of([])
      )
    ),
    { initialValue: [] }
  );
}
```

---

## Shared / Directives — Eventos DOM com RxJS

```typescript
// src/app/shared/directives/intersection.directive.ts
import {
  Directive, ElementRef, output, input,
  OnInit, OnDestroy, inject
} from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil, filter } from 'rxjs/operators';

@Directive({ selector: '[appVisible]', standalone: true })
export class VisibilityDirective implements OnInit, OnDestroy {
  private readonly el      = inject(ElementRef<HTMLElement>);
  private readonly destroy = new Subject<void>();

  readonly threshold  = input<number>(0.5);
  readonly visible    = output<boolean>();

  ngOnInit(): void {
    new Observable<boolean>(observer => {
      const obs = new IntersectionObserver(
        ([entry]) => observer.next(entry.isIntersecting),
        { threshold: this.threshold() }
      );
      obs.observe(this.el.nativeElement);
      return () => obs.disconnect();
    }).pipe(
      distinctUntilChanged(),
      takeUntil(this.destroy)
    ).subscribe(isVisible => this.visible.emit(isVisible));
  }

  ngOnDestroy(): void {
    this.destroy.next();
    this.destroy.complete();
  }
}
```
