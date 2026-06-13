# Feature Routing — Referência

## Conceito

Cada Feature tem seu **próprio arquivo de rotas** (`[feature].routes.ts`), registrado no routing principal via lazy loading. O NgRx da feature é provido diretamente na rota.

---

## Rotas da feature (completo)

```typescript
// src/app/features/users/users.routes.ts
import { Routes } from '@angular/router';
import { provideState }   from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';

import { authGuard }            from '../../core/guards/auth.guard';
import { permissionGuard }      from '../../core/guards/permission.guard';
import { unsavedChangesGuard }  from '../../core/guards/unsaved-changes.guard';
import { userResolver }         from '../../core/resolvers/user.resolver';

import { usersReducer, usersFeatureName } from './store/users.reducer';
import { UsersEffects }                   from './store/users.effects';
import { UserSelectionService }           from './services/user-selection.service';

export const usersRoutes: Routes = [
  {
    path: '',
    // ─── Store e serviços com escopo nesta feature ────────
    providers: [
      provideState(usersFeatureName, usersReducer),
      provideEffects(UsersEffects),
      UserSelectionService  // Feature Service de escopo limitado
    ],
    // ─── Guard para todas as rotas filhas ─────────────────
    canActivate: [authGuard],
    children: [

      // ── Listagem ──────────────────────────────────────────
      {
        path: '',
        loadComponent: () => import('./pages/user-list-page/user-list-page.component')
          .then(m => m.UserListPageComponent),
        title: 'Usuários'
      },

      // ── Detalhe ───────────────────────────────────────────
      {
        path: ':id',
        loadComponent: () => import('./pages/user-detail-page/user-detail-page.component')
          .then(m => m.UserDetailPageComponent),
        resolve: { user: userResolver },
        title: 'Detalhe do Usuário'
      },

      // ── Criação (apenas Admin/Manager) ────────────────────
      {
        path: 'new',
        loadComponent: () => import('./pages/user-form-page/user-form-page.component')
          .then(m => m.UserFormPageComponent),
        canActivate: [permissionGuard],
        data: { roles: ['Admin', 'Manager'] },
        title: 'Novo Usuário'
      },

      // ── Edição (apenas Admin/Manager) ─────────────────────
      {
        path: ':id/edit',
        loadComponent: () => import('./pages/user-form-page/user-form-page.component')
          .then(m => m.UserFormPageComponent),
        canActivate: [permissionGuard],
        canDeactivate: [unsavedChangesGuard],
        resolve: { user: userResolver },
        data: { roles: ['Admin', 'Manager'] },
        title: 'Editar Usuário'
      }
    ]
  }
];
```

---

## Registro no routing principal

```typescript
// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  // ── Públicas ──────────────────────────────────────────────
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.routes')
      .then(m => m.authRoutes)
  },

  // ── Privadas (com layout) ─────────────────────────────────
  {
    path: '',
    canActivate: [authGuard],
    loadComponent: () => import('./shared/layout/main-layout.component')
      .then(m => m.MainLayoutComponent),
    children: [
      {
        path: 'dashboard',
        loadChildren: () => import('./features/dashboard/dashboard.routes')
          .then(m => m.dashboardRoutes)
      },
      {
        path: 'users',
        loadChildren: () => import('./features/users/users.routes')
          .then(m => m.usersRoutes)
      },
      {
        path: 'orders',
        loadChildren: () => import('./features/orders/orders.routes')
          .then(m => m.ordersRoutes)
      },
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      }
    ]
  },

  // ── Fallback ──────────────────────────────────────────────
  {
    path: 'forbidden',
    loadComponent: () => import('./core/error-handler/error-page.component')
      .then(m => m.ErrorPageComponent),
    data: { code: 'FORBIDDEN' }
  },
  {
    path: '**',
    loadComponent: () => import('./core/error-handler/error-page.component')
      .then(m => m.ErrorPageComponent),
    data: { code: 'NOT_FOUND' }
  }
];
```

