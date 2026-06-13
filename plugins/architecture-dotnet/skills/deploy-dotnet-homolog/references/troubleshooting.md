# Troubleshooting

## Problemas por Etapa

---

## Etapa 1: Restore

### Erro: Package not found

```
error NU1101: Unable to find package 'SomePackage' version '1.0.0'
```

**Causas**:
1. Pacote não existe no NuGet.org
2. Pacote privado sem configuração de source
3. Versão específica não existe

**Soluções**:

```bash
# Verificar sources configuradas
dotnet nuget list source

# Adicionar source privada
dotnet nuget add source "https://pkgs.dev.azure.com/org/_packaging/feed/nuget/v3/index.json" \
    --name "PrivateFeed" \
    --username "user" \
    --password "PAT"

# Limpar cache e tentar novamente
dotnet nuget locals all --clear
dotnet restore
```

### Erro: Authentication failed

```
error NU1301: Unable to load the service index for source https://...
Response status code does not indicate success: 401 (Unauthorized)
```

**Soluções**:

```bash
# Verificar credenciais
cat ~/.nuget/NuGet/NuGet.Config

# Atualizar credenciais
dotnet nuget update source "PrivateFeed" --username "user" --password "NEW_PAT"
```

---

## Etapa 2: Build

### Erro: Compilation error

```
error CS0246: The type or namespace name 'ILogger' could not be found
```

**Soluções**:

```bash
# Verificar se restore foi executado
dotnet restore

# Verificar referências no .csproj
cat src/MyApp/MyApp.csproj | grep PackageReference

# Limpar e rebuildar
dotnet clean
dotnet build
```

### Erro: SDK not found

```
error MSB4236: The SDK 'Microsoft.NET.Sdk.Web' specified could not be found.
```

**Soluções**:

```bash
# Verificar SDKs instalados
dotnet --list-sdks

# Verificar global.json
cat global.json

# Instalar SDK correto
# Download: https://dotnet.microsoft.com/download
```

### Warning: Nullable reference types

```
warning CS8618: Non-nullable property 'Name' must contain a non-null value
```

**Soluções**:

```csharp
// Opção 1: Inicializar propriedade
public string Name { get; set; } = string.Empty;

// Opção 2: Tornar nullable
public string? Name { get; set; }

// Opção 3: Desabilitar no projeto (não recomendado)
<Nullable>disable</Nullable>
```

---

## Etapa 3: Test

### Erro: Test discovery failed

```
No test matches the given testcase filter
```

**Soluções**:

```bash
# Listar todos os testes disponíveis
dotnet test --list-tests

# Verificar se projetos de teste estão na solution
dotnet sln list

# Verificar referência do test framework
cat tests/MyApp.Tests/MyApp.Tests.csproj | grep -i xunit
```

### Erro: Database connection in tests

```
Npgsql.NpgsqlException: Failed to connect to 127.0.0.1:5432
```

**Soluções**:

```bash
# Verificar se está usando TestContainers ou banco real
# Se TestContainers, verificar Docker

# Verificar Docker rodando
docker info

# Verificar se teste usa InMemory para CI
# tests/MyApp.Tests/CustomWebApplicationFactory.cs
```

### Erro: Flaky tests

```
Test 'SomeTest' failed on attempt 1, passed on attempt 2
```

**Soluções**:

1. Identificar testes com dependência de ordem
2. Verificar uso de dados compartilhados
3. Adicionar retry policy para CI:

```bash
# Usar retry
dotnet test --blame-hang-timeout 60s
```

---

## Etapa 4: Docker Build

### Erro: Dockerfile not found

```
unable to prepare context: unable to evaluate symlinks: lstat Dockerfile: no such file
```

**Soluções**:

```bash
# Verificar nome do arquivo
ls -la Dockerfile*

# Se nome diferente, especificar
docker build -f docker/Dockerfile.homolog -t myapp:homolog .
```

### Erro: COPY failed

```
COPY failed: file not found in build context
```

**Soluções**:

```bash
# Verificar .dockerignore
cat .dockerignore

# Verificar se arquivo existe
ls -la src/MyApp/

# Verificar contexto de build
# O caminho é relativo ao contexto, não ao Dockerfile
```

### Erro: Out of disk space

```
no space left on device
```

**Soluções**:

