# Catálogo de Métricas por Tipo de Projeto

Este documento oferece exemplos de métricas para diferentes tipos de projeto, organizados por categoria.

---

## E-commerce / Marketplace

### North Star Options
- **Receita por usuário ativo** (foco em monetização)
- **Pedidos completados** (foco em conversão)
- **Transações bem-sucedidas** (marketplace bilateral)

### Métricas de Negócio

| Métrica | Definição | Benchmark típico |
|---------|-----------|------------------|
| GMV | Gross Merchandise Value | Depende do setor |
| AOV | Average Order Value | Varia por categoria |
| Taxa de conversão | Visitantes → compradores | 2-5% (e-commerce geral) |
| CAC | Custo de aquisição de cliente | < LTV/3 |
| LTV | Lifetime Value | > 3x CAC |
| Taxa de recompra | % que compra novamente | 20-40% (bom) |

### Métricas de Usuário (HEART)

| Dimensão | Métrica | Como medir |
|----------|---------|------------|
| Happiness | NPS pós-compra | Survey após entrega |
| Engagement | Sessões por mês | Analytics |
| Adoption | Primeira compra em X dias | Cohort |
| Retention | Compras repetidas em 90 dias | Cohort |
| Task Success | Checkout completion rate | Funil |

### Métricas de Produto

| Métrica | Fórmula |
|---------|---------|
| Add-to-cart rate | Adições ao carrinho / Visualizações de produto |
| Cart abandonment | Carrinhos abandonados / Carrinhos criados |
| Checkout abandonment | Abandonos no checkout / Checkouts iniciados |
| Search-to-purchase | Compras / Buscas realizadas |

---

## SaaS B2B

### North Star Options
- **Weekly Active Users (WAU)** (foco em engajamento)
- **Net Revenue Retention (NRR)** (foco em expansão)
- **Value delivered** (ações de valor por usuário)

### Métricas de Negócio

| Métrica | Definição | Benchmark típico |
|---------|-----------|------------------|
| MRR/ARR | Monthly/Annual Recurring Revenue | Crescimento > 100% a/a (early stage) |
| Churn rate | % receita perdida por mês | < 2% mensal (bom) |
| NRR | Net Revenue Retention | > 100% (saudável), > 120% (excelente) |
| CAC | Custo de aquisição | Payback < 18 meses |
| LTV | Lifetime Value do cliente | > 3x CAC |
| ACV | Annual Contract Value | Depende do segmento |

### Métricas de Usuário

| Dimensão | Métrica | Como medir |
|----------|---------|------------|
| Happiness | NPS trimestral | Survey |
| Engagement | DAU/WAU/MAU | Analytics |
| Adoption | Time to first value | Onboarding analytics |
| Retention | Logo retention | CRM |
| Task Success | Feature completion rate | Product analytics |

### Métricas de Produto

| Métrica | O que indica |
|---------|--------------|
| Feature adoption rate | % usuários que usam feature X |
| Depth of use | Features diferentes usadas por usuário |
| Power user ratio | % usuários com uso avançado |
| Support tickets per user | Proxy para usabilidade |

---

## Sistema Interno / Corporativo

### North Star Options
- **Tempo economizado por processo** (foco em eficiência)
- **Custo evitado** (foco em redução de custos)
- **Processos concluídos sem erro** (foco em qualidade)

### Métricas de Negócio

| Métrica | Definição | Como calcular |
|---------|-----------|---------------|
| Tempo médio de processo | Minutos/horas por tarefa | (Tempo antes - Tempo depois) |
| Custo por transação | R$ gastos por operação | Custo total / Transações |
| Taxa de erro | % transações com erro | Erros / Total |
| Capacidade | Transações por período | Volume / Tempo |
| FTE economizado | Pessoas reposicionadas | Horas economizadas / Jornada |

### Métricas de Usuário

| Dimensão | Métrica | Como medir |
|----------|---------|------------|
| Happiness | CSAT dos funcionários | Survey |
| Engagement | % de adesão ao sistema | Usuários ativos / Total |
| Adoption | Migração do sistema antigo | % usando apenas sistema novo |
| Task Success | Taxa de conclusão | Tarefas completas / Iniciadas |

### Métricas de Qualidade

| Métrica | O que indica |
|---------|--------------|
| Taxa de retrabalho | % tarefas que precisam ser refeitas |
| Tempo de resolução | Tempo para resolver problemas |
| Tickets de suporte | Volume de pedidos de ajuda |
| Conformidade | % processos dentro do padrão |

---

## App Mobile / Consumer

### North Star Options
- **Daily Active Users (DAU)** (foco em hábito)
- **Tempo no app por sessão** (foco em engajamento)
- **Ações de valor por usuário** (foco em resultado)

### Métricas de Negócio

| Métrica | Definição | Benchmark típico |
|---------|-----------|------------------|
| Downloads | Instalações totais | Depende do mercado |
| CPI | Cost per Install | Varia por categoria/país |
| ARPU | Average Revenue per User | Depende da monetização |
| DAU/MAU | Stickiness | > 20% (bom), > 50% (excelente) |

