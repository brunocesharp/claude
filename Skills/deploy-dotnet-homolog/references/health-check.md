# Health Check

## Visão Geral

O health check é a última etapa do deploy e valida se a aplicação está funcionando corretamente.

---

## Endpoints de Health Check

### Estrutura Recomendada

| Endpoint | Propósito | Quando Usar |
|----------|-----------|-------------|
| `/health` | Check completo | Validação pós-deploy |
| `/health/live` | Liveness probe | Kubernetes liveness |
| `/health/ready` | Readiness probe | Kubernetes readiness |

---

## Validação Pós-Deploy

### Script de Validação

```bash
#!/bin/bash

HEALTH_URL="${HEALTH_URL:-http://localhost:8080/health}"
MAX_RETRIES="${MAX_RETRIES:-5}"
RETRY_INTERVAL="${RETRY_INTERVAL:-5}"
TIMEOUT="${TIMEOUT:-10}"

echo "Health Check Configuration:"
echo "  URL: $HEALTH_URL"
echo "  Max Retries: $MAX_RETRIES"
echo "  Retry Interval: ${RETRY_INTERVAL}s"
echo "  Timeout: ${TIMEOUT}s"
echo ""

for i in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $i/$MAX_RETRIES..."
    
    # Fazer request com timeout
    RESPONSE=$(curl -s -w "\n%{http_code}" \
        --max-time $TIMEOUT \
        --connect-timeout 5 \
        $HEALTH_URL 2>/dev/null)
    
    # Extrair status code (última linha)
    HTTP_STATUS=$(echo "$RESPONSE" | tail -n 1)
    
    # Extrair body (tudo exceto última linha)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    echo "  Status: $HTTP_STATUS"
    
    # Verificar sucesso
    if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "204" ]; then
        echo ""
        echo "✅ Health check PASSED"
        echo ""
        
        # Mostrar detalhes se houver body
        if [ -n "$BODY" ]; then
            echo "Response:"
            echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
        fi
        
        exit 0
    fi
    
    # Se não for a última tentativa, aguardar
    if [ $i -lt $MAX_RETRIES ]; then
        echo "  Retrying in ${RETRY_INTERVAL}s..."
        sleep $RETRY_INTERVAL
    fi
done

echo ""
echo "❌ Health check FAILED after $MAX_RETRIES attempts"
echo ""

# Tentar obter logs do container para diagnóstico
echo "Container logs (últimas 20 linhas):"
docker compose logs --tail=20 api 2>/dev/null || echo "Unable to fetch logs"

exit 1
```

---

## Interpretando Respostas

### Resposta Healthy (HTTP 200)

```json
{
  "status": "Healthy",
  "totalDuration": "00:00:00.0234567",
  "entries": {
    "database": {
      "status": "Healthy",
      "duration": "00:00:00.0123456",
      "tags": ["ready"]
    },
    "redis": {
      "status": "Healthy",
      "duration": "00:00:00.0012345",
      "tags": ["ready"]
    }
  }
}
```

**Ação**: Deploy bem-sucedido ✅

### Resposta Degraded (HTTP 200)

```json
{
  "status": "Degraded",
  "totalDuration": "00:00:00.5234567",
  "entries": {
    "database": {
      "status": "Healthy",
      "duration": "00:00:00.0123456"
    },
    "external-api": {
      "status": "Degraded",
      "duration": "00:00:00.5012345",
      "description": "Response time above threshold"
    }
  }
}
```

**Ação**: Deploy bem-sucedido com aviso ⚠️
- Aplicação funcional mas com performance degradada
- Monitorar e investigar causa

### Resposta Unhealthy (HTTP 503)

```json
{
  "status": "Unhealthy",
  "totalDuration": "00:00:05.0234567",
  "entries": {
    "database": {
      "status": "Unhealthy",
      "duration": "00:00:05.0123456",
      "description": "Connection refused",
      "exception": "Npgsql.NpgsqlException: Failed to connect"
    }
  }
}
```

**Ação**: Deploy FALHOU ❌
- Verificar conexão com o banco de dados
- Verificar se o container do banco está rodando
- Verificar connection string

---

## Diagnóstico de Falhas

### Status 000 (Conexão recusada)

```
Health check failed. Status: 000
```

