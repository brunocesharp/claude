# Adapter/Gateway Pattern

## Estrutura de Arquivos

```
Infrastructure/
└── ExternalServices/
    └── {Provider}/
        ├── I{Provider}Gateway.cs         # Interface
        ├── {Provider}Adapter.cs          # Implementação
        ├── {Provider}Settings.cs         # Configurações
        ├── Models/
        │   ├── Requests/
        │   │   └── {Action}ApiRequest.cs
        │   └── Responses/
        │       └── {Action}ApiResponse.cs
        └── Mappers/
            └── {Provider}Mapper.cs
```

---

## Gateway Interface

```csharp
// Infrastructure/ExternalServices/Stripe/IStripeGateway.cs
using Ardalis.Result;

namespace Infrastructure.ExternalServices.Stripe;

/// <summary>
/// Gateway para integração com Stripe Payment API.
/// </summary>
public interface IStripeGateway
{
    /// <summary>
    /// Cria um novo pagamento.
    /// </summary>
    Task<Result<CreatePaymentResponse>> CreatePaymentAsync(
        CreatePaymentRequest request,
        CancellationToken ct = default);
    
    /// <summary>
    /// Obtém detalhes de um pagamento.
    /// </summary>
    Task<Result<PaymentDetailsResponse>> GetPaymentAsync(
        string paymentId,
        CancellationToken ct = default);
    
    /// <summary>
    /// Cancela um pagamento pendente.
    /// </summary>
    Task<Result> CancelPaymentAsync(
        string paymentId,
        CancellationToken ct = default);
    
    /// <summary>
    /// Reembolsa um pagamento.
    /// </summary>
    Task<Result<RefundResponse>> RefundPaymentAsync(
        RefundRequest request,
        CancellationToken ct = default);
    
    /// <summary>
    /// Cria um cliente.
    /// </summary>
    Task<Result<CustomerResponse>> CreateCustomerAsync(
        CreateCustomerRequest request,
        CancellationToken ct = default);
}
```

---

## Settings

```csharp
// Infrastructure/ExternalServices/Stripe/StripeSettings.cs
namespace Infrastructure.ExternalServices.Stripe;

public class StripeSettings
{
    public const string SectionName = "ExternalServices:Stripe";
    
    /// <summary>
    /// URL base da API (ex: https://api.stripe.com)
    /// </summary>
    public string BaseUrl { get; set; } = string.Empty;
    
    /// <summary>
    /// Secret Key para autenticação
    /// </summary>
    public string SecretKey { get; set; } = string.Empty;
    
    /// <summary>
    /// Publishable Key (para uso no frontend)
    /// </summary>
    public string PublishableKey { get; set; } = string.Empty;
    
    /// <summary>
    /// Webhook Secret para validar eventos
    /// </summary>
    public string WebhookSecret { get; set; } = string.Empty;
    
    /// <summary>
    /// Timeout em segundos
    /// </summary>
    public int TimeoutSeconds { get; set; } = 30;
    
    /// <summary>
    /// Número de tentativas em caso de falha
    /// </summary>
    public int RetryCount { get; set; } = 3;
}
```

### appsettings.json

```json
{
  "ExternalServices": {
    "Stripe": {
      "BaseUrl": "https://api.stripe.com",
      "SecretKey": "",
      "PublishableKey": "",
      "WebhookSecret": "",
      "TimeoutSeconds": 30,
      "RetryCount": 3
    }
  }
}
```

---

## Adapter Implementation

