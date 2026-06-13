# Feature Store NgRx — Referência

## Estrutura completa

```
features/users/store/
├── users.state.ts       → Interface do estado
├── users.actions.ts     → Actions (createActionGroup)
├── users.reducer.ts     → Reducer (createFeature + createEntityAdapter)
├── users.effects.ts     → Effects (side-effects: HTTP, SignalR)
└── users.selectors.ts   → Selectors (memoizados com createSelector)
```

---

## State

```typescript
// src/app/features/users/store/users.state.ts
import { EntityState, createEntityAdapter } from '@ngrx/entity';
import { User } from '../../../core/models/user.model';

export interface UsersState extends EntityState<User> {
  selectedUserId: string | null;
  loading:        boolean;
  saveSuccess:    boolean;
  error:          string | null;
  filters:        Record<string, string>;
  totalCount:     number;
}

// EntityAdapter gerencia ids[] e entities{} automaticamente
export const usersAdapter = createEntityAdapter<User>({
  selectId: (user) => user.id,
  sortComparer: (a, b) => a.name.localeCompare(b.name)
});

export const initialUsersState: UsersState = usersAdapter.getInitialState({
  selectedUserId: null,
  loading:        false,
  saveSuccess:    false,
  error:          null,
  filters:        {},
  totalCount:     0
});
```

---

## Actions

```typescript
// src/app/features/users/store/users.actions.ts
import { createActionGroup, emptyProps, props } from '@ngrx/store';
import { User, CreateUserDto, UpdateUserDto } from '../../../core/models/user.model';

export const UsersActions = createActionGroup({
  source: 'Users',
  events: {
    // ── Listagem ──────────────────────────────────────────
    'Load All':         emptyProps(),
    'Load All Success': props<{ users: User[]; totalCount: number }>(),
    'Load All Failure': props<{ error: string }>(),

    // ── Seleção ───────────────────────────────────────────
    'Select':               props<{ userId: string }>(),
    'Select From Resolver': props<{ user: User }>(),

    // ── Criação ───────────────────────────────────────────
    'Create':         props<{ dto: CreateUserDto }>(),
    'Create Success': props<{ user: User }>(),
    'Create Failure': props<{ error: string }>(),

    // ── Edição ────────────────────────────────────────────
    'Update':         props<{ userId: string; dto: UpdateUserDto }>(),
    'Update Success': props<{ user: User }>(),
    'Update Failure': props<{ error: string }>(),

    // ── Remoção ───────────────────────────────────────────
    'Remove':         props<{ userId: string }>(),
    'Remove Success': props<{ userId: string }>(),
    'Remove Failure': props<{ error: string }>(),

    // ── Filtros ───────────────────────────────────────────
    'Apply Filters': props<{ filters: Record<string, string> }>(),
    'Clear Filters': emptyProps(),

    // ── Reset ─────────────────────────────────────────────
    'Reset Save Status': emptyProps()
  }
});
```

---

## Reducer

```typescript
// src/app/features/users/store/users.reducer.ts
import { createFeature, createReducer, on } from '@ngrx/store';
import { UsersActions } from './users.actions';
import { initialUsersState, usersAdapter } from './users.state';

export const usersFeature = createFeature({
  name: 'users',  // deve bater com provideState() no routing
  reducer: createReducer(
    initialUsersState,

    // ── Listagem ──────────────────────────────────────────
    on(UsersActions.loadAll, state => ({
      ...state, loading: true, error: null
    })),
    on(UsersActions.loadAllSuccess, (state, { users, totalCount }) =>
      usersAdapter.setAll(users, { ...state, loading: false, totalCount })
    ),
    on(UsersActions.loadAllFailure, (state, { error }) => ({
      ...state, loading: false, error
    })),

    // ── Seleção ───────────────────────────────────────────
    on(UsersActions.select, (state, { userId }) => ({
      ...state, selectedUserId: userId
    })),
    on(UsersActions.selectFromResolver, (state, { user }) =>
      usersAdapter.upsertOne(user, { ...state, selectedUserId: user.id })
    ),

    // ── Criação ───────────────────────────────────────────
    on(UsersActions.create, state => ({
      ...state, loading: true, saveSuccess: false, error: null
    })),
    on(UsersActions.createSuccess, (state, { user }) =>
      usersAdapter.addOne(user, {
        ...state, loading: false, saveSuccess: true,
        totalCount: state.totalCount + 1
      })
    ),
    on(UsersActions.createFailure, (state, { error }) => ({
      ...state, loading: false, error
    })),

    // ── Edição ────────────────────────────────────────────
    on(UsersActions.update, state => ({
      ...state, loading: true, saveSuccess: false, error: null
    })),
    on(UsersActions.updateSuccess, (state, { user }) =>
      usersAdapter.updateOne(
        { id: user.id, changes: user },
        { ...state, loading: false, saveSuccess: true }
      )
    ),
    on(UsersActions.updateFailure, (state, { error }) => ({
      ...state, loading: false, error
    })),

    // ── Remoção ───────────────────────────────────────────
    on(UsersActions.remove, state => ({ ...state, loading: true, error: null })),
    on(UsersActions.removeSuccess, (state, { userId }) =>
      usersAdapter.removeOne(userId, {
        ...state, loading: false, selectedUserId: null,
        totalCount: state.totalCount - 1
      })
    ),
    on(UsersActions.removeFailure, (state, { error }) => ({
      ...state, loading: false, error
    })),

    // ── Filtros ───────────────────────────────────────────
    on(UsersActions.applyFilters, (state, { filters }) => ({
      ...state, filters
    })),
    on(UsersActions.clearFilters, state => ({ ...state, filters: {} })),

    // ── Reset ─────────────────────────────────────────────
    on(UsersActions.resetSaveStatus, state => ({ ...state, saveSuccess: false }))
  )
});

// Exporta reducer para registro no routing
export const { name: usersFeatureName, reducer: usersReducer } = usersFeature;
```

