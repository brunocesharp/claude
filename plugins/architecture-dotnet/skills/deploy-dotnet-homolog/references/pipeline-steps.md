# Pipeline Steps

## Visão Geral

Cada etapa deve ser executada sequencialmente. Se qualquer etapa falhar, **PARAR IMEDIATAMENTE**.

---

## Etapa 1: Restore

### Comando

```bash
dotnet restore
```

### O que faz
- Baixa todos os pacotes NuGet referenciados
- Restaura dependências de todos os projetos da solution

### Critério de Sucesso
- Exit code: `0`
- Mensagem: `Restore completed`

### Exemplo de Sucesso

```
Determining projects to restore...
Restored /app/src/MyApp.Domain/MyApp.Domain.csproj
Restored /app/src/MyApp.Application/MyApp.Application.csproj
Restored /app/src/MyApp.Infrastructure/MyApp.Infrastructure.csproj
Restored /app/src/MyApp.Presentation/MyApp.Presentation.csproj
```

### Exemplo de Falha

```
error NU1101: Unable to find package SomePackage. No packages exist with this id in source(s): nuget.org
```

### Ação em Caso de Falha
- Verificar se o pacote existe no NuGet
- Verificar configuração de sources em `nuget.config`
- Verificar conexão com a internet

---

## Etapa 2: Build

### Comando

```bash
dotnet build --no-restore --configuration Release
```

### O que faz
- Compila todos os projetos em modo Release
- Não executa restore novamente (`--no-restore`)
- Gera binários otimizados para produção

### Critério de Sucesso
- Exit code: `0`
- Mensagem: `Build succeeded`
- `0 Warning(s)` (idealmente)
- `0 Error(s)`

### Exemplo de Sucesso

```
Microsoft (R) Build Engine version 17.x
Build started 1/1/2025 10:00:00 AM.

MyApp.Domain -> /app/src/MyApp.Domain/bin/Release/net8.0/MyApp.Domain.dll
MyApp.Application -> /app/src/MyApp.Application/bin/Release/net8.0/MyApp.Application.dll
MyApp.Infrastructure -> /app/src/MyApp.Infrastructure/bin/Release/net8.0/MyApp.Infrastructure.dll
MyApp.Presentation -> /app/src/MyApp.Presentation/bin/Release/net8.0/MyApp.Presentation.dll

Build succeeded.
    0 Warning(s)
    0 Error(s)

Time Elapsed 00:00:05.32
```

### Exemplo de Falha

```
error CS1002: ; expected
error CS0246: The type or namespace name 'SomeType' could not be found
```

### Ação em Caso de Falha
- Analisar erros de compilação
- Verificar se todas as referências estão corretas
- Verificar se o código compila localmente

---

## Etapa 3: Test

### Comando

```bash
dotnet test --no-build --configuration Release
```

### Opções adicionais úteis

```bash
# Com verbosidade mínima
dotnet test --no-build --configuration Release --verbosity minimal

# Com cobertura de código
dotnet test --no-build --configuration Release --collect:"XPlat Code Coverage"

# Com filtro de categoria
dotnet test --no-build --configuration Release --filter "Category!=Integration"
```

### O que faz
- Executa todos os testes unitários e de integração
- Usa os binários já compilados (`--no-build`)
- Executa em modo Release

### Critério de Sucesso
- Exit code: `0`
- Todos os testes passando
- `Failed: 0`

### Exemplo de Sucesso

```
Starting test execution, please wait...
A total of 1 test files matched the specified pattern.

Passed!  - Failed:     0, Passed:    42, Skipped:     0, Total:    42, Duration: 3 s
```

### Exemplo de Falha

```
Starting test execution, please wait...
A total of 1 test files matched the specified pattern.

  Failed CreateProduct_Should_ReturnSuccess_WhenValidData [45 ms]
  Error Message:
   Expected result.IsSuccess to be true, but found false.

Failed!  - Failed:     1, Passed:    41, Skipped:     0, Total:    42, Duration: 3 s
```

### Ação em Caso de Falha
- Analisar quais testes falharam
- Verificar se há dependências de ambiente (banco, APIs)
- Verificar se os testes passam localmente

---

## Etapa 4: Docker Build

### Comando

