---
name: dotnet-deploy-prod
description: Executa deploy de aplicação .NET API no ambiente de Produção. Use quando o usuário mencionar "deploy produção", "deploy prod", "publicar em produção", "subir para prod", "deploy production", "fazer deploy prod", "atualizar produção", "release produção", "go live", "deploy prd". Também dispara quando pedir para fazer build e deploy da aplicação em ambiente de produção/live. NÃO use para deploy em homologação (use dotnet-deploy-homolog) ou desenvolvimento.
---

# .NET Deploy Produção

Executa pipeline completo de deploy para ambiente de Produção com Docker Compose.

## ⚠️ AMBIENTE DE PRODUÇÃO - ATENÇÃO REDOBRADA

Este deploy afeta o ambiente de **PRODUÇÃO**. Todas as etapas incluem validações extras de segurança.

## IMPORTANTE: Execução Obrigatória e Sequencial

**TODAS as etapas devem ser executadas NA ORDEM especificada.**
**Se QUALQUER etapa falhar, INTERROMPER IMEDIATAMENTE.**
**CONFIRMAR com o usuário antes de iniciar o deploy.**

## Pipeline de Deploy

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Validação  │───►│   Restore   │───►│    Build    │───►│    Test     │───►│Docker Build │───►│   Deploy    │───►│Health Check │
│   Prévia    │    │             │    │             │    │             │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼                  ▼                  ▼                  ▼
   Falhou?            Falhou?            Falhou?            Falhou?            Falhou?            Falhou?            Falhou?
      │                  │                  │                  │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼                  ▼                  ▼                  ▼
   PARAR              PARAR              PARAR              PARAR              PARAR              PARAR              PARAR
```

## Instruções

### ANTES de executar, consulte as referências:

1. **Leia `references/pre-deploy-checklist.md`** para validações obrigatórias antes do deploy
2. **Leia `references/pipeline-steps.md`** para comandos detalhados de cada etapa
3. **Leia `references/rollback.md`** para procedimento de rollback em caso de falha

### Passo 0: Confirmação do Usuário

**OBRIGATÓRIO**: Antes de iniciar, perguntar ao usuário:

```
⚠️  DEPLOY EM PRODUÇÃO

Você está prestes a fazer deploy em PRODUÇÃO.
Esta ação afetará usuários reais.

Confirme as seguintes informações:
- Branch: main/master
- Última versão em homolog foi validada? (S/N)
- Backup do banco foi realizado? (S/N)
- Janela de manutenção acordada? (S/N)

Digite CONFIRMAR para prosseguir:
```

### Passo 1: Validação Prévia

Antes de iniciar o pipeline, verificar:
- [ ] Branch é `main` ou `master`
- [ ] Não há commits pendentes
- [ ] Arquivo `*.sln` existe na raiz
- [ ] `Dockerfile` existe
- [ ] `docker-compose.prod.yml` ou `docker-compose.yml` existe
- [ ] Docker está rodando
- [ ] Variáveis de ambiente de produção configuradas

### Passo 2: Executar Pipeline

Executar **EXATAMENTE** nesta ordem:

| Etapa | Comando | Critério de Sucesso |
|-------|---------|---------------------|
| 1. Restore | `dotnet restore` | Exit code 0 |
| 2. Build | `dotnet build --no-restore --configuration Release` | Exit code 0, 0 warnings (ideal) |
| 3. Test | `dotnet test --no-build --configuration Release` | Exit code 0, 100% passando |
| 4. Docker Build | `docker build -t {image}:{tag} .` | Exit code 0 |
| 5. Deploy | `docker compose -f docker-compose.prod.yml up -d --build` | Exit code 0 |
| 6. Health Check | `curl http://localhost:{port}/health` | HTTP 200, status "Healthy" |

### Passo 3: Gerar Relatório

#### Em caso de SUCESSO (todas as etapas OK):

```
✅ Deploy em PRODUÇÃO concluído com sucesso.

Resumo:
- Validação prévia: OK
- Restore: OK
- Build: OK
- Testes: OK (X passed, 0 failed, 0 skipped)
- Docker build: OK
- Deploy: OK
- Health check: OK (Healthy)

Artefatos:
- Imagem: {nome-app}:prod-{version}-{timestamp}
- Ambiente: PRODUÇÃO
- Estratégia: docker compose
- URL: https://{domain}

Versão anterior (para rollback):
- Imagem: {nome-app}:prod-{previous-version}
```

#### Em caso de FALHA (qualquer etapa):

```
❌ Deploy em PRODUÇÃO falhou na etapa: {ETAPA}

Resumo:
- Validação prévia: OK
- Restore: OK
- Build: OK
- Testes: FALHOU ← erro aqui
- Docker build: NÃO EXECUTADO
- Deploy: NÃO EXECUTADO
- Health check: NÃO EXECUTADO

Erro:
{mensagem de erro detalhada}

⚠️  AÇÃO IMEDIATA NECESSÁRIA:
1. NÃO tente deploy novamente sem corrigir o erro
2. Corrija o problema identificado
3. Execute novamente o pipeline completo
4. Se necessário, consulte references/rollback.md

Ação sugerida:
{sugestão de correção}
```

## Variáveis de Ambiente

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `ASPNETCORE_ENVIRONMENT` | `Production` | Ambiente da aplicação |
| `IMAGE_TAG` | `prod-{version}-{yyyyMMddHHmmss}` | Tag da imagem Docker |
| `HEALTH_CHECK_URL` | `https://{domain}/health` | URL do health check |
| `HEALTH_CHECK_TIMEOUT` | `60` | Timeout em segundos |
| `HEALTH_CHECK_RETRIES` | `10` | Número de tentativas |

## Checklist Final

- [ ] Confirmação do usuário obtida
- [ ] Validação prévia passou
- [ ] Todas as 6 etapas executadas com sucesso
- [ ] Health check retornou "Healthy"
- [ ] Todos os componentes (DB, Redis, etc.) healthy
- [ ] Relatório gerado com versão anterior para rollback
- [ ] Logs verificados para erros/warnings
- [ ] Monitoramento ativo confirmado

## Troubleshooting Rápido

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| Branch incorreta | Não está em main/master | `git checkout main && git pull` |
| Testes falham | Código quebrado | **NÃO FAZER DEPLOY** - corrigir primeiro |
| Health check Degraded | Dependência lenta | Verificar conexões externas |
| Health check Unhealthy | Erro crítico | **ROLLBACK IMEDIATO** |

## ⚠️ Procedimento de Rollback

Se algo der errado após o deploy, executar IMEDIATAMENTE:

```bash
# Rollback para versão anterior
docker compose -f docker-compose.prod.yml down
docker tag {app}:{previous-version} {app}:prod-latest
docker compose -f docker-compose.prod.yml up -d

# Verificar health
curl https://{domain}/health
```

Consulte `references/rollback.md` para procedimento completo.
