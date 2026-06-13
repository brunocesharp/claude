# Shared Pipes — Referência

## Princípios

- **Sempre puros** (`pure: true` é o padrão — não alterar)
- **Standalone**: importar diretamente no componente
- **Sem side-effects**: mesma entrada → mesma saída, sempre
- **Locale-aware**: usar `LOCALE_ID` para formatações regionais

---

## Registro do locale pt-BR no app.config.ts

```typescript
// src/app/app.config.ts
import { ApplicationConfig, LOCALE_ID } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';

registerLocaleData(localePt);

export const appConfig: ApplicationConfig = {
  providers: [
    { provide: LOCALE_ID, useValue: 'pt-BR' }
  ]
};
```

---

## DateFormatPipe — formatação de datas

```typescript
// src/app/shared/pipes/date-format.pipe.ts
import { Pipe, PipeTransform, inject, LOCALE_ID } from '@angular/core';
import { DatePipe } from '@angular/common';

export type DatePreset =
  | 'short'       // 01/01/2024
  | 'long'        // 1 de janeiro de 2024
  | 'datetime'    // 01/01/2024 14:30
  | 'time'        // 14:30
  | 'relative'    // há 3 dias
  | 'fromNow';    // em 2 horas

@Pipe({ name: 'dateFormat', standalone: true })
export class DateFormatPipe implements PipeTransform {
  private readonly locale = inject(LOCALE_ID);
  private readonly datePipe = new DatePipe(this.locale);

  transform(value: string | Date | null | undefined, preset: DatePreset = 'short'): string {
    if (!value) return '—';

    const date = value instanceof Date ? value : new Date(value);
    if (isNaN(date.getTime())) return '—';

    switch (preset) {
      case 'short':
        return this.datePipe.transform(date, 'dd/MM/yyyy') ?? '—';
      case 'long':
        return this.datePipe.transform(date, "d 'de' MMMM 'de' yyyy") ?? '—';
      case 'datetime':
        return this.datePipe.transform(date, 'dd/MM/yyyy HH:mm') ?? '—';
      case 'time':
        return this.datePipe.transform(date, 'HH:mm') ?? '—';
      case 'relative':
        return this.toRelative(date);
      case 'fromNow':
        return this.fromNow(date);
      default:
        return this.datePipe.transform(date, preset) ?? '—';
    }
  }

  private toRelative(date: Date): string {
    const diffMs   = Date.now() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHrs  = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHrs / 24);

    if (diffMins < 1)   return 'agora mesmo';
    if (diffMins < 60)  return `há ${diffMins} min`;
    if (diffHrs  < 24)  return `há ${diffHrs}h`;
    if (diffDays < 7)   return `há ${diffDays} dias`;
    if (diffDays < 30)  return `há ${Math.floor(diffDays / 7)} sem`;
    if (diffDays < 365) return `há ${Math.floor(diffDays / 30)} meses`;
    return `há ${Math.floor(diffDays / 365)} anos`;
  }

  private fromNow(date: Date): string {
    const diffMs   = date.getTime() - Date.now();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHrs  = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHrs / 24);

    if (diffMins < 0)   return 'vencido';
    if (diffMins < 60)  return `em ${diffMins} min`;
    if (diffHrs  < 24)  return `em ${diffHrs}h`;
    return `em ${diffDays} dias`;
  }
}
```

**Uso:**
```html
<span>{{ user.createdAt | dateFormat }}</span>           <!-- 15/03/2024 -->
<span>{{ user.createdAt | dateFormat:'long' }}</span>    <!-- 15 de março de 2024 -->
<span>{{ user.createdAt | dateFormat:'relative' }}</span><!-- há 3 dias -->
<span>{{ task.dueDate  | dateFormat:'fromNow' }}</span>  <!-- em 2 dias -->
```

---

## CurrencyBrPipe — moeda brasileira

