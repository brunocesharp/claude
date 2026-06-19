# Resilience (Polly)

## Pacotes Necessários

```xml
<PackageReference Include="Microsoft.Extensions.Http.Resilience" Version="8.5.0" />
```

> **Nota**: `Microsoft.Extensions.Http.Resilience` é a forma recomendada de usar Polly com HttpClient no .NET 8+. Ele encapsula Polly v8 com uma API mais simples.

---

## Configuração no DI

```csharp
// Infrastructure/ExternalServices/DependencyInjection.cs
using Infrastructure.ExternalServices.Common;
using Infrastructure.ExternalServices.Stripe;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Http.Resilience;
using Polly;

namespace Infrastructure.ExternalServices;

public static class DependencyInjection
{
    public static IServiceCollection AddExternalServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Stripe
        services.Configure<StripeSettings>(
            configuration.GetSection(StripeSettings.SectionName));
        
        services
            .AddHttpClient<IStripeGateway, StripeAdapter>((sp, client) =>
            {
                var settings = configuration
                    .GetSection(StripeSettings.SectionName)
                    .Get<StripeSettings>()!;
                
                client.BaseAddress = new Uri(settings.BaseUrl);
                client.Timeout = TimeSpan.FromSeconds(settings.TimeoutSeconds);
                client.DefaultRequestHeaders.Add("Accept", "application/json");
            })
            .AddStandardResilienceHandler(options =>
            {
                // Configurar retry
                options.Retry.MaxRetryAttempts = 3;
                options.Retry.Delay = TimeSpan.FromMilliseconds(500);
                options.Retry.UseJitter = true;
                options.Retry.BackoffType = DelayBackoffType.Exponential;
                
                // Configurar circuit breaker
                options.CircuitBreaker.SamplingDuration = TimeSpan.FromSeconds(30);
                options.CircuitBreaker.FailureRatio = 0.5;
                options.CircuitBreaker.MinimumThroughput = 10;
                options.CircuitBreaker.BreakDuration = TimeSpan.FromSeconds(30);
                
                // Configurar timeout total
                options.TotalRequestTimeout.Timeout = TimeSpan.FromSeconds(60);
                
                // Configurar timeout por tentativa
                options.AttemptTimeout.Timeout = TimeSpan.FromSeconds(10);
            });
        
        return services;
    }
}
```

---

## Configuração Customizada (Avançada)

Para casos que precisam de mais controle:

```csharp
// Infrastructure/ExternalServices/DependencyInjection.cs
using Microsoft.Extensions.Http.Resilience;
using Polly;
using Polly.CircuitBreaker;
using Polly.Retry;
using Polly.Timeout;

public static class DependencyInjection
{
    public static IServiceCollection AddExternalServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Configuração customizada para Stripe
        services
            .AddHttpClient<IStripeGateway, StripeAdapter>(ConfigureStripeClient)
            .AddResilienceHandler("stripe-pipeline", ConfigureStripePipeline);
        
        return services;
    }
    
    private static void ConfigureStripeClient(
        IServiceProvider sp, 
        HttpClient client)
    {
        var configuration = sp.GetRequiredService<IConfiguration>();
        var settings = configuration
            .GetSection(StripeSettings.SectionName)
            .Get<StripeSettings>()!;
        
        client.BaseAddress = new Uri(settings.BaseUrl);
        client.Timeout = TimeSpan.FromSeconds(settings.TimeoutSeconds);
        client.DefaultRequestHeaders.Add("Accept", "application/json");
        client.DefaultRequestHeaders.Add("User-Agent", "MyApp/1.0");
    }
    
    private static void ConfigureStripePipeline(
        ResiliencePipelineBuilder<HttpResponseMessage> builder,
        ResilienceHandlerContext context)
    {
        var logger = context.ServiceProvider
            .GetRequiredService<ILogger<StripeAdapter>>();
        
        // 1. Timeout total (outermost)
        builder.AddTimeout(new TimeoutStrategyOptions
        {
            Timeout = TimeSpan.FromSeconds(60),
            Name = "TotalTimeout",
            OnTimeout = args =>
            {
                logger.LogWarning(
                    "Total timeout exceeded for Stripe request after {Timeout}s",
                    args.Timeout.TotalSeconds);
                return default;
            }
        });
        
        // 2. Retry
        builder.AddRetry(new RetryStrategyOptions<HttpResponseMessage>
        {
            MaxRetryAttempts = 3,
            Delay = TimeSpan.FromMilliseconds(500),
            BackoffType = DelayBackoffType.Exponential,
            UseJitter = true,
            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                .Handle<HttpRequestException>()
                .Handle<TimeoutRejectedException>()
                .HandleResult(r => r.StatusCode >= System.Net.HttpStatusCode.InternalServerError)
                .HandleResult(r => r.StatusCode == System.Net.HttpStatusCode.RequestTimeout)
                .HandleResult(r => r.StatusCode == System.Net.HttpStatusCode.TooManyRequests),
            OnRetry = args =>
            {
                logger.LogWarning(
                    "Retry {Attempt} for Stripe request after {Delay}ms. Reason: {Reason}",
                    args.AttemptNumber,
                    args.RetryDelay.TotalMilliseconds,
                    args.Outcome.Exception?.Message ?? args.Outcome.Result?.StatusCode.ToString());
                return default;
            }
        });
        
        // 3. Circuit Breaker
        builder.AddCircuitBreaker(new CircuitBreakerStrategyOptions<HttpResponseMessage>
        {
            SamplingDuration = TimeSpan.FromSeconds(30),
            FailureRatio = 0.5,
            MinimumThroughput = 10,
            BreakDuration = TimeSpan.FromSeconds(30),
            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                .Handle<HttpRequestException>()
                .Handle<TimeoutRejectedException>()
                .HandleResult(r => r.StatusCode >= System.Net.HttpStatusCode.InternalServerError),
            OnOpened = args =>
            {
                logger.LogError(
                    "Circuit breaker OPENED for Stripe. Break duration: {Duration}s",
                    args.BreakDuration.TotalSeconds);
                return default;
            },
            OnClosed = args =>
            {
                logger.LogInformation("Circuit breaker CLOSED for Stripe");
                return default;
            },
            OnHalfOpened = args =>
            {
                logger.LogInformation("Circuit breaker HALF-OPENED for Stripe");
                return default;
            }
        });
        
        // 4. Timeout por tentativa (innermost)
        builder.AddTimeout(new TimeoutStrategyOptions
        {
            Timeout = TimeSpan.FromSeconds(10),
            Name = "AttemptTimeout"
        });
    }
}
```

