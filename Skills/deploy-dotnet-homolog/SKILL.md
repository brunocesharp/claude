---
name: dotnet-deploy-homolog
description: Executa deploy de aplicação .NET API no ambiente de Homologação. Use quando o usuário mencionar "deploy homologação", "deploy homolog", "publicar em homologação", "subir para homolog", "deploy staging", "deploy hml", "fazer deploy homolog", "atualizar homologação", "deploy ambiente de teste", "publicar API homolog". Também dispara quando pedir para fazer build e deploy da aplicação em ambiente de teste/staging. NÃO use para deploy em produção (use dotnet-deploy-prod) ou para desenvolvimento local.
---

# .NET Deploy Homologação

Executa pipeline completo de deploy para ambiente de Homologação com Docker Compose.

## IMPORTANTE: Execução Obrigatória e Sequencial

**TODAS as etapas devem ser executadas NA ORDEM especificada.**
**Se QUALQUER etapa falhar, INTERROMPER IMEDIATAMENTE.**

## Pipeline de Deploy

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Restore   │───►│    Build    │───►│    Test     │───►│Docker Build │───►│   Deploy    │───►│Health Check │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼                  ▼                  ▼
   Falhou?            Falhou?            Falhou?            Falhou?            Falhou?            Falhou?
      │                  │                  │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼                  ▼                  ▼
   PARAR              PARAR              PARAR              PARAR              PARAR              PARAR
```

## Instruções

### ANTES de executar, consulte as referências:

1. **Leia `references/pipeline-steps.md`** para comandos detalhados de cada etapa
2. **Leia `references/health-check.md`** para validação pós-deploy
3. **Leia `references/troubleshooting.md`** para resolução de problemas

### Passo 1: Verificar Pré-requisitos

Antes de iniciar, confirmar:
- [ ] Arquivo `*.sln` existe na raiz do projeto
- [ ] `Dockerfile` existe
- [ ] `docker-compose.yml` ou `docker-compose.homolog.yml` existe
- [ ] Docker está rodando

### Passo 2: Executar Pipeline

Executar **EXATAMENTE** nesta ordem:

| Etapa | Comando | Critério de Sucesso |
|-------|---------|---------------------|
| 1. Restore | `dotnet restore` | Exit code 0 |
| 2. Build | `dotnet build --no-restore --configuration Release` | Exit code 0 |
| 3. Test | `dotnet test --no-build --configuration Release` | Exit code 0, todos os testes passando |
| 4. Docker Build | `docker build -t {image}:{tag} .` | Exit code 0 |
| 5. Deploy | `docker compose up -d --build` | Exit code 0 |
| 6. Health Check | `curl http://localhost:{port}/health` | HTTP 200 ou 204 |

### Passo 3: Gerar Relatório

#### Em caso de SUCESSO (todas as etapas OK):

```
✅ Deploy concluído com sucesso.

Resumo:
- Restore: OK
- Build: OK
- Testes: OK (X passed, 0 failed)
- Docker build: OK
- Deploy: OK
- Health check: OK

Artefatos:
- Imagem: {nome-app}:homolog-{timestamp}
- Ambiente: HOMOLOGAÇÃO
- Estratégia: docker compose
- URL: http://localhost:{port}
```

#### Em caso de FALHA (qualquer etapa):

```
❌ Deploy falhou na etapa: {ETAPA}

Resumo:
- Restore: OK
- Build: OK
- Testes: FALHOU ← erro aqui
- Docker build: NÃO EXECUTADO
- Deploy: NÃO EXECUTADO
- Health check: NÃO EXECUTADO

Erro:
{mensagem de erro detalhada}

Ação sugerida:
{sugestão de correção}
```

## Variáveis de Ambiente

| Variável | Valor Padrão | Descrição |
|----------|--------------|-----------|
| `ASPNETCORE_ENVIRONMENT` | `Staging` | Ambiente da aplicação |
| `IMAGE_TAG` | `homolog-{yyyyMMddHHmmss}` | Tag da imagem Docker |
| `HEALTH_CHECK_URL` | `http://localhost:8080/health` | URL do health check |
| `HEALTH_CHECK_TIMEOUT` | `30` | Timeout em segundos |
| `HEALTH_CHECK_RETRIES` | `5` | Número de tentativas |

## Checklist Final

- [ ] Todas as 6 etapas executadas com sucesso
- [ ] Health check retornou status saudável
- [ ] Relatório gerado com todos os artefatos
- [ ] Logs verificados para erros/warnings

## Troubleshooting Rápido

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| Restore falha | Pacotes não encontrados | Verificar NuGet sources |
| Build falha | Erro de compilação | Verificar logs de build |
| Testes falham | Testes quebrando | Analisar testes que falharam |
| Docker build falha | Dockerfile inválido | Verificar sintaxe do Dockerfile |
| Deploy falha | Porta em uso | Verificar `docker ps` |
| Health check falha | App não iniciou | Verificar logs do container |
