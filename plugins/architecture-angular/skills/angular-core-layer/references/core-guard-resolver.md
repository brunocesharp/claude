# Guards e Resolvers — Referência

## Guard de Autenticação (funcional — Angular 15+)

```typescript
// src/app/core/guards/auth.guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  const token = localStorage.getItem('token');

  if (!token) {
    // Salva a URL de destino para redirecionar após login
    router.navigate(['/auth/login'], {
      queryParams: { returnUrl: route.url.join('/') }
    });
    return false;
  }

  return true;
};
```

## Guard de Permissão (baseado em roles)

```typescript
// src/app/core/guards/permission.guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { map, take } from 'rxjs/operators';

export const permissionGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  // Roles definidas na rota via data: { roles: ['Admin', 'Manager'] }
  const requiredRoles: string[] = route.data['roles'] ?? [];

  return auth.currentUser$.pipe(
    take(1),
    map(user => {
      if (!user) {
        router.navigate(['/auth/login']);
        return false;
      }

      const hasRole = requiredRoles.length === 0 ||
        requiredRoles.some(role => user.roles.includes(role));

      if (!hasRole) {
        router.navigate(['/forbidden']);
        return false;
      }

      return true;
    })
  );
};
```

## Guard de saída (unsaved changes)

```typescript
// src/app/core/guards/unsaved-changes.guard.ts
import { CanDeactivateFn } from '@angular/router';

export interface HasUnsavedChanges {
  hasUnsavedChanges(): boolean;
}

export const unsavedChangesGuard: CanDeactivateFn<HasUnsavedChanges> = (component) => {
  if (component.hasUnsavedChanges()) {
    return confirm('Você tem alterações não salvas. Deseja sair mesmo assim?');
  }
  return true;
};
```

## Resolver — carrega dados antes de ativar a rota

```typescript
// src/app/core/resolvers/user.resolver.ts
import { inject } from '@angular/core';
import { ResolveFn, ActivatedRouteSnapshot, Router } from '@angular/router';
import { Observable, EMPTY, catchError } from 'rxjs';
import { UserApiService } from '../http/user-api.service';
import { User } from '../models/user.model';

export const userResolver: ResolveFn<User> = (
  route: ActivatedRouteSnapshot
): Observable<User> => {
  const api = inject(UserApiService);
  const router = inject(Router);
  const id = route.paramMap.get('id')!;

  return api.getById(id).pipe(
    catchError(() => {
      router.navigate(['/not-found']);
      return EMPTY; // EMPTY cancela a navegação
    })
  );
};
```

## Resolver — carrega múltiplos dados em paralelo

```typescript
// src/app/core/resolvers/dashboard.resolver.ts
import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { forkJoin, Observable } from 'rxjs';
import { DashboardApiService } from '../http/dashboard-api.service';
import { DashboardSummary } from '../models/dashboard.model';

export const dashboardResolver: ResolveFn<DashboardSummary> = (): Observable<DashboardSummary> => {
  const api = inject(DashboardApiService);
  return api.getSummary();
};
```

## Configuração nas rotas

```typescript
// app.routes.ts
import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { permissionGuard } from './core/guards/permission.guard';
import { unsavedChangesGuard } from './core/guards/unsaved-changes.guard';
import { userResolver } from './core/resolvers/user.resolver';
import { dashboardResolver } from './core/resolvers/dashboard.resolver';

export const routes: Routes = [
  {
    path: 'dashboard',
    canActivate: [authGuard],
    resolve: { summary: dashboardResolver },
    loadComponent: () => import('./features/dashboard/dashboard.component')
      .then(m => m.DashboardComponent)
  },
  {
    path: 'admin',
    canActivate: [authGuard, permissionGuard],
    data: { roles: ['Admin'] },
    children: [
      {
        path: 'users/:id',
        resolve: { user: userResolver },
        canDeactivate: [unsavedChangesGuard],
        loadComponent: () => import('./features/admin/user-edit/user-edit.component')
          .then(m => m.UserEditComponent)
      }
    ]
  }
];
```

## Consumindo o Resolver no componente

```typescript
// features/admin/user-edit/user-edit.component.ts
import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { User } from '../../../core/models/user.model';
import { HasUnsavedChanges } from '../../../core/guards/unsaved-changes.guard';

@Component({ selector: 'app-user-edit', standalone: true, template: `...` })
export class UserEditComponent implements HasUnsavedChanges {
  private readonly route = inject(ActivatedRoute);

  // Dados já disponíveis — sem loading, sem requisição extra
  readonly user: User = this.route.snapshot.data['user'];
  private isDirty = false;

  hasUnsavedChanges(): boolean {
    return this.isDirty;
  }
}
```
