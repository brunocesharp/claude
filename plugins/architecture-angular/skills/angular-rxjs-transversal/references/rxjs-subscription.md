# RxJS — Gerenciamento de Subscriptions

## Por que importa

Subscriptions não encerradas causam **memory leaks** — o componente é destruído mas o Observable continua executando, mantendo referências vivas e podendo disparar `setState` em componente destruído.

---

## `takeUntilDestroyed` — padrão Angular 16+ (preferido)

```typescript
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DestroyRef, inject } from '@angular/core';

// ── Em componente (inject context — construtor) ───────────
@Component({ standalone: true })
export class UserListComponent implements OnInit {
  private readonly store = inject(Store);

  // takeUntilDestroyed sem argumento: usa o DestroyRef do componente atual
  ngOnInit(): void {
    this.store.select(selectUsersAll).pipe(
      takeUntilDestroyed()          // ← cancela quando o componente é destruído
    ).subscribe(users => {
      // processamento local
    });
  }
}

// ── Fora do injection context (ngOnInit, ngAfterViewInit) ─
@Component({ standalone: true })
export class UserListComponent implements OnInit {
  private readonly destroyRef = inject(DestroyRef); // ← captura no construtor

  ngOnInit(): void {
    someObservable$.pipe(
      takeUntilDestroyed(this.destroyRef) // ← passa o DestroyRef explicitamente
    ).subscribe();
  }
}

// ── Em Service singleton — NÃO usar takeUntilDestroyed ───
// Services com providedIn: 'root' vivem para sempre — não destruídos
// Use takeUntil com Subject de shutdown ou deixe vivo (é o objetivo)
@Injectable({ providedIn: 'root' })
export class NotificationService {
  constructor(private hub: NotificationHub) {
    // Este stream deve viver enquanto o app viver — sem takeUntil
    this.hub.notification$.pipe(
      tap(n => this.processNotification(n))
    ).subscribe();
  }
}
```

---

## `async pipe` — melhor prática para templates

```typescript
// ✅ PREFERIDO — async pipe gerencia subscription automaticamente
@Component({
  standalone: true,
  imports: [AsyncPipe, CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <!-- async pipe: subscribe e unsubscribe automático -->
    @if (users$ | async; as users) {
      @for (user of users; track user.id) {
        <app-user-card [user]="user" />
      }
    }

    <!-- Multiple async pipes reutilizando o mesmo Observable -->
    @if (vm$ | async; as vm) {
      <h1>{{ vm.title }}</h1>
      <span>{{ vm.count }} itens</span>
    }
  `
})
export class UserListComponent {
  private readonly store = inject(Store);

  // Observable para o template — sem subscribe manual
  readonly users$ = this.store.select(selectUsersAll);

  // Combine em um único ViewModel para evitar múltiplos async pipes
  readonly vm$ = combineLatest({
    title:   of('Usuários'),
    count:   this.store.select(selectUsersTotalCount),
    loading: this.store.select(selectUsersLoading)
  });
}

// ❌ EVITAR — subscribe manual sem gerenciamento
@Component({})
export class BadComponent implements OnInit, OnDestroy {
  users: User[] = [];
  private sub!: Subscription;

  ngOnInit() {
    this.sub = this.store.select(selectUsersAll)
      .subscribe(users => this.users = users); // ← memory leak potencial
  }

  ngOnDestroy() { this.sub.unsubscribe(); }    // ← fácil de esquecer
}
```

---

## `toSignal` — integração Observable → Signal

```typescript
import { toSignal } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';

// ── Padrão base ──────────────────────────────────────────
@Component({ standalone: true, changeDetection: ChangeDetectionStrategy.OnPush })
export class UserListComponent {
  private readonly store = inject(Store);

  // toSignal gerencia a subscription automaticamente
  readonly users   = toSignal(this.store.select(selectUsersAll),    { initialValue: [] });
  readonly loading = toSignal(this.store.select(selectUsersLoading), { initialValue: false });
  readonly error   = toSignal(this.store.select(selectUsersError),   { initialValue: null });

