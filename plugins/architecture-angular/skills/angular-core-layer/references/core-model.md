# Models e Interfaces — Referência

## Padrão de organização

```
core/models/
├── user.model.ts          → Entidade + DTOs + tipos relacionados
├── notification.model.ts
├── app-config.model.ts
└── shared.model.ts        → Tipos genéricos reutilizáveis (PagedResult, ApiResponse, etc.)
```

## Interface de entidade base

```typescript
// src/app/core/models/shared.model.ts

// Base para todas as entidades com id e auditoria
export interface BaseEntity {
  id: string;
  createdAt: string;
  updatedAt: string;
}

// Resultado paginado genérico — compatível com padrão .NET PagedResult
export interface PagedResult<T> {
  items: T[];
  totalCount: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Resposta padrão da API
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  errors?: Record<string, string[]>;
}

// Seleção em dropdown/combobox
export interface SelectOption<T = string> {
  label: string;
  value: T;
  disabled?: boolean;
}
```

## Modelo de entidade completo

```typescript
// src/app/core/models/user.model.ts
import { BaseEntity } from './shared.model';

// ─── Enums ───────────────────────────────────────────────
export enum UserRole {
  Admin = 'Admin',
  Manager = 'Manager',
  Viewer = 'Viewer'
}

export enum UserStatus {
  Active = 'Active',
  Inactive = 'Inactive',
  Pending = 'Pending'
}

// ─── Entidade principal ──────────────────────────────────
export interface User extends BaseEntity {
  name: string;
  email: string;
  avatarUrl?: string;
  roles: UserRole[];
  status: UserStatus;
  lastLoginAt?: string;
}

// ─── DTOs (Data Transfer Objects) ────────────────────────
// Usado em POST /users
export interface CreateUserDto {
  name: string;
  email: string;
  password: string;
  roles: UserRole[];
}

// Usado em PUT /users/:id
export interface UpdateUserDto {
  name?: string;
  email?: string;
  roles?: UserRole[];
  status?: UserStatus;
}

// Usado em POST /auth/login → resposta
export interface LoginResponseDto {
  user: User;
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

// ─── ViewModels (para componentes) ───────────────────────
// Dados formatados para exibição
export interface UserViewModel {
  id: string;
  displayName: string;
  email: string;
  roleLabel: string;
  statusLabel: string;
  statusColor: 'success' | 'warning' | 'danger';
  initials: string;
}

// ─── Mappers ─────────────────────────────────────────────
export function toUserViewModel(user: User): UserViewModel {
  return {
    id: user.id,
    displayName: user.name,
    email: user.email,
    roleLabel: user.roles.join(', '),
    statusLabel: user.status,
    statusColor: user.status === UserStatus.Active ? 'success'
      : user.status === UserStatus.Pending ? 'warning' : 'danger',
    initials: user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  };
}
```

## Modelo de Notification (SignalR)

```typescript
// src/app/core/models/notification.model.ts
import { BaseEntity } from './shared.model';

export enum NotificationType {
  Info = 'Info',
  Success = 'Success',
  Warning = 'Warning',
  Error = 'Error'
}

export interface Notification extends BaseEntity {
  title: string;
  message: string;
  type: NotificationType;
  isRead: boolean;
  userId: string;
  actionUrl?: string;
  actionLabel?: string;
}

export interface CreateNotificationDto {
  title: string;
  message: string;
  type: NotificationType;
  userId: string;
  actionUrl?: string;
}
```

## Type Guards (verificação em runtime)

```typescript
// src/app/core/models/user.model.ts — adicionar ao arquivo

export function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    'roles' in value
  );
}

export function isAdmin(user: User): boolean {
  return user.roles.includes(UserRole.Admin);
}
```

## Uso nos componentes e effects

```typescript
// Em componente
import { User, UserViewModel, toUserViewModel } from '../../core/models/user.model';

// Em NgRx State
export interface UsersState {
  users: User[];
  selectedUser: User | null;
  loading: boolean;
  error: string | null;
}

// Em NgRx Selector com mapeamento
export const selectUserViewModels = createSelector(
  selectAllUsers,
  (users): UserViewModel[] => users.map(toUserViewModel)
);
```
