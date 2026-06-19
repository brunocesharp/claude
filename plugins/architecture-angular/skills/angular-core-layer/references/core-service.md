# Core Service — Referência

## Quando usar
Serviços singleton com lógica de negócio, estado compartilhado e BehaviorSubject.

## Padrão base

```typescript
// src/app/core/services/auth.service.ts
import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap, catchError, throwError } from 'rxjs';
import { User } from '../models/user.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);

  // Estado reativo com BehaviorSubject (para ser observado externamente)
  private readonly _currentUser$ = new BehaviorSubject<User | null>(null);
  readonly currentUser$ = this._currentUser$.asObservable();

  // Estado reativo com Signal (para estado local/computed)
  private readonly _isLoading = signal(false);
  readonly isLoading = this._isLoading.asReadonly();
  readonly isAuthenticated = computed(() => this._currentUser$.value !== null);

  login(email: string, password: string): Observable<User> {
    this._isLoading.set(true);
    return this.http.post<User>(`${environment.apiUrl}/auth/login`, { email, password }).pipe(
      tap(user => {
        this._currentUser$.next(user);
        this._isLoading.set(false);
      }),
      catchError(err => {
        this._isLoading.set(false);
        return throwError(() => err);
      })
    );
  }

  logout(): void {
    this._currentUser$.next(null);
    localStorage.removeItem('token');
  }

  getCurrentUser(): User | null {
    return this._currentUser$.value;
  }
}
```

## Padrão com ReplaySubject (para late subscribers)

```typescript
// src/app/core/services/config.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ReplaySubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { AppConfig } from '../models/app-config.model';

@Injectable({ providedIn: 'root' })
export class ConfigService {
  private readonly http = inject(HttpClient);

  // ReplaySubject guarda 1 valor — ideal para config carregada uma vez
  private readonly _config$ = new ReplaySubject<AppConfig>(1);
  readonly config$ = this._config$.asObservable();

  load(): Observable<AppConfig> {
    return this.http.get<AppConfig>('/assets/config.json').pipe(
      tap(config => this._config$.next(config))
    );
  }
}
```

## Padrão com shareReplay (para requisições cacheadas)

```typescript
// src/app/core/services/reference-data.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, shareReplay } from 'rxjs';
import { Country } from '../models/country.model';

@Injectable({ providedIn: 'root' })
export class ReferenceDataService {
  private readonly http = inject(HttpClient);

  // shareReplay(1) garante que a chamada HTTP é feita apenas uma vez
  readonly countries$: Observable<Country[]> = this.http
    .get<Country[]>('/api/reference/countries')
    .pipe(shareReplay(1));
}
```

## Registro no app.config.ts

Serviços com `providedIn: 'root'` são registrados automaticamente.
Para serviços que precisam de inicialização, use `APP_INITIALIZER`:

```typescript
// app.config.ts
import { ApplicationConfig, APP_INITIALIZER } from '@angular/core';
import { ConfigService } from './core/services/config.service';

export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: APP_INITIALIZER,
      useFactory: (config: ConfigService) => () => config.load(),
      deps: [ConfigService],
      multi: true
    }
  ]
};
```

## Exemplo de uso em componente

```typescript
import { Component, inject } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [AsyncPipe],
  template: `
    @if (auth.currentUser$ | async; as user) {
      <span>Olá, {{ user.name }}</span>
    }
  `
})
export class HeaderComponent {
  readonly auth = inject(AuthService);
}
```
