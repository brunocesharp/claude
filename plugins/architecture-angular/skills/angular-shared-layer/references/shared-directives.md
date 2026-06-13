# Shared Directives — Referência

## Tipos de Directives

| Tipo | Quando usar | Exemplo |
|---|---|---|
| **Attribute** | Modifica comportamento de elemento existente | `appAutoFocus`, `appTooltip` |
| **Structural** | Adiciona/remove elementos do DOM | `*appIfRole`, `*appRepeat` |
| **Host Directive** | Compõe comportamentos em componentes | `appClickOutside` em modal |

---

## ClickOutsideDirective — detecta clique fora

```typescript
// src/app/shared/directives/click-outside.directive.ts
import {
  Directive, ElementRef, output, HostListener, inject
} from '@angular/core';

@Directive({
  selector: '[appClickOutside]',
  standalone: true
})
export class ClickOutsideDirective {
  private readonly el = inject(ElementRef);

  readonly clickedOutside = output<void>();

  @HostListener('document:click', ['$event.target'])
  onDocumentClick(target: HTMLElement): void {
    if (!this.el.nativeElement.contains(target)) {
      this.clickedOutside.emit();
    }
  }
}
```

**Uso:**
```html
<div appClickOutside (clickedOutside)="closeDropdown()">
  <button (click)="toggle()">Abrir menu</button>
  @if (open) {
    <ul class="dropdown">...</ul>
  }
</div>
```

---

## AutoFocusDirective — foco automático

```typescript
// src/app/shared/directives/auto-focus.directive.ts
import { Directive, ElementRef, AfterViewInit, input, inject } from '@angular/core';

@Directive({
  selector: '[appAutoFocus]',
  standalone: true
})
export class AutoFocusDirective implements AfterViewInit {
  private readonly el = inject(ElementRef<HTMLElement>);

  // delay opcional para animações de modal
  readonly appAutoFocus = input<number>(0);

  ngAfterViewInit(): void {
    const delay = this.appAutoFocus();
    if (delay > 0) {
      setTimeout(() => this.focus(), delay);
    } else {
      this.focus();
    }
  }

  private focus(): void {
    const el = this.el.nativeElement;
    if (typeof el.focus === 'function') {
      el.focus();
      // Seleciona todo o texto se for input
      if ('select' in el) (el as HTMLInputElement).select();
    }
  }
}
```

**Uso:**
```html
<!-- Foca imediatamente -->
<input appAutoFocus placeholder="Nome" />

<!-- Foca após 200ms (espera animação do modal) -->
<input [appAutoFocus]="200" placeholder="Buscar..." />
```

---

## TooltipDirective — tooltip nativo

```typescript
// src/app/shared/directives/tooltip.directive.ts
import {
  Directive, ElementRef, Renderer2, input,
  HostListener, inject, OnDestroy
} from '@angular/core';

export type TooltipPosition = 'top' | 'bottom' | 'left' | 'right';

@Directive({
  selector: '[appTooltip]',
  standalone: true
})
export class TooltipDirective implements OnDestroy {
  private readonly el       = inject(ElementRef<HTMLElement>);
  private readonly renderer = inject(Renderer2);

  readonly appTooltip         = input.required<string>();
  readonly tooltipPosition    = input<TooltipPosition>('top');
  readonly tooltipDelay       = input<number>(300);
  readonly tooltipDisabled    = input<boolean>(false);

  private tooltipEl: HTMLElement | null = null;
  private showTimeout?: ReturnType<typeof setTimeout>;

  @HostListener('mouseenter')
  onMouseEnter(): void {
    if (this.tooltipDisabled() || !this.appTooltip()) return;
    this.showTimeout = setTimeout(() => this.show(), this.tooltipDelay());
  }

  @HostListener('mouseleave')
  @HostListener('click')
  onMouseLeave(): void {
    clearTimeout(this.showTimeout);
    this.hide();
  }

  private show(): void {
    this.tooltipEl = this.renderer.createElement('div');
    this.renderer.addClass(this.tooltipEl, 'app-tooltip');
    this.renderer.addClass(this.tooltipEl, `tooltip-${this.tooltipPosition()}`);
    this.renderer.setProperty(this.tooltipEl, 'textContent', this.appTooltip());

    // Estilos inline para não depender de CSS global
    Object.assign(this.tooltipEl!.style, {
      position:      'fixed',
      background:    '#111827',
      color:         '#fff',
      padding:       '6px 10px',
      borderRadius:  '6px',
      fontSize:      '12px',
      whiteSpace:    'nowrap',
      zIndex:        '9999',
      pointerEvents: 'none',
      opacity:       '0',
      transition:    'opacity .15s'
    });

    this.renderer.appendChild(document.body, this.tooltipEl);
    this.position();
    requestAnimationFrame(() => {
      if (this.tooltipEl) this.tooltipEl.style.opacity = '1';
    });
  }

  private hide(): void {
    if (this.tooltipEl) {
      this.renderer.removeChild(document.body, this.tooltipEl);
      this.tooltipEl = null;
    }
  }

  private position(): void {
    if (!this.tooltipEl) return;
    const rect    = this.el.nativeElement.getBoundingClientRect();
    const tip     = this.tooltipEl;
    const pos     = this.tooltipPosition();
    const GAP     = 8;

    // Posiciona após render para ter as dimensões corretas
    requestAnimationFrame(() => {
      const tw = tip.offsetWidth;
      const th = tip.offsetHeight;
      const positions: Record<TooltipPosition, { top: number; left: number }> = {
        top:    { top: rect.top  - th - GAP,               left: rect.left + rect.width / 2 - tw / 2 },
        bottom: { top: rect.bottom + GAP,                  left: rect.left + rect.width / 2 - tw / 2 },
        left:   { top: rect.top  + rect.height / 2 - th / 2, left: rect.left - tw - GAP },
        right:  { top: rect.top  + rect.height / 2 - th / 2, left: rect.right + GAP }
      };
      const { top, left } = positions[pos];
      tip.style.top  = `${top}px`;
      tip.style.left = `${left}px`;
    });
  }

  ngOnDestroy(): void {
    clearTimeout(this.showTimeout);
    this.hide();
  }
}
```