```csharp
// Infrastructure/ExternalServices/Stripe/StripeAdapter.cs
using Ardalis.Result;
using Infrastructure.ExternalServices.Common;
using Infrastructure.ExternalServices.Stripe.Mappers;
using Infrastructure.ExternalServices.Stripe.Models.Requests;
using Infrastructure.ExternalServices.Stripe.Models.Responses;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace Infrastructure.ExternalServices.Stripe;

public class StripeAdapter : HttpClientBase, IStripeGateway
{
    private readonly StripeSettings _settings;
    private readonly StripeMapper _mapper;
    
    protected override string ServiceName => "Stripe";
    
    public StripeAdapter(
        HttpClient httpClient,
        IOptions<StripeSettings> settings,
        ILogger<StripeAdapter> logger)
        : base(httpClient, logger)
    {
        _settings = settings.Value;
        _mapper = new StripeMapper();
        
        // Configurar autenticação Bearer Token
        SetBearerToken(_settings.SecretKey);
    }
    
    public async Task<Result<CreatePaymentResponse>> CreatePaymentAsync(
        CreatePaymentRequest request,
        CancellationToken ct = default)
    {
        // Mapear para modelo da API
        var apiRequest = _mapper.ToCreatePaymentApiRequest(request);
        
        // Chamar API
        var response = await PostAsync<PaymentIntentApiResponse>(
            "/v1/payment_intents",
            apiRequest,
            ct);
        
        // Tratar resposta
        if (!response.IsSuccess)
        {
            return MapErrorToResult<CreatePaymentResponse>(response);
        }
        
        // Mapear resposta para modelo de domínio
        var result = _mapper.ToCreatePaymentResponse(response.Data!);
        
        return Result.Success(result);
    }
    
    public async Task<Result<PaymentDetailsResponse>> GetPaymentAsync(
        string paymentId,
        CancellationToken ct = default)
    {
        var response = await GetAsync<PaymentIntentApiResponse>(
            $"/v1/payment_intents/{paymentId}",
            ct);
        
        if (!response.IsSuccess)
        {
            if (response.StatusCode == 404)
                return Result.NotFound($"Payment {paymentId} not found");
            
            return MapErrorToResult<PaymentDetailsResponse>(response);
        }
        
        var result = _mapper.ToPaymentDetailsResponse(response.Data!);
        
        return Result.Success(result);
    }
    
    public async Task<Result> CancelPaymentAsync(
        string paymentId,
        CancellationToken ct = default)
    {
        var response = await PostAsync(
            $"/v1/payment_intents/{paymentId}/cancel",
            body: null,
            ct);
        
        if (!response.IsSuccess)
        {
            return MapErrorToResult(response);
        }
        
        return Result.Success();
    }
    
    public async Task<Result<RefundResponse>> RefundPaymentAsync(
        RefundRequest request,
        CancellationToken ct = default)
    {
        var apiRequest = _mapper.ToRefundApiRequest(request);
        
        var response = await PostAsync<RefundApiResponse>(
            "/v1/refunds",
            apiRequest,
            ct);
        
        if (!response.IsSuccess)
        {
            return MapErrorToResult<RefundResponse>(response);
        }
        
        var result = _mapper.ToRefundResponse(response.Data!);
        
        return Result.Success(result);
    }
    
    public async Task<Result<CustomerResponse>> CreateCustomerAsync(
        CreateCustomerRequest request,
        CancellationToken ct = default)
    {
        var apiRequest = _mapper.ToCreateCustomerApiRequest(request);
        
        var response = await PostAsync<CustomerApiResponse>(
            "/v1/customers",
            apiRequest,
            ct);
        
        if (!response.IsSuccess)
        {
            return MapErrorToResult<CustomerResponse>(response);
        }
        
        var result = _mapper.ToCustomerResponse(response.Data!);
        
        return Result.Success(result);
    }
    
    #region Error Mapping
    
    private Result<T> MapErrorToResult<T>(ExternalServiceResponse<T> response)
    {
        return response.StatusCode switch
        {
            400 => Result<T>.Invalid(new ValidationError("Stripe", response.ErrorMessage ?? "Bad request")),
            401 => Result<T>.Unauthorized(),
            403 => Result<T>.Forbidden(),
            404 => Result<T>.NotFound(response.ErrorMessage ?? "Resource not found"),
            429 => Result<T>.Error("Rate limit exceeded. Please try again later."),
            >= 500 => Result<T>.Error($"Stripe service error: {response.ErrorMessage}"),
            _ => Result<T>.Error(response.ErrorMessage ?? "Unknown error")
        };
    }
    
    private Result MapErrorToResult(ExternalServiceResponse response)
    {
        return response.StatusCode switch
        {
            400 => Result.Invalid(new ValidationError("Stripe", response.ErrorMessage ?? "Bad request")),
            401 => Result.Unauthorized(),
            403 => Result.Forbidden(),
            404 => Result.NotFound(response.ErrorMessage ?? "Resource not found"),
            429 => Result.Error("Rate limit exceeded. Please try again later."),
            >= 500 => Result.Error($"Stripe service error: {response.ErrorMessage}"),
            _ => Result.Error(response.ErrorMessage ?? "Unknown error")
        };
    }
    
    #endregion
}
```

