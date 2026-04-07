---
name: dotnet-endpoint-generator
description: Gera endpoints ASP.NET Core seguindo Clean Architecture e padrões estabelecidos. Use quando o usuário mencionar "criar endpoint", "novo endpoint", "adicionar endpoint", "API endpoint", "controller", "minimal API", "rota", "HTTP GET/POST/PUT/DELETE", "CRUD endpoint", "endpoint para", "expor via API", "criar rota". Também dispara quando o usuário pedir para criar funcionalidades que precisam ser expostas via HTTP. NÃO use para lógica de domínio pura sem exposição HTTP.
---

# .NET Endpoint Generator

Gera endpoints ASP.NET Core completos seguindo Clean Architecture, Result Pattern e boas práticas.

## Instruções

### ANTES de gerar qualquer código, consulte as referências:

1. **Leia `references/patterns.md`** para entender os padrões de código
2. **Leia `references/structure.md`** para a estrutura de arquivos
3. **Leia `references/examples.md`** para exemplos completos

### Passo 1: Identificar Tipo de Endpoint

Pergunte ao usuário se não estiver claro:
- **Controller (MVC)**: Quando precisar de mais controle, atributos complexos
- **Minimal API**: Para endpoints simples e diretos

### Passo 2: Coletar Informações

Determine:
- Nome da entidade/recurso
- Operações necessárias (GET, POST, PUT, DELETE)
- Campos de request/response
- Validações necessárias
- Se precisa de paginação

### Passo 3: Gerar Artefatos

Para cada endpoint, gere na ordem:

1. **Request Model** (`Models/Requests/{Action}{Entity}Request.cs`)
2. **Response Model** (se diferente do DTO existente)
3. **Validator** (`Validators/{Action}{Entity}RequestValidator.cs`)
4. **Command/Query** (na camada Application)
5. **Handler** (na camada Application)
6. **Endpoint** (Controller ou Minimal API)

### Passo 4: Validar

Antes de finalizar, verifique:
- [ ] Usa `Result<T>` como retorno dos handlers
- [ ] Tem `CancellationToken` em todos os métodos async
- [ ] Validators estão registrados
- [ ] Documentação OpenAPI com `ProducesResponseType`
- [ ] Tratamento de erros adequado

## Padrões Obrigatórios

### Result Pattern
Todos os handlers retornam `Result<T>` ou `Result`:
```csharp
public async Task<Result<EntityDto>> Handle(Command request, CancellationToken ct)
{
    // Validação de negócio
    if (conditionFails)
        return Result.Invalid(new ValidationError("Field", "Message"));
    
    // Not found
    if (entity is null)
        return Result.NotFound("Entity not found");
    
    // Sucesso
    return Result.Success(dto);
}
```

### Injeção via MediatR
Controllers usam `ISender` (não `IMediator`):
```csharp
private ISender? _mediator;
protected ISender Mediator => _mediator ??= 
    HttpContext.RequestServices.GetRequiredService<ISender>();
```

### Nomenclatura

| Artefato | Padrão | Exemplo |
|----------|--------|---------|
| Controller | `{Entity}Controller` | `ProductsController` |
| Endpoint Group | `{Entity}Endpoints` | `ProductEndpoints` |
| Command | `{Action}{Entity}Command` | `CreateProductCommand` |
| Query | `Get{Entity}Query` | `GetProductByIdQuery` |
| Request | `{Action}{Entity}Request` | `CreateProductRequest` |
| Validator | `{Request}Validator` | `CreateProductRequestValidator` |

## Troubleshooting

### Erro: Handler não encontrado
**Causa**: MediatR não registrou o handler
**Solução**: Verificar se `AddApplication()` está no Program.cs

### Erro: Validação não executa
**Causa**: Validator não registrado ou behavior ausente
**Solução**: Verificar `AddValidatorsFromAssembly()` e `ValidationBehavior`

### Erro: Result não converte para ActionResult
**Causa**: Filter não configurado ou método `ToActionResult` ausente
**Solução**: Usar `ApiControllerBase` ou adicionar `ResultTransformFilter`
