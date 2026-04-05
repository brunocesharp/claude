# Template: stakeholders.md

Use este template para gerar o documento de mapeamento de stakeholders.

Salve em: `docs/{nome-do-projeto}/discovery/stakeholders.md`

---

## Template

```markdown
# Mapa de Stakeholders — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}
> Versão: 1.0
> Última revisão: {data}

---

## Resumo Executivo

**Total de stakeholders mapeados:** {número}
**Stakeholders críticos (engajar ativamente):** {número}
**Principais riscos de relacionamento:** {resumo breve}

---

## Visão Geral

### Matriz de Stakeholders

```
                    INTERESSE
                 Baixo     Alto
            ┌──────────┬──────────┐
    Alta    │ {nomes}  │ {nomes}  │
INFLUÊNCIA  ├──────────┼──────────┤
    Baixa   │ {nomes}  │ {nomes}  │
            └──────────┴──────────┘
```

### Mapa de Envolvidos

| # | Stakeholder | Papel | Interesse | Influência | Classificação |
|---|-------------|-------|-----------|------------|---------------|
| 1 | {nome/grupo} | {papel} | Alto/Médio/Baixo | Alta/Média/Baixa | Engajar/Satisfazer/Informar/Monitorar |
| 2 | {nome/grupo} | {papel} | {interesse} | {influência} | {classificação} |
| 3 | {nome/grupo} | {papel} | {interesse} | {influência} | {classificação} |

---

## Stakeholders Críticos ⚠️

> Alta influência — requerem atenção especial.

### {Nome do Stakeholder 1}

| Aspecto | Detalhe |
|---------|---------|
| **Papel** | {descrição do papel no projeto} |
| **Por que é crítico** | {pode vetar? controla orçamento? decide escopo?} |
| **O que espera do projeto** | {expectativas principais} |
| **Preocupações / riscos** | {possíveis resistências ou objeções} |
| **Como engajar** | {estratégia específica} |
| **Frequência de comunicação** | {diária / semanal / por marco} |
| **Canal preferido** | {reunião 1:1 / email / Slack / call} |
| **Responsável pelo relacionamento** | {nome do time} |

**Plano de ação:**
1. {ação específica com prazo}
2. {ação específica com prazo}

---

### {Nome do Stakeholder 2}

| Aspecto | Detalhe |
|---------|---------|
| **Papel** | {descrição} |
| **Por que é crítico** | {motivo} |
| **O que espera do projeto** | {expectativas} |
| **Preocupações / riscos** | {resistências} |
| **Como engajar** | {estratégia} |
| **Frequência de comunicação** | {frequência} |
| **Canal preferido** | {canal} |
| **Responsável pelo relacionamento** | {nome} |

**Plano de ação:**
1. {ação}
2. {ação}

---

## Stakeholders a Manter Satisfeitos

> Alta influência + Baixo interesse — não incomodar, mas manter informados.

| Stakeholder | Papel | Expectativa | Canal | Frequência | Responsável |
|-------------|-------|-------------|-------|------------|-------------|
| {nome} | {papel} | {o que quer saber} | {canal} | {freq} | {responsável} |

---

## Stakeholders a Manter Informados

> Alto interesse + Baixa influência — comunicação regular, coleta de feedback.

| Stakeholder | Papel | O que acompanha | Canal | Frequência | Responsável |
|-------------|-------|-----------------|-------|------------|-------------|
| {nome} | {papel} | {interesse específico} | {canal} | {freq} | {responsável} |

---

## Stakeholders a Monitorar

> Baixa influência + Baixo interesse — atenção mínima, verificar periodicamente.

| Stakeholder | Papel | Quando revisar | Condição para reclassificar |
|-------------|-------|----------------|----------------------------|
| {nome} | {papel} | {data/evento} | {o que faria mudar de quadrante} |

---

## Rede de Influência

> Quem influencia quem — útil para estratégias indiretas.

```
{Representação visual ou descrição das relações}

Exemplo:
CEO
 ├── influencia → Diretor de TI
 │                 └── influencia → Gerente de Desenvolvimento
 └── influencia → Diretor Comercial
                   └── influencia → Equipe de Vendas (usuários)
```

### Relacionamentos-chave

| De | Para | Tipo de influência | Como usar |
|----|------|-------------------|-----------|
| {stakeholder A} | {stakeholder B} | {hierárquica/técnica/política} | {estratégia} |

---

## Tensões e Conflitos

> Conflitos de interesse entre stakeholders que precisam ser gerenciados.

### Conflito 1: {Título}

| Aspecto | Detalhe |
|---------|---------|
| **Entre quem** | {stakeholder A} vs {stakeholder B} |
| **Sobre o quê** | {motivo do conflito} |
| **Impacto no projeto** | {como afeta se não resolver} |
| **Estratégia de mitigação** | {como vamos lidar} |
| **Responsável** | {quem vai mediar} |

---

## Matriz de Comunicação

| Stakeholder | Classificação | Canal | Frequência | Conteúdo | Responsável |
|-------------|---------------|-------|------------|----------|-------------|
| {nome} | Engajar | 1:1 | Semanal | Status detalhado + decisões | {nome} |
| {nome} | Satisfazer | Email | Quinzenal | Resumo executivo | {nome} |
| {nome} | Informar | Newsletter | Por sprint | Updates gerais | {nome} |
| {nome} | Monitorar | Newsletter | Mensal | Highlights | {nome} |

---

## Plano de Ação Imediato

> Próximos passos para estabelecer relacionamentos.

| # | Ação | Stakeholder | Responsável | Prazo | Status |
|---|------|-------------|-------------|-------|--------|
| 1 | {ação} | {stakeholder} | {nome} | {data} | Pendente |
| 2 | {ação} | {stakeholder} | {nome} | {data} | Pendente |
| 3 | {ação} | {stakeholder} | {nome} | {data} | Pendente |

---

## Stakeholders Não Mapeados / A Investigar

> Pessoas ou áreas que podem ser relevantes mas ainda não foram mapeadas.

| Potencial Stakeholder | Por que pode ser relevante | Como investigar |
|-----------------------|---------------------------|-----------------|
| {nome/área} | {motivo} | {próximo passo} |

---

## Histórico de Revisões

| Versão | Data | Alteração | Autor |
|--------|------|-----------|-------|
| 1.0 | {data} | Versão inicial | {nome} |
```

---

## Instruções de Uso

### Campos obrigatórios

- Mapa de envolvidos com classificação
- Pelo menos 1 stakeholder crítico detalhado
- Matriz de comunicação básica

### Campos opcionais (preencher quando relevante)

- Rede de influência (útil em organizações políticas)
- Tensões e conflitos (se houver)
- Plano de ação imediato
- Stakeholders a investigar

### Convenção de classificação

| Classificação | Critério |
|---------------|----------|
| **Engajar** | Alta influência + Alto interesse |
| **Satisfazer** | Alta influência + Baixo interesse |
| **Informar** | Baixa influência + Alto interesse |
| **Monitorar** | Baixa influência + Baixo interesse |

### Quando atualizar

- A cada fase do projeto
- Quando houver mudança organizacional
- Quando novos stakeholders forem descobertos
- Quando classificações mudarem
- Após conflitos ou crises

### Boas práticas

- Use linguagem neutra e profissional
- Não registre opiniões pessoais negativas
- Foque em comportamentos e expectativas, não em julgamentos
- Mantenha confidencial se contiver informações sensíveis
- Revise com a equipe antes de compartilhar amplamente
