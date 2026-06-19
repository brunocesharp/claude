# RxJS ↔ Signals — Interoperabilidade Angular 17+

## Visão geral

| | Signals | Observables |
|---|---|---|
| **Natureza** | Valor síncrono reativo | Stream assíncrono |
| **Leitura** | `signal()` — síncrona | `subscribe()` — assíncrona |
| **Template** | Direto — sem `async pipe` | Precisa `async pipe` ou `toSignal` |
| **Derivação** | `computed()` | `map`, `combineLatest` |
| **Side-effect** | `effect()` | `tap`, `subscribe` |
| **Melhor para** | Estado local/UI, computeds simples | HTTP, SignalR, NgRx, streams complexos |

---

## `toSignal` — Observable → Signal

```typescript
import { toSignal } from '@angular/core/rxjs-interop';
import { computed, inject } from '@angular/core';
import { Store } from '@ngrx/store';

@Component({
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <!-- Signals: sem async pipe, sem null check -->
    <div>Total: {{ userCount() }}</div>
    <div>Ativos: {{ activeCount() }}</div>

    @if (loading()) { <app-spinner /> }

    @for (user of filteredUsers(); track user.id) {
      <app-user-card [user]="user" />
    }
  `
})
export class UserListComponent {
  private readonly store = inject(Store);

  // NgRx Selectors → Signals
  readonly users   = toSignal(this.store.select(selectUsersAll),    { initialValue: [] as User[] });
  readonly loading = toSignal(this.store.select(selectUsersLoading), { initialValue: false });
  readonly error   = toSignal(this.store.select(selectUsersError),   { initialValue: null });

  // Computeds derivados de Signals — sem Observable
  readonly userCount    = computed(() => this.users().length);
  readonly activeCount  = computed(() => this.users().filter(u => u.status === 'Active').length);
  readonly filteredUsers = computed(() =>
    this.users().filter(u => !this.loading() && u.status !== 'Deleted')
  );

  // Signal de estado local da UI
  readonly searchTerm   = signal('');
  readonly selectedId   = signal<string | null>(null);

  // Computed que combina Store + estado local
  readonly searchResults = computed(() => {
    const term  = this.searchTerm().toLowerCase();
    const users = this.users();
    return term ? users.filter(u => u.name.toLowerCase().includes(term)) : users;
  });
}
```

---

## `toObservable` — Signal → Observable

```typescript
import { toObservable } from '@angular/core/rxjs-interop';
import { signal, inject } from '@angular/core';

@Component({ standalone: true, changeDetection: ChangeDetectionStrategy.OnPush })
export class SearchComponent {
  private readonly api = inject(UserApiService);

  // Signal controlado pelo usuário
  readonly searchTerm = signal('');

  // Signal → Observable para usar operadores RxJS complexos
  readonly results = toSignal(
    toObservable(this.searchTerm).pipe(   // ← Signal vira Observable
      debounceTime(300),
      distinctUntilChanged(),
      filter(t => t.length >= 2 || t.length === 0),
      switchMap(term =>
        term
          ? this.api.search(term).pipe(catchError(() => of([])))
          : of([])
      )
    ),
    { initialValue: [] as User[] }
  );

