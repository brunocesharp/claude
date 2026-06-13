# Core HTTP Service — Referência

## Padrão base — BaseApiService

```typescript
// src/app/core/http/base-api.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable()
export abstract class BaseApiService {
  protected readonly http = inject(HttpClient);
  protected readonly baseUrl = environment.apiUrl;

  protected get<T>(endpoint: string, params?: Record<string, string | number>): Observable<T> {
    const httpParams = params
      ? new HttpParams({ fromObject: params as Record<string, string> })
      : undefined;
    return this.http.get<T>(`${this.baseUrl}/${endpoint}`, { params: httpParams });
  }

  protected post<T>(endpoint: string, body: unknown): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}/${endpoint}`, body);
  }

  protected put<T>(endpoint: string, body: unknown): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}/${endpoint}`, body);
  }

  protected patch<T>(endpoint: string, body: unknown): Observable<T> {
    return this.http.patch<T>(`${this.baseUrl}/${endpoint}`, body);
  }

  protected delete<T>(endpoint: string): Observable<T> {
    return this.http.delete<T>(`${this.baseUrl}/${endpoint}`);
  }
}
```

## HTTP Service específico

```typescript
// src/app/core/http/user-api.service.ts
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { BaseApiService } from './base-api.service';
import { User, CreateUserDto, UpdateUserDto, PagedResult } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class UserApiService extends BaseApiService {

  getAll(page = 1, size = 20): Observable<PagedResult<User>> {
    return this.get<PagedResult<User>>('users', { page, size });
  }

  getById(id: string): Observable<User> {
    return this.get<User>(`users/${id}`);
  }

  create(dto: CreateUserDto): Observable<User> {
    return this.post<User>('users', dto);
  }

  update(id: string, dto: UpdateUserDto): Observable<User> {
    return this.put<User>(`users/${id}`, dto);
  }

  remove(id: string): Observable<void> {
    return this.delete<void>(`users/${id}`);
  }
}
```

## HTTP Service com operadores RxJS avançados

```typescript
// src/app/core/http/dashboard-api.service.ts
import { Injectable } from '@angular/core';
import { Observable, forkJoin, combineLatest } from 'rxjs';
import { map, switchMap, retry, timeout } from 'rxjs/operators';
import { BaseApiService } from './base-api.service';
import { DashboardSummary, KpiData, ChartData } from '../models/dashboard.model';

@Injectable({ providedIn: 'root' })
export class DashboardApiService extends BaseApiService {

  // Requisições paralelas com forkJoin
  getSummary(): Observable<DashboardSummary> {
    return forkJoin({
      kpis: this.get<KpiData[]>('dashboard/kpis'),
      charts: this.get<ChartData[]>('dashboard/charts')
    }).pipe(
      map(({ kpis, charts }) => ({ kpis, charts })),
      retry(2),
      timeout(10000)
    );
  }

  // Requisição encadeada com switchMap
  getUserDashboard(userId: string): Observable<DashboardSummary> {
    return this.get<{ dashboardId: string }>(`users/${userId}/dashboard`).pipe(
      switchMap(({ dashboardId }) => this.get<DashboardSummary>(`dashboards/${dashboardId}`))
    );
  }
}
```

## Registro no app.config.ts

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { errorInterceptor } from './core/interceptors/error.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor, errorInterceptor])
    )
  ]
};
```

## Uso em NgRx Effect

```typescript
// features/users/store/users.effects.ts
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { UserApiService } from '../../../core/http/user-api.service';
import { UsersActions } from './users.actions';
import { switchMap, map, catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Injectable()
export class UsersEffects {
  private readonly actions$ = inject(Actions);
  private readonly api = inject(UserApiService);

  loadUsers$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.loadAll),
      switchMap(() =>
        this.api.getAll().pipe(
          map(result => UsersActions.loadAllSuccess({ users: result.items })),
          catchError(error => of(UsersActions.loadAllFailure({ error: error.message })))
        )
      )
    )
  );
}
```
