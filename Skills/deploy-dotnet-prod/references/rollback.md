# Rollback - Produção

## ⚠️ PROCEDIMENTO DE EMERGÊNCIA

Este documento descreve como reverter um deploy em produção quando algo dá errado.

---

## Quando Fazer Rollback

### Indicadores Críticos (Rollback Imediato)

| Indicador | Ação |
|-----------|------|
| Health check retorna `Unhealthy` | Rollback imediato |
| Erros 5xx em massa | Rollback imediato |
| Aplicação não inicia | Rollback imediato |
| Perda de dados detectada | Rollback imediato + investigação |
| Timeout generalizado | Avaliar e rollback se persistir |

### Indicadores de Alerta (Avaliar)

| Indicador | Ação |
|-----------|------|
| Health check retorna `Degraded` | Monitorar por 5-10 min |
| Aumento de latência | Monitorar e avaliar |
| Alguns erros isolados | Investigar antes de rollback |

---

## Rollback Rápido (Docker Compose)

### Passo 1: Identificar Versão Anterior

```bash
# Verificar histórico de deploys
cat deploy-history.log | tail -5

# Ou listar imagens disponíveis
docker images myapp --format "{{.Tag}}\t{{.CreatedAt}}" | head -10

# Exemplo de saída:
# prod-1.0.0-20250110120000    2025-01-10 12:00:00
# prod-1.0.0-20250109100000    2025-01-09 10:00:00  <- versão anterior
# prod-0.9.0-20250108150000    2025-01-08 15:00:00
```

### Passo 2: Executar Rollback

```bash
#!/bin/bash

# Variáveis
APP_NAME="myapp"
COMPOSE_FILE="docker-compose.prod.yml"
PREVIOUS_TAG="${1:-prod-latest-previous}"  # Passar como argumento ou usar default

echo "══════════════════════════════════════════════════════════════"
echo "           ⚠️  ROLLBACK PRODUÇÃO - INICIANDO"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "  Versão atual será substituída por: ${PREVIOUS_TAG}"
echo ""

# Confirmar
read -p "Digite ROLLBACK para confirmar: " CONFIRM
if [[ "$CONFIRM" != "ROLLBACK" ]]; then
    echo "Rollback cancelado"
    exit 0
fi

echo ""
echo "[1/4] Parando containers atuais..."
docker compose -f ${COMPOSE_FILE} down

echo ""
echo "[2/4] Restaurando imagem anterior..."
docker tag ${APP_NAME}:${PREVIOUS_TAG} ${APP_NAME}:prod-latest

echo ""
echo "[3/4] Iniciando com versão anterior..."
docker compose -f ${COMPOSE_FILE} up -d

echo ""
echo "[4/4] Verificando health check..."
sleep 10

HEALTH_URL="http://localhost:8080/health"
MAX_RETRIES=5

for i in $(seq 1 $MAX_RETRIES); do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL 2>/dev/null || echo "000")
    
    if [[ "$HTTP_STATUS" == "200" ]]; then
        echo ""
        echo "✅ ROLLBACK CONCLUÍDO COM SUCESSO"
        echo ""
        echo "  Versão restaurada: ${PREVIOUS_TAG}"
        echo "  Status: Healthy"
        exit 0
    fi
    
    echo "  Tentativa $i/$MAX_RETRIES - Status: $HTTP_STATUS"
    sleep 5
done

echo ""
echo "❌ ROLLBACK FALHOU - Health check não passou"
echo ""
echo "AÇÃO MANUAL NECESSÁRIA!"
exit 1
```

### Passo 3: Verificar Rollback

```bash
# Verificar containers
docker compose -f docker-compose.prod.yml ps

# Verificar logs
docker compose -f docker-compose.prod.yml logs --tail=50 api

# Verificar health
curl -s http://localhost:8080/health | jq .

# Verificar versão da imagem rodando
docker compose -f docker-compose.prod.yml images
```

---

## Rollback com Banco de Dados

### Se houver migrations

