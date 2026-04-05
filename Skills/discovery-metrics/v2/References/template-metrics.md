# Template: success-metrics.md

Use este template para gerar o documento de métricas de sucesso.

Salve em: `docs/{nome-do-projeto}/discovery/success-metrics.md`

---

## Template

```markdown
# Métricas de Sucesso — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}
> Versão: 1.0
> Próxima revisão: {data — sugestão: 3 meses após lançamento}

---

## Resumo Executivo

**Objetivo central:** {uma frase descrevendo o resultado esperado}

**North Star Metric:** {a métrica mais importante}

**Meta principal:** {baseline} → {meta} em {prazo}

---

## Objetivo Central

{Declaração clara do resultado esperado com o projeto — não funcionalidades, mas transformação}

### Conexão com Discovery

| Documento | Como as métricas se conectam |
|-----------|------------------------------|
| Vision | {qual transformação da visão estamos medindo} |
| Opportunities | {quais oportunidades estamos validando} |
| Assumptions | {quais hipóteses as métricas vão validar} |

---

## North Star Metric

> A métrica mais importante — aquela que melhor representa o valor entregue.

| Aspecto | Detalhe |
|---------|---------|
| **Métrica** | {nome da métrica} |
| **Definição** | {como é calculada exatamente} |
| **Por que é a North Star** | {por que essa métrica captura o valor central} |
| **Baseline** | {valor atual ou "a medir"} |
| **Meta 3 meses** | {meta} |
| **Meta 6 meses** | {meta} |
| **Responsável** | {quem acompanha} |
| **Fonte de dados** | {de onde vem o dado} |
| **Frequência** | {diária / semanal / mensal} |

---

## Métricas de Negócio

| # | Métrica | Definição | Baseline | Meta 3m | Meta 6m | Responsável |
|---|---------|-----------|----------|---------|---------|-------------|
| N1 | {métrica} | {como calcula} | {atual} | {meta} | {meta} | {nome} |
| N2 | {métrica} | {como calcula} | {atual} | {meta} | {meta} | {nome} |
| N3 | {métrica} | {como calcula} | {atual} | {meta} | {meta} | {nome} |

### Detalhamento

#### N1: {Nome da Métrica}

- **O que indica:** {interpretação}
- **Como melhorar:** {alavancas principais}
- **Riscos de otimizar:** {o que pode piorar se focar só nisso}
- **Fonte:** {sistema/ferramenta}

---

## Métricas de Produto e Usuário

### Framework HEART

| Dimensão | Métrica | Baseline | Meta | Como medir |
|----------|---------|----------|------|------------|
| **Happiness** | {métrica} | {atual} | {meta} | {ferramenta/método} |
| **Engagement** | {métrica} | {atual} | {meta} | {ferramenta/método} |
| **Adoption** | {métrica} | {atual} | {meta} | {ferramenta/método} |
| **Retention** | {métrica} | {atual} | {meta} | {ferramenta/método} |
| **Task Success** | {métrica} | {atual} | {meta} | {ferramenta/método} |

### Detalhamento

#### Happiness: {Nome da Métrica}

- **O que indica:** {interpretação}
- **Como coletar:** {survey, feedback, análise de sentimento}
- **Frequência:** {quando medir}

---

## Anti-métricas ⚠️

> Métricas que NÃO devemos otimizar, pois podem prejudicar a experiência ou o negócio.

| Anti-métrica | Por que evitar | O que monitorar em vez |
|--------------|----------------|------------------------|
| {métrica} | {risco se otimizar} | {alternativa saudável} |
| {métrica} | {risco} | {alternativa} |

**Exemplo:**
| Anti-métrica | Por que evitar | Monitorar em vez |
|--------------|----------------|------------------|
| Tempo no app | Pode indicar dificuldade, não engajamento | Tarefas completadas |
| Cadastros | Não indica valor, só topo de funil | Ativação em 7 dias |

---

## Critérios de Aceitação do Lançamento

> O que precisa ser verdade no go-live para considerar o lançamento bem-sucedido.

### Funcionais

- [ ] {critério funcional 1}
- [ ] {critério funcional 2}
- [ ] {critério funcional 3}

### Não-funcionais

- [ ] Performance: {critério, ex: "tempo de resposta < 2s para 95% das requests"}
- [ ] Disponibilidade: {critério, ex: "uptime > 99.5%"}
- [ ] Segurança: {critério, ex: "aprovação do time de segurança"}

### De Adoção

- [ ] {critério de adoção, ex: "50 usuários ativos na primeira semana"}

---

## Critérios de Sucesso do Projeto (longo prazo)

> O que define sucesso depois de 6-12 meses em produção.

| Horizonte | Critério | Como saberemos |
|-----------|----------|----------------|
| 3 meses | {critério} | {evidência} |
| 6 meses | {critério} | {evidência} |
| 12 meses | {critério} | {evidência} |

---

## Plano de Instrumentação

> Como vamos coletar os dados para cada métrica.

| Métrica | Fonte de dados | Já existe? | Ação necessária | Responsável | Prazo |
|---------|----------------|------------|-----------------|-------------|-------|
| {métrica} | {sistema} | Sim/Não | {implementar tracking / criar query / etc} | {nome} | {data} |

### Ferramentas planejadas

- **Analytics de produto:** {ferramenta}
- **Surveys:** {ferramenta}
- **BI/Dashboard:** {ferramenta}
- **Logs/Observability:** {ferramenta}

---

## Riscos de Medição

> O que pode dificultar o acompanhamento das métricas.

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| {risco, ex: "sistema legado não tem logs"} | {impacto} | {plano} |
| {risco} | {impacto} | {plano} |

---

## Cadência de Revisão

| Frequência | O que revisar | Quem participa |
|------------|---------------|----------------|
| Semanal | North Star, métricas operacionais | Time de produto |
| Mensal | Todas as métricas, tendências | Time + stakeholders |
| Trimestral | Metas, relevância das métricas | Time + liderança |

---

## Dashboard

> Onde as métricas serão visualizadas.

**Ferramenta:** {ferramenta escolhida}
**Responsável pela manutenção:** {nome}
**Link:** {a definir após criação}

### Visões planejadas

1. **Executiva:** North Star + métricas de negócio
2. **Produto:** HEART completo + funis
3. **Operacional:** Métricas técnicas + incidentes

---

## Histórico de Versões

| Versão | Data | Alteração | Autor |
|--------|------|-----------|-------|
| 1.0 | {data} | Versão inicial | {nome} |
```

---

## Instruções de Uso

### Campos obrigatórios

- Objetivo central
- North Star Metric com definição clara
- Pelo menos 2-3 métricas de negócio
- Pelo menos 2-3 métricas de usuário (HEART)
- Critérios de aceitação do lançamento

### Campos opcionais (preencher quando relevante)

- Anti-métricas (recomendado)
- Plano de instrumentação
- Riscos de medição
- Dashboard

### Convenção de códigos

- **N** = Negócio (N1, N2, N3...)
- **U** = Usuário (U1, U2, U3...)
- **T** = Técnica (T1, T2, T3...)

### Quando atualizar

- A cada revisão trimestral de metas
- Quando baseline for estabelecido
- Quando métricas se mostrarem inadequadas
- Após mudanças significativas de escopo

### Boas práticas

- Mantenha entre 10-15 métricas no total
- Revise relevância das métricas trimestralmente
- Documente mudanças de definição
- Conecte com hipóteses do assumptions.md