  // Computed derivado de Signals (sem Observable)
  readonly hasUsers    = computed(() => this.users().length > 0);
  readonly activeUsers = computed(() => this.users().filter(u => u.status === 'Active'));
  readonly userCount   = computed(() => this.users().length);
}

// ── Com requireSync (quando o Observable SEMPRE tem valor inicial) ─
@Component({ standalone: true })
export class ConfigComponent {
  private readonly config = inject(ConfigService);

  // requireSync: não precisa de initialValue — o Observable já emitiu
  readonly config = toSignal(this.configService.config$, { requireSync: true });
}

// ── toSignal fora do construtor ─────────────────────────
@Component({ standalone: true })
export class MyComponent {
  private readonly injector = inject(Injector);

  someMethod(): void {
    // runInInjectionContext para chamar toSignal fora do construtor
    runInInjectionContext(this.injector, () => {
      const signal = toSignal(someObservable$);
    });
  }
}

// ── fromSignal — Signal → Observable ─────────────────────
import { toObservable } from '@angular/core/rxjs-interop';

@Component({ standalone: true })
export class SearchComponent {
  readonly searchTerm = signal('');

  // Converte Signal em Observable para usar operadores RxJS
  readonly results$ = toObservable(this.searchTerm).pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.api.search(term))
  );

  readonly results = toSignal(this.results$, { initialValue: [] });
}
```

---

## Padrão: múltiplas subscriptions com `Subscription` bag

```typescript
import { Subscription } from 'rxjs';

// Quando há muitas subscriptions manuais (legado ou casos específicos)
@Component({})
export class LegacyComponent implements OnInit, OnDestroy {
  private readonly subs = new Subscription(); // ← bag de subscriptions

  ngOnInit(): void {
    // Adiciona todas ao bag
    this.subs.add(
      stream1$.subscribe(v => this.handleV1(v))
    );
    this.subs.add(
      stream2$.subscribe(v => this.handleV2(v))
    );
    this.subs.add(
      stream3$.subscribe(v => this.handleV3(v))
    );
  }

  ngOnDestroy(): void {
    this.subs.unsubscribe(); // ← cancela todas de uma vez
  }
}
```

---

## Detectando memory leaks

```typescript
// Estratégia: adicionar tap de debug para verificar se o stream
// continua ativo após destruição do componente

someStream$.pipe(
  tap({
    next:      v    => console.log('[STREAM] next:', v),
    error:     err  => console.error('[STREAM] error:', err),
    complete:  ()   => console.log('[STREAM] completed ✅'),
    subscribe: ()   => console.log('[STREAM] subscribed'),
    finalize:  ()   => console.log('[STREAM] finalized ✅')
  }),
  takeUntilDestroyed()
).subscribe();

// Se "next" continuar aparecendo após destruir o componente = memory leak
```

---

## Anti-patterns a evitar

```typescript
// ❌ subscribe dentro de subscribe (use switchMap)
this.route.params.subscribe(params => {
  this.api.getUser(params['id']).subscribe(user => { // ← nested subscribe
    this.user = user;
  });
});

// ✅ switchMap
this.route.params.pipe(
  map(p => p['id']),
  switchMap(id => this.api.getUser(id)),
  takeUntilDestroyed()
).subscribe(user => this.user.set(user));

// ❌ subscribe em Effect (use map/tap)
someEffect$ = createEffect(() =>
  this.actions$.pipe(
    ofType(SomeActions.trigger),
    switchMap(() => {
      this.someService$.subscribe(v => doSomething(v)); // ← subscribe dentro de Effect
      return this.api.getData();
    })
  )
);

// ✅ withLatestFrom para pegar valor de Observable sem subscribe
someEffect$ = createEffect(() =>
  this.actions$.pipe(
    ofType(SomeActions.trigger),
    withLatestFrom(this.someService.value$),
    switchMap(([action, value]) => {
      doSomething(value);
      return this.api.getData();
    })
  )
);

// ❌ take(1) em BehaviorSubject para "leitura única" (use .value)
this.authService.user$.pipe(take(1)).subscribe(user => { ... });

// ✅ leitura síncrona via .value
const user = this.authService.currentUser; // getter que retorna _user$.value
```
