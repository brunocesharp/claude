# Pipeline Steps - Produção

## Visão Geral

Pipeline de deploy para **PRODUÇÃO** com validações extras de segurança.

**REGRA FUNDAMENTAL**: Se qualquer etapa falhar, **PARAR IMEDIATAMENTE**.

---

## Etapa 1: Restore

### Comando

```bash
dotnet restore
```

### Validações Extras (Produção)

```bash
# Verificar se há vulnerabilidades conhecidas
dotnet list package --vulnerable

# Se houver vulnerabilidades HIGH ou CRITICAL, PARAR
if dotnet list package --vulnerable 2>&1 | grep -E "(High|Critical)"; then
    echo "❌ ERRO: Pacotes com vulnerabilidades críticas encontrados"
    echo "   Atualize os pacotes antes de fazer deploy em produção"
    exit 1
fi
```

### Critério de Sucesso
- Exit code: `0`
- Sem vulnerabilidades HIGH ou CRITICAL

---

## Etapa 2: Build

### Comando

```bash
dotnet build --no-restore --configuration Release
```

### Validações Extras (Produção)

```bash
# Build com tratamento de warnings como erros (opcional mas recomendado)
dotnet build --no-restore --configuration Release /p:TreatWarningsAsErrors=true

# Verificar se há TODOs ou FIXMEs no código (opcional)
if grep -r "TODO\|FIXME\|HACK" src/ --include="*.cs" | grep -v "obj/" | head -5; then
    echo "⚠️  AVISO: TODOs/FIXMEs encontrados no código"
fi
```

### Critério de Sucesso
- Exit code: `0`
- `0 Error(s)`
- Idealmente `0 Warning(s)`

---

## Etapa 3: Test

### Comando

```bash
dotnet test --no-build --configuration Release --logger "trx;LogFileName=test-results.trx"
```

### Validações Extras (Produção)

```bash
# Executar com cobertura de código
dotnet test --no-build --configuration Release \
    --collect:"XPlat Code Coverage" \
    --results-directory ./coverage

# Verificar cobertura mínima (se configurado)
# Exemplo usando reportgenerator
# reportgenerator -reports:./coverage/**/coverage.cobertura.xml -targetdir:./coverage/report

# Verificar se TODOS os testes passaram (zero skipped em produção)
TEST_RESULT=$(dotnet test --no-build --configuration Release --verbosity minimal 2>&1)

if echo "$TEST_RESULT" | grep -q "Failed:.*[1-9]"; then
    echo "❌ ERRO: Testes falhando - Deploy em produção NÃO PERMITIDO"
    exit 1
fi

if echo "$TEST_RESULT" | grep -q "Skipped:.*[1-9]"; then
    echo "⚠️  AVISO: Existem testes sendo ignorados"
    read -p "Deseja continuar mesmo assim? (s/n): " CONTINUE
    if [[ "$CONTINUE" != "s" ]]; then
        exit 1
    fi
fi
```

### Critério de Sucesso
- Exit code: `0`
- `Failed: 0`
- Idealmente `Skipped: 0`

---

## Etapa 4: Docker Build

### Comando

```bash
# Variáveis
APP_NAME="myapp"
VERSION=$(grep -oPm1 "(?<=<Version>)[^<]+" src/*/*.csproj 2>/dev/null | head -1 || echo "1.0.0")
TIMESTAMP=$(date +%Y%m%d%H%M%S)
IMAGE_TAG="prod-${VERSION}-${TIMESTAMP}"

# Build com tags múltiplas
docker build \
    --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
    --build-arg VERSION=${VERSION} \
    --build-arg VCS_REF=$(git rev-parse --short HEAD) \
    -t ${APP_NAME}:${IMAGE_TAG} \
    -t ${APP_NAME}:prod-latest \
    -t ${APP_NAME}:${VERSION} \
    .
```

### Validações Extras (Produção)

```bash
# Scan de vulnerabilidades na imagem (usando Trivy)
if command -v trivy &> /dev/null; then
    echo "Executando scan de segurança na imagem..."
    trivy image --severity HIGH,CRITICAL ${APP_NAME}:${IMAGE_TAG}
    
    # Se houver vulnerabilidades críticas, avisar
    CRITICAL_COUNT=$(trivy image --severity CRITICAL --quiet ${APP_NAME}:${IMAGE_TAG} | wc -l)
    if [[ $CRITICAL_COUNT -gt 0 ]]; then
        echo "⚠️  AVISO: Vulnerabilidades CRÍTICAS encontradas na imagem"
        read -p "Deseja continuar mesmo assim? (s/n): " CONTINUE
        if [[ "$CONTINUE" != "s" ]]; then
            exit 1
        fi
    fi
fi

# Verificar tamanho da imagem
IMAGE_SIZE=$(docker image inspect ${APP_NAME}:${IMAGE_TAG} --format='{{.Size}}')
IMAGE_SIZE_MB=$((IMAGE_SIZE / 1024 / 1024))
echo "Tamanho da imagem: ${IMAGE_SIZE_MB}MB"

if [[ $IMAGE_SIZE_MB -gt 500 ]]; then
    echo "⚠️  AVISO: Imagem muito grande (${IMAGE_SIZE_MB}MB)"
fi
```

