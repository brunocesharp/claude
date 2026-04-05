# Gestão de Situação do Escopo

Este documento detalha o fluxo de estados do escopo e os critérios para transição entre eles.

---

## Estados do Escopo

```
┌─────────────┐
│  RASCUNHO   │
└──────┬──────┘
       │ Revisão solicitada
       ▼
┌─────────────┐
│ EM REVISÃO  │◄────────────┐
└──────┬──────┘             │
       │ Aprovado           │ Ajustes necessários
       ▼                    │
┌─────────────┐             │
│  APROVADO   │─────────────┘
└──────┬──────┘
       │ Desenvolvimento iniciado
       ▼
┌─────────────┐
│ EM EXECUÇÃO │
└──────┬──────┘
       │ Entregue e validado
       ▼
┌─────────────┐
│  CONCLUÍDO  │
└─────────────┘
```

---

## Detalhamento dos Estados

### Rascunho

**Definição:** Escopo em elaboração inicial, ainda não pronto para revisão.

**Quem pode estar neste estado:**
- Escopos recém-criados
- Escopos que precisam de revisão significativa

**Ações permitidas:**
- Editar qualquer seção
- Adicionar/remover funcionalidades
- Mudar abrangência

**Critérios para sair:**
- Todas as seções obrigatórias preenchidas
- Pelo menos 1 revisor identificado
- Funcionalidades conectadas a oportunidades

---

### Em Revisão

**Definição:** Escopo completo aguardando feedback e aprovação formal.

**Quem pode estar neste estado:**
- Escopos que passaram pela elaboração inicial
- Escopos que voltaram de "Aprovado" para ajustes

**Ações permitidas:**
- Ajustes baseados em feedback
- Resolução de pendências
- Negociação de escopo

**Critérios para sair (→ Aprovado):**
- Todos os stakeholders com "Precisa aprovar? Sim" aprovaram
- Decisões pendentes críticas resolvidas
- Hipóteses críticas validadas ou aceitas como premissa

**Critérios para voltar (→ Rascunho):**
- Mudanças significativas necessárias
- Descoberta de novas informações que mudam o escopo

---

### Aprovado

**Definição:** Escopo formalmente aprovado, pronto para desenvolvimento.

**Quem pode estar neste estado:**
- Escopos que passaram pela revisão com sucesso
- Escopos aguardando início de desenvolvimento

**Ações permitidas:**
- Pequenos ajustes (com registro)
- Atualização de datas
- Refinamento de estimativas

**Ações que requerem nova aprovação:**
- Mudança de funcionalidades Must/Should
- Mudança de prazo > 20%
- Mudança de orçamento > 15%

**Critérios para sair (→ Em Execução):**
- Equipe alocada
- Sprint/ciclo de desenvolvimento iniciado

---

### Em Execução

**Definição:** Desenvolvimento em andamento.

**Quem pode estar neste estado:**
- Escopos em desenvolvimento ativo

**Ações permitidas:**
- Atualizações de progresso
- Ajustes de prioridade dentro do MoSCoW
- Detalhamento de funcionalidades

**Critérios para sair (→ Concluído):**
- Todas as funcionalidades Must entregues
- Critérios de lançamento (Go/No-Go) atingidos
- Validação dos stakeholders

**Critérios para voltar (→ Em Revisão):**
- Mudança significativa de escopo descoberta
- Hipótese crítica invalidada

---

### Concluído

**Definição:** Escopo entregue e validado em produção.

**Quem pode estar neste estado:**
- Escopos que passaram por todas as validações
- Funcionalidades em produção e estáveis

**Ações permitidas:**
- Registro de aprendizados
- Atualização de métricas reais
- Documentação de desvios

**Este é um estado terminal** — não há transição para outros estados.

---

## Fluxo de Aprovação

### Preparação para Revisão

Antes de mudar para "Em Revisão":

- [ ] Seções obrigatórias completas
- [ ] Funcionalidades com critérios de aceite
- [ ] Stakeholders identificados
- [ ] Métricas com baseline e meta
- [ ] Riscos mapeados

