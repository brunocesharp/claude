# Feature Services — Referência

## Conceito

Feature Services diferem dos Core Services:

| | Core Service | Feature Service |
|---|---|---|
| **Escopo** | `providedIn: 'root'` — singleton global | `providedIn: 'root'` ou fornecido na rota |
| **Estado** | Estado global compartilhado | Estado local da feature |
| **Responsabilidade** | Lógica de negócio transversal | Lógica específica da feature |
| **Dependências** | HTTP Services, Hubs | Core Services + lógica local |

---

## Feature Service com estado local (Signal-based)

```typescript
// src/app/features/users/services/user-selection.service.ts
import { Injectable, signal, computed } from '@angular/core';
import { User } from '../../../core/models/user.model';

// Fornecido na rota — destruído ao sair da feature
@Injectable()
export class UserSelectionService {
  // Estado interno com Signals
  private readonly _selectedIds = signal<Set<string>>(new Set());
  private readonly _allUsers    = signal<User[]>([]);

  // Computeds públicos
  readonly selectedIds    = this._selectedIds.asReadonly();
  readonly selectedCount  = computed(() => this._selectedIds().size);
  readonly hasSelection   = computed(() => this._selectedIds().size > 0);
  readonly selectedUsers  = computed(() =>
    this._allUsers().filter(u => this._selectedIds().has(u.id))
  );
  readonly isAllSelected  = computed(() =>
    this._allUsers().length > 0 &&
    this._allUsers().every(u => this._selectedIds().has(u.id))
  );

  setUsers(users: User[]): void {
    this._allUsers.set(users);
  }

  toggleSelect(userId: string): void {
    this._selectedIds.update(ids => {
      const next = new Set(ids);
      next.has(userId) ? next.delete(userId) : next.add(userId);
      return next;
    });
  }

  selectAll(): void {
    this._selectedIds.set(new Set(this._allUsers().map(u => u.id)));
  }

  clearSelection(): void {
    this._selectedIds.set(new Set());
  }

  isSelected(userId: string): boolean {
    return this._selectedIds().has(userId);
  }
}
```

---

## Feature Service com lógica de negócio complexa

```typescript
// src/app/features/users/services/user-export.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { User } from '../../../core/models/user.model';
import { environment } from '../../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class UserExportService {
  private readonly http = inject(HttpClient);

  // Exporta para CSV no frontend (sem backend)
  exportToCsv(users: User[]): void {
    const headers = ['ID', 'Nome', 'E-mail', 'Perfis', 'Status', 'Criado em'];
    const rows    = users.map(u => [
      u.id,
      u.name,
      u.email,
      u.roles.join(';'),
      u.status,
      new Date(u.createdAt).toLocaleDateString('pt-BR')
    ]);

    const csv = [headers, ...rows]
      .map(row => row.map(v => `"${v}"`).join(','))
      .join('\n');

    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const url  = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href     = url;
    link.download = `usuarios_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  }

  // Exporta via backend (PDF, Excel)
  exportToExcel(filters: Record<string, string>): Observable<Blob> {
    return this.http.get(`${environment.apiUrl}/users/export`, {
      params: filters,
      responseType: 'blob'
    });
  }
}
```

---

## Feature Service com RxJS (estado reativo sem NgRx)

```typescript
// src/app/features/users/services/user-search.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject, combineLatest, debounceTime, distinctUntilChanged, switchMap, shareReplay } from 'rxjs';
import { inject } from '@angular/core';
import { UserApiService } from '../../../core/http/user-api.service';
import { User, PagedResult } from '../../../core/models/user.model';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class UserSearchService {
  private readonly api = inject(UserApiService);

  private readonly _searchTerm$ = new BehaviorSubject<string>('');
  private readonly _page$       = new BehaviorSubject<number>(1);
  private readonly _pageSize$   = new BehaviorSubject<number>(20);

  readonly searchTerm$ = this._searchTerm$.asObservable();
  readonly page$       = this._page$.asObservable();

  // Stream de resultados reativo — reage a qualquer mudança nos filtros
  readonly results$: Observable<PagedResult<User>> = combineLatest([
    this._searchTerm$.pipe(debounceTime(300), distinctUntilChanged()),
    this._page$,
    this._pageSize$
  ]).pipe(
    switchMap(([term, page, size]) =>
      this.api.getAll(page, size, term ? { search: term } : {}).pipe(
        catchError(() => of({ items: [], totalCount: 0, page: 1, pageSize: 20, totalPages: 0 }))
      )
    ),
    shareReplay(1)
  );

  readonly users$: Observable<User[]> = this.results$.pipe(
    map(r => r.items)
  );

  readonly totalCount$: Observable<number> = this.results$.pipe(
    map(r => r.totalCount)
  );

  setSearch(term: string): void {
    this._searchTerm$.next(term);
    this._page$.next(1);  // Reset para primeira página ao buscar
  }

  setPage(page: number): void {
    this._page$.next(page);
  }

  setPageSize(size: number): void {
    this._pageSize$.next(size);
    this._page$.next(1);
  }

  reset(): void {
    this._searchTerm$.next('');
    this._page$.next(1);
    this._pageSize$.next(20);
  }
}
```

---

## Registro do Feature Service na rota (escopo limitado)

```typescript
// src/app/features/users/users.routes.ts
import { Routes } from '@angular/router';
import { UserSelectionService } from './services/user-selection.service';

export const usersRoutes: Routes = [
  {
    path: '',
    // providers aqui: serviço é criado ao entrar e destruído ao sair da rota
    providers: [UserSelectionService],
    children: [
      {
        path: '',
        loadComponent: () => import('./pages/user-list-page/user-list-page.component')
          .then(m => m.UserListPageComponent)
      }
    ]
  }
];
```

---

## Uso em componente

```typescript
// Smart Component consumindo Feature Service
import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { UserSelectionService } from '../../services/user-selection.service';
import { UserExportService } from '../../services/user-export.service';

@Component({
  selector: 'app-user-toolbar',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="toolbar">
      <span>{{ selection.selectedCount() }} selecionados</span>

      @if (selection.hasSelection()) {
        <button (click)="onExport()">Exportar selecionados</button>
        <button (click)="selection.clearSelection()">Limpar seleção</button>
      }
    </div>
  `
})
export class UserToolbarComponent {
  readonly selection = inject(UserSelectionService);
  readonly exporter  = inject(UserExportService);

  onExport(): void {
    this.exporter.exportToCsv(this.selection.selectedUsers());
  }
}
```