---

## API Models (Requests)

```csharp
// Infrastructure/ExternalServices/Stripe/Models/Requests/CreatePaymentIntentApiRequest.cs
using System.Text.Json.Serialization;

namespace Infrastructure.ExternalServices.Stripe.Models.Requests;

/// <summary>
/// Request para criar PaymentIntent na API do Stripe.
/// </summary>
public class CreatePaymentIntentApiRequest
{
    /// <summary>
    /// Valor em centavos (ex: 1000 = $10.00)
    /// </summary>
    [JsonPropertyName("amount")]
    public long Amount { get; set; }
    
    /// <summary>
    /// Código da moeda (ex: "usd", "brl")
    /// </summary>
    [JsonPropertyName("currency")]
    public string Currency { get; set; } = "usd";
    
    /// <summary>
    /// ID do cliente no Stripe
    /// </summary>
    [JsonPropertyName("customer")]
    public string? CustomerId { get; set; }
    
    /// <summary>
    /// Descrição do pagamento
    /// </summary>
    [JsonPropertyName("description")]
    public string? Description { get; set; }
    
    /// <summary>
    /// Metadados customizados
    /// </summary>
    [JsonPropertyName("metadata")]
    public Dictionary<string, string>? Metadata { get; set; }
    
    /// <summary>
    /// Métodos de pagamento aceitos
    /// </summary>
    [JsonPropertyName("payment_method_types")]
    public List<string>? PaymentMethodTypes { get; set; }
    
    /// <summary>
    /// Confirmar automaticamente
    /// </summary>
    [JsonPropertyName("confirm")]
    public bool? Confirm { get; set; }
}

// Infrastructure/ExternalServices/Stripe/Models/Requests/CreateRefundApiRequest.cs
namespace Infrastructure.ExternalServices.Stripe.Models.Requests;

public class CreateRefundApiRequest
{
    [JsonPropertyName("payment_intent")]
    public string PaymentIntentId { get; set; } = string.Empty;
    
    [JsonPropertyName("amount")]
    public long? Amount { get; set; }
    
    [JsonPropertyName("reason")]
    public string? Reason { get; set; }
}

// Infrastructure/ExternalServices/Stripe/Models/Requests/CreateCustomerApiRequest.cs
namespace Infrastructure.ExternalServices.Stripe.Models.Requests;

public class CreateCustomerApiRequest
{
    [JsonPropertyName("email")]
    public string Email { get; set; } = string.Empty;
    
    [JsonPropertyName("name")]
    public string? Name { get; set; }
    
    [JsonPropertyName("phone")]
    public string? Phone { get; set; }
    
    [JsonPropertyName("metadata")]
    public Dictionary<string, string>? Metadata { get; set; }
}
```

---

## API Models (Responses)

