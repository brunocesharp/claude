# Authentication (OAuth2 / Bearer Token)

## Tipos de Autenticação

| Tipo | Quando Usar | Exemplo |
|------|-------------|---------|
| **Static Bearer Token** | API Key fixa | Stripe, SendGrid |
| **OAuth2 Client Credentials** | Token com expiração | Salesforce, Microsoft Graph |
| **OAuth2 Authorization Code** | Ações em nome do usuário | Google APIs com user consent |

---

## Static Bearer Token

Para APIs com API Key/Secret que não expira:

```csharp
// Infrastructure/ExternalServices/Stripe/StripeAdapter.cs
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
        
        // Configurar Bearer Token estático
        SetBearerToken(_settings.SecretKey);
    }
}
```

---

## OAuth2 Client Credentials

Para tokens com expiração que precisam ser renovados:

### Token Service

```csharp
// Infrastructure/ExternalServices/Common/IOAuth2TokenService.cs
namespace Infrastructure.ExternalServices.Common;

public interface IOAuth2TokenService
{
    Task<string> GetAccessTokenAsync(string serviceName, CancellationToken ct = default);
    void InvalidateToken(string serviceName);
}

// Infrastructure/ExternalServices/Common/OAuth2TokenService.cs
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using System.Net.Http.Json;
using System.Text.Json.Serialization;

namespace Infrastructure.ExternalServices.Common;

public class OAuth2TokenService : IOAuth2TokenService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly IMemoryCache _cache;
    private readonly ILogger<OAuth2TokenService> _logger;
    private readonly Dictionary<string, OAuth2Config> _configs;
    
    public OAuth2TokenService(
        IHttpClientFactory httpClientFactory,
        IMemoryCache cache,
        ILogger<OAuth2TokenService> logger,
        IConfiguration configuration)
    {
        _httpClientFactory = httpClientFactory;
        _cache = cache;
        _logger = logger;
        
        // Carregar configurações de todos os serviços OAuth2
        _configs = configuration
            .GetSection("OAuth2")
            .Get<Dictionary<string, OAuth2Config>>() ?? new();
    }
    
    public async Task<string> GetAccessTokenAsync(string serviceName, CancellationToken ct = default)
    {
        var cacheKey = $"oauth2_token_{serviceName}";
        
        // Tentar obter do cache
        if (_cache.TryGetValue<string>(cacheKey, out var cachedToken))
        {
            return cachedToken!;
        }
        
        // Obter novo token
        var token = await FetchTokenAsync(serviceName, ct);
        
        // Cachear (com margem de segurança de 5 minutos antes da expiração)
        var cacheExpiration = TimeSpan.FromSeconds(token.ExpiresIn - 300);
        if (cacheExpiration > TimeSpan.Zero)
        {
            _cache.Set(cacheKey, token.AccessToken, cacheExpiration);
        }
        
        return token.AccessToken;
    }
    
    public void InvalidateToken(string serviceName)
    {
        var cacheKey = $"oauth2_token_{serviceName}";
        _cache.Remove(cacheKey);
        
        _logger.LogInformation("Token invalidated for {Service}", serviceName);
    }
    
    private async Task<OAuth2TokenResponse> FetchTokenAsync(string serviceName, CancellationToken ct)
    {
        if (!_configs.TryGetValue(serviceName, out var config))
        {
            throw new InvalidOperationException($"OAuth2 config not found for {serviceName}");
        }
        
        var client = _httpClientFactory.CreateClient();
        
        var requestBody = new Dictionary<string, string>
        {
            ["grant_type"] = "client_credentials",
            ["client_id"] = config.ClientId,
            ["client_secret"] = config.ClientSecret
        };
        
        // Adicionar scopes se configurado
        if (!string.IsNullOrEmpty(config.Scope))
        {
            requestBody["scope"] = config.Scope;
        }
        
        var request = new HttpRequestMessage(HttpMethod.Post, config.TokenUrl)
        {
            Content = new FormUrlEncodedContent(requestBody)
        };
        
        _logger.LogDebug("Fetching OAuth2 token for {Service} from {Url}", 
            serviceName, config.TokenUrl);
        
        var response = await client.SendAsync(request, ct);
        
        if (!response.IsSuccessStatusCode)
        {
            var error = await response.Content.ReadAsStringAsync(ct);
            _logger.LogError(
                "Failed to obtain OAuth2 token for {Service}. Status: {Status}, Error: {Error}",
                serviceName, response.StatusCode, error);
            
            throw new ExternalServiceException(
                serviceName,
                $"Failed to obtain access token: {error}",
                (int)response.StatusCode);
        }
        
        var tokenResponse = await response.Content.ReadFromJsonAsync<OAuth2TokenResponse>(ct);
        
        if (tokenResponse?.AccessToken is null)
        {
            throw new ExternalServiceException(serviceName, "Invalid token response");
        }
        
        _logger.LogInformation(
            "OAuth2 token obtained for {Service}. Expires in {ExpiresIn}s",
            serviceName, tokenResponse.ExpiresIn);
        
        return tokenResponse;
    }
}

public class OAuth2Config
{
    public string TokenUrl { get; set; } = string.Empty;
    public string ClientId { get; set; } = string.Empty;
    public string ClientSecret { get; set; } = string.Empty;
    public string? Scope { get; set; }
}

public class OAuth2TokenResponse
{
    [JsonPropertyName("access_token")]
    public string AccessToken { get; set; } = string.Empty;
    
    [JsonPropertyName("token_type")]
    public string TokenType { get; set; } = "Bearer";
    
    [JsonPropertyName("expires_in")]
    public int ExpiresIn { get; set; }
    
    [JsonPropertyName("scope")]
    public string? Scope { get; set; }
}
```