```bash
# Gerar tag com timestamp
IMAGE_TAG="homolog-$(date +%Y%m%d%H%M%S)"

# Build da imagem
docker build -t myapp:${IMAGE_TAG} -t myapp:homolog-latest .
```

### O que faz
- Constrói a imagem Docker conforme o Dockerfile
- Aplica duas tags: uma específica com timestamp e uma `latest`
- Copia os artefatos de build para a imagem

### Critério de Sucesso
- Exit code: `0`
- Mensagem: `Successfully built`
- Mensagem: `Successfully tagged`

### Exemplo de Sucesso

```
[+] Building 45.2s (15/15) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [build 1/5] FROM mcr.microsoft.com/dotnet/sdk:8.0
 => [build 2/5] WORKDIR /src
 => [build 3/5] COPY . .
 => [build 4/5] RUN dotnet restore
 => [build 5/5] RUN dotnet publish -c Release -o /app/publish
 => [final 1/2] FROM mcr.microsoft.com/dotnet/aspnet:8.0
 => [final 2/2] COPY --from=build /app/publish .
 => exporting to image
 => => naming to docker.io/library/myapp:homolog-20250110120000
 => => naming to docker.io/library/myapp:homolog-latest
```

### Exemplo de Falha

```
ERROR: failed to solve: process "/bin/sh -c dotnet restore" did not complete successfully: exit code: 1
```

### Ação em Caso de Falha
- Verificar sintaxe do Dockerfile
- Verificar se a imagem base está acessível
- Verificar se o build funciona localmente

---

## Etapa 5: Deploy (Docker Compose)

### Comando

```bash
# Se existir docker-compose.homolog.yml
docker compose -f docker-compose.homolog.yml up -d --build

# Ou usar o padrão
docker compose up -d --build
```

### O que faz
- Inicia os containers definidos no compose
- Reconstrói se necessário (`--build`)
- Executa em modo detached (`-d`)

### Critério de Sucesso
- Exit code: `0`
- Containers em estado `running`

### Verificar status após deploy

```bash
docker compose ps
```

### Exemplo de Sucesso

```
[+] Running 3/3
 ✔ Network myapp_default      Created
 ✔ Container myapp-db-1       Started
 ✔ Container myapp-api-1      Started
```

```bash
$ docker compose ps
NAME            IMAGE                    STATUS          PORTS
myapp-api-1     myapp:homolog-latest     Up 10 seconds   0.0.0.0:8080->8080/tcp
myapp-db-1      postgres:16              Up 12 seconds   0.0.0.0:5432->5432/tcp
```

### Exemplo de Falha

```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:8080 -> 0.0.0.0:0: listen tcp 0.0.0.0:8080: bind: address already in use
```

### Ação em Caso de Falha
- Verificar se a porta está em uso: `lsof -i :8080`
- Parar containers anteriores: `docker compose down`
- Verificar logs: `docker compose logs`

---

## Etapa 6: Health Check

### Comando

```bash
# Aguardar aplicação iniciar e verificar health
MAX_RETRIES=5
RETRY_INTERVAL=5
HEALTH_URL="http://localhost:8080/health"

for i in $(seq 1 $MAX_RETRIES); do
    echo "Health check attempt $i/$MAX_RETRIES..."
    
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)
    
    if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "204" ]; then
        echo "Health check passed! Status: $HTTP_STATUS"
        exit 0
    fi
    
    echo "Health check failed. Status: $HTTP_STATUS. Retrying in ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

echo "Health check failed after $MAX_RETRIES attempts"
exit 1
```

### O que faz
- Verifica se a aplicação está respondendo
- Tenta múltiplas vezes com intervalo
- Valida endpoint `/health`

### Critério de Sucesso
- HTTP Status: `200` ou `204`
- Response body indicando `Healthy` (opcional)

### Exemplo de Sucesso

```
Health check attempt 1/5...
Health check passed! Status: 200

Response:
{
  "status": "Healthy",
  "totalDuration": "00:00:00.0234567",
  "entries": {
    "database": { "status": "Healthy", "duration": "00:00:00.0123456" },
    "redis": { "status": "Healthy", "duration": "00:00:00.0012345" }
  }
}
```

### Exemplo de Falha

```
Health check attempt 1/5...
Health check failed. Status: 000. Retrying in 5s...
Health check attempt 2/5...
Health check failed. Status: 503. Retrying in 5s...
...
Health check failed after 5 attempts
```

