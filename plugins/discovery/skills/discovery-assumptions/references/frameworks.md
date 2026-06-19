# Frameworks de Referência

Este documento detalha os frameworks teóricos utilizados na skill `discovery-assumptions`.

---

## Assumption Mapping (David Bland & Alex Osterwalder)

### O que é

Técnica visual para identificar, categorizar e priorizar suposições de negócio antes de investir recursos em desenvolvimento. Apresentada no livro "Testing Business Ideas".

### Por que usar

- Evita construir produtos baseados em suposições não testadas
- Prioriza o que validar primeiro
- Reduz risco de investimento em ideias que não funcionam
- Cria alinhamento no time sobre incertezas

### Tipos de Hipóteses

| Tipo | Descrição | Exemplos |
|------|-----------|----------|
| **Desirability** | O cliente quer isso? | "Usuários pagariam por essa feature", "Isso resolve uma dor real" |
| **Feasibility** | Conseguimos construir? | "A API suporta esse volume", "Temos a expertise técnica" |
| **Viability** | Faz sentido para o negócio? | "O custo de aquisição é sustentável", "O mercado é grande o suficiente" |

### Processo de Mapping

1. **Listar** — Identificar todas as suposições embutidas na ideia
2. **Categorizar** — Classificar por tipo (Desirability, Feasibility, Viability)
3. **Priorizar** — Usar matriz impacto x certeza
4. **Testar** — Desenhar experimentos para hipóteses críticas
5. **Aprender** — Ajustar a ideia com base nos resultados

### Armadilhas Comuns

| Armadilha | Como evitar |
|-----------|-------------|
| Tratar suposição como fato | Pergunte: "Qual foi a última evidência?" |
| Validar apenas hipóteses fáceis | Priorize por impacto, não por conveniência |
| Pular direto para desenvolvimento | Exija validação das hipóteses críticas primeiro |
| Confirmation bias | Busque evidências que refutem a hipótese |

### Referências

- Livro: "Testing Business Ideas" — David Bland & Alex Osterwalder
- Livro: "Value Proposition Design" — Alex Osterwalder
- Ferramenta: Strategyzer

---

## Lean Startup (Eric Ries)

### O que é

Metodologia de desenvolvimento de produtos que enfatiza ciclos rápidos de construir-medir-aprender para reduzir incerteza e desperdício.

### Conceitos-chave

#### Build-Measure-Learn Loop

```
       ┌─────────────┐
       │    IDEA     │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │    BUILD    │ ← Construir o mínimo para testar
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │   MEASURE   │ ← Coletar dados reais
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │    LEARN    │ ← Validar ou pivotar
       └──────┬──────┘
              │
              ▼
         Próximo ciclo
```

#### MVP (Minimum Viable Product)

Versão mais simples do produto que permite validar hipóteses com usuários reais.

**Não é:**
- Produto mal feito
- Versão beta bugada
- Funcionalidade incompleta

**É:**
- Experimento deliberado
- Mínimo necessário para aprender
- Focado em validar uma hipótese específica

#### Pivot vs Persevere

Após cada ciclo de aprendizado:
- **Persevere** — Hipótese validada, continuar no caminho
- **Pivot** — Hipótese invalidada, mudar direção estratégica

### Tipos de MVP

| Tipo | Descrição | Quando usar |
|------|-----------|-------------|
| **Landing Page** | Página simples com proposta de valor | Validar interesse inicial |
| **Concierge** | Serviço manual fingindo ser produto | Validar se a solução resolve o problema |
| **Wizard of Oz** | Interface real com backend manual | Validar UX antes de automatizar |
| **Smoke Test** | Botão de compra sem produto | Validar intenção de pagamento |
| **Prototype** | Mockup interativo | Validar usabilidade |
| **Single Feature** | Uma funcionalidade completa | Validar valor de uma feature específica |

### Métricas de Validação

**Métricas de Vaidade (evitar):**
- Número de visitantes
- Downloads totais
- Usuários cadastrados

**Métricas Acionáveis (preferir):**
- Taxa de conversão
- Retenção (D1, D7, D30)
- Net Promoter Score (NPS)
- Receita por usuário

### Referências

- Livro: "The Lean Startup" — Eric Ries
- Livro: "Running Lean" — Ash Maurya
- Livro: "The Mom Test" — Rob Fitzpatrick

---

## Combinando os Frameworks

Na prática, usamos Assumption Mapping para **identificar e priorizar** hipóteses, e Lean Startup para **desenhar experimentos** que as validem.

### Fluxo Integrado

```
1. DESCOBERTA (Assumption Mapping)
   │
   ├── Listar todas as hipóteses
   ├── Categorizar (Desirability, Feasibility, Viability)
   └── Priorizar na matriz impacto x certeza
   
2. VALIDAÇÃO (Lean Startup)
   │
   ├── Escolher hipóteses críticas
   ├── Desenhar MVP ou experimento mínimo
   ├── Executar e medir
   └── Aprender e decidir (pivot ou persevere)
   
3. ITERAÇÃO
   │
   └── Repetir para próximas hipóteses
```

### Perguntas-guia

| Fase | Pergunta |
|------|----------|
| Antes de listar | "O que estamos assumindo que é verdade?" |
| Ao priorizar | "Se isso estiver errado, o que acontece?" |
| Ao validar | "Qual é o experimento mais barato que nos dá a resposta?" |
| Ao aprender | "O que essa evidência nos diz? Precisamos mudar algo?" |