---

## Preloading Strategy (carrega features em background)

```typescript
// src/app/core/services/selective-preloading.strategy.ts
import { Injectable } from '@angular/core';
import { PreloadingStrategy, Route } from '@angular/router';
import { Observable, of } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class SelectivePreloadingStrategy implements PreloadingStrategy {
  preload(route: Route, load: () => Observable<unknown>): Observable<unknown> {
    // Faz preload apenas em rotas com data: { preload: true }
    return route.data?.['preload'] === true ? load() : of(null);
  }
}
```

```typescript
// app.config.ts — registro da estratégia
import { ApplicationConfig }             from '@angular/core';
import { provideRouter, withPreloading } from '@angular/router';
import { routes }                        from './app.routes';
import { SelectivePreloadingStrategy }   from './core/services/selective-preloading.strategy';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      withPreloading(SelectivePreloadingStrategy)
    )
  ]
};
```

---

## Rota com sub-feature (nested lazy loading)

```typescript
// src/app/features/admin/admin.routes.ts
import { Routes } from '@angular/router';
import { permissionGuard } from '../../core/guards/permission.guard';

export const adminRoutes: Routes = [
  {
    path: '',
    canActivate: [permissionGuard],
    data: { roles: ['Admin'] },
    loadComponent: () => import('./layout/admin-layout.component')
      .then(m => m.AdminLayoutComponent),
    children: [
      {
        path: 'users',
        // Sub-feature lazy loaded dentro de admin
        loadChildren: () => import('../users/users.routes')
          .then(m => m.usersRoutes)
      },
      {
        path: 'settings',
        loadChildren: () => import('./settings/settings.routes')
          .then(m => m.settingsRoutes)
      },
      {
        path: '',
        redirectTo: 'users',
        pathMatch: 'full'
      }
    ]
  }
];
```

---

## app.config.ts completo

```typescript
// src/app/app.config.ts
import { ApplicationConfig, ErrorHandler, APP_INITIALIZER } from '@angular/core';
import { provideRouter, withPreloading, withComponentInputBinding } from '@angular/router';
import { provideHttpClient, withInterceptors }                      from '@angular/common/http';
import { provideStore }                                             from '@ngrx/store';
import { provideEffects }                                           from '@ngrx/effects';
import { provideStoreDevtools }                                     from '@ngrx/store-devtools';

import { routes }                       from './app.routes';
import { SelectivePreloadingStrategy }  from './core/services/selective-preloading.strategy';
import { authInterceptor }              from './core/interceptors/auth.interceptor';
import { errorInterceptor }             from './core/interceptors/error.interceptor';
import { loadingInterceptor }           from './core/interceptors/loading.interceptor';
import { GlobalErrorHandler }           from './core/error-handler/global-error-handler';
import { NotificationHub }              from './core/hubs/notification.hub';
import { environment }                  from '../environments/environment';

function initHubs(hub: NotificationHub) {
  return () => hub.startConnection();
}

export const appConfig: ApplicationConfig = {
  providers: [
    // ── Router ────────────────────────────────────────────
    provideRouter(
      routes,
      withPreloading(SelectivePreloadingStrategy),
      withComponentInputBinding()  // permite @Input() receber route params
    ),

    // ── HTTP ──────────────────────────────────────────────
    provideHttpClient(
      withInterceptors([authInterceptor, loadingInterceptor, errorInterceptor])
    ),

    // ── NgRx (Store global vazio — features registram via rota) ──
    provideStore({}),
    provideEffects([]),
    provideStoreDevtools({ maxAge: 25, logOnly: environment.production }),

    // ── Error Handler ─────────────────────────────────────
    { provide: ErrorHandler, useClass: GlobalErrorHandler },

    // ── SignalR — inicializa ao subir o app ───────────────
    {
      provide: APP_INITIALIZER,
      useFactory: initHubs,
      deps: [NotificationHub],
      multi: true
    }
  ]
};
```
