# Shared UI Library — Referência

## Escolha da biblioteca

| Biblioteca | Quando escolher |
|---|---|
| **Angular Material** | Design system Google/Material, projetos corporativos, acessibilidade nativa |
| **PrimeNG** | Muitos componentes de dados (tabelas, charts, calendars), projetos empresariais |
| **Tailwind CSS** | Máxima customização visual, design system próprio, controle total |
| **Nenhuma (CSS puro)** | Projetos pequenos, design muito específico |

---

## Angular Material — configuração e wrappers

### Instalação

```bash
ng add @angular/material
# ou
npm install @angular/material @angular/cdk
```

### Configuração no app.config.ts

```typescript
// src/app/app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MAT_DATE_LOCALE } from '@angular/material/core';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS } from '@angular/material/form-field';
import { MAT_SNACK_BAR_DEFAULT_OPTIONS } from '@angular/material/snack-bar';
import { MAT_DIALOG_DEFAULT_OPTIONS } from '@angular/material/dialog';

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimationsAsync(),

    // Locale pt-BR para datepicker
    { provide: MAT_DATE_LOCALE, useValue: 'pt-BR' },

    // Aparência padrão dos campos
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: { appearance: 'outline', subscriptSizing: 'dynamic' }
    },

    // Duração padrão do snackbar
    {
      provide: MAT_SNACK_BAR_DEFAULT_OPTIONS,
      useValue: { duration: 4000, horizontalPosition: 'right', verticalPosition: 'top' }
    },

    // Dialog com largura padrão
    {
      provide: MAT_DIALOG_DEFAULT_OPTIONS,
      useValue: { width: '560px', maxWidth: '90vw', panelClass: 'app-dialog' }
    }
  ]
};
```

### Tema customizado (Angular Material 17+ com M3)

```scss
// src/styles/_theme.scss
@use '@angular/material' as mat;

$primary:   mat.define-palette(mat.$indigo-palette);
$accent:    mat.define-palette(mat.$pink-palette, A200, A100, A400);
$warn:      mat.define-palette(mat.$red-palette);

$theme: mat.define-light-theme((
  color:      (primary: $primary, accent: $accent, warn: $warn),
  typography: mat.define-typography-config(),
  density:    0
));

@include mat.all-component-themes($theme);

// Dark mode
@media (prefers-color-scheme: dark) {
  $dark-theme: mat.define-dark-theme((
    color: (primary: $primary, accent: $accent, warn: $warn)
  ));
  @include mat.all-component-colors($dark-theme);
}
```

```scss
// src/styles.scss
@use 'styles/theme';
```

### Wrapper: MatDialogService

```typescript
// src/app/shared/ui/mat-dialog.service.ts
import { Injectable, inject } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { ConfirmDialogComponent } from '../components/confirm-dialog/confirm-dialog.component';

@Injectable({ providedIn: 'root' })
export class UiService {
  private readonly dialog   = inject(MatDialog);
  private readonly snackBar = inject(MatSnackBar);

  // Abre diálogo de confirmação padronizado
  confirm(message: string, title = 'Confirmar'): Observable<boolean> {
    return this.dialog.open(ConfirmDialogComponent, {
      data: { message, title },
      width: '400px',
      disableClose: true
    }).afterClosed();
  }

  // Abre qualquer componente como dialog
  openDialog<T, D = unknown, R = unknown>(
    component: new (...args: unknown[]) => T,
    config?: MatDialogConfig<D>
  ): Observable<R> {
    return this.dialog.open(component, config).afterClosed() as Observable<R>;
  }

  success(message: string): void {
    this.snackBar.open(message, '✕', { panelClass: ['snack-success'] });
  }

  error(message: string): void {
    this.snackBar.open(message, '✕', { panelClass: ['snack-error'] });
  }

  warning(message: string): void {
    this.snackBar.open(message, '✕', { panelClass: ['snack-warning'] });
  }
}
```

### ConfirmDialogComponent (Material)

