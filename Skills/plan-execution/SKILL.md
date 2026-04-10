---
name: dotnet-execution-plan
description: Gera planos de execução para implementação de features baseados em especificações funcionais. Use quando o usuário mencionar "plano de execução", "execution plan", "planejar implementação", "dividir em tarefas", "quebrar feature", "plano de desenvolvimento", "roadmap técnico", "sprint planning técnico", "como implementar", "etapas de desenvolvimento", "ordem de implementação", "tasks de desenvolvimento", "decomposição técnica". Também dispara quando pedir para criar um plano para implementar uma especificação ou feature. NÃO use para especificação funcional (use spec-functional) ou discovery (use discovery-*).
---

# .NET Execution Plan Generator

Gera planos de execução técnicos para implementação de features, dividindo em entregas incrementais e referenciando as skills de arquitetura apropriadas.

## Instruções

### ANTES de gerar o plano, consulte as referências:

1. **Leia `references/plan-structure.md`** para estrutura do plano
2. **Leia `references/task-breakdown.md`** para decomposição de tarefas
3. **Leia `references/skill-mapping.md`** para mapeamento de skills por tipo de tarefa

### Passo 1: Analisar Especificação

Identificar na especificação:
- Entidades de domínio envolvidas
- Casos de uso (Commands/Queries)
- Endpoints necessários
- Integrações externas
- Regras de negócio

### Passo 2: Definir Entregas (Releases)

Dividir em entregas incrementais que:
- Entregam valor isoladamente
- Podem ser deployadas separadamente
- Têm dependências claras entre si
- Permitem validação parcial

### Passo 3: Decompor em Tarefas

Para cada entrega, criar tarefas seguindo a ordem de camadas:
1. **Domain** → Entidades, Value Objects, Interfaces
2. **Infrastructure** → Repositórios, Configurações EF
3. **Application** → Commands, Queries, Handlers
4. **Presentation** → Endpoints, Validators

### Passo 4: Gerar Documento

Criar `execution-plan.md` com:
- Visão geral das entregas
- Tarefas detalhadas por entrega
- Estimativas de esforço
- Dependências e riscos

## Estrutura do Plano

```markdown
# Plano de Execução: {Nome da Feature}

## Visão Geral
- **Especificação**: {link ou referência}
- **Total de Entregas**: {N}
- **Estimativa Total**: {X} dias

## Entregas

### Entrega 1: {Nome}
- **Objetivo**: {o que entrega de valor}
- **Estimativa**: {X} dias
- **Dependências**: Nenhuma | Entrega N

#### Tarefas
| # | Tarefa | Camada | Skill | Estimativa |
|---|--------|--------|-------|------------|
| 1.1 | Criar entidade X | Domain | dotnet-domain-entity | 2h |
| 1.2 | Criar repositório X | Infrastructure | dotnet-infrastructure-repository | 2h |
...
```

## Mapeamento de Skills

| Tipo de Tarefa | Skill a Usar |
|----------------|--------------|
| Entidade, Value Object, Aggregate | `dotnet-domain-entity` |
| Command, Query, Handler | `dotnet-application-feature` |
| Repositório, DbContext | `dotnet-infrastructure-repository` |
| Controller, Endpoint | `dotnet-endpoint-generator` |
| API Externa, Integração | `dotnet-external-service` |
| Deploy Homolog | `dotnet-deploy-homolog` |
| Deploy Prod | `dotnet-deploy-prod` |

## Regras de Ordenação

### Ordem entre Camadas (Obrigatória)

```
1. Domain (primeiro)
   ├── Entidades
   ├── Value Objects
   ├── Enums
   ├── Interfaces de Repositório
   └── Domain Events

2. Infrastructure (segundo)
   ├── Configurações EF Core
   ├── Repositórios
   ├── Migrations
   └── Serviços externos

3. Application (terceiro)
   ├── DTOs
   ├── Commands + Handlers
   ├── Queries + Handlers
   └── Validators

4. Presentation (último)
   ├── Request/Response Models
   ├── Controllers/Endpoints
   └── Validators de Request
```

### Ordem dentro de cada Camada

**Domain:**
1. Value Objects (sem dependência)
2. Enums
3. Entidades base
4. Aggregates (dependem de entidades)
5. Interfaces de repositório
6. Domain Events

**Application:**
1. DTOs
2. Queries simples (GetById)
3. Queries de listagem
4. Commands de criação
5. Commands de atualização
6. Commands de deleção/ação

## Critérios de Divisão de Entregas

### Por Funcionalidade (Recomendado)

```
Entrega 1: CRUD Básico
  - Criar, Ler, Atualizar, Deletar

Entrega 2: Listagem e Filtros
  - Paginação, busca, filtros

Entrega 3: Regras de Negócio
  - Validações complexas, workflows

Entrega 4: Integrações
  - APIs externas, notificações
```

### Por Entidade (Alternativo)

```
Entrega 1: Entidade A (completa)
Entrega 2: Entidade B (completa)
Entrega 3: Relacionamentos A-B
```

### Por Caso de Uso (Para features complexas)

```
Entrega 1: Caso de Uso 1
Entrega 2: Caso de Uso 2
Entrega 3: Caso de Uso 3
```

## Estimativas Padrão

| Tipo de Tarefa | Estimativa Base |
|----------------|-----------------|
| Entidade simples | 1-2h |
| Entidade com regras | 2-4h |
| Aggregate Root | 4-8h |
| Value Object | 1-2h |
| Repositório simples | 1-2h |
| Repositório com queries complexas | 2-4h |
| Command simples | 2-3h |
| Command com validações | 3-5h |
| Query simples | 1-2h |
| Query paginada | 2-3h |
| Endpoint CRUD | 2-4h |
| Integração externa | 4-8h |
| Testes unitários | +50% do tempo da feature |
| Testes integração | +30% do tempo da feature |

## Checklist do Plano

- [ ] Todas as entidades da especificação mapeadas
- [ ] Todos os casos de uso cobertos
- [ ] Ordem de dependências respeitada
- [ ] Skills apropriadas referenciadas
- [ ] Estimativas realistas
- [ ] Entregas com valor independente
- [ ] Testes incluídos nas estimativas
- [ ] Riscos e dependências documentados

## Troubleshooting

### Problema: Feature muito grande
**Solução**: Dividir em mais entregas menores, cada uma deployável

### Problema: Dependência circular entre entregas
**Solução**: Reorganizar tarefas ou criar entrega intermediária

### Problema: Estimativa muito incerta
**Solução**: Criar spike/POC como primeira entrega para reduzir incerteza
