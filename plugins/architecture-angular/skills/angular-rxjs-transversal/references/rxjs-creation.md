# RxJS — Criação de Streams

## Fontes fundamentais

### `of` — emite valores síncronos e completa
```typescript
import { of } from 'rxjs';

// Emite 1, 2, 3 e completa
const numbers$ = of(1, 2, 3);

// Uso comum: fallback em catchError
catchError(() => of(defaultValue))

// Uso comum: wrap valor em Observable
of(user).pipe(map(u => u.name))
```

### `from` — converte Promise, Array, Iterable em Observable
```typescript
import { from } from 'rxjs';

// De Promise (ex: fetch API, SignalR invoke)
const user$ = from(fetch('/api/user').then(r => r.json()));

// De Array (emite cada item e completa)
const items$ = from([1, 2, 3]);

// De Promise do SignalR
const result$ = from(this.connection.invoke('GetData', params));
```

### `EMPTY` — completa imediatamente sem emitir
```typescript
import { EMPTY } from 'rxjs';

// Uso: cancelar um flow sem propagar erro
catchError(err => {
  if (err.status === 404) return EMPTY; // cancela silenciosamente
  return throwError(() => err);
})

// Uso: Resolver que redireciona
export const userResolver: ResolveFn<User> = (route) => {
  return api.getById(route.paramMap.get('id')!).pipe(
    catchError(() => {
      router.navigate(['/not-found']);
      return EMPTY; // cancela a navegação
    })
  );
};
```

### `throwError` — cria Observable que falha imediatamente
```typescript
import { throwError } from 'rxjs';

// Propagar erro com contexto adicional
catchError(err => throwError(() => new Error(`Falha ao carregar: ${err.message}`)))

// Em interceptor
catchError((err: HttpErrorResponse) => {
  logError(err);
  return throwError(() => err); // re-propaga para o caller
})
```

### `interval` e `timer` — streams temporais
```typescript
import { interval, timer } from 'rxjs';

// Polling a cada 30 segundos
const polling$ = interval(30_000).pipe(
  switchMap(() => this.api.getStatus()),
  takeUntilDestroyed(this.destroyRef)
);

// Delay de 2 segundos e depois completa
const delayed$ = timer(2000).pipe(
  switchMap(() => this.api.getData())
);

// Retry com backoff: 1s, 2s, 4s, 8s...
retry({
  count: 4,
  delay: (_, retryCount) => timer(Math.pow(2, retryCount - 1) * 1000)
})
```

### `fromEvent` — eventos do DOM e Node.js
```typescript
import { fromEvent } from 'rxjs';
import { debounceTime, distinctUntilChanged, map } from 'rxjs/operators';

// Search input reativo
const input = document.getElementById('search') as HTMLInputElement;
const search$ = fromEvent(input, 'input').pipe(
  debounceTime(300),
  map(e => (e.target as HTMLInputElement).value),
  distinctUntilChanged()
);

// Uso em Directive
@Directive({ selector: '[appSearch]', standalone: true })
export class SearchDirective implements OnInit {
  private readonly el      = inject(ElementRef<HTMLInputElement>);
  private readonly destroy = inject(DestroyRef);

  readonly searched = output<string>();

  ngOnInit(): void {
    fromEvent<InputEvent>(this.el.nativeElement, 'input').pipe(
      debounceTime(300),
      map(e => (e.target as HTMLInputElement).value.trim()),
      distinctUntilChanged(),
      filter(v => v.length >= 2 || v.length === 0),
      takeUntilDestroyed(this.destroy)
    ).subscribe(term => this.searched.emit(term));
  }
}
```

### `Subject` — multicast manual, sem valor inicial
```typescript
import { Subject } from 'rxjs';

// Uso típico: eventos SignalR, EventBus simples
@Injectable({ providedIn: 'root' })
export class NotificationHub extends BaseHubService {
  private readonly _notification$ = new Subject<Notification>();
  readonly notification$ = this._notification$.asObservable(); // expõe readonly

  private registerHandlers(): void {
    this.connection.on('ReceiveNotification', (data: Notification) => {
      this._notification$.next(data);
    });
  }
}

// Uso típico: destroy$ para takeUntil (legado — prefer takeUntilDestroyed)
private readonly destroy$ = new Subject<void>();

ngOnDestroy(): void {
  this.destroy$.next();
  this.destroy$.complete();
}
```

### `BehaviorSubject` — estado reativo com valor inicial
```typescript
import { BehaviorSubject } from 'rxjs';

// Uso típico: estado em Service
@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly _user$ = new BehaviorSubject<User | null>(null);
  readonly user$          = this._user$.asObservable();

  // Leitura síncrona do valor atual
  get currentUser(): User | null {
    return this._user$.value;
  }

  login(user: User): void { this._user$.next(user); }
  logout(): void          { this._user$.next(null); }
}

// Uso em componente via async pipe
@Component({
  template: `@if (auth.user$ | async; as user) { <span>{{ user.name }}</span> }`
})
```

### `ReplaySubject` — guarda N valores para late subscribers
```typescript
import { ReplaySubject } from 'rxjs';

// Uso típico: configuração carregada uma vez, múltiplos subscribers
@Injectable({ providedIn: 'root' })
export class ConfigService {
  private readonly _config$ = new ReplaySubject<AppConfig>(1); // guarda 1 valor
  readonly config$          = this._config$.asObservable();

  load(): Observable<AppConfig> {
    return this.http.get<AppConfig>('/assets/config.json').pipe(
      tap(config => this._config$.next(config))
    );
  }
}

// Subscriber que chega DEPOIS do load() ainda recebe o valor
configService.config$.subscribe(config => console.log(config)); // ✅ funciona
```

### `combineLatest` como factory para estado derivado
```typescript
import { combineLatest } from 'rxjs';

// Estado derivado de múltiplos Subjects
@Injectable({ providedIn: 'root' })
export class CartService {
  private readonly _items$    = new BehaviorSubject<CartItem[]>([]);
  private readonly _discount$ = new BehaviorSubject<number>(0);

  // Stream derivado — recalcula sempre que items ou desconto muda
  readonly summary$ = combineLatest({
    items:    this._items$,
    discount: this._discount$
  }).pipe(
    map(({ items, discount }) => ({
      count:    items.length,
      subtotal: items.reduce((acc, i) => acc + i.price * i.qty, 0),
      discount,
      total:    items.reduce((acc, i) => acc + i.price * i.qty, 0) * (1 - discount / 100)
    })),
    shareReplay(1)
  );
}
```
