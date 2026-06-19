# Core Hub (SignalR) — Referência

## Instalação

```bash
npm install @microsoft/signalr
```

## Padrão base — BaseHubService

```typescript
// src/app/core/hubs/base-hub.service.ts
import { Injectable, OnDestroy } from '@angular/core';
import {
  HubConnection,
  HubConnectionBuilder,
  HubConnectionState,
  LogLevel,
  HttpTransportType
} from '@microsoft/signalr';
import { Subject, BehaviorSubject } from 'rxjs';

@Injectable()
export abstract class BaseHubService implements OnDestroy {
  protected connection!: HubConnection;

  private readonly _connectionState$ = new BehaviorSubject<HubConnectionState>(
    HubConnectionState.Disconnected
  );
  readonly connectionState$ = this._connectionState$.asObservable();

  protected readonly destroy$ = new Subject<void>();

  protected buildConnection(hubUrl: string, accessToken?: () => string): void {
    const builder = new HubConnectionBuilder()
      .withUrl(hubUrl, {
        transport: HttpTransportType.WebSockets,
        ...(accessToken ? { accessTokenFactory: accessToken } : {})
      })
      .withAutomaticReconnect([0, 2000, 5000, 10000, 30000])
      .configureLogging(LogLevel.Warning);

    this.connection = builder.build();

    // Rastreia estado da conexão
    this.connection.onreconnecting(() =>
      this._connectionState$.next(HubConnectionState.Reconnecting)
    );
    this.connection.onreconnected(() =>
      this._connectionState$.next(HubConnectionState.Connected)
    );
    this.connection.onclose(() =>
      this._connectionState$.next(HubConnectionState.Disconnected)
    );
  }

  async startConnection(): Promise<void> {
    if (this.connection.state === HubConnectionState.Disconnected) {
      try {
        await this.connection.start();
        this._connectionState$.next(HubConnectionState.Connected);
      } catch (err) {
        console.error('SignalR connection failed:', err);
        this._connectionState$.next(HubConnectionState.Disconnected);
        throw err;
      }
    }
  }

  async stopConnection(): Promise<void> {
    if (this.connection.state !== HubConnectionState.Disconnected) {
      await this.connection.stop();
    }
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.stopConnection();
  }
}
```

## Hub específico — NotificationHub

```typescript
// src/app/core/hubs/notification.hub.ts
import { Injectable, inject } from '@angular/core';
import { Subject } from 'rxjs';
import { BaseHubService } from './base-hub.service';
import { AuthService } from '../services/auth.service';
import { Notification } from '../models/notification.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class NotificationHub extends BaseHubService {
  private readonly auth = inject(AuthService);

  // Subjects para cada evento do Hub
  private readonly _notification$ = new Subject<Notification>();
  private readonly _notificationRead$ = new Subject<string>();

  // Observables públicos — componentes e effects consomem daqui
  readonly notification$ = this._notification$.asObservable();
  readonly notificationRead$ = this._notificationRead$.asObservable();

  constructor() {
    super();
    this.buildConnection(
      `${environment.apiUrl}/hubs/notifications`,
      () => localStorage.getItem('token') ?? ''
    );
    this.registerHandlers();
  }

  private registerHandlers(): void {
    // Escuta eventos do servidor .NET
    this.connection.on('ReceiveNotification', (notification: Notification) => {
      this._notification$.next(notification);
    });

    this.connection.on('NotificationRead', (id: string) => {
      this._notificationRead$.next(id);
    });
  }

  // Invoca métodos no servidor .NET
  async markAsRead(notificationId: string): Promise<void> {
    await this.connection.invoke('MarkNotificationAsRead', notificationId);
  }

  async markAllAsRead(): Promise<void> {
    await this.connection.invoke('MarkAllNotificationsAsRead');
  }
}
```

## Integração com NgRx — Effect que escuta o Hub

```typescript
// src/app/features/notifications/store/notifications.effects.ts
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect } from '@ngrx/effects';
import { NotificationHub } from '../../../core/hubs/notification.hub';
import { NotificationsActions } from './notifications.actions';
import { map, switchMap, takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Injectable()
export class NotificationsEffects {
  private readonly actions$ = inject(Actions);
  private readonly hub = inject(NotificationHub);
  private readonly destroy$ = new Subject<void>();

  // Effect que escuta SignalR e despacha Action para a Store
  receiveNotification$ = createEffect(() =>
    this.hub.notification$.pipe(
      takeUntil(this.destroy$),
      map(notification => NotificationsActions.received({ notification }))
    )
  );
}
```

## Inicialização no app.config.ts

```typescript
// app.config.ts
import { ApplicationConfig, APP_INITIALIZER } from '@angular/core';
import { NotificationHub } from './core/hubs/notification.hub';

function initHubs(notificationHub: NotificationHub) {
  return () => notificationHub.startConnection();
}

export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: APP_INITIALIZER,
      useFactory: initHubs,
      deps: [NotificationHub],
      multi: true
    }
  ]
};
```

## Backend .NET — Exemplo do Hub correspondente

```csharp
// Hubs/NotificationHub.cs
[Authorize]
public class NotificationHub : Hub
{
    public async Task MarkNotificationAsRead(string notificationId)
    {
        // lógica...
        await Clients.Caller.SendAsync("NotificationRead", notificationId);
    }

    public async Task MarkAllNotificationsAsRead()
    {
        // lógica...
    }
}

// Program.cs
app.MapHub<NotificationHub>("/hubs/notifications");
```