---

## Settings com Configuração de Resiliência

```csharp
// Infrastructure/ExternalServices/Stripe/StripeSettings.cs
namespace Infrastructure.ExternalServices.Stripe;

public class StripeSettings
{
    public const string SectionName = "ExternalServices:Stripe";
    
    public string BaseUrl { get; set; } = string.Empty;
    public string SecretKey { get; set; } = string.Empty;
    
    // Timeout
    public int TimeoutSeconds { get; set; } = 30;
    public int AttemptTimeoutSeconds { get; set; } = 10;
    
    // Retry
    public int RetryCount { get; set; } = 3;
    public int RetryDelayMilliseconds { get; set; } = 500;
    
    // Circuit Breaker
    public int CircuitBreakerFailureThreshold { get; set; } = 5;
    public int CircuitBreakerSamplingDurationSeconds { get; set; } = 30;
    public int CircuitBreakerBreakDurationSeconds { get; set; } = 30;
    public double CircuitBreakerFailureRatio { get; set; } = 0.5;
    public int CircuitBreakerMinimumThroughput { get; set; } = 10;
}
```

### appsettings.json

```json
{
  "ExternalServices": {
    "Stripe": {
      "BaseUrl": "https://api.stripe.com",
      "SecretKey": "",
      "TimeoutSeconds": 30,
      "AttemptTimeoutSeconds": 10,
      "RetryCount": 3,
      "RetryDelayMilliseconds": 500,
      "CircuitBreakerFailureThreshold": 5,
      "CircuitBreakerSamplingDurationSeconds": 30,
      "CircuitBreakerBreakDurationSeconds": 30,
      "CircuitBreakerFailureRatio": 0.5,
      "CircuitBreakerMinimumThroughput": 10
    }
  }
}
```

---

## Configuração Dinâmica (baseada em Settings)

