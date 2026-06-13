# Shared Dumb Components — Referência

## Regra de ouro

Um Dumb Component da camada Shared:
- Recebe dados via `input()` — nunca injeta Store ou serviços de negócio
- Emite eventos via `output()` — nunca navega ou chama HTTP diretamente
- É `standalone: true` e `OnPush`
- Tem nome **genérico** (não vinculado a uma feature)

---

## ButtonComponent

```typescript
// src/app/shared/components/button/button.component.ts
import {
  Component, ChangeDetectionStrategy, input, output
} from '@angular/core';
import { CommonModule } from '@angular/common';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost';
export type ButtonSize    = 'sm' | 'md' | 'lg';

@Component({
  selector: 'app-button',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    <button
      [type]="type()"
      [disabled]="disabled() || loading()"
      [class]="buttonClasses()"
      (click)="clicked.emit()"
    >
      @if (loading()) {
        <span class="spinner" aria-hidden="true"></span>
      }
      <ng-content />
    </button>
  `,
  styles: [`
    button { display: inline-flex; align-items: center; gap: 8px;
             border-radius: 6px; font-weight: 500; cursor: pointer;
             transition: all 0.2s; border: 1px solid transparent; }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    .sm { padding: 6px 12px; font-size: 13px; }
    .md { padding: 8px 16px; font-size: 14px; }
    .lg { padding: 12px 24px; font-size: 16px; }
    .primary   { background: #2563eb; color: #fff; }
    .secondary { background: transparent; border-color: #d1d5db; color: #374151; }
    .danger    { background: #dc2626; color: #fff; }
    .ghost     { background: transparent; color: #2563eb; }
    .spinner   { width: 14px; height: 14px; border: 2px solid currentColor;
                 border-top-color: transparent; border-radius: 50%;
                 animation: spin 0.6s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
  `]
})
export class ButtonComponent {
  readonly variant  = input<ButtonVariant>('primary');
  readonly size     = input<ButtonSize>('md');
  readonly type     = input<'button' | 'submit' | 'reset'>('button');
  readonly loading  = input<boolean>(false);
  readonly disabled = input<boolean>(false);

  readonly clicked = output<void>();

  readonly buttonClasses = () =>
    [this.variant(), this.size()].join(' ');
}
```

---

## CardComponent

```typescript
// src/app/shared/components/card/card.component.ts
import { Component, ChangeDetectionStrategy, input } from '@angular/core';