**Uso:**
```html
<button [appTooltip]="'Excluir registro'" tooltipPosition="top">
  🗑
</button>
<span [appTooltip]="user.email" tooltipPosition="right" [tooltipDelay]="500">
  {{ user.name | truncate:20 }}
</span>
```

---

## CopyToClipboardDirective

```typescript
// src/app/shared/directives/copy-to-clipboard.directive.ts
import { Directive, input, output, HostListener, inject } from '@angular/core';
import { NotificationService } from '../../core/services/notification.service';

@Directive({
  selector: '[appCopy]',
  standalone: true,
  host: { '[style.cursor]': '"pointer"' }
})
export class CopyToClipboardDirective {
  private readonly notification = inject(NotificationService);

  readonly appCopy        = input.required<string>();
  readonly copySuccessMsg = input<string>('Copiado!');

  readonly copied = output<void>();

  @HostListener('click')
  async onClick(): Promise<void> {
    try {
      await navigator.clipboard.writeText(this.appCopy());
      this.notification.success(this.copySuccessMsg());
      this.copied.emit();
    } catch {
      this.notification.error('Não foi possível copiar.');
    }
  }
}
```

---

## InfiniteScrollDirective — scroll infinito

```typescript
// src/app/shared/directives/infinite-scroll.directive.ts
import {
  Directive, ElementRef, output, input, OnInit, OnDestroy, inject
} from '@angular/core';

@Directive({
  selector: '[appInfiniteScroll]',
  standalone: true
})
export class InfiniteScrollDirective implements OnInit, OnDestroy {
  private readonly el = inject(ElementRef<HTMLElement>);

  readonly threshold    = input<number>(0.8);   // 80% do scroll
  readonly disabled     = input<boolean>(false);
  readonly scrolled     = output<void>();

  private observer!: IntersectionObserver;
  private sentinel!: HTMLElement;

  ngOnInit(): void {
    // Cria um elemento sentinela no final do container
    this.sentinel = document.createElement('div');
    this.sentinel.style.height = '1px';
    this.el.nativeElement.appendChild(this.sentinel);

    this.observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !this.disabled()) {
          this.scrolled.emit();
        }
      },
      { root: this.el.nativeElement, threshold: this.threshold() }
    );

    this.observer.observe(this.sentinel);
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
    this.sentinel?.remove();
  }
}
```

**Uso:**
```html
<div class="list-container" appInfiniteScroll
     [disabled]="allLoaded()" (scrolled)="loadMore()">
  @for (item of items(); track item.id) {
    <app-card [title]="item.title" />
  }
  @if (loading()) { <app-spinner /> }
</div>
```

---

## IfRoleDirective — structural directive de permissão

```typescript
// src/app/shared/directives/if-role.directive.ts
import {
  Directive, TemplateRef, ViewContainerRef,
  input, inject, effect
} from '@angular/core';
import { AuthService } from '../../core/services/auth.service';

@Directive({
  selector: '[appIfRole]',
  standalone: true
})
export class IfRoleDirective {
  private readonly template = inject(TemplateRef);
  private readonly vcr      = inject(ViewContainerRef);
  private readonly auth     = inject(AuthService);

  readonly appIfRole = input.required<string | string[]>();

  constructor() {
    effect(() => {
      const roles   = this.appIfRole();
      const user    = this.auth.currentUser$;  // ou signal
      const allowed = Array.isArray(roles) ? roles : [roles];
      // Limpa e re-renderiza baseado na permissão
      this.vcr.clear();
      // Lógica de verificação de role aqui
    });
  }
}
```

**Uso:**
```html
<button *appIfRole="'Admin'">Excluir</button>
<button *appIfRole="['Admin', 'Manager']">Editar</button>
```