### appsettings.json

```json
{
  "OAuth2": {
    "Salesforce": {
      "TokenUrl": "https://login.salesforce.com/services/oauth2/token",
      "ClientId": "",
      "ClientSecret": "",
      "Scope": "api refresh_token"
    },
    "MicrosoftGraph": {
      "TokenUrl": "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
      "ClientId": "",
      "ClientSecret": "",
      "Scope": "https://graph.microsoft.com/.default"
    }
  }
}
```

---

## OAuth2 Adapter Base

```csharp
// Infrastructure/ExternalServices/Common/OAuth2HttpClientBase.cs
namespace Infrastructure.ExternalServices.Common;

/// <summary>
/// HttpClientBase com suporte a OAuth2 Client Credentials.
/// </summary>
public abstract class OAuth2HttpClientBase : HttpClientBase
{
    private readonly IOAuth2TokenService _tokenService;
    
    protected abstract string OAuth2ServiceName { get; }
    
    protected OAuth2HttpClientBase(
        HttpClient httpClient,
        IOAuth2TokenService tokenService,
        ILogger logger)
        : base(httpClient, logger)
    {
        _tokenService = tokenService;
    }
    
    protected override async Task<ExternalServiceResponse<T>> SendAsync<T>(
        HttpMethod method,
        string endpoint,
        HttpContent? content,
        CancellationToken ct)
    {
        // Obter token antes de cada request
        await EnsureAuthenticatedAsync(ct);
        
        var response = await base.SendAsync<T>(method, endpoint, content, ct);
        
        // Se 401, invalidar token e tentar novamente
        if (response.StatusCode == 401)
        {
            Logger.LogWarning("Received 401. Refreshing token for {Service}", OAuth2ServiceName);
            
            _tokenService.InvalidateToken(OAuth2ServiceName);
            await EnsureAuthenticatedAsync(ct);
            
            // Retry
            response = await base.SendAsync<T>(method, endpoint, content, ct);
        }
        
        return response;
    }
    
    private async Task EnsureAuthenticatedAsync(CancellationToken ct)
    {
        var token = await _tokenService.GetAccessTokenAsync(OAuth2ServiceName, ct);
        SetBearerToken(token);
    }
}
```