```typescript
// src/app/shared/components/confirm-dialog/confirm-dialog.component.ts
import { Component, inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

export interface ConfirmDialogData {
  title:   string;
  message: string;
  confirm?: string;
  cancel?:  string;
}

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>{{ data.title }}</h2>
    <mat-dialog-content>{{ data.message }}</mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="ref.close(false)">
        {{ data.cancel ?? 'Cancelar' }}
      </button>
      <button mat-flat-button color="primary" (click)="ref.close(true)">
        {{ data.confirm ?? 'Confirmar' }}
      </button>
    </mat-dialog-actions>
  `
})
export class ConfirmDialogComponent {
  readonly data = inject<ConfirmDialogData>(MAT_DIALOG_DATA);
  readonly ref  = inject(MatDialogRef<ConfirmDialogComponent>);
}
```

### Componente com Material (exemplo completo)

```typescript
// src/app/shared/components/data-table/data-table.component.ts
import { Component, ChangeDetectionStrategy, input, output } from '@angular/core';
import { MatTableModule }     from '@angular/material/table';
import { MatSortModule, Sort } from '@angular/material/sort';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule }       from '@angular/material/icon';
import { MatButtonModule }     from '@angular/material/button';
import { CommonModule }        from '@angular/common';

@Component({
  selector: 'app-data-table',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    CommonModule, MatTableModule, MatSortModule,
    MatPaginatorModule, MatProgressBarModule,
    MatIconModule, MatButtonModule
  ],
  template: `
    @if (loading()) { <mat-progress-bar mode="indeterminate" /> }

    <table mat-table [dataSource]="rows()" matSort (matSortChange)="sortChange.emit($event)">
      <ng-content />
      <tr mat-header-row *matHeaderRowDef="displayedColumns()"></tr>
      <tr mat-row *matRowDef="let row; columns: displayedColumns();"
          (click)="rowClick.emit(row)"></tr>
    </table>

    <mat-paginator
      [length]="totalCount()"
      [pageSize]="pageSize()"
      [pageSizeOptions]="[10, 20, 50]"
      (page)="pageChange.emit($event)"
      showFirstLastButtons
    />
  `
})
export class DataTableComponent<T> {
  readonly rows             = input.required<T[]>();
  readonly displayedColumns = input.required<string[]>();
  readonly totalCount       = input<number>(0);
  readonly pageSize         = input<number>(20);
  readonly loading          = input<boolean>(false);

  readonly rowClick    = output<T>();
  readonly sortChange  = output<Sort>();
  readonly pageChange  = output<PageEvent>();
}
```

---

## PrimeNG — configuração e uso

### Instalação

```bash
npm install primeng primeicons
```

### Configuração no app.config.ts

```typescript
// src/app/app.config.ts
import { ApplicationConfig }    from '@angular/core';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { providePrimeNG }       from 'primeng/config';
import Aura from '@primeng/themes/aura';

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimationsAsync(),
    providePrimeNG({
      theme: {
        preset: Aura,
        options: {
          darkModeSelector: '.dark',  // toggle manual
          cssLayer: { name: 'primeng', order: 'tailwind-base, primeng, tailwind-utilities' }
        }
      },
      ripple: true,
      inputStyle: 'outlined'
    })
  ]
};
```

### Wrapper: PrimeNG Table com funcionalidades completas

```typescript
// src/app/shared/components/prime-table/prime-table.component.ts
import { Component, ChangeDetectionStrategy, input, output } from '@angular/core';
import { CommonModule }        from '@angular/common';
import { TableModule }         from 'primeng/table';
import { ButtonModule }        from 'primeng/button';
import { TagModule }           from 'primeng/tag';
import { SkeletonModule }      from 'primeng/skeleton';

export interface PrimeColumn {
  field:    string;
  header:   string;
  sortable?: boolean;
  width?:   string;
}

@Component({
  selector: 'app-prime-table',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, TableModule, ButtonModule, TagModule, SkeletonModule],
  template: `
    <p-table
      [value]="rows()"
      [loading]="loading()"
      [paginator]="true"
      [rows]="pageSize()"
      [totalRecords]="totalCount()"
      [lazy]="true"
      (onLazyLoad)="lazyLoad.emit($event)"
      [sortMode]="'single'"
      [rowHover]="true"
      [scrollable]="true"
      styleClass="p-datatable-gridlines p-datatable-sm"
    >
      <ng-template pTemplate="header">
        <tr>
          @for (col of columns(); track col.field) {
            <th [pSortableColumn]="col.sortable ? col.field : ''"
                [style.width]="col.width">
              {{ col.header }}
              @if (col.sortable) { <p-sortIcon [field]="col.field" /> }
            </th>
          }
          @if (hasActions()) { <th style="width: 100px">Ações</th> }
        </tr>
      </ng-template>

      <ng-template pTemplate="body" let-row>
        <tr (click)="rowClick.emit(row)">
          @for (col of columns(); track col.field) {
            <td>{{ row[col.field] }}</td>
          }
          @if (hasActions()) {
            <td>
              <ng-content select="[row-actions]" />
            </td>
          }
        </tr>
      </ng-template>

      <ng-template pTemplate="emptymessage">
        <tr><td [attr.colspan]="columns().length">
          Nenhum registro encontrado.
        </td></tr>
      </ng-template>
    </p-table>
  `
})
export class PrimeTableComponent<T extends Record<string, unknown>> {
  readonly columns    = input.required<PrimeColumn[]>();
  readonly rows       = input.required<T[]>();
  readonly totalCount = input<number>(0);
  readonly pageSize   = input<number>(20);
  readonly loading    = input<boolean>(false);
  readonly hasActions = input<boolean>(false);

