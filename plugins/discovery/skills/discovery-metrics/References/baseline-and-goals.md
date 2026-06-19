# Baseline e Metas

Este documento detalha técnicas para definir baseline (linha de base) e metas realistas.

---

## O que é Baseline

Baseline é o valor atual de uma métrica ANTES de qualquer intervenção. É o ponto de partida para medir progresso.

### Por que é essencial

| Sem baseline | Com baseline |
|--------------|--------------|
| "Melhoramos a conversão" | "Conversão subiu de 2.3% para 3.8%" |
| "Usuários estão satisfeitos" | "NPS subiu de 32 para 48" |
| "O processo está mais rápido" | "Tempo caiu de 45min para 12min" |

**Sem baseline, não há como provar impacto.**

---

## Como Estabelecer Baseline

### Cenário 1: Dados existem

**Situação:** O sistema atual já coleta a métrica.

**Ações:**
1. Extraia dados históricos (últimos 3-12 meses)
2. Calcule média e desvio padrão
3. Identifique sazonalidade ou tendências
4. Use a média recente como baseline

**Exemplo:**
```
Dados de conversão dos últimos 6 meses:
Jan: 2.1% | Fev: 2.3% | Mar: 2.4% | Abr: 2.2% | Mai: 2.5% | Jun: 2.3%

Baseline: 2.3% (média dos últimos 3 meses)
Variação: ±0.2% (desvio padrão)
```

---

### Cenário 2: Dados existem mas não são coletados

**Situação:** A métrica poderia ser medida, mas ninguém está fazendo.

**Ações:**
1. Identifique a fonte de dados
2. Configure coleta/extração
3. Colete por 2-4 semanas antes de lançar
4. Use esse período como baseline

**Exemplo:**
```
Métrica: Tempo de processamento de pedidos
Fonte: Logs do sistema ERP
Ação: Criar query que mede tempo entre status "recebido" e "concluído"
Período de coleta: 4 semanas antes do lançamento
```

---

### Cenário 3: Dados não existem

**Situação:** Não há sistema atual, ou a métrica é nova.

**Ações:**
1. Registre "a medir" no documento
2. Defina como PRIMEIRA ação pós-lançamento
3. Colete por 2-4 semanas após lançamento
4. Só depois defina metas numéricas

**Exemplo:**
```
Métrica: NPS do novo sistema
Baseline: A medir (não havia sistema antes)
Plano: Aplicar survey após 4 semanas de uso
       Usar resultado como baseline para metas futuras
```

---

### Cenário 4: Proxy metrics

**Situação:** Métrica ideal é impossível de medir, mas há aproximações.

**Ações:**
1. Identifique métrica proxy que correlaciona
2. Documente a relação assumida
3. Use proxy com ressalvas

**Exemplos de proxies:**

| Métrica ideal | Proxy | Limitação |
|---------------|-------|-----------|
| Satisfação do cliente | NPS | Amostra pode não representar todos |
| Produtividade | Tarefas por hora | Não mede qualidade |
| Engajamento | Tempo no app | Pode indicar dificuldade, não engajamento |
| Valor entregue | Retention | Pessoas podem ficar por falta de alternativa |

---

## Como Definir Metas

### Princípios Gerais

| Princípio | Explicação |
|-----------|------------|
| **Baseadas em baseline** | Nunca defina meta sem saber onde está |
| **Específicas** | Número exato, não "melhorar" |
| **Com prazo** | "Em 3 meses", não "eventualmente" |
| **Ambiciosas mas atingíveis** | 70% de chance de atingir |
| **Conectadas ao objetivo** | Mover essa métrica importa? |

---

### Técnica 1: Benchmark de mercado

**Quando usar:** Você não tem histórico, mas o mercado tem.

**Como fazer:**
1. Pesquise benchmarks do setor
2. Identifique onde você está vs. mercado
3. Defina meta como % do benchmark

**Exemplo:**
```
Benchmark de e-commerce: Taxa de conversão média = 3%
Seu baseline: 1.8%
Meta: Atingir 2.5% em 6 meses (80% do benchmark)
```

**Fontes de benchmark:**
- Relatórios de indústria
- Publicações de VCs
- Conferências de produto
- Ferramentas de analytics (Mixpanel, Amplitude publicam benchmarks)

---

### Técnica 2: Melhoria percentual

**Quando usar:** Você tem baseline e quer definir crescimento.

**Como fazer:**
1. Avalie melhorias típicas de projetos similares
2. Aplique % de melhoria ao baseline

