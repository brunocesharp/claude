# Core Interceptors — Referência

## Interceptor de Autenticação (funcional — Angular 15+)

```typescript
// src/app/core/interceptors/auth.interceptor.ts
import { HttpInterceptorFn, HttpRequest, HttpHandlerFn, HttpEvent } from '@angular/common/http';
import { inject } from '@angular/core';
import { Observable, switchMap, take } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> => {
  const auth = inject(AuthService);
  const token = localStorage.getItem('token');

  // Não intercepta requisições públicas
  if (req.url.includes('/auth/login') || req.url.includes('/assets')) {
    return next(req);
  }

  if (!token) {
    return next(req);
  }

  const authReq = req.clone({
    setHeaders: { Authorization: `Bearer ${token}` }
  });

  return next(authReq);
};
```

## Interceptor de Erro Global

```typescript
// src/app/core/interceptors/error.interceptor.ts
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { NotificationService } from '../services/notification.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const notification = inject(NotificationService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      switch (error.status) {
        case 401:
          // Token expirado — redireciona para login
          localStorage.removeItem('token');
          router.navigate(['/auth/login']);
          break;

        case 403:
          notification.error('Acesso negado. Você não tem permissão para esta ação.');
          router.navigate(['/forbidden']);
          break;

        case 404:
          notification.error('Recurso não encontrado.');
          break;

        case 422:
          // Validation errors do backend
          const validationErrors = error.error?.errors;
          if (validationErrors) {
            Object.values(validationErrors).flat().forEach((msg: any) =>
              notification.error(msg)
            );
          }
          break;

        case 500:
          notification.error('Erro interno do servidor. Tente novamente mais tarde.');
          break;

        default:
          notification.error('Ocorreu um erro inesperado.');
      }

      return throwError(() => error);
    })
  );
};
```

## Interceptor de Loading

```typescript
// src/app/core/interceptors/loading.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { LoadingService } from '../services/loading.service';

export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loading = inject(LoadingService);

  // Ignora requisições silenciosas (com header customizado)
  if (req.headers.has('X-Silent')) {
    return next(req.clone({ headers: req.headers.delete('X-Silent') }));
  }

  loading.show();
  return next(req).pipe(
    finalize(() => loading.hide())
  );
};
```

## Interceptor de Retry com Backoff

```typescript
// src/app/core/interceptors/retry.interceptor.ts
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { retry, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';

export const retryInterceptor: HttpInterceptorFn = (req, next) => {
  // Não retenta requisições de escrita
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
    return next(req);
  }

  return next(req).pipe(
    retry({
      count: 3,
      delay: (error: HttpErrorResponse, retryCount) => {
        // Só retenta em erros de rede (0) ou servidor (500+)
        if (error.status !== 0 && error.status < 500) {
          throw error;
        }
        // Exponential backoff: 1s, 2s, 4s
        return timer(Math.pow(2, retryCount - 1) * 1000);
      }
    })
  );
};
```

## Registro no app.config.ts

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { errorInterceptor } from './core/interceptors/error.interceptor';
import { loadingInterceptor } from './core/interceptors/loading.interceptor';
import { retryInterceptor } from './core/interceptors/retry.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    // Ordem importa: auth → loading → retry → error
    provideHttpClient(
      withInterceptors([
        authInterceptor,
        loadingInterceptor,
        retryInterceptor,
        errorInterceptor
      ])
    )
  ]
};
```
