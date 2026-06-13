# Feature Pages — Referência

## Conceito

Pages são **componentes roteados** — ativados pelo Router. Diferem dos Components porque:
- São o **ponto de entrada** da rota (não recebem `@Input` de pai)
- **Orquestram o layout** da feature, compondo Smart e Dumb Components
- Geralmente contêm a **lógica de inicialização** da feature (dispatch inicial)
- Recebem dados do `ActivatedRoute` (params, queryParams, resolve data)

```
features/users/pages/
├── user-list-page/
│   ├── user-list-page.component.ts
│   └── user-list-page.component.html
├── user-detail-page/
│   ├── user-detail-page.component.ts
│   └── user-detail-page.component.html
└── user-create-page/
    ├── user-create-page.component.ts
    └── user-create-page.component.html
```

---

## Page de listagem

```typescript
// src/app/features/users/pages/user-list-page/user-list-page.component.ts
import {
  Component, inject, ChangeDetectionStrategy, OnInit
} from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { toSignal } from '@angular/core/rxjs-interop';
import { UsersActions } from '../../store/users.actions';
import { selectUsersTotalCount, selectUsersLoading } from '../../store/users.selectors';
import { UserListComponent } from '../../components/user-list/user-list.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-list-page',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, UserListComponent],
  template: `
    <div class="page-header">
      <h1>Usuários</h1>
      <span class="badge">{{ totalCount() }} registros</span>
      <button (click)="onCreate()">+ Novo Usuário</button>
    </div>

    <app-user-list />
  `
})
export class UserListPageComponent implements OnInit {
  private readonly store  = inject(Store);
  private readonly router = inject(Router);

  readonly totalCount = toSignal(this.store.select(selectUsersTotalCount), { initialValue: 0 });
  readonly loading    = toSignal(this.store.select(selectUsersLoading),    { initialValue: false });

  ngOnInit(): void {
    // Page é responsável pelo dispatch de inicialização
    this.store.dispatch(UsersActions.loadAll());
  }

  onCreate(): void {
    this.router.navigate(['/users/new']);
  }
}
```

---

## Page de detalhe (com Resolver)

```typescript
// src/app/features/users/pages/user-detail-page/user-detail-page.component.ts
import {
  Component, inject, ChangeDetectionStrategy, OnInit
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { toSignal } from '@angular/core/rxjs-interop';
import { UsersActions } from '../../store/users.actions';
import { selectSelectedUser, selectUsersLoading } from '../../store/users.selectors';
import { User } from '../../../../core/models/user.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-detail-page',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    @if (loading()) {
      <div class="skeleton-loader">Carregando...</div>
    }

    @if (user(); as u) {
      <div class="page-header">
        <button (click)="goBack()">← Voltar</button>
        <h1>{{ u.name }}</h1>
        <button (click)="onEdit(u)">Editar</button>
        <button (click)="onDelete(u)" class="danger">Excluir</button>
      </div>

      <div class="detail-grid">
        <div class="field">
          <label>E-mail</label>
          <span>{{ u.email }}</span>
        </div>
        <div class="field">
          <label>Perfil</label>
          <span>{{ u.roles.join(', ') }}</span>
        </div>
        <div class="field">
          <label>Status</label>
          <span [class]="u.status.toLowerCase()">{{ u.status }}</span>
        </div>
      </div>
    }
  `
})
export class UserDetailPageComponent implements OnInit {
  private readonly store  = inject(Store);
  private readonly route  = inject(ActivatedRoute);
  private readonly router = inject(Router);

  // Dados do resolver — disponíveis imediatamente, sem loading extra
  private readonly resolvedUser: User = this.route.snapshot.data['user'];

  readonly user    = toSignal(this.store.select(selectSelectedUser), { initialValue: null });
  readonly loading = toSignal(this.store.select(selectUsersLoading), { initialValue: false });

  ngOnInit(): void {
    // Carrega o usuário resolvido na Store
    this.store.dispatch(UsersActions.selectFromResolver({ user: this.resolvedUser }));
  }

  goBack(): void {
    this.router.navigate(['/users']);
  }

  onEdit(user: User): void {
    this.router.navigate(['/users', user.id, 'edit']);
  }

  onDelete(user: User): void {
    if (confirm(`Excluir ${user.name}?`)) {
      this.store.dispatch(UsersActions.remove({ userId: user.id }));
      this.router.navigate(['/users']);
    }
  }
}
```

---

## Page de criação/edição (com Form)

```typescript
// src/app/features/users/pages/user-form-page/user-form-page.component.ts
import {
  Component, inject, ChangeDetectionStrategy, OnInit
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { toSignal } from '@angular/core/rxjs-interop';
import { CommonModule } from '@angular/common';
import { UsersActions } from '../../store/users.actions';
import { selectUsersLoading, selectUsersSaveSuccess } from '../../store/users.selectors';
import { UserFormComponent } from '../../components/user-form/user-form.component';
import { User, CreateUserDto, UpdateUserDto } from '../../../../core/models/user.model';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-user-form-page',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, UserFormComponent],
  template: `
    <div class="page-header">
      <button (click)="goBack()">← Voltar</button>
      <h1>{{ isEditMode ? 'Editar Usuário' : 'Novo Usuário' }}</h1>
    </div>

    <app-user-form
      [user]="editUser"
      [loading]="loading()"
      (save)="onSave($event)"
      (cancel)="goBack()"
    />
  `
})
export class UserFormPageComponent implements OnInit {
  private readonly store  = inject(Store);
  private readonly route  = inject(ActivatedRoute);
  private readonly router = inject(Router);

  readonly loading     = toSignal(this.store.select(selectUsersLoading),     { initialValue: false });
  readonly saveSuccess = toSignal(this.store.select(selectUsersSaveSuccess), { initialValue: false });

  readonly editUser: User | null = this.route.snapshot.data['user'] ?? null;
  readonly isEditMode = !!this.editUser;

  constructor() {
    // Navega após salvar com sucesso
    this.store.select(selectUsersSaveSuccess).pipe(
      filter(Boolean),
      takeUntilDestroyed()
    ).subscribe(() => this.router.navigate(['/users']));
  }

  ngOnInit(): void {
    if (this.isEditMode && this.editUser) {
      this.store.dispatch(UsersActions.selectFromResolver({ user: this.editUser }));
    }
  }

  onSave(dto: CreateUserDto | UpdateUserDto): void {
    if (this.isEditMode && this.editUser) {
      this.store.dispatch(UsersActions.update({ userId: this.editUser.id, dto: dto as UpdateUserDto }));
    } else {
      this.store.dispatch(UsersActions.create({ dto: dto as CreateUserDto }));
    }
  }

  goBack(): void {
    this.router.navigate(['/users']);
  }
}
```