### Processo de Revisão

1. **Comunicar revisores:**
   - Notifique stakeholders com "Precisa aprovar? Sim"
   - Defina prazo para feedback (sugestão: 3-5 dias úteis)

2. **Coletar feedback:**
   - Agende reunião de revisão ou
   - Solicite comentários assíncronos

3. **Consolidar feedback:**
   - Agrupe por tema
   - Identifique conflitos
   - Priorize resoluções

4. **Ajustar escopo:**
   - Incorpore feedback aceito
   - Documente feedback rejeitado com justificativa
   - Atualize histórico

5. **Obter aprovação formal:**
   - Confirmação por escrito (email, Slack, assinatura)
   - Registro no histórico de situação

### Critérios de Aprovação

| Critério | Obrigatório? | Como verificar |
|----------|--------------|----------------|
| Aprovação do patrocinador | Sim | Confirmação por escrito |
| Aprovação técnica | Sim | Tech Lead assinou |
| Aprovação de produto | Sim | PM/PO assinou |
| Hipóteses críticas resolvidas | Sim | Todas validadas ou aceitas |
| Decisões pendentes resolvidas | Não* | Críticas resolvidas |
| Riscos mitigados | Não* | Planos documentados |

*Não bloqueiam, mas devem ter plano de resolução.

---

## Gestão de Mudanças

### Mudanças Durante "Em Revisão"

**Permitidas sem re-aprovação:**
- Ajustes de texto e clarificação
- Adição de detalhes em funcionalidades
- Correção de erros

**Requerem re-aprovação:**
- Adição/remoção de funcionalidades
- Mudança de prioridade Must ↔ Should
- Mudança de prazo/orçamento

### Mudanças Durante "Aprovado" ou "Em Execução"

Use o processo de Change Request:

```markdown
## Change Request #{número}

**Data:** {DD/MM/YYYY}
**Solicitante:** {nome}

### Mudança Proposta
{descrição da mudança}

### Justificativa
{por que é necessária}

### Impacto
- Prazo: {impacto}
- Orçamento: {impacto}
- Escopo: {impacto}

### Aprovadores
- [ ] {nome} — {papel}
- [ ] {nome} — {papel}

### Decisão
{aprovado/rejeitado} em {data} por {quem}
```

---

## Registro no Histórico

### Formato de Entrada

```markdown
| {DD/MM/YYYY} | {Estado} | {Responsável} | {Observação} |
```

### Exemplos

```markdown
| 15/01/2025 | Rascunho | João Silva | Criação inicial |
| 18/01/2025 | Em revisão | João Silva | Enviado para aprovação |
| 20/01/2025 | Em revisão | Maria Santos | Feedback: ajustar métricas |
| 22/01/2025 | Aprovado | Pedro Costa | Aprovado com ressalvas |
| 25/01/2025 | Em execução | João Silva | Sprint 1 iniciada |
| 15/03/2025 | Concluído | João Silva | Entregue em produção |
```

---

## Papéis e Responsabilidades

| Papel | Responsabilidades |
|-------|-------------------|
| **Autor do escopo** | Criar, atualizar, solicitar revisão |
| **Revisor** | Fornecer feedback, apontar gaps |
| **Aprovador** | Dar aprovação formal |
| **Executor** | Implementar, reportar progresso |
| **Validador** | Confirmar entrega, aceitar conclusão |

---

## Métricas do Processo

### Tempo em cada estado (benchmark)

| Estado | Tempo típico | Alerta se exceder |
|--------|--------------|-------------------|
| Rascunho | 3-5 dias | 2 semanas |
| Em revisão | 3-7 dias | 2 semanas |
| Aprovado | 1-5 dias | 2 semanas |
| Em execução | Variável | Conforme cronograma |

### Indicadores de saúde

| Indicador | Bom | Atenção | Problema |
|-----------|-----|---------|----------|
| Ciclos de revisão | 1-2 | 3 | 4+ |
| Change Requests | 0-2 | 3-5 | 6+ |
| Retrabalho | <10% | 10-20% | >20% |
