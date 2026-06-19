# Pipeline Behaviors

## Visão Geral

Behaviors são middlewares do MediatR que interceptam requests antes/depois do handler.

```
Request → ValidationBehavior → LoggingBehavior → Handler → Response
```

## Estrutura de Arquivos

```
Application/
└── Common/
    └── Behaviors/
        ├── ValidationBehavior.cs
        ├── LoggingBehavior.cs
        ├── PerformanceBehavior.cs
        ├── UnhandledExceptionBehavior.cs
        └── TransactionBehavior.cs
```

---

## ValidationBehavior

Executa validators FluentValidation antes do handler.

```csharp
using FluentValidation;
using MediatR;

namespace Application.Common.Behaviors;

public class ValidationBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        if (!_validators.Any())
            return await next();

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, ct)));

        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();

        if (failures.Count != 0)
            throw new ValidationException(failures);

        return await next();
    }
}
```

### ValidationBehavior com Result Pattern

Quando handlers retornam `Result<T>`, o behavior pode retornar `Result.Invalid()`:

```csharp
using Ardalis.Result;
using FluentValidation;
using MediatR;

namespace Application.Common.Behaviors;

public class ValidationBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        if (!_validators.Any())
            return await next();

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, ct)));

        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();

        if (failures.Count != 0)
        {
            // Se TResponse é Result ou Result<T>, retornar Invalid
            if (typeof(TResponse).IsGenericType && 
                typeof(TResponse).GetGenericTypeDefinition() == typeof(Result<>))
            {
                var resultType = typeof(TResponse).GetGenericArguments()[0];
                var invalidMethod = typeof(Result<>)
                    .MakeGenericType(resultType)
                    .GetMethod(nameof(Result<object>.Invalid), 
                        new[] { typeof(IEnumerable<ValidationError>) });

                var validationErrors = failures
                    .Select(f => new ValidationError(f.PropertyName, f.ErrorMessage));

                return (TResponse)invalidMethod!.Invoke(null, new object[] { validationErrors })!;
            }

            if (typeof(TResponse) == typeof(Result))
            {
                var validationErrors = failures
                    .Select(f => new ValidationError(f.PropertyName, f.ErrorMessage));
                
                return (TResponse)(object)Result.Invalid(validationErrors.ToList());
            }

            // Fallback: throw exception
            throw new ValidationException(failures);
        }

        return await next();
    }
}
```

---

## LoggingBehavior

Loga requests e responses para debugging.

```csharp
using MediatR;
using Microsoft.Extensions.Logging;
using System.Diagnostics;

namespace Application.Common.Behaviors;

public class LoggingBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        var requestName = typeof(TRequest).Name;

        _logger.LogInformation(
            "Handling {RequestName} {@Request}",
            requestName,
            request);

        var response = await next();

        _logger.LogInformation(
            "Handled {RequestName} with response {@Response}",
            requestName,
            response);

        return response;
    }
}
```

---

## PerformanceBehavior

Monitora requests lentos.

```csharp
using MediatR;
using Microsoft.Extensions.Logging;
using System.Diagnostics;

namespace Application.Common.Behaviors;

public class PerformanceBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<PerformanceBehavior<TRequest, TResponse>> _logger;
    private readonly Stopwatch _timer;

    public PerformanceBehavior(ILogger<PerformanceBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
        _timer = new Stopwatch();
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        _timer.Start();

        var response = await next();

        _timer.Stop();

        var elapsedMilliseconds = _timer.ElapsedMilliseconds;

        if (elapsedMilliseconds > 500) // Threshold: 500ms
        {
            var requestName = typeof(TRequest).Name;

            _logger.LogWarning(
                "Long Running Request: {RequestName} ({ElapsedMilliseconds}ms) {@Request}",
                requestName,
                elapsedMilliseconds,
                request);
        }

        return response;
    }
}
```

---

## UnhandledExceptionBehavior

Captura exceções não tratadas para logging.

```csharp
using MediatR;
using Microsoft.Extensions.Logging;

namespace Application.Common.Behaviors;

public class UnhandledExceptionBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<UnhandledExceptionBehavior<TRequest, TResponse>> _logger;

    public UnhandledExceptionBehavior(
        ILogger<UnhandledExceptionBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        try
        {
            return await next();
        }
        catch (Exception ex)
        {
            var requestName = typeof(TRequest).Name;

            _logger.LogError(
                ex,
                "Unhandled Exception for Request {RequestName} {@Request}",
                requestName,
                request);

            throw;
        }
    }
}
```

---

## TransactionBehavior

Envolve Commands em transações (apenas para Commands, não Queries).

```csharp
using Application.Common.Interfaces;
using MediatR;

namespace Application.Common.Behaviors;

public class TransactionBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IUnitOfWork _unitOfWork;

    public TransactionBehavior(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        // Apenas para Commands (que terminam com "Command")
        var requestName = typeof(TRequest).Name;
        if (!requestName.EndsWith("Command"))
            return await next();

        await using var transaction = await _unitOfWork.BeginTransactionAsync(ct);

        try
        {
            var response = await next();
            await transaction.CommitAsync(ct);
            return response;
        }
        catch
        {
            await transaction.RollbackAsync(ct);
            throw;
        }
    }
}
```

---

## Registro dos Behaviors

### Ordem de Execução

A ordem de registro define a ordem de execução:

```csharp
// Application/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        // MediatR
        services.AddMediatR(cfg => 
            cfg.RegisterServicesFromAssembly(typeof(DependencyInjection).Assembly));

        // FluentValidation
        services.AddValidatorsFromAssembly(typeof(DependencyInjection).Assembly);

        // Pipeline Behaviors (ordem importa!)
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(UnhandledExceptionBehavior<,>));
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(PerformanceBehavior<,>));
        // services.AddTransient(typeof(IPipelineBehavior<,>), typeof(TransactionBehavior<,>));

        // AutoMapper
        services.AddAutoMapper(typeof(DependencyInjection).Assembly);

        return services;
    }
}
```

### Pipeline de Execução

```
Request
    │
    ▼
┌─────────────────────────────┐
│ UnhandledExceptionBehavior  │  ← Captura exceções
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│     LoggingBehavior         │  ← Log de entrada
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│    ValidationBehavior       │  ← FluentValidation
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│   PerformanceBehavior       │  ← Mede tempo
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│         Handler             │  ← Lógica de negócio
└─────────────┬───────────────┘
              ▼
         Response
```

---

## Interfaces Necessárias

```csharp
// Application/Common/Interfaces/IUnitOfWork.cs
namespace Application.Common.Interfaces;

public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken ct = default);
    Task<IDbContextTransaction> BeginTransactionAsync(CancellationToken ct = default);
}

// Application/Common/Interfaces/ICurrentUserService.cs
namespace Application.Common.Interfaces;

public interface ICurrentUserService
{
    Guid? UserId { get; }
    string? UserName { get; }
    bool IsAuthenticated { get; }
    IEnumerable<string> Roles { get; }
    bool IsInRole(string role);
}
```
