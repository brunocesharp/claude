# Frameworks de Referência

Este documento detalha os frameworks teóricos utilizados na skill `discovery-metrics`.

---

## OKR (Objectives and Key Results)

### O que é

Framework de definição de metas criado na Intel e popularizado pelo Google. Conecta objetivos qualitativos (O que queremos alcançar?) a resultados mensuráveis (Como sabemos que alcançamos?).

### Estrutura

```
OBJECTIVE (O)
"O que queremos alcançar?"
- Qualitativo e inspirador
- Ambicioso mas atingível
- Prazo definido (geralmente trimestral)

KEY RESULTS (KRs)
"Como sabemos que alcançamos?"
- Quantitativos e mensuráveis
- 2-5 por objetivo
- Específicos e verificáveis
```

### Exemplo

```
OBJECTIVE: Transformar a experiência de onboarding de clientes

KEY RESULTS:
- KR1: Reduzir tempo de onboarding de 5 dias para 1 dia
- KR2: Aumentar taxa de ativação de 60% para 85%
- KR3: Atingir NPS de onboarding > 50
```

### Boas Práticas

| Fazer | Evitar |
|-------|--------|
| Objetivos inspiradores | Objetivos vagos |
| KRs mensuráveis | KRs subjetivos |
| 2-5 KRs por objetivo | Muitos KRs (>5) |
| Resultados, não tarefas | Lista de entregas |
| Metas ambiciosas (70% sucesso = ok) | Metas fáceis demais |

### Quando usar

- Planejamento trimestral
- Alinhamento de equipes
- Projetos com múltiplos stakeholders
- Quando precisa conectar visão a métricas

---

## North Star Metric

### O que é

Uma única métrica que melhor captura o valor central que seu produto entrega aos clientes. Serve como bússola para todas as decisões de produto.

### Características de uma boa North Star

| Critério | Descrição |
|----------|-----------|
| **Reflete valor para o cliente** | Não só receita, mas valor real entregue |
| **Indicador leading** | Prevê sucesso futuro, não só mede passado |
| **Acionável** | Equipe pode influenciar diretamente |
| **Compreensível** | Todos entendem o que significa |
| **Única** | Uma só métrica, não um conjunto |

### Exemplos por Tipo de Produto

| Produto | North Star Metric | Por quê |
|---------|-------------------|---------|
| **Spotify** | Tempo de escuta | Reflete engajamento real |
| **Airbnb** | Noites reservadas | Captura valor para hóspede E anfitrião |
| **Slack** | Mensagens enviadas por organização | Indica colaboração ativa |
| **Facebook** | Daily Active Users | Mede engajamento diário |
| **Netflix** | Horas assistidas por mês | Reflete valor entregue ao assinante |
| **Uber** | Corridas completadas | Captura valor bilateral |

### Framework para Encontrar sua North Star

1. **Qual é o momento de valor?**
   - Quando o usuário diz "isso valeu a pena"?

2. **O que leva a esse momento?**
   - Que ação do usuário indica valor?

3. **Como medimos isso?**
   - Frequência? Volume? Velocidade?

4. **Essa métrica leva a receita sustentável?**
   - Se cresce, o negócio fica saudável?

### Armadilhas

| Armadilha | Exemplo | Problema |
|-----------|---------|----------|
| Métrica de vaidade | Cadastros | Não indica valor |
| Foco só em receita | MRR | Ignora saúde do cliente |
| Múltiplas North Stars | "Engagement E conversão E..." | Dilui o foco |
| Métrica lagging | Churn | Mede o que já aconteceu |

---

## HEART Framework (Google)

### O que é

Framework criado pelo Google para medir qualidade da experiência do usuário em escala. Cobre cinco dimensões complementares.

### As Cinco Dimensões

#### H - Happiness (Felicidade)

**O que mede:** Satisfação subjetiva do usuário

**Métricas típicas:**
- Net Promoter Score (NPS)
- Customer Satisfaction (CSAT)
- Perceived usability (SUS score)
- Sentiment analysis

**Como coletar:**
- Surveys in-app
- Pesquisas periódicas
- Análise de reviews

---

#### E - Engagement (Engajamento)

**O que mede:** Intensidade do uso

**Métricas típicas:**
- Frequência de uso (DAU/WAU/MAU)
- Sessões por usuário
- Tempo na aplicação
- Features usadas
- Ações por sessão

**Como coletar:**
- Analytics de produto
- Eventos de uso
- Logs de atividade

---

#### A - Adoption (Adoção)

