# Pre-Deploy Checklist

## ⚠️ VALIDAÇÃO OBRIGATÓRIA ANTES DO DEPLOY EM PRODUÇÃO

Este checklist DEVE ser validado antes de iniciar o pipeline de deploy.

---

## 1. Confirmação do Usuário

### Perguntas Obrigatórias

```
┌─────────────────────────────────────────────────────────────┐
│           ⚠️  DEPLOY EM PRODUÇÃO - CONFIRMAÇÃO              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Você está prestes a fazer deploy em PRODUÇÃO.              │
│  Esta ação afetará USUÁRIOS REAIS.                          │
│                                                             │
│  Por favor, confirme:                                       │
│                                                             │
│  1. A versão foi testada em homologação? ........... [ ]    │
│  2. Todos os testes automatizados passaram? ........ [ ]    │
│  3. O backup do banco de dados foi realizado? ...... [ ]    │
│  4. A janela de manutenção foi comunicada? ......... [ ]    │
│  5. A equipe de suporte foi notificada? ............ [ ]    │
│  6. O plano de rollback está documentado? .......... [ ]    │
│                                                             │
│  Digite CONFIRMAR para prosseguir ou CANCELAR para abortar  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Validação de Resposta

- Se usuário digitar `CONFIRMAR` → Prosseguir
- Se usuário digitar `CANCELAR` ou qualquer outra coisa → Abortar
- Se usuário não responder em 5 minutos → Abortar

---

## 2. Validação de Branch

### Comando

```bash
# Verificar branch atual
CURRENT_BRANCH=$(git branch --show-current)

# Validar se é main ou master
if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
    echo "❌ ERRO: Branch atual é '$CURRENT_BRANCH'"
    echo "   Deploy em produção só é permitido a partir de 'main' ou 'master'"
    exit 1
fi

echo "✅ Branch: $CURRENT_BRANCH"
```

### Verificar commits pendentes

```bash
# Verificar se há mudanças não commitadas
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ ERRO: Existem alterações não commitadas"
    echo "   Faça commit ou stash das alterações antes do deploy"
    git status --short
    exit 1
fi

echo "✅ Working directory limpo"
```

### Verificar se está atualizado

```bash
# Fetch das últimas mudanças
git fetch origin

# Comparar com remote
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$CURRENT_BRANCH)

if [[ "$LOCAL" != "$REMOTE" ]]; then
    echo "⚠️  AVISO: Branch local não está sincronizada com origin"
    echo "   Local:  $LOCAL"
    echo "   Remote: $REMOTE"
    echo ""
    read -p "Deseja fazer pull antes de continuar? (s/n): " PULL
    if [[ "$PULL" == "s" ]]; then
        git pull origin $CURRENT_BRANCH
    else
        echo "❌ Deploy cancelado"
        exit 1
    fi
fi

echo "✅ Branch sincronizada com origin"
```

---

## 3. Validação de Arquivos

### Verificar arquivos obrigatórios

```bash
# Lista de arquivos obrigatórios
REQUIRED_FILES=(
    "*.sln"
    "Dockerfile"
    "docker-compose.prod.yml"
    ".env.prod"
)

MISSING_FILES=()

for pattern in "${REQUIRED_FILES[@]}"; do
    if ! ls $pattern 1> /dev/null 2>&1; then
        MISSING_FILES+=("$pattern")
    fi
done

