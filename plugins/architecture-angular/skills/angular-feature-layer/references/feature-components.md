# Feature Components — Referência

## Conceito: Smart vs Dumb

| | Smart Component | Dumb Component |
|---|---|---|
| **Responsabilidade** | Orquestra dados e ações | Apresenta dados recebidos |
| **Acesso à Store** | Sim — via `inject(Store)` | Nunca |
| **Inputs** | Poucos ou nenhum | Todos via `@Input()` |
| **Outputs** | Despacha Actions | Emite `@Output()` events |
| **Change Detection** | `OnPush` | `OnPush` |
| **Localização** | `features/[x]/components/` | `shared/components/` ou `features/[x]/components/` |

---

## Smart Component — Padrão completo

```typescript
// src/app/features/users/components/user-list/user-list.component.ts
import {
  Component, inject, ChangeDetectionStrategy, OnInit
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Store } from '@ngrx/store';
import { toSignal } from '@angular/core/rxjs-interop';
import { UsersActions } from '../../store/users.actions';
import {
  selectUsersAll,
  selectUsersLoading,
  selectUsersError,
  selectSelectedUser
} from '../../store/users.selectors';
import { User } from '../../../../core/models/user.model';
import { UserCardComponent } from '../user-card/user-card.component';
import { UserFiltersComponent } from '../user-filters/user-filters.component';

@Component({
  selector: 'app-user-list',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, UserCardComponent, UserFiltersComponent],
  template: `
    <app-user-filters (filterChange)="onFilterChange($event)" />

    @if (loading()) {
      <div class="loading-spinner">Carregando...</div>
    }

    @if (error()) {
      <div class="error-message">{{ error() }}</div>
    }

    @if (!loading() && users().length === 0) {
      <div class="empty-state">Nenhum usuário encontrado.</div>
    }

    <div class="user-grid">
      @for (user of users(); track user.id) {
        <app-user-card
          [user]="user"
          [isSelected]="selectedUser()?.id === user.id"
          (select)="onSelect($event)"
          (delete)="onDelete($event)"
        />
      }
    </div>
  `
})
export class UserListComponent implements OnInit {
  private readonly store = inject(Store);

  // Selectors convertidos em Signals para template reativo
  readonly users    = toSignal(this.store.select(selectUsersAll),    { initialValue: [] });
  readonly loading  = toSignal(this.store.select(selectUsersLoading), { initialValue: false });
  readonly error    = toSignal(this.store.select(selectUsersError),   { initialValue: null });
  readonly selectedUser = toSignal(this.store.select(selectSelectedUser), { initialValue: null });

  ngOnInit(): void {
    this.store.dispatch(UsersActions.loadAll());
  }

  onSelect(user: User): void {
    this.store.dispatch(UsersActions.select({ userId: user.id }));
  }

  onDelete(user: User): void {
    this.store.dispatch(UsersActions.remove({ userId: user.id }));
  }

  onFilterChange(filters: Record<string, string>): void {
    this.store.dispatch(UsersActions.applyFilters({ filters }));
  }
}
```

---

## Dumb Component — Padrão completo

```typescript
// src/app/features/users/components/user-card/user-card.component.ts
import {
  Component, Input, Output, EventEmitter,
  ChangeDetectionStrategy, input, output
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { User } from '../../../../core/models/user.model';

@Component({
  selector: 'app-user-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    <div class="card" [class.selected]="isSelected()">
      <div class="card-header">
        <div class="avatar">{{ initials() }}</div>
        <div class="info">
          <h3>{{ user().name }}</h3>
          <span>{{ user().email }}</span>
        </div>
      </div>

      <div class="card-actions">
        <button (click)="select.emit(user())">Selecionar</button>
        <button (click)="delete.emit(user())" class="danger">Excluir</button>
      </div>
    </div>
  `
})
export class UserCardComponent {
  // Angular 17+ signal inputs (preferido sobre @Input())
  readonly user       = input.required<User>();
  readonly isSelected = input<boolean>(false);

  // Angular 17+ signal outputs
  readonly select = output<User>();
  readonly delete = output<User>();

  // Computed diretamente no componente — sem lógica no template
  readonly initials = () => this.user().name
    .split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}
```

---

## Componente com Form interno (sem Store)

```typescript
// src/app/features/users/components/user-filters/user-filters.component.ts
import {
  Component, output, ChangeDetectionStrategy, inject, OnInit
} from '@angular/core';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-user-filters',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" class="filters">
      <input formControlName="search" placeholder="Buscar usuário..." />
      <select formControlName="role">
        <option value="">Todos os perfis</option>
        <option value="Admin">Admin</option>
        <option value="Manager">Manager</option>
        <option value="Viewer">Viewer</option>
      </select>
    </form>
  `
})
export class UserFiltersComponent implements OnInit {
  private readonly fb = inject(FormBuilder);

  readonly filterChange = output<Record<string, string>>();

  readonly form = this.fb.nonNullable.group({
    search: [''],
    role:   ['']
  });

  constructor() {
    // takeUntilDestroyed no constructor — Angular 17+
    this.form.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      takeUntilDestroyed()
    ).subscribe(values => {
      this.filterChange.emit(values as Record<string, string>);
    });
  }

  ngOnInit(): void {}
}
```

---

## Boas práticas

```typescript
// ✅ CORRETO — OnPush + toSignal + inject()
@Component({ changeDetection: ChangeDetectionStrategy.OnPush })
export class MyComponent {
  private readonly store = inject(Store);
  readonly items = toSignal(this.store.select(selectItems), { initialValue: [] });
}

// ❌ EVITAR — Default change detection + subscribe manual
@Component({}) // sem OnPush
export class MyComponent implements OnInit, OnDestroy {
  items: Item[] = [];
  private sub!: Subscription;

  constructor(private store: Store) {}  // constructor injection — evitar

  ngOnInit() {
    this.sub = this.store.select(selectItems).subscribe(i => this.items = i);
  }
  ngOnDestroy() { this.sub.unsubscribe(); }
}
```
