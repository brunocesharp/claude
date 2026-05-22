# RxJS — Combinação de Streams

## Guia de escolha rápida

```
Quero emitir quando QUALQUER stream emite (todos precisam ter emitido ao menos 1x):
  → combineLatest

Quero esperar TODOS completarem e pegar o último valor de cada:
  → forkJoin  (ideal para requisições HTTP paralelas)

Quero o valor mais recente de outro stream SEM re-disparar:
  → withLatestFrom

Quero combinar por ÍNDICE (1º com 1º, 2º com 2º):
  → zip

Quero pegar apenas o PRIMEIRO que emitir:
  → race
```

---

## `combineLatest` — reage quando qualquer stream emite

```typescript
import { combineLatest } from 'rxjs';
import { map, distinctUntilChanged } from 'rxjs/operators';

// ── Caso 1: Estado derivado em Service ───────────────────
@Injectable({ providedIn: 'root' })
export class OrderService {
  private readonly _orders$   = new BehaviorSubject<Order[]>([]);
  private readonly _filter$   = new BehaviorSubject<OrderFilter>({ status: 'all' });
  private readonly _search$   = new BehaviorSubject<string>('');

  // Recomputa sempre que orders, filter ou search muda
  readonly filteredOrders$ = combineLatest({
    orders: this._orders$,
    filter: this._filter$,
    search: this._search$.pipe(debounceTime(300), distinctUntilChanged())
  }).pipe(
    map(({ orders, filter, search }) => {
      let result = orders;
      if (filter.status !== 'all') {
        result = result.filter(o => o.status === filter.status);
      }
      if (search) {
        const term = search.toLowerCase();
        result = result.filter(o =>
          o.customerName.toLowerCase().includes(term) ||
          o.id.includes(term)
        );
      }
      return result;
    }),
    shareReplay(1)
  );

  setFilter(filter: OrderFilter): void { this._filter$.next(filter); }
  setSearch(term: string): void        { this._search$.next(term); }
}

// ── Caso 2: NgRx Selector combinado ─────────────────────
export const selectDashboardVm = createSelector(
  selectUsersAll,
  selectOrdersAll,
  selectProductsAll,
  (users, orders, products) => ({
    totalUsers:    users.length,
    activeOrders:  orders.filter(o => o.status === 'active').length,
    lowStockCount: products.filter(p => p.stock < 10).length
  })
);

// ── Caso 3: Combinar 2 streams reativos em componente ───
@Component({ standalone: true, changeDetection: ChangeDetectionStrategy.OnPush })
export class DashboardComponent {
  private readonly store = inject(Store);

  // Dois selectors combinados
  readonly vm$ = combineLatest({
    users:  this.store.select(selectUsersAll),
    orders: this.store.select(selectOrdersAll)
  }).pipe(
    map(({ users, orders }) => ({
      totalUsers:  users.length,
      totalOrders: orders.length,
      ratio:       orders.length / Math.max(users.length, 1)
    }))
  );

  readonly vm = toSignal(this.vm$, { initialValue: null });
}
```

---

## `forkJoin` — requisições paralelas, aguarda todas

```typescript
import { forkJoin, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

// ── Caso 1: Carregar múltiplos recursos em paralelo ──────
@Injectable({ providedIn: 'root' })
export class DashboardApiService extends BaseApiService {
  // Dispara 3 requisições ao mesmo tempo, aguarda todas
  getDashboardData(): Observable<DashboardData> {
    return forkJoin({
      kpis:         this.get<KpiData[]>('dashboard/kpis'),
      chartData:    this.get<ChartPoint[]>('dashboard/charts'),
      recentOrders: this.get<Order[]>('dashboard/recent-orders')
    }).pipe(
      map(({ kpis, chartData, recentOrders }) => ({
        kpis,
        chartData,
        recentOrders,
        generatedAt: new Date()
      }))
    );
  }
}

// ── Caso 2: NgRx Effect com forkJoin ────────────────────
loadDashboard$ = createEffect(() =>
  this.actions$.pipe(
    ofType(DashboardActions.load),
    switchMap(() =>
      forkJoin({              // ← paralelo e aguarda todos
        summary: this.api.getSummary(),
        alerts:  this.api.getAlerts()
      }).pipe(
        map(data => DashboardActions.loadSuccess(data)),
        catchError(err => of(DashboardActions.loadFailure({ error: err.message })))
      )
    )
  )
);

// ── Caso 3: Deletar múltiplos itens aguardando todos ─────
deleteMany(ids: string[]): Observable<void> {
  if (ids.length === 0) return of(undefined);

  return forkJoin(
    ids.map(id => this.api.delete(id))  // ← array de Observables
  ).pipe(map(() => undefined));
}
```

