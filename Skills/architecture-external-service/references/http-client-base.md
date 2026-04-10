# HttpClientBase

## Estrutura de Arquivos

```
Infrastructure/
└── ExternalServices/
    └── Common/
        ├── HttpClientBase.cs
        ├── ExternalServiceResponse.cs
        └── ExternalServiceException.cs
```

---

## ExternalServiceResponse

```csharp
// Infrastructure/ExternalServices/Common/ExternalServiceResponse.cs
namespace Infrastructure.ExternalServices.Common;

/// <summary>
/// Resposta padronizada de chamadas a serviços externos.
/// </summary>
public class ExternalServiceResponse<T>
{
    public bool IsSuccess { get; private init; }
    public T? Data { get; private init; }
    public int StatusCode { get; private init; }
    public string? ErrorMessage { get; private init; }
    public string? ErrorCode { get; private init; }
    public Dictionary<string, object>? ErrorDetails { get; private init; }
    
    private ExternalServiceResponse() { }
    
    public static ExternalServiceResponse<T> Success(T data, int statusCode = 200)
    {
        return new ExternalServiceResponse<T>
        {
            IsSuccess = true,
            Data = data,
            StatusCode = statusCode
        };
    }
    
    public static ExternalServiceResponse<T> Failure(
        int statusCode,
        string errorMessage,
        string? errorCode = null,
        Dictionary<string, object>? errorDetails = null)
    {
        return new ExternalServiceResponse<T>
        {
            IsSuccess = false,
            StatusCode = statusCode,
            ErrorMessage = errorMessage,
            ErrorCode = errorCode,
            ErrorDetails = errorDetails
        };
    }
    
    public static ExternalServiceResponse<T> FromException(Exception ex)
    {
        return new ExternalServiceResponse<T>
        {
            IsSuccess = false,
            StatusCode = 0,
            ErrorMessage = ex.Message,
            ErrorCode = ex.GetType().Name
        };
    }
}

// Versão não-genérica para respostas sem corpo
public class ExternalServiceResponse
{
    public bool IsSuccess { get; private init; }
    public int StatusCode { get; private init; }
    public string? ErrorMessage { get; private init; }
    public string? ErrorCode { get; private init; }
    
    private ExternalServiceResponse() { }
    
    public static ExternalServiceResponse Success(int statusCode = 200)
    {
        return new ExternalServiceResponse
        {
            IsSuccess = true,
            StatusCode = statusCode
        };
    }
    
    public static ExternalServiceResponse Failure(
        int statusCode,
        string errorMessage,
        string? errorCode = null)
    {
        return new ExternalServiceResponse
        {
            IsSuccess = false,
            StatusCode = statusCode,
            ErrorMessage = errorMessage,
            ErrorCode = errorCode
        };
    }
}
```

---

## ExternalServiceException

```csharp
// Infrastructure/ExternalServices/Common/ExternalServiceException.cs
namespace Infrastructure.ExternalServices.Common;

/// <summary>
/// Exceção para erros de serviços externos.
/// </summary>
public class ExternalServiceException : Exception
{
    public string ServiceName { get; }
    public int? StatusCode { get; }
    public string? ErrorCode { get; }
    public string? ResponseBody { get; }
    
    public ExternalServiceException(
        string serviceName,
        string message,
        int? statusCode = null,
        string? errorCode = null,
        string? responseBody = null,
        Exception? innerException = null)
        : base(message, innerException)
    {
        ServiceName = serviceName;
        StatusCode = statusCode;
        ErrorCode = errorCode;
        ResponseBody = responseBody;
    }
    
    public override string ToString()
    {
        return $"[{ServiceName}] {Message} (StatusCode: {StatusCode}, ErrorCode: {ErrorCode})";
    }
}
```

---

## HttpClientBase

