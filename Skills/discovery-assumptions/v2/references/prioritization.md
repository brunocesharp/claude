# Matriz de Priorização de Hipóteses

Este documento detalha como priorizar hipóteses usando a matriz impacto x certeza.

---

## A Matriz

```
                         CERTEZA ATUAL
                    Baixa              Alta
                ┌───────────────┬───────────────┐
                │               │               │
        Alto    │   VALIDAR     │   CONFIRMAR   │
                │   PRIMEIRO    │   E SEGUIR    │
   IMPACTO      │      ⚠️       │      ✓        │
   SE FALSA     │               │               │
                ├───────────────┼───────────────┤
                │               │               │
        Baixo   │   MONITORAR   │    IGNORAR    │
                │               │               │
                │      👁️       │      ✗        │
                │               │               │
                └───────────────┴───────────────┘
```

---

## Os Quadrantes

### ⚠️ VALIDAR PRIMEIRO (Alto Impacto + Baixa Certeza)

**O que significa:**
- Se essa hipótese estiver errada, o projeto falha ou perde muito valor
- Não temos evidências fortes de que é verdadeira
- É a maior fonte de risco do projeto

**O que fazer:**
- Parar tudo e validar ANTES de continuar desenvolvimento
- Desenhar experimento específico para testar
- Definir critério claro de sucesso/falha
- Timeboxar a validação (1-2 semanas no máximo)

**Exemplos:**
- "Usuários pagariam R$50/mês por isso" (sem pré-vendas feitas)
- "Conseguimos integrar com o sistema legado" (sem spike técnico)
- "O time de vendas vai adotar a ferramenta" (sem entrevistas com vendedores)

---

### ✓ CONFIRMAR E SEGUIR (Alto Impacto + Alta Certeza)

**O que significa:**
- Se essa hipótese estiver errada, o projeto falha
- MAS temos boas evidências de que é verdadeira
- É uma premissa forte do projeto

**O que fazer:**
- Documentar as evidências que sustentam a certeza
- Monitorar durante o desenvolvimento
- Ter plano B caso mude

**Exemplos:**
- "Clientes reclamam desse problema" (com 50 tickets de suporte documentados)
- "A API do parceiro funciona" (com integração já testada em outro projeto)
- "O mercado está crescendo" (com dados de pesquisa recentes)

---

### 👁️ MONITORAR (Baixo Impacto + Baixa Certeza)

**O que significa:**
- Não temos certeza, mas também não é crítico
- Se errar, o projeto continua mas pode ser afetado
- Vale ficar de olho, mas não bloqueia

**O que fazer:**
- Registrar a hipótese
- Revisar periodicamente
- Validar se houver oportunidade (ex: durante entrevistas para outra hipótese)

**Exemplos:**
- "Usuários preferem tema escuro" (afeta UX, não o core)
- "O pico de uso será às 9h" (afeta infra, pode ajustar depois)
- "Maioria dos usuários usa iPhone" (afeta priorização de plataforma)

---

### ✗ IGNORAR (Baixo Impacto + Alta Certeza)

**O que significa:**
- Sabemos que é verdade e não muda muito se não for
- Não vale investir tempo validando

**O que fazer:**
- Documentar como premissa aceita
- Seguir em frente

**Exemplos:**
- "Usuários têm acesso a internet" (para app web B2B)
- "O time sabe programar em Python" (linguagem já usada)
- "A empresa vai continuar existindo" (premissa básica)

---

## Como Classificar

### Passo 1: Avaliar Impacto

Pergunte: **"Se essa hipótese estiver ERRADA, o que acontece?"**

| Resposta | Impacto |
|----------|---------|
| "O projeto inteiro falha" | Alto |
| "Perdemos a maior parte do valor" | Alto |
| "Uma feature importante não funciona" | Médio→Alto |
| "Precisamos ajustar algumas coisas" | Médio |
| "Quase nada muda" | Baixo |
| "Só afeta detalhes" | Baixo |

### Passo 2: Avaliar Certeza

Pergunte: **"Que EVIDÊNCIA temos de que isso é verdade?"**

| Tipo de Evidência | Certeza |
|-------------------|---------|
| "Eu acho que..." | Baixa |
| "Todo mundo sabe que..." | Baixa (viés) |
| "Um stakeholder disse..." | Baixa-Média |
| "Vimos em 2-3 conversas informais" | Média |
| "Temos dados de pesquisa com N>30" | Alta |
| "Já fizemos isso antes com sucesso" | Alta |
| "Está funcionando em produção agora" | Alta |

### Passo 3: Plotar na Matriz

| Impacto | Certeza | Quadrante |
|---------|---------|-----------|
| Alto | Baixa | ⚠️ VALIDAR PRIMEIRO |
| Alto | Alta | ✓ CONFIRMAR E SEGUIR |
| Baixo | Baixa | 👁️ MONITORAR |
| Baixo | Alta | ✗ IGNORAR |

---

## Erros Comuns na Priorização

### Erro 1: Superestimar certeza

**Sintoma:** "Temos certeza porque faz sentido"

**Correção:** Certeza vem de EVIDÊNCIA, não de lógica. Pergunte: "Qual foi a última vez que vimos isso acontecer?"

---

### Erro 2: Subestimar impacto

**Sintoma:** "Se não funcionar, a gente ajusta"

**Correção:** Calcule o custo de estar errado. Pergunte: "Quanto tempo e dinheiro perdemos se isso estiver errado?"

---

### Erro 3: Priorizar por facilidade

**Sintoma:** "Vamos validar essa porque é fácil"

**Correção:** Priorize por RISCO (impacto x certeza), não por conveniência.

---

### Erro 4: Muitas hipóteses "críticas"

**Sintoma:** Tudo é alto impacto + baixa certeza

**Correção:** Force ranking relativo. Pergunte: "Se só pudéssemos validar UMA, qual seria?"

---

## Template de Classificação

Use esta tabela durante a priorização:

| # | Hipótese | Se errada... | Evidência que temos | Impacto | Certeza | Quadrante |
|---|----------|--------------|---------------------|---------|---------|-----------|
| 1 | {texto} | {consequência} | {evidências} | A/M/B | A/M/B | {quadrante} |
| 2 | {texto} | {consequência} | {evidências} | A/M/B | A/M/B | {quadrante} |

---

## Ordem de Ação

1. **Primeiro:** Hipóteses ⚠️ VALIDAR PRIMEIRO — bloquear desenvolvimento até resolver
2. **Depois:** Hipóteses ✓ CONFIRMAR — documentar evidências e seguir
3. **Paralelo:** Hipóteses 👁️ MONITORAR — validar quando houver oportunidade
4. **Ignorar:** Hipóteses ✗ — aceitar como premissa e não gastar tempo