```bash
# Limpar imagens não utilizadas
docker system prune -a

# Limpar volumes
docker volume prune

# Verificar espaço
df -h
```

### Erro: Build muito lento

**Soluções**:

```dockerfile
# Usar multi-stage build
# Aproveitar cache de layers

# Copiar apenas arquivos necessários para restore primeiro
COPY ["src/MyApp/MyApp.csproj", "src/MyApp/"]
RUN dotnet restore "src/MyApp/MyApp.csproj"

# Depois copiar o resto
COPY . .
RUN dotnet publish -c Release -o /app/publish
```

---

## Etapa 5: Deploy (Docker Compose)

### Erro: Port already in use

```
Error: bind: address already in use
```

**Soluções**:

```bash
# Identificar processo usando a porta
lsof -i :8080
# ou
netstat -tlnp | grep 8080

# Matar processo
kill -9 <PID>

# Ou parar containers anteriores
docker compose down
docker ps -a | grep myapp | awk '{print $1}' | xargs docker rm -f
```

### Erro: Network conflict

```
network myapp_default: network with name myapp_default already exists
```

**Soluções**:

```bash
# Remover network
docker network rm myapp_default

# Ou forçar recreate
docker compose up -d --force-recreate
```

### Erro: Container exits immediately

```
Container myapp-api-1 exited with code 1
```

**Soluções**:

```bash
# Verificar logs
docker compose logs api

# Verificar variáveis de ambiente
docker compose config

# Rodar interativamente para debug
docker compose run --rm api /bin/sh
```

### Erro: Database not ready

```
Connection refused to localhost:5432
```

**Soluções**:

```yaml
# docker-compose.yml - Usar depends_on com condition
services:
  api:
    depends_on:
      db:
        condition: service_healthy
  
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 10
```

---

## Etapa 6: Health Check

### Erro: Connection refused

```
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

**Diagnóstico**:

```bash
# Verificar se container está rodando
docker compose ps

# Verificar se aplicação iniciou
docker compose logs api --tail=50

# Verificar porta dentro do container
docker compose exec api ss -tlnp
```

### Erro: Timeout

```
curl: (28) Operation timed out after 30000 milliseconds
```

**Diagnóstico**:

```bash
# Verificar uso de CPU/memória
docker stats --no-stream

# Verificar se aplicação está travada
docker compose exec api ps aux

# Verificar logs de erro
docker compose logs api | grep -i error
```

### Erro: 503 Service Unavailable

```
{"status":"Unhealthy","entries":{"database":{"status":"Unhealthy"}}}
```

**Diagnóstico**:

```bash
# Verificar conexão com banco
docker compose exec api ping db

# Verificar se banco está rodando
docker compose logs db

# Testar conexão direta
docker compose exec db psql -U postgres -c "SELECT 1"
```

---

## Comandos Úteis de Debug

### Logs

```bash
# Logs de todos os serviços
docker compose logs

# Logs de um serviço específico
docker compose logs api

# Seguir logs em tempo real
docker compose logs -f api

# Últimas N linhas
docker compose logs --tail=100 api
```

### Inspeção

```bash
# Status dos containers
docker compose ps -a

# Uso de recursos
docker stats

# Inspecionar container
docker inspect myapp-api-1

# Variáveis de ambiente
docker compose exec api env
```

### Acesso ao Container

```bash
# Shell interativo
docker compose exec api /bin/sh

# Executar comando
docker compose exec api dotnet --info

# Verificar processos
docker compose exec api ps aux
```

### Cleanup

```bash
# Parar tudo
docker compose down

# Parar e remover volumes
docker compose down -v

# Remover imagens também
docker compose down --rmi all

# Limpar tudo (cuidado!)
docker system prune -a --volumes
```

---

## Checklist de Diagnóstico

Quando o deploy falhar, seguir este checklist:

```
[ ] 1. Verificar em qual etapa falhou
[ ] 2. Ler mensagem de erro completa
[ ] 3. Verificar logs relevantes
[ ] 4. Verificar se funciona localmente
[ ] 5. Verificar diferenças de ambiente
[ ] 6. Verificar recursos (disco, memória, CPU)
[ ] 7. Verificar conectividade de rede
[ ] 8. Verificar credenciais/secrets
[ ] 9. Tentar reproduzir isoladamente
[ ] 10. Consultar documentação/equipe
```