```bash
#!/bin/bash

echo "⚠️  ROLLBACK COM BANCO DE DADOS"
echo ""
echo "Este procedimento irá:"
echo "  1. Parar a aplicação"
echo "  2. Reverter migrations do banco"
echo "  3. Restaurar versão anterior da aplicação"
echo ""

read -p "Digite ROLLBACK-DB para confirmar: " CONFIRM
if [[ "$CONFIRM" != "ROLLBACK-DB" ]]; then
    echo "Cancelado"
    exit 0
fi

# 1. Parar aplicação
echo "[1/4] Parando aplicação..."
docker compose -f docker-compose.prod.yml stop api

# 2. Reverter migration
echo "[2/4] Revertendo última migration..."
# Conectar ao container e executar rollback
docker compose -f docker-compose.prod.yml run --rm api \
    dotnet ef database update <PREVIOUS_MIGRATION_NAME>

# Ou se tiver script SQL de rollback:
# docker compose -f docker-compose.prod.yml exec db \
#     psql -U postgres -d myapp -f /rollback/rollback_v1.0.1.sql

# 3. Restaurar imagem anterior
echo "[3/4] Restaurando versão anterior..."
docker tag myapp:${PREVIOUS_TAG} myapp:prod-latest

# 4. Iniciar
echo "[4/4] Iniciando aplicação..."
docker compose -f docker-compose.prod.yml up -d api

# Verificar
sleep 15
curl -s http://localhost:8080/health | jq .
```

### Se precisar restaurar backup

```bash
#!/bin/bash

BACKUP_FILE="${1:-backup_latest.sql}"

echo "⚠️  RESTAURAÇÃO DE BACKUP DO BANCO"
echo ""
echo "  Arquivo: ${BACKUP_FILE}"
echo ""
echo "  ATENÇÃO: Isso irá SUBSTITUIR todos os dados atuais!"
echo ""

read -p "Digite RESTAURAR-BACKUP para confirmar: " CONFIRM
if [[ "$CONFIRM" != "RESTAURAR-BACKUP" ]]; then
    echo "Cancelado"
    exit 0
fi

# 1. Parar aplicação
docker compose -f docker-compose.prod.yml stop api

# 2. Restaurar backup
docker compose -f docker-compose.prod.yml exec db \
    psql -U postgres -d myapp < ${BACKUP_FILE}

# 3. Restaurar imagem anterior
docker tag myapp:${PREVIOUS_TAG} myapp:prod-latest

# 4. Iniciar
docker compose -f docker-compose.prod.yml up -d api
```

---

## Comandos de Emergência

### Parar Tudo Imediatamente

```bash
# Parar todos os containers do compose
docker compose -f docker-compose.prod.yml down

# Ou forçar parada
docker compose -f docker-compose.prod.yml kill
```

### Ver Logs em Tempo Real

```bash
# Todos os serviços
docker compose -f docker-compose.prod.yml logs -f

# Apenas API
docker compose -f docker-compose.prod.yml logs -f api

# Com timestamp
docker compose -f docker-compose.prod.yml logs -f --timestamps api
```

### Verificar Estado

```bash
# Status dos containers
docker compose -f docker-compose.prod.yml ps -a

# Uso de recursos
docker stats --no-stream

# Processos dentro do container
docker compose -f docker-compose.prod.yml exec api ps aux
```

### Reiniciar Serviço

```bash
# Reiniciar apenas API (sem rebuild)
docker compose -f docker-compose.prod.yml restart api

# Reiniciar com rebuild
docker compose -f docker-compose.prod.yml up -d --build api
```

---

## Script Completo de Rollback

