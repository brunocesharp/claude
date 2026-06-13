# Error Handler Global — Referência

## GlobalErrorHandler

```typescript
// src/app/core/error-handler/global-error-handler.ts
import { ErrorHandler, Injectable, inject, NgZone } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { NotificationService } from '../services/notification.service';

@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  private readonly router = inject(Router);
  private readonly zone = inject(NgZone);
  private readonly notification = inject(NotificationService);

  handleError(error: unknown): void {
    // Erros HTTP são tratados pelo interceptor — ignora aqui
    if (error instanceof HttpErrorResponse) {
      return;
    }

    // Unwrap erros de Promise rejeitada
    const err = error instanceof Error ? error
      : error instanceof PromiseRejectionEvent ? error.reason
      : new Error(String(error));

    console.error('[GlobalErrorHandler]', err);

    // Executa dentro do NgZone para atualizar a UI
    this.zone.run(() => {
      this.notification.error(
        'Ocorreu um erro inesperado. Nossa equipe foi notificada.'
      );

      // Redireciona para página de erro em erros críticos
      if (this.isCriticalError(err)) {
        this.router.navigate(['/error'], {
          queryParams: { code: 'UNHANDLED' }
        });
      }
    });

    // Aqui você integraria com Sentry, Datadog, etc.
    this.reportToMonitoring(err);
  }

  private isCriticalError(error: Error): boolean {
    return (
      error.message.includes('ChunkLoadError') ||
      error.message.includes('Cannot read properties of null')
    );
  }

  private reportToMonitoring(error: Error): void {
    // Exemplo: Sentry.captureException(error);
    // Exemplo: datadogLogs.logger.error(error.message, { error });
    console.warn('[Monitoring] Would report:', error.message);
  }
}
```

## Página de erro

```typescript
// src/app/core/error-handler/error-page.component.ts
import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-error-page',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="error-container">
      <h1>Oops! Algo deu errado</h1>
      <p>Código: {{ errorCode }}</p>
      <button (click)="goHome()">Voltar ao início</button>
      <button (click)="retry()">Tentar novamente</button>
    </div>
  `
})
export class ErrorPageComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  readonly errorCode = this.route.snapshot.queryParams['code'] ?? 'UNKNOWN';

  goHome(): void {
    this.router.navigate(['/']);
  }

  retry(): void {
    window.location.reload();
  }
}
```

## NotificationService (dependência do ErrorHandler)

```typescript
// src/app/core/services/notification.service.ts
import { Injectable, signal } from '@angular/core';

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
}

@Injectable({ providedIn: 'root' })
export class NotificationService {
  // Signal para a lista de toasts ativos
  readonly toasts = signal<ToastMessage[]>([]);

  success(message: string): void {
    this.add({ type: 'success', message });
  }

  error(message: string): void {
    this.add({ type: 'error', message });
  }

  warning(message: string): void {
    this.add({ type: 'warning', message });
  }

  info(message: string): void {
    this.add({ type: 'info', message });
  }

  dismiss(id: string): void {
    this.toasts.update(list => list.filter(t => t.id !== id));
  }

  private add(toast: Omit<ToastMessage, 'id'>): void {
    const id = crypto.randomUUID();
    this.toasts.update(list => [...list, { ...toast, id }]);
    // Auto-dismiss após 5 segundos
    setTimeout(() => this.dismiss(id), 5000);
  }
}
```

## Registro no app.config.ts

```typescript
// app.config.ts
import { ApplicationConfig, ErrorHandler } from '@angular/core';
import { GlobalErrorHandler } from './core/error-handler/global-error-handler';

export const appConfig: ApplicationConfig = {
  providers: [
    // Substitui o ErrorHandler padrão do Angular
    {
      provide: ErrorHandler,
      useClass: GlobalErrorHandler
    }
  ]
};
```

## Rota da página de erro

```typescript
// app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'error',
    loadComponent: () => import('./core/error-handler/error-page.component')
      .then(m => m.ErrorPageComponent)
  }
];
```

## Uso em componente (captura manual de erro)

```typescript
// Quando precisar capturar erros locais sem deixar chegar no handler global:
import { Component, inject } from '@angular/core';
import { NotificationService } from '../../core/services/notification.service';

@Component({ selector: 'app-form', standalone: true, template: `...` })
export class FormComponent {
  private readonly notification = inject(NotificationService);

  save(): void {
    try {
      // lógica...
    } catch (err) {
      this.notification.error('Erro ao salvar. Tente novamente.');
      console.error(err);
    }
  }
}
```