```csharp
public static IServiceCollection AddExternalServices(
    this IServiceCollection services,
    IConfiguration configuration)
{
    var stripeSettings = configuration
        .GetSection(StripeSettings.SectionName)
        .Get<StripeSettings>()!;
    
    services.Configure<StripeSettings>(
        configuration.GetSection(StripeSettings.SectionName));
    
    services
        .AddHttpClient<IStripeGateway, StripeAdapter>((sp, client) =>
        {
            client.BaseAddress = new Uri(stripeSettings.BaseUrl);
            client.Timeout = TimeSpan.FromSeconds(stripeSettings.TimeoutSeconds);
        })
        .AddStandardResilienceHandler(options =>
        {
            // Retry baseado em settings
            options.Retry.MaxRetryAttempts = stripeSettings.RetryCount;
            options.Retry.Delay = TimeSpan.FromMilliseconds(stripeSettings.RetryDelayMilliseconds);
            options.Retry.UseJitter = true;
            options.Retry.BackoffType = DelayBackoffType.Exponential;
            
            // Circuit breaker baseado em settings
            options.CircuitBreaker.SamplingDuration = 
                TimeSpan.FromSeconds(stripeSettings.CircuitBreakerSamplingDurationSeconds);
            options.CircuitBreaker.FailureRatio = stripeSettings.CircuitBreakerFailureRatio;
            options.CircuitBreaker.MinimumThroughput = stripeSettings.CircuitBreakerMinimumThroughput;
            options.CircuitBreaker.BreakDuration = 
                TimeSpan.FromSeconds(stripeSettings.CircuitBreakerBreakDurationSeconds);
            
            // Timeouts
            options.TotalRequestTimeout.Timeout = 
                TimeSpan.FromSeconds(stripeSettings.TimeoutSeconds);
            options.AttemptTimeout.Timeout = 
                TimeSpan.FromSeconds(stripeSettings.AttemptTimeoutSeconds);
        });
    
    return services;
}
```

---

## Tratamento de Exceções no Adapter

```csharp
public class StripeAdapter : HttpClientBase, IStripeGateway
{
    public async Task<Result<CreatePaymentResponse>> CreatePaymentAsync(
        CreatePaymentRequest request,
        CancellationToken ct = default)
    {
        try
        {
            var apiRequest = _mapper.ToCreatePaymentApiRequest(request);
            
            var response = await PostAsync<PaymentIntentApiResponse>(
                "/v1/payment_intents",
                apiRequest,
                ct);
            
            if (!response.IsSuccess)
                return MapErrorToResult<CreatePaymentResponse>(response);
            
            return Result.Success(_mapper.ToCreatePaymentResponse(response.Data!));
        }
        catch (BrokenCircuitException)
        {
            Logger.LogError("Stripe circuit breaker is open. Service temporarily unavailable.");
            return Result<CreatePaymentResponse>.Error(
                "Payment service temporarily unavailable. Please try again later.");
        }
        catch (TimeoutRejectedException)
        {
            Logger.LogError("Stripe request timed out.");
            return Result<CreatePaymentResponse>.Error(
                "Payment service timeout. Please try again.");
        }
        catch (HttpRequestException ex)
        {
            Logger.LogError(ex, "Network error calling Stripe.");
            return Result<CreatePaymentResponse>.Error(
                "Unable to connect to payment service.");
        }
    }
}
```

---

## Teste de Resiliência

```csharp
// Tests/Infrastructure.Tests/ExternalServices/StripeResilienceTests.cs
public class StripeResilienceTests
{
    [Fact]
    public async Task Should_Retry_On_TransientError()
    {
        // Arrange
        var handler = new MockHttpMessageHandler();
        handler.SetupSequence()
            .Returns(HttpStatusCode.ServiceUnavailable)
            .Returns(HttpStatusCode.ServiceUnavailable)
            .Returns(HttpStatusCode.OK, new PaymentIntentApiResponse { Id = "pi_123" });
        
        var adapter = CreateAdapter(handler);
        
        // Act
        var result = await adapter.CreatePaymentAsync(new CreatePaymentRequest(100, "usd"), CancellationToken.None);
        
        // Assert
        result.IsSuccess.Should().BeTrue();
        handler.CallCount.Should().Be(3);
    }
    
    [Fact]
    public async Task Should_OpenCircuitBreaker_After_FailureThreshold()
    {
        // Arrange
        var handler = new MockHttpMessageHandler();
        handler.SetupAlwaysReturns(HttpStatusCode.InternalServerError);
        
        var adapter = CreateAdapter(handler);
        
        // Act - fazer múltiplas chamadas para abrir o circuit breaker
        for (int i = 0; i < 15; i++)
        {
            await adapter.CreatePaymentAsync(new CreatePaymentRequest(100, "usd"), CancellationToken.None);
        }
        
        // Assert - próxima chamada deve falhar imediatamente com BrokenCircuitException
        var act = () => adapter.CreatePaymentAsync(
            new CreatePaymentRequest(100, "usd"), 
            CancellationToken.None);
        
        await act.Should().ThrowAsync<BrokenCircuitException>();
    }
}
```