**O que mede:** Novos usuários ou expansão de uso

**Métricas típicas:**
- Taxa de ativação
- Novos usuários por período
- Primeira ação de valor
- Upgrade de plano
- Features adotadas pela primeira vez

**Como coletar:**
- Funil de onboarding
- Cohort analysis
- Feature flags

---

#### R - Retention (Retenção)

**O que mede:** Usuários que continuam usando ao longo do tempo

**Métricas típicas:**
- Retenção D1, D7, D30
- Churn rate
- Renovação de assinatura
- Usuários recorrentes

**Como coletar:**
- Cohort analysis
- Análise de churn
- Billing data

---

#### T - Task Success (Sucesso na Tarefa)

**O que mede:** Eficácia em completar tarefas específicas

**Métricas típicas:**
- Taxa de conclusão
- Tempo para completar
- Taxa de erro
- Abandono de tarefa
- Necessidade de suporte

**Como coletar:**
- Funil analytics
- Testes de usabilidade
- Tickets de suporte
- Session recordings

---

### Matriz HEART Completa

| Dimensão | Goals | Signals | Metrics |
|----------|-------|---------|---------|
| Happiness | Usuários satisfeitos | Feedback positivo | NPS > 50 |
| Engagement | Uso diário | Sessões frequentes | DAU/MAU > 30% |
| Adoption | Novos usuários ativos | Primeira ação de valor | Ativação > 70% |
| Retention | Usuários fiéis | Retorno frequente | D30 > 20% |
| Task Success | Tarefas fáceis | Conclusão sem erros | Completion > 90% |

### Quando usar cada dimensão

| Tipo de projeto | Priorizar |
|-----------------|-----------|
| App de consumo | Engagement, Retention |
| Ferramenta B2B | Task Success, Adoption |
| E-commerce | Task Success (checkout), Happiness |
| Marketplace | Adoption, Retention (ambos os lados) |
| Plataforma SaaS | Engagement, Retention, Task Success |

---

## AARRR (Pirate Metrics)

### O que é

Framework de Dave McClure para startups, focado no funil de crescimento. Nome vem das cinco fases: Acquisition, Activation, Retention, Referral, Revenue.

### O Funil

```
    ACQUISITION (Aquisição)
         "Como usuários nos encontram?"
              │
              ▼
    ACTIVATION (Ativação)
         "Primeira experiência de valor?"
              │
              ▼
    RETENTION (Retenção)
         "Voltam e continuam usando?"
              │
              ▼
    REFERRAL (Referência)
         "Recomendam para outros?"
              │
              ▼
    REVENUE (Receita)
         "Pagam pelo valor?"
```

### Métricas por Fase

| Fase | Métrica típica | Meta comum |
|------|----------------|------------|
| **Acquisition** | CAC, Visitantes únicos, Leads | Otimizar custo por lead qualificado |
| **Activation** | Taxa de ativação, Time to value | >50% completam setup |
| **Retention** | D1/D7/D30, Churn | Manter usuários ativos |
| **Referral** | NPS, K-factor, Convites | NPS > 50, viralidade |
| **Revenue** | LTV, MRR, Conversão | LTV > 3x CAC |

### Quando usar

- Startups em fase de crescimento
- Produtos com modelo de aquisição definido
- Quando precisa diagnosticar onde o funil quebra
- Otimização de growth

---

## Combinando os Frameworks

### Fluxo Recomendado

1. **Defina a North Star Metric**
   - Uma métrica que captura o valor central

2. **Use OKRs para objetivos de período**
   - Objetivo qualitativo + Key Results mensuráveis

3. **Use HEART para métricas de usuário**
   - Cobertura completa da experiência

4. **Use AARRR para diagnóstico de funil**
   - Identificar onde otimizar

### Exemplo Integrado

```
NORTH STAR: Usuários ativos semanais que completam 3+ tarefas

OKR:
  O: Aumentar engajamento dos usuários no Q1
  KR1: WAU de 10k para 25k
  KR2: Média de tarefas por usuário de 2 para 4
  KR3: NPS de 35 para 50

HEART:
  - Happiness: NPS mensal
  - Engagement: Tarefas por semana
  - Adoption: Ativação em 7 dias
  - Retention: Retenção D30
  - Task Success: Taxa de conclusão

AARRR:
  - Acquisition: Leads orgânicos
  - Activation: Setup completo em 24h
  - Retention: WAU/MAU
  - Referral: Convites enviados
  - Revenue: Conversão trial→pago
```