### Exemplo: Salesforce Adapter

```csharp
// Infrastructure/ExternalServices/Salesforce/SalesforceAdapter.cs
namespace Infrastructure.ExternalServices.Salesforce;

public class SalesforceAdapter : OAuth2HttpClientBase, ISalesforceGateway
{
    private readonly SalesforceSettings _settings;
    
    protected override string ServiceName => "Salesforce";
    protected override string OAuth2ServiceName => "Salesforce";
    
    public SalesforceAdapter(
        HttpClient httpClient,
        IOAuth2TokenService tokenService,
        IOptions<SalesforceSettings> settings,
        ILogger<SalesforceAdapter> logger)
        : base(httpClient, tokenService, logger)
    {
        _settings = settings.Value;
    }
    
    public async Task<Result<SalesforceContact>> GetContactAsync(
        string contactId,
        CancellationToken ct = default)
    {
        var response = await GetAsync<SalesforceContactApiResponse>(
            $"/services/data/v58.0/sobjects/Contact/{contactId}",
            ct);
        
        if (!response.IsSuccess)
        {
            return MapErrorToResult<SalesforceContact>(response);
        }
        
        return Result.Success(MapToContact(response.Data!));
    }
    
    public async Task<Result<string>> CreateContactAsync(
        CreateContactRequest request,
        CancellationToken ct = default)
    {
        var apiRequest = new
        {
            FirstName = request.FirstName,
            LastName = request.LastName,
            Email = request.Email
        };
        
        var response = await PostAsync<CreateRecordApiResponse>(
            "/services/data/v58.0/sobjects/Contact",
            apiRequest,
            ct);
        
        if (!response.IsSuccess)
        {
            return MapErrorToResult<string>(response);
        }
        
        return Result.Success(response.Data!.Id);
    }
}
```

---

## DelegatingHandler para Token

Alternativa usando DelegatingHandler:

```csharp
// Infrastructure/ExternalServices/Common/OAuth2AuthHandler.cs
namespace Infrastructure.ExternalServices.Common;

public class OAuth2AuthHandler : DelegatingHandler
{
    private readonly IOAuth2TokenService _tokenService;
    private readonly string _serviceName;
    
    public OAuth2AuthHandler(IOAuth2TokenService tokenService, string serviceName)
    {
        _tokenService = tokenService;
        _serviceName = serviceName;
    }
    
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken ct)
    {
        // Adicionar token
        var token = await _tokenService.GetAccessTokenAsync(_serviceName, ct);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        
        var response = await base.SendAsync(request, ct);
        
        // Se 401, renovar token e retry
        if (response.StatusCode == HttpStatusCode.Unauthorized)
        {
            _tokenService.InvalidateToken(_serviceName);
            
            token = await _tokenService.GetAccessTokenAsync(_serviceName, ct);
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
            
            response = await base.SendAsync(request, ct);
        }
        
        return response;
    }
}
```

### Registro com Handler

```csharp
// Infrastructure/ExternalServices/DependencyInjection.cs
public static IServiceCollection AddExternalServices(
    this IServiceCollection services,
    IConfiguration configuration)
{
    // Token Service
    services.AddMemoryCache();
    services.AddSingleton<IOAuth2TokenService, OAuth2TokenService>();
    
    // Salesforce com OAuth2 Handler
    services
        .AddHttpClient<ISalesforceGateway, SalesforceAdapter>((sp, client) =>
        {
            var settings = configuration
                .GetSection(SalesforceSettings.SectionName)
                .Get<SalesforceSettings>()!;
            
            client.BaseAddress = new Uri(settings.BaseUrl);
        })
        .AddHttpMessageHandler(sp =>
        {
            var tokenService = sp.GetRequiredService<IOAuth2TokenService>();
            return new OAuth2AuthHandler(tokenService, "Salesforce");
        })
        .AddStandardResilienceHandler();
    
    return services;
}
```

