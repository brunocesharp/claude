# Checklist de Qualidade do Escopo

Use este checklist para validar a qualidade do escopo antes de mudar a situação para "Em Revisão".

---

## Checklist Completo

### 1. Estrutura e Completude

#### Seções Obrigatórias
- [ ] Título claro e descritivo
- [ ] Situação definida (Rascunho)
- [ ] Data de criação
- [ ] Projeto e repositório identificados
- [ ] Resumo executivo (2-3 frases)
- [ ] Contexto com situação atual e desejada
- [ ] Abrangência com "Inclui" e "Não inclui"
- [ ] Funcionalidades com critérios de aceite
- [ ] Stakeholders com aprovadores identificados
- [ ] Métricas com baseline e meta
- [ ] Histórico de situação iniciado

#### Seções Recomendadas
- [ ] Usuários afetados com estimativa de quantidade
- [ ] Oportunidades endereçadas (conectadas ao discovery)
- [ ] Hipóteses críticas com plano de validação
- [ ] Riscos com mitigação
- [ ] Restrições e dependências
- [ ] Decisões pendentes (se houver)
- [ ] Estimativa de esforço

---

### 2. Qualidade do Conteúdo

#### Contexto
- [ ] O problema está claramente descrito
- [ ] A motivação para o escopo está explícita
- [ ] "Antes" e "depois" estão distinguíveis
- [ ] Conecta-se com o vision.md do discovery

#### Abrangência
- [ ] "Inclui" lista itens específicos, não genéricos
- [ ] "Não inclui" explica por que cada item está fora
- [ ] Fronteiras com outros escopos estão claras
- [ ] Não há ambiguidade sobre o que entra ou não

#### Funcionalidades
- [ ] Cada funcionalidade tem descrição clara
- [ ] Critérios de aceite são verificáveis (sim/não)
- [ ] Prioridades MoSCoW estão definidas
- [ ] Funcionalidades estão agrupadas logicamente
- [ ] Funcionalidades Must são realmente essenciais
- [ ] Cada funcionalidade conecta-se a uma oportunidade

#### Métricas
- [ ] North Star do escopo está definida
- [ ] Baseline existe ou tem plano para medir
- [ ] Metas são específicas e com prazo
- [ ] Critérios de lançamento (Go/No-Go) estão listados
- [ ] Métricas são mensuráveis, não vagas

#### Stakeholders
- [ ] Todos os aprovadores estão identificados
- [ ] Papéis estão claros
- [ ] Matriz de aprovação está definida
- [ ] Ninguém crítico foi esquecido

---

### 3. Consistência e Rastreabilidade

#### Com o Discovery
- [ ] Funcionalidades derivam de oportunidades
- [ ] Hipóteses críticas estão contempladas
- [ ] Métricas alinham com success-metrics.md
- [ ] Stakeholders alinham com stakeholders.md
- [ ] Contexto alinha com vision.md

#### Interna
- [ ] Título da pasta = título do documento
- [ ] Códigos são consistentes (F1.1, F1.2...)
- [ ] Referências cruzadas funcionam
- [ ] Não há contradições entre seções

#### Com Outros Escopos
- [ ] Não repete funcionalidades de escopos aprovados
- [ ] Sobreposições com escopos em rascunho estão sinalizadas
- [ ] Escopos relacionados estão listados

---

### 4. Viabilidade e Realismo

#### Técnica
- [ ] Restrições técnicas estão identificadas
- [ ] Dependências técnicas estão mapeadas
- [ ] Requisitos não-funcionais são atingíveis
- [ ] Não há "mágica" assumida

#### Organizacional
- [ ] Prazo é realista para o escopo
- [ ] Recursos necessários estão identificados
- [ ] Dependências organizacionais mapeadas
- [ ] Capacidade da equipe foi considerada

#### Negócio
- [ ] ROI faz sentido (se aplicável)
- [ ] Métricas de negócio são atingíveis
- [ ] Stakeholders de negócio validaram

---

### 5. Riscos e Pendências

#### Riscos
- [ ] Riscos principais estão identificados
- [ ] Cada risco tem probabilidade e impacto
- [ ] Planos de mitigação existem
- [ ] Responsáveis por riscos definidos

#### Hipóteses
- [ ] Hipóteses críticas não estão ignoradas
- [ ] Hipóteses "a validar" têm plano
- [ ] Hipóteses invalidadas foram tratadas

#### Decisões
- [ ] Decisões pendentes estão listadas
- [ ] Decisões críticas têm prazo
- [ ] Responsáveis por decidir estão definidos
- [ ] Impacto de não decidir está claro

---

## Checklist Rápido (Versão Resumida)

Use quando precisar de validação rápida:

### Essencial (deve ter tudo)
- [ ] Título, projeto, data
- [ ] Contexto claro
- [ ] Abrangência definida
- [ ] Funcionalidades com critérios
- [ ] Aprovadores identificados
- [ ] Pelo menos 1 métrica com meta

### Importante (deveria ter)
- [ ] Conexão com discovery
- [ ] Priorização MoSCoW
- [ ] Riscos principais
- [ ] Dependências críticas

### Desejável (bom ter)
- [ ] Estimativa de esforço
- [ ] Requisitos não-funcionais
- [ ] Decisões pendentes
- [ ] Histórico completo

---

## Níveis de Qualidade

### Nível A — Pronto para Aprovação
- 100% do checklist essencial ✓
- 80%+ do checklist importante ✓
- Discovery completo usado como base
- Sem contradições ou gaps críticos

### Nível B — Precisa de Ajustes
- 100% do checklist essencial ✓
- 50-80% do checklist importante
- Alguns gaps não-críticos
- Pode ir para revisão com ressalvas

### Nível C — Precisa de Trabalho
- <100% do checklist essencial
- Discovery incompleto
- Gaps críticos identificados
- Não deve ir para revisão ainda

---

## Problemas Comuns de Qualidade

| Problema | Como identificar | Como resolver |
|----------|------------------|---------------|
| Escopo vago | "Inclui" tem itens genéricos | Detalhar cada item |
| Funcionalidades sem critério | "Fazer X" sem "aceito quando" | Adicionar critérios verificáveis |
| Métricas vagas | "Melhorar Y" sem número | Definir baseline e meta |
| Aprovadores não definidos | Tabela de stakeholders incompleta | Confirmar com patrocinador |
| Desconexão com discovery | Funcionalidades "do nada" | Vincular a oportunidades |
| Escopo grande demais | Lista enorme de funcionalidades Must | Dividir em fases |

---

## Perguntas de Validação

Antes de finalizar, pergunte:

1. **Clareza:** Se eu der este documento para alguém que não participou, ela entende o que será feito?

2. **Verificabilidade:** Consigo verificar se cada funcionalidade está "pronta" ou "não pronta"?

3. **Rastreabilidade:** Consigo explicar por que cada funcionalidade existe (qual oportunidade resolve)?

4. **Viabilidade:** A equipe que vai executar diria que é possível no prazo?

5. **Completude:** Tem algo óbvio que deveria estar aqui e não está?

6. **Priorização:** Se cortar 30% do escopo, sei o que cortar primeiro?

7. **Sucesso:** Sei exatamente como vou medir se deu certo?