### Critério de Sucesso
- Exit code: `0`
- Sem vulnerabilidades CRITICAL (ou aceitas explicitamente)
- Imagem criada com todas as tags

---

## Etapa 5: Deploy

### Comando

```bash
# Salvar versão anterior para rollback
PREVIOUS_IMAGE=$(docker compose -f docker-compose.prod.yml images -q api 2>/dev/null || echo "none")
echo "Versão anterior: $PREVIOUS_IMAGE" >> deploy-history.log

# Deploy com zero-downtime (se possível)
docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
```

### Validações Extras (Produção)

```bash
# Aguardar containers ficarem healthy
echo "Aguardando containers ficarem healthy..."

MAX_WAIT=120  # 2 minutos
WAIT_INTERVAL=5
ELAPSED=0

while [[ $ELAPSED -lt $MAX_WAIT ]]; do
    UNHEALTHY=$(docker compose -f docker-compose.prod.yml ps | grep -c "unhealthy" || true)
    STARTING=$(docker compose -f docker-compose.prod.yml ps | grep -c "starting" || true)
    
    if [[ $UNHEALTHY -eq 0 && $STARTING -eq 0 ]]; then
        echo "✅ Todos os containers healthy"
        break
    fi
    
    echo "  Aguardando... ($ELAPSED/${MAX_WAIT}s)"
    sleep $WAIT_INTERVAL
    ELAPSED=$((ELAPSED + WAIT_INTERVAL))
done

if [[ $ELAPSED -ge $MAX_WAIT ]]; then
    echo "❌ ERRO: Timeout aguardando containers ficarem healthy"
    docker compose -f docker-compose.prod.yml ps
    exit 1
fi
```

### Critério de Sucesso
- Exit code: `0`
- Todos os containers em estado `running` e `healthy`

---

## Etapa 6: Health Check

### Comando

```bash
#!/bin/bash

HEALTH_URL="${HEALTH_URL:-http://localhost:8080/health}"
MAX_RETRIES=10
RETRY_INTERVAL=6
TIMEOUT=15

echo "Health Check - Produção"
echo "  URL: $HEALTH_URL"
echo "  Tentativas: $MAX_RETRIES"
echo "  Intervalo: ${RETRY_INTERVAL}s"
echo ""

for i in $(seq 1 $MAX_RETRIES); do
    echo "Tentativa $i/$MAX_RETRIES..."
    
    RESPONSE=$(curl -s -w "\n%{http_code}" \
        --max-time $TIMEOUT \
        --connect-timeout 5 \
        $HEALTH_URL 2>/dev/null)
    
    HTTP_STATUS=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    echo "  Status: $HTTP_STATUS"
    
    # Em PRODUÇÃO, verificar se status é exatamente "Healthy"
    if [[ "$HTTP_STATUS" == "200" ]]; then
        HEALTH_STATUS=$(echo "$BODY" | jq -r '.status' 2>/dev/null)
        
        if [[ "$HEALTH_STATUS" == "Healthy" ]]; then
            echo ""
            echo "✅ Health check PASSED - Status: Healthy"
            echo ""
            echo "Detalhes:"
            echo "$BODY" | jq .
            exit 0
        elif [[ "$HEALTH_STATUS" == "Degraded" ]]; then
            echo "⚠️  Status: Degraded"
            echo "$BODY" | jq '.entries | to_entries[] | select(.value.status != "Healthy")' 2>/dev/null
            
            # Em produção, Degraded pode ser aceitável dependendo da política
            read -p "Aplicação em estado Degraded. Continuar? (s/n): " CONTINUE
            if [[ "$CONTINUE" == "s" ]]; then
                echo "✅ Health check PASSED (Degraded aceito)"
                exit 0
            fi
        fi
    fi
    
    if [[ $i -lt $MAX_RETRIES ]]; then
        echo "  Aguardando ${RETRY_INTERVAL}s..."
        sleep $RETRY_INTERVAL
    fi
done

echo ""
echo "❌ Health check FAILED após $MAX_RETRIES tentativas"
echo ""
echo "AÇÃO NECESSÁRIA: Verificar logs e considerar ROLLBACK"
echo ""

# Mostrar logs para diagnóstico
echo "Últimas 30 linhas de log:"
docker compose -f docker-compose.prod.yml logs --tail=30 api

exit 1
```

### Critério de Sucesso
- HTTP Status: `200`
- Body.status: `Healthy`
- Todos os entries: `Healthy`

---

## Script Completo de Deploy

