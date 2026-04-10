---
name: dotnet-external-service
description: Gera integrações com APIs de terceiros usando padrão Adapter/Gateway. Use quando o usuário mencionar "integração com API", "API externa", "chamar API", "consumir API", "serviço externo", "third-party", "webhook", "REST client", "HTTP client", "adapter", "gateway", "integração com", "conectar com API", "cliente HTTP". Também dispara quando pedir para criar integrações com serviços como pagamento, envio de email, SMS, notificações push, CEP, ou qualquer serviço externo. NÃO use para APIs internas do próprio sistema (use dotnet-endpoint-generator).
---

# .NET External Service Integration

Gera integrações com APIs externas usando padrão Adapter/Gateway, HttpClientBase com Polly (resiliência) e logging estruturado.

## Instruções

### ANTES de gerar código, consulte as referências:

1. **Leia `references/http-client-base.md`** para a classe base HTTP
2. **Leia `references/adapter-gateway.md`** para padrão Adapter/Gateway
3. **Leia `references/resilience.md`** para configuração de Polly
4. **Leia `references/authentication.md`** para OAuth2/Bearer Token

### Passo 1: Coletar Informações do Serviço

Pergunte ao usuário:
- Nome do serviço/provider (ex: Stripe, SendGrid, ViaCEP)
- URL base da API
- Tipo de autenticação (Bearer Token/OAuth2)
- Endpoints necessários
- Documentação da API (se disponível)

### Passo 2: Definir Contratos

Para cada endpoint, definir:
- Request model (o que enviar)
- Response model (o que receber)
- Possíveis erros da API

### Passo 3: Gerar Artefatos

```
Infrastructure/
└── ExternalServices/
    ├── Common/
    │   ├── HttpClientBase.cs
    │   ├── ExternalServiceException.cs
    │   └── ExternalServiceResponse.cs
    ├── {Provider}/
    │   ├── I{Provider}Gateway.cs        # Interface
    │   ├── {Provider}Adapter.cs         # Implementação
    │   ├── {Provider}Settings.cs        # Configurações
    │   ├── Models/
    │   │   ├── Requests/
    │   │   │   └── {Action}Request.cs
    │   │   └── Responses/
    │   │       └── {Action}Response.cs
    │   └── Mappers/
    │       └── {Provider}Mapper.cs      # Conversão Domain <-> API
    └── DependencyInjection.cs
```

### Passo 4: Validar Checklist

- [ ] Herda de `HttpClientBase`
- [ ] Interface `I{Provider}Gateway` definida
- [ ] `{Provider}Settings` com URL base e credenciais
- [ ] Models de Request/Response separados dos DTOs de Application
- [ ] Retorna `Result<T>` em todos os métodos
- [ ] Polly configurado (retry, circuit breaker, timeout)
- [ ] Logging estruturado sem dados sensíveis
- [ ] Registrado no DI com `AddHttpClient<T>()`
- [ ] Configuração em `appsettings.json`

## Padrões Obrigatórios

### Adapter herda de HttpClientBase

```csharp
// ✅ CORRETO
public class StripeAdapter : HttpClientBase, IStripeGateway
{
    public StripeAdapter(
        HttpClient httpClient,
        IOptions<StripeSettings> settings,
        ILogger<StripeAdapter> logger)
        : base(httpClient, logger)
    {
    }
}

// ❌ INCORRETO - Não injetar HttpClient diretamente
public class StripeAdapter : IStripeGateway
{
    private readonly HttpClient _httpClient; // NÃO FAZER
}
```

### Retorno com Result Pattern

```csharp
// ✅ CORRETO
public async Task<Result<PaymentResponse>> CreatePaymentAsync(
    CreatePaymentRequest request,
    CancellationToken ct)
{
    var response = await PostAsync<PaymentApiResponse>("/payments", request, ct);
    
    if (!response.IsSuccess)
        return Result.Error(response.ErrorMessage);
    
    return Result.Success(_mapper.ToPaymentResponse(response.Data!));
}
```

### Nomenclatura

| Artefato | Padrão | Exemplo |
|----------|--------|---------|
| Gateway Interface | `I{Provider}Gateway` | `IStripeGateway` |
| Adapter | `{Provider}Adapter` | `StripeAdapter` |
| Settings | `{Provider}Settings` | `StripeSettings` |
| API Request | `{Action}ApiRequest` | `CreatePaymentApiRequest` |
| API Response | `{Action}ApiResponse` | `CreatePaymentApiResponse` |

## Fluxo de Integração

```
Application Layer          Infrastructure Layer              External API
      │                           │                               │
      │  IStripeGateway           │                               │
      ├──────────────────────────►│                               │
      │                           │  StripeAdapter                │
      │                           │  (herda HttpClientBase)       │
      │                           │         │                     │
      │                           │         │ POST /payments      │
      │                           │         ├────────────────────►│
      │                           │         │                     │
      │                           │         │◄────────────────────┤
      │                           │         │  JSON Response      │
      │                           │◄────────┤                     │
      │  Result<PaymentResponse>  │  Map to Domain                │
      │◄──────────────────────────┤                               │
```

## Troubleshooting

### Erro: HttpClient não resolvido
**Causa**: Não registrado com `AddHttpClient<T>()`
**Solução**: Usar `services.AddHttpClient<IStripeGateway, StripeAdapter>()`

### Erro: Timeout em todas as requests
**Causa**: Timeout muito baixo ou API lenta
**Solução**: Ajustar `TimeoutSeconds` nas settings

### Erro: Circuit breaker sempre aberto
**Causa**: Taxa de falha muito alta
**Solução**: Verificar conectividade, credenciais, ou ajustar thresholds