```csharp
// Infrastructure/ExternalServices/Stripe/Models/Responses/PaymentIntentApiResponse.cs
using System.Text.Json.Serialization;

namespace Infrastructure.ExternalServices.Stripe.Models.Responses;

/// <summary>
/// Resposta de PaymentIntent da API do Stripe.
/// </summary>
public class PaymentIntentApiResponse
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = string.Empty;
    
    [JsonPropertyName("object")]
    public string Object { get; set; } = "payment_intent";
    
    [JsonPropertyName("amount")]
    public long Amount { get; set; }
    
    [JsonPropertyName("currency")]
    public string Currency { get; set; } = string.Empty;
    
    [JsonPropertyName("status")]
    public string Status { get; set; } = string.Empty;
    
    [JsonPropertyName("client_secret")]
    public string? ClientSecret { get; set; }
    
    [JsonPropertyName("customer")]
    public string? CustomerId { get; set; }
    
    [JsonPropertyName("description")]
    public string? Description { get; set; }
    
    [JsonPropertyName("metadata")]
    public Dictionary<string, string>? Metadata { get; set; }
    
    [JsonPropertyName("created")]
    public long Created { get; set; }
    
    [JsonPropertyName("canceled_at")]
    public long? CanceledAt { get; set; }
    
    [JsonPropertyName("cancellation_reason")]
    public string? CancellationReason { get; set; }
}

// Infrastructure/ExternalServices/Stripe/Models/Responses/RefundApiResponse.cs
namespace Infrastructure.ExternalServices.Stripe.Models.Responses;

public class RefundApiResponse
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = string.Empty;
    
    [JsonPropertyName("amount")]
    public long Amount { get; set; }
    
    [JsonPropertyName("currency")]
    public string Currency { get; set; } = string.Empty;
    
    [JsonPropertyName("status")]
    public string Status { get; set; } = string.Empty;
    
    [JsonPropertyName("payment_intent")]
    public string PaymentIntentId { get; set; } = string.Empty;
    
    [JsonPropertyName("reason")]
    public string? Reason { get; set; }
    
    [JsonPropertyName("created")]
    public long Created { get; set; }
}

// Infrastructure/ExternalServices/Stripe/Models/Responses/CustomerApiResponse.cs
namespace Infrastructure.ExternalServices.Stripe.Models.Responses;

public class CustomerApiResponse
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = string.Empty;
    
    [JsonPropertyName("email")]
    public string? Email { get; set; }
    
    [JsonPropertyName("name")]
    public string? Name { get; set; }
    
    [JsonPropertyName("phone")]
    public string? Phone { get; set; }
    
    [JsonPropertyName("created")]
    public long Created { get; set; }
}
```

---

## Domain Models (Request/Response do Gateway)

```csharp
// Infrastructure/ExternalServices/Stripe/CreatePaymentRequest.cs
namespace Infrastructure.ExternalServices.Stripe;

/// <summary>
/// Request para criar pagamento (modelo de domínio).
/// </summary>
public record CreatePaymentRequest(
    decimal Amount,
    string Currency,
    string? CustomerId = null,
    string? Description = null,
    Dictionary<string, string>? Metadata = null);

/// <summary>
/// Response de criação de pagamento (modelo de domínio).
/// </summary>
public record CreatePaymentResponse(
    string PaymentId,
    string Status,
    string? ClientSecret,
    decimal Amount,
    string Currency,
    DateTime CreatedAt);

/// <summary>
/// Detalhes do pagamento (modelo de domínio).
/// </summary>
public record PaymentDetailsResponse(
    string PaymentId,
    string Status,
    decimal Amount,
    string Currency,
    string? CustomerId,
    string? Description,
    DateTime CreatedAt,
    DateTime? CanceledAt,
    string? CancellationReason);

/// <summary>
/// Request de reembolso (modelo de domínio).
/// </summary>
public record RefundRequest(
    string PaymentId,
    decimal? Amount = null,
    string? Reason = null);

/// <summary>
/// Response de reembolso (modelo de domínio).
/// </summary>
public record RefundResponse(
    string RefundId,
    string PaymentId,
    string Status,
    decimal Amount,
    string Currency,
    DateTime CreatedAt);

/// <summary>
/// Request para criar cliente (modelo de domínio).
/// </summary>
public record CreateCustomerRequest(
    string Email,
    string? Name = null,
    string? Phone = null,
    Dictionary<string, string>? Metadata = null);

/// <summary>
/// Response de criação de cliente (modelo de domínio).
/// </summary>
public record CustomerResponse(
    string CustomerId,
    string? Email,
    string? Name,
    DateTime CreatedAt);
```