---

## Effects

```typescript
// src/app/features/users/store/users.effects.ts
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { switchMap, map, catchError, withLatestFrom, tap } from 'rxjs/operators';
import { of } from 'rxjs';
import { Router } from '@angular/router';
import { UsersActions } from './users.actions';
import { selectUsersFilters } from './users.selectors';
import { UserApiService } from '../../../core/http/user-api.service';

@Injectable()
export class UsersEffects {
  private readonly actions$ = inject(Actions);
  private readonly store    = inject(Store);
  private readonly api      = inject(UserApiService);
  private readonly router   = inject(Router);

  // ── Listagem ────────────────────────────────────────────
  loadAll$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.loadAll, UsersActions.applyFilters),
      withLatestFrom(this.store.select(selectUsersFilters)),
      switchMap(([, filters]) =>
        this.api.getAll(1, 20, filters).pipe(
          map(result => UsersActions.loadAllSuccess({
            users: result.items,
            totalCount: result.totalCount
          })),
          catchError(err => of(UsersActions.loadAllFailure({ error: err.message })))
        )
      )
    )
  );

  // ── Criação ─────────────────────────────────────────────
  create$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.create),
      switchMap(({ dto }) =>
        this.api.create(dto).pipe(
          map(user => UsersActions.createSuccess({ user })),
          catchError(err => of(UsersActions.createFailure({ error: err.message })))
        )
      )
    )
  );

  // ── Edição ──────────────────────────────────────────────
  update$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.update),
      switchMap(({ userId, dto }) =>
        this.api.update(userId, dto).pipe(
          map(user => UsersActions.updateSuccess({ user })),
          catchError(err => of(UsersActions.updateFailure({ error: err.message })))
        )
      )
    )
  );

  // ── Remoção ─────────────────────────────────────────────
  remove$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.remove),
      switchMap(({ userId }) =>
        this.api.remove(userId).pipe(
          map(() => UsersActions.removeSuccess({ userId })),
          catchError(err => of(UsersActions.removeFailure({ error: err.message })))
        )
      )
    )
  );

  // ── Navegação pós-sucesso (sem dispatch) ─────────────────
  navigateAfterRemove$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.removeSuccess),
      tap(() => this.router.navigate(['/users']))
    ),
    { dispatch: false }
  );
}
```

---

## Selectors

```typescript
// src/app/features/users/store/users.selectors.ts
import { createSelector } from '@ngrx/store';
import { usersFeature } from './users.reducer';
import { usersAdapter } from './users.state';
import { toUserViewModel } from '../../../core/models/user.model';

// Selectors base do EntityAdapter
const {
  selectAll,
  selectEntities,
  selectIds,
  selectTotal
} = usersAdapter.getSelectors();

// Feature selectors gerados pelo createFeature
export const {
  selectUsersState,
  selectLoading:     selectUsersLoading,
  selectError:       selectUsersError,
  selectSaveSuccess: selectUsersSaveSuccess,
  selectFilters:     selectUsersFilters,
  selectTotalCount:  selectUsersTotalCount,
  selectSelectedUserId
} = usersFeature;

// Selectors de entidades
export const selectUsersAll      = createSelector(selectUsersState, selectAll);
export const selectUsersEntities = createSelector(selectUsersState, selectEntities);
export const selectUsersCount    = createSelector(selectUsersState, selectTotal);

// Selector do usuário selecionado
export const selectSelectedUser = createSelector(
  selectUsersEntities,
  selectSelectedUserId,
  (entities, id) => (id ? entities[id] ?? null : null)
);

// Selector com transformação para ViewModel
export const selectUserViewModels = createSelector(
  selectUsersAll,
  users => users.map(toUserViewModel)
);

// Selector com filtro aplicado
export const selectFilteredUsers = createSelector(
  selectUsersAll,
  selectUsersFilters,
  (users, filters) => {
    if (!filters['search']) return users;
    const term = filters['search'].toLowerCase();
    return users.filter(u =>
      u.name.toLowerCase().includes(term) ||
      u.email.toLowerCase().includes(term)
    );
  }
);

// Selector de estado de UI
export const selectUsersUiState = createSelector(
  selectUsersLoading,
  selectUsersError,
  selectUsersTotalCount,
  (loading, error, totalCount) => ({ loading, error, totalCount })
);
```