**Referências de melhoria:**

| Tipo de intervenção | Melhoria típica |
|---------------------|-----------------|
| Otimização de UX | 10-30% |
| Novo feature | 15-50% |
| Redesign completo | 30-100% |
| Automação de processo | 50-80% |
| Novo produto | Difícil prever |

**Exemplo:**
```
Baseline: Tempo de processo = 45 minutos
Intervenção: Automação parcial
Melhoria típica: 50-70%
Meta: Reduzir para 15-22 minutos
```

---

### Técnica 3: Objetivo reverso

**Quando usar:** Você sabe o resultado de negócio necessário.

**Como fazer:**
1. Comece pelo resultado de negócio
2. Trabalhe de trás para frente
3. Calcule a métrica necessária

**Exemplo:**
```
Resultado necessário: Aumentar receita em R$500k/ano
Ticket médio: R$200
Clientes necessários: 2.500 novos
Conversão atual: 2%
Tráfego atual: 100.000/mês

Opções:
A) Aumentar tráfego para 125.000 (25%)
B) Aumentar conversão para 2.5% (25%)
C) Combinação: tráfego +10%, conversão +10%
```

---

### Técnica 4: Análise de cohorts

**Quando usar:** Métricas de retenção ou comportamento ao longo do tempo.

**Como fazer:**
1. Analise cohorts históricos
2. Identifique padrões de queda/crescimento
3. Defina meta como melhoria da curva

**Exemplo:**
```
Retenção atual por cohort:
D1: 45% | D7: 20% | D30: 8%

Meta: Melhorar em 20% cada ponto
D1: 54% | D7: 24% | D30: 10%
```

---

## Estrutura de Metas por Período

### Horizonte de 3 meses (curto prazo)

- Metas de ativação e adoção
- Métricas operacionais
- Correções de baseline

**Exemplo:**
```
Meta 3 meses:
- Taxa de ativação: de 45% para 60%
- Tempo de onboarding: de 5 dias para 2 dias
- Bugs críticos: de 12 para 0
```

---

### Horizonte de 6 meses (médio prazo)

- Metas de engajamento e retenção
- Métricas de negócio iniciais
- Validação de hipóteses

**Exemplo:**
```
Meta 6 meses:
- DAU: de 1.000 para 5.000
- Retention D30: de 15% para 25%
- NPS: de 30 para 45
```

---

### Horizonte de 12 meses (longo prazo)

- Metas de receita e crescimento
- North Star Metric
- ROI do projeto

**Exemplo:**
```
Meta 12 meses:
- MRR: de R$50k para R$200k
- Churn: de 8% para 3%
- NRR: de 95% para 115%
```

---

## Erros Comuns

### Erro 1: Meta sem baseline

**Errado:** "Vamos atingir NPS de 50"
**Correto:** "Vamos aumentar NPS de 32 para 50"

---

### Erro 2: Meta vaga

**Errado:** "Melhorar a conversão"
**Correto:** "Aumentar conversão de 2.3% para 3.5% em 6 meses"

---

### Erro 3: Meta impossível

**Errado:** "Aumentar retenção de 10% para 80%"
**Correto:** "Aumentar retenção de 10% para 20% (dobrar)"

---

### Erro 4: Meta fácil demais

**Errado:** "Manter conversão atual"
**Correto:** "Aumentar conversão em 20%"

---

### Erro 5: Meta sem prazo

**Errado:** "Atingir 10.000 usuários"
**Correto:** "Atingir 10.000 usuários em 6 meses"

---

### Erro 6: Meta desconectada

**Errado:** "Aumentar tempo no app" (se o objetivo é eficiência)
**Correto:** "Reduzir tempo para completar tarefa"

---

## Template de Definição

| Métrica | Baseline | Meta 3m | Meta 6m | Meta 12m | Responsável | Fonte |
|---------|----------|---------|---------|----------|-------------|-------|
| {nome} | {valor atual} | {meta} | {meta} | {meta} | {quem acompanha} | {de onde vem o dado} |

---

## Checklist de Qualidade

Antes de finalizar uma meta, verifique:

- [ ] Baseline definido ou plano para definir
- [ ] Meta é um número específico
- [ ] Meta tem prazo definido
- [ ] Meta é desafiadora mas atingível
- [ ] Meta está conectada ao objetivo do projeto
- [ ] Responsável por acompanhar definido
- [ ] Fonte de dados identificada
- [ ] Frequência de medição definida
