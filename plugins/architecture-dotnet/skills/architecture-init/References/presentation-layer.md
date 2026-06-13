# Presentation Layer

## Visão Geral

Gateway da aplicação. Recebe requisições HTTP, valida input básico, roteia para Application layer e formata responses.

## Estrutura

```
Presentation/
├── Controllers/
│   └── {Entity}Controller.cs
├── Endpoints/              # Minimal APIs (alternativa)
│   └── {Feature}Endpoints.cs
├── Middleware/
│   ├── ExceptionHandlingMiddleware.cs
│   └── RequestLoggingMiddleware.cs
├── Filters/
│   └── ApiExceptionFilterAttribute.cs
├── Models/
│   ├── Requests/
│   │   └── Create{Entity}Request.cs
│   └── Responses/
│       └── ApiResponse.cs
├── Extensions/
│   └── ServiceCollectionExtensions.cs
├── Program.cs
├── appsettings.json
└── appsettings.Development.json
```

## Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly ISender _mediator;
    
    public ProductsController(ISender mediator)
    {
        _mediator = mediator;
    }
    
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<ProductDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll(CancellationToken ct)
    {
        var result = await _mediator.Send(new GetProductListQuery(), ct);
        return Ok(result);
    }
    
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(Guid id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetProductByIdQuery(id), ct);
        return result is null ? NotFound() : Ok(result);
    }
    
    [HttpPost]
    [ProducesResponseType(typeof(Guid), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(
        [FromBody] CreateProductRequest request, 
        CancellationToken ct)
    {
        var command = new CreateProductCommand(
            request.Name,
            request.Description,
            request.Price);
            
        var id = await _mediator.Send(command, ct);
        
        return CreatedAtAction(nameof(GetById), new { id }, id);
    }
    
    [HttpPut("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(
        Guid id, 
        [FromBody] UpdateProductRequest request,
        CancellationToken ct)
    {
        var command = new UpdateProductCommand(id, request.Name, request.Price);
        await _mediator.Send(command, ct);
        return NoContent();
    }
    
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    public async Task<IActionResult> Delete(Guid id, CancellationToken ct)
    {
        await _mediator.Send(new DeleteProductCommand(id), ct);
        return NoContent();
    }
}
```

## Minimal API Endpoints (Alternativa)

```csharp
public static class ProductEndpoints
{
    public static void MapProductEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/products")
            .WithTags("Products");
        
        group.MapGet("/", GetAll);
        group.MapGet("/{id:guid}", GetById);
        group.MapPost("/", Create);
        group.MapPut("/{id:guid}", Update);
        group.MapDelete("/{id:guid}", Delete);
    }
    
    private static async Task<IResult> GetAll(
        ISender mediator, 
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetProductListQuery(), ct);
        return Results.Ok(result);
    }
    
    private static async Task<IResult> GetById(
        Guid id, 
        ISender mediator, 
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetProductByIdQuery(id), ct);
        return result is null ? Results.NotFound() : Results.Ok(result);
    }
    
    private static async Task<IResult> Create(
        CreateProductRequest request,
        ISender mediator,
        CancellationToken ct)
    {
        var command = new CreateProductCommand(
            request.Name, request.Description, request.Price);
        var id = await mediator.Send(command, ct);
        return Results.Created($"/api/products/{id}", id);
    }
}
```

## Exception Handling Middleware

```csharp
public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;
    
    public ExceptionHandlingMiddleware(
        RequestDelegate next,
        ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }
    
    private async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        var (statusCode, title) = exception switch
        {
            ValidationException => (StatusCodes.Status400BadRequest, "Validation Error"),
            EntityNotFoundException => (StatusCodes.Status404NotFound, "Not Found"),
            UnauthorizedAccessException => (StatusCodes.Status401Unauthorized, "Unauthorized"),
            _ => (StatusCodes.Status500InternalServerError, "Server Error")
        };
        
        _logger.LogError(exception, "Exception: {Message}", exception.Message);
        
        var problemDetails = new ProblemDetails
        {
            Status = statusCode,
            Title = title,
            Detail = exception.Message,
            Instance = context.Request.Path
        };
        
        context.Response.StatusCode = statusCode;
        context.Response.ContentType = "application/problem+json";
        
        await context.Response.WriteAsJsonAsync(problemDetails);
    }
}
```

## Request Model

```csharp
public record CreateProductRequest(
    string Name,
    string Description,
    decimal Price);

public record UpdateProductRequest(
    string Name,
    decimal Price);
```

## API Response Wrapper (Opcional)

```csharp
public class ApiResponse<T>
{
    public bool Success { get; init; }
    public T? Data { get; init; }
    public string? Message { get; init; }
    public IEnumerable<string>? Errors { get; init; }
    
    public static ApiResponse<T> Ok(T data, string? message = null) =>
        new() { Success = true, Data = data, Message = message };
        
    public static ApiResponse<T> Fail(string message, IEnumerable<string>? errors = null) =>
        new() { Success = false, Message = message, Errors = errors };
}
```

## Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add layers
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

// Add presentation services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// CORS, Auth, etc.
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseMiddleware<ExceptionHandlingMiddleware>();
app.UseHttpsRedirection();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
// ou app.MapProductEndpoints(); para Minimal APIs

app.Run();
```

## Regras

1. **Controllers são finos** - apenas roteamento
2. **Sem lógica de negócio** - delega para Application
3. **Request/Response models próprios** - não expõe DTOs diretamente
4. **Exception handling centralizado** - middleware ou filter
5. **Documentação via atributos** - ProducesResponseType
6. **Dependency Injection no Program.cs**
7. **Separação Controllers vs Minimal APIs** - escolher um padrão