---

## Mapper

```csharp
// Infrastructure/ExternalServices/Stripe/Mappers/StripeMapper.cs
using Infrastructure.ExternalServices.Stripe.Models.Requests;
using Infrastructure.ExternalServices.Stripe.Models.Responses;

namespace Infrastructure.ExternalServices.Stripe.Mappers;

public class StripeMapper
{
    public CreatePaymentIntentApiRequest ToCreatePaymentApiRequest(CreatePaymentRequest request)
    {
        return new CreatePaymentIntentApiRequest
        {
            // Converter para centavos
            Amount = (long)(request.Amount * 100),
            Currency = request.Currency.ToLowerInvariant(),
            CustomerId = request.CustomerId,
            Description = request.Description,
            Metadata = request.Metadata
        };
    }
    
    public CreatePaymentResponse ToCreatePaymentResponse(PaymentIntentApiResponse response)
    {
        return new CreatePaymentResponse(
            PaymentId: response.Id,
            Status: response.Status,
            ClientSecret: response.ClientSecret,
            Amount: response.Amount / 100m, // Converter de centavos
            Currency: response.Currency.ToUpperInvariant(),
            CreatedAt: DateTimeOffset.FromUnixTimeSeconds(response.Created).UtcDateTime);
    }
    
    public PaymentDetailsResponse ToPaymentDetailsResponse(PaymentIntentApiResponse response)
    {
        return new PaymentDetailsResponse(
            PaymentId: response.Id,
            Status: response.Status,
            Amount: response.Amount / 100m,
            Currency: response.Currency.ToUpperInvariant(),
            CustomerId: response.CustomerId,
            Description: response.Description,
            CreatedAt: DateTimeOffset.FromUnixTimeSeconds(response.Created).UtcDateTime,
            CanceledAt: response.CanceledAt.HasValue 
                ? DateTimeOffset.FromUnixTimeSeconds(response.CanceledAt.Value).UtcDateTime 
                : null,
            CancellationReason: response.CancellationReason);
    }
    
    public CreateRefundApiRequest ToRefundApiRequest(RefundRequest request)
    {
        return new CreateRefundApiRequest
        {
            PaymentIntentId = request.PaymentId,
            Amount = request.Amount.HasValue ? (long)(request.Amount.Value * 100) : null,
            Reason = request.Reason
        };
    }
    
    public RefundResponse ToRefundResponse(RefundApiResponse response)
    {
        return new RefundResponse(
            RefundId: response.Id,
            PaymentId: response.PaymentIntentId,
            Status: response.Status,
            Amount: response.Amount / 100m,
            Currency: response.Currency.ToUpperInvariant(),
            CreatedAt: DateTimeOffset.FromUnixTimeSeconds(response.Created).UtcDateTime);
    }
    
    public CreateCustomerApiRequest ToCreateCustomerApiRequest(CreateCustomerRequest request)
    {
        return new CreateCustomerApiRequest
        {
            Email = request.Email,
            Name = request.Name,
            Phone = request.Phone,
            Metadata = request.Metadata
        };
    }
    
    public CustomerResponse ToCustomerResponse(CustomerApiResponse response)
    {
        return new CustomerResponse(
            CustomerId: response.Id,
            Email: response.Email,
            Name: response.Name,
            CreatedAt: DateTimeOffset.FromUnixTimeSeconds(response.Created).UtcDateTime);
    }
}
```