---

## `withLatestFrom` — valor snapshot sem re-disparar

```typescript
import { withLatestFrom } from 'rxjs/operators';

// ── Caso 1: NgRx Effect com contexto do estado ───────────
// Precisa dos filtros atuais mas não quer re-disparar quando eles mudam
loadWithFilters$ = createEffect(() =>
  this.actions$.pipe(
    ofType(UsersActions.loadAll, UsersActions.applyFilters),
    withLatestFrom(
      this.store.select(selectUsersFilters),   // ← valor atual dos filtros
      this.store.select(selectUsersPagination) // ← valor atual da paginação
    ),
    switchMap(([, filters, pagination]) =>
      this.api.getAll(pagination.page, pagination.size, filters).pipe(
        map(result => UsersActions.loadAllSuccess({
          users: result.items,
          totalCount: result.totalCount
        })),
        catchError(err => of(UsersActions.loadAllFailure({ error: err.message })))
      )
    )
  )
);

// ── Caso 2: Ação de UI com contexto do usuário logado ────
saveAction$ = createEffect(() =>
  this.actions$.pipe(
    ofType(DocumentActions.save),
    withLatestFrom(this.store.select(selectCurrentUser)),
    switchMap(([{ document }, user]) =>
      this.api.save({ ...document, lastModifiedBy: user!.id }).pipe(
        map(saved => DocumentActions.saveSuccess({ document: saved })),
        catchError(err => of(DocumentActions.saveFailure({ error: err.message })))
      )
    )
  )
);

// ── Caso 3: Submit de form com estado da Store ───────────
@Component({ standalone: true })
export class OrderFormComponent {
  private readonly store = inject(Store);

  onSubmit(formValue: OrderFormValue): void {
    // withLatestFrom em componente — usar take(1)
    this.store.select(selectCurrentCustomer).pipe(
      take(1),
      withLatestFrom(this.store.select(selectCartItems))
    ).subscribe(([customer, items]) => {
      this.store.dispatch(OrderActions.create({
        dto: { ...formValue, customerId: customer!.id, items }
      }));
    });
  }
}
```

---

## `zip` — combina por índice (sincronização)

```typescript
import { zip } from 'rxjs';

// Uso: sincronizar streams que emitem no mesmo ritmo
// Ex: lista de IDs + detalhes de cada ID em paralelo

const ids$    = from(['id1', 'id2', 'id3']);
const labels$ = from(['Label 1', 'Label 2', 'Label 3']);

zip(ids$, labels$).pipe(
  map(([id, label]) => ({ id, label }))
);
// Emite: {id:'id1', label:'Label 1'}, {id:'id2', label:'Label 2'}, ...
```

---

## `startWith` — garante valor inicial para combineLatest

```typescript
import { startWith } from 'rxjs/operators';

// Problema: combineLatest não emite até TODOS emitirem
// Solução: startWith garante emissão inicial

const filter$ = this.filterControl.valueChanges.pipe(
  startWith(this.filterControl.value)  // ← emite valor inicial do form
);

const search$ = this.searchControl.valueChanges.pipe(
  debounceTime(300),
  startWith('')                        // ← começa com string vazia
);

// Agora combineLatest emite imediatamente
combineLatest({ filter: filter$, search: search$ }).pipe(
  switchMap(({ filter, search }) => this.api.getAll(filter, search))
)
```

---

## `merge` — mescla múltiplos streams

```typescript
import { merge } from 'rxjs';

// Uso: múltiplas fontes de atualização para o mesmo dado
@Injectable({ providedIn: 'root' })
export class UserSyncService {
  // Atualiza usuário por 3 fontes diferentes
  readonly userUpdates$ = merge(
    this.hub.userUpdated$,          // ← SignalR em tempo real
    this.actions$.pipe(             // ← ação do próprio app
      ofType(UsersActions.updateSuccess),
      map(({ user }) => user)
    ),
    this.authService.user$.pipe(    // ← mudança de perfil
      filter(Boolean),
      distinctUntilChanged((a, b) => a.id === b.id)
    )
  );
}
```

---

## `race` — o primeiro a emitir vence

```typescript
import { race, timer } from 'rxjs';
import { map } from 'rxjs/operators';

// Timeout manual: o que vier primeiro — resposta ou timeout
function withTimeout<T>(source$: Observable<T>, ms: number): Observable<T> {
  return race(
    source$,
    timer(ms).pipe(
      map(() => { throw new Error(`Timeout após ${ms}ms`); })
    )
  );
}

// Uso
withTimeout(this.api.getSlow(), 5000).pipe(
  catchError(err => {
    if (err.message.includes('Timeout')) {
      return of(fallbackData);
    }
    return throwError(() => err);
  })
)
```