```csharp
// Infrastructure/ExternalServices/Common/HttpClientBase.cs
using Microsoft.Extensions.Logging;
using System.Diagnostics;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Infrastructure.ExternalServices.Common;

/// <summary>
/// Classe base para clientes HTTP com logging estruturado e serialização padronizada.
/// </summary>
public abstract class HttpClientBase
{
    protected readonly HttpClient HttpClient;
    protected readonly ILogger Logger;
    
    protected virtual string ServiceName => GetType().Name.Replace("Adapter", "");
    
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        WriteIndented = false,
        Converters =
        {
            new JsonStringEnumConverter(JsonNamingPolicy.CamelCase)
        }
    };
    
    protected HttpClientBase(HttpClient httpClient, ILogger logger)
    {
        HttpClient = httpClient;
        Logger = logger;
    }
    
    #region GET
    
    protected async Task<ExternalServiceResponse<T>> GetAsync<T>(
        string endpoint,
        CancellationToken ct = default)
    {
        return await SendAsync<T>(HttpMethod.Get, endpoint, content: null, ct);
    }
    
    protected async Task<ExternalServiceResponse<T>> GetAsync<T>(
        string endpoint,
        Dictionary<string, string>? queryParams,
        CancellationToken ct = default)
    {
        var url = BuildUrlWithQuery(endpoint, queryParams);
        return await SendAsync<T>(HttpMethod.Get, url, content: null, ct);
    }
    
    #endregion
    
    #region POST
    
    protected async Task<ExternalServiceResponse<TResponse>> PostAsync<TResponse>(
        string endpoint,
        object? body,
        CancellationToken ct = default)
    {
        var content = CreateJsonContent(body);
        return await SendAsync<TResponse>(HttpMethod.Post, endpoint, content, ct);
    }
    
    protected async Task<ExternalServiceResponse> PostAsync(
        string endpoint,
        object? body,
        CancellationToken ct = default)
    {
        var content = CreateJsonContent(body);
        return await SendAsync(HttpMethod.Post, endpoint, content, ct);
    }
    
    protected async Task<ExternalServiceResponse<TResponse>> PostFormAsync<TResponse>(
        string endpoint,
        Dictionary<string, string> formData,
        CancellationToken ct = default)
    {
        var content = new FormUrlEncodedContent(formData);
        return await SendAsync<TResponse>(HttpMethod.Post, endpoint, content, ct);
    }
    
    #endregion
    
    #region PUT
    
    protected async Task<ExternalServiceResponse<TResponse>> PutAsync<TResponse>(
        string endpoint,
        object? body,
        CancellationToken ct = default)
    {
        var content = CreateJsonContent(body);
        return await SendAsync<TResponse>(HttpMethod.Put, endpoint, content, ct);
    }
    
    protected async Task<ExternalServiceResponse> PutAsync(
        string endpoint,
        object? body,
        CancellationToken ct = default)
    {
        var content = CreateJsonContent(body);
        return await SendAsync(HttpMethod.Put, endpoint, content, ct);
    }
    
    #endregion
    
    #region PATCH
    
    protected async Task<ExternalServiceResponse<TResponse>> PatchAsync<TResponse>(
        string endpoint,
        object? body,
        CancellationToken ct = default)
    {
        var content = CreateJsonContent(body);
        return await SendAsync<TResponse>(HttpMethod.Patch, endpoint, content, ct);
    }
    
    #endregion
    
    #region DELETE
    
    protected async Task<ExternalServiceResponse> DeleteAsync(
        string endpoint,
        CancellationToken ct = default)
    {
        return await SendAsync(HttpMethod.Delete, endpoint, content: null, ct);
    }
    
    protected async Task<ExternalServiceResponse<TResponse>> DeleteAsync<TResponse>(
        string endpoint,
        CancellationToken ct = default)
    {
        return await SendAsync<TResponse>(HttpMethod.Delete, endpoint, content: null, ct);
    }
    
    #endregion
    
    #region Core Send Methods
    
    protected virtual async Task<ExternalServiceResponse<T>> SendAsync<T>(
        HttpMethod method,
        string endpoint,
        HttpContent? content,
        CancellationToken ct)
    {
        var stopwatch = Stopwatch.StartNew();
        var requestId = Guid.NewGuid().ToString("N")[..8];
        
        using var request = new HttpRequestMessage(method, endpoint);
        
        if (content is not null)
            request.Content = content;
        
        // Log request
        LogRequest(requestId, method, endpoint, content);
        
        try
        {
            using var response = await HttpClient.SendAsync(request, ct);
            stopwatch.Stop();
            
            var responseBody = await response.Content.ReadAsStringAsync(ct);
            
            // Log response
            LogResponse(requestId, method, endpoint, response.StatusCode, stopwatch.ElapsedMilliseconds, responseBody);
            
            if (!response.IsSuccessStatusCode)
            {
                var errorResponse = TryParseErrorResponse(responseBody);
                
                return ExternalServiceResponse<T>.Failure(
                    (int)response.StatusCode,
                    errorResponse?.Message ?? $"Request failed with status {response.StatusCode}",
                    errorResponse?.Code,
                    errorResponse?.Details);
            }
            
            // Deserialize response
            if (string.IsNullOrWhiteSpace(responseBody))
            {
                return ExternalServiceResponse<T>.Success(default!, (int)response.StatusCode);
            }
            
            var data = JsonSerializer.Deserialize<T>(responseBody, JsonOptions);
            
            return ExternalServiceResponse<T>.Success(data!, (int)response.StatusCode);
        }
        catch (TaskCanceledException ex) when (ex.InnerException is TimeoutException)
        {
            stopwatch.Stop();
            LogError(requestId, method, endpoint, "Timeout", stopwatch.ElapsedMilliseconds);
            
            return ExternalServiceResponse<T>.Failure(
                408,
                $"Request to {ServiceName} timed out",
                "TIMEOUT");
        }
        catch (HttpRequestException ex)
        {
            stopwatch.Stop();
            LogError(requestId, method, endpoint, ex.Message, stopwatch.ElapsedMilliseconds);
            
            return ExternalServiceResponse<T>.Failure(
                0,
                $"Network error calling {ServiceName}: {ex.Message}",
                "NETWORK_ERROR");
        }
        catch (JsonException ex)
        {
            stopwatch.Stop();
            LogError(requestId, method, endpoint, $"JSON parse error: {ex.Message}", stopwatch.ElapsedMilliseconds);
            
            return ExternalServiceResponse<T>.Failure(
                0,
                $"Failed to parse response from {ServiceName}",
                "PARSE_ERROR");
        }
    }
    
    protected virtual async Task<ExternalServiceResponse> SendAsync(
        HttpMethod method,
        string endpoint,
        HttpContent? content,
        CancellationToken ct)
    {
        var response = await SendAsync<object>(method, endpoint, content, ct);
        
        if (response.IsSuccess)
            return ExternalServiceResponse.Success(response.StatusCode);
        
        return ExternalServiceResponse.Failure(
            response.StatusCode,
            response.ErrorMessage!,
            response.ErrorCode);
    }
    
    #endregion
    
    #region Helpers
    
    protected StringContent CreateJsonContent(object? body)
    {
        if (body is null)
            return new StringContent("{}", Encoding.UTF8, "application/json");
        
        var json = JsonSerializer.Serialize(body, JsonOptions);
        return new StringContent(json, Encoding.UTF8, "application/json");
    }
    
    protected string BuildUrlWithQuery(string endpoint, Dictionary<string, string>? queryParams)
    {
        if (queryParams is null || queryParams.Count == 0)
            return endpoint;
        
        var query = string.Join("&", queryParams
            .Where(kv => !string.IsNullOrEmpty(kv.Value))
            .Select(kv => $"{Uri.EscapeDataString(kv.Key)}={Uri.EscapeDataString(kv.Value)}"));
        
        return string.IsNullOrEmpty(query) ? endpoint : $"{endpoint}?{query}";
    }
    
    protected void SetBearerToken(string token)
    {
        HttpClient.DefaultRequestHeaders.Authorization = 
            new AuthenticationHeaderValue("Bearer", token);
    }
    
    protected void SetHeader(string name, string value)
    {
        HttpClient.DefaultRequestHeaders.Remove(name);
        HttpClient.DefaultRequestHeaders.Add(name, value);
    }
    
    #endregion
    
    #region Error Parsing
    
    protected virtual ErrorResponse? TryParseErrorResponse(string responseBody)
    {
        if (string.IsNullOrWhiteSpace(responseBody))
            return null;
        
        try
        {
            // Tentar formato padrão
            var error = JsonSerializer.Deserialize<ErrorResponse>(responseBody, JsonOptions);
            if (error?.Message is not null)
                return error;
            
            // Tentar formato alternativo com "error" wrapper
            var wrapped = JsonSerializer.Deserialize<WrappedErrorResponse>(responseBody, JsonOptions);
            return wrapped?.Error;
        }
        catch
        {
            return new ErrorResponse { Message = responseBody };
        }
    }
    
    protected record ErrorResponse
    {
        public string? Message { get; init; }
        public string? Code { get; init; }
        public Dictionary<string, object>? Details { get; init; }
    }
    
    private record WrappedErrorResponse
    {
        public ErrorResponse? Error { get; init; }
    }
    
    #endregion
    
    #region Logging
    
    private void LogRequest(string requestId, HttpMethod method, string endpoint, HttpContent? content)
    {
        // Não logar corpo de requests sensíveis
        var sanitizedEndpoint = SanitizeForLogging(endpoint);
        
        Logger.LogInformation(
            "[{Service}] [{RequestId}] → {Method} {Endpoint}",
            ServiceName,
            requestId,
            method,
            sanitizedEndpoint);
    }
    
    private void LogResponse(
        string requestId,
        HttpMethod method,
        string endpoint,
        System.Net.HttpStatusCode statusCode,
        long elapsedMs,
        string responseBody)
    {
        var sanitizedEndpoint = SanitizeForLogging(endpoint);
        var truncatedBody = TruncateForLogging(responseBody, 500);
        
        if ((int)statusCode >= 400)
        {
            Logger.LogWarning(
                "[{Service}] [{RequestId}] ← {StatusCode} {Method} {Endpoint} ({ElapsedMs}ms) Response: {Response}",
                ServiceName,
                requestId,
                (int)statusCode,
                method,
                sanitizedEndpoint,
                elapsedMs,
                truncatedBody);
        }
        else
        {
            Logger.LogInformation(
                "[{Service}] [{RequestId}] ← {StatusCode} {Method} {Endpoint} ({ElapsedMs}ms)",
                ServiceName,
                requestId,
                (int)statusCode,
                method,
                sanitizedEndpoint,
                elapsedMs);
        }
    }
    
    private void LogError(string requestId, HttpMethod method, string endpoint, string error, long elapsedMs)
    {
        var sanitizedEndpoint = SanitizeForLogging(endpoint);
        
        Logger.LogError(
            "[{Service}] [{RequestId}] ✗ {Method} {Endpoint} ({ElapsedMs}ms) Error: {Error}",
            ServiceName,
            requestId,
            method,
            sanitizedEndpoint,
            elapsedMs,
            error);
    }
    
    protected virtual string SanitizeForLogging(string value)
    {
        // Remover tokens, keys, senhas de query strings
        var sensitiveParams = new[] { "key", "token", "secret", "password", "api_key", "apikey", "access_token" };
        
        foreach (var param in sensitiveParams)
        {
            var pattern = $@"({param}=)[^&]+";
            value = System.Text.RegularExpressions.Regex.Replace(
                value, 
                pattern, 
                $"$1[REDACTED]", 
                System.Text.RegularExpressions.RegexOptions.IgnoreCase);
        }
        
        return value;
    }
    
    private static string TruncateForLogging(string value, int maxLength)
    {
        if (string.IsNullOrEmpty(value) || value.Length <= maxLength)
            return value;
        
        return value[..maxLength] + "...[truncated]";
    }
    
    #endregion
}
```

---

## Exemplo de Uso

```csharp
public class StripeAdapter : HttpClientBase, IStripeGateway
{
    private readonly StripeSettings _settings;
    
    public StripeAdapter(
        HttpClient httpClient,
        IOptions<StripeSettings> settings,
        ILogger<StripeAdapter> logger)
        : base(httpClient, logger)
    {
        _settings = settings.Value;
    }
    
    public async Task<Result<PaymentResponse>> CreatePaymentAsync(
        CreatePaymentRequest request,
        CancellationToken ct)
    {
        var apiRequest = new CreatePaymentApiRequest
        {
            Amount = request.Amount,
            Currency = request.Currency,
            CustomerId = request.CustomerId
        };
        
        var response = await PostAsync<CreatePaymentApiResponse>("/v1/payments", apiRequest, ct);
        
        if (!response.IsSuccess)
        {
            Logger.LogWarning("Payment creation failed: {Error}", response.ErrorMessage);
            return Result.Error(response.ErrorMessage ?? "Payment failed");
        }
        
        return Result.Success(new PaymentResponse
        {
            PaymentId = response.Data!.Id,
            Status = response.Data.Status
        });
    }
}
```