**Causas possíveis**:
1. Container não iniciou
2. Aplicação crashou durante startup
3. Porta incorreta

**Comandos de diagnóstico**:

```bash
# Verificar se container está rodando
docker compose ps

# Verificar logs do container
docker compose logs api --tail=50

# Verificar se porta está escutando
docker compose exec api netstat -tlnp
```

### Status 503 (Service Unavailable)

```
Health check failed. Status: 503
```

**Causas possíveis**:
1. Dependência não disponível (banco, cache)
2. Aplicação ainda inicializando
3. Erro de configuração

**Comandos de diagnóstico**:

```bash
# Ver detalhes do health check
curl -s http://localhost:8080/health | jq .

# Verificar logs de erro
docker compose logs api | grep -i error

# Verificar variáveis de ambiente
docker compose exec api env | grep -i connection
```

### Status 404 (Not Found)

```
Health check failed. Status: 404
```

**Causas possíveis**:
1. Endpoint de health não configurado
2. Rota incorreta
3. Middleware bloqueando

**Solução**:

```csharp
// Program.cs - Verificar se health checks estão configurados
app.MapHealthChecks("/health");
```

### Timeout

```
curl: (28) Operation timed out
```

**Causas possíveis**:
1. Health check muito lento
2. Deadlock na aplicação
3. Dependência travando

**Comandos de diagnóstico**:

```bash
# Verificar uso de recursos
docker stats --no-stream

# Verificar se aplicação responde em outras rotas
curl -s http://localhost:8080/

# Verificar threads/connections
docker compose exec api ss -tlnp
```

---

## Configuração de Health Check na Aplicação

### Configuração Básica (ASP.NET Core)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Adicionar health checks
builder.Services.AddHealthChecks()
    .AddNpgSql(
        builder.Configuration.GetConnectionString("DefaultConnection")!,
        name: "database",
        tags: new[] { "ready" })
    .AddRedis(
        builder.Configuration.GetConnectionString("Redis")!,
        name: "redis",
        tags: new[] { "ready" });

var app = builder.Build();

// Mapear endpoints
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // Não executa nenhum check
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

### Health Check no Docker Compose

```yaml
# docker-compose.yml
services:
  api:
    image: myapp:homolog-latest
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Staging
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## Validação Completa

### Script de Validação Avançada

```bash
#!/bin/bash

BASE_URL="${BASE_URL:-http://localhost:8080}"

echo "=== Validação Completa Pós-Deploy ==="
echo ""

# 1. Health Check Principal
echo "[1/4] Health Check Principal..."
HEALTH=$(curl -s -w "\n%{http_code}" ${BASE_URL}/health)
HEALTH_STATUS=$(echo "$HEALTH" | tail -n 1)
HEALTH_BODY=$(echo "$HEALTH" | sed '$d')

if [ "$HEALTH_STATUS" = "200" ]; then
    echo "  ✅ /health: OK"
    
    # Verificar status de cada componente
    echo "$HEALTH_BODY" | jq -r '.entries | to_entries[] | "  - \(.key): \(.value.status)"' 2>/dev/null
else
    echo "  ❌ /health: FAILED (HTTP $HEALTH_STATUS)"
fi

# 2. Liveness
echo ""
echo "[2/4] Liveness Probe..."
LIVE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/health/live)
if [ "$LIVE_STATUS" = "200" ] || [ "$LIVE_STATUS" = "204" ]; then
    echo "  ✅ /health/live: OK"
else
    echo "  ❌ /health/live: FAILED (HTTP $LIVE_STATUS)"
fi

# 3. Readiness
echo ""
echo "[3/4] Readiness Probe..."
READY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/health/ready)
if [ "$READY_STATUS" = "200" ]; then
    echo "  ✅ /health/ready: OK"
else
    echo "  ❌ /health/ready: FAILED (HTTP $READY_STATUS)"
fi

# 4. OpenAPI/Swagger
echo ""
echo "[4/4] OpenAPI Documentation..."
SWAGGER_STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/openapi/v1.json)
if [ "$SWAGGER_STATUS" = "200" ]; then
    echo "  ✅ /openapi/v1.json: OK"
else
    echo "  ⚠️  /openapi/v1.json: Not available (HTTP $SWAGGER_STATUS)"
fi

echo ""
echo "=== Validação Concluída ==="
```
