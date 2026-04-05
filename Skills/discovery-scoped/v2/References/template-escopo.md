# Template: escopo.md

Use este template para gerar o documento de escopo.

Salve em: `docs/{nome-do-projeto}/escopo/{titulo-kebab-case}/escopo.md`

---

## Template

```markdown
# {Título do Escopo}

**Situação:** Rascunho
**Data de criação:** {DD/MM/YYYY}
**Última atualização:** {DD/MM/YYYY}
**Projeto:** {Nome do Projeto}
**Repositório:** {URL do repositório ou "a definir"}

---

## Resumo Executivo

{2-3 frases resumindo o que este escopo entrega e por que é importante}

---

## Contexto

{Resumo do problema e motivação para este escopo, extraído do vision.md}

### Situação Atual

{Descreva como funciona hoje — o "antes"}

### Situação Desejada

{Descreva como deve funcionar — o "depois"}

---

## Abrangência

> O que este escopo cobre e o que está explicitamente fora.

### Inclui (In Scope)

- {item 1}
- {item 2}
- {item 3}

### Não Inclui (Out of Scope)

- {item 1 — por que está fora}
- {item 2 — por que está fora}

### Fronteiras com Outros Escopos

| Escopo relacionado | O que ele cobre | Fronteira com este escopo |
|--------------------|-----------------|---------------------------|
| {nome} | {resumo} | {onde um termina e outro começa} |

---

## Usuários Afetados

{Perfis de usuário impactados por este escopo}

| Perfil | Quantidade estimada | Como é afetado | Nível de impacto |
|--------|---------------------|----------------|------------------|
| {perfil} | {número ou faixa} | {descrição} | Alto/Médio/Baixo |

---

## Oportunidades Endereçadas

{Dores e jobs to be done que este escopo resolve, extraído de opportunity.md}

| # | Oportunidade | Prioridade original | Como este escopo endereça |
|---|--------------|---------------------|---------------------------|
| 1 | {oportunidade} | A/B/C | {como resolve} |
| 2 | {oportunidade} | A/B/C | {como resolve} |

### Oportunidades NÃO Endereçadas

{Oportunidades do discovery que ficaram de fora deste escopo}

| Oportunidade | Por que ficou de fora | Quando será endereçada |
|--------------|----------------------|------------------------|
| {oportunidade} | {motivo} | {escopo futuro ou "a definir"} |

---

## Funcionalidades e Comportamentos Esperados

{Descrição do que o sistema deve fazer dentro deste escopo}

### {Agrupamento 1 — ex: Cadastro de Usuários}

| # | Funcionalidade | Descrição | Critério de Aceite | Prioridade |
|---|----------------|-----------|-------------------|------------|
| F1.1 | {nome} | {o que faz} | {como saber se está pronto} | Must/Should/Could |
| F1.2 | {nome} | {o que faz} | {critério} | {prioridade} |

### {Agrupamento 2 — ex: Fluxo de Aprovação}

| # | Funcionalidade | Descrição | Critério de Aceite | Prioridade |
|---|----------------|-----------|-------------------|------------|
| F2.1 | {nome} | {o que faz} | {critério} | {prioridade} |

### Legenda de Prioridade (MoSCoW)

- **Must:** Obrigatório para o lançamento
- **Should:** Importante, mas pode ser ajustado
- **Could:** Desejável se houver tempo
- **Won't (this time):** Não será feito neste escopo

---

## Requisitos Não-Funcionais

| Categoria | Requisito | Meta | Como medir |
|-----------|-----------|------|------------|
| Performance | {ex: tempo de resposta} | {ex: < 2s} | {ferramenta/método} |
| Disponibilidade | {ex: uptime} | {ex: 99.5%} | {ferramenta/método} |
| Segurança | {ex: autenticação} | {ex: OAuth 2.0} | {critério} |
| Escalabilidade | {ex: usuários simultâneos} | {ex: 1000} | {teste de carga} |

---

## Hipóteses Críticas Associadas

{Hipóteses de alto impacto relacionadas a este escopo, extraídas de assumptions.md}

| # | Hipótese | Impacto se falsa | Situação | Plano de validação |
|---|----------|------------------|----------|-------------------|
| H1 | {hipótese} | {impacto} | Validada/A validar/Invalidada | {como validar} |
| H2 | {hipótese} | {impacto} | {situação} | {plano} |

### Hipóteses Aceitas como Premissa

{Hipóteses que foram aceitas sem validação formal}

- {premissa 1}
- {premissa 2}

---

## Stakeholders Envolvidos

| Stakeholder | Papel no escopo | Interesse | Influência | Precisa aprovar? |
|-------------|-----------------|-----------|------------|------------------|
| {nome} | {papel} | Alto/Médio/Baixo | Alta/Média/Baixa | Sim/Não |

### Matriz de Aprovação

| Decisão | Quem aprova | Quem é consultado | Quem é informado |
|---------|-------------|-------------------|------------------|
| Escopo geral | {nomes} | {nomes} | {nomes} |
| Mudanças de prazo | {nomes} | {nomes} | {nomes} |
| Mudanças de funcionalidade | {nomes} | {nomes} | {nomes} |

---

## Métricas de Sucesso

{Indicadores que definem o sucesso deste escopo}

### North Star deste Escopo

| Métrica | Baseline | Meta | Prazo |
|---------|----------|------|-------|
| {métrica principal} | {valor atual} | {meta} | {prazo} |

### Métricas de Suporte

| Categoria | Métrica | Baseline | Meta | Prazo |
|-----------|---------|----------|------|-------|
| Negócio | {métrica} | {valor} | {meta} | {prazo} |
| Usuário | {métrica} | {valor} | {meta} | {prazo} |
| Técnica | {métrica} | {valor} | {meta} | {prazo} |

### Critérios de Lançamento (Go/No-Go)

- [ ] {critério 1}
- [ ] {critério 2}
- [ ] {critério 3}

---

## Riscos do Escopo

| # | Risco | Probabilidade | Impacto | Mitigação | Responsável |
|---|-------|---------------|---------|-----------|-------------|
| R1 | {descrição} | Alta/Média/Baixa | Alto/Médio/Baixo | {plano} | {nome} |
| R2 | {descrição} | {prob} | {impacto} | {plano} | {nome} |

---

## Restrições e Dependências

### Restrições

| Tipo | Restrição | Impacto no escopo |
|------|-----------|-------------------|
| Prazo | {ex: entregar até data X} | {como afeta} |
| Orçamento | {ex: limite de R$X} | {como afeta} |
| Tecnologia | {ex: usar sistema Y} | {como afeta} |
| Regulatório | {ex: LGPD} | {como afeta} |

### Dependências

| Dependência | Tipo | Status | Responsável | Impacto se atrasar |
|-------------|------|--------|-------------|-------------------|
| {descrição} | Técnica/Organizacional/Externa | Resolvida/Pendente | {nome} | {impacto} |

---

## Decisões Pendentes

| # | Decisão | Opções | Quem decide | Prazo | Impacto de não decidir |
|---|---------|--------|-------------|-------|------------------------|
| D1 | {descrição} | {opção A, B, C} | {nome} | {data} | {impacto} |

---

## Premissas do Escopo

> Condições assumidas como verdadeiras para este escopo funcionar.

- {premissa 1}
- {premissa 2}
- {premissa 3}

---

## Estimativa de Esforço (Alto Nível)

| Fase | Esforço estimado | Confiança |
|------|------------------|-----------|
| Especificação | {dias/semanas} | Alta/Média/Baixa |
| Desenvolvimento | {dias/semanas} | Alta/Média/Baixa |
| Testes | {dias/semanas} | Alta/Média/Baixa |
| Homologação | {dias/semanas} | Alta/Média/Baixa |
| **Total** | **{total}** | **{confiança geral}** |

*Nota: Estimativas de alto nível. Detalhamento será feito na fase de planejamento.*

---

## Escopos Relacionados

| Escopo | Situação | Relação com este escopo |
|--------|----------|------------------------|
| [{título}](../{pasta}/escopo.md) | {situação} | {como se relaciona} |

---

## Histórico de Situação

| Data | Situação | Responsável | Observação |
|------|----------|-------------|------------|
| {DD/MM/YYYY} | Rascunho | {nome} | Criação inicial |

---

## Anexos e Referências

- [Discovery - Vision](./discovery/vision.md)
- [Discovery - Opportunity](./discovery/opportunity.md)
- [Discovery - Assumptions](./discovery/assumptions.md)
- [Discovery - Stakeholders](./discovery/stakeholders.md)
- [Discovery - Metrics](./discovery/success-metrics.md)
```

---

## Instruções de Uso

### Seções Obrigatórias

- Resumo Executivo
- Contexto
- Abrangência (Inclui / Não Inclui)
- Funcionalidades e Comportamentos
- Stakeholders com aprovadores
- Métricas de Sucesso
- Histórico de Situação

### Seções Opcionais (preencher quando relevante)

- Requisitos Não-Funcionais
- Riscos do Escopo
- Decisões Pendentes
- Estimativa de Esforço
- Escopos Relacionados

### Convenção de códigos

- **F** = Funcionalidade (F1.1, F1.2, F2.1...)
- **H** = Hipótese (H1, H2...)
- **R** = Risco (R1, R2...)
- **D** = Decisão pendente (D1, D2...)

### Estados válidos para Situação

1. **Rascunho** — Em elaboração
2. **Em revisão** — Aguardando feedback/aprovação
3. **Aprovado** — Pronto para execução
4. **Em execução** — Desenvolvimento em andamento
5. **Concluído** — Entregue e validado

### Quando atualizar

- Mudança de situação
- Adição/remoção de funcionalidades
- Mudança de prazo ou escopo
- Resolução de decisões pendentes
- Validação de hipóteses