### Métricas de Usuário

| Dimensão | Métrica | Benchmark |
|----------|---------|-----------|
| Retention D1 | % volta no dia seguinte | > 40% |
| Retention D7 | % volta após 7 dias | > 20% |
| Retention D30 | % volta após 30 dias | > 10% |
| Session length | Tempo médio por sessão | Varia por categoria |
| Sessions per day | Sessões por usuário/dia | > 2 (alto engajamento) |

### Métricas de Growth

| Métrica | Fórmula |
|---------|---------|
| K-factor (viralidade) | Convites enviados × Taxa de conversão |
| Organic ratio | Downloads orgânicos / Total |
| Reactivation rate | Usuários dormentes que voltaram |

---

## Plataforma / Marketplace Bilateral

### North Star Options
- **Transações completadas** (captura valor dos dois lados)
- **Liquidity** (oferta disponível × demanda ativa)
- **Match rate** (conexões bem-sucedidas)

### Métricas por Lado

#### Lado da Oferta (sellers, drivers, hosts)
| Métrica | O que indica |
|---------|--------------|
| Supply growth | Crescimento de fornecedores |
| Supply utilization | % capacidade utilizada |
| Earnings per provider | Receita média por fornecedor |
| Provider churn | Perda de fornecedores |
| Time to first transaction | Velocidade de ativação |

#### Lado da Demanda (buyers, riders, guests)
| Métrica | O que indica |
|---------|--------------|
| Demand growth | Crescimento de compradores |
| Purchase frequency | Frequência de compra |
| Average transaction value | Ticket médio |
| Buyer retention | Retenção de compradores |
| Search-to-book | Conversão de busca |

### Métricas de Plataforma

| Métrica | O que indica |
|---------|--------------|
| Take rate | % da transação retida pela plataforma |
| Match rate | % buscas que resultam em transação |
| Time to match | Tempo entre busca e match |
| Cancellation rate | % transações canceladas |
| Dispute rate | % transações com problemas |

---

## Projeto de Automação / RPA

### North Star Options
- **Processos automatizados por dia** (volume)
- **Tempo humano economizado** (eficiência)
- **Taxa de automação sem intervenção** (qualidade)

### Métricas de Eficiência

| Métrica | Fórmula |
|---------|---------|
| Tempo economizado | (Tempo manual - Tempo automatizado) × Volume |
| FTE equivalent | Horas automatizadas / 2.080 |
| ROI do projeto | (Economia anual - Custo do projeto) / Custo |
| Payback period | Custo / Economia mensal |

### Métricas de Qualidade

| Métrica | O que indica |
|---------|--------------|
| Straight-through rate | % processos sem intervenção humana |
| Exception rate | % que precisa de revisão manual |
| Error rate | % com erro de processamento |
| Rework rate | % que precisa ser refeito |

### Métricas Operacionais

| Métrica | O que indica |
|---------|--------------|
| Uptime | Disponibilidade do processo |
| Processing time | Tempo por transação |
| Queue depth | Tamanho da fila de processamento |
| Throughput | Transações por período |

---

## MVP / Validação de Hipótese

### North Star Options
- **Usuários que completam ação de valor** (validação de demanda)
- **Willingness to pay** (validação de negócio)
- **Retenção semanal** (validação de engajamento)

### Métricas de Validação

| Hipótese | Métrica | Threshold |
|----------|---------|-----------|
| Existe demanda? | Landing page conversion | > 5% |
| Resolvemos o problema? | % completam tarefa principal | > 60% |
| Usariam de novo? | Retention D7 | > 30% |
| Pagariam? | Pré-vendas / Conversão trial | > 2% |
| Recomendariam? | NPS | > 30 |

### Métricas de Aprendizado

| Métrica | O que indica |
|---------|--------------|
| Time to learn | Tempo até ter dados suficientes |
| Experiment velocity | Experimentos por semana |
| Decision confidence | Significância estatística |

---

## Como Escolher Métricas

### Checklist de Qualidade

Antes de definir uma métrica, pergunte:

| Pergunta | Se NÃO... |
|----------|-----------|
| É mensurável? | Não é métrica, é desejo |
| Podemos influenciar? | Não é acionável |
| Reflete valor para usuário? | Pode ser métrica de vaidade |
| Temos como coletar? | Precisa planejar instrumentação |
| É comparável no tempo? | Difícil avaliar progresso |

### Quantidade Ideal

| Tipo | Quantidade recomendada |
|------|------------------------|
| North Star | 1 (apenas uma) |
| Métricas de negócio | 3-5 |
| Métricas de usuário | 3-5 |
| Métricas operacionais | 2-4 |
| **Total** | **10-15 métricas** |

### Evite

- Mais de 20 métricas (perda de foco)
- Menos de 5 métricas (visão incompleta)
- Só métricas de negócio (ignora usuário)
- Só métricas de vaidade (cadastros, downloads)
