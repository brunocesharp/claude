---
name: angular-shared-layer
description: Gera todos os elementos da camada Shared de uma solução Angular: Dumb Components reutilizáveis, Pipes customizados, Directives de comportamento e integração com bibliotecas de UI (Angular Material, PrimeNG, Tailwind). Use sempre que o usuário mencionar "shared component", "componente compartilhado", "dumb component shared", "pipe Angular", "pipe customizado", "directive Angular", "directive de comportamento", "UI library Angular", "Angular Material", "PrimeNG", "Tailwind Angular", "criar pipe", "criar directive", "criar componente reutilizável", "camada shared", "shared module", "componente de apresentação", "componente sem lógica". Também dispara quando o usuário pedir para criar qualquer um destes itens: ButtonComponent, CardComponent, ModalComponent, TableComponent, BadgeComponent, AvatarComponent, SpinnerComponent, EmptyStateComponent, DatePipe, CurrencyPipe, TruncatePipe, ClickOutsideDirective, AutoFocusDirective, InfiniteScrollDirective, TooltipDirective. NÃO use para componentes com lógica de negócio ou acesso à Store (use angular-feature-layer) nem para serviços singleton (use angular-core-layer).
compatibility: Angular 17+, TypeScript 5+, RxJS 7+, Angular Material 17+ ou PrimeNG 17+ (opcional)
metadata:
  author: angular-architecture
  version: 1.0.0
  category: angular
  tags: [angular, shared, components, pipes, directives, ui-library, material, primeng, tailwind]
---

# Angular Shared Layer

Skill para geração da **camada Shared** de uma solução Angular — componentes de apresentação, pipes e directives reutilizáveis em toda a aplicação, sem dependência de lógica de negócio ou Store.

## Princípio fundamental

> Tudo na camada Shared deve ser **reutilizável, sem opinião de negócio e sem acesso à Store**.

```
shared/
├── components/        → Dumb Components (apresentação pura, @Input/@Output)
│   ├── button/
│   ├── card/
│   ├── modal/
│   ├── table/
│   ├── badge/
│   ├── avatar/
│   ├── spinner/
│   └── empty-state/
├── pipes/             → Pipes de transformação de dados
│   ├── date-format.pipe.ts
│   ├── currency-br.pipe.ts
│   ├── truncate.pipe.ts
│   ├── cpf.pipe.ts
│   └── file-size.pipe.ts
├── directives/        → Directives de comportamento DOM
│   ├── click-outside.directive.ts
│   ├── auto-focus.directive.ts
│   ├── infinite-scroll.directive.ts
│   ├── tooltip.directive.ts
│   └── copy-to-clipboard.directive.ts
└── ui/                → Configuração e wrappers de UI Library
    ├── material.config.ts
    ├── primeng.config.ts
    └── tailwind-tokens.ts
```

## Itens disponíveis

Identifique o item solicitado e leia o arquivo de referência correspondente:

| Item | Arquivo de referência | Quando usar |
|---|---|---|
| Dumb Components | `references/shared-components.md` | Componentes de apresentação reutilizáveis |
| Pipes | `references/shared-pipes.md` | Transformações de dados no template |
| Directives | `references/shared-directives.md` | Comportamentos DOM reutilizáveis |
| UI Library | `references/shared-ui-library.md` | Angular Material, PrimeNG, Tailwind |

## Fluxo de geração

### Passo 1 — Identificar o item
Pergunte ao usuário:
- Qual **tipo** de item Shared deseja criar
- O **nome** e **propósito** do item (ex: `TruncatePipe` para truncar texto longo)
- Se existe preferência de **UI library** (Material, PrimeNG, Tailwind, nenhuma)

### Passo 2 — Verificar reusabilidade
Confirme que o item:
- **Não acessa a Store NgRx** (isso o tornaria um Smart Component)
- **Não contém regras de negócio** específicas de uma feature
- **Funciona em qualquer contexto** da aplicação

### Passo 3 — Ler referência e gerar
Leia o arquivo de referência correspondente e gere o código completo.

### Passo 4 — Entregar
Entregue:
1. O arquivo `.ts` com path correto (`src/app/shared/...`)
2. O arquivo `.html` e `.scss` se for componente
3. Como importar no componente consumidor (standalone import)

## Convenções obrigatórias

- **Standalone**: sempre `standalone: true`
- **OnPush**: sempre `ChangeDetectionStrategy.OnPush`
- **input() signal**: usar `input()` e `output()` do Angular 17+ (não `@Input/@Output`)
- **Prefixo de seletor**: usar prefixo da aplicação (ex: `app-button`, `app-card`)
- **Pipes puros**: sempre `pure: true` (padrão) — evitar pipes impuros
- **Directives**: usar `hostDirectives` quando possível para composição
- **Sem serviços de negócio**: Shared items só podem injetar serviços utilitários

## Checklist de reusabilidade

Antes de gerar, confirme que o item atende:
- [ ] Funciona passando apenas `@Input` — sem depender de contexto externo
- [ ] Não importa serviços de features ou do Core (exceto utilitários)
- [ ] Tem nome genérico (não `UserCard` — isso é Feature; sim `Card`)
- [ ] Pode ser usado em pelo menos 3 lugares diferentes da aplicação
- [ ] Não possui lógica de roteamento interno

## Troubleshooting comum

**Componente com OnPush não atualiza**
- Confirmar que os `@Input` usam referências novas (imutabilidade)
- Usar `input.required()` para garantir que o valor sempre chega
- Usar `markForCheck()` se houver assinatura de Observable interno

**Pipe não transforma corretamente**
- Verificar se o pipe está nos `imports` do componente standalone
- Para pipes com locale, confirmar `LOCALE_ID` no `app.config.ts`

**Directive não aplica estilo**
- Confirmar que o `host` binding está correto
- Usar `HostListener` ou `host: { '(event)': 'handler()' }` para eventos