@Component({
  selector: 'app-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="card" [class.elevated]="elevated()" [class.bordered]="bordered()">
      @if (title()) {
        <div class="card-header">
          <h3 class="card-title">{{ title() }}</h3>
          @if (subtitle()) {
            <p class="card-subtitle">{{ subtitle() }}</p>
          }
          <ng-content select="[card-actions]" />
        </div>
      }
      <div class="card-body">
        <ng-content />
      </div>
      <ng-content select="[card-footer]" />
    </div>
  `,
  styles: [`
    .card { border-radius: 12px; background: #fff; overflow: hidden; }
    .bordered  { border: 1px solid #e5e7eb; }
    .elevated  { box-shadow: 0 1px 3px rgba(0,0,0,.1), 0 1px 2px rgba(0,0,0,.06); }
    .card-header { padding: 20px 24px 0; display: flex;
                   align-items: flex-start; justify-content: space-between; }
    .card-title    { font-size: 16px; font-weight: 600; color: #111827; margin: 0; }
    .card-subtitle { font-size: 13px; color: #6b7280; margin: 4px 0 0; }
    .card-body { padding: 20px 24px; }
  `]
})
export class CardComponent {
  readonly title    = input<string>('');
  readonly subtitle = input<string>('');
  readonly elevated = input<boolean>(true);
  readonly bordered = input<boolean>(false);
}
```

**Uso:**
```html
<app-card title="Usuários ativos" subtitle="Últimos 30 dias">
  <p>Conteúdo do card</p>
  <div card-actions>
    <app-button size="sm">Ver todos</app-button>
  </div>
</app-card>
```

---

## BadgeComponent

```typescript
// src/app/shared/components/badge/badge.component.ts
import { Component, ChangeDetectionStrategy, input } from '@angular/core';
import { CommonModule } from '@angular/common';

export type BadgeColor = 'gray' | 'blue' | 'green' | 'yellow' | 'red' | 'purple';
export type BadgeSize  = 'sm' | 'md';

@Component({
  selector: 'app-badge',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    <span [class]="'badge ' + color() + ' ' + size()">
      @if (dot()) { <span class="dot"></span> }
      <ng-content />
    </span>
  `,
  styles: [`
    .badge { display: inline-flex; align-items: center; gap: 5px;
             border-radius: 9999px; font-weight: 500; white-space: nowrap; }
    .sm { padding: 2px 8px; font-size: 11px; }
    .md { padding: 4px 10px; font-size: 12px; }
    .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
    .gray   { background: #f3f4f6; color: #374151; }
    .blue   { background: #eff6ff; color: #1d4ed8; }
    .green  { background: #f0fdf4; color: #15803d; }
    .yellow { background: #fefce8; color: #a16207; }
    .red    { background: #fef2f2; color: #b91c1c; }
    .purple { background: #faf5ff; color: #7e22ce; }
  `]
})
export class BadgeComponent {
  readonly color = input<BadgeColor>('gray');
  readonly size  = input<BadgeSize>('md');
  readonly dot   = input<boolean>(false);
}
```

---

## AvatarComponent

```typescript
// src/app/shared/components/avatar/avatar.component.ts
import { Component, ChangeDetectionStrategy, input, computed } from '@angular/core';
import { CommonModule } from '@angular/common';

export type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

@Component({
  selector: 'app-avatar',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    <div [class]="'avatar ' + size()" [title]="name()">
      @if (src()) {
        <img [src]="src()" [alt]="name()" (error)="onImgError($event)" />
      } @else {
        <span class="initials">{{ initials() }}</span>
      }
      @if (status()) {
        <span [class]="'status-dot ' + status()"></span>
      }
    </div>
  `,
  styles: [`
    .avatar { position: relative; display: inline-flex; align-items: center;
              justify-content: center; border-radius: 50%;
              background: #e0e7ff; color: #4338ca; font-weight: 600;
              overflow: hidden; flex-shrink: 0; }
    img { width: 100%; height: 100%; object-fit: cover; }
    .xs { width: 24px;  height: 24px;  font-size: 10px; }
    .sm { width: 32px;  height: 32px;  font-size: 12px; }
    .md { width: 40px;  height: 40px;  font-size: 14px; }
    .lg { width: 56px;  height: 56px;  font-size: 18px; }
    .xl { width: 72px;  height: 72px;  font-size: 24px; }
    .status-dot { position: absolute; bottom: 0; right: 0;
                  width: 25%; height: 25%; border-radius: 50%;
                  border: 2px solid white; }
    .online  { background: #22c55e; }
    .offline { background: #9ca3af; }
    .busy    { background: #ef4444; }
  `]
})
export class AvatarComponent {
  readonly name   = input.required<string>();
  readonly src    = input<string>('');
  readonly size   = input<AvatarSize>('md');
  readonly status = input<'online' | 'offline' | 'busy' | ''>('');

  readonly initials = computed(() =>
    this.name()
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  );

  onImgError(event: Event): void {
    (event.target as HTMLImageElement).style.display = 'none';
  }
}
```

---

## SpinnerComponent

```typescript
// src/app/shared/components/spinner/spinner.component.ts
import { Component, ChangeDetectionStrategy, input } from '@angular/core';

export type SpinnerSize = 'sm' | 'md' | 'lg' | 'xl';

@Component({
  selector: 'app-spinner',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div
      [class]="'spinner ' + size()"
      [style.color]="color()"
      role="status"
      [attr.aria-label]="label()"
    >
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="currentColor"
                stroke-width="3" stroke-linecap="round"
                stroke-dasharray="32" stroke-dashoffset="32"
                opacity="0.25"/>
        <circle cx="12" cy="12" r="10" stroke="currentColor"
                stroke-width="3" stroke-linecap="round"
                stroke-dasharray="32" stroke-dashoffset="24"/>
      </svg>
      @if (label()) {
        <span class="sr-only">{{ label() }}</span>
      }
    </div>
  `,
  styles: [`
    .spinner { display: inline-flex; animation: spin 0.75s linear infinite; }
    .spinner svg { display: block; }
    .sm  svg { width: 16px;  height: 16px; }
    .md  svg { width: 24px;  height: 24px; }
    .lg  svg { width: 40px;  height: 40px; }
    .xl  svg { width: 64px;  height: 64px; }
    .sr-only { position: absolute; width: 1px; height: 1px;
               overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; }
    @keyframes spin { to { transform: rotate(360deg); } }
  `]
})
export class SpinnerComponent {
  readonly size  = input<SpinnerSize>('md');
  readonly color = input<string>('currentColor');
  readonly label = input<string>('Carregando...');
}
```

---

## EmptyStateComponent

```typescript
// src/app/shared/components/empty-state/empty-state.component.ts
import { Component, ChangeDetectionStrategy, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-empty-state',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    <div class="empty-state">
      @if (icon()) {
        <div class="icon-wrapper" [innerHTML]="icon()"></div>
      }
      <h3 class="title">{{ title() }}</h3>
      @if (description()) {
        <p class="description">{{ description() }}</p>
      }
      @if (actionLabel()) {
        <button class="action-btn" (click)="action.emit()">
          {{ actionLabel() }}
        </button>
      }
      <ng-content />
    </div>
  `,
  styles: [`
    .empty-state { display: flex; flex-direction: column; align-items: center;
                   justify-content: center; padding: 48px 24px; text-align: center; gap: 12px; }
    .icon-wrapper { width: 64px; height: 64px; color: #9ca3af; }
    .title       { font-size: 18px; font-weight: 600; color: #111827; margin: 0; }
    .description { font-size: 14px; color: #6b7280; margin: 0; max-width: 360px; }
    .action-btn  { margin-top: 8px; padding: 10px 20px; background: #2563eb;
                   color: #fff; border: none; border-radius: 8px;
                   font-size: 14px; font-weight: 500; cursor: pointer; }
  `]
})
export class EmptyStateComponent {
  readonly title       = input.required<string>();
  readonly description = input<string>('');
  readonly icon        = input<string>('');       // SVG inline string
  readonly actionLabel = input<string>('');

  readonly action = output<void>();
}
```

**Uso:**
```html
<app-empty-state
  title="Nenhum usuário encontrado"
  description="Crie o primeiro usuário para começar."
  actionLabel="Criar usuário"
  (action)="onCreate()"
/>
```

---

## TableComponent genérico

```typescript
// src/app/shared/components/table/table.component.ts
import {
  Component, ChangeDetectionStrategy, input, output, computed
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { SpinnerComponent } from '../spinner/spinner.component';
import { EmptyStateComponent } from '../empty-state/empty-state.component';

export interface TableColumn<T = unknown> {
  key:       keyof T | string;
  header:    string;
  width?:    string;
  sortable?: boolean;
  align?:    'left' | 'center' | 'right';
}

@Component({
  selector: 'app-table',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, SpinnerComponent, EmptyStateComponent],
  template: `
    <div class="table-wrapper">
      @if (loading()) {
        <div class="loading-overlay">
          <app-spinner size="lg" />
        </div>
      }

      <table class="table">
        <thead>
          <tr>
            @for (col of columns(); track col.key) {
              <th
                [style.width]="col.width"
                [class.sortable]="col.sortable"
                [style.text-align]="col.align ?? 'left'"
                (click)="col.sortable && sortChange.emit(col.key as string)"
              >
                {{ col.header }}
                @if (col.sortable) {
                  <span class="sort-icon">↕</span>
                }
              </th>
            }
            @if (hasActions()) { <th class="actions-col">Ações</th> }
          </tr>
        </thead>
        <tbody>
          @if (!loading() && rows().length === 0) {
            <tr>
              <td [attr.colspan]="columns().length + (hasActions() ? 1 : 0)">
                <app-empty-state [title]="emptyMessage()" />
              </td>
            </tr>
          }
          @for (row of rows(); track trackBy()(row)) {
            <tr (click)="rowClick.emit(row)" [class.clickable]="rowClickable()">
              @for (col of columns(); track col.key) {
                <td [style.text-align]="col.align ?? 'left'">
                  {{ getCell(row, col.key as string) }}
                </td>
              }
              @if (hasActions()) {
                <td class="actions-col">
                  <ng-content select="[row-actions]" />
                </td>
              }
            </tr>
          }
        </tbody>
      </table>
    </div>
  `,
  styles: [`
    .table-wrapper { position: relative; overflow-x: auto; }
    .loading-overlay { position: absolute; inset: 0; background: rgba(255,255,255,.7);
                       display: flex; align-items: center; justify-content: center; z-index: 1; }
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th { padding: 12px 16px; background: #f9fafb; font-weight: 600;
         color: #374151; border-bottom: 1px solid #e5e7eb; white-space: nowrap; }
    td { padding: 14px 16px; color: #111827; border-bottom: 1px solid #f3f4f6; }
    tr:last-child td { border-bottom: none; }
    .sortable { cursor: pointer; user-select: none; }
    .sortable:hover { background: #f3f4f6; }
    .sort-icon { margin-left: 4px; opacity: 0.4; font-size: 11px; }
    .clickable { cursor: pointer; }
    .clickable:hover td { background: #f9fafb; }
    .actions-col { width: 80px; text-align: center; }
  `]
})
export class TableComponent<T extends Record<string, unknown>> {
  readonly columns      = input.required<TableColumn<T>[]>();
  readonly rows         = input.required<T[]>();
  readonly loading      = input<boolean>(false);
  readonly hasActions   = input<boolean>(false);
  readonly rowClickable = input<boolean>(false);
  readonly emptyMessage = input<string>('Nenhum registro encontrado.');
  readonly trackBy      = input<(row: T) => unknown>((row: T) => row['id']);

  readonly rowClick   = output<T>();
  readonly sortChange = output<string>();

  getCell(row: T, key: string): unknown {
    return key.split('.').reduce((obj: unknown, k) =>
      (obj as Record<string, unknown>)?.[k], row
    );
  }
}
```

---

## ModalComponent

```typescript
// src/app/shared/components/modal/modal.component.ts
import {
  Component, ChangeDetectionStrategy, input, output, OnChanges, SimpleChanges
} from '@angular/core';
import { CommonModule } from '@angular/common';

export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

@Component({
  selector: 'app-modal',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    @if (open()) {
      <div class="overlay" (click)="onOverlayClick($event)" role="dialog"
           [attr.aria-modal]="true" [attr.aria-label]="title()">
        <div [class]="'modal ' + size()">
          <div class="modal-header">
            <div class="modal-title-group">
              <h2 class="modal-title">{{ title() }}</h2>
              @if (subtitle()) {
                <p class="modal-subtitle">{{ subtitle() }}</p>
              }
            </div>
            @if (closable()) {
              <button class="close-btn" (click)="closed.emit()" aria-label="Fechar">✕</button>
            }
          </div>
          <div class="modal-body">
            <ng-content />
          </div>
          <ng-content select="[modal-footer]" />
        </div>
      </div>
    }
  `,
  styles: [`
    .overlay { position: fixed; inset: 0; background: rgba(0,0,0,.5);
               display: flex; align-items: center; justify-content: center;
               z-index: 1000; padding: 16px; animation: fadeIn .15s ease; }
    .modal   { background: #fff; border-radius: 12px; width: 100%;
               display: flex; flex-direction: column; max-height: 90vh;
               animation: slideUp .2s ease; overflow: hidden; }
    .sm   { max-width: 400px; }
    .md   { max-width: 560px; }
    .lg   { max-width: 720px; }
    .xl   { max-width: 960px; }
    .full { max-width: calc(100vw - 32px); height: calc(100vh - 32px); }
    .modal-header { display: flex; align-items: flex-start; justify-content: space-between;
                    padding: 24px 24px 0; gap: 16px; }
    .modal-title    { font-size: 18px; font-weight: 600; color: #111827; margin: 0; }
    .modal-subtitle { font-size: 13px; color: #6b7280; margin: 4px 0 0; }
    .close-btn { background: none; border: none; cursor: pointer; padding: 4px;
                 color: #9ca3af; font-size: 18px; line-height: 1; border-radius: 4px; }
    .close-btn:hover { background: #f3f4f6; color: #374151; }
    .modal-body { padding: 20px 24px; overflow-y: auto; flex: 1; }
    @keyframes fadeIn  { from { opacity: 0; }         to { opacity: 1; } }
    @keyframes slideUp { from { transform: translateY(12px); opacity: 0; }
                         to   { transform: translateY(0); opacity: 1; } }
  `]
})
export class ModalComponent {
  readonly open     = input.required<boolean>();
  readonly title    = input.required<string>();
  readonly subtitle = input<string>('');
  readonly size     = input<ModalSize>('md');
  readonly closable = input<boolean>(true);
  readonly closeOnOverlay = input<boolean>(true);

  readonly closed = output<void>();

  onOverlayClick(event: MouseEvent): void {
    if (this.closeOnOverlay() && event.target === event.currentTarget) {
      this.closed.emit();
    }
  }
}
```

**Uso:**
```html
<app-modal [open]="showModal" title="Confirmar exclusão" size="sm"
           (closed)="showModal = false">
  <p>Deseja excluir este registro?</p>
  <div modal-footer style="padding: 16px 24px; display: flex; gap: 8px; justify-content: flex-end">
    <app-button variant="secondary" (clicked)="showModal = false">Cancelar</app-button>
    <app-button variant="danger" (clicked)="onConfirm()">Excluir</app-button>
  </div>
</app-modal>
```
