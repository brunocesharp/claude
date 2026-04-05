# Template: assumptions.md

Use este template para gerar o documento de hipóteses e premissas.

Salve em: `docs/{nome-do-projeto}/discovery/assumptions.md`

---

## Template

```markdown
# Hipóteses e Premissas — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}
> Versão: 1.0
> Status: Em validação

---

## Resumo Executivo

**Total de hipóteses mapeadas:** {número}
**Hipóteses críticas (a validar):** {número}
**Próxima validação planejada:** {descrição ou "a definir"}

---

## Hipóteses sobre Usuários

> Suposições sobre quem vai usar, o que quer, e como se comporta.

| # | Hipótese | Se errada... | Evidência atual | Impacto | Certeza | Prioridade |
|---|----------|--------------|-----------------|---------|---------|------------|
| U1 | {hipótese} | {consequência} | {evidências ou "nenhuma"} | Alto/Médio/Baixo | Alta/Média/Baixa | Crítica/Importante/Monitorar |
| U2 | {hipótese} | {consequência} | {evidências} | {impacto} | {certeza} | {prioridade} |
| U3 | {hipótese} | {consequência} | {evidências} | {impacto} | {certeza} | {prioridade} |

### Conexão com Oportunidades

| Hipótese | Oportunidade relacionada (de opportunity.md) |
|----------|---------------------------------------------|
| U1 | {oportunidade} |
| U2 | {oportunidade} |

---

## Hipóteses sobre o Negócio

> Suposições sobre viabilidade, mercado, modelo de negócio e resultados esperados.

| # | Hipótese | Se errada... | Evidência atual | Impacto | Certeza | Prioridade |
|---|----------|--------------|-----------------|---------|---------|------------|
| N1 | {hipótese} | {consequência} | {evidências} | {impacto} | {certeza} | {prioridade} |
| N2 | {hipótese} | {consequência} | {evidências} | {impacto} | {certeza} | {prioridade} |

---

## Hipóteses Técnicas

> Suposições sobre tecnologia, integrações, performance e capacidade de execução.

| # | Hipótese | Se errada... | Evidência atual | Impacto | Certeza | Prioridade |
|---|----------|--------------|-----------------|---------|---------|------------|
| T1 | {hipótese} | {consequência} | {evidências} | {impacto} | {certeza} | {prioridade} |
| T2 | {hipótese} | {consequência} | {evidências} | {impacto} | {certeza} | {prioridade} |

---

## Hipóteses Críticas ⚠️

> Alto impacto + Baixa certeza — VALIDAR ANTES de continuar desenvolvimento.

### {Código}: {Título da Hipótese}

**Hipótese:** {descrição completa}

**Se estiver errada:** {consequência detalhada}

**Evidência atual:** {o que sabemos hoje}

**Como validar:**
- **Método:** {entrevistas / spike / PoC / survey / etc.}
- **Critério de sucesso:** {o que precisa acontecer para considerar validada}
- **Critério de falha:** {o que indica que a hipótese está errada}
- **Responsável:** {nome ou "a definir"}
- **Prazo:** {data ou "a definir"}

**Plano B (se falhar):** {o que fazemos se a hipótese for invalidada}

---

### {Código}: {Título da Hipótese}

**Hipótese:** {descrição completa}

**Se estiver errada:** {consequência detalhada}

**Evidência atual:** {o que sabemos hoje}

**Como validar:**
- **Método:** {método}
- **Critério de sucesso:** {critério}
- **Critério de falha:** {critério}
- **Responsável:** {nome}
- **Prazo:** {data}

**Plano B (se falhar):** {alternativa}

---

## Premissas Aceitas

> Hipóteses que a equipe decidiu aceitar como verdadeiras sem validação adicional.

| # | Premissa | Justificativa para aceitar |
|---|----------|---------------------------|
| P1 | {premissa} | {por que não precisa validar} |
| P2 | {premissa} | {justificativa} |

---

## Experimentos Planejados

> Validações em andamento ou próximas.

| # | Hipótese | Método | Critério de Sucesso | Responsável | Início | Fim Previsto | Status |
|---|----------|--------|---------------------|-------------|--------|--------------|--------|
| 1 | {código} | {método} | {critério} | {nome} | {data} | {data} | Planejado/Em andamento/Concluído |
| 2 | {código} | {método} | {critério} | {nome} | {data} | {data} | {status} |

---

## Histórico de Validações

> Registro de hipóteses já validadas ou invalidadas.

| Data | Hipótese | Resultado | Evidência | Decisão |
|------|----------|-----------|-----------|---------|
| {data} | {código} | Validada/Invalidada | {resumo da evidência} | {o que fizemos} |

---

## Próximos Passos

1. **Imediato:** {ação mais urgente}
2. **Esta semana:** {próximas validações}
3. **Este mês:** {planejamento de validações}

---

## Histórico de Versões

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | {data} | Versão inicial |
```

---

## Instruções de Uso

### Campos obrigatórios

- Pelo menos 1 hipótese de cada tipo (usuário, negócio, técnica)
- Classificação de impacto e certeza para todas
- Pelo menos 1 hipótese crítica detalhada

### Campos opcionais (preencher quando disponível)

- Conexão com oportunidades
- Experimentos planejados
- Histórico de validações
- Plano B para hipóteses críticas

### Convenção de códigos

- **U** = Usuário (U1, U2, U3...)
- **N** = Negócio (N1, N2, N3...)
- **T** = Técnica (T1, T2, T3...)
- **P** = Premissa aceita (P1, P2, P3...)

### Critérios de prioridade

| Impacto | Certeza | Prioridade |
|---------|---------|------------|
| Alto | Baixa | **Crítica** — validar antes de desenvolver |
| Alto | Média | **Importante** — validar em paralelo |
| Alto | Alta | Confirmar — documentar evidências |
| Médio | Baixa | **Importante** — validar quando possível |
| Médio | Média/Alta | Monitorar |
| Baixo | Qualquer | Monitorar ou ignorar |

### Atualização do documento

Este documento deve ser atualizado:
- Quando novas hipóteses forem identificadas
- Quando validações forem concluídas
- Quando premissas forem questionadas
- A cada sprint/ciclo de discovery