if [[ ${#MISSING_FILES[@]} -gt 0 ]]; then
    echo "❌ ERRO: Arquivos obrigatórios não encontrados:"
    for file in "${MISSING_FILES[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

echo "✅ Todos os arquivos obrigatórios presentes"
```

### Verificar docker-compose.prod.yml

```bash
# Validar sintaxe do docker-compose
if ! docker compose -f docker-compose.prod.yml config > /dev/null 2>&1; then
    echo "❌ ERRO: docker-compose.prod.yml inválido"
    docker compose -f docker-compose.prod.yml config
    exit 1
fi

echo "✅ docker-compose.prod.yml válido"
```

---

## 4. Validação de Ambiente

### Verificar Docker

```bash
# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ ERRO: Docker não está rodando"
    exit 1
fi

echo "✅ Docker rodando"

# Verificar espaço em disco
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [[ $DISK_USAGE -gt 85 ]]; then
    echo "⚠️  AVISO: Disco com ${DISK_USAGE}% de uso"
    echo "   Considere limpar imagens não utilizadas: docker system prune"
fi
```

### Verificar variáveis de ambiente

```bash
# Variáveis obrigatórias para produção
REQUIRED_VARS=(
    "DATABASE_URL"
    "REDIS_URL"
    "JWT_SECRET"
    "API_KEY"
)

# Carregar .env.prod
if [[ -f .env.prod ]]; then
    export $(grep -v '^#' .env.prod | xargs)
fi

MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var}" ]]; then
        MISSING_VARS+=("$var")
    fi
done

if [[ ${#MISSING_VARS[@]} -gt 0 ]]; then
    echo "❌ ERRO: Variáveis de ambiente não configuradas:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    exit 1
fi

echo "✅ Variáveis de ambiente configuradas"
```

---

## 5. Validação de Versão

### Obter versão atual

```bash
# Tentar obter versão do .csproj
VERSION=$(grep -oPm1 "(?<=<Version>)[^<]+" src/*/*.csproj 2>/dev/null | head -1)

if [[ -z "$VERSION" ]]; then
    # Fallback: usar tag git
    VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "0.0.0")
fi

echo "Versão a ser deployada: $VERSION"

# Verificar se a tag já existe
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo "⚠️  AVISO: Tag v$VERSION já existe"
    read -p "Deseja continuar mesmo assim? (s/n): " CONTINUE
    if [[ "$CONTINUE" != "s" ]]; then
        exit 1
    fi
fi
```

### Gerar tag de imagem

```bash
# Formato: prod-{version}-{timestamp}
TIMESTAMP=$(date +%Y%m%d%H%M%S)
IMAGE_TAG="prod-${VERSION}-${TIMESTAMP}"

echo "Tag da imagem: $IMAGE_TAG"
```

---

## 6. Backup Verification

### Verificar backup recente

```bash
echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│                    VERIFICAÇÃO DE BACKUP                    │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│                                                             │"
echo "│  Antes de prosseguir, confirme que:                         │"
echo "│                                                             │"
echo "│  1. Backup do banco de dados foi realizado                  │"
echo "│  2. Backup foi testado/validado                             │"
echo "│  3. Backup está armazenado em local seguro                  │"
echo "│                                                             │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""
read -p "Backup verificado? (s/n): " BACKUP_OK

if [[ "$BACKUP_OK" != "s" ]]; then
    echo "❌ Deploy cancelado - Backup não verificado"
    exit 1
fi

echo "✅ Backup verificado"
```

---

## 7. Script Completo de Validação

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "  Validação Pré-Deploy - PRODUÇÃO"
echo "=========================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
    ((CHECKS_PASSED++))
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    ((CHECKS_FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

# 1. Branch
echo "[1/7] Verificando branch..."
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
    check_pass "Branch: $BRANCH"
else
    check_fail "Branch inválida: $BRANCH (esperado: main ou master)"
fi

# 2. Working directory
echo ""
echo "[2/7] Verificando working directory..."
if [[ -z $(git status --porcelain) ]]; then
    check_pass "Working directory limpo"
else
    check_fail "Alterações não commitadas encontradas"
fi

# 3. Arquivos obrigatórios
echo ""
echo "[3/7] Verificando arquivos obrigatórios..."
for file in "Dockerfile" "docker-compose.prod.yml"; do
    if [[ -f "$file" ]]; then
        check_pass "$file encontrado"
    else
        check_fail "$file não encontrado"
    fi
done

# 4. Docker
echo ""
echo "[4/7] Verificando Docker..."
if docker info > /dev/null 2>&1; then
    check_pass "Docker rodando"
else
    check_fail "Docker não está rodando"
fi

# 5. Docker Compose válido
echo ""
echo "[5/7] Validando docker-compose.prod.yml..."
if docker compose -f docker-compose.prod.yml config > /dev/null 2>&1; then
    check_pass "docker-compose.prod.yml válido"
else
    check_fail "docker-compose.prod.yml inválido"
fi

# 6. Espaço em disco
echo ""
echo "[6/7] Verificando espaço em disco..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [[ $DISK_USAGE -lt 80 ]]; then
    check_pass "Espaço em disco OK (${DISK_USAGE}% usado)"
elif [[ $DISK_USAGE -lt 90 ]]; then
    check_warn "Espaço em disco baixo (${DISK_USAGE}% usado)"
else
    check_fail "Espaço em disco crítico (${DISK_USAGE}% usado)"
fi

# 7. Versão
echo ""
echo "[7/7] Obtendo versão..."
VERSION=$(grep -oPm1 "(?<=<Version>)[^<]+" src/*/*.csproj 2>/dev/null | head -1 || echo "1.0.0")
check_pass "Versão: $VERSION"

# Resumo
echo ""
echo "=========================================="
echo "  Resumo da Validação"
echo "=========================================="
echo -e "  Passou:  ${GREEN}${CHECKS_PASSED}${NC}"
echo -e "  Falhou:  ${RED}${CHECKS_FAILED}${NC}"
echo -e "  Avisos:  ${YELLOW}${WARNINGS}${NC}"
echo ""

if [[ $CHECKS_FAILED -gt 0 ]]; then
    echo -e "${RED}❌ Validação FALHOU - Corrija os erros antes de continuar${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Validação PASSOU - Pronto para deploy${NC}"
    exit 0
fi
```

---

## Checklist Visual

```
PRE-DEPLOY CHECKLIST - PRODUÇÃO
═══════════════════════════════════════════════════════

CONFIRMAÇÃO DO USUÁRIO
  [ ] Usuário confirmou ciência do deploy em produção
  [ ] Versão foi testada em homologação
  [ ] Stakeholders foram notificados

CÓDIGO
  [ ] Branch é main/master
  [ ] Sem commits pendentes
  [ ] Sincronizado com origin
  [ ] Todos os testes passando

INFRAESTRUTURA  
  [ ] Docker rodando
  [ ] Espaço em disco suficiente (>15% livre)
  [ ] Variáveis de ambiente configuradas
  [ ] Secrets não expostos

ARQUIVOS
  [ ] Dockerfile presente
  [ ] docker-compose.prod.yml válido
  [ ] .env.prod configurado
  [ ] Health checks implementados

BACKUP & ROLLBACK
  [ ] Backup do banco realizado
  [ ] Backup testado/validado
  [ ] Versão anterior documentada
  [ ] Plano de rollback pronto

COMUNICAÇÃO
  [ ] Equipe de suporte notificada
  [ ] Janela de manutenção (se necessário)
  [ ] Canais de comunicação ativos

═══════════════════════════════════════════════════════
```