```bash
#!/bin/bash
set -e

echo "══════════════════════════════════════════════════════════════"
echo "           ⚠️  ROLLBACK PRODUÇÃO"
echo "══════════════════════════════════════════════════════════════"
echo ""

# Configuração
APP_NAME="${APP_NAME:-myapp}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
HEALTH_URL="${HEALTH_URL:-http://localhost:8080/health}"

# Listar versões disponíveis
echo "Versões disponíveis:"
echo ""
docker images ${APP_NAME} --format "table {{.Tag}}\t{{.CreatedAt}}\t{{.Size}}" | head -10
echo ""

# Solicitar versão
read -p "Digite a TAG para rollback (ou 'latest' para anterior): " TARGET_TAG

if [[ -z "$TARGET_TAG" ]]; then
    echo "Tag não informada. Cancelando."
    exit 1
fi

# Verificar se tag existe
if ! docker image inspect ${APP_NAME}:${TARGET_TAG} > /dev/null 2>&1; then
    echo "❌ Tag '${TARGET_TAG}' não encontrada"
    exit 1
fi

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  Versão atual:  $(docker compose -f ${COMPOSE_FILE} images api --format '{{.Tag}}')"
echo "  Rollback para: ${TARGET_TAG}"
echo "══════════════════════════════════════════════════════════════"
echo ""

# Confirmar
read -p "Digite ROLLBACK para confirmar: " CONFIRM
if [[ "$CONFIRM" != "ROLLBACK" ]]; then
    echo "Cancelado pelo usuário"
    exit 0
fi

# Executar rollback
echo ""
echo "[1/5] Salvando estado atual..."
CURRENT_TAG=$(docker compose -f ${COMPOSE_FILE} images api --format '{{.Tag}}' 2>/dev/null || echo "unknown")
echo "  Tag atual salva: ${CURRENT_TAG}"

echo ""
echo "[2/5] Parando containers..."
docker compose -f ${COMPOSE_FILE} down

echo ""
echo "[3/5] Atualizando tag prod-latest..."
docker tag ${APP_NAME}:${TARGET_TAG} ${APP_NAME}:prod-latest

echo ""
echo "[4/5] Iniciando com versão anterior..."
docker compose -f ${COMPOSE_FILE} up -d

echo ""
echo "[5/5] Verificando health check..."
sleep 10

MAX_RETRIES=10
RETRY_INTERVAL=5

for i in $(seq 1 $MAX_RETRIES); do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 $HEALTH_URL 2>/dev/null || echo "000")
    
    if [[ "$HTTP_STATUS" == "200" ]]; then
        HEALTH_BODY=$(curl -s --max-time 10 $HEALTH_URL 2>/dev/null)
        HEALTH_STATUS=$(echo "$HEALTH_BODY" | jq -r '.status' 2>/dev/null)
        
        if [[ "$HEALTH_STATUS" == "Healthy" || "$HEALTH_STATUS" == "Degraded" ]]; then
            echo ""
            echo "══════════════════════════════════════════════════════════════"
            echo "  ✅ ROLLBACK CONCLUÍDO COM SUCESSO"
            echo "══════════════════════════════════════════════════════════════"
            echo ""
            echo "  Versão anterior: ${CURRENT_TAG}"
            echo "  Versão atual:    ${TARGET_TAG}"
            echo "  Status:          ${HEALTH_STATUS}"
            echo ""
            
            # Registrar rollback
            echo "$(date -Iseconds) ROLLBACK: ${CURRENT_TAG} -> ${TARGET_TAG}" >> deploy-history.log
            
            exit 0
        fi
    fi
    
    echo "  Tentativa $i/$MAX_RETRIES - HTTP: $HTTP_STATUS"
    sleep $RETRY_INTERVAL
done

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  ❌ ROLLBACK FALHOU"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "  Health check não passou após rollback."
echo "  AÇÃO MANUAL NECESSÁRIA!"
echo ""
echo "  Comandos úteis:"
echo "    docker compose -f ${COMPOSE_FILE} logs api"
echo "    docker compose -f ${COMPOSE_FILE} ps"
echo ""

exit 1
```

---

## Checklist Pós-Rollback

```
CHECKLIST PÓS-ROLLBACK
═══════════════════════════════════════════════════════

VERIFICAÇÃO IMEDIATA
  [ ] Health check passou
  [ ] Aplicação respondendo
  [ ] Sem erros 5xx
  [ ] Funcionalidades críticas funcionando

COMUNICAÇÃO
  [ ] Equipe de desenvolvimento notificada
  [ ] Stakeholders informados
  [ ] Incidente registrado

INVESTIGAÇÃO
  [ ] Logs coletados da versão que falhou
  [ ] Causa raiz identificada
  [ ] Ação corretiva planejada

DOCUMENTAÇÃO
  [ ] Rollback registrado em deploy-history.log
  [ ] Post-mortem agendado
  [ ] Lessons learned documentadas

═══════════════════════════════════════════════════════
```

---

## Prevenção

### Manter Histórico de Imagens

```bash
# Não deletar imagens recentes
# Manter pelo menos 5 versões anteriores

# Listar imagens de prod
docker images myapp | grep prod

# Limpar apenas imagens muito antigas (mais de 30 dias)
docker images myapp --format "{{.ID}} {{.CreatedAt}}" | \
    while read id created; do
        age=$(( ($(date +%s) - $(date -d "$created" +%s)) / 86400 ))
        if [[ $age -gt 30 ]]; then
            docker rmi $id 2>/dev/null || true
        fi
    done
```

### Backup Automático Pré-Deploy

```bash
# Adicionar ao script de deploy
backup_database() {
    BACKUP_FILE="backup_$(date +%Y%m%d%H%M%S).sql"
    
    docker compose -f docker-compose.prod.yml exec -T db \
        pg_dump -U postgres myapp > backups/${BACKUP_FILE}
    
    echo "Backup criado: ${BACKUP_FILE}"
}

# Chamar antes do deploy
backup_database
```