```bash
#!/bin/bash
set -e

echo "══════════════════════════════════════════════════════════════"
echo "           DEPLOY PRODUÇÃO - INICIANDO"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "  ⚠️   AMBIENTE: PRODUÇÃO"
echo "  ⚠️   Esta ação afetará USUÁRIOS REAIS"
echo ""
echo "══════════════════════════════════════════════════════════════"

# Variáveis
APP_NAME="${APP_NAME:-myapp}"
VERSION=$(grep -oPm1 "(?<=<Version>)[^<]+" src/*/*.csproj 2>/dev/null | head -1 || echo "1.0.0")
TIMESTAMP=$(date +%Y%m%d%H%M%S)
IMAGE_TAG="prod-${VERSION}-${TIMESTAMP}"
HEALTH_URL="${HEALTH_URL:-http://localhost:8080/health}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

# Status tracking
declare -A STATUS
STATUS[validation]="NÃO EXECUTADO"
STATUS[restore]="NÃO EXECUTADO"
STATUS[build]="NÃO EXECUTADO"
STATUS[test]="NÃO EXECUTADO"
STATUS[docker_build]="NÃO EXECUTADO"
STATUS[deploy]="NÃO EXECUTADO"
STATUS[health_check]="NÃO EXECUTADO"

# Salvar versão anterior
PREVIOUS_TAG=$(docker images ${APP_NAME}:prod-latest --format "{{.ID}}" 2>/dev/null || echo "none")

print_summary() {
    echo ""
    echo "══════════════════════════════════════════════════════════════"
    echo "           RESUMO DO DEPLOY"
    echo "══════════════════════════════════════════════════════════════"
    echo "- Validação prévia: ${STATUS[validation]}"
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
        echo "- Ambiente: PRODUÇÃO"
        echo "- Estratégia: docker compose"
        echo "- URL: ${HEALTH_URL%/health}"
        echo ""
        echo "Versão anterior (para rollback):"
        echo "- Image ID: ${PREVIOUS_TAG}"
    fi
    echo "══════════════════════════════════════════════════════════════"
}

handle_error() {
    echo ""
    echo "❌ Deploy em PRODUÇÃO falhou na etapa: $1"
    print_summary "failure"
    echo ""
    echo "⚠️  AÇÃO NECESSÁRIA:"
    echo "   1. NÃO tente deploy novamente sem corrigir o erro"
    echo "   2. Verifique os logs acima para detalhes"
    echo "   3. Se necessário, execute rollback manual"
    exit 1
}

# Confirmação
echo ""
read -p "Digite CONFIRMAR para prosseguir com o deploy em PRODUÇÃO: " CONFIRM
if [[ "$CONFIRM" != "CONFIRMAR" ]]; then
    echo "Deploy cancelado pelo usuário"
    exit 0
fi

# Etapa 0: Validação Prévia
echo ""
echo "[0/6] Executando validação prévia..."
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" != "main" && "$BRANCH" != "master" ]]; then
    STATUS[validation]="FALHOU"
    handle_error "Validação (branch: $BRANCH)"
fi
if [[ -n $(git status --porcelain) ]]; then
    STATUS[validation]="FALHOU"
    handle_error "Validação (commits pendentes)"
fi
STATUS[validation]="OK"
echo "✓ Validação prévia concluída"

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
if docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:prod-latest .; then
    STATUS[docker_build]="OK"
    echo "✓ Docker build concluído"
else
    STATUS[docker_build]="FALHOU"
    handle_error "Docker Build"
fi

# Etapa 5: Deploy
echo ""
echo "[5/6] Executando deploy..."
if docker compose -f ${COMPOSE_FILE} up -d --build; then
    STATUS[deploy]="OK"
    echo "✓ Deploy concluído"
else
    STATUS[deploy]="FALHOU"
    handle_error "Deploy"
fi

# Etapa 6: Health Check
echo ""
echo "[6/6] Verificando health check..."
MAX_RETRIES=10
RETRY_INTERVAL=6

for i in $(seq 1 $MAX_RETRIES); do
    echo "  Tentativa $i/$MAX_RETRIES..."
    
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 $HEALTH_URL 2>/dev/null || echo "000")
    
    if [[ "$HTTP_STATUS" == "200" ]]; then
        HEALTH_BODY=$(curl -s --max-time 15 $HEALTH_URL 2>/dev/null)
        HEALTH_STATUS=$(echo "$HEALTH_BODY" | jq -r '.status' 2>/dev/null)
        
        if [[ "$HEALTH_STATUS" == "Healthy" ]]; then
            STATUS[health_check]="OK"
            echo "✓ Health check passou (Healthy)"
            break
        fi
    fi
    
    if [[ $i -eq $MAX_RETRIES ]]; then
        STATUS[health_check]="FALHOU"
        handle_error "Health Check"
    fi
    
    sleep $RETRY_INTERVAL
done

# Sucesso!
echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  ✅ DEPLOY EM PRODUÇÃO CONCLUÍDO COM SUCESSO!"
echo "══════════════════════════════════════════════════════════════"
print_summary "success"

# Criar tag git
git tag -a "v${VERSION}-${TIMESTAMP}" -m "Deploy produção ${VERSION}" 2>/dev/null || true
echo ""
echo "Tag git criada: v${VERSION}-${TIMESTAMP}"
```