```typescript
// src/app/shared/pipes/currency-br.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'currencyBr', standalone: true })
export class CurrencyBrPipe implements PipeTransform {
  transform(
    value: number | null | undefined,
    options: { symbol?: boolean; decimals?: number } = {}
  ): string {
    if (value == null || isNaN(value)) return '—';

    const { symbol = true, decimals = 2 } = options;

    const formatted = new Intl.NumberFormat('pt-BR', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value);

    return symbol ? `R$ ${formatted}` : formatted;
  }
}
```

**Uso:**
```html
{{ product.price | currencyBr }}                        <!-- R$ 1.299,90 -->
{{ product.price | currencyBr:{ symbol: false } }}      <!-- 1.299,90 -->
{{ product.price | currencyBr:{ decimals: 0 } }}        <!-- R$ 1.300 -->
```

---

## TruncatePipe — texto longo

```typescript
// src/app/shared/pipes/truncate.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'truncate', standalone: true })
export class TruncatePipe implements PipeTransform {
  transform(
    value: string | null | undefined,
    limit  = 100,
    suffix = '...'
  ): string {
    if (!value) return '';
    if (value.length <= limit) return value;
    // Não corta no meio de uma palavra
    const trimmed = value.slice(0, limit);
    const lastSpace = trimmed.lastIndexOf(' ');
    return (lastSpace > 0 ? trimmed.slice(0, lastSpace) : trimmed) + suffix;
  }
}
```

---

## CpfPipe e CnpjPipe — documentos brasileiros

```typescript
// src/app/shared/pipes/document.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'cpf', standalone: true })
export class CpfPipe implements PipeTransform {
  transform(value: string | null | undefined): string {
    if (!value) return '—';
    const digits = value.replace(/\D/g, '');
    if (digits.length !== 11) return value;
    return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  }
}

@Pipe({ name: 'cnpj', standalone: true })
export class CnpjPipe implements PipeTransform {
  transform(value: string | null | undefined): string {
    if (!value) return '—';
    const digits = value.replace(/\D/g, '');
    if (digits.length !== 14) return value;
    return digits.replace(
      /(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/,
      '$1.$2.$3/$4-$5'
    );
  }
}
```

---

## FileSizePipe — tamanho de arquivos

```typescript
// src/app/shared/pipes/file-size.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'fileSize', standalone: true })
export class FileSizePipe implements PipeTransform {
  private readonly units = ['B', 'KB', 'MB', 'GB', 'TB'];

  transform(bytes: number | null | undefined, decimals = 1): string {
    if (bytes == null || isNaN(bytes)) return '—';
    if (bytes === 0) return '0 B';

    const k     = 1024;
    const i     = Math.floor(Math.log(bytes) / Math.log(k));
    const value = bytes / Math.pow(k, i);

    return `${value.toFixed(decimals)} ${this.units[i]}`;
  }
}
```

---

## PhonePipe — telefone brasileiro

```typescript
// src/app/shared/pipes/phone.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'phone', standalone: true })
export class PhonePipe implements PipeTransform {
  transform(value: string | null | undefined): string {
    if (!value) return '—';
    const digits = value.replace(/\D/g, '');

    if (digits.length === 11) {
      // Celular: (11) 99999-9999
      return digits.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    }
    if (digits.length === 10) {
      // Fixo: (11) 3333-3333
      return digits.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    }
    return value;
  }
}
```

---

## Importando pipes em componentes standalone

```typescript
// Em qualquer componente standalone
import { DateFormatPipe }  from '../../shared/pipes/date-format.pipe';
import { CurrencyBrPipe }  from '../../shared/pipes/currency-br.pipe';
import { TruncatePipe }    from '../../shared/pipes/truncate.pipe';
import { CpfPipe }         from '../../shared/pipes/document.pipe';
import { FileSizePipe }    from '../../shared/pipes/file-size.pipe';

@Component({
  imports: [DateFormatPipe, CurrencyBrPipe, TruncatePipe, CpfPipe, FileSizePipe],
  template: `
    <td>{{ user.birthDate  | dateFormat:'long' }}</td>
    <td>{{ order.total     | currencyBr }}</td>
    <td>{{ product.desc    | truncate:80 }}</td>
    <td>{{ user.cpf        | cpf }}</td>
    <td>{{ file.size       | fileSize }}</td>
  `
})
export class MyComponent {}
```