---

## Registro Completo

```csharp
// Infrastructure/ExternalServices/DependencyInjection.cs
using Infrastructure.ExternalServices.Common;
using Infrastructure.ExternalServices.Stripe;
using Infrastructure.ExternalServices.Salesforce;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Http.Resilience;

namespace Infrastructure.ExternalServices;

public static class DependencyInjection
{
    public static IServiceCollection AddExternalServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Cache para tokens
        services.AddMemoryCache();
        
        // Token Service OAuth2
        services.AddSingleton<IOAuth2TokenService, OAuth2TokenService>();
        
        // === Stripe (Static Bearer Token) ===
        services.Configure<StripeSettings>(
            configuration.GetSection(StripeSettings.SectionName));
        
        var stripeSettings = configuration
            .GetSection(StripeSettings.SectionName)
            .Get<StripeSettings>()!;
        
        services
            .AddHttpClient<IStripeGateway, StripeAdapter>((sp, client) =>
            {
                client.BaseAddress = new Uri(stripeSettings.BaseUrl);
                client.Timeout = TimeSpan.FromSeconds(stripeSettings.TimeoutSeconds);
            })
            .AddStandardResilienceHandler();
        
        // === Salesforce (OAuth2 Client Credentials) ===
        services.Configure<SalesforceSettings>(
            configuration.GetSection(SalesforceSettings.SectionName));
        
        var salesforceSettings = configuration
            .GetSection(SalesforceSettings.SectionName)
            .Get<SalesforceSettings>()!;
        
        services
            .AddHttpClient<ISalesforceGateway, SalesforceAdapter>((sp, client) =>
            {
                client.BaseAddress = new Uri(salesforceSettings.BaseUrl);
                client.Timeout = TimeSpan.FromSeconds(salesforceSettings.TimeoutSeconds);
            })
            .AddHttpMessageHandler(sp =>
            {
                var tokenService = sp.GetRequiredService<IOAuth2TokenService>();
                return new OAuth2AuthHandler(tokenService, "Salesforce");
            })
            .AddStandardResilienceHandler();
        
        return services;
    }
}
```

---

## Testes

```csharp
// Tests/Infrastructure.Tests/ExternalServices/OAuth2TokenServiceTests.cs
public class OAuth2TokenServiceTests
{
    [Fact]
    public async Task Should_CacheToken_AndReuse()
    {
        // Arrange
        var handler = new MockHttpMessageHandler();
        handler.SetupReturns(HttpStatusCode.OK, new OAuth2TokenResponse
        {
            AccessToken = "token123",
            ExpiresIn = 3600
        });
        
        var service = CreateTokenService(handler);
        
        // Act
        var token1 = await service.GetAccessTokenAsync("TestService", CancellationToken.None);
        var token2 = await service.GetAccessTokenAsync("TestService", CancellationToken.None);
        
        // Assert
        token1.Should().Be("token123");
        token2.Should().Be("token123");
        handler.CallCount.Should().Be(1); // Apenas uma chamada HTTP
    }
    
    [Fact]
    public async Task Should_FetchNewToken_AfterInvalidation()
    {
        // Arrange
        var handler = new MockHttpMessageHandler();
        handler.SetupSequence()
            .Returns(HttpStatusCode.OK, new OAuth2TokenResponse { AccessToken = "token1", ExpiresIn = 3600 })
            .Returns(HttpStatusCode.OK, new OAuth2TokenResponse { AccessToken = "token2", ExpiresIn = 3600 });
        
        var service = CreateTokenService(handler);
        
        // Act
        var token1 = await service.GetAccessTokenAsync("TestService", CancellationToken.None);
        service.InvalidateToken("TestService");
        var token2 = await service.GetAccessTokenAsync("TestService", CancellationToken.None);
        
        // Assert
        token1.Should().Be("token1");
        token2.Should().Be("token2");
        handler.CallCount.Should().Be(2);
    }
}
```