  onInput(event: Event): void {
    this.searchTerm.set((event.target as HTMLInputElement).value);
  }
}
```

---

## `effect` com Observables

```typescript
import { effect, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({ standalone: true })
export class ThemeAwareComponent {
  private readonly theme = inject(ThemeService);
  private readonly store = inject(Store);

  readonly isDark = toSignal(this.theme.isDark$, { initialValue: false });

  constructor() {
    // effect: executa quando Signal muda — ideal para side-effects
    effect(() => {
      const dark = this.isDark();
      document.documentElement.classList.toggle('dark', dark);
      // Não usar effect para mudar outros Signals — use computed
    });

    // effect com cleanup (para subscriptions manuais dentro de effect)
    effect(onCleanup => {
      const sub = this.theme.events$.subscribe(event => {
        console.log('Theme event:', event);
      });
      onCleanup(() => sub.unsubscribe()); // ← cleanup quando effect re-executa
    });
  }
}
```

---

## Padrão híbrido: Store NgRx + Signals locais

```typescript
// O padrão mais comum no Angular 17+ com NgRx
@Component({
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <!-- Estado global (Store) via toSignal -->
    @for (user of users(); track user.id) {
      <app-user-card
        [user]="user"
        [isSelected]="selectedId() === user.id"
        (select)="onSelect($event)"
        (delete)="onDelete($event)"
      />
    }

    <!-- Estado de UI local via signal() -->
    @if (showFilters()) {
      <app-user-filters (filterChange)="applyFilter($event)" />
    }

    <button (click)="showFilters.update(v => !v)">
      {{ showFilters() ? 'Ocultar' : 'Mostrar' }} filtros
    </button>
  `
})
export class UserListComponent implements OnInit {
  private readonly store = inject(Store);

  // ── Estado global (NgRx → Signal) ────────────────────
  readonly users   = toSignal(this.store.select(selectFilteredUsers), { initialValue: [] });
  readonly loading = toSignal(this.store.select(selectUsersLoading),  { initialValue: false });

  // ── Estado local de UI (Signal puro) ─────────────────
  readonly showFilters = signal(false);
  readonly selectedId  = signal<string | null>(null);

  // ── Estado derivado (computed) ────────────────────────
  readonly selectedUser = computed(() =>
    this.users().find(u => u.id === this.selectedId()) ?? null
  );
  readonly hasSelection = computed(() => this.selectedId() !== null);

  ngOnInit(): void {
    this.store.dispatch(UsersActions.loadAll());
  }

  onSelect(user: User): void {
    // Estado local → Signal
    this.selectedId.set(user.id);
    // Estado global → Store
    this.store.dispatch(UsersActions.select({ userId: user.id }));
  }

  onDelete(user: User): void {
    this.store.dispatch(UsersActions.remove({ userId: user.id }));
  }

  applyFilter(filters: Record<string, string>): void {
    this.store.dispatch(UsersActions.applyFilters({ filters }));
  }
}
```

---

## Quando usar Signal vs Observable

```typescript
// ✅ USE SIGNAL para:
const count         = signal(0);                    // estado local simples
const isOpen        = signal(false);                // toggle de UI
const selectedTab   = signal<'list' | 'grid'>('list'); // enum local
const formDirty     = signal(false);                // estado de formulário
const activeCount   = computed(() => users().filter(u => u.active).length); // derivado

// ✅ USE OBSERVABLE para:
const users$        = this.http.get<User[]>('/api/users'); // HTTP
const notification$ = this.hub.events$;              // SignalR
const filtered$     = this.store.select(selectFiltered); // NgRx
const search$       = input$.pipe(debounceTime(300)); // transformação complexa
const combined$     = combineLatest([a$, b$, c$]);   // múltiplas fontes

// ✅ USE toSignal para CONSUMIR Observable no template sem async pipe
readonly users = toSignal(this.users$, { initialValue: [] });

// ✅ USE async pipe quando o Observable vem de @Input ou não está no constructor
@Component({ template: `{{ data$ | async }}` })
export class MyComponent {
  @Input() data$!: Observable<Data>;  // ← toSignal não pode ser usado aqui facilmente
}

// ✅ USE toObservable quando precisar de operadores RxJS em cima de Signal
readonly filtered$ = toObservable(this.searchSignal).pipe(
  debounceTime(300),
  switchMap(term => this.api.search(term))
);
```

---

## Signals no NgRx (NgRx Signals Store — futuro)

```typescript
// NgRx Signal Store (ngx-signal-store / @ngrx/signals)
import { signalStore, withState, withMethods, withComputed } from '@ngrx/signals';

export const UsersStore = signalStore(
  withState<UsersState>(initialUsersState),

  withComputed(({ users, loading }) => ({
    activeUsers:  computed(() => users().filter(u => u.active)),
    hasUsers:     computed(() => users().length > 0),
    isIdle:       computed(() => !loading())
  })),

  withMethods((store, api = inject(UserApiService)) => ({
    async loadAll(): Promise<void> {
      patchState(store, { loading: true });
      try {
        const users = await firstValueFrom(api.getAll());
        patchState(store, { users, loading: false });
      } catch (err) {
        patchState(store, { error: String(err), loading: false });
      }
    }
  }))
);

// Uso no componente
@Component({ providers: [UsersStore] })
export class UsersComponent {
  private readonly store = inject(UsersStore);

  readonly users       = this.store.users;       // Signal<User[]>
  readonly activeUsers = this.store.activeUsers; // computed Signal
  readonly loading     = this.store.loading;     // Signal<boolean>
}
```