  readonly rowClick  = output<T>();
  readonly lazyLoad  = output<unknown>();
}
```

---

## Tailwind CSS — configuração e tokens

### Instalação

```bash
npm install tailwindcss @tailwindcss/forms
npx tailwindcss init
```

### tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50:  '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          900: '#1e3a8a'
        },
        surface: {
          0:    '#ffffff',
          50:   '#f8fafc',
          100:  '#f1f5f9',
          200:  '#e2e8f0',
          border: '#e5e7eb'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      borderRadius: {
        'card': '12px',
        'btn':  '8px'
      }
    }
  },
  plugins: [require('@tailwindcss/forms')]
};
```

### Tokens e classes utilitárias customizadas

```scss
// src/styles/_utilities.scss
@layer utilities {
  .card-base {
    @apply bg-white rounded-card border border-surface-border shadow-sm p-6;
  }
  .btn-primary {
    @apply bg-primary-600 hover:bg-primary-700 text-white font-medium
           px-4 py-2 rounded-btn transition-colors disabled:opacity-50;
  }
  .btn-secondary {
    @apply border border-surface-200 hover:bg-surface-50 text-gray-700
           font-medium px-4 py-2 rounded-btn transition-colors;
  }
  .form-label {
    @apply block text-sm font-medium text-gray-700 mb-1;
  }
  .form-input {
    @apply w-full border-surface-200 rounded-btn text-sm
           focus:ring-primary-500 focus:border-primary-500;
  }
  .badge-green  { @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800; }
  .badge-red    { @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800; }
  .badge-yellow { @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800; }
  .badge-blue   { @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800; }
}
```

### Exemplo de componente com Tailwind

```typescript
// src/app/shared/components/stats-card/stats-card.component.ts
import { Component, ChangeDetectionStrategy, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stats-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: `
    <div class="card-base flex items-center gap-4">
      @if (icon()) {
        <div class="w-12 h-12 rounded-xl flex items-center justify-content-center text-2xl"
             [class]="iconBg()">
          {{ icon() }}
        </div>
      }
      <div class="flex-1">
        <p class="text-sm text-gray-500 font-medium">{{ label() }}</p>
        <p class="text-2xl font-bold text-gray-900 mt-0.5">{{ value() }}</p>
        @if (change()) {
          <p class="text-xs mt-1" [class]="changeClass()">
            {{ change()! > 0 ? '↑' : '↓' }} {{ change()! | number:'1.1-1' }}%
          </p>
        }
      </div>
    </div>
  `
})
export class StatsCardComponent {
  readonly label   = input.required<string>();
  readonly value   = input.required<string | number>();
  readonly icon    = input<string>('');
  readonly iconBg  = input<string>('bg-blue-50');
  readonly change  = input<number | null>(null);

  readonly changeClass = () => {
    const c = this.change();
    if (c == null) return '';
    return c > 0 ? 'text-green-600' : 'text-red-600';
  };
}
```

---

## Qual biblioteca usar em qual situação

```typescript
// ✅ Angular Material — forms complexos, acessibilidade, data tables
import { MatTableModule, MatSortModule, MatPaginatorModule } from '@angular/material/...';
import { MatDatepickerModule, MatNativeDateModule }          from '@angular/material/...';
import { MatAutocompleteModule }                             from '@angular/material/...';

// ✅ PrimeNG — dashboards, charts, file upload, rich calendar
import { ChartModule }        from 'primeng/chart';
import { FileUploadModule }   from 'primeng/fileupload';
import { CalendarModule }     from 'primeng/calendar';
import { EditorModule }       from 'primeng/editor';

// ✅ Tailwind — layout, espaçamento, responsividade, tokens do design system
// Usar nas classes do template, combinando com os componentes acima

// ✅ Sem biblioteca — componentes simples e totalmente customizados
// ButtonComponent, BadgeComponent, AvatarComponent da camada Shared
```