### Ação em Caso de Falha
- Verificar logs do container: `docker compose logs api`
- Verificar se o container está rodando: `docker compose ps`
- Verificar conexões com dependências (DB, Redis)
- Verificar se a porta está correta

---

## Script Completo de Deploy

```bash
#!/bin/bash
set -e  # Parar em caso de erro

echo "=========================================="
echo "  Deploy Homologação - Iniciando"
echo "=========================================="

# Variáveis
APP_NAME="myapp"
IMAGE_TAG="homolog-$(date +%Y%m%d%H%M%S)"
HEALTH_URL="http://localhost:8080/health"
MAX_RETRIES=5
RETRY_INTERVAL=5

# Status tracking
declare -A STATUS
STATUS[restore]="NÃO EXECUTADO"
STATUS[build]="NÃO EXECUTADO"
STATUS[test]="NÃO EXECUTADO"
STATUS[docker_build]="NÃO EXECUTADO"
STATUS[deploy]="NÃO EXECUTADO"
STATUS[health_check]="NÃO EXECUTADO"

print_summary() {
    echo ""
    echo "=========================================="
    echo "  Resumo do Deploy"
    echo "=========================================="
    echo "- Restore: ${STATUS[restore]}"
    echo "- Build: ${STATUS[build]}"
    echo "- Testes: ${STATUS[test]}"
    echo "- Docker build: ${STATUS[docker_build]}"
    echo "- Deploy: ${STATUS[deploy]}"
    echo "- Health check: ${STATUS[health_check]}"
    echo ""
    
    if [ "$1" = "success" ]; then
        echo "Artefatos:"
        echo "- Imagem: ${APP_NAME}:${IMAGE_TAG}"
        echo "- Ambiente: HOMOLOGAÇÃO"
        echo "- Estratégia: docker compose"
        echo "- URL: ${HEALTH_URL%/health}"
    fi
}

handle_error() {
    echo ""
    echo "❌ Deploy falhou na etapa: $1"
    print_summary "failure"
    exit 1
}

# Etapa 1: Restore
echo ""
echo "[1/6] Executando restore..."
if dotnet restore; then
    STATUS[restore]="OK"
    echo "✓ Restore concluído"
else
    STATUS[restore]="FALHOU"
    handle_error "Restore"
fi

# Etapa 2: Build
echo ""
echo "[2/6] Executando build..."
if dotnet build --no-restore --configuration Release; then
    STATUS[build]="OK"
    echo "✓ Build concluído"
else
    STATUS[build]="FALHOU"
    handle_error "Build"
fi

# Etapa 3: Test
echo ""
echo "[3/6] Executando testes..."
if dotnet test --no-build --configuration Release; then
    STATUS[test]="OK"
    echo "✓ Testes concluídos"
else
    STATUS[test]="FALHOU"
    handle_error "Test"
fi

# Etapa 4: Docker Build
echo ""
echo "[4/6] Construindo imagem Docker..."
if docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:homolog-latest .; then
    STATUS[docker_build]="OK"
    echo "✓ Docker build concluído"
else
    STATUS[docker_build]="FALHOU"
    handle_error "Docker Build"
fi

# Etapa 5: Deploy
echo ""
echo "[5/6] Executando deploy..."
if docker compose up -d --build; then
    STATUS[deploy]="OK"
    echo "✓ Deploy concluído"
else
    STATUS[deploy]="FALHOU"
    handle_error "Deploy"
fi

# Etapa 6: Health Check
echo ""
echo "[6/6] Verificando health check..."
for i in $(seq 1 $MAX_RETRIES); do
    echo "  Tentativa $i/$MAX_RETRIES..."
    
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL 2>/dev/null || echo "000")
    
    if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "204" ]; then
        STATUS[health_check]="OK"
        echo "✓ Health check passou (HTTP $HTTP_STATUS)"
        break
    fi
    
    if [ $i -eq $MAX_RETRIES ]; then
        STATUS[health_check]="FALHOU"
        handle_error "Health Check"
    fi
    
    sleep $RETRY_INTERVAL
done

# Sucesso!
echo ""
echo "=========================================="
echo "  ✅ Deploy concluído com sucesso!"
echo "=========================================="
print_summary "success"
```
